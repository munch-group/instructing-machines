"""Where the course lives on the web.

You never run this file. It exists so that `get.py` and `update.py` cannot
disagree about the address of the course website: both of them ask this file.

If you are curious, the two functions below are the whole of it — one builds a
web address, the other downloads it and hands back the text.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

# Where the course folder is published. Change this if the website moves.
BASE_URL = "https://munch-group.org/instructing-machines"

# The folder this file is in — that is, the course folder itself.
HERE = Path(__file__).resolve().parent


def url_for(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def fetch(path: str, timeout: int = 60) -> str:
    """Download BASE_URL/path and return it as text.

    Raises urllib.error.URLError if the website cannot be reached, which the
    calling script is expected to catch and turn into a friendly message.
    """
    request = urllib.request.Request(
        url_for(path), headers={"User-Agent": "instructing-machines"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")
