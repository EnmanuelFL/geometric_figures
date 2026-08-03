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
LABEL_SPACE = 40

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


def _label_offset(dim):
    return max(14, dim * 0.06)


def _flat(points):
    return [coord for point in points for coord in point]


def _polygon_extent(v):
    n = _num(v, "sides", 6)
    radius = _val(v, "side") / (2 * math.sin(math.pi / n))
    return (2 * radius, 2 * radius)


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
    c.create_text(cx + r + _label_offset(r), cy, text=_lbl(values, "radio"), fill=_edge(), anchor="w")


def _draw_rectangle(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    x0, y0 = cx - b / 2, cy - h / 2
    x1, y1 = cx + b / 2, cy + h / 2
    c.create_rectangle(x0, y0, x1, y1, outline=_accent(), width=2, fill=_fill())
    c.create_line(cx, y0, cx, y1, fill=_edge(), dash=(4, 3))
    c.create_text(cx, y1 + _label_offset(h), text=_lbl(values, "base"), fill=_edge())
    c.create_text(x1 + _label_offset(b), cy, text=_lbl(values, "height"), fill=_edge(), anchor="w")


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
    c.create_text(cx, cy + h / 2 + _label_offset(h), text=_lbl(values, "base"), fill=_edge())
    c.create_text(cx, cy - h / 2 - _label_offset(h), text=_lbl(values, "base_minior"), fill=_edge())
    c.create_text(cx + b_major / 2 + _label_offset(b_major), cy, text=_lbl(values, "height"), fill=_edge(), anchor="w")


def _draw_polygon(c, cx, cy, s, values):
    n = _num(values, "sides", 6)
    radius = (_val(values, "side") / (2 * math.sin(math.pi / n))) * s
    points = [
        (cx + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / n),
         cy + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / n))
        for i in range(n)
    ]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_text(cx, cy + radius + _label_offset(radius), text=f"n={n}, s={_lbl(values, 'side')}", fill=_edge())


def _draw_sector(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    angle = _val(values, "angle", 90)
    c.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=angle,
                 outline=_accent(), width=2, fill=_fill(), style="pieslice")
    c.create_line(cx, cy, cx + r * math.cos(math.radians(angle)),
                  cy - r * math.sin(math.radians(angle)), fill=_accent(), width=2)
    c.create_text(cx + r * math.cos(math.radians(angle / 2)) * 0.7,
                  cy - r * math.sin(math.radians(angle / 2)) * 0.7,
                  text=f"θ={_val(values, 'angle'):.0f}°", fill=_edge())
    c.create_text(cx + r + _label_offset(r), cy, text=_lbl(values, "radio"), fill=_edge(), anchor="w")


def _draw_annulus(c, cx, cy, s, values):
    outer = _val(values, "radio") * s
    inner = _val(values, "radio_inner") * s
    c.create_oval(cx - outer, cy - outer, cx + outer, cy + outer,
                  outline=_accent(), width=2, fill=_fill())
    c.create_oval(cx - inner, cy - inner, cx + inner, cy + inner,
                  outline=_accent(), width=2, fill=_bg())
    c.create_text(cx + outer + _label_offset(outer), cy, text=_lbl(values, "radio"), fill=_edge(), anchor="w")
    c.create_text(cx, cy + outer + _label_offset(outer), text=_lbl(values, "radio_inner"), fill=_edge())


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
    c.create_text(cx, cy + a / 2 + _label_offset(a), text=f"s={_lbl(values, 'sides')}", fill=_edge())


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
    c.create_text(cx, bot_y + _label_offset(h), text=f"r={_lbl(values, 'radio')}, h={_lbl(values, 'height')}", fill=_edge())


