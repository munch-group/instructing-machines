#!/usr/bin/env python3
"""Check that every notebook we publish names the course kernel.

VS Code picks a notebook's kernel in three steps: the kernel it remembers for
that notebook, then a match against ``metadata.kernelspec``, and only then the
Python environment the Python extension has active for the workspace. A student
who has just unzipped the course folder misses the first and the third —
nothing is remembered for a path they have never opened, and no environment has
been selected there yet — which leaves the kernelspec written in the file as
the only thing VS Code has to go on.

Left alone, that metadata says whatever the machine that last executed the
notebook called its kernel. The book had three names in it at once, two of them
naming a Python version the environment no longer installs::

    "instructing-machines:default (3.13.14)"   # a name only one machine ever had
    "Python 3 (ipykernel)"                     # what ipykernel calls itself
    "Python 3"                                 # neutral, and matches nothing in particular

None of the three helps. The first two name kernels a student does not have.
The third is what every Python on the machine is called, so VS Code cannot tell
the course environment from the system Python, and offers "+ Create Python
Environment" as its recommendation while the environment the student installed
half an hour ago sits further down the list.

So the notebooks name the kernel the course registers for itself:
``instructing-machines``, written into the environment prefix by the ``kernel``
task in ``student-folder/pixi.toml``, which ``pixi run check`` runs on day one.
That kernelspec lives inside ``.pixi``, so it goes away with the folder and
breaks no promise about installing things elsewhere, and having a name of its
own makes it both findable in the picker and matchable from the file.

One consequence to know about: a student who never ran ``pixi run check`` has
no kernel by that name, and VS Code says so rather than quietly picking
something else. That is the trade worth making. A student in that state has no
working environment either way, and a named miss is easier to diagnose than a
notebook running silently on the wrong Python.

``language_info.version`` is stripped for a related reason — nbconvert stamps
the running interpreter's patch version into every notebook it executes, so it
drifts the moment the environment is rebuilt, and it is one more hint VS Code
can weigh against a perfectly good environment.

Run it read-only, which is what CI does::

    python3 scripts/check_notebook_kernels.py

Exit status is 0 when every notebook already names it, 1 when any of them
drifted. To rewrite them in place::

    python3 scripts/check_notebook_kernels.py --fix

``--fix`` needs nbformat (so run it inside the course environment, or with
``pixi run``); the read-only check is plain stdlib so it can run on a bare
runner with no environment installed.

The file list is the book's own chapter list plus the two notebooks that ship
pre-placed inside the download, both read from the modules that already own
them, so a notebook added to the book or to the zip is covered here without
anyone remembering to update a list.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quarto_profile import quarto_config  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"

# What every published notebook should say. This has to match the --name and
# --display-name of the `kernel` task in student-folder/pixi.toml exactly: that
# task is what puts a kernelspec by this name inside the student's environment,
# and this is what points a notebook at it.
CANONICAL_KERNELSPEC = {
    "display_name": "Instructing Machines",
    "language": "python",
    "name": "instructing-machines",
}

# Dropped from language_info wherever it appears. nbconvert stamps the running
# interpreter's version on every execute, so this drifts on its own every time
# the environment is rebuilt.
DRIFTING_LANGUAGE_INFO_KEYS = ("version",)

# Matches `    - python/iteration.ipynb`, skipping the `- "!python/..."`
# exclusions in the render list. Kept in step with the same pattern in
# build_student_folder.py.
CHAPTER_LINE = re.compile(r'^\s*-\s+"?(?!!)([A-Za-z0-9_./-]+\.ipynb)"?\s*$')


def published_notebooks() -> list[Path]:
    """Every notebook a student can end up holding, in render order.

    That is the book's chapters (each published loose for `im get`) plus the
    week-one pair that ships inside the zip. The second list is imported from
    build_student_folder rather than repeated, so the two cannot disagree about
    what is in the download.
    """
    from build_student_folder import WEEK1_NOTEBOOKS

    config = quarto_config(DOCS)
    paths = []
    for line in config.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("#"):
            continue
        match = CHAPTER_LINE.match(line)
        if match:
            paths.append(DOCS / match.group(1))

    for extra in WEEK1_NOTEBOOKS:
        if extra not in paths:
            paths.append(extra)

    return [p for p in paths if p.exists()]


def drift(notebook: dict) -> list[str]:
    """Return a description of everything wrong with this notebook's metadata."""
    problems = []
    metadata = notebook.get("metadata", {})

    kernelspec = metadata.get("kernelspec")
    if kernelspec != CANONICAL_KERNELSPEC:
        if kernelspec is None:
            problems.append("no kernelspec at all")
        else:
            name = kernelspec.get("display_name", "?")
            problems.append(f'kernelspec display_name is "{name}"')

    language_info = metadata.get("language_info", {})
    for key in DRIFTING_LANGUAGE_INFO_KEYS:
        if key in language_info:
            problems.append(f"language_info.{key} is pinned to {language_info[key]}")

    return problems


def normalize(notebook) -> bool:
    """Rewrite this notebook's kernel metadata in place. True if anything moved.

    Takes a plain dict or an nbformat NotebookNode — NotebookNode is a dict
    subclass, so clean_notebooks.py can hand its parsed notebook straight in
    rather than parsing the file a second time.
    """
    changed = False
    metadata = notebook.setdefault("metadata", {})

    if metadata.get("kernelspec") != CANONICAL_KERNELSPEC:
        metadata["kernelspec"] = dict(CANONICAL_KERNELSPEC)
        changed = True

    language_info = metadata.get("language_info")
    if isinstance(language_info, dict):
        for key in DRIFTING_LANGUAGE_INFO_KEYS:
            if language_info.pop(key, None) is not None:
                changed = True

    return changed


def fix(path: Path) -> bool:
    """Normalize one notebook on disk, writing it back in nbformat's own style."""
    import nbformat

    notebook = nbformat.read(path, as_version=4)
    if not normalize(notebook):
        return False
    nbformat.write(notebook, path)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true",
                        help="rewrite the drifted notebooks instead of reporting them")
    args = parser.parse_args()

    paths = published_notebooks()
    if not paths:
        print("error: found no notebooks to check", file=sys.stderr)
        return 1

    drifted = 0
    for path in paths:
        relative = path.relative_to(REPO)
        problems = drift(json.loads(path.read_text(encoding="utf-8")))
        if not problems:
            continue
        drifted += 1
        if args.fix:
            fix(path)
            print(f"fixed: {relative} ({'; '.join(problems)})")
        else:
            print(f"{relative}: {'; '.join(problems)}", file=sys.stderr)

    if not drifted:
        print(f"{len(paths)} notebook(s) checked, all naming the course kernel.")
        return 0

    if args.fix:
        print(f"\n{drifted} of {len(paths)} notebook(s) normalized.")
        return 0

    print(f"\n{drifted} of {len(paths)} notebook(s) do not name the course kernel,\n"
          "so VS Code will not suggest it when a student opens them. Fix with:\n"
          "    python3 scripts/check_notebook_kernels.py --fix",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
