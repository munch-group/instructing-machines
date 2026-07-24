"""
Turing machine — an animated visual aid for *Instructing Machines*.

Renders the same 0 1 1 -> 1 0 1 trace that the lecture note poses as a SOLO
exercise, in the book's colour language (amber = kept, blue = temporary,
slate = the CPU/worker, teal = the tools/program).

USAGE
-----
    # medium quality (720p30):
    manim -qm turing_machine.py TuringMachine
    # high quality (1080p60) for the final:
    manim -qh turing_machine.py TuringMachine

SUBTITLES / NARRATION
---------------------
Every beat calls self.add_subcaption(...), so Manim writes a matching .srt
next to the video (…/subtitles/TuringMachine.srt). That file is both a
subtitle track you can load in any player AND a ready-made narration script
you can read aloud, beat by beat.

Set SHOW_CAPTIONS = False below to render a *clean* version with no on-screen
text — ideal when you want to narrate over it live. The .srt is still written
either way.
"""

from manim import *

# ---- toggle: on-screen captions burned into the video ----
SHOW_CAPTIONS = True

# ---- the book's palette ----
PAPER = "#f6f4ef"
INK = "#26313f"
INK_SOFT = "#5a6675"
LINE = "#dfd9cf"
KEEP = "#b26a1f"          # amber  - kept / permanent
TEMP = "#2f6db3"          # blue   - temporary / the tape
TEMP_BG = "#e8f1fb"
CPU = "#3a4250"           # slate  - the worker (head + state)
TOOL = "#1f7a68"          # teal   - the program (rule table)
CELL_FILL = "#ffffff"

# ---- the machine definition (same as the note's SOLO exercise) ----
BLANK = None
START_TAPE = [BLANK, "0", "1", "1", BLANK]   # 5 squares
START_HEAD = 1                               # over the "0"
START_STATE = "A"
RULES = {
    ("A", "0"): ("1", "R", "A"),
    ("A", "1"): ("0", "R", "B"),
    ("B", "1"): ("1", "L", "STOP"),
}
# human-readable rule lines for the on-screen table
RULE_LINES = [
    "state A · reads 0  →  write 1, move →, stay A",
    "state A · reads 1  →  write 0, move →, go B",
    "state B · reads 1  →  write 1, move ←, STOP",
]


