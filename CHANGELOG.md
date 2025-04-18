# Change log

hoverdrive is versioned with [semver](https://semver.org/).
Dependencies are updated to the latest available version during each release, and aren't noted here.

Find changes for the upcoming release in the project's [changelog.d directory](https://github.com/lsst-sqre/hoverdrive/tree/main/changelog.d/).

<!-- scriv-insert-here -->

<a id='changelog-0.1.0'></a>
## 0.1.0 (2025-04-18)

### New features

- Initial release of Hoverdrive with two endpoints:

  - `/hoverdrive/column-docs-links{?table,column,redirect}` to get documentation links for TAP columns.
  - `/hoverdrive/table-docs-links{?table,redirect}` to get documentation links for TAP tables.

  At the moment, only `redirect=true` requests are supported since the VOTable response type is not yet implemented.
