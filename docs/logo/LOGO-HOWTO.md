# Rebuilding the logo

`build_logo.py` generates every logo file from one source of truth: the
JetBrains Mono outlines plus four hex values. You run it when you change the
name, a colour, or the caret proportions, never edit the SVGs by hand, because
the next run overwrites them.

## 1. One-time setup

**The font.** fontTools draws the *default instance* of a variable font, so
`JetBrainsMono[wght].ttf` would silently come out at Regular 400 instead of
Medium. You need the static Medium:

```
curl -L -o JetBrainsMono.zip https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
unzip -j JetBrainsMono.zip 'fonts/ttf/JetBrainsMono-Medium.ttf' -d .
```

Put the file in the same directory as `build_logo.py`. The script also looks in
the usual system font directories; if it finds nothing it stops with an error
rather than rendering the wrong weight.

**The Python packages.**

```
pip install fonttools cairosvg
```

`cairosvg` needs the Cairo C library. macOS: `brew install cairo pango`.
Debian/Ubuntu: `apt install libcairo2 libpango-1.0-0`. If Cairo is more trouble
than it's worth, see step 4, you can skip the PNGs.

## 2. Run it

```
cd docs/logo
python build_logo.py
```

Output goes to the script's own directory, so `docs/logo/`. To send it
elsewhere:

```
IM_LOGO_OUT=/tmp/logo python build_logo.py
```

It prints the font it resolved and the files it wrote. Check the font line on
the first run, that is where a wrong-weight mistake shows up.

## 3. What comes out

| File | Where it goes |
|:--|:--|
| `im-prompt.svg` | the lockup; README, slides, anything print |
| `im-prompt-1200px.png` `-2400px.png` | raster fallback, social cards |
| `im-prompt-mono-black.svg` | one-colour, for faxes and embroidery |
| `im-prompt-mono-white.svg` | for placing on any dark background |
| `im-prompt-au-blue.svg` | AU-blue, for university templates |
| `im-prompt-on-dark.svg` | pre-composed on `#00303C`, lightened hues |
| `im-mark.svg` + `-16/32/64/180/512px.png` | favicon and touch icon |
| `im-mark-ink.svg` `im-mark-au-blue.svg` | alternate mark backgrounds |
| `im-stacked.svg` | mark over name, for square crops |

The header on the site does **not** use any of these, it is live text styled by
`.im-header` in `custom.scss`. These files are for everywhere you cannot ship
CSS: GitHub, PDFs, slides, the favicon.

## 4. Wiring up the favicon

In `_quarto.yml`:

```yaml
format:
  html:
    favicon: logo/im-mark-32px.png
```

For the Apple touch icon, add to `include-in-header`:

```html
<link rel="apple-touch-icon" sizes="180x180" href="logo/im-mark-180px.png">
```

If you skipped `cairosvg`, delete the `for wpx in PNG_WIDTHS[name]` loop at the
bottom of the script and point `favicon:` at `logo/im-mark.svg` instead, every
current browser accepts an SVG favicon.

## 5. Changing things

All the knobs are at the top of the file or in the function signatures.

**Colours.** `TEAL` is the prompt, `CARET` the block cursor, `INK` the name.
`TEAL` must stay equal to `$primary` in `custom.scss`, and `CARET` equal to
`$lp-caret`, or the SVG and the live header drift apart.

**The name.** `TEXT = "instructing machines"`. Lowercase is deliberate, it is a
typed command. Capitalise it and the caret starts looking like a stray box.

**Caret proportions.** `build_prompt(caret_w=0.50, caret_h=0.78)`, as fractions
of the em. `caret_h=0.73` matches the cap height exactly, which is more correct
and slightly less assertive; `0.78` is what the design used, sitting a little
above the caps.

**Prompt-to-name gap.** Currently one real monospace cell, computed from the
font, so the lockup is literally the string as typed. To tighten it, change
`x_name = w_prompt + cell` to `w_prompt + cell * 0.7` in `build_prompt`.

**A new variant.** Add an entry to `VARIANTS` and a matching one to
`PNG_WIDTHS`, both dicts are keyed by output filename. For example, a version
on the teal:

```python
VARIANTS["im-prompt-on-teal"] = build_prompt(
    ink=PAPER, prompt_col="#BFE6ED", caret_col=PAPER, bg=TEAL)
PNG_WIDTHS["im-prompt-on-teal"] = [1200]
```

## 6. Checking the result

Open `im-mark-16px.png` at 100% and look at it small. That is the size at which
the old gear failed. If the chevron and underscore are still two distinct marks
at 16px, the geometry is holding; if they merge, raise `stroke-width` from
`s * 0.08` in `_mark_body`.
