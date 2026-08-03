import math

from tools.base import ToolScreen


class StairsTool(ToolScreen):
    tool_key = "stairs"
    tool_name = "Stair Calculator"
    description = "Design stairs using the Blondel rule (2·riser + tread = 64 cm) and check normative compliance."

    def _build_form(self, form):
        self._add_entry("rise", "Total rise", "cm", realtime=True)
        self._add_entry("tread", "Desired tread", "cm", realtime=True)
        self.entry_vars["tread"].insert(0, "30")

    def compute(self):
        rise = self._get_float("rise", "Total rise")
        tread = self._get_float("tread", "Desired tread")
        if tread <= 0 or rise <= 0:
            raise ValueError("Both values must be greater than zero.")

        ideal_riser = (64 - tread) / 2
        steps = max(1, int(math.ceil(rise / ideal_riser)))
        riser = rise / steps
        total_run = (steps - 1) * tread

        riser_ok = 13 <= riser <= 20
        tread_ok = 24 <= tread <= 30
        status = "Complies" if (riser_ok and tread_ok) else "Does not comply"

        params = {"rise": rise, "tread": tread}
        results = [
            ("Number of steps", steps, ""),
            ("Riser (contrahuella)", riser, "cm"),
            ("Tread (huella)", tread, "cm"),
            ("Total run in plan", total_run, "cm"),
            ("Normative check", status, ""),
        ]
        return params, results
