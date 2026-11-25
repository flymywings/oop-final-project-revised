# Khael's handoff: the look, the battle screen and the sprites

## The game in 10 seconds
You pick a hero and fight 4 monsters in a row (Goblin, Orc, Ogre Warlord, Elder Dragon) by clicking buttons. Mouse only, no keyboard. Beat all 4 and you win.

The game uses **two toolkits, one window at a time**. The menu, where you pick a hero, is a **Tkinter** window. Clicking Start closes it and opens a **Pygame** window for the fights, the rewards and the ending. Restart closes the Pygame window and opens the menu again. ([PLAN.md, section B.1](../PLAN.md#b1-window-routing) has the full routing.)

## Your job in one sentence
You decide how the game looks in both toolkits, and you build the Pygame battle screen where the fighting happens.

## Your files (touch ONLY these)
- `ui/theme.py`: colours, fonts and the buttons that everyone reuses. It has a Tkinter half (for Joseph's menu) and a Pygame half (for your battle screen and Joseph's reward and end screens).
- `ui/battle.py`: the battle screen (Pygame)
- `assets/`: the 9 sprites

## Deadlines
- **2:00**: push your final `ui/theme.py`. Joseph builds his screens on it. You can restyle anything, but **keep every name** (`BG`, `FONT_BODY`, `HoverButton`, `bind_hover`, `load_sprite`, `pg_font`, `PgButton`, `load_surface`...) because his code uses them.
- **5:00**: the battle screen and sprites are done.

---

## Step 0: Set up (10 min)
1. Get the project folder, **either** way:
   - **With git:** Run `git clone https://github.com/flymywings/oop-final-project-revised.git`, then `cd` into the folder. Accept the Lead's GitHub invitation before pushing.
   - **Without git:** ask the Lead for the zip, unzip it, and open a terminal in that folder.
2. `python --version` must say 3.12.
3. Install Pygame and the test tool: `python -m pip install pygame pytest`
4. Run the **fake** game: `python main.py stub`

"Stub" means fake: fake numbers, fake enemies, but the same buttons and names as the real game. You can build the whole screen today without waiting for anyone. When the real game is ready, `python main.py` just works.

The skeleton is already two-toolkit. `ui/battle.py` is a plain Pygame placeholder that plays a whole fight, and `ui/theme.py` has plain working versions of the Pygame names. You make them look good and add what's missing (sprites, bars, chips, portrait hover).
If your `ui/battle.py` still says `class BattleScreen(tk.Frame)`, you have an old copy: pull again (or ask the Lead for a fresh zip).

## Step 1: Understand the 4 ideas you need (10 min)

**Idea 1: the screen never does math. It only shows things and forwards clicks.**
The game object `self.app.game` knows everything. You **read** from it and **draw**. When something is clicked, you **tell** the game.

What you can read (`b = self.app.game.battle`):
- `b.hero` and `b.enemy`, each with `.name`, `.hp`, `.max_hp`, `.mana`, `.max_mana`, `.statuses` (a dict like `{"BLOCK": 1}`) and `.sprite_name` (like `"knight"`). The hero also has `.level`.
- `b.log`: a list of sentences. Show the last few in the log panel.
- `b.round` and `b.turn` (`"player"` or `"enemy"`)
- `b.can_special()`, `b.special_label()` (button text, for example `"Fireball - need 8 MP"`) and `b.can_potion()`
- `b.hero.potion_count()`

What you can call:
- `self.app.game.player_action("light")` (also `"heavy"`, `"special"`, `"potion"`)
- `self.app.game.enemy_turn()`
- `self.app.show()`: this switches screens. Call it when `self.app.game.state` is no longer `"battle"` (someone won).

**Idea 2: a Pygame screen is four methods, and `main.py` runs the loop.**
You never write the `while` loop, `pygame.init()`, `set_mode()`, `flip()` or `pygame.quit()`. `main.py` (the Lead's file) does all of that and calls your screen:
```python
class BattleScreen:
    def __init__(self, app):         # build fonts, sprites and buttons HERE
    def handle_click(self, pos):     # a left click at (x, y) in the window
    def update(self, now_ms):        # called every frame: use it for the enemy pause
    def draw(self, surface):         # draw the WHOLE screen, every frame (30 times a second)
```
Because `draw()` repaints everything every frame from `app.game.battle`, there is no separate "refresh". Hover works the same way: in `draw()`, a button is lighter if `pygame.mouse.get_pos()` is inside it.

**Idea 3: the click loop.**
```
handle_click(pos) -> which button (or the enemy portrait) is under pos?
   -> on_action(action): game.player_action(action)
   -> if game.state != "battle": app.show() and stop   (fight is over)
   -> if battle.turn == "enemy": self.enemy_due = pygame.time.get_ticks() + 600

update(now_ms) -> if enemy_due is set and now_ms >= enemy_due:
   -> enemy_due = None; game.enemy_turn()
   -> if game.state != "battle": app.show()
```
While `enemy_due` is set, ignore clicks, grey out the buttons and show "Enemy turn...". The 600 ms is only a pause so the player can see each turn. It is not an animation.

**Idea 4: build Pygame things in `__init__`, never at the top of a file.**
Each Start opens a brand-new Pygame window, and each Restart closes it with `pygame.quit()`. A font or image made at import time, or kept in a module-level variable, dies with the old window and crashes the next one. So `theme.pg_font(...)`, `theme.load_surface(...)` and `PgButton(...)` are called from `__init__`. The same goes for Tk images on Joseph's menu: `load_sprite` is called when his screen is built.

## Step 2: theme.py, by 2:00
Keep every existing name. Add the Pygame half with exactly these names:
- **Colours:** keep them as `"#rrggbb"` strings. Pygame accepts the same strings, so one palette serves both toolkits.
- **Tk half (Joseph's menu):** `FONT_*` tuples, `HoverButton`, `bind_hover`, `load_sprite(name)` returning a `tk.PhotoImage` or `None`.
- **Pygame half:**
  - `pg_font(spec)`: turn a theme font tuple like `FONT_BODY` into a Pygame font (for example `pygame.font.SysFont("arial", size, bold=...)`). You choose the sizes.
  - `PgButton(rect, text, font)`: has `.enabled`, `.hit(pos)` (True only when enabled and `pos` is inside) and `.draw(surface)`. It draws in the `HOVER` colour while the mouse is over an enabled button, in `DISABLED` when not enabled, else in `BUTTON`.
  - `load_surface(name)`: the Pygame image of `assets/<name>.png`, or `None` if the file is missing.

## Step 3: Build the battle screen, in this order
The window is 1100x720.
1. Layout: hero panel on the left, enemy panel on the right, buttons at the bottom, log panel above the buttons.
2. Each panel shows the sprite (`theme.load_surface(b.hero.sprite_name)`, loaded once in `__init__`; draw a coloured box if it is `None`) and the name (and level for the hero).
   It also shows an **HP bar** and a **mana bar** (`pygame.draw.rect`, width = full width × hp / max_hp), and **status chips** (one small box with text per key in `.statuses`).
3. A label with the round and turn: `"Round 3 - your turn"` or `"Enemy turn..."`. The player always goes first.
4. 4 `theme.PgButton`s: Light, Heavy, Special, Potion.
   - Special text = `b.special_label()`. Disable it when `not b.can_special()`.
   - Potion shows how many potions are left. Disable it when `not b.can_potion()`.
5. **Click the enemy portrait = Light attack.** In `handle_click`, if `pos` is inside the enemy sprite's rect, call the **same** `on_action("light")` the Light button uses. Draw a hover outline round the portrait while the mouse is over it. The lab asks for this specifically.
6. Log panel: the last lines of `b.log`, drawn as text, newest at the bottom.

## Step 4: Sprites
9 PNG files, **200x200**, in `assets/`, named exactly:
`knight.png thief.png jester.png sorcerer.png druid.png goblin.png orc.png ogrewarlord.png elderdragon.png`
Draw them however you like (pixel art is fine). Do the screen first and the sprites second. The coloured boxes work until the PNGs exist.
The same five hero PNGs also appear on Joseph's Tkinter menu buttons through `load_sprite`, so keep them as plain PNGs, which both toolkits can read.

## Rules (please don't break these)
- **Hover on everything clickable.** Use `theme.PgButton` in Pygame, plus the portrait outline. Joseph's Tk menu uses `theme.HoverButton`.
- **Mouse only**: never use `KEYDOWN`, `KEYUP` or `pygame.key`, and no Tk key bindings.
- No animation, no sound.
- Never compute game numbers (damage, HP) in the UI. Read them from the game.
- Never call `pygame.init()`, `pygame.display.set_mode()`, `pygame.display.flip()` or `pygame.quit()`. `main.py` does those.
- Don't rename `BattleScreen` or change its four methods.

## How you know you're done
With `python main.py stub` (and later `python main.py`), in the Pygame battle window, you can fight a whole battle with only the mouse:
- every button and the enemy portrait has hover
- the HP and mana bars move
- the Special button greys out with "need N MP"
- clicking the enemy picture attacks
- the log fills up
- the turn label flips, and clicks do nothing during "Enemy turn..."
- winning or losing moves to the next screen, still in the same Pygame window

Then run the team's [acceptance check (PLAN.md B.1)](../PLAN.md#b1-window-routing). It takes 3 minutes, and Start, Restart and both window closes must behave.

## Push your work
```
git pull
git add ui/theme.py ui/battle.py assets/
git commit -m "Battle screen"
git push
```
Push `ui/theme.py` separately at 2:00 so Joseph gets it early.

### No git? Send your code to the Lead instead
That's fine. The Lead checks it and puts it in the project for you.
1. Run the "How you know you're done" check first, and write in your message whether it passed (copy the last line it printed).
2. Send **only your files**: `ui/theme.py`, `ui/battle.py` and your PNGs from `assets/`.
3. Send the **whole file** as an attachment (or the zip of those files), not a pasted piece of it. Keep the exact file names.
4. Each time you send a newer version, send the whole file again, so there's never a question about which copy is the latest.
5. Send `ui/theme.py` by **2:00** on its own, so the Lead can pass it to Joseph.

## Stuck for more than 10 minutes?
Message the Lead with the error text.

---

## Copy-paste prompt for your AI
Paste this, then paste `ui/theme.py`, `ui/battle.py`, `main.py` and `logic/stub.py`.
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
