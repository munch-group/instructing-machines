# Proposed authorship progression across the projects, weeks 6 to 13

A design for how decomposition, test-writing, and body-writing should be distributed between the teacher, the student, and the assistant in each project, so that the projects carry the same escalation the AI notes teach. This is a proposal for what the project material should become, not a description of what it currently does. The current state is recorded in `authorship-split.md`, and the short version of it is that all eight projects hand the student a complete decomposition and a complete test suite, so neither of the two transfers the notes stage ever reaches assessed work.

## The principle

Three rules generate everything below.

The first is that a project may ask the student to do only what a note has already taught, and should ask it in the week immediately after it is taught. A skill introduced on an invented problem and never applied to real work has not been taught, it has been mentioned. Applying it one week later, while the note is still fresh, is what turns it into a habit.

The second is that each transfer happens once and does not revert. Once the student is writing the contract for a function in week 8, no later project may go back to shipping every test. A scaffold that comes and goes teaches that the scaffolding, rather than the skill, is what is real.

The third is that the three parts fade on three different schedules, in the order the notes establish them. Body-writing moves to the assistant first and fastest, because it is the part the course is happy to delegate. Test-writing moves to the student second, from week 8, because the note on tests as contracts lands there. Decomposition moves to the student last, from week 10, because the note on planning before prompting lands there. By week 13 the student holds both of the parts the course insists must stay theirs, and the assistant holds the part the course is content to give away.

## What fades, and when

| Week | Project | Decomposition | Tests shipped | Assistant licence |
|---|---|---|---|---|
| 6 | translation | all given | all | `AI: Explainer` |
| 7 | folding | all given | all | `AI: Drafter` on one nominated function |
| 8 | alignment | all given | all but one | `AI: Drafter`, after the student's test exists |
| 9 | codonbias | all given | half | `AI: Worker` on library glue |
| 10 | hiv | most given, two pieces the student names | for the given pieces only | `AI: Worker`, one planned piece at a time |
| 11 | seqdist | top-level function only | one end-to-end acceptance test | `AI: Collaborator` |
| 12 | orf | goal and data only | none visible | `AI: Delegate` on specified pieces |
| 13 | assembly | student first, teacher's version revealed after | none visible | `AI: Delegate` |

## Week by week

### Week 6, translation

Nothing fades. This is the baseline against which everything later is measured, and the student has just met the assistant as a Comparer on throwaway code. The project gives both functions fully specified and a complete test suite, and the student writes both bodies.

The one change is that the project should say so. A licence line stating `AI: Explainer`, meaning the assistant may explain an error message or a concept but may not write code the student keeps, converts an assumption into a statement. At present the projects are silent, so a student who uses the assistant to write the whole thing has broken no stated rule.

### Week 7, folding

The first delegation on real work, and it should be small enough to be safe. The project keeps its full decomposition and full test suite, and nominates exactly one of its four functions as the drafting target, chosen as the shortest and most mechanical of them. The student reads the shipped test for that function first, then lets the assistant draft the body, then reads what came back and runs the test.

This is `let-it-draft` applied verbatim: a piece small enough to read in full, with a test already standing behind it. The other three functions carry `SOLO`.

### Week 8, alignment

The first transfer. Three of the four functions ship with tests as before. The fourth ships with a docstring and no test, and the project instructs the student to write the test before writing or requesting any implementation.

Once that test exists, the assistant may draft the body against it. The sequence matters and should be stated as a sequence: contract, then draft, then run. This is the exact claim of `tests-are-the-contract`, that writing the test after seeing the code lets the code anchor your idea of correctness, now made on a function the student is graded on rather than on an invented one.

### Week 9, codonbias

The test transfer widens from one function to half of them, and gains a second dimension. Two of the four functions ship with tests, two ship with docstrings only.

One of the two untested functions should wrap a library call, because that is where the week's other lesson lives. The project asks the student to test their own code and to sanity-check the library's output against the real documentation rather than against a test they invent, which is the distinction `the-docs-are-the-test` and `directing-a-resource` draw. The assistant's licence is `AI: Worker` on the glue over library calls, which is the narrowest useful delegation and the one whose contract can be confirmed in a source that is not the assistant.

### Week 10, hiv

The decomposition transfer begins, and it begins in the smallest form that is still real. The project gives the goal, the data, the top-level function signature, and three of the five helpers. The remaining two are described only by what has to happen between the given pieces, and the student names them, decides what each takes and returns, writes the docstrings, and writes the tests.

Tests ship for the three given helpers and for nothing else. The project requires the plan, meaning the names and signatures of the two new pieces and the order in which they will be built, to be written down before any prompt is sent, which is `plan-before-you-prompt` applied to assessed work. The assistant works one planned piece at a time, in dependency order.

