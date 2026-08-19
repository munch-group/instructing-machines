#!/usr/bin/env python3
"""Check that the AI role ladder in the book runs straight.

The course licenses the assistant in five escalating roles.  Each role is
introduced by exactly one chapter, and no exercise may license a role before
the chapter that introduces it.  This script walks the book's chapter list in
render order (``scripts/quarto_profile.py`` finds whichever config file holds
it), reads the badge under every ``#### Exercise`` heading, and fails if a badge
appears too early.

Translator, Illustrator and Worker were retired: the first two were folded
into Explainer (translating code to English and back, and asking for more
examples, are now moves within that rung) and Worker was folded into Drafter
(writing tests before any code, and hiding them from the assistant, is now a
stricter form of that rung). A badge using one of the three old names is not
a stale reference to update quietly; it is a ladder violation this script
should catch, which is why they stay out of LADDER below rather than being
mapped onto their replacements.

A badge is a plain link, set smaller than the surrounding text, to the rung's
own section in ``intro/course-introduction.qmd``, so a student who has
forgotten what a role permits is one click from the answer::

    #### Exercise
    [AI: Drafter](../intro/course-introduction.qmd#sec-badge-drafter){.small}

Badges are written in Title Case; this script matches them case-insensitively
and reports them in the ladder's own capitalisation.

Run it with no arguments from anywhere in the repository::

    python3 scripts/check-badge-order.py

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

# quarto_profile lives next to this script, so import it by the script's own
# location rather than trusting the working directory: build_student_folder.py
# runs from docs/ as Quarto's post-render hook, and todo.py loads
# check-badge-order.py by path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from quarto_profile import quarto_config  # noqa: E402

# The ladder, in the order the course grants it.  The second field is the
# chapter that introduces the role: the first chapter, in render order, that
# is allowed to carry the badge.  Change this map when you move a note, and
# the build will tell you which exercises now sit on the wrong side of it.
LADDER = [
    ("Explainer",           "intro/course-introduction.qmd"),
    ("Comparer",            "ai/ask-for-another-way.qmd"),
    ("Drafter",             "ai/let-it-draft.qmd"),
    ("Collaborator",        "ai/plan-before-you-prompt.md"),
    ("Developer",           "ai/delegate-the-full-problem.md"),
]
INTRODUCED_BY = dict(LADDER)

HEADING = re.compile(r"^#{2,6}\s+Exercise\b(.*)$")
# A badge is a plain link, set smaller than the surrounding text, to the
# rung's section in the course introduction, e.g.
#   [AI: Drafter](../intro/course-introduction.qmd#sec-badge-drafter){.small}
# The bare code span and the small-caps span are older forms, still
# recognised so that a half-converted note is reported rather than silently
# skipped.
BADGE = re.compile(
    r"`(SOLO|AI: [A-Za-z ]+?)`"
    r"|\[\[(SOLO|AI: [A-Za-z ]+?)\]\{\.smallcaps\}\]"
    r"|\[(SOLO|AI: [A-Za-z ]+?)\]\([^)]*\)\{\.small\}",
    re.IGNORECASE,
)


def canonical(match: "re.Match[str]") -> str:
    """The badge as the ladder spells it, whatever case or form the note used."""
    badge = next(g for g in match.groups() if g is not None)
    if badge.strip().lower() == "solo":
        return "SOLO"
    role = badge.split(":", 1)[1].strip()
    return "AI: " + " ".join(word.capitalize() for word in role.split())
# A chapter line in the config: "        - ai/meet-ai.qmd" (comments skipped).
CHAPTER = re.compile(r"^\s*-\s+(?!part:)([\w./-]+\.(?:qmd|md|ipynb))\s*$")


PART = re.compile(r'^\s*-\s+part:\s*"?([^"\n]+?)"?\s*$')


def chapters_in_order(quarto_yml: Path):
    """Yield (week, path) for every chapter the book actually renders."""
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
            yield number, canonical(inline)
            continue
        # Otherwise the badge sits on its own line just below the heading.
        for below in lines[number : number + 3]:
            if not below.strip():
                continue
            found = BADGE.search(below)
            if found:
                yield number, canonical(found)
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
            yield number, canonical(inline)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", action="store_true",
                        help="print the per-role and per-week counts as well")
    args = parser.parse_args()

    docs = Path(__file__).resolve().parent.parent / "docs"
    quarto_yml = quarto_config(docs)
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
                    f" which {quarto_yml.name} does not render")
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
        print(f"Chapters listed in {quarto_yml.name} but not on disk:")
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

    if not seen_order:
        # Nothing to check because nothing is listed. With profiles this is the
        # likelier of the two blind spots: a profile whose file carries no
        # chapters of its own renders no book, and a checker that shrugged at
        # that would report a straight ladder for a book that does not exist.
        print(f"{quarto_yml.name} lists no chapters, so there was nothing to"
              " check.  Either that profile has no book of its own, or"
              " QUARTO_PROFILE names the wrong one.")
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
