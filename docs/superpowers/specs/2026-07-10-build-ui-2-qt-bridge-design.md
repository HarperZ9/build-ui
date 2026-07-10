# Build UI 2 Qt Binding Bridge Design

**Date:** 2026-07-10
**Target release:** 2.0.0
**Status:** Approved for Calibrate Pro packaging dependency implementation

## Objective

Make Build UI usable by both the existing PyQt6 Build applications and the
PySide6-only Calibrate Pro release without loading two Qt bindings into one
process. Preserve the public theme/widget API while moving binding selection to
QtPy and explicit installation extras.

## Verified Starting Point

- PyPI currently serves Build UI 1.0.1 with a required `PyQt6>=6.5,<7`
  dependency.
- Build Color, Build Finance, Build Oracle, Build Engine, and Calibrate Pro all
  import Build UI while their GUI sources currently import PyQt6 directly.
- Several consumers declare unbounded `build-ui>=1.0.0`; publishing a
  PySide6-only minor release would resolve into a PyQt application and produce
  incompatible `QObject`/widget types.
- QtPy 2.4.3 is an MIT-licensed binding abstraction supporting PyQt6 and
  PySide6. It exposes `Signal`, `Slot`, and `Property` consistently.
- Disposable offscreen probes passed `Signal(dict)` and `QWidget` construction
  through QtPy 2.4.3 with both PyQt6 6.11.0 and PySide6 6.11.1.
- The existing Build UI suite passes 17 tests, Ruff, and Mypy, but only proves
  the PyQt6 import path and mostly tests class importability rather than widget
  behavior.

## Decision

Release Build UI 2.0.0 as a binding-neutral library using QtPy. The major
version reflects the changed installation contract: the core wheel depends on
QtPy but does not silently choose or install a Qt binding. Users install one of
the explicit extras:

```text
build-ui[pyqt6]>=2,<3
build-ui[pyside6]>=2,<3
```

Calibrate Pro installs the `pyside6` extra and sets `QT_API=pyside6` before the
first QtPy/Build UI import. Existing PyQt applications already declaring PyQt6
remain compatible; their dependency declarations should move to the explicit
`pyqt6` extra as they next release.

This avoids a forced simultaneous migration of every Build application while
ensuring Calibrate Pro's frozen graph contains only PySide6.

## Requirements

- **B1 — Stable public API:** Preserve `C`, `STYLE`, `create_stylesheet`,
  `Card`, `StatusDot`, `Heading`, `Stat`, `NavButton`, `Sidebar`, and
  `ToastNotification` at their current import paths.
- **B2 — QtPy source boundary:** `build_ui.widgets` imports Qt classes and
  `Signal` from QtPy. It contains no direct PyQt5, PyQt6, PySide2, or PySide6
  import.
- **B3 — Explicit binding extras:** Core dependency is
  `QtPy>=2.4.3,<3`. Extras provide `PyQt6>=6.5,<7` and
  `PySide6>=6.11.1,<7` independently. The wheel never installs both bindings.
- **B4 — Deterministic selection:** Build UI respects the caller's `QT_API` and
  does not set or change it at import time. Consumers with multiple installed
  bindings must set it before importing QtPy/Build UI.
- **B5 — Canonical version:** `build_ui.__version__` is `2.0.0` and setuptools
  reads it dynamically. README badges, changelog, wheel metadata, and release
  receipts have no independent version source.
- **B6 — Behavioral parity:** Card construction/layout, Sidebar signal
  emission/navigation, StatusDot/Stat mutation, NavButton selection, and Toast
  construction/timer behavior pass under both bindings with an offscreen
  `QApplication`.
- **B7 — Process isolation in tests:** PyQt6 and PySide6 compatibility probes
  execute in separate subprocesses or clean environments because a process may
  not switch Qt bindings after QtPy imports.
- **B8 — Source hygiene:** Repository scans reject direct Qt-binding imports and
  legacy `pyqtSignal`, `pyqtSlot`, or `pyqtProperty` tokens in package source.
- **B9 — Wheel verification:** Clean PyQt6 and PySide6 virtual environments each
  install the built wheel with exactly one binding extra, verify metadata, set
  `QT_API`, import every public name, and construct representative widgets
  offscreen.
- **B10 — Consumer transition:** Publish a migration guide for existing PyQt6
  consumers and the Calibrate Pro PySide6 consumer. Record that direct
  `pip install build-ui` installs no binding and is insufficient for widget
  construction.
