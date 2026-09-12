#!/usr/bin/env python3
"""Split a notebook's markdown cells so that each block gets a cell of its own.

The turtle notes, like most of the book's .ipynb chapters, were authored as one
enormous markdown cell — prose and fenced code together, the code shown as text
rather than as cells that run. That reads fine and works badly for everything
else: a cell is the unit VS Code folds, moves and runs, so a chapter in one cell
cannot be worked on a paragraph at a time, and no fenced block can become
executable without first being a cell of its own.

This does the mechanical half of that. A block is a fenced code block, taken
whole, or a run of non-blank lines between blank lines — a heading, a paragraph,
the badge line under an exercise heading. Each becomes one markdown cell, in
order, and nothing else about the notebook changes.

Fenced code stays fenced, inside a markdown cell. Turning it into a code cell is
a separate decision with consequences this script has no business making on its
own: the notes are written to be typed rather than copy-pasted, and a code cell
also joins the set that ``pixi run clean-notebooks`` executes on every run.

What it will not do is split a cell holding a construct whose meaning survives
only while it stays in one piece — a ``:::`` callout or column-margin div, a
``$$`` display, a list, a table, a blockquote, an indented code block. A blank
line inside any of those is not a block boundary, and splitting there produces a
page that renders wrong in a way nothing here checks. It names them and stops,
leaving the notebook untouched.

Cells are written the way the repository stores them: nbformat's own line lists,
and no per-cell ``id`` unless the notebook is new enough to carry one (4.5 and
later — the book's notebooks are 4.4, where validation rejects it).

Run it on one notebook or several::

    python3 scripts/split_notebook_cells.py docs/turtle/turtle-functions.ipynb
    python3 scripts/split_notebook_cells.py --dry-run docs/turtle/*.ipynb

``--dry-run`` reports the cell count each notebook would end up with and writes
nothing, which is how to find out whether a chapter is safe to split before
splitting it. Exit status is 1 if any notebook was refused.

The rendered page should not change. Splitting a markdown cell in two puts a
blank line between two blocks that already had one, so pandoc sees the same
document either way. A render that differs before and after means the notebook
held one of the constructs above and this script failed to notice.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat

FENCE_CHARS = ("```", "~~~")

# Line openings that say this line belongs to something a blank line does not
# end, or would turn into a broken fragment if it were split off alone. The
# four-space entry catches an indented code block, which is why it is matched
# against the raw line rather than the stripped one.
UNSAFE_STARTS = (":::", "$$", "|", ">", "- ", "* ", "+ ", "    ")


def closes(line: str, fence: str) -> bool:
    """True if this line is the closing fence for an open ``fence``."""
    stripped = line.lstrip()
    return stripped.startswith(fence) and not stripped[len(fence):].strip()


def opens(line: str) -> str | None:
    """The fence characters this line opens a code block with, if it does."""
    stripped = line.lstrip()
    return next((f for f in FENCE_CHARS if stripped.startswith(f)), None)


def blocks(source: str):
    """Yield the blocks of one markdown cell, each as a list of lines."""
    current: list[str] = []
    fence: str | None = None

    for line in source.split("\n"):
        if fence is not None:
            current.append(line)
            if closes(line, fence):
                yield current
                current, fence = [], None
            continue

        opener = opens(line)
        if opener:
            # A fence starts a block of its own even with no blank line before
            # it, which is how the notes usually write one: prose, then code.
            if current:
                yield current
            current, fence = [line], opener
        elif line.strip():
            current.append(line)
        elif current:
            yield current
            current = []

    if fence is not None:
        raise ValueError("unclosed code fence")
    if current:
        yield current


def unsafe(source: str) -> list[str]:
    """The lines of ``source`` that belong to a construct this cannot split."""
    found: list[str] = []
    fence: str | None = None
    for line in source.split("\n"):
        if fence is not None:
            if closes(line, fence):
                fence = None
            continue
        opener = opens(line)
        if opener:
            fence = opener
            continue
        if any(line.startswith(start) for start in UNSAFE_STARTS):
            found.append(line[:70])
    return found


def new_cell(block: list[str], like) -> nbformat.NotebookNode:
    """A markdown cell holding one block, shaped like the cell it came from.

    Built by hand rather than with ``nbformat.v4.new_markdown_cell``, which
    stamps the per-cell ``id`` that only nbformat 4.5 and later allow. The
    source goes in as one string; nbformat's writer splits it back into the
    list of lines the repository's notebooks are stored as.
    """
    cell = nbformat.NotebookNode(
        cell_type="markdown",
        metadata=nbformat.NotebookNode(like.metadata),
        source="\n".join(block),
    )
    if "id" in like:
        # A 4.5+ notebook wants a distinct id per cell, so the pieces cannot
        # all inherit the id of the cell they were cut from.
        from nbformat.v4.nbbase import random_cell_id

        cell["id"] = random_cell_id()
    return cell


def split(path: Path, dry_run: bool) -> tuple[int, int] | None:
    """Split one notebook. Returns (before, after), or None if it was refused."""
    nb = nbformat.read(path, as_version=4)

    problems = [line for cell in nb.cells if cell.cell_type == "markdown"
                for line in unsafe("".join(cell.source))]
    if problems:
        print(f"{path}: refusing to split — these lines belong to a construct "
              f"that has to stay whole:", file=sys.stderr)
        for line in problems:
            print(f"    {line}", file=sys.stderr)
        return None

    before, cells = len(nb.cells), []
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            cells.append(cell)
            continue
        cells.extend(new_cell(block, cell) for block in blocks("".join(cell.source)))

    nb.cells = cells
    nbformat.validate(nb)
    if not dry_run:
        nbformat.write(nb, path)
    return before, len(cells)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="+", type=Path,
                        help="the .ipynb files to split")
    parser.add_argument("--dry-run", action="store_true",
                        help="report what each notebook would become, write nothing")
    args = parser.parse_args()

    refused = 0
    for path in args.notebooks:
        result = split(path, args.dry_run)
        if result is None:
            refused += 1
            continue
        before, after = result
        verb = "would become" if args.dry_run else "->"
        print(f"{path}: {before} cell(s) {verb} {after}")

    if refused:
        print(f"\n{refused} notebook(s) left untouched.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
