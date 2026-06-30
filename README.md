# Build UI

Shared PyQt6 theme and widget library for the Build ecosystem. Provides a consistent dark theme, reusable chart widgets, and styled controls across all Build applications.

## Installation

```bash
pip install build-ui
```

## Quick Start

```python
from build_ui.theme import apply_theme
from build_ui.widgets import ChartWidget

# Apply the Build dark theme to any PyQt6 app
apply_theme(app)

# Use pre-built widgets
chart = ChartWidget()
chart.plot(data)
```

## Repository

[https://github.com/HarperZ9/build-ui](https://github.com/HarperZ9/build-ui)
