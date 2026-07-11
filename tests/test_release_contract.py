from __future__ import annotations

import ast
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _subprocess_argv(text: str, method: str) -> list[str]:
    match = re.search(r'python -c "(?P<source>[^"]+)"', text, re.DOTALL)
    assert match is not None, "CI must invoke the type checker through python -c"
    source = " ".join(line.strip() for line in match.group("source").splitlines())
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "subprocess"
            and node.func.attr == method
        ):
            continue
        assert node.args and isinstance(node.args[0], ast.List)
        argv: list[str] = []
        for item in node.args[0].elts:
            if (
                isinstance(item, ast.Attribute)
                and isinstance(item.value, ast.Name)
                and item.value.id == "sys"
                and item.attr == "executable"
            ):
                argv.append("sys.executable")
            elif isinstance(item, ast.Constant) and isinstance(item.value, str):
                argv.append(item.value)
            elif isinstance(item, ast.Starred) and isinstance(item.value, ast.Name):
                argv.append(f"*{item.value.id}")
            else:
                raise AssertionError(ast.dump(item))
        return argv
    raise AssertionError(f"subprocess.{method} call not found")


def test_ci_runs_both_qt_binding_lanes() -> None:
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "pyqt6" in text
    assert "pyside6" in text
    assert "QT_API" in text
    assert "QT_QPA_PLATFORM" in text
    assert "tests/qt_binding_probe.py" in text
    assert "tests/qt_selection_mismatch_probe.py" in text
    assert "--cov-fail-under=70" in text
    assert _subprocess_argv(text, "check_output") == [
        "sys.executable",
        "-m",
        "qtpy",
        "mypy-args",
    ]
    assert _subprocess_argv(text, "call") == [
        "sys.executable",
        "-m",
        "mypy",
        "*flags",
        "build_ui",
    ]
    assert "--expect-no-binding" in text


def test_release_verifies_built_wheel_with_both_extras() -> None:
    text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "actions/checkout@v6" in text
    assert "actions/checkout@v7" not in text
    assert "actions/setup-python@v6" in text
    assert "actions/upload-artifact@v7" in text
    assert "scripts/verify_wheel.py" in text
    assert "pyqt6" in text
    assert "pyside6" in text
    assert "--expect-no-binding" in text
    assert 'cd "$RUNNER_TEMP"' in text
    assert "--source-root" in text
    assert text.count("pip check") >= 3
    assert "packaging>=24,<26" in text
    assert "tests/qt_selection_mismatch_probe.py" in text
    assert "pypa/gh-action-pypi-publish" not in text
    assert "id-token: write" not in text
    assert "\n  publish:" not in text


def test_wheel_verifier_exists() -> None:
    assert (ROOT / "scripts" / "verify_wheel.py").is_file()
    assert (ROOT / "tests" / "qt_selection_mismatch_probe.py").is_file()
