import customtkinter as ctk

from ui import theme, t


class SidebarPanel(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_select_figure,
        on_history_load,
        on_history_delete,
        on_tool_select,
        on_reference_select,
        on_section_change,
        **kwargs,
    ):
        super().__init__(master, fg_color=t("panel"), corner_radius=12, **kwargs)
        self.on_select_figure = on_select_figure
        self.on_history_load = on_history_load
        self.on_history_delete = on_history_delete
        self.on_tool_select = on_tool_select
        self.on_reference_select = on_reference_select
        self.on_section_change = on_section_change
        self.figure_buttons = {}
        self.selected_cls = None
        self._tools = []
        self._references = []
        self._history_entries = []

        self.nav = ctk.CTkSegmentedButton(
            self,
            values=["Figuras", "Herramientas", "Referencia"],
            command=self._on_nav,
            selected_color=t("accent"),
            selected_hover_color=t("accent_hover"),
            unselected_color=t("section_bg"),
            unselected_hover_color=t("border"),
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.nav.pack(fill="x", padx=12, pady=(14, 10))

        self.view_area = ctk.CTkFrame(self, fg_color="transparent", height=340)
        self.view_area.pack(fill="x", padx=8, pady=(0, 6))
        self.view_area.pack_propagate(False)

        self.figures_view = ctk.CTkScrollableFrame(self.view_area, fg_color="transparent", corner_radius=0)
        self.tools_view = ctk.CTkScrollableFrame(self.view_area, fg_color="transparent", corner_radius=0)
        self.reference_view = ctk.CTkScrollableFrame(self.view_area, fg_color="transparent", corner_radius=0)

        separator = ctk.CTkFrame(self, height=1, fg_color=t("border"), corner_radius=0)
        self.separator = separator
        separator.pack(fill="x", padx=16, pady=4)

        history_header = ctk.CTkLabel(
            self,
            text="Historial",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=t("text"),
        )
        history_header.pack(anchor="w", padx=16, pady=(4, 0))

        history_subtitle = ctk.CTkLabel(
            self,
            text="Últimos 20 cálculos",
            font=ctk.CTkFont(size=11),
            text_color=t("muted"),
        )
        history_subtitle.pack(anchor="w", padx=16, pady=(0, 4))

        self.history_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.history_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 12))

        self.set_section("Figuras")
        self.update_history([])
        theme.register(self.apply_theme)

    def apply_theme(self):
        self.configure(fg_color=t("panel"))
        self.nav.configure(
            selected_color=t("accent"),
            selected_hover_color=t("accent_hover"),
            unselected_color=t("section_bg"),
            unselected_hover_color=t("border"),
        )
        self.separator.configure(fg_color=t("border"))
        for scrollable in (self.figures_view, self.tools_view, self.reference_view, self.history_scroll):
            scrollable.configure(fg_color="transparent")
        if self.figure_buttons:
            self.set_figures(self.figures_2d, self.figures_3d)
        if self._tools:
            self.set_tools(self._tools)
        if self._references:
            self.set_references(self._references)
        if self._history_entries is not None:
            self.update_history(self._history_entries)
        if self.selected_cls:
            self._select(self.selected_cls)

    def set_section(self, section):
        self.nav.set(section)
        self._show_view(section)

    def _on_nav(self, value):
        self._show_view(value)
        self.on_section_change(value)

    def _show_view(self, section):
        for view in (self.figures_view, self.tools_view, self.reference_view):
            view.pack_forget()
        view = {
            "Figuras": self.figures_view,
            "Herramientas": self.tools_view,
            "Referencia": self.reference_view,
        }[section]
        view.pack(fill="both", expand=True)

    def set_figures(self, figures_2d, figures_3d):
        self.figures_2d = figures_2d
        self.figures_3d = figures_3d
        for widget in self.figures_view.winfo_children():
            widget.destroy()
        self.figure_buttons = {}
        row = 0
        for title, group in (("2D", figures_2d), ("3D", figures_3d)):
            section = ctk.CTkLabel(
                self.figures_view,
                text=title,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=t("muted"),
            )
            section.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
            row += 1
            column = 0
            for cls in group:
                button = ctk.CTkButton(
                    self.figures_view,
                    text=cls.name,
                    height=32,
                    corner_radius=8,
                    fg_color=t("section_bg"),
                    hover_color=t("accent_soft"),
                    text_color=t("text"),
                    command=lambda c=cls: self._select(c),
                )
                button.grid(row=row, column=column, sticky="ew", padx=3, pady=2)
                self.figure_buttons[cls] = button
                column += 1
                if column == 2:
                    column = 0
                    row += 1
            if column == 1:
                row += 1
        self.figures_view.grid_columnconfigure(0, weight=1)
        self.figures_view.grid_columnconfigure(1, weight=1)

    def set_tools(self, tools):
        self._tools = list(tools)
        for widget in self.tools_view.winfo_children():
            widget.destroy()
        for key, label in tools:
            button = ctk.CTkButton(
                self.tools_view,
                text=label,
                height=34,
                corner_radius=8,
                anchor="w",
                fg_color=t("section_bg"),
                hover_color=t("accent_soft"),
                text_color=t("text"),
                command=lambda k=key: self._select_tool(k),
            )
            button.pack(fill="x", padx=6, pady=3)

    def set_references(self, references):
        self._references = list(references)
        for widget in self.reference_view.winfo_children():
            widget.destroy()
        for key, label in references:
            button = ctk.CTkButton(
                self.reference_view,
                text=label,
                height=34,
                corner_radius=8,
                anchor="w",
                fg_color=t("section_bg"),
                hover_color=t("accent_soft"),
                text_color=t("text"),
                command=lambda k=key: self._select_reference(k),
            )
            button.pack(fill="x", padx=6, pady=3)

    def _select(self, cls):
        self.selected_cls = cls
        for figure_cls, button in self.figure_buttons.items():
            if figure_cls is cls:
                button.configure(fg_color=t("accent"), hover_color=t("accent_hover"), text_color="#FFFFFF")
            else:
                button.configure(fg_color=t("section_bg"), hover_color=t("accent_soft"), text_color=t("text"))
        self.on_select_figure(cls)

    def _select_tool(self, key):
        self.set_section("Herramientas")
        self.on_tool_select(key)

    def _select_reference(self, key):
        self.set_section("Referencia")
        self.on_reference_select(key)

    def update_history(self, entries):
        self._history_entries = list(entries)
        for widget in self.history_scroll.winfo_children():
            widget.destroy()
        if not entries:
            ctk.CTkLabel(
                self.history_scroll,
                text="Aún no hay cálculos.\nLos resultados aparecerán aquí.",
                font=ctk.CTkFont(size=12),
                text_color=t("muted"),
                justify="center",
            ).pack(pady=16)
            return
        for entry in entries:
            row = ctk.CTkFrame(self.history_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            timestamp = entry.get("timestamp", "")[:16]
            module = entry.get("module", "figures")
            module_tag = {"tools": "herramientas", "reference": "referencia"}.get(module, module)
            tag = f"[{module_tag}]" if module != "figures" else ""
            label = ctk.CTkButton(
                row,
                text=f'{tag} {entry["figure"]}  ·  {timestamp}'.strip(),
                anchor="w",
                height=30,
                corner_radius=8,
                fg_color=t("accent_soft"),
                hover_color=t("border"),
                text_color=t("text"),
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
                hover_color=t("error_soft"),
                text_color=t("muted"),
                command=lambda e=entry: self.on_history_delete(e["id"]),
            )
            delete_button.pack(side="left", padx=(4, 0))
