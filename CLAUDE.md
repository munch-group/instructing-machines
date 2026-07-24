# CLAUDE.md — Instructing Machines

Guidance for Claude (and collaborators) when writing or editing content in this repository.

**What this is.** *Instructing Machines* is a Quarto book of lecture notes, exercises, and tutorials for a 14-week introductory programming course for undergraduates in Molecular Biology and Molecular Medicine at Aarhus University. The audience has **no prior programming experience** and little sense of how a computer works. The goal is not to make programmers, but to build abstract/computational thinking and the vocabulary to direct and verify AI-generated code. The course introduces an AI assistant **from week 1** in escalating "roles," and leans on a family of custom notebook widgets.

**Read first.** The full course design lives in `docs/planning/course-plan.md` (learning goals, the 14-week distribution, the AI-role ladder + licence badges, the logbook, the widget mapping, tooling). The one-page student mental-model visual is `docs/planning/machine-map-poster.html`. Anything below is downstream of that plan.

---

## 1. Format conventions

**Author in Markdown now; target is Quarto-rendered notebooks later.** The end state is Jupyter notebooks (`.ipynb`) rendered by Quarto to HTML and PDF, so a student can *read* a note on the web or as PDF **and** download the same note as a notebook to do the small interspersed exercises. For now we develop everything as plain Markdown (`.md`) because it is easier to write and diff; conversion to `.ipynb` happens later.

Practical implications while authoring in Markdown:

- Write so the content converts cleanly to a Quarto `.ipynb`: use the Quarto conventions already in the book — `## Heading {#sec-anchor}` section anchors, `@sec-...` / `@fig-...` cross-references, `::: {.callout-note}` / `.callout-important` / `.callout-tip` admonitions, `::: {.column-margin}` for side tables, and fenced code with `{.txt filename="Terminal"}` for terminal transcripts.
- **Prefer runnable code over hand-typed output.** The single biggest source of defects in the existing notes is hand-written program output and error messages that have drifted from what current Python prints (see §4). When a note is converted to a notebook, code cells should *execute* so Quarto renders authoritative output. While in Markdown, mark clearly which blocks are meant to run.
- **Small exercises are interspersed**, not dumped at the end. Each exercise is a separate cell using the `%%exercise` magic (from `script-widget`) so it runs in isolation like a small script. When drafting in Markdown, write each exercise as its own fenced block tagged so it can become an `%%exercise` cell.
- Cross-reference style must be consistent: `@fig-x` and `@sec-x` (bare, not bracketed). The existing notes mix `[@fig-x]` and `@fig-x` — use the bare form.

---

## 2. Writing-style guide (Kasper's voice)

New notes must sound like the author. The voice is warm, funny, and rigorous. Concretely:

**Person and stance.** Second-person address to the student ("you"), with a visible first-person demonstrator ("If I do it, I get…", "let me introduce the if-statement"). Reassuring and low-anxiety, especially right after something looks like it failed ("It seems that nothing happened, but…"). Encouraging, never condescending.

**Introduce by doing, then name.** The reader *writes and runs* something first; only afterward does the text say what it was called and why it worked ("What you just wrote is called a *for-loop*"). Follow the preface's two principles: introduce each concept so it can be applied immediately on top of what the student already knows, and cover only the minimum needed before practice takes over.

**Predict-then-run is the core exercise device.** Almost every exercise says some version of *"Decide what you think will happen before you run it, then run it to check."* Preserve this relentlessly. Pair it with the rule that students **type code, never copy-paste** it (Oath 1).

**The substitution & reduction mantra.** The spine of the whole book is the mental model of evaluation as step-by-step *substitution* (variables → values) and *reduction* (expressions → simpler expressions → a single value). The phrase "do all the substitution and reduction steps in your head" recurs by design. This is what the `myiagi`/`pysteps`/`steps-widget` tools drill. Keep it central.

**Signature rituals and devices — reuse these:**

