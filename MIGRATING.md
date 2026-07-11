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
