from fastapi import FastAPI

from src.api.routes.health import router as health_router
from src.api.routes.pipeline import router as pipeline_router
from src.api.routes.ui import router as ui_router
from src.core.config import get_settings
from src.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name)
app.include_router(ui_router)
app.include_router(health_router)
app.include_router(pipeline_router)
