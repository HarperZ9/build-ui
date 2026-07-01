# Build UI Enterprise Readiness

Build UI is the shared presentation layer of the build/Project Telos family: a
small, dependency-light PyQt6 theme and widget set that gives every Build
application (Calibrate Pro, Build Color, Build Finance, Build Oracle, Build
Engine) one consistent look instead of five divergent ones.

## Enterprise role

- Provide a single source of truth for color (`build_ui.theme.C`) and Qt
  stylesheet generation (`create_stylesheet`) so a palette change propagates to
  every consuming application.
- Provide a small set of reusable, pre-styled widgets (`Card`, `Sidebar`,
  `NavButton`, `Stat`, `Heading`, `StatusDot`, `ToastNotification`) so
  applications don't re-implement layout chrome.
- Keep the dependency surface to PyQt6 alone, so it installs cleanly anywhere
  the consuming application already runs.

## Operator surface

- The importable Python API (`build_ui.theme`, `build_ui.widgets`) for embedding
  in PyQt6 applications. There is no CLI or standalone GUI — this is a library.

## Reproducibility and provenance

- Theme and widget code is deterministic: the same color class always produces
  the same stylesheet string, and widgets render the same way given the same
  constructor arguments.
- There are no generated artifacts beyond the in-memory Qt stylesheet string.

## Dependencies and boundary

- **Runtime:** `PyQt6` only. No network, no code evaluation, no file I/O.
- There are no optional extras — the full library is available with the single
  runtime dependency installed.

## Quality gates

- `ruff check .` (style), `mypy` (types — the full package is type-clean), and
  `pytest` with coverage run in CI on every push and pull request.

## Honest limits

- Widget-level behavior (paint events, animations, signal wiring) is exercised
  by unit tests at the import/construction level; full interactive verification
  happens in the consuming applications where the widgets are actually placed
  on screen. Coverage reflects this: theme logic is fully covered, and the
  widget module's coverage floor is set low and honestly, not padded.