- **Oaths.** Numbered, first-person vows in `::: {.callout-important}` blocks, staged physically ("Raise your right hand!… You can take your hand down now"). Three exist across the course (Oath 1: never copy-paste; Oath 2: lines run top to bottom; Oath 3: consciously trace every substitution/reduction). New rituals should match this register.
- **Anthropomorphism.** Methods vs. functions framed as *"Hey string, capitalize yourself!"* vs. *"Hey function, capitalize this string!"*. Python is "nice like that"; a string "knows how to serve one character at a time."
- **"Peek behind the curtain" dunder reveals.** A running thread: `__add__`, then `__len__`/`__contains__`, showing that operators and built-ins dispatch to special methods. Bookends the "everything is an object" arc — keep it.
- **FAQ callouts and pop-culture hooks.** Mock-FAQ asides ("*Q: Isn't 'If' a poem by Rudyard Kipling? A: Yes.*"), Karate-Kid "wax on, wax off," "It's alive!" Frankenstein energy. Blunt trust-me asides ("Do not call your file `math.py`. It may bite you later. Just trust me on that one.").
- **Memorable example casts.** Danish/everyman names (Mogens, Preben, Henning, Heinz, Giovanni) and biology/food examples (DNA strings like `'ATGTAG'`, bananas, species counts, kroner, codons/amino acids). New examples should favour the molecular-biology domain where natural.
- **Rhythm.** Short imperative micro-instructions; rhetorical-question-then-answer ("What is an *iterable*, you may ask? It is…"); occasional `:-)`; gentle overload warnings ("your brain may overheat and explode — we have seen that happen").

**Formatting habits.** Italic one-line chapter abstract at the top; `#### Exercise` headings; `.column-margin` reference tables for operators/types; admonition callouts for tips/important points; `$…$`/`$$…$$` for arithmetic where it aids clarity.

**Two cautions from the audit:**

- **Don't let the voice drift.** `classes.ipynb` is the cautionary example — after a strong authored opening it collapses into generic reference-manual prose with zero exercises. New notes must keep the warm, exercise-dense voice all the way through.
- **Label intentional bugs.** The notes deliberately plant bugs so students learn to read tracebacks — but they are not visually distinguished from accidental typos. In new material, mark deliberate-bug exercises with an explicit callout (e.g. a "spot-the-bug" admonition) so students (and the AI) can tell them apart.

---

## 3. The AI thread and the widgets (how new notes integrate them)

Full detail is in `docs/planning/course-plan.md`; the essentials for authoring:

- **AI from week 1, in escalating roles.** Each note that uses the assistant states the sanctioned **role** for that context via a licence badge — the cumulative ladder is Explainer → Translator → Illustrator → Comparer → Drafter → Unreliable Narrator → Worker → Collaborator → Delegate. Exercises carry either a role badge (🟢 `AI: Drafter`) or 🔒 `SOLO` (do it yourself first). The AI lives in the **browser** (Copilot Chat), never inside the editor; VS Code is the AI-free space.
- **The rule that ties AI to the widgets:** *"the AI predicts; the widget proves."* Whenever the assistant claims what code does, students check it with the machine.
- **Logbook.** A term-long student artifact — one weekly entry: what the AI got right, what it got wrong, how they knew. New weekly notes should prompt an entry.
- **Widgets — where each fits when authoring:**
  - `steps-widget` (`%%steps`, `# PRINT STEPS`): substitution/reduction traces — the evaluation, precedence, and logic notes.
  - `puzzle-widget` (`%%puzzle <result>`): reorder shuffled lines — the "unscramble the statements" exercises (already present in precedence/general/data_structures) and truthiness/keyword drills.
  - `codelens-widget` (`%%codelens`, Python Tutor): step through execution with heap/reference diagrams — objects, **list/dict aliasing and shared references**, function call frames/scope, `__init__`, nested loops.
  - `turtle-widget`: visual functions/loops — the safe first place to let the AI "Draft" because output is visually checkable.
  - `script-widget` (`%%exercise` / pretend-script cell): the isolation model and every interspersed exercise.
  - `snippet-cast`: teacher tool for narrated walkthroughs and human–AI transcript videos; also a student "narrate your own code" assessment.

