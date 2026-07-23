Quarto gives you three levels of control, from broadest to narrowest. Here's how they apply to your setup (a book of `.ipynb` chapters, Jupyter engine, no `execute:` block currently set — so everything is running on Quarto's defaults: code shown, output shown, warnings shown, errors fail the render).

## 1. Project-wide default — `_quarto.yml`

Add an `execute:` block (top-level, or nested under `format: html:` if you want it HTML-only) to set the default for every notebook:

```yaml
execute:
  echo: true       # show the source code (default: true)
  output: true      # show the cell's output (default: true)
  warning: false    # hide Python warnings (default: true)
  error: false      # false = a runtime error stops the render; true = print the traceback and continue
  freeze: auto      # cache execution; only re-run a notebook when its source changes
```

`freeze` is worth calling out even though you didn't ask: with 20+ notebooks as chapters, `freeze: auto` means `quarto render` only re-executes a notebook when its content actually changed, which will make your iteration loop much faster.

## 2. Per-notebook override — front-matter in the `.ipynb`

To override the project default for one chapter, add a **raw cell** (not code, not markdown) at the very top of the notebook containing YAML fenced by `---`:

```yaml
---
execute:
  echo: false
---
```

Anything set here overrides the project default just for that notebook.

## 3. Per-cell control — `#|` options inside the code cell

This is the one you'll use most. Quarto reads leading `#|` comment lines inside a code cell as options for that cell specifically — works the same in `.ipynb` code cells as in `.qmd` chunks:

```python
#| echo: false
#| fig-cap: "Sorting steps"
df.head()
```

Common ones:
- `echo: false` — run it, show only the output (good for demo output without cluttering with code)
- `output: false` — run it, show neither output (good for setup/import cells)
- `include: false` — run it, show nothing at all (still has side effects, e.g. defining a variable used later)
- `eval: false` — don't run it; just show the code as a static listing
- `code-fold: true` (+ `code-summary: "Show the code"`) — collapse the code behind a toggle, handy for keeping long chapters scannable while letting curious students expand it
- `output: asis` — treat printed output as raw Markdown/HTML rather than escaping it

**Alternative for `.ipynb` specifically:** instead of `#|` comments, you can tag a cell in Jupyter/VS Code's cell-tag UI with `hide-input`, `hide-output`, `remove-input`, `remove-output`, or `remove-cell` — Quarto recognizes these tags too. Functionally equivalent to the `#|` options above; use whichever fits your editing workflow. I'd lean toward `#|` comments since they're visible in the source and travel with git diffs, whereas tags live in cell metadata and are easy to lose track of.

## A couple of HTML-specific niceties for a teaching book

Since your notebooks are Python/bioinformatics-flavored, two more `format: html:` options are worth knowing about:

```yaml
format:
  html:
    df-print: paged     # pandas DataFrames render as a nice paged/sortable HTML table instead of a text repr
    code-tools: true     # adds a "</> Code" menu in the top-right to show/hide all code and view page source
    code-fold: false     # project-wide default for folding (per-cell/per-notebook can still override)
```

I noticed `docs/custom.scss` already has unused `.styled-output` CSS rules (`.cell-output`, `.cell-output-display`, etc.) that were clearly meant to wrap certain outputs, but no notebook currently applies that class — that's a leftover, not something active.

Want me to wire any of this up in `_quarto.yml` (e.g. `freeze: auto` plus `df-print: paged`, since those seem like clear wins for your setup), or were you just looking to understand the mechanism first?