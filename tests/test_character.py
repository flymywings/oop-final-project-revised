"""Character tests that need only models/character.py (green from hour 1:30).

Uses tiny test doubles, so they pass before heroes/enemies/items exist.
Run: python -m pytest -q
"""

import random

import pytest

from models.character import BLOCK, CRIT_UP, REGEN, Character


class Dummy(Character):
    """Smallest concrete Character: configurable stats and gear, no abilities."""

    BASE_HP = 10_000          # big pool so hp never clamps at 0 during a test

    def __init__(self, stats=None, attack=0, defense=0):
        self.STATS = stats or {}
        self._attack = attack
        self._defense = defense
        super().__init__("Dummy")

    def gear_bonus(self, key):
        return {"attack": self._attack, "defense": self._defense}.get(key, 0)

    def special_attack(self, target, rng):
        return "special"

    def describe(self):
        return "dummy"


def test_character_is_abstract():
    with pytest.raises(TypeError):
        Character("x")


def test_damage_never_below_one():
    rng = random.Random(1)
    weak = Dummy(attack=1)
    wall = Dummy(defense=999)
    for _ in range(300):
        before = wall.hp
        weak.light_attack(wall, rng)
        assert before - wall.hp >= 1


def test_block_halves_but_keeps_minimum_one():
    rng = random.Random(2)
    weak = Dummy(attack=1)
    wall = Dummy(defense=999)
    wall.add_status(BLOCK)
    before = wall.hp
    line = weak.light_attack(wall, rng)
    assert before - wall.hp == 1
    assert "BLOCKED" in line
    assert not wall.has_status(BLOCK)


def test_light_never_dodged_but_heavy_can_be():
    rng = random.Random(3)
    hitter = Dummy(attack=20)
    dodger = Dummy(stats={"DEX": 100})          # dodge capped at 35 %
    assert dodger.dodge == 35
    for _ in range(500):
        dodger.full_heal()
        before = dodger.hp
        hitter.light_attack(dodger, rng)
        assert dodger.hp < before
    lines = [hitter.heavy_attack(dodger, rng) for _ in range(200)]
    assert any("DODGED" in line or "MISS" in line for line in lines)


def test_crit_up_forces_crit_and_is_used_up():
    rng = random.Random(4)
    hitter = Dummy(attack=20)
    target = Dummy()
    hitter.add_status(CRIT_UP)
    assert "CRIT" in hitter.light_attack(target, rng)
    assert not hitter.has_status(CRIT_UP)


def test_hp_setter_validates_and_clamps():
    d = Dummy()
    d.hp = -50
    assert d.hp == 0 and not d.is_alive
    d.hp = 10 ** 9
    assert d.hp == d.max_hp
    with pytest.raises(TypeError):
        d.hp = 3.5


def test_end_turn_regen_and_mana():
    d = Dummy(stats={"SPR": 20})
    d.mana = 0
    d.hp = 100
    d.add_status(REGEN, 3)
    d.end_turn()
    assert d.mana == 4
    assert d.hp == 100 + int(d.max_hp * 0.04)
    d.end_turn()
    d.end_turn()
    assert not d.has_status(REGEN)


def test_statuses_property_is_a_copy():
    d = Dummy()
    d.statuses["STUN"] = 1
    assert not d.has_status("STUN")


def test_derived_stats_use_int():
    d = Dummy(stats={"DEX": 12, "LUCK": 2})
    assert d.dodge == pytest.approx(15.2)         # docx: Goblin dodge 15.2 %
    assert d.crit == pytest.approx(15.8)          # docx: Goblin crit 15.8 %
    assert isinstance(d.max_hp, int) and isinstance(d.max_mana, int)
