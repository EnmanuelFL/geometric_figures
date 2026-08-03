import tkinter as tk

import customtkinter as ctk

from ui import ACCENT, ACCENT_SOFT, BORDER, CANVAS_BG, ERROR, PANEL, SUCCESS, TEXT, TEXT_MUTED
from ui.drawer import draw


class ResultPanel(ctk.CTkFrame):
    def __init__(self, master, on_calculate, **kwargs):
        super().__init__(master, fg_color=PANEL, corner_radius=12, **kwargs)
        self.on_calculate = on_calculate
        self.figure_class = None
        self.entries = {}
        self.current_values = None
        self.current_results = None

        self.title_label = ctk.CTkLabel(
            self,
            text="No figure selected",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT,
            anchor="w",
        )
        self.title_label.pack(fill="x", padx=20, pady=(18, 2))

        self.desc_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=520,
        )
        self.desc_label.pack(fill="x", padx=20, pady=(0, 8))

        self.formula_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color=ACCENT,
            fg_color=ACCENT_SOFT,
            corner_radius=8,
            anchor="w",
            padx=12,
            pady=6,
        )
        self.formula_label.pack(fill="x", padx=20, pady=(0, 12))

        self.canvas_box = ctk.CTkFrame(self, fg_color=CANVAS_BG, corner_radius=10)
        self.canvas_box.pack(fill="x", padx=20, pady=(0, 12))
        self.canvas = tk.Canvas(
            self.canvas_box,
            width=540,
            height=190,
            bg=CANVAS_BG,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.canvas.pack(padx=6, pady=6)

        self.form = ctk.CTkFrame(self, fg_color="transparent")
        self.form.pack(fill="x", padx=20, pady=(0, 12))

        self.calc_button = ctk.CTkButton(
            self,
            text="Calculate",
            height=38,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color="#453E9E",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._calculate,
        )
        self.calc_button.pack(fill="x", padx=20, pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=ERROR,
            justify="left",
            anchor="w",
            wraplength=520,
        )
        self.error_label.pack(fill="x", padx=20, pady=(0, 4))

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=SUCCESS,
            justify="left",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=20, pady=(0, 4))

        self.results = ctk.CTkFrame(self, fg_color="transparent")
        self.results.pack(fill="both", expand=True, padx=20, pady=(0, 18))

    def show_figure(self, figure_class):
        self.figure_class = figure_class
        self.current_values = None
        self.current_results = None
        self.error_label.configure(text="")
        self.status_label.configure(text="")
        self.canvas.delete("all")

        figure = figure_class()
        self.title_label.configure(text=figure.get_display_name())
        self.desc_label.configure(text=figure.get_description())
        self.formula_label.configure(text=figure.get_formula())

        self._build_form(figure)
        self._clear_results()

    def _build_form(self, figure):
        for widget in self.form.winfo_children():
            widget.destroy()
        self.entries = {}
        for index, param in enumerate(figure.get_parameters()):
            label_text = param["label"]
            if param["unit"]:
                label_text += f" ({param['unit']})"
            label = ctk.CTkLabel(
                self.form,
                text=label_text,
                font=ctk.CTkFont(size=13),
                text_color=TEXT,
                anchor="w",
            )
            label.grid(row=index, column=0, sticky="w", padx=(0, 12), pady=4)
            entry = ctk.CTkEntry(
                self.form,
                height=32,
                corner_radius=8,
                fg_color=CANVAS_BG,
                border_color=BORDER,
                text_color=TEXT,
            )
            entry.grid(row=index, column=1, sticky="ew", pady=4)
            self.entries[param["name"]] = entry
        self.form.grid_columnconfigure(1, weight=1)

    def _parse_values(self):
        values = {}
        figure = self.figure_class()
        for param in figure.get_parameters():
            name, label = param["name"], param["label"]
            raw = self.entries[name].get().strip()
            if not raw:
                return None, f"Please enter a value for '{label}'."
            try:
                value = float(raw)
            except ValueError:
                return None, f"'{raw}' is not a valid number for '{label}'."
            if value <= 0:
                return None, f"'{label}' must be greater than zero."
            if name == "sides" and (value != int(value) or int(value) < 3):
                return None, "'Number of sides (n)' must be an integer of at least 3."
            if name == "angle" and value > 360:
                return None, "'Angle' must be between 0 and 360 degrees."
            values[name] = value
        if self.figure_class.__name__ == "Annulus" and values.get("radio_inner") >= values.get("radio"):
            return None, "Inner radius must be smaller than outer radius."
        return values, None

    def _calculate(self):
        values, error = self._parse_values()
        if error:
            self.show_error(error)
            return
        figure = self.figure_class()
        figure.set_values(values)
        try:
            results = figure.calculate_results()
        except Exception as exc:
            self.show_error(f"Calculation failed: {exc}")
            return
        draw(self.canvas, figure, values)
        self._show_results(results)
        self.current_values = {k: v for k, v in values.items()}
        self.current_results = [[label, value, unit] for label, value, unit in results]
        self.status_label.configure(text="Saved to history.")
        self.on_calculate(figure, self.current_values, self.current_results)

    def load_entry(self, figure_class, entry):
        self.show_figure(figure_class)
        parameters = entry.get("parameters", {})
        for name, entry_widget in self.entries.items():
            if name in parameters:
                entry_widget.delete(0, "end")
                entry_widget.insert(0, str(parameters[name]))
        figure = figure_class()
        figure.set_values(parameters)
        draw(self.canvas, figure, parameters)
        results = [(label, float(value), unit) for label, value, unit in entry.get("results", [])]
        self._show_results(results)
        self.current_values = dict(parameters)
        self.current_results = entry.get("results", [])

    def show_error(self, message):
        self.status_label.configure(text="")
        self.error_label.configure(text=message)
        self._clear_results()

    def _show_results(self, results):
        self.error_label.configure(text="")
        self._clear_results()
        for label, value, unit in results:
            row = ctk.CTkFrame(self.results, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_MUTED,
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=f"{value:.2f} {unit}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=TEXT,
            ).pack(side="right")

    def _clear_results(self):
        for widget in self.results.winfo_children():
            widget.destroy()
