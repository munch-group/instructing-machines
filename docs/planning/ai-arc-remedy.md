# Remedying the AI arc

*The role ladder is the spine of this course. Read as it currently stands in the book, it does not run straight. This is what is bent, and what would straighten it.*

This document is downstream of item 4 of `checklist.md` ("Consistency of the AI thread"). It is not a rewrite of the pedagogy, the ladder in `intro/course-introduction.qmd` §`sec-badges` and `ai/meet-ai.qmd` is sound, and nothing here proposes changing what the nine roles mean. The problem is entirely one of delivery: which role is licensed in which week, by which note, with how much practice. Everything below was measured from the shipped book, by walking `_quarto.yml` in order and reading every `#### Exercise` heading and the badge under it.

## The census

Across the whole book there are 436 badged exercises. They fall out like this. (This is the book as it stood *before* the remedy; the seven moves below have since been carried out, and the after-state is in the **After** section at the end.)

| Role | Badges | Note that introduces it | First week a badge appears |
|---|---|---|---|
| `SOLO` | 338 | — | 1 |
| Explainer | 44 | `meet-ai.qmd` (wk 1) | 1 |
| Translator | **0** | nowhere | never |
| Illustrator | **0** | nowhere | never |
| Comparer | 35 | `ask-for-another-way.qmd` (wk 6) | **2** |
| Drafter | 11 | `let-it-draft.qmd` (wk 7) | 7 |
| Unreliable Narrator | 5 | `reading-and-judging.md` (wk 8) | **7** |
| Worker | **1** | `tests-are-the-contract.md` (wk 8) | 9 |
| Collaborator | **1** | `plan-before-you-prompt.md` (wk 10) | **9** |
| Delegate | **1** | `delegate-the-full-problem.md` (wk 11) | 13 |

And week by week, counting only the AI badges:

| Wk | AI roles licensed | Wk | AI roles licensed |
|---|---|---|---|
| 1 | Explainer ×6 | 8 | Unreliable Narrator ×1, Drafter ×1 |
| 2 | Comparer ×21, Explainer ×5 | 9 | Unreliable Narrator ×2, Drafter ×1, Worker ×1, Collaborator ×1 |
| 3 | Explainer ×10 | 10 | Unreliable Narrator ×1 |
| 4 | Explainer ×15 | 11 | **nothing** |
| 5 | Explainer ×3 | 12 | Comparer ×2, Drafter ×1, Explainer ×1 |
| 6 | Comparer ×11 | 13 | Delegate ×1 |
| 7 | Drafter ×7, Explainer ×3, Comparer ×1, Unreliable Narrator ×1 | 14 | none (one `SOLO`) |

Read as a curve, the arc rises steeply to week 7 and then thins to almost nothing exactly where it is supposed to become demanding. The five weeks that carry the four hardest roles carry six badged exercises between them.

## What is wrong

- [x] **Comparer is licensed four weeks before it is taught.** `predict-then-prove.qmd` sits in week 2 and hands out 21 `AI: Comparer` badges; `ask-for-another-way.qmd`, the note that introduces Comparer, is in week 6. This is the single largest inconsistency in the book, and it is 21 exercises deep, so a student meets the fourth level of the ladder as their first substantial AI work. Two smaller versions of the same fault: `classes.ipynb` (wk 7) licenses Unreliable Narrator a week before `reading-and-judging.md` teaches it, and `directing-a-resource.qmd` (wk 9) licenses Collaborator a week before `plan-before-you-prompt.md` teaches it.

- [x] **Translator and Illustrator exist only in the margin note.** They are named in `course-introduction.qmd` and listed in the `.column-margin` ladder in `meet-ai.qmd`, and then never used: zero badges in 436 exercises. A student who reads the ladder and then works the book will conclude that two of the nine levels were quietly cancelled, which is exactly the sort of thing the course teaches them to notice.

- [x] **The top of the ladder is one exercise wide.** Worker, Collaborator and Delegate have one badged exercise each. Against 338 `SOLO` and 44 Explainer, that is not an escalation; it is a mention. The whole argument of the course is that permission is earned by practice, and the final three permissions are granted after a single exercise apiece.

- [x] **Every `.md` note in `docs/ai/` has zero exercises, and they are the six longest AI notes in the book.** `reading-and-judging.md` (2238 words), `plan-before-you-prompt.md` (1949), `tests-are-the-contract.md` (1923), `instruction.md` (1788), `surviving-ai.md` (1739), `delegate-the-full-problem.md` (1698). This is not a coincidence of authorship taste: the badge sweep ran over `.qmd` and `.ipynb` and never touched the `.md` drafts, so the back half of the arc is 11,000 words of prose with nothing to do. `about-microsoft-copilot.qmd` (948 words, week 1) and `finale-kickoff.qmd` (110 words, week 13) are exercise-free for different reasons. Fixing this one item fixes the previous one as a side effect, because those notes are precisely where Worker, Collaborator and Delegate live.

