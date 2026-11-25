"""Shared look for both toolkits: colours, fonts, buttons, sprite loaders.

Owner: Khael. CONTRACT STUB: the names below are fixed and already work
in a plain way so Joseph can build on them. Khael restyles freely but
keeps every name and signature. Push the final version by 2:00.

Tkinter half (the menu):  FONT_*, HoverButton, bind_hover, load_sprite.
Pygame half (battle, reward, end): pg_font, PgButton, load_surface.
The colours are "#rrggbb" strings, which both toolkits accept.
Never build a Tk image or a Pygame font/surface at import time: call these
from a screen's __init__, because every window is new.
"""

import os
import tkinter as tk

import pygame

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

# Fonts (Tk tuples; pg_font turns them into Pygame fonts)
FONT_TITLE = ("Arial", 28, "bold")
FONT_HEAD = ("Arial", 16, "bold")
FONT_BODY = ("Arial", 12)
FONT_SMALL = ("Arial", 10)
FONT_LOG = ("Consolas", 10)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


# ---------- Tkinter half ----------

class HoverButton(tk.Button):
    """A Button that changes colour on mouse Enter/Leave. Use for every Tk clickable."""

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
    """Give any Tk widget (Label, Canvas, picture) Enter/Leave hover colours."""
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


# ---------- Pygame half ----------

def pg_font(spec):
    """Pygame font for a theme font tuple such as FONT_BODY.

    Tk sizes are points and Pygame sizes are pixels, so the size is scaled by 4/3.
    Call it from a screen's __init__ (Pygame is running by then), never at import time.
    """
    family, size = spec[0], spec[1]
    return pygame.font.SysFont(family.lower(), int(size * 4 / 3), bold="bold" in spec[2:])


class PgButton:
    """A Pygame button with hover. Use for every clickable in a Pygame screen."""

    def __init__(self, rect, text, font):
        """rect is (x, y, width, height); font comes from pg_font."""
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.enabled = True

    def hit(self, pos):
        """True if the button is enabled and pos is inside it."""
        return self.enabled and self.rect.collidepoint(pos)

    def draw(self, surface):
        """DISABLED when not enabled, HOVER while the mouse is over it, else BUTTON."""
        if not self.enabled:
            colour = DISABLED
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            colour = HOVER
        else:
            colour = BUTTON
        pygame.draw.rect(surface, colour, self.rect, border_radius=6)
        label = self.font.render(self.text, True, FG)
        surface.blit(label, label.get_rect(center=self.rect.center))


def load_surface(name):
    """Pygame Surface of assets/<name>.png, or None if the file is missing."""
    path = os.path.join(ASSETS, name + ".png")
    if not os.path.exists(path):
        return None
    return pygame.image.load(path)
