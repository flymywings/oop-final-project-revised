"""Character: the abstract root of every combatant, hero or enemy.

Owns the six stats, the private HP and mana pools, the status dict,
the Light and Heavy verbs and the ONE damage pipeline (_roll_damage).
Rule for this package: models/ and logic/ contain no GUI code.

Owner: Lead.
"""

from abc import ABC, abstractmethod

# Status names. Statuses live in a plain dict {name: turns}.
BLOCK = "BLOCK"        # next incoming hit x0.5 (min 1), used up by that hit
REGEN = "REGEN"        # heal 4 % of max HP at the end of each own turn
STUN = "STUN"          # skip the next action, used up by that skip
CRIT_UP = "CRIT UP"    # next attack is a crit, used up by that attack

STAT_NAMES = ("STR", "DEX", "INT", "VIT", "SPR", "LUCK")

MANA_REGEN = 4         # +4 mana per turn, both sides
REGEN_PCT = 0.04       # REGEN heals 4 % of max HP per turn
HEAVY_MISS_PCT = 30    # Heavy misses 30 % of the time
LIGHT_SCALE = 1.0
HEAVY_SCALE = 1.5
BLOCK_SCALE = 0.5


class Character(ABC):
    """Abstract combatant: stats, HP and mana, statuses, verbs, damage pipeline."""

    # Class constants. Every leaf class overrides these (docx Tables 22, 23, 25).
    BASE_HP = 1
    HP_PCT = 1.0
    BASE_MANA = 0
    MANA_PCT = 1.0
    CRIT_MULT = 1.5
    STATS = {}              # e.g. {"STR": 16, "DEX": 6, ...}; missing stats are 0
    MANA_COST = 0           # mana price of special_attack()
    SPECIAL_NAME = "Special"

    def __init__(self, name):
        """Copy the class stats into this instance, then fill HP and mana."""
        self.name = name
        # Each instance gets its own copy, so a level-up never changes the class.
        self._stats = {stat: self.STATS.get(stat, 0) for stat in STAT_NAMES}
        self.__statuses = {}
        self.__hp = self.max_hp
        self.__mana = self.max_mana

    # ---------- stats ----------

    def stat(self, name):
        """Trained stat plus any gear bonus (accessories add STR, LUCK, ...)."""
        return self._stats[name] + self.gear_bonus(name)

    def gear_bonus(self, key):
        """Bonus from gear for 'attack', 'focus', 'defense' or a stat name. Hook: 0."""
        return 0

    def damage_bonus(self):
        """Multiplier on outgoing raw damage. Hook: 1.0; Orc and bosses override."""
        return 1.0

    def grow(self, growth):
        """Add a growth row like {"STR": 2, "VIT": 2} to the trained stats."""
        for stat, amount in growth.items():
            self._stats[stat] += amount
        # Re-assign through the setters so HP and mana clamp to the new maximums.
        self.hp = self.hp
        self.mana = self.mana

    # ---------- derived stats: read-only, int() never round() ----------

    @property
    def max_hp(self):
        """int((BASE_HP + VIT*2) * HP_PCT)."""
        return int((self.BASE_HP + self.stat("VIT") * 2) * self.HP_PCT)

    @property
    def max_mana(self):
        """int((BASE_MANA + SPR*1.5) * MANA_PCT)."""
        return int((self.BASE_MANA + self.stat("SPR") * 1.5) * self.MANA_PCT)

    @property
    def attack_power(self):
        """weapon attack + STR//2."""
        return self.gear_bonus("attack") + self.stat("STR") // 2

    @property
    def spell_power(self):
        """INT*2 + weapon focus + armor focus."""
        return self.stat("INT") * 2 + self.gear_bonus("focus")

    @property
    def defense(self):
        """Armor only; accessories and levels add none."""
        return self.gear_bonus("defense")

    @property
    def dodge(self):
        """Dodge chance in percent: min(35, DEX*1.2 + LUCK*0.4)."""
        return min(35, self.stat("DEX") * 1.2 + self.stat("LUCK") * 0.4)

    @property
    def crit(self):
        """Crit chance in percent: min(50, 5 + DEX*0.8 + LUCK*0.6)."""
        return min(50, 5 + self.stat("DEX") * 0.8 + self.stat("LUCK") * 0.6)

    # ---------- private pools behind validated properties ----------

    @property
    def hp(self):
        """Current HP, always within [0, max_hp]."""
        return self.__hp

    @hp.setter
    def hp(self, value):
        if not isinstance(value, int):
            raise TypeError("hp must be an int")
        self.__hp = max(0, min(value, self.max_hp))

    @property
    def mana(self):
        """Current mana, always within [0, max_mana]."""
        return self.__mana

    @mana.setter
    def mana(self, value):
        if not isinstance(value, int):
            raise TypeError("mana must be an int")
        self.__mana = max(0, min(value, self.max_mana))

    @property
    def is_alive(self):
        """True while HP is above 0."""
        return self.__hp > 0

    def heal(self, amount):
        """Heal by int(amount), clamped to max_hp. Returns the HP actually gained."""
        before = self.__hp
        self.hp = self.__hp + int(amount)
        return self.__hp - before

    def full_heal(self):
        """Victory reset: full HP, full mana, no statuses."""
        self.__hp = self.max_hp
        self.__mana = self.max_mana
        self.__statuses.clear()

    # ---------- statuses ----------

    @property
    def statuses(self):
        """A copy of the status dict {name: turns}, safe for the UI to read."""
        return dict(self.__statuses)

    def add_status(self, name, turns=1):
        """Set a status for a number of turns (re-adding refreshes, never stacks)."""
        self.__statuses[name] = turns

    def has_status(self, name):
        """True if the status is active."""
        return name in self.__statuses

    def consume_status(self, name):
        """Remove the status if present. Returns True if it was there."""
        if name in self.__statuses:
            del self.__statuses[name]
            return True
        return False

    def end_turn(self):
        """End of this side's turn: +4 mana and the REGEN tick. Returns log lines."""
        lines = []
        self.mana = self.__mana + MANA_REGEN
        if REGEN in self.__statuses:
            healed = self.heal(max(1, int(self.max_hp * REGEN_PCT)))
            lines.append(f"{self.name} regenerates {healed} HP.")
            self.__statuses[REGEN] -= 1
            if self.__statuses[REGEN] <= 0:
                del self.__statuses[REGEN]
                lines.append(f"{self.name}'s REGEN fades.")
        return lines

    # ---------- the three verbs ----------

    def light_attack(self, target, rng):
        """Light: 1.0x attack power, cannot be dodged, free. Returns a log line."""
        return self._roll_damage(target, self.attack_power * LIGHT_SCALE, rng,
                                 "Light Attack", dodgeable=False)

    def heavy_attack(self, target, rng):
        """Heavy: 1.5x attack power, 30 % miss, can be dodged, free. Returns a log line."""
        if rng.random() * 100 < HEAVY_MISS_PCT:
            return f"{self.name}'s Heavy Attack misses {target.name}! (MISS)"
        return self._roll_damage(target, self.attack_power * HEAVY_SCALE, rng,
                                 "Heavy Attack")

    def can_special(self):
        """True if there is enough mana for special_attack()."""
        return self.__mana >= self.MANA_COST

    def use_special(self, target, rng):
        """Pay MANA_COST, then run this class's special_attack(). Refuses if short."""
        if not self.can_special():
            short = self.MANA_COST - self.__mana
            return f"{self.name} needs {short} more MP for {self.SPECIAL_NAME}."
        self.mana = self.__mana - self.MANA_COST
        return self.special_attack(target, rng)

    @abstractmethod
    def special_attack(self, target, rng):
        """The class ability. Mana is already paid. Returns one log line."""

    @abstractmethod
    def describe(self):
        """One line describing this character, for the UI."""

    # ---------- the ONE damage pipeline ----------

    def _roll_damage(self, target, power, rng, label,
                     dodgeable=True, ignore_armor=False, force_crit=False):
        """raw -> crit -> dodge -> armor -> BLOCK -> apply. Returns a log line.

        power        attack_power or spell_power times the move's multiplier
        dodgeable    False only for Light Attack
        ignore_armor True for spells and boss slam/breath (skips step 4)
        force_crit   True for Backstab
        """
        tags = []

        # 1. Raw damage (Orc and bosses add their damage_bonus here).
        raw = power * self.damage_bonus()

        # 2. Crit. CRIT UP is used up by this attack whether or not it was needed.
        crit_up = self.consume_status(CRIT_UP)
        if force_crit or crit_up or rng.random() * 100 < self.crit:
            raw = raw * self.CRIT_MULT
            tags.append("CRIT")

        # 3. Dodge. A dodged hit deals 0, even a crit.
        if dodgeable and rng.random() * 100 < target.dodge:
            return f"{self.name}'s {label} is DODGED by {target.name}!"

        # 4. Armor: max(1, raw - defense). Spells and slams skip the subtraction.
        damage = int(raw)
        if ignore_armor:
            tags.append("ignores armor")
        else:
            damage = damage - target.defense
        damage = max(1, damage)

        # 5. BLOCK halves this hit (minimum 1) and is used up.
        if target.consume_status(BLOCK):
            damage = max(1, int(damage * BLOCK_SCALE))
            tags.append("BLOCKED")

        # 6. Apply. The hp setter clamps at 0.
        target.hp = target.hp - damage
        note = f" [{', '.join(tags)}]" if tags else ""
        return f"{self.name}'s {label} hits {target.name} for {damage}{note}."

    # ---------- read-only helpers for the UI ----------

    @property
    def sprite_name(self):
        """File stem of this character's sprite: assets/<sprite_name>.png."""
        return type(self).__name__.lower()

    def snapshot(self):
        """Stats and derived stats as a dict of ints, for stat text and deltas."""
        data = {stat: self.stat(stat) for stat in STAT_NAMES}
        data["HP"] = self.max_hp
        data["MP"] = self.max_mana
        data["ATK"] = self.attack_power
        data["SPELL"] = self.spell_power
        data["DEF"] = self.defense
        data["DODGE"] = int(self.dodge)
        data["CRIT"] = int(self.crit)
        return data
