# AGENTS.md - Build UI

## Scope

This file applies to the `build-ui` repository. Root workspace instructions
still apply; this repo is a shared PyQt6 theme and widget library consumed by
other Build applications (Calibrate Pro, Build Color, Build Finance, Build
Oracle, Build Engine).

## Product Boundary

Build UI provides a shared visual theme (`theme.py`) and a small set of reusable
widgets (`widgets.py`). It has no application logic, no network access, and no
file I/O beyond what Qt itself performs to render.

Publishable surfaces:

- `build_ui/` - package code.
- `tests/` - regression coverage for theme constants, stylesheet generation, and
  widget importability.
- `README.md`, `ARCHITECTURE.md`, `USAGE.md`, and `pyproject.toml` - package and
  product posture.

Keep local-only unless deliberately scrubbed:

- `.env`, `.env.*`, local settings, generated logs, and build artifacts.

## Editing Rules

- Keep this package dependency-light: PyQt6 is the only runtime dependency.
  Do not add application-specific logic here — it belongs in the consuming app.
- Any new widget must apply colors from `build_ui.theme.C`, not hardcoded hex
  values, so a future theme change propagates automatically.
- Preserve the existing public names (`C`, `STYLE`, `create_stylesheet`, and the
  widget classes) — other repositories in the Build family import them directly.
- New widgets need at least an importability test; widgets with non-trivial
  logic (e.g., color state, signal emission) need a behavior test.

## Verification

For documentation-only changes:

```powershell
git diff --check
```

For package changes:

```powershell
python -m pytest -q
ruff check .
mypy
```

Before committing or pushing, scan changed files for credential-shaped content
and confirm `.env` remains ignored.
