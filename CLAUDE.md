# CLAUDE.md — Instructing Machines

Guidance for Claude (and collaborators) when writing or editing content in this repository.

**What this is.** *Instructing Machines* is a Quarto book of lecture notes, exercises, projects, and tutorials for a 14-week introductory programming course for undergraduates in Molecular Biology and Molecular Medicine at Aarhus University. The audience has **no prior programming experience** and little sense of how a computer works. The goal is not to make programmers, but to build abstract/computational thinking and the vocabulary to direct and verify AI-generated code. The course introduces an AI assistant **from week 1** in escalating "roles," and leans on a family of custom notebook widgets.

**Read first.** The authoritative course design now lives in `docs/planning/course-design.qmd` — it is both the plan and the second chapter of the book, and it holds the guiding principles, the week-by-week grid, the learning curve and cliffs, the AI-role ladder, the tool schedule, the workload shape, and the open decisions. The one-page student mental-model visual is `docs/planning/machine-map-poster.html`. The `weekplan.qmd` of the existing bioinformatics course, whose Python sequence and pace this course matches, is archived at `docs/planning/old_weekplan.md`. (The old `course-plan.md` has been folded into `course-design.qmd` and no longer exists.) Anything below is downstream of the design doc, with one exception: **`docs/_quarto.yml` is the authoritative week plan.** It is what the book actually renders, so where it and any prose document disagree about which chapter falls in which week, it wins. Each `- part: "Week N"` carries three annotations — `Python:` for what the week teaches, `AI:` for the ladder rung it licenses, `Workload:` for what it costs a student — and the outstanding work on each chapter sits as a `CLAUDE:` comment under the chapter's own line.

---

## 0. Repository layout

The book is now organized **by week** in `docs/_quarto.yml` (Part: Week 1 … Week 14), interleaving programming notes, AI-arc notes, and projects in teaching order. Content is split across folders by kind:

- **`docs/python/`** — the programming lecture notes (`.ipynb`) plus the four worked-example/clinic notes (`.qmd`: `composition`, `decomposition`, `debugging`, `dataframes`).
- **`docs/ai/`** — the AI arc: the week-1 machine/AI framing (`insides.md`, `instruction.md`, `meet-ai.qmd`), the short weekly AI beats and clinics (`.qmd`), and the five long conceptual notes (`.md`). This is where most of the recent writing has happened; it is now largely drafted.
- **`docs/projects/`** — one `.qmd` chapter per project describing the task (not the code). Eight are in the book; `curration-project.qmd` (an exam-derived curation assignment) is written but held out of the book.
- **`project-files/`** (repo root, **not** under `docs/`) — the runnable project code students download: each project dir has `<project>.py` (stub), `test_<project>.py` (the pytest suite), data files, `<project>_solution.py.encrypted`, and `solution_walkthrough.ipynb`. `hivproject/` also has `recap.py`, the provided resource module.
- **`docs/blocks/`** — "building blocks": planned mini-pages for single concepts (assignment, expression, for-loop, if-statement, …) to be cross-referenced and used as hover tooltips. Only a `for-loop.ipynb` stub and a `README.md` exist so far.
- **`docs/planning/`** — `course-design.qmd`, `machine-map-poster.html`, `old_weekplan.md`.
- **`docs/slides/`**, **`docs/videos/`**, **`docs/jupyterlite/`** (a git submodule), **`docs/_extensions/`**, `docs/index.qmd` (landing), `docs/notes.qmd` (scratch), `docs/AI-opening.qmd` (scratch "recent AI news" page), `docs/quarto-publishing.md` (authoring reference for Quarto render options).

The `im_pytest` / pytest check-widget that runs the project suites lives in a **separate widget repository**, not here; `docs/python/testing.ipynb` refers to it as "the project testing utility."

---

## 1. Format conventions

**Chapters are a mix of `.ipynb`, `.qmd`, and `.md`, rendered by Quarto to HTML (PDF later).** The programming notes are `.ipynb`; the AI arc and the clinics are `.qmd`/`.md`. A student should be able to *read* a note on the web **and** download the same note as a notebook to do the small interspersed exercises.

Two practical realities to keep in mind:

- **The `.ipynb` notes are still authored as a single markdown cell** — code appears as fenced text, not as executable code cells (`code0` in almost every notebook). The end state is real executable cells so Quarto renders authoritative output, but that conversion has **not** happened yet. Until it does, code and its shown output are hand-written and drift-prone (see §4).
- **Prefer runnable code over hand-typed output.** The single biggest source of defects in the notes is hand-written program output and error messages that have drifted from what current Python prints. When you convert or add cells, make them *execute*. While still in a single markdown cell, mark clearly which blocks are meant to run.

Quarto conventions already in use, and to keep consistent: `## Heading {#sec-anchor}` section anchors, `@sec-…` / `@fig-…` cross-references (bare, not bracketed), `::: {.callout-note}` / `.callout-important` / `.callout-tip` admonitions, `::: {.column-margin}` for side tables, fenced code with `{.txt filename="Terminal"}` for terminal transcripts, and the exercise widget magics (`%%sandbox`, `%%steps`, `%%puzzle`, `%%codelens`). Small exercises are **interspersed**, not dumped at the end.

