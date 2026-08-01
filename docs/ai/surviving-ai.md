# Surviving AI {#sec-surviving-ai}

The whole of this course has been an argument that you can trust the assistant more precisely because you have learned to check it. That argument is true, and it is the right way to work, but it would be dishonest to end there, because checking well does not remove every limit, and some of the most important judgments you will make are about when the assistant should not be used at all. This last part is about the limits that remain even for someone who specifies, reads, judges, and tests carefully, and about the responsibility that stays with you no matter how good your checking becomes.

## The limit that lives in you, not in the machine {#sec-automation-bias}

Begin with a fact about people rather than about machines, because it is the one most likely to undo you. Humans tend to trust the output of an automated system more than they should, and the more fluent and confident that output looks, the stronger the pull. This is a well documented tendency, and it has a name, automation bias, and it does not spare people who know about it.

The danger for you is not that you will fail to learn the checking discipline. It is that once you have it, it will quietly erode. The first weeks of using the assistant you will check everything, because it is new and you are wary. Then it will be right several times in a row, and you will relax, and you will start accepting a function because it looks like the ones that were fine before, which is exactly the plausible surface you were taught to distrust.

The better the code looks and the longer the assistant's recent record, the more suspicious you should become, not less, because that is the situation in which your guard is lowest and its confident wrongness is most expensive. The checking is not a phase you pass through on the way to trusting the machine. It is the permanent condition of using it well.

## Tests are a floor, not a proof {#sec-tests-are-a-floor}

The second limit is one you have already met but must now state sharply, because it is easy to half learn. Passing tests is necessary, and it is not sufficient. A green result tells you that the code produced the right answer on the particular inputs you thought to try. It tells you nothing whatever about the inputs you did not try, and there are always inputs you did not try, because a handful of tests cannot cover the infinity of possible inputs.

This means a wrong function can pass a weak suite, and a function that passes even a strong suite can still be wrong on a case nobody imagined. Tests are a floor under your confidence, not a proof of correctness, and the assistant is specifically good at producing code that clears the visible floor while hiding a fault just out of sight of it. The only thing that stands behind the tests is your understanding of what the code does, which is why the rule that you never accept code you cannot read is not a beginner's caution you will one day outgrow. It is the last line of defence for every case your tests forgot.

## The limit no test can reach {#sec-domain-facts}

The third limit is the one that matters most in your field, and it is the one no amount of testing can reach, because it is not about the code at all. The assistant states facts about biology with exactly the same fluent confidence whether those facts are true or false, because it has no way of knowing which they are. It will tell you a base pairing, a codon assignment, a gene function, a statistical assumption, and it will sound equally certain when it is right and when it is inventing.

A wrong fact of this kind is more dangerous than a wrong loop for two reasons. It hides better, because there is no error and no failing test to draw your eye to it, and it does more damage, because a false premise propagates silently into every result built on top of it. No test you write about the code will ever catch a mistake in the biology the code assumes, because the code may be a flawless implementation of a wrong idea.

The only defence is to check the domain facts against something other than the assistant: your own knowledge, a textbook, a database, a primary source. In a scientific context this is not an optional nicety. A result that rests on a biological claim you accepted from the assistant without checking is a result you cannot defend, however green its tests.

## When not to use it at all {#sec-when-not-to-use}

These limits together sharpen a question the course has mostly answered by demonstration and should now answer directly, which is when you should not use the assistant at all. There are four cases worth naming.

The clearest is when you do not understand the problem well enough to check the answer. The assistant amplifies judgment you already have; it cannot supply judgment you lack. If you could not tell a correct solution from a plausible wrong one, then delegating the problem does not get you a solution, it gets you a guess you are unable to evaluate, and you are simply trusting blind, which is the one thing this course was built to stop.

The second is when the stakes are high and you cannot verify. If a wrong answer would matter and you have no way to check the answer, the assistant's speed is worth nothing, because speed toward an unverifiable result is not progress.

