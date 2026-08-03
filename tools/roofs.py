import math

from tools.base import ToolScreen


class RoofsTool(ToolScreen):
    tool_key = "roofs"
    tool_name = "Calculadora de techos"
    description = "Estima el área real del techo y el volumen bajo cubierta para los tipos de techo más comunes."

    def _build_form(self, form):
        self._add_option("roof_type", "Tipo de techo", ["Plano", "A un agua", "A dos aguas", "A cuatro aguas"], realtime=True)
        self._add_entry("length", "Largo en planta", "m", realtime=True)
        self._add_entry("width", "Ancho en planta", "m", realtime=True)
        self._add_entry("slope", "Pendiente", "%", realtime=True)
        self.entry_vars["slope"].insert(0, "15")

    def compute(self):
        roof_type = self._get_option("roof_type")
        length = self._get_float("length", "Largo en planta")
        width = self._get_float("width", "Ancho en planta")
        slope = self._get_float("slope", "Pendiente")
        if slope < 0:
            raise ValueError("La pendiente debe ser cero o mayor.")

        base_area = length * width
        theta = math.atan(slope / 100)
        cos_theta = math.cos(theta)

        if roof_type == "Plano":
            roof_area = base_area
            ridge = 0.0
            volume = 0.0
        elif roof_type == "A un agua":
            roof_area = base_area / cos_theta
            ridge = width * slope / 100
            volume = 0.5 * width * ridge * length
        elif roof_type == "A dos aguas":
            roof_area = base_area / cos_theta
            ridge = width / 2 * slope / 100
            volume = 0.5 * width * ridge * length
        else:
            roof_area = base_area / cos_theta
            ridge = width / 2 * slope / 100
            volume = (1 / 3) * base_area * ridge

        params = {"roof_type": roof_type, "length": length, "width": width, "slope": slope}
        results = [
            ("Área real del techo", roof_area, "m²"),
            ("Volumen bajo cubierta", volume, "m³"),
            ("Altura de cumbrera", ridge, "m"),
            ("Ángulo de pendiente", math.degrees(theta), "°"),
        ]
        return params, results
