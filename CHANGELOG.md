# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Added
- Two-step release automation: `prepare-release.sh X.Y.Z` turns the Unreleased
  changelog section into a dated version block, refreshes the compare links,
  and commits/pushes it; `release.sh` then tags and pushes. Splitting the
  changelog push from the tag push keeps the tag push a clean, isolated event
  so the release workflow triggers reliably.

## [1.0.3] - 2026-08-04
### Fixed
- Documented minimum Checkmk version now matches the manifest: both require
  2.5. The README previously stated 2.3, which was never tested.

### Changed
- Bump manifest package version to 1.0.3.

## [1.0.2] - 2026-08-04
### Added
- Changelog and an automated release workflow (release notes are derived
  from this file on tag push).

## [1.0.1] - 2026-07-26
### Added
- pylint configuration (`.pylintrc`).
- Docstrings across all modules.

### Changed
- Converted string formatting to f-strings.

## [1.0.0] - 2026-07-22
### Added
- Initial release: a Checkmk special agent that pulls detailed DSL line
  metrics from an AVM FRITZ!Box over TR-064 — values the built-in FRITZ!Box
  agent does not expose: SNR margin, line attenuation, current/attainable
  sync rates and the line error counters (FEC/CRC/HEC, errored seconds,
  link retrains).

[Unreleased]: https://github.com/peisenh/checkmk-fritzbox-dsl/compare/v1.0.3...HEAD
[1.0.3]: https://github.com/peisenh/checkmk-fritzbox-dsl/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/peisenh/checkmk-fritzbox-dsl/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/peisenh/checkmk-fritzbox-dsl/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/peisenh/checkmk-fritzbox-dsl/releases/tag/v1.0.0