---

## 4. Quality checklist for new and revised notes

The audit of the existing notes surfaced recurring, avoidable defects. Do not reproduce them:

1. **No hand-typed output/error transcripts.** Render output from executed cells. Where a transcript must be static, use *current* Python wording (e.g. `SyntaxError: unterminated string literal (detected at line 1)`, `SyntaxError: unmatched ')'`), not pre-3.8 text.
2. **Code and prose must agree on identifiers.** The notes are riddled with mismatches (`number` vs `numbers`, `result` vs `results`, `is_palindome` vs `is_palindrome`, `chrous_text`/`chrorus_text`, `square_numbers` vs `squared_numbers`, `tmp` vs `temp`). Every identifier in prose must match the code exactly. A "run every code cell" check catches the NameErrors.
3. **Quarto syntax hygiene.** No four-backtick fences; anchors are `{#sec-x}` (brace, not `)`); close every inline-code backtick; keep punctuation *outside* code spans (`` `def` ``, not `` `def,` ``).
4. **Cross-reference style consistent** (`@fig-x`, `@sec-x`, bare). Verify every `@sec-`/`@fig-` target resolves in the assembled book (several currently point across chapters).
5. **No European decimal grouping** in English prose (`170,000`, not `170.000`).
6. **Refresh dated examples** (Trump family etc. — the author has already TODO'd these) toward neutral or biological data.
7. **Copyedit pass.** Recurring typos to watch: "his"→"this", "source"→"course", "stings"→"strings", "substations"→"substitutions", "Celcius"→"Celsius". Danish-authored spellings leak in.
8. **Modern idioms.** Introduce `with open(...) as f:` for files (the notes teach only the `close`-heavy form); soften "dictionary order is arbitrary" to "don't rely on order" (dicts preserve insertion order since 3.7).
9. **Keep it in scope.** Calibrate for absolute-beginner molecular-biology students. `classes.ipynb`-style material (multiple inheritance, mixins, MRO, static/class methods, SOLID) is over-scoped; defer to an optional appendix.

---

## 5. Per-note catalog

Status legend: **Solid** = reusable after a copyedit; **Needs work** = good bones, real fixes required; **Stub** = little/no content, write from scratch; **Infra** = tooling/appendix.

### Front matter & thesis chapters
- **preface.ipynb** — *Solid.* States the two pedagogical principles and the inviting tone; the reference voice for the book. Fixes: book title is *Learn Python the Hard Way* (not "Learning"); verify the GitHub issues link. Reuse: add a paragraph planting the "AI as a new layer of instruction" thesis and the week-1 assistant.
- **machine-insides.ipynb** — *Stub (prime slot).* Lorem-ipsum placeholder. This is where the "what's inside the machine" content goes (hard disk / memory / CPU / interpreter) — anchor it to `docs/planning/machine-map-poster.html`. Give it a real `{#sec-}` anchor.
- **history-of-instruction.ipynb** — *Stub (prime slot).* Outline only, but the heading arc (Machine instructions → Compilers → Interpreted languages → AI) is exactly the central thesis: each era adds a layer of translation between human intent and silicon, and the AI is the newest "layer of compilation." Stage it so students derive *"but is it really like a compiler?"* themselves (see plan §2). Write the content; add an anchor.

### Part: You and your machine
- **getting_started.ipynb** — *Needs work.* Gentle terminal walkthrough (`pwd`/`ls`/`cd`) + install + Oath 1 — keep these. Cut: the orphaned "Installing Phasic" block, the "Dummy" exercise, the empty heading/cell, and the large commented-out Conda legacy. Fix: dead links `()`, "which include"→"includes", restore a **two-column OS command table** (live version is Mac-only despite dual-OS prose). Add: week-1 AI-assistant intro box; first real `%%exercise`.
- **course_tools.ipynb** — *Needs work.* Introduces `myiagi` and `pysteps` (the substitution/reduction drills) with the Karate-Kid metaphor. **Critical fix:** the worked example is arithmetically broken — `4 * 8` is written as `24` (needs `y = 6`, i.e. `4 * 6 + x`), and the "deduce y and x" text is wrong. Also the `pysteps` output says "Line 4 in test_studentfile.py" but the file is `myfile.py` line 3; the myiagi figure caption is copied from VScode; unify the `myiagi`/`Myagi`/`Miyagi` spellings. Reuse: pair with `%%exercise`; the modern equivalents are `steps-widget`/`puzzle-widget`.

### Part: Speaking the language
- **hello-world.ipynb** — *Needs work.* First program, running from the terminal, reading errors, strings/quotes, comments; Oath 2. Fix: quote inconsistency between code and shown error, a four-backtick fence, unbalanced paren in prose, and **update the error-message transcripts to current Python**. Reuse: ideal first Explainer exercise ("ask the assistant to explain this error, then judge it"); `codelens`/`puzzle` on the two-line print-order demo.
- **values-operators-logic.ipynb** — *Solid-ish / Needs work.* Values, operators, comparison/logical operators, truthiness & short-circuit, types, conversion. Excellent assignment-vs-substitution framing and "confirm the truth table in code." Fix: "are that are called", "I may sound weird"→"It", duplicate list number (4,4), a **duplicated exercise line** (`print("apple" and "")` twice), punctuation inside code spans. Reuse: `steps-widget` on precedence/short-circuit; split the long "Mixed exercises" into interspersed items; predict-then-check AI role.
- **precedence-steps.ipynb** — *Solid (keystone).* Precedence table, statements vs. expressions, and the substitution/reduction model + Oath 3. Highest-value note — preserve wholesale. Fix: "his"→"this" (×5), `result` vs `results`, `{#sec-puzzle)`→`}`, an unterminated inline-code target (`"Banana. "` should be `'Banana'`). Reuse: maps 1:1 onto `steps-widget` (traces) and `puzzle-widget` (the shuffled-statement puzzles, all verified solvable); caveat/cut the `and/or` one-line-ternary anti-pattern.
- **if-else.ipynb** — *Needs work.* Conditionals, truthiness, nesting, blocks/indentation, `elif`, via bus/cookie/DNA-base examples + FAQ humor. Fix: missing closing quote in an `if x` demo (won't run), `'Not thirsty, thanks or asking'`→"for asking", `7 = 7`→`y = 7`, "superstar"/"super star" mismatch. Weakness: no executed cells. Reuse: thin the long General-exercises block into interspersed puzzles; `codelens` for nested-if tracing; `puzzle` for the truthiness table.
- **functions.ipynb** — *Needs work.* Functions as reusable mini-programs via a song; `def`/`return`/`None`, args vs. params, local scope ("temporary little world"), built-ins. Strong "a call is substituted by its return value" refrain — keep it. Fix: mis-numbered list item, comma inside code span, `chrous_text`/`chrorus_text` NameError, `c == I` (unquoted) latent bug, celsius→Fahrenheit direction error and `celcius` spelling, "27"/"37" mismatch, missing comma in reserved-words list, several typos. Reuse: `codelens` for call frames/scope; the "delete the return / move def to bottom / find the bug" tasks are ideal escalating AI prompts.
- **objects.ipynb** — *Needs work.* Everything is an object with methods; string methods, docs navigation, `.format()`, dunders (`__add__`), indexing/slicing. Fix: **the demo alphabet `'abcdefghijklmnopqrstuvxyz'` is missing `w`** (recurs in ~5 cells incl. the reversed string); "list" said for "string" twice; "Linneaus"→"Linnaeus"; "is"→"are" for double-underscores. Reuse: keep the "Hey string, …yourself!" and dunder reveal; `codelens` on indexing offsets; turn method tables inline instead of relying on external doc links.
- **lists.ipynb** — *Needs work.* Ordered mutable containers; build/index/slice/`del`/`split`/`join`; a container-value aliasing exercise. **Critical fix:** flagship exercise uses `number[i]` but defines `numbers` → NameError (×3); stale intro says "lists and dictionaries"; stray quotes in "the`' in'`operator". Reuse: **prime `codelens` chapter** — add an explicit aliasing exercise (`a=[1,2,3]; b=a; b.append(4); print(a)`) the notes stop just short of; have students predict then adjudicate with codelens.
- **tuples.ipynb** — *Needs work (thin).* Immutable tuples vs. lists, packing/unpacking, the `a, b = b, a` swap. Fix: traceback shows `fruits[3]` but text says "second element" (use `fruits[1]`); `tmp`/`temp` drift; add the missing italic intro blurb; the swap is previewed in the body *and* posed as an exercise — delete the preview so the "aha" survives. Reuse: add a forward link (immutability → dict keys); light AI role.
- **dictionaries.ipynb** — *Needs work.* Key–value containers, access, nesting, `in`, and the closing `__len__`/`__contains__` reveal. Fix: intro "is"→"are" and duplicated "Dictionaries dictionaries"; an **orphaned note about replacing age 70→71 that doesn't match the code** (the real overwrite is `job`); soften "order is arbitrary." Reuse: replace the Trump-family example with a codon/gene-annotation dict (author already TODO'd); `codelens` on shared nested-dict references; assistant-as-collaborator "design a dict schema" task.
- **iteration.ipynb** — *Solid-ish / Needs work.* For-loops from first principles, iterables/`__iter__`, `range`, nested loops. Reusable almost as-is after fixes: "The,n"→"Then", a scrambled "second time they run `x`" sentence, garbled `__iter__` sentence, "first and last"→"start and step", missing "why" in the final line. Consider demoting the premature `__iter__` digression. Reuse: `codelens`/`steps` for the nested-loop and `range`-step examples.
- **list-comprehensions.ipynb** — *Stub.* Title + empty headings only. Write from scratch following the do-first pattern: show the for-loop-plus-`append` version (already taught) then reveal the comprehension as its compression — a natural side-by-side `puzzle`/`steps` moment and a good "refactor this loop, then judge the AI's version" task.
- **files.ipynb** — *Needs work.* File I/O: `open`/`write`/`close`/`\n`/`print(file=)`, reading, iterating a file. **Two real runtime bugs:** `print("Second line, file=f")` (the `file=f` is inside the string) and `open('workfile', 'r')` (missing `.txt`, raises the wrong error). Plus "stings"→"strings", "read a from". Reuse: introduce `with open(...) as f:`; `codelens`/`steps` to visualize the read cursor advancing; paste-the-traceback AI exercises.
- **classes.ipynb** — *Needs work (voice + scope).* Comprehensive OOP tour. **Two problems beyond typos:** (1) the voice collapses to generic reference prose with **zero exercises** — rewrite in the author's voice with interspersed practice; (2) it is badly over-scoped (multiple inheritance, mixins, properties, static/class methods, SOLID) — keep `Point`, `__init__`/`self`, instance methods, light `__str__`/`__len__`/`__getitem__`; defer the rest to an optional appendix. Fix: `is_palindrome("ATCGCTA") # False` is wrong (it's a palindrome → `True`); the truncated `codon_table` produces garbage protein output; `TreeNode` is undefined; "`__init__` … constructor" → initializer. Reuse: `codelens` for `__init__`/`super().__init__` and attribute assignment.

