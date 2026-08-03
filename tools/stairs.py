import math

from tools.base import ToolScreen


class StairsTool(ToolScreen):
    tool_key = "stairs"
    tool_name = "Calculadora de escaleras"
    description = "Diseña escaleras con la regla de Blondel (2·huella + contrahuella = 64 cm) y comprueba el cumplimiento normativo."

    def _build_form(self, form):
        self._add_entry("rise", "Altura a salvar", "cm", realtime=True)
        self._add_entry("tread", "Huella deseada", "cm", realtime=True)
        self.entry_vars["tread"].insert(0, "30")

    def compute(self):
        rise = self._get_float("rise", "Altura a salvar")
        tread = self._get_float("tread", "Huella deseada")
        if tread <= 0 or rise <= 0:
            raise ValueError("Ambos valores deben ser mayores que cero.")

        ideal_riser = (64 - tread) / 2
        steps = max(1, int(math.ceil(rise / ideal_riser)))
        riser = rise / steps
        total_run = (steps - 1) * tread

        riser_ok = 13 <= riser <= 20
        tread_ok = 24 <= tread <= 30
        status = "Cumple" if (riser_ok and tread_ok) else "No cumple"

        params = {"rise": rise, "tread": tread}
        results = [
            ("Número de escalones", steps, ""),
            ("Contrahuella", riser, "cm"),
            ("Huella", tread, "cm"),
            ("Recorrido total en planta", total_run, "cm"),
            ("Comprobación normativa", status, ""),
        ]
        return params, results
