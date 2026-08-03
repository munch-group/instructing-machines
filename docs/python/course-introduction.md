# How this course works {#sec-course-introduction}

You are about to learn to program at a moment when a machine can already write the program for you. That is an odd position to be in, and pretending otherwise would waste your time. So this course is arranged around it. You will learn Python the way anyone learns Python, by writing small programs and watching them run, and alongside that you will learn what it takes to hand work to an assistant and know whether what comes back is any good. Those two things turn out to be the same skill approached from two directions, and this chapter explains the arrangement before you meet it week by week.

## What the course is for {#sec-what-for}

By the end of the term you should be able to look at a problem from your own field, decide what smaller problems it breaks into, say what each of those smaller pieces must do, and check whether a piece does it. Some of the code that fills those pieces you will have written yourself. Some of it an assistant will have written for you. In either case you are the one who decides whether it is correct, and the whole course is built to make you capable of that decision.

The hard part of programming is almost never the individual piece. Students who understand variables, loops, functions and dictionaries perfectly well can still sit in front of a new problem with no idea where to start, because putting the pieces together is a separate skill that only comes from doing it many times. That is why the first five weeks introduce the language and the eight weeks after that are projects. The concepts are the smaller half of the work. The composition is the larger half, and it is built by practice.

Everything the course asks you to do rests on one idea, which is that plausible and correct are different states, and moving from the first to the second is called verification. Code is verified by tests and by reading it. A claim about biology is verified by evidence and by what you already know. Your own learning is verified by doing the thing with the assistant switched off. Three situations, one idea, applied three times.

## How the material teaches {#sec-how-it-teaches}

The notes introduce things by doing them first and naming them afterward. You write and run something, it works, and only then does the text tell you that what you just wrote is called a for-loop and explain why it did what it did. This is deliberate. A name attached to something you have already made work sticks; a name attached to nothing does not.

Almost every exercise asks you to predict before you run. Decide what you think will appear on the screen, write it down or say it out loud, then run the code and find out. The gap between your prediction and the result is the only reliable signal of what you do not yet understand, and you get that signal for free every time, provided you actually commit to a prediction first. Skipping the prediction and going straight to the run turns an exercise into a demonstration and teaches you very little.

Underneath all of it is a way of reading code that the course calls substitution and reduction. A variable is replaced by its value. An expression is replaced by the simpler expression it evaluates to, and then by a simpler one again, until only a single value is left. A function call is replaced by the value it returns. If you can carry out those replacements in your head, in order, for a piece of code you have never seen, then you can read code, and everything else follows. Several of the course tools exist for no other reason than to show you the substitution steps the machine actually took, so you can compare them against the ones you took.

The course also asks you to swear three oaths, and it asks in earnest. The first is that you type code and never paste it, because the typing is where the syntax settles into your hands. The second is that lines run from top to bottom, which sounds obvious until the day it stops feeling obvious. The third is that you trace every substitution and reduction consciously rather than guessing at what a line probably does. They are numbered vows, taken with a raised hand, and students who keep them do better than students who do not.

## The assistant and the arc it follows {#sec-ai-arc}

An assistant is present from the first week, and its part in the course grows across the term along a fixed sequence of roles. Each role licenses a different kind of request, and each new role is added to the ones you already have rather than replacing them. By week fourteen you have all of them and choose between them.

The sequence opens with Explainer. You put something in front of the assistant that already exists, an error message or a few lines of code, and ask what it means. You are not asking it to produce anything, so there is nothing yet to be wrong about beyond the explanation itself, which you check by running the code.

Translator comes next. You ask it to turn code into plain language, or a plain-language description into code, and you check the translation in both directions. Illustrator asks for examples and analogies for something you half understand. Comparer puts two versions of the same thing side by side and asks which is better and why, after which you make the decision yourself; the assistant supplies the argument and you supply the judgment.

Drafter is the first role that produces code you intend to keep. You specify a small function, the assistant writes a first version, and you test it before it goes anywhere near the rest of your program. The next role, Unreliable Narrator, exists to keep Drafter from becoming a habit of trust. In those exercises you work with examples that carry a planted mistake, a bug in the code or an error in the biology, and your job is to find it. The mistakes are written by us rather than harvested from a live assistant, because on small beginner tasks a capable assistant is usually right, and a lesson about unreliability that depends on the assistant misbehaving on cue would be theater.

The last three roles hand over progressively more. As a Worker the assistant fills in a piece you have already specified and already written a test for, so the check exists before the code does. As a Collaborator it works with you on something where you set the decomposition and it contributes pieces and opinions. As a Delegate it takes a goal and a specification and returns something you then check against acceptance criteria you wrote in advance.

