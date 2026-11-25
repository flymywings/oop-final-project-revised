"""Items, equipment, the Health Potion, Inventory, starter kits and rewards.

Owner: TJ. CONTRACT SKELETON: keep every name and signature;
replace each `raise NotImplementedError` with the real body.
Numbers are docx Table 26 (prices dropped: no shop). Starter kits are Table 18.
"""

from abc import ABC, abstractmethod

SLOTS = ("weapon", "armor", "accessory")


class Item(ABC):
    """Abstract item: a name and a description."""

    slot = None   # Equipment sets 'weapon' / 'armor' / 'accessory'; consumables stay None

    def __init__(self, name):
        """Every item has its own name."""
        self.name = name

    @abstractmethod
    def describe(self):
        """One line for the reward card, e.g. 'Warhammer: +15 attack'."""


class Equipment(Item, ABC):
    """Abstract gear that sits in one slot and gives bonuses."""

    @abstractmethod
    def bonuses(self):
        """Dict of bonuses, keys 'attack', 'focus', 'defense' or a stat name."""


class Weapon(Equipment):
    """Weapon slot: attack and focus (focus feeds spell_power)."""

    slot = "weapon"

    def __init__(self, name, attack, focus=0):
        """A weapon with its own attack and focus."""
        super().__init__(name)
        self.attack = attack
        self.focus = focus

    def bonuses(self):
        """{'attack': attack, 'focus': focus}."""
        raise NotImplementedError("TJ")

    def describe(self):
        """e.g. 'Oak Staff: +3 attack, +14 focus'."""
        raise NotImplementedError("TJ")


class Armor(Equipment):
    """Armor slot: defense and focus."""

    slot = "armor"

    def __init__(self, name, defense, focus=0):
        """An armor with its own defense and focus."""
        super().__init__(name)
        self.defense = defense
        self.focus = focus

    def bonuses(self):
        """{'defense': defense, 'focus': focus}."""
        raise NotImplementedError("TJ")

    def describe(self):
        """e.g. 'Plate Armor: +8 defense'."""
        raise NotImplementedError("TJ")


class Accessory(Equipment):
    """Accessory slot: one stat bonus, never defense."""

    slot = "accessory"

    def __init__(self, name, stat, amount):
        """An accessory such as Lucky Coin (stat 'LUCK', amount 8)."""
        super().__init__(name)
        self.stat = stat
        self.amount = amount

    def bonuses(self):
        """{stat: amount}."""
        raise NotImplementedError("TJ")

    def describe(self):
        """e.g. 'Lucky Coin: +8 LUCK'."""
        raise NotImplementedError("TJ")


class Consumable(Item, ABC):
    """Abstract one-use item."""

    @abstractmethod
    def apply(self, hero):
        """Use the item on hero. Returns a log line."""


class Potion(Consumable):
    """Health Potion: heals a fixed amount."""

    def __init__(self, name="Health Potion", heal_amount=35):
        """A potion with its own heal amount."""
        super().__init__(name)
        self.heal_amount = heal_amount

    def apply(self, hero):
        """hero.heal(heal_amount). Returns e.g. 'Knight drinks Health Potion: +35 HP.'"""
        raise NotImplementedError("TJ")

    def describe(self):
        """'Health Potion: heals 35 HP'."""
        raise NotImplementedError("TJ")


class Inventory:
    """The hero's bag (hidden list) plus the three equipment slots."""

    def __init__(self):
        """Empty bag, empty slots."""
        self.__items = []
        self.__slots = {slot: None for slot in SLOTS}

    def add(self, item):
        """Put an item in the bag (aggregation: the item was made elsewhere)."""
        raise NotImplementedError("TJ")

    def remove(self, item):
        """Take an item out of the bag."""
        raise NotImplementedError("TJ")

    def items(self):
        """A tuple copy of the bag, never the list itself."""
        raise NotImplementedError("TJ")

    def count(self, name):
        """How many items with this name are in the bag."""
        raise NotImplementedError("TJ")

    def find(self, name):
        """First bag item with this name, or None."""
        raise NotImplementedError("TJ")

    def equipped(self, slot):
        """The item in slot, or None."""
        raise NotImplementedError("TJ")

    def equip(self, item):
        """Bag -> slot. The old item (if any) goes back to the bag and is returned."""
        raise NotImplementedError("TJ")

    def unequip(self, slot):
        """Slot -> bag. Returns the item, or None if the slot was empty."""
        raise NotImplementedError("TJ")

    def gear_bonus(self, key):
        """Sum of bonuses()[key] over the equipped items."""
        raise NotImplementedError("TJ")

    def owned_names(self):
        """Set of names in the bag and in the slots."""
        raise NotImplementedError("TJ")


# ---------- catalogue: one row per item, built fresh by make_item() ----------

CATALOGUE = {
    # weapons: (attack, focus)
    "Rusty Dagger": ("weapon", 5, 0),
    "Short Blade": ("weapon", 7, 0),
    "Iron Sword": ("weapon", 8, 0),
    "Twin Blades": ("weapon", 10, 0),
    "Gnarled Club": ("weapon", 10, 5),
    "Oak Staff": ("weapon", 3, 14),
    "Warhammer": ("weapon", 15, 0),
    # armors: (defense, focus)
    "Cloth Robe": ("armor", 1, 0),
    "Leather Vest": ("armor", 2, 0),
    "Hide Armor": ("armor", 3, 0),
    "Chainmail": ("armor", 5, 0),
    "Mage Robe": ("armor", 2, 8),
    "Plate Armor": ("armor", 8, 0),
    # accessories: (stat, amount)
    "Lucky Coin": ("accessory", "LUCK", 8),
    "Bracer of Might": ("accessory", "STR", 3),
    # consumable: (heal amount, unused)
    "Health Potion": ("potion", 35, 0),
}

STARTER_KITS = {
    "Knight": ["Iron Sword", "Leather Vest", "Health Potion"],
    "Thief": ["Rusty Dagger", "Leather Vest", "Health Potion"],
    "Jester": ["Short Blade", "Cloth Robe", "Health Potion"],
    "Sorcerer": ["Oak Staff", "Mage Robe", "Health Potion"],
    "Druid": ["Gnarled Club", "Hide Armor", "Health Potion"],
}


def make_item(name):
    """A NEW Item object for this catalogue name."""
    raise NotImplementedError("TJ")


def starter_kit(class_name):
    """New Item objects for this class's starter kit."""
    raise NotImplementedError("TJ")


def reward_choices(owned_names, rng, count=3):
    """count NEW items, distinct, none already owned (Health Potion is always allowed)."""
    raise NotImplementedError("TJ")
