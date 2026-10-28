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

# Query parameters become data- attributes on the widget div, so a link can preset the widget the
# same way the attributes do in Quarto, e.g.
#   perceptron.html?set=x1=0,x2=1,x3=1,w1=2,w2=2,w3=2,th=3&inputs=Weather,Company,Accessible
# The script runs before the widget's own script, which reads the attributes when it starts.
URL_PARAMS = """<script>
  new URLSearchParams(location.search).forEach((value, key) => {
    if (/^[a-z]+$/.test(key)) document.querySelector('{selector}').setAttribute('data-' + key, value);
  });
</script>
"""

for source, target, title, div in PAGES:
    fragment = (here / source).read_text()
    selector = "." + div.split('"')[1]
    params = URL_PARAMS.replace("{selector}", selector)
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
{params}{fragment}</body>
</html>
"""
    (here / target).write_text(page)
    print(f"Wrote {target}")