### Week 11, seqdist

Decomposition passes to the student in earnest. The project states the question, the data format, and the signature of the single top-level function that answers it, and nothing else. Every intermediate piece is the student's to name and specify.

The only thing that ships is one end-to-end acceptance test on the top-level function, which tells the student whether the whole thing works without telling them anything about how to build it. All unit tests are theirs. The licence is `AI: Collaborator`, meaning the assistant may take part in the planning conversation, with the student adjudicating every decision, which is the step `delegate-the-full-problem` reaches.

### Week 12, orf

The current project already contains the right exercise in its unassessed "On your own" section. The proposal is to make that section the project. The student receives the biological question and the data, decomposes it entirely, specifies every piece, writes every test, and delegates bodies to the assistant once each piece is specified.

Nothing visible ships. The licence is `AI: Delegate` on individual pieces after specification, which is the last step before the finale.

### Week 13, assembly

Assembly is currently the most heavily scaffolded project in the course, with ten specified functions, which is the sharpest single symptom of the problem. It is also genuinely the hardest decomposition in the course, and simply deleting its scaffolding would be cruel in the same week the finale starts.

The proposal is to keep the teacher's decomposition but withhold it. The student decomposes the assembly problem first, writing down the pieces they think it needs, and only then reveals the teacher's ten-function version and compares the two. Where they differ, the student says which is better and why, using the rubric they learned as a Comparer in week 6, and then builds against whichever they can defend.

This does three things at once. It gives the student the hardest decomposition in the course as real practice, it preserves the teacher's version as the teaching artefact it deserves to be, and it turns comparison, the very first thing the assistant was used for, into the last thing it is used for, applied now to a design rather than to two versions of a loop.

## How the fading is signalled in the project text

Once projects stop being uniform, the student needs to be able to see at a glance what is given and what is theirs, or the fading reads as inconsistency rather than as design.

Each project should open with two short statements. The first says what is given, meaning which functions are specified and which tests ship. The second is the licence line, in the same code-formatted form the notes use, saying which role the assistant may take on this project and on which parts. Both are one line each, and both belong above the first task rather than buried in a section at the end.

It is also worth adding one sentence per project saying what changed since the previous project and why, because the reason is the lesson. A student who reads "you write the test for the fourth function this week, because last week's note showed what happens when the test comes after the code" learns something that a student who simply finds one test missing does not.

## Grading when the student writes the tests

Thinning the shipped tests raises an obvious practical problem, which is that the shipped suite is currently both the student's feedback and the marker's instrument, and those two jobs come apart as soon as the student writes their own tests.

The clean separation is to keep a complete acceptance suite for every project, but stop shipping all of it. The student receives the visible portion described above, and the hidden remainder runs at hand-in, or is released after the deadline. The student's own tests then genuinely function as their contract, written without knowing what will be checked, which is exactly the position they will be in for the rest of their working lives, and the marker keeps a uniform instrument across all eight projects.

This also gives an assessable artefact for the transfers themselves. From week 8 the student's own tests are handed in alongside the code and can be judged on whether they cover the awkward cases, and from week 10 the written plan is handed in and can be judged on whether the decomposition holds together. Both are cheap to mark and both make the two skills the course cares most about visible for the first time.

## What this asks of the notes

Very little, which is the point. The proposal is built so that every transfer lands the week after the note that justifies it, using material that already exists.

Two small additions would help. The projects need somewhere to point when they say what a licence means, so a short reference listing the roles and what each permits, linked from every project, would save repeating it eight times. And week 13's use of the comparison rubric on a decomposition rather than on code is a slight extension of what week 6 taught, so `ask-for-another-way` could gain a closing paragraph noting that the same rubric applies to designs, which also gives that note a forward reach it currently lacks.

## What has to be rewritten to do this

The eight project files change by different amounts, and the work is not evenly distributed. Weeks 6 and 7 need only the licence line and the nomination of one drafting target. Weeks 8 and 9 need the licence line plus the removal of some shipped tests and the corresponding instruction to write them. Weeks 10 through 12 need real rewriting of the specification sections, since the point is to stop specifying. Week 13 needs the least new writing and the most restructuring, because its ten-function decomposition survives intact but moves from the front of the chapter to a reveal partway through.

The test files change in the same pattern, mostly by splitting each `test_<project>.py` into a shipped part and a withheld part, which is a mechanical change to files that already exist.

One open question sits alongside this. `curration-project.qmd` exists on disk at 507 lines and is not in `_quarto.yml`. If it is meant to return, week 12 is where a project with no shipped scaffolding would fit, and it should be assessed against this progression before being slotted anywhere.
