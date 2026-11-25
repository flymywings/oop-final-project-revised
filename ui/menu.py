"""MenuScreen: title plus class select, each class with its stats as text.

Owner: Joseph. CONTRACT SKELETON: keep the class name and the
__init__(self, master, app) signature; build the rest with ui/theme.py.
Reads: app.game.CLASS_NAMES, app.game.class_preview(name).
Calls: app.game.new_run(name), then app.show().
"""

import tkinter as tk

from ui import theme


class MenuScreen(tk.Frame):
    """Title and five class buttons (HoverButton), stats shown as text."""

    def __init__(self, master, app):
        """Build the title and one card per class."""
        super().__init__(master, bg=theme.BG)
        self.app = app
        tk.Label(self, text="MenuScreen - Joseph TODO", font=theme.FONT_HEAD,
                 bg=theme.BG, fg=theme.FG).pack(pady=40)

    def pick(self, class_name):
        """game.new_run(class_name), then app.show()."""