The third is more ordinary and more common than students expect, which is when the task is small enough that writing it yourself is faster and surer than specifying it, prompting for it, reading it, and testing it. The whole apparatus of delegation has a cost, and for a three line function you understand completely, paying that cost is slower than just typing the three lines.

The fourth is the one that matters while you are still learning, which is when using the assistant would rob you of understanding you actually need to acquire. There are things you must be able to do yourself, not because the assistant cannot do them, but because your ability to check its work on everything else depends on your having learned them. Handing those to the machine early is a false economy that leaves you unable to judge it later.

## Responsibility and honest attribution {#sec-responsibility-and-honesty}

Underneath all of these is a single principle that does not bend, which is that responsibility does not transfer. Whatever the assistant produces, the moment you submit it, run it, or publish a result that depends on it, it is yours. Pointing at the assistant is not a defence for a wrong answer, in this course or in the science you will go on to do, any more than a calculator's arithmetic excuses a wrong sum you copied without checking. Delegating the typing never delegates the responsibility, and the entire structure you have learned, the specifying and reading and planning and testing, exists so that you can accept that responsibility honestly while still using the machine heavily.

This has a practical companion, which is honesty about what the assistant did. Recording where and how you used it, in your logbook, in your prompt journal, in the notes on a piece of work, is not an admission of weakness and it is not something to hide. Concealing the assistant's involvement is the dishonest act. Disclosing it is simply an accurate account of how the work was done, and in a scientific setting an accurate account of method is not optional. The habit of honest attribution you build now is the same habit that will keep your later research defensible.

## The newest layer, and why it is different {#sec-newest-layer}

It is worth ending where the course began. In the first week the idea was offered that instructing a machine has passed through a sequence of layers, from switches to machine code to compiled languages to interpreted languages like Python, and that an assistant is one more layer, a way of describing what you want in something close to ordinary language and having code come back.

The difference, the one that has organised everything since, is that a compiler is a faithful translator and an assistant is not. A compiler always produces code that means exactly what you wrote. An assistant produces code that is merely plausible, and may mean something other than what you wanted, and cannot tell you which. That single difference is why this new layer, unlike the ones beneath it, cannot be trusted and must be verified, and it is why you had to learn what a program is, and what correct means, and how to specify and read and test, in order to use the newest layer safely.

The syntax you learned this term may fade with disuse, and the assistants will keep improving, but the durable skill, the one that will still be yours when the tools have changed, is the judgment: knowing what correct means, being able to say it precisely, being able to read what you are given, and always, always checking. The machine is a powerful new way to instruct a computer. It is your job to instruct it well, and to never stop verifying what it does.

#### Exercise {#sec-ex-should-not-have-used}

`SOLO`

Identify one task from the course where, looking back, you should not have used the assistant, either because you could not really check its answer, or because leaning on it cost you an understanding you later needed. Say which of the four cases above it falls under, and what you would do differently if you met the same task again tomorrow.

#### Exercise {#sec-ex-genuine-augmentation}

`SOLO`

Identify one task where the assistant genuinely let you produce something correct that you could not have written unaided, and be specific about which part of your checking made that safe. Name the actual test, the actual reading, or the actual hand-worked case, rather than saying in general that you were careful.

#### Exercise {#sec-ex-verify-a-claim}

`AI: Unreliable Narrator`

Take one biological claim the assistant makes, whether in an explanation or in a comment inside code it wrote for you, and verify it against a real source rather than against the assistant itself. Record the claim, the source, and whether it held. If it held, note whether the source stated it more precisely, less precisely, or with conditions the assistant left out, because a claim that is true but stripped of its conditions is the next most dangerous thing after a claim that is false.

For your last logbook entry, look across the whole term. Describe how your use of the assistant changed as your understanding grew, from the first weeks when it could only explain things to you, through the point where you let it draft and learned to distrust the draft, to the finale where you delegated real work and kept the responsibility. Name the single habit from this course you most want to still have in three years, and say why.