### Part: Expressing information
- **data_structures.ipynb** — *Solid (the model to imitate).* Practice-heavy: counting with dicts, bucketing, nested loops, matrices, guided `is_palindrome`. This is the exemplar for the "intersperse small exercises" goal and the authentic voice — keep essentially all of it. Fix: "The,n", "of cause"→"of course" + "if know"→"if we know", `square_numbers`/`squared_numbers` clash, a four-backtick fence, `i'`→`` `i` ``, "This larger [exercise]", "170.000"→"170,000". Reuse: convert `# Your code here` stubs to runnable cells + collapsible solutions; `puzzle` for the reorder-and-indent exercises; `codelens` for the matrix/nested-loop builders.

### Part: Defining truth
- **testing.ipynb** — *Needs work (AI-thread hub).* Why/how to test, hand-written boolean tests, the per-project test suites and their pass/fail transcripts. Make this the backbone of the AI-verification theme. Fix: **`is_palindome` (missing "r") repeated ×8** vs. `is_palindrome` in prose; "their code"→"your code"; the text promises **"four" cases but shows three**; the "Ran 16/14 tests" counts don't reconcile. Reuse: frame tests explicitly as how you verify AI-generated code; add `%%exercise` to write one failing then one passing test; expand rather than shrink.
- **general_exercises.ipynb** — *Solid.* Bite-sized exercises on types/coercion/precedence/tracing + two solvable scramble puzzles. Ideal `%%exercise`/widget fodder. Fix: "his"→"this" (×5), `results`→`result` (×2), stray "?." Reuse: fold inline next to the relevant concepts; add optional "ask the assistant to check your reasoning, then verify by running" prompts.

