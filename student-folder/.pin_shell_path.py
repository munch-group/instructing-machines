"""Tell your terminal where pixi is, whichever shell it opens with.

You do not need to run this yourself. `pixi run check` runs it, and running it
again is harmless.

The problem it solves is that a Mac has two shells and they do not read the same
files. Terminal opens zsh, which reads ~/.zshrc when it starts. Anything you
started from an older tutorial, from VS Code with a changed setting, or from a
`bash` you typed yourself, reads ~/.bash_profile instead. Neither shell has ever
heard of the other's file.

The pixi installer writes one line into one of them -- whichever shell it
happened to be run from -- and that is the whole of what puts pixi on your PATH.
Run the installer from the wrong shell and you get a machine where pixi works
perfectly in the window you installed it from and does not exist in the next one
you open. What you see is `pixi: command not found` in a terminal that worked
yesterday, which reads like a broken installation and is not one: the program is
there, on the disk, where it has always been, and this particular window has
simply never been told.

So this looks at where pixi actually is, works out which shells you have, and
writes the line into the startup file each of them really reads -- including the
one the installer missed. It writes nothing if the line is already there, and
nothing at all if pixi came from somewhere other than its own installer (from
Homebrew, say), because then the line would point at a folder that does not
exist and the problem is not this one.

Windows keeps its PATH somewhere else entirely, in the registry rather than in a
startup file, so there is nothing here for it to do.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Where the pixi installer puts pixi, written the way a startup file writes it.
# Anywhere else and the line below would point at nothing: a pixi from Homebrew
# or from a package manager is already on PATH by some other means, and adding
# this would neither help nor be true.
INSTALLER_BIN = ".pixi/bin"

# What each shell reads when it starts, best file first.
#
# The bash order is macOS's, and it is the trap this whole script exists next
# to: macOS opens bash as a *login* shell, which reads .bash_profile and stops
# without ever looking at .bashrc. Everywhere else it is the other way round.
# Getting it wrong writes a correct line into a file the shell never opens,
# which looks exactly like having done nothing at all.
STARTUP_FILES = {
    "zsh": (".zshrc", ".zprofile", ".zshenv"),
    "bash": (".bash_profile", ".bashrc", ".profile"),
    "fish": (".config/fish/config.fish",),
}
LINUX_BASH = (".bashrc", ".bash_profile", ".profile")

# The two this is about. A student who has both -- and on a Mac that is most of
# them, because plenty of software drops a .bash_profile in passing -- should be
# able to open either and find pixi, so both get the line rather than only the
# one they happen to be using today.
BOTH = ("zsh", "bash")

# Written above the line so that whoever finds it later knows where it came from
# and that deleting it is allowed.
MARKER = "# Added for the Instructing Machines course by `pixi run check`."


def shell_named(value: str | None) -> str:
    """A shell's name out of a path or a process name, however it was written.

    A login shell lists itself as -zsh and $SHELL is usually a whole path, so
    neither arrives as the bare word this needs to look anything up by.
    """
    return Path((value or "").strip().lstrip("-")).name.lower()


def login_shell() -> str:
    """The shell a new terminal window will start.

    $SHELL is the right question here, and it is a different one from "what am I
    running inside". This script is called by pixi, so the shell around it is
    pixi's business; what matters is the shell the student will meet tomorrow
    when they open Terminal, and that is the login shell.
    """
    found = shell_named(os.environ.get("SHELL"))
    if found in STARTUP_FILES:
        return found
    return "zsh" if sys.platform == "darwin" else "bash"


def startup_files(shell: str, home: Path) -> list[Path]:
    """The files that shell reads when it starts, the one to write to first."""
    names = STARTUP_FILES.get(shell, ())
    if shell == "bash" and sys.platform != "darwin":
        names = LINUX_BASH
    base = home
    if shell == "zsh" and os.environ.get("ZDOTDIR"):
        base = Path(os.environ["ZDOTDIR"]).expanduser()
    return [base.joinpath(*name.split("/")) for name in names]


def path_line(shell: str) -> str:
    """The line that puts pixi on PATH, written the way that shell writes it."""
    if shell == "fish":
        return 'fish_add_path "$HOME/.pixi/bin"'
    return 'export PATH="$HOME/.pixi/bin:$PATH"'


def already_on_path(files: list[Path]) -> Path | None:
    """The first of those files that puts pixi's own folder on PATH, if any does.

    Looked for by the folder rather than by the whole line, so that a line the
    installer wrote, or one a student typed themselves in some other form,
    counts as done and is not doubled up on.
    """
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if INSTALLER_BIN in text.replace("\\", "/"):
            return path
    return None


def tilde(path: Path, home: Path) -> str:
    """A path in the home folder as a student would type it."""
    try:
        return "~/" + path.relative_to(home).as_posix()
    except ValueError:
        return str(path)


def append(path: Path, shell: str) -> bool:
    """Add the line to the end of that file, making it if it is not there.

    Opened for appending rather than read and rewritten, so that nothing already
    in the file can be lost by this even if it is being written to at the time.
    The newline goes on first because a file whose last line has no newline of
    its own would otherwise have this one welded onto the end of it.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_bytes() if path.exists() else b""
        with path.open("a", encoding="utf-8") as handle:
            if existing and not existing.endswith(b"\n"):
                handle.write("\n")
            handle.write(f"\n{MARKER}\n{path_line(shell)}\n")
    except OSError as error:
        print(f"could not write to {path}: {error}")
        return False
    return True


def pixi_is_the_installers(home: Path) -> bool:
    """Whether the pixi in play is the one its own installer put in the home folder.

    PIXI_EXE is set by pixi itself, so under `pixi run` this is not a guess.
    """
    found = os.environ.get("PIXI_EXE") or shutil.which("pixi")
    if not found:
        return False
    try:
        return Path(found).resolve().parent == (home / ".pixi" / "bin").resolve()
    except OSError:
        return Path(found).parent == home / ".pixi" / "bin"


def shells_to_cover(home: Path) -> list[str]:
    """The login shell, plus the other of zsh and bash if it is set up here.

    The second one is the point of this. A student whose login shell is zsh and
    who has a .bash_profile from some installer or other will one day type
    `bash`, or open something that does, and land in a shell that has never
    heard of pixi. Writing to both costs one line in a file they do not read and
    removes a whole class of "it worked yesterday".

    A shell with no startup file at all is left alone: making one for a shell
    nobody on this machine uses is clutter, not a fix.
    """
    first = login_shell()
    covered = [first]
    for shell in BOTH:
        if shell != first and any(path.exists() for path in startup_files(shell, home)):
            covered.append(shell)
    return covered


def main() -> int:
    if sys.platform == "win32":
        return 0                        # PATH lives in the registry here

    home = Path.home()
    if not pixi_is_the_installers(home):
        # Either pixi came from somewhere else and is on PATH by some other
        # means, or it is not here at all -- and neither is fixed by pointing a
        # startup file at ~/.pixi/bin.
        return 0

    written = []
    for shell in shells_to_cover(home):
        files = startup_files(shell, home)
        if not files or already_on_path(files):
            continue
        if append(files[0], shell):
            written.append((shell, files[0]))

    if not written:
        print("Your terminal already knows where pixi is.")
        return 0

    print("Told your terminal where pixi is:")
    for shell, path in written:
        print(f"    {shell}: added the line to {tilde(path, home)}")
    print("")
    print("A shell only reads those files when it starts, so this terminal is")
    print("unchanged. Open a new one and pixi will be there in that, and in every")
    print("terminal after it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
