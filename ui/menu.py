"""MenuScreen (Tkinter): title plus class select, each class with its stats as text.

Owner: Joseph. CONTRACT SKELETON: keep the class name and the
__init__(self, master, app) signature; build the rest with ui/theme.py.
This placeholder is plain on purpose: it already works by mouse so the window
routing can be tested. Joseph restyles it.
Reads: app.game.CLASS_NAMES, app.game.class_preview(name).
Calls: app.game.new_run(self.selected), then app.show(). That closes this
window and opens the Pygame battle.
"""

import tkinter as tk

from ui import theme


class MenuScreen(tk.Frame):
    """Title and five class buttons (HoverButton, sprite on top), stats shown as text."""

    def __init__(self, master, app):
        """Build the title, one button per class, the stats text and Start."""
        super().__init__(master, bg=theme.BG)
        self.app = app
        self.selected = None             # the clicked class name; nothing is created until Start
        self.images = {}                 # keep PhotoImages alive
        self.buttons = {}
        tk.Label(self, text="Essence of the Five", font=theme.FONT_TITLE,
                 bg=theme.BG, fg=theme.FG).pack(pady=(40, 20))
        row = tk.Frame(self, bg=theme.BG)
        row.pack(pady=10)
        for name in app.game.CLASS_NAMES:
            image = theme.load_sprite(name.lower())
            options = {"image": image, "compound": "top"} if image else {"width": 12}
            if image:
                self.images[name] = image
            button = theme.HoverButton(row, text=name, command=lambda n=name: self.pick(n), **options)
            button.pack(side="left", padx=6)
            self.buttons[name] = button
        self.preview = tk.Label(self, text="Pick a class", font=theme.FONT_BODY,
                                bg=theme.BG, fg=theme.FG, justify="center")
        self.preview.pack(pady=20)
        self.start_button = theme.HoverButton(self, text="Start", width=16, command=self.start,
                                              state="disabled")
        self.start_button.pack(pady=10)

    def pick(self, class_name):
        """Select (do not start): highlight the button and show the class stats."""
        self.selected = class_name
        for name, button in self.buttons.items():
            button.configure(fg=theme.ACCENT if name == class_name else theme.FG)
        text, stats = self.app.game.class_preview(class_name)
        pairs = [f"{key} {value}" for key, value in stats.items()]
        self.preview.configure(text=f"{text}\n{'  '.join(pairs[:6])}\n{'  '.join(pairs[6:])}")
        self.start_button.configure(state="normal")

    def start(self):
        """game.new_run(self.selected), then app.show()."""
        self.app.game.new_run(self.selected)
        self.app.show()
