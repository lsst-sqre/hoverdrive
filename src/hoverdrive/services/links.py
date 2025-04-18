"""Hoverdrive links service."""

from __future__ import annotations

from hoverdrive.storage.ookapi import OokClient

__all__ = ["LinksService"]


class LinksService:
    """A service for getting links."""

    def __init__(self, ook_client: OokClient) -> None:
        self._ook_client = ook_client

    async def get_redirect_link_for_column(
        self, tap_table_name: str, column_name: str
    ) -> str | None:
        """Get the most relevant documentation link for this column to use
        as a redirect.
        """
        links = await self._ook_client.get_sdm_column_links(
            tap_table_name, column_name
        )
        if len(links.root) == 0:
            return None
        # TODO(jonathansick): preferentiallly get specific types of links,
        # like "schema_browser"
        return links.root[0].url

    async def get_redirect_link_for_table(
        self, tap_table_name: str
    ) -> str | None:
        """Get the most relevant documentation link for this table to use
        as a redirect.
        """
        links = await self._ook_client.get_sdm_table_links(tap_table_name)
        if len(links.root) == 0:
            return None
        # TODO(jonathansick): preferentiallly get specific types of links,
        # like "schema_browser"
        return links.root[0].url
