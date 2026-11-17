"""Draw the script-versus-notebook figure for docs/intro/notebooks.ipynb.

The figure is embedded in the notebook as a cell attachment rather than
linked as an image file, because a student fetches the notebook on its own
with `im get` (no images folder travels with it) and the book renders with
execution switched off. An attachment is the one form that shows up both on
the website and in VS Code.

Run from the repository root:

    python scripts/make_notebooks_figure.py

It redraws the PNG into docs/intro/images/ and replaces the attachment on the
notebook cell that shows it (found by its cell id).
"""

import base64
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

REPO = Path(__file__).resolve().parent.parent
NOTEBOOK = REPO / "docs" / "intro" / "notebooks.ipynb"
PNG = REPO / "docs" / "intro" / "images" / "script-vs-notebook.png"
CELL_ID = "f1g5cr1p"
PNG_ORDER = REPO / "docs" / "intro" / "images" / "run-order.png"
CELL_ID_ORDER = "f1g0rder"

INK = "#2b2b2b"
MUTED = "#6b6b6b"
PAPER = "#ffffff"
FILE_BG = "#f4f1ea"
CELL_BG = "#eef2f7"
PROC_BG = "#e6f2ea"
PROC_EDGE = "#3c8c5a"
GONE_BG = "#f6e7e4"
GONE_EDGE = "#b5523b"
ACCENT = "#2f6db5"
MONO = "DejaVu Sans Mono"


def box(ax, x, y, w, h, fc, ec=INK, lw=1.2, ls="-", r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls))


def arrow(ax, start, end, color=INK, lw=1.4, rad=0.0, style="-|>", ms=12):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def badge(ax, x, y, n, color=ACCENT):
    ax.text(x, y, str(n), ha="center", va="center", fontsize=9, color="white",
            fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.25", fc=color, ec="none"))


def snapshot(ax, x, y, w, rows, caption):
    """A white box showing memory at one moment, centred on height y."""
    h = 0.36 * max(len(rows), 1) + 0.22
    box(ax, x, y - h / 2, w, h, PAPER, ec=MUTED, lw=0.9, r=0.06)
    ax.text(x + 0.05, y + h / 2 + 0.15, caption, fontsize=8, color=MUTED, va="center",
            style="italic")
    if not rows:
        ax.text(x + 0.2, y, "empty", fontsize=9, color=MUTED, va="center", style="italic")
    for i, (name, value) in enumerate(rows):
        yy = y + h / 2 - 0.29 - 0.36 * i
        ax.text(x + 0.2, yy, name, family=MONO, fontsize=9.5, va="center", color=INK)
        ax.text(x + 0.85, yy, "\u2192", fontsize=9.5, va="center", color=MUTED)
        ax.text(x + 1.2, yy, value, family=MONO, fontsize=9.5, va="center", color=INK)


# What memory holds after each of the three lines (or cells) has run.
SNAPSHOTS = [
    [("dna", '"ATGTGCAT"')],
    [("dna", '"ATGTGCAT"'), ("n", "2")],
    [("dna", '"ATGTGCAT"'), ("n", "2")],
]


def timeline(ax, x0, x1, y, alive_until, label_start, label_end, ticks, dies):
    """Lifetime bar of a Python process along the bottom of a panel."""
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))
    ax.text(x1, y - 0.32, "time", fontsize=8.5, color=MUTED, ha="right", va="center")
    color = GONE_EDGE if dies else PROC_EDGE
    ax.plot([x0 + 0.15, alive_until], [y + 0.32, y + 0.32], color=color, lw=6,
            solid_capstyle="butt")
    ax.text(x0 + 0.15, y + 0.62, label_start, fontsize=8.5, color=INK, va="center")
    ax.text(alive_until, y + 0.62, label_end, fontsize=8.5, color=color, va="center",
            ha="right", fontweight="bold")
    if dies:
        ax.plot([alive_until], [y + 0.32], marker="X", ms=11, color=GONE_EDGE)
    else:
        ax.plot([alive_until], [y + 0.32], marker=">", ms=9, color=PROC_EDGE)
    for xt, n, color in ticks:
        badge(ax, xt, y + 0.32, n, color=color)


LINE_Y = [7.35, 5.9, 4.45]


