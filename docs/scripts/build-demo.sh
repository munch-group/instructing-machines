#!/usr/bin/env bash
# Builds the vendored munch-group-jupyterlite submodule with this book's
# course notebooks baked in, and publishes the result inside docs/_book/demo/
# (the book's actual output-dir, which `quarto publish gh-pages` pushes to
# the gh-pages branch root) so it ends up reachable at <htmlroot>/demo/.
#
# Called from the book's `post-render` (cwd = docs/), so _book/ already has
# this render's output by the time this script runs. Safe to run by hand too.
set -euo pipefail

cd "$(dirname "$0")/.."   # docs/

LITE_DIR="jupyterlite"
CONTENT_DIR="$LITE_DIR/content/course"

echo "==> Syncing course notebooks into $CONTENT_DIR"
rm -rf "$CONTENT_DIR"
mkdir -p "$CONTENT_DIR"
for nb in notebooks/*.ipynb; do
  [ "$(basename "$nb")" = "snippet-cast.ipynb" ] && continue
  cp "$nb" "$CONTENT_DIR/"
done
cp -r notebooks/images "$CONTENT_DIR/images"

echo "==> Building JupyterLite ($LITE_DIR)"
pixi run --manifest-path "$LITE_DIR/pixi.toml" build

echo "==> Publishing to _book/demo/"
rm -rf _book/demo
mv "$LITE_DIR/dist" _book/demo
