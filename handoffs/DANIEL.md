# Daniel's handoff: heroes and enemies

## The game in 10 seconds
You pick a hero (Knight, Thief, Jester, Sorcerer or Druid). You fight 4 monsters in a row, one at a time, by clicking buttons. Beat all 4 and you win.

## Your job in one sentence
Make the 5 heroes and 4 monsters actually *do* their moves.

## Your files (touch ONLY these)
- `models/heroes.py`
- `models/enemies.py`

Everything else belongs to someone else. If you think another file is wrong, tell the Lead. Don't fix it yourself.

## Deadline
- Done by **3:30**, so the Lead can start playtesting.
- Backup job: if the Lead disappears, you take `logic/battle.py`. Its docstrings list every step in order.

---

## Step 0: Set up (10 min)
1. Get the project folder, **either** way:
   - **With git:** `git clone <REPO-URL>` (the Lead sends you the link), then `cd` into the folder.
   - **Without git:** ask the Lead for the zip, unzip it, and open a terminal in that folder.
2. Check Python: `python --version` must say 3.12.
3. Install the test tool: `pip install pytest`
4. Run the tests: `python -m pytest -q`. Lots of red is normal. Red means "not built yet".

## Step 1: Understand the 3 ideas you need (5 min)

**Idea 1: the class constants are already filled in.**
Open `models/heroes.py`. The Knight already has its HP, stats, growth and mana cost. Don't change those numbers. You only replace the lines that say `raise NotImplementedError("Daniel")`.