def _draw_sphere(c, cx, cy, s, values):
    r = _val(values, "radio") * s
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=_accent(), width=2, fill=_fill())
    c.create_oval(cx - r, cy - r * 0.55, cx + r, cy + r * 0.55, outline=_accent(), width=1)
    c.create_oval(cx - r * 0.55, cy - r, cx + r * 0.55, cy + r, outline=_accent(), width=1)
    c.create_text(cx + r + _label_offset(r), cy, text=f"r={_lbl(values, 'radio')}", fill=_edge(), anchor="w")


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
    c.create_text(cx, cy + height / 2 + _label_offset(height),
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
    c.create_text(cx, bot + _label_offset(h), text=f"r={_lbl(values, 'radio')}, h={_lbl(values, 'height')}", fill=_edge())


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
    c.create_text(cx, cy + height / 2 + _label_offset(height),
                  text=f"l={_lbl(values, 'length')}, w={_lbl(values, 'width')}", fill=_edge())


def _draw_triangle(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    points = [(cx - b / 2, cy + h / 2), (cx + b / 2, cy + h / 2), (cx, cy - h / 2)]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_line(cx, cy - h / 2, cx, cy + h / 2, fill=_edge(), dash=(4, 3))
    c.create_text(cx, cy + h / 2 + _label_offset(h), text=f"b={_lbl(values, 'base')}", fill=_edge())
    c.create_text(cx + b / 2 + _label_offset(b), cy, text=f"h={_lbl(values, 'height')}", fill=_edge(), anchor="w")


def _draw_ellipse(c, cx, cy, s, values):
    a = _val(values, "semi_major") * s
    b = _val(values, "semi_minor") * s
    c.create_oval(cx - a, cy - b, cx + a, cy + b, outline=_accent(), width=2, fill=_fill())
    c.create_line(cx - a, cy, cx + a, cy, fill=_edge(), dash=(4, 3))
    c.create_line(cx, cy - b, cx, cy + b, fill=_edge(), dash=(4, 3))
    c.create_text(cx + a + _label_offset(a), cy, text=_lbl(values, "semi_major"), fill=_edge(), anchor="w")
    c.create_text(cx, cy - b - _label_offset(b), text=_lbl(values, "semi_minor"), fill=_edge())


def _draw_rhombus(c, cx, cy, s, values):
    d1 = _val(values, "diag_major") * s
    d2 = _val(values, "diag_minor") * s
    points = [(cx, cy - d2 / 2), (cx + d1 / 2, cy), (cx, cy + d2 / 2), (cx - d1 / 2, cy)]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_line(cx - d1 / 2, cy, cx + d1 / 2, cy, fill=_edge(), dash=(4, 3))
    c.create_text(cx, cy + d2 / 2 + _label_offset(d2), text=f"D={_lbl(values, 'diag_major')}", fill=_edge())
    c.create_text(cx + d1 / 2 + _label_offset(d1), cy, text=f"d={_lbl(values, 'diag_minor')}", fill=_edge(), anchor="w")


def _draw_parallelogram(c, cx, cy, s, values):
    b = _val(values, "base") * s
    h = _val(values, "height") * s
    angle = math.radians(_val(values, "angle", 60))
    off = h * math.cos(angle) / math.sin(angle)
    points = [(cx - b / 2 - off, cy - h / 2), (cx + b / 2 - off, cy - h / 2),
              (cx + b / 2, cy + h / 2), (cx - b / 2, cy + h / 2)]
    c.create_polygon(*_flat(points), outline=_accent(), width=2, fill=_fill())
    c.create_line(cx - b / 2 - off, cy + h / 2, cx - b / 2 - off, cy - h / 2, fill=_edge(), dash=(4, 3))
    c.create_text(cx, cy + h / 2 + _label_offset(h),
                  text=f"b={_lbl(values, 'base')}, θ={_val(values, 'angle'):.0f}°", fill=_edge())
    c.create_text(cx - b / 2 - off - _label_offset(b), cy, text=f"h={_lbl(values, 'height')}", fill=_edge(), anchor="e")


def _draw_torus(c, cx, cy, s, values):
    outer = _val(values, "major_radius") * s
    inner = _val(values, "minor_radius") * s
    c.create_oval(cx - (outer + inner), cy - (outer + inner), cx + (outer + inner), cy + (outer + inner),
                  outline=_accent(), width=2, fill=_fill())
    c.create_oval(cx - (outer - inner), cy - (outer - inner), cx + (outer - inner), cy + (outer - inner),
                  outline=_accent(), width=2, fill=_bg())
    c.create_text(cx + (outer + inner) + _label_offset(outer + inner), cy,
                  text=f"R={_lbl(values, 'major_radius')}, r={_lbl(values, 'minor_radius')}", fill=_edge(), anchor="w")


def _draw_tetrahedron(c, cx, cy, s, values):
    a = _val(values, "side") * s
    h = a * math.sqrt(3) / 2
    base = [(cx - a / 2, cy + h / 2), (cx + a / 2, cy + h / 2), (cx, cy - h / 2)]
    apex = (cx, cy - h / 2 - a * 0.55)
    for p in base:
        c.create_line(apex[0], apex[1], p[0], p[1], fill=_accent(), width=2)
    c.create_polygon(*_flat(base), outline=_accent(), width=2, fill=_fill())
    c.create_text(cx, cy + h / 2 + _label_offset(h), text=f"a={_lbl(values, 'side')}", fill=_edge())


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
    Circle: lambda v: (2 * _val(v, "radio"), 2 * _val(v, "radio")),
    Rectangle: lambda v: (_val(v, "base"), _val(v, "height")),
    Trapeze: lambda v: (_val(v, "base"), _val(v, "height")),
    RegularPolygon: lambda v: _polygon_extent(v),
    CircularSector: lambda v: (2 * _val(v, "radio"), 2 * _val(v, "radio")),
    Annulus: lambda v: (2 * _val(v, "radio"), 2 * _val(v, "radio")),
    Cube: lambda v: (1.55 * _val(v, "sides"), 1.55 * _val(v, "sides")),
    Cylinder: lambda v: (2 * _val(v, "radio"), _val(v, "height")),
    Sphere: lambda v: (2 * _val(v, "radio"), 2 * _val(v, "radio")),
    RectangularPyramid: lambda v: (_val(v, "base") + 0.6 * _val(v, "width"), _val(v, "height")),
    Cone: lambda v: (2 * _val(v, "radio"), _val(v, "height")),
    RectangularPrism: lambda v: (_val(v, "length") + 0.6 * _val(v, "width"), _val(v, "height")),
    Triangle: lambda v: (_val(v, "base"), _val(v, "height")),
    Ellipse: lambda v: (2 * _val(v, "semi_major"), 2 * _val(v, "semi_minor")),
    Rhombus: lambda v: (_val(v, "diag_major"), _val(v, "diag_minor")),
    Parallelogram: lambda v: (_val(v, "base") + 2 * abs(_val(v, "height")), _val(v, "height")),
    Torus: lambda v: (2 * (_val(v, "major_radius") + _val(v, "minor_radius")), 2 * (_val(v, "major_radius") + _val(v, "minor_radius"))),
    Tetrahedron: lambda v: (_val(v, "side"), _val(v, "side") * 1.4),
}


MIN_VISIBLE_PX = 160


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
    fit_scale = min((cw - 2 * MARGIN - 2 * LABEL_SPACE) / nw,
                    (ch - 2 * MARGIN - LABEL_SPACE) / nh)
    legible_scale = max(MIN_VISIBLE_PX / max(nw, nh), 1.0)
    scale = max(fit_scale, legible_scale)
    content_w = max(cw, nw * scale + 2 * MARGIN + 2 * LABEL_SPACE)
    content_h = max(ch, nh * scale + 2 * MARGIN + LABEL_SPACE)
    draw_func(canvas, content_w / 2, content_h / 2, scale, values)
    bbox = canvas.bbox("all")
    if bbox:
        x0, y0, x1, y1 = bbox
        pad = MARGIN
        region_w = max(content_w, x1 - x0 + 2 * pad)
        region_h = max(content_h, y1 - y0 + 2 * pad)
        content_w, content_h = region_w, region_h
    canvas.configure(scrollregion=(0, 0, content_w, content_h))
    if content_w > cw:
        canvas.xview_moveto((content_w - cw) / 2 / content_w)
    else:
        canvas.xview_moveto(0)
    if content_h > ch:
        canvas.yview_moveto((content_h - ch) / 2 / content_h)
    else:
        canvas.yview_moveto(0)
