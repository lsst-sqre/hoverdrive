"""Application exceptions."""

from fastapi import status
from safir.fastapi import ClientRequestError

__all__ = [
    "EndpointNotImplementedError",
    "LinkRedirectRequestError",
    "NotFoundError",
]


class EndpointNotImplementedError(ClientRequestError):
    """Functionality is not implemented."""

    error = "not_implemented"
    status_code = status.HTTP_501_NOT_IMPLEMENTED


class NotFoundError(ClientRequestError):
    """Requested resource not found."""

    error = "not_found"
    status_code = status.HTTP_404_NOT_FOUND


class LinkRedirectRequestError(ClientRequestError):
    """Link redirect request error."""

    error = "bad_link_redirect_request"
    status_code = status.HTTP_400_BAD_REQUEST
