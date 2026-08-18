"""The project half of `pixi run get`.

    pixi run get alignmentproject

You never run this file yourself; get.py runs it. It knows which projects the
course website is offering, and how to unpack one into `projects/` here without
ever writing over work you have already done.

A project arrives as a folder holding the file you write your code in, the test
program that checks it, and any data the project reads. They arrive one at a
time, in the week each one is set.
"""

from __future__ import annotations

import io
import urllib.error
import zipfile
from pathlib import Path

from course import HERE, fetch, fetch_bytes, url_for

INDEX = "project-files/index.txt"
FOLDER = "projects"


def available() -> list[str]:
    """The project names the website is offering, one per line."""
    return [line.strip() for line in fetch(INDEX).splitlines() if line.strip()]


def normalise(name: str) -> str:
    """Fold away the differences nobody should have to remember.

    So `alignment`, `alignmentproject`, `alignment-project` and
    `alignment_project` all mean the same project.
    """
    name = name.strip().lower()
    if name.endswith(".zip"):
        name = name[: -len(".zip")]
    name = name.replace("-", "_").replace(" ", "_")
    for tail in ("_project", "project"):
        if name.endswith(tail) and len(name) > len(tail):
            return name[: -len(tail)]
    return name


def resolve(wanted: str, projects: list[str]) -> str | None:
    return {normalise(p): p for p in projects}.get(normalise(wanted))


def safe_members(archive: zipfile.ZipFile, name: str) -> list[str] | None:
    """Every member of the zip, checked to live inside a folder called `name`.

    A zip can name its files anything at all, including `../../somewhere-else`,
    and unpacking one without looking writes wherever it says. Nothing that
    comes off the website should be able to put a file outside `projects/`.
    """
    members = []
    root = Path(name)
    for member in archive.namelist():
        if member.endswith("/"):
            continue
        path = Path(member)
        if path.is_absolute() or ".." in path.parts:
            return None
        if path.parts[:1] != root.parts:
            return None
        members.append(member)
    return members or None


def download(name: str) -> int:
    """Fetch project `name` into projects/ here, unless it is already there."""
    # A project is a folder you work in for a week, not a file you can be
    # handed a second copy of. If it is already here, stop: unpacking over it
    # would put the empty starting file back on top of your own code.
    destination = HERE / FOLDER / name
    if destination.exists():
        print(f"You already have {FOLDER}/{name}, so I have left it alone.")
        print("")
        print("If you want to start that project over from scratch, rename or")
        print(f"move your {FOLDER}/{name} folder first, then ask again.")
        return 1

    print(f"Fetching {url_for(f'project-files/{name}.zip')}")
    try:
        data = fetch_bytes(f"project-files/{name}.zip")
    except urllib.error.URLError as error:
        print(f"\nCould not download it: {error}")
        print("Nothing has been changed.")
        return 1

    # Every zip in the world starts with these four bytes. If these are not
    # them, what came back is a "page not found" page wearing a zip's name.
    if not data.startswith(b"PK\x03\x04"):
        print("\nWhat came back does not look like a project.")
        print("Nothing has been changed. Please tell your instructor.")
        return 1

    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
        members = safe_members(archive, name)
    except zipfile.BadZipFile:
        members = None

    if members is None:
        print("\nThat project download is damaged, or it is not laid out as")
        print("expected. Nothing has been changed. Please tell your instructor.")
        return 1

    target = HERE / FOLDER
    target.mkdir(exist_ok=True)
    archive.extractall(target, members=members)

    print(f"\nSaved {FOLDER}/{name} ({len(members)} files).")
    print(f"Open the folder in VS Code and start with {name}.py.")
    return 0
