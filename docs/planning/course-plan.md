# Instructing Machines — Course Plan & Learning Goals (v2)

*A planning document for the 14-week programming course for undergraduates in Molecular Biology and Molecular Medicine. This revision integrates the decision to introduce AI from week 1, the "AI role" dogma and permission system, the notebook + terminal split, and the five pedagogical widgets. Everything here is a draft for discussion.*

---

## 1. What this course is really for

The stated goal decides every design question downstream:

> Teach basic programming — **not to make programmers**, but as a means to train abstract and computational thinking, and to give students the understanding and vocabulary that let them take advantage of AI for producing code.

Two consequences follow.

First, the fundamentals are not "syntax to memorize." They are the construction of a **mental model of computation** — the substitution/reduction view of evaluation, the notion of a value with a type, a function as a contract, a test as a definition of correctness. That model is the durable payload. A student who has it can steer and check an AI long after they've forgotten the exact syntax of a comprehension.

Second, the AI skills are not "prompting technique," which dates fast and differs per tool. They are the same skills the fundamentals build, now pointed at code the student did not write: **decompose, specify, read, judge, iterate.** Testing is the hinge between the two — a test is an executable specification, and specification is the single most important skill in working with an AI.

**We introduce the AI from week 1.** Not as a finished tool, but in a role that grows as the student's competence grows, so they *feel their leverage increase* as they understand more. That felt experience — "the same machine becomes more powerful in my hands, and I can trust it more because I can now check it" — is itself one of the deepest lessons the course teaches.

---

## 2. The central thesis, and how students derive it themselves

The opening frame is the **evolution of instructing a machine**: from electrical signals to machine code, to assembly, to compiled languages, to interpreted languages like Python, to natural language through an AI — each step trading precision and control for expressiveness and closeness to human language. An AI, *for the purpose of producing code*, can be introduced as **one more layer of compilation**: it takes a description even closer to natural language and turns it into code the machine runs.

The power of this framing is where the metaphor **breaks**, and the design goal is to let students walk into that break themselves. A compiler and an interpreter are *deterministic, meaning-preserving* translators: the same input always yields the same output, and the output means exactly what the input said — which is why you can trust a compiler without ever reading its assembly. An AI is a *probabilistic, meaning-approximating* translator: the same prompt can yield different code, and the code may not mean what you asked.

> **Design principle — let them derive the thesis.** We present the AI as "just another layer of compilation," and then set up the moment where a student asks *"but is it really like a compiler?"* When they ask that, they have derived the entire justification for the course themselves: *because this new translation layer is unreliable, I must be able to read the language it emits (Python) and check that it means what I wanted — and understanding Python is exactly what lets me do that.* You trust a compiler; you verify an AI. Nothing we could tell them lands as hard as the conclusion they reach on their own.

Use the history to pre-empt the "why learn Python at all" question: at every previous layer, people predicted the skill below would become obsolete, and every time, understanding the layer below stayed valuable exactly for the cases where the translation went wrong or the stakes were high. Molecular biology is full of high-stakes cases.

---

## 3. The AI-role ladder: weekly dogma and a visible licence

Two problems have one shared solution. Students need (a) a crisp, memorable idea of *how* they may use the AI each week, and (b) an unambiguous signal, on every exercise, telling them *whether and how* AI use is sanctioned right now so they never wonder "is this cheating?".

The solution is a single **ladder of named roles**. Each role is a two-word name plus a one-sentence **dogma** — the rule for that role. The roles are **cumulative**: reaching a new rung never revokes an earlier one. The role's name doubles as the **licence badge** printed on every exercise, so the same vocabulary that defines the week also defines what's allowed.

### The ladder (the AI's role grows as the student does)

| Wk | Role | Dogma (the rule, stated to students) | Unlocked because the student can now… |
|---|---|---|---|
| 1 | **Explainer** | *It explains what code means. The running machine — not the AI — tells you if that's true.* | …run a program and read its output |
| 2 | **Translator** | *It turns error messages and jargon into plain language. The interpreter has the final word.* | …read an error and trace evaluation |
| 3 | **Illustrator** | *It gives you more examples like the one you know. Predict the result before you run it.* | …read and write small functions |
| 4 | **Comparer** | *It offers another way to do it. You decide which is better, and you say why.* | …compare two pieces of code |
| 5 | **Drafter** | *It drafts a small piece you can already read. Read it, run it, compare it to what you expected.* | …read loops, collections, files |
| 6 | **Unreliable Narrator** | *It states things confidently — including biology — that can be false. Check every claim.* | …judge correctness, incl. domain facts |
| 7 | **Worker** | *It does a job you have specified. Your tests decide whether it's done.* | …write tests |
| 8–11 | **Collaborator** | *You plan and specify; it builds piece by piece; you verify every piece.* | …decompose, spec, and test a program |
| 12–14 | **Delegate** | *You hand it a well-specified job you couldn't do alone — and you remain responsible for the result.* | …run the full plan→spec→prompt→verify loop |

