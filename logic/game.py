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

    def _equip_effect(self, item):
        """(is_upgrade, change text) if item replaced the one in its slot.

        Tried on a throwaway copy, so the real hero is untouched. An upgrade is a
        higher total of ATK + SPELL + DEF (the numbers that decide fights).
        """
        before = self.hero.snapshot()
        trial = copy.deepcopy(self.hero)
        trial_item = copy.deepcopy(item)
        trial.inventory.add(trial_item)
        trial.equip(trial_item)
        after = trial.snapshot()
        changes = [f"{key} {before[key]} -> {after[key]}"
                   for key in before if before[key] != after[key]]
        score = lambda stats: stats["ATK"] + stats["SPELL"] + stats["DEF"]
        return score(after) > score(before), ", ".join(changes) or "no stat change"

    def reward_delta(self, item):
        """Stat change text if item were claimed, e.g. 'ATK 16 -> 23'.
        A gear item that would not be an upgrade says 'Bag only', because claiming
        it keeps the item in the bag instead of wearing it."""
        if item.slot is None:
            return f"+1 {item.name} (have {self.hero.inventory.count(item.name)})"
        better, text = self._equip_effect(item)
        return text if better else f"Bag only (not an upgrade): {text}"

    def claim_reward(self, item):
        """Add item to the bag, equip it if it is an upgrade, full heal, next floor battle."""
        if self.state != REWARD or item not in self.offers:
            raise ValueError("that item is not on offer")
        better = item.slot is not None and self._equip_effect(item)[0]
        self.hero.inventory.add(item)
        if better:                    # wear it only if it is an upgrade; otherwise keep it in the bag
            self.hero.equip(item)
        self.hero.full_heal()
        self.floor += 1
        self.offers = []
        self._start_battle()
        self.state = BATTLE
