"""Handlers for the app's external root, ``/hoverdrive/``."""

from fastapi import APIRouter, Request
from safir.slack.webhook import SlackRouteErrorHandler

from .models import Index

__all__ = ["router"]

router = APIRouter(route_class=SlackRouteErrorHandler)
"""FastAPI router for all external handlers."""


@router.get(
    "/",
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def get_index(request: Request) -> Index:
    """Provides the application's version and links to API documentation and
    endpoints.
    """
    return Index.create(request)
