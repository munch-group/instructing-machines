"""Tell VS Code where pixi and the course Python are on this particular machine.

You do not need to run this yourself. `pixi run check` runs it on day one, and
running it again is harmless.

The problem it solves is a mismatch between two ways of starting a program. A
terminal knows where pixi is, because installing pixi put it on your PATH and
your terminal reads PATH when it starts. VS Code, started from the Dock or the
Start menu, does not: on a Mac an application launched that way never sees your
shell's PATH at all, and on Windows a VS Code that was already running when you
installed pixi is still working from the PATH it had beforehand.

The VS Code extension that finds your course Python has to run `pixi` before it
can do anything. When it cannot find it, it gives up silently, and what you see
several minutes later is "No Python found. Would you like to install uv and use
it to install Python?" -- an offer to install a second Python, because the first
one could not be located. Nothing is actually wrong with your installation.

So this writes the full path to pixi into .vscode/settings.json, where the
extension reads it. That path is right for this machine and no other, which is
why it is written here rather than shipped in the download. Afterwards it stops
mattering how you start VS Code.

It writes a second path for a related reason. Choosing the interpreter is the
pixi extension's job, and it does it well, but it cannot do it before it has
started and it cannot do it at all on a machine where it never found pixi. In
that gap the Python extension picks one on its own, and the one it picks in a
pixi folder is one it then cannot run -- which produces "An Invalid Python
interpreter is selected", a message that sounds like your installation is broken
when nothing is. Naming the course Python outright means there is a valid one
selected from the start and the message never appears. This script is run by
that very interpreter, so it does not have to guess: sys.executable is the
answer, on every platform, without a bin-versus-Scripts special case.

The file is edited as text rather than parsed and rewritten, because
settings.json is full of comments explaining what each setting is for, and
rewriting it as JSON would throw all of them away.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# The settings written, and where each value comes from. Both are
# "machine-overridable" in VS Code's scheme, which is what allows a workspace
# settings.json to carry them at all.
PIXI_SETTING = "im-pixi-vscode.pixiExecutable"
PYTHON_SETTING = "python.defaultInterpreterPath"

# Written above each setting so that whoever finds it later knows it was not
# hand-written, and that a copy of this folder on another machine needs it
# regenerated rather than copied.
COMMENTS = {
    PIXI_SETTING: """\
    // Written by `pixi run check` on this machine. The full path to pixi,
    // which the pixi extension needs before it can find the Python in .pixi.
    // Right for this computer only -- if you copy this folder to another one,
    // run `pixi run check` there to rewrite it.
""",
    PYTHON_SETTING: """\
    // Written by `pixi run check` on this machine. The course Python itself,
    // named so that until the pixi extension has chosen one, the Python
    // extension does not go looking and settle on one it cannot run -- which
    // is what produces "An Invalid Python interpreter is selected". Right for
    // this computer only, as above.
""",
}


def settings_path() -> Path | None:
    """The .vscode/settings.json belonging to the folder pixi was run in."""
    root = os.environ.get("PIXI_PROJECT_ROOT")
    if not root:
        return None
    return Path(root) / ".vscode" / "settings.json"


def pin(text: str, setting: str, path: str) -> str | None:
    """Return the settings with one path set, or None if it was already right."""
    # json.dumps does the escaping, which matters on Windows: a path like
    # C:\Users\x\.pixi\bin\pixi.exe is not valid JSON until its backslashes
    # are doubled.
    value = json.dumps(path)
    existing = re.search(rf'^([ \t]*)"{re.escape(setting)}"\s*:\s*("(?:[^"\\]|\\.)*")',
                         text, re.MULTILINE)
    if existing:
        if existing.group(2) == value:
            return None
        return text[:existing.start(2)] + value + text[existing.end(2):]

    # Not there yet. Put it directly after the opening brace, where it is
    # visible and cannot land inside another setting's block.
    opening = re.search(r"\{\s*\n", text)
    if not opening:
        return None
    return (text[:opening.end()] + COMMENTS[setting]
            + f'    "{setting}": {value},\n\n' + text[opening.end():])


def main() -> int:
    pixi_exe = os.environ.get("PIXI_EXE")
    if not pixi_exe:
        # Running outside `pixi run`. Nothing to write, and nothing broken.
        print("PIXI_EXE is not set, so there is nothing to pin "
              "(run this with `pixi run check`).")
        return 0

    path = settings_path()
    if path is None or not path.is_file():
        print(f"no .vscode/settings.json to write to ({path}), skipping")
        return 0

    wanted = {PIXI_SETTING: pixi_exe}

    # sys.executable is this environment's own interpreter, because pixi ran
    # this script with it -- no guessing at bin/python versus Scripts/python.exe.
    # But only when pixi really did: run by hand with some other python, it is
    # that other python, and writing it here would point VS Code at an
    # interpreter with none of the course packages in it. Better to write
    # nothing than to write something wrong into a student's settings.
    interpreter = Path(sys.executable).resolve()
    if interpreter.is_relative_to(path.parent.parent.resolve()):
        wanted[PYTHON_SETTING] = str(interpreter)
    else:
        print(f"not writing {PYTHON_SETTING}: this script is running on")
        print(f"    {interpreter}")
        print("which is not the environment in this folder. Use `pixi run check`.")

    text = path.read_text(encoding="utf-8")
    written = []
    for setting, value in wanted.items():
        updated = pin(text, setting, value)
        if updated is not None:
            text = updated
            written.append(f"    {setting} = {value}")

    if not written:
        print("VS Code already knows where pixi and the course Python are.")
        return 0

    path.write_text(text, encoding="utf-8")
    print("Told VS Code where things are on this machine:")
    for line in written:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
