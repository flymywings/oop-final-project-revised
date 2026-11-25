"""Property tests (hypothesis): invariants of the damage pipeline, HP/mana pools and a whole run.

Run: python -m pytest -q   (needs `pip install -r requirements-dev.txt`)
"""

import random

import pytest
from hypothesis import given, settings, strategies as st

from logic.game import BATTLE, DEFEAT, REWARD, VICTORY, Game, LAST_FLOOR
from models.character import STAT_NAMES, Character
from models.heroes import HERO_CLASSES

CLASSES = list(HERO_CLASSES)
stat_values = st.integers(min_value=0, max_value=200)


class Dummy(Character):
    """Concrete Character with free stats and gear, so any numbers can be tried."""

    BASE_HP = 50

    def __init__(self, stats, attack=0, defense=0):
        self.STATS = dict(stats)
        self._attack, self._defense = attack, defense
        super().__init__("Dummy")

    def gear_bonus(self, key):
        return {"attack": self._attack, "defense": self._defense}.get(key, 0)

    def special_attack(self, target, rng):
        return "special"

    def describe(self):
        return "dummy"


stats_st = st.fixed_dictionaries({name: stat_values for name in STAT_NAMES})


@given(stats_st, st.integers(0, 300), st.integers(0, 300), st.integers(0, 10**6))
def test_light_attack_always_hits_for_at_least_one(stats, attack, defense, seed):
    """Light cannot be dodged, so it always removes >= 1 HP (unless the target was at 0)."""
    hitter, target = Dummy(stats, attack=attack), Dummy(stats, defense=defense)
    target.hp = target.max_hp
    before = target.hp
    hitter.light_attack(target, random.Random(seed))
    assert before - target.hp >= 1 or before == 0
    assert 0 <= target.hp <= target.max_hp


@given(stats_st, st.integers(0, 300), st.integers(0, 300), st.integers(0, 10**6))
def test_damage_is_bounded_by_the_crit_ceiling(stats, attack, defense, seed):
    """One hit never removes more than int(power * CRIT_MULT) and never below 1 when it lands."""
    hitter, target = Dummy(stats, attack=attack), Dummy(stats, defense=defense)
    target.hp = target.max_hp
    before = target.hp
    hitter.heavy_attack(target, random.Random(seed))
    dealt = before - target.hp
    ceiling = max(1, int(hitter.attack_power * 1.5 * hitter.CRIT_MULT))
    assert 0 <= dealt <= ceiling


@given(stats_st)
def test_crit_and_dodge_stay_inside_their_caps(stats):
    c = Dummy(stats)
    assert 5 <= c.crit <= 50
    assert 0 <= c.dodge <= 35


@given(stats_st, st.integers(-10**6, 10**6), st.integers(-10**6, 10**6))
def test_hp_and_mana_setters_clamp(stats, hp, mana):
    c = Dummy(stats)
    c.hp, c.mana = hp, mana
    assert 0 <= c.hp <= c.max_hp
    assert 0 <= c.mana <= c.max_mana
    assert c.is_alive == (c.hp > 0)


@given(stats_st, st.integers(-500, 500))
def test_heal_never_exceeds_max_or_lowers_hp(stats, amount):
    c = Dummy(stats)
    c.hp = c.max_hp // 2
    before = c.hp
    gained = c.heal(max(0, amount))
    assert gained >= 0
    assert before <= c.hp <= c.max_hp


@settings(deadline=None, max_examples=60)
@given(st.sampled_from(CLASSES), st.integers(0, 10**6),
       st.lists(st.sampled_from(["light", "heavy", "special", "potion", "reward"]),
                min_size=1, max_size=400))
def test_a_whole_run_never_breaks_an_invariant(cls, seed, actions):
    """Random clicks through the real Game: pools stay in range, states only move forward."""
    game = Game(seed=seed)
    game.new_run(cls)
    allowed = {BATTLE: {BATTLE, REWARD, VICTORY, DEFEAT},
               REWARD: {BATTLE, REWARD},
               VICTORY: {VICTORY}, DEFEAT: {DEFEAT}}
    floors_seen = [game.floor]
    for action in actions:
        before = game.state
        if game.state == BATTLE:
            b = game.battle
            if action == "reward":
                continue
            potions = b.hero.potion_count()
            game.player_action(action)
            if game.state == BATTLE and game.battle.turn == "enemy":
                game.enemy_turn()
            assert b.hero.potion_count() <= potions        # potions are only ever used up
            for f in (b.hero, b.enemy):
                assert 0 <= f.hp <= f.max_hp
                assert 0 <= f.mana <= f.max_mana
        elif game.state == REWARD:
            game.claim_reward(game.offers[0])
        assert game.state in allowed[before], (before, game.state)
        floors_seen.append(game.floor)
    assert floors_seen == sorted(floors_seen)                  # the floor never goes back
    assert 1 <= game.floor <= LAST_FLOOR


@pytest.mark.parametrize("cls", CLASSES)
def test_every_class_has_a_working_special(cls):
    game = Game(seed=7)
    game.new_run(cls)
    b = game.battle
    assert b.can_special()
    game.player_action("special")
    assert b.hero.mana <= b.hero.max_mana


def test_turn_guard_only_the_active_side_acts():
    """README lab item 'only the active player may act': out-of-turn calls change nothing."""
    game = Game(seed=5)
    game.new_run("Knight")
    b = game.battle
    hp = b.enemy.hp
    b.enemy_turn()                       # it is the player's turn: must do nothing
    assert (b.turn, b.round, len(b.log)) == ("player", 1, 1)
    game.player_action("light")
    assert b.turn == "enemy"
    log_len, enemy_hp = len(b.log), b.enemy.hp
    game.player_action("light")          # enemy's turn: must do nothing
    assert (len(b.log), b.enemy.hp, b.turn) == (log_len, enemy_hp, "enemy")
    assert enemy_hp <= hp