One rule holds at every level. The assistant predicts, and the machine proves. Whenever the assistant tells you what a piece of code does, you check with a tool that runs it. Whenever it hands you a function, you check with a test. The prediction is cheap and the proof is what makes it worth anything.

## Badges {#sec-badges}

Every exercise in the course carries a badge naming what the assistant is licensed to do for that particular exercise. The badge sits on its own line just below the exercise heading, formatted as code, and it looks like this:

`AI: Explainer`

That badge means you may ask the assistant to explain, and nothing further. An exercise that permits drafting says so:

`AI: Drafter`

And an exercise you must do with the assistant closed says:

`SOLO`

The `SOLO` badge is the one that carries the most weight, and it is there for your benefit rather than as a rule to be policed. Nobody can tell whether you kept it. What a `SOLO` exercise buys you is evidence about yourself: if you can do it alone, you have learned the thing, and if you cannot, you have found out now rather than in week twelve when everything depends on it. Doing a `SOLO` exercise with help does not get you in trouble. It just deletes the only measurement you had.

The assistant lives in your browser, in Microsoft 365 Copilot, and it includes a Study and Learn agent that guides your reasoning instead of handing over the answer. VS Code stays free of it. Keeping the two apart is a working arrangement rather than a moral position: when the help is one deliberate window away, using it becomes a decision you make rather than something that happens to your code while you are typing.

## The logbook {#sec-logbook}

Once a week you write one entry in a logbook you keep all term. An entry records something the assistant got right, something it got wrong, and how you knew which was which. It takes a few minutes and it is the single best record of your own development that the course produces, because by week twelve you will be reading week-two entries where you could not tell a plausible answer from a correct one, and the difference will be visible on the page.

## The projects, and who writes what {#sec-projects}

From week six to week thirteen the course is eight weekly projects, each one a small piece of working biology code. Every project has three parts, and it helps to name them separately because the course moves them between hands at different times.

The decomposition is the list of functions the project consists of, with what each one takes and what each one returns. The tests are the code that decides whether a function does what it is supposed to. The bodies are the actual lines inside each function.

In the first project all three parts start in familiar places. The decomposition is given to you, the tests are given to you, and you write the bodies. Over the following weeks each part changes hands on its own schedule, and once a part has moved it does not move back.

The bodies go first, and they go to the assistant. In week seven you nominate one function and let the assistant draft it, then test what comes back. In week eight it drafts again, but only after you have written a test for the function yourself, which is the point at which the order of operations becomes the lesson: the check exists before the code exists. From week nine the assistant does more of the routine work, the glue between your code and a library, while you keep the parts that carry the actual biology.

The tests move second, and they move to you. Week eight ships you every test but one, and you write the missing one. Week nine ships half. By week eleven you get a single end-to-end test that says whether the whole thing works, and nothing that tells you which part is broken. By week twelve you get none, and what you can check is what you thought to check.

The decomposition moves last, because it is the hardest of the three. Through week nine the full list of functions is given. In week ten most of it is given and you name two pieces yourself. In week eleven you get only the top-level function and decide everything under it. In week twelve you get the goal and the data. In week thirteen you formulate the problem, build it, and only afterward see how we would have broken it up, which is the closest thing the course has to a final examination of the skill it is actually teaching.

Two rules keep this from becoming unfair. A project never asks for anything the notes have not already taught, and it asks for it the week after they taught it, so there is always a week between meeting an idea and having to use it under your own direction. And each transfer happens once. A part that has become yours stays yours, so the ground never shifts back under you.

## What to expect from yourself {#sec-expect}

There is a fear worth addressing directly, which is that learning to program is pointless now that a machine can do it. The opposite is closer to the truth, and the reason is arithmetic. What you can safely get out of an assistant is limited twice over by what you know: once by your ability to ask for the right thing, and again by your ability to tell whether what came back is right. Both limits are your own knowledge, so the value the assistant has for you grows roughly as the square of what you know. At zero knowledge it is worth nothing, or less than nothing, because you cannot catch its mistakes. And every new thing you learn is now worth more than it used to be, because it pays you twice, once directly and once by unlocking more of the assistant that you can use without danger.

That is also where the line about cheating falls, and it is a sharper line than it first appears. Producing something you did not formulate, do not understand, and cannot check is cheating, and you will feel it. Producing something you formulated, understand, and validated is tool use, no different in kind from using a microscope. The same habit of never trusting what you have not checked keeps your work correct and tells you which side of that line you are standing on.

#### Exercise {#sec-exercise-start-the-logbook}

`SOLO`

Make a file called `logbook.md` somewhere you will find it again, and write the first entry today, before you have used the assistant for anything in this course. Write down what you currently expect it to be good at, what you expect it to be bad at, and how you imagine you would tell the difference. You will read this again in week fourteen. Nobody else will, so make it truthful rather than impressive.
