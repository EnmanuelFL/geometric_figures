import customtkinter as ctk

from ui import ACCENT, ACCENT_HOVER, ACCENT_SOFT, BG, BORDER, ERROR_SOFT, PANEL, TEXT, TEXT_MUTED


class FigurePanel(ctk.CTkFrame):
    def __init__(self, master, on_select, on_history_load, on_history_delete, **kwargs):
        super().__init__(master, fg_color=PANEL, corner_radius=12, **kwargs)
        self.on_select = on_select
        self.on_history_load = on_history_load
        self.on_history_delete = on_history_delete
        self.figure_buttons = {}
        self.selected_cls = None

        header = ctk.CTkLabel(
            self,
            text="Geometry Figures",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT,
        )
        header.pack(anchor="w", padx=16, pady=(16, 2))

        subtitle = ctk.CTkLabel(
            self,
            text="Select a shape to calculate",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED,
        )
        subtitle.pack(anchor="w", padx=16, pady=(0, 8))

        self.figures_scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.figures_scroll.pack(fill="x", padx=10, pady=(0, 6))

        separator = ctk.CTkFrame(self, height=1, fg_color=BORDER, corner_radius=0)
        separator.pack(fill="x", padx=16, pady=6)

        history_header = ctk.CTkLabel(
            self,
            text="History",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT,
        )
        history_header.pack(anchor="w", padx=16, pady=(4, 0))

        history_subtitle = ctk.CTkLabel(
            self,
            text="Last 20 calculations",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED,
        )
        history_subtitle.pack(anchor="w", padx=16, pady=(0, 4))

        self.history_scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.history_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 12))

        self.update_history([])

    def set_figures(self, figures_2d, figures_3d):
        for widget in self.figures_scroll.winfo_children():
            widget.destroy()
        self.figure_buttons = {}
        row = 0
        for title, group in (("2D", figures_2d), ("3D", figures_3d)):
            section = ctk.CTkLabel(
                self.figures_scroll,
                text=title,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TEXT_MUTED,
            )
            section.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
            row += 1
            column = 0
            for cls in group:
                button = ctk.CTkButton(
                    self.figures_scroll,
                    text=cls.name,
                    height=34,
                    corner_radius=8,
                    fg_color=BG,
                    hover_color=ACCENT_SOFT,
                    text_color=TEXT,
                    command=lambda c=cls: self._select(c),
                )
                button.grid(row=row, column=column, sticky="ew", padx=3, pady=3)
                self.figure_buttons[cls] = button
                column += 1
                if column == 2:
                    column = 0
                    row += 1
            if column == 1:
                row += 1
        self.figures_scroll.grid_columnconfigure(0, weight=1)
        self.figures_scroll.grid_columnconfigure(1, weight=1)

    def _select(self, cls):
        self.selected_cls = cls
        for figure_cls, button in self.figure_buttons.items():
            if figure_cls is cls:
                button.configure(fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="#FFFFFF")
            else:
                button.configure(fg_color=BG, hover_color=ACCENT_SOFT, text_color=TEXT)
        self.on_select(cls)

    def update_history(self, entries):
        for widget in self.history_scroll.winfo_children():
            widget.destroy()
        if not entries:
            ctk.CTkLabel(
                self.history_scroll,
                text="No calculations yet.\nResults will appear here.",
                font=ctk.CTkFont(size=12),
                text_color=TEXT_MUTED,
                justify="center",
            ).pack(pady=16)
            return
        for entry in entries:
            row = ctk.CTkFrame(self.history_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            timestamp = entry.get("timestamp", "")[:16]
            label = ctk.CTkButton(
                row,
                text=f'{entry["figure"]}  ·  {timestamp}',
                anchor="w",
                height=30,
                corner_radius=8,
                fg_color=ACCENT_SOFT,
                hover_color=BORDER,
                text_color=TEXT,
                command=lambda e=entry: self.on_history_load(e),
            )
            label.pack(side="left", fill="x", expand=True)
            delete_button = ctk.CTkButton(
                row,
                text="x",
                width=30,
                height=30,
                corner_radius=8,
                fg_color="transparent",
                hover_color=ERROR_SOFT,
                text_color=TEXT_MUTED,
                command=lambda e=entry: self.on_history_delete(e["id"]),
            )
            delete_button.pack(side="left", padx=(4, 0))
