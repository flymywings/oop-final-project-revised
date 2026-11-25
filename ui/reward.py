"""RewardScreen: pick 1 of 3 items, each card shows the stat change.

Owner: Joseph. CONTRACT SKELETON: keep the class name and the
__init__(self, master, app) signature; build the rest with ui/theme.py.
Reads: app.game.offers, item.describe(), app.game.reward_delta(item), app.game.hero.
Calls: app.game.claim_reward(item), then app.show().
"""

import tkinter as tk

from ui import theme


class RewardScreen(tk.Frame):
    """Three item cards (HoverButton). One click claims and moves on."""

    def __init__(self, master, app):
        """Build one card per offer."""
        super().__init__(master, bg=theme.BG)
        self.app = app
        tk.Label(self, text="RewardScreen - Joseph TODO", font=theme.FONT_HEAD,
                 bg=theme.BG, fg=theme.FG).pack(pady=40)

    def pick(self, item):
        """game.claim_reward(item), then app.show()."""
