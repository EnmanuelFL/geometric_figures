import math

from tools.base import ToolScreen


def _deg(rad):
    return math.degrees(rad)


def _triangle_type(a, b, c):
    sides = sorted([a, b, c])
    if sides[0] + sides[1] <= sides[2]:
        return "Invalid"
    if math.isclose(a, b, rel_tol=1e-9) and math.isclose(b, c, rel_tol=1e-9):
        return "Equilateral"
    if math.isclose(a, b, rel_tol=1e-9) or math.isclose(b, c, rel_tol=1e-9) or math.isclose(a, c, rel_tol=1e-9):
        return "Isosceles"
    return "Scalene"


class TrianglesTool(ToolScreen):
    tool_key = "triangles"
    tool_name = "Triangle Solver"
    description = "Solve any triangle from three sides, two sides + included angle, or one side + two angles."

    def _build_form(self, form):
        self._add_option(
            "mode",
            "Mode",
            ["3 sides (SSS)", "2 sides + angle (SAS)", "1 side + 2 angles (ASA)"],
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
            "Mode",
            ["3 sides (SSS)", "2 sides + angle (SAS)", "1 side + 2 angles (ASA)"],
            realtime=True,
            command=lambda v: self._rebuild_mode(),
        )
        mode = self._get_option("mode")
        if mode.startswith("3 sides"):
            self._add_entry("a", "Side a", "cm", realtime=True)
            self._add_entry("b", "Side b", "cm", realtime=True)
            self._add_entry("c", "Side c", "cm", realtime=True)
        elif mode.startswith("2 sides"):
            self._add_entry("a", "Side a", "cm", realtime=True)
            self._add_entry("b", "Side b", "cm", realtime=True)
            self._add_entry("angle_c", "Included angle C", "deg", realtime=True)
        else:
            self._add_entry("c", "Side c", "cm", realtime=True)
            self._add_entry("angle_a", "Angle A", "deg", realtime=True)
            self._add_entry("angle_b", "Angle B", "deg", realtime=True)
        self.refresh()

    def compute(self):
        mode = self._get_option("mode")
        if mode.startswith("3 sides"):
            a = self._get_float("a", "Side a")
            b = self._get_float("b", "Side b")
            c = self._get_float("c", "Side c")
            sides = sorted([a, b, c])
            if sides[0] + sides[1] <= sides[2]:
                raise ValueError("These side lengths do not form a valid triangle.")
            angle_c = _deg(math.acos((a * a + b * b - c * c) / (2 * a * b)))
            angle_a = _deg(math.acos((b * b + c * c - a * a) / (2 * b * c)))
            angle_b = 180 - angle_a - angle_c
            area = 0.5 * a * b * math.sin(math.radians(angle_c))
            params = {"mode": mode, "a": a, "b": b, "c": c}
        elif mode.startswith("2 sides"):
            a = self._get_float("a", "Side a")
            b = self._get_float("b", "Side b")
            angle_c = self._get_float("angle_c", "Included angle C")
            if not (0 < angle_c < 180):
                raise ValueError("Included angle C must be between 0 and 180 degrees.")
            c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(angle_c)))
            angle_a = _deg(math.acos((b * b + c * c - a * a) / (2 * b * c)))
            angle_b = 180 - angle_a - angle_c
            area = 0.5 * a * b * math.sin(math.radians(angle_c))
            params = {"mode": mode, "a": a, "b": b, "angle_c": angle_c}
        else:
            c = self._get_float("c", "Side c")
            angle_a = self._get_float("angle_a", "Angle A")
            angle_b = self._get_float("angle_b", "Angle B")
            if angle_a <= 0 or angle_b <= 0 or angle_a + angle_b >= 180:
                raise ValueError("The two angles must be positive and sum to less than 180 degrees.")
            angle_c = 180 - angle_a - angle_b
            a = c * math.sin(math.radians(angle_a)) / math.sin(math.radians(angle_c))
            b = c * math.sin(math.radians(angle_b)) / math.sin(math.radians(angle_c))
            area = 0.5 * a * b * math.sin(math.radians(angle_c))
            params = {"mode": mode, "c": c, "angle_a": angle_a, "angle_b": angle_b}

        perimeter = a + b + c
        ttype = _triangle_type(a, b, c)
        results = [
            ("Side a", a, "cm"),
            ("Side b", b, "cm"),
            ("Side c", c, "cm"),
            ("Angle A", angle_a, "deg"),
            ("Angle B", angle_b, "deg"),
            ("Angle C", angle_c, "deg"),
            ("Area", area, "cm²"),
            ("Perimeter", perimeter, "cm"),
            ("Type", ttype, ""),
        ]
        return params, results
