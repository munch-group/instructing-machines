# Instructing Machines — Course Design (14 weeks)

*This document locks the week-by-week design: the sequence, the learning curve, the tool-introduction schedule, the workload shape, and the pitfalls with their mitigations. It is downstream of the pedagogy in `course-plan.md` (the AI-role ladder, the widgets, the "AI as a layer of compilation" thesis) — read that for the *why*; this is the *what, when, and in what order*. Where the two differ on the week grid, this file wins.*

---

## 1. Fixed constraints (the shape everything fits)

- **10 ECTS (~275 h), 14 weeks.** Deliberately under-fill: required work is capped well below the nominal ~19 h/week so the weakest 20% can finish; the ECTS budget is absorbed by optional enrichment and the capstone ramp for stronger students.
- **Weekly rhythm** — three lecture slots + one TA session:
  - **Double lecture (2×45 min):** slot 1 = a *demanding* programming topic; slot 2 = the shorter **AI / "different" slot** (the AI thread and other lighter/background material). Because the AI slot rarely fills its 45 min, its spare time is available for programming basics.
  - **Single lecture (45 min):** a second *demanding* topic.
  - **TA (3 h):** works the **previous** week's material, so every student has had both lectures first.
- **At most one demanding new concept per lecture sitting** (Kasper's rule, borne out over years).
- **The lab-practical split (weeks 4–5).** Half the cohort is away at a parallel lab practical in week 4, the other half in week 5, and the away half misses that week's TA. Consequences, which the grid is built around:
  - **TA4 and TA5 are one identical session** delivered twice — each half attends the week they're not away — so it can only carry material *both* halves have been lectured on, i.e. **week 3's**.
  - **Weeks 4 and 5 lecture material gets no TA of its own**; that load lands on **TA6, which covers both week 4 and week 5**.
  - Therefore weeks 4–5 must hold **light, self-recoverable** topics (survivable on the notes + self-checking widgets + the AI-as-Explainer without a live TA), and the **functions cliff must not fall there**.
- **The course ends at week 14** — no work extends into the exam period.

---

## 2. The 14-week grid (locked)

`⛰` = a known cliff week; `⚠️` = a lab-split / disruption week. TA each week works the previous week's two demanding topics unless noted.

| Wk | Demanding A (double-lec 1 + spare) | Demanding B (single lec) | AI / "different" slot | TA covers |
|----|--------------------------------------|----------------------------|------------------------|-----------|
| 1 | Machine model + first **script** in the terminal | Edit–save–run; values & types; operators | Levels of instruction; **Explainer**; the machine-map poster; logbook & badges | setup / terminal clinic |
| 2 | Expressions, precedence, **substitution/reduction** | Variables & assignment (Oath 3) | **Translator**; "the AI predicts, `%%steps` proves" | → wk 1 |
| 3 | Boolean logic & truthiness | Conditionals: `if`/`else`, blocks, `elif`, nested | **Illustrator** | → wk 2 |
| 4 ⚠️ | Objects & string methods | Indexing & slicing | AI: practical use (how to prompt, how to read a reply) | **→ wk 3** (shared, half the cohort) |
| 5 ⚠️ | Lists (+ tuples as a short coda) | Dictionaries | AI: practical use | **→ wk 3** (shared, other half — identical to wk 4) |
| 6 ⛰ | **Functions:** `def` / call / `return` | **Scope** + built-in functions | AI background: how a model produces code | **→ wk 4 + wk 5** (double) |
| 7 ⛰ | `for`-loops & `range` (iteration begins) | **Classes: `__init__`, `self`, methods** (add-a-method exercises) | **Comparer** | → wk 6 |
| 8 ⛰ | Nested loops; building data structures | References & aliasing (`%%codelens`) + consolidation | **Worker**; "it does a job you specify" → why we test | → wk 7 |
| 9 | **Testing:** tests as executable specifications | Files; a small end-to-end script | Spec & testing as the contract | → wk 8 |
| 10 | Reading & judging generated code (the rubric) | **Guided project** kickoff (HIV subtyping) | **Unreliable Narrator**; verify the *biology* | → wk 9 |
| 11 | Decomposition & planning before prompting | Guided project: build & verify | **Collaborator** | → wk 10 |
| 12 | Capstone kickoff: decompose, plan, first tests | Capstone planning clinic | Collaborator → **Delegate** | → wk 11 |
| 13 | Capstone build clinic: verify each piece | Capstone build clinic: integrate | **Delegate**; the prompt journal | → wk 12 |
| 14 | Finishing & debugging clinic | Limits of the machine: over-reliance, hallucinated biology, when *not* to use AI | Reflection / presentations; the logbook arc | → wk 13 |

The two demanding slots carry the programming; the AI thread rides the third slot every week from day one, never competing with the hard topic of the day.

---

## 3. Concept dependency graph

The sequence walks a strict prerequisite chain, so nothing is used before it's taught:

```
values/types/operators (wk1-2)
        └─ expressions & precedence → substitution/reduction model (wk2)   ← the spine
                └─ variables & assignment (wk2)
                        └─ boolean logic & truthiness (wk3)
                                └─ conditionals (wk3)
        objects & string methods (wk4) ─┐
        indexing & slicing (wk4-5) ─────┤
        lists / dictionaries / tuples (wk5) ────┐
                                                ├─ functions (wk6) ── scope (wk6)
                                                │        ├─ classes: __init__/self/methods (wk7)   ← needs functions + objects
                                                │        └─ iteration: for/range (wk7)
                                                │                └─ nested loops & building data structures (wk8)
                                                │                        └─ references & aliasing (wk8)
                                                └─ testing (wk9) ── files (wk9)
                                                        └─ AI integration: read/judge (wk10) → plan (wk11)
                                                                └─ guided project (wk10-11) → capstone (wk12-14)
```

Two placement facts the graph guarantees: **functions depend only on values/expressions/variables** (all taught with full TA support in weeks 1–3), so putting functions at week 6 is safe even though the week 4–5 container topics sit "between" — functions don't need them. And **testing (wk9) is the hinge**: everything in the AI arc (specify, judge, plan) stands on being able to write a test.

---

## 4. The learning curve & cliff cushioning

Kasper's two historical dropout points are **functions & scope** and **iteration & nested loops**. Both are cushioned by *depth of practice*, not extra lecture time:

- **Functions & scope — week 6.** One intensive week (both demanding slots), then a **dedicated 3-hour TA in week 7**, `%%codelens` on call frames and the "temporary little world" of scope, and heavy exercise density. Week 6's second slot is scope + built-ins (consolidation of the same idea), not a second brand-new hard thing.
- **Iteration & nested loops — weeks 7–8.** `for`/`range` in week 7 (dedicated TA in week 8), nested loops and building data structures in week 8 (dedicated TA in week 9), with `%%steps`/`%%codelens` to watch the loop variable change. Week 8's second slot is aliasing + consolidation.

**The disruption zone (weeks 4–5)** deliberately holds the most self-recoverable topics — objects, string methods, indexing/slicing, lists, dictionaries — because a student who misses that week's lecture and TA can rebuild them from the notes and the **self-checking widgets** (`%%puzzle`, `%%codelens`, and the AI-as-Explainer) without a human. None is a prerequisite for the functions cliff, and all are reinforced constantly afterward, so a shaky first exposure doesn't compound. **Conditionals finish in week 3**, so they get the full shared TA. Booleans/truthiness (which Kasper's notes flag for overload) also sit in week 3 with full TA.

**Classes (week 7, single lecture)** cap the objects arc — "you've been *using* objects; here is the scaffolding one is made from." Scope is deliberately small so it doesn't crowd the iteration onset in the same week: `class`, `__init__`, `self`, instance attributes, and methods, with a light `__str__`; the exercises have students **add a method to a given class** rather than design one from scratch. It sits at week 7 because methods *are* functions (taught week 6) and it builds on the objects/methods work of week 4. `%%codelens` visualizes `__init__` and attribute assignment, so the "what `self` is" question is answered by watching it. The advanced OOP material in the old `classes.ipynb` (multiple inheritance, mixins, static/class methods, SOLID) stays cut to an optional appendix.

---

## 5. Tool-introduction schedule

Each tool is introduced at the moment it *relieves* cognitive load rather than adds it. This schedule is itself a design artifact — front-loading all of it in weeks 1–2 would drown beginners.

| When | Tool / apparatus | Introduced because |
|------|------------------|--------------------|
| Wk 1 | Terminal, VS Code, first `.py` script, the **machine-map poster** | The script-first model makes disk/memory/CPU/interpreter legible before notebooks hide them |
| Wk 1 | **AI in the browser** (Copilot Chat), the **licence badges**, the **logbook** | The AI thread starts as *Explainer* on day one, in its own low-stakes slot |
| Wk 1–2 | **`script-widget`** (`%%exercise` / `%%test`), notebooks & IPython | The bridge from terminal scripts to notebooks — a cell that "starts clean" like a script |
| Wk 2 | **`steps-widget`** (`%%steps`) | Lands exactly on the substitution/reduction lecture; first "AI predicts, the widget proves" demo |
| Wk 2–4 | **`puzzle-widget`** (`%%puzzle`) | Order/structure drills; self-checking, ideal for the disruption weeks |
| Wk 3–4 | **`turtle-widget`** (optional) | Visual functions/loops; the safe first place to let the AI *Draft* |
| Wk 4–8 | **`codelens-widget`** (`%%codelens`) | Arrives at the aliasing/scope/reference cliff, where paper stops working; also visualizes `__init__` and attribute assignment for classes (wk7) |
| Wk 9 | **raw `pytest`** (im-pytest mode 2) | The testing chapter — students read the real tool's output |
| Wk 10–14 | **student-authored tests** (im-pytest mode 3) | They write tests to validate AI-produced code in the projects |

The **im-pytest check widget** (mode 1 — the friendly ✓/✗ panel) is available from week 1 for any auto-checked interspersed exercise, and becomes the everyday interface for the projects from week 10. All three modes are built and validated (see §7).

---

## 6. Per-week workload

Contact time is fixed at **5.25 h/week** (135 min lecture + 180 min TA). The design target for **required self-study is ~5–7 h/week for the median student** — below the ~14 h the nominal 10 ECTS would imply — with the surplus offered as *optional* enrichment and absorbed by the capstone for stronger students. This protects the floor while keeping the ceiling high.

Relative load by week (to smooth the curve, not to fill it):

| Wk | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|----|---|---|---|---|---|---|---|---|---|----|----|----|----|----|
| Load | light | med | med | light⚠️ | light⚠️ | **heavy**⛰ | med⛰ | **heavy**⛰ | med | med | med | build | build | light |

Deliberate breathers: **week 1** (onboarding), **weeks 4–5** (disruption + the weakest students' cushion), **week 14** (reflection). The heavy weeks are the two cliffs; nothing brand-new-and-hard is stacked next to them. The capstone weeks are self-study-heavy but carry *no new lectured concepts* — the demanding slots are clinics, so the load is applied effort, not new material.

*(Exact hour budgets should be validated against a pilot cohort; the shape above is the commitment, the numbers are estimates.)*

---

## 7. The AI arc and the projects (project-based)

The AI thread runs in the "different" slot for all 14 weeks, escalating through the role ladder (§8). From week 9 the demanding slots turn from new syntax to **applying it through bioinformatics projects** — Kasper's proven, project-driven style — using the ported test suites as the verification spine.

- **Week 9 — the verification toolkit.** Testing (tests as executable specs, raw `pytest`), files, a small end-to-end script.
- **Weeks 10–11 — guided project: HIV subtyping.** Chosen as the flagship: self-contained-ish, intro-only concepts, a clean function-composition ladder, and the "ignore columns that are gaps in both sequences" rule is the perfect *spec detail an AI gets subtly wrong while the code still runs* — caught by the data-pinned tests. The AI-integration skills (reading/judging in wk10, planning in wk11) are taught in this project's context, run through the im-pytest widget: plan → prompt → verify.
- **Weeks 12–14 — capstone: genome assembly.** The standout for this audience: no algorithm over-scope, biology fully self-contained, and a strong 25-check suite whose order-independence and no-false-overlap tests punish the sloppy code beginners can't spot. **ORF finding** is the sanctioned alternative for students who want a gene-finding flavour. Workflow: plan → specify with tests → prompt → read & verify → iterate; keep the prompt journal; week 14 closes with the limits-of-the-machine discussion.
- **Cut:** **alignment** (dynamic programming is the wrong hill for absolute beginners, even with AI). **seqdist** and **folding** are secondary/optional.

**The testing layer is built and in the repo** (`im-pytest` + `projects/`). Every project ships three ways — the friendly hidden check widget (early self-checking + project work), raw `pytest` (week 9), and student-authored tests (capstone) — all validated end to end. See `projects/<name>/` for each ported suite, stub, data, encrypted solution, and a `solution_walkthrough.ipynb`.

**Assessment.** There are **no mandatory graded hand-ins for now** — the projects are formative, and students verify their own work with the im-pytest suites. If graded assessment is added later, the natural candidates are the translation warm-up and the HIV guided project (both auto-checkable via their suites); grade *process* (plan, tests written, logbook) over *product* (see §9).

---

## 8. The AI-role ladder, badges & logbook (locked; detail in `course-plan.md`)

The AI's sanctioned role escalates with the student's competence, one named role at a time, each a two-word name + a one-sentence dogma:

| Wk | Role | Dogma |
|----|------|-------|
| 1 | **Explainer** | It explains; the running machine decides if that's true. |
| 2 | **Translator** | It turns errors and jargon into plain words; the interpreter has the final word. |
| 3 | **Illustrator** | It gives more examples like the one you know; predict before you run. |
| 4 | **Comparer** | It offers another way; you decide which is better, and why. |
| 5 | **Drafter** | It drafts a small piece you can already read; read it, run it, compare it. |
| 6 | **Unreliable Narrator** | It states things confidently — including biology — that can be false. Check everything. |
| 8–9 | **Worker** | It does a job you've specified; your tests decide if it's done. |
| 10–11 | **Collaborator** | You plan and specify; it builds piece by piece; you verify each piece. |
| 12–14 | **Delegate** | You hand it a job you couldn't do alone — and you stay responsible for the result. |

Every exercise carries a **licence badge** (🟢 the role permitted, or 🔒 `SOLO` — do it yourself first). The **AI lives in the browser**; VS Code stays an AI-free space all term. Each week prompts one **logbook** entry: what the AI got right, what it got wrong, how the student knew.

---

## 9. Assessment (deferred)

No mandatory graded hand-ins are part of the current design — the projects are **formative**, with students checking their own work through the im-pytest suites. When graded assessment *is* designed, the course's logic argues for assessing **judgment and verification, not just working output** (otherwise a student passes by pasting an AI's answer — the exact failure the course exists to prevent). Levers to reach for then, several free from the structure above:

- Grade the **plan** and the **tests the student wrote** as deliverables in their own right.
- Grade the **logbook / prompt journal** — honest reporting of the AI's failures and the student's catches.
- Weight "can explain and defend every part of this program" above "it runs" in the capstone rubric.
- The translation and HIV suites are auto-checkable (a grade/report mode can be re-added to im-pytest when needed).
- **An exam format that tests the transferable skill directly:** hand the student a piece of AI-generated code, ask them to find the defect, fix it, and justify the fix.

---

## 10. Pitfalls & mitigations

| Pitfall | Mitigation |
|---------|-----------|
| Functions/scope cliff (wk6) | Dedicated TA (wk7), `%%codelens` on frames/scope, high exercise density, no competing new-hard concept |
| Iteration/nested cliff (wk7–8) | Same pattern; dedicated TAs (wk8, wk9); `%%steps`/`%%codelens` |
| Lab-split weeks 4–5 (no own TA, half-cohort away) | Light, self-recoverable container topics; self-checking widgets substitute for the missing TA; TA6 catches up wk4+wk5 |
| Meta-tool overload | Staggered tool schedule (§5); the AI confined to its own weekly slot |
| Over-reliance on AI | Licence badges + `SOLO` exercises; the logbook; "verify everything" rule; the whole role ladder |
| Hallucinated biology (high-stakes for this cohort) | The Unreliable Narrator week (wk6/wk10); "verify domain facts, not just code" |
| Workload creep losing the weakest 20% | Required work capped (§6); enrichment optional; breather weeks 1, 4–5, 14 |
| Voice/scope drift in materials | Authored against the writing-style guide + quality checklist in the repo `CLAUDE.md` |

---

## 11. Decisions

**Resolved.**
- The `translationproject.py` stub is fixed (`translate_codon` returns `'?'` for an untranslatable codon, not the leftover `'kasper'`).
- **No mid-course auto-checked mini-project** — weeks 1–8 stay exercise-only; the first project is the week 10–11 guided one.
- **No mandatory graded hand-ins for now** — the projects are formative (§9).
- **Classes are in the core** — a week-7 lecture on the basic scaffolding (`class`, `__init__`, `self`, attributes, methods, light `__str__`) with exercises that have students *add a method to a given class*, so they understand the machinery. Advanced OOP stays cut to an optional appendix. Tuples fold into week 5 (a short coda to lists) so nothing is displaced.

**Still open.**
1. **Per-week required-hour budgets** — validate the §6 estimates against a real cohort.

---

*Once §11 is settled, the next production step is Week 1 end to end — the integrated specimen (first script, the machine model + poster, the compiler thesis staged so students derive it, the first Explainer exercise, the logbook + badge reference page) — built in markdown against the repo `CLAUDE.md`.*