- [x] **Week 9 carries three AI notes; week 11 carries no AI practice at all.** Week 9 is `the-docs-are-the-test.qmd`, `directing-a-resource.qmd` and `documentation-and-resources.qmd`, plus the codon-bias project and `packages-modules.ipynb`, five chapters, three of them AI notes, and it licenses four different roles in five exercises. Week 11 is `delegate-the-full-problem.md` and `seqdist-project.qmd`, and licenses nothing at all. `course-design.qmd` §282 already flagged the overload risk, one week off from where it actually landed.

- [x] **Week 12 reads as a step down.** The week's AI note, `learning-with-an-ai.qmd`, carries a single `AI: Explainer` badge, level one, in the week after Delegate territory opens. The ladder is cumulative so it is not *wrong*, but as the only AI badge in that note it reads as a regression rather than as a deliberate return to a lower level.

- [x] **`course-design.qmd` disagrees with itself in three places.** The live grid at §45–82 matches `_quarto.yml`. The "AI arc (weeks 9–14)" table at §253 is a week or two later throughout (it puts `reading-and-judging` in week 10 where the book ships it in week 8, and `plan-before-you-prompt` in week 11 where the book ships it in week 10) and names two files that do not exist, `delegating-a-whole-job.md` and `limits-of-the-machine.md`, which shipped as `delegate-the-full-problem.md` and `surviving-ai.md`. A third, commented-out grid inside the `{=html}` block at §83 disagrees with both, putting `let-it-draft` in week 11 and `ask-for-another-way` in week 12. The Decisions paragraph adds a fourth small disagreement: it says testing is taught in week 5, one week before the first project; the book teaches it in week 4, two weeks before. Nobody can check the arc against a plan while there are four plans.

## The remedy

Seven moves, in the order I would do them. The first three cost almost nothing and remove most of the incoherence; the fourth is the real writing job.

- [x] **1. Make `_quarto.yml` the plan of record, and say so once.** It is what renders, so it is what students experience; every other grid should be deleted or regenerated from it. Concretely: delete the commented-out grid in the `{=html}` block (it is dead and it is the most divergent of the three), rewrite the §253 table to the shipped weeks and the shipped filenames, and correct the testing-week sentence in Decisions. Then add one line at the top of `course-design.qmd` saying that the week grid is generated from `_quarto.yml` and that changes go there first. Note that `_quarto.yml` currently has uncommitted edits of your own, so this move touches `course-design.qmd` only.

- [x] **2. Re-badge `predict-then-prove.qmd` from Comparer to Explainer.** Read what those 21 exercises actually ask: *predict what this line does, then run it and see*. That is the assistant explaining something that already exists and the machine adjudicating, Explainer, exactly as `meet-ai.qmd` defines it in week 1. Nothing about the exercises changes; only the badge and one sentence of framing. This is a search-and-replace that removes a four-week ladder violation and, incidentally, makes the week-6 arrival of Comparer in `ask-for-another-way.qmd` land as a genuinely new permission rather than as a re-introduction. The two one-badge violations follow the same rule: either re-badge, or accept them as deliberate one-week previews and say so in the note.

- [x] **3. Move `directing-a-resource.qmd` from week 9 to week 11.** One move, three fixes: week 9 drops from three AI notes to two, week 11 stops being an AI hole, and Collaborator stops being licensed a week before `plan-before-you-prompt.md` teaches it, it now arrives a week *after*, which is what the ladder promises. Week 9 keeps the pair that belongs together (`the-docs-are-the-test` and `documentation-and-resources`), and week 11 gets Collaborator practice immediately before the Delegate material.

- [x] **4. Give the six exercise-free `.md` notes their exercises.** This is the substantial one and it is where the arc actually lives. `course-design.qmd` already fixes the unit: roughly one worked example, one reusable artifact (a rubric, a template), three to four interspersed exercises, and a logbook prompt per demanding slot. Applied to the six: `tests-are-the-contract.md` gets three or four `AI: Worker` exercises (turn a vague ask into `assert`s; write one failing and one passing test `SOLO`; then let the assistant fill the function and let the test decide). `reading-and-judging.md` gets `AI: Unreliable Narrator` exercises against the planted-bug examples it already describes. `plan-before-you-prompt.md` gets `AI: Collaborator` exercises around the plan template. `delegate-the-full-problem.md` gets `AI: Delegate` exercises with acceptance criteria written before the prompt. `instruction.md` (week 1) gets two Explainer or `SOLO` exercises. `surviving-ai.md` (week 14) gets reflection exercises that close the logbook arc. Doing this takes Worker, Collaborator and Delegate from one badge each to three or four each, which is what the ladder claims to deliver.

