# The turtle widget and the AI arc

Suggestions for how `turtle-widget` could be used in the course, and in particular how it can be introduced early as an object with methods and then retired deliberately in week 8 as the vehicle for teaching students to match the kind of validation to the kind of claim they are making. Written after reading the widget's own source and every place it currently appears in the repository, so the starting position below is what is on disk rather than what was intended.

## Where the widget currently stands

The turtle widget appears in exactly one file in the book, `docs/python/course-tools.ipynb`, which is a widget showcase and not a course chapter, and which is not in the `_quarto.yml` chapter list. Line 54 installs it, line 252 imports `Turtle` from `turtle_widget`, line 277 instantiates it. `docs/jupyterlite/content/course-tools.ipynb` mirrors the same cells.

In the planning material it appears once, at line 212 of `course-design.qmd`, as a row reading "Wk 2-3, `turtle-widget` (optional), Visual functions/loops; safe first place to let the AI draft". That is the whole of its presence. It is pencilled in before the AI arc begins, marked optional, and no note uses it.

Everything below is therefore net-new material.

## What the widget can actually do

The demo undersells the widget considerably.

It replays a recorded event stream rather than drawing live. Every run therefore leaves behind a list of operations that is ordinary data and can be inspected and asserted on. The operations include `line`, `move`, `turn`, `teleport`, `dot`, `stamp`, `write`, `fill`, `bgcolor`, `color`, `pen`, `show`, `hide` and `clear`.

It carries an obstacle layer supporting segment, circle, rectangle and polygon obstacles, and `sense`, `distance_ahead` and `nearest` operations that can draw dashed rays with hit markers. The turtle can detect what is in front of it, and `on_collision` gives it a handler.

It has a `show_code` mode that places the source in a column beside the canvas and highlights the currently executing line as the replay advances, with Replay and Pause controls.

Critically for what follows, it already exposes a complete query API alongside the drawing commands: `position`, `xcor`, `ycor`, `heading`, `isdown` and `isvisible`, plus public counters `nr_collisions`, `nr_left`, `nr_right`, `nr_sense`, `nr_distance_ahead` and `total_movement`, all zeroed by `reset`. Nothing needs to be added to the widget for a student to write an assertion about a turtle's state. The instrument for the week 8 lesson below is already there.

## Introducing it in week 3, as an object with methods

The natural place to introduce the turtle is not as a graphics toy but alongside the string object, when methods are first taught. It fits the existing device exactly: "Hey string, capitalise yourself" acquires a sibling in "Hey turtle, turn yourself".

The pairing earns its keep because the two objects differ in precisely the way beginners find hardest. A string method hands you something back and leaves the string alone, so `s.upper()` is worthless unless you catch the result. A turtle method hands you nothing back and changes the turtle, so `t.forward(50)` is a command whose whole effect is a change of state elsewhere. Students routinely write `s.upper()` on its own line and expect the string to have changed, and the turtle is the object for which that expectation is correct. Having both in view at once, with the query methods `position` and `heading` as a third category that asks rather than commands, gives the distinction between changing something and returning something a concrete home rather than leaving it as a rule to memorise.

From there the turtle is the standard vehicle for nested loops, and it is a good one because the failure modes are legible. A loop nested the wrong way round produces a picture that is wrong in a way that tells you which loop is which.

## Retiring it in week 8, and what the retirement teaches

The retirement should be explicit. A tool that quietly stops appearing teaches nothing; a tool that is retired in the text, with the reason stated, teaches the reason. So week 8 says outright that this is the last time the course uses the turtle, and then earns that by using it to demonstrate the limits of looking.

The lesson is not that visual validation is weak. That framing is untrue, students will discover that it is untrue, and a rule they have caught you overstating will not survive to the moment they need it. The honest lesson is that a check has to match the claim it is being used to support, and the turtle is an unusually good instrument for showing why, because it makes both the claim and the evidence visible at once.

### The two ways looking fails

There are exactly two, they are different, and they have different remedies. Separating them is what turns a warning into a skill.

The first is sampling. You ran it once, the picture was right, and you concluded that the function is right. The picture was complete and truthful evidence about that run, and it said nothing whatever about the runs you did not make. This is not a defect of eyes. A test suite with one case is wrong in exactly the same way and to exactly the same degree, which is worth saying explicitly, because it makes visual and executable checks commensurable rather than opposed and it retroactively sharpens what the student already learned about tests.

The second is observability. The picture does not contain the property you care about, so it is not evidence about that property even for the run you made. A function can leave the turtle facing the wrong way, or with the pen up, or a unit short of where it started, and the drawing is perfect. Looking harder does not help, because the fact is not in the image.

