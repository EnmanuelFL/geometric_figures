from tools.base import ToolScreen

LENGTH = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
}

AREA = {
    "cm²": 0.0001,
    "m²": 1,
    "km²": 1000000,
    "ft²": 0.092903,
    "acre": 4046.856,
    "hectare": 10000,
}

VOLUME = {
    "cm³": 0.000001,
    "m³": 1,
    "L": 0.001,
    "gallon": 0.00378541,
}

CATEGORIES = {"Longitud": LENGTH, "Área": AREA, "Volumen": VOLUME}


class UnitsTool(ToolScreen):
    tool_key = "units"
    tool_name = "Conversor de unidades"
    description = "Conversión en tiempo real entre unidades comunes de longitud, área y volumen."

    def _build_form(self, form):
        self._add_option("category", "Categoría", ["Longitud", "Área", "Volumen"], realtime=True,
                         command=lambda v: self._rebuild_units())
        self._add_entry("value", "Valor", "", realtime=True)
        self._add_option("from_unit", "De", ["m", "cm", "mm"], realtime=True)
        self._add_option("to_unit", "A", ["cm", "m", "km"], realtime=True)

    def _rebuild_units(self):
        category = self._get_option("category")
        units = list(CATEGORIES[category].keys())
        for widget in self.form.winfo_children():
            widget.destroy()
        self.entry_vars = {}
        self._add_option("category", "Categoría", ["Longitud", "Área", "Volumen"], realtime=True,
                         command=lambda v: self._rebuild_units())
        self._add_entry("value", "Valor", "", realtime=True)
        self._add_option("from_unit", "De", units, realtime=True)
        self._add_option("to_unit", "A", units, realtime=True)
        self.entry_vars["to_unit"].set(units[1] if len(units) > 1 else units[0])
        self.refresh()

    def compute(self):
        category = self._get_option("category")
        value = self._get_float("value", "Valor")
        from_unit = self._get_option("from_unit")
        to_unit = self._get_option("to_unit")
        factors = CATEGORIES[category]
        base = value * factors[from_unit]
        result = base / factors[to_unit]
        params = {"category": category, "value": value, "from": from_unit, "to": to_unit}
        results = [
            (f"Resultado ({category.lower()})", result, to_unit),
        ]
        return params, results
