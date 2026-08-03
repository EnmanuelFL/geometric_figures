import math
import tkinter as tk

from figures import (
    Circle,
    Rectangle,
    Trapeze,
    RegularPolygon,
    CircularSector,
    Annulus,
    Cube,
    Cylinder,
    Sphere,
    RectangularPyramid,
    Cone,
    RectangularPrism,
)

ACCENT = "#534AB7"
EDGE = "#3A3F55"
INTERIOR = "#E3E7F6"
CANVAS_BG = "#FFFFFF"
MARGIN = 24


def _val(values, key, default=1.0):
    try:
        v = float(values.get(key, default))
    except (TypeError, ValueError):
        v = default
    return v if v and v > 0 else default


def _num(values, key, default=1.0):
    return int(round(_val(values, key, default)))


def _lbl(values, key, suffix="cm"):
    return f"{_val(values, key):.1f} {suffix}".strip()


def _flat(points):
    return [coord for point in points for coord in point]


def _draw_circle(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=ACCENT, width=2, fill=INTERIOR)
    c.create_line(cx, cy, cx + r, cy, fill=EDGE, dash=(4, 3))
    c.create_text((cx + cx + r) / 2, cy - 10, text=_lbl(values, "radio"), fill=EDGE)


def _draw_rectangle(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    x0, y0 = cx - b / 2, cy - h / 2
    x1, y1 = cx + b / 2, cy + h / 2
    c.create_rectangle(x0, y0, x1, y1, outline=ACCENT, width=2, fill=INTERIOR)
    c.create_line(cx, y0, cx, y1, fill=EDGE, dash=(4, 3))
    c.create_text(cx, y1 + 12, text=_lbl(values, "base"), fill=EDGE)
    c.create_text(x1 + 12, cy, text=_lbl(values, "height"), fill=EDGE)


def _draw_trapeze(c, cx, cy, s, values):
    b_major = _val(values, "base") * s
    b_minor = _val(values, "base_minior") * s
    h = _val(values, "height") * s
    offset = (b_major - b_minor) / 2
    points = [
        (cx - b_major / 2, cy + h / 2),
        (cx + b_major / 2, cy + h / 2),
        (cx + offset, cy - h / 2),
        (cx - offset, cy - h / 2),
    ]
    c.create_polygon(*_flat(points), outline=ACCENT, width=2, fill=INTERIOR)
    c.create_text(cx, cy + h / 2 + 12, text=_lbl(values, "base"), fill=EDGE)
    c.create_text(cx, cy - h / 2 - 12, text=_lbl(values, "base_minior"), fill=EDGE)
    c.create_text(cx + b_major / 2 + 14, cy, text=_lbl(values, "height"), fill=EDGE)


def _draw_polygon(c, cx, cy, s, values):
    n = _num(values, "sides", 6)
    radius = (_val(values, "side") / (2 * math.sin(math.pi / n))) * s
    points = [
        (cx + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / n),
         cy + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / n))
        for i in range(n)
    ]
    c.create_polygon(*_flat(points), outline=ACCENT, width=2, fill=INTERIOR)
    c.create_text(cx, cy + radius + 16, text=f"n={n}, s={_lbl(values, 'side')}", fill=EDGE)


def _draw_sector(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    angle = _val(values, "angle", 90)
    c.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=angle,
                 outline=ACCENT, width=2, fill=INTERIOR, style="pieslice")
    c.create_line(cx, cy, cx + r * math.cos(math.radians(angle)),
                  cy - r * math.sin(math.radians(angle)), fill=ACCENT, width=2)
    c.create_text(cx + r / 2, cy - r / 2 - 8, text=f"θ={_val(values, 'angle'):.0f}°", fill=EDGE)
    c.create_text(cx + r * 0.7, cy + r * 0.55, text=_lbl(values, "radio"), fill=EDGE)


def _draw_annulus(c, cx, cy, s, values):
    outer = _val(values, "radio") * s
    inner = _val(values, "radio_inner") * s
    c.create_oval(cx - outer, cy - outer, cx + outer, cy + outer,
                  outline=ACCENT, width=2, fill=INTERIOR)
    c.create_oval(cx - inner, cy - inner, cx + inner, cy + inner,
                  outline=ACCENT, width=2, fill=CANVAS_BG)
    c.create_text(cx + outer * 0.6, cy - outer * 0.6, text=_lbl(values, "radio"), fill=EDGE)
    c.create_text(cx + inner * 0.45, cy - inner * 0.45, text=_lbl(values, "radio_inner"), fill=EDGE)


def _draw_cube(c, cx, cy, s, values):
    a = _val(values, "sides") * s
    dx, dy = a * 0.55, a * 0.55
    front = [(cx - a / 2, cy - a / 2), (cx + a / 2, cy - a / 2),
             (cx + a / 2, cy + a / 2), (cx - a / 2, cy + a / 2)]
    back = [(x + dx, y - dy) for x, y in front]
    c.create_polygon(*_flat(back), outline=ACCENT, width=2, fill=INTERIOR)
    for f, b in zip(front, back):
        c.create_line(f[0], f[1], b[0], b[1], fill=ACCENT, width=2)
    c.create_polygon(*_flat(front), outline=ACCENT, width=2, fill=CANVAS_BG)
    c.create_text(cx, cy + a / 2 + 16, text=f"s={_lbl(values, 'sides')}", fill=EDGE)


