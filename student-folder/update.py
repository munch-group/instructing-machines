#!/usr/bin/env python3
"""Refresh the course environment from the course website.

You only need this if you are told to run it — for instance if a new widget
version is released halfway through the term. It downloads a fresh pixi.toml
and pixi.lock next to this script, keeps a backup of the old ones, and runs
`pixi install` for you.

    pixi run update-env

It never touches your notebooks, your data, or anything in projects/.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Where the course folder is published. Change this if the website moves.
BASE_URL = "https://munch-group.org/instructing-machines"

FILES = ("pixi.toml", "pixi.lock")
HERE = Path(__file__).resolve().parent

# A downloaded file must contain this to be believable as a pixi manifest or
# lock file. Cheap insurance against silently saving a "404 not found" page
# over a working environment.
SANITY = {"pixi.toml": "[workspace]", "pixi.lock": "version:"}


def fetch(name: str) -> str:
    url = f"{BASE_URL}/{name}"
    print(f"Fetching {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "instructing-machines-update"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def main() -> int:
    downloaded: dict[str, str] = {}

    for name in FILES:
        try:
            text = fetch(name)
        except urllib.error.URLError as error:
            print(f"\nCould not download {name}: {error}")
            print("Check that you are online. Nothing has been changed.")
            return 1
        if SANITY[name] not in text:
            print(f"\nWhat came back for {name} does not look like a {name}.")
            print("Nothing has been changed. Please tell your instructor.")
            return 1
        downloaded[name] = text

    # Only start writing once both downloads have arrived and look sane, so a
    # failure halfway cannot leave a half-updated environment behind.
    for name, text in downloaded.items():
        target = HERE / name
        if target.exists():
            backup = HERE / f"{name}.backup"
            shutil.copy2(target, backup)
            print(f"Kept your old {name} as {backup.name}")
        target.write_text(text, encoding="utf-8")
        print(f"Updated {name}")

    print("\nInstalling. This may take a few minutes.\n")
    pixi = shutil.which("pixi")
    if pixi is None:
        print("Could not find pixi. Open a new terminal and run `pixi install` yourself.")
        return 1

    result = subprocess.run([pixi, "install"], cwd=HERE)
    if result.returncode != 0:
        print("\n`pixi install` did not finish cleanly. Bring the message above to class.")
        return result.returncode

    print("\nDone. Run `pixi run check` to confirm.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
