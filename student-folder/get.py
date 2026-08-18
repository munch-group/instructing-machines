#!/usr/bin/env python3
"""Fetch a chapter notebook, or a whole project, from the course website.

    pixi run get iteration              a lecture notebook
    pixi run get alignmentproject       a project

You get exactly the same files as the **Download notebook** and **Download
project** buttons on the website give you. The difference is where they land:
right here, next to the data files and the Python environment, instead of in
your Downloads folder.

To see everything you can ask for:

    pixi run get

A notebook lands beside this file; a project lands in `projects/`. Neither ever
overwrites your work. If you already have a notebook of that name, yours is left
alone and the fresh copy is saved beside it with a number on the end. If you
already have a project of that name, nothing happens at all.
"""

from __future__ import annotations

import difflib
import sys
import urllib.error
from pathlib import Path

import project
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


def download(stem: str) -> int:
    """Fetch the notebook for chapter `stem` into this folder."""
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


def catalog(offering) -> tuple[list[str], Exception | None]:
    """What one of the two lists is offering, or nothing if it is not there.

    Asked for separately, and forgiven separately: a website published before
    the projects existed has no project list, and that should cost you the
    projects rather than the whole command.
    """
    try:
        return offering(), None
    except urllib.error.URLError as error:
        return [], error


def main(argv: list[str]) -> int:
    chapters, chapter_error = catalog(available)
    projects, project_error = catalog(project.available)

    if not chapters and not projects:
        error = chapter_error or project_error
        if error is not None:
            print(f"Could not reach the course website: {error}")
            print("Check that you are online. Nothing has been changed.")
        else:
            print("The course website is not offering anything right now.")
            print("Use the download buttons on the website instead.")
        return 1

    if not argv:
        if chapters:
            print("Ask for a chapter, like `pixi run get iteration`:\n")
            for chapter in chapters:
                print(f"    {chapter}")
        if projects:
            print("\nOr for a project, like `pixi run get alignmentproject`:\n")
            for name in projects:
                print(f"    {name}")
        return 0

    if len(argv) > 1:
        print("One at a time, please, like `pixi run get iteration`.")
        return 1

    wanted = argv[0]
    chapter = resolve(wanted, chapters)
    name = project.resolve(wanted, projects)

    # Nothing is called both today, but nothing stops a chapter and a project
    # from sharing a name later, and quietly picking one of them would be a
    # bad way to find out. The file extension settles it.
    if chapter and name:
        as_chapter = f"{chapter}.ipynb"
        as_project = f"{name}.zip"
        width = max(len(as_chapter), len(as_project))
        print(f"There is both a chapter and a project called '{wanted}'.")
        print("")
        print(f"    pixi run get {as_chapter:<{width}}   for the chapter")
        print(f"    pixi run get {as_project:<{width}}   for the project")
        return 1

    if chapter:
        return download(chapter)

    if name:
        return project.download(name)

    print(f"There is nothing called '{wanted}'.")
    near = difflib.get_close_matches(wanted, chapters + projects, n=3, cutoff=0.6)
    if near:
        print("Did you mean: " + ", ".join(near) + "?")
    else:
        print("Run `pixi run get` on its own to see the whole list.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
