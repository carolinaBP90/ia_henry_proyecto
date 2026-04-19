"""Image parsing module that extracts legal text using GPT-4o Vision."""

from __future__ import annotations

import base64
from pathlib import Path

from src.services.openai_client import OpenAIClient, OpenAIClientError, get_openai_client


OCR_PROMPT = """
Extract the full legal text from this contract image with high fidelity.

Extraction rules:
1. Preserve section numbering, clause numbering, bullet hierarchy and line breaks.
2. Do not summarize, do not interpret, do not redact, do not translate.
3. Keep legal entities, dates, currency values and percentages exactly as shown.
4. If text is unreadable, insert [UNREADABLE:<short reason>] in place.
5. Output plain text only.
""".strip()


def validate_contract_image_path(path: str) -> Path:
    """Validate that an image path exists and contains bytes.

    Args:
        path: Filesystem path to image file.

    Returns:
        Normalized Path object.

    Raises:
        FileNotFoundError: If the image path does not exist.
        ValueError: If the file is empty.
    """
    image_path = Path(path)
    if not image_path.exists() or not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    image_bytes = image_path.read_bytes()
    if not image_bytes:
        raise ValueError(f"Image file is empty: {path}")
    return image_path


def encode_contract_image_to_base64(image_path: Path) -> str:
    """Encode a contract image to base64 for multimodal API calls."""
    image_bytes = image_path.read_bytes()
    return base64.b64encode(image_bytes).decode("utf-8")


def parse_contract_image(path: str, client: OpenAIClient | None = None) -> str:
    """Parse a legal contract image and return extracted OCR text.

    Args:
        path: Filesystem path to image file.
        client: Optional pre-configured OpenAIClient (e.g. with Langfuse callbacks).
            When omitted the module-level singleton is used.

    Returns:
        Extracted text from image.

    Raises:
        FileNotFoundError: If the image path does not exist.
        ValueError: If the file is empty.
        OpenAIClientError: If model extraction fails.
    """
    image_path = validate_contract_image_path(path)
    image_base64 = encode_contract_image_to_base64(image_path)
    active_client = client or get_openai_client()
    return active_client.extract_text_from_image(image_base64=image_base64, extraction_prompt=OCR_PROMPT)