def draw_script(ax):
    ax.text(0.2, 9.55, "Script", fontsize=15, fontweight="bold", color=INK)
    ax.text(1.65, 9.55, "python script.py", family=MONO, fontsize=11.5, color=MUTED,
            va="baseline")

    ax.text(0.2, 9.05, "Every line runs from top to bottom, and then Python exits.",
            fontsize=9.5, color=INK, va="center")

    # The file on disk.
    box(ax, 0.2, 3.7, 4.3, 5.1, FILE_BG)
    ax.text(0.4, 8.45, "script.py", family=MONO, fontsize=10, fontweight="bold")
    ax.text(0.4, 8.12, "a file on the disk", fontsize=8.5, color=MUTED, style="italic")
    lines = ['dna = "ATGTGCAT"', 'n = dna.count("A")', "print(n)"]
    for i, line in enumerate(lines):
        y = LINE_Y[i]
        ax.text(0.45, y, str(i + 1), family=MONO, fontsize=9, color=MUTED, va="center")
        ax.text(0.8, y, line, family=MONO, fontsize=10, va="center")

    # The Python process, which lives for this one run only.
    box(ax, 5.3, 3.7, 4.5, 5.1, GONE_BG, ec=GONE_EDGE, lw=1.4, ls=(0, (4, 2)))
    ax.text(5.5, 8.45, "Python process", fontsize=10.5, fontweight="bold", color=INK)
    ax.text(5.5, 8.12, "Runs all code in one go and exits", fontsize=8.5, color=GONE_EDGE,
            style="italic")
    for i, rows in enumerate(SNAPSHOTS):
        snapshot(ax, 5.55, LINE_Y[i], 4.0, rows, f"memory after line {i + 1}")

    # Python reads lines 1, 2, 3 from the file.
    for i in range(3):
        y = LINE_Y[i]
        arrow(ax, (4.15, y), (5.53, y), color=ACCENT, lw=1.2, ms=10)
        badge(ax, 4.8, y, i + 1)

    # The terminal shows what print wrote.
    box(ax, 0.2, 2.35, 4.3, 1.05, "#262626", ec="#262626")
    ax.text(0.4, 3.13, "Terminal", fontsize=8.5, color="#bdbdbd", va="center")
    ax.text(0.4, 2.7, "$ python script.py\n2", family=MONO, fontsize=9.5,
            color="#e8e8e8", va="center", linespacing=1.35)
    arrow(ax, (6.0, 3.65), (4.55, 2.95), color=INK, lw=1.0, rad=-0.25, ms=10)
    ax.text(6.0, 3.25, "print(n) writes 2", fontsize=8.5, color=MUTED, va="center")

    ax.text(5.3, 2.6, "Run it again and it starts from nothing.",
            fontsize=9.5, color=INK, va="center")

    timeline(ax, 0.2, 9.8, 1.25, alive_until=9.35, label_start="Python starts",
             label_end="runs until all code has executed", ticks=[(2.5, 1, ACCENT), (4.6, 2, ACCENT), (7.2, 3, ACCENT)],
             dies=True)


CODE = ['dna = "ATGTGCAT"', 'n = dna.count("A")', "print(n)"]
TICKS = [2.5, 4.6, 7.2]


