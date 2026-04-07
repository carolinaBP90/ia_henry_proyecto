"""Extraction agent for legal change detection and structured summarization."""

from __future__ import annotations

import json
from typing import Any

from src.services.openai_client import OpenAIClient


class ExtractionAgent:
    """Extracts legal changes and emits a strict JSON-compatible payload."""

    def __init__(self, llm_client: OpenAIClient) -> None:
        """Initialize agent with centralized LLM client dependency."""
        self._llm = llm_client

    def run(self, context_report: str, original_text: str, amendment_text: str) -> dict[str, Any]:
        """Generate candidate JSON payload for contract change output.

        Args:
            context_report: Output from contextualization agent.
            original_text: OCR text from original contract.
            amendment_text: OCR text from amendment contract.

        Returns:
            Dictionary expected to match ContractChangeOutput schema.

        Raises:
            ValueError: If the model output is not valid JSON.
        """
        system_prompt = (
            "You are a legal extraction agent specialized in contract amendments. "
            "Return valid JSON only, with no markdown and no additional keys."
        )

        user_prompt = (
            "Using the provided context report and source texts, identify legal changes\n"
            "and produce a JSON object with EXACTLY this schema:\n"
            "{\n"
            '  "sections_changed": ["string"],\n'
            '  "topics_touched": ["string"],\n'
            '  "summary_of_the_change": "string"\n'
            "}\n\n"
            "Rules:\n"
            "1. sections_changed: concrete section titles or clause ids affected.\n"
            "2. topics_touched: legal themes (e.g., payment terms, liabilities, termination).\n"
            "3. summary_of_the_change: professional legal summary, concise and factual.\n"
            "4. The summary MUST clearly distinguish additions, deletions and modifications.\n"
            "5. If uncertainty exists, mention it briefly in summary_of_the_change.\n"
            "6. Do not invent sections not present in source texts.\n\n"
            "CONTEXT REPORT:\n"
            f"{context_report}\n\n"
            "ORIGINAL TEXT:\n"
            f"{original_text}\n\n"
            "AMENDMENT TEXT:\n"
            f"{amendment_text}"
        )

        model_output = self._llm.invoke_text_task(system_prompt=system_prompt, user_prompt=user_prompt)
        try:
            return json.loads(model_output)
        except json.JSONDecodeError as exc:
            raise ValueError("ExtractionAgent returned non-JSON output") from exc
