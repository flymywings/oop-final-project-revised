"""Entry point and window router.

Owner: Lead.
    python main.py        real game
    python main.py stub   UI against logic/stub.py (no models needed)

Two toolkits, one window at a time (PLAN.md section B.1):
    state "menu"                               -> TkApp (Tkinter)  -> MenuScreen
    states "battle", "reward", "victory", "defeat" -> PygameApp (Pygame) -> its screen
Both windows share ONE game object. Rule for every screen: after calling a game
method, if game.state changed, call app.show(). Mouse only: no key bindings anywhere.
"""

import os
import sys

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # before pygame is first imported

import tkinter as tk  # noqa: E402

import pygame  # noqa: E402

from ui import theme  # noqa: E402
from ui.battle import BattleScreen  # noqa: E402
from ui.end import EndScreen  # noqa: E402
from ui.menu import MenuScreen  # noqa: E402
from ui.reward import RewardScreen  # noqa: E402

TITLE = "Essence of the Five"
SIZE = (1100, 720)
FPS = 30

TK_SCREENS = {"menu": MenuScreen}
PG_SCREENS = {"battle": BattleScreen, "reward": RewardScreen,
              "victory": EndScreen, "defeat": EndScreen}


class TkApp(tk.Tk):
    """The Tkinter window. Shows TK_SCREENS; closes itself when the state leaves them."""

    def __init__(self, game):
        """Build the window, show the screen for game.state, then take focus."""
        super().__init__()
        self.game = game
        self.closed = False
        self.screen = None
        self.title(TITLE)
        self.geometry(f"{SIZE[0]}x{SIZE[1]}")
        self.configure(bg=theme.BG)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.show()
        # Without this, the menu opened after Restart is inactive (measured on Windows 10).
        self.after(50, self.focus_force)

    def run(self):
        """Block until this window closes."""
        self.mainloop()

    def show(self):
        """Rebuild the screen for game.state, or close this window if Pygame owns that state."""
        if self.game.state not in TK_SCREENS:
            self.destroy()
            return
        if self.screen is not None:
            self.screen.destroy()
        self.screen = TK_SCREENS[self.game.state](self, self)
        self.screen.pack(fill="both", expand=True)

    def close(self):
        """The window's X: end the program."""
        self.closed = True
        self.destroy()


class PygameApp:
    """The Pygame window. Shows PG_SCREENS; ends its loop when the state leaves them."""

    def __init__(self, game):
        """Nothing opens until run()."""
        self.game = game
        self.closed = False
        self.running = False
        self.screen = None
        self.surface = None

    def run(self):
        """Open the window and loop until it closes (X) or the state goes back to Tkinter."""
        pygame.init()
        try:
            self.surface = pygame.display.set_mode(SIZE)
            pygame.display.set_caption(TITLE)
            clock = pygame.time.Clock()
            self.running = True
            self.show()
            while self.running:
                self.handle_events()
                if self.running:
                    self.screen.update(pygame.time.get_ticks())
                if self.running:
                    self.surface.fill(theme.BG)
                    self.screen.draw(self.surface)
                    pygame.display.flip()
                    clock.tick(FPS)
        finally:
            pygame.quit()

    def handle_events(self):
        """X closes the program. A left click goes to the screen this frame started with."""
        current = self.screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.closed = True
                self.running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                  and self.running and self.screen is current):
                self.screen.handle_click(event.pos)

    def show(self):
        """Build the screen for game.state, or stop the loop if Tkinter owns that state."""
        if self.game.state in PG_SCREENS:
            self.screen = PG_SCREENS[self.game.state](self)
        else:
            self.running = False


def main():
    """Pick the real Game or the stub, then hand it from window to window."""
    if len(sys.argv) > 1 and sys.argv[1] == "stub":
        from logic.stub import StubGame
        game = StubGame()
    else:
        from logic.game import Game
        game = Game()
    while True:
        if game.state not in TK_SCREENS and game.state not in PG_SCREENS:
            raise ValueError(f"no screen for game.state {game.state!r}")
        app = TkApp(game) if game.state in TK_SCREENS else PygameApp(game)
        app.run()
        if app.closed:
            break


if __name__ == "__main__":
    main()
