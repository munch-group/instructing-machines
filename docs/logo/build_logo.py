import math, os, glob
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import cairosvg

# Written next to this script by default: docs/logo/
OUT = os.environ.get("IM_LOGO_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__))))
os.makedirs(OUT, exist_ok=True)

# ---------- fonts ----------
# The wordmark is now set in JetBrains Mono Medium. fontTools draws the DEFAULT
# instance of a variable font, so JetBrainsMono[wght].ttf would come out at
# Regular 400, you need the STATIC Medium. Grab it from
# https://github.com/JetBrains/JetBrainsMono/releases and drop it next to this
# script if none of the candidates below resolve.
FONT_CANDIDATES = [
    "./JetBrainsMono-Medium.ttf",
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf",
    "/usr/share/fonts/truetype/google-fonts/JetBrainsMono-Medium.ttf",
    "/Library/Fonts/JetBrainsMono-Medium.ttf",
    os.path.expanduser("~/Library/Fonts/JetBrainsMono-Medium.ttf"),
]

def resolve_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    hits = glob.glob("/usr/share/fonts/**/JetBrainsMono-Medium.ttf", recursive=True)
    if hits:
        return hits[0]
    raise SystemExit(
        "JetBrainsMono-Medium.ttf not found. Download the static Medium from\n"
        "  https://github.com/JetBrains/JetBrainsMono/releases\n"
        "and put it beside this script, or add its path to FONT_CANDIDATES.\n"
        "Do not substitute JetBrainsMono[wght].ttf, fontTools would draw it at 400."
    )

FONT = resolve_font()

TEAL   = "#0D7D93"   # $primary, the prompt
CARET  = "#7C5CB0"   # lightness-matched purple (was #7F77DD)
INK    = "#1A1A18"
AUBLUE = "#002546"
PAPER  = "#FFFFFF"

TEXT = "instructing machines"

# ---------- wordmark outlines ----------
_FONTS = {}

def _load(path):
    if path not in _FONTS:
        f = TTFont(path)
        _FONTS[path] = (f, f["head"].unitsPerEm, f.getGlyphSet(),
                        f.getBestCmap(), f["hmtx"])
    return _FONTS[path]

def wordmark(text, size, tracking=0.0, font_path=None):
    """(path_d, advance_width) for text as outlines, em box = size px."""
    font, upem, gs, cmap, hmtx = _load(font_path or FONT)
    scale = size / upem
    pen = SVGPathPen(gs)
    x = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            continue
        gs[gname].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0)))
        x += hmtx[gname][0] * scale + tracking
    return pen.getCommands(), x - (tracking if text else 0.0)

def advance(ch, size, font_path=None):
    font, upem, gs, cmap, hmtx = _load(font_path or FONT)
    return hmtx[cmap[ord(ch)]][0] * size / upem

def metrics(size, font_path=None):
    """(cap_height, descender) in px at the given em size."""
    font, upem, *_ = _load(font_path or FONT)
    os2 = font["OS/2"]
    cap = getattr(os2, "sCapHeight", None) or int(upem * 0.73)
    desc = abs(font["hhea"].descender)
    return cap * size / upem, desc * size / upem


# ---------- the prompt lockup (header variant 2d) ----------
def build_prompt(text=TEXT, fs=132.0, ink=INK, prompt_col=TEAL,
                 caret_col=CARET, bg=None, caret_w=0.50, caret_h=0.86,
                 caret_gap=0.28, caret_drop=0.16, pad=24.0):
    """`> instructing machines ▌`, a teal prompt, the name, a block caret.

    All four caret numbers are fractions of the em:
      caret_w     width of the block
      caret_h     height of the block
      caret_gap   space between the last letter and the block
      caret_drop  how far the block hangs BELOW the baseline

    The gap between the prompt and the name is one real monospace cell, so that
    part of the lockup is literally the string as it would be typed.
    """
    d_prompt, w_prompt = wordmark(">", fs)
    d_name, w_name = wordmark(text, fs)
    cell = advance(" ", fs)
    cap, desc = metrics(fs)

    cw, ch = caret_w * fs, caret_h * fs
    gap, drop = caret_gap * fs, caret_drop * fs
    x_name = w_prompt + cell
    x_caret = x_name + w_name + gap
    # place the baseline so the caret's top edge lands exactly on the padding
    baseline = pad + ch - drop
    h = baseline + max(desc, drop) + pad
    w = x_caret + cw + pad

    body = (
        f'<g transform="translate({pad:.2f} {baseline:.2f})">\n'
        f'  <path d="{d_prompt}" fill="{prompt_col}"/>\n'
        f'</g>\n'
        f'<g transform="translate({pad + x_name:.2f} {baseline:.2f})">\n'
        f'  <path d="{d_name}" fill="{ink}"/>\n'
        f'</g>\n'
        f'<rect x="{pad + x_caret:.2f}" y="{baseline - ch + drop:.2f}" '
        f'width="{cw:.2f}" height="{ch:.2f}" fill="{caret_col}"/>'
    )
    return svg(round(w), round(h), body, bg)


