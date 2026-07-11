# Contributing

Build UI is a shared, binding-neutral Qt 6 theme and widget library for the
Build ecosystem. Keep the package dependency-light, theme widgets through
`build_ui.theme.C` rather than hardcoded colors, and include tests.

## Local setup

Choose one binding lane per environment:

```powershell
python -m pip install -e ".[dev,pyqt6]"
$env:QT_API = "pyqt6"
```

or:

```powershell
python -m pip install -e ".[dev,pyside6]"
$env:QT_API = "pyside6"
```

Do not install both extras into one test environment. Set
`QT_QPA_PLATFORM=offscreen` for automated widget tests.

## Verification

For documentation changes:

```powershell
python -m pytest tests/test_release_contract.py -q
git diff --check
```

For package changes, run the complete suite in both isolated binding lanes:

```powershell
python -m pytest tests -q --cov=build_ui --cov-report=term-missing --cov-fail-under=70
python -m ruff check .
python -m ruff format --check .
$qtpyMypyArgs = (& python -m qtpy mypy-args) -split " "
python -m mypy @qtpyMypyArgs
python tests/qt_binding_probe.py
```

Do not commit `.env` files, credentials, generated distributions, or local-only
build artifacts. Publication requires a separate reviewed release decision.
