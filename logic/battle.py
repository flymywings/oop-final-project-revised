"""Battle: one fight. Composes its Enemy, borrows the Hero, keeps the battle log.

Owner: Lead (backup: Daniel).
Every log string is written inline, right where its event happens.
"""

from models.character import STUN
from models.enemies import make_enemy

ACTIONS = ("light", "heavy", "special", "potion")


class Battle:
    """One hero against one enemy. The UI reads the attributes, calls the methods."""

    def __init__(self, hero, floor, rng):
        """Borrow hero (association), CREATE the enemy (composition), start the log."""
        self.hero = hero
        self.enemy = make_enemy(floor)
        self.floor = floor
        self.rng = rng
        self.log = [f"Floor {floor}: {self.enemy.name} appears!"]
        self.turn = "player"        # "player" or "enemy"
        self.round = 1
        self.winner = None          # None, "hero" or "enemy"

    @property
    def over(self):
        """True once someone has won."""
        return self.winner is not None

    def can_special(self):
        """True if the hero can pay for the special right now."""
        return self.hero.can_special()

    def special_label(self):
        """'Shield Bash (10 MP)', or 'Shield Bash - need 4 MP' when short."""
        hero = self.hero
        if self.can_special():
            return f"{hero.SPECIAL_NAME} ({hero.MANA_COST} MP)"
        return f"{hero.SPECIAL_NAME} - need {hero.MANA_COST - hero.mana} MP"

    def can_potion(self):
        """True if the hero has a Health Potion."""
        return self.hero.potion_count() > 0

    def player_action(self, action):
        """Run one hero action from ACTIONS, if it is the player's turn.

        Order: act and log -> enemy.check_phase() -> win check (log win,
        hero.gain_essence lines) -> hero.end_turn() lines -> turn = "enemy".
        An unaffordable special or a missing potion logs a refusal and
        does NOT use the turn.
        """
        if action not in ACTIONS:
            raise ValueError(f"unknown action {action!r}")
        if self.over or self.turn != "player":
            return
        hero, enemy = self.hero, self.enemy

        # 1. Act and log. Refusals keep the turn.
        if action == "light":
            self.log.append(hero.light_attack(enemy, self.rng))
        elif action == "heavy":
            self.log.append(hero.heavy_attack(enemy, self.rng))
        elif action == "special":
            if not self.can_special():
                self.log.append(f"Not enough mana: {self.special_label()}.")
                return
            self.log.append(hero.use_special(enemy, self.rng))
        else:
            if not self.can_potion():
                self.log.append("No Health Potion left.")
                return
            self.log.append(hero.use_potion())

        # 2. Boss phase change.
        phase_line = enemy.check_phase()
        if phase_line:
            self.log.append(phase_line)

        # 3. Win check.
        if not enemy.is_alive:
            self.winner = "hero"
            self.log.append(f"{enemy.name} is defeated! {hero.name} wins.")
            self.log.extend(hero.gain_essence(enemy.ESSENCE))
            return

        # 4. End of the hero's turn: mana regen and REGEN.
        self.log.extend(hero.end_turn())
        self.turn = "enemy"

    def enemy_turn(self):
        """Run the enemy's turn, if it is the enemy's turn.

        Order: STUN skip (log) or choose_action() -> basic/special attack
        and log -> loss check (log) -> enemy.end_turn() -> round += 1 ->
        turn = "player".
        """
        if self.over or self.turn != "enemy":
            return
        hero, enemy = self.hero, self.enemy

        # 1. Stunned enemies lose this action; otherwise they pick one and act.
        if enemy.consume_status(STUN):
            self.log.append(f"{enemy.name} is stunned and skips its turn.")
        else:
            if enemy.choose_action() == "special":
                self.log.append(enemy.special_attack(hero, self.rng))
            else:
                self.log.append(enemy.basic_attack(hero, self.rng))

            # 2. Loss check.
            if not hero.is_alive:
                self.winner = "enemy"
                self.log.append(f"{hero.name} is defeated...")
                return

        # 3. End of the enemy's turn, next round.
        self.log.extend(enemy.end_turn())
        self.round += 1
        self.turn = "player"
