"""Battle: one fight. Composes its Enemy, borrows the Hero, keeps the battle log.

Owner: Lead (backup: Daniel). CONTRACT SKELETON.
Every log string is written inline, right where its event happens.
"""

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
        raise NotImplementedError("Lead")

    def special_label(self):
        """'Shield Bash (10 MP)', or 'Shield Bash - need 4 MP' when short."""
        raise NotImplementedError("Lead")

    def can_potion(self):
        """True if the hero has a Health Potion."""
        raise NotImplementedError("Lead")

    def player_action(self, action):
        """Run one hero action from ACTIONS, if it is the player's turn.

        Order: act and log -> enemy.check_phase() -> win check (log win,
        hero.gain_essence lines) -> hero.end_turn() lines -> turn = "enemy".
        An unaffordable special or a missing potion logs a refusal and
        does NOT use the turn.
        """
        raise NotImplementedError("Lead")

    def enemy_turn(self):
        """Run the enemy's turn, if it is the enemy's turn.

        Order: STUN skip (log) or choose_action() -> basic/special attack
        and log -> loss check (log) -> enemy.end_turn() -> round += 1 ->
        turn = "player".
        """
        raise NotImplementedError("Lead")
