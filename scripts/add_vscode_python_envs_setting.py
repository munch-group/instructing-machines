#!/usr/bin/env python3
"""Add "python-envs.workspaceSearchPaths" to the VS Code User settings.json.

Inserts:

    "python-envs.workspaceSearchPaths": [
        ".pixi",
        "*/.pixi"
    ]

so the VS Code Python extension discovers pixi environments (both a
project-root .pixi and any */.pixi one level down) as interpreters.

VS Code's settings.json is JSONC (comments and trailing commas allowed), so
this script edits the file as text rather than round-tripping it through
json.load/json.dump, which would strip comments and reformat everything.
It is safe to re-run: if the key is already present it does nothing.

Usage:
    python scripts/add_vscode_python_envs_setting.py [path/to/settings.json]

With no argument it targets the standard per-OS VS Code User settings path.
"""

import argparse
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

KEY = "python-envs.workspaceSearchPaths"
VALUE_BLOCK = (
    '    "python-envs.workspaceSearchPaths": [\n'
    '        ".pixi",\n'
    '        "*/.pixi"\n'
    "    ],\n"
)


def default_settings_path() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library/Application Support/Code/User/settings.json"
    if system == "Windows":
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        return appdata / "Code/User/settings.json"
    return Path.home() / ".config/Code/User/settings.json"


def find_object_close(text: str) -> int:
    """Return the index of the '}' that closes the top-level JSON object.

    Walks the text tracking brace depth while skipping over string literals
    and // and /* */ comments, so nested braces inside language-specific
    blocks (e.g. "[python]": {...}) don't get mistaken for the outer close.
    """
    depth = 0
    in_string = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            nl = text.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            i = end + 2 if end != -1 else n
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("could not find the closing brace of the top-level JSON object")


def strip_jsonc(text: str) -> str:
    """Strip // and /* */ comments (outside strings), leaving plain JSON."""
    out = []
    in_string = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            nl = text.find("\n", i)
            i = nl if nl != -1 else n
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            i = end + 2 if end != -1 else n
            continue
        if ch == '"':
            in_string = True
        out.append(ch)
        i += 1
    return "".join(out)


def strip_trailing_commas(text: str) -> str:
    return re.sub(r",(\s*[}\]])", r"\1", text)


def validate_jsonc(text: str) -> None:
    json.loads(strip_trailing_commas(strip_jsonc(text)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "settings_path",
        nargs="?",
        type=Path,
        default=None,
        help="Path to settings.json (defaults to the standard VS Code User settings location)",
    )
    args = parser.parse_args()

    settings_path = args.settings_path or default_settings_path()
    if not settings_path.exists():
        print(f"error: {settings_path} does not exist", file=sys.stderr)
        return 1

    text = settings_path.read_text(encoding="utf-8")

    if f'"{KEY}"' in text:
        print(f"{settings_path}: {KEY!r} already present, nothing to do")
        return 0

    try:
        validate_jsonc(text)
    except json.JSONDecodeError as exc:
        print(f"error: existing {settings_path} is not valid JSONC: {exc}", file=sys.stderr)
        return 1

    close_idx = find_object_close(text)
    prefix = text[:close_idx].rstrip()
    suffix = text[close_idx:]

    if prefix.endswith("{") or prefix.endswith(","):
        new_prefix = prefix + "\n"
    else:
        new_prefix = prefix + ",\n"

    new_text = new_prefix + VALUE_BLOCK + suffix

    try:
        validate_jsonc(new_text)
    except json.JSONDecodeError as exc:
        print(f"error: generated settings would be invalid JSON: {exc}", file=sys.stderr)
        return 1

    backup_path = settings_path.with_suffix(settings_path.suffix + ".bak")
    shutil.copy2(settings_path, backup_path)
    settings_path.write_text(new_text, encoding="utf-8")

    print(f"Added {KEY!r} to {settings_path}")
    print(f"Backup saved to {backup_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
