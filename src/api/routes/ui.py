from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["ui"])

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_INDEX_FILE = _PROJECT_ROOT / "src" / "static" / "index.html"


@router.get("/")
def home() -> FileResponse:
    return FileResponse(_INDEX_FILE)
