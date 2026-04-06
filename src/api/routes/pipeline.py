import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.image_parser import parse_contract_image
from src.layers.orchestration_layer.engine import run_pipeline
from src.schemas.pipeline import ProcessRequest, ProcessResponse

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/process", response_model=ProcessResponse)
def process_request(payload: ProcessRequest) -> ProcessResponse:
    return run_pipeline(payload)


@router.post("/process-image", response_model=ProcessResponse)
async def process_image_request(
    file: UploadFile = File(...),
    metadata: str = Form("{}"),
) -> ProcessResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="file must be an image")

    try:
        metadata_obj = json.loads(metadata.strip() or "{}")
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="metadata must be valid JSON") from exc

    if not isinstance(metadata_obj, dict):
        raise HTTPException(status_code=400, detail="metadata must be a JSON object")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="uploaded image is empty")

    suffix = Path(file.filename or "upload.png").suffix or ".png"
    temp_path: Path | None = None
    try:
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(image_bytes)
            temp_path = Path(temp_file.name)

        extracted_text = parse_contract_image(str(temp_path))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="image processing failed") from exc
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    payload = ProcessRequest(
        source_type="text",
        source_value=extracted_text,
        metadata={
            **metadata_obj,
            "source_type": "image",
            "source_filename": file.filename or "uploaded_image",
        },
    )
    return run_pipeline(payload)
