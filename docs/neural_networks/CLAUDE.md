# Interactive neural-network widgets for teaching

Interactive HTML widgets used in lecture notes on the basics of neural networks, plus two sets of
predict-then-check exercises. The notes are published with **Quarto**; the widgets are plain
HTML/CSS/JS with no dependencies and no build step other than `build_standalone.py`.

## Files

| File | What it is |
|---|---|
| `nnw-widget.html` | **Source** of the network widget: a fragment with one `<style>` and one `<script>`. Turns every `<div class="nnw">` on a page into a widget. |
| `perceptron-widget.html` | **Source** of the perceptron widget (3 inputs, 1 neuron). Turns every `<div class="pcp">` into a widget. Uses its own `pcp-` class names, so both widgets can share a page. |
| `tiny-network.html`, `perceptron.html` | Standalone pages with one widget each. **Generated** by `build_standalone.py`; never edit them by hand. |
| `build_standalone.py` | Regenerates both standalone pages. Run `python3 build_standalone.py` after every change to a fragment. |
| `exercises.qmd` | Network exercises: 9 exercises + 3 challenges, one preconfigured widget before each, answers in collapsed callouts. |
| `perceptron-exercises.qmd` | Perceptron exercises: everyday decisions (8 exercises + 3 challenges, the last one XOR), same format. |
| `exercises.md` | Earlier plain-Markdown version of the network exercises (superseded by the `.qmd`). |
| `perceptron_examples.pdf` | The user's full course slide deck (843 pages, in Danish/English, 90 MB). The perceptron slides are pages 420–429 (Nielsen's festival example: Weather/Company/Accessible). Too large to read directly; extract text with macOS PDFKit via `osascript -l JavaScript`. |
| `*.html`, `*_files/` from Quarto | Render output; regenerate with `quarto render <file>.qmd`. |

## Using the network widget in Quarto

Load the widget code once per page, then place configured divs where widgets should appear:

```yaml
format:
  html:
    include-after-body: nnw-widget.html   # path relative to the .qmd (or set it in _quarto.yml)
```

````markdown
```{=html}
<div class="nnw" data-act="sigmoid" data-hidden="1" data-example="flat"></div>
```
````

Attributes (all optional) set the starting state, which the widget's **Reset** button returns to
(Reset is only shown when at least one attribute is given):

- `data-act`: `step` (default) | `sigmoid` | `relu`
- `data-hidden`: `1` | `2` (default) | `3`
- `data-example`: `flat` | `bump` | `stairs` | `random`; the example buttons are then hidden,
  leaving Reset (which returns to this example)
- `data-outact="true"`: tick "Apply f at output"; `data-contrib="true"`: tick "Show contributions"
- `data-set="v1=10, t1=2"`: extra slider values (keys `w1-w3`, `t1-t3`, `v1-v3`, `th`; −10..10)
- `data-theme`: `light` (default) | `dark` | `auto`
- `data-layout="side"`: plot, hint and formula in a second column right of the network; the max
  width grows to 1400 px, and below 900 px of widget width it falls back to the stacked layout
- `data-notes="false"`: hide the hint under the plot and the "where f(z) = …" line under the
  formula (the formula itself stays)
- `data-negative="false"`: weight sliders *w*, *v* run 0..10 (thresholds keep −10..10) and the
  plot's *x*-axis runs 0..10 instead of −5..5. Negative values from `data-set` are clamped to 0.
  The Bump button is hidden (with non-negative weights the output can only rise with *x*); Staircase
  centres its steps on *x* = 5; Random puts each step/kink at a random *x* in 1..9
- `data-thresholds="false"`: every threshold (θ₁–θ₃ and θ) is fixed at 0; their sliders are not
  drawn and the formula drops the "− θ" terms. Bump and Staircase are hidden

Any number of widgets per page is supported: each gets a unique id prefix (`nnw-`, `nnw1-`, …).

The perceptron widget works the same way (`include-after-body: perceptron-widget.html`,
`<div class="pcp" …>`), with these attributes:

- `data-example`: `and` | `or` | `maj` | `random`
- `data-set="x1=0, x2=1, x3=1, w1=2, w2=2, w3=2, th=3"`: inputs 0..1, weights and threshold −10..10
- `data-inputs="Weather, Company, Accessible"`: names shown above the three input sliders
- `data-output="Go to the festival"`: name shown under the output arrow
- `data-examples="false"`: hide the example buttons (the whole toolbar if Reset is not shown either)
- `data-formula="false"`: hide the formula below the diagram
- `data-theme` as above

`data-examples` and `data-formula` only change what is shown, so on their own they do not make the
Reset button appear.

The standalone pages take the same attributes as URL query parameters, without the `data-` prefix
(`build_standalone.py` adds a small script that copies them onto the div before the widget starts):
`perceptron.html?set=x1=0,x2=1,x3=1,w1=2,w2=2,w3=2,th=3&inputs=Weather,Company,Accessible&output=Go%20to%20the%20festival`,
`tiny-network.html?act=relu&hidden=3&example=random`, `tiny-network.html?negative=false&thresholds=false`.

## The model (network widget)

