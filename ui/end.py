"""EndScreen (Pygame): victory or defeat, with a Restart button.

Owner: Joseph. CONTRACT SKELETON: keep the class name and the four methods
(__init__(self, app), handle_click, update, draw); build the rest with ui/theme.py.
This placeholder is plain on purpose: it already works by mouse so the window
routing can be tested. Joseph restyles it.
Reads: app.game.state ("victory" or "defeat"), app.game.floor, app.game.hero.
Calls: app.game.restart(), then app.show(). That closes the Pygame window and
opens a fresh Tkinter menu.
Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
"""

from ui import theme


class EndScreen:
    """'Victory!' or 'Defeat', the floor reached, and Restart."""

    def __init__(self, app):
        """Build the fonts and the Restart PgButton."""
        self.app = app
        self.title = theme.pg_font(theme.FONT_TITLE)
        self.font = theme.pg_font(theme.FONT_BODY)
        self.restart_button = theme.PgButton((450, 480, 200, 60), "Restart", self.font)

    def handle_click(self, pos):
        """Restart is the only clickable."""
        if self.restart_button.hit(pos):
            self.restart()

    def restart(self):
        """game.restart(), then app.show() (back to the menu)."""
        self.app.game.restart()
        self.app.show()

    def update(self, now_ms):
        """Nothing moves on this screen."""

    def draw(self, surface):
        """The result, the floor reached, the hero line and Restart."""
        game = self.app.game
        text = "Victory!" if game.state == "victory" else "Defeat"
        lines = ((text, self.title, theme.ACCENT, 220),
                 (f"Floor reached: {game.floor}", self.font, theme.FG, 300),
                 (game.hero.describe(), self.font, theme.FG, 340))
        for line, font, colour, y in lines:
            image = font.render(line, True, colour)
            surface.blit(image, image.get_rect(center=(550, y)))
        self.restart_button.draw(surface)
