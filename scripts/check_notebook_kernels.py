#!/usr/bin/env python3
"""Check that every notebook we publish carries neutral kernel metadata.

VS Code picks a notebook's kernel in three steps: the kernel it remembers for
that notebook, then an exact match against ``metadata.kernelspec``, and only
then the Python environment the Python extension has active for the workspace.
A student who has just unzipped the course folder misses all three — nothing is
remembered for a path they have never opened, and no environment has been
selected yet — so what is left in ``metadata.kernelspec`` is the only thing
VS Code has to go on.

That metadata is written by whichever machine last executed the notebook, which
is how three different display names ended up in the book at once, two of them
naming a Python version the environment no longer installs::

    "instructing-machines:default (3.13.14)"   # a name only Kasper's machine has
    "Python 3 (ipykernel)"                     # whatever ipykernel called itself
    "Python 3"                                 # what we actually want

A name that matches nothing is not merely useless. VS Code shows it in the
picker as the kernel the notebook "wants", so a student goes looking for an
entry that does not exist on their machine.

The course deliberately registers no kernel of its own — ``pixi.toml`` promises
that nothing is installed outside the course folder, and a named kernelspec
would have to live in the user's Jupyter directory to be found. So the aim here
is not to make a notebook name the course environment. It is the opposite: keep
the metadata neutral and honest, so VS Code offers its own recommendation
instead of chasing a name that cannot resolve, and the student picks the
``.pixi`` entry once. ``language_info.version`` goes for the same reason — a
pinned patch version drifts the moment the environment is rebuilt, and it is a
hint VS Code can weigh against a perfectly good environment.

Run it read-only, which is what CI does::

    python3 scripts/check_notebook_kernels.py

Exit status is 0 when every notebook is already neutral, 1 when any of them
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

# What every published notebook should say. `python3` is the name ipykernel
# gives its own kernelspec, so it is what the course environment exposes too —
# but it is also what every other Python environment on the machine exposes,
# which is the point: it is a neutral hint, not a claim to a specific
# environment, and VS Code is left to recommend rather than mis-match.
CANONICAL_KERNELSPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
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
        print(f"{len(paths)} notebook(s) checked, all with neutral kernel metadata.")
        return 0

    if args.fix:
        print(f"\n{drifted} of {len(paths)} notebook(s) normalized.")
        return 0

    print(f"\n{drifted} of {len(paths)} notebook(s) carry kernel metadata that names\n"
          "a kernel a student's machine will not have. Fix them with:\n"
          "    python3 scripts/check_notebook_kernels.py --fix",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