- *hᵢ = f(wᵢ·x − θᵢ)*, *y = Σ vᵢ·hᵢ − θ*, or *y = f(Σ vᵢ·hᵢ − θ)* with "Apply f at output".
- Step: *f(z) = 1 if z ≥ 0 else 0* (note *f(0) = 1*). Sigmoid, ReLU also available.
- Sliders for all weights and thresholds run −10..10 in steps of 0.1.
- Input *x* is set by hovering over the plot area (not its margins); it returns to 0 when the
  pointer leaves the plot. Plot: *x* in −5..5 (0..10 with `data-negative="false"`), *y*-axis **fixed** at ±25.
- Examples: **Flat** (all *w* = 1, all thresholds 0, all *v* = 0 → flat *y* = 0; this is also the
  state on page load; keeps activation and neuron count), **Bump** (2 neurons, step), **Staircase**
  (one step per hidden neuron, levels centred on 0), **Random** (for ReLU: every kink visible).

## Design decisions agreed with the user (keep them)

Colours and drawing
- Positive = green `#0d9488`, negative = red `#dc2626` (edges, node outlines, slider values).
- All nodes gray; node outline colour follows the sign of its threshold and its width grows with
  |threshold| (same scale as edge width vs |weight|). Edges never overlap nodes (opaque node discs).
- Plot curve dark gray; contribution lines blue / magenta / amber (colours not used in the network).
- No frame around the widget; slider boxes are transparent.

Sliders
- Light-gray handle, white track with a hairline black outline, pale-gray fill.
- Label `w₁:` / `θ:` left of the bar; weight and threshold **values centred above the bar**.
- Slider text scales with the drawing exactly like node labels (numbers 15, names 18 diagram units
  out of 710 across); the bar keeps a fixed 18 px thickness, only its length changes.
- Placement (computed in `placeSliders()`, redone on every resize):
  - weight sliders sit above their edge midpoint, 1 px clear of the widest possible edge
    (≈ 4 px between edge and handle at default size), so they are evenly spaced; on sloped edges
    the line may cross the ends of the slider row (accepted);
  - threshold sliders sit above their node and are pushed up until every edge is ≥ 1 px away
    (measured perpendicular to the edge, at maximum edge width);
  - hidden-neuron spacing grows until nothing collides, then +20 %, with the top and bottom hidden
    neurons at least 300 units apart.
- Layout: network on top, plot below, hint and formula underneath; widget max width 760 px.

Perceptron (`perceptron-widget.html`)
- Inputs x₁–x₃ are slider rows (0–1) instead of nodes; edges start just right of each row.
- One neuron *y* (no pass-through output node); output arrow shows just the value and is as long
  as the incoming edges; inputs spaced half an edge length apart.
- Weights and threshold −10..10 (so the slide examples, e.g. w₁ = 6, can be used as they are);
  step activation only, firing when Σ wᵢxᵢ ≥ θ (the slides use >; exercises avoid exact ties so
  both agree); examples AND, OR, Majority, Random.
- Input sliders need a minimum width of 110 px (value beside the bar); weight and threshold rows
  only 70 px. On narrow screens the threshold row and a long output name are shifted left to stay
  inside the drawing.
- Weight rows aligned in one column, evenly spaced; w₂ above its horizontal edge, w₃'s bar centred
  on its edge, w₁ placed for equal spacing. Input values right of the bar (gap = name-to-bar gap);
  weight/threshold values above the bar. Formula below the network; widget max width 1080 px.

## Working on the widgets

- Edit the fragment (`nnw-widget.html` or `perceptron-widget.html`), then run
  `python3 build_standalone.py`. The two widgets share their design but not their code: a design
  change meant for both must be made in both fragments.
- Check syntax: extract the `<script>` and run `node --check` on it.
- Preview: serve the folder (`python3 -m http.server 8777`) and open
  `http://localhost:8777/tiny-network.html`; `file://` URLs are blocked in the app's browser pane.
- Verify layout changes numerically in the browser, at several widths (e.g. phone, ~600 px, the
  width cap) and for 1–3 hidden neurons with all sliders at ±10: no slider/node/label overlaps,
  threshold sliders ≥ 1 px from edges, values fit, and the drawing height stays sensible. Test inside
  a rendered Quarto page too: its text column on a phone is narrower (≈ 292 px) than a standalone page.
  Visual inspection alone has missed problems.
- Known limitation: at phone width the bars get short and the diagram is cramped.

## Exercises

- Style: each exercise starts from a preconfigured widget, then 1–5 single slider changes; students
  predict before changing the slider; answers are hidden (collapsed callouts in Quarto).
- Every answer was verified by driving the widget (setting sliders and reading the "y = …" output
  at chosen *x* values). Re-verify after any change to the widget's maths, presets or ranges.
- Use only values the sliders can reach (−10..10) and large enough to be visible on the ±25 axis.
- Perceptron exercises: avoid exact ties (weighted sum = θ), e.g. whole-number weights with
  half-number thresholds, so the widget's ≥ and the slides' > give the same answer.

## The user

Kasper teaches the basics of neural networks and publishes lecture notes with Quarto. Prefers
careful planning, asking before hard-to-reverse choices, and verified results.
