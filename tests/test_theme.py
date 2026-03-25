"""Tests for quanta-ui shared theme."""
import pytest


class TestColorConstants:
    """Test the C color constant class."""

    def test_all_colors_defined(self):
        from quanta_ui.theme import C
        required = ['BG', 'BG_ALT', 'SURFACE', 'SURFACE2', 'BORDER', 'BORDER_LT',
                     'TEXT', 'TEXT2', 'TEXT3', 'ACCENT', 'ACCENT_HI', 'ACCENT_TX',
                     'GREEN', 'GREEN_HI', 'YELLOW', 'RED', 'CYAN']
        for name in required:
            assert hasattr(C, name), f"Missing color constant: {name}"

    def test_colors_are_hex_strings(self):
        from quanta_ui.theme import C
        for name in ['BG', 'TEXT', 'ACCENT', 'GREEN', 'RED']:
            val = getattr(C, name)
            assert isinstance(val, str)
            assert val.startswith('#'), f"{name} should start with #"
            assert len(val) == 7, f"{name} should be 7 chars (#RRGGBB)"

    def test_accent_color_is_pink(self):
        from quanta_ui.theme import C
        # Soft pink = #d4a0a0
        assert C.ACCENT == "#d4a0a0"


class TestStylesheet:
    """Test stylesheet generation."""

    def test_style_is_string(self):
        from quanta_ui.theme import STYLE
        assert isinstance(STYLE, str)
        assert len(STYLE) > 100

    def test_style_contains_font_family(self):
        from quanta_ui.theme import STYLE
        assert "Segoe UI" in STYLE or "font-family" in STYLE

    def test_style_contains_colors(self):
        from quanta_ui.theme import STYLE, C
        assert C.BG in STYLE
        assert C.ACCENT in STYLE

    def test_create_stylesheet_default(self):
        from quanta_ui.theme import create_stylesheet
        style = create_stylesheet()
        assert isinstance(style, str)
        assert len(style) > 100

    def test_create_stylesheet_custom(self):
        from quanta_ui.theme import create_stylesheet, C

        class Custom(C):
            ACCENT = "#ff0000"

        style = create_stylesheet(Custom)
        assert "#ff0000" in style


class TestWidgetImports:
    """Test that all widgets are importable."""

    def test_import_card(self):
        from quanta_ui.widgets import Card
        assert Card is not None

    def test_import_status_dot(self):
        from quanta_ui.widgets import StatusDot
        assert StatusDot is not None

    def test_import_heading(self):
        from quanta_ui.widgets import Heading
        assert Heading is not None

    def test_import_stat(self):
        from quanta_ui.widgets import Stat
        assert Stat is not None

    def test_import_nav_button(self):
        from quanta_ui.widgets import NavButton
        assert NavButton is not None

    def test_import_sidebar(self):
        from quanta_ui.widgets import Sidebar
        assert Sidebar is not None

    def test_import_toast(self):
        from quanta_ui.widgets import ToastNotification
        assert ToastNotification is not None


class TestPackageInit:
    """Test package-level imports."""

    def test_version(self):
        import quanta_ui
        assert quanta_ui.__version__ == "1.0.0"

    def test_top_level_imports(self):
        from quanta_ui.theme import C, STYLE, create_stylesheet
        from quanta_ui.widgets import Card, StatusDot, Heading, Stat, NavButton, Sidebar, ToastNotification
        assert all([C, STYLE, create_stylesheet, Card, StatusDot, Heading, Stat, NavButton, Sidebar, ToastNotification])
