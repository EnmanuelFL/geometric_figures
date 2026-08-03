import math

from tools.base import ToolScreen

BRICK_W = 0.24
BRICK_H = 0.075
JOINT = 0.01


class MaterialsTool(ToolScreen):
    tool_key = "materials"
    tool_name = "Calculadora de materiales"
    description = "Estima los materiales para un área dada, incluyendo un 10% de margen de desperdicio."

    def _build_form(self, form):
        self._add_entry("area", "Área", "m²", realtime=True)
        self._add_option(
            "material",
            "Material",
            ["Ladrillo", "Baldosa", "Pintura", "Hormigón", "Enlucido / Mortero"],
            realtime=True,
            command=lambda v: self._rebuild_subform(),
        )
        self.sub_form = None
        self._rebuild_subform()

    def _rebuild_subform(self):
        for widget in self.form.winfo_children():
            widget.destroy()
        self.entry_vars = {}
        self._add_entry("area", "Área", "m²", realtime=True)
        self._add_option(
            "material",
            "Material",
            ["Ladrillo", "Baldosa", "Pintura", "Hormigón", "Enlucido / Mortero"],
            realtime=True,
            command=lambda v: self._rebuild_subform(),
        )
        material = self._get_option("material")
        if material == "Baldosa":
            self._add_option("tile", "Formato de baldosa", ["30×30 cm", "45×45 cm", "60×60 cm", "90×90 cm"], realtime=True)
        elif material == "Pintura":
            self._add_entry("paint_yield", "Rendimiento de pintura", "m²/L", realtime=True)
            self.entry_vars["paint_yield"].insert(0, "11")
        elif material == "Hormigón":
            self._add_entry("thickness", "Espesor", "cm", realtime=True)
            self.entry_vars["thickness"].insert(0, "15")
        elif material == "Enlucido / Mortero":
            self._add_entry("rate", "Consumo", "kg/m²", realtime=True)
            self.entry_vars["rate"].insert(0, "17")
        self.refresh()

    def compute(self):
        area = self._get_float("area", "Área")
        material = self._get_option("material")

        if material == "Ladrillo":
            per_m2 = 1 / ((BRICK_W + JOINT) * (BRICK_H + JOINT))
            quantity = area * per_m2
            unit = "ladrillos"
        elif material == "Baldosa":
            size = float(self._get_option("tile").split("×")[0]) / 100
            quantity = area / (size * size)
            unit = "baldosas"
        elif material == "Pintura":
            paint_yield = self._get_float("paint_yield", "Rendimiento de pintura")
            if paint_yield <= 0:
                raise ValueError("El rendimiento de pintura debe ser mayor que cero.")
            quantity = area / paint_yield
            unit = "L"
        elif material == "Hormigón":
            thickness = self._get_float("thickness", "Espesor") / 100
            quantity = area * thickness
            unit = "m³"
        else:
            rate = self._get_float("rate", "Consumo")
            quantity = area * rate
            unit = "kg"

        params = {"area": area, "material": material}
        results = [
            (f"Cantidad exacta ({material})", quantity, unit),
            ("Con 10% de desperdicio", quantity * 1.1, unit),
        ]
        if material == "Ladrillo":
            params["per_m2"] = per_m2
        return params, results
