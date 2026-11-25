"""Tests for heroes, enemies and items (green when Daniel's and TJ's files are done)."""

import random

import pytest

from models.enemies import BossEnemy, ElderDragon, Enemy, Goblin, OgreWarlord, make_enemy
from models.heroes import Druid, Hero, Knight, Sorcerer
from models.items import (Consumable, Equipment, Item, make_item, reward_choices,
                          starter_kit)


def kitted(hero_cls):
    """A hero with its starter kit added and equipped (what Game._make_hero does)."""
    hero = hero_cls()
    for item in starter_kit(hero.name):
        hero.inventory.add(item)
        if item.slot is not None:
            hero.equip(item)
    hero.full_heal()
    return hero


@pytest.mark.parametrize("cls", [Hero, Enemy, BossEnemy, Item, Equipment, Consumable])
def test_abstract_classes_cannot_be_built(cls):
    with pytest.raises(TypeError):
        cls("x")


def test_level1_numbers_match_docx_table_24():
    knight = kitted(Knight)
    assert (knight.max_hp, knight.max_mana, knight.attack_power) == (158, 27, 16)
    sorcerer = kitted(Sorcerer)
    assert (sorcerer.max_hp, sorcerer.max_mana, sorcerer.spell_power) == (101, 130, 54)
    assert kitted(Druid).max_hp == 115


def test_level_up_applies_growth():
    knight = Knight()
    knight.gain_essence(10)
    assert knight.level == 1
    knight.gain_essence(15)                       # total 25 -> Lv2
    assert knight.level == 2
    assert knight.stat("STR") == 18 and knight.stat("VIT") == 18
    assert knight.max_hp == int((100 + 18 * 2) * 1.2)


def test_level_up_only_once_per_call():
    knight = Knight()
    knight.gain_essence(200)
    assert knight.level == 2


def test_enemies_match_table_25():
    goblin = make_enemy(1)
    assert isinstance(goblin, Goblin)
    assert (goblin.max_hp, goblin.attack_power, goblin.defense) == (67, 24, 2)
    assert isinstance(make_enemy(3), OgreWarlord)
    assert isinstance(make_enemy(4), ElderDragon)


def test_boss_special_every_third_turn():
    ogre = OgreWarlord()
    actions = [ogre.choose_action() for _ in range(6)]
    assert actions == ["attack", "attack", "special"] * 2


def test_boss_phase_change_once():
    dragon = ElderDragon()
    dragon.hp = dragon.max_hp // 2 - 1
    assert dragon.check_phase() is not None
    assert dragon.check_phase() is None
    assert dragon.damage_bonus() == 1.25


def test_equip_returns_old_item_to_bag():
    knight = kitted(Knight)
    hammer = make_item("Warhammer")
    knight.inventory.add(hammer)
    old = knight.equip(hammer)
    assert old.name == "Iron Sword"
    assert knight.inventory.equipped("weapon") is hammer
    assert "Iron Sword" in [i.name for i in knight.inventory.items()]
    assert knight.attack_power == 15 + 16 // 2


def test_inventory_hides_its_list():
    knight = kitted(Knight)
    knight.inventory.items()                      # returns a copy
    with pytest.raises(AttributeError):
        knight.inventory.__items


def test_rewards_are_three_new_unowned_items():
    knight = kitted(Knight)
    owned = knight.inventory.owned_names()
    offers = reward_choices(owned, random.Random(5))
    names = [item.name for item in offers]
    assert len(offers) == 3 and len(set(names)) == 3
    assert all(n not in owned or n == "Health Potion" for n in names)


def test_potion_heals_and_is_used_up():
    knight = kitted(Knight)
    knight.hp = 50
    assert knight.potion_count() == 1
    knight.use_potion()
    assert knight.hp == 85 and knight.potion_count() == 0
