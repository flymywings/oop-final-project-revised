"""Enemy (abstract), BossEnemy (abstract) and the four floor enemies.

Owner: Daniel. CONTRACT SKELETON: keep every name and signature;
replace each `raise NotImplementedError` with the real body.
Stats are docx Table 25, Variant B. Essence drops are from the brief.
Balancing rule: if a fight is impossible or trivial, change BASE_HP or ATK only.
"""

from abc import ABC, abstractmethod

from models.character import Character


class Enemy(Character, ABC):
    """Abstract monster: fixed ATK/DEF, an essence drop and choose_action()."""

    ATK = 0          # used as attack_power (enemies have STR 0)
    DEF = 0          # used as defense
    ESSENCE = 0      # essence the hero gains on a win
    HP_PCT = 1.0     # so max_hp == BASE_HP (enemy VIT is 0)
    BASE_MANA = 0    # enemies have no mana pool

    def __init__(self, name):
        """A fresh enemy at full HP with an action counter at 0."""
        super().__init__(name)
        self.turns_taken = 0

    def gear_bonus(self, key):
        """Enemies have no gear: 'attack' is ATK, 'defense' is DEF, else 0."""
        return {"attack": self.ATK, "defense": self.DEF}.get(key, 0)

    def basic_attack(self, target, rng):
        """1.0x attack_power, can be dodged. Returns a log line."""
        return self._roll_damage(target, self.attack_power, rng, "attack")

    def special_attack(self, target, rng):
        """Default for plain monsters: same as basic_attack. Bosses override."""
        return self.basic_attack(target, rng)

    def check_phase(self):
        """Plain monsters have no phases. Returns None. BossEnemy overrides."""
        return None

    @abstractmethod
    def choose_action(self):
        """Return 'attack' or 'special' for this turn (may update turns_taken)."""

    def describe(self):
        """e.g. 'Goblin - 67 HP, 24 ATK'."""
        return f"{self.name} - {self.max_hp} HP, {self.ATK} ATK"


class BossEnemy(Enemy, ABC):
    """Abstract boss: big hit every 3rd turn and one HP-threshold phase change."""

    PHASE_AT = 0.5        # phase 2 starts below this fraction of max HP
    PHASE_BONUS = 1.25    # damage_bonus() in phase 2
    PHASE_TEXT = "enters phase 2!"
    SPECIAL_SCALE = 1.5   # slam / breath = 1.5x ATK, ignores armor

    def __init__(self, name):
        """A fresh boss in phase 1."""
        super().__init__(name)
        self.phase = 1

    def check_phase(self):
        """Move to phase 2 once, when HP < PHASE_AT * max_hp. Returns a log line or None."""
        if self.phase == 1 and self.hp < self.max_hp * self.PHASE_AT:
            self.phase = 2
            return f"{self.name} {self.PHASE_TEXT}"
        return None

    def damage_bonus(self):
        """PHASE_BONUS in phase 2, else 1.0."""
        if self.phase == 2:
            return self.PHASE_BONUS
        return 1.0

    def special_attack(self, target, rng):
        """_roll_damage(SPECIAL_SCALE x attack_power, label=SPECIAL_NAME,
        ignore_armor=True). Returns a log line."""
        return self._roll_damage(target, self.attack_power * self.SPECIAL_SCALE,
                                 rng, self.SPECIAL_NAME, ignore_armor=True)


class Goblin(Enemy):
    """Floor 1. Attacks only."""

    BASE_HP, ATK, DEF, ESSENCE = 67, 24, 2, 25
    STATS = {"DEX": 12, "LUCK": 2}

    def __init__(self):
        """A fresh Goblin."""
        super().__init__("Goblin")

    def choose_action(self):
        """Always 'attack'."""
        return "attack"


class Orc(Enemy):
    """Floor 2. +25 % damage while below 50 % HP."""

    BASE_HP, ATK, DEF, ESSENCE = 170, 30, 2, 30
    STATS = {"DEX": 5, "LUCK": 0}

    def __init__(self):
        """A fresh Orc."""
        super().__init__("Orc")

    def damage_bonus(self):
        """1.25 while hp < 50 % of max_hp, else 1.0."""
        if self.hp < self.max_hp * 0.5:
            return 1.25
        return 1.0

    def choose_action(self):
        """Always 'attack'."""
        return "attack"


class OgreWarlord(BossEnemy):
    """Floor 3 boss. Slam every 3rd turn; ENRAGED (+50 %) below 30 % HP."""

    BASE_HP, ATK, DEF, ESSENCE = 200, 23, 3, 35
    STATS = {"DEX": 6, "LUCK": 0}
    PHASE_AT, PHASE_BONUS, PHASE_TEXT = 0.30, 1.50, "is ENRAGED!"
    SPECIAL_NAME = "Slam"

    def __init__(self):
        """A fresh Ogre Warlord."""
        super().__init__("Ogre Warlord")

    def choose_action(self):
        """turns_taken += 1; 'special' when turns_taken % 3 == 0, else 'attack'."""
        self.turns_taken += 1
        return "special" if self.turns_taken % 3 == 0 else "attack"


class ElderDragon(BossEnemy):
    """Floor 4 boss. Breath every 3rd turn; PHASE 2 (+25 %) below 50 % HP."""

    BASE_HP, ATK, DEF, ESSENCE = 345, 23, 2, 80
    STATS = {"DEX": 7, "LUCK": 0}
    PHASE_AT, PHASE_BONUS, PHASE_TEXT = 0.50, 1.25, "enters PHASE 2!"
    SPECIAL_NAME = "Fire Breath"

    def __init__(self):
        """A fresh Elder Dragon."""
        super().__init__("Elder Dragon")

    def choose_action(self):
        """turns_taken += 1; 'special' when turns_taken % 3 == 0, else 'attack'."""
        self.turns_taken += 1
        return "special" if self.turns_taken % 3 == 0 else "attack"


FLOORS = [Goblin, Orc, OgreWarlord, ElderDragon]   # floor 1..4


def make_enemy(floor):
    """A NEW enemy for floor 1-4 (Battle calls this, so Battle owns the result)."""
    return FLOORS[floor - 1]()