These nine roles cluster into the four competence rungs from the pedagogy: *can barely read* (Explainer, Translator) → *reads/writes small functions* (Illustrator, Comparer) → *handles programs* (Drafter, Unreliable Narrator) → *can verify* (Worker, Collaborator, Delegate). The whole-course arc is one sentence: **the AI's role grows exactly as the student's competence does.**

### The AI licence badge (so permission is never ambiguous)

Every notebook opens with a callout — *"🤖 AI this week: **Drafter**"* — restating that week's dogma and noting that all earlier roles remain in force. Then **every exercise carries a badge** naming the maximum role permitted for that exercise, drawn from the same ladder, plus one special tag:

- 🟢 **`AI: Drafter`** (or any role name) — AI use up to and including that role is sanctioned here.
- 🔒 **`SOLO`** — do this one yourself first, no AI. Reserved for exercises whose whole point is building the raw muscle (evaluation tracing, writing a first function, reading code unaided).

Because the ladder is named and cumulative, a single badge fully specifies what's allowed. Define the badge vocabulary once on a permanent reference page students can always return to. Three payoffs: it removes the "am I cheating?" anxiety, it makes the escalation *visible* week over week, and it quietly teaches a real-world truth — different contexts sanction different AI use, and a competent person knows which context they're in.

### The AI logbook (so they see their own leverage grow)

From week 1, each student keeps a running **AI logbook** — one short entry per week: *something the AI got right, something it got wrong, and how they knew.* It is small, but it does a lot: it makes the growing-leverage experience explicit and personal, it builds the habit of skeptical verification from day one, it produces a term-long record of the student's own development, and it hands you assessment material for free (see §7). By week 14 the logbook is a visible arc from "it explained a line for me" to "I caught it inventing a gene function and my test proved it."

---

## 4. Two environments, introduced in order — and the AI kept outside both

The course uses script/terminal work **and** notebooks, but not side by side and not at the same time. They come in a deliberate order, because the first exists to build a mental model the second one hides.

**First, scripts in the terminal — to make the machine legible.** Before notebooks, students write a `.py` file in the editor, save it to disk, and run it with `python myfile.py` in the terminal. This is slower, and that is the point: it forces apart four things a notebook silently fuses — *a file of code sitting on the hard disk*, *the Python interpreter* (a program that reads that file), *the CPU* that actually carries out the work, and *the terminal* where you launch it and watch the output. In a notebook a cell "just runs," so these distinctions can never be learned there; they have to be built first.

**Then IPython and notebook cells — once the model is in place.** With the script picture established, introduce IPython and then notebook cells as a more convenient, interactive way to run Python: a session that stays alive in memory and remembers earlier cells.

**The `script-widget` removes the back-and-forth.** So students don't have to shuttle between terminal and notebook once notebooks arrive, your `script-widget` turns a notebook cell into a small *pretend script* that runs in isolation — the fresh, start-to-finish, self-contained behaviour of `python file.py`, but inside a cell. That lets you keep teaching the script *mental model* (isolation, no leftover state) without leaving the notebook, and lets students feel the difference between "a cell that remembers" and "a script that starts clean" in one place.

**The AI is kept outside both (see §9).** Neither the editor nor the notebook contains the AI. It lives in a separate window — the browser — so that consulting it is always a deliberate act. The notebook and terminal are where the machine's truth is made *visible* (via the widgets, §5); the AI is somewhere the student chooses to walk to.

**A visual anchor for all of this.** These distinctions — disk vs. memory, file vs. running program, editor vs. terminal vs. interpreter, script vs. cell, machine vs. AI — arrive faster than beginners can absorb them. The **re-anchoring poster** (a one-page visual, delivered alongside this plan) lays out every component and how they relate, with short captions, so students can reorient whenever the vocabulary piles up. It is meant to sit beside every early exercise and be returned to all term.

---

## 5. The five widgets, and how to apply them

