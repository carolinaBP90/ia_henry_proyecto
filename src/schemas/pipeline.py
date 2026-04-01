from typing import Any, Literal

from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    source_type: Literal["text", "url", "file"] = "text"
    source_value: str = Field(..., min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    chunk_id: str
    content: str
    chunk_type: Literal["plain_text", "web_text", "file_text"]


class StrategyDecision(BaseModel):
    strategy_name: str
    confidence: float
    reasoning: str


class ProcessResponse(BaseModel):
    request_id: str
    extracted_preview: str
    chunk_count: int
    route: str
    strategy: StrategyDecision
    output: dict[str, Any]
