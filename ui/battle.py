"""BattleScreen: sprites, HP/mana bars, status chips, action buttons, log panel.

Owner: Khael. CONTRACT SKELETON: keep the class name and the
__init__(self, master, app) signature; build the rest.
Reads only: app.game.battle (hero, enemy, log, turn, round, over,
can_special(), special_label(), can_potion()). Calls only:
app.game.player_action(action), app.game.enemy_turn(), app.show().
"""

import tkinter as tk

from ui import theme

ENEMY_DELAY_MS = 600   # pause before the enemy acts, so the player sees each turn


class BattleScreen(tk.Frame):
    """One fight on screen. Mouse only."""

    def __init__(self, master, app):
        """Build widgets once, then refresh()."""
        super().__init__(master, bg=theme.BG)
        self.app = app
        tk.Label(self, text="BattleScreen - Khael TODO", font=theme.FONT_HEAD,
                 bg=theme.BG, fg=theme.FG).pack(pady=40)

    def refresh(self):
        """Redraw bars, chips, labels, button states and the log from the battle."""

    def on_action(self, action):
        """Button or enemy-portrait click: game.player_action(action), then
        app.show() if the state changed, else refresh() and, if it is now the
        enemy's turn, self.after(ENEMY_DELAY_MS, self.enemy_step)."""

    def enemy_step(self):
        """game.enemy_turn(), then app.show() if the state changed, else refresh()."""
