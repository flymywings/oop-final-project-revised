"""Sound effects for the UI layer (Tkinter menu and Pygame screens).

No audio code lives in models/ or logic/. The battle screen reads the new lines of
Battle.log and calls play(event). Every function is safe to call with no audio device
or with missing files: it then does nothing and the game runs silently.

Files: sounds/<event>.wav (see sounds/SOURCES.md for where each one came from).
Mouse only: the mute and volume buttons are clicked, never keyed.
"""

import os

import pygame

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sounds")

# One sound per event. The file for each event is sounds/<event>.wav.
EVENTS = ("hover", "click", "light", "heavy", "special", "crit", "dodge", "miss",
          "block", "potion", "enemy_hit", "floor_clear", "victory", "defeat")

VOLUME_STEP = 0.1

_sounds = {}              # event -> pygame.mixer.Sound (empty when silent)
_state = {"ready": False, "failed": False, "muted": False, "volume": 0.6}


def ensure():
    """Start the mixer and preload every file, once per mixer session. Never raises.

    main.py calls pygame.quit() between windows, which shuts the mixer down and
    invalidates every Sound, so this re-initialises and reloads when needed.
    """
    if _state["failed"]:
        return False
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(44100, -16, 2, 512)
            _sounds.clear()
            _state["ready"] = False
        if not _state["ready"]:
            for event in EVENTS:
                path = os.path.join(SOUNDS_DIR, event + ".wav")
                if os.path.exists(path):
                    _sounds[event] = pygame.mixer.Sound(path)
            _state["ready"] = True
        return True
    except Exception:          # no audio device, bad driver, corrupt file: stay silent
        _state["failed"] = True
        _sounds.clear()
        return False


def play(event):
    """Play the sound for one event, unless muted or unavailable."""
    if _state["muted"] or not ensure():
        return
    sound = _sounds.get(event)
    if sound is None:
        return
    try:
        sound.set_volume(_state["volume"])
        sound.play()
    except Exception:
        _state["failed"] = True


def is_muted():
    return _state["muted"]


def toggle_mute():
    """Flip mute. Returns the new muted state."""
    _state["muted"] = not _state["muted"]
    return _state["muted"]


def volume():
    return _state["volume"]


def change_volume(delta):
    """Move the volume by delta, kept inside 0.0 .. 1.0. Returns the new volume."""
    _state["volume"] = round(max(0.0, min(1.0, _state["volume"] + delta)), 2)
    return _state["volume"]


def events_for_log_line(line, hero_name, enemy_name):
    """Map one Battle.log line to the sound events it should play (usually 0 or 1).

    The log is plain text, so the match is on the exact phrases written in
    models/character.py, models/heroes.py and models/items.py.
    """
    mine = line.startswith(hero_name)
    theirs = line.startswith(enemy_name)
    if "is DODGED by" in line:
        return ["dodge"]
    if "(MISS)" in line:
        return ["miss"]
    if "drinks " in line and "HP" in line:
        return ["potion"]
    if " heals " in line and "HP" in line and (mine or theirs):
        return ["potion"]
    if " hits " in line and " for " in line:
        if "BLOCKED" in line:
            return ["block"]
        if theirs:
            return ["enemy_hit"]
        if mine:
            if "CRIT" in line:
                return ["crit"]
            if "'s Heavy Attack hits" in line:
                return ["heavy"]
            if "'s Light Attack hits" in line:
                return ["light"]
            return ["special"]
    return []


class HoverTracker:
    """Plays 'hover' once each time the mouse moves onto a new clickable."""

    def __init__(self):
        self.current = None

    def update(self, rects, pos):
        """rects: {key: Rect} of the clickables that are enabled right now."""
        over = next((key for key, rect in rects.items() if rect.collidepoint(pos)), None)
        if over is not None and over != self.current:
            play("hover")
        self.current = over


def bind_tk(widget):
    """Hover and click sounds for a Tk widget (adds to its existing bindings)."""
    widget.bind("<Enter>", lambda e: play("hover") if str(widget.cget("state")) != "disabled" else None, add="+")
    widget.bind("<ButtonPress-1>", lambda e: play("click") if str(widget.cget("state")) != "disabled" else None, add="+")
