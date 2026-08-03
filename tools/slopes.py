import math

from tools.base import ToolScreen


class SlopesTool(ToolScreen):
    tool_key = "slopes"
    tool_name = "Calculadora de pendientes y rampas"
    description = "Calcula el porcentaje de pendiente, el ángulo y la longitud real. Comprueba la accesibilidad (rampas ≤ 8%)."

    def _build_form(self, form):
        self._add_option("method", "Modo de entrada", ["Desnivel + longitud", "Ángulo + longitud"], realtime=True)
        self._add_entry("rise", "Desnivel vertical", "m", realtime=True)
        self._add_entry("length", "Longitud horizontal", "m", realtime=True)
        self._add_entry("angle", "Ángulo", "°", realtime=True)

    def compute(self):
        method = self._get_option("method")
        length = self._get_float("length", "Longitud horizontal")
        if length <= 0:
            raise ValueError("La longitud horizontal debe ser mayor que cero.")

        if method.startswith("Desnivel"):
            rise = self._get_float("rise", "Desnivel vertical")
            if rise < 0:
                raise ValueError("El desnivel vertical debe ser cero o mayor.")
            percent = rise / length * 100
            angle = math.degrees(math.atan(rise / length))
            real_length = math.hypot(rise, length)
            params = {"method": method, "rise": rise, "length": length}
        else:
            angle = self._get_float("angle", "Ángulo")
            if angle < 0 or angle >= 90:
                raise ValueError("El ángulo debe estar entre 0 y 90 grados.")
            rise = length * math.tan(math.radians(angle))
            percent = rise / length * 100
            real_length = length / math.cos(math.radians(angle))
            params = {"method": method, "angle": angle, "length": length}

        accessible = "Accesible" if percent <= 8 else "No accesible (límite 8%)"
        results = [
            ("Pendiente", percent, "%"),
            ("Ángulo", angle, "°"),
            ("Longitud real", real_length, "m"),
            ("Desnivel vertical", rise, "m"),
            ("Accesibilidad", accessible, ""),
        ]
        return params, results
