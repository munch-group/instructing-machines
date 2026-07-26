# The AI arc — content map (weeks 9–14)

*A map of the notes and exercises that flesh out the AI arc, so we can judge what realistically fits a 45-minute slot and how the notes, the check widget, and the projects interface. The one fully-drafted note — `reading-and-judging.md` (week 10) — is the density/voice specimen; everything here is calibrated to that unit: roughly one worked example + a reusable rubric/template + 3–4 interspersed exercises + a logbook prompt per 45-minute demanding slot.*

## The through-line

The AI thread runs in the short "different" slot every week (Explainer → Delegate). From week 9 the *demanding* slots turn from new syntax to **applying it through verification**, and the escalating role is what each note trains:

| Wk | New AI-arc note (demanding slot) | AI role | Core idea | Interfaces with |
|----|----------------------------------|---------|-----------|-----------------|
| 9 | **Tests are the contract** *(drafted: `tests-are-the-contract.md`)* | Worker | A test is an *executable specification*: write the test first, let the AI fill the function, and the test tells truth from plausible. | im-pytest **mode 2** (raw `pytest`), **mode 3** (write your own `assert`s); the testing chapter |
| 10 | **Reading & judging code you didn't write** *(drafted: `reading-and-judging.md`)* | Unreliable Narrator | The AI produces code that runs and is wrong, and wrong *biology*. Judge it with a rubric; the machine is the witness. | the judging rubric; the **check widget**; the HIV project |
| 11 | **Plan before you prompt** *(drafted: `plan-before-you-prompt.md`)* | Collaborator | Break a problem into named, testable functions and write the plan *before* touching the assistant; drive it piece by piece. | the **plan template**; `%%test` per piece; the HIV build |
| 12–13 | **Delegating a whole job** *(drafted: `delegating-a-whole-job.md`)* | Collaborator → Delegate | Assemble plan + specify + judge + iterate into one loop on a task beyond your unaided reach; the provided suite is a floor; keep the prompt journal. | the assembly capstone; im-pytest; the prompt journal |
| 14 | **The limits of the machine** *(drafted: `limits-of-the-machine.md`)* | (reflection) | Automation bias, tests necessary not sufficient, hallucinated biology, when *not* to use AI, responsibility that does not transfer, honest attribution. | the logbook arc; a closing reflection |

## Per-note detail (what each slot holds)

**Week 9 — Tests are the contract.** Do-first: take a vague ask ("a function that finds the GC-richest window"), turn it into concrete input→output examples, turn those into `assert`s, *then* let the assistant write the function and run the tests. Refrain: a green test is the only reason to believe generated code. Exercises: (a) turn one vague ask into three examples then three `assert`s; (b) 🔒 SOLO write one *failing* test and one *passing* test for a given function; (c) prompt the assistant for a function that "looks perfect," then catch it with your own nasty test. Interface: this is where students first run raw `pytest` (mode 2) and first author their own tests (mode 3).

**Week 10 — Reading & judging *(drafted; see `reading-and-judging.md`)*.** Worked example: an AI `reverse_complement` that complements but forgets to reverse (passes on `'A'`/`'AAAA'`, fails on `'ATGC'`); the judging rubric; a confidently-wrong-*biology* example (C mispaired); precise change requests; judging with the check widget. Ties directly into next week's HIV project.

**Week 11 — Plan before you prompt.** Do-first: hand students a small multi-function task (e.g., "from a FASTA string, report each sequence's length and GC content") and have them fill a **plan template** — one row per function: name, inputs, outputs, one test idea — *before* prompting anything. Then prompt piece by piece, `%%test`-ing each. Exercises: (a) 🔒 SOLO decompose a task into named functions on paper; (b) fill the plan template; (c) "submit the plan before you may prompt" — build one function from your own plan with the assistant and verify. Interface: the plan template becomes the scaffold students carry into the capstone; each planned function is a `%%test` unit.

**Weeks 12–14 — the capstone (assembly).** These are clinics, not new-concept lectures. Week 12: choose/scope, decompose, write the plan and the first tests (reviewed before building). Week 13: build with the assistant against the suite, keeping the **prompt journal** (what the AI got wrong, how you caught it). Week 14: finish, then the **limits-of-the-machine** discussion and reflection. Interface: the ported `assemblyproject` suite is the adjudicator throughout; the prompt journal feeds assessment.

## Realism notes (what this exercise surfaced)

- **One note ≈ one worked example + one reusable artifact (rubric/template) + 3–4 short exercises + a logbook prompt.** The week-10 draft is about the largest that fits a 45-minute slot with in-class exercises. Anything with two big new artifacts (e.g. a rubric *and* a template in one slot) should be split.
- **Week 9 is the densest and the riskiest to overload:** it carries the testing chapter *and* the spec-as-contract framing *and* the first raw-pytest exposure. Consider letting the testing mechanics live in the week-9 *slot A* (the existing testing note, reworked) and keeping *slot B / the AI slot* purely for "the test is the contract you give the AI." Flagged for a decision.
- **The projects carry the weight from week 11 on.** Weeks 12–14 need very little new *note* content — they are supported build time. So the writing effort concentrates in weeks 9–11 (three notes) plus the week-14 limits piece; the capstone weeks need briefs and clinic prompts, not chapters.
- **Every exercise resolves to the check widget.** That keeps the arc honest: each new skill (spec, judge, plan, delegate) ends with the machine delivering a verdict, so "the AI predicts; the widget proves" is not a slogan but the literal structure of every exercise.
