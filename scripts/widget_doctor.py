#!/usr/bin/env python3
"""Find out why a course widget does not appear.

Run it from anywhere, with any Python:

    python3 widget_doctor.py

It changes nothing. It reads settings files, looks in the course environment,
tries the two downloads VS Code would try, and reads the editor's own log, then
says which of those is the reason a widget did not draw. It writes what it found
to widget-doctor-report.txt beside itself, to be sent to the instructor.

Background, so that the checks below make sense.

Every widget on this course -- steps, puzzle, codelens, turtle, sandbox, iplot --
is built on a package called anywidget, and VS Code does not ship with anywidget.
Before it can draw any of them it has to get hold of one file of supporting
JavaScript. There are two places it can get it: out of the course environment,
which already contains it, or by downloading it from one of two public websites.
Which of those it tries is decided by a setting, jupyter.widgetScriptSources.

A download that is refused fails quickly and VS Code recovers. A download that is
neither answered nor refused -- which is what a VPN, an outbound firewall or a
content blocker produces -- leaves VS Code waiting for an answer that never
arrives. Nothing is drawn, no error appears, and a second widget on the same page
waits behind the first. That is the state this script is looking for.
"""

from __future__ import annotations

import json
import os
import platform
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# How long to wait for each download before calling it unanswered. VS Code
# itself waits far longer, which is the whole problem; the point here is to find
# out quickly rather than to reproduce the wait.
TIMEOUT = 12

# The two addresses VS Code builds, taken from the extension itself:
#   unpkg.com     https://unpkg.com/${packageName}@${moduleVersionSpec}/dist/${fileName}
#   jsdelivr.com  https://cdn.jsdelivr.net/npm/${packageName}@${moduleVersion}/dist/${fileName}
CDNS = {
    "jsdelivr.com": "https://cdn.jsdelivr.net/npm/anywidget@{version}/dist/index.js",
    "unpkg.com": "https://unpkg.com/anywidget@{version}/dist/index.js",
}

# Used to tell "this student's whole network is down" apart from "these two
# addresses in particular do not answer". It is the course's own website, so a
# student who can read the notes can reach it.
CONTROL = "https://munch-group.org/instructing-machines/"

# Version to ask the download for when the environment cannot be read.
FALLBACK_VERSION = "0.11.0"

# How long the search for course folders may take before it gives up and says
# so. A folder inside a sync client can be slow enough to stall the search on
# its own, which is a finding rather than a reason to wait.
SEARCH_BUDGET = 20

SETTING = "jupyter.widgetScriptSources"

# Directory names never worth descending into when looking for the course
# folder. .pixi is the big one: it holds tens of thousands of files.
SKIP_DIRS = {
    ".pixi", ".git", "node_modules", "__pycache__", ".venv", "venv",
    "Library", "Applications", ".Trash", ".cache", "site-packages",
}

report_lines = []


def say(text=""):
    print(text)
    report_lines.append(text)


def heading(number, text):
    say()
    say(f"{number}. {text}")
    say("-" * (len(text) + len(str(number)) + 2))


def read_jsonc(path):
    """Load a settings file. VS Code allows comments and trailing commas in
    these, which json.load does not, so both are taken out first."""
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)          # /* block */
    text = re.sub(r"(?m)(?<![:\"/])//[^\n]*", "", text)         # // line
    text = re.sub(r",(\s*[}\]])", r"\1", text)                  # trailing comma
    return json.loads(text)


# --------------------------------------------------------------------------- #
# Where the editor keeps its files, which differs per platform and per flavour  #
# --------------------------------------------------------------------------- #

def vscode_dirs():
    """Every VS Code installation's support directory on this machine."""
    flavours = ["Code", "Code - Insiders", "VSCodium"]
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif os.name == "nt":
        base = Path(os.environ.get("APPDATA", str(Path.home())))
    else:
        base = Path.home() / ".config"
    return [(name, base / name) for name in flavours if (base / name).is_dir()]


# Roots that could not be listed, and why. A folder living in a sync client can
# take so long to answer that the listing times out, which is worth reporting:
# the same wait happens to anything else that reads a file in there.
unreadable_roots = []


def safe_iterdir(path):
    """List a directory, giving up rather than waiting.

    A folder that a sync client has not fetched yet can block for a long time,
    and a script written to diagnose a hang must not hang itself.
    """
    try:
        return sorted(path.iterdir())
    except OSError as error:
        if not any(path == seen for seen, _ in unreadable_roots):
            unreadable_roots.append((path, error))
        return []


