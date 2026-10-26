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

# The settings file beside it, read the same two ways and for the same reason.
SETTINGS_FILE = (".vscode", "settings.json")
AUTHORING_SETTINGS = ("vscode", "settings.json")

# The setting that says where VS Code may fetch the code that draws a widget.
# This folder ships it empty, which means "only out of the environment". That is
# an instruction that carries a precondition: everything a notebook here asks
# for has to actually BE in the environment, because an empty list leaves no
# second place to look. The precondition held when it was written and is checked
# below rather than assumed, since the thing that would break it -- a widget
# added later whose JavaScript is not installed alongside it -- breaks it
# silently. Nothing is drawn and no error appears, which is the same symptom the
# setting exists to prevent, arriving by the opposite route.
SETTING = "jupyter.widgetScriptSources"
SOURCES = re.compile(r'"jupyter\.widgetScriptSources"\s*:\s*\[(.*?)]', re.DOTALL)

# How VS Code finds the widget code inside an environment: every nbextension
# there has an extension.js, and each one announces the modules it can serve in
# a require config near the top. These are the spellings the editor looks for,
# taken from the extension itself. The two with a question mark matter: the
# anywidget one is written that way, and a reader that knows only the plain
# spelling concludes the file offers nothing and that anywidget is missing.
REQUIRE_PATTERNS = (
    "require.config({", "requirejs.config({", "requirejs?.config({",
    "window.requirejs?.config({", '["require"].config({', "['require'].config({",
)

# Where the packages this folder installs are listed, so that the check and the
# course are reading one list. Same reason extensions come out of
# extensions.json rather than being written down here a second time.
MANIFEST = "pixi.toml"
DEPENDENCIES = re.compile(r"^\[dependencies]$(.*?)(?=^\[)", re.DOTALL | re.MULTILINE)
DEPENDENCY = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s*=", re.MULTILINE)

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


def widget_script_sources(folder: Path) -> list[str] | None:
    """The places this folder lets VS Code fetch widget code from, or None if it
    no longer says."""
    for parts in (SETTINGS_FILE, AUTHORING_SETTINGS):
        try:
            text = folder.joinpath(*parts).read_text(encoding="utf-8")
            break
        except OSError:
            continue
    else:
        return None
    listed = SOURCES.search(COMMENT.sub("", text))
    return QUOTED.findall(listed.group(1)) if listed else None


def environment(folder: Path) -> Path | None:
    """The environment pixi built for this folder."""
    built = folder / ".pixi" / "envs" / "default"
    if built.is_dir():
        return built
    running = Path(sys.prefix)
    return running if (running / "share" / "jupyter").is_dir() else None


def servable(prefix: Path) -> dict[str, Path]:
    """Widget modules the environment can serve out of itself, by name, found
    the way VS Code finds them."""
    found: dict[str, Path] = {}
    share = prefix / "share" / "jupyter"
    for entry in sorted(share.glob("nbextensions/*/extension.js")):
        try:
            text = entry.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern in REQUIRE_PATTERNS:
            start = text.find(pattern)
            if start == -1:
                continue
            # The require config is one object; take it whole, then the
            # innermost group in it, which is where the names are.
            opening = text.index("{", start + len(pattern) - 1)
            depth, cursor = 0, opening
            while cursor < len(text):
                depth += (text[cursor] == "{") - (text[cursor] == "}")
                if depth == 0:
                    break
                cursor += 1
            groups = text[opening:cursor + 1].split("{")
            for line in groups[len(groups) - 1].split("}")[0].split(","):
                name, _, target = line.partition(":")
                name, target = name.strip().strip("\"'"), target.strip().strip("\"'")
                if name and target:
                    found[name] = share / (target + ".js")
            break
    return {name: path for name, path in found.items() if path.is_file()}


