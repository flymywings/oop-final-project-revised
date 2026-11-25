# TJ's handoff: items, inventory and tests

## The game in 10 seconds
You pick a hero and fight 4 monsters in a row by clicking buttons. After each win you pick 1 of 3 items (a sword, armor, a potion...). Beat all 4 and you win.

## Your job in one sentence
Make the items, the hero's bag (inventory) and the "pick 1 of 3" rewards work, then keep the tests green.

## Your files (touch ONLY these)
- `models/items.py`
- everything in `tests/` (already written; you own them and keep them running)

## Deadlines
- **2:30**: push `Inventory`, `make_item` and `starter_kit`. Daniel's tests need them, so this goes first.
- **5:00**: the full test suite is green (`python -m pytest -q`).

---

## Step 0: Set up (10 min)
1. Get the project folder, **either** way:
   - **With git:** Run `git clone https://github.com/flymywings/oop-final-project-revised.git`, then `cd` into the folder. Accept the Lead's GitHub invitation before pushing.
   - **Without git:** ask the Lead for the zip, unzip it, and open a terminal in that folder.
2. `python --version` must say 3.12.
3. `pip install pytest`
4. `python -m pytest -q`. Lots of red is normal. Red means "not built yet".

## Step 1: Understand the 3 ideas you need (5 min)

**Idea 1: an item is just a small object with numbers.**
A `Weapon("Iron Sword", 8, 0)` has `attack=8` and `focus=0`. The constructors are already written. You fill in `bonuses()` and `describe()`.

`bonuses()` returns a dictionary of what the item adds:
```python
# Weapon
def bonuses(self):
    return {"attack": self.attack, "focus": self.focus}
```
Armor returns `{"defense": ..., "focus": ...}`. An accessory returns `{self.stat: self.amount}`, for example `{"LUCK": 8}`.

**Idea 2: the Inventory is a bag plus 3 slots.**
- The bag is `self.__items`, a list. The two underscores make it private: nobody outside can touch the list directly. That's the "encapsulation" the professor will ask about.
- The slots are `self.__slots`: `{"weapon": None, "armor": None, "accessory": None}`.
- **equip(item)**: take the item out of the bag and put it in its slot (`item.slot` tells you which). If something was already in that slot, put the old one back in the bag and **return it**.
- **unequip(slot)**: the reverse. Slot to bag, and return the item.
- **gear_bonus(key)**: add up `item.bonuses().get(key, 0)` for every *equipped* item (not the bag).

**Idea 3: always build NEW items.**
`make_item("Iron Sword")` reads the row from `CATALOGUE` and builds a brand-new object every time. Never keep one shared sword at the top of the file. Two heroes must never hold the same sword object.

## Step 2: items.py, in this order
1. `Weapon`, `Armor`, `Accessory`: `bonuses()` and `describe()` (for example `"Oak Staff: +3 attack, +14 focus"`).
2. `Potion.apply(hero)`: `healed = hero.heal(self.heal_amount)`, then return `"Knight drinks Health Potion: +35 HP."` `Potion.describe()`: `"Health Potion: heals 35 HP"`.
3. `Inventory`: `add`, `remove`, `items` (return `tuple(self.__items)`, a copy), `count`, `find`, `equipped`, `equip`, `unequip`, `gear_bonus`, `owned_names` (a set of names from the bag AND the slots).
4. `make_item(name)`: look up `CATALOGUE[name]`. The first value says the kind (`"weapon"`, `"armor"`, `"accessory"` or `"potion"`); build the matching class.
5. `starter_kit(class_name)`: `[make_item(n) for n in STARTER_KITS[class_name]]`
6. **Push now** (2:30 goal).
7. `reward_choices(owned_names, rng, count=3)`: list every catalogue name the hero doesn't own ("Health Potion" is always allowed). Pick 3 different ones with `rng.sample(pool, count)` and return new items. Use the `rng` you are given; never `import random`.

## Rules (please don't break these)
- Don't rename anything or change any `def` line, any CATALOGUE row or STARTER_KITS.
- No prices, no shop, no gold. They are cut.
- Only `@property` and `@abstractmethod` decorators.
- Never write the word `tkinter` in `models/`. A test checks for it.

## How you know you're done
```
python -m pytest -q tests/test_models.py
```
The equip, inventory, reward and potion tests are green. At 5:00, run `python -m pytest -q` and **everything** must be green. If a test goes red that isn't yours, tell that file's owner with the error text.

## Push your work
```
git pull
git add models/items.py tests/
git commit -m "Items and inventory"
git push
```

### No git? Send your code to the Lead instead
That's fine. The Lead checks it and puts it in the project for you.
1. Run the "How you know you're done" check first, and write in your message whether it passed (copy the last line it printed).
2. Send **only your files**: `models/items.py` (plus any file in `tests/` you changed).
3. Send the **whole file** as an attachment (or the zip of those files), not a pasted piece of it. Keep the exact file names.
4. Each time you send a newer version, send the whole file again, so there's never a question about which copy is the latest.
5. Send `models/items.py` by **2:30** even if `reward_choices` isn't done yet, because Daniel needs it. Send the rest when it's done.

## Stuck for more than 10 minutes?
Message the Lead with the error text.

---

## Copy-paste prompt for your AI
Paste this, then paste `models/items.py` and `models/character.py`.
```
You are helping a sophomore finish ONE file for a graded Python 3.12 OOP project.
I own models/items.py ONLY. I paste my skeleton file and models/character.py (read-only).
Fill every `raise NotImplementedError` body. Do NOT rename, add or remove classes, methods,
parameters, CATALOGUE rows or STARTER_KITS. Do NOT add prices, shops or features. Rules:
- Inventory keeps self.__items (list) and self.__slots (dict) private; items() returns a tuple copy.
- equip(item): item must be in the bag; move it into slots[item.slot]; put the old item (if any)
  back in the bag and return it. unequip(slot) moves it back to the bag and returns it.
- gear_bonus(key) sums item.bonuses().get(key, 0) over equipped items only.
- make_item(name) builds a NEW object from CATALOGUE every call (no shared module-level items).
- reward_choices(owned_names, rng, count=3): distinct names, none owned except "Health Potion"
  (always allowed), picked with rng.sample, returned as NEW items.
- Potion.apply(hero) uses hero.heal(amount) and returns one log string.
- No decorators except @property and @abstractmethod. No GUI imports; never write "tkinter" here.
Then run python -m pytest -q tests/test_models.py and show me the output.
```