- [x] **5. Decide about Translator and Illustrator: use them or retire them.** Using them is cheap and I would recommend it, because they are genuinely distinct skills and weeks 2 to 4 are over-saturated with Explainer (44 badges, 33 of them in those three weeks). Re-badge a handful of the week-3 `objects.ipynb`/`lists.ipynb` exercises as `AI: Translator`, "describe this loop in one English sentence, then ask the assistant to do the same, then compare" is a translation in both directions and it is already what those exercises want, and add one `AI: Illustrator` exercise to `dictionaries.ipynb` asking for three more examples of a pattern the student half understands. That is perhaps six badges and no new prose. If you would rather not, the honest alternative is to cut both levels from the ladder in `meet-ai.qmd` and `course-introduction.qmd` and ship a seven-role ladder. What should not survive is a ladder with two levels nobody stands on.

- [x] **6. Turn the week-12 Explainer badge into a deliberate return, not a regression.** `learning-with-an-ai.qmd` is about using the Study and Learn agent to teach yourself something, which by week 12 is Collaborator work, not Explainer work. Re-badge it and frame the exercise as the setup for the week-14 AI-off test: use the assistant to learn something, then demonstrate it with the assistant closed. That also gives week 14 something to point back at.

- [x] **7. Make the drift impossible to reintroduce.** Two small pieces of machinery. First, a `.column-margin` strip at the top of each AI note showing the ladder with the roles earned so far in normal weight and the new one emphasised, the students then *see* the arc, which they currently cannot, and an author who adds a badge out of order will notice while writing. Second, `scripts/check-badge-order.py`: walk `_quarto.yml` in order, carry a canonical map of role to introducing chapter, and fail the build if any badge appears before its introducing chapter. It is about forty lines and it is the same script that produced the census at the top of this document. Add it to the render workflow and the ladder stays straight without anyone having to re-audit it.

## After

*Added when the seven moves were carried out. The numbers below come from `scripts/check-badge-order.py --census`, which is the same script that produced the census at the top.*

| Role | Badges before | Badges after | First week a badge appears | Introduced in week |
|---|---|---|---|---|
| `SOLO` | 338 | 353 | 1 |, |
| Explainer | 44 | 67 | 1 | 1 |
| Translator | **0** | 2 | 3 | 3 |
| Illustrator | **0** | 2 | 3 | 3 |
| Comparer | 35 | 14 | 6 | 6 |
| Drafter | 11 | 11 | 7 | 7 |
| Unreliable Narrator | 5 | 8 | 8 | 8 |
| Worker | **1** | 4 | 8 | 8 |
| Collaborator | **1** | 5 | 10 | 10 |
| Delegate | **1** | 4 | 11 | 11 |

Every role now first appears in the week that teaches it, so the "first week" and "introduced in week" columns agree on every row, which is the whole of what was wrong. Week by week the AI badges now read:

| Wk | AI roles licensed | Wk | AI roles licensed |
|---|---|---|---|
| 1 | Explainer ×8 | 8 | Unreliable Narrator ×4, Worker ×3, Drafter ×1 |
| 2 | Explainer ×26 | 9 | Unreliable Narrator ×2, Worker ×1, Drafter ×1 |
| 3 | Explainer ×10, Translator ×2, Illustrator ×2 | 10 | Collaborator ×3, Unreliable Narrator ×1 |
| 4 | Explainer ×15 | 11 | Delegate ×3, Collaborator ×1 |
| 5 | Explainer ×3 | 12 | Comparer ×2, Collaborator ×1, Drafter ×1 |
| 6 | Comparer ×11 | 13 | Delegate ×1 |
| 7 | Drafter ×7, Explainer ×4, Comparer ×1 | 14 | Unreliable Narrator ×1 |

The curve no longer collapses after week 7: weeks 8 to 14 now carry twenty-three AI badges where they carried six, and the four hardest roles have three to five exercises each instead of one. Weeks 2 to 5 still lean heavily on Explainer, which is now correct rather than misleading, those exercises always were Explainer work, they were merely wearing a Comparer badge.

Two things were done differently from the plan above. Move 4 turned out to be smaller than budgeted: all six `.md` notes already ended in two or three exercise paragraphs in the author's voice plus a logbook prompt, and had simply never been formatted as `#### Exercise` headings, which is exactly why the badge sweep missed them. Restructuring what was there and adding one to three genuinely new exercises per note was enough. And several prose exercises the plan listed as Worker or Delegate work turn out to be assistant-free, writing the contract before requesting any code, writing the prompt-journal entry, so they are badged `SOLO` rather than force-fitted to a role count, and new role-appropriate exercises were added beside them instead.

What remains open is exercise *density* rather than exercise *order*. The six `.md` notes now carry three to six exercises each against one to two thousand words, which is thinner than the `.qmd` sessions manage. That is a writing job, not a structural one, and the ladder is straight while it waits.

## What this does not touch

The role definitions, the badge placement (its own line under the heading, the badge itself has since become a small-caps link to the level's section in `intro/course-introduction.qmd`, but it still sits exactly where it sat), the "AI predicts, the machine proves" rule, the logbook, and the browser-only placement of the assistant are all consistent across the book and need nothing. The `SOLO`-heavy balance is also not a defect: 338 of 436 exercises being do-it-yourself-first is the course working as designed, and the remedy above raises the AI count by perhaps twenty exercises, not by two hundred.
