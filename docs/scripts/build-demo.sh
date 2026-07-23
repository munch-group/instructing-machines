#!/usr/bin/env bash
# Builds the vendored munch-group-jupyterlite submodule with this book's
# course notebooks baked in, and publishes the result at docs/demo/, so it
# renders at <htmlroot>/demo/ alongside the book.
#
# Called from the book's `post-render` (cwd = docs/), but safe to run by hand
# from anywhere too.
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

echo "==> Publishing to demo/"
rm -rf demo
mv "$LITE_DIR/dist" demo
