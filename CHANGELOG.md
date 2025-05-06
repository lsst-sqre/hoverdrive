# Change log

Hoverdrive is versioned with [semver](https://semver.org/).
Dependencies are updated to the latest available version during each release, and aren't noted here.

Find changes for the upcoming release in the project's [changelog.d directory](https://github.com/lsst-sqre/hoverdrive/tree/main/changelog.d/).

<!-- scriv-insert-here -->

<a id='changelog-0.2.0'></a>

## 0.2.0 (2025-05-06)

### Backwards-incompatible changes

- Dropped the original `GET /hoverdrive/column-docs-links` and `GET /hoverdrive/table-docs-links` endpoints. These are replaced with new `GET /hoverdrive/column-docs-redirect` and `GET /hoverdrive/table-docs-redirect` endpoints that return a 307 redirect to the most relevant documentation page. We will re-add the original endpoints in the future, but without the `?redirect` query parameter. Make this change avoids complexity in formulating the VO service descriptors for these endpoints.

### New features

- New `GET /hoverdrive/column-docs-redirect` and `GET /hoverdrive/table-docs-redirect` endpoints. These endpoints return a 307 redirect to the most relevant documentation page for the given column or table.

### Bug fixes

- Fix caching in Docker for the application layer itself.

<a id='changelog-0.1.0'></a>

## 0.1.0 (2025-04-18)

### New features

- Initial release of Hoverdrive with two endpoints:

  - `/hoverdrive/column-docs-links{?table,column,redirect}` to get documentation links for TAP columns.
  - `/hoverdrive/table-docs-links{?table,redirect}` to get documentation links for TAP tables.

  At the moment, only `redirect=true` requests are supported since the VOTable response type is not yet implemented.
