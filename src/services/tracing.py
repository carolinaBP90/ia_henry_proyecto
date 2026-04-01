"""Langfuse tracing helpers with graceful no-op fallback."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Generator

from src.config import Settings


LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class TraceHandle:
    """Reference to a root trace object plus a lightweight metadata context."""

    trace_obj: Any | None
    metadata: dict[str, Any]


class TracingService:
    """Facade for Langfuse trace/span creation.

    The service isolates Langfuse SDK details and keeps business logic
    independent from observability provider internals.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize Langfuse client when enabled, otherwise no-op mode."""
        self._enabled = settings.langfuse_enabled
        self._client: Any | None = None

        if not self._enabled:
            LOGGER.info("Langfuse disabled; tracing running in no-op mode")
            return

        try:
            from langfuse import Langfuse

            self._client = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Failed to initialize Langfuse; falling back to no-op tracing")
            self._enabled = False
            self._client = None
            LOGGER.debug("Langfuse init exception: %s", exc)

    def start_root_trace(self, name: str, metadata: dict[str, Any]) -> TraceHandle:
        """Create a root trace for a contract analysis request.

        Args:
            name: Trace name (for example, contract-analysis).
            metadata: Request-level metadata (ids, tenant, timing context).

        Returns:
            TraceHandle that can be used to create child spans.
        """
        if not self._enabled or self._client is None:
            return TraceHandle(trace_obj=None, metadata=metadata)

        trace_obj = None
        try:
            trace_obj = self._client.trace(name=name, metadata=metadata)
        except Exception:  # noqa: BLE001
            LOGGER.exception("Could not create root Langfuse trace")
        return TraceHandle(trace_obj=trace_obj, metadata=metadata)

    @contextmanager
    def span(
        self,
        trace_handle: TraceHandle,
        name: str,
        input_data: Any | None = None,
    ) -> Generator[Any | None, None, None]:
        """Create a child span under a root trace.

        This context manager never raises tracing errors to caller code.
        """
        span_obj: Any | None = None

        if self._enabled and trace_handle.trace_obj is not None:
            try:
                span_obj = trace_handle.trace_obj.span(name=name, input=input_data)
            except Exception:  # noqa: BLE001
                LOGGER.exception("Failed to create Langfuse span: %s", name)
                span_obj = None

        try:
            yield span_obj
        except Exception as exc:  # noqa: BLE001
            self._safe_span_end(span_obj, level="ERROR", output={"error": str(exc)})
            raise
        else:
            self._safe_span_end(span_obj, level="DEFAULT", output={"status": "ok"})

    def _safe_span_end(self, span_obj: Any | None, level: str, output: Any) -> None:
        """End a span safely regardless of SDK version differences."""
        if span_obj is None:
            return

        try:
            if hasattr(span_obj, "end"):
                span_obj.end(level=level, output=output)
            elif hasattr(span_obj, "update"):
                span_obj.update(level=level, output=output)
        except Exception:  # noqa: BLE001
            LOGGER.exception("Failed to close span cleanly")
