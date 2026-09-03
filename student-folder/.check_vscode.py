"""Say whether VS Code has what this folder asks of it.

You run this one yourself, once, at the end of the VS Code section of the
Getting Started chapter: `pixi run check-vscode`. Running it again is harmless,
and worth doing whenever the editor starts behaving as if it cannot find the
course environment.

It is a separate script from .check_env.py beside it, and the reason is when
each of them can answer. `pixi run check` is the last of the terminal steps,
which come before VS Code has even been downloaded. What it can say there is
whether the environment installed, and whether this folder has the notebook
kernel and the two paths VS Code will read when it opens the folder. What it
cannot say is anything about extensions, because at that point there is no
editor to have any. This one runs after the editor's own setup, when there is.

Splitting them that way rather than having one script work out which of the two
moments it is in also means neither has to guess. A check that decides what to
report by looking at whether VS Code happens to be installed is a check that
says nothing on the machine of a student who installed VS Code last year, and
that is the student most likely to be in trouble.

Which extensions it looks for is read out of .vscode/extensions.json beside it
rather than written down here, the same way .check_env.py reads the packages out
of pixi.toml. The list the course publishes and the list this reports on are
then the same list, and adding one is a single edit in the file that had to
change anyway.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# The file VS Code reads when it offers to install extensions for a folder, and
# the same file as it stands in the book's own repository, where this directory
# is not dotted and only becomes .vscode in the download. The undotted one is
# read as a fallback so that this script can be tried out where it is written.
EXTENSIONS_FILE = (".vscode", "extensions.json")
AUTHORING_EXTENSIONS = ("vscode", "extensions.json")

# Only the recommendations. The same file carries unwantedRecommendations,
# which is a list of extensions to keep out, and taking those for things to
# install would be exactly backwards. Comments come out first, because the ones
# in that file quote extension and setting names, and a name quoted inside a
# comment is not a recommendation.
RECOMMENDATIONS = re.compile(r'"recommendations"\s*:\s*\[(.*?)]', re.DOTALL)
QUOTED = re.compile(r'"([^"]+)"')
COMMENT = re.compile(r"//[^\n]*")

# Where VS Code keeps its command-line tool when it is not on PATH. On a Mac it
# is on PATH only for someone who ran "Shell Command: Install 'code' command in
# PATH" from the palette, which the chapter does ask for -- but a student who
# missed that step has a working VS Code all the same, and this should find it
# rather than tell them it is not installed.
APPLICATIONS = (
    "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",
    str(Path.home() / "Applications/Visual Studio Code.app"
        "/Contents/Resources/app/bin/code"),
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd"),
    os.path.expandvars(r"%PROGRAMFILES%\Microsoft VS Code\bin\code.cmd"),
)


def course_folder() -> Path:
    """The folder this script belongs to, which is the folder pixi was run in."""
    root = os.environ.get("PIXI_PROJECT_ROOT")
    return Path(root) if root else Path(__file__).resolve().parent


def code_command() -> str | None:
    """VS Code's command-line tool, wherever this machine keeps it."""
    on_path = shutil.which("code")
    if on_path:
        return on_path
    for candidate in APPLICATIONS:
        if Path(candidate).is_file():
            return candidate
    return None


def recommended(folder: Path) -> list[str]:
    """The extensions this folder asks VS Code to install."""
    for parts in (EXTENSIONS_FILE, AUTHORING_EXTENSIONS):
        try:
            text = folder.joinpath(*parts).read_text(encoding="utf-8")
            break
        except OSError:
            continue
    else:
        return []
    listed = RECOMMENDATIONS.search(COMMENT.sub("", text))
    return QUOTED.findall(listed.group(1)) if listed else []


def versions(command: str) -> dict[str, str] | None:
    """Every extension VS Code has, by name, with the version it is at."""
    try:
        listed = subprocess.run(
            [command, "--list-extensions", "--show-versions"], capture_output=True,
            text=True, timeout=60,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if listed.returncode != 0:
        return None

    found = {}
    for line in listed.stdout.splitlines():
        name, _, version = line.strip().partition("@")
        if name:
            found[name.lower()] = version
    return found


def main() -> int:
    folder = course_folder()

    command = code_command()
    if command is None:
        print("VS Code was not found on this machine.")
        print("")
        print("This is the check for the step after installing it, so if you have")
        print("not done the VS Code section of the Getting Started chapter yet, do")
        print("that first and then run this again.")
        return 1

    wanted = recommended(folder)
    if not wanted:
        print(f"There is no {'/'.join(EXTENSIONS_FILE)} in {folder},")
        print("or it names no extensions, so there is nothing to check VS Code")
        print("against. Run `im update` to fetch the course's current copy of it.")
        return 1

    have = versions(command)
    if have is None:
        print(f"VS Code is installed ({command}), but it would not say which")
        print("extensions it has, so this cannot tell you. Try again, and if it")
        print("keeps happening, bring this message to class.")
        return 1

    here = [f"{name} {have[name.lower()]}".strip() for name in wanted
            if name.lower() in have]
    absent = [name for name in wanted if name.lower() not in have]

    if not absent:
        print("VS Code has what this folder asks for:")
        print("")
        for name in here:
            print(f"    {name}")
        return 0

    print("VS Code does not have what this folder asks for:")
    print("")
    for name in absent:
        print(f"    {name}")
    print("")
    print("Open your instructing-machines folder in VS Code with File -> Open")
    print("Folder, then the Extensions panel on the left (the icon with four")
    print("squares), search '@recommended' and install what it lists. Then run")
    print("this again.")
    if here:
        print("")
        print("It does have:")
        for name in here:
            print(f"    {name}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
