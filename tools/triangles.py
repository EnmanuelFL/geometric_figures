import math

from tools.base import ToolScreen


def _deg(rad):
    return math.degrees(rad)


def _triangle_type(a, b, c):
    sides = sorted([a, b, c])
    if sides[0] + sides[1] <= sides[2]:
        return "Inválido"
    if math.isclose(a, b, rel_tol=1e-9) and math.isclose(b, c, rel_tol=1e-9):
        return "Equilátero"
    if math.isclose(a, b, rel_tol=1e-9) or math.isclose(b, c, rel_tol=1e-9) or math.isclose(a, c, rel_tol=1e-9):
        return "Isósceles"
    return "Escaleno"


class TrianglesTool(ToolScreen):
    tool_key = "triangles"
    tool_name = "Resolvedor de triángulos"
    description = "Resuelve cualquier triángulo a partir de tres lados, dos lados + ángulo incluido, o un lado + dos ángulos."

    def _build_form(self, form):
        self._add_option(
            "mode",
            "Modo",
            ["3 lados (SSS)", "2 lados + ángulo (SAS)", "1 lado + 2 ángulos (ASA)"],
            realtime=True,
            command=lambda v: self._rebuild_mode(),
        )
        self._rebuild_mode()

    def _rebuild_mode(self):
        for widget in self.form.winfo_children():
            widget.destroy()
        self.entry_vars = {}
        self._add_option(
            "mode",
            "Modo",
            ["3 lados (SSS)", "2 lados + ángulo (SAS)", "1 lado + 2 ángulos (ASA)"],
            realtime=True,
            command=lambda v: self._rebuild_mode(),
        )
        mode = self._get_option("mode")
        if mode.startswith("3 lados"):
            self._add_entry("a", "Lado a", "cm", realtime=True)
            self._add_entry("b", "Lado b", "cm", realtime=True)
            self._add_entry("c", "Lado c", "cm", realtime=True)
        elif mode.startswith("2 lados"):
            self._add_entry("a", "Lado a", "cm", realtime=True)
            self._add_entry("b", "Lado b", "cm", realtime=True)
            self._add_entry("angle_c", "Ángulo incluido C", "°", realtime=True)
        else:
            self._add_entry("c", "Lado c", "cm", realtime=True)
            self._add_entry("angle_a", "Ángulo A", "°", realtime=True)
            self._add_entry("angle_b", "Ángulo B", "°", realtime=True)
        self.refresh()

    def compute(self):
        mode = self._get_option("mode")
        if mode.startswith("3 lados"):
            a = self._get_float("a", "Lado a")
            b = self._get_float("b", "Lado b")
            c = self._get_float("c", "Lado c")
            sides = sorted([a, b, c])
            if sides[0] + sides[1] <= sides[2]:
                raise ValueError("Estas longitudes de lado no forman un triángulo válido.")
            angle_c = _deg(math.acos((a * a + b * b - c * c) / (2 * a * b)))
            angle_a = _deg(math.acos((b * b + c * c - a * a) / (2 * b * c)))
            angle_b = 180 - angle_a - angle_c
            area = 0.5 * a * b * math.sin(math.radians(angle_c))
            params = {"mode": mode, "a": a, "b": b, "c": c}
        elif mode.startswith("2 lados"):
            a = self._get_float("a", "Lado a")
            b = self._get_float("b", "Lado b")
            angle_c = self._get_float("angle_c", "Ángulo incluido C")
            if not (0 < angle_c < 180):
                raise ValueError("El ángulo incluido C debe estar entre 0 y 180 grados.")
            c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(angle_c)))
            angle_a = _deg(math.acos((b * b + c * c - a * a) / (2 * b * c)))
            angle_b = 180 - angle_a - angle_c
            area = 0.5 * a * b * math.sin(math.radians(angle_c))
            params = {"mode": mode, "a": a, "b": b, "angle_c": angle_c}
        else:
            c = self._get_float("c", "Lado c")
            angle_a = self._get_float("angle_a", "Ángulo A")
            angle_b = self._get_float("angle_b", "Ángulo B")
            if angle_a <= 0 or angle_b <= 0 or angle_a + angle_b >= 180:
                raise ValueError("Los dos ángulos deben ser positivos y sumar menos de 180 grados.")
            angle_c = 180 - angle_a - angle_b
            a = c * math.sin(math.radians(angle_a)) / math.sin(math.radians(angle_c))
            b = c * math.sin(math.radians(angle_b)) / math.sin(math.radians(angle_c))
            area = 0.5 * a * b * math.sin(math.radians(angle_c))
            params = {"mode": mode, "c": c, "angle_a": angle_a, "angle_b": angle_b}

        perimeter = a + b + c
        ttype = _triangle_type(a, b, c)
        results = [
            ("Lado a", a, "cm"),
            ("Lado b", b, "cm"),
            ("Lado c", c, "cm"),
            ("Ángulo A", angle_a, "°"),
            ("Ángulo B", angle_b, "°"),
            ("Ángulo C", angle_c, "°"),
            ("Área", area, "cm²"),
            ("Perímetro", perimeter, "cm"),
            ("Tipo", ttype, ""),
        ]
        return params, results
