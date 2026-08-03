import json
import math
import os
import tkinter as tk

import customtkinter as ctk

from ui import theme, t

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "core",
    "reference_data.json",
)

PHI = (1 + 5 ** 0.5) / 2


def _load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


class ReferenceScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=t("panel"), corner_radius=12)
        self.all_labels = []
        self.all_entries = []

        self.title_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t("text"),
            anchor="w",
        )
        self.title_label.pack(fill="x", padx=20, pady=(18, 2))

        self.desc_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=t("muted"),
            justify="left",
            anchor="w",
            wraplength=560,
        )
        self.desc_label.pack(fill="x", padx=20, pady=(0, 10))

        self.body = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.body.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        theme.register(self.apply_theme)

    def set_header(self, title, desc):
        self.title_label.configure(text=title)
        self.desc_label.configure(text=desc)

    def _label(self, parent, text, key, size=13, bold=False, anchor="w", wraplength=0):
        colors = {"accent": t("accent"), "muted": t("muted"), "value": t("text")}
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=size, weight="bold" if bold else "normal"),
            text_color=colors[key],
            anchor=anchor,
            justify="left",
        )
        if wraplength:
            label.configure(wraplength=wraplength)
        self.all_labels.append((label, key))
        return label

    def _entry(self, parent, height=32):
        entry = ctk.CTkEntry(
            parent,
            height=height,
            corner_radius=8,
            fg_color=t("entry_bg"),
            border_color=t("border"),
            text_color=t("text"),
        )
        self.all_entries.append(entry)
        return entry

    def add_table(self, title, headers, rows):
        self._label(self.body, title, "accent", size=15, bold=True).pack(anchor="w", pady=(12, 6))
        header_row = ctk.CTkFrame(self.body, fg_color=t("section_bg"), corner_radius=8)
        header_row.pack(fill="x", pady=(0, 2))
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_row,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=t("accent"),
            ).grid(row=0, column=i, sticky="w", padx=12, pady=6)
        for row in rows:
            row_frame = ctk.CTkFrame(self.body, fg_color="transparent")
            row_frame.pack(fill="x")
            for i, cell in enumerate(row):
                self._label(row_frame, str(cell), "value", size=13).grid(
                    row=0, column=i, sticky="w", padx=12, pady=2
                )

    def add_paragraph(self, text):
        self._label(self.body, text, "value", size=13, wraplength=560).pack(anchor="w", pady=4)

    def apply_theme(self):
        self.configure(fg_color=t("panel"))
        self.title_label.configure(text_color=t("text"))
        self.desc_label.configure(text_color=t("muted"))
        colors = {"accent": t("accent"), "muted": t("muted"), "value": t("text")}
        for label, key in list(self.all_labels):
            if not label.winfo_exists():
                self.all_labels.remove((label, key))
                continue
            label.configure(text_color=colors[key])
        for entry in self.all_entries:
            entry.configure(fg_color=t("entry_bg"), border_color=t("border"), text_color=t("text"))
        self._refresh_theme_extra()

    def _refresh_theme_extra(self):
        pass


class MaterialsScreen(ReferenceScreen):
    def __init__(self, master):
        super().__init__(master)
        data = _load_data()
        self.set_header(
            "Material Strength",
            "Reference compressive and tensile strength, and specific weight of common building materials.",
        )
        rows = [
            (m["material"], m["compression"], m["tension"], m["density"])
            for m in data["materials"]
        ]
        self.add_table(
            "Materials",
            ["Material", "Compression (MPa)", "Tension (MPa)", "Weight (kg/m³)"],
            rows,
        )


class NormativeScreen(ReferenceScreen):
    def __init__(self, master):
        super().__init__(master)
        data = _load_data()
        self.set_header(
            "Basic Normative Dimensions",
            "Reference minimum dimensions commonly used in residential and commercial design.",
        )
        self.add_table(
            "Minimum heights by use",
            ["Use", "Min. height"],
            [(h["use"], h["min"]) for h in data["heights"]],
        )
        self.add_table(
            "Minimum widths",
            ["Element", "Min. width"],
            [(w["item"], w["min"]) for w in data["widths"]],
        )
        self.add_table(
            "Parking dimensions",
            ["Type", "Dimensions"],
            [(p["type"], p["dimensions"]) for p in data["parking"]],
        )


