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

CATEGORIES = {"Length": LENGTH, "Area": AREA, "Volume": VOLUME}


class UnitsTool(ToolScreen):
    tool_key = "units"
    tool_name = "Unit Converter"
    description = "Real-time conversion between common length, area and volume units."

    def _build_form(self, form):
        self._add_option("category", "Category", ["Length", "Area", "Volume"], realtime=True,
                         command=lambda v: self._rebuild_units())
        self._add_entry("value", "Value", "", realtime=True)
        self._add_option("from_unit", "From", ["m", "cm", "mm"], realtime=True)
        self._add_option("to_unit", "To", ["cm", "m", "km"], realtime=True)

    def _rebuild_units(self):
        category = self._get_option("category")
        units = list(CATEGORIES[category].keys())
        for widget in self.form.winfo_children():
            widget.destroy()
        self.entry_vars = {}
        self._add_option("category", "Category", ["Length", "Area", "Volume"], realtime=True,
                         command=lambda v: self._rebuild_units())
        self._add_entry("value", "Value", "", realtime=True)
        self._add_option("from_unit", "From", units, realtime=True)
        self._add_option("to_unit", "To", units, realtime=True)
        self.entry_vars["to_unit"].set(units[1] if len(units) > 1 else units[0])
        self.refresh()

    def compute(self):
        category = self._get_option("category")
        value = self._get_float("value", "Value")
        from_unit = self._get_option("from_unit")
        to_unit = self._get_option("to_unit")
        factors = CATEGORIES[category]
        base = value * factors[from_unit]
        result = base / factors[to_unit]
        params = {"category": category, "value": value, "from": from_unit, "to": to_unit}
        results = [
            (f"Result ({category.lower()})", result, to_unit),
        ]
        return params, results