The remedies differ accordingly. Sampling is answered by more cases, which is what a test suite is. Observability is answered by asserting on state the picture never showed, which is what `position`, `heading` and `isdown` are for.

### The asymmetry worth naming

Underneath both is a single asymmetry that is worth giving to students as a keepsake, because it is true far beyond turtles. Looking is a strong instrument for finding faults and a weak one for confirming correctness. A picture that looks wrong is wrong, and you knew it in a quarter of a second, which no test suite can match for cost. A picture that looks right is weak evidence that anything is right.

That gives visual checking its proper and permanent job. It is the first filter, run because it is nearly free and rules out whole classes of gross error immediately. It is not the last word, and the reason it is not is that a passing glance and a passing test both certify only what they actually covered.

### When looking really is enough

Say this plainly rather than letting students work out that you left it out. Looking is a sufficient check when the artefact is itself the product, when you can see the whole of it, and when the property you care about is one the rendering actually shows. A figure for a paper, a page layout, a colour scheme: the picture is the deliverable, there is no general claim being made about other inputs, and there is nothing behind the image that the image fails to report. Checking it by eye is not a shortcut in that case, it is the correct instrument.

The trouble begins the moment the thing being claimed is about a function rather than about an artefact, because a function is a claim about all its inputs and a picture is one input.

| What you are claiming | What actually checks it |
|---|---|
| this picture is right | looking at it |
| this function draws the right picture for this input | looking at it |
| this function draws the right picture for any input | cases you did not choose to be kind |
| this function leaves things as it found them | an assertion on state the picture does not show |
| this function composes with the next one | running them together, and asserting |

## Four examples for the week 8 note

These are ordered so that each one closes off the escape route from the one before.

The first is sampling in its purest form. Ask for a function `polygon(n, size)` and let it come back using integer division for the turn, `t.right(360 // n)`. For four, five, six, eight and ten sides the division is exact and the shape closes perfectly. For seven it turns 51 degrees instead of 51.43 and the polygon fails to close by a visible margin. Every picture the student chose to look at was correct, and the one they did not choose was not. This is the same failure as a test suite that happens to miss the awkward case, and it should be named as such on the spot.

The second is observability. A function that draws a five-pointed star, correctly, but leaves the turtle rotated by 36 degrees from where it started. The picture is beyond criticism. Call it twice with a move in between and the second star is tilted. Nothing about the first drawing could have told you, and the remedy is to assert on `t.heading()` before and after, which is the moment the student sees that the interesting property was never in the image.

The third is the same failure in the form that bites hardest in a loop. A function that ends one unit short of where it began, or leaves the pen up. Once, invisible. Fifty times in a loop, ruinous, and ruinous in a way that looks like a different bug entirely. This is where `total_movement` and `isdown` earn their place as things you can assert on.

The fourth is the one to end on, because it removes the possibility of a picture ever settling the question. Show two functions that draw a square. One uses a loop of `forward` and `right`. The other uses four hardcoded `goto` calls. Their output is pixel-identical. Move the turtle away from the origin and run each again, and one of them still draws a square while the other draws the same square in the same place as before. Two identical pictures, two functions that are not remotely the same function. Whatever a student concluded from the picture, they concluded it about the picture.

This last example is also the natural place for the multi-turtle work, if it lands: two pens on one canvas, one running each version, drawing over each other identically on the first run and diverging visibly on the second, with the shared highlighted source column showing which line did it. It is the week 6 comparison rubric applied to a case where comparison by appearance is exactly what fails.

## What the retirement costs

An earlier draft of this document proposed a maze-and-sensing delegation task for weeks 10 and 11. Retiring the turtle at week 8 rules that out, and the loss is acceptable. Its value was that it supplied a non-project problem with enough substance to carry a real delegation exercise, and the authorship progression proposed in `authorship-progression.md` supplies that from the projects themselves from week 10 onward, on assessed work, which is strictly better. The turtle no longer has to stand in for a real problem.

What the retirement buys instead is that the turtle leaves the course having taught something the course could not otherwise demonstrate cheaply, at the exact week where the student is learning that a contract has to be written before the code that satisfies it.

## Two practical notes

If the turtle arrives in week 3 it must be introduced as an object with methods, not as a drawing library, or the week 8 payoff loses its footing. The whole of the week 8 argument depends on the student already thinking of the turtle as a thing with state that methods change, because the observability failure is precisely a claim about state.

Everything week 8 needs already exists in the widget. `position`, `heading`, `isdown`, `isvisible` and the counters are public, and the recorded event stream is ordinary data. No new capability is required, only the exercises.
