# Migrating to Build UI 2

Build UI 2 preserves the public theme and widget names but changes the Qt
installation contract. The core package installs QtPy and no Qt binding.

## PyQt6 applications

Install `pip install "build-ui[pyqt6]>=2,<3"`. If more than one Qt binding is
installed, set `QT_API=pyqt6` before the first QtPy or Build UI import.

## PySide6 applications

Install `pip install "build-ui[pyside6]>=2,<3"`. Set `QT_API=pyside6` before the
first QtPy or Build UI import. Calibrate Pro uses this lane.

## Process invariant

Do not mix PyQt6 and PySide6 objects in one process and do not change `QT_API`
after importing QtPy. Build UI rejects Qt 5 bindings.

## Downstream acceptance

Build UI proves its public boundary under both bindings. Each consuming
application must run its own GUI acceptance tests before updating its version
constraint. Build Engine must declare its GUI dependencies, and Build
Ecosystem must not aggregate PyQt6-only and PySide6-only applications as one
proven single-binding environment.

### Calibrate Pro candidate handoff

The candidate has not been published. Before Build UI 2 is released, hand the
Calibrate Pro acceptance lane these exact files from the same candidate run:

- `dist/build_ui-2.0.0-py3-none-any.whl`
- `dist/SHA256SUMS.txt`, including the SHA-256 line for that wheel

The downstream operator records and checks the exact wheel before running the
Calibrate binding contract:

```powershell
$env:BUILD_UI_2_WHEEL = (Resolve-Path -LiteralPath .\dist\build_ui-2.0.0-py3-none-any.whl).Path
Get-FileHash -LiteralPath $env:BUILD_UI_2_WHEEL -Algorithm SHA256
# In the Calibrate Pro acceptance environment:
python -m pip install "$($env:BUILD_UI_2_WHEEL)[pyside6]"
python -m pip check
python -m pytest tests/test_qt_binding_contract.py -q
```

The reported SHA-256 must equal the wheel's entry in `dist/SHA256SUMS.txt`.
Handoff evidence consists of the resolved wheel path, matching SHA-256, Python,
QtPy, and PySide6 versions, and the passing probe output. A passing Build UI
candidate alone does not claim Calibrate Pro release acceptance.
