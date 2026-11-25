# Joseph's handoff: menu, reward and end screens, then the README

## The game in 10 seconds
You pick a hero (Knight, Thief, Jester, Sorcerer or Druid) and fight 4 monsters in a row by clicking buttons. After each win you pick 1 of 3 items. Lose once and it's over; beat all 4 and you win. Mouse only.

The game uses **two toolkits, one window at a time**. The menu is a **Tkinter** window. Clicking Start closes it and opens a **Pygame** window for the fights, the rewards and the ending. Restart closes the Pygame window and opens the menu again. ([PLAN.md, section B.1](../PLAN.md#b1-window-routing) has the full routing.)

## Your job in one sentence
Build the 3 simple screens around the battle (pick a hero in Tkinter; pick a reward and win/lose + Restart in Pygame), then write the README.

## Your files (touch ONLY these)
| File | Toolkit | Screen |
|---|---|---|
| `ui/menu.py` | **Tkinter** | title + pick your hero + Start |
| `ui/reward.py` | **Pygame** | pick 1 of 3 items |
| `ui/end.py` | **Pygame** | "Victory!" or "Defeat" + Restart button |
| `README.md` | – | the final README |

## Deadlines
- **5:00**: all 3 screens done.
- **Last 1:30 of the day**: README done.

---

## Step 0: Set up (10 min)
1. Get the project folder, **either** way:
   - **With git:** Run `git clone https://github.com/flymywings/oop-final-project-revised.git`, then `cd` into the folder. Accept the Lead's GitHub invitation before pushing.
   - **Without git:** ask the Lead for the zip, unzip it, and open a terminal in that folder.
2. `python --version` must say 3.12.
3. Install Pygame and the test tool: `python -m pip install pygame pytest`
4. Run the **fake** game: `python main.py stub`

"Stub" means fake: fake numbers, but the same names as the real game. You can build all 3 screens today without waiting for anyone. When the real game is ready, `python main.py` just works.

**Before 1:30** the Lead pushes a new skeleton in which `ui/reward.py` and `ui/end.py` are Pygame placeholder screens. Pull it (or get the Lead's fresh zip) before you start them. If they still say `(tk.Frame)`, you have the old ones. `ui/menu.py` stays Tkinter, so you can start it at once.

## Step 1: Understand the 4 ideas you need (10 min)

**Idea 1: use Khael's look, don't make your own.**
`from ui import theme`. The theme has a Tkinter half and a Pygame half with the same colours:
- In the **menu** (Tkinter), use `theme.HoverButton(self, text="Start", command=self.start)` for every button, plus `theme.BG`, `theme.FG`, `theme.FONT_TITLE` and so on.
- In **reward** and **end** (Pygame), use `theme.PgButton(rect, text, font)` for every clickable, and `theme.pg_font(theme.FONT_BODY)` for text.

Both buttons already have hover, which the lab requires. Khael pushes the final theme at 2:00. The names stay the same, so your screens restyle by themselves.

**Idea 2: the screen asks the game, then says "switch screens".**
Every screen gets `self.app`. The game is `self.app.game`. The pattern is the same in both toolkits:
```python
def start(self):
    self.app.game.new_run(self.selected)   # 1. tell the game
    self.app.show()                        # 2. switch to whatever screen the game is on now
```
You never decide which screen comes next, and you never open or close a window yourself. `app.show()` looks at the game and picks. If the next screen belongs to the other toolkit, it closes this window and `main.py` opens the other one. So after Start the menu window closes and the battle opens in Pygame; after Restart the Pygame window closes and a fresh menu opens.

**Idea 3: a Pygame screen is four methods, and `main.py` runs the loop.**
```python
class RewardScreen:                  # EndScreen has the same four methods
    def __init__(self, app):         # build fonts and buttons HERE, never at the top of the file
    def handle_click(self, pos):     # a left click at (x, y): which button is under pos?
    def update(self, now_ms):        # leave empty (only the battle screen needs it)
    def draw(self, surface):         # draw the WHOLE screen, every frame
```
Never call `pygame.init()`, `set_mode()`, `flip()` or `pygame.quit()`. `main.py` (the Lead's file) does that.

**Idea 4: never do math in the UI.**
The stats text, the "ATK 16 -> 23" text and so on all come from the game. You just put them on screen.

## Step 2: Build the screens, in this order

**MenuScreen (`ui/menu.py`, Tkinter, `tk.Frame`, `__init__(self, master, app)`)**
1. A big title.
2. One `HoverButton` per name in `self.app.game.CLASS_NAMES`. Each shows its hero picture: `img = theme.load_sprite(name.lower())`, then `image=img, compound="top"`.
   Keep every image on `self` (for example in a dict), or Tk throws it away. If it returns `None` (no PNG yet), show text only. The lab asks for `PhotoImage` pictures on buttons, and this is the only Tkinter screen, so the pictures go here.
3. Clicking a class **selects** it, but does not start yet:
   - store the name: `self.selected = name`
   - highlight that button (for example change its colour)
   - show its stats as text from `text, stats = self.app.game.class_preview(name)`. `text` is a line like "Knight Lv1 - Shield Bash (10 MP)". `stats` is a dict like `{"STR": 16, "HP": 158, "ATK": 16, ...}`. Print it as something like `STR 16  DEX 6 ...` and `HP 158  MP 27  ATK 16 ...`
4. A **Start** button, disabled until a class is picked. Clicking it runs `self.app.game.new_run(self.selected)`, then `self.app.show()`. That is the only way the chosen class reaches the game, and it is the moment a fresh run is made.

(The lab says "clicking highlights the selected hero". That's why it's select first, then Start.)

**RewardScreen (`ui/reward.py`, Pygame)**
1. One card (a `PgButton` is fine) for each item in `self.app.game.offers` (always 3).
2. Each card shows `item.describe()` and `self.app.game.reward_delta(item)` (for example "ATK 16 -> 23").
3. In `handle_click`, a click on a card runs `self.app.game.claim_reward(item)`, then `self.app.show()`. The next fight opens in the same Pygame window.

**EndScreen (`ui/end.py`, Pygame)**
1. A big "Victory!" if `self.app.game.state == "victory"`, otherwise "Defeat".
2. The floor reached (`self.app.game.floor`) and `self.app.game.hero.describe()`.
3. A **Restart** `PgButton`. A click on it runs `self.app.game.restart()`, then `self.app.show()`. That closes the Pygame window and opens a fresh menu, with nothing selected.

**Tip:** the current stub can never lose, so Defeat never shows. The Lead's 1:30 stub fixes this: then clicking only Light (or only the enemy picture) loses on floor 4, and clicking only Heavy wins.

## Step 3: README.md (last part of the day)
Follow section G in `PLAN.md`. Open with the **game concept** paragraph, because it replaces the lab's Marvel vs DC. Say there that the menu is Tkinter and the fights are Pygame. Then:
- how to run (including `python -m pip install pygame pytest`)
- how to play
- the 5 classes
- the rules in 6 lines
- the **week-to-file table** (copy it from PLAN.md G). The professor reads this one most.
- the lab checklist
- the file owners, with the toolkit of each screen

## Rules (please don't break these)
- Hover on every button: `theme.HoverButton` in the menu, `theme.PgButton` in reward and end, and nothing else for clickables.
- Mouse only: no Tk key bindings, and never use `KEYDOWN`, `KEYUP` or `pygame.key`.
- Don't rename the classes or change their methods (`__init__(self, master, app)` for the menu; the four Pygame methods for reward and end).
- Don't edit `ui/theme.py`. That's Khael's file. Ask Khael if you need something added.
- Never open, close or quit a window yourself. Always call `self.app.show()`.

## How you know you're done
In `python main.py stub` (and later `python main.py`), using only the mouse:
- menu (Tkinter): the hero pictures show, you pick a class, it highlights, Start
- the menu window closes and the battle window (Pygame) opens
- win a fight, the reward screen appears, pick an item, the next fight starts
- win or lose, the end screen appears, Restart closes the battle window and the menu comes back with nothing picked

Then run the team's [acceptance check (PLAN.md B.1)](../PLAN.md#b1-window-routing). It takes 3 minutes and also checks closing each window.

## Push your work
```
git pull
git add ui/menu.py ui/reward.py ui/end.py README.md
git commit -m "Menu, reward and end screens"
git push
```

### No git? Send your code to the Lead instead
That's fine. The Lead checks it and puts it in the project for you.
1. Run the "How you know you're done" check first, and write in your message whether it passed (copy the last line it printed).
2. Send **only your files**: `ui/menu.py`, `ui/reward.py`, `ui/end.py` and `README.md`.
3. Send the **whole file** as an attachment (or the zip of those files), not a pasted piece of it. Keep the exact file names.
4. Each time you send a newer version, send the whole file again, so there's never a question about which copy is the latest.
5. Khael's final `ui/theme.py` lands at 2:00. The Lead sends you a fresh zip, and your screens restyle by themselves.

## Stuck for more than 10 minutes?
Message the Lead with the error text.

---

## Copy-paste prompt for your AI
Paste this, then paste `ui/menu.py`, `ui/reward.py`, `ui/end.py`, `ui/theme.py`, `main.py` and `logic/stub.py`.
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
