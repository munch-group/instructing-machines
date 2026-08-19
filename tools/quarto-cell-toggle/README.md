# Quarto Cell Toggle

A very small VS Code extension for authoring *Instructing Machines*. It flips the
selected notebook cell between an executable Python code cell and a markdown cell
holding the same code in a fence:

```
#  code cell                     markdown cell
x = 1                    <-->    ```python
print(x)                         x = 1
                                 print(x)
                                 ```
```

The point is the migration described in `docs/planning/checklist.md`: fifteen of the
seventeen Python chapters carry every example as a hand-typed markdown fence, and they
need to become cells that actually run. One keystroke per example, reversible.

## Install

Nothing to compile - it is plain JavaScript.

```bash
cd tools/quarto-cell-toggle
npm run install-local     # packages a .vsix and installs it into VS Code
```

If you would rather not package it, symlink the folder into your extensions
directory and reload the window:

```bash
ln -s "$PWD" ~/.vscode/extensions/quarto-cell-toggle
```

To run the tests (no VS Code required - the API is stubbed):

```bash
npm test
```

## Use

With a notebook focused and the cell selected but *not* being edited, press
<kbd>Alt</kbd>+<kbd>/</kbd>. The three commands are also in the palette:

- **Quarto: Toggle Cell Between Code and Fenced Markdown**
- **Quarto: Convert Fenced Markdown Cell to Code Cell** - forces the direction, and
  ignores the runnable-language guard
- **Quarto: Convert Code Cell to Fenced Markdown Cell**

Select several cells first and it converts all of them, deciding the direction per
cell.

## What it refuses to do

The whole risk in a bulk conversion is turning something into a code cell that was
never meant to run, so the guard rails matter more than the convenience:

- A markdown cell is only converted if it is **exactly one fenced block**, blank lines
  aside. Prose before or after the fence, two fences in one cell, or an unclosed fence
  all leave the cell untouched and report why.
- A fence whose language is not in `quartoCellToggle.runnableLanguages` is left alone.
  That is what protects the `{.txt filename="Terminal"}` transcripts - the shell
  sessions in `getting_started` would otherwise become code cells that raise on the
  first render. Use the explicit **to Code Cell** command to override.
- Converting a code cell that has outputs asks first, because the outputs and the
  execution count are discarded by the change of cell kind.

## What it preserves

The original info string is stashed in the cell's metadata as `quartoFence`, so a fence
that carries attributes survives the round trip: ```` ```{.python filename="demo.py"} ````
comes back with `filename="demo.py"` intact rather than flattened away. Other cell
metadata is carried across untouched.

A remembered info string that says nothing the language name does not - ```` ```{.python} ````,
```` ```{python} ```` - is *not* restored. Those come back as ```` ```python ````, because
that spelling is the one being migrated to and restoring the old one would undo the work.

## Settings

| Setting | Default | Meaning |
| --- | --- | --- |
| `quartoCellToggle.fenceStyle` | `plain` | ```` ```python ````, `braced-dot` for ```` ```{.python} ```` (shown, not executed), or `braced` for ```` ```{python} ```` (Quarto executes it) |
| `quartoCellToggle.runnableLanguages` | `["python", "py", "r"]` | Fence languages allowed to become code cells |
| `quartoCellToggle.defaultLanguage` | `python` | Language for a fence with no info string |
| `quartoCellToggle.confirmDiscardOutputs` | `true` | Warn before throwing outputs away |

`plain` is the default because it is the only spelling a notebook highlights. Jupyter
reads the info string as a bare language name, so ```` ```{.python} ```` renders as grey
unhighlighted text in exactly the cells this extension exists to author, while Quarto
understands all three. Every style is still *read* correctly, so a chapter written with
```` ```{.python} ```` converts to code cells as it always did.

If the aim is a cell Quarto will *execute*, you want a real code cell, not
```` ```{python} ```` - that form is for `.qmd` files.

## The no-extension alternative

If this ever feels like too much machinery, VS Code's built-in `runCommands` plus the
`notebookCellType` context key gets you a cruder version in `keybindings.json` with no
code at all. It cannot check the fence language or preserve attributes, and it deletes
the first and last line of a markdown cell without looking at them, so it will eat
prose cells if you misfire. That is the trade.
