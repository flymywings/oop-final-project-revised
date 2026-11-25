# Khael's handoff: the look, the battle screen and the sprites

## The game in 10 seconds
You pick a hero and fight 4 monsters in a row (Goblin, Orc, Ogre Warlord, Elder Dragon) by clicking buttons. Mouse only, no keyboard. Beat all 4 and you win.

## Your job in one sentence
You decide how the game looks, and you build the battle screen where the fighting happens.

## Your files (touch ONLY these)
- `ui/theme.py`: colours, fonts and the hover button that everyone reuses
- `ui/battle.py`: the battle screen
- `assets/`: the 9 sprites

## Deadlines
- **2:00**: push your final `ui/theme.py`. Joseph builds his screens on it. You can restyle anything, but **keep every name** (`BG`, `FONT_BODY`, `HoverButton`, `bind_hover`, `load_sprite`...) because his code uses them.
- **5:00**: the battle screen and sprites are done.

---

## Step 0: Set up (10 min)
1. Get the project folder, **either** way:
   - **With git:** Accept the Lead's GitHub invitation, run `git clone https://github.com/flymywings/oop-final-project-revised.git`, then `cd` into the folder.
   - **Without git:** ask the Lead for the zip, unzip it, and open a terminal in that folder.
2. `python --version` must say 3.12.
3. Run the **fake** game: `python main.py stub`

"Stub" means fake: fake numbers, fake enemies, but the same buttons and names as the real game. You can build the whole screen today without waiting for anyone. When the real game is ready, `python main.py` just works.

## Step 1: Understand the 3 ideas you need (5 min)

**Idea 1: the screen never does math. It only shows things and forwards clicks.**
The game object `self.app.game` knows everything. You **read** from it and **draw**. When a button is clicked, you **tell** the game and then redraw.

What you can read (`b = self.app.game.battle`):
- `b.hero` and `b.enemy`, each with `.name`, `.hp`, `.max_hp`, `.mana`, `.max_mana`, `.statuses` (a dict like `{"BLOCK": 1}`) and `.sprite_name` (like `"knight"`). The hero also has `.level`.
- `b.log`: a list of sentences. Show them in the log panel.
- `b.round` and `b.turn` (`"player"` or `"enemy"`)
- `b.can_special()`, `b.special_label()` (button text, for example `"Fireball - need 8 MP"`) and `b.can_potion()`
- `b.hero.potion_count()`

What you can call:
- `self.app.game.player_action("light")` (also `"heavy"`, `"special"`, `"potion"`)
- `self.app.game.enemy_turn()`
- `self.app.show()`: this switches screens. Call it when `self.app.game.state` is no longer `"battle"` (someone won).

**Idea 2: the click loop.**
```
player clicks -> game.player_action(...)
   -> if game.state != "battle": app.show() and stop   (fight is over)
   -> else refresh()
   -> if battle.turn == "enemy": disable buttons, show "Enemy turn...",
      self.after(600, self.enemy_step)

enemy_step -> game.enemy_turn()
   -> if game.state != "battle": app.show() and stop
   -> else refresh()   (buttons come back on, "Your turn")
```
`self.after(600, ...)` means "do this in 600 ms". It's only a pause so the player can see each turn. Not an animation.

**Idea 3: images vanish if you don't keep them.**
`self.hero_img = theme.load_sprite(b.hero.sprite_name)`. Store it on `self.` or Tk throws the picture away. If it returns `None` (no PNG yet), draw a coloured box instead.

## Step 2: Build the battle screen, in this order
1. Layout: hero panel on the left, enemy panel on the right, buttons at the bottom, log panel underneath.
2. Each panel shows: the sprite, name (and level for the hero), an **HP bar** and a **mana bar** (Canvas rectangles: width = full width × hp / max_hp), and **status chips** (one small label per key in `.statuses`).
3. A label with the round and turn: `"Round 3 - your turn"` or `"Enemy turn..."`. The player always goes first.
4. 4 `HoverButton`s: Light, Heavy, Special, Potion.
   - Special text = `b.special_label()`. Disable it when `not b.can_special()`.
   - Potion shows how many potions are left. Disable it when `not b.can_potion()`.
5. **Click the enemy portrait = Light attack.** Bind `<Button-1>` on the enemy picture to the **same** method the Light button uses. Give it hover with `theme.bind_hover(...)`. The lab asks for this specifically.
6. Log panel: a `Text` widget showing `b.log`, scrolled to the bottom, read-only.
7. `refresh()` redraws everything above from the battle.

## Step 3: Sprites
9 PNG files, **200x200**, in `assets/`, named exactly:
`knight.png thief.png jester.png sorcerer.png druid.png goblin.png orc.png ogrewarlord.png elderdragon.png`
Draw them however you like (pixel art is fine). Do the screen first and the sprites second. The coloured boxes work until the PNGs exist.

## Rules (please don't break these)
- **Hover on everything clickable.** Use `theme.HoverButton`, or `theme.bind_hover` for pictures.
- **Mouse only**: no key bindings at all.
- No animation, no sound.
- Never compute game numbers (damage, HP) in the UI. Read them from the game.
- Don't rename `BattleScreen` or change `__init__(self, master, app)`.

## How you know you're done
With `python main.py stub` (and later `python main.py`) you can fight a whole battle with only the mouse:
- every button has hover
- the HP and mana bars move
- the Special button greys out with "need N MP"
- clicking the enemy picture attacks
- the log fills up
- the turn label flips
- winning or losing moves to the next screen

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
