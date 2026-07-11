from __future__ import annotations

import pathlib

import tomli

import build_ui

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _project() -> dict:
    return tomli.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_version_is_dynamic_and_authoritative() -> None:
    data = _project()
    assert build_ui.__version__ == "2.0.0"
    assert data["project"]["dynamic"] == ["version"]
    assert "version" not in data["project"]
    assert data["tool"]["setuptools"]["dynamic"]["version"] == {"attr": "build_ui.__version__"}


def test_pep639_license_payload_is_declared() -> None:
    data = _project()
    assert data["build-system"]["requires"] == ["setuptools>=77.0.0"]
    assert data["project"]["license"] == "FSL-1.1-MIT"
    assert data["project"]["license-files"] == [
        "LICENSE",
        "THIRD_PARTY_NOTICES.md",
    ]
    notice = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for token in ("QtPy", "MIT", "PyQt6", "GPL", "PySide6", "LGPLv3"):
        assert token in notice


def test_qtpy_core_and_binding_extras_are_disjoint() -> None:
    project = _project()["project"]
    assert project["dependencies"] == ["QtPy>=2.4.3,<3"]
    extras = project["optional-dependencies"]
    assert extras["pyqt6"] == ["PyQt6>=6.5,<7"]
    assert extras["pyside6"] == ["PySide6>=6.11.1,<7"]
    assert not any("PyQt" in item or "PySide" in item for item in project["dependencies"])
    for name, requirements in extras.items():
        has_pyqt = any("PyQt" in item for item in requirements)
        has_pyside = any("PySide" in item for item in requirements)
        assert not (has_pyqt and has_pyside)
        if name in {"test", "dev"}:
            assert not has_pyqt and not has_pyside