class TuringMachine(Scene):
    def construct(self):
        self.camera.background_color = PAPER
        self.caption_mob = None

        # ---------- title ----------
        title = Text("The Turing machine", color=INK, weight=BOLD).scale(0.9)
        subtitle = Text("Alan Turing, 1936 — the simplest machine that can compute anything",
                        color=INK_SOFT).scale(0.42)
        subtitle.next_to(title, DOWN, buff=0.18)
        header = VGroup(title, subtitle).to_edge(UP, buff=0.35)

        self.beat("In 1936 Alan Turing imagined the simplest possible machine — "
                  "and it can compute anything your laptop can.",
                  lambda: self.play(FadeIn(title, shift=DOWN * 0.2),
                                    FadeIn(subtitle), run_time=1.4),
                  hold=0.4)

        # ---------- build the tape ----------
        cell_size = 1.15
        cells = VGroup()
        symbol_mobs = []   # one entry per square (Text or None)
        for i, val in enumerate(START_TAPE):
            sq = Square(side_length=cell_size, fill_color=CELL_FILL,
                        fill_opacity=1, stroke_color=LINE, stroke_width=2)
            cells.add(sq)
            symbol_mobs.append(None)
        cells.arrange(RIGHT, buff=0).move_to(ORIGIN + DOWN * 0.6)

        # place symbols
        for i, val in enumerate(START_TAPE):
            if val is not None:
                t = Text(val, color=INK, weight=BOLD).scale(0.9).move_to(cells[i])
                symbol_mobs[i] = t

        dots_l = Text("…", color="#b9b1a3").scale(0.8).next_to(cells, LEFT, buff=0.12)
        dots_r = Text("…", color="#b9b1a3").scale(0.8).next_to(cells, RIGHT, buff=0.12)

        self.beat("A paper tape, divided into squares. Each square holds a single symbol — "
                  "here a 0, a 1, or a blank.",
                  lambda: self.play(Create(cells), FadeIn(dots_l), FadeIn(dots_r),
                                    *[FadeIn(m) for m in symbol_mobs if m], run_time=1.4),
                  hold=0.3)

        # ---------- the head ----------
        head = Triangle(color=CPU, fill_color=CPU, fill_opacity=1).scale(0.28)
        head.rotate(PI)  # point downward
        head_label = Text("HEAD", color="#ffffff", weight=BOLD).scale(0.32)
        head_box = RoundedRectangle(corner_radius=0.08, width=head_label.width + 0.4,
                                    height=0.5, fill_color=CPU, fill_opacity=1,
                                    stroke_width=0)
        head_label.move_to(head_box)
        head_grp = VGroup(head_box, head_label)
        head = VGroup(head_grp, head)
        head.arrange(DOWN, buff=0.05)

        def head_target(idx):
            return cells[idx].get_top() + UP * (head.height / 2 + 0.12)

        head.move_to(head_target(START_HEAD))

        # ---------- the state ----------
        state_title = Text("STATE", color=CPU, weight=BOLD).scale(0.34)
        state_val = Text(START_STATE, color=CPU, weight=BOLD).scale(0.8)
        state_val.next_to(state_title, DOWN, buff=0.12)
        state_box = VGroup(state_title, state_val)
        state_frame = RoundedRectangle(corner_radius=0.12,
                                       width=1.7, height=1.5,
                                       stroke_color=CPU, stroke_width=2,
                                       fill_color="#eceef1", fill_opacity=1)
        state_box.move_to(state_frame)
        state_grp = VGroup(state_frame, state_box).to_edge(LEFT, buff=0.6).shift(UP * 0.7)

        self.beat("A head sits over one square. It can read the symbol, write a new one, "
                  "and move one step left or right. And it remembers a state.",
                  lambda: self.play(FadeIn(head, shift=DOWN * 0.2),
                                    FadeIn(state_grp), run_time=1.2),
                  hold=0.4)

        # ---------- the rules ----------
        rule_title = Text("THE RULES — the program", color=TOOL, weight=BOLD).scale(0.4)
        rule_texts = VGroup(*[Text(r, color=INK).scale(0.4) for r in RULE_LINES])
        rule_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rule_title.next_to(rule_texts, UP, buff=0.22).align_to(rule_texts, LEFT)
        rules_panel = VGroup(rule_title, rule_texts)
        panel_frame = RoundedRectangle(corner_radius=0.12,
                                       width=rules_panel.width + 0.6,
                                       height=rules_panel.height + 0.5,
                                       stroke_color=TOOL, stroke_width=2,
                                       fill_color="#ffffff", fill_opacity=1)
        panel_frame.move_to(rules_panel)
        rules_grp = VGroup(panel_frame, rules_panel).to_edge(RIGHT, buff=0.6).shift(UP * 0.9)

        self.beat("It follows a fixed table of rules. For each state and symbol, the table "
                  "says what to write, which way to move, and which state comes next.",
                  lambda: self.play(FadeIn(rules_grp), run_time=1.2),
                  hold=0.5)

        # ---------- run the machine ----------
        self.beat("Let's run it. The three squares say 0 1 1, the head is on the 0, "
                  "and the state is A. Predict the ending before each step.",
                  lambda: self.play(Indicate(cells[START_HEAD], color=TEMP,
                                             scale_factor=1.12), run_time=1.0),
                  hold=0.4)

        head_idx = START_HEAD
        state = START_STATE
        step_no = 0
        while True:
            sym = START_TAPE[head_idx]
            rule = RULES.get((state, sym))
            step_no += 1
            if rule is None:
                break
            write, move, new_state = rule

            # ---- read: highlight the current cell ----
            t0 = self.renderer.time
            self.set_caption(f"Step {step_no}: state {state} reads {sym} …")
            self.play(cells[head_idx].animate.set_fill(TEMP_BG, opacity=1)
                                             .set_stroke(TEMP, width=4), run_time=0.4)
            self.wait(0.5)
            self._sub_since(f"Step {step_no}: in state {state} the head reads {sym}.", t0)

            # ---- write + apply the rule (write, move, change state) ----
            t0 = self.renderer.time
            move_word = "right" if move == "R" else "left"
            if new_state == "STOP":
                tail = ", then the machine halts."
                cap_tail = ", then STOP"
            elif new_state != state:
                tail = f", and switch to state {new_state}."
                cap_tail = f", go to {new_state}"
            else:
                tail = f", and stay in state {state}."
                cap_tail = f", stay {state}"
            self.set_caption(f"write {write}, move {'→' if move=='R' else '←'}{cap_tail}")

            if write != sym and symbol_mobs[head_idx] is not None:
                new_t = Text(write, color=INK, weight=BOLD).scale(0.9).move_to(cells[head_idx])
                self.play(Transform(symbol_mobs[head_idx], new_t), run_time=0.6)
            START_TAPE[head_idx] = write

            # un-highlight before moving on
            self.play(cells[head_idx].animate.set_fill(CELL_FILL, opacity=1)
                                             .set_stroke(LINE, width=2), run_time=0.3)

            if new_state == "STOP":
                self.wait(0.3)
                self._sub_since(f"The rule says: write {write}, move {move_word}{tail}", t0)
                state = new_state
                break

            # move the head
            head_idx += 1 if move == "R" else -1
            self.play(head.animate.move_to(head_target(head_idx)), run_time=0.7)

            # change state
            if new_state != state:
                new_sv = Text(new_state, color=CPU, weight=BOLD).scale(0.8).move_to(state_val)
                self.play(Transform(state_val, new_sv), run_time=0.5)
                state = new_state
            self.wait(0.2)
            self._sub_since(f"The rule says: write {write}, move {move_word}{tail}", t0)

        # ---------- halted ----------
        halt = Text("HALTED", color=KEEP, weight=BOLD).scale(0.5)
        halt.next_to(cells, DOWN, buff=0.5)
        self.beat("It halts. The tape now reads 1 0 1, with the head resting on the middle "
                  "square. Did your prediction match?",
                  lambda: self.play(FadeIn(halt, scale=1.2),
                                    Indicate(cells[head_idx], color=KEEP), run_time=1.2),
                  hold=0.8)

        # ---------- the correspondence to a real computer ----------
        self.set_caption("")
        self.play(FadeOut(rules_grp), FadeOut(state_grp), FadeOut(head),
                  FadeOut(halt), FadeOut(dots_l), FadeOut(dots_r),
                  FadeOut(header), run_time=0.8)

        map_title = Text("The same idea became your computer", color=INK, weight=BOLD).scale(0.66)
        map_title.to_edge(UP, buff=0.6)
        rows = VGroup(
            self._map_row("the tape", "→", "memory", TEMP),
            self._map_row("the head", "→", "the CPU", CPU),
            self._map_row("the rule table", "→", "your program", TOOL),
        ).arrange(DOWN, buff=0.4).next_to(map_title, DOWN, buff=0.7)

        self.beat("And this paper fantasy is your computer's blueprint. The tape became "
                  "memory. The head became the CPU. The rule table became your program.",
                  lambda: self.play(FadeIn(map_title, shift=DOWN * 0.2),
                                    FadeOut(cells),
                                    *[FadeOut(m) for m in symbol_mobs if m],
                                    LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                                                lag_ratio=0.4),
                                    run_time=2.2),
                  hold=1.0)

        closing = Text("One machine that can run any program — that is a general-purpose computer.",
                       color=INK_SOFT).scale(0.42)
        closing.to_edge(DOWN, buff=0.8)
        self.beat("One machine that can run any program at all — that is exactly what a "
                  "general-purpose computer is.",
                  lambda: self.play(FadeIn(closing), run_time=1.2),
                  hold=1.6)

    # ---------------- helpers ----------------
    def _map_row(self, left, arrow, right, right_color):
        l = Text(left, color=INK).scale(0.6)
        a = Text(arrow, color=INK_SOFT).scale(0.6)
        r = Text(right, color=right_color, weight=BOLD).scale(0.6)
        row = VGroup(l, a, r).arrange(RIGHT, buff=0.5)
        return row

    def set_caption(self, text):
        """Swap the on-screen caption instantly (no time cost)."""
        if self.caption_mob is not None:
            self.remove(self.caption_mob)
            self.caption_mob = None
        if SHOW_CAPTIONS and text:
            cap = Text(text, color=INK).scale(0.42)
            maxw = config.frame_width - 1.2
            if cap.width > maxw:
                cap.scale(maxw / cap.width)
            cap.to_edge(DOWN, buff=0.45)
            self.caption_mob = cap
            self.add(cap)

    def _sub_since(self, text, t0):
        """Write one .srt entry spanning t0 → now (exact, non-overlapping)."""
        elapsed = max(0.1, self.renderer.time - t0)
        self.add_subcaption(text, duration=elapsed, offset=-elapsed)

    def beat(self, subtitle, play_callable, hold=0.5):
        """One narrated beat: show caption, play, hold, then log an exact subtitle."""
        t0 = self.renderer.time
        self.set_caption(subtitle)
        play_callable()
        if hold:
            self.wait(hold)
        self._sub_since(subtitle, t0)
