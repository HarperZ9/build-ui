# Quanta UI

Shared PyQt6 theme and widget library for the Quanta ecosystem. Provides a consistent dark theme, reusable chart widgets, and styled controls across all Quanta applications.

## Installation

```bash
pip install quanta-ui
```

## Quick Start

```python
from quanta_ui.theme import apply_theme
from quanta_ui.widgets import ChartWidget

# Apply the Quanta dark theme to any PyQt6 app
apply_theme(app)

# Use pre-built widgets
chart = ChartWidget()
chart.plot(data)
```

## Repository

[https://github.com/HarperZ9/quanta-ui](https://github.com/HarperZ9/quanta-ui)
