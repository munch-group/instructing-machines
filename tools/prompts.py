#!/usr/bin/env python3
"""Collect the inline instructions left in the book for the assistant.

While authoring, it is much cheaper to write "expand this" next to the
paragraph than to remember it and describe it afterwards in a chat message.
This script is the other half of that: it walks ``docs/_quarto.yml`` in render
order and prints every instruction, where it sits, and what it points at, so
the assistant can pick up a term's worth of notes-to-self in one go.

The notation is a token inside an ordinary comment, in the form the
surrounding cell already uses::

    <!-- CLAUDE: expand the paragraph below to cover the empty string -->

    # CLAUDE: add four exercises about lists here, predict-then-run

The prose form works in a markdown cell, a ``.qmd`` and a ``.md``; the code
form works in a code cell and a ``.py``.  Both are invisible to the student:
pandoc drops the comment for PDF and EPUB, and leaves it unrendered in HTML.
The token matters more than the comment does.  A bare ``<!-- ... -->`` is not
enough to search for, because the book already contains over a thousand of
them -- commented-out figures, slide scratch, notes to self -- and an
instruction lost in that crowd is an instruction that never gets done.

An instruction applies to what follows it, up to the next heading, unless its
own text says otherwise.  Put it immediately above the paragraph, cell or
exercise it is about, rather than at the top of the chapter: "the paragraph
below" is unambiguous, "the third paragraph" stops being true on the next
edit.

Instructions also live in ``docs/_quarto.yml`` itself, in the ``#`` form,
where they carry the work that belongs to a chapter as a whole rather than to
a paragraph inside it -- and the work that belongs to no chapter at all, which
has nowhere else to sit.  Those are read first and reported against the
chapter line they are written under.

Run it from anywhere in the repository::

    python3 tools/prompts.py                # everything, in render order
    python3 tools/prompts.py --json         # the same, for a machine
    python3 tools/prompts.py python/lists   # only chapters matching a string
    python3 tools/prompts.py --strict       # exit 1 if any instruction remains

Exit status is 1 when an instruction is malformed -- ``<!-- CLAUDE add a
figure -->`` with no colon, say -- because a malformed instruction is worse
than an unfinished one: it is silently invisible to this script and so will
never be picked up at all.  Otherwise it is 0, since leaving instructions
lying around is the normal state of a chapter being written, and only
``--strict`` treats that as a failure.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

# check-badge-order.py already knows how to read _quarto.yml in render order.
# Its name has a hyphen in it, so it cannot be imported by name; loading it by
# path is uglier than "import" and still better than a second copy of the
# parser that can drift from the first.
def _sibling(name: str):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), Path(__file__).resolve().parent / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ORDER = _sibling("check-badge-order.py")

# The instruction itself.  Case-insensitive on the token so that a shouted or
# a quiet CLAUDE both count, and tolerant of whitespace around the colon.
PROSE = re.compile(r"<!--\s*CLAUDE\s*:\s*(.*?)-->", re.S | re.I)
CODE = re.compile(r"#\s*CLAUDE\s*:\s*(.*)$", re.I | re.M)  # re.M: a code
# cell is many lines, and without it "$" would only match the last of them.

# Near misses: the token is there but the shape is wrong, so neither pattern
# above will ever see it.  Reported loudly rather than skipped.
MALFORMED = re.compile(r"(<!--[^>]{0,20}CLAUDE(?!\s*:)[^>]{0,60}-->"
                       r"|^\s*#\s*CLAUDE(?!\s*:).{0,60}$)", re.M | re.I)

HEADING = re.compile(r"^#{1,6}\s")

# Reading _quarto.yml as prose rather than as YAML, because a YAML parser
# throws comments away and the comments are the entire point here.
PART = re.compile(r"^\s*-\s*part:\s*[\"']?(.+?)[\"']?\s*$")
CHAPTER = re.compile(r"^\s{4,}-\s+([\w./-]+\.(?:qmd|md|ipynb))\s*$")
QSTART = re.compile(r"^\s*#\s*CLAUDE\s*:\s*(.*)$", re.I)
# A continuation is a comment line indented past the token; ordinary
# commentary in this file is written with a single space after the "#", so the
# two cannot be confused and a blank "#" ends an instruction.
QCONT = re.compile(r"^\s*#\s{2,}(\S.*)$")


def cells_of(path: Path):
    """Yield (kind, first line number, text) for each cell of a chapter.

    A ``.qmd`` or ``.md`` is one cell of prose.  A notebook is its cells, kept
    separate so that a location can name the cell a student would click on,
    and so that a code cell is scanned for the ``#`` form rather than the
    ``<!-- -->`` one.
    """
    text = path.read_text(encoding="utf-8")
    if path.suffix != ".ipynb":
        yield "markdown", 1, text
        return
    line = 1
    for cell in json.loads(text).get("cells", []):
        source = "".join(cell.get("source", []))
        yield cell.get("cell_type", "markdown"), line, source
        line += source.count("\n") + 1


def target_of(body: str, offset: int) -> str:
    """The first line of what an instruction points at, for the report.

    Blank lines and the tail of the instruction's own line are skipped; the
    search stops at the next heading, because an instruction does not reach
    past one.
    """
    for line in body[offset:].split("\n")[1:]:
        stripped = line.strip()
        if not stripped:
            continue
        if HEADING.match(stripped):
            return "(end of section)"
        return stripped[:88] + ("..." if len(stripped) > 88 else "")
    return "(end of chapter)"


def instructions_in(path: Path):
    """Yield every instruction in a chapter, in the order it is read."""
    for kind, first, body in cells_of(path):
        pattern = CODE if kind == "code" else PROSE
        for found in pattern.finditer(body):
            line = first + body[:found.start()].count("\n")
            yield {
                "line": line,
                "cell": kind,
                "text": " ".join(found.group(1).split()),
                "target": target_of(body, found.end()),
            }


def malformed_in(path: Path):
    """Yield (line, text) for every instruction the patterns cannot read."""
    for _, first, body in cells_of(path):
        for found in MALFORMED.finditer(body):
            # A well-formed instruction never reaches here, but a code cell
            # discussing the convention might; the colon is the whole test.
            line = first + body[:found.start()].count("\n")
            yield line, " ".join(found.group(0).split())[:100]


def instructions_in_quarto(path: Path):
    """Yield every instruction written into _quarto.yml itself.

    An instruction is reported against the chapter line it sits under, or as
    week-wide or book-wide when it sits under a part or above the first one.
    """
    found, current = [], None
    week, chapter = "None", "(book-wide)"
    for number, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        part = PART.match(raw)
        if part:
            week, chapter, current = part.group(1), "(week-wide)", None
        seen = CHAPTER.match(raw)
        if seen:
            chapter, current = seen.group(1), None
        start = QSTART.match(raw)
        if start:
            current = {"week": week, "chapter": chapter, "line": number,
                       "cell": "yaml", "text": start.group(1).strip(),
                       "target": chapter}
            found.append(current)
            continue
        if current is not None:
            more = QCONT.match(raw)
            if more:
                current["text"] += " " + more.group(1).strip()
            else:
                current = None
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("match", nargs="?", default="",
                        help="only chapters whose path contains this string")
    parser.add_argument("--json", action="store_true",
                        help="machine-readable output")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if any instruction is still outstanding")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    docs = root / "docs"

    collected, broken = [], []
    for one in instructions_in_quarto(docs / "_quarto.yml"):
        if args.match and args.match not in one["chapter"]:
            continue
        collected.append(one)
    for week, relative in ORDER.chapters_in_order(docs / "_quarto.yml"):
        if args.match and args.match not in relative:
            continue
        path = docs / relative
        if not path.exists():
            continue
        for one in instructions_in(path):
            collected.append({"week": week, "chapter": relative, **one})
        for line, text in malformed_in(path):
            broken.append({"chapter": relative, "line": line, "text": text})

    if args.json:
        print(json.dumps({"instructions": collected, "malformed": broken},
                         indent=2, ensure_ascii=False))
    else:
        chapter = object()
        for one in collected:
            if one["chapter"] != chapter:
                chapter = one["chapter"]
                print(f"\n{one['week']} - {chapter}")
            where = f"line {one['line']}"
            if one["cell"] == "code":
                where += ", code cell"
            elif one["cell"] == "yaml":
                where += ", in _quarto.yml"
            print(f"  {where}: {one['text']}")
            if one["cell"] != "yaml":
                print(f"      points at: {one['target']}")
        if collected:
            print(f"\n{len(collected)} instruction(s) outstanding.")
        else:
            print("No instructions outstanding.")

    if broken:
        print(f"\n{len(broken)} instruction(s) are malformed and would never "
              f"be picked up:", file=sys.stderr)
        for one in broken:
            print(f"  {one['chapter']}:{one['line']}: {one['text']}",
                  file=sys.stderr)
        print("The form is 'CLAUDE:' with a colon, inside an HTML comment in "
              "prose or after a # in a code cell.", file=sys.stderr)
        return 1

    return 1 if (args.strict and collected) else 0


if __name__ == "__main__":
    sys.exit(main())
