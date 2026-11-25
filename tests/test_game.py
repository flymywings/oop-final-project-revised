"""Battle and Game tests (green when the whole model + logic layer is done)."""

from logic.game import Game


def test_restart_resets_the_hero():
    game = Game(seed=1)
    game.new_run("Knight")
    first = game.hero
    first.hp = 5
    first.gain_essence(25)
    game.restart()
    assert game.hero is None and game.battle is None and game.state == "menu"
    game.new_run("Knight")
    hero = game.hero
    assert hero is not first
    assert hero.level == 1 and hero.essence == 0 and hero.hp == hero.max_hp
    assert game.floor == 1 and game.battle.enemy.name == "Goblin"
    assert game.battle.enemy.hp == game.battle.enemy.max_hp
    assert hero.inventory.owned_names() == {"Iron Sword", "Leather Vest", "Health Potion"}


def test_win_on_floor_1_goes_to_reward():
    game = Game(seed=2)
    game.new_run("Thief")
    game.battle.enemy.hp = 1
    game.player_action("light")                  # Light cannot be dodged
    assert game.battle.winner == "hero"
    assert game.state == "reward" and len(game.offers) == 3


def test_win_on_floor_4_is_victory():
    game = Game(seed=3)
    game.new_run("Sorcerer")
    game.floor = 4
    game._start_battle()
    game.battle.enemy.hp = 1
    game.player_action("light")
    assert game.state == "victory"


def test_defeat_is_detected():
    game = Game(seed=4)
    game.new_run("Jester")
    battle = game.battle
    game.hero.hp = 1
    for _ in range(100):
        battle.turn = "enemy"
        game.enemy_turn()
        if game.state == "defeat":
            break
    assert game.state == "defeat" and battle.winner == "enemy"


def test_claim_reward_heals_and_moves_on():
    game = Game(seed=5)
    game.new_run("Druid")
    game.battle.enemy.hp = 1
    game.player_action("light")
    game.hero.hp = 1
    game.claim_reward(game.offers[0])
    assert game.state == "battle" and game.floor == 2
    assert game.hero.hp == game.hero.max_hp
    assert game.hero.level == 2                  # 25 essence from the Goblin


def test_light_button_and_portrait_share_one_call():
    """The UI calls game.player_action('light') for both; refusals keep the turn."""
    game = Game(seed=6)
    game.new_run("Sorcerer")
    game.hero.mana = 0
    log_len = len(game.battle.log)
    game.player_action("special")                # unaffordable: refused, turn kept
    assert game.battle.turn == "player" and len(game.battle.log) == log_len + 1



def test_offers_are_only_upgrades_and_claiming_wears_them():
    """No dead cards: every offered piece of gear beats what the hero wears."""
    for seed in range(30):
        game = Game(seed=seed)
        game.new_run("Druid")
        game.battle.enemy.hp = 1
        game.player_action("light")
        assert game.state == "reward"
        for item in game.offers:
            if item.slot is not None:
                assert game._is_upgrade(item)
        gear = [item for item in game.offers if item.slot is not None]
        if gear:
            game.claim_reward(gear[0])
            assert game.hero.inventory.equipped(gear[0].slot) is gear[0]


def test_worse_gear_is_never_offered():
    """A hero wearing the best armor is not offered Cloth Robe."""
    from models.items import make_item
    game = Game(seed=7)
    game.new_run("Knight")
    best = make_item("Dragon Scale")
    game.hero.inventory.add(best)
    game.hero.equip(best)
    assert not game._is_upgrade(make_item("Cloth Robe"))
    assert game._is_upgrade(make_item("Lucky Coin"))        # fills the empty accessory slot
