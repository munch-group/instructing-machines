# Insides {#sec-insides}

Before you write a single line of Python, two pictures are worth having in your head: what a computer actually is, and what the AI you will be talking to actually is. This note draws the first of those pictures, and it ends by setting up the second.

{{< video https://youtu.be/d86ws7mQYIg >}}

While you read, keep the machine map poster next to you. It uses the same visual language as this note: amber for things kept on the disk, blue for things held temporarily in memory, slate for the CPU, teal for the tools you drive yourself, and purple for the AI, which sits elsewhere on purpose.

You are about to spend fourteen weeks giving instructions to a machine, and part of that time telling an AI to give instructions to the same machine on your behalf. It helps enormously to know, in broad strokes, what is actually sitting under your fingers. You do not need to become an electrical engineer. What you need is a mental model, a small and sturdy picture you can return to whenever the words pile up. That is all this note is trying to give you. Later we will build the same kind of picture for the AI, and the two pictures together set up the single most important idea in the course.

Let us open the box.

## It's switches all the way down {#sec-switches}

Deep down, a computer is millions of tiny switches, and each switch is either off or on. That is it. There is no secret third thing. We write "off" as `0` and "on" as `1`, and one such off-or-on is called a bit, the smallest possible piece of information.

One bit on its own cannot say much. But line eight of them up and you get a byte, and a byte can be in 256 different patterns, enough to stand for a number from 0 to 255, or a single letter, or one dot of color. Group bytes together and you can represent anything at all: this sentence, a photograph, a song, an entire genome, or the program that is reading them.

![Underneath everything, a computer stores numbers made of bits, and the meaning of those bits comes from the program that reads them, never from the bits themselves.](./images/fig-everything-is-numbers.svg){#fig-everything-is-numbers}

Here is the one idea to carry out of this section, because we will lean on it all term. The bits are dumb. The number `01100100` in @fig-everything-is-numbers does not know whether it is the number 100, the letter `'d'`, or a shade of gray. Its meaning comes entirely from the piece of code that decides how to read it. When you learn later that in Python `'d'` and `100` are different types, this is why: a type is nothing more than an agreement about how to read some bits. Hold onto that, because it will save you a lot of confusion in a few weeks.

## The three parts that do the work {#sec-anatomy}

Inside the box, three components matter most for us, and the whole trick to keeping them straight is a single distinction: some things are kept and some things are temporary.

![The three parts that do the work. The disk keeps things, memory forgets things, and the CPU works only on whatever memory is holding right now.](./images/fig-machine-anatomy.svg){#fig-machine-anatomy}

The hard disk is where your files live: your code, your data, everything. Crucially, the disk is permanent, so what you save there survives when you switch the computer off. When you save a file, you are writing it to the disk. It is roomy but slow.

The memory, usually called RAM, holds whatever is running right now, meaning the program that is currently going and the values it is working on. Memory is temporary. The instant a program stops, or the computer restarts, whatever was in memory is gone. This is the single most common source of beginner heartbreak, so let me say it plainly: nothing in memory is saved unless you write it to the disk. A value your program computed but never saved vanishes when the program ends. It was in the blue, not the amber.

The CPU, the central processing unit, is the worker. It does the actual computing, one tiny step at a time, but staggeringly fast, billions of steps a second. And it has one important limitation: it only ever works on what is currently in memory. So the normal rhythm of a running program goes from disk to memory to CPU. A copy of your file is loaded from the disk into memory, and the CPU works through it from there.

This gives you a habit worth forming now. Whenever something surprising happens, a value that seems to have disappeared or a change that did not stick, your first question should be whether that thing was kept on the disk or was only ever temporary in memory. Nine times out of ten, that question is the answer.

#### Exercise {#sec-exercise-kept}

🔒 `SOLO`

Before reading on, decide what you think and write it down. You run a program that calculates the number of `A` bases in a DNA sequence and prints the answer to the screen. You then close the program. Is that count still anywhere on the computer? Where was it while the program ran, kept or temporary? Where would it need to go for you to still have it tomorrow?

Predict first. We will build the tools to actually save such a result in the chapter on files. For now the point is only to feel the line between kept and temporary.

## A machine that was only ever imagined {#sec-turing}

You just met the CPU, a worker that does one tiny step at a time, extremely fast. The idea that everything, no matter how clever, is really just a long chain of tiny mechanical steps is so important that it is worth meeting the moment it was born, years before any chip existed.

In 1936, a young mathematician named Alan Turing asked a beautifully simple question: what is the least a machine would need in order to compute anything at all? His answer became one of the most famous ideas in all of science, and it is small enough to fit in your head.

It is worth being clear about one thing first, because the difference is lovely. The Turing machine was a thought experiment, a machine Turing built on paper and in his head in order to reason about what computers could and could not do, never a device he bolted together in a workshop. People have since built working models for the fun of it, and Turing himself went on to help design very real machines, including ones that broke wartime codes. So when we say the machine does this or that, picture a machine you are running in your imagination. That it was imaginary is exactly what made it powerful, because Turing could prove things about every possible computer by studying this one tiny made-up one.

Here is the whole machine. There is a long paper tape divided into squares, and each square holds a single symbol, say a `0`, a `1`, or a blank. There is a head parked over one square that can do only three things: read the symbol under it, write a new symbol in its place, and move one square left or right. There is a state, a little sticky note reminding the machine roughly where it is in the task. And there is a fixed table of rules which says, for every combination of current state and symbol under the head, what to write, which way to move, and which state to switch to next.

![The Turing machine: a tape of symbols, a head that reads and writes one square, a current state, and a fixed table of rules. It reads, looks up the matching rule, writes, moves one step, changes state, and repeats.](./images/fig-turing-machine.svg){#fig-turing-machine}

And that is all it does, as @fig-turing-machine shows. It reads the square under the head, looks up the one rule that matches the current state and symbol, writes, moves one step, changes state, and then does it again, and again, until it reaches a rule that says stop. No screen, no keyboard, no apps. Just a head shuffling along a tape, following a table.

If that sounds too feeble to matter, hold that thought, and first try running it yourself, because the whole spirit of this course is to do all the little steps in your head before trusting anything to do them for you.

#### Exercise {#sec-exercise-turing}

🔒 `SOLO`

Grab a scrap of paper. Draw three squares holding `0 1 1`, put the head on the leftmost square, and set the state to A. Now follow exactly three rules, one step at a time. In state A reading a `0`, write `1`, move right, and stay in state A. In state A reading a `1`, write `0`, move right, and switch to state B. In state B reading a `1`, write `1`, move left, and then stop.

Before you start, predict what the three squares will say when the machine stops, and where the head will end up. Then trace it slowly and check. If you got `1 0 1`, halted on the middle square, you traced it correctly. If not, find the step where your prediction and the rules parted ways, because that hunt is the real exercise.

## What the imagined machine has to do with yours {#sec-turing-vs-modern}

Now the astonishing part. This ridiculous little tape shuffler can compute anything that any computer can compute, your laptop included. Give it the right table of rules and it can add numbers, sort a list, or translate a DNA sequence into a protein. Even better, Turing showed that you can build a universal one, a single machine whose rules let it read a description of any other machine written on its tape and then act it out. One machine that can become any machine, just by being fed the right instructions. That is the theoretical birth certificate of the thing on your desk, a general-purpose computer that runs any program you give it.

So how does this paper fantasy line up with the chips from the previous section? Strikingly well in its bones, and completely differently in its body.

![The Turing machine and a modern computer share a deep idea, that fixed rules are applied one step at a time by a universal machine which runs any program, but they differ completely in how they are built and how fast they go.](./images/fig-turing-vs-modern.svg){#fig-turing-vs-modern}

The similarities run deep, as @fig-turing-vs-modern lays out. Both grind through a fixed set of instructions one tiny step at a time, and the head's cycle of reading, writing, and moving is a paper ancestor of the CPU doing one small operation after another. Both keep the storage, which is the tape, separate from the worker, which is the head and its rules, just as your computer keeps memory separate from the CPU. And notice that on the tape the rules and the data sit together as plain symbols, which is exactly the modern truth that a program is just more data in memory. When Python reads your `hello.py` and acts it out, it is playing the role of a universal machine reading instructions off a tape. You will meet that same idea again when we come to the AI.

The differences are mostly about being real instead of imagined. The Turing machine has an endless tape, while your computer has finite memory, enormous but not infinite. The head must shuffle left and right, square by square, to reach a distant spot, while your computer can jump straight to any location at once, and that instant jumping is the random access in the name RAM. And where the imagined machine plods one symbol at a time, a real chip does billions of steps a second using the tiny on and off switches, called transistors, that you met at the very start of this note. The tape became memory, the head became the CPU, and the rule table became the program. The dream was 1936 and the hardware caught up later.

Keep this picture close, because it quietly sets up everything ahead. If any computation is really just simple steps following a table of rules over stored symbols, then the whole game of programming is writing good tables of rules, and the rest of the book is about the ever friendlier ways we have invented to write them.

## The operating system, the manager in the middle {#sec-os}

You never actually talk to the disk, memory, and CPU directly. Sitting between your programs and the hardware is the operating system, and macOS, Windows, and Linux are all operating systems. Think of it as the manager of the whole building.

![The operating system sits between your programs and the hardware, handing out memory, finding files, and sharing the CPU so your programs do not have to fight over the electronics.](./images/fig-os-stack.svg){#fig-os-stack}

As @fig-os-stack shows, when your program wants to open a file it does not go rummaging through the disk itself. It asks the operating system, and the operating system finds the file and hands it over. When a program needs memory to work in, the operating system parcels some out. When you have a browser, an editor, and a music player all running at once, the operating system is the one sharing the single CPU between them, giving each a slice of time so quickly that they all seem to run at the same moment. It also draws the windows on your screen and listens to your keyboard.

For this course you mostly will not think about the operating system, but two of its jobs will touch you directly. It is the operating system that gives you the terminal, the place where you will type `python hello.py`. And it is the operating system that organizes your files into folders, which is why the very first practical skill in this course is finding your way around folders in the terminal with `cd` and `ls`.

## Software is just files full of instructions {#sec-software}

So what is a program, or a piece of software? It is, in the end, a file on the disk full of instructions for the CPU. A game, your browser, VS Code, Python itself, every one of them is a file of instructions that the operating system loads into memory and lets the CPU carry out.

But there is a catch that the whole rest of this note hangs on. The CPU only understands one language, and it is a brutally simple one. It is called machine code, and it consists of raw numbers standing for the tiniest possible actions: move this number here, add these two, compare them, jump to that instruction. Machine code is total control and utterly unreadable by humans:

```txt
10111000 00000100 00000000
```

That is roughly "put the number 4 into a register". No human writes serious programs like that, and no human should have to. The entire history of programming is the story of building friendlier and friendlier languages on top of machine code, and then having the machine translate back down. That story is where we go next, and it is where your first program and your first AI conversation both fit in.
