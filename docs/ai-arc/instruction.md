
# From machine code to Python to AI {#sec-instruction}

## The ladder of instruction {#sec-ladder}

Everyone who has ever programmed has faced the same trade-off. The closer your instructions are to the machine's own language, the more precise control you have — and the more painful they are to write. The closer your instructions are to plain human language, the easier they are to write — and the more you are trusting something else to fill in the details. The history of programming is a ladder built out of exactly this trade-off, one rung at a time.

![Every step up the ladder trades precise control for closeness to human language. Each layer is a *translator* down to the one below it — and the AI is the newest, and strangest, rung.](./images/fig-instruction-ladder.svg){#fig-instruction-ladder}

At the bottom is **machine code**, the raw bits the CPU runs. One step up is **assembly**, which swaps the bit-patterns for short words like `MOV` and `ADD` — still one word per machine step, still gruelling, but readable. Higher up are **compiled languages** like C: now you write recognisable words and arithmetic, and a program translates the whole thing down to machine code before it runs. Higher still are **interpreted languages** — and this is where **Python** lives, the language you are about to learn.

The key move to notice in @fig-instruction-ladder is that *every rung is a translator down to the rung below*. Assembly is translated to machine code; C is translated to machine code; Python is handled by a program that turns it into machine steps as it goes. At each level, people worried that the level below would become a lost art — and every time, understanding the level below stayed valuable exactly for the moments when the translation went wrong or the stakes were high. Molecular biology is full of high-stakes moments. Keep that thought; we'll return to it.

## Compilers and interpreters: two kinds of honest translator {#sec-compile-interpret}

Since Python is an *interpreted* language, it's worth seeing clearly what that means, next to its cousin the compiler.

![A compiler translates the whole file ahead of time into a finished machine-code file. An interpreter reads and runs your file live, one line at a time, keeping no machine-code file behind.](./images/fig-compiler-vs-interpreter.svg){#fig-compiler-vs-interpreter}

Compare the two in @fig-compiler-vs-interpreter. A **compiler** takes your entire code file and translates all of it, in one go, into a finished machine-code file — *before* anything runs. After that, the machine-code file can be run directly by the CPU, again and again, very fast. The translating happens once, up front.

An **interpreter** works differently: it reads your file and runs it *live*, one line at a time. It reads a line, tells the CPU to do it, reads the next line, tells the CPU to do that, and so on to the end. Nothing is translated ahead of time and no separate machine-code file is left behind. This is exactly what happens when you type `python hello.py`: the program called `python` — the **interpreter** — reads your `hello.py`, holds it in memory, and drives the CPU through it line by line.

This is also, quietly, why we make you run scripts from the terminal before we ever open a notebook. Typing `python hello.py` forces four things apart that a notebook glues together: the *file on the disk*, the *interpreter* that reads it, the *CPU* that does the work, and the *terminal* where you launch it and watch the output. Once you've felt those four as separate things, the rest of the course is much less mysterious.

::: {.callout-important}
## The line that ties it together
*The AI predicts; the machine proves.* An interpreter is a translator you can trust to mean exactly what your code says. Hold that thought right up against the AI — because the AI is about to look like just one more rung on the ladder, and the most important lesson in this course is the precise way in which it is **not**.
:::

## The newest rung: instructing a machine in plain language {#sec-ai-rung}

Now the AI. For the purpose of producing code, an AI assistant looks like it belongs at the very top of the ladder: you describe what you want in ordinary English — *"read this DNA sequence, find the open reading frames, and translate them"* — and it hands back Python. No syntax, no rules to memorise, closer to human language than any rung before it. On the ladder, it is simply the next translator: from a description even nearer to how you actually think, down toward code the machine can run.

That framing is genuinely useful — right up until the moment it breaks. And where it breaks is the whole point. To see the break, you have to look at what the AI is actually doing under the hood, which is nothing like what a compiler does.

## What the AI is actually doing: guessing the next word {#sec-next-word}

A modern AI language model, underneath all the polish, does one small thing over and over: it guesses the next word.

You give it some text — your question, your request. It reads all of it and then scores every possible next **token** (a token is a word, or a small piece of a word) by how likely that token is to come next. It picks one, adds it to the text, and then does the whole thing again to choose the word after that, and the word after that, until it has produced a full answer.

![Underneath, the model reads everything so far, scores how likely each possible next word is, picks one, appends it, and repeats. It produces a *plausible* continuation — often right, sometimes confidently wrong.](./images/fig-next-word.svg){#fig-next-word}

Look carefully at the example in @fig-next-word. Asked to continue *"The stop codon in this sequence is…"*, the model rates `TAG` as the most likely next word and picks it. But notice *why*: it chose `TAG` because, across the mountains of text it has seen, that word tends to follow in sentences like this — **not** because it went and checked your actual sequence. It is producing a *plausible* continuation. Often the plausible answer is also the correct one. Sometimes it is fluent, confident, and simply wrong. That gap — between *plausible* and *true* — is the most important thing to understand about these tools.

## Where the skill comes from: training and weights {#sec-training}

Fair question: how does it know that `TAG` usually follows? Nobody programmed grammar or biology into it by hand. It learned, in a process called **training**, which happens once, before you ever use it.

![Training: over an enormous amount of text, the model repeatedly plays "guess the hidden next word," and each time nudges millions of internal dials — its *weights* — so that its next guess is a little better. Afterwards the dials are frozen.](./images/fig-training.svg){#fig-training}

During training, the model is shown an enormous amount of text — books, websites, articles, code, much of the public internet. Over and over it plays a game: hide the next word, let the model guess it, then compare the guess to the word that was really there. Every time, it nudges millions of internal numbers — called **weights**, the "dials" in @fig-training — a tiny bit, so that next time the guess is a little closer. Repeat that billions of times and the dials settle into a configuration that makes startlingly good guesses about what word comes next. Those weights *are* everything the model knows. There is no library of facts inside it, no lookup table — only the dials.

Two consequences matter for you, and they matter a lot:

First, when you chat with the model, it is **not learning** and it is **not looking anything up**. The dials are frozen. It is just running the same next-word guess with fixed weights. Whatever it "knows" is baked into those dials from training, which is why it can be out of date, and why it does not actually consult your specific DNA sequence unless you paste it in — and even then, it is still *guessing a plausible continuation*, not running a check.

Second, because it learned patterns from human text rather than following rules someone wrote down, it can produce something that *sounds* exactly like a correct answer while being false. It has no separate sense of "true"; it has a sense of "likely to come next." When a false statement is a *likely-sounding* one — a plausible-but-wrong gene function, an off-by-one in a loop, a codon table with a quiet mistake — the model will hand it to you with total confidence. This has a name you'll hear a lot: a **hallucination**.

## The break in the metaphor — and the reason for this course {#sec-the-break}

Now we can put the two pictures side by side, and the whole course snaps into focus.

![Both a compiler and an AI turn a description into code — but a compiler is a *deterministic, meaning-preserving* translator you can trust, while an AI is a *probabilistic, meaning-approximating* translator you must verify.](./images/fig-compiler-vs-ai.svg){#fig-compiler-vs-ai}

Set them side by side, as in @fig-compiler-vs-ai. A compiler or interpreter is a **deterministic, meaning-preserving** translator. The same input always yields the same output, and the output means *exactly* what the input said, because it follows fixed rules a person wrote down. That is precisely why you can trust a compiler without ever reading the machine code it produces — the trust is built into how it works.

An AI is a **probabilistic, meaning-approximating** translator. The same prompt can yield different code on different days. The code may not mean what you asked, because it was produced by guessing a plausible continuation, not by applying meaning-preserving rules. It can be fluent, plausible, and wrong.

So the AI is *not* just one more rung on the ladder, even though it first looks like one. Every earlier rung — assembly, C, Python — is a faithful translator you can trust. The AI is an unreliable one. And that single difference is the entire justification for what you are about to do:

::: {.callout-important}
## Why you are learning Python at all
Because this newest translation layer is unreliable, you have to be able to **read the language it emits — Python — and check that it means what you wanted.** You trust a compiler; you *verify* an AI. And understanding Python is exactly what puts you in a position to verify. That is why a course whose goal is to help you use AI well spends its first months teaching you to read and run code yourself. The machine is the only thing that can settle whether the AI was right — and you have to be able to ask the machine.
:::

#### Exercise `AI: Explainer`

Open the assistant in your browser and ask it a small factual question you can check — for example, *"What are the three stop codons in the standard genetic code?"* Read its answer. Then find a way to **verify** it that does not involve asking another AI: a textbook, a trusted database, or later in this course a tiny program of your own. Was it right? How did you know it was right, independently of the AI telling you so?

Write two or three sentences in your **logbook**: what you asked, what it said, and how you checked. This is your first entry, and by the end of the course you'll have a running record of exactly where the machine helped you and where it quietly misled you — and, more importantly, of your own growing ability to tell the difference.

::: {.callout-note}
## Where this leaves you
You now have both pictures. A computer is switches, made into numbers, made into files of instructions, run by a CPU on what memory holds, all managed by an operating system — and Python is a trustworthy translator from words you can read down to those instructions. An AI is a next-word guesser whose skill is real but whose output is plausible rather than guaranteed. Everything else in this book is you building the one ability that lets you use the second safely: the ability to read what it writes, run it, and see for yourself.
:::
