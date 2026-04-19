"""Centralized OpenAI access for all LLM interactions in the system."""

from __future__ import annotations

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import Settings, get_settings


LOGGER = logging.getLogger(__name__)


class OpenAIClientError(RuntimeError):
    """Raised when an OpenAI request fails after controlled retries."""


class OpenAIClient:
    """Centralized OpenAI client abstraction used by parser and agents.

    This class prevents direct OpenAI coupling inside business components and
    standardizes timeout/retry/error handling.
    """

    def __init__(self, settings: Settings, callbacks: list[Any] | None = None) -> None:
        """Initialize model clients for vision and text tasks.

        Args:
            settings: Runtime configuration.
            callbacks: Optional LangChain callbacks (e.g. Langfuse CallbackHandler)
                passed to every model invocation for automatic generation tracing.
        """
        self._settings = settings
        self._callbacks: list[Any] = callbacks or []
        self._last_call_metadata: dict[str, Any] = {}
        self._vision_model = ChatOpenAI(
            model=settings.openai_model_vision,
            api_key=settings.openai_api_key,
            temperature=0,
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self._text_model = ChatOpenAI(
            model=settings.openai_model_text,
            api_key=settings.openai_api_key,
            temperature=settings.openai_temperature,
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )

    def extract_text_from_image(self, image_base64: str, extraction_prompt: str) -> str:
        """Extract faithful OCR text from an image via GPT-4o Vision.

        Args:
            image_base64: Raw base64 image payload.
            extraction_prompt: OCR prompt with extraction constraints.

        Returns:
            The extracted document text.

        Raises:
            OpenAIClientError: When model execution fails.
        """
        config = {"callbacks": self._callbacks} if self._callbacks else {}
        try:
            response = self._vision_model.invoke(
                [
                    SystemMessage(
                        content=(
                            "You are a legal OCR assistant. Return only extracted text, "
                            "preserving line breaks and legal numbering."
                        )
                    ),
                    HumanMessage(
                        content=[
                            {"type": "text", "text": extraction_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                            },
                        ]
                    ),
                ],
                config=config,
            )
        except Exception as exc:  # noqa: BLE001
            raise OpenAIClientError("Vision extraction failed") from exc

        self._last_call_metadata = {
            "task": "vision_extraction",
            "model": self._settings.openai_model_vision,
            "usage": getattr(response, "usage_metadata", None),
            "response_metadata": getattr(response, "response_metadata", None),
        }

        text = str(response.content).strip()
        if not text:
            raise OpenAIClientError("Vision extraction returned empty content")
        return text

    def invoke_text_task(self, system_prompt: str, user_prompt: str) -> str:
        """Run a text-only task through LangChain prompt pipeline.

        Args:
            system_prompt: Role and behavior constraints.
            user_prompt: Concrete task payload.

        Returns:
            String model output.

        Raises:
            OpenAIClientError: If invocation fails.
        """
        config = {"callbacks": self._callbacks} if self._callbacks else {}
        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", user_prompt),
                ]
            )
            messages = prompt.format_messages()
            response = self._text_model.invoke(messages, config=config)
            output = StrOutputParser().invoke(response)
        except Exception as exc:  # noqa: BLE001
            raise OpenAIClientError("Text task failed") from exc

        self._last_call_metadata = {
            "task": "text_task",
            "model": self._settings.openai_model_text,
            "usage": getattr(response, "usage_metadata", None),
            "response_metadata": getattr(response, "response_metadata", None),
        }

        result = output.strip()
        if not result:
            raise OpenAIClientError("Text task returned empty content")
        return result

    def get_last_call_metadata(self) -> dict[str, Any]:
        """Return best-effort metadata for the latest model invocation."""
        return dict(self._last_call_metadata)

    def repair_json_payload(self, invalid_payload: str, validation_error: str) -> dict[str, Any]:
        """Repair a JSON payload to satisfy required output schema.

        Args:
            invalid_payload: Original non-valid JSON content.
            validation_error: Validator error string to guide correction.

        Returns:
            Repaired JSON dictionary.

        Raises:
            OpenAIClientError: If repaired output is still not valid JSON.
        """
        system_prompt = (
            "You are a strict JSON repair assistant. "
            "You MUST return valid JSON only, with no markdown fences."
        )
        user_prompt = (
            "Repair the following JSON so that it matches this schema exactly:\n"
            "{{\n"
            '  "sections_changed": ["string"],\n'
            '  "topics_touched": ["string"],\n'
            '  "summary_of_the_change": "string"\n'
            "}}\n\n"
            "Validation errors:\n"
            f"{validation_error}\n\n"
            "Invalid JSON:\n"
            f"{invalid_payload}"
        )

        repaired_text = self.invoke_text_task(system_prompt=system_prompt, user_prompt=user_prompt)
        try:
            return json.loads(repaired_text)
        except json.JSONDecodeError as exc:
            LOGGER.warning("JSON repair output was invalid JSON")
            raise OpenAIClientError("JSON repair did not return valid JSON") from exc


_OPENAI_CLIENT: OpenAIClient | None = None


def get_openai_client(callbacks: list[Any] | None = None) -> OpenAIClient:
    """Return an OpenAI client, optionally configured with LangChain callbacks.

    When callbacks are provided a fresh instance is returned (not cached) so
    each pipeline run gets its own Langfuse-scoped handler.
    When no callbacks are needed the cached singleton is reused.
    """
    global _OPENAI_CLIENT
    if callbacks:
        return OpenAIClient(settings=get_settings(), callbacks=callbacks)
    if _OPENAI_CLIENT is None:
        _OPENAI_CLIENT = OpenAIClient(settings=get_settings())
    return _OPENAI_CLIENT
