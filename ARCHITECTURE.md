# Architecture

Build UI is a two-module PyQt6 support library: a shared theme and a shared widget
set. It has no business logic of its own — it exists so every application in the
Build family (Calibrate Pro, Build Color, Build Finance, Build Oracle, Build
Engine) renders with one consistent look instead of five divergent ones.

## Layers

```
build_ui/
  theme.py     Color constants (class C) + create_stylesheet() Qt stylesheet generator
  widgets.py   Reusable QWidget subclasses built on top of theme.py
  __init__.py  Public API surface (re-exports; version)
```

## theme.py

`C` is a plain class of hex-string color constants (background, surface, text,
accent, semantic colors for success/warning/error/info). `create_stylesheet(c=None)`
renders a full Qt stylesheet string from a color class, defaulting to `C`. `STYLE`
is the pre-rendered stylesheet for `C`, computed once at import time.

Passing a different class (subclassing `C` and overriding constants) into
`create_stylesheet` produces a themed variant without touching widget code —
this is the library's only extension point.

## widgets.py

Each widget is a thin `QWidget`/`QFrame`/`QLabel`/`QPushButton` subclass that
applies `theme.py` colors in its constructor: `Card`, `StatusDot`, `Heading`,
`Stat`, `NavButton`, `Sidebar`, `ToastNotification`. Widgets read colors directly
from `build_ui.theme.C` — they are not restyled by passing a custom theme class at
construction time. Consumers who need a different palette should override the
process-wide stylesheet via `create_stylesheet`.

`Sidebar` and `NavButton` cooperate: `Sidebar` owns the list of `NavButton`s and
emits `page_changed` when the active page changes. `ToastNotification` owns its
own `QTimer` and `QPropertyAnimation` for auto-dismiss and slide/fade transitions.

## Design decisions

- **No state beyond the widget itself.** Widgets hold their own display state
  (current color, current page) and emit Qt signals; they do not reach into
  application state.
- **PyQt6 only.** This library exists to standardize on one Qt binding across the
  Build family. It is not binding-agnostic by design.
- **Headless-safe import, GUI-only construction.** The module can be imported in
  a script with no display (colors and stylesheet generation are pure string
  work); constructing a widget requires a running `QApplication`.

## Testing

The suite under `tests/` verifies theme constants exist and are valid hex colors,
stylesheet generation produces a non-trivial string containing those colors, and
every widget class is importable from its public path. `ruff check .` and `mypy`
gate style and types.
