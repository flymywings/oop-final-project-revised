"""Game: the run. Composes the Hero and the current Battle; the UI only talks to Game.

Owner: Lead.
"""

import copy
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
        hero = HERO_CLASSES[class_name]()
        for item in starter_kit(class_name):
            hero.inventory.add(item)
            if item.slot is not None:
                hero.equip(item)
        hero.full_heal()          # gear can change the maximums, so start full
        return hero

    def class_preview(self, class_name):
        """(describe() text, snapshot() dict) of a throwaway hero, for the menu."""
        hero = self._make_hero(class_name)
        return hero.describe(), hero.snapshot()

    def new_run(self, class_name):
        """Fresh hero, floor 1, first battle, state BATTLE."""
        self.hero = self._make_hero(class_name)
        self.floor = 1
        self.offers = []
        self._start_battle()
        self.state = BATTLE

    def _start_battle(self):
        """self.battle = Battle(self.hero, self.floor, self.rng)."""
        self.battle = Battle(self.hero, self.floor, self.rng)

    def player_action(self, action):
        """Forward to battle.player_action(action), then _update_state()."""
        if self.state != BATTLE:
            return
        self.battle.player_action(action)
        self._update_state()

    def enemy_turn(self):
        """Forward to battle.enemy_turn(), then _update_state()."""
        if self.state != BATTLE:
            return
        self.battle.enemy_turn()
        self._update_state()

    def _update_state(self):
        """Hero won: VICTORY on floor 4, else make 3 offers and go to REWARD.
        Enemy won: DEFEAT."""
        if self.battle.winner == "hero":
            if self.floor >= LAST_FLOOR:
                self.state = VICTORY
            else:
                self.offers = reward_choices(self.hero.inventory.owned_names(), self.rng)
                self.state = REWARD
        elif self.battle.winner == "enemy":
            self.state = DEFEAT

    def reward_delta(self, item):
        """Stat change text if item were claimed, e.g. 'ATK 16 -> 23'."""
        if item.slot is None:
            return f"+1 {item.name} (have {self.hero.inventory.count(item.name)})"
        before = self.hero.snapshot()
        trial = copy.deepcopy(self.hero)          # a throwaway copy: the real hero is untouched
        trial_item = copy.deepcopy(item)
        trial.inventory.add(trial_item)
        trial.equip(trial_item)
        after = trial.snapshot()
        changes = [f"{key} {before[key]} -> {after[key]}"
                   for key in before if before[key] != after[key]]
        return ", ".join(changes) if changes else "no stat change"

    def claim_reward(self, item):
        """Add item to the bag, equip it if it has a slot, full heal, next floor battle."""
        if self.state != REWARD or item not in self.offers:
            raise ValueError("that item is not on offer")
        self.hero.inventory.add(item)
        if item.slot is not None:
            self.hero.equip(item)
        self.hero.full_heal()
        self.floor += 1
        self.offers = []
        self._start_battle()
        self.state = BATTLE
