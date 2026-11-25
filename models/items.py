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
        return {"attack": self.attack, "focus": self.focus}

    def describe(self):
        """e.g. 'Oak Staff: +3 attack, +14 focus'."""
        text = f"{self.name}: +{self.attack} attack"
        if self.focus:
            text += f", +{self.focus} focus"
        return text


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
        return {"defense": self.defense, "focus": self.focus}

    def describe(self):
        """e.g. 'Plate Armor: +8 defense'."""
        text = f"{self.name}: +{self.defense} defense"
        if self.focus:
            text += f", +{self.focus} focus"
        return text


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
        return {self.stat: self.amount}

    def describe(self):
        """e.g. 'Lucky Coin: +8 LUCK'."""
        return f"{self.name}: +{self.amount} {self.stat}"


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
        healed = hero.heal(self.heal_amount)
        return f"{hero.name} drinks {self.name}: +{healed} HP."

    def describe(self):
        """'Health Potion: heals 35 HP'."""
        return f"{self.name}: heals {self.heal_amount} HP"


class Inventory:
    """The hero's bag (hidden list) plus the three equipment slots."""

    def __init__(self):
        """Empty bag, empty slots."""
        self.__items = []
        self.__slots = {slot: None for slot in SLOTS}

    def add(self, item):
        """Put an item in the bag (aggregation: the item was made elsewhere)."""
        self.__items.append(item)

    def remove(self, item):
        """Take an item out of the bag."""
        self.__items.remove(item)

    def items(self):
        """A tuple copy of the bag, never the list itself."""
        return tuple(self.__items)

    def count(self, name):
        """How many items with this name are in the bag."""
        return sum(1 for item in self.__items if item.name == name)

    def find(self, name):
        """First bag item with this name, or None."""
        for item in self.__items:
            if item.name == name:
                return item
        return None

    def equipped(self, slot):
        """The item in slot, or None."""
        return self.__slots[slot]

    def equip(self, item):
        """Bag -> slot. The old item (if any) goes back to the bag and is returned."""
        if item not in self.__items:
            raise ValueError("item is not in the bag")
        if item.slot not in self.__slots:
            raise ValueError("item cannot be equipped")
        self.__items.remove(item)
        old = self.__slots[item.slot]
        self.__slots[item.slot] = item
        if old is not None:
            self.__items.append(old)
        return old

    def unequip(self, slot):
        """Slot -> bag. Returns the item, or None if the slot was empty."""
        item = self.__slots[slot]
        if item is None:
            return None
        self.__slots[slot] = None
        self.__items.append(item)
        return item

    def gear_bonus(self, key):
        """Sum of bonuses()[key] over the equipped items."""
        return sum(item.bonuses().get(key, 0)
                   for item in self.__slots.values() if item is not None)

    def owned_names(self):
        """Set of names in the bag and in the slots."""
        names = {item.name for item in self.__items}
        names.update(item.name for item in self.__slots.values() if item is not None)
        return names


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
    "Dragon Fang": ("weapon", 20, 0),
    "Archmage Staff": ("weapon", 6, 24),
    # armors: (defense, focus)
    "Cloth Robe": ("armor", 1, 0),
    "Leather Vest": ("armor", 2, 0),
    "Hide Armor": ("armor", 3, 0),
    "Chainmail": ("armor", 5, 0),
    "Mage Robe": ("armor", 2, 8),
    "Plate Armor": ("armor", 8, 0),
    "Dragon Scale": ("armor", 11, 0),
    "Archmage Robe": ("armor", 4, 14),
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
    kind, first, second = CATALOGUE[name]
    if kind == "weapon":
        return Weapon(name, first, second)
    if kind == "armor":
        return Armor(name, first, second)
    if kind == "accessory":
        return Accessory(name, first, second)
    if kind == "potion":
        return Potion(name, first)
    raise ValueError(f"unknown item kind: {kind}")


def starter_kit(class_name):
    """New Item objects for this class's starter kit."""
    return [make_item(name) for name in STARTER_KITS[class_name]]


def reward_choices(owned_names, rng, count=3):
    """count NEW items, distinct, none already owned (Health Potion is always allowed)."""
    pool = [name for name in CATALOGUE
            if name == "Health Potion" or name not in owned_names]
    chosen = rng.sample(pool, min(count, len(pool)))
    return [make_item(name) for name in chosen]