def draw_notebook(ax, title, tagline, runs, title_suffix=None):
    """One notebook panel.

    `runs` has one entry per cell in page order: None for a cell that was never
    run, else (execution count, output text or None, True if it raised, memory
    rows after that run).
    """
    ax.text(0.2, 9.55, title, fontsize=15, fontweight="bold", color=INK)
    if title_suffix:
        ax.text(2.35, 9.55, title_suffix, family=MONO, fontsize=11.5, color=MUTED,
                va="baseline")
    ax.text(0.2, 9.05, tagline, fontsize=9.5, color=INK, va="center")

    # The file: cells in page order, each with the run number it got.
    box(ax, 0.2, 2.3, 4.5, 6.5, FILE_BG)
    ax.text(0.4, 8.45, "notebook.ipynb", family=MONO, fontsize=10, fontweight="bold")
    ax.text(0.4, 8.12, "a file on the disk, made of cells", fontsize=8.5, color=MUTED,
            style="italic")
    tops = [7.55, 5.95, 4.15]
    anchors = []
    for code, run, top in zip(CODE, runs, tops):
        count, out, failed, rows = run if run else (None, None, False, None)
        lines = out.count("\n") + 1 if out else 0
        h = 0.8 + (0.25 + 0.3 * lines if out else 0)
        box(ax, 1.05, top - h, 3.45, h, CELL_BG, ec=MUTED, lw=0.9, r=0.06)
        label = f"[{count}]" if count else "[ ]"
        ax.text(0.95, top - 0.38, label, family=MONO, fontsize=9.5,
                color=ACCENT if count else MUTED, ha="right", va="center",
                fontweight="bold")
        ax.text(1.2, top - 0.38, code, family=MONO, fontsize=10, va="center")
        if out:
            ax.plot([1.05, 4.5], [top - 0.78, top - 0.78], color=MUTED, lw=0.6)
            ax.text(1.2, top - 0.93, out, family=MONO, va="top",
                    fontsize=8.5 if failed else 10, linespacing=1.25,
                    color=GONE_EDGE if failed else INK)
        if count:
            anchors.append((top - 0.38, count, failed, rows))

    # The kernel, which keeps running between cells.
    box(ax, 5.6, 2.3, 4.2, 6.5, PROC_BG, ec=PROC_EDGE, lw=1.6)
    ax.text(5.8, 8.45, "iPython kernel", fontsize=10.5, fontweight="bold", color=INK)
    ax.text(5.8, 7.98, "Runs in the background.\nExecutes code in the cells you run.",
            fontsize=8.5, color=PROC_EDGE, style="italic")
    ax.text(5.85, 2.55, "kept until you restart the kernel",
            fontsize=8.5, color=PROC_EDGE, va="center")

    # Each run hands one cell to the kernel; the badge is the order in time,
    # red when the run raised an error.
    for y, count, failed, rows in anchors:
        snapshot(ax, 5.85, y, 3.7, rows, f"memory after run {count}")
        arrow(ax, (4.55, y), (5.83, y), color=ACCENT, lw=1.2, ms=10)
        badge(ax, 5.1, y, count, color=GONE_EDGE if failed else ACCENT)

    timeline(ax, 0.2, 9.8, 1.25, alive_until=9.35, label_start="kernel starts",
             label_end="runs until you close the notebook or restart the kernel",
             ticks=[(TICKS[c - 1], c, GONE_EDGE if f else ACCENT)
                    for _, c, f, _ in sorted(anchors, key=lambda a: a[1])],
             dies=False)


DNA = ("dna", '"ATGTGCAT"')
N = ("n", "2")
NO_DNA = "NameError: name 'dna'\nis not defined"
NO_N = "NameError: name 'n'\nis not defined"


def new_figure():
    fig, (left, right) = plt.subplots(1, 2, figsize=(13, 6.4), facecolor=PAPER)
    for ax in (left, right):
        ax.set_xlim(0, 10)
        ax.set_ylim(0.7, 10.1)
        ax.axis("off")
    fig.add_artist(plt.Line2D([0.5, 0.5], [0.06, 0.94], color="#d0d0d0", lw=1.0,
                              transform=fig.transFigure))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.08)
    return fig, left, right


def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, facecolor=PAPER)
    plt.close(fig)


def draw_script_vs_notebook() -> None:
    fig, left, right = new_figure()
    draw_script(left)
    draw_notebook(right, "Notebook",
                  "Each cell runs only when you run it. The numbers in [ ] record the order.",
                  [(1, None, False, [DNA]),
                   (2, None, False, [DNA, N]),
                   (3, "2", False, [DNA, N])],
                  title_suffix="notebook.ipynb")
    save(fig, PNG)


def draw_run_order() -> None:
    fig, left, right = new_figure()
    draw_notebook(left, "Cells 2 and 3",
                  "Cell 2 is run, then cell 3. Cell 1 is never run.",
                  [None,
                   (1, NO_DNA, True, []),
                   (2, NO_N, True, [])])
    draw_notebook(right, "Cells 2, 1, 3",
                  "Cell 2 is run first, then cell 1, then cell 3.",
                  [(2, None, False, [DNA]),
                   (1, NO_DNA, True, []),
                   (3, NO_N, True, [DNA])])
    save(fig, PNG_ORDER)


def embed(path, cell_id) -> None:
    nb = json.loads(NOTEBOOK.read_text())
    cell = next(c for c in nb["cells"] if c.get("id") == cell_id)
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    cell["attachments"] = {path.name: {"image/png": data}}
    NOTEBOOK.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    draw_script_vs_notebook()
    draw_run_order()
    embed(PNG, CELL_ID)
    embed(PNG_ORDER, CELL_ID_ORDER)
    print(f"wrote {PNG.name} and {PNG_ORDER.name} and embedded them in {NOTEBOOK.relative_to(REPO)}")
