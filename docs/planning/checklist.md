# Readiness checklist

*What still stands between the current repository and material a class can be taught from.*

This is a working list, not a verdict. It was written by reading the book as it currently stands in `docs/`, against the intentions set out in `course-design.qmd` and `CLAUDE.md`. Items are grouped by what happens if they are not done: the first group breaks teaching, the second leaves a hole in a specific week, and the rest are quality, consistency and housekeeping. Each item says what is wrong and what "done" looks like, so that anyone — including an assistant — can pick one up without rereading the whole book first.

## 1. Blocking: the book cannot yet be taught as written

- [ ] **Nothing in the Python chapters runs.** Fifteen of the seventeen notebooks under `docs/python/` contain zero code cells; every example is a markdown ` ```python ` fence. Only `dataframes.ipynb` (16 code cells) and `widget-demo.ipynb` (17) execute, along with the three notebooks in `docs/intro/`. Everything else — every printed value, every traceback, every "you should see something like this" — is hand-typed prose that no machine has checked. This is the single largest risk in the repository, because it makes three other things impossible at once: the `execute:` settings in `_quarto.yml` are inert for those chapters, CI cannot tell you when an example has drifted, and the rule in `CLAUDE.md` §4.1 against hand-typed output cannot be enforced. Done looks like one of two decisions, taken deliberately and written down: either the fenced blocks go back to being code cells and Quarto renders authoritative output, or the fences stay and a separate harness extracts and runs every fenced snippet in CI so that a broken example still turns the build red.

- [ ] **The hand-typed tracebacks are older than the Python the students will run.** While the output is static it is also stale: error wording in `hello-world.ipynb`, `tuples.ipynb`, `files.ipynb` and `functions.ipynb` predates the message rewrites of Python 3.8–3.12. A student who reads the note and then reads their own screen sees two different errors on the first day. Done looks like every static transcript regenerated against the interpreter pinned in `student-folder/pixi.toml`.

- [ ] **No widget appears in any Python chapter.** Across the whole book the widget magics occur in exactly five places: `turtle/week3.qmd`, `intro/script-vs-notebook.ipynb`, `intro/widget-reference.ipynb`, `python/widget-demo.ipynb` and `ai/predict-then-prove.qmd`. The turtle chapters for weeks four through eight use none. `docs/planning/widgets-in-the-python-notes.md` already maps which widget belongs where; that mapping is simply unimplemented. This matters more than it looks: "the AI predicts; the widget proves" is the organising principle of the course, and at the moment the proving half has no machinery in the notes where the predicting happens. Done looks like `%%steps` in the evaluation and precedence material, `%%puzzle` on the shuffled-statement exercises that already exist as plain text, and `%%codelens` on the aliasing, scope and nested-loop examples.

- [ ] **Week 13 opens on a stub.** `ai/finale-kickoff.qmd` is 110 words. The finale is the assessment the whole role ladder builds toward, and its first chapter is a placeholder. Done looks like a kickoff that states the task, the deliverable, the rules about AI involvement, and how the work is judged.

- [ ] **`docs/planning/course-plan.md` does not exist.** Both `CLAUDE.md` and `course-design.qmd` §204 send the reader to it for the detail of the role ladder. Either write it or repoint both references at `course-design.qmd`, which now carries most of that content.

## 2. Content that is thin or missing where a week needs it

- [ ] **`python/testing.ipynb` is the smallest chapter doing the largest job.** At around a thousand words and three code blocks it is the designated hub for the idea that a test is how you verify code you did not write. Weeks 8 through 13 all lean on it. It should be the chapter that grows most.
- [ ] **`ai/about-microsoft-copilot.qmd`, `ai/the-docs-are-the-test.qmd` and `ai/practical-ai-use.qmd`** are all under 700 words and each carries a week's AI slot on its own.
- [ ] **`python/tuples.ipynb` and `python/course_tools.ipynb`** are thin relative to their neighbours and both were flagged in the earlier audit for content, not just typos.
- [ ] **`preface.ipynb` and `references.ipynb` exist but are not in `_quarto.yml`.** The preface is described in `CLAUDE.md` as the reference voice for the whole book, and it is currently unpublished. Decide whether it becomes the front matter of `index.qmd` or a chapter in its own right.
- [ ] **Three empty notebooks are still on disk:** `python/biopython.ipynb`, `python/list-comprehensions.ipynb` and `python/introduction.ipynb`. None is in the book. Either write them or delete them, so that nobody has to work out again whether they are pending or abandoned.
- [ ] **`python/general_exercises.ipynb` is a real chapter that is not in the book.** Its fourteen exercises duplicate material now living in `precedence-steps.ipynb`. Fold the non-duplicates in and retire the file, or add it as a revision chapter.
- [ ] **`projects/curration-project.qmd` is written but unscheduled.** Week 12 currently has `orf-project.qmd` only. Decide whether the curation project joins it or is dropped.
- [ ] **Weeks 11 and 14 carry two chapters each** while weeks 1 and 3 carry eleven and six. Check that the load actually matches the teaching hours before term, not during it.

## 3. Correctness sweep

Every one of these is a specific, known, reproducible defect. They are cheap individually and expensive in aggregate, because each one costs a student the assumption that the notes are right.

- [ ] `course_tools.ipynb`: the worked substitution example is arithmetically wrong — `4 * 8` is rendered as `24`, and the surrounding "deduce y and x" prose depends on the wrong number. The `pysteps` transcript also names `test_studentfile.py` line 4 where the file is `myfile.py` line 3.
- [ ] `classes.ipynb`: the `codon_table` is truncated, so the worked protein output is garbage; `TreeNode` is referenced but never defined; `__init__` is called a constructor where the book means initializer.
- [ ] `functions.ipynb`: the Celsius-to-Fahrenheit example converts in the wrong direction, and the spelling `celcius` appears in identifiers.
- [ ] `lists.ipynb`: `'ATG…'.split('')` raises, which kills the three examples after it. Decide whether the empty separator is the lesson or an accident, and either mark it as a deliberate bug or fix it.
- [ ] `dictionaries.ipynb`: a note explains replacing age 70 with 71, but the code overwrites `job`.
- [ ] **Run every fenced snippet once, in order, per chapter.** Most remaining identifier mismatches — the `number`/`numbers` family — surface as a `NameError` within seconds of actually executing them. This is the single highest-yield hour available anywhere in this list, and it stays true whichever way the executable-cells question in §1 is decided.

## 4. Consistency of the AI thread

- [x] **Every exercise now carries a badge.** All 450 `#### Exercise` headings in `docs/ai`, `docs/intro`, `docs/python`, `docs/projects` and `docs/turtle` now carry a licence: 352 `SOLO`, 44 `AI: Explainer`, 35 `AI: Comparer`, 11 `AI: Drafter`, 5 `AI: Unreliable Narrator`, and one each of `AI: Worker`, `AI: Collaborator` and `AI: Delegate`. The convention is a lock or a green circle followed by a code span — ``🔒 `SOLO` `` or ``🟢 `AI: Explainer` `` — on its own line below the heading, except in the compact numbered drills of `ai/predict-then-prove.qmd` and `ai/ask-for-another-way.qmd` where it stays inline in the heading. The earlier `**bold**` and bare-backtick variants were normalised to this form.
- [ ] **The ladder in `course-design.qmd` disagrees with the book.** The table places Unreliable Narrator in week 10 and Collaborator in week 11, but `_quarto.yml` puts `reading-and-judging.md` in week 8, and `turtle/week8.qmd` already licenses Unreliable Narrator. One of the two is the plan of record; make it so and correct the other.
- [ ] **Translator and Illustrator are in the ladder and in no chapter.** Nothing in the book licenses either role. Either write the slot that introduces them or shorten the ladder to the seven roles the course actually teaches.
- [ ] **Decide whether the badge is also an instruction.** A badge grants a licence; it does not tell the student what to do with the assistant. In the turtle chapters and the `ai/` notes the surrounding prose does that work. In the Python chapters the `AI: Explainer` badges added on error-message exercises are a licence only. If they should also prompt ("ask the assistant to explain this traceback, then run it and judge the explanation"), that sentence needs writing, exercise by exercise.
- [ ] **The logbook is named in ten chapters and defined in none.** There is no template, no statement of where it lives, and no description of how it is assessed. Students will ask in week one.

