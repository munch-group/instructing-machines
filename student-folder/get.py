#!/usr/bin/env python3
"""Fetch a lecture notebook from the course website into this folder.

    pixi run get iteration

You get exactly the same notebook as the **Download notebook** button on the
website gives you. The difference is where it lands: right here, next to the
data files and the Python environment, instead of in your Downloads folder.

To see which chapters you can ask for:

    pixi run get

If you already have a notebook of that name, yours is left alone and the fresh
copy is saved beside it with a number on the end. Nothing you have written is
ever overwritten.
"""

from __future__ import annotations

import difflib
import sys
import urllib.error
from pathlib import Path

from course import HERE, fetch, url_for

INDEX = "notebooks/index.txt"


def available() -> list[str]:
    """The chapter names the website is offering, one per line."""
    return [line.strip() for line in fetch(INDEX).splitlines() if line.strip()]


def normalise(name: str) -> str:
    """Fold away the differences nobody should have to remember.

    So `data_structures`, `data-structures`, `Data Structures` and
    `data_structures.ipynb` all mean the same chapter.
    """
    name = name.strip()
    if name.endswith(".ipynb"):
        name = name[: -len(".ipynb")]
    return name.replace("-", "_").replace(" ", "_").lower()


def resolve(wanted: str, chapters: list[str]) -> str | None:
    return {normalise(c): c for c in chapters}.get(normalise(wanted))


def free_path(stem: str) -> tuple[Path, bool]:
    """Where to save, and whether we had to step aside for an existing file."""
    target = HERE / f"{stem}.ipynb"
    if not target.exists():
        return target, False
    number = 2
    while (HERE / f"{stem}-{number}.ipynb").exists():
        number += 1
    return HERE / f"{stem}-{number}.ipynb", True


def main(argv: list[str]) -> int:
    try:
        chapters = available()
    except urllib.error.URLError as error:
        print(f"Could not reach the course website: {error}")
        print("Check that you are online. Nothing has been changed.")
        return 1

    if not chapters:
        print("The course website is not offering any notebooks right now.")
        print("Use the Download notebook button on the website instead.")
        return 1

    if not argv:
        print("Ask for one of these, like `pixi run get iteration`:\n")
        for chapter in chapters:
            print(f"    {chapter}")
        return 0

    if len(argv) > 1:
        print("One chapter at a time, please, like `pixi run get iteration`.")
        return 1

    wanted = argv[0]
    stem = resolve(wanted, chapters)

    if stem is None:
        print(f"There is no chapter called '{wanted}'.")
        near = difflib.get_close_matches(wanted, chapters, n=3, cutoff=0.6)
        if near:
            print("Did you mean: " + ", ".join(near) + "?")
        else:
            print("Run `pixi run get` on its own to see the whole list.")
        return 1

    print(f"Fetching {url_for(f'notebooks/{stem}.ipynb')}")
    try:
        text = fetch(f"notebooks/{stem}.ipynb")
    except urllib.error.URLError as error:
        print(f"\nCould not download it: {error}")
        print("Nothing has been changed.")
        return 1

    # A notebook is a JSON file, and every notebook has cells. If what came
    # back does not, it is a "page not found" page wearing a notebook's name.
    if '"cells"' not in text:
        print("\nWhat came back does not look like a notebook.")
        print("Nothing has been changed. Please tell your instructor.")
        return 1

    target, stepped_aside = free_path(stem)
    target.write_text(text, encoding="utf-8")

    if stepped_aside:
        print(f"\nYou already had {stem}.ipynb, so I left it exactly as it was.")
        print(f"The fresh copy is {target.name}.")
    else:
        print(f"\nSaved {target.name}. Open it in VS Code and pick the .pixi kernel.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
