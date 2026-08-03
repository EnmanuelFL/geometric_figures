import tkinter as tk

import customtkinter as ctk

from ui import theme, t
from ui.drawer import draw


def _fmt(value, unit):
    if isinstance(value, (int, float)):
        return f"{value:.2f} {unit}".strip()
    return f"{value} {unit}".strip()


class ResultPanel(ctk.CTkFrame):
    def __init__(self, master, on_calculate, **kwargs):
        super().__init__(master, fg_color=t("panel"), corner_radius=12, **kwargs)
        self.on_calculate = on_calculate
        self.figure_class = None
        self.entries = {}
        self.current_values = None
        self.current_results = None
        self.current_figure = None
        self.live_values = None

        self.title_label = ctk.CTkLabel(
            self,
            text="Ninguna figura seleccionada",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t("text"),
            anchor="w",
        )
        self.title_label.pack(fill="x", padx=20, pady=(18, 2))
        self.desc_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=t("muted"),
            justify="left",
            anchor="w",
            wraplength=520,
        )
        self.desc_label.pack(fill="x", padx=20, pady=(0, 8))

        self.formula_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color=t("accent"),
            fg_color=t("accent_soft"),
            corner_radius=8,
            anchor="w",
            padx=12,
            pady=6,
        )
        self.formula_label.pack(fill="x", padx=20, pady=(0, 12))

        self.canvas_box = ctk.CTkFrame(self, fg_color=t("canvas_bg"), corner_radius=10)
        self.canvas_box.pack(fill="x", padx=20, pady=(0, 12))
        self.canvas = tk.Canvas(
            self.canvas_box,
            width=640,
            height=240,
            bg=t("canvas_bg"),
            highlightthickness=1,
            highlightbackground=t("border"),
        )
        self.canvas.pack(padx=6, pady=6)

        self.form = ctk.CTkFrame(self, fg_color="transparent")
        self.form.pack(fill="x", padx=20, pady=(0, 12))

        self.calc_button = ctk.CTkButton(
            self,
            text="Calcular",
            height=38,
            corner_radius=8,
            fg_color=t("accent"),
            hover_color=t("accent_hover"),
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._calculate,
        )
        self.calc_button.pack(fill="x", padx=20, pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=t("error"),
            justify="left",
            anchor="w",
            wraplength=520,
        )
        self.error_label.pack(fill="x", padx=20, pady=(0, 4))

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=t("success"),
            justify="left",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=20, pady=(0, 4))

        self.results = ctk.CTkFrame(self, fg_color="transparent")
        self.results.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        theme.register(self.apply_theme)

    def apply_theme(self):
        self.configure(fg_color=t("panel"))
        self.title_label.configure(text_color=t("text"))
        self.desc_label.configure(text_color=t("muted"))
        self.formula_label.configure(text_color=t("accent"), fg_color=t("accent_soft"))
        self.canvas_box.configure(fg_color=t("canvas_bg"))
        self.canvas.configure(bg=t("canvas_bg"), highlightbackground=t("border"))
        self.calc_button.configure(fg_color=t("accent"), hover_color=t("accent_hover"))
        self.error_label.configure(text_color=t("error"))
        self.status_label.configure(text_color=t("success"))
        for child in self.form.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                child.configure(fg_color=t("entry_bg"), border_color=t("border"), text_color=t("text"))
            elif isinstance(child, ctk.CTkLabel):
                child.configure(text_color=t("text"))
        if self.current_figure is not None and self.current_values is not None:
            draw(self.canvas, self.current_figure, self.current_values, theme.palette)
        elif self.figure_class is not None and self.live_values:
            figure = self.figure_class()
            figure.set_values(self.live_values)
            draw(self.canvas, figure, self.live_values, theme.palette)
        if self.current_results is not None:
            self._show_results(self.current_results)

    def show_figure(self, figure_class):
        self.figure_class = figure_class
        self.current_values = None
        self.current_results = None
        self.current_figure = None
        self.live_values = None
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
                text_color=t("text"),
                anchor="w",
            )
            label.grid(row=index, column=0, sticky="w", padx=(0, 12), pady=4)
            entry = ctk.CTkEntry(
                self.form,
                height=32,
                corner_radius=8,
                fg_color=t("entry_bg"),
                border_color=t("border"),
                text_color=t("text"),
            )
            entry.grid(row=index, column=1, sticky="ew", pady=4)
            entry.bind("<KeyRelease>", lambda e: self._live_draw())
            self.entries[param["name"]] = entry
        self.form.grid_columnconfigure(1, weight=1)

    def _parse_values(self):
        values = {}
        figure = self.figure_class()
        for param in figure.get_parameters():
            name, label = param["name"], param["label"]
            raw = self.entries[name].get().strip()
            if not raw:
                return None, f"Introduce un valor para '{label}'."
            try:
                value = float(raw)
            except ValueError:
                return None, f"'{raw}' no es un número válido para '{label}'."
            if value <= 0:
                return None, f"'{label}' debe ser mayor que cero."
            if name == "sides" and (value != int(value) or int(value) < 3):
                return None, "El número de lados (n) debe ser un entero de al menos 3."
            if name == "angle" and value > 360:
                return None, "El ángulo debe estar entre 0 y 360 grados."
            values[name] = value
        return values, None

    def _live_draw(self):
        if self.figure_class is None:
            return
        figure = self.figure_class()
        values = {}
        for param in figure.get_parameters():
            name = param["name"]
            raw = self.entries[name].get().strip()
            try:
                value = float(raw)
            except (ValueError, AttributeError):
                continue
            if value > 0:
                values[name] = value
        if not values:
            self.live_values = None
            self.canvas.delete("all")
            return
        self.live_values = values
        figure.set_values(values)
        draw(self.canvas, figure, values, theme.palette)

    def _calculate(self):
        values, error = self._parse_values()
        if error:
            self.show_error(error)
            return
        figure = self.figure_class()
        figure.set_values(values)
        geometry_error = figure.validate()
        if geometry_error:
            self.show_error(geometry_error)
            return
        try:
            results = figure.calculate_results()
        except Exception as exc:
            self.show_error(f"Error en el cálculo: {exc}")
            return
        draw(self.canvas, figure, values, theme.palette)
        self._show_results(results)
        self.current_values = {k: v for k, v in values.items()}
        self.current_results = [[label, value, unit] for label, value, unit in results]
        self.current_figure = figure
        self.live_values = None
        self.status_label.configure(text="Guardado en el historial.")
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
        draw(self.canvas, figure, parameters, theme.palette)
        results = [(label, value, unit) for label, value, unit in entry.get("results", [])]
        self._show_results(results)
        self.current_values = dict(parameters)
        self.current_results = entry.get("results", [])
        self.current_figure = figure

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
                text_color=t("muted"),
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=_fmt(value, unit),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=t("text"),
            ).pack(side="right")

    def _clear_results(self):
        for widget in self.results.winfo_children():
            widget.destroy()
