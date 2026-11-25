"""Hero (abstract) and the five playable classes.

Owner: Daniel. CONTRACT SKELETON: keep every name and signature;
replace each `raise NotImplementedError` with the real body.
Constants are docx Tables 22 (stats) and 23 (growth), with the D16 levers.
"""

from abc import ABC

from models.character import Character, BLOCK, CRIT_UP, REGEN, STUN
from models.items import Inventory


class Hero(Character, ABC):
    """Abstract player character: inventory, gear slots, essence and levels."""

    LEVEL_THRESHOLDS = (25, 55, 90)   # cumulative essence for Lv2, Lv3, Lv4
    GROWTH = {}                       # per-class stat gain on level-up

    def __init__(self, name):
        """Create the Inventory FIRST: Character.__init__ reads max_hp, which reads gear."""
        self.inventory = Inventory()       # composition: the Hero owns its Inventory
        super().__init__(name)
        self.level = 1
        self.essence = 0

    def gear_bonus(self, key):
        """Sum of equipped items' bonuses for key (delegates to Inventory)."""
        return self.inventory.gear_bonus(key)

    def equip(self, item):
        """Move item from the bag into its slot. Returns the item it replaced, or None."""
        return self.inventory.equip(item)

    def unequip(self, slot):
        """Move the item in slot back to the bag. Returns it, or None if empty."""
        return self.inventory.unequip(slot)

    def potion_count(self):
        """How many Health Potions are in the bag."""
        return self.inventory.count("Health Potion")

    def use_potion(self):
        """Drink one Health Potion (Potion.apply) and remove it. Returns a log line."""
        potion = self.inventory.find("Health Potion")
        if potion is None:
            return f"{self.name} has no Health Potion left."
        self.inventory.remove(potion)
        return potion.apply(self)

    def gain_essence(self, amount):
        """Add essence; level up at most once if a threshold is crossed. Returns log lines."""
        self.essence += int(amount)
        crossed = 0
        for threshold in self.LEVEL_THRESHOLDS:
            if self.essence >= threshold:
                crossed += 1
        lines = []
        # At most one level per call, even if 200 essence arrives at once.
        if crossed + 1 > self.level:
            lines.append(self.level_up())
        return lines

    def level_up(self):
        """level += 1 and self.grow(self.GROWTH). Returns a log line."""
        self.level += 1
        self.grow(self.GROWTH)
        return f"LEVEL UP! {self.name} is now Lv{self.level}."

    def describe(self):
        """e.g. 'Knight Lv2 - Shield Bash (10 MP)'."""
        return f"{self.name} Lv{self.level} - {self.SPECIAL_NAME} ({self.MANA_COST} MP)"


class Knight(Hero):
    """Tank. Shield Bash: 1.2x attack, then BLOCK halves the next hit taken."""

    BASE_HP, HP_PCT, BASE_MANA, MANA_PCT = 100, 1.20, 20, 1.00
    CRIT_MULT = 1.5
    STATS = {"STR": 16, "DEX": 6, "INT": 5, "VIT": 16, "SPR": 5, "LUCK": 5}
    GROWTH = {"STR": 2, "DEX": 1, "INT": 0, "VIT": 2, "SPR": 1, "LUCK": 0}
    MANA_COST, SPECIAL_NAME = 10, "Shield Bash"

    def __init__(self):
        """A fresh level-1 Knight."""
        super().__init__("Knight")

    def special_attack(self, target, rng):
        """_roll_damage(1.2x attack_power), then add_status(BLOCK). Returns a log line."""
        line = self._roll_damage(target, self.attack_power * 1.2, rng, "Shield Bash")
        self.add_status(BLOCK)
        return f"{line} {self.name} braces for the next hit (BLOCK)."


class Thief(Hero):
    """Crits. Backstab: 1.5x attack, guaranteed crit at x2.0. No gold steal."""

    BASE_HP, HP_PCT, BASE_MANA, MANA_PCT = 85, 1.00, 30, 1.00
    CRIT_MULT = 2.0
    STATS = {"STR": 9, "DEX": 16, "INT": 6, "VIT": 9, "SPR": 6, "LUCK": 9}
    GROWTH = {"STR": 1, "DEX": 2, "INT": 0, "VIT": 2, "SPR": 1, "LUCK": 0}
    MANA_COST, SPECIAL_NAME = 12, "Backstab"

    def __init__(self):
        """A fresh level-1 Thief."""
        super().__init__("Thief")

    def special_attack(self, target, rng):
        """_roll_damage(1.5x attack_power, force_crit=True). Returns a log line."""
        return self._roll_damage(target, self.attack_power * 1.5, rng,
                                 "Backstab", force_crit=True)