def _draw_cylinder(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    h = _val(values, "height") * s
    ry = r * 0.3
    top_y = cy - h / 2
    bot_y = cy + h / 2
    c.create_rectangle(cx - r, top_y + ry, cx + r, bot_y, outline=ACCENT, width=2, fill=INTERIOR)
    c.create_arc(cx - r, bot_y - 2 * ry, cx + r, bot_y, start=0, extent=180,
                 outline=ACCENT, width=2, fill=INTERIOR, style="chord")
    c.create_oval(cx - r, top_y, cx + r, top_y + 2 * ry, outline=ACCENT, width=2, fill=CANVAS_BG)
    c.create_line(cx, top_y + ry, cx, bot_y, fill=EDGE, dash=(4, 3))
    c.create_text(cx, bot_y + 16, text=f"r={_lbl(values, 'radio')}, h={_lbl(values, 'height')}", fill=EDGE)


def _draw_sphere(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=ACCENT, width=2, fill=INTERIOR)
    c.create_oval(cx - r, cy - r * 0.55, cx + r, cy + r * 0.55, outline=ACCENT, width=1)
    c.create_oval(cx - r * 0.55, cy - r, cx + r * 0.55, cy + r, outline=ACCENT, width=1)
    c.create_text(cx, cy + r + 16, text=f"r={_lbl(values, 'radio')}", fill=EDGE)


def _draw_rect_pyramid(c, cx, cy, s, values):
    length = _val(values, "base") * s
    width = _val(values, "width") * s * 0.6
    height = _val(values, "height") * s
    ox, oy = width * 0.5, width * 0.5
    apex = (cx, cy - height / 2)
    base = [(cx - length / 2, cy + height / 2), (cx + length / 2, cy + height / 2),
            (cx + length / 2 + ox, cy + height / 2 - oy), (cx - length / 2 + ox, cy + height / 2 - oy)]
    c.create_polygon(*_flat(base), outline=ACCENT, width=2, fill=CANVAS_BG)
    for p in base:
        c.create_line(apex[0], apex[1], p[0], p[1], fill=ACCENT, width=2)
    c.create_polygon(cx - length / 2, cy + height / 2, cx + length / 2, cy + height / 2,
                     apex[0], apex[1], outline=ACCENT, width=2, fill=INTERIOR)
    c.create_text(cx, cy + height / 2 + 16,
                  text=f"l={_lbl(values, 'base')}, w={_lbl(values, 'width')}", fill=EDGE)


def _draw_cone(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    h = _val(values, "height") * s
    ry = r * 0.3
    top = (cx, cy - h / 2)
    bot = cy + h / 2
    c.create_polygon(cx - r, bot, cx + r, bot, top[0], top[1], outline=ACCENT, width=2, fill=INTERIOR)
    c.create_arc(cx - r, bot - 2 * ry, cx + r, bot, start=0, extent=180,
                 outline=ACCENT, width=2, fill=CANVAS_BG, style="chord")
    c.create_text(cx, bot + 16, text=f"r={_lbl(values, 'radio')}, h={_lbl(values, 'height')}", fill=EDGE)


def _draw_rect_prism(c, cx, cy, s, values):
    length = _val(values, "length") * s
    width = _val(values, "width") * s * 0.6
    height = _val(values, "height") * s
    ox, oy = width * 0.5, width * 0.5
    front = [(cx - length / 2, cy - height / 2), (cx + length / 2, cy - height / 2),
             (cx + length / 2, cy + height / 2), (cx - length / 2, cy + height / 2)]
    back = [(x + ox, y - oy) for x, y in front]
    c.create_polygon(*_flat(back), outline=ACCENT, width=2, fill=INTERIOR)
    for f, b in zip(front, back):
        c.create_line(f[0], f[1], b[0], b[1], fill=ACCENT, width=2)
    c.create_polygon(*_flat(front), outline=ACCENT, width=2, fill=CANVAS_BG)
    c.create_text(cx, cy + height / 2 + 16,
                  text=f"l={_lbl(values, 'length')}, w={_lbl(values, 'width')}", fill=EDGE)


_DRAWERS = {
    Circle: _draw_circle,
    Rectangle: _draw_rectangle,
    Trapeze: _draw_trapeze,
    RegularPolygon: _draw_polygon,
    CircularSector: _draw_sector,
    Annulus: _draw_annulus,
    Cube: _draw_cube,
    Cylinder: _draw_cylinder,
    Sphere: _draw_sphere,
    RectangularPyramid: _draw_rect_pyramid,
    Cone: _draw_cone,
    RectangularPrism: _draw_rect_prism,
}

_SIZES = {
    Circle: lambda v: (2, 2),
    Rectangle: lambda v: (1, 1),
    Trapeze: lambda v: (1, 1),
    RegularPolygon: lambda v: (2, 2),
    CircularSector: lambda v: (2, 2),
    Annulus: lambda v: (2, 2),
    Cube: lambda v: (1.55, 1.55),
    Cylinder: lambda v: (2, 1.4),
    Sphere: lambda v: (2, 2),
    RectangularPyramid: lambda v: (1.3, 1.4),
    Cone: lambda v: (2, 1.4),
    RectangularPrism: lambda v: (1.3, 1.4),
}


def draw(canvas, figure, values):
    draw_func = _DRAWERS.get(type(figure))
    if draw_func is None:
        return
    canvas.delete("all")
    cw = max(canvas.winfo_width(), 320)
    ch = max(canvas.winfo_height(), 220)
    nw, nh = _SIZES.get(type(figure), lambda v: (1, 1))(values)
    scale = min((cw - 2 * MARGIN) / nw, (ch - 2 * MARGIN) / nh, 60)
    draw_func(canvas, cw / 2, ch / 2, max(scale, 1.0), values)
