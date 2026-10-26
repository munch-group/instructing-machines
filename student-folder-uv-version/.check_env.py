"""Say whether this folder's Python environment has everything the course needs.

You do not need to run this yourself. `pixi run check` runs it on day one and
whenever you want to know that things are still in order, and running it again
is harmless: it only reads.

What it checks is read out of pixi.toml beside it rather than written down here,
so the environment the course asks for and the environment this reports on are
the same list by construction. Adding a package to the course means adding it to
pixi.toml, which is where it had to go anyway, and nothing else has to be told.

This lives in the course folder rather than in the `im` command, and the reason
is the day it matters. `pixi run check` is the first thing a student types after
`pixi install`, and what it has to answer is "did that install work". A check
that arrives as part of the environment cannot answer that: when the install
went wrong, the check went wrong with it, and what a student gets instead of a
list of what is missing is `im: command not found`. This file needs nothing but
a Python to run on, so it still speaks on the morning it is needed most. `im
update` keeps it current the same way it keeps pixi.toml current, so a fix to it
still reaches everyone without anybody downloading anything by hand.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

# Packages whose import name is not simply their manifest name with the dashes
# turned into underscores. There is only one today, and a new one announces
# itself by being reported missing on an environment that plainly has it.
IMPORT_NAMES = {"biopython": "Bio"}

# The manifest sections that name something this environment should contain.
# Matched exactly, so `[target.win-64.dependencies]` is passed over rather than
# insisted on: a package another platform needs is not missing from this one.
PACKAGE_SECTIONS = ("dependencies", "pypi-dependencies")

SECTION = re.compile(r"^\[([^]]+)]")
ENTRY = re.compile(r"^([A-Za-z0-9._-]+)\s*=")

# Where an environment keeps the programs it installed. Not everything in the
# manifest is importable -- `quarto` is a command-line tool and `python` is the
# interpreter itself -- so a name that does not import is looked for here before
# it is called missing.
#
# Unix keeps all of them in bin. Windows spreads them over three places, and the
# prefix root is one of them: python.exe sits there, while pip and jupyter go to
# Scripts and anything a conda package built around a C library goes to
# Library\bin. Leaving the root out is what made the Windows CI job report
# `python` missing from an environment that had just run ipykernel with it.
BIN_DIRS = (".", "bin", "Scripts", "Library/bin")

# What the tasks before this one write, and that this reads back.
#
# `pixi run check` installs a notebook kernel and writes two paths into
# .vscode/settings.json before it reaches this file, in tasks that run one
# after another and stop at the first one to fail. Nothing announces that: a
# chain that stops early simply ends. So the command that answers "did the
# install work" reads back the rest of its own work too, rather than leaving a
# student to find out weeks later that VS Code cannot see the environment.
#
# This is as far as it can see. Whether VS Code itself has the extensions the
# folder asks for is .check_vscode.py's question, and it is a separate script
# because it is a question for a separate moment: this one runs at the end of
# the terminal steps, before the chapter has asked anybody to install an editor.
KERNEL_NAME = "instructing-machines"
KERNEL_SPEC = ("share", "jupyter", "kernels", KERNEL_NAME, "kernel.json")
SETTINGS = (".vscode", "settings.json")

# The same file as it stands in the book's own repository, where it is not
# dotted and only becomes .vscode in the download. The paths are never written
# there, so its absence is not a fault worth reporting on every run.
AUTHORING_SETTINGS = ("vscode", "settings.json")

# Written by .pin_pixi_path.py, and absolute paths, which is why they are
# written on the machine instead of published with the folder.
PINNED = ("im-pixi-vscode.pixiExecutable", "python.defaultInterpreterPath")

# Looked for by matching the line rather than by parsing, because settings.json
# is JSON with comments in it and the comments are the point: each setting there
# carries the paragraph saying why it is there.
PINNED_LINE = r'^[ \t]*"{}"[ \t]*:[ \t]*"'


def course_folder() -> Path:
    """The folder this script belongs to, which is the folder pixi was run in."""
    root = os.environ.get("PIXI_PROJECT_ROOT")
    return Path(root) if root else Path(__file__).resolve().parent


def packages(text: str) -> list[str]:
    """The packages a pixi.toml asks for, in the order it asks for them.

    Read line by line rather than parsed as TOML. The parser for that arrived in
    Python 3.11, and the whole point of this file is that it runs on whatever
    Python it is handed and still says something useful. What it is reading is a
    manifest the course publishes itself, where a dependency is one line and its
    name is whatever stands before the first `=`, so the cheap way of reading it
    is also an accurate one.
    """
    found: list[str] = []
    section = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        heading = SECTION.match(line)
        if heading:
            section = heading.group(1).strip()
            continue
        entry = ENTRY.match(line)
        if section in PACKAGE_SECTIONS and entry:
            found.append(entry.group(1))
    return list(dict.fromkeys(found))


def commands(prefix: Path) -> str:
    """The places in this environment where a program would have been put."""
    return os.pathsep.join(str(prefix / name) for name in BIN_DIRS)


def present(name: str, prefix: Path) -> bool:
    """Whether this environment has that package, as a module or as a program."""
    module = IMPORT_NAMES.get(name, name.replace("-", "_"))
    try:
        __import__(module)
        return True
    except Exception:
        # Not only ImportError. A package that raises something else while
        # importing is one a student cannot use either, and saying it is
        # missing is nearer the truth than letting the exception through and
        # reporting nothing at all about the rest of the list.
        pass
    return shutil.which(name, path=commands(prefix)) is not None


def editor_problems(folder: Path, prefix: Path) -> list[str] | None:
    """What VS Code still needs from this folder, or None when it was not asked.

    None is the book's own copy of this folder, where the paths are never
    written and there is nothing here to be wrong. It is not an empty list,
    because an empty list is a claim that everything was looked at and found in
    order, and nothing was looked at.
    """
    settings = folder.joinpath(*SETTINGS)
    if not settings.is_file() and folder.joinpath(*AUTHORING_SETTINGS).is_file():
        return None

    problems = []
    if not prefix.joinpath(*KERNEL_SPEC).is_file():
        problems.append(f"the {KERNEL_NAME} notebook kernel is not installed")

    if not settings.is_file():
        problems.append(f"there is no {'/'.join(SETTINGS)} for VS Code to read")
        return problems

    try:
        text = settings.read_text(encoding="utf-8")
    except OSError as error:
        problems.append(f"{'/'.join(SETTINGS)} could not be read ({error})")
        return problems

    for name in PINNED:
        if not re.search(PINNED_LINE.format(re.escape(name)), text, re.MULTILINE):
            problems.append(f"{name} has not been written into {'/'.join(SETTINGS)}")
    return problems


def main() -> int:
    folder = course_folder()
    manifest = folder / "pixi.toml"
    if not manifest.is_file():
        print(f"There is no pixi.toml next to this script ({manifest}),")
        print("so there is nothing to check it against.")
        return 1

    # This can only report on the Python it is itself running on, so it has to
    # be the folder's own. Run by hand with some other python -- one from the
    # system, or from a conda environment that activates itself -- it would
    # report the course's packages missing from an environment that has all of
    # them, which is a worse answer than admitting it cannot tell.
    prefix = Path(sys.prefix).resolve()
    if not prefix.is_relative_to((folder / ".pixi").resolve()):
        print("This is not the course environment:")
        print(f"    {sys.executable}")
        print("")
        print("So there is nothing here to say about the packages the course")
        print("needs. From your course folder, ask pixi to run it instead:")
        print("")
        print("    pixi run check")
        return 1

    wanted = packages(manifest.read_text(encoding="utf-8"))
    if not wanted:
        print(f"{manifest} does not ask for any packages, which cannot be right.")
        print("Run `im update` to fetch the course's current copy of it.")
        return 1

    missing = [name for name in wanted if not present(name, prefix)]
    problems = editor_problems(folder, prefix)

    if missing:
        print("Your environment is missing:")
        print("")
        for name in missing:
            print(f"    {name}")
        print("")
        print("Run `im update` to refresh the environment. If that does not fix it,")
        print("bring this message to class.")
    else:
        print(f"Everything is installed. Python {sys.version.split()[0]}")

    if problems:
        print("")
        print("This folder is not ready for VS Code yet:")
        print("")
        for problem in problems:
            print(f"    {problem}")
        print("")
        print("These are written by the tasks that run just before this one, and a")
        print("task that fails stops the ones after it. Run `pixi run check` again")
        print("and read what it prints on the way past.")
    elif problems is not None and not missing:
        print("This folder has the notebook kernel and both of the paths VS Code")
        print("will read when it opens the folder.")

    return 1 if missing or problems else 0


if __name__ == "__main__":
    sys.exit(main())