class Jester(Hero):
    """Chaos. Trick: 0.5x spell damage, then a d6 + LUCK//5 band."""

    BASE_HP, HP_PCT, BASE_MANA, MANA_PCT = 92, 1.00, 50, 1.00
    CRIT_MULT = 2.5
    STATS = {"STR": 11, "DEX": 11, "INT": 9, "VIT": 7, "SPR": 9, "LUCK": 15}
    GROWTH = {"STR": 2, "DEX": 2, "INT": 1, "VIT": 2, "SPR": 0, "LUCK": 1}
    MANA_COST, SPECIAL_NAME = 15, "Trick"

    def __init__(self):
        """A fresh level-1 Jester."""
        super().__init__("Jester")

    def special_attack(self, target, rng):
        """0.5x spell_power (ignore_armor), then roll = rng.randint(1, 6) + LUCK//5:
        <=4 CRIT UP on self; 5-6 STUN target 1 turn; 7-8 heal 20 % max HP;
        >=9 extra 1.5x spell_power hit. Returns one log line."""
        lines = [self._roll_damage(target, self.spell_power * 0.5, rng,
                                   "Trick", ignore_armor=True)]
        roll = rng.randint(1, 6) + self.stat("LUCK") // 5
        if roll <= 4:
            self.add_status(CRIT_UP)
            lines.append(f"{self.name} feels lucky (CRIT UP).")
        elif roll <= 6:
            target.add_status(STUN, 1)
            lines.append(f"{target.name} is stunned!")
        elif roll <= 8:
            healed = self.heal(self.max_hp * 0.2)
            lines.append(f"{self.name} heals {healed} HP.")
        else:
            lines.append(self._roll_damage(target, self.spell_power * 1.5, rng,
                                           "Wild Card", ignore_armor=True))
        return " ".join(lines)


class Sorcerer(Hero):
    """Glass cannon. Fireball: 1.0x spell damage, ignores armor."""

    BASE_HP, HP_PCT, BASE_MANA, MANA_PCT = 95, 0.95, 80, 1.25
    CRIT_MULT = 1.5
    STATS = {"STR": 5, "DEX": 8, "INT": 16, "VIT": 6, "SPR": 16, "LUCK": 7}
    GROWTH = {"STR": 0, "DEX": 1, "INT": 1, "VIT": 2, "SPR": 3, "LUCK": 0}
    MANA_COST, SPECIAL_NAME = 32, "Fireball"

    def __init__(self):
        """A fresh level-1 Sorcerer."""
        super().__init__("Sorcerer")

    def special_attack(self, target, rng):
        """_roll_damage(1.0x spell_power, ignore_armor=True). Returns a log line."""
        return self._roll_damage(target, self.spell_power * 1.0, rng,
                                 "Fireball", ignore_armor=True)


class Druid(Hero):
    """Sustain. Rejuvenate: heal 25 % max HP, REGEN 3 turns, 0.5x spell damage."""

    BASE_HP, HP_PCT, BASE_MANA, MANA_PCT = 92, 1.05, 70, 1.10
    CRIT_MULT = 1.5
    STATS = {"STR": 12, "DEX": 10, "INT": 14, "VIT": 9, "SPR": 14, "LUCK": 8}
    GROWTH = {"STR": 2, "DEX": 0, "INT": 1, "VIT": 2, "SPR": 1, "LUCK": 0}
    MANA_COST, SPECIAL_NAME = 20, "Rejuvenate"

    def __init__(self):
        """A fresh level-1 Druid."""
        super().__init__("Druid")

    def special_attack(self, target, rng):
        """heal(25 % max_hp), add_status(REGEN, 3), then 0.5x spell_power
        (ignore_armor). Returns one log line."""
        healed = self.heal(self.max_hp * 0.25)
        self.add_status(REGEN, 3)
        line = self._roll_damage(target, self.spell_power * 0.5, rng,
                                 "Rejuvenate", ignore_armor=True)
        return f"{self.name} heals {healed} HP and sets REGEN. {line}"


# Class-select order. Game builds heroes only through this dict.
HERO_CLASSES = {"Knight": Knight, "Thief": Thief, "Jester": Jester,
                "Sorcerer": Sorcerer, "Druid": Druid}