---

## 2. Writing-style guide (Kasper's voice)

There are now **two registers** in the book, and you should match the one belonging to the folder you are editing.

**The programming notes (`docs/python/`) use the warm authorial voice.** It is warm, funny, and rigorous. Concretely:

**Person and stance.** Second-person address to the student ("you"), with a visible first-person demonstrator ("If I do it, I get…", "let me introduce the if-statement"). Reassuring and low-anxiety, especially right after something looks like it failed ("It seems that nothing happened, but…"). Encouraging, never condescending.

**Introduce by doing, then name.** The reader *writes and runs* something first; only afterward does the text say what it was called and why it worked ("What you just wrote is called a *for-loop*"). Follow the preface's two principles: introduce each concept so it can be applied immediately on top of what the student already knows, and cover only the minimum needed before practice takes over.

**Predict-then-run is the core exercise device.** Almost every exercise says some version of *"Decide what you think will happen before you run it, then run it to check."* Preserve this relentlessly. Pair it with the rule that students **type code, never copy-paste** it.

**The substitution & reduction mantra.** The spine of the whole book is the mental model of evaluation as step-by-step *substitution* (variables → values) and *reduction* (expressions → simpler expressions → a single value). The phrase "do all the substitution and reduction steps in your head" recurs by design. This is what the `myiagi`/`pysteps`/`steps-widget` tools drill. Keep it central.

**Signature rituals and devices — reuse these:**

- **Anthropomorphism.** Methods vs. functions framed as *"Hey string, capitalize yourself!"* vs. *"Hey function, capitalize this string!"*. Python is "nice like that"; a string "knows how to serve one character at a time."
- **"Peek behind the curtain" dunder reveals.** A running thread: `__add__`, then `__len__`/`__contains__`, showing that operators and built-ins dispatch to special methods. Bookends the "everything is an object" arc — keep it.
- **FAQ callouts and pop-culture hooks.** Mock-FAQ asides ("*Q: Isn't 'If' a poem by Rudyard Kipling? A: Yes.*"), Karate-Kid "wax on, wax off," "It's alive!" Frankenstein energy. Blunt trust-me asides ("Do not call your file `math.py`. It may bite you later. Just trust me on that one.").
- **Memorable example casts.** Danish/everyman names (Mogens, Preben, Henning, Heinz, Giovanni) and biology/food examples (DNA strings like `'ATGTAG'`, bananas, species counts, kroner, codons/amino acids). New examples should favor the molecular-biology domain where natural.
- **Rhythm.** Short imperative micro-instructions; rhetorical-question-then-answer ("What is an *iterable*, you may ask? It is…"); occasional `:-)`; gentle overload warnings ("your brain may overheat and explode — we have seen that happen").

**Formatting habits.** Italic one-line chapter abstract at the top; `#### Exercise` headings; `.column-margin` reference tables for operators/types; admonition callouts for tips/important points; `$…$`/`$$…$$` for arithmetic where it aids clarity.

**The AI-arc notes (`docs/ai/`) use a deliberately plainer register**, per Kasper's explicit instruction: continuous prose, more of it, with **no bold, no bulleted or numbered lists, no emoji/icons, no em-dashes, and no fancy paragraph titles** — concentrate on the content, not the voice. The five long conceptual notes (`insides.md`, `instruction.md`, `reading-and-judging.md`, `tests-are-the-contract.md`, `plan-before-you-prompt.md`, `delegate-the-full-problem.md`, `surviving-ai.md`) are pure prose in this style. The shorter AI beats and in-class clinics (`.qmd`) add a light session scaffold on top of that prose: a `## Session length` note, `## Part 1 / ## Part 2` segments, and `#### Exercise` blocks carrying an `AI: <Role>` or `SOLO` badge. When editing an AI-arc note, keep the plainer register; do not import the Python notes' bold/list/emoji habits.

**Overused words and constructions to avoid (both registers).** These are tics of AI-generated prose rather than Kasper's, and they have accumulated across the notes. Do not reach for them when drafting, and rewrite them when you find them:

- **"points out"** — for a person or a text drawing attention to something, prefer "says", "shows", "notes", or recast the sentence so the thing itself does the work.
- **"not X but Y"** — the corrective-contrast frame. Occasionally it earns its place; as a habit it makes every paragraph sound like a rebuttal. Prefer stating Y directly, or splitting into two sentences.
- **"is real" / "are real"** — as in "the difference is real" or "that failure is real". Say what is actually being claimed instead: that it happens, that it can be measured, that it will bite you.
- **"worth remembering"** (and "worth noting", "worth saying") — usually a throat-clearing preface. Delete it and state the thing.
- **"load-bearing"** — the architectural metaphor. Prefer saying what depends on what.
- **"mechanism"** — prefer "how it works", "the machinery", or naming the specific thing.
- **"precise" / "precisely"** — usually padding on a claim that is either exact or not. Prefer "exactly", or give the number.
- **"clean" / "cleanly"** — vague praise. Say what property is meant: it runs without error, it reads easily, it has no leftover state.
- **"critical gate"** — and the gatekeeping metaphor generally.
- **"literally"** — almost always deletable; where it is doing real work, prefer "actually" or restate the claim.
- **"genuine" / "genuinely"** — delete, or say why the thing is not merely apparent.
- **"honest" / "honestly"** — as an intensifier. Keep it only where honesty is the subject, as in asking a student to answer honestly.

