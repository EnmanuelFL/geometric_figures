import math

from tools.base import ToolScreen


class SlopesTool(ToolScreen):
    tool_key = "slopes"
    tool_name = "Slope & Ramp Calculator"
    description = "Calculate slope percentage, angle and real length. Check accessibility (ramps ≤ 8%)."

    def _build_form(self, form):
        self._add_option("method", "Input mode", ["Rise + length", "Angle + length"], realtime=True)
        self._add_entry("rise", "Vertical rise", "m", realtime=True)
        self._add_entry("length", "Horizontal length", "m", realtime=True)
        self._add_entry("angle", "Angle", "°", realtime=True)

    def compute(self):
        method = self._get_option("method")
        length = self._get_float("length", "Horizontal length")
        if length <= 0:
            raise ValueError("Horizontal length must be greater than zero.")

        if method.startswith("Rise"):
            rise = self._get_float("rise", "Vertical rise")
            if rise < 0:
                raise ValueError("Vertical rise must be zero or greater.")
            percent = rise / length * 100
            angle = math.degrees(math.atan(rise / length))
            real_length = math.hypot(rise, length)
            params = {"method": method, "rise": rise, "length": length}
        else:
            angle = self._get_float("angle", "Angle")
            if angle < 0 or angle >= 90:
                raise ValueError("Angle must be between 0 and 90 degrees.")
            rise = length * math.tan(math.radians(angle))
            percent = rise / length * 100
            real_length = length / math.cos(math.radians(angle))
            params = {"method": method, "angle": angle, "length": length}

        accessible = "Accessible" if percent <= 8 else "Not accessible (limit 8%)"
        results = [
            ("Slope", percent, "%"),
            ("Angle", angle, "°"),
            ("Real length", real_length, "m"),
            ("Vertical rise", rise, "m"),
            ("Accessibility", accessible, ""),
        ]
        return params, results
