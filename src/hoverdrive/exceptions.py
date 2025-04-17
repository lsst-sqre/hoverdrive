"""Application exceptions."""

from fastapi import status
from safir.fastapi import ClientRequestError

__all__ = ["EndpointNotImplementedError", "NotFoundError"]


class EndpointNotImplementedError(ClientRequestError):
    """Functionality is not implemented."""

    error = "not_implemented"
    status_code = status.HTTP_501_NOT_IMPLEMENTED


class NotFoundError(ClientRequestError):
    """Requested resource not found."""

    error = "not_found"
    status_code = status.HTTP_404_NOT_FOUND
