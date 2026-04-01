from src.schemas.pipeline import Chunk


def ingest_text(raw_text: str, chunk_size: int = 300) -> list[Chunk]:
    text = " ".join(raw_text.split())
    chunks: list[Chunk] = []
    start = 0
    index = 1

    while start < len(text):
        piece = text[start : start + chunk_size]
        if not piece:
            break
        chunks.append(
            Chunk(
                chunk_id=f"chunk-{index}",
                content=piece,
                chunk_type="plain_text",
            )
        )
        start += chunk_size
        index += 1

    return chunks