The widgets (the notebook successors to `bp-help`, `myiagi`, `pysteps`) share one property that makes them perfect for this course: **they make the machine's truth visible.** That is exactly what lets a beginner *adjudicate the AI*. The unifying rule to teach — the operational form of "the machine adjudicates" — is:

> **The AI predicts; the widget proves.** Whenever the AI claims what code does or what a value will be, check it with the widget that shows the machine actually doing it.

### `steps-widget` — `%%steps` / `# PRINT STEPS` (successor to `pysteps`)
Renders the substitution/reduction trace of a tagged statement as a widget. **Primary home: week 2**, as the ground truth behind expression evaluation, paired with the puzzle widget below. **As an AI tool:** the canonical week-2 demonstration of the AI-vs-machine distinction — the AI *predicts plausible tokens* and can be wrong about what `4 * y + x` evaluates to; `%%steps` *shows the interpreter actually reducing it*. First, vivid, memorable proof that the AI is not an oracle.

### `puzzle-widget` — `%%puzzle <result>` (successor to `myiagi`)
Students drag scrambled code lines into the order that produces the target value; it re-runs after every move and checkmarks when correct. **Primary home: weeks 2–4**, for evaluation order and for assembling small programs from parts — self-checking, low-stakes, daily-practice-friendly like `myiagi`. **As an AI tool:** later in the course, "reassemble the AI's lines into a working order" turns reading generated code into an active, checkable task, and makes the point that *plausible lines in the wrong order don't run* — order and structure are meaning.

### `codelens-widget` — `%%codelens` (Python-Tutor execution visualizer)
Guo's Online Python Tutor engine in a notebook: step through execution with heap and reference diagrams, aliasing, recursion, and class instances. **Primary home: weeks 4–6**, exactly when objects, references/aliasing, collections, and classes become confusing on paper. **As an AI tool — its highest-value use:** paste AI-generated code into `%%codelens` and *watch what it actually does*, versus what the AI claimed. This is how "read before you run" becomes "watch before you trust" — the single most powerful verification move available to a student who can't yet write exhaustive tests. It should be the students' default reflex whenever a Drafter/Worker hands them something non-trivial.

### `turtle-widget` — animated turtle graphics in the notebook
Ordinary turtle code replayed as a smooth animation with the active line highlighted. **Primary home: weeks 3–4**, for functions and iteration with immediate, motivating visual feedback (a loop *draws a square* in front of you). **As an AI tool:** turtle is the ideal *first safe domain for the Drafter*, because verification is trivial for a beginner — you can literally *see* whether the AI's code drew the right shape. Visual correctness lowers the bar to catching a mistake, so students practise judging generated code before they can read every line of it.

### `script-widget` — a notebook cell that runs as an isolated script
Turns a notebook cell into a *pretend script*: it runs start-to-finish in a fresh, isolated namespace, like `python file.py`, instead of in the notebook's persistent session. **Primary home: the transition from terminal to notebooks (early weeks).** It lets you keep teaching the script mental model — a program that starts clean every time, with no leftover state — without sending students back to the terminal, and makes the *script vs. notebook-cell* distinction something they can feel with two adjacent cells. It matters for the AI half too: a "pretend script" is a clean, reproducible place to run and test AI-drafted code, closer to how the project test-suites actually execute it.

### `snippet-cast` — annotated snippet → narrated screencast (`%%snippet-cast` / CLI)
Turns a Python snippet with `#:` narration comments into an MP4 with progressive reveal, a live variable panel, and spoken narration. This is primarily a **teacher production tool**, and a strong one for this course:
- Produce the **annotated human–AI transcripts** as short narrated videos — including "here's the AI's code, here's the bug, here's the test catching it" — which is far more vivid than a static transcript.
- Generate consistent worked-example videos for the fundamentals in your own voice at low effort.
- **As a student assessment**: have students `snippet-cast` a narration of their *own* code, explaining each line. Narrating a line forces you to actually understand it — it's the reading/judging skill turned into a deliverable, and it's very hard to fake with pasted AI output.

A compact placement view:

| Widget | Fundamentals home | Role in the AI story |
|---|---|---|
| `steps-widget` | Wk 2 — evaluation | AI predicts, `%%steps` proves — the first AI-vs-machine demo |
| `puzzle-widget` | Wk 2–4 — order, structure | Reassemble/read generated code as an active check |
| `codelens-widget` | Wk 4–6 — refs, objects, classes | *Watch* what generated code really does before trusting it |
| `turtle-widget` | Wk 3–4 — functions, loops | The safe first domain for judging a Drafter's output visually |
| `script-widget` | Terminal→notebook bridge | Clean, isolated place to run and test generated code |
| `snippet-cast` | (teacher) all weeks | Produce narrated transcripts; students narrate their own code |