class WeightsScreen(ReferenceScreen):
    def __init__(self, master):
        super().__init__(master)
        data = _load_data()
        self.set_header(
            "Weights per m²",
            "Typical surface weights of common building elements for structural estimation.",
        )
        self.add_table(
            "Elements",
            ["Element", "Weight"],
            [(w["element"], w["weight"]) for w in data["weights"]],
        )


class GoldenRatioScreen(ReferenceScreen):
    def __init__(self, master):
        super().__init__(master)
        self.set_header(
            "Golden Ratio",
            "Derive golden proportions from a base measure and visualize the golden rectangle with its spiral.",
        )
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", pady=(4, 8))
        self._label(row, "Base measure", "value", size=13).pack(side="left")
        self.base_entry = self._entry(row)
        self.base_entry.pack(side="left", fill="x", expand=True, padx=12)
        self.base_entry.insert(0, "10")
        self.base_entry.bind("<KeyRelease>", lambda e: self._update())

        self.canvas = tk.Canvas(
            self.body,
            width=540,
            height=260,
            bg=t("canvas_bg"),
            highlightthickness=1,
            highlightbackground=t("border"),
        )
        self.canvas.pack(pady=8)

        self.series_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.series_frame.pack(fill="x", pady=(4, 0))

        self._update()

    def _update(self):
        raw = self.base_entry.get().strip()
        try:
            base = float(raw) if raw else 10.0
        except ValueError:
            base = 10.0
        if base <= 0:
            base = 10.0
        for widget in self.series_frame.winfo_children():
            widget.destroy()
        self._draw_series(base)
        self._draw_spiral(base)

    def _draw_series(self, base):
        entries = [
            ("Base × φ", base * PHI),
            ("Base ÷ φ", base / PHI),
            ("Base × φ²", base * PHI ** 2),
            ("Base ÷ φ²", base / PHI ** 2),
            ("Base + Base·φ", base + base * PHI),
        ]
        for label_text, value in entries:
            self._label(self.series_frame, label_text, "muted", size=13).pack(anchor="w")
            self._label(self.series_frame, f"{value:.2f} cm", "value", size=14, bold=True).pack(anchor="e")

    def _draw_spiral(self, base):
        self.canvas.delete("all")
        cw = max(self.canvas.winfo_width(), 340)
        ch = max(self.canvas.winfo_height(), 220)
        turns = 1.75
        max_theta = turns * 2 * math.pi
        max_r = base * PHI ** (2 * max_theta / math.pi)
        scale = min((cw - 60) / (2 * max_r), (ch - 60) / (2 * max_r))
        cx, cy = cw / 2, ch / 2
        points = []
        steps = 400
        for i in range(steps + 1):
            theta = i / steps * max_theta
            r = base * PHI ** (2 * theta / math.pi) * scale
            points.append(cx + r * math.cos(theta))
            points.append(cy - r * math.sin(theta))
        self.canvas.create_line(*points, smooth=True, width=2, fill=t("accent"))
        w = base * PHI * scale
        h = base * scale
        x0, y0 = cx - w / 2, cy - h / 2
        self.canvas.create_rectangle(x0, y0, x0 + w, y0 + h, outline=t("canvas_edge"), width=1)
        x, y, wc, hc = x0, y0, w, h
        for _ in range(8):
            side = min(wc, hc)
            self.canvas.create_rectangle(x, y, x + side, y + side, outline=t("canvas_edge"), width=1)
            if wc > hc:
                x += side
                wc -= side
            else:
                y += side
                hc -= side

    def _refresh_theme_extra(self):
        self.canvas.configure(bg=t("canvas_bg"), highlightbackground=t("border"))
        self._update()
