"""Tests for the hoverdrive.handlers.external module and routes."""

from __future__ import annotations

import pytest
import respx
from httpx import AsyncClient, Response

from hoverdrive.config import config


@pytest.mark.asyncio
async def test_get_index(client: AsyncClient) -> None:
    """Test ``GET /hoverdrive/``."""
    response = await client.get("/hoverdrive/")
    assert response.status_code == 200
    data = response.json()
    metadata = data["metadata"]
    assert metadata["name"] == config.name
    assert isinstance(metadata["version"], str)
    assert isinstance(metadata["description"], str)
    assert isinstance(metadata["repository_url"], str)
    assert isinstance(metadata["documentation_url"], str)


@pytest.mark.asyncio
async def test_get_column_docs_redirect(
    client: AsyncClient, respx_mock: respx.Router
) -> None:
    """Test ``GET /hoverdrive/column-docs-redirect``."""
    respx_mock.get(
        "https://roundtable.lsst.cloud/ook/links/domains/sdm/schemas/"
        "dp02_dc2_catalogs/tables/Object/columns/detect_isPrimary"
    ).mock(
        return_value=Response(
            status_code=200,
            json=[
                {
                    "url": (
                        "https://sdm-schemas.lsst.io/dp02.html#Object.detect_isPrimary"
                    ),
                    "type": "schema_browser",
                    "title": "dp02_dc2_catalogs.Object.detect_isPrimary",
                    "collection_title": "SDM Schema Browser",
                }
            ],
        )
    )
    response = await client.get(
        "/hoverdrive/column-docs-redirect",
        params={
            "table": "dp02_dc2_catalogs.Object",
            "column": "detect_isPrimary",
        },
    )
    assert response.status_code == 307
    assert response.headers["Location"] == (
        "https://sdm-schemas.lsst.io/dp02.html#Object.detect_isPrimary"
    )


@pytest.mark.asyncio
async def test_get_table_docs_redirect(
    client: AsyncClient, respx_mock: respx.Router
) -> None:
    """Test ``GET /hoverdrive/table-docs-redirect``."""
    respx_mock.get(
        "https://roundtable.lsst.cloud/ook/links/domains/sdm/schemas/"
        "dp02_dc2_catalogs/tables/Object"
    ).mock(
        return_value=Response(
            status_code=200,
            json=[
                {
                    "url": ("https://sdm-schemas.lsst.io/dp02.html#Object"),
                    "type": "schema_browser",
                    "title": "dp02_dc2_catalogs.Object",
                    "collection_title": "SDM Schema Browser",
                }
            ],
        )
    )
    response = await client.get(
        "/hoverdrive/table-docs-redirect",
        params={
            "table": "dp02_dc2_catalogs.Object",
        },
    )
    assert response.status_code == 307
    assert response.headers["Location"] == (
        "https://sdm-schemas.lsst.io/dp02.html#Object"
    )