## 5. Student-facing infrastructure

- [ ] **`docs/jupyterlite/content/` holds stale duplicates** of `objects.ipynb`, `testing.ipynb`, `lists.ipynb`, `files.ipynb`, `values-operators-logic.ipynb` and `getting_started.ipynb`, each still containing bugs that were fixed in `docs/python/` in commit `4be799d`. Either regenerate them from the source chapters as a build step or delete them, but do not leave two copies of a chapter with different bugs.
- [ ] **`.github/workflows/student-env-check.yml` has never run.** It is committed but untriggered. A workflow that has not run is a workflow that does not work.
- [ ] **Verify the Windows install path end to end on Windows.** The `.msi` installer route is the documented one; nobody has confirmed the full sequence — install pixi, unpack the course folder, open VS Code, run a widget — on a clean Windows machine.
- [ ] **Decide the solutions policy.** Solutions appear in some chapters and not others, in no consistent form. Students will notice by week two.
- [ ] **Confirm that `pixi run get <chapter>` reaches every chapter** a student is asked to download, and that `docs/_book/notebooks/index.txt` lists them all after a full render.

## 6. Housekeeping

- [ ] Three `.DS_Store` files and `.vscode/settings.json` are tracked in git; untrack them and extend `.gitignore`.
- [ ] `_to_delete/` at the repository root needs deleting by hand — the device mount cannot unlink, so it accumulates.
- [ ] `planning/authorship-split.md` and `planning/authorship-progression.md` cover the same ground and should be one document.
- [ ] The word "capstone" survives in several places where the book now says "finale".
- [ ] `docs/slides/` contains build leftovers (`index_files/`, `libs/`, two `*.quarto_ipynb_*` files) that should be ignored rather than committed.

## 7. Decisions only you can make

These are not tasks; they are forks in the road that block tasks. Nothing below should be settled by an assistant guessing.

- [ ] Executable cells or markdown fences in the Python chapters — see §1. Everything about output fidelity, CI and the `execute:` settings follows from this one answer.
- [ ] Whether the widget mapping in `widgets-in-the-python-notes.md` is a commitment for this run of the course or an aspiration for the next.
- [ ] Which week actually introduces Unreliable Narrator, and whether the ladder keeps nine roles or seven.
- [ ] Whether `classes.ipynb` stays in week 7 at its current scope, or the over-scoped half moves to an appendix as `CLAUDE.md` §4.9 recommends.
- [ ] What the logbook is worth, and whether it is assessed at all.
