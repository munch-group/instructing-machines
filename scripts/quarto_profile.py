"""Which config file the book's chapter list lives in.

Quarto merges `docs/_quarto.yml` with `docs/_quarto-<profile>.yml` for whichever
profile is in force, so the chapter list may sit in either one, and it has moved
between them more than once. Four scripts need that list — the badge checker,
the annotation collector, the notebook cleaner and the student-folder builder —
and all four must read the same book the render reads, or they quietly report on
a book nobody is publishing.

So rather than naming a file, this asks which file actually lists chapters. The
active profile's file wins when it has them (that is what a profile override
would mean); otherwise the base `_quarto.yml` does. The profile itself is
resolved the way Quarto resolves it: `QUARTO_PROFILE` when set, taking the first
name that has a file, since Quarto accepts a comma-separated list; otherwise the
`default:` named in `_quarto.yml`.

    from quarto_profile import quarto_config
    config = quarto_config(repo / "docs")
"""

from __future__ import annotations

import os
import re
from pathlib import Path

DEFAULT_PROFILE = re.compile(r"^\s*default:\s*(\S+)\s*$", re.M)

# "    - python/lists.ipynb". Deliberately not matching the quoted `- "!x.ipynb"`
# exclusions in the render list: those name a file the book leaves out, which is
# the opposite of a chapter.
CHAPTER_LINE = re.compile(r"^\s*-\s+[\w./-]+\.(?:qmd|md|ipynb)\s*$", re.M)


def profile_candidates(docs: Path) -> list[str]:
    """The profile names to try, most specific first."""
    names = [name.strip()
             for name in os.environ.get("QUARTO_PROFILE", "").split(",")
             if name.strip()]
    root = docs / "_quarto.yml"
    if root.exists():
        match = DEFAULT_PROFILE.search(root.read_text(encoding="utf-8"))
        if match and match.group(1) not in names:
            names.append(match.group(1))
    return names


def lists_chapters(path: Path) -> bool:
    return path.exists() and bool(CHAPTER_LINE.search(path.read_text(encoding="utf-8")))


def quarto_config(docs: Path) -> Path:
    """The config file that lists the chapters, for the profile now in force."""
    for name in profile_candidates(docs):
        candidate = docs / f"_quarto-{name}.yml"
        if lists_chapters(candidate):
            return candidate
    # The base config, whether or not it has chapters: when nothing does, this
    # is still the file a person would open to find out why.
    return docs / "_quarto.yml"


if __name__ == "__main__":                    # `python3 scripts/quarto_profile.py`
    here = Path(__file__).resolve().parent.parent / "docs"
    print(quarto_config(here))
