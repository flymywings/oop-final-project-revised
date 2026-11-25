"""models/ and logic/ must never mention the GUI toolkit (same check as the grep)."""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLKIT = "tk" + "inter"   # split so this file does not match its own grep


def test_no_gui_import_in_models_or_logic():
    offenders = [str(path.relative_to(ROOT))
                 for folder in ("models", "logic")
                 for path in (ROOT / folder).rglob("*.py")
                 if TOOLKIT in path.read_text(encoding="utf-8")]
    assert offenders == []
