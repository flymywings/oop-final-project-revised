"""BattleScreen (Pygame): sprites, HP/mana bars, status chips, action buttons, log panel.

Owner: Khael. Keeps the contract: class BattleScreen with __init__(self, app),
handle_click, update, draw.
Reads only: app.game.battle (hero, enemy, log, turn, round, over,
can_special(), special_label(), can_potion()) and on hero/enemy: name, level,
hp, max_hp, mana, max_mana, statuses, sprite_name, plus hero.potion_count().
Calls only: app.game.player_action(action), app.game.enemy_turn(), app.show().
Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
Mouse only: no key events.
"""

import pygame

from ui import sound, theme

ENEMY_DELAY_MS = 600   # pause before the enemy acts, so the player sees each turn
ACTIONS = ("light", "heavy", "special", "potion")
LOG_LINES = 7
SPRITE_SIZE = (200, 200)
BAR_W, BAR_H = 160, 18


class BattleScreen:
    """One fight on screen. Mouse only."""

    def __init__(self, app):
        """Build fonts, sprites, buttons and the rects once."""
        self.app = app
        self.font = theme.pg_font(theme.FONT_BODY)
        self.small = theme.pg_font(theme.FONT_SMALL)
        self.head = theme.pg_font(theme.FONT_HEAD)
        self.log_font = theme.pg_font(theme.FONT_LOG)
        self.enemy_due = None            # time (ms) the enemy acts, or None on the player's turn

        self.buttons = {action: theme.PgButton((50 + i * 255, 630, 235, 70), action.title(), self.font)
                        for i, action in enumerate(ACTIONS)}

        self.hero_panel = pygame.Rect(50, 60, 420, 320)
        self.enemy_panel = pygame.Rect(630, 60, 420, 320)
        self.hero_box = pygame.Rect(self.hero_panel.x + 20, self.hero_panel.y + 52, *SPRITE_SIZE)
        self.portrait = pygame.Rect(self.enemy_panel.x + 20, self.enemy_panel.y + 52, *SPRITE_SIZE)
        self.log_rect = pygame.Rect(50, 400, 1000, 210)

        b = app.game.battle
        self.hero_img = self._load(b.hero)
        self.enemy_img = self._load(b.enemy)

        bg = theme.load_surface("battle_bg")
        self.bg = pygame.transform.scale(bg, (1100, 720)) if bg else None

        # Sound: log lines already voiced, hover tracking, and mouse-only mute/volume buttons.
        self.seen = len(b.log)
        self.hover = sound.HoverTracker()
        self.sound_buttons = {"vol_down": theme.PgButton((790, 8, 44, 34), "-", self.font),
                              "vol_up": theme.PgButton((840, 8, 44, 34), "+", self.font),
                              "mute": theme.PgButton((890, 8, 160, 34), "", self.small)}
        sound.ensure()

    @staticmethod
    def _load(fighter):
        """Sprite scaled to 200x200, or None (a coloured box is drawn instead)."""
        image = theme.load_surface(fighter.sprite_name)
        if image is None:
            return None
        return pygame.transform.scale(image, SPRITE_SIZE)

    # ---------- input and timing ----------

    def handle_click(self, pos):
        """Enemy portrait = Light. Clicks do nothing while the enemy is acting."""
        for key, button in self.sound_buttons.items():     # sound controls work at any time
            if button.hit(pos):
                self._sound_button(key)
                return
        if self.enemy_due is not None:
            return
        if self.portrait.collidepoint(pos):
            sound.play("click")
            self.on_action("light")
            return
        for action, button in self.buttons.items():
            if button.hit(pos):
                sound.play("click")
                self.on_action(action)
                return

    def _sound_button(self, key):
        """Volume down, volume up, or mute."""
        if key == "mute":
            sound.toggle_mute()
        else:
            sound.change_volume(-sound.VOLUME_STEP if key == "vol_down" else sound.VOLUME_STEP)
        sound.play("click")

    def _play_log(self, battle):
        """Play a sound for every log line added since the last call."""
        for line in battle.log[self.seen:]:
            for event in sound.events_for_log_line(line, battle.hero.name, battle.enemy.name):
                sound.play(event)
        self.seen = len(battle.log)

    def on_action(self, action):
        """game.player_action(action), then app.show() if the state changed,
        else start the enemy pause if it is now the enemy's turn."""
        game = self.app.game
        battle = game.battle
        game.player_action(action)
        self._play_log(battle)
        if game.state != "battle":
            self.app.show()
            return
        if game.battle.turn == "enemy":
            self.enemy_due = pygame.time.get_ticks() + ENEMY_DELAY_MS

    def update(self, now_ms):
        """When the pause is over: game.enemy_turn(), then app.show() if the state changed."""
        rects = {key: button.rect for key, button in self.sound_buttons.items()}
        if self.enemy_due is None:
            rects.update({key: button.rect for key, button in self.buttons.items() if button.enabled})
            rects["portrait"] = self.portrait
        self.hover.update(rects, pygame.mouse.get_pos())
        if self.enemy_due is not None and now_ms >= self.enemy_due:
            self.enemy_due = None
            battle = self.app.game.battle
            self.app.game.enemy_turn()
            self._play_log(battle)
            if self.app.game.state != "battle":
                self.app.show()

    # ---------- drawing ----------

    def draw(self, surface):
        """Redraw everything from the battle."""
        b = self.app.game.battle
        waiting = self.enemy_due is not None

        if self.bg is not None:
            surface.blit(self.bg, (0, 0))

        self.buttons["light"].enabled = not waiting
        self.buttons["heavy"].enabled = not waiting
        self.buttons["special"].enabled = not waiting and b.can_special()
        self.buttons["special"].text = b.special_label()
        self.buttons["potion"].enabled = not waiting and b.can_potion()
        self.buttons["potion"].text = f"Potion ({b.hero.potion_count()})"

        turn = "Enemy turn..." if waiting else f"Round {b.round} - your turn"
        self._text(surface, turn, self.head, theme.ACCENT, (550, 32), centre=True)

        self._draw_panel(surface, self.hero_panel, self.hero_box, b.hero, self.hero_img, theme.MP_COLOR)
        self._draw_panel(surface, self.enemy_panel, self.portrait, b.enemy, self.enemy_img, theme.HP_COLOR)

        if not waiting and self.portrait.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, theme.ACCENT, self.portrait.inflate(8, 8), width=3, border_radius=4)

        self._draw_log(surface, b.log)
        for button in self.buttons.values():
            button.draw(surface)
        self.sound_buttons["mute"].text = "Muted" if sound.is_muted() else f"Sound {round(sound.volume() * 100)}%"
        for button in self.sound_buttons.values():
            button.draw(surface)

    def _draw_panel(self, surface, panel, box, fighter, image, box_colour):
        """Panel, name, sprite, bars and status chips for one fighter."""
        pygame.draw.rect(surface, theme.PANEL, panel, border_radius=10)
        pygame.draw.rect(surface, theme.PANEL_EDGE, panel, width=2, border_radius=10)
        level = getattr(fighter, "level", None)   # enemies have no level
        title = fighter.name if level is None else f"{fighter.name}  Lv{level}"
        self._text(surface, title, self.head, theme.FG,
                   (panel.x + 20, panel.y + 14))

        if image is not None:
            surface.blit(image, box)
        else:
            pygame.draw.rect(surface, box_colour, box, border_radius=4)
            self._text(surface, fighter.name[:1].upper(), self.head, theme.FG, box.center, centre=True)

        x = box.right + 20
        y = box.y
        self._bar(surface, x, y, "HP", fighter.hp, fighter.max_hp, theme.HP_COLOR)
        y += 56
        if fighter.max_mana > 0:
            self._bar(surface, x, y, "MP", fighter.mana, fighter.max_mana, theme.MP_COLOR)
            y += 56
        self._chips(surface, x, y, panel.right - 10, fighter.statuses)

    def _bar(self, surface, x, y, label, value, maximum, colour):
        """Label line, then a background bar and a filled bar."""
        self._text(surface, f"{label} {value}/{maximum}", self.small, theme.FG, (x, y))
        back = pygame.Rect(x, y + 22, BAR_W, BAR_H)
        pygame.draw.rect(surface, theme.BAR_BG, back)
        width = BAR_W * value // maximum if maximum > 0 else 0
        width = max(0, min(BAR_W, width))
        if width > 0:
            pygame.draw.rect(surface, colour, pygame.Rect(x, y + 22, width, BAR_H))
        pygame.draw.rect(surface, theme.PANEL_EDGE, back, width=1)

    def _chips(self, surface, x, y, right, statuses):
        """One small box with text per statuses key, wrapping at the panel edge."""
        start = x
        for key in statuses:
            image = self.small.render(str(key), True, theme.FG)
            rect = pygame.Rect(x, y, image.get_width() + 14, 24)
            if rect.right > right and x > start:
                x, y = start, y + 30
                rect.topleft = (x, y)
            pygame.draw.rect(surface, theme.CHIP, rect, border_radius=6)
            surface.blit(image, image.get_rect(center=rect.center))
            x = rect.right + 6

    def _draw_log(self, surface, log):
        """The last lines of battle.log, oldest first, newest brightest."""
        pygame.draw.rect(surface, theme.LOG_BG, self.log_rect, border_radius=8)
        pygame.draw.rect(surface, theme.PANEL_EDGE, self.log_rect, width=2, border_radius=8)
        lines = log[-LOG_LINES:]
        for i, line in enumerate(lines):
            colour = theme.FG if i == len(lines) - 1 else theme.FG_DIM
            self._text(surface, line, self.log_font, colour, (self.log_rect.x + 14, self.log_rect.y + 12 + i * 27))

    @staticmethod
    def _text(surface, text, font, colour, pos, centre=False):
        image = font.render(text, True, colour)
        rect = image.get_rect(center=pos) if centre else image.get_rect(topleft=pos)
        surface.blit(image, rect)