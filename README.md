<img src="assets/icon.svg" width="64" height="64" alt="">

# OOP Final Project: Essence of the Five

A single-player, turn-based fantasy RPG in Python 3.12, built with Tkinter and Pygame. You play it with the mouse only.
Pick one of five hero classes (Knight, Thief, Jester, Sorcerer, or Druid) and fight the Goblin, Orc, Ogre Warlord, and Elder Dragon in order.
After winning any of the first three fights, you level up, pick one of three items, and heal before the next floor. Beat the dragon to win the run. A loss ends the run.

## How to run

You need Python 3.12 (`python --version`).

```
git clone https://github.com/flymywings/oop-final-project-revised.git
cd oop-final-project-revised
python -m pip install -r requirements.txt
python main.py
```

No git? [Download the ZIP](https://github.com/flymywings/oop-final-project-revised/archive/refs/heads/main.zip), extract it, open a terminal in that folder and run the last two commands.

| Command | What it does |
|---|---|
| `python main.py` | Plays the real game: the Tkinter menu, then the Pygame battle. |
| `python main.py stub` | Same screens on fake data (`logic/stub.py`), for testing the UI alone. |
| `python -m pytest -q` | Runs the tests. First `python -m pip install -r requirements-dev.txt`. No display or sound card is needed: the GUI and sound tests use Pygame's silent "dummy" drivers. |

`models/` and `logic/` must never mention either toolkit: `grep -rE "tkinter|pygame" models/ logic/` prints nothing.

## How to play (mouse only)

1. In the menu, click a hero. It gets a gold ring and its stats appear. Click **Start**.
2. The menu closes and the battle window opens. You always act first. Click **Light**, **Heavy**, **Special** or **Potion**. Clicking the enemy portrait is the same as Light.
3. Win a fight and you level up, then pick **1 of 3 reward items**. Only upgrades are offered, and the item you pick is worn at once. You heal to full before the next floor.
4. Beat all 4 floors (Goblin, Orc, Ogre Warlord, Elder Dragon) to win. If your HP reaches 0, the run is over.
5. On the Victory or Defeat screen, **Restart** closes the battle window and opens a fresh menu. Closing either window with its X quits the game.
6. **Sound:** hits, dodges, misses, blocks, potions, clicks and the win and lose screens each have a sound. The `-`, `+` and `Sound` buttons at the top right of the menu and the battle screen change the volume or mute. With no sound card, or no files in `sounds/`, the game just plays silently.

## The 5 classes

| Class | Role | Special (mana) |
|---|---|---|
| Knight | Tank, most HP | Shield Bash (10): 1.2x attack, then BLOCK halves the next hit taken |
| Thief | Crits and dodges | Backstab (12): 1.5x attack, always a crit (x2.0) |
| Jester | Chaos, high luck | Trick (15): small hit that ignores armor, then a dice roll: CRIT UP, stun, heal, or a bonus hit |
| Sorcerer | Glass cannon | Fireball (32): 1.0x spell power, ignores armor |
| Druid | Sustain | Rejuvenate (20): heals 25 % max HP, REGEN for 3 turns, and a small hit |

## The rules in 6 lines

1. **Actions:** Light is 1.0x attack and cannot be dodged. Heavy is 1.5x attack but misses 30 % of the time. Special costs mana. Potion heals. All but Special are free.
2. **Damage order:** raw damage, crit (x1.5 to x2.5 by class), dodge (a dodged hit deals 0), armor (minus defense, at least 1), BLOCK (half), apply.
3. **Chances:** dodge % = min(35, DEX x 1.2 + LUCK x 0.4). Crit % = min(50, 5 + DEX x 0.8 + LUCK x 0.6).
4. **Statuses:** BLOCK halves the next hit, STUN skips a turn, CRIT UP makes the next attack a crit, REGEN heals 4 % max HP per turn.
5. **Mana:** both sides get +4 mana at the end of each turn. Bosses use a special every third turn.
6. **Levels:** essence from each kill gives Lv2, Lv3 and Lv4 at 25, 55 and 90 total. Each level raises the class's stats.

## One game, two windows

| Screen | Toolkit | Owner |
|---|---|---|
| Title and class selection (menu) | Tkinter | Joseph |
| Battle | Pygame | Khael |
| Rewards | Pygame | Joseph |
| Victory and defeat (with Restart) | Pygame | Joseph |

Only one window is open at a time, and both use the same `Game` object. `main.py` closes one window and opens the other whenever the game state changes. The exact contract and an acceptance check are in [PLAN.md, section B.1](PLAN.md#b1-window-routing).

## Files and owners

| Person | Files |
|---|---|
| Daniel | `models/heroes.py`, `models/enemies.py` |
| TJ | `models/items.py` (items, inventory, 20 catalogue items) |
| Khael | `ui/theme.py`, `ui/battle.py`, `assets/` sprites and background |
| Joseph | `ui/menu.py`, `ui/reward.py`, `ui/end.py`, `README.md` |
| Lead | `models/character.py`, `logic/battle.py`, `logic/game.py`, `logic/stub.py`, `main.py`, `tests/`, sound (`ui/sound.py`, `sounds/`, `tools/process_sounds.py`; the battle screen calls it), `requirements*.txt` |

[PLAN.md](PLAN.md) holds the full plan, the requirement trace and the contracts. [STUDY_GUIDE.md](STUDY_GUIDE.md) explains every concept in plain words, with code references and demos, for the presentation. The class diagram is [docs/class_diagram.png](docs/class_diagram.png).

## OOP concepts by week (where each is in the code)

| Week | Concept | Where |
|---|---|---|
| 1 | Classes and objects | `models/heroes.py`, `models/enemies.py`, `models/items.py` |
| 2 | Encapsulation, abstraction | Private HP and mana behind properties in `models/character.py`. Abstract base classes such as `Character`, `Hero` and `Item` |
| 3 | Inheritance, polymorphism | `Character` → `Hero` → 5 classes. `Character` → `Enemy` → `BossEnemy`. Each hero and boss has its own `special_attack`. Each enemy has its own `choose_action` |
| 4 | Composition, aggregation, association | `Game` owns `Battle`. `Inventory` holds items. `Battle` borrows the hero (`logic/`) |
| 5 | Mouse-only GUI | Tkinter menu `ui/menu.py` (`HoverButton`, `PhotoImage` class buttons). Pygame `ui/battle.py`, `ui/reward.py`, `ui/end.py` (`PgButton`, click the enemy). `ui/theme.py` serves both, and `main.py` routes between the windows |

## Lab requirement checklist

| Lab item | Done in |
|---|---|
| Mouse hero selection, highlight on click | `ui/menu.py` (gold ring, stats panel) |
| Attack, skill and heal buttons | `ui/battle.py` (Light, Heavy, Special, Potion) |
| Only the active player may act | `Battle.turn` guard in `logic/battle.py` |
| Hover effects on every button | `HoverButton` (Tk) and `PgButton` (Pygame) in `ui/theme.py` |
| Restart | `ui/end.py` calls `Game.restart()` and opens a new menu |
| Winner detection | `Battle.winner`, `Game` states `victory` and `defeat` |
| Battle log | `Battle.log`, shown in the battle screen |
| Images on buttons | sprites on the menu class buttons (`PhotoImage`) and in the battle |
| Click the enemy to attack | portrait click in `ui/battle.py` |
| Max-health cap | `Character.hp` setter clamps to `max_hp` |

## Credits

The team: Daniel, TJ, Khael, Joseph and the Lead. The five hero sprites and the battle background are by Khael.

Enemy sprites, from OpenGameArt.org:
- Goblin, Orc and Ogre Warlord: "Orc, Ogre and Goblin Chibi Sprites" by CraftPix.net, OGA-BY 3.0 (https://opengameart.org/content/orc-ogre-and-goblin-chibi-sprites). Idle frame 0, scaled to 200x200.
- Elder Dragon: "Dragon Sprites" by Chibizilla, CC-BY 4.0 (https://opengameart.org/content/dragon-sprites). Scaled to 200x200.

Sound effects are Undertale sounds by Toby Fox. They are copyrighted and **not free-use**: they are used here only for a class project and must not be redistributed. Where each file came from is in `sounds/SOURCES.md`. If `sounds/` has no files, or the PC has no audio device, the game runs silently. Mute and volume are mouse buttons at the top of the menu and the battle screen. To rebuild the files from raw sounds, run `python tools/process_sounds.py` (needs ffmpeg).

## How to contribute

Git is optional. Choose one way:

- **With git:** run `git pull`, then `git add` only your files, then commit and push. Accept the Lead's GitHub invitation before you push.
- **Without git:** send the Lead your **complete** owned files, with their paths (for example `models/items.py`). Do not send pasted pieces. The Lead reviews the files, copies them in and runs the tests.
