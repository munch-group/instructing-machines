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

# ---------- wordmark outlines ----------
def wordmark(text, size, tracking=0.0):
    """Return (path_d, width) for text rendered as outlines at given cap size (px em)."""
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
        tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0))
        gs[gname].draw(tpen)
        x += hmtx[gname][0] * scale + tracking
    return pen.getCommands(), x - tracking

# ---------- gear + prompt mark ----------
def mark(cx, cy, r, ring_col, ink_col):
    """Gear ring with terminal prompt inside. r = ring radius."""
    ring_w   = r * 0.0625
    tooth_w  = r * 0.145
    tooth_in = r * 1.0
    tooth_out= r * 1.25
    prompt_w = r * 0.166
    e = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" '
         f'stroke="{ring_col}" stroke-width="{ring_w:.2f}"/>']
    e.append(f'<g stroke="{ring_col}" stroke-width="{tooth_w:.2f}" stroke-linecap="round">')
    for k in range(8):
        a = math.radians(45 * k)
        x1, y1 = cx + tooth_in * math.cos(a), cy + tooth_in * math.sin(a)
        x2, y2 = cx + tooth_out * math.cos(a), cy + tooth_out * math.sin(a)
        e.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')
    e.append('</g>')
    cx1, cy1 = cx - r * 0.458, cy - r * 0.458
    cx2, cy2 = cx + r * 0.042, cy
    cx3, cy3 = cx - r * 0.458, cy + r * 0.458
    e.append(f'<path d="M{cx1:.2f} {cy1:.2f}L{cx2:.2f} {cy2:.2f}L{cx3:.2f} {cy3:.2f}" '
             f'fill="none" stroke="{ink_col}" stroke-width="{prompt_w:.2f}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    ux1, uy = cx + r * 0.25, cy + r * 0.458
    ux2 = cx + r * 0.625
    e.append(f'<line x1="{ux1:.2f}" y1="{uy:.2f}" x2="{ux2:.2f}" y2="{uy:.2f}" '
             f'stroke="{ink_col}" stroke-width="{prompt_w:.2f}" stroke-linecap="round"/>')
    return "\n".join(e)

def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>\n' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n'
            f'<title>Instructing Machines</title>\n{b}{body}\n</svg>\n')

# ---------- layouts ----------
TEXT = "Instructing Machines"

def build_mark(ring, ink, bg=None):
    r, pad = 100.0, 10.0
    size = 2 * (r * 1.25) + 2 * pad
    c = size / 2
    return svg(round(size), round(size), mark(c, c, r, ring, ink), bg)

def build_horizontal(ring, ink, bg=None):
    r = 60.0
    fs = 132.0
    d, tw = wordmark(TEXT, fs)
    gap = r * 0.95
    pad = 24.0
    cx = pad + r * 1.25
    h = 2 * (r * 1.25) + 2 * pad
    cy = h / 2
    tx = cx + r * 1.25 + gap
    ty = cy + fs * 0.355
    w = tx + tw + pad
    body = mark(cx, cy, r, ring, ink)
    body += f'\n<g transform="translate({tx:.2f} {ty:.2f})" fill="{ink}"><path d="{d}"/></g>'
    return svg(round(w), round(h), body, bg)

def build_stacked(ring, ink, bg=None):
    r = 84.0
    fs = 92.0
    d, tw = wordmark(TEXT, fs)
    pad = 28.0
    w = max(tw + 2 * pad, 2 * r * 1.25 + 2 * pad)
    cx = w / 2
    cy = pad + r * 1.25
    ty = cy + r * 1.25 + pad * 1.5 + fs * 0.71
    h = ty + fs * 0.24 + pad
    body = mark(cx, cy, r, ring, ink)
    body += (f'\n<g transform="translate({cx - tw / 2:.2f} {ty:.2f})" fill="{ink}">'
             f'<path d="{d}"/></g>')
    return svg(round(w), round(h), body, bg)

VARIANTS = {
    "im-mark":              build_mark(PURPLE, INK),
    "im-mark-mono-black":   build_mark(INK, INK),
    "im-mark-mono-white":   build_mark(PAPER, PAPER),
    "im-mark-au-blue":      build_mark(AUBLUE, AUBLUE),
    "im-horizontal":            build_horizontal(PURPLE, INK),
    "im-horizontal-mono-black": build_horizontal(INK, INK),
    "im-horizontal-mono-white": build_horizontal(PAPER, PAPER),
    "im-horizontal-au-blue":    build_horizontal(AUBLUE, AUBLUE),
    "im-stacked":            build_stacked(PURPLE, INK),
    "im-stacked-mono-black": build_stacked(INK, INK),
    "im-stacked-mono-white": build_stacked(PAPER, PAPER),
}

PNG_WIDTHS = {
    "im-mark": [64, 256, 512, 1024],
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
    p = os.path.join(OUT, name + ".svg")
    with open(p, "w") as f:
        f.write(src)
    for wpx in PNG_WIDTHS[name]:
        suffix = f"-{wpx}px" if len(PNG_WIDTHS[name]) > 1 else ""
        cairosvg.svg2png(bytestring=src.encode(), write_to=os.path.join(OUT, f"{name}{suffix}.png"),
                         output_width=wpx)

print("\n".join(sorted(os.listdir(OUT))))
