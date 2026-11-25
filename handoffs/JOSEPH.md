# Joseph's handoff: menu, reward and end screens, then the README

## The game in 10 seconds
You pick a hero (Knight, Thief, Jester, Sorcerer or Druid) and fight 4 monsters in a row by clicking buttons. After each win you pick 1 of 3 items. Lose once and it's over; beat all 4 and you win. Mouse only.

## Your job in one sentence
Build the 3 simple screens around the battle (pick a hero, pick a reward, win/lose + Restart), then write the README.

## Your files (touch ONLY these)
- `ui/menu.py`: title + pick your hero
- `ui/reward.py`: pick 1 of 3 items
- `ui/end.py`: "Victory!" or "Defeat" + Restart button
- `README.md`

## Deadlines
- **5:00**: all 3 screens done.
- **Last 1:30 of the day**: README done.

---

## Step 0: Set up (10 min)
1. Get the project folder, **either** way:
   - **With git:** Accept the Lead's GitHub invitation, run `git clone https://github.com/flymywings/oop-final-project-revised.git`, then `cd` into the folder.
   - **Without git:** ask the Lead for the zip, unzip it, and open a terminal in that folder.
2. `python --version` must say 3.12.
3. Run the **fake** game: `python main.py stub`

"Stub" means fake: fake numbers, but the same names as the real game. You can build all 3 screens today without waiting for anyone. When the real game is ready, `python main.py` just works.

## Step 1: Understand the 3 ideas you need (5 min)

**Idea 1: use Khael's look, don't make your own.**
`from ui import theme`, then use `theme.HoverButton(self, text="Start", command=self.start)` for every button. It already has hover, which the lab requires. Use `theme.BG`, `theme.FG`, `theme.FONT_TITLE`, etc. for colours and fonts. Khael pushes the final theme at 2:00. The names stay the same, so your screens restyle by themselves.

**Idea 2: the screen asks the game, then says "switch screens".**
Every screen gets `self.app`. The game is `self.app.game`. The pattern is always:
```python
def pick(self, class_name):
    self.app.game.new_run(class_name)   # 1. tell the game
    self.app.show()                     # 2. switch to whatever screen the game is on now
```
You never decide which screen comes next. `app.show()` looks at the game and picks.

**Idea 3: never do math in the UI.**
The stats text, the "ATK 16 -> 23" text and so on all come from the game. You just put them in labels.

## Step 2: Build the screens, in this order

**MenuScreen (`ui/menu.py`)**
1. A big title.
2. One `HoverButton` per name in `self.app.game.CLASS_NAMES`.
3. Clicking a class **selects** it, but does not start yet:
   - highlight that button (for example change its colour)
   - show its stats as text from `text, stats = self.app.game.class_preview(name)`. `text` is a line like "Knight Lv1 - Shield Bash (10 MP)". `stats` is a dict like `{"STR": 16, "HP": 158, "ATK": 16, ...}`. Print it as something like `STR 16  DEX 6 ...` and `HP 158  MP 27  ATK 16 ...`
4. A **Start** button, disabled until a class is picked. Clicking it runs `new_run(name)` then `app.show()`.

(The lab says "clicking highlights the selected hero". That's why it's select first, then Start.)

**RewardScreen (`ui/reward.py`)**
1. One card (a `HoverButton` is fine) for each item in `self.app.game.offers` (always 3).
2. Each card shows `item.describe()` and `self.app.game.reward_delta(item)` (for example "ATK 16 -> 23").
3. Clicking a card runs `self.app.game.claim_reward(item)` then `self.app.show()`.

**EndScreen (`ui/end.py`)**
1. A big "Victory!" if `self.app.game.state == "victory"`, otherwise "Defeat".
2. The floor reached (`self.app.game.floor`) and `self.app.game.hero.describe()`.
3. A **Restart** `HoverButton` that runs `self.app.game.restart()` then `self.app.show()`. That takes you back to the menu.

## Step 3: README.md (last part of the day)
Follow section G in `PLAN.md`. Open with the **game concept** paragraph, because it replaces the lab's Marvel vs DC. Then:
- how to run
- how to play
- the 5 classes
- the rules in 6 lines
- the **week-to-file table** (copy it from PLAN.md G). The professor reads this one most.
- the lab checklist
- the file owners

## Rules (please don't break these)
- Hover on every button: use `theme.HoverButton` and nothing else for clickables.
- Mouse only: no key bindings at all.
- Don't rename the classes or change `__init__(self, master, app)`.
- Don't edit `ui/theme.py`. That's Khael's file. Ask Khael if you need something added.

## How you know you're done
In `python main.py stub` (and later `python main.py`), using only the mouse:
- menu: pick a class, it highlights, Start
- win a fight, the reward screen appears, pick an item, the next fight starts
- win or lose, the end screen appears, Restart goes back to the menu

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
