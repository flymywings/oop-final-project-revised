"""RewardScreen (Pygame): pick 1 of 3 items, each card shows the stat change.

Owner: Joseph. CONTRACT SKELETON: keep the class name and the four methods
(__init__(self, app), handle_click, update, draw); build the rest with ui/theme.py.
This placeholder is plain on purpose: it already works by mouse so the window
routing can be tested. Joseph restyles it.
Reads: app.game.offers, item.describe(), app.game.reward_delta(item), app.game.hero.
Calls: app.game.claim_reward(item), then app.show().
Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
"""

from ui import theme


class RewardScreen:
    """Three item cards (PgButton). One click claims and moves on."""

    def __init__(self, app):
        """Build one card per offer."""
        self.app = app
        self.font = theme.pg_font(theme.FONT_BODY)
        self.small = theme.pg_font(theme.FONT_SMALL)
        self.head = theme.pg_font(theme.FONT_HEAD)
        self.cards = [(item, theme.PgButton((70 + i * 330, 250, 300, 120), item.name, self.font))
                      for i, item in enumerate(app.game.offers)]

    def handle_click(self, pos):
        """A click on a card claims that item."""
        for item, card in self.cards:
            if card.hit(pos):
                self.pick(item)
                return

    def pick(self, item):
        """game.claim_reward(item), then app.show()."""
        self.app.game.claim_reward(item)
        self.app.show()

    def update(self, now_ms):
        """Nothing moves on this screen."""

    def draw(self, surface):
        """Title, then each card with its describe() line and stat change."""
        title = self.head.render("Victory! Choose a reward", True, theme.ACCENT)
        surface.blit(title, title.get_rect(center=(550, 150)))
        for item, card in self.cards:
            card.draw(surface)
            lines = (item.describe(), self.app.game.reward_delta(item))
            for i, line in enumerate(lines):
                image = self.small.render(line, True, theme.FG)
                surface.blit(image, (card.rect.x, card.rect.bottom + 12 + i * 22))
