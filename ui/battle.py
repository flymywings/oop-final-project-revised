"""BattleScreen (Pygame): sprites, HP/mana bars, status chips, action buttons, log panel.

Owner: Khael. CONTRACT SKELETON: keep the class name and the four methods
(__init__(self, app), handle_click, update, draw); build the rest.
This placeholder is plain on purpose: it already plays a fight by mouse so
the window routing can be tested. Khael adds the sprites (theme.load_surface),
the HP and mana bars, the status chips, the portrait hover outline and the look.
Reads only: app.game.battle (hero, enemy, log, turn, round, over,
can_special(), special_label(), can_potion()). Calls only:
app.game.player_action(action), app.game.enemy_turn(), app.show().
Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
"""

import pygame

from ui import theme

ENEMY_DELAY_MS = 600   # pause before the enemy acts, so the player sees each turn
ACTIONS = ("light", "heavy", "special", "potion")


class BattleScreen:
    """One fight on screen. Mouse only."""

    def __init__(self, app):
        """Build fonts, buttons and the portrait rect once."""
        self.app = app
        self.font = theme.pg_font(theme.FONT_BODY)
        self.head = theme.pg_font(theme.FONT_HEAD)
        self.log_font = theme.pg_font(theme.FONT_LOG)
        self.enemy_due = None            # time (ms) the enemy acts, or None on the player's turn
        self.buttons = {action: theme.PgButton((100 + i * 240, 620, 210, 60), action.title(), self.font)
                        for i, action in enumerate(ACTIONS)}
        self.hero_box = pygame.Rect(100, 110, 200, 200)
        self.portrait = pygame.Rect(800, 110, 200, 200)   # click = Light attack

    def handle_click(self, pos):
        """Enemy portrait = Light. Clicks do nothing while the enemy is acting."""
        if self.enemy_due is not None:
            return
        if self.portrait.collidepoint(pos):
            self.on_action("light")
            return
        for action, button in self.buttons.items():
            if button.hit(pos):
                self.on_action(action)
                return

    def on_action(self, action):
        """game.player_action(action), then app.show() if the state changed,
        else start the enemy pause if it is now the enemy's turn."""
        game = self.app.game
        game.player_action(action)
        if game.state != "battle":
            self.app.show()
        elif game.battle.turn == "enemy":
            self.enemy_due = pygame.time.get_ticks() + ENEMY_DELAY_MS

    def update(self, now_ms):
        """When the pause is over: game.enemy_turn(), then app.show() if the state changed."""
        if self.enemy_due is not None and now_ms >= self.enemy_due:
            self.enemy_due = None
            self.app.game.enemy_turn()
            if self.app.game.state != "battle":
                self.app.show()

    def draw(self, surface):
        """Redraw everything from the battle (plain placeholder)."""
        b = self.app.game.battle
        waiting = self.enemy_due is not None
        self.buttons["light"].enabled = not waiting
        self.buttons["heavy"].enabled = not waiting
        self.buttons["special"].enabled = not waiting and b.can_special()
        self.buttons["special"].text = b.special_label()
        self.buttons["potion"].enabled = not waiting and b.can_potion()
        self.buttons["potion"].text = f"Potion ({b.hero.potion_count()})"

        turn = "Enemy turn..." if waiting else f"Round {b.round} - your turn"
        self._text(surface, turn, self.head, theme.ACCENT, (550, 40), centre=True)
        for fighter, box in ((b.hero, self.hero_box), (b.enemy, self.portrait)):
            pygame.draw.rect(surface, theme.PANEL, box)
            name = f"{fighter.name} Lv{fighter.level}" if fighter is b.hero else fighter.name
            self._text(surface, name, self.head, theme.FG, (box.x, box.y - 34))
            self._text(surface, f"HP {fighter.hp}/{fighter.max_hp}   MP {fighter.mana}/{fighter.max_mana}",
                       self.font, theme.FG, (box.x, box.bottom + 10))
            if fighter.statuses:
                self._text(surface, "  ".join(fighter.statuses), self.font, theme.CHIP,
                           (box.x, box.bottom + 36))
        for i, line in enumerate(b.log[-8:]):
            self._text(surface, line, self.log_font, theme.FG, (100, 380 + i * 26))
        for button in self.buttons.values():
            button.draw(surface)

    @staticmethod
    def _text(surface, text, font, colour, pos, centre=False):
        image = font.render(text, True, colour)
        rect = image.get_rect(center=pos) if centre else image.get_rect(topleft=pos)
        surface.blit(image, rect)
