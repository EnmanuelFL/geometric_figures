import customtkinter as ctk

import core.history as history
from figures import (
    Annulus,
    Circle,
    CircularSector,
    Cone,
    Cube,
    Cylinder,
    Rectangle,
    RectangularPrism,
    RectangularPyramid,
    RegularPolygon,
    Sphere,
    Trapeze,
)
from ui import ACCENT, BG
from ui.figure_panel import FigurePanel
from ui.result_panel import ResultPanel

FIGURES_2D = [Circle, Rectangle, Trapeze, RegularPolygon, CircularSector, Annulus]
FIGURES_3D = [Cube, Cylinder, Sphere, RectangularPyramid, Cone, RectangularPrism]
ALL_FIGURES = FIGURES_2D + FIGURES_3D
NAME_TO_CLASS = {cls.name: cls for cls in ALL_FIGURES}


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Geometry Figures")
        self.geometry("1020x700")
        self.minsize(880, 620)
        self.configure(fg_color=BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.figure_panel = FigurePanel(
            self,
            on_select=self.on_select_figure,
            on_history_load=self.on_history_load,
            on_history_delete=self.on_history_delete,
            width=330,
        )
        self.figure_panel.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        self.figure_panel.set_figures(FIGURES_2D, FIGURES_3D)

        self.result_panel = ResultPanel(self, on_calculate=self.on_calculate)
        self.result_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)

        self.figure_panel.update_history(history.load_history())
        self.on_select_figure(FIGURES_2D[0])

    def on_select_figure(self, figure_class):
        self.result_panel.show_figure(figure_class)

    def on_calculate(self, figure, values, results):
        history.add_entry(figure.get_display_name(), values, results)
        self.figure_panel.update_history(history.load_history())

    def on_history_load(self, entry):
        figure_class = NAME_TO_CLASS.get(entry.get("figure"))
        if figure_class:
            self.result_panel.load_entry(figure_class, entry)

    def on_history_delete(self, entry_id):
        history.delete_entry(entry_id)
        self.figure_panel.update_history(history.load_history())