def required(folder: Path) -> dict[str, set[str]] | None:
    """Widget modules the packages this folder installs ask for, each with the
    packages asking, or None if this Python cannot see them.

    Only the folder's own environment can answer. Another Python may well have
    ipywidgets in it and would then answer for that one instead -- naming the
    handful of modules ipywidgets itself defines, missing every course widget,
    and reporting that as everything the folder asks for. A check that passes
    because it looked in the wrong place is worse than one that says it cannot
    look, so this declines rather than half-answers.
    """
    prefix = environment(folder)
    if prefix is None or Path(sys.prefix).resolve() != prefix.resolve():
        return None
    try:
        import ipywidgets
    except Exception:
        return None

    try:
        manifest = (folder / MANIFEST).read_text(encoding="utf-8")
    except OSError:
        return None
    listed = DEPENDENCIES.search(manifest)
    if not listed:
        return None

    import importlib
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for package in DEPENDENCY.findall(listed.group(1)):
            try:
                importlib.import_module(package.replace("-", "_"))
            except BaseException:
                # Not importable, or not a Python package at all. Either way it
                # asks for no widget code, which is all this is looking for.
                continue

    def descendants(cls):
        for subclass in cls.__subclasses__():
            yield subclass
            yield from descendants(subclass)

    asked: dict[str, set[str]] = {}
    for widget in descendants(ipywidgets.Widget):
        trait = widget.class_traits().get("_model_module")
        if trait is not None and trait.default_value:
            asked.setdefault(trait.default_value, set()).add(
                widget.__module__.split(".")[0])
    return asked


def check_widget_sources(folder: Path) -> int:
    """Say whether the folder's instruction to fetch no widget code still holds."""
    sources = widget_script_sources(folder)
    if sources is None:
        print(f"This folder no longer sets {SETTING}, so VS Code will use")
        print("whatever each machine happens to have answered to its one-time")
        print("offer to download widget code. Run `im update` to fetch the")
        print("course's current copy of the settings file.")
        return 1
    if sources:
        print(f"This folder lets VS Code download widget code from {', '.join(sources)}.")
        print("")
        print("That is not what the course ships. A download that is refused")
        print("fails quickly, but one that is neither answered nor refused --")
        print("what a VPN, an outbound firewall or a content blocker produces --")
        print("leaves a widget waiting for an answer that never comes. Run")
        print("`im update` to put the setting back, or bring this to class.")
        return 1

    prefix = environment(folder)
    if prefix is None:
        print("This folder tells VS Code to draw widgets using only the code in")
        print("its own environment, but that environment was not found. Run")
        print("`pixi install`, then `pixi run check`, and then this again.")
        return 1

    here = servable(prefix)
    asked = required(folder)
    if asked is None:
        # Run by a Python that is not the environment's own. What each widget
        # asks for cannot be read from here, but what the environment can serve
        # still can, and that is the half that goes wrong.
        print("Widget code is served out of this folder's own environment:")
        print("")
        for name in sorted(here):
            print(f"    {name}")
        print("")
        print("Run this as `pixi run check-vscode` to also check that against")
        print("what the course's widgets ask for.")
        return 0

    missing = {name: who for name, who in asked.items() if name not in here}
    if not missing:
        print("Widgets will draw without downloading anything. This folder's")
        print("environment serves every module they ask for:")
        print("")
        for name in sorted(asked):
            print(f"    {name}")
        return 0

    print("A widget in this folder will not draw, and will not say why.")
    print("")
    print(f"This folder sets {SETTING} to nothing, which tells")
    print("VS Code to draw widgets using only the code in its own environment.")
    print("That environment does not have all of it. Missing:")
    print("")
    for name, who in sorted(missing.items()):
        print(f"    {name}  (asked for by {', '.join(sorted(who))})")
    print("")
    print("Either install the missing widget code into the environment, or let")
    print(f"VS Code download it by naming a source in {SETTING}.")
    print("Bring this message to class if neither is obviously yours to do.")
    return 1


def check_extensions(folder: Path) -> int:
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


def main() -> int:
    # Two questions, both about what this folder asks of the editor: whether it
    # has the extensions named for it, and whether its instruction to draw
    # widgets without downloading anything still has what it needs. The second
    # does not depend on the first, so both are reported every time rather than
    # the first standing in the way of the second.
    folder = course_folder()
    extensions = check_extensions(folder)
    print("")
    return max(extensions, check_widget_sources(folder))


if __name__ == "__main__":
    sys.exit(main())
