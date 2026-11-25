<img src="assets/icon.svg" width="64" height="64" alt="">

# OOP Final Project: Essence of the Five

A single-player, turn-based fantasy RPG in Python 3.12, built with Tkinter and Pygame. You play it with the mouse only.
Pick one of five hero classes (Knight, Thief, Jester, Sorcerer, or Druid) and fight the Goblin, Orc, Ogre Warlord, and Elder Dragon in order.
After winning any of the first three fights, you level up, pick one of three items, and heal before the next floor. Beat the dragon to win the run. A loss ends the run.

This repo contains the starter code and API contracts. The game logic and screens are still under construction.

## One game, two windows

| Screen | Toolkit | Owner |
|---|---|---|
| Title and class selection (menu) | Tkinter | Joseph |
| Battle | Pygame | Khael |
| Rewards | Pygame | Joseph |
| Victory and defeat (with Restart) | Pygame | Joseph |

Only one window is open at a time, and both windows use the same game object.
- **Start** (menu) creates a fresh run with the selected class. The menu window then closes and the Pygame window opens on the battle.
- **Restart** (victory or defeat screen) clears the run. The Pygame window then closes and a new menu opens with nothing selected.
- **Closing either window** with its X ends the program. Closing the Pygame window does not bring the menu back.

The exact contract and a 3-minute acceptance check are in [PLAN.md, section B.1](PLAN.md#b1-window-routing).

**Assumption:** the Week 5 lab uses Tkinter, and no newer final-project instructions were available. We assume the team may choose its toolkits. The Lead is confirming this with the professor ([PLAN.md, section A, resolved item 6](PLAN.md#requirements-this-brief-misses-resolved)).

**Skeleton status:** `main.py`, `ui/theme.py`, `ui/battle.py`, `ui/reward.py`, `ui/end.py` and `logic/stub.py` still contain the earlier all-Tkinter skeleton. The Lead re-pushes them to match this plan before 1:30. Until then, `python main.py stub` shows the old Tkinter-only placeholders.

## Start by reading your handoff

Your handoff has your files, deadlines, setup steps and a ready-made AI prompt.

| Person | Handoff | Responsibility |
|---|---|---|
| Daniel | [handoffs/DANIEL.md](handoffs/DANIEL.md) | Heroes and enemies: `models/heroes.py`, `models/enemies.py` |
| TJ | [handoffs/TJ.md](handoffs/TJ.md) | Items, inventory and rewards: `models/items.py`. Keeps `tests/` green |
| Khael | [handoffs/KHAEL.md](handoffs/KHAEL.md) | The look in both toolkits and the Pygame battle screen: `ui/theme.py`, `ui/battle.py`, `assets/` sprites |
| Joseph | [handoffs/JOSEPH.md](handoffs/JOSEPH.md) | Tkinter menu (`ui/menu.py`), Pygame reward and end screens (`ui/reward.py`, `ui/end.py`). Final `README.md` |
| Lead | [PLAN.md, section E](PLAN.md#lead-modelscharacterpy-done-logicbattlepy-logicgamepy-mainpy-qa) | `models/character.py` (done), `logic/battle.py`, `logic/game.py`, `main.py` (window routing), `logic/stub.py`, QA and reviews |

[PLAN.md](PLAN.md) is the full plan: the requirement trace, the contract, the build order and the tests.
Touch only your own files. If another file looks wrong, tell the Lead.

## Quick start

You need Python 3.12 (`python --version`). To get the code, clone the repository or [download the ZIP](https://github.com/flymywings/oop-final-project-revised/archive/refs/heads/main.zip).

```
git clone https://github.com/flymywings/oop-final-project-revised.git
cd oop-final-project-revised
```

If you downloaded the ZIP, extract it and open a terminal in the extracted folder. From the project folder, run:

```
python -m pip install pygame pytest
python -m pytest -q
python main.py stub
```

| Command | What it does today |
|---|---|
| `python -m pytest -q` | Runs the tests. In the starter code, 17 pass and 15 fail where methods are still stubs. The tests need neither toolkit nor a display. |
| `python main.py stub` | **Preview with fake data** (`logic/stub.py`). Build and test the screens with it. It needs no models. After the Lead's 1:30 skeleton it opens the Tkinter menu, then the Pygame battle. |
| `python main.py` | Launches the game entry point. A full run requires the remaining game logic and screens. |

`models/` and `logic/` must never mention either toolkit: `grep -rE "tkinter|pygame" models/ logic/` prints nothing.

## How to contribute

Git is optional. Choose one way:

- **With git:** run `git pull`, then `git add` only your files, then commit and push. Accept the Lead's GitHub invitation before you push.
- **Without git:** send the Lead your **complete** owned files, with their paths (for example `models/items.py`). Do not send pasted pieces. Say whether your handoff's "How you know you're done" check passed. The Lead reviews the files, copies them in and runs the tests.

## OOP concepts by week

| Week | Concept | Where |
|---|---|---|
| 1 | Classes and objects | `models/heroes.py`, `models/enemies.py`, `models/items.py` |
| 2 | Encapsulation, abstraction | Private HP and mana behind properties in `models/character.py`. Abstract base classes such as `Character`, `Hero` and `Item` |
| 3 | Inheritance, polymorphism | `Character` → `Hero` → 5 classes. `Character` → `Enemy` → `BossEnemy`. Each hero and boss has its own `special_attack`. Each enemy has its own `choose_action` |
| 4 | Composition, aggregation, association | `Game` owns `Battle`. `Inventory` holds items. `Battle` borrows the hero (`logic/`) |
| 5 | Mouse-only GUI | Tkinter menu `ui/menu.py` (`HoverButton`, `PhotoImage` class buttons). Pygame `ui/battle.py`, `ui/reward.py`, `ui/end.py` (`PgButton`, click the enemy). `ui/theme.py` serves both, and `main.py` routes between the windows |

The full table is in [PLAN.md, section G](PLAN.md#g-readme-outline-joseph). Joseph expands this README into the final version from that outline.
