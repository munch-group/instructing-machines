# Who does what: decomposition, tests, and bodies across weeks 6 to 14 {.unnumbered}

An audit of how the three parts of building a program are distributed between the teacher, the student, and the assistant across the AI arc of the course. Read off the chapter and project files as they currently stand, not off the intentions recorded in `course-design.qmd`.

The three parts are decomposition, meaning the decision about what the pieces are and what each one takes and returns; the tests, meaning the executable statement of what correct means; and the bodies, meaning the implementation of each piece. The course has a stated position that these are separable and that the first two are the ones the student must keep. This document asks whether the material actually distributes them that way.

## The current distribution {.unnumbered}

| Week | Decomposition | Tests | Bodies |
|---|---|---|---|
| 6 translation | teacher | teacher | student on the project, AI on a disposable note exercise |
| 7 folding | teacher | teacher on the project, student in the note | student on the project, AI writes its first kept code in the note |
| 8 alignment | teacher on the project, student in the note | teacher on the project, student in the note | student on the project, AI in the note |
| 9 codonbias | teacher, with the student deciding which parts are the library's | teacher on the project; in the note the student tests own code and sanity-checks library output | student on the project, AI writing glue over library calls in the note |
| 10 hiv | teacher on the project, student in the note | teacher on the project, student in the note | student on the project, AI on one planned piece in the note |
| 11 seqdist | teacher on the project, student in the note | teacher, with the student adding nasty cases of their own | student on the project, AI in the note |
| 12 orf | teacher, with the student decomposing the unassessed "On your own" section | teacher, and none at all for "On your own" | student, AI |
| 13 assembly and finale | teacher on the assembly project, student on the finale | teacher on the assembly project, student on the finale | student on the assembly project, AI as Delegate on the finale |
| 14 | student, working from a docstring alone | the student's own understanding, with no machine to appeal to | student, assistant switched off |

## The three parts transfer on three different schedules {.unnumbered}

Body-writing moves to the assistant early and on a clean ladder, and this is the part of the design that works as intended. Week 6 lets it write two versions of a throwaway function so the student has something to compare rather than something to keep. Week 7 lets it write a function the student keeps, safe because the piece is small enough to read in full and a test stands behind it. Week 8 makes it write against a contract the student wrote before it saw the problem. Week 9 restricts it to glue over library calls whose contracts were confirmed in the real documentation first. Weeks 10 and 11 restrict it to one planned piece at a time, taken in dependency order. Week 13 hands it a whole tool. Every step has a stated reason and each one is conditional on the checking discipline introduced just before it.

Test-writing transfers to the student in week 8, in the note on tests as contracts, and the argument for the transfer is strong: writing the test after seeing the code lets the code anchor your idea of what correct means, so the contract has to come first or it proves nothing.

Decomposition transfers in week 10, in the note on planning before prompting, with an equally strong argument: asking for everything in one prompt delegates the thinking and not merely the typing.

Both of those transfers happen only inside the AI notes, and only on small invented side problems. This is the central finding of the audit.

## The projects do not participate in either transfer {.unnumbered}

All eight projects, from translation in week 6 through assembly in week 13, hand the student a complete decomposition and a complete test suite. The decomposition arrives as the "Write a function" prose that names each function, lists its arguments, and states what it must return. The tests arrive as a downloadable `test_<project>.py` alongside the stub file. Neither of these thins out over the eight weeks.

Counting the functions specified for the student in each project gives translation two, folding four, alignment four, codonbias four, hiv five, seqdist five, orf five, and assembly ten. The scaffolding does not fade across the project weeks. It increases, and the assembly project in week 13 is the most heavily scaffolded project in the course.

The consequence is that a student practises writing a contract on `count_codon` and practises decomposition on a paper exercise, and then returns to a project where both jobs have already been done for them. The first occasion on which they decompose and specify something they will actually build, and be assessed on, is the finale in week 13. Two skills that the notes treat as the ones that must remain theirs are never exercised on real work until the last building week.

## Two gaps this opens {.unnumbered}

The first is that `course-design.qmd` states that the scaffolding fades across the project weeks, that the earliest projects arrive fully decomposed with a complete test suite and the later ones give less skeleton and leave more of the tests to the student, and that by the assembly project the student is doing much more of the decomposition and verification. No project file implements this. The intention is recorded and the mechanism does not exist.

The second is that the projects are entirely silent about the assistant. No project chapter carries a licence badge, and none of the eight mentions the assistant at all. The role ladder therefore governs the notes only. For the eight weeks in which students spend most of their hours, the material makes no statement about what the assistant may be used for, which leaves the escalation the notes carefully stage unenforced in the place where it matters most, and leaves each student to decide privately how much of a project the assistant wrote.

## Options for closing the gap {.unnumbered}

Three approaches, which can be combined.

The lightest is to give each project a licence line, stating for that project which role the assistant may take. This costs one line per project, changes no exercise, and makes the ladder visible where students actually work. It also makes the honest observation that the earlier projects are meant to be done without the assistant into something stated rather than assumed.

The middle option is to thin the test suite rather than the decomposition. From roughly week 10 the shipped `test_*.py` could cover only some of the specified functions, with the project text naming which functions the student must write the contract for before implementing them. The decomposition stays given, so the project remains navigable, but the specifying becomes real work on real code. This is the smaller of the two transfers and the one the notes support earliest.

The heaviest is to thin the decomposition in the last one or two projects, giving the goal, the data, and the required top-level function while leaving the intermediate pieces for the student to name. Assembly is the natural candidate because its ten functions make it the clearest demonstration of the problem, and because it sits in the same week as the finale, where the student is asked to decompose from a blank page with no prior practice on anything they will be graded on.

If only one change is made, the licence line is the cheapest and the test-suite thinning is the most valuable.

## Terminology to reconcile {.unnumbered}

The notes `delegate-the-full-problem.md` and `plan-before-you-prompt.md` still refer to the capstone, where the week 13 and 14 notes now say the finale. The word should be settled one way in all five.

`course-design.qmd` still records the student-formulated finale as deferred and the three finale notes as parked for when it is added back. The current `_quarto.yml` places all three in week 13 alongside the assembly project, so that paragraph now describes a state the book has moved past, and should be rewritten to describe week 13 as it stands, with two things happening in it.
