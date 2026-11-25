"""EndScreen: victory or defeat, with a Restart button.

Owner: Joseph. CONTRACT SKELETON: keep the class name and the
__init__(self, master, app) signature; build the rest with ui/theme.py.
Reads: app.game.state ("victory" or "defeat"), app.game.floor, app.game.hero.
Calls: app.game.restart(), then app.show().
"""

import tkinter as tk

from ui import theme


class EndScreen(tk.Frame):
    """'Victory!' or 'Defeat', the floor reached, and Restart."""

    def __init__(self, master, app):
        """Build the message and the Restart HoverButton."""
        super().__init__(master, bg=theme.BG)
        self.app = app
        tk.Label(self, text="EndScreen - Joseph TODO", font=theme.FONT_HEAD,
                 bg=theme.BG, fg=theme.FG).pack(pady=40)

    def restart(self):
        """game.restart(), then app.show() (back to the menu)."""