---

## 6. The AI thread across weeks 1–7 (with widgets and dogma in place)

Each addition is small and attached to a topic you already teach, not a parallel track.

**Week 1 — your first script + the thesis.** Setup, then write a first `.py` file and run it in the terminal (`python hello.py`) — the moment to build the file/disk/interpreter/CPU/terminal picture (§4), with the re-anchoring poster introduced here as the map they'll keep returning to. Tell the levels-of-instruction story; introduce the AI as "one more layer of compilation" and set up the compiler question (§2). Seed the founding rule: *the running machine is the only truth; every advisor — textbook, tutor, AI — is fallible.* First hands-on, licence **Explainer**: have the AI (in the browser) explain a line of their first program, then confirm or refute it by running it. Start the logbook.

**Week 2 — evaluation + the first AI-vs-machine proof.** The AI as **Translator** for errors and jargon. The concept lands through the widgets: the AI *predicts*, but `%%steps` *shows the interpreter reducing the expression*, and `%%puzzle` drills the same order. Some exercises here are 🔒 **SOLO** (trace it yourself in your head / with `myiagi`-style puzzles first), then a 🟢 **Translator** exercise where the AI explains an error the interpreter actually threw.

**Week 3 — conditionals & functions.** The AI as **Illustrator**: "give me more examples like this." Predict-before-you-run is the discipline. `turtle-widget` makes functions and simple loops visible and fun; a Drafter-preview is safe here precisely because output is visual. Concept: a prompt is an instruction — vague prompt, vague result, exactly like vague code.

**Week 4 — objects & collections.** The AI as **Comparer**: "show me another way," student decides which is better and *why*. `codelens-widget` enters to make references and aliasing visible — and doubles as the tool for checking a Comparer's alternatives actually behave the same. Concept: the AI is a great source of *idioms and vocabulary* — names for things you couldn't yet name.

**Week 5 — dicts, iteration, files, comprehensions.** The AI as **Drafter** of small, readable pieces. Discipline: scope the request to something you can read, then *read, run, compare* — `%%codelens` for anything non-obvious. Concept: the AI only knows what you tell it; context and examples improve output — the first taste of specification.

**Week 6 — classes & data structures.** The AI as **Unreliable Narrator**: now that students can judge more, confront confident wrongness head-on, *especially wrong biology*. Exercises where the AI states a plausible but false claim (about code and about molecular biology) that the student must catch — with `%%codelens`/running as the adjudicator. This is the crucial "verify domain facts, not just code" lesson, and it matters more here than in any CS class.

**Week 7 — testing (the pivot).** The AI as **Worker**: it does a job you've specified, and your **tests** decide whether it's done. This fuses the two threads and is the on-ramp to the AI half. The move from notebook exploration to terminal test-suites (`python test_*.py`) is the move from "watch what it does" to "prove it's correct."

---

## 7. The AI arc, weeks 8–14 (picking up warm, not cold)

Because students have used the AI as Explainer→Worker for seven weeks, **week 8 is consolidation and theory, not first contact** — which is stronger. "You've been using this for seven weeks; now let's name exactly what it is."

**Week 8 — Naming the machine.** Consolidate the ladder into an explicit mental model; make the compiler thesis (§2) explicit now that they've *felt* it; formalize the golden rules (*never accept code you can't read and can't test*). Extend the "type it, don't paste it" oath to AI: even AI-suggested code gets read and typed, not blindly accepted. Licence steps up to **Collaborator**.

**Week 9 — Specification & testing as the contract.** The heart of the arc and the payoff of week 7. A test is an executable specification: it's how you tell truth from plausible. Workflow: vague ask → concrete examples → tests → prompt → run tests → accept or reject. Reuse the palindrome / DNA-translation examples. The lesson lands when a student's *own* test catches AI code that looked perfect.

**Week 10 — Reading and judging generated code.** The most important skill for a non-programmer who uses AI. Build the vocabulary of critique (wrong variable, off-by-one, unhandled edge case, wrong data structure, silent failure, plausible-but-wrong biology). "Spot the bug in the AI's code" exercises run through the test harness; `%%codelens` to watch the failure happen; a reusable **code-judging rubric** they'll carry into the capstone; precise change-requests instead of "fix it."

