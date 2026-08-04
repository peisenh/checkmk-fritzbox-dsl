# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Added
- Add changelog and automated release workflow.

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

[Unreleased]: https://github.com/peisenh/checkmk-fritzbox-dsl/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/peisenh/checkmk-fritzbox-dsl/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/peisenh/checkmk-fritzbox-dsl/releases/tag/v1.0.0
