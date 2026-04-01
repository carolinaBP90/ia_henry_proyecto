from uuid import uuid4

from src.layers.ai_strategy_layer.agents import decide_strategy
from src.layers.ingestion_layer.ingestor import ingest_text
from src.layers.input_layer.collector import collect
from src.layers.processing_router_layer.router import route_chunks
from src.schemas.pipeline import ProcessRequest, ProcessResponse
from src.storage.queue import broker
from src.storage.repositories import document_store, vector_store


def run_pipeline(payload: ProcessRequest) -> ProcessResponse:
    request_id = str(uuid4())

    raw_text = collect(payload.source_type, payload.source_value)
    chunks = ingest_text(raw_text)
    route = route_chunks(chunks)
    strategy = decide_strategy(route, raw_text)

    broker.publish(
        "ingestion_events",
        {
            "request_id": request_id,
            "source_type": payload.source_type,
            "route": route,
        },
    )

    document_store.save(
        {
            "request_id": request_id,
            "content": raw_text,
            "metadata": payload.metadata,
        }
    )

    for chunk in chunks:
        vector_store.upsert(
            {
                "request_id": request_id,
                "chunk_id": chunk.chunk_id,
                "embedding": [0.0, 0.1, 0.2],
                "content": chunk.content,
            }
        )

    output = {
        "next_action": "dispatch_agent",
        "agent": strategy.strategy_name,
        "queue": "agent_execution_queue",
    }

    return ProcessResponse(
        request_id=request_id,
        extracted_preview=raw_text[:120],
        chunk_count=len(chunks),
        route=route,
        strategy=strategy,
        output=output,
    )
