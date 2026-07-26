# Turing machine animation — narration script

*Auto-generated from the rendered subtitles. Read one line per beat while the video plays, or load `turing_machine.srt` as a subtitle track. Timecodes are `mm:ss`.*

| # | In | Out | Narration |
|---|----|-----|-----------|
| 1 | 00:00 | 00:01 | In 1936 Alan Turing imagined the simplest possible machine — and it can compute anything your laptop can. |
| 2 | 00:01 | 00:03 | A paper tape, divided into squares. Each square holds a single symbol — here a 0, a 1, or a blank. |
| 3 | 00:03 | 00:05 | A head sits over one square. It can read the symbol, write a new one, and move one step left or right. And it remembers a state. |
| 4 | 00:05 | 00:06 | It follows a fixed table of rules. For each state and symbol, the table says what to write, which way to move, and which state comes next. |
| 5 | 00:06 | 00:08 | Let's run it. The three squares say 0 1 1, the head is on the 0, and the state is A. Predict the ending before each step. |
| 6 | 00:08 | 00:09 | Step 1: in state A the head reads 0. |
| 7 | 00:09 | 00:10 | The rule says: write 1, move right, and stay in state A. |
| 8 | 00:10 | 00:11 | Step 2: in state A the head reads 1. |
| 9 | 00:11 | 00:14 | The rule says: write 0, move right, and switch to state B. |
| 10 | 00:14 | 00:15 | Step 3: in state B the head reads 1. |
| 11 | 00:15 | 00:15 | The rule says: write 1, move left, then the machine halts. |
| 12 | 00:15 | 00:17 | It halts. The tape now reads 1 0 1, with the head resting on the middle square. Did your prediction match? |
| 13 | 00:18 | 00:21 | And this paper fantasy is your computer's blueprint. The tape became memory. The head became the CPU. The rule table became your program. |
| 14 | 00:21 | 00:24 | One machine that can run any program at all — that is exactly what a general-purpose computer is. |

---

**Total run time:** ~24 s.  
**Clean (caption-free) version:** set `SHOW_CAPTIONS = False` near the top of `turing_machine.py` and re-render — the `.srt` is still written, so you can narrate live over a caption-free picture.  
**Render commands:** `manim -qm turing_machine.py TuringMachine` (720p) or `-qh` for 1080p.