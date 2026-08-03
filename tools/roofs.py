import math

from tools.base import ToolScreen


class RoofsTool(ToolScreen):
    tool_key = "roofs"
    tool_name = "Roof Calculator"
    description = "Estimate real roof area and the volume under the roof for common roof types."

    def _build_form(self, form):
        self._add_option("roof_type", "Roof type", ["Flat", "Single-slope", "Gable", "Hip"], realtime=True)
        self._add_entry("length", "Plan length", "m", realtime=True)
        self._add_entry("width", "Plan width", "m", realtime=True)
        self._add_entry("slope", "Slope", "%", realtime=True)
        self.entry_vars["slope"].insert(0, "15")

    def compute(self):
        roof_type = self._get_option("roof_type")
        length = self._get_float("length", "Plan length")
        width = self._get_float("width", "Plan width")
        slope = self._get_float("slope", "Slope")
        if slope < 0:
            raise ValueError("Slope must be zero or greater.")

        base_area = length * width
        theta = math.atan(slope / 100)
        cos_theta = math.cos(theta)

        if roof_type == "Flat":
            roof_area = base_area
            ridge = 0.0
            volume = 0.0
        elif roof_type == "Single-slope":
            roof_area = base_area / cos_theta
            ridge = width * slope / 100
            volume = 0.5 * width * ridge * length
        elif roof_type == "Gable":
            roof_area = base_area / cos_theta
            ridge = width / 2 * slope / 100
            volume = 0.5 * width * ridge * length
        else:
            roof_area = base_area / cos_theta
            ridge = width / 2 * slope / 100
            volume = (1 / 3) * base_area * ridge

        params = {"roof_type": roof_type, "length": length, "width": width, "slope": slope}
        results = [
            ("Roof real area", roof_area, "m²"),
            ("Volume under roof", volume, "m³"),
            ("Ridge height", ridge, "m"),
            ("Slope angle", math.degrees(theta), "°"),
        ]
        return params, results
