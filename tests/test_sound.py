"""Sound tests. Run headless: SDL_AUDIODRIVER and SDL_VIDEODRIVER are set to 'dummy' below.

Each event has one test that drives the REAL game and screens and checks that the right
event reaches sound.play (which is replaced by a recorder, so nothing is actually played).
"""

import os

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import random  # noqa: E402

import pygame  # noqa: E402
import pytest  # noqa: E402

from logic.game import Game  # noqa: E402
from models.heroes import HERO_CLASSES  # noqa: E402
from ui import sound  # noqa: E402
from ui.battle import BattleScreen  # noqa: E402
from ui.end import EndScreen  # noqa: E402
from ui.reward import RewardScreen  # noqa: E402


@pytest.fixture(autouse=True)
def clean_sound_state():
    """Every test starts with sound on, volume 0.6, mixer not yet failed."""
    sound._state.update(ready=False, failed=False, muted=False, volume=0.6)
    sound._sounds.clear()
    yield
    sound._sounds.clear()


@pytest.fixture(scope="module")
def display():
    pygame.init()
    pygame.display.set_mode((1100, 720))
    yield
    pygame.quit()


class FakeApp:
    def __init__(self, game):
        self.game = game
        self.shown = 0

    def show(self):
        self.shown += 1


@pytest.fixture
def played(monkeypatch):
    """Record every event passed to sound.play instead of playing it."""
    events = []
    monkeypatch.setattr(sound, "play", events.append)
    return events


# ---------- every battle event, found by playing the real game ----------

BATTLE_EVENTS = ["light", "heavy", "special", "crit", "dodge", "miss", "block", "potion", "enemy_hit"]


@pytest.fixture(scope="module")
def observed(display):
    """Play many seeded real fights through BattleScreen and record which events fire."""
    seen = set()
    recorder = []
    real_play = sound.play
    sound.play = recorder.append
    try:
        for cls in HERO_CLASSES:
            for seed in range(25):
                for floor in (1, 2):
                    game = Game(seed=seed)
                    game.new_run(cls)
                    game.floor = floor
                    game._start_battle()
                    app = FakeApp(game)
                    screen = BattleScreen(app)
                    rng = random.Random(seed)
                    for _ in range(60):
                        if game.state != "battle":
                            break
                        if screen.enemy_due is not None:
                            screen.update(10 ** 9)
                            continue
                        b = game.battle
                        if b.hero.hp < 0.4 * b.hero.max_hp and b.can_potion():
                            action = "potion"
                        elif b.can_special():
                            action = "special"
                        else:
                            action = rng.choice(["light", "heavy"])
                        screen.on_action(action)
                    seen.update(recorder)
                    recorder.clear()
    finally:
        sound.play = real_play
    return seen


@pytest.mark.parametrize("event", BATTLE_EVENTS)
def test_battle_event_reaches_sound_play(observed, event):
    assert event in observed, f"no real fight produced the {event!r} sound"


# ---------- the log-line mapping, on exact phrases the models write ----------

@pytest.mark.parametrize("line, hero, enemy, expected", [
    ("Knight's Light Attack hits Goblin for 14.", "Knight", "Goblin", ["light"]),
    ("Knight's Heavy Attack hits Goblin for 21.", "Knight", "Goblin", ["heavy"]),
    ("Knight's Heavy Attack misses Goblin! (MISS)", "Knight", "Goblin", ["miss"]),
    ("Goblin's attack is DODGED by Knight!", "Knight", "Goblin", ["dodge"]),
    ("Knight's Light Attack hits Goblin for 22 [CRIT].", "Knight", "Goblin", ["crit"]),
    ("Goblin's attack hits Knight for 9 [BLOCKED].", "Knight", "Goblin", ["block"]),
    ("Goblin's attack hits Knight for 22.", "Knight", "Goblin", ["enemy_hit"]),
    ("Knight drinks Health Potion: +35 HP.", "Knight", "Goblin", ["potion"]),
    ("Druid heals 30 HP and sets REGEN. Druid's Rejuvenate hits Orc for 5.", "Druid", "Orc", ["potion"]),
    ("Knight's Shield Bash hits Goblin for 20. Knight braces for the next hit (BLOCK).",
     "Knight", "Goblin", ["special"]),
    ("Floor 1: Goblin appears!", "Knight", "Goblin", []),
    ("Knight regenerates 4 HP.", "Knight", "Goblin", []),
])
def test_log_line_mapping(line, hero, enemy, expected):
    assert sound.events_for_log_line(line, hero, enemy) == expected