None of these is banned outright; the test is whether the word is doing work that no plainer word would do. Where one survives, it should be because the sentence would be worse without it.

**Two standing cautions:**

- **Don't let the voice drift.** `classes.ipynb` remains the cautionary example — it is AI-generated reference-manual prose with zero exercises (see §5). New and rewritten Python notes must keep the warm, exercise-dense voice all the way through.
- **Label intentional bugs.** The notes deliberately plant bugs so students learn to read tracebacks. Mark deliberate-bug exercises with an explicit "Spot the bug" callout (the clinic notes `composition.qmd` and `debugging.qmd` already do this) so students and the AI can tell them apart from accidental typos.

---

## 3. The AI thread and the widgets

Full detail is in `docs/planning/course-design.qmd` (§7 there); the essentials for authoring:

- **AI from week 1, in escalating roles, and the badges are live in every note.** Every `#### Exercise` in the book carries a licence badge: either the sanctioned **role** for that context or `SOLO` for do-it-yourself-first. The cumulative ladder is Explainer → Comparer → Drafter → Collaborator → Developer; roles in use are `AI: Explainer`, `AI: Comparer`, `AI: Drafter`, `AI: Collaborator`, `AI: Developer`. Explainer covers three moves (asking what something means, translating code to English and back, asking for more examples of a pattern); Drafter covers two forms (the ordinary specify-draft-read-test order, and a stricter contract-first form where tests are written before any code and hidden from the assistant). The ladder previously ran to eight rungs (Translator and Illustrator sat between Explainer and Comparer; Worker sat between Drafter and Collaborator) before those three were retired as too thin to be memorable and folded into Explainer and Drafter respectively; see `intro/course-introduction.qmd` §Badges for the current definitions. A badge only ever licenses a role the current week has unlocked. The AI lives in the **browser** (Microsoft 365 Copilot, including its Study and Learn agent); VS Code stays the AI-free space.
- **Badge format — a Title Case link, styled smaller, no icons.** Write the badge as a link to that rung's own section in `intro/course-introduction.qmd`, on its own line directly under the heading with a blank line either side, with the `{.small}` attribute so it renders smaller than the surrounding text. **The badge text is Title Case** — `[SOLO](...){.small}`, `[AI: Drafter](...){.small}`, `[AI: Developer](...){.small}` — SOLO stays fully capitalized as the acronym-like exception. The `### AI: Drafter` section headings in the course introduction and the ladder-progress strips in `docs/ai/` are ordinary prose, not badges, and keep their own Title Case with no `{.small}`:

  ```markdown
  #### Exercise

  [SOLO](../intro/course-introduction.qmd#sec-badge-solo){.small}

  Decide what you think will happen before you run it.
  ```

  The link target is `../intro/course-introduction.qmd#sec-badge-<role>` from any chapter one directory deep (`ai/`, `python/`, `turtle/`, `projects/`), `course-introduction.qmd#sec-badge-<role>` from within `intro/`, and a bare `#sec-badge-<role>` inside `course-introduction.qmd` itself. The anchors are `sec-badge-solo`, `-explainer`, `-translator`, `-illustrator`, `-comparer`, `-drafter`, `-worker`, `-collaborator`, `-developer`; each is a short section under `## Badges {#sec-badges}` saying what that rung permits, what it forbids, and how the student proves the answer. A student who has forgotten what a role licenses is one click from finding out, which is the point of the link.

  **Do not prefix badges with 🔒, 🟢 or any other emoji, and do not bold them.** Earlier drafts used `🔒 **SOLO**` and `🟢 **AI: Comparer**`; those were normalised away and must not come back. Two older forms are also gone: the plain code span (`` `SOLO` ``), and a lower-case small-caps span (`[[solo]{.smallcaps}](...)`, `[[ai: drafter]{.smallcaps}](...)`) that was itself later normalised away in favor of the current Title Case `{.small}` form — `scripts/check-badge-order.py` still recognises both older forms so that a half-converted note is reported rather than skipped, but new material must use the current link form. An earlier draft also let compact numbered drill lists (`ai/predict-then-prove.qmd`, `ai/ask-for-another-way.qmd`) keep the badge inline in the heading to save a line; that broke PDF rendering (the inline badge collided with the auto-generated chapter-subsubsection number) and was reverted — the own-line form above is now the only form, everywhere, no exception, and `scripts/check-badge-order.py` fails on an inline badge, naming the chapter and line.
