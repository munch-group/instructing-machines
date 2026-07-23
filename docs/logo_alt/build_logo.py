import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import cairosvg

OUT = "/mnt/user-data/outputs/logo"
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
PURPLE = "#7F77DD"
INK    = "#1A1A18"
AUBLUE = "#002546"
PAPER  = "#FFFFFF"

N_TEETH   = 9
TIP_RATIO = 1.215   # tooth tip radius / root radius
HOLE      = 0.760   # inner hole radius / root radius
W_ROOT    = 0.300   # tooth half-width at root, as fraction of pitch angle
W_TIP     = 0.205   # tooth half-width at tip, as fraction of pitch angle


def wordmark(text, size, tracking=0.0):
    font = TTFont(FONT)
    upem = font["head"].unitsPerEm
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    scale = size / upem
    pen = SVGPathPen(gs)
    x = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            continue
        gs[gname].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0)))
        x += hmtx[gname][0] * scale + tracking
    return pen.getCommands(), x - tracking


def gear_path(cx, cy, r):
    """Closed cogwheel outline: toothed rim plus a circular hole (evenodd)."""
    rt = r * TIP_RATIO
    pitch = 2 * math.pi / N_TEETH
    wr = pitch * W_ROOT
    wt = pitch * W_TIP
    P = lambda rad, a: (cx + rad * math.cos(a), cy + rad * math.sin(a))
    d = []
    a0 = -math.pi / 2
    x, y = P(r, a0 - wr)
    d.append(f"M{x:.2f} {y:.2f}")
    for k in range(N_TEETH):
        a = a0 + k * pitch
        for rad, ang in ((rt, a - wt), (rt, a + wt), (r, a + wr)):
            x, y = P(rad, ang)
            if rad == rt and ang == a + wt:
                d.append(f"A{rt:.2f} {rt:.2f} 0 0 1 {x:.2f} {y:.2f}")
            else:
                d.append(f"L{x:.2f} {y:.2f}")
        nx, ny = P(r, a + pitch - wr)
        d.append(f"A{r:.2f} {r:.2f} 0 0 1 {nx:.2f} {ny:.2f}")
    d.append("Z")
    h = r * HOLE
    d.append(f"M{cx + h:.2f} {cy:.2f}")
    d.append(f"A{h:.2f} {h:.2f} 0 1 0 {cx - h:.2f} {cy:.2f}")
    d.append(f"A{h:.2f} {h:.2f} 0 1 0 {cx + h:.2f} {cy:.2f}")
    d.append("Z")
    return " ".join(d)


def mark(cx, cy, r, ring_col, ink_col):
    stroke_w = r * 0.143
    e = [f'<path d="{gear_path(cx, cy, r)}" fill="{ring_col}" fill-rule="evenodd"/>']
    x1, y1 = cx - r * 0.356, cy - r * 0.347
    x2, y2 = cx + r * 0.053, cy - r * 0.009
    x3, y3 = cx - r * 0.356, cy + r * 0.329
    e.append(f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}L{x3:.2f} {y3:.2f}" '
             f'fill="none" stroke="{ink_col}" stroke-width="{stroke_w:.2f}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    uy = cy + r * 0.329
    e.append(f'<line x1="{cx + r * 0.165:.2f}" y1="{uy:.2f}" '
             f'x2="{cx + r * 0.467:.2f}" y2="{uy:.2f}" '
             f'stroke="{ink_col}" stroke-width="{stroke_w:.2f}" stroke-linecap="round"/>')
    return "\n".join(e)


def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>\n' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n'
            f'<title>Instructing Machines</title>\n{b}{body}\n</svg>\n')


TEXT = "Instructing Machines"
R_OUT = TIP_RATIO


def build_mark(ring, ink, bg=None):
    r, pad = 100.0, 8.0
    size = 2 * (r * R_OUT) + 2 * pad
    c = size / 2
    return svg(round(size), round(size), mark(c, c, r, ring, ink), bg)


def build_horizontal(ring, ink, bg=None):
    r, fs, pad = 60.0, 132.0, 24.0
    d, tw = wordmark(TEXT, fs)
    gap = r * 1.32
    cx = pad + r * R_OUT
    h = 2 * (r * R_OUT) + 2 * pad
    cy = h / 2
    tx = cx + r * R_OUT + gap
    ty = cy + fs * 0.355
    w = tx + tw + pad
    body = mark(cx, cy, r, ring, ink)
    body += f'\n<g transform="translate({tx:.2f} {ty:.2f})" fill="{ink}"><path d="{d}"/></g>'
    return svg(round(w), round(h), body, bg)


def build_stacked(ring, ink, bg=None):
    r, fs, pad = 84.0, 92.0, 28.0
    d, tw = wordmark(TEXT, fs)
    w = max(tw + 2 * pad, 2 * r * R_OUT + 2 * pad)
    cx = w / 2
    cy = pad + r * R_OUT
    ty = cy + r * R_OUT + pad * 2.3 + fs * 0.71
    h = ty + fs * 0.24 + pad
    body = mark(cx, cy, r, ring, ink)
    body += (f'\n<g transform="translate({cx - tw / 2:.2f} {ty:.2f})" fill="{ink}">'
             f'<path d="{d}"/></g>')
    return svg(round(w), round(h), body, bg)


VARIANTS = {
    "im-mark":                  build_mark(PURPLE, INK),
    "im-mark-mono-black":       build_mark(INK, INK),
    "im-mark-mono-white":       build_mark(PAPER, PAPER),
    "im-mark-au-blue":          build_mark(AUBLUE, AUBLUE),
    "im-horizontal":            build_horizontal(PURPLE, INK),
    "im-horizontal-mono-black": build_horizontal(INK, INK),
    "im-horizontal-mono-white": build_horizontal(PAPER, PAPER),
    "im-horizontal-au-blue":    build_horizontal(AUBLUE, AUBLUE),
    "im-stacked":               build_stacked(PURPLE, INK),
    "im-stacked-mono-black":    build_stacked(INK, INK),
    "im-stacked-mono-white":    build_stacked(PAPER, PAPER),
}

PNG_WIDTHS = {
    "im-mark": [32, 64, 256, 512, 1024],
    "im-mark-mono-black": [512],
    "im-mark-mono-white": [512],
    "im-mark-au-blue": [512],
    "im-horizontal": [1200, 2400],
    "im-horizontal-mono-black": [1200],
    "im-horizontal-mono-white": [1200],
    "im-horizontal-au-blue": [1200],
    "im-stacked": [1200],
    "im-stacked-mono-black": [1200],
    "im-stacked-mono-white": [1200],
}

for name, src in VARIANTS.items():
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(src)
    for wpx in PNG_WIDTHS[name]:
        suffix = f"-{wpx}px" if len(PNG_WIDTHS[name]) > 1 else ""
        cairosvg.svg2png(bytestring=src.encode(),
                         write_to=os.path.join(OUT, f"{name}{suffix}.png"),
                         output_width=wpx)

print("ok")