**Idea 2: ALL damage goes through one machine, `_roll_damage`.**
It lives in `models/character.py` (the Lead's file, already done). Think of it as a vending machine: you put in "how hard" and "what kind of hit", and it handles crits, dodges, armor and blocks. It also lowers the target's HP and hands back a sentence for the battle log.

```python
self._roll_damage(target, power, rng, "Name Of Move",
                  dodgeable=True,       # False only for Light Attack (already done)
                  ignore_armor=False,   # True for spells and boss slam/breath
                  force_crit=False)     # True only for Backstab
```

It **returns a string** (the log line). Your `special_attack` returns that string, maybe with a bit more text added.

Example (Sorcerer, basically the whole answer):
```python
def special_attack(self, target, rng):
    return self._roll_damage(target, self.spell_power * 1.0, rng, "Fireball", ignore_armor=True)
```

**Idea 3: `rng` is the dice.**
Never `import random` in your files. Use the `rng` you are given: `rng.randint(1, 6)` rolls a d6. The game passes in the dice so tests can replay the exact same game.

Useful helpers already on every character: `self.heal(amount)` (returns how much it healed), `self.add_status(BLOCK)`, `target.add_status(STUN, 1)`, `self.add_status(REGEN, 3)`, `self.stat("LUCK")`, `self.max_hp`, `self.attack_power`, `self.spell_power`, `self.hp`.

## Step 2: heroes.py, in this order
1. `Hero.potion_count()`: `return self.inventory.count("Health Potion")`
2. `Hero.use_potion()`: find a potion in the inventory, remove it, return `potion.apply(self)`.
3. `Hero.gain_essence(amount)`: add to `self.essence`. Count how many of `LEVEL_THRESHOLDS` (25, 55, 90) you've passed. If that means a higher level than now, call `level_up()` **once only**. Return a list of log strings.
4. `Hero.level_up()`: `self.level += 1`, `self.grow(self.GROWTH)`, return `"LEVEL UP! Knight is now Lv2."`
5. `Hero.describe()`: return `"Knight Lv2 - Shield Bash (10 MP)"`
6. The 5 specials:
   - **Knight**: hit for `attack_power * 0.8`, then `self.add_status(BLOCK)`.
   - **Thief**: hit for `attack_power * 1.5` with `force_crit=True`.
   - **Jester**: hit for `spell_power * 0.5` (ignore_armor). Then `roll = rng.randint(1, 6) + self.stat("LUCK") // 5`:
     - 4 or less: `self.add_status(CRIT_UP)`
     - 5-6: `target.add_status(STUN)`
     - 7-8: `self.heal(self.max_hp * 0.2)`
     - 9 or more: one more hit for `spell_power * 1.5` (ignore_armor)
   - **Sorcerer**: the example above.
   - **Druid**: `self.heal(self.max_hp * 0.25)`, `self.add_status(REGEN, 3)`, then hit for `spell_power * 0.5` (ignore_armor).

## Step 3: enemies.py, in this order
1. `Enemy.describe()`: `"Goblin - 67 HP, 24 ATK"`
2. `Goblin.choose_action()` and `Orc.choose_action()`: `return "attack"`
3. `Orc.damage_bonus()`: `1.25` if `self.hp < self.max_hp * 0.5`, else `1.0`
4. `BossEnemy.check_phase()`: if `self.phase == 1` and HP is under `PHASE_AT * max_hp`, set `self.phase = 2` and return `f"{self.name} {self.PHASE_TEXT}"`. Otherwise return `None`. It must only fire once.
5. `BossEnemy.damage_bonus()`: `self.PHASE_BONUS` in phase 2, else `1.0`
6. `BossEnemy.special_attack()`: hit for `attack_power * self.SPECIAL_SCALE`, label `self.SPECIAL_NAME`, `ignore_armor=True`.
7. Both bosses' `choose_action()`: `self.turns_taken += 1`, return `"special"` every 3rd turn, else `"attack"`.

## Rules (please don't break these)
- Don't rename anything or change any `def` line. Other people's code calls these exact names.
- Use `int()`, never `round()`.
- Only `@property` and `@abstractmethod` decorators. No dataclasses.
- Never write the word `tkinter` anywhere in `models/`. A test checks for it.
- No new features (no gold, no shop, no extra moves).

## How you know you're done
```
python -m pytest -q tests/test_models.py
```
Every hero and enemy test is green. Item tests may stay red until TJ pushes (around 2:30). That's fine.

## Push your work
```
git pull
git add models/heroes.py models/enemies.py
git commit -m "Heroes and enemies"
git push
```

### No git? Send your code to the Lead instead
That's fine. The Lead checks it and puts it in the project for you.
1. Run the "How you know you're done" check first, and write in your message whether it passed (copy the last line it printed).
2. Send **only your files**: `models/heroes.py` and `models/enemies.py`.
3. Send the **whole file** as an attachment (or the zip of those files), not a pasted piece of it. Keep the exact file names.
4. Each time you send a newer version, send the whole file again, so there's never a question about which copy is the latest.
5. TJ's `models/items.py` lands around 2:30. The Lead sends you a fresh zip, and then the kitted tests can go green.

## Stuck for more than 10 minutes?
Message the Lead with the error text. Don't spend 30 minutes alone, because we don't have them.

---

## Copy-paste prompt for your AI
Paste this, then paste `models/character.py`, `models/heroes.py`, `models/enemies.py` and `models/items.py`.
```
You are helping a sophomore finish ONE file pair for a graded Python 3.12 OOP project.
I own models/heroes.py and models/enemies.py ONLY. I paste: models/character.py (do not change it),
my two skeleton files, and models/items.py (read-only).
Fill every `raise NotImplementedError` body. Do NOT rename, add or remove classes, methods,
parameters or constants. Do NOT add features. Rules:
- Every damage number goes through self._roll_damage(target, power, rng, label, dodgeable=...,
  ignore_armor=..., force_crit=...). Never subtract HP by hand except through heal().
- special_attack(self, target, rng) returns ONE log string. Mana is already paid by use_special().
- Use int(), never round(). No decorators except @property and @abstractmethod. No dataclasses.
- No GUI imports and never write the word "tkinter" in models/.
- Spells (Trick, Fireball, Rejuvenate damage) and boss slam/breath use ignore_armor=True.
- gain_essence levels up at most once per call; level_up calls self.grow(self.GROWTH).
- Abilities: Knight 0.8x attack then BLOCK; Thief 1.5x attack force_crit; Jester 0.5x spell then
  roll=rng.randint(1,6)+LUCK//5: <=4 CRIT UP self, 5-6 STUN target, 7-8 heal 20% max HP,
  >=9 extra 1.5x spell hit; Sorcerer 1.0x spell; Druid heal 25% max HP, REGEN 3 turns, 0.5x spell.
- Bosses: choose_action increments turns_taken, 'special' every 3rd turn; check_phase switches
  phase 1->2 once below PHASE_AT and returns the log line, else None.
Keep the code short and readable for a sophomore. Then run python -m pytest -q tests/test_models.py
and show me the output.
```
