# Changelog

All notable changes to Build UI are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-06-30

### Added
- Flagship parity pass: `[tool.mypy]` and `[tool.coverage]` configuration, `dev` extras,
  mypy + coverage gate in CI, OIDC trusted-publishing release workflow, full root doc set
  (ARCHITECTURE, SECURITY, AGENTS, AUTHORS, CONTRIBUTING, USAGE, ENTERPRISE-READINESS),
  and brand assets.

### Fixed
- Type annotation on `widgets` (`color: str | None`) so `mypy` passes clean.

## [1.0.0]

### Added
- Shared PyQt6 dark theme and reusable widget library (theme + widgets) for the Build
  ecosystem: consistent styling and chart/control widgets across the Build applications.