# ---------- favicon / app mark: >_ in a rounded square ----------
def _mark_body(s, bg_col=TEAL, fg=PAPER, radius=0.21, dx=0.0, dy=0.0):
    """Geometric, not glyph-based: strokes stay crisp at 16px where outlines mush."""
    sw = s * 0.08
    x0, y0 = dx + s * 0.34, dy + s * 0.33
    x1, y1 = dx + s * 0.54, dy + s * 0.50
    y2 = dy + s * 0.67
    ux1, ux2 = dx + s * 0.62, dx + s * 0.76
    return (
        f'<rect x="{dx:.2f}" y="{dy:.2f}" width="{s:.2f}" height="{s:.2f}" '
        f'rx="{s * radius:.2f}" fill="{bg_col}"/>\n'
        f'<path d="M{x0:.2f},{y0:.2f}L{x1:.2f},{y1:.2f}L{x0:.2f},{y2:.2f}" fill="none" '
        f'stroke="{fg}" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>\n'
        f'<path d="M{ux1:.2f},{y2:.2f}L{ux2:.2f},{y2:.2f}" fill="none" '
        f'stroke="{fg}" stroke-width="{sw:.2f}" stroke-linecap="round"/>'
    )

def build_prompt_mark(size=512.0, bg_col=TEAL, fg=PAPER, radius=0.21):
    return svg(round(size), round(size), _mark_body(size, bg_col, fg, radius))


# ---------- stacked: mark over the name, for square crops ----------
def build_prompt_stacked(text=TEXT, fs=92.0, mark=180.0, gap=44.0, pad=28.0,
                         ink=INK, caret_col=CARET, bg=None):
    d_name, w_name = wordmark(text, fs)
    cap, desc = metrics(fs)
    cw, ch = 0.50 * fs, 0.86 * fs
    gap, drop = 0.28 * fs, 0.16 * fs
    content_w = w_name + gap + cw
    w = max(content_w, mark) + 2 * pad
    cx = w / 2
    baseline = pad + mark + gap + ch
    h = baseline + desc + pad
    x_name = cx - content_w / 2
    body = (f'{_mark_body(mark, dx=cx - mark / 2, dy=pad)}\n'
            f'<g transform="translate({x_name:.2f} {baseline:.2f})">'
            f'<path d="{d_name}" fill="{ink}"/></g>\n'
            f'<rect x="{x_name + w_name + gap:.2f}" y="{baseline - ch + drop:.2f}" '
            f'width="{cw:.2f}" height="{ch:.2f}" fill="{caret_col}"/>')
    return svg(round(w), round(h), body, bg)


def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>\n' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n'
            f'<title>Instructing Machines</title>\n{b}{body}\n</svg>\n')


VARIANTS = {
    # header lockup
    "im-prompt":              build_prompt(),
    "im-prompt-mono-black":   build_prompt(ink=INK, prompt_col=INK, caret_col=INK),
    "im-prompt-mono-white":   build_prompt(ink=PAPER, prompt_col=PAPER, caret_col=PAPER),
    "im-prompt-au-blue":      build_prompt(ink=AUBLUE, prompt_col=AUBLUE, caret_col=AUBLUE),
    # on the dark band, if you ever reinstate one
    "im-prompt-on-dark":      build_prompt(ink=PAPER, prompt_col="#4FB3C4",
                                           caret_col="#A88FD8", bg="#00303C"),
    # square marks
    "im-mark":                build_prompt_mark(),
    "im-mark-ink":            build_prompt_mark(bg_col=INK),
    "im-mark-au-blue":        build_prompt_mark(bg_col=AUBLUE),
    # stacked
    "im-stacked":             build_prompt_stacked(),
}

PNG_WIDTHS = {
    "im-prompt": [1200, 2400],
    "im-prompt-mono-black": [1200],
    "im-prompt-mono-white": [1200],
    "im-prompt-au-blue": [1200],
    "im-prompt-on-dark": [1200],
    "im-mark": [16, 32, 64, 180, 512],
    "im-mark-ink": [512],
    "im-mark-au-blue": [512],
    "im-stacked": [1200],
}

for name, src in VARIANTS.items():
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(src)
    for wpx in PNG_WIDTHS[name]:
        suffix = f"-{wpx}px" if len(PNG_WIDTHS[name]) > 1 else ""
        cairosvg.svg2png(bytestring=src.encode(),
                         write_to=os.path.join(OUT, f"{name}{suffix}.png"),
                         output_width=wpx)

print(f"font: {FONT}")
print("\n".join(sorted(os.listdir(OUT))))
