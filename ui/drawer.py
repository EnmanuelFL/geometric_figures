import math
import tkinter as tk

from figures import (
    Annulus,
    Circle,
    CircularSector,
    Cone,
    Cube,
    Cylinder,
    Ellipse,
    Parallelogram,
    Rectangle,
    RectangularPrism,
    RectangularPyramid,
    RegularPolygon,
    Rhombus,
    Sphere,
    Tetrahedron,
    Torus,
    Trapeze,
    Triangle,
)

from ui.theme import LIGHT

MARGIN = 24

_PALETTE = LIGHT


def _c(key):
    return _PALETTE[key]


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


def _accent():
    return _c("accent")


def _edge():
    return _c("canvas_edge")


def _fill():
    return _c("canvas_fill")


def _bg():
    return _c("canvas_bg")


def _draw_circle(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=_accent(), width=2, fill=_fill())
    c.create_line(cx, cy, cx + r, cy, fill=_edge(), dash=(4, 3))
    c.create_text((cx + cx + r) / 2, cy - 10, text=_lbl(values, "radio"), fill=_edge())


def _draw_rectangle(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    x0, y0 = cx - b / 2, cy - h / 2
    x1, y1 = cx + b / 2, cy + h / 2
    c.create_rectangle(x0, y0, x1, y1, outline=_accent(), width=2, fill=_fill())
    c.create_line(cx, y0, cx, y1, fill=_edge(), dash=(4, 3))
    c.create_text(cx, y1 + 12, text=_lbl(values, "base"), fill=_edge())
    c.create_text(x1 + 12, cy, text=_lbl(values, "height"), fill=_edge())


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
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_text(cx, cy + h / 2 + 12, text=_lbl(values, "base"), fill=_edge())
    c.create_text(cx, cy - h / 2 - 12, text=_lbl(values, "base_minior"), fill=_edge())
    c.create_text(cx + b_major / 2 + 14, cy, text=_lbl(values, "height"), fill=_edge())


def _draw_polygon(c, cx, cy, s, values):
    n = _num(values, "sides", 6)
    radius = (_val(values, "side") / (2 * math.sin(math.pi / n))) * s
    points = [
        (cx + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / n),
         cy + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / n))
        for i in range(n)
    ]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_text(cx, cy + radius + 16, text=f"n={n}, s={_lbl(values, 'side')}", fill=_edge())


def _draw_sector(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    angle = _val(values, "angle", 90)
    c.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=angle,
                 outline=_accent(), width=2, fill=_fill(), style="pieslice")
    c.create_line(cx, cy, cx + r * math.cos(math.radians(angle)),
                  cy - r * math.sin(math.radians(angle)), fill=_accent(), width=2)
    c.create_text(cx + r / 2, cy - r / 2 - 8, text=f"θ={_val(values, 'angle'):.0f}°", fill=_edge())
    c.create_text(cx + r * 0.7, cy + r * 0.55, text=_lbl(values, "radio"), fill=_edge())


def _draw_annulus(c, cx, cy, s, values):
    outer = _val(values, "radio") * s
    inner = _val(values, "radio_inner") * s
    c.create_oval(cx - outer, cy - outer, cx + outer, cy + outer,
                  outline=_accent(), width=2, fill=_fill())
    c.create_oval(cx - inner, cy - inner, cx + inner, cy + inner,
                  outline=_accent(), width=2, fill=_bg())
    c.create_text(cx + outer * 0.6, cy - outer * 0.6, text=_lbl(values, "radio"), fill=_edge())
    c.create_text(cx + inner * 0.45, cy - inner * 0.45, text=_lbl(values, "radio_inner"), fill=_edge())


def _draw_cube(c, cx, cy, s, values):
    a = _val(values, "sides") * s
    dx, dy = a * 0.55, a * 0.55
    front = [(cx - a / 2, cy - a / 2), (cx + a / 2, cy - a / 2),
             (cx + a / 2, cy + a / 2), (cx - a / 2, cy + a / 2)]
    back = [(x + dx, y - dy) for x, y in front]
    c.create_polygon(*_flat(back), outline=_accent(), width=2, fill=_fill())
    for f, b in zip(front, back):
        c.create_line(f[0], f[1], b[0], b[1], fill=_accent(), width=2)
    c.create_polygon(*_flat(front), outline=_accent(), width=2, fill=_bg())
    c.create_text(cx, cy + a / 2 + 16, text=f"s={_lbl(values, 'sides')}", fill=_edge())


