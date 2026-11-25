# One-day build plan

This brief cuts Complete.docx down. Where they disagree, this file and the code skeleton win.
**The contract is the code**: every class, signature and one-line docstring is already in the
skeleton files. Owners fill bodies. Nobody renames or re-signs anything without the Lead.

Install: `python -m pip install pygame pytest` (Python 3.12; Tkinter ships with Python).
Run: `python main.py` (real game) or `python main.py stub` (UI against fake data).
Tests: `python -m pytest -q`.
GUI check: `grep -rE "tkinter|pygame" models/ logic/` must print nothing.

**Two toolkits, one game.** Tkinter shows the title and class-selection screen. Pygame shows battle, rewards, victory and defeat.
One `Game` object is shared by both windows, and only one window is open at a time. [Section B.1](#b1-window-routing) is the routing contract.
**Skeleton status:** `main.py`, `ui/theme.py`, `ui/battle.py`, `ui/reward.py`, `ui/end.py` and `logic/stub.py` still contain the earlier all-Tkinter skeleton.
The Lead re-pushes them to match section B before 1:30 (see D). Until then, section B wins over those six files. Every other file already matches.

---

## A. Requirement trace

Screens: **Menu** is Tkinter. **Battle**, **Reward** and **End** (victory or defeat) are Pygame. "Demo" means the step is checked by hand with `python main.py stub`, and then with `python main.py`.

| # | Requirement (lab PDF unless noted) | Screen (toolkit) | Owner | file::function | Verify |
|---|---|---|---|---|---|
| 1 | Playable battle game | all four | Lead | main.py router, logic/game.py::Game | [acceptance check](#b1-window-routing); one full run per class (5:00-6:30); tests/test_game.py |
| 2 | Mouse hero selection; "clicking highlights the selected hero" (Ex 1) | Menu (Tk) | Joseph | ui/menu.py::MenuScreen: a class click sets `self.selected`; Start → Game.new_run(self.selected) | demo: a click highlights the class and shows its stats; Start stays grey until a class is picked |
| 3 | Mouse attack buttons (Ex 2, Part 3) | Battle (Pygame) | Khael | ui/battle.py::BattleScreen.on_action → Game.player_action("light"/"heavy") | demo: the enemy HP bar drops and a log line appears |
| 4 | Mouse skill activation (Part 5) | Battle (Pygame) | Khael (button), Daniel (specials) | Special button → Character.use_special → Knight/Thief/Jester/Sorcerer/Druid.special_attack | demo: the disabled button reads "need N MP"; test_models.py special tests |
| 5 | Heal button (main activity: Attack / Use Skill / Heal) | Battle (Pygame) | Khael (button), Daniel (use_potion), TJ (Potion) | Potion button → Hero.use_potion → Potion.apply | test_potion_heals_and_is_used_up; demo: the count drops and the button greys at 0 |
| 6 | Only the active player may click (Part 6) plus turn indicator | Battle (Pygame) | Lead (guard), Khael (screen) | Battle.turn guard; BattleScreen ignores clicks and greys buttons while the enemy acts; turn label | test_light_button_and_portrait_share_one_call (a refused action keeps the turn); demo: "Enemy turn..." shows and clicks do nothing |
| 7 | Hover effects on all buttons, including Restart (Ex 2, Ex 3, Part 7) | all four | Khael (theme), Joseph (uses it) | Tk: ui/theme.py::HoverButton, bind_hover. Pygame: ui/theme.py::PgButton (hover from the mouse position) | demo: move over every clickable on all four screens, including the enemy portrait and Restart |
| 8 | Restart (Ex 4, Part 9) | End (Pygame) → Menu (Tk) | Joseph (button), Lead (Game.restart, router) | ui/end.py::EndScreen.restart → Game.restart → app.show() closes Pygame and opens a new Tk menu | test_restart_resets_the_hero; acceptance check steps 3-5 |
| 9 | Winner detection (Ex 5, Part 8) | Battle → End (Pygame) | Lead (logic), Joseph (End text) | Battle.winner, Game._update_state → EndScreen "Victory!" / "Defeat" | test_win_on_floor_4_is_victory, test_defeat_is_detected; acceptance check steps 3 and 5 |
| 10 | Battle log (Ex 6, Guided Challenge 3) | Battle (Pygame) | Lead (Battle.log), Khael (panel) | Battle.log (strings written inline) → BattleScreen log panel (last lines drawn as text) | demo; the log is shown in every test run |
| 11 | Images; `PhotoImage` (Ex 7, Guided Challenge 1 "Display image on button") | Menu (Tk) and Battle (Pygame) | Khael (sprites, loaders), Joseph (menu buttons) | Menu: class buttons carry their sprite from theme.load_sprite (`tk.PhotoImage`). Battle: theme.load_surface (`pygame.image.load`); assets/*.png | demo: sprites on the five class buttons and in both battle panels |
| 12 | Click the enemy portrait to attack (Guided Challenge 2) | Battle (Pygame) | Khael | a left click inside the portrait rect → on_action("light"), the same call as the Light button | demo; test_light_button_and_portrait_share_one_call |
| 13 | Improved GUI layout | all four | Khael (battle, theme), Joseph (menu, reward, end) | ui/* | demo |
| 14 | Max-health cap (action rules) | – | Lead | Character.hp setter clamps to [0, max_hp] | test_hp_setter_validates_and_clamps |
| 15 | Week 1: classes and objects | – | Daniel, TJ | heroes, enemies, items: each instance owns its state | test_restart_resets_the_hero (new objects) |
| 16 | Week 2: encapsulation | – | Lead, TJ | Character.__hp/__mana with validated setters; Inventory.__items; read-only derived properties | test_hp_setter_..., test_inventory_hides_its_list |
| 17 | Week 2: abstraction | – | Lead, Daniel, TJ | 7 ABCs: Character, Hero, Enemy, BossEnemy, Item, Equipment, Consumable | test_character_is_abstract, test_abstract_classes_cannot_be_built |
| 18 | Week 3: inheritance | – | Daniel, TJ | Character→Hero→5; Character→Enemy→BossEnemy→2; Item→Equipment→3; Consumable→Potion; super().__init__ at every level | code walk |
| 19 | Week 3: polymorphism | – | Daniel, TJ | special_attack (5 heroes + BossEnemy), choose_action (4 enemies), damage_bonus (Orc, BossEnemy), gear_bonus (Hero, Enemy), bonuses (3 gear), describe | test_boss_special_every_third_turn, test_level1_numbers_match_docx_table_24 |
| 20 | Week 4: composition | – | Lead, Daniel | Game→Battle; Battle→Enemy (make_enemy inside Battle.__init__); Hero→Inventory | code walk |
| 21 | Week 4: aggregation | – | TJ | Inventory holds Items made by make_item() elsewhere | test_equip_returns_old_item_to_bag |
| 22 | Week 4: association | – | Lead | Battle borrows Hero (passed in, never created) | code walk |
| 23 | Week 5: mouse-only GUI | all four | Khael, Joseph | ui/*: no Tk key bindings, no Pygame key events | demo; the mouse-only grep in section F prints nothing |
| 24 | models/ and logic/ have no GUI import (brief) | – | TJ (test), Daniel, Lead | neither "tkinter" nor "pygame" appears in models/ or logic/ | tests/test_no_gui_in_models.py (TJ extends it to both names) and the GUI grep at the top of this file |
| 25 | One window at a time; Start, Restart and close behave as in B.1 (our contract) | Menu ↔ Pygame | Lead | main.py::main, TkApp, PygameApp | [acceptance check](#b1-window-routing), steps 1-7 |

### Requirements this brief misses (resolved)
1. **No rubric exists.** The lab PDF is the only grading source, so section A is the full checklist.
2. **Theme and single-player are allowed** (confirmed by the Lead). The lab's two-player Marvel vs DC setup is replaced by our own game concept, stated at the top of the README.
3. **Turn indicator (lab Part 6).** The player always goes first, with no initiative roll. Khael's card adds one label ("Round 3 - your turn" / "Enemy turn...").
4. **Heal button.** The Table 18 starter kits have no potion, so the Potion button would be dead in the F1 demo. Every starter kit gets 1 Health Potion (models/items.py STARTER_KITS).
5. **Ex 1 "clicking highlights the selected hero".** The menu click selects and highlights, then a Start button begins the run. A click that starts the run at once would skip the highlight.
6. **Toolkit split: an ASSUMPTION.** No newer final-project instructions were available. The sources checked were the Week 5 lab PDF, the Week 1, 3 and 4 lab PDFs, and our own Complete.docx.
   The Week 5 lab says "We will continue using Tkinter", and every lab example is Tkinter. We assume the team may choose its toolkits, as it chose its own theme (resolved item 2).
   Tkinter still carries the lab's Tkinter-specific items: `PhotoImage` hero images on buttons (row 11), and hover via `<Enter>`/`<Leave>` bindings (row 7) on the menu.
   **The Lead confirms this with the professor before 1:30.** If the answer is "Tkinter only", go back to the all-Tkinter plan in git history (commit `8ac63af`, PLAN.md and handoffs/). Do not mix the two plans.

---

## B. Contract

```
main.py                    Lead     main() router + TkApp(tk.Tk) + PygameApp: one window at a time (B.1)
models/character.py        Lead     Character ABC: stats, pools, statuses, verbs, _roll_damage  (FULL CODE)
models/heroes.py           Daniel   Hero ABC + Knight Thief Jester Sorcerer Druid, HERO_CLASSES
models/enemies.py          Daniel   Enemy ABC, BossEnemy ABC, Goblin Orc OgreWarlord ElderDragon, make_enemy
models/items.py            TJ       Item/Equipment/Consumable ABCs, Weapon Armor Accessory Potion,
                                    Inventory, CATALOGUE, STARTER_KITS, make_item, starter_kit, reward_choices
logic/battle.py            Lead     Battle (composes Enemy, borrows Hero, owns log)
logic/game.py              Lead     Game (composes Hero + Battle; the only object the UI talks to)
logic/stub.py              Lead     StubGame/StubBattle: same surface, fake numbers (FULL CODE)
ui/theme.py                Khael    shared colours + Tk: fonts, HoverButton, bind_hover, load_sprite
                                    + Pygame: pg_font, PgButton, load_surface (working stubs)
ui/menu.py                 Joseph   MenuScreen(tk.Frame)          Tkinter   state "menu"
ui/battle.py               Khael    BattleScreen                  Pygame    state "battle"
ui/reward.py               Joseph   RewardScreen                  Pygame    state "reward"
ui/end.py                  Joseph   EndScreen                     Pygame    states "victory", "defeat"
assets/<sprite_name>.png   Khael    knight thief jester sorcerer druid goblin orc ogrewarlord elderdragon (200x200)
tests/                     TJ       test_character.py, test_models.py, test_game.py, test_no_gui_in_models.py
README.md                  Joseph
```

Exact signatures and docstrings are in each file. Dependency rule: `ui → logic → models → stdlib`. No upward imports.
Only `main.py` and `ui/` import `tkinter` or `pygame`. `logic/` and `models/` never name either one.

### The API the UI may use (nothing else)
The same API serves both toolkits. Every screen, Tk or Pygame, gets the same `app` and talks only to `app.game`.

| Object | Read | Call |
|---|---|---|
| `app` (TkApp or PygameApp) | `app.game` | `app.show()` after any call that changed `game.state`. It picks the screen, or closes this window if the new state belongs to the other toolkit |
| `game` | `state` ("menu", "battle", "reward", "victory", "defeat"), `CLASS_NAMES`, `hero`, `battle`, `floor`, `offers` | `class_preview(name)` → (text, stats dict), `new_run(name)`, `player_action(a)` with a in light/heavy/special/potion, `enemy_turn()`, `reward_delta(item)` → str, `claim_reward(item)`, `restart()` |
| `game.battle` | `hero`, `enemy`, `log` (list of str), `turn` ("player"/"enemy"), `round`, `over`, `winner` | `can_special()`, `special_label()`, `can_potion()` |
| hero / enemy | `name`, `level` (hero), `hp`, `max_hp`, `mana`, `max_mana`, `statuses` (dict copy), `sprite_name`, `SPECIAL_NAME`, `MANA_COST` | `describe()`, `snapshot()`, `potion_count()` (hero) |
| item | `name`, `slot` | `describe()` |

The battle-screen loop (Pygame): click → `game.player_action(a)` → if the state changed, `app.show()`. If `battle.turn == "enemy"`, set `self.enemy_due = now + 600` ms; buttons grey out and clicks are ignored.
Each frame, `update(now_ms)` checks the time. Once `now_ms >= enemy_due`: `game.enemy_turn()`, then `app.show()` if the state changed. `draw()` always redraws from the battle, so there is no separate refresh.

### B.1 Window routing

One process, one `Game` (or `StubGame`) object, **one window open at a time**. Owner: Lead (`main.py`).

| `game.state` | Window | Screen | Owner |
|---|---|---|---|
| `menu` | Tkinter, `TkApp(tk.Tk)` | `ui/menu.py::MenuScreen(tk.Frame)`, built as `MenuScreen(master, app)` | Joseph |
| `battle` | Pygame, `PygameApp` | `ui/battle.py::BattleScreen`, built as `BattleScreen(app)` | Khael |
| `reward` | Pygame | `ui/reward.py::RewardScreen(app)` | Joseph |
| `victory`, `defeat` | Pygame | `ui/end.py::EndScreen(app)` | Joseph |

```python
TK_SCREENS = {"menu": MenuScreen}
PG_SCREENS = {"battle": BattleScreen, "reward": RewardScreen,
              "victory": EndScreen, "defeat": EndScreen}

def main():
    game = StubGame() if stub else Game()     # made ONCE; both windows use this object
    while True:
        app = TkApp(game) if game.state in TK_SCREENS else PygameApp(game)
        app.run()                             # blocks until this window closes
        if app.closed:                        # the player clicked this window's X
            break                             # so the program ends
```

Both apps have the same four members: `game`, `closed` (False until the X is clicked), `run()` and `show()`.
- **TkApp(tk.Tk):** `__init__` sets the title "Essence of the Five", the size 1100x720 and `protocol("WM_DELETE_WINDOW", self.close)`. It then calls `show()`, then `self.after(50, self.focus_force)`.
  `run()` is `mainloop()`. `show()` rebuilds the frame if `game.state` is in `TK_SCREENS`, else `self.destroy()`, so `run()` returns. `close()` sets `closed = True`, then calls `destroy()`.
- **PygameApp:** `run()` calls `pygame.init()` and opens a 1100x720 window with the same title. It then calls `show()` and loops at 30 frames per second:
  - `pygame.QUIT` sets `closed = True` and stops the loop.
  - A left `MOUSEBUTTONDOWN` goes to `screen.handle_click(event.pos)`, only while the screen is the one this frame started with.
  - Then `screen.update(pygame.time.get_ticks())`, `screen.draw(surface)` and `pygame.display.flip()`.
  - `pygame.quit()` runs in a `finally`. `show()` builds `PG_SCREENS[game.state](self)`, or stops the loop if the state is not a Pygame state.
- **Pygame screen interface** (BattleScreen, RewardScreen, EndScreen): `__init__(self, app)`, `handle_click(self, pos)`, `update(self, now_ms)`, `draw(self, surface)`. `draw` paints the whole screen every frame. Reward and End have an empty `update`.

**What each control does**

| The player | Where | Game call | Then |
|---|---|---|---|
| clicks a class | Menu (Tk) | `class_preview(name)` only | The class is highlighted and its stats shown. Nothing is created |
| clicks **Start** (grey until a class is picked) | Menu (Tk) | `new_run(selected)`: a NEW hero, floor 1, the first Battle, state `battle` | `app.show()` → the Tk window is destroyed → the router opens the Pygame window on BattleScreen |
| wins, loses, or claims a reward | Pygame | as in section B | The screen changes inside the same Pygame window |
| clicks **Restart** | End (Pygame) | `restart()`: hero None, battle None, floor 0, offers [], state `menu` | `app.show()` → the Pygame loop ends, then `pygame.quit()` → the router opens a NEW Tk menu with nothing selected |
| closes the menu window (X) | Menu (Tk) | none | The program exits with code 0. A run never starts |
| closes the Pygame window (X) | Battle, Reward, End | none | The program exits with code 0. The run is dropped and the menu does **not** reopen |

**When a fresh run is created:** only on Start, by `game.new_run(name)`. Nothing else makes a hero. Restart only clears the run, and closing a window saves nothing.
Every Start builds a new hero object; `test_restart_resets_the_hero` checks this for `Game`.

**How the selected class reaches the game:** MenuScreen keeps the clicked name in `self.selected` (a plain `str`, like the lab's `selected_hero`).
Start passes it on: `self.app.game.new_run(self.selected)`. The router then gives the same `game` object to PygameApp.
Nothing else crosses between the toolkits: no globals, no files, no command-line arguments. The selection is not remembered after Restart.

**Handoff rules** (the prototype test below followed all four; only the focus rule was measured both with and without it):
- Build every `tk.PhotoImage` and every Pygame `Font`, `Surface` and image inside a screen's `__init__`. Never build them at import time or keep them in a module-level cache.
  Each window is new, and objects from the last one are dead after `destroy()` or `pygame.quit()`.
- Call `pygame.init()` only inside `PygameApp.run()`. `main.py` sets `os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"` before any `ui` import, which hides Pygame's console greeting.
- Keep `self.after(50, self.focus_force)` in TkApp. Without it, the menu opened after Restart was inactive: greyed title bar, focus left in another app (Windows 10, measured).
- A click that changes the screen ends click handling for that frame, so one click never lands on two screens.

**How `StubGame` exercises the same flow.** `python main.py stub` runs this same `main()` with `StubGame` in place of `Game`.
StubGame has the same `state` values and the same `class_preview`, `new_run`, `player_action`, `enemy_turn`, `claim_reward` and `restart` calls, so every row of the control table runs unchanged.
The stub path is menu → Start → battle F1 → reward → F2 → reward → F3 → reward → F4 → victory or defeat → Restart → menu.
**Gap, found by an exhaustive search of all 3,841 stub click states:** the current stub can never reach Defeat. Its enemy hits for 14, which is too weak.
**Lead fix before 1:30, in `StubBattle.enemy_turn`:** use `hit = 5 + 4 * self.floor` (BLOCK halves it) in place of the fixed 14.
With that change, Heavy-only wins on floor 4 and Light-only (or portrait-only) loses on floor 4. Both results were measured in the prototype.

**Acceptance check** (3 minutes, any teammate, `python main.py stub`; needs the stub fix):
1. The menu (Tk) opens and Start is grey. Click Knight: it highlights and shows stats. Click Start.
2. The menu closes and the battle window (Pygame) opens in front. Only one game window shows in the taskbar.
3. Click Heavy until Victory; on each reward screen, click any card. Then click Restart.
4. The battle window closes and the menu opens in front, active, with nothing selected.
5. Pick Thief, then Start. Click only the enemy portrait until Defeat. Click Restart: the menu appears again.
6. Close the menu with its X. The program ends, the terminal prompt returns, and there is no traceback.
7. Run it again: Start, then close the battle window with its X. The program ends, and the menu does not come back.

Pass means all 7 hold. With `python main.py` the outcomes in steps 3 and 5 depend on play. Run the same steps during 5:00-6:30.

**Prototype test (25 November 2026, Windows 10, Python 3.12.10, Tk 8.6, pygame 2.6.1).**
A throwaway copy of this router, with one Tk screen and three Pygame screens on a copy of `StubGame` with the fix, was run outside the repo.
Real OS mouse clicks drove it on the desktop, in 5 launches:
- two full Start → … → Restart round trips in one process (Victory, then Defeat), then a close of the menu;
- a close of the menu at launch;
- a close of the Pygame window in battle (during the enemy pause);
- a close of the Pygame window on the reward screen;
- Start → Restart → Start, then a close of the second Pygame window on the end screen.

The window list was sampled every 20 ms. Result: **53/53 checks passed** with the `focus_force` line, and 50/53 without it (the 3 failures were the inactive menu after Restart).
Each launch exited with code 0, wrote nothing to stderr and left no window open. There was never more than one window, and each Start made a new hero.
Not verified: macOS and Linux, display scaling above 100 %, the real `Game` (logic not written yet), real sprites, and hover colours (not checked).

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
| 0:00-1:30 | Lead | Confirm the toolkit split with the professor (A, resolved item 6). Re-push the six skeleton files listed at the top: the B.1 router in main.py; working stubs of pg_font, PgButton and load_surface in ui/theme.py; Pygame placeholder screens in ui/battle.py, ui/reward.py and ui/end.py; the defeat fix in logic/stub.py. Pass the acceptance check (B.1) on the placeholders. Everyone pulls, runs `python -m pip install pygame pytest`, then `python main.py stub` and `python -m pytest -q` (17 green, 15 red until owners fill their files). |
| 1:30-2:00 | Khael | Final ui/theme.py pushed by **2:00**: both the Tk half and the Pygame half, names unchanged. |
| 1:30-3:30 | Daniel, TJ | heroes/enemies and items. TJ first: Inventory + make_item + starter_kit by 2:30, because Daniel's tests need them. |
| 1:30-3:30 | Lead | logic/battle.py and logic/game.py. Run test_game.py as soon as Daniel and TJ push. |
| 2:00-5:00 | Joseph | Menu (Tkinter) first, then reward and end (Pygame), all on the stub. Then the README. |
| 1:30-5:00 | Khael | Battle screen (Pygame) on the stub, then sprites. A missing PNG gets a coloured placeholder box in both toolkits. |
| ~3:30 | Lead | **First playable fight** (one class beats the Goblin): start playtesting and file bugs to the file owner. |
| 5:00 | all | **Feature freeze.** `python -m pytest -q` all green, both greps empty (GUI grep at the top, mouse-only grep in F), acceptance check (B.1) passes on the stub. |
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
  The acceptance check (B.1) passes on `python main.py stub` and on `python main.py`.
- **Window routing (main.py, by 1:30):** build `main()`, `TkApp` and `PygameApp` exactly as in B.1, with the `focus_force` line and the per-frame click rule. Neither app ever computes game numbers.
  If a screen calls `app.show()` and the state belongs to the other toolkit, that app closes its own window; the router opens the next one.
  Closing either window ends the program. Restart reopens the menu.
- **Skeleton re-push (by 1:30):** the five other files listed at the top of this plan, as placeholders that already pass the acceptance check. Owners take them over at 1:30.
- **Waits on:** Daniel (heroes, enemies) and TJ (items) for real runs. The stub covers the UI until then.
- **QA:** file each bug to the owner of the file it lives in, with the battle log lines. A window bug (two windows, a lost menu, a hang on close) is the Lead's.

### Daniel: models/heroes.py, models/enemies.py
- **Done when:** tests/test_models.py hero and enemy tests are green and `grep -rE "tkinter|pygame" models/` prints nothing.
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
- No GUI imports. Never write the words "tkinter" or "pygame" anywhere in models/, not even in comments.
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
  tests/test_no_gui_in_models.py checks both toolkit names (section F).
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
- No decorators except @property and @abstractmethod. No GUI imports; never write "tkinter" or
  "pygame" in this file, not even in comments.
Then run python -m pytest -q tests/test_models.py and show me the output.
```

### Khael: ui/theme.py, ui/battle.py, assets/
- **Done when:** with `python main.py stub` and then `python main.py`, a full fight is playable in the Pygame window by mouse only. That means hover on every clickable, HP/mana bars, status chips from `statuses`, Light/Heavy/Special/Potion buttons, a disabled Special showing `special_label()`, enemy portrait click = Light, a log panel, a turn label and sprites. Nine 200x200 PNGs are in assets/.
  The theme serves both toolkits: Joseph's Tk menu and his Pygame reward and end screens use it unchanged.
- **Waits on:** nothing (stub, plus the Lead's 1:30 skeleton). theme.py final by **2:00**.
- **Prompt:**
```
You are helping a sophomore build the Pygame battle screen and the shared theme for a graded
Python 3.12 project. The game uses Tkinter for the menu and Pygame for battle, reward and end.
I own ui/theme.py and ui/battle.py ONLY. I paste: both files, main.py and logic/stub.py (read-only).
theme.py: keep every name and signature, restyle freely.
- Tk half: colours as "#rrggbb" strings (Pygame uses the same strings), fonts, HoverButton,
  bind_hover, load_sprite(name) -> tk.PhotoImage or None.
- Pygame half: pg_font(spec) -> a pygame Font from a theme font tuple; PgButton(rect, text, font)
  with .enabled, .hit(pos) and .draw(surface): HOVER colour while the mouse is over an enabled
  button, DISABLED colour when not enabled; load_surface(name) -> Surface of assets/<name>.png or None.
- Create no pygame Font, Surface or image at import time or in a module-level cache. Build them
  when a screen's __init__ calls these functions.
BattleScreen(app): __init__(self, app), handle_click(self, pos), update(self, now_ms), draw(self, surface).
- Read ONLY: app.game.battle.{hero, enemy, log, turn, round, over, can_special(), special_label(),
  can_potion()}, and on hero/enemy: name, level, hp, max_hp, mana, max_mana, statuses, sprite_name,
  plus hero.potion_count().
- Call ONLY: app.game.player_action('light'|'heavy'|'special'|'potion'), app.game.enemy_turn(),
  app.show(). After each call: if app.game.state != 'battle' call app.show() and stop.
- After a player action, if battle.turn == 'enemy': set self.enemy_due = now + 600 ms. While it is
  set, ignore clicks, grey all buttons and show "Enemy turn...". update(now_ms) calls
  game.enemy_turn() once now_ms >= enemy_due, then clears it.
- draw() redraws everything from the battle each frame (1100x720): hero panel left, enemy panel
  right (200x200 sprite from theme.load_surface, loaded in __init__; a coloured box if None),
  HP and mana bars (pygame.draw.rect, width = full * hp / max_hp), status chips (one small box
  with text per statuses key), a "Round 3 - your turn" / "Enemy turn..." label, 4 PgButtons,
  and a log panel with the last lines of battle.log.
- Special button: text = battle.special_label(); enabled only when can_special().
  Potion button: shows the potion count; enabled only when can_potion().
- A left click inside the enemy portrait rect calls the SAME method as the Light button.
  Draw a hover outline on the portrait while the mouse is over it.
- Mouse only: never use KEYDOWN, KEYUP or pygame.key. No animation, no sound. Never compute game
  numbers in the UI. Never call pygame.init(), set_mode(), flip() or pygame.quit(): main.py does.
Test with: python main.py stub
```

### Joseph: ui/menu.py, ui/reward.py, ui/end.py, README.md
- **Done when:** on the stub and then the real game, the acceptance check (B.1) passes by mouse only: the Tk menu → Start → the Pygame battle → reward → … → victory or defeat → Restart → the Tk menu. README follows section G.
- **Split:** `ui/menu.py` is Tkinter (`tk.Frame`, `theme.HoverButton`). `ui/reward.py` and `ui/end.py` are Pygame (the B.1 screen interface, `theme.PgButton`).
- **Waits on:** Khael's theme.py (the stub version works from 1:30, final at 2:00).
- **Prompt:**
```
You are helping a sophomore build three small screens for a graded Python 3.12 project. The game
uses Tkinter for the menu and Pygame for battle, reward and end. I own ui/menu.py, ui/reward.py and
ui/end.py ONLY. I paste: those files, ui/theme.py, main.py and logic/stub.py (all read-only except
mine). Keep each class name and signature. Use theme colours and fonts. Rules:
- MenuScreen(tk.Frame), __init__(self, master, app), TKINTER: a title and one theme.HoverButton
  per app.game.CLASS_NAMES, each showing its sprite (theme.load_sprite(name.lower()),
  compound="top"; keep the PhotoImage on self; text only if it returns None). Clicking a class
  SELECTS it: store the name in self.selected, highlight that button, and show
  app.game.class_preview(name) as text (the describe line plus the stats dict as
  "STR 16  DEX 6 ..." and "HP 158  MP 27  ATK 16 ..."). A Start HoverButton, disabled until a
  class is picked, calls app.game.new_run(self.selected), then app.show(). app.show() closes this
  window and the battle opens in Pygame, so do nothing after it.
- RewardScreen and EndScreen, PYGAME: __init__(self, app), handle_click(self, pos),
  update(self, now_ms) (empty), draw(self, surface) (redraw the whole screen every frame).
  Use theme.PgButton for every clickable and theme.pg_font for text. Build fonts and buttons in
  __init__, never at import time. Never call pygame.init(), set_mode(), flip() or pygame.quit().
- RewardScreen: one PgButton card per item in app.game.offers, showing item.describe() and
  app.game.reward_delta(item). Clicking a card calls app.game.claim_reward(item), then app.show().
- EndScreen: "Victory!" if app.game.state == 'victory' else "Defeat", the floor reached
  (app.game.floor) and app.game.hero.describe(). A Restart PgButton calls app.game.restart(),
  then app.show(). That closes the Pygame window and opens a fresh Tk menu.
- Mouse only: no Tk key bindings, never use KEYDOWN, KEYUP or pygame.key. No animation.
  Never compute game numbers in the UI.
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
| No GUI in models/ logic/ | test_no_gui_in_models.py, plus the GUI grep below |
| Start, Restart, close, one window at a time | no automated test (it needs a desktop): the acceptance check in B.1 |

**GUI check, both toolkits.** Today `tests/test_no_gui_in_models.py` looks only for `tkinter`. TJ extends it to both names before 2:30, keeping the split-string trick so the file does not match its own grep:
```python
TOOLKITS = ("tk" + "inter", "py" + "game")   # split so this file does not match its own grep
...
                 if any(name in path.read_text(encoding="utf-8") for name in TOOLKITS)]
```
GUI grep (must print nothing): `grep -rE "tkinter|pygame" models/ logic/`

Mouse-only grep (must print nothing; run after 5:00): `grep -rnE "<Key|<Return>|<space>|KEYDOWN|KEYUP|key\.get_pressed" ui/ main.py`

Status now: 17 of 32 green on the skeleton (all of test_character.py, the grep test, and the ABC tests). The other 15 stay red until their files are filled. All 32 passed against a throwaway reference fill of this contract, so the tests and the signatures agree.
The tests import neither toolkit, so they need only `pytest`, not `pygame` or a display.

---

## G. README outline (Joseph)
1. Title, screenshot and the **game concept** (one short paragraph, it replaces the lab's Marvel vs DC): a single-player, turn-based fantasy gauntlet. Pick 1 of 5 classes and fight 4 floors (Goblin, Orc, Ogre Warlord, Elder Dragon) one enemy at a time. Win a fight to level up, pick 1 of 3 items and heal to full. Lose once and the run is over. Mouse only, and the player always acts first. The menu is a Tkinter window; the fights, rewards and ending are a Pygame window. One window is open at a time.
2. How to run: Python 3.12, `python -m pip install pygame pytest`, then `python main.py`; tests: `python -m pytest -q`.
3. How to play (mouse only): pick a class, then Start (the battle window opens). Use Light / Heavy / Special / Potion, or click the enemy. Win: pick 1 of 3 items. Beat 4 floors. Restart goes back to the menu; closing either window quits.
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
| 5 | Mouse GUI | Tkinter: ui/menu.py (class select with PhotoImage buttons, HoverButton). Pygame: ui/battle.py, ui/reward.py, ui/end.py (PgButton hover, click the enemy). ui/theme.py serves both; main.py routes between the two windows |

7. Lab requirement checklist (section A rows 1-14, in short form).
8. File map and owners, with the toolkit of each screen (B.1 table).
9. Credits: the team; sprites drawn by Khael.

---

## Could not verify. Check these.
- **Enemy damage formula and enemy CRIT_MULT:** not stated in Complete.docx. The Table 27 medians suggest the old simulator may have used a different formula. Check BALANCE_KIT.md or simulate.py if you still have them.
- **Docx numbers** were read from the text extraction of Complete.docx Tables 18, 22, 23, 25 and 26. They match Table 24 (Knight 158 HP/27 MP/16 ATK, Sorcerer 101/130/54 spell, Druid 115 HP) and Goblin dodge 15.2 % / crit 15.8 %. The figures (images) were not read.
- **macOS:** tk.Button ignores `bg`, so hover colours do not show on the Tk menu on a Mac. If anyone demos on a Mac, HoverButton must become a Label with a click binding.
  The Tk → Pygame → Tk handoff in one process was tested only on Windows 10. Tk and SDL both drive the macOS app event loop, so **demo on Windows** unless the acceptance check (B.1) passes on that Mac.
- **Toolkit split approved?** It is an assumption (A, resolved item 6) until the professor confirms it.
- **Display scaling above 100 %:** the prototype ran at 96 DPI only. If the menu and the battle window come out at different sizes on a scaled laptop, the Lead makes main.py DPI-aware at start-up (Windows only), before the first window opens.
