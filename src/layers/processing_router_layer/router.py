from src.schemas.pipeline import Chunk


def route_chunks(chunks: list[Chunk]) -> str:
    if not chunks:
        return "empty"

    avg_size = sum(len(c.content) for c in chunks) / len(chunks)
    if avg_size > 180:
        return "deep_processing"
    return "fast_processing"