def _draw_cylinder(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    h = _val(values, "height") * s
    ry = r * 0.3
    top_y = cy - h / 2
    bot_y = cy + h / 2
    c.create_rectangle(cx - r, top_y + ry, cx + r, bot_y, outline=_accent(), width=2, fill=_fill())
    c.create_arc(cx - r, bot_y - 2 * ry, cx + r, bot_y, start=0, extent=180,
                 outline=_accent(), width=2, fill=_fill(), style="chord")
    c.create_oval(cx - r, top_y, cx + r, top_y + 2 * ry, outline=_accent(), width=2, fill=_bg())
    c.create_line(cx, top_y + ry, cx, bot_y, fill=_edge(), dash=(4, 3))
    c.create_text(cx, bot_y + 16, text=f"r={_lbl(values, 'radio')}, h={_lbl(values, 'height')}", fill=_edge())


def _draw_sphere(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=_accent(), width=2, fill=_fill())
    c.create_oval(cx - r, cy - r * 0.55, cx + r, cy + r * 0.55, outline=_accent(), width=1)
    c.create_oval(cx - r * 0.55, cy - r, cx + r * 0.55, cy + r, outline=_accent(), width=1)
    c.create_text(cx, cy + r + 16, text=f"r={_lbl(values, 'radio')}", fill=_edge())


def _draw_rect_pyramid(c, cx, cy, s, values):
    length = _val(values, "base") * s
    width = _val(values, "width") * s * 0.6
    height = _val(values, "height") * s
    ox, oy = width * 0.5, width * 0.5
    apex = (cx, cy - height / 2)
    base = [(cx - length / 2, cy + height / 2), (cx + length / 2, cy + height / 2),
            (cx + length / 2 + ox, cy + height / 2 - oy), (cx - length / 2 + ox, cy + height / 2 - oy)]
    c.create_polygon(*_flat(base), outline=_accent(), width=2, fill=_bg())
    for p in base:
        c.create_line(apex[0], apex[1], p[0], p[1], fill=_accent(), width=2)
    c.create_polygon(cx - length / 2, cy + height / 2, cx + length / 2, cy + height / 2,
                     apex[0], apex[1], outline=_accent(), width=2, fill=_fill())
    c.create_text(cx, cy + height / 2 + 16,
                  text=f"l={_lbl(values, 'base')}, w={_lbl(values, 'width')}", fill=_edge())


def _draw_cone(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    h = _val(values, "height") * s
    ry = r * 0.3
    top = (cx, cy - h / 2)
    bot = cy + h / 2
    c.create_polygon(cx - r, bot, cx + r, bot, top[0], top[1], outline=_accent(), width=2, fill=_fill())
    c.create_arc(cx - r, bot - 2 * ry, cx + r, bot, start=0, extent=180,
                 outline=_accent(), width=2, fill=_bg(), style="chord")
    c.create_text(cx, bot + 16, text=f"r={_lbl(values, 'radio')}, h={_lbl(values, 'height')}", fill=_edge())


def _draw_rect_prism(c, cx, cy, s, values):
    length = _val(values, "length") * s
    width = _val(values, "width") * s * 0.6
    height = _val(values, "height") * s
    ox, oy = width * 0.5, width * 0.5
    front = [(cx - length / 2, cy - height / 2), (cx + length / 2, cy - height / 2),
             (cx + length / 2, cy + height / 2), (cx - length / 2, cy + height / 2)]
    back = [(x + ox, y - oy) for x, y in front]
    c.create_polygon(*_flat(back), outline=_accent(), width=2, fill=_fill())
    for f, b in zip(front, back):
        c.create_line(f[0], f[1], b[0], b[1], fill=_accent(), width=2)
    c.create_polygon(*_flat(front), outline=_accent(), width=2, fill=_bg())
    c.create_text(cx, cy + height / 2 + 16,
                  text=f"l={_lbl(values, 'length')}, w={_lbl(values, 'width')}", fill=_edge())


def _draw_triangle(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    points = [(cx - b / 2, cy + h / 2), (cx + b / 2, cy + h / 2), (cx, cy - h / 2)]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_line(cx, cy - h / 2, cx, cy + h / 2, fill=_edge(), dash=(4, 3))
    c.create_text(cx, cy + h / 2 + 12, text=f"b={_lbl(values, 'base')}", fill=_edge())
    c.create_text(cx + b / 2 + 12, cy, text=f"h={_lbl(values, 'height')}", fill=_edge())


def _draw_ellipse(c, cx, cy, s, values):
    a = _val(values, "semi_major") * s
    b = _val(values, "semi_minor") * s
    c.create_oval(cx - a, cy - b, cx + a, cy + b, outline=_accent(), width=2, fill=_fill())
    c.create_line(cx - a, cy, cx + a, cy, fill=_edge(), dash=(4, 3))
    c.create_line(cx, cy - b, cx, cy + b, fill=_edge(), dash=(4, 3))
    c.create_text(cx + a / 2, cy - 10, text=_lbl(values, "semi_major"), fill=_edge())
    c.create_text(cx + 10, cy - b / 2, text=_lbl(values, "semi_minor"), fill=_edge())


def _draw_rhombus(c, cx, cy, s, values):
    d1 = _val(values, "diag_major") * s
    d2 = _val(values, "diag_minor") * s
    points = [(cx, cy - d2 / 2), (cx + d1 / 2, cy), (cx, cy + d2 / 2), (cx - d1 / 2, cy)]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_line(cx - d1 / 2, cy, cx + d1 / 2, cy, fill=_edge(), dash=(4, 3))
    c.create_text(cx, cy + d2 / 2 + 14, text=f"D={_lbl(values, 'diag_major')}", fill=_edge())
    c.create_text(cx + d1 / 2 + 10, cy, text=f"d={_lbl(values, 'diag_minor')}", fill=_edge())


def _draw_parallelogram(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    angle = math.radians(_val(values, "angle", 60))
    off = h * math.cos(angle) / math.sin(angle)
    points = [(cx - b / 2 - off, cy - h / 2), (cx + b / 2 - off, cy - h / 2),
              (cx + b / 2, cy + h / 2), (cx - b / 2, cy + h / 2)]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_line(cx - b / 2 - off, cy + h / 2, cx - b / 2 - off, cy - h / 2, fill=_edge(), dash=(4, 3))
    c.create_text(cx, cy + h / 2 + 14,
                  text=f"b={_lbl(values, 'base')}, θ={_val(values, 'angle'):.0f}°", fill=_edge())
    c.create_text(cx - b / 2 - off - 12, cy, text=f"h={_lbl(values, 'height')}", fill=_edge())


def _draw_torus(c, cx, cy, s, values):
    outer = _val(values, "major_radius") * s
    inner = _val(values, "minor_radius") * s
    c.create_oval(cx - (outer + inner), cy - (outer + inner), cx + (outer + inner), cy + (outer + inner),
                  outline=_accent(), width=2, fill=_fill())
    c.create_oval(cx - (outer - inner), cy - (outer - inner), cx + (outer - inner), cy + (outer - inner),
                  outline=_accent(), width=2, fill=_bg())
    c.create_text(cx, cy + (outer + inner) + 16,
                  text=f"R={_lbl(values, 'major_radius')}, r={_lbl(values, 'minor_radius')}", fill=_edge())


def _draw_tetrahedron(c, cx, cy, s, values):
    a = _val(values, "side") * s
    h = a * math.sqrt(3) / 2
    base = [(cx - a / 2, cy + h / 2), (cx + a / 2, cy + h / 2), (cx, cy - h / 2)]
    apex = (cx, cy - h / 2 - a * 0.55)
    for p in base:
        c.create_line(apex[0], apex[1], p[0], p[1], fill=_accent(), width=2)
    c.create_polygon(*_flat(base), outline=_accent(), width=2, fill=_fill())
    c.create_text(cx, cy + h / 2 + 16, text=f"a={_lbl(values, 'side')}", fill=_edge())


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
    Triangle: _draw_triangle,
    Ellipse: _draw_ellipse,
    Rhombus: _draw_rhombus,
    Parallelogram: _draw_parallelogram,
    Torus: _draw_torus,
    Tetrahedron: _draw_tetrahedron,
}

_SIZES = {
    Circle: lambda v: (2, 2),
    Rectangle: lambda v: (_val(v, "base"), _val(v, "height")),
    Trapeze: lambda v: (_val(v, "base"), _val(v, "height")),
    RegularPolygon: lambda v: (2, 2),
    CircularSector: lambda v: (2, 2),
    Annulus: lambda v: (2, 2),
    Cube: lambda v: (1.55, 1.55),
    Cylinder: lambda v: (2, 1.4),
    Sphere: lambda v: (2, 2),
    RectangularPyramid: lambda v: (1.3, 1.4),
    Cone: lambda v: (2, 1.4),
    RectangularPrism: lambda v: (1.3, 1.4),
    Triangle: lambda v: (_val(v, "base"), _val(v, "height")),
    Ellipse: lambda v: (2 * _val(v, "semi_major"), 2 * _val(v, "semi_minor")),
    Rhombus: lambda v: (_val(v, "diag_major"), _val(v, "diag_minor")),
    Parallelogram: lambda v: (_val(v, "base") + abs(_val(v, "height")), _val(v, "height")),
    Torus: lambda v: (2, 2),
    Tetrahedron: lambda v: (_val(v, "side"), _val(v, "side") * 1.4),
}


def draw(canvas, figure, values, palette=None):
    global _PALETTE
    _PALETTE = palette or LIGHT
    draw_func = _DRAWERS.get(type(figure))
    if draw_func is None:
        return
    canvas.delete("all")
    cw = max(canvas.winfo_width(), 320)
    ch = max(canvas.winfo_height(), 220)
    nw, nh = _SIZES.get(type(figure), lambda v: (1, 1))(values)
    scale = min((cw - 2 * MARGIN) / nw, (ch - 2 * MARGIN) / nh, 60)
    draw_func(canvas, cw / 2, ch / 2, max(scale, 1.0), values)