- **A badge licenses; the exercise must also instruct.** The badge says which rung the student is allowed to stand on. It does not say what to do with the assistant, and a badge on its own leaves the student holding a permit and no task. Every non-`solo` exercise must therefore also contain, in its own prose, a sentence saying **what to ask** and **how the answer gets settled** — settled by running the code, by a test, by the documentation, or by the student's own worked reasoning, never by the assistant's confidence. Write it as ordinary prose at the end of the exercise, not as a formula: twenty exercises that all open "Ask the assistant to explain this error" read as boilerplate and get skipped. Vary the ask (predict the exact wording, name the error before running, explain why rather than what, give it the code and nothing else) and vary what settles it.

  A shared lead-in may carry the instruction for a run of exercises that all work the same way — a `::: {.callout-tip}` above a numbered drill list, or a Part introduction. `ai/predict-then-prove.qmd`, `ai/explain-then-confirm.qmd`, `ai/ask-for-another-way.qmd` and `ai/let-it-draft.qmd` are covered this way and must not have the sentence repeated into each drill. Everywhere else it goes in the exercise itself.
- **The ladder is checked by machine.** `scripts/check-badge-order.py` walks `docs/_quarto.yml` in render order, reads the badge under every `#### Exercise` heading (JSON-loading notebook cells, which a plain grep cannot see), and fails if any exercise licenses a role before the chapter that introduces it, if it finds no badges at all, or if a badge is still inline in its heading. It runs in `.github/workflows/quarto-publish.yml` before the render. Run `python3 scripts/check-badge-order.py --census` to print the per-role and per-week counts. When you move a note between weeks, update the `LADDER` map at the top of that script in the same commit.
- **Ladder-progress strip.** Every note in `docs/ai/` opens with a `::: {.column-margin}` block headed **The ladder so far**, listing the rungs earned up to that note with the one the note works in bold and the rest under *Still to come*. Add one when you add an AI note, and keep it consistent with the checker's `LADDER` map.
- **The rule that ties AI to the widgets:** *"the AI predicts; the widget proves."* Whenever the assistant claims what code does, students check it with the machine (this is the whole point of `predict-then-prove.qmd`).
- **One verification principle, several modes.** Code is verified by tests and reading; facts/biology by evidence and knowledge; your own learning by the "AI-off test" (can you do it with the assistant switched off). This thread runs through the AI-arc notes and closes in `surviving-ai.md` and `the-ai-off-test.qmd`.
- **Logbook.** A term-long student artifact — one weekly entry: what the AI got right, what it got wrong, how they knew. Weekly notes should prompt an entry.
- **Widgets — where each fits when authoring:**
  - `steps-widget` (`%%steps`): substitution/reduction traces — the evaluation, precedence, and logic notes, and `predict-then-prove.qmd`.
  - `puzzle-widget` (`%%puzzle <result>`): reorder shuffled lines — the "unscramble the statements" exercises (precedence/general/data_structures) and truthiness/keyword drills.
  - `codelens-widget` (`%%codelens`, Python Tutor): step through execution with heap/reference diagrams — objects, list/dict aliasing and shared references, function call frames/scope, `__init__`, nested loops; used in the `debugging.qmd` clinic.
  - `turtle-widget`: visual functions/loops — a safe first place to let the AI "Draft" because output is visually checkable.
  - `sandbox-widget` (`%%sandbox`): the isolation model and every interspersed exercise.
  - `iplot-widget`: pass a dataframe, get a dropdown-driven plot builder that also reveals the generated code — introduced light in `dataframes.qmd` and the later projects.
  - `snippet-cast` (`%%snippet`): teacher tool for narrated walkthroughs and human–AI transcript videos; demoed in `python/snippet-cast.ipynb`.

---

## 4. Quality checklist for new and revised notes

The audit surfaced recurring, avoidable defects. Do not reproduce them:

