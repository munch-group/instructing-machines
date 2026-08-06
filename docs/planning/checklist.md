# Readiness checklist

*Moved. What still stands between the current repository and material a class
can be taught from now lives in `docs/_quarto.yml`.*

This document was a single list read end to end, which meant that a task about
`python/tuples.ipynb` sat several screens away from the line that schedules
`python/tuples.ipynb` in week 3. Everything in it has been rewritten as a
`CLAUDE:` comment in `docs/_quarto.yml`, under the chapter it concerns —
or, where it concerns no single chapter, in the block at the top of
`chapters:`. The week annotations there (`Python:`, `AI:`, `Workload:`) carry
what the old section on uneven week load was trying to say, week by week
rather than as one paragraph of counts.

To read the whole list at once, as this document used to be read:

```
python3 tools/prompts.py            # in render order, with week and chapter
python3 tools/prompts.py --json     # the same, for a machine
```

Items that were already done are not carried over; they are in the git history
of this file, and the last version that still listed them is the commit that
replaced this text. The convention itself is described in `CLAUDE.md` §7.
