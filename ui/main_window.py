import customtkinter as ctk

import core.history as history
import core.settings as settings
from figures import (
    Annulus,
    Circle,
    CircularSector,
    Cone,
    Cube,
    Cylinder,
    Ellipse,
    Parallelogram,
    Rectangle,
    RectangularPrism,
    RectangularPyramid,
    RegularPolygon,
    Rhombus,
    Sphere,
    Tetrahedron,
    Torus,
    Trapeze,
    Triangle,
)
from tools.materials import MaterialsTool
from tools.roofs import RoofsTool
from tools.scale import ScaleTool
from tools.slopes import SlopesTool
from tools.stairs import StairsTool
from tools.triangles import TrianglesTool
from tools.units import UnitsTool
from ui import theme, t
from ui.figure_panel import SidebarPanel
from ui.reference_panel import (
    GoldenRatioScreen,
    MaterialsScreen,
    NormativeScreen,
    WeightsScreen,
)
from ui.result_panel import ResultPanel

FIGURES_2D = [
    Circle, Rectangle, Trapeze, RegularPolygon, CircularSector, Annulus,
    Triangle, Ellipse, Rhombus, Parallelogram,
]
FIGURES_3D = [
    Cube, Cylinder, Sphere, RectangularPyramid, Cone, RectangularPrism,
    Torus, Tetrahedron,
]
ALL_FIGURES = FIGURES_2D + FIGURES_3D
NAME_TO_CLASS = {cls.name: cls for cls in ALL_FIGURES}

TOOLS = [
    ("scale", "Scale Calculator", ScaleTool),
    ("materials", "Materials Calculator", MaterialsTool),
    ("stairs", "Stair Calculator", StairsTool),
    ("slopes", "Slope & Ramp Calculator", SlopesTool),
    ("units", "Unit Converter", UnitsTool),
    ("triangles", "Triangle Solver", TrianglesTool),
    ("roofs", "Roof Calculator", RoofsTool),
]
TOOL_KEY_BY_NAME = {cls.tool_name: key for key, _, cls in TOOLS}

REFERENCES = [
    ("materials", "Material strength"),
    ("normative", "Normative dimensions"),
    ("golden", "Golden ratio"),
    ("weights", "Weights per m²"),
]


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Geometry Figures")
        self.geometry("1060x720")
        self.minsize(920, 640)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(self, fg_color=t("panel"), corner_radius=12, height=54)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 8))
        self.topbar.grid_propagate(False)

        self.brand = ctk.CTkLabel(
            self.topbar,
            text="Geometry Figures",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=t("text"),
        )
        self.brand.pack(side="left", padx=16)

        self.theme_toggle = ctk.CTkSegmentedButton(
            self.topbar,
            values=["Light", "Dark"],
            command=self._on_theme,
            selected_color=t("accent"),
            selected_hover_color=t("accent_hover"),
            unselected_color=t("section_bg"),
            unselected_hover_color=t("border"),
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.theme_toggle.pack(side="right", padx=16)

        self.content = ctk.CTkFrame(self, fg_color=t("bg"), corner_radius=0)
        self.content.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(0, 16))

        self.result_panel = ResultPanel(self.content, on_calculate=self.on_calculate)
        self.tool_screens = {}
        self.reference_screens = {}
        self.current_tool_key = None
        self.current_reference_key = None

        self.sidebar = SidebarPanel(
            self,
            on_select_figure=self.on_select_figure,
            on_history_load=self.on_history_load,
            on_history_delete=self.on_history_delete,
            on_tool_select=self.on_tool_select,
            on_reference_select=self.on_reference_select,
            on_section_change=self.on_section_change,
            width=330,
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(0, 16))
        self.sidebar.set_figures(FIGURES_2D, FIGURES_3D)
        self.sidebar.set_tools([(key, label) for key, label, _ in TOOLS])
        self.sidebar.set_references(REFERENCES)
        self.sidebar.update_history(history.load_history())
        self.on_select_figure(FIGURES_2D[0])

        theme.register(self.apply_theme)
        saved = settings.get_theme()
        self.theme_toggle.set(saved.title())
        theme.set_mode(saved)

    def apply_theme(self):
        self.configure(fg_color=t("bg"))
        self.topbar.configure(fg_color=t("panel"))
        self.brand.configure(text_color=t("text"))
        self.content.configure(fg_color=t("bg"))
        self.theme_toggle.configure(
            selected_color=t("accent"),
            selected_hover_color=t("accent_hover"),
            unselected_color=t("section_bg"),
            unselected_hover_color=t("border"),
        )

    def _on_theme(self, value):
        mode = value.lower()
        theme.set_mode(mode)
        settings.set_theme(mode)

    def show_content(self, widget):
        for child in self.content.winfo_children():
            child.pack_forget()
        widget.pack(fill="both", expand=True)

    def on_section_change(self, section):
        if section == "Figures":
            self.show_content(self.result_panel)
        elif section == "Tools":
            if self.current_tool_key in self.tool_screens:
                self.show_content(self.tool_screens[self.current_tool_key])
            else:
                self.on_tool_select(TOOLS[0][0])
        else:
            if self.current_reference_key in self.reference_screens:
                self.show_content(self.reference_screens[self.current_reference_key])
            else:
                self.on_reference_select(REFERENCES[0][0])

    def on_select_figure(self, figure_class):
        self.show_content(self.result_panel)
        self.result_panel.show_figure(figure_class)

    def on_tool_select(self, key):
        if key not in self.tool_screens:
            tool_class = {k: cls for k, _, cls in TOOLS}[key]
            self.tool_screens[key] = tool_class(self.content, on_save=self.on_tool_save)
        self.current_tool_key = key
        self.show_content(self.tool_screens[key])

    def on_reference_select(self, key):
        if key not in self.reference_screens:
            screen_class = {
                "materials": MaterialsScreen,
                "normative": NormativeScreen,
                "golden": GoldenRatioScreen,
                "weights": WeightsScreen,
            }[key]
            self.reference_screens[key] = screen_class(self.content)
        self.current_reference_key = key
        self.show_content(self.reference_screens[key])

    def on_calculate(self, figure, values, results):
        history.add_entry(figure.get_display_name(), values, results)
        self.refresh_history()

    def on_tool_save(self, tool_name, parameters, results):
        history.add_entry(tool_name, parameters, results, module="tools")
        self.refresh_history()

    def refresh_history(self):
        self.sidebar.update_history(history.load_history())

    def on_history_load(self, entry):
        module = entry.get("module", "figures")
        if module == "tools":
            key = TOOL_KEY_BY_NAME.get(entry.get("figure"))
            if key:
                self.sidebar.set_section("Tools")
                self.on_tool_select(key)
                self.tool_screens[key].set_inputs(entry.get("parameters", {}))
            return
        figure_class = NAME_TO_CLASS.get(entry.get("figure"))
        if figure_class:
            self.sidebar.set_section("Figures")
            self.result_panel.load_entry(figure_class, entry)

    def on_history_delete(self, entry_id):
        history.delete_entry(entry_id)
        self.refresh_history()
