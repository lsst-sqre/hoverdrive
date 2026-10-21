# Change log

Hoverdrive is versioned with [semver](https://semver.org/).
Dependencies are updated to the latest available version during each release, and aren't noted here.

Find changes for the upcoming release in the project's [changelog.d directory](https://github.com/lsst-sqre/hoverdrive/tree/main/changelog.d/).

<!-- scriv-insert-here -->

<a id='changelog-0.2.2'></a>
## 0.2.2 (2026-10-21)

### Other changes

- Update the Python runtime to 3.14. The Docker base image is now `python:3.14.7-slim-trixie` (Debian 13), and `.python-version`, `requires-python`, and the PyPI classifier are all bumped to match so that CI and the container run the same interpreter.

- Update dependencies. Safir 15.2.2 lifts the `cryptography<50` cap, which takes cryptography to 50.0.2 and PyJWT to 2.15.1 and closes the open Dependabot security alerts for both, along with urllib3 2.8.0 and virtualenv 21.14.7.

- Update certifi to 2026.10.19 and uv to 0.13.4 ([GHSA-6q48-6c7w-9gw2](https://github.com/advisories/GHSA-6q48-6c7w-9gw2), [GHSA-hq85-5cpj-mr62](https://github.com/advisories/GHSA-hq85-5cpj-mr62)). Earlier versions of both trust the `emSign ECC Root CA - G3` root certificate, whose intermediate CAs have compromised private keys. uv is updated in the Dockerfile, CI, and pre-commit configuration as well as `uv.lock`. The rebuilt image also picks up Debian's `ca-certificates` security update ([DSA-6572-1](https://security-tracker.debian.org/tracker/DSA-6572-1)), which removes the same root from the system trust store.

<a id='changelog-0.2.1'></a>
## 0.2.1 (2026-07-20)

### Other changes

- Update pinned dependencies and pre-commit hooks.

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
