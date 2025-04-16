"""Models for hoverdrive."""

from typing import Self

from fastapi import Request
from pydantic import AnyHttpUrl, BaseModel, Field
from safir.metadata import Metadata as SafirMetadata
from safir.metadata import get_metadata

from hoverdrive.config import config

__all__ = ["Index"]


class Index(BaseModel):
    """Metadata about the Hoverdrive application."""

    metadata: SafirMetadata = Field(..., title="Application metadata")

    api_docs: AnyHttpUrl = Field(..., title="API documentation URL")

    redoc_api_docs: AnyHttpUrl = Field(
        ..., title="ReDoc API documentation URL"
    )

    @classmethod
    def create(cls, request: Request) -> Self:
        """Create an Index model from a request.

        Parameters
        ----------
        request
            The incoming request.

        Returns
        -------
        Index
            The Index model.
        """
        metadata = get_metadata(
            package_name="hoverdrive",
            application_name=config.name,
        )
        api_docs_url = AnyHttpUrl(
            str(request.url.replace(path=f"/{config.path_prefix}/docs"))
        )
        redoc_url = AnyHttpUrl(
            str(request.url.replace(path=f"/{config.path_prefix}/redoc"))
        )
        return cls(
            metadata=metadata, api_docs=api_docs_url, redoc_api_docs=redoc_url
        )
