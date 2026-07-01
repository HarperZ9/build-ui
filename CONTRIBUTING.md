# Contributing

Build UI is a shared PyQt6 theme and widget library for the Build ecosystem.
Contributions should keep the package dependency-light, keep widgets themed
through `build_ui.theme.C` rather than hardcoded colors, and include tests.

## Local Setup

```powershell
python -m pip install -e ".[dev]"
```

## Verification

For documentation changes:

```powershell
git diff --check
```

For package changes:

```powershell
python -m pytest -q
ruff check .
ruff format --check .
mypy
```

Do not commit `.env` files, credentials, or local-only build artifacts.
