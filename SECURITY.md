# Security Policy

## Supported

Build UI follows a rolling release. Until a 2.0 line exists, only the latest
release on the default branch is supported for fixes.

## Reporting a vulnerability

Report suspected vulnerabilities privately via GitHub Security Advisories — the
"Security" tab of this repository, then "Report a vulnerability". Do NOT open a
public issue for an unfixed vulnerability.

Please include the affected module and version, a minimal reproduction, and the
impact. The maintainer will acknowledge within a stated window and agree a
disclosure date.

## Attack surface (the honest part)

Build UI is a UI-only support library. Its surface is small by design:

- **No network.** The library performs no network access. Nothing is fetched or
  sent.
- **No code evaluation.** The library never `eval`s or executes input; it only
  builds Qt stylesheet strings from color constants and constructs widgets.
- **No file I/O.** `theme.py` and `widgets.py` read no files and write no files;
  all rendering goes through Qt's own widget and paint APIs.
- **PyQt6 carries its own surface.** PyQt6 is the sole runtime dependency; its
  own advisories apply. Build UI adds no additional attack surface on top of it.

## What does not count

- A style regression (wrong color, wrong layout) is a correctness issue, not a
  security vulnerability — open a normal issue.
- Crashes from constructing a widget without a running `QApplication` are
  expected PyQt6 behavior, not a vulnerability in this library.
