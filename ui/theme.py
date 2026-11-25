"""Shared look: colours, fonts, HoverButton, bind_hover, load_sprite.

Owner: Khael. CONTRACT STUB: the names below are fixed and already work
in a plain way so Joseph can build on them. Khael restyles freely but
keeps every name and signature. Push the final version by 2:00.
"""

import os
import tkinter as tk

# Colours
BG = "#1e1e2a"
PANEL = "#2b2b3c"
FG = "#f0f0f0"
ACCENT = "#e3b44c"
BUTTON = "#3e5b7c"
HOVER = "#6e93bc"
DISABLED = "#555555"
HP_COLOR = "#c93b32"
MP_COLOR = "#4f7fdc"
CHIP = "#3e9c8c"

# Fonts
FONT_TITLE = ("Arial", 28, "bold")
FONT_HEAD = ("Arial", 16, "bold")
FONT_BODY = ("Arial", 12)
FONT_SMALL = ("Arial", 10)
FONT_LOG = ("Consolas", 10)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


class HoverButton(tk.Button):
    """A Button that changes colour on mouse Enter/Leave. Use for every clickable."""

    def __init__(self, master, text="", command=None, **kw):
        """Same arguments as tk.Button; colours default to the theme."""
        kw.setdefault("bg", BUTTON)
        kw.setdefault("fg", FG)
        kw.setdefault("activebackground", HOVER)
        kw.setdefault("font", FONT_BODY)
        kw.setdefault("relief", "flat")
        kw.setdefault("cursor", "hand2")
        super().__init__(master, text=text, command=command, **kw)
        self._normal_bg = kw["bg"]
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        if str(self["state"]) != "disabled":
            self["bg"] = HOVER

    def _on_leave(self, event):
        self["bg"] = self._normal_bg


def bind_hover(widget, normal_bg, hover_bg):
    """Give any widget (Label, Canvas, portrait) Enter/Leave hover colours."""
    widget.bind("<Enter>", lambda e: widget.configure(bg=hover_bg))
    widget.bind("<Leave>", lambda e: widget.configure(bg=normal_bg))


def load_sprite(name):
    """tk.PhotoImage of assets/<name>.png, or None if the file is missing.

    The caller MUST keep a reference (e.g. self.img = ...) or Tk drops the image.
    """
    path = os.path.join(ASSETS, name + ".png")
    if not os.path.exists(path):
        return None
    return tk.PhotoImage(file=path)