### Part: Tools of the trade
- **modules.ipynb / packages.ipynb / biopython.ipynb** — *Stubs, redundant.* All three circle "using code from other files / BioPython / Seq class." **Consolidate into one "reusing others' code" chapter.** Fix the duplicated tagline ("a bird's-eye view … modules classes" → "modules **and** classes"; `packages` also drops the apostrophe). Frame the AI assistant as the modern "giant's shoulders," a layer atop libraries you still must understand; show a worked `Seq`/`SeqIO` example the assistant helps write (understanding `Seq` object vs. string is the point).

### Part: Negotiating outcomes (the AI arc)
- **placeholder.ipynb** — *Stub.* The reserved slot for the AI material (weeks 8–14). Build from `docs/planning/course-plan.md` §7.

### Appendices & infra
- **recursion.ipynb** — *Stub.* Placeholder with PDF-workflow leakage (`\pagebreak`, "merge into the pdf" note) that must not ship. Good hidden angle to develop: "if you understand recursion, you understand functions too"; pair with an AI call-stack-tracing exercise.
- **appendix_bsf.ipynb** — *Infra.* Install appendix for students also taking BSF (Biomolecular Structure and Function) — Pixi + PyMOL. Not part of the pedagogy. Cut the large commented Conda legacy; standardize "PyMOL"; add an Apple-Silicon note (`osx-64` pin).
- **snippet-cast.ipynb** — *Infra (move out of `notebooks/`).* Developer scratchpad/demo for the `snippet_cast` tool, with hard-coded local paths — not a student chapter. Keep as an internal authoring demo.
- **references.ipynb** — *Infra.* Bibliography stub, machine-populated. Consider adding responsible-AI-use sources.
- **introduction.ipynb / widget-demo.ipynb** — not course chapters (a Phasic/coalescent tutorial and a widget showcase respectively); not in the book's chapter list.

---

## 6. Authoring a new note — quick checklist

1. Open with a one-line italic abstract; give the section a `{#sec-}` anchor.
2. Teach by doing → naming; keep the warm second-person voice all the way through.
3. Intersperse small `%%exercise` cells; every exercise is predict-then-run.
4. Reinforce substitution & reduction; reach for the matching widget (`steps`/`puzzle`/`codelens`/`turtle`).
5. State the AI **role/licence** for each exercise (badge), keep the AI in the browser, and prompt a logbook entry where appropriate.
6. Make all code runnable; never hand-type output. Label any deliberate-bug exercise.
7. Run the §4 quality checklist before calling it done.
