import customtkinter as ctk

from ui import theme, t


def _fmt(value, unit):
    if isinstance(value, (int, float)):
        return f"{value:.2f} {unit}".strip()
    return f"{value} {unit}".strip()


class ToolScreen(ctk.CTkFrame):
    tool_key = "tool"
    tool_name = "Tool"
    description = ""

    def __init__(self, master, on_save):
        super().__init__(master, fg_color=t("panel"), corner_radius=12)
        self.on_save = on_save
        self.entry_vars = {}
        self.last_params = None
        self.last_results = None

        self.title_label = ctk.CTkLabel(
            self,
            text=self.tool_name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t("text"),
            anchor="w",
        )
        self.title_label.pack(fill="x", padx=20, pady=(18, 2))

        self.desc_label = ctk.CTkLabel(
            self,
            text=self.description,
            font=ctk.CTkFont(size=13),
            text_color=t("muted"),
            justify="left",
            anchor="w",
            wraplength=560,
        )
        self.desc_label.pack(fill="x", padx=20, pady=(0, 10))

        self.form = ctk.CTkFrame(self, fg_color="transparent")
        self.form.pack(fill="x", padx=20, pady=(0, 12))
        self._build_form(self.form)

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=t("error"),
            justify="left",
            anchor="w",
            wraplength=560,
        )
        self.error_label.pack(fill="x", padx=20, pady=(0, 4))

        self.result_area = ctk.CTkFrame(self, fg_color="transparent")
        self.result_area.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.save_button = ctk.CTkButton(
            self,
            text="Save to history",
            height=34,
            corner_radius=8,
            fg_color=t("accent"),
            hover_color=t("accent_hover"),
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        )
        self.save_button.pack(fill="x", padx=20, pady=(0, 16))

        theme.register(self.apply_theme)

    def _build_form(self, form):
        pass

    def _add_entry(self, name, label, unit="", realtime=False):
        label_text = label + (f" ({unit})" if unit else "")
        row = ctk.CTkFrame(self.form, fg_color="transparent")
        row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            row,
            text=label_text,
            width=170,
            anchor="w",
            text_color=t("text"),
            font=ctk.CTkFont(size=13),
        ).pack(side="left")
        entry = ctk.CTkEntry(
            row,
            height=32,
            corner_radius=8,
            fg_color=t("entry_bg"),
            border_color=t("border"),
            text_color=t("text"),
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 0))
        self.entry_vars[name] = entry
        if realtime:
            entry.bind("<KeyRelease>", lambda e: self.refresh())
        return entry

    def _add_option(self, name, label, options, realtime=False, command=None):
        row = ctk.CTkFrame(self.form, fg_color="transparent")
        row.pack(fill="x", pady=3)
        ctk.CTkLabel(
            row,
            text=label,
            width=170,
            anchor="w",
            text_color=t("text"),
            font=ctk.CTkFont(size=13),
        ).pack(side="left")
        var = ctk.StringVar(value=options[0])
        menu = ctk.CTkOptionMenu(
            row,
            values=list(options),
            variable=var,
            height=32,
            corner_radius=8,
            fg_color=t("section_bg"),
            button_color=t("border"),
            button_hover_color=t("accent_soft"),
            text_color=t("text"),
            command=command,
        )
        menu.pack(side="left", fill="x", expand=True)
        self.entry_vars[name] = var
        if realtime:
            menu.configure(command=lambda v: self.refresh())
        return menu

    def _get_float(self, name, label):
        widget = self.entry_vars[name]
        if isinstance(widget, ctk.CTkEntry):
            raw = widget.get().strip()
        else:
            raw = widget.get().strip()
        if not raw:
            raise ValueError(f"Please enter a value for '{label}'.")
        try:
            return float(raw)
        except ValueError:
            raise ValueError(f"'{raw}' is not a valid number for '{label}'.")

    def _get_option(self, name):
        widget = self.entry_vars[name]
        return widget.get()

    def compute(self):
        raise NotImplementedError

    def refresh(self):
        if not hasattr(self, "result_area"):
            return
        try:
            params, results = self.compute()
        except ValueError as exc:
            self.show_error(str(exc))
            return
        self.last_params = params
        self.last_results = results
        self.show_results(results)

    def _save(self):
        self.refresh()
        if self.last_results:
            self.on_save(self.tool_name, self.last_params, self.last_results)

    def show_results(self, results):
        self.error_label.configure(text="")
        for widget in self.result_area.winfo_children():
            widget.destroy()
        for label, value, unit in results:
            row = ctk.CTkFrame(self.result_area, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=14),
                text_color=t("muted"),
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=_fmt(value, unit),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=t("text"),
            ).pack(side="right")

    def show_error(self, message):
        for widget in self.result_area.winfo_children():
            widget.destroy()
        self.error_label.configure(text=message)

    def set_inputs(self, params):
        for name, value in params.items():
            if name not in self.entry_vars:
                continue
            widget = self.entry_vars[name]
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
                widget.insert(0, str(value))
            else:
                widget.set(str(value))
        self.refresh()

    def apply_theme(self):
        self.configure(fg_color=t("panel"))
        self.title_label.configure(text_color=t("text"))
        self.desc_label.configure(text_color=t("muted"))
        self.error_label.configure(text_color=t("error"))
        self.save_button.configure(fg_color=t("accent"), hover_color=t("accent_hover"))
        for child in self.form.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                for widget in child.winfo_children():
                    if isinstance(widget, ctk.CTkLabel):
                        widget.configure(text_color=t("text"))
                    elif isinstance(widget, ctk.CTkEntry):
                        widget.configure(fg_color=t("entry_bg"), border_color=t("border"), text_color=t("text"))
                    elif isinstance(widget, ctk.CTkOptionMenu):
                        widget.configure(
                            fg_color=t("section_bg"),
                            button_color=t("border"),
                            button_hover_color=t("accent_soft"),
                            text_color=t("text"),
                        )
        if self.last_results:
            self.show_results(self.last_results)
