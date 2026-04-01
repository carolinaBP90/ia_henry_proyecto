"""Contextualization agent for structural legal document analysis."""

from __future__ import annotations

from src.services.openai_client import OpenAIClient


class ContextualizationAgent:
    """Builds structural context between original contract and amendment."""

    def __init__(self, llm_client: OpenAIClient) -> None:
        """Initialize agent with centralized LLM client dependency."""
        self._llm = llm_client

    def run(self, original_text: str, amendment_text: str) -> str:
        """Analyze document structure and cross-document correspondence.

        Args:
            original_text: OCR text from original contract.
            amendment_text: OCR text from amendment document.

        Returns:
            Structured context string used by the extraction agent.
        """
        system_prompt = (
            "You are a senior legal document analyst. "
            "Produce rigorous structural context to enable downstream legal diff extraction. "
            "Be precise, avoid speculation, and mark uncertainty explicitly."
        )

        user_prompt = (
            "You will receive two legal texts: ORIGINAL and AMENDMENT.\n"
            "Your task is to produce a structured context report with these exact sections:\n"
            "1) DOCUMENT_MAP: normalized section hierarchy for both texts\n"
            "2) SECTION_ALIGNMENT: mapping between amended sections and original sections\n"
            "3) LEGAL_ENTITIES: parties, obligations, dates, amounts, penalties\n"
            "4) CROSS_REFERENCES: references affected by the amendment\n"
            "5) AMBIGUITIES: potential OCR or semantic ambiguities\n\n"
            "Output plain text only. Keep each section concise but complete.\n\n"
            "ORIGINAL:\n"
            f"{original_text}\n\n"
            "AMENDMENT:\n"
            f"{amendment_text}"
        )

        return self._llm.invoke_text_task(system_prompt=system_prompt, user_prompt=user_prompt)
