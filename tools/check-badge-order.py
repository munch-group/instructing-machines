#!/usr/bin/env python3
"""Check that the AI role ladder in the book runs straight.

The course licenses the assistant in nine escalating roles.  Each role is
introduced by exactly one chapter, and no exercise may license a role before
the chapter that introduces it.  This script walks ``docs/_quarto.yml`` in
render order, reads the badge under every ``#### Exercise`` heading, and fails
if a badge appears too early.

A badge is a small-caps link to the rung's own section in
``intro/course-introduction.qmd``, so a student who has forgotten what a role
permits is one click from the answer::

    #### Exercise
    [[ai: drafter]{.smallcaps}](../intro/course-introduction.qmd#sec-badge-drafter)

Badges are written in lower case; this script matches them case-insensitively
and reports them in the ladder's own capitalisation.

Run it with no arguments from anywhere in the repository::

    python3 tools/check-badge-order.py

Add ``--census`` to print the per-role and per-week tables instead of just the
verdict.  Exit status is 0 when the ladder is straight and 1 when it is not,
so it can sit in the render workflow.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# The ladder, in the order the course grants it.  The second field is the
# chapter that introduces the role: the first chapter, in render order, that
# is allowed to carry the badge.  Change this map when you move a note, and
# the build will tell you which exercises now sit on the wrong side of it.
LADDER = [
    ("Explainer",           "intro/course-introduction.qmd"),
    ("Translator",          "ai/how-models-produce-code.qmd"),
    ("Illustrator",         "ai/how-models-produce-code.qmd"),
    ("Comparer",            "ai/ask-for-another-way.qmd"),
    ("Drafter",             "ai/let-it-draft.qmd"),
    ("Unreliable Narrator", "ai/reading-and-judging.md"),
    ("Worker",              "ai/tests-are-the-contract.md"),
    ("Collaborator",        "ai/plan-before-you-prompt.md"),
    ("Delegate",            "ai/delegate-the-full-problem.md"),
]
INTRODUCED_BY = dict(LADDER)

HEADING = re.compile(r"^#{2,6}\s+Exercise\b(.*)$")
# A badge is a small-caps link to the rung's section in the course
# introduction, e.g.
#   [[ai: drafter]{.smallcaps}](../intro/course-introduction.qmd#sec-badge-drafter)
# The bare code span is the older form, and the older Title Case spelling is
# also still recognised, so that a half-converted note is reported rather than
# silently skipped.
BADGE = re.compile(r"(?:`|\[\[)(SOLO|AI: [A-Za-z ]+?)(?:`|\]\{\.smallcaps\})",
                   re.IGNORECASE)


def canonical(badge: str) -> str:
    """The badge as the ladder spells it, whatever case the note used."""
    if badge.strip().lower() == "solo":
        return "SOLO"
    role = badge.split(":", 1)[1].strip()
    return "AI: " + " ".join(word.capitalize() for word in role.split())
# A chapter line in _quarto.yml: "        - ai/meet-ai.qmd" (comments skipped).
CHAPTER = re.compile(r"^\s*-\s+(?!part:)([\w./-]+\.(?:qmd|md|ipynb))\s*$")
PART = re.compile(r'^\s*-\s+part:\s*"?([^"\n]+?)"?\s*$')


def chapters_in_order(quarto_yml: Path):
    """Yield (week, path) for every chapter _quarto.yml actually renders."""
    week = None
    for line in quarto_yml.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("#"):
            continue
        part = PART.match(line)
        if part:
            week = part.group(1)
            continue
        chapter = CHAPTER.match(line)
        if chapter:
            yield week, chapter.group(1)


def markdown_of(path: Path) -> str:
    """The prose of a chapter, whether it is markdown or a notebook."""
    text = path.read_text(encoding="utf-8")
    if path.suffix != ".ipynb":
        return text
    # A notebook stores each cell's source as a JSON array of lines, so the
    # headings are invisible to a plain grep of the file.
    notebook = json.loads(text)
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "markdown"
    )


def badges_in(path: Path):
    """Yield (line number, badge) for every badged exercise heading."""
    lines = markdown_of(path).split("\n")
    for number, line in enumerate(lines, start=1):
        heading = HEADING.match(line)
        if not heading:
            continue
        inline = BADGE.search(heading.group(1))
        if inline:
            yield number, canonical(inline.group(1))
            continue
        # Otherwise the badge sits on its own line just below the heading.
        for below in lines[number : number + 3]:
            if not below.strip():
                continue
            found = BADGE.search(below)
            if found:
                yield number, canonical(found.group(1))
            break


def inline_badges_in(path: Path):
    """Yield (line number, badge) for every badge still stuck in its heading.

    The badge belongs on its own line below the heading.  Inline, it collides
    with the subsubsection number Quarto generates for the PDF, so the form is
    not merely untidy: it renders wrong.
    """
    for number, line in enumerate(markdown_of(path).split("\n"), start=1):
        heading = HEADING.match(line)
        if not heading:
            continue
        inline = BADGE.search(heading.group(1))
        if inline:
            yield number, canonical(inline.group(1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", action="store_true",
                        help="print the per-role and per-week counts as well")
    args = parser.parse_args()

    docs = Path(__file__).resolve().parent.parent / "docs"
    quarto_yml = docs / "_quarto.yml"
    if not quarto_yml.exists():
        print(f"cannot find {quarto_yml}", file=sys.stderr)
        return 1

    seen_order = [path for _, path in chapters_in_order(quarto_yml)]
    position = {path: index for index, path in enumerate(seen_order)}

    problems = []
    inline = []
    missing = []
    per_role = Counter()
    per_week = defaultdict(Counter)
    first_week = {}

    for week, chapter in chapters_in_order(quarto_yml):
        path = docs / chapter
        if not path.exists():
            missing.append(chapter)
            continue
        for line, badge in inline_badges_in(path):
            inline.append(
                f"{chapter}:{line}: `{badge}` is inline in the heading;"
                " it belongs on its own line below it")
        for line, badge in badges_in(path):
            per_role[badge] += 1
            per_week[week][badge] += 1
            if badge == "SOLO":
                continue
            role = badge[len("AI: "):]
            introducer = INTRODUCED_BY.get(role)
            if introducer is None:
                problems.append(
                    f"{chapter}:{line}: `{badge}` is not a rung of the ladder")
                continue
            first_week.setdefault(role, week)
            if introducer not in position:
                problems.append(
                    f"{chapter}:{line}: `{badge}` is introduced by {introducer},"
                    " which _quarto.yml does not render")
            elif position[chapter] < position[introducer]:
                problems.append(
                    f"{chapter}:{line}: `{badge}` is licensed here, but"
                    f" {introducer} introduces the role and comes later")

    if args.census:
        print("Role                  Badges  Introduced by")
        for role, introducer in [("SOLO", "-")] + LADDER:
            key = role if role == "SOLO" else f"AI: {role}"
            print(f"{role:21s} {per_role[key]:6d}  {introducer}")
        print()
        for week in per_week:
            counts = ", ".join(f"{b} x{n}" for b, n in sorted(per_week[week].items()))
            print(f"{week}: {counts}")
        print()

    if missing:
        print("Chapters listed in _quarto.yml but not on disk:")
        for chapter in missing:
            print(f"  {chapter}")
        print()

    if inline:
        print(f"{len(inline)} badge(s) are still inline in their heading:")
        for one in inline:
            print(f"  {one}")
        print("The badge goes on its own line below the heading, with a blank"
              " line either side, or the PDF renders it against the generated"
              " subsubsection number.")
        return 1

    total = sum(per_role.values())
    if problems:
        print(f"The ladder is out of order in {len(problems)} place(s):")
        for problem in problems:
            print(f"  {problem}")
        return 1

    if not total:
        # A green tick on nothing checked is worse than a red one: it means
        # the badge format moved and BADGE stopped matching it.
        print("No badges found at all.  The badge format has probably changed"
              " and this check has gone blind — update BADGE in this script.")
        return 1

    print(f"The ladder runs straight: {total} badged exercises,"
          f" {len(seen_order)} chapters, no role licensed before it is taught.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