1. **No hand-typed output/error transcripts.** Render output from executed cells. Where a transcript must be static, use *current* Python wording (e.g. `SyntaxError: unterminated string literal (detected at line 1)`, `SyntaxError: unmatched ')'`), not pre-3.8 text. (Most `.ipynb` notes are still single-cell markdown, so this is the dominant risk.)
2. **Code and prose must agree on identifiers.** The notes have documented mismatches (`number` vs `numbers`, `result` vs `results`, `is_palindome` vs `is_palindrome`, `chrous_text`/`chrorus_text`, `square_numbers` vs `squared_numbers`, `tmp` vs `temp`). Every identifier in prose must match the code exactly; running every code cell catches the NameErrors.
3. **Quarto syntax hygiene.** No four-backtick fences; anchors are `{#sec-x}` (brace, not `)`); close every inline-code backtick; keep punctuation *outside* code spans (`` `def` ``, not `` `def,` ``).
4. **Cross-reference style consistent** (`@fig-x`, `@sec-x`, bare). Verify every `@sec-`/`@fig-` target resolves in the assembled book.
5. **No European decimal grouping** in English prose (`170,000`, not `170.000`).
6. **Refresh dated examples** toward neutral or biological data.
7. **Copyedit pass.** Recurring typos to watch: "his"→"this", "source"→"course", "stings"→"strings", "substations"→"substitutions", "Celcius"→"Celsius", "assingment"→"assignment", "curration"→"curation". Danish-authored spellings leak in.
8. **Modern idioms.** Introduce `with open(...) as f:` for files (the notes teach only the `close`-heavy form); soften "dictionary order is arbitrary" to "don't rely on order" (dicts preserve insertion order since 3.7).
9. **Keep it in scope.** Calibrate for absolute-beginner molecular-biology students. `classes.ipynb`-style material (multiple inheritance, mixins, MRO, static/class methods, properties, SOLID) is over-scoped; keep classes to `__init__`/`self`/attributes/methods and a light `__str__`.
10. **US English spelling.** Write `color`, `organize`, `behavior`, `license`, `catalog`, `program`, `defense`, `judgment`, `practice`, `toward`/`forward`/`backward` (no trailing *-s*), `modeled`/`modeling`, `theater`, `gray`, not the British equivalents. Proper nouns keep their own spelling (e.g. Aarhus University's *Bioinformatics Research Centre*).

---

## 5. Content catalog (current state)

Status legend: **Solid** = reusable after a copyedit; **Needs work** = good bones, real fixes required; **Stub** = little/no content; **Infra** = tooling/appendix/non-chapter. The audit-era per-note fixes are retained below because the `.ipynb` notes are largely unchanged since then (character counts are stable); treat them as known issues that may be only partially addressed.

### `docs/python/` — programming notes

- **getting_started.ipynb** — *Needs work.* Terminal walkthrough (`pwd`/`ls`/`cd`) + install. Cut the orphaned "Installing Phasic" block and the large commented Conda legacy; restore a two-column Mac/Windows command table; add the first real `%%sandbox`.
- **hello-world.ipynb** — *Needs work.* First program, running from the terminal, reading errors, strings/quotes, comments;. Fix quote/error-message inconsistencies and update transcripts to current Python. Ideal first `AI: Explainer` exercise ("ask the assistant to explain this error, then judge it").
- **values-operators-logic.ipynb** — *Solid-ish / Needs work.* Values, operators, comparison/logical operators, truthiness & short-circuit, types, conversion. Excellent assignment-vs-substitution framing. Fix the duplicated exercise line (`print("apple" and "")` twice) and punctuation inside code spans; `steps-widget` on precedence/short-circuit.
- **precedence-steps.ipynb** — *Solid (keystone).* Precedence table, statements vs. expressions, the substitution/reduction model. Highest-value note. Fix "his"→"this", `result`/`results`, an unterminated inline-code target. Maps 1:1 onto `steps-widget` and `puzzle-widget`.
- **course_tools.ipynb** — *Needs work.* Introduces `myiagi`/`pysteps` (the substitution/reduction drills) via the Karate-Kid metaphor. Verify the worked arithmetic example and the `pysteps` line/file references; unify the `myiagi`/`Myagi`/`Miyagi` spelling.
- **if-else.ipynb** — *Needs work.* Conditionals, truthiness, nesting, blocks/indentation, `elif`, via bus/cookie/DNA-base examples + FAQ humor. Fix the missing closing quote in an `if x` demo and `7 = 7`→`y = 7`. No executed cells yet.
- **functions.ipynb** — *Needs work.* Functions as reusable mini-programs via a song; `def`/`return`/`None`, args vs. params, local scope, built-ins. Strong "a call is substituted by its return value" refrain. Fix the `chrous_text`/`chrorus_text` NameError, the celsius↔Fahrenheit direction error, and assorted typos; `codelens` for call frames/scope.
- **objects.ipynb** — *Needs work.* Everything is an object with methods; string methods, docs navigation, `.format()`, dunders (`__add__`), indexing/slicing. Fix the demo alphabet missing `w`; keep the "Hey string, …yourself!" and dunder reveal.
- **lists.ipynb** — *Needs work.* Ordered mutable containers; build/index/slice/`del`/`split`/`join`. Fix the flagship exercise's `number[i]`/`numbers` NameError; prime `codelens` chapter — add the explicit aliasing exercise (now also covered by `debugging.qmd`).
- **dictionaries.ipynb** — *Needs work.* Key–value containers, access, nesting, `in`, and the closing `__len__`/`__contains__` reveal. Fix the orphaned age-70→71 note (the real overwrite is `job`); soften "order is arbitrary"; replace any dated example with a codon/gene-annotation dict.
- **tuples.ipynb** — *Needs work (thin).* Immutable tuples vs. lists, packing/unpacking, the `a, b = b, a` swap. Fix the `fruits[3]`/"second element" mismatch and `tmp`/`temp` drift; delete the swap preview so the exercise "aha" survives.
- **iteration.ipynb** — *Solid-ish / Needs work.* For-loops from first principles, iterables, `range`, nested loops. Fix "The,n"→"Then" and the garbled `__iter__` sentence; consider demoting the premature `__iter__` digression; `codelens`/`steps` for nested loops and `range` steps.
- **data_structures.ipynb** — *Solid (the model to imitate).* Practice-heavy: counting with dicts, bucketing, nested loops, matrices, guided `is_palindrome`. The exemplar for interspersed exercises and authentic voice. Convert `# Your code here` stubs to runnable cells + collapsible solutions; `puzzle` for reorder-and-indent.
- **files.ipynb** — *Needs work.* File I/O: `open`/`write`/`close`/`\n`/`print(file=)`, reading, iterating a file. Fix the two runtime bugs (`print("Second line, file=f")` and `open('workfile','r')` missing `.txt`); introduce `with open(...) as f:`.
- **testing.ipynb** — *Needs work (thin, AI-thread hub).* Why/how to test, basic testing, "the project testing utility." Currently light (~6k). Frame tests explicitly as how you verify AI-generated code; add `%%sandbox` to write one failing then one passing test; reconcile any test-count transcripts. This is the hinge between the Python notes and the AI arc.
- **classes.ipynb** — *Needs work (high priority: voice + scope).* Still the cautionary example: ~32k of generic reference-manual prose with **zero exercises and zero badges**, and badly over-scoped (inheritance, composition, properties, static/class methods, multiple inheritance, mixins, SOLID single-responsibility, a "complete BioSequence class"). Rewrite in the author's voice with interspersed practice, and cut to `class`/`__init__`/`self`/attributes/instance methods plus a light `__str__`/`__len__`/`__getitem__`; defer everything else to an optional appendix. `codelens` for `__init__`/attribute assignment.
- **modules.ipynb** — *Stub (in the book, week 9).* One line + a TODO. Needs the "using code from other files" chapter; pairs with the AI-arc `documentation-and-resources.qmd` and the codon-bias project.
- **recursion.ipynb** — *Stub (in the book, week 10).* ~600 chars with PDF-workflow leakage to remove. Develop the "if you understand recursion you understand functions" angle; pair with an AI call-stack-tracing exercise.
- **packages.ipynb / biopython.ipynb** — *Stubs (out of the book).* Both circle "reusing others' code / BioPython / the `Seq` class." Fold into the modules chapter or the giant's-shoulders framing; the AI is the modern giant's shoulders, a layer atop libraries you still must understand.
- **list-comprehensions.ipynb** — *Stub (out of the book).* Title + empty headings. Write do-first: the for-loop-plus-`append` version, then reveal the comprehension as its compression.
- **general_exercises.ipynb** — *Solid (out of the book).* Bite-sized type/coercion/precedence/tracing exercises + two solvable scramble puzzles. Good `%%sandbox`/widget fodder; fold inline next to the relevant concepts.
- **preface.ipynb** — *Solid (out of the book).* States the two pedagogical principles and the inviting tone. If reinstated, add a paragraph planting the "AI as a new layer of instruction" thesis (now fully developed in `ai/instruction.md`).
- **references.ipynb** — *Infra (stub).* Bibliography stub.
- **appendix_bsf.ipynb** — *Infra.* Install appendix for students also taking BSF (Pixi + PyMOL). Standardize "PyMOL"; add an Apple-Silicon note.
- **snippet-cast.ipynb / course-tools.ipynb / introduction.ipynb** — *Infra / non-chapter.* Widget demos and a leftover Coalescent tutorial; not student chapters.

### `docs/python/` — worked-example & clinic notes (`.qmd`, drafted)

- **composition.qmd** — *Drafted.* Week-6 worked example: a small biology problem solved live by composition, with a "Spot the bug" beat and a `SOLO` exercise. Companion to the lecture's snippet-cast.
- **decomposition.qmd** — *Drafted.* Week-10 worked example: naming the pieces and the shape of the data before writing code; pairs with `ai/plan-before-you-prompt.md`. `SOLO` exercise.
- **debugging.qmd** — *Drafted.* Week-7 clinic: read a traceback, form a hypothesis, confirm with a print or `codelens`; uses curated authored bugs ("Spot the bug"). `SOLO` exercise. Reused across project weeks.
- **dataframes.qmd** — *Drafted.* Week-12 light introduction: a dataframe as a complex data type worth knowing exists, met by doing (`read_csv`, pulling a column), the `apply` bridge from an authored/tested function to whole-column application, then a plot. Real data analysis is out of scope. `SOLO` exercise.

### `docs/ai/` — the AI arc (mostly drafted)

Week-1 framing:

- **insides.md** — *Drafted.* "What a computer is, from the bottom up": switches, the CPU/memory/disk anatomy, kept-vs-temporary, and a Turing-machine section. This realizes the old `machine-insides` stub. `SOLO` exercise.
- **instruction.md** — *Drafted.* "From machine code to Python to AI": the ladder of instruction, compilers/interpreters as honest translators, the AI as the newest rung, next-word prediction, training/weights, and "the break in the metaphor" (the AI is not a faithful translator) — the course's central thesis, written out.
- **machine-insides.qmd** — *Stub (in the book, week 1).* Currently just a YouTube embed; overlaps `insides.md`. Decide whether it stays a video landing page or is merged.
- **meet-ai.qmd** — *Drafted.* Week-1 assistant intro: where it lives, the license badges, the logbook, and the rule the course turns on. `AI: Explainer` exercise.
- **about-microsoft-copilot.qmd** — *Stub (out of the book).* How to log into Microsoft 365 Copilot ("Work" on the landing page); not to be confused with GitHub Copilot.

Weekly AI beats and in-class clinics (short `.qmd`, session-structured with badges):

- **predict-then-prove.qmd** — *Drafted (wk2).* The AI predicts, the `%%steps` widget proves. `AI: Comparer`.
- **how-models-produce-code.qmd** — *Drafted (wk3).* Plain account of next-word prediction and why fluent code can be wrong. `AI: Explainer`.
- **explain-then-confirm.qmd** — *Drafted (wk4).* Ask it to explain an error, then confirm by running. `AI: Explainer`.
- **practical-ai-use.qmd** — *Drafted (wk5).* Tool-light browser-use guide: prompting, reading a reply critically. `AI: Explainer`.
- **ask-for-another-way.qmd** — *Drafted (wk6).* Comparer clinic with a rubric for judging two solutions. `AI: Comparer`.
- **let-it-draft.qmd** — *Drafted (wk7).* Drafter clinic: specify small, read every line, test before believing. `AI: Drafter`.
- **the-docs-are-the-test.qmd** — *Drafted (wk9).* The AI invents functions/endpoints; the real documentation is the test that fails them. `AI: Worker`.
- **directing-a-resource.qmd** — *Drafted (wk9).* Clinic on building on machinery you did not write; rehearses the codon-bias/BioPython move. `AI: Collaborator`.
- **documentation-and-resources.qmd** — *Drafted (wk9).* Reading a library/API as a catalog of contracts; what you do and do not verify. `AI: Worker`.
- **learning-with-an-ai.qmd** — *Drafted (wk12).* Using the assistant to learn, the Study-and-Learn tutor mode, and verifying facts against evidence. `AI: Explainer`.
- **the-ai-off-test.qmd** — *Drafted (wk14).* Verification turned on your own learning; the line between augmenting and cheating. `SOLO`.

The five long conceptual notes (`.md`, pure plain-prose register):

- **reading-and-judging.md** — *Drafted (wk8).* Reading and judging code you did not write; the judging rubric.
- **tests-are-the-contract.md** — *Drafted (wk8).* The test as an executable specification you hand the AI; the Worker role.
- **plan-before-you-prompt.md** — *Drafted (wk10).* Decompose into named, testable functions and write the plan as stub-and-docstring before prompting; the Collaborator role.
- **delegate-the-full-problem.md** — *Drafted (wk11).* The full loop assembled once per piece on a task beyond your unaided reach; the Developer role, the prompt journal. (Renamed from `delegating-a-whole-job`.)
- **surviving-ai.md** — *Drafted (wk14).* The closing note: automation bias, tests necessary-not-sufficient, hallucinated biology, when not to use the AI, responsibility that does not transfer, honest attribution, and the augmentation ("squares your knowledge") ending. (Renamed from `limits-of-the-machine`.)

The finale (week 13) — **stubs**:

- **finale-kickoff.qmd / finale-build.qmd / finale-finishing.qmd** — *Stubs (in the book, week 13).* Still the "Draft stub — planned contents" placeholders for the student-formulated finale. The `curration-project` may become the concrete finale/exam; decide whether these stubs are written or replaced.

### `docs/projects/` — project chapters (`.qmd`, drafted)

In the book in teaching order (weeks 6–13). Note the actual biology, which differs from earlier assumptions:

- **translation-project.qmd** (wk6) — *Drafted.* Translate ORFs to protein via a codon→amino-acid dict. The gentlest first project; also the check-widget demo. Existing course marks it a mandatory hand-in.
- **folding-project.qmd** (wk7) — *Drafted.* Actually **"Primer analysis"**: base counts, melting temperature, reverse complement, hairpin check — not protein folding. Carries `# TA note` blocks.
- **alignment-project.qmd** (wk8) — *Drafted.* Global pairwise alignment; implement Needleman–Wunsch (build/fill the DP matrix, traceback). Has `# Hint` blocks.
- **codonbias-project.qmd** (wk9) — *Drafted.* Codon usage: read ORFs, split into codons, count, group by amino acid, turn counts into frequencies.
- **hiv-project.qmd** (wk10) — *Drafted.* HIV subtyping: sequence similarity, read `subtypeA–D.txt` + `unknown_type.txt`, classify. Uses `project-files/hivproject/recap.py` as a provided resource. Existing course marks it a mandatory hand-in.
- **seqdist-project.qmd** (wk11) — *Drafted.* "Sequence trees": Jukes–Cantor distance, lower-triangular distance matrix, clustering.
- **orf-project.qmd** (wk12) — *Drafted.* Finding genes: locate ORFs (start/stop codons) in a virulent *E. coli* genome, then translate.
- **assembly-project.qmd** (wk13) — *Drafted.* Genome assembly from short sequencing reads; the hardest, most integrative project.

Out of the book:

- **curration-project.qmd** — *Drafted but held out.* "Sequence Curation," an exam-derived assignment (DNA sequences with quality-score strings, Problems 1–3, download-package/offline flow). Tagged "TURN EXAM ASSIGNMENT INTO PROJECT." Candidate to become the concrete finale. Note the spelling: **"curration"/"assingment"** should be fixed to **curation/assignment**.

### `docs/blocks/` — building blocks

- **README.md + for-loop.ipynb** — *Stub/planned.* Mini-pages for single concepts (assignment, expression, for-loop, if-statement, function, list, dict, indentation-after-colon…) meant to be cross-referenced and surfaced as hover tooltips and as a browsable listing. Only the for-loop block is scaffolded.

### `docs/planning/` and top-level

- **planning/course-design.qmd** — the authoritative plan and the book's second chapter. Keep it and this file in sync.
- **planning/machine-map-poster.html** — the one-page student mental-model poster.
- **planning/old_weekplan.md** — the existing bioinformatics course's week plan, kept as the pacing reference.
- **docs/index.qmd** — landing page. **docs/notes.qmd** — scratch (e.g. making the "squares your knowledge" idea precise). **docs/AI-opening.qmd** — scratch "recent AI news" page. **docs/quarto-publishing.md** — Quarto render-option reference.

---

## 6. Authoring a new note — quick checklist

1. Open with a one-line italic abstract (Python notes) or a plain opening sentence (AI-arc notes); give the section a `{#sec-}` anchor.
2. Match the register of the folder: warm authorial voice in `docs/python/`, plain continuous prose in `docs/ai/`.
3. Teach by doing → naming; intersperse small `%%sandbox` cells; every exercise is predict-then-run.
4. Reinforce substitution & reduction; reach for the matching widget (`steps`/`puzzle`/`codelens`/`turtle`/`iplot`).
5. Badge every exercise — `[SOLO](../intro/course-introduction.qmd#sec-badge-solo){.small}` or the same form for `[AI: <Role>](...){.small}`, on its own line under the heading, no emoji, no bold, and no role the week has not unlocked; run `scripts/check-badge-order.py` afterwards; keep the AI in the browser; prompt a logbook entry where appropriate.
6. Make code runnable rather than hand-typed; label any deliberate-bug exercise with a "Spot the bug" callout.
7. Place the file in the right folder and add it to the correct week in `docs/_quarto.yml`; run the §4 quality checklist before calling it done.

---

## 7. Instructions left in the book for the assistant

While authoring, Kasper leaves instructions inline, next to the thing they are
about, rather than describing them afterwards in a chat message. The notation
is a token inside an ordinary comment, in whichever form the surrounding cell
already uses:

```
<!-- CLAUDE: expand the paragraph below to cover the empty string -->
```

```python
# CLAUDE: add four exercises about lists here, predict-then-run
```

The prose form belongs in a markdown cell, a `.qmd` or a `.md`; the code form
in a code cell or a `.py`. Both are invisible to the student — pandoc drops
the comment for PDF and EPUB and leaves it unrendered in HTML.

The code form also works in `docs/_quarto.yml`, and that is where work about a
chapter *as a whole* belongs — "this chapter is thin", "this chapter needs a
widget" — rather than at the top of the chapter itself, where it would sit
above a paragraph it is not about. Write it under the chapter's own line,
indented past the `-`, and wrap continuation lines with two spaces after the
`#` so the collector can tell a continuation from ordinary commentary:

```yaml
        - python/tuples.ipynb
          # CLAUDE: at 643 words the thinnest chapter in the book that is not
          #   a stub. Its hand-typed traceback is stale too.
```

Work that belongs to no chapter at all — a policy to decide, a workflow that
has never run, housekeeping — goes in the block at the top of `chapters:`,
where it is reported as book-wide. This is where the old
`docs/planning/checklist.md` went, on the principle that a task sitting next
to the week it lands in gets done and a task in a separate document does not.

The `CLAUDE:` token, with the colon, is what makes an instruction findable. A
bare `<!-- ... -->` is not: the book already contains over a thousand HTML
comments — commented-out figures, slide scratch, notes to self — and an
instruction lost in that crowd never gets done. `TODO:` and `FIXME:` stay what
they have always been, a note Kasper is writing to himself; `CLAUDE:` is work
handed over. All three share the same shape (an HTML comment in prose, a `#`
comment in code) and the same collector, but are picked up separately so a
personal note is never mistaken for a handoff.

An instruction applies to what follows it, up to the next heading, unless its
own text says otherwise. Put it immediately above the paragraph, cell or
exercise it concerns: "the paragraph below" stays true across edits, "the
third paragraph" does not.

`scripts/todo.py` is the pickup side. It reads `_quarto.yml` itself and then
walks the chapters it lists in render order, printing every instruction with
its week, chapter, line and the first line of whatever it points at, so a
term's worth of notes can be collected in one pass. `--claude` collects the
handoff notes, `--todo` collects `TODO:`/`FIXME:`, and both can be given
together, each labelled with which token it was:

```
python3 scripts/todo.py --claude                # CLAUDE:, in render order
python3 scripts/todo.py --todo                  # TODO:/FIXME: only
python3 scripts/todo.py --claude --todo         # both, each labelled
python3 scripts/todo.py --claude python/lists   # only chapters matching a string
python3 scripts/todo.py --claude --json         # the same, for a machine
python3 scripts/todo.py --claude --strict       # exit 1 if any instruction remains
```

It exits 1 on a *malformed* instruction — `<!-- CLAUDE add a figure -->`, with
the token but no colon — because that is worse than an unfinished one: it is
invisible to the collector and so would never be picked up at all. Outstanding
instructions are not themselves a failure; that is the normal state of a
chapter being written, and only `--strict` treats it as one.

When an instruction has been carried out, delete the comment in the same
commit that does the work, and say in the commit message which chapter it came
from. An instruction that survives the work it asked for will be done twice.