# ---------- clicks and hover ----------

def test_click_on_a_button_plays_click(display, played):
    game = Game(seed=1)
    game.new_run("Knight")
    screen = BattleScreen(FakeApp(game))
    screen.handle_click(screen.buttons["light"].rect.center)
    assert played[0] == "click"


def test_disabled_button_makes_no_click(display, played):
    game = Game(seed=1)
    game.new_run("Knight")
    screen = BattleScreen(FakeApp(game))
    screen.buttons["potion"].enabled = False
    screen.handle_click(screen.buttons["potion"].rect.center)
    assert played == []


def test_hover_plays_once_per_entry():
    rect = pygame.Rect(0, 0, 10, 10)
    recorded = []
    real_play = sound.play
    sound.play = recorded.append
    try:
        tracker = sound.HoverTracker()
        tracker.update({"a": rect}, (50, 50))     # outside
        tracker.update({"a": rect}, (5, 5))       # enters: one hover
        tracker.update({"a": rect}, (6, 6))       # still inside: nothing
        tracker.update({"a": rect}, (50, 50))     # leaves
        tracker.update({"a": rect}, (5, 5))       # enters again: second hover
    finally:
        sound.play = real_play
    assert recorded == ["hover", "hover"]


# ---------- floor cleared, victory, defeat ----------

def _won_game():
    game = Game(seed=2)
    game.new_run("Druid")
    game.battle.enemy.hp = 1
    game.player_action("heavy")
    for _ in range(30):                      # heavy can miss; keep attacking until the enemy falls
        if game.state != "battle":
            break
        if game.battle.turn == "enemy":
            game.enemy_turn()
        else:
            game.player_action("light")
    return game


def test_floor_cleared_plays_on_the_reward_screen(display, played):
    game = _won_game()
    assert game.state == "reward"
    RewardScreen(FakeApp(game))
    assert played == ["floor_clear"]


def test_victory_and_defeat_play_on_the_end_screen(display, played):
    game = Game(seed=1)
    game.new_run("Knight")
    game.state = "victory"
    EndScreen(FakeApp(game))
    game.state = "defeat"
    EndScreen(FakeApp(game))
    assert played == ["victory", "defeat"]


# ---------- mute, volume, and never crashing ----------

def test_mute_blocks_play(monkeypatch):
    class Fake:
        plays = 0

        def set_volume(self, v):
            pass

        def play(self):
            Fake.plays += 1
    monkeypatch.setattr(sound, "ensure", lambda: True)
    sound._sounds["click"] = Fake()
    sound.play("click")
    assert Fake.plays == 1
    sound.toggle_mute()
    sound.play("click")
    assert Fake.plays == 1
    sound.toggle_mute()
    sound.play("click")
    assert Fake.plays == 2


def test_volume_stays_between_0_and_1():
    for _ in range(30):
        sound.change_volume(-sound.VOLUME_STEP)
    assert sound.volume() == 0.0
    for _ in range(30):
        sound.change_volume(sound.VOLUME_STEP)
    assert sound.volume() == 1.0


def test_missing_files_are_silent_not_fatal(monkeypatch, tmp_path):
    monkeypatch.setattr(sound, "SOUNDS_DIR", str(tmp_path))      # empty folder
    for event in sound.EVENTS:
        sound.play(event)                                         # must not raise


def test_no_audio_device_is_silent_not_fatal(monkeypatch):
    def boom(*a, **k):
        raise pygame.error("no audio device")
    monkeypatch.setattr(pygame.mixer, "get_init", lambda: None)
    monkeypatch.setattr(pygame.mixer, "init", boom)
    assert sound.ensure() is False
    for event in sound.EVENTS:
        sound.play(event)                                         # must not raise


def test_real_wav_loads_and_plays_with_dummy_driver(monkeypatch, tmp_path):
    import wave
    path = tmp_path / "click.wav"
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(b"\x00\x00" * 2 * 441)
    monkeypatch.setattr(sound, "SOUNDS_DIR", str(tmp_path))
    assert sound.ensure() is True
    assert "click" in sound._sounds
    sound.play("click")                                           # real Sound.play on the dummy driver
    pygame.mixer.quit()
