"""MenuScreen (Tkinter): title plus class select, each class with its stats as text.

Owner: Joseph. CONTRACT: keeps the class name and the
__init__(self, master, app) signature; everything is built with ui/theme.py.
Reads: app.game.CLASS_NAMES, app.game.class_preview(name).
Calls: app.game.new_run(self.selected), then app.show(). That closes this
window and opens the Pygame battle.
Mouse only: no key bindings.
"""

import tkinter as tk

from ui import theme

ATTRIBUTE_COUNT = 6          # the first 6 stats (STR..LUCK) go on row 1, the rest on row 2
MAX_SPRITE = 160             # widest a class sprite may be on its button, in pixels
DIM = "#8a8a99"              # hint text and the disabled Start label


class MenuScreen(tk.Frame):
    """Title and five class buttons (HoverButton, sprite on top), stats shown as text."""

    def __init__(self, master, app):
        """Build the title, one button per class, the stats panel and Start."""
        super().__init__(master, bg=theme.BG)
        self.app = app
        self.selected = None             # the clicked class name; nothing is created until Start
        self.images = {}                 # keep PhotoImages alive
        self.buttons = {}
        tk.Label(self, text="Essence of the Five", font=theme.FONT_TITLE,
                 bg=theme.BG, fg=theme.ACCENT).pack(pady=(36, 4))
        tk.Label(self, text="Choose your hero", font=theme.FONT_HEAD,
                 bg=theme.BG, fg=theme.FG).pack(pady=(0, 16))
        row = tk.Frame(self, bg=theme.BG)
        row.pack(pady=6)
        for name in app.game.CLASS_NAMES:
            image = theme.load_sprite(name.lower())
            if image:
                # 200px sprites would make five buttons wider than the window: shrink to fit.
                factor = -(-image.width() // MAX_SPRITE)
                if factor > 1:
                    image = image.subsample(factor)
                self.images[name] = image
            options = {"image": image, "compound": "top"} if image else {"width": 12, "height": 4}
            # An invisible ring around each button turns gold when it is selected.
            button = theme.HoverButton(row, text=name, command=lambda n=name: self.pick(n),
                                       font=theme.FONT_HEAD, padx=10, pady=8,
                                       highlightthickness=3, highlightbackground=theme.BG,
                                       **options)
            button.pack(side="left", padx=8)
            self.buttons[name] = button
        # Fixed-size panel, so the layout does not jump when a class is picked.
        self.panel = tk.Frame(self, bg=theme.PANEL, width=780, height=190)
        self.panel.pack(pady=18)
        self.panel.pack_propagate(False)
        self.preview = tk.Label(self.panel, text="Click a hero to see its stats",
                                font=theme.FONT_HEAD, bg=theme.PANEL, fg=theme.FG,
                                wraplength=740, justify="center")
        self.preview.pack(pady=(20, 8))
        self.stats = tk.Frame(self.panel, bg=theme.PANEL)
        self.stats.pack()
        self.start_button = theme.HoverButton(self, text="Start", width=14, font=theme.FONT_HEAD,
                                              pady=6, command=self.start, state="disabled",
                                              disabledforeground=DIM, highlightthickness=0)
        self.start_button.pack(pady=(6, 6))
        self.hint = tk.Label(self, text="Pick a hero to enable Start", font=theme.FONT_SMALL,
                             bg=theme.BG, fg=DIM)
        self.hint.pack()

    def pick(self, class_name):
        """Select (do not start): highlight the button and show the class stats."""
        self.selected = class_name
        for name, button in self.buttons.items():
            chosen = name == class_name
            button.configure(fg=theme.ACCENT if chosen else theme.FG,
                             highlightbackground=theme.ACCENT if chosen else theme.BG)
        text, stats = self.app.game.class_preview(class_name)
        self.preview.configure(text=text)
        self.show_stats(stats)
        self.start_button.configure(state="normal")
        self.hint.configure(text=f"{class_name} selected - press Start")

    def show_stats(self, stats):
        """Draw the stats dict as two rows of small label-over-value cells."""
        for cell in self.stats.winfo_children():
            cell.destroy()
        for index, (key, value) in enumerate(stats.items()):
            cell = tk.Frame(self.stats, bg=theme.PANEL)
            cell.grid(row=0 if index < ATTRIBUTE_COUNT else 1,
                      column=index if index < ATTRIBUTE_COUNT else index - ATTRIBUTE_COUNT,
                      padx=12, pady=4)
            tk.Label(cell, text=key, font=theme.FONT_SMALL, bg=theme.PANEL,
                     fg=theme.HOVER).pack()
            tk.Label(cell, text=str(value), font=theme.FONT_HEAD, bg=theme.PANEL,
                     fg=theme.FG).pack()

    def start(self):
        """game.new_run(self.selected), then app.show()."""
        self.app.game.new_run(self.selected)
        self.app.show()
