"""Pydantic models for contract-change structured output."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ContractChangeOutput(BaseModel):
    """Final validated output for legal contract change analysis."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    sections_changed: list[str] = Field(
        default_factory=list,
        description="Contract sections where legal modifications were identified.",
    )
    topics_touched: list[str] = Field(
        default_factory=list,
        description="High-level legal topics impacted by the amendment.",
    )
    summary_of_the_change: str = Field(
        ...,
        min_length=20,
        description="Professional and concise narrative summary of legal changes.",
    )

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def _normalize_string_lists(cls, values: list[str]) -> list[str]:
        """Normalize, de-duplicate and clean list values while preserving order."""
        normalized: list[str] = []
        for item in values:
            clean = item.strip()
            if clean and clean not in normalized:
                normalized.append(clean)
        return normalized