def course_folders():
    """Every copy of the course folder this script can find.

    Looks up from the working directory first, since a student running this
    inside the folder should get that one, then through the handful of places a
    download normally lands.
    """
    found = []

    def is_course(path):
        manifest = path / "pixi.toml"
        try:
            if not manifest.is_file():
                return False
            text = manifest.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False
        return 'name = "instructing-machines"' in text

    for parent in [Path.cwd(), *Path.cwd().parents]:
        if is_course(parent) and parent not in found:
            found.append(parent)

    home = Path.home()
    roots = [home, home / "Desktop", home / "Documents", home / "Downloads"]
    # Desktop and Documents are frequently redirected into a sync client, and
    # the folder is then not where the plain path says it is.
    for pattern in ("OneDrive*", "Library/Mobile Documents/com~apple~CloudDocs"):
        try:
            roots.extend(p for p in home.glob(pattern) if p.is_dir())
        except OSError:
            continue

    deadline = time.monotonic() + SEARCH_BUDGET
    for root in roots:
        if time.monotonic() > deadline:
            unreadable_roots.append((root, "not searched: the search was taking too long"))
            continue
        try:
            if not root.is_dir():
                continue
        except OSError as error:
            unreadable_roots.append((root, error))
            continue
        for depth1 in safe_iterdir(root):
            if time.monotonic() > deadline:
                break
            try:
                if not depth1.is_dir() or depth1.name in SKIP_DIRS:
                    continue
            except OSError:
                continue
            candidates = [depth1]
            candidates.extend(
                d for d in safe_iterdir(depth1)
                if d.name not in SKIP_DIRS and not d.name.startswith("."))
            for candidate in candidates:
                if is_course(candidate) and candidate not in found:
                    found.append(candidate)
    return found


def environment_prefix(folder):
    """The Python environment pixi built inside a course folder, if it is there."""
    prefix = folder / ".pixi" / "envs" / "default"
    return prefix if prefix.is_dir() else None


def anywidget_version(prefix):
    """The anywidget version installed in an environment, read from the file the
    editor would serve. Falls back to a constant when it cannot be read."""
    if prefix is None:
        return FALLBACK_VERSION
    manifest = prefix / "share" / "jupyter" / "labextensions" / "anywidget" / "package.json"
    try:
        return json.loads(manifest.read_text(encoding="utf-8"))["version"]
    except Exception:
        return FALLBACK_VERSION


# --------------------------------------------------------------------------- #
# The download test, which is the point of the whole script                    #
# --------------------------------------------------------------------------- #

