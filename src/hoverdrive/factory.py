"""Service factory."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import aclosing, asynccontextmanager
from dataclasses import dataclass
from typing import Self

from httpx import AsyncClient
from structlog.stdlib import BoundLogger


@dataclass(kw_only=True, frozen=True, slots=True)
class ProcessContext:
    """Holds singletons in the context of a Hoverdrive process, which might be
    an API server or a CLI command.
    """

    http_client: AsyncClient
    """Shared HTTP client."""

    @classmethod
    async def create(cls) -> Self:
        """Create a ProcessContext."""
        http_client = AsyncClient()

        return cls(
            http_client=http_client,
        )

    async def aclose(self) -> None:
        """Clean up a process context.

        Called during shutdown, or before recreating the process context using
        a different configuration.
        """
        await self.http_client.aclose()


class Factory:
    """Service factory."""

    def __init__(
        self,
        *,
        logger: BoundLogger,
        process_context: ProcessContext,
    ) -> None:
        self._process_context = process_context
        self._logger = logger

    @classmethod
    async def create(
        cls,
        *,
        logger: BoundLogger,
    ) -> Self:
        """Create a Factory (for use outside a request context)."""
        context = await ProcessContext.create()
        return cls(
            logger=logger,
            process_context=context,
        )

    @classmethod
    @asynccontextmanager
    async def create_standalone(
        cls,
        *,
        logger: BoundLogger,
    ) -> AsyncIterator[Self]:
        """Create a standalone factory, outside the FastAPI process, as a
        context manager.

        Use this for creating a factory in CLI commands.
        """
        factory = await cls.create(logger=logger)
        async with aclosing(factory):
            yield factory

    async def aclose(self) -> None:
        """Shut down the factory and the internal process context."""
        try:
            await self._process_context.aclose()
        finally:
            ...

    def set_logger(self, logger: BoundLogger) -> None:
        """Set the logger for the factory."""
        self._logger = logger

    @property
    def http_client(self) -> AsyncClient:
        """The shared HTTP client."""
        return self._process_context.http_client
