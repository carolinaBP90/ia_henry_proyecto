"""Langfuse tracing helpers using SDK v3 with LangChain integration."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Generator

from src.config import Settings


LOGGER = logging.getLogger(__name__)


class TracingService:
    """Facade for Langfuse trace/span creation using SDK v3.

    Uses the Langfuse singleton pattern and context-manager API so that
    LangChain CallbackHandlers automatically inherit the active observation
    context — no manual parent linking required.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize Langfuse singleton when enabled, otherwise no-op mode."""
        self._enabled = settings.langfuse_enabled
        self._client: Any | None = None

        if not self._enabled:
            LOGGER.info("Langfuse disabled; tracing running in no-op mode")
            return

        try:
            # Import AFTER env vars are loaded (dotenv already called by Settings).
            # Initialize the global singleton; subsequent get_client() calls return it.
            from langfuse import Langfuse, get_client

            Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )
            self._client = get_client()
            LOGGER.info("Langfuse initialized (host=%s)", settings.langfuse_host)
        except Exception:  # noqa: BLE001
            LOGGER.exception("Failed to initialize Langfuse; falling back to no-op tracing")
            self._enabled = False

    @contextmanager
    def root_trace(
        self,
        name: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Generator[Any | None, None, None]:
        """Start a root trace as a context manager.

        Yields the underlying span object so callers can call .update() on it.
        All child spans and LangChain generations are automatically nested here.
        """
        if not self._enabled or self._client is None:
            yield None
            return

        with self._client.start_as_current_observation(
            as_type="span",
            name=name,
            input=input,
            metadata=metadata,
        ) as span:
            yield span

    @contextmanager
    def span(
        self,
        name: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Generator[Any | None, None, None]:
        """Create a child span nested under the current active observation.

        Must be called inside a root_trace() context (or another span() context).
        """
        if not self._enabled or self._client is None:
            yield None
            return

        with self._client.start_as_current_observation(
            as_type="span",
            name=name,
            input=input,
            metadata=metadata,
        ) as span:
            yield span

    def get_langchain_handler(self) -> Any | None:
        """Return a LangChain CallbackHandler for the current observation context.

        Call this inside a root_trace() or span() context. The handler
        automatically nests LangChain generations (with model name and token
        usage) under the active Langfuse observation.

        Why: Framework integrations capture model name, token usage, and latency
        automatically — avoiding manual generation tracking.
        """
        if not self._enabled or self._client is None:
            return None

        try:
            from langfuse.langchain import CallbackHandler

            return CallbackHandler()
        except Exception:  # noqa: BLE001
            LOGGER.exception("Failed to create LangChain CallbackHandler")
            return None

    def shutdown(self) -> None:
        """Flush all queued events and shut down the Langfuse client.

        MUST be called before a short-lived script exits — without this,
        queued traces are never delivered to the Langfuse API.
        """
        if self._enabled and self._client is not None:
            try:
                self._client.shutdown()
                LOGGER.info("Langfuse shutdown complete; all traces flushed")
            except Exception:  # noqa: BLE001
                LOGGER.exception("Langfuse shutdown failed")