def try_download(url):
    """Attempt one download and say which of three things happened.

    Returns (verdict, detail). The verdict is one of:

      answered   something came back, even a "not found" -- the path works
      refused    turned away at once, which VS Code survives
      no answer  nothing came back before the timeout -- the fault being hunted
    """
    request = urllib.request.Request(url, headers={"User-Agent": "widget-doctor"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT,
                                    context=ssl.create_default_context()) as response:
            return "answered", f"HTTP {response.status}, {len(response.read())} bytes"
    except urllib.error.HTTPError as error:
        return "answered", f"HTTP {error.code}"
    except urllib.error.URLError as error:
        reason = error.reason
        if isinstance(reason, socket.timeout):
            return "no answer", f"nothing came back within {TIMEOUT} seconds"
        if isinstance(reason, socket.gaierror):
            return "refused", f"the address could not be looked up ({reason})"
        if isinstance(reason, ssl.SSLError):
            return "refused", f"the secure connection was interfered with ({reason})"
        return "refused", str(reason)
    except socket.timeout:
        return "no answer", f"nothing came back within {TIMEOUT} seconds"
    except Exception as error:                       # noqa: BLE001 - report anything
        return "refused", f"{type(error).__name__}: {error}"


# --------------------------------------------------------------------------- #
# The editor's own log                                                          #
# --------------------------------------------------------------------------- #

LOG_MARKERS = (
    "Script source for Widget",
    "Widget Script Source not found",
    "nbextensions folder found",
    "Widget load failure",
    "Searching for Widget Script",
    "was not found on on any cdn",
    "Failed to download widget script source",
    "cannot use CDN",
    "Widget Error",
)


def jupyter_logs():
    """Every Jupyter output-panel log this machine has kept, newest first."""
    logs = []
    for _, support in vscode_dirs():
        root = support / "logs"
        if not root.is_dir():
            continue
        try:
            logs.extend(root.glob("*/window*/exthost/output_logging_*/*-Jupyter.log"))
            logs.extend(root.glob("*/window*/exthost/ms-toolsai.jupyter/*.log"))
        except OSError:
            continue

    def when(path):
        try:
            return path.stat().st_mtime
        except OSError:
            return 0

    return sorted(logs, key=when, reverse=True)


# When a widget fails, the editor prints the list of download sources it was
# configured with, in square brackets, on the same line. That list is the whole
# answer to "did the fix take effect": [] means it did, and a list naming the
# two websites means VS Code is still being told to download.
CONFIGURED_SOURCES = re.compile(r"Widget load failure\s+\S+\s+(\[[^\]]*\])")
NOTEBOOK_PATH = re.compile(r"[~/][^\s'\"]*\.ipynb")


def analyse_logs(paths, limit=6):
    """Read the newest logs and pull out what they say about widgets."""
    found = {
        "lines": [],          # the widget lines themselves, newest file first
        "sources": [],        # (timestamp, configured source list) pairs
        "notebooks": [],      # notebooks the editor was working on
        "fetch_failed": 0,    # times a download failed from inside the editor
        "timed_out": 0,       # times the editor called it a timeout
        "read": [],           # which files were actually read
        "evidence_written": 0,  # when the newest widget line was written
    }
    # paths arrive newest first; read them in the opposite order so that the
    # last entry collected is genuinely the most recent one.
    for path in reversed(paths[:limit]):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found["read"].append(path)
        try:
            written_at = path.stat().st_mtime
        except OSError:
            written_at = 0
        had_widget_line = False
        for line in text.splitlines():
            for notebook in NOTEBOOK_PATH.findall(line):
                if notebook not in found["notebooks"]:
                    found["notebooks"].append(notebook)
            if "Failed to access CDN" in line:
                found["fetch_failed"] += 1
            if "timedout: true" in line:
                found["timed_out"] += 1
            match = CONFIGURED_SOURCES.search(line)
            if match:
                # The log line carries a time but no date; take the date from
                # the file so that entries from different days can be told
                # apart and read in order.
                day = time.strftime("%d %b", time.localtime(written_at))
                clock = line.split(" ", 1)[0]
                found["sources"].append((f"{day} {clock}", match.group(1)))
            if any(marker in line for marker in LOG_MARKERS):
                found["lines"].append(line.strip())
                had_widget_line = True
        if had_widget_line:
            found["evidence_written"] = max(found.get("evidence_written", 0), written_at)
    return found


# --------------------------------------------------------------------------- #

def main():
    say("Widget doctor")
    say("=============")
    say()
    say(f"{platform.system()} {platform.release()} on {platform.machine()}, "
        f"Python {sys.version.split()[0]}")
    say(f"run from {Path.cwd()}")

    verdicts = {}

    # ---------------------------------------------------------------- 1
    heading(1, "The course folder")
    folders = course_folders()
    if not folders:
        say("No course folder found. Run this script from inside the course")
        say("folder -- the one with pixi.toml in it -- and try again.")
        say()
        say("Nothing else below can be checked without it.")
        write_report()
        return 1
    for folder in folders:
        say(f"  {folder}")
    if len(folders) > 1:
        say()
        say(f"There are {len(folders)} copies of the course folder on this machine.")
        say("That matters: `im update` only updates the one it is run in, and VS")
        say("Code only reads the settings of the folder actually open. If these")
        say("disagree below, that is the reason.")
    if unreadable_roots:
        say()
        say("Some folders could not be listed while looking:")
        for path, error in unreadable_roots[:6]:
            say(f"  {path}")
            say(f"      {error}")
        say()
        say("A folder that is slow to answer like this is usually one a sync")
        say("client (OneDrive, iCloud Drive) has not fetched yet. If the course")
        say("folder itself is inside one of those, move it somewhere local --")
        say("reading any file in it can stall the same way.")
    working = folders[0]
    say()
    say(f"Reading the first of these as the one in use: {working}")

    # ---------------------------------------------------------------- 2
    heading(2, "Did the fix arrive in the folder?")
    say("The course folder now ships a setting that stops VS Code downloading")
    say("widget support and makes it use the copy in the environment instead.")
    say("`im update` is what delivers it.")
    say()
    fixed_folders = []
    for folder in folders:
        settings_path = folder / ".vscode" / "settings.json"
        if not settings_path.is_file():
            say(f"  {folder}\n      no .vscode/settings.json at all")
            continue
        try:
            settings = read_jsonc(settings_path)
        except Exception as error:                   # noqa: BLE001
            say(f"  {folder}\n      settings.json could not be read ({error})")
            continue
        if SETTING in settings:
            value = settings[SETTING]
            state = "the fix is present" if value == [] else f"present but set to {value!r}"
            say(f"  {folder}\n      {state}")
            if value == []:
                fixed_folders.append(folder)
        else:
            say(f"  {folder}\n      the setting is NOT there -- this folder has not been updated")
        backup = folder / ".vscode" / "settings.json.backup"
        if backup.is_file():
            say(f"      (a settings.json.backup is here, so `im update` did replace this file)")
    verdicts["fix_in_folder"] = bool(fixed_folders) and working in fixed_folders

    # ---------------------------------------------------------------- 3
    heading(3, "What your VS Code itself is set to")
    say("This is the machine-wide setting, written when VS Code once offered to")
    say("download widget support and was told yes. The folder's setting overrides")
    say("it, but only for a folder that is actually open as a folder.")
    say()
    user_values = {}
    for name, support in vscode_dirs():
        settings_path = support / "User" / "settings.json"
        if not settings_path.is_file():
            say(f"  {name}: no user settings file")
            continue
        try:
            settings = read_jsonc(settings_path)
        except Exception as error:                   # noqa: BLE001
            say(f"  {name}: settings could not be read ({error})")
            continue
        value = settings.get(SETTING, "(not set)")
        user_values[name] = value
        say(f"  {name}: {SETTING} = {value!r}")
    if not vscode_dirs():
        say("  No VS Code installation found in the usual place.")
    verdicts["cdn_enabled_by_user"] = any(
        isinstance(v, list) and v for v in user_values.values())

    # ---------------------------------------------------------------- 4
    heading(4, "The downloads VS Code would try")
    prefix = environment_prefix(working)
    version = anywidget_version(prefix)
    say(f"Asking for anywidget {version}, the way the editor would.")
    say()
    control_verdict, control_detail = try_download(CONTROL)
    say(f"  the course website   {control_verdict:<10} ({control_detail})")
    results = {}
    for name, template in CDNS.items():
        verdict, detail = try_download(template.format(version=version))
        results[name] = verdict
        say(f"  {name:<20} {verdict:<10} ({detail})")
    verdicts["cdn_hangs"] = "no answer" in results.values()
    verdicts["network_down"] = control_verdict != "answered"

    # ---------------------------------------------------------------- 5
    heading(5, "The copy in the environment")
    say("This is what the fix makes VS Code use instead of downloading.")
    say()
    if prefix is None:
        say(f"  No environment in {working}. Run `pixi install` there.")
        verdicts["local_copy"] = False
    else:
        local = prefix / "share" / "jupyter" / "nbextensions" / "anywidget" / "index.js"
        if local.is_file():
            say(f"  present, {local.stat().st_size} bytes")
            say(f"  {local}")
            verdicts["local_copy"] = True
        else:
            say(f"  MISSING -- expected it at {local}")
            verdicts["local_copy"] = False

    # ---------------------------------------------------------------- 6
    heading(6, "What the editor's own log says")
    logs = jupyter_logs()
    if not logs:
        say("No Jupyter log found. VS Code writes one only once a notebook has")
        say("been opened, so open a notebook, run a widget cell, then run this again.")
        verdicts["log"] = None
    else:
        log = analyse_logs(logs)
        verdicts["log"] = log
        say(f"Read the newest {len(log['read'])} of {len(logs)} log file(s).")

        # The decisive part: what VS Code believed it was configured with the
        # last few times a widget failed.
        say()
        if log["sources"]:
            say("Download sources in force each time a widget failed (oldest first):")
            for stamp, sources in log["sources"][-6:]:
                verdict = "the fix is in force" if sources == "[]" else "STILL DOWNLOADING"
                say(f"  {stamp}  {sources}   <- {verdict}")
        else:
            say("The log has no record of a widget failing to load.")

        if log["notebooks"]:
            say()
            say("Notebooks the editor has been working on (which folder is open):")
            for notebook in log["notebooks"][:6]:
                say(f"  {notebook}")

        say()
        say(f"Downloads that failed from inside the editor: {log['fetch_failed']}")
        say(f"Failures the editor itself called a timeout:  {log['timed_out']}")

        if log["lines"]:
            say()
            say("The widget lines themselves (most recent last):")
            for line in log["lines"][-20:]:
                say(f"  {line}")
        else:
            say()
            say("Nothing about widgets in the log at all. If a widget was run and")
            say("nothing was drawn, that silence is itself informative: it means")
            say("the editor is still waiting rather than having given up.")

    # ---------------------------------------------------------------- 7
    heading(7, "What this adds up to")
    conclusions = []
    log = verdicts.get("log")

    # The log outranks everything else here. The two checks above say what
    # this machine can do now; the log says what the editor actually did.
    latest_sources = log["sources"][-1][1] if log and log["sources"] else None

    # Log records written before the fix arrived say nothing about whether the
    # fix works. Compare when the evidence was written against when the folder's
    # settings file was last changed.
    stale_evidence = False
    if log and log.get("evidence_written"):
        settings_path = working / ".vscode" / "settings.json"
        try:
            if settings_path.stat().st_mtime > log["evidence_written"]:
                stale_evidence = True
        except OSError:
            pass

    if stale_evidence:
        conclusions.append(
            "THE EVIDENCE IS OUT OF DATE. Everything the log says about widgets "
            "was written before this folder's settings were last changed, so it "
            "describes how things were before the fix arrived, not after. Open "
            "the course folder, run a cell with a widget in it, wait until it "
            "either draws or clearly does not, and then run this script again. "
            "That second report is the one worth sending.")
    elif latest_sources == "[]":
        conclusions.append(
            "THE FIX IS IN FORCE AND IS NOT ENOUGH. The last time a widget "
            "failed, the editor had no download sources configured, so it was "
            "not waiting on a download. Whatever is stopping the widget is "
            "something else, and the widget lines above are the evidence for "
            "it. Send this report.")
    elif latest_sources is not None:
        conclusions.append(
            "THE FIX IS NOT IN FORCE. The last time a widget failed, the "
            f"editor was still configured to download from {latest_sources}. "
            "So the setting has not reached the window that is open: either "
            "the folder was not updated, or the folder is not open as a "
            "folder, or VS Code has not been reloaded since it changed.")
    elif log and log["fetch_failed"]:
        conclusions.append(
            "The editor failed to download widget support at least "
            f"{log['fetch_failed']} time(s). That is the fault this is looking "
            "for.")

    if log and log["fetch_failed"] and not verdicts.get("cdn_hangs") \
            and not verdicts.get("network_down"):
        conclusions.append(
            "Note the disagreement, which is worth reporting: the editor could "
            "not fetch the file, yet this script downloaded it from the same "
            "address without trouble a moment ago. The block is therefore not "
            "the network in general but something in the editor's own "
            "connection -- which is a reason to stop it downloading at all "
            "rather than to try to fix the download.")

    if verdicts.get("network_down"):
        conclusions.append(
            "This machine could not reach the course website either, so the "
            "download results prove nothing on their own. Check the internet "
            "connection and run this again.")
    elif verdicts.get("cdn_hangs"):
        conclusions.append(
            "At least one of the two download addresses did not answer at all "
            "just now. VS Code waits for that answer, draws nothing, and "
            "reports no error. Something on this machine or network -- a VPN, "
            "an outbound firewall, a content blocker -- is swallowing the "
            "request rather than refusing it.")

    if verdicts.get("fix_in_folder"):
        conclusions.append(
            "The fix IS in the folder this script read, so `im update` did "
            "deliver it. For it to take effect the folder has to be opened "
            "with File -> Open Folder rather than the notebook opened on its "
            "own, VS Code has to be reloaded, and the kernel restarted.")
    else:
        conclusions.append(
            "The fix is NOT in the folder this script read. Run `im update` "
            "in that folder and check again. If step 1 listed more than one "
            "copy of the course folder, make sure the one being updated is "
            "the one being opened.")

    if verdicts.get("cdn_enabled_by_user"):
        conclusions.append(
            "This VS Code is set machine-wide to download widget support. The "
            "folder's setting overrides that, but only for a folder that is "
            "open as a folder. Setting jupyter.widgetScriptSources to an empty "
            "list in the machine-wide settings as well would remove the fault "
            "everywhere, whichever way a notebook is opened. In VS Code: "
            "Cmd/Ctrl+Shift+P, 'Preferences: Open User Settings (JSON)'.")

    if verdicts.get("local_copy") is False:
        conclusions.append(
            "The copy in the environment is missing, so the fix has nothing to "
            "fall back on. Run `pixi install` and then `pixi run check`.")

    for index, text in enumerate(conclusions, start=1):
        say()
        say(f"({index}) {text}")

    write_report()
    return 0


def write_report():
    target = Path.cwd() / "widget-doctor-report.txt"
    try:
        target.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        print()
        print(f"Written to {target}")
        print("Send that file to your instructor.")
    except OSError as error:
        print(f"\n(Could not write the report: {error})")


if __name__ == "__main__":
    sys.exit(main())
