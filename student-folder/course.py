"""Where the course lives on the web.

You never run this file. It exists so that `get.py` and `update.py` cannot
disagree about the address of the course website: both of them ask this file.

If you are curious, the functions below are the whole of it — one builds a web
address, the others download it and hand back what came.
"""

from __future__ import annotations

import os
import urllib.request
from pathlib import Path

# Where the course folder is published. Change this if the website moves.
# IM_COURSE_URL overrides it, which is how the course website is tested
# against a local preview before it is published; students never set it.
BASE_URL = os.environ.get(
    "IM_COURSE_URL", "https://munch-group.org/instructing-machines"
).rstrip("/")

# The folder this file is in — that is, the course folder itself.
HERE = Path(__file__).resolve().parent


def url_for(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def fetch_bytes(path: str, timeout: int = 60) -> bytes:
    """Download BASE_URL/path and return it exactly as it arrived.

    Raises urllib.error.URLError if the website cannot be reached, which the
    calling script is expected to catch and turn into a friendly message.
    """
    request = urllib.request.Request(
        url_for(path), headers={"User-Agent": "instructing-machines"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch(path: str, timeout: int = 60) -> str:
    """The same, for the files that are text — notebooks, manifests, pixi.toml."""
    return fetch_bytes(path, timeout).decode("utf-8")