- **B11 — Calibrate frozen closure:** The Calibrate release installs
  `build-ui[pyside6]>=2,<3`, contains PySide6/QtPy only, and its frozen doctor
  proves `qtpy.API_NAME == "PySide6"`.
- **B12 — Truthful compatibility:** Build UI 2 does not claim every downstream
  application is migrated. PyQt compatibility is proven at Build UI's public
  boundary; each consumer retains its own release acceptance tests.

## Package Metadata

The intended dependency shape is:

```toml
[project]
dynamic = ["version"]
dependencies = ["QtPy>=2.4.3,<3"]

[project.optional-dependencies]
pyqt6 = ["PyQt6>=6.5,<7"]
pyside6 = ["PySide6>=6.11.1,<7"]
test = ["pytest>=8.0", "pytest-cov>=5"]
dev = [
  "pytest>=8.0",
  "pytest-cov>=5",
  "ruff>=0.6",
  "mypy>=1.10",
  "build>=1.2",
]

[tool.setuptools.dynamic]
version = {attr = "build_ui.__version__"}
```

CI installs the binding separately; the `test` and `dev` extras deliberately do
not pull both bindings into the same environment.

## Runtime Contract

Consumers select a binding before the first Qt import:

```python
import os

os.environ.setdefault("QT_API", "pyside6")

from build_ui.widgets import Card
```

Library code uses:

```python
from qtpy.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt, QTimer, Signal
from qtpy.QtGui import QColor, QPainter
from qtpy.QtWidgets import QFrame, QLabel, QWidget
```

`Sidebar.page_changed = Signal(int)` retains the observable signal contract.
No public API exposes a binding-specific signal type.

## CI and Release Matrix

1. Pure theme and metadata tests across Python 3.10–3.13.
2. PyQt6 compatibility on Linux and Windows, Python 3.12, offscreen.
3. PySide6 compatibility on Linux and Windows, Python 3.12, offscreen.
4. Ruff, format, Mypy, build, and credential scan.
5. Wheel metadata inspection proving QtPy core and independent binding extras.
6. Two clean wheel smoke environments proving exactly one Qt binding each.
7. Calibrate Pro integration smoke consumes the local/published candidate wheel
   using the PySide6 extra before Build UI 2 is published.

## Documentation and Compatibility

README and USAGE lead with explicit installs:

```bash
pip install "build-ui[pyside6]>=2,<3"
# or
pip install "build-ui[pyqt6]>=2,<3"
```

The migration guide states:

- PyQt6 applications install the `pyqt6` extra or keep their own PyQt6
  dependency and set `QT_API=pyqt6` if multiple bindings exist.
- PySide6 applications install the `pyside6` extra and set
  `QT_API=pyside6` before importing Build UI.
- A single process must not mix widget objects from two Qt bindings.
- Build UI 2 preserves public class/function names but changes the dependency
  installation contract, hence the major version.

## Verification Strategy

1. Metadata tests fail on the current PyQt6-only dependency and static version.
2. Source-token tests fail on direct PyQt6 imports and `pyqtSignal`.
3. Subprocess binding probes fail before QtPy migration and pass afterward under
   both bindings.
4. Behavioral widget tests assert emitted values and state changes, not only
   class importability.
5. Wheel smoke tests install from `dist/`, not the source checkout.
6. A Calibrate integration probe imports its active window with
   `QT_API=pyside6` and scans the environment/artifact for PyQt distributions.

## Delivery Sequence

1. Add metadata/source-contract tests.
2. Migrate imports and signal declarations through QtPy.
3. Add binding-isolated behavioral tests.
4. Move version metadata to one source and define binding extras.
5. Update CI and clean-wheel verification.
6. Update README, USAGE, architecture, changelog, AGENTS, and release notes.
7. Build the candidate wheel and consume it from Calibrate Pro's PySide6
   integration acceptance lane.
8. Publish Build UI 2 only after both binding lanes and Calibrate integration
   pass.

## Success Criteria

- [ ] The same Build UI wheel passes public widget behavior under PyQt6 and
  PySide6 in isolated processes.
- [ ] Package source has no direct binding import or legacy signal alias.
- [ ] Core metadata installs QtPy and exposes independent binding extras without
  installing both bindings.
- [ ] Existing public names and signal behavior remain stable.
- [ ] Calibrate Pro resolves Build UI through the PySide6 extra and freezes no
  PyQt package.
- [ ] Documentation and release metadata accurately describe the new install
  contract and version.

## Approval Record

The operator previously approved the Calibrate Pro self-contained dependency
and PySide6 packaging lane. This bridge is the dependency-safe implementation
of that approval; it avoids breaking the other mapped PyQt6 consumers.
