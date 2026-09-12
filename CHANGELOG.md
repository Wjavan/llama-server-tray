# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2026-09-12

### Added
- Initial release
- Silent tray launcher with no console window
- Auto-restart mechanism with failure protection (3 consecutive failures)
- Single-instance lock to prevent duplicate launches
- Dual logging system (tray log + server log)
- Tray context menu (status, logs, restart, exit)
- PyInstaller packaging support
- SHA256 checksum generation for releases
- GitHub Actions CI/CD for automated builds
- MIT License

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- Linux CI `import` test failure with `.pyw` extension (now uses `py_compile` syntax check only)

### Security
- None

---

## [Unreleased]
### Planned
- Command-line argument configuration support
- Customizable tray icon
- Multi-model switching support
- Health check endpoint
- Additional error messages and log level options
