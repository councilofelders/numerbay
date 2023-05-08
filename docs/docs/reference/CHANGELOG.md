# Changelog
Notable changes to this project.

## [0.2.3] - 2022-09-20
- added exponential backoff retry for requests

## [0.2.2] - 2022-05-13
- added warning for encrypted upload when no sale available

## [0.2.1] - 2022-02-19
- added install dependency for nacl

## [0.2.0] - 2022-02-02
- added support for per-order artifact upload and encryption
- added support for per-order artifact download and decryption
- added support for per-order direct Numerai submission

## [0.1.4] - 2022-01-16
- added `get_my_sales`
- added error message for resolving artifact_id in `download_artifact` when no active artifact exists
- set pypi GitHub workflow to run only on tagged commits
- trimmed docs to API reference only

## [0.1.3] - 2022-01-09
- initial code release