**Week 11 — Decomposition & planning before prompting.** Students drive, the AI types. Before touching the assistant, break the problem into named, testable functions and write a short plan (name, inputs, outputs, test idea); then prompt piece by piece, verifying each against tests. Planning, testing, and prompting become one loop. A **plan template** and a "submit the plan before you may prompt" exercise.

**Weeks 12–14 — Capstone: the Delegate.** A molecular-biology pipeline the student could not write solo — e.g. read a FASTA file, quality-filter, find ORFs, translate, compute GC content and codon usage, emit a report — offered as one well-scoped default plus a couple of alternatives. The workflow *is* the four words: **plan → specify with tests → prompt → read & verify → iterate.** A partial `test_*.py` suite is provided; students write more themselves; the agentic in-editor mode is permitted here (§6).

- **Week 12** — choose, decompose, write the plan and first tests (reviewed before building).
- **Week 13** — build with the assistant, verifying every piece; keep the prompt-journal strand of the logbook.
- **Week 14** — finish and integrate; then the critical discussion: the limits of the machine — over-reliance, hallucinated biology, code that passes weak tests but is still wrong, when *not* to use AI, honest attribution. Short presentations or a written reflection (a natural `snippet-cast` deliverable) close the course.

---

## 8. Assessment (brief, to react to)

The course's own logic argues for assessing **judgment and verification, not just working output** — otherwise a student can pass by pasting an AI's answer, the exact failure mode the course exists to prevent. Practical levers, several of which come for free from the structure above: grade the **plan** and the **tests** as deliverables in their own right; grade the **AI logbook** (honest reporting of the AI's failures and the student's catches); have students **narrate their own code** via `snippet-cast` (very hard to fake with pasted output); and in the capstone rubric weight "can explain and defend every part of this program" above "the program runs." An effective exam format: hand the student a piece of AI-generated code and ask them to find the defect, fix it, and justify the fix — the transferable skill, directly tested.

---

## 9. Tooling recommendation — the AI outside the editor

Reconsidering the earlier in-editor recommendation: **keeping the AI out of VS Code is the stronger choice for this course.** With no good free in-editor option and Microsoft **Copilot Chat reachable in the browser using the students' existing student credentials**, the browser route is both the practical option and the pedagogically better one.

The decisive point is *deliberateness*. An in-editor assistant — even a chat panel — sits one keystroke away and quietly invites use, whereas the whole course is about making AI use a deliberate, licensed choice (§3). Putting the AI in a **separate browser window** turns "consult the AI" into a small physical act the student chooses to take — exactly the habit the licence badges and dogma exist to instill. It also keeps **VS Code as a guaranteed AI-free space for the whole course**: the place where the student's own fingers and mental model do the work, protecting the "type it, don't paste it" discipline where it matters most.

Practical implications:

- Copying code and errors **by hand** between browser and editor is a feature, not a bug — it forces reading, and it naturally throttles over-reliance.
- The licence ladder still stages capability, now by *what students are asked to do in the chat* rather than by which tool: Explainer→Worker in weeks 1–7, Collaborator in 8–11, Delegate in the capstone. There is no agentic file-editing in this setup — and for a course whose goal is judgment, hand-carried chat is arguably ideal; the capstone's "build beyond your unaided reach" is reached through disciplined plan→prompt→verify, not autonomous edits.
- Confirm the exact Copilot Chat access path for AU student accounts and any data/privacy guidance, and build the week-1/week-8 setup pages around the browser login rather than an extension.
- One trade-off to accept openly: students forgo in-context autocomplete and repo-aware suggestions. Given the course goals, that loss is aligned with what you're teaching, not counter to it.

---

## 10. Suggested next steps

1. React to this revision — especially the role ladder and badge names (§3), the widget placements (§5), and the reframed week 8 (§7).
2. Then I'll draft **Week 1's material** end to end as a notebook in your book's voice: the levels-of-instruction thesis, the compiler question staged so students derive it, the first Explainer exercise, the logbook kickoff, and the badge/reference page — so you have a concrete specimen of the *integrated* approach (fundamentals + AI + widget + dogma) rather than of the AI half alone.
3. In parallel I can draft the **capstone brief and its starter `test_*.py` suite**, since it anchors the back three weeks and, working backward, tells us exactly what weeks 9–11 must prepare students to do.

The fastest way to test the whole approach is to build one week end to end and look at it, rather than to keep planning in the abstract.
