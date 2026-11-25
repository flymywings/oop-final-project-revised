<img src="assets/icon.svg" width="64" height="64" alt="">

# OOP Final Project: Essence of the Five

A single-player, turn-based fantasy RPG in Python 3.12 and Tkinter. You play it with the mouse only.
Pick one of five hero classes (Knight, Thief, Jester, Sorcerer, or Druid) and fight the Goblin, Orc, Ogre Warlord, and Elder Dragon in order.
After winning any of the first three fights, you level up, pick one of three items, and heal before the next floor. Beat the dragon to win the run. A loss ends the run.

This repo contains the starter code and API contracts. The game logic and screens are still under construction.

## Start by reading your handoff

Your handoff has your files, deadlines, setup steps and a ready-made AI prompt.

| Person | Handoff | Responsibility |
|---|---|---|
| Daniel | [handoffs/DANIEL.md](handoffs/DANIEL.md) | Heroes and enemies: `models/heroes.py`, `models/enemies.py` |
| TJ | [handoffs/TJ.md](handoffs/TJ.md) | Items, inventory and rewards: `models/items.py`. Keeps `tests/` green |
| Khael | [handoffs/KHAEL.md](handoffs/KHAEL.md) | Look and battle screen: `ui/theme.py`, `ui/battle.py`, `assets/` sprites |
| Joseph | [handoffs/JOSEPH.md](handoffs/JOSEPH.md) | Menu, reward and end screens: `ui/menu.py`, `ui/reward.py`, `ui/end.py`. Final `README.md` |
| Lead | [PLAN.md, section E](PLAN.md#lead-modelscharacterpy-done-logicbattlepy-logicgamepy-mainpy-qa) | `models/character.py` (done), `logic/battle.py`, `logic/game.py`, `main.py`, QA and reviews |

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
python -m pip install pytest
python -m pytest -q
python main.py stub
```

| Command | What it does today |
|---|---|
| `python -m pytest -q` | Runs the tests. In the starter code, 17 pass and 15 fail where methods are still stubs. |
| `python main.py stub` | **Preview with fake data** (`logic/stub.py`). Build and test the screens with it. It needs no models. |
| `python main.py` | Launches the game entry point. A full run requires the remaining game logic and screens. |

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
| 5 | Mouse-only GUI | `ui/` (`HoverButton` in `ui/theme.py`) |

The full table is in [PLAN.md, section G](PLAN.md#g-readme-outline-joseph). Joseph expands this README into the final version from that outline.
