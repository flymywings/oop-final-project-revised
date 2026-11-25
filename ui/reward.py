"""RewardScreen (Pygame): pick 1 of 3 items, each card shows the stat change.

Owner: Joseph. CONTRACT: keeps the class name and the four methods
(__init__(self, app), handle_click, update, draw); everything is built with ui/theme.py.
Reads: app.game.offers, item.name, item.slot, item.describe(), app.game.reward_delta(item),
app.game.floor.
Calls: app.game.claim_reward(item), then app.show().
Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
Mouse only: no key events.
"""

from ui import theme

CARD_W, CARD_H, CARD_GAP = 320, 300, 30
CARD_Y = 210
DIM = "#8a8a99"


def wrap(text, font, width):
    """Split text into lines that each fit in width pixels."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and font.size(trial)[0] > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


class RewardScreen:
    """Three item cards (PgButton). One click claims and moves on."""

    def __init__(self, app):
        """Build one card per offer, with its text wrapped once."""
        self.app = app
        self.title = theme.pg_font(theme.FONT_TITLE)
        self.head = theme.pg_font(theme.FONT_HEAD)
        self.font = theme.pg_font(theme.FONT_BODY)
        self.small = theme.pg_font(theme.FONT_SMALL)
        offers = app.game.offers
        left = (1100 - (len(offers) * CARD_W + (len(offers) - 1) * CARD_GAP)) // 2
        # The PgButton is the whole card (hit area and hover); its label is empty
        # because draw() writes the text on top of it.
        self.cards = [(item, theme.PgButton((left + i * (CARD_W + CARD_GAP), CARD_Y, CARD_W, CARD_H),
                                            "", self.font))
                      for i, item in enumerate(offers)]
        self.texts = [((item.slot or "item").upper(),
                       wrap(item.describe(), self.font, CARD_W - 40),
                       wrap(app.game.reward_delta(item), self.font, CARD_W - 40))
                      for item, _ in self.cards]

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
        """Title, then each card with its slot, name, description and stat change."""
        title = self.title.render(f"Floor {self.app.game.floor} cleared!", True, theme.ACCENT)
        surface.blit(title, title.get_rect(center=(550, 100)))
        sub = self.head.render("Choose one reward", True, theme.FG)
        surface.blit(sub, sub.get_rect(center=(550, 150)))
        for (item, card), (slot, lines, delta) in zip(self.cards, self.texts):
            card.draw(surface)
            x, y = card.rect.x + 20, card.rect.y
            surface.blit(self.small.render(slot, True, theme.ACCENT), (x, y + 18))
            surface.blit(self.head.render(item.name, True, theme.FG), (x, y + 42))
            for i, line in enumerate(lines[:4]):
                surface.blit(self.font.render(line, True, theme.FG), (x, y + 88 + i * 24))
            # The stat change can be long (an accessory swap changes five stats): wrap it
            # and draw it upward from the bottom edge of the card.
            delta_lines = delta[:4]
            top = card.rect.bottom - 20 - len(delta_lines) * 24
            for i, line in enumerate(delta_lines):
                surface.blit(self.font.render(line, True, theme.ACCENT), (x, top + i * 24))
        hint = self.small.render("Click a card to claim it and continue", True, DIM)
        surface.blit(hint, hint.get_rect(center=(550, CARD_Y + CARD_H + 50)))
