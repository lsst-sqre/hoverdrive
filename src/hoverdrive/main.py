"""The main application factory for the hoverdrive service.

Notes
-----
Be aware that, following the normal pattern for FastAPI services, the app is
constructed when this module is loaded and is not deferred until a function is
called.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from importlib.metadata import metadata, version

import structlog
from fastapi import FastAPI
from safir.fastapi import ClientRequestError, client_request_error_handler
from safir.logging import configure_logging, configure_uvicorn_logging
from safir.middleware.x_forwarded import XForwardedMiddleware
from safir.slack.webhook import SlackRouteErrorHandler

from .config import config
from .dependencies.context import context_dependency
from .handlers.external import external_router
from .handlers.internal import internal_router

__all__ = ["app"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Set up and tear down the application."""
    # Any code here will be run when the application starts up.
    await context_dependency.initialize()

    yield

    # Any code here will be run when the application shuts down.
    await context_dependency.aclose()


configure_logging(
    profile=config.profile,
    log_level=config.log_level,
    name="hoverdrive",
)
configure_uvicorn_logging(config.log_level)

app = FastAPI(
    title="hoverdrive",
    description=metadata("hoverdrive")["Summary"],
    version=version("hoverdrive"),
    openapi_url=f"{config.path_prefix}/openapi.json",
    docs_url=f"{config.path_prefix}/docs",
    redoc_url=f"{config.path_prefix}/redoc",
    lifespan=lifespan,
)
"""The main FastAPI application for hoverdrive."""

# Attach the routers.
app.include_router(internal_router, include_in_schema=False)
app.include_router(external_router, prefix=f"{config.path_prefix}")

# Add middleware.
app.add_middleware(XForwardedMiddleware)
app.exception_handler(ClientRequestError)(client_request_error_handler)

# Configure Slack alerts.
if config.slack_webhook:
    logger = structlog.get_logger("hoverdrive")
    SlackRouteErrorHandler.initialize(
        config.slack_webhook, "hoverdrive", logger
    )
    logger.debug("Initialized Slack webhook")
