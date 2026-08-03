from tools.base import ToolScreen


class ScaleTool(ToolScreen):
    tool_key = "scale"
    tool_name = "Scale Calculator"
    description = "Convert between a real measurement and its plan representation for a given scale (1:X)."

    def _build_form(self, form):
        self._add_entry("value", "Measurement", "m", realtime=True)
        self._add_option("scale", "Scale", ["1:10", "1:20", "1:50", "1:100", "1:200", "1:500", "Custom"], realtime=True)
        self._add_entry("custom", "Custom scale 1:", "X", realtime=True)
        self._add_option("direction", "Direction", ["Real → Plan", "Plan → Real"], realtime=True)

    def compute(self):
        value = self._get_float("value", "Measurement")
        scale_opt = self._get_option("scale")
        if scale_opt == "Custom":
            denominator = self._get_float("custom", "Custom scale")
        else:
            denominator = float(scale_opt.split(":")[1])
        if denominator <= 0:
            raise ValueError("Scale denominator must be greater than zero.")
        direction = self._get_option("direction")

        if direction.startswith("Real"):
            result = value / denominator
            result_label = f"Plan measurement (1:{denominator:g})"
        else:
            result = value * denominator
            result_label = f"Real measurement (1:{denominator:g})"

        params = {"value": value, "scale": scale_opt, "direction": direction}
        results = [
            (result_label, result, "m"),
            ("In centimetres", result * 100, "cm"),
        ]
        return params, results
