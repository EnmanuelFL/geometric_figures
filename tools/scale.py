from tools.base import ToolScreen


class ScaleTool(ToolScreen):
    tool_key = "scale"
    tool_name = "Calculadora de escala"
    description = "Convierte entre una medida real y su representación en plano para una escala dada (1:X)."

    def _build_form(self, form):
        self._add_entry("value", "Medida", "m", realtime=True)
        self._add_option("scale", "Escala", ["1:10", "1:20", "1:50", "1:100", "1:200", "1:500", "Personalizada"], realtime=True)
        self._add_entry("custom", "Escala personalizada 1:", "X", realtime=True)
        self._add_option("direction", "Dirección", ["Real → Plano", "Plano → Real"], realtime=True)

    def compute(self):
        value = self._get_float("value", "Medida")
        scale_opt = self._get_option("scale")
        if scale_opt == "Personalizada":
            denominator = self._get_float("custom", "Escala personalizada")
        else:
            denominator = float(scale_opt.split(":")[1])
        if denominator <= 0:
            raise ValueError("El denominador de la escala debe ser mayor que cero.")
        direction = self._get_option("direction")

        if direction.startswith("Real"):
            result = value / denominator
            result_label = f"Medida en el plano (1:{denominator:g})"
        else:
            result = value * denominator
            result_label = f"Medida real (1:{denominator:g})"

        params = {"value": value, "scale": scale_opt, "direction": direction}
        results = [
            (result_label, result, "m"),
            ("En centímetros", result * 100, "cm"),
        ]
        return params, results
