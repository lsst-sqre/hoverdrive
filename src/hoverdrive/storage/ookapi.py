"""Ook API interface."""

from __future__ import annotations

from httpx import AsyncClient
from pydantic import BaseModel, Field, RootModel
from structlog.stdlib import BoundLogger
from uritemplate import expand, variable

__all__ = ["OokClient", "OokLink", "OokLinksArray"]


class OokClient:
    """Client for the Ook API.

    Parameters
    ----------
    base_url
        The base URL of the Ook API.
        Example: "https://roundtable.lsst.cloud/ook"
    http_client
        The httpx client to use for making requests.
    """

    def __init__(
        self, *, base_url: str, http_client: AsyncClient, logger: BoundLogger
    ) -> None:
        base_url = base_url.removesuffix("/")
        self.base_url = base_url
        self._http_client = http_client
        self._logger = logger

    async def get_sdm_column_links(
        self, tap_table_name: str, column_name: str
    ) -> OokLinksArray:
        """Make a GET request to the Ook API for the SDM column links.

        Parameters
        ----------
        tap_table_name
            The name of the TAP table.
        column_name
            The name of the column.

        Returns
        -------
        links
            The links for the column.
        """
        schema_name, table_name = self._parse_tap_table_name_to_sdm(
            tap_table_name
        )
        path_template = (
            "/links/domains/sdm/schemas/{schema_name}/tables/{table_name}"
            "/columns/{column_name}"
        )
        url_params = {
            "schema_name": schema_name,
            "table_name": table_name,
            "column_name": column_name,
        }
        json_data = await self.get_item(path_template, url_params=url_params)
        # Ideally we should convert this into an internal domain model to avoid
        # coupling the rest of the codebase to the Ook API.
        return OokLinksArray.model_validate_json(json_data)

    async def get_sdm_table_links(self, tap_table_name: str) -> OokLinksArray:
        """Make a GET request to the Ook API for the SDM table links.

        Parameters
        ----------
        tap_table_name
            The name of the TAP table.

        Returns
        -------
        OokLinksArray
            The links for the column.
        """
        schema_name, table_name = self._parse_tap_table_name_to_sdm(
            tap_table_name
        )
        path_template = (
            "/links/domains/sdm/schemas/{schema_name}/tables/{table_name}"
        )
        url_params = {
            "schema_name": schema_name,
            "table_name": table_name,
        }
        json_data = await self.get_item(path_template, url_params=url_params)
        # Ideally we should convert this into an internal domain model to avoid
        # coupling the rest of the codebase to the Ook API.
        return OokLinksArray.model_validate_json(json_data)

    async def get_item(
        self,
        path_template: str,
        *,
        url_params: dict | None = None,
    ) -> str:
        """Make a GET request to the Ook API for a single item.

        Parameters
        ----------
        path_template
            Template for the Ook endpoint's path.
        url_params
            Parameters for the `path_template`.

        Returns
        -------
        str
            The response, as text.
        """
        url = self._format_url(
            path_template,
            url_params=url_params,
        )
        self._logger.info("Sending OOK Get", url=url)
        response = await self._http_client.get(url)
        response.raise_for_status()
        return response.text

    def _format_url(
        self,
        path_template: str,
        *,
        url_params: variable.VariableValueDict | None = None,
    ) -> str:
        if not path_template.startswith("/"):
            path_template = "/" + path_template
        uri_template = f"{self.base_url}{path_template}"
        return expand(uri_template, url_params)

    def _parse_tap_table_name_to_sdm(
        self, tap_table_name: str
    ) -> tuple[str, str]:
        """Parse the TAP table name into SDM schema and table names.

        SDM has a concept fo schema name, whereas TAP does not.
        In SDM, the schema name is the first part of the table name,

        Parameters
        ----------
        tap_table_name
            The name of the TAP table.

        Returns
        -------
        tuple[str, str]
            The schema and table names.
        """
        schema_name, table_name = tap_table_name.split(".", maxsplit=1)
        return schema_name, table_name


class OokLink(BaseModel):
    """A documentation link."""

    url: str = Field(..., title="Documentation URL")

    title: str = Field(
        ...,
        title="Title of the resource",
        description=(
            "The title of the page or section that this link references."
        ),
    )

    type: str = Field(..., title="Type of documentation")

    collection_title: str | None = Field(
        None,
        title="Title of the documentation collection",
        description=(
            "For a link into a user guide, this would be the title of "
            "the user guide itself."
        ),
    )


class OokLinksArray(RootModel):
    """An array of documentation links."""

    root: list[OokLink]
