"""Tell your terminal where pixi is, whichever shell it opens and however that
shell was started.

You do not need to run this yourself. `pixi run check` runs it, and running it
again is harmless.

There is a second copy of this program beside it, .pin_shell_path.sh, written in
shell for the machine that has no Python to run this one with -- which is the
machine this is for, on the day it is for. The two do the same things in the
same order and write the same line under the same marker, and each looks for the
folder rather than for its own handiwork, so whichever runs first does the work
and the other finds nothing left to do. Change what one of them writes and
change the other in the same commit.

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

There is a second half to the same problem, and it is the one that bites hardest
because there is no window in which to see it. A shell reads different files
depending on how it was started, not only on which shell it is. An interactive
shell, one you type in, reads the rc file: ~/.zshrc or ~/.bashrc. A login shell
reads the profile file: ~/.zprofile or ~/.bash_profile. And a login shell that
is not interactive reads only that profile file, which matters because `zsh -lc`
and `bash -lc` are exactly that, and they are what VS Code, its extensions and
most other tooling run when they run something on your behalf. A line sitting in
the rc file is invisible to all of it. That is how pixi comes to work when you
type it yourself and to be missing when something else runs it for you.

So the line goes wherever that shell will read it whatever kind of shell it is.
For zsh that is ~/.zshenv, the one file zsh reads on every invocation, login or
not, interactive or not. bash has no such file, so it takes two: the login file
it opens when it is a login shell, and ~/.bashrc for when it is interactive
without being one. A `bash -c` that is neither reads no startup file at all, and
nothing here can reach that one.

Both shells are set up, whichever one this machine happens to open by default.
The default shell is not the only shell a student will meet: VS Code opens what
its own settings say, a tutorial tells them to type `bash`, an extension runs
`zsh -lc`, and any one of those can be the thing that cannot find pixi while
Terminal works perfectly.

It writes nothing where the line is already there, and nothing at all if pixi
came from somewhere other than its own installer (from Homebrew, say), because
then the line would point at a folder that does not exist and the problem is not
this one.

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

# The two this is about, and both are always done. Which of them a student's
# machine opens by default decides nothing here: the other is one typed word
# away, and the window that cannot find pixi is usually the one they did not
# choose.
BOTH = ("zsh", "bash")

# The shells this knows how to write for at all. Anything else is left alone
# rather than guessed at, because a startup line in a syntax the shell does not
# speak is worse than no line: it fails on every start from then on.
KNOWN = ("zsh", "bash", "fish")

# Making the login file read the rc file. This is a separate fix from the PATH
# line, and with the line where it now goes pixi is found without it. It earns
# its place on everything else: a conda init, an alias, another tool's PATH
# line, anything a student or an installer drops into the rc file later is then
# true in a login shell too, without anyone having to know that these are two
# files read on two different occasions.
#
# Each is written the way that shell's own manual writes it, so a student who
# opens the file meets the idiom they will find everywhere else for that shell.
# Both are guarded on the rc file existing, so neither breaks a home folder that
# has not got one.
BRIDGE = {
    "bash": (".bashrc", "if [ -f ~/.bashrc ]; then\n    source ~/.bashrc\nfi"),
    "zsh": (".zshrc", "[[ -f ~/.zshrc ]] && source ~/.zshrc"),
}

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
    if found in KNOWN:
        return found
    return "zsh" if sys.platform == "darwin" else "bash"


def shells_to_cover() -> list[str]:
    """Every shell to set up: both of them, plus the default one if it is neither.

    A student whose default shell is fish still gets zsh and bash configured. It
    costs a few lines in files they do not read, and it means that the day
    something opens a bash for them, and something will, pixi is there in it.
    """
    shells = list(BOTH)
    first = login_shell()
    if first not in shells:
        shells.append(first)
    return shells


def shell_home(shell: str, home: Path) -> Path:
    """Where that shell keeps its startup files, which is not always the home folder.

    zsh reads $ZDOTDIR instead when it is set, and a student who has set it has
    done so on purpose; writing to the home folder anyway would put the line in
    a file that shell no longer opens.
    """
    if shell == "zsh" and os.environ.get("ZDOTDIR"):
        return Path(os.environ["ZDOTDIR"]).expanduser()
    return home


def bash_login_file(base: Path) -> Path:
    """The file bash opens when it starts as a login shell.

    bash reads the first of these that exists and then stops, so the one to
    write to is the first that is already there rather than always
    .bash_profile. Writing to .bash_profile while a .profile is the file being
    read today would both put the line where bash never looks and, by creating
    .bash_profile, silence that .profile from then on. Where none of the three
    exists there is nothing to shadow, and .bash_profile is the one to make.
    """
    for name in (".bash_profile", ".bash_login", ".profile"):
        if (base / name).exists():
            return base / name
    return base / ".bash_profile"


def path_files(shell: str, base: Path) -> list[Path]:
    """Every file that shell has to be told, so that it is told in all its moods.

    zsh needs one and bash needs two; the top of this script says why. fish
    reads its one config file whether or not it is interactive, so it needs only
    that.
    """
    if shell == "zsh":
        return [base / ".zshenv"]
    if shell == "bash":
        return [bash_login_file(base), base / ".bashrc"]
    if shell == "fish":
        return [base / ".config" / "fish" / "config.fish"]
    return []


def bridge_file(shell: str, base: Path) -> Path | None:
    """The login file to make read the rc file, or None where there is no safe one.

    For bash this is deliberately not whatever bash_login_file returns. That can
    be ~/.profile, which sh reads too, and `source` is bash's spelling of `.`:
    an sh reading it would print an error on every login. So the bridge only
    goes in a file belonging to bash alone, and is only created where there is
    no ~/.profile for a new ~/.bash_profile to shadow.
    """
    if shell == "zsh":
        return base / ".zprofile"
    if shell != "bash":
        return None
    for name in (".bash_profile", ".bash_login"):
        if (base / name).exists():
            return base / name
    return None if (base / ".profile").exists() else base / ".bash_profile"


def path_line(shell: str) -> str:
    """The line that puts pixi on PATH, written the way that shell writes it.

    Guarded on the folder not being on PATH already, which the plain export was
    not. The line now goes in more than one file per shell and a login shell
    reads more than one of them, so unguarded, PATH would collect a copy of the
    folder from each, and another copy for every shell opened inside another.

    The guard is written in POSIX shell rather than with [[ ]], because for bash
    the file it lands in can be ~/.profile, and on a Linux machine sh reads that
    one as well, where [[ is a syntax error rather than a test.
    """
    if shell == "fish":
        return 'fish_add_path "$HOME/.pixi/bin"'      # already does not repeat
    return ('case ":$PATH:" in\n'
            '    *":$HOME/.pixi/bin:"*) ;;\n'
            '    *) export PATH="$HOME/.pixi/bin:$PATH" ;;\n'
            'esac')


def mentions(path: Path, needle: str) -> bool:
    """Whether that file already says that, a missing file counting as a no.

    Looked for by the folder, or by the rc file's name, rather than by the whole
    line, so that what the pixi installer wrote, or what a student typed
    themselves in one of the several forms people write these in, counts as done
    and does not get a second copy underneath it.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return needle in text.replace("\\", "/")


def tilde(path: Path, home: Path) -> str:
    """A path in the home folder as a student would type it."""
    try:
        return "~/" + path.relative_to(home).as_posix()
    except ValueError:
        return str(path)


def append(path: Path, block: str) -> bool:
    """Add the block to the end of that file, making it if it is not there.

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
            handle.write(f"\n{MARKER}\n{block}\n")
    except OSError as error:
        print(f"could not write to {path}: {error}")
        return False
    return True


def pixi_is_the_installers(home: Path) -> bool:
    """Whether the pixi in play is the one its own installer put in the home folder.

    PIXI_EXE is set by pixi itself, so under `pixi run` this is not a guess.

    Where neither of those finds anything, the folder is asked directly. The
    moment this script is most needed is the one in which nothing can find pixi
    yet: run by hand straight after the installer, from the shell the installer
    has just written a line for and which has not read it, there is no PIXI_EXE
    and no pixi on PATH, and the only evidence that the install happened is the
    file sitting there in the home folder. Asking PATH alone would make the
    script do nothing, and say nothing, in exactly that case. A pixi from
    somewhere else still fails this test, since it leaves no ~/.pixi/bin behind.
    """
    found = os.environ.get("PIXI_EXE") or shutil.which("pixi")
    if not found:
        return (home / ".pixi" / "bin" / "pixi").exists()
    try:
        return Path(found).resolve().parent == (home / ".pixi" / "bin").resolve()
    except OSError:
        return Path(found).parent == home / ".pixi" / "bin"


def main() -> int:
    if sys.platform == "win32":
        return 0                        # PATH lives in the registry here

    home = Path.home()
    if not pixi_is_the_installers(home):
        # Either pixi came from somewhere else and is on PATH by some other
        # means, or it is not here at all -- and neither is fixed by pointing a
        # startup file at ~/.pixi/bin.
        return 0

    written, bridged = [], []
    for shell in shells_to_cover():
        base = shell_home(shell, home)

        # The PATH line goes in first, so that in a home folder with no startup
        # files at all the rc file exists by the time the bridge below asks
        # whether there is anything there worth reading.
        for path in path_files(shell, base):
            if not mentions(path, INSTALLER_BIN) and append(path, path_line(shell)):
                written.append((shell, path))

        if shell in BRIDGE:
            rc_name, line = BRIDGE[shell]
            profile = bridge_file(shell, base)
            if profile and not mentions(profile, rc_name) and append(profile, line):
                bridged.append((shell, profile, rc_name))

    if not written and not bridged:
        print("Your terminal already knows where pixi is.")
        return 0

    if written:
        print("Told your terminal where pixi is:")
        for shell, path in written:
            print(f"    {shell}: added the line to {tilde(path, home)}")
    if bridged:
        print("Made your login shell read the file that line is in:")
        for shell, path, rc_name in bridged:
            print(f"    {shell}: {tilde(path, home)} now reads ~/{rc_name}")
    print("")
    print("A shell only reads those files when it starts, so this terminal is")
    print("unchanged. Open a new one and pixi will be there in that, and in every")
    print("terminal after it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
