# One-day build plan

This brief cuts Complete.docx down. Where they disagree, this file and the code skeleton win.
**The contract is the code**: every class, signature and one-line docstring is already in the
skeleton files. Owners fill bodies. Nobody renames or re-signs anything without the Lead.

Run: `python main.py` (real game) or `python main.py stub` (UI against fake data).
Tests: `pip install pytest`, then `python -m pytest -q`.
GUI check: `grep -r tkinter models/ logic/` must print nothing.

---

## A. Requirement trace

| # | Requirement (lab PDF unless noted) | file::function | Shown / tested by |
|---|---|---|---|
| 1 | Playable battle game | logic/game.py::Game, main.py::App | full run per class (5:00-6:30); tests/test_game.py |
| 2 | Mouse hero selection; "clicking highlights the selected hero" (Ex 1) | ui/menu.py::MenuScreen.pick → Game.new_run | click a class: it highlights and shows its stats. Start button begins the run |
| 3 | Mouse attack buttons (Ex 2, Part 3) | ui/battle.py::BattleScreen.on_action → Battle.player_action("light"/"heavy") | demo |
| 4 | Mouse skill activation (Part 5) | Character.use_special → Knight/Thief/Jester/Sorcerer/Druid.special_attack | demo; disabled button reads "need N MP" |
| 5 | Heal button (main activity: Attack / Use Skill / Heal) | Potion button → Hero.use_potion → Potion.apply | test_potion_heals_and_is_used_up |
| 6 | Only the active player may click (Part 6) plus turn indicator | Battle.turn guard; BattleScreen disables buttons on the enemy turn; turn label | test_light_button_and_portrait_share_one_call (a refused action keeps the turn) |
| 7 | Hover effects on all buttons (Ex 3, Part 7) | ui/theme.py::HoverButton, bind_hover | demo: hover every clickable |
| 8 | Restart (Ex 4, Part 9) | ui/end.py::EndScreen.restart → Game.restart, Game.new_run | test_restart_resets_the_hero |
| 9 | Winner detection (Ex 5, Part 8) | Battle.winner, Game._update_state | test_win_on_floor_4_is_victory, test_defeat_is_detected |
| 10 | Battle log (Ex 6, Guided Challenge 3) | Battle.log (strings written inline) → BattleScreen log panel | demo; log shown in every test run |
| 11 | Images via PhotoImage (Ex 7, Guided Challenge 1) | ui/theme.py::load_sprite, assets/*.png | demo |
| 12 | Click the enemy portrait to attack (Guided Challenge 2) | portrait `<Button-1>` → on_action("light"), the same call as the Light button | demo |
| 13 | Improved GUI layout | ui/battle.py | demo |
| 14 | Max-health cap (action rules) | Character.hp setter clamps to [0, max_hp] | test_hp_setter_validates_and_clamps |
| 15 | Week 1: classes and objects | heroes, enemies, items: each instance owns its state | test_restart_resets_the_hero (new objects) |
| 16 | Week 2: encapsulation | Character.__hp/__mana with validated setters; Inventory.__items; read-only derived properties | test_hp_setter_..., test_inventory_hides_its_list |
| 17 | Week 2: abstraction | 7 ABCs: Character, Hero, Enemy, BossEnemy, Item, Equipment, Consumable | test_character_is_abstract, test_abstract_classes_cannot_be_built |
| 18 | Week 3: inheritance | Character→Hero→5; Character→Enemy→BossEnemy→2; Item→Equipment→3; Consumable→Potion; super().__init__ at every level | code walk |
| 19 | Week 3: polymorphism | special_attack (5 heroes + BossEnemy), choose_action (4 enemies), damage_bonus (Orc, BossEnemy), gear_bonus (Hero, Enemy), bonuses (3 gear), describe | test_boss_special_every_third_turn, test_level1_numbers_match_docx_table_24 |
| 20 | Week 4: composition | Game→Battle; Battle→Enemy (make_enemy inside Battle.__init__); Hero→Inventory | code walk |
| 21 | Week 4: aggregation | Inventory holds Items made by make_item() elsewhere | test_equip_returns_old_item_to_bag |
| 22 | Week 4: association | Battle borrows Hero (passed in, never created) | code walk |
| 23 | Week 5: mouse-only GUI | ui/*; no key bindings anywhere | demo; `grep -r "bind(\"<Key" ui/` is empty |
| 24 | models/ and logic/ have no GUI import (brief) | – | tests/test_no_gui_in_models.py and the grep |

### Requirements this brief misses (resolved)
1. **No rubric exists.** The lab PDF is the only grading source, so section A is the full checklist.
2. **Theme and single-player are allowed** (confirmed by the Lead). The lab's two-player Marvel vs DC setup is replaced by our own game concept, stated at the top of the README.
3. **Turn indicator (lab Part 6).** The player always goes first, with no initiative roll. Khael's card adds one label ("Round 3 - your turn" / "Enemy turn...").
4. **Heal button.** The Table 18 starter kits have no potion, so the Potion button would be dead in the F1 demo. Every starter kit gets 1 Health Potion (models/items.py STARTER_KITS).
5. **Ex 1 "clicking highlights the selected hero".** The menu click selects and highlights, then a Start button begins the run. A click that starts the run at once would skip the highlight.

---

## B. Contract

```
main.py                    Lead     App(tk.Tk) router: shows the screen for game.state
models/character.py        Lead     Character ABC: stats, pools, statuses, verbs, _roll_damage  (FULL CODE)
models/heroes.py           Daniel   Hero ABC + Knight Thief Jester Sorcerer Druid, HERO_CLASSES
models/enemies.py          Daniel   Enemy ABC, BossEnemy ABC, Goblin Orc OgreWarlord ElderDragon, make_enemy
models/items.py            TJ       Item/Equipment/Consumable ABCs, Weapon Armor Accessory Potion,
                                    Inventory, CATALOGUE, STARTER_KITS, make_item, starter_kit, reward_choices
logic/battle.py            Lead     Battle (composes Enemy, borrows Hero, owns log)
logic/game.py              Lead     Game (composes Hero + Battle; the only object the UI talks to)
logic/stub.py              Lead     StubGame/StubBattle: same surface, fake numbers (FULL CODE)
ui/theme.py                Khael    colours, fonts, HoverButton, bind_hover, load_sprite (working stub)
ui/battle.py               Khael    BattleScreen
ui/menu.py                 Joseph   MenuScreen
ui/reward.py               Joseph   RewardScreen
ui/end.py                  Joseph   EndScreen
assets/<sprite_name>.png   Khael    knight thief jester sorcerer druid goblin orc ogrewarlord elderdragon (200x200)
tests/                     TJ       test_character.py, test_models.py, test_game.py, test_no_gui_in_models.py
README.md                  Joseph
```

Exact signatures and docstrings are in each file. Dependency rule: `ui → logic → models → stdlib`. No upward imports.

### The API the UI may use (nothing else)
| Object | Read | Call |
|---|---|---|
| `app` | `app.game` | `app.show()` after any call that changed `game.state` |
| `game` | `state` ("menu", "battle", "reward", "victory", "defeat"), `CLASS_NAMES`, `hero`, `battle`, `floor`, `offers` | `class_preview(name)` → (text, stats dict), `new_run(name)`, `player_action(a)` with a in light/heavy/special/potion, `enemy_turn()`, `reward_delta(item)` → str, `claim_reward(item)`, `restart()` |
| `game.battle` | `hero`, `enemy`, `log` (list of str), `turn` ("player"/"enemy"), `round`, `over`, `winner` | `can_special()`, `special_label()`, `can_potion()` |
| hero / enemy | `name`, `level` (hero), `hp`, `max_hp`, `mana`, `max_mana`, `statuses` (dict copy), `sprite_name`, `SPECIAL_NAME`, `MANA_COST` | `describe()`, `snapshot()`, `potion_count()` (hero) |
| item | `name`, `slot` | `describe()` |

The battle-screen loop: click → `game.player_action(a)` → if state changed `app.show()` else refresh. If `battle.turn == "enemy"`: disable buttons, then `after(600, enemy_step)`. `enemy_step` → `game.enemy_turn()` → show or refresh.

### Rules fixed by the contract (decisions where the docx or brief was silent or in conflict)
- **Damage pipeline** (`Character._roll_damage`, the only place damage is computed): raw × damage_bonus → crit (CRIT UP or force_crit or roll; × CRIT_MULT) → dodge (0 damage) → `max(1, int(raw) - defense)`, where spells and boss slam/breath skip the subtraction but keep the minimum of 1 → BLOCK `max(1, int(d × 0.5))` → apply.
- **Only Light ignores dodge.** Heavy, specials and enemy attacks all roll dodge.
- **Enemies:** `attack_power = ATK` and `defense = DEF` (through `gear_bonus`). Enemy CRIT_MULT is 1.5. Neither is stated in the docx.
- **Log:** one line per action, with crit, dodge, miss, block and "ignores armor" as tags on that line. Status, phase, regen, stun-skip, level-up and win/loss each get their own line.
- **Items:** 16 rows (7 weapons, 6 armors, 2 accessories, Health Potion). The Table 18 kits alone need 5 weapons and 4 armors, so "about 10" cannot hold.
- **Rewards:** 3 distinct catalogue items not owned (Health Potion always allowed). The Table 19 tiers are dropped. **Claiming always equips into the item's slot**, and the replaced item goes to the bag. "Only into an empty slot" would make weapon and armor rewards do nothing, because the starter kit fills both slots and there is no other equip screen.
- **Knight** Bash while BLOCK is up just refreshes BLOCK (no stack, no refusal).
- **"need N MP"** shows the shortfall.
- **Levels:** 25/30/35/80 essence, thresholds 25/55/90, at most one level per `gain_essence` call. F1 Lv1, F2 Lv2, F3 Lv3, F4 Lv4.

---

## C. models/character.py
Full code is in the file. Tests in tests/test_character.py are green now.

---

## D. Build order

| Time | Who | What |
|---|---|---|
| 0:00-1:30 | Lead | Push this skeleton (done: review, then commit and push). Everyone pulls and runs `python main.py stub` and `python -m pytest -q` (17 green, 15 red until owners fill their files). |
| 1:30-2:00 | Khael | Final ui/theme.py pushed by **2:00** (names unchanged). |
| 1:30-3:30 | Daniel, TJ | heroes/enemies and items. TJ first: Inventory + make_item + starter_kit by 2:30, because Daniel's tests need them. |
| 1:30-3:30 | Lead | logic/battle.py and logic/game.py. Run test_game.py as soon as Daniel and TJ push. |
| 2:00-5:00 | Joseph | menu, reward, end on the stub. Then the README. |
| 1:30-5:00 | Khael | battle screen on the stub, then sprites. Missing PNG = coloured placeholder box. |
| ~3:30 | Lead | **First playable fight** (one class beats the Goblin): start playtesting and file bugs to the file owner. |
| 5:00 | all | **Feature freeze.** `python -m pytest -q` all green, grep empty. |
| 5:00-6:30 | Lead + all | Integration on the real Game: one full run per class (5 runs). Balance by changing enemy BASE_HP or ATK only. |
| 6:30-8:00 | all | Bug fixes only, cold playtest by a classmate outside the group, README final. |

**No-git option:** anyone can skip git and send their own files to the Lead instead. The Lead checks them, copies them into the repo and runs the tests. Then the Lead sends a fresh zip to whoever is waiting on them: items.py to Daniel at 2:30, theme.py to Joseph at 2:00, and everyone at 5:00.

### Balance warning (measured, not guessed)
A throwaway bot (special when affordable, potion under 35 % HP, always takes the first reward) ran 1000 runs per class on a reference fill of this contract. Docx Table 25 values were built for 6 floors with more gear. In this 4-floor cut they give **Orc F2 15-87 % and Dragon F4 0-45 %** (Knight 0 %, Sorcerer 1 % run win). Start the manual playtest from these values, then adjust:

| Enemy | Docx | Suggested start |
|---|---|---|
| Orc | 170 HP / 30 ATK | 110 / 22 |
| Ogre Warlord | 200 / 23 | 170 / 19 |
| Elder Dragon | 345 / 23 | 260 / 18 |

With those values, run win is Knight 18 %, Thief 30 %, Jester 64 %, Sorcerer 30 % and Druid 99 %. **Enemy-only levers cannot fix the class spread** (the Druid's sustain and the Sorcerer's lost Mana Potion). If the manual runs agree, the Lead decides whether to allow one class constant change, such as the Sorcerer's MANA_COST. The bot plays worse than a human, so treat these numbers as direction only.

---

## E. Task cards

### Lead: models/character.py (done), logic/battle.py, logic/game.py, main.py, QA
- **Done when:** tests/test_game.py is green, `python main.py` plays all 4 floors, and each class has had one full run.
- **Waits on:** Daniel (heroes, enemies) and TJ (items) for real runs. The stub covers the UI until then.
- **QA:** file each bug to the owner of the file it lives in, with the battle log lines.

### Daniel: models/heroes.py, models/enemies.py
- **Done when:** tests/test_models.py hero and enemy tests are green and `grep -r tkinter models/` is empty.
- **Waits on:** character.py (pushed), TJ's Inventory for the kitted tests.
- **Backup:** takes logic/battle.py if the Lead is pulled away. Its docstrings give the exact step order.
- **Prompt:**
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

### TJ: models/items.py, tests/
- **Done when:** the item, inventory and reward tests in tests/test_models.py are green, and the full suite passes at 5:00.
- **Waits on:** nothing. Push Inventory + make_item + starter_kit by **2:30** (Daniel's kitted tests use them).
- **Prompt:**
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

### Khael: ui/theme.py, ui/battle.py, assets/
- **Done when:** with `python main.py stub` and then `python main.py`, a full fight is playable by mouse only: hover on every clickable, HP/mana bars, status chips from `statuses`, Light/Heavy/Special/Potion buttons, disabled Special showing `special_label()`, enemy portrait click = Light, log panel, turn label, sprites. Nine 200x200 PNGs are in assets/.
- **Waits on:** nothing (stub). theme.py final by **2:00**.
- **Prompt:**
```
You are helping a sophomore build the Tkinter battle screen for a graded Python 3.12 project.
I own ui/theme.py and ui/battle.py ONLY. I paste: both files, main.py and logic/stub.py (read-only).
In theme.py keep every name and signature (colours, fonts, HoverButton, bind_hover, load_sprite);
restyle freely. Build BattleScreen(tk.Frame) with __init__(self, master, app). Rules:
- Read ONLY: app.game.battle.{hero, enemy, log, turn, round, over, can_special(), special_label(),
  can_potion()}, and on hero/enemy: name, level, hp, max_hp, mana, max_mana, statuses, sprite_name,
  plus hero.potion_count().
- Call ONLY: app.game.player_action('light'|'heavy'|'special'|'potion'), app.game.enemy_turn(),
  app.show(). After each call: if app.game.state != 'battle' call app.show() and stop.
- After a player action, if battle.turn == 'enemy': disable all buttons, show "Enemy turn...",
  then self.after(600, self.enemy_step).
- Layout: hero panel left, enemy panel right (200x200 sprite via theme.load_sprite(sprite_name);
  keep a reference on self; draw a coloured box if it returns None), HP and mana bars (Canvas
  rectangles), status chips (one small label per statuses key), a label with round and turn,
  4 HoverButtons, a read-only log panel (Text widget, last lines visible).
- Special button: text = battle.special_label(); state disabled when not can_special().
  Potion button: shows potion count, disabled when not can_potion().
- Clicking the enemy portrait (<Button-1>) calls the SAME method as the Light button. Give it
  hover with theme.bind_hover.
- Mouse only: no key bindings. No animation, no sound. Never compute game numbers in the UI.
Test with: python main.py stub
```

### Joseph: ui/menu.py, ui/reward.py, ui/end.py, README.md
- **Done when:** on the stub and then the real game, menu → battle → reward → … → victory/defeat → Restart → menu all work by mouse. README follows section G.
- **Waits on:** Khael's theme.py (stub version works now, final at 2:00).
- **Prompt:**
```
You are helping a sophomore build three small Tkinter screens for a graded Python 3.12 project.
I own ui/menu.py, ui/reward.py, ui/end.py ONLY. I paste: those files, ui/theme.py, main.py and
logic/stub.py (all read-only except mine). Keep each class name and __init__(self, master, app).
Use ONLY theme.HoverButton for clickables and theme colours and fonts. Rules:
- MenuScreen: title, one HoverButton per app.game.CLASS_NAMES. Clicking a class SELECTS it:
  highlight that button and show app.game.class_preview(name) as text (describe line plus the
  stats dict as "STR 16  DEX 6 ..." and "HP 158  MP 27  ATK 16 ..."). A Start button
  (disabled until a class is picked) calls app.game.new_run(name), then app.show().
- RewardScreen: one card per item in app.game.offers: item.describe() plus
  app.game.reward_delta(item). Clicking a card calls app.game.claim_reward(item), then app.show().
- EndScreen: "Victory!" if app.game.state == 'victory' else "Defeat", the floor reached
  (app.game.floor) and the hero's describe(). A Restart HoverButton calls app.game.restart(),
  then app.show().
- Mouse only, no key bindings, no animation. Never compute game numbers in the UI.
Test with: python main.py stub
```

---

## F. Tests
`python -m pytest -q` (headless, seeded `random.Random`). Owner: TJ. Written now.

| Brief item | Test |
|---|---|
| Character() raises TypeError | test_character.py::test_character_is_abstract; test_models.py::test_abstract_classes_cannot_be_built (6 more ABCs) |
| Damage never below 1 | test_damage_never_below_one, test_block_halves_but_keeps_minimum_one |
| Light never misses on dodge | test_light_never_dodged_but_heavy_can_be |
| Level-up applies growth | test_level_up_applies_growth, test_level_up_only_once_per_call |
| Restart resets the hero | test_game.py::test_restart_resets_the_hero |
| Victory and defeat detected | test_win_on_floor_1_goes_to_reward, test_win_on_floor_4_is_victory, test_defeat_is_detected |
| No GUI in models/ logic/ | test_no_gui_in_models.py, plus `grep -r tkinter models/ logic/` prints nothing |

Status now: 17 of 32 green on the skeleton (all of test_character.py, the grep test, and the ABC tests). The other 15 stay red until their files are filled. All 32 passed against a throwaway reference fill of this contract, so the tests and the signatures agree.

---

## G. README outline (Joseph)
1. Title, screenshot and the **game concept** (one short paragraph, it replaces the lab's Marvel vs DC): a single-player, turn-based fantasy gauntlet. Pick 1 of 5 classes and fight 4 floors (Goblin, Orc, Ogre Warlord, Elder Dragon) one enemy at a time. Win a fight to level up, pick 1 of 3 items and heal to full. Lose once and the run is over. Mouse only, and the player always acts first.
2. How to run: Python 3.12, `python main.py`; tests: `pip install pytest`, `python -m pytest -q`.
3. How to play (mouse only): pick a class, Start, Light / Heavy / Special / Potion, or click the enemy. Win: pick 1 of 3 items. Beat 4 floors.
4. The 5 classes: one line each (ability, cost).
5. The rules in 6 lines: the damage pipeline, dodge/crit formulas, statuses, levels.
6. **Week-to-file map:**

| Week | Concept | Where |
|---|---|---|
| 1 | Classes and objects | models/heroes.py, models/enemies.py, models/items.py (every instance owns its state; make_item builds new objects) |
| 2 | Encapsulation | Character.__hp / __mana behind validated properties (models/character.py); Inventory.__items (models/items.py); read-only derived stats |
| 2 | Abstraction | ABCs: Character, Hero, Enemy, BossEnemy, Item, Equipment, Consumable |
| 3 | Inheritance | Character → Hero → 5 classes; Character → Enemy → BossEnemy → OgreWarlord, ElderDragon; Item → Equipment → Weapon/Armor/Accessory; Consumable → Potion; super().__init__() at every level |
| 3 | Polymorphism | special_attack, choose_action, check_phase, damage_bonus, gear_bonus, bonuses, describe, apply |
| 4 | Composition | Game → Battle (logic/game.py); Battle → Enemy (logic/battle.py); Hero → Inventory (models/heroes.py) |
| 4 | Aggregation | Inventory → Items (models/items.py) |
| 4 | Association | Battle borrows Hero (logic/battle.py) |
| 5 | Mouse GUI | ui/menu.py, ui/battle.py, ui/reward.py, ui/end.py, ui/theme.py (HoverButton) |

7. Lab requirement checklist (section A rows 1-14, in short form).
8. File map and owners.
9. Credits: the team; sprites drawn by Khael.

---

## Could not verify. Check these.
- **Enemy damage formula and enemy CRIT_MULT:** not stated in Complete.docx. The Table 27 medians suggest the old simulator may have used a different formula. Check BALANCE_KIT.md or simulate.py if you still have them.
- **Docx numbers** were read from the text extraction of Complete.docx Tables 18, 22, 23, 25 and 26. They match Table 24 (Knight 158 HP/27 MP/16 ATK, Sorcerer 101/130/54 spell, Druid 115 HP) and Goblin dodge 15.2 % / crit 15.8 %. The figures (images) were not read.
- **macOS:** tk.Button ignores `bg`, so hover colours do not show on a Mac. If anyone demos on a Mac, HoverButton must become a Label with a click binding.
