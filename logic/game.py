"""Game: the run. Composes the Hero and the current Battle; the UI only talks to Game.

Owner: Lead. CONTRACT SKELETON.
"""

import random

from logic.battle import Battle
from models.heroes import HERO_CLASSES
from models.items import reward_choices, starter_kit

LAST_FLOOR = 4
# state values the UI routes on
MENU, BATTLE, REWARD, VICTORY, DEFEAT = "menu", "battle", "reward", "victory", "defeat"


class Game:
    """Run state machine: menu -> battle -> reward -> ... -> victory or defeat."""

    CLASS_NAMES = list(HERO_CLASSES)

    def __init__(self, seed=None):
        """One seeded random.Random for the whole program, then an empty run."""
        self.rng = random.Random(seed)
        self.restart()

    def restart(self):
        """Drop the whole run: no hero, no battle, floor 0, state MENU."""
        self.hero = None
        self.battle = None
        self.floor = 0
        self.offers = []
        self.state = MENU

    def _make_hero(self, class_name):
        """A NEW hero of this class with its starter kit added and equipped."""
        raise NotImplementedError("Lead")

    def class_preview(self, class_name):
        """(describe() text, snapshot() dict) of a throwaway hero, for the menu."""
        raise NotImplementedError("Lead")

    def new_run(self, class_name):
        """Fresh hero, floor 1, first battle, state BATTLE."""
        raise NotImplementedError("Lead")

    def _start_battle(self):
        """self.battle = Battle(self.hero, self.floor, self.rng)."""
        raise NotImplementedError("Lead")

    def player_action(self, action):
        """Forward to battle.player_action(action), then _update_state()."""
        raise NotImplementedError("Lead")

    def enemy_turn(self):
        """Forward to battle.enemy_turn(), then _update_state()."""
        raise NotImplementedError("Lead")

    def _update_state(self):
        """Hero won: VICTORY on floor 4, else make 3 offers and go to REWARD.
        Enemy won: DEFEAT."""
        raise NotImplementedError("Lead")

    def reward_delta(self, item):
        """Stat change text if item were claimed, e.g. 'ATK 16 -> 23'."""
        raise NotImplementedError("Lead")

    def claim_reward(self, item):
        """Add item to the bag, equip it if it has a slot, full heal, next floor battle."""
        raise NotImplementedError("Lead")
