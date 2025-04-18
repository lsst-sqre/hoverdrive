"""Handlers for the app's external root, ``/hoverdrive/``."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from safir.models import ErrorLocation
from safir.slack.webhook import SlackRouteErrorHandler

from hoverdrive.dependencies.context import RequestContext, context_dependency
from hoverdrive.exceptions import (
    EndpointNotImplementedError,
    LinkRedirectRequestError,
    NotFoundError,
)

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


@router.get(
    "/column-docs-links",
    summary="Get documention links for a column",
)
async def get_column_docs_links(
    *,
    table_name: Annotated[
        str,
        Query(
            ...,
            alias="table",
            title="Table name",
            examples=["dp02_dc2_catalogs.Object"],
        ),
    ],
    column_names: Annotated[
        list[str],
        Query(
            ...,
            alias="column",
            title="Column name",
            description=(
                "The name of the column to get links for. Provide multiple "
                "column parameters to get links for multiple columns."
            ),
            examples=["detect_isPrimary"],
        ),
    ],
    redirect: Annotated[
        bool,
        Query(
            title="Redirect",
            description="Whether to redirect to the documentation link.",
        ),
    ] = False,
    context: Annotated[RequestContext, Depends(context_dependency)],
) -> RedirectResponse:
    """Use a `redirect=true` query parameter to get a redirect to the most
    documentation link for this column.
    """
    factory = context.factory
    links_service = factory.get_links_service()
    if redirect:
        if len(column_names) != 1:
            raise LinkRedirectRequestError(
                "Only one column name is supported for redirection.",
                ErrorLocation.query,
                ["column"],
            )
        column_name = column_names[0]
        link = await links_service.get_redirect_link_for_column(
            table_name, column_name
        )
        if link is None:
            raise NotFoundError(
                "No documentation link found for column "
                f"{table_name}.{column_name}"
            )
        return RedirectResponse(url=link, status_code=307)

    raise EndpointNotImplementedError(
        "Use of `redirect=true` is required for this endpoint."
    )


@router.get(
    "/table-docs-links",
    summary="Get documention links for a table",
)
async def get_table_docs_links(
    *,
    table_names: Annotated[
        list[str],
        Query(
            ...,
            alias="table",
            title="Table name",
            description=(
                "The name of the table to get links for. Provide multiple "
                "table parameters to get links for multiple tables."
            ),
            examples=["dp02_dc2_catalogs.Object"],
        ),
    ],
    redirect: Annotated[
        bool,
        Query(
            title="Redirect",
            description="Whether to redirect to the documentation link.",
        ),
    ] = False,
    context: Annotated[RequestContext, Depends(context_dependency)],
) -> RedirectResponse:
    """Use a `redirect=true` query parameter to get a redirect to the most
    documentation link for this table.
    """
    factory = context.factory
    links_service = factory.get_links_service()
    if redirect:
        if len(table_names) != 1:
            raise LinkRedirectRequestError(
                "Only one table name is supported for redirection.",
                ErrorLocation.query,
                ["table"],
            )
        table_name = table_names[0]
        link = await links_service.get_redirect_link_for_table(table_name)
        if link is None:
            raise NotFoundError(
                f"No documentation link found for table {table_name}"
            )
        return RedirectResponse(url=link, status_code=307)

    raise EndpointNotImplementedError(
        "Use of `redirect=true` is required for this endpoint."
    )
