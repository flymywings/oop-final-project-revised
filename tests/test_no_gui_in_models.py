"""models/ and logic/ must never mention either GUI toolkit (same check as the grep)."""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLKITS = ("tk" + "inter", "py" + "game")   # split so this file does not match its own grep


def test_no_gui_import_in_models_or_logic():
    offenders = [f"{path.relative_to(ROOT)} mentions {word}"
                 for folder in ("models", "logic")
                 for path in (ROOT / folder).rglob("*.py")
                 for word in TOOLKITS
                 if word in path.read_text(encoding="utf-8")]
    assert offenders == []
