"""Entry point and screen router.

Owner: Lead.
    python main.py        real game
    python main.py stub   UI against logic/stub.py (no models needed)
Rule for every screen: after calling a game method, if game.state changed,
call app.show(). Mouse only: no key bindings anywhere.
"""

import sys
import tkinter as tk

from ui.battle import BattleScreen
from ui.end import EndScreen
from ui.menu import MenuScreen
from ui.reward import RewardScreen
from ui import theme

SCREENS = {"menu": MenuScreen, "battle": BattleScreen, "reward": RewardScreen,
           "victory": EndScreen, "defeat": EndScreen}


class App(tk.Tk):
    """The one window. Shows the screen that matches game.state."""

    def __init__(self, game):
        """Build the window, then show the first screen."""
        super().__init__()
        self.game = game
        self.title("Essence of the Five")
        self.geometry("1100x720")
        self.configure(bg=theme.BG)
        self.screen = None
        self.show()

    def show(self):
        """Destroy the current screen and build the one for game.state."""
        if self.screen is not None:
            self.screen.destroy()
        self.screen = SCREENS[self.game.state](self, self)
        self.screen.pack(fill="both", expand=True)


def main():
    """Pick the real Game or the stub, then run the window."""
    if len(sys.argv) > 1 and sys.argv[1] == "stub":
        from logic.stub import StubGame
        game = StubGame()
    else:
        from logic.game import Game
        game = Game()
    App(game).mainloop()


if __name__ == "__main__":
    main()
