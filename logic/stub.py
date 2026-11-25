"""StubGame / StubBattle: fake objects with the SAME surface as Game and Battle.

Owner: Lead. The UI team runs against this before the real models exist:
    python main.py stub
Imports nothing from models/, so it works on day one. Delete nothing here
when the real code lands; it stays as the UI's test double.
"""

STATES = ("menu", "battle", "reward", "victory", "defeat")


class StubItem:
    """Looks like an Item: name, slot, describe()."""

    def __init__(self, name, slot, text):
        self.name = name
        self.slot = slot
        self._text = text

    def describe(self):
        """One line for the reward card."""
        return f"{self.name}: {self._text}"


class StubFighter:
    """Looks like a Hero or Enemy to the UI (read-only use)."""

    SPECIAL_NAME = "Shield Bash"
    MANA_COST = 10

    def __init__(self, name, sprite_name, max_hp, max_mana):
        self.name = name
        self.sprite_name = sprite_name
        self.level = 1
        self.max_hp = max_hp
        self.max_mana = max_mana
        self.hp = max_hp
        self.mana = max_mana
        self.statuses = {}
        self._potions = 1

    def describe(self):
        """One line of text."""
        return f"{self.name} Lv{self.level} - {self.SPECIAL_NAME} ({self.MANA_COST} MP)"

    def potion_count(self):
        """Health Potions left."""
        return self._potions

    def snapshot(self):
        """Fake stat block, same keys as Character.snapshot()."""
        return {"STR": 16, "DEX": 6, "INT": 5, "VIT": 16, "SPR": 5, "LUCK": 5,
                "HP": self.max_hp, "MP": self.max_mana, "ATK": 16, "SPELL": 10,
                "DEF": 2, "DODGE": 9, "CRIT": 12}


class StubBattle:
    """Same attributes and methods as logic.battle.Battle, fixed fake numbers."""

    def __init__(self, hero, floor):
        names = ["Goblin", "Orc", "Ogre Warlord", "Elder Dragon"]
        self.hero = hero
        self.enemy = StubFighter(names[floor - 1],
                                 names[floor - 1].replace(" ", "").lower(),
                                 40 + 20 * floor, 0)
        self.floor = floor
        self.log = [f"Floor {floor}: {self.enemy.name} appears!"]
        self.turn = "player"
        self.round = 1
        self.winner = None

    @property
    def over(self):
        return self.winner is not None

    def can_special(self):
        return self.hero.mana >= self.hero.MANA_COST

    def special_label(self):
        h = self.hero
        if self.can_special():
            return f"{h.SPECIAL_NAME} ({h.MANA_COST} MP)"
        return f"{h.SPECIAL_NAME} - need {h.MANA_COST - h.mana} MP"

    def can_potion(self):
        return self.hero.potion_count() > 0

    def player_action(self, action):
        if self.over or self.turn != "player":
            return
        h, e = self.hero, self.enemy
        if action == "special":
            if not self.can_special():
                self.log.append("Not enough mana.")
                return
            h.mana -= h.MANA_COST
            e.hp = max(0, e.hp - 25)
            h.statuses["BLOCK"] = 1
            self.log.append(f"{h.name}'s {h.SPECIAL_NAME} hits {e.name} for 25 [CRIT].")
        elif action == "potion":
            if not self.can_potion():
                self.log.append("No potions left.")
                return
            h._potions -= 1
            h.hp = min(h.max_hp, h.hp + 35)
            self.log.append(f"{h.name} drinks Health Potion: +35 HP.")
        elif action == "heavy":
            e.hp = max(0, e.hp - 18)
            self.log.append(f"{h.name}'s Heavy Attack hits {e.name} for 18.")
        else:
            e.hp = max(0, e.hp - 12)
            self.log.append(f"{h.name}'s Light Attack hits {e.name} for 12.")
        if e.hp <= 0:
            self.winner = "hero"
            self.log.append(f"{e.name} is defeated! {h.name} wins.")
            return
        h.mana = min(h.max_mana, h.mana + 4)
        self.turn = "enemy"

    def enemy_turn(self):
        if self.over or self.turn != "enemy":
            return
        h, e = self.hero, self.enemy
        # 9, 13, 17, 21 by floor: on floor 4 Light-only loses and Heavy-only wins,
        # so the UI team can reach both the victory and the defeat screens.
        hit = 5 + 4 * self.floor
        damage = hit // 2 if h.statuses.pop("BLOCK", None) else hit
        h.hp = max(0, h.hp - damage)
        self.log.append(f"{e.name}'s attack hits {h.name} for {damage}.")
        if h.hp <= 0:
            self.winner = "enemy"
            self.log.append(f"{h.name} is defeated...")
            return
        self.round += 1
        self.turn = "player"


class StubGame:
    """Same attributes and methods as logic.game.Game."""

    CLASS_NAMES = ["Knight", "Thief", "Jester", "Sorcerer", "Druid"]

    def __init__(self, seed=None):
        self.restart()

    def restart(self):
        self.hero = None
        self.battle = None
        self.floor = 0
        self.offers = []
        self.state = "menu"

    def class_preview(self, class_name):
        fake = StubFighter(class_name, class_name.lower(), 150, 30)
        return fake.describe(), fake.snapshot()

    def new_run(self, class_name):
        self.hero = StubFighter(class_name, class_name.lower(), 150, 30)
        self.floor = 1
        self.battle = StubBattle(self.hero, self.floor)
        self.state = "battle"

    def player_action(self, action):
        self.battle.player_action(action)
        self._update_state()

    def enemy_turn(self):
        self.battle.enemy_turn()
        self._update_state()

    def _update_state(self):
        if self.battle.winner == "hero":
            if self.floor == 4:
                self.state = "victory"
            else:
                self.offers = [StubItem("Warhammer", "weapon", "+15 attack"),
                               StubItem("Plate Armor", "armor", "+8 defense"),
                               StubItem("Health Potion", None, "heals 35 HP")]
                self.state = "reward"
        elif self.battle.winner == "enemy":
            self.state = "defeat"

    def reward_delta(self, item):
        return {"weapon": "ATK 16 -> 23", "armor": "DEF 2 -> 8"}.get(item.slot, "+1 potion")

    def claim_reward(self, item):
        self.hero.level += 1
        self.hero.hp, self.hero.mana = self.hero.max_hp, self.hero.max_mana
        self.floor += 1
        self.battle = StubBattle(self.hero, self.floor)
        self.offers = []
        self.state = "battle"
