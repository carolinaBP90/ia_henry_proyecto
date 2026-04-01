from fastapi import APIRouter

from src.layers.orchestration_layer.engine import run_pipeline
from src.schemas.pipeline import ProcessRequest, ProcessResponse

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/process", response_model=ProcessResponse)
def process_request(payload: ProcessRequest) -> ProcessResponse:
    return run_pipeline(payload)
