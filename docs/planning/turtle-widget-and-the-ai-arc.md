# The turtle widget and the AI arc {.unnumbered}

Suggestions for how `turtle-widget` could be used to support the AI arc in weeks 6 to 14. Written after reading the widget's own source and every place it currently appears in the repository, so the starting position below is what is on disk rather than what was intended.

## Where the widget currently stands {.unnumbered}

The turtle widget appears in exactly one file in the book, `docs/python/widget-demo.ipynb`, which is a widget showcase and not a course chapter, and which is not in the `_quarto.yml` chapter list. Line 54 installs it, line 252 imports `Turtle` from `turtle_widget`, line 277 instantiates it. `docs/jupyterlite/content/widget-demo.ipynb` mirrors the same cells.

In the planning material it appears once, at line 212 of `course-design.qmd`, as a row reading "Wk 2-3, `turtle-widget` (optional), Visual functions/loops; safe first place to let the AI draft". That is the whole of its presence. It is pencilled in before the AI arc begins, marked optional, and no note uses it.

Everything below is therefore net-new material rather than a revision of something already running.

## What the widget can actually do {.unnumbered}

The demo undersells the widget considerably. Reading the embedded module source shows a tool with more to offer the arc than decorative drawing.

It replays a recorded event stream rather than drawing live. Every run therefore leaves behind a list of operations that is ordinary data and can be inspected and asserted on. The operations include `line`, `move`, `turn`, `teleport`, `dot`, `write`, `stamp`, `fill`, `bgcolor`, `color`, `pen`, `show`, `hide` and `clear`.

It carries an obstacle layer supporting segment, circle and polygon obstacles, and a `sense` operation that draws dashed rays with hit markers. The turtle can therefore detect what is in front of it, which makes navigation problems possible rather than only drawing problems.

It has a `show_code` mode that places the source in a column beside the canvas and highlights the currently executing line as the replay advances, with Replay and Pause controls.

That last capability is the one that matters most here, and it is not a drawing feature. It makes the turtle a third member of the family that already contains `steps-widget` and `codelens-widget`. Where the steps widget proves an expression reduced correctly and codelens proves an object was shared, the turtle proves that a piece of code the student did not write does what someone claimed it does, in a medium where the claim and the evidence are visible at the same moment.

## Week 7, the first draft {.unnumbered}

`let-it-draft.qmd` is the natural first home. The argument is the one `course-design.qmd` already half makes: a wrong drawing is wrong in a way an absolute beginner can see, so the student can practise the reading-and-judging half of drafting before they have a working test in place to lean on.

The exercise shape is to ask the assistant for a function that draws a regular polygon, predict the picture from reading the code before running anything, then run it. The polygon is not the point. The point is that the student formed an expectation from reading and had it confirmed or broken by the machine within seconds, which is the loop the whole arc depends on. The `show_code` column makes the post-mortem cheap when the prediction was wrong, because the student can watch which line produced the segment that went astray rather than guessing.

## Week 8, the turtle used against itself {.unnumbered}

This is the more interesting use, and it is where the turtle stops being a friendly medium and becomes a trap set on purpose. It belongs with `reading-and-judging.md` and `tests-are-the-contract.md`.

Have the assistant produce a function that draws a five-pointed star, and let it produce one whose picture is convincingly star-shaped but whose turtle does not end where it started, or ends facing a different direction than it began. The drawing looks right. The student says it looks right. Then show that composing two calls, or calling the function inside a loop that also moves between stars, falls apart, because the function silently broke a contract nobody had written down.

That is the week 8 argument delivered in a medium where the student can feel the difference between a picture that looks correct and a function that is correct. Once it lands, the exercise inverts: write the contract first, as an assertion on the turtle's final position and heading, and only then let the assistant draft the body against it.

## The rule that keeps the turtle usable after week 8 {.unnumbered}

Eyeball verification is precisely the habit that weeks 8 onward exist to break, so from week 8 on no turtle exercise should be checkable by looking at it. Every one should assert on the recorded event stream, on the final coordinates, on the heading, or on the number of segments drawn. The picture becomes the thing that misleads you rather than the thing that convinces you.

The widget supports this directly because the events are data and not pixels, which is what makes the turtle survivable in the later arc at all. Any note that introduces a turtle exercise after week 7 should state this rule explicitly, because the temptation to accept a drawing that looks right is exactly the automation bias the course closes on in `surviving-ai.md`.

## Weeks 10 and 11, a delegation task with a checkable outcome {.unnumbered}

The obstacle layer and the `sense` operation together give a genuinely non-trivial delegation task, which is what `plan-before-you-prompt.md` and `delegate-the-full-problem.md` currently lack outside the projects.

A maze or a corridor of segment obstacles, a turtle that must reach a target using only `sense` readings to decide where to turn, and a success condition that is a coordinate rather than an impression. This has the shape those two weeks need. It decomposes naturally, into reading the sensor, deciding the turn, taking a step and detecting arrival, so the plan-before-you-prompt discipline has real structure to bite on rather than an invented one. It is beyond what a beginner would write unaided, so the delegation is honest rather than theatre. It cannot be faked by output that merely looks plausible. And each intermediate piece can be verified without the student having to invent test data, because the geometry supplies it.

This is also the closest thing in the course to a non-project problem with enough substance to carry a Delegate exercise, which matters given that the projects themselves are silent about the assistant.

## Two cautions {.unnumbered}

The widget costs a dependency and a chapter's worth of context to introduce. If it enters the arc at week 7 it should have been met in weeks 2 or 3 as `course-design.qmd` already proposes, otherwise the student is learning a graphics API in the middle of the most conceptual week of the term. If the weeks 2 to 3 slot stays optional, the week 7 use has to assume nothing.

There is also a real risk that turtle exercises read as light relief, a break from the serious work, which would undercut week 8 in particular. The framing has to make clear that the drawing is the bait and not the reward.

## If only part of this is taken {.unnumbered}

The week 8 use is the one that earns its keep. It is the only place in the current material where a student can be shown, in a single glance, the gap between output that looks correct and code that is correct, and that gap is the thesis of the second half of the course. The week 7 draft exercise is a cheap and pleasant on-ramp to it. The weeks 10 and 11 navigation task is the largest piece of new work and should only be built if a non-project delegation problem is wanted for its own sake.
