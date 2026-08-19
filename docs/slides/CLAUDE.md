# CLAUDE.md — `docs/slides/`

Rules for converting the Keynote lecture slides into Quarto revealjs decks. They
are derived from the hand-edited `week01-values-operators.qmd`, which is the
reference deck: when this file and that file disagree, that file wins.

`index.qmd` is a feature demo, not a style model. Copy conventions from
`week01-values-operators.qmd` instead.

---

## 1. Source material and the conversion procedure

The originals are `Slides.pptx` and `Slides.pdf` (a Keynote export) in the
sandbox folder. One `.qmd` per lecture unit, named `weekNN-topic-words.qmd`, one
file per "Uge N | topic" section slide in the deck.

Three sources, each authoritative for a different thing:

- **The `.pptx` XML** is authoritative for **text**. Walk `p:sp` shapes for
  prose and code, and walk `p:graphicFrame` → `a:tbl` → `a:tr` → `a:tc`
  separately for tables; a text-shape-only walk silently drops every table.
- **The `.pdf`** is authoritative for **layout**. Slice the pages and look at
  them.
- The `.pptx` shape geometry is **not** authoritative for anything. Grouped
  shapes report offsets in group-local coordinates, so the percentages disagree
  with what is rendered. Read positions off the PDF.

The PDF is not 1:1 with the pptx: Keynote collapses some build stages onto one
page and drops others entirely, and the offset drifts within a single lecture.
Build the page mapping empirically by matching `extract_text()` against the
slide dump before writing anything.

Slide text is **translated to English**. Keep the author's register: short,
spoken, occasionally funny. `Tanketjek` is `Mind check`, not `Conceptual check`.

Images are extracted from the `.pptx` into `images/` with a `wNN-` prefix
(`w01-vscode.png`, `w01-bruce-diagram.png`). Convert `.tif` to `.png`. Skip
decorations that carry no content — the small blue "try this" dot is a marker,
not an illustration, and does not survive the conversion.

Add each finished file to the `render:` list in `_quarto.yml`.

---

## 2. YAML header

Copy the header from `week01-values-operators.qmd` verbatim, changing only
`title` and `subtitle`. The parts that matter:

```yaml
format:
  revealjs:
    controls-layout: bottom-right
    slide-number: c
    classoption: fleqn
    fleqn: true
    mainfont: "Helvetica"
    syntax-highlighting: slides.theme
    code-line-numbers: false
    code-block-bg: false
```

`code-line-numbers: false` and `code-block-bg: false` are global, so code blocks
are bare by default and line numbers appear only where a slide asks for them.
`syntax-highlighting` lives **inside** the `revealjs:` block and points at
`slides.theme`, not at `../numpy.theme`. No `logo:` — it is commented out.

`title` is the lecture topic, `subtitle` is `"Week N"`.

---

## 3. Code on slides

**Never wrap code in a `::: {.code}` div.** Use a bare fenced block:

````
```python
print("Hello world")
```
````

The root font size in `slides.scss` is set so that plain code is already the
right size for projection. The `.code` / `.code-small` / `.code-big` /
`.code-huge` classes still exist but are not the default tool.

When a slide holds only a line or two, add `.large` to the fence:

````
```{.python .large}
"Hello world"
```
````

Options go in the fence attributes, not in a `#|` comment. `#|` is for
executable cells; inside a `{.python}` block it renders as a literal line of
code.

### Highlighting

Use `code-line-numbers` to walk through a program a line at a time. **Always
start the sequence with a bare `|`** so the first press shows the whole block
with nothing highlighted, and the first highlight is a deliberate step rather
than the state the slide opens in:

````
```{.python code-line-numbers="|1|2|3"}
````

Blank lines inside the block count as lines. Use one to separate two halves of
an example and skip its number in the sequence: `"|1|2|3|5|6"` for a six-line
block with a gap after line three.

### Animation

Repeat the `##` heading with `{auto-animate="true"}` on each state. Change as
little as possible between states so the eye tracks the one thing that moved.
When a reduction shortens a line, pad with leading spaces to hold the remaining
terms in their original columns:

````
```python
3 * 8 + 6
```
```python
  24  + 6
```
```python
    30
```
````

For substitution and reduction with variables, keep the assignment lines on
screen unchanged and change only the expression being worked on. Label the step
underneath the block, green for substitution and red for reduction:

```
[Substitution]{.fg style="--col: #2e8b57"}

[Reduction]{.alert}
```

### Annotations

Quarto code annotations are the way to comment on a line without a slide full of
prose:

````
```{.python .large}
print("Hello world") # <1>
```
1. It is alive!
````

---

## 4. Widgets

Widgets are not decoration and do not go on a slide because a slide could carry
one. A widget belongs on a slide when **the machine doing the thing is the
point** — above all `%%steps`, where the whole lesson is the sequence of
substitutions and reductions the widget prints.

Everything a student is meant to *try* stays in the notes and the exercises. The
"try this" slides in the Keynote originals become static code on the slide; they
do not become `%%sandbox` cells.

An executed cell needs its import in a `{python}` cell on the same slide:

````
```{python}
import steps_widget
```

```{python}
%%steps
3 + 2 * 4 + 9 # PRINT STEPS
```
````

---

## 5. Prose, lists and tables

Prose on a slide is a list. `slides.scss` no longer suppresses bullets, so use
`-` items and let them render as bullets. Do not use loose paragraphs where the
original slide had three points.

A one-line gloss under a heading is bold, not a `###` subheading:

```
**(a piece of code that reduces to a value)**
```

Tables go in a `::: {.large}` div so they read from the back of the room. One
table beats two: if the original split a single list of operators across two
columns purely to fit Keynote's layout, merge it back into one table. Position a
free-standing table with `.absolute` rather than a `layout` row:

```
::: {.large .absolute top="15%" left="5%"}
```

Reserve `::::: {layout="[...]"}` with `::: column` for a genuine two-up, such as
code beside its diagram.

---

## 6. Sections

Separate slide decks for each lecture using level one headers and three comment lines:

```
<!-- =============================================================================== -->
<!-- =============================================================================== -->
## Workflow
<!-- =============================================================================== -->
```

## 7. Slide furniture


Every top-level slide is bracketed by banner comments:

```
<!-- =============================================================================== -->
## Slide title
```

The continuation states of an animated or repeated-heading sequence do **not**
get banners — only the first slide of the group does, so the banners mark
lecture beats rather than key presses.

Keep the arrow-glyph reference block and the red-text reminder comment at the
top of every file, copied from the reference deck.

A section divider is a `#` heading bracketed by doubled banner lines. A
title-only divider slide in the original becomes one of these.

A full-bleed photograph is a heading-free background slide:

```
## {background-image="images/w01-computer-room.png" background-size="contain"}
```

Positioned images use `::: {.absolute top= left= width=}` with a separate
`.absolute` div for each caption. A single image that should fill the slide uses
`![](images/x.png){.r-stretch}`.

---

## 8. Trimming

The Keynote decks repeat a slide to fake a build. Where two consecutive slides
differ only by one added line, that is an `auto-animate` pair, not two slides.
Where a slide adds nothing — the same code shown twice with the same emphasis —
drop it.

Count the slides against the original when you are done and be able to say what
happened to every one of them.
