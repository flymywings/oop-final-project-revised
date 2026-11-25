"""EndScreen (Pygame): victory or defeat, with a Restart button.

Owner: Joseph. CONTRACT: keeps the class name and the four methods
(__init__(self, app), handle_click, update, draw); everything is built with ui/theme.py.
Reads: app.game.state ("victory" or "defeat"), app.game.floor, app.game.hero.
Calls: app.game.restart(), then app.show(). That closes the Pygame window and
opens a fresh Tkinter menu.
Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
Mouse only: no key events.
"""

import pygame

from ui import theme

BIG_FONT = ("Arial", 54, "bold")     # the Victory / Defeat headline
DIM = "#8a8a99"


class EndScreen:
    """'Victory!' or 'Defeat', the floor reached, and Restart."""

    def __init__(self, app):
        """Build the fonts, the hero sprite and the Restart PgButton."""
        self.app = app
        game = app.game
        self.won = game.state == "victory"
        self.big = theme.pg_font(BIG_FONT)
        self.head = theme.pg_font(theme.FONT_HEAD)
        self.font = theme.pg_font(theme.FONT_BODY)
        self.small = theme.pg_font(theme.FONT_SMALL)
        self.sprite = theme.load_surface(game.hero.sprite_name)   # None until the PNGs exist
        self.panel = pygame.Rect(270, 270, 560, 240)
        self.restart_button = theme.PgButton((425, 560, 250, 64), "Restart", self.head)

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
        """The result, a hero panel (sprite, floor reached, hero line) and Restart."""
        game = self.app.game
        headline = "Victory!" if self.won else "Defeat"
        colour = theme.ACCENT if self.won else theme.HP_COLOR
        subtitle = "The Elder Dragon has fallen." if self.won else "Your run has ended."
        for text, font, tint, y in ((headline, self.big, colour, 130),
                                    (subtitle, self.head, theme.FG, 205)):
            image = font.render(text, True, tint)
            surface.blit(image, image.get_rect(center=(550, y)))
        pygame.draw.rect(surface, theme.PANEL, self.panel, border_radius=10)
        text_x = self.panel.x + 30
        if self.sprite is not None:
            surface.blit(self.sprite, (self.panel.x + 20, self.panel.y + 20))
            text_x = self.panel.x + 250
        floor = self.head.render(f"Floor reached: {game.floor}", True, theme.ACCENT)
        surface.blit(floor, (text_x, self.panel.y + 80))
        hero = self.font.render(game.hero.describe(), True, theme.FG)
        surface.blit(hero, (text_x, self.panel.y + 125))
        self.restart_button.draw(surface)
        hint = self.small.render("Restart takes you back to the class menu", True, DIM)
        surface.blit(hint, hint.get_rect(center=(550, 650)))
