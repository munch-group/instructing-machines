# Instructing Machines — logo assets

## Files

| Prefix | Use |
|---|---|
| `im-mark` | Icon only. Favicon, avatar, slide corner, Quarto `favicon:`. |
| `im-horizontal` | Default lockup. Title slides, course page header, handout footer. |
| `im-stacked` | Square-ish contexts. Poster, front page, anywhere width is tight. |

| Suffix | Use |
|---|---|
| *(none)* | Two-colour: purple `#7F77DD` ring, near-black `#1A1A18` prompt and wordmark. |
| `-au-blue` | Same, in Aarhus blue `#002546`, for official university material. |
| `-mono-black` | Single colour. Print, photocopies, embroidery, laser cutting. |
| `-mono-white` | Single colour white. **Only visible on a dark background** — it will look blank in a light image viewer. |

SVGs have transparent backgrounds and the wordmark converted to outlines, so no
font installation is needed anywhere. Prefer the SVG for anything that will be
scaled; the PNGs exist for tools that refuse SVG (some LMS uploaders, Word).

## Minimum sizes

The mark holds up to about 32px. Below that the gear teeth merge into the ring —
use a plain circle or drop the mark entirely. The horizontal lockup should not
go below roughly 200px wide, or the wordmark closes up.

## Clear space

Leave at least one gear-radius of empty space on all sides. The SVGs already
include a small internal margin; add the rest in your layout.

## Regenerating

`build_logo.py` produces every file here. To change the colour scheme, edit the
`PURPLE` / `INK` / `AUBLUE` constants at the top and re-run:

```bash
pip install fontTools cairosvg
python3 build_logo.py
```

The wordmark is Poppins Medium (SIL Open Font License), outlined at build time.
Swap `FONT` to any TTF/OTF path to change it.
