#!/usr/bin/env python3
"""Assemble the downloadable student course folder and zip it into the book.

The zip that students download is built from four places:

    student-folder/     the hand-maintained template (pixi.toml, .vscode, ...)
    docs/python/data/   data files the lecture notes read
    project-files/      the programming projects
    docs/intro/         the two week-one notebooks, which ship pre-placed

Run it by hand from anywhere:

    python3 scripts/build_student_folder.py

It also runs automatically from Quarto's `post-render`, so the zip on the
website can never drift from the book that describes it. The zip, loose copies
of pixi.toml and pixi.lock (which `update.py` fetches), and every chapter
notebook (which `get.py` fetches) are written into the rendered book so they
are published as part of the site:

    docs/_book/instructing-machines.zip
    docs/_book/pixi.toml
    docs/_book/pixi.lock
    docs/_book/notebooks/*.ipynb
    docs/_book/notebooks/index.txt
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from fnmatch import fnmatch
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# The name students see once they unzip. Also the VS Code window title, so
# keep it recognisable and free of spaces.
FOLDER_NAME = "instructing-machines"

TEMPLATE = REPO / "student-folder"
DEFAULT_OUT = REPO / "docs" / "_book"

# (source directory, destination inside the student folder)
#
# The vscode -> .vscode rename is deliberate. Kept undotted in the repository,
# the template is visible in a file listing and cannot be mistaken for settings
# that apply to this repository itself; it becomes .vscode only in the folder
# students actually open.
EXTRA_TREES = [
    (TEMPLATE / "vscode", ".vscode"),
    (REPO / "docs" / "python" / "data", "data"),
    (REPO / "project-files", "projects"),
]

# Copied by EXTRA_TREES under a different name, so skip it in the plain pass.
TEMPLATE_SKIP = {"vscode"}

# The one exception to "download notebooks as you go". These ship inside
# the folder so that day one tests one thing only — whether the environment
# works. Students meet the downloading ritual in week two, when a failure can
# only mean one thing. The log book is here for the same reason: course-
# introduction.qmd has students write their first entry on day one, before
# the download ritual exists for them yet.
WEEK1_DESTINATION = "week1"
WEEK1_NOTEBOOKS = [
    REPO / "docs" / "intro" / "notebooks.ipynb",
    REPO / "docs" / "ai" / "log-book.ipynb",
]

# Every chapter notebook is published loose next to the zip so that
# `pixi run get <chapter>` has something to fetch. The list comes from the
# book's own chapter list, so it cannot drift from what the website offers.
QUARTO_CONFIG = REPO / "docs" / "_quarto.yml"
NOTEBOOK_DIR = "notebooks"

# Matches `    - python/iteration.ipynb` but not a commented-out chapter and
# not the `- "!python/snippet-cast.ipynb"` exclusions in the render list.
CHAPTER_LINE = re.compile(r'^\s*-\s+"?(?!!)([A-Za-z0-9_./-]+\.ipynb)"?\s*$')

# Never ship these. Directory names are matched exactly; file patterns are
# globs. Solution walkthroughs are held back deliberately — the encrypted
# solution files are meant to travel with the projects, the walkthroughs are
# not.
EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".ipynb_checkpoints", ".pixi", ".git"}
EXCLUDE_FILES = [
    "*.pyc",
    ".DS_Store",
    "*_solution.py",
    "solution_walkthrough.ipynb",
]

# Files copied loose into the site root as well as into the zip, because
# update.py downloads them individually.
PUBLISH_LOOSE = ["pixi.toml", "pixi.lock"]

# A fixed timestamp keeps the zip byte-identical between runs when nothing has
# changed, so republishing the site does not churn.
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def excluded_file(name: str) -> bool:
    return any(fnmatch(name, pattern) for pattern in EXCLUDE_FILES)


def copy_tree(source: Path, destination: Path, prune: set[str] | None = None) -> int:
    """Copy source into destination, honouring the exclusions. Returns a count."""
    copied = 0
    skip_dirs = EXCLUDE_DIRS | (prune or set())
    for dirpath, dirnames, filenames in os.walk(source):
        # Pruning dirnames in place stops os.walk descending into them at all.
        dirnames[:] = sorted(d for d in dirnames if d not in skip_dirs)
        here = Path(dirpath)
        relative = here.relative_to(source)
        for filename in sorted(filenames):
            if excluded_file(filename):
                continue
            target = destination / relative / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(here / filename, target)
            copied += 1
    return copied


def chapter_notebooks() -> list[Path]:
    """Every .ipynb listed as a chapter in the book, in book order."""
    if not QUARTO_CONFIG.exists():
        return []
    found: list[Path] = []
    seen: set[Path] = set()
    for line in QUARTO_CONFIG.read_text(encoding="utf-8").splitlines():
        match = CHAPTER_LINE.match(line)
        if not match:
            continue
        path = (QUARTO_CONFIG.parent / match.group(1)).resolve()
        if path.is_file() and path not in seen:
            seen.add(path)
            found.append(path)
    return found


def publish_notebooks(out_dir: Path) -> int:
    """Copy the chapter notebooks into out_dir/notebooks/ with a manifest."""
    notebooks = chapter_notebooks()
    if not notebooks:
        print(
            f"warning: found no chapter notebooks in {QUARTO_CONFIG}, so\n"
            "         `pixi run get` will have nothing to fetch",
            file=sys.stderr,
        )
        return 0

    target = out_dir / NOTEBOOK_DIR
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    # Students name a chapter by its stem, so two chapters sharing one stem
    # would be indistinguishable from the command line.
    by_stem: dict[str, Path] = {}
    for notebook in notebooks:
        if notebook.stem in by_stem:
            print(
                f"warning: two chapters are both called {notebook.stem}\n"
                f"         ({by_stem[notebook.stem]} and {notebook});\n"
                f"         `pixi run get {notebook.stem}` can only offer the first",
                file=sys.stderr,
            )
            continue
        by_stem[notebook.stem] = notebook
        shutil.copy2(notebook, target / notebook.name)

    (target / "index.txt").write_text(
        "\n".join(sorted(by_stem)) + "\n", encoding="utf-8"
    )
    return len(by_stem)


def build(out_dir: Path) -> int:
    if not TEMPLATE.is_dir():
        print(f"error: no template at {TEMPLATE}", file=sys.stderr)
        return 1

    # Staging happens in a temporary directory rather than inside the
    # repository: nothing to gitignore, and no half-built folder left behind to
    # confuse the next run.
    with tempfile.TemporaryDirectory(prefix="student-folder-") as staging_name:
        return assemble(Path(staging_name), out_dir)


def assemble(staging: Path, out_dir: Path) -> int:
    folder = staging / FOLDER_NAME
    folder.mkdir(parents=True)

    total = copy_tree(TEMPLATE, folder, prune=TEMPLATE_SKIP)

    for source, destination in EXTRA_TREES:
        if not source.is_dir():
            print(f"warning: {source} does not exist, skipping", file=sys.stderr)
            continue
        total += copy_tree(source, folder / destination)

    week1 = folder / WEEK1_DESTINATION
    for notebook in WEEK1_NOTEBOOKS:
        if not notebook.is_file():
            print(f"warning: {notebook} does not exist, skipping", file=sys.stderr)
            continue
        week1.mkdir(parents=True, exist_ok=True)
        shutil.copy2(notebook, week1 / notebook.name)
        total += 1

    lock = folder / "pixi.lock"
    if not lock.exists():
        print(
            "warning: student-folder/pixi.lock is missing, so students will each\n"
            "         solve the environment themselves (slow, and they may not all\n"
            "         get the same versions). Generate it with:\n"
            "             pixi lock --manifest-path student-folder/pixi.toml",
            file=sys.stderr,
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{FOLDER_NAME}.zip"

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(folder.rglob("*")):
            if item.is_dir():
                continue
            arcname = item.relative_to(staging).as_posix()
            info = zipfile.ZipInfo(arcname, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, item.read_bytes())

    for name in PUBLISH_LOOSE:
        source = folder / name
        if source.exists():
            shutil.copy2(source, out_dir / name)

    published = publish_notebooks(out_dir)

    size = archive.stat().st_size / 1024
    print(f"Built {archive} ({total} files, {size:.0f} kB)")
    print(f"Published {published} chapter notebooks to {out_dir / NOTEBOOK_DIR}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"where to write the zip (default: {DEFAULT_OUT})",
    )
    args = parser.parse_args()
    return build(args.out.resolve())


if __name__ == "__main__":
    sys.exit(main())
