"""Generate the standalone pages from the widget fragments:

    nnw-widget.html        -> tiny-network.html  (one network widget)
    perceptron-widget.html -> perceptron.html    (one perceptron widget)

The fragments are the single source of the widgets. After changing one, run:

    python3 build_standalone.py
"""
from pathlib import Path

here = Path(__file__).parent

PAGES = [
    ("nnw-widget.html", "tiny-network.html", "Tiny Neural Network", '<div class="nnw"></div>'),
    ("perceptron-widget.html", "perceptron.html", "Perceptron", '<div class="pcp"></div>'),
]

for source, target, title, div in PAGES:
    fragment = (here / source).read_text()
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
</head>
<body style="margin:0; padding:16px; background:#ffffff;">
<!-- Generated from {source} by build_standalone.py; edit that file instead. -->
{div}
{fragment}</body>
</html>
"""
    (here / target).write_text(page)
    print(f"Wrote {target}")
