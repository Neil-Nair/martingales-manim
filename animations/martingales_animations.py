"""
martingales_animations.py
=========================
One Manim Scene per animation cue in the script.
Each scene is self-contained and exports a short video clip
you can embed in PowerPoint and trigger on click.

The random walks and Brownian paths come from the `simulations`
package at the repository root; this file only draws them.

HOW TO RENDER A SINGLE SCENE (recommended workflow, from the repo root):
    manim -pql animations/martingales_animations.py SceneName

HOW TO RENDER ALL SCENES AT ONCE:
    manim -pql animations/martingales_animations.py

QUALITY FLAGS:
    -ql  low quality  (fast preview, 480p)
    -qm  medium       (720p)
    -qh  high         (1080p, use for final export)

OUTPUT: media/videos/martingales_animations/<quality>/SceneName.mp4

GLOBAL STYLE NOTES:
  - All scenes use a white background with dark text.
  - Font sizes, colours, and spacing are defined as named constants
    at the top of each scene — adjust there to change layout globally.
  - MathTex uses LaTeX; Text uses plain strings.
  - Positions use Manim's coordinate system:
      centre = ORIGIN, right edge ≈ 7.1, top edge ≈ 4.0 (16:9 frame)
"""

import sys
from pathlib import Path

from manim import *
import numpy as np

# Make the repo-root `simulations` package importable however manim is run.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from simulations import (  # noqa: E402
    simple_random_walk,
    random_walk_ensemble,
    rescaled_random_walk,
    first_exit_index,
    brownian_path,
    first_hitting_index,
)

config.background_color = WHITE

Text.set_default(color=BLACK)
MathTex.set_default(color=BLACK)
Tex.set_default(color=BLACK)

# ─────────────────────────────────────────────────────────────
# GLOBAL PALETTE  (edit here to retheme everything at once)
# ─────────────────────────────────────────────────────────────
C_GREEN   = "#2E7D32"   # darker green — readable on white
C_RED     = "#C62828"   # darker red   — readable on white
C_BLUE    = "#1565C0"   # darker blue  — readable on white
C_YELLOW  = "#F57F17"   # dark amber   — readable on white
C_WHITE   = "#FFFFFF"   # used for coin fill / box fills
C_GREY    = "#757575"   # mid-grey for secondary text
C_DARK    = "#212121"   # near-black for main text / axes
C_BLACK   = "#000000"   # pure black outlines

# ── background / foreground shortcuts ──────────────────────
BG        = WHITE       # Manim colour constant for camera bg
FG        = C_DARK      # default text / stroke colour


# ═══════════════════════════════════════════════════════════════
# SECTION 1
# ═══════════════════════════════════════════════════════════════
class S1_TitleReveal(Scene):
    """
    SCRIPT CUE: [Animate: Title text fades in letter by letter —
    "Martingales: Get Even or Get Even Worse"]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        FONT_SIZE       = 52
        SUBTITLE_SIZE   = 32
        HOLD_TIME       = 2.0
        SUBTITLE_BUFF   = 0.5     # gap between title and subtitle
        # ───────────────────────────────────────────────────

        title = Text(
            "Martingales: Get Even or Get Even Worse",
            font_size=FONT_SIZE,
            color=C_DARK,
        )
        subtitle = Text(
            "by Neil Nair",
            font_size=SUBTITLE_SIZE,
            color=C_GREY,
        )

        title.move_to(ORIGIN)
        subtitle.next_to(title, DOWN, buff=SUBTITLE_BUFF)

        self.play(FadeIn(title))
        self.play(FadeIn(subtitle))
        self.wait(HOLD_TIME)

# ═══════════════════════════════════════════════════════════════
# SECTION 2
# ═══════════════════════════════════════════════════════════════
class S2_CoinLabels(Scene):
    """
    SCRIPT CUE: [Two coins appear centre-screen. They shift up, then the
    expected value equation builds term by term below.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        COIN_RADIUS   = 1.1
        COIN_COLOR    = "#F5CD69"
        COIN_STROKE   = "#8B6914"
        COIN_Y        = 0.6
        HEADS_X       = -3.0
        TAILS_X       =  3.0
        LABEL_FONT    = 44
        FACE_FONT     = 64
        LABEL_BUFF    = 0.35
        FADE_TIME     = 1
        STEP_PAUSE    = 0.5
        PULSE_SCALE   = 1.25
        PULSE_TIME    = 0.3
        HOLD_TIME     = 2.5
        EQ_FONT       = 40
        SHIFT_UP      = 1.5
        # ───────────────────────────────────────────────────

        def make_coin(x, y, face_char):
            circle = Circle(
                radius=COIN_RADIUS,
                fill_color=COIN_COLOR,
                fill_opacity=1,
                stroke_color=COIN_STROKE,
                stroke_width=6,
            ).move_to([x, y, 0])
            letter = Text(face_char, font_size=FACE_FONT,
                          color=C_DARK, weight=BOLD)
            letter.move_to(circle.get_center())
            return VGroup(circle, letter)

        heads_coin = make_coin(HEADS_X, COIN_Y, "H")
        tails_coin = make_coin(TAILS_X, COIN_Y, "T")

        profit_lbl = Text("profit  £1", font_size=LABEL_FONT, color=C_GREEN)
        loss_lbl   = Text("lose  £1",   font_size=LABEL_FONT, color=C_RED)
        profit_lbl.next_to(heads_coin, DOWN, buff=LABEL_BUFF)
        loss_lbl.next_to(tails_coin,   DOWN, buff=LABEL_BUFF)

        coin_group = VGroup(heads_coin, tails_coin, profit_lbl, loss_lbl)

        scene_title = Text("Fair Game", font_size=32, color=C_DARK, weight=BOLD)
        scene_title.to_edge(UP, buff=0.3)
        bet_lbl = Text("Bet: £1", font_size=28, color=C_GREY)
        bet_lbl.to_corner(UR, buff=0.4)
        
        self.play(FadeIn(scene_title), FadeIn(bet_lbl))
        self.play(FadeIn(heads_coin), FadeIn(tails_coin), run_time=FADE_TIME)
        self.wait(5)
        self.play(FadeIn(profit_lbl), run_time=FADE_TIME)
        self.play(FadeIn(loss_lbl),   run_time=FADE_TIME)
        self.wait(0.6)

        self.play(coin_group.animate.shift(UP * SHIFT_UP), run_time=0.8)

        define_p = Text("Let P be your profit after one round of this game.",
                        font_size=26, color=C_DARK)
        define_p.move_to([0, -1.2, 0])
        self.play(FadeIn(define_p, shift=UP * 0.1))
        self.wait(2.0)
        self.play(FadeOut(define_p))
        self.wait(0.3)

        lhs      = MathTex(r"E(P)",                          font_size=EQ_FONT, color=C_DARK)
        eq       = MathTex(r"=",                             font_size=EQ_FONT, color=C_DARK)
        neg_term = MathTex(r"\tfrac{1}{2} \times (-1)",      font_size=EQ_FONT, color=C_RED)
        plus     = MathTex(r"+",                             font_size=EQ_FONT, color=C_DARK)
        pos_term = MathTex(r"\tfrac{1}{2} \times (+1)",      font_size=EQ_FONT, color=C_GREEN)
        eq2      = MathTex(r"=",                             font_size=EQ_FONT, color=C_DARK)
        zero     = MathTex(r"0",                             font_size=EQ_FONT, color=C_YELLOW)

        full_eq = VGroup(lhs, eq, neg_term, plus, pos_term, eq2, zero)
        full_eq.arrange(RIGHT, buff=0.2)
        full_eq.move_to([0, -2.0, 0])

        self.play(FadeIn(lhs), FadeIn(eq))
        self.wait(STEP_PAUSE)
        self.play(FadeIn(neg_term))
        self.wait(STEP_PAUSE)
        self.play(FadeIn(plus), FadeIn(pos_term))
        self.wait(STEP_PAUSE)
        self.play(FadeIn(eq2), FadeIn(zero))
        self.wait(STEP_PAUSE)
        self.play(scene_title.animate.set_color(C_YELLOW), run_time=0.4)

        self.play(zero.animate.scale(PULSE_SCALE), run_time=PULSE_TIME)
        self.play(zero.animate.scale(1 / PULSE_SCALE), run_time=PULSE_TIME)
        self.wait(HOLD_TIME)


class S2_SingleRandomWalk(Scene):
    """
    SCRIPT CUE: [One simulation draws slowly then fast. Expected profit line
    appears. After a pause, 20 more simulations fade in. Then the spread
    envelope draws itself.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        N_STEPS        = 100
        N_WALKS        = 20
        SEED_SINGLE    = 42
        SLOW_STEPS     = 5
        SLOW_DURATION  = 0.35
        FAST_DURATION  = 0.017
        WALK_OPACITY   = 0.08
        AXIS_X_RANGE   = [0, 100, 10]
        AXIS_Y_RANGE   = [-20, 20, 5]
        AXIS_X_LEN     = 10.0
        AXIS_Y_LEN     = 5.5
        PAUSE_AFTER_EXP   = 3.0
        PAUSE_AFTER_MANY  = 2.0
        HOLD_TIME         = 3.0
        # ───────────────────────────────────────────────────

        axes = Axes(
            x_range=AXIS_X_RANGE,
            y_range=AXIS_Y_RANGE,
            x_length=AXIS_X_LEN,
            y_length=AXIS_Y_LEN,
            axis_config={
                "color": BLACK,
                "include_tip": False,
                "include_numbers": False,
            },
        ).move_to(ORIGIN)

        x_labels = VGroup()
        for val in range(0, 101, 10):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(axes.c2p(val, 0), DOWN, buff=0.15)
            x_labels.add(lbl)

        y_labels = VGroup()
        for val in range(-20, 21, 5):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(axes.c2p(0, val), LEFT, buff=0.15)
            y_labels.add(lbl)

        title = Text("One simulation", font_size=28)
        title.next_to(axes, UP, buff=0.25)

        x_label = Text("Round number", font_size=22)
        x_label.next_to(axes, DOWN, buff=0.55)

        y_label = Text("Cumulative profit £", font_size=22)
        y_label.rotate(PI / 2)
        y_label.next_to(axes, LEFT, buff=0.65)

        exp_line = axes.plot(lambda x: 0, x_range=[0, 100],
                             color=C_RED, stroke_width=2.5)
        exp_label = Text("Expected profit", font_size=16, color=C_RED)
        exp_label.next_to(axes.c2p(100, 0), RIGHT, buff=0.15)

        # ── Phase 1: axes + single walk ──────────────────────
        self.play(
            Create(axes),
            FadeIn(title),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(x_labels),
            FadeIn(y_labels),
        )

        profit = simple_random_walk(N_STEPS, seed=SEED_SINGLE)

        for i in range(N_STEPS):
            duration = SLOW_DURATION if i < SLOW_STEPS else FAST_DURATION
            seg = VMobject(stroke_color=C_BLUE, stroke_width=2.5, fill_opacity=0)
            seg.set_points_as_corners([
                axes.c2p(i,     profit[i]),
                axes.c2p(i + 1, profit[i + 1]),
            ])
            self.play(Create(seg), run_time=duration)

        self.play(Create(exp_line), FadeIn(exp_label))
        self.wait(PAUSE_AFTER_EXP)

        # ── Phase 2: update title, fade in 20 more walks ─────
        new_title = Text("20 simulations", font_size=28)
        new_title.next_to(axes, UP, buff=0.25)
        self.play(Transform(title, new_title))

        walks   = random_walk_ensemble(N_WALKS, N_STEPS, seed=99)
        colours = color_gradient([C_BLUE, "#E91E63", "#4CAF50", "#FF9800"], N_WALKS)
        walk_group = VGroup()
        for i in range(N_WALKS):
            p = walks[i]
            path = VMobject(stroke_color=colours[i], stroke_width=1.8, fill_opacity=0)
            path.set_points_as_corners(
                [axes.c2p(x, y) for x, y in enumerate(p)]
            )
            path.set_opacity(0.5)
            walk_group.add(path)

        self.play(FadeIn(walk_group))
        self.wait(PAUSE_AFTER_MANY)

        # ── Phase 3: spread envelope ─────────────────────────
        sqrt_pos = DashedVMobject(
            axes.plot(lambda x: np.sqrt(max(x, 0.001)),
                      x_range=[0.1, 100], color=BLACK, stroke_width=2.5),
            num_dashes=40,
        )
        sqrt_neg = DashedVMobject(
            axes.plot(lambda x: -np.sqrt(max(x, 0.001)),
                      x_range=[0.1, 100], color=BLACK, stroke_width=2.5),
            num_dashes=40,
        )
        spread_label = MathTex(r"\text{spread} \sim \sqrt{n}", font_size=30)
        spread_label.next_to(axes.c2p(100, np.sqrt(100)), RIGHT, buff=0.1)

        self.play(Create(sqrt_pos), Create(sqrt_neg), run_time=1.5)
        self.play(FadeIn(spread_label))
        self.wait(HOLD_TIME)


class S2_DoublingTable(Scene):
    """
    SCRIPT CUE: [Table with 4 columns. Rows fill in one at a time.
    Table scrolls up, revealing ellipsis rows, then LIMIT REACHED crashes down.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        HEADER_FS   = 28
        ROW_FS      = 26
        ROW_PAUSE   = 0.5
        BANNER_FS   = 44
        HOLD_TIME   = 2.0
        ROW_HEIGHT  = 0.65
        COL_GAPS    = [1.8, 1.2, 2, 2]   # spacing between columns
        # ───────────────────────────────────────────────────

        headers = ["Round", "Bet", "Net if W now", "Net if L now"]
        rows = [
            ["1", "£1",   "+£1",    "-£1"],
            ["2", "£2",   "+£1",    "-£3"],
            ["3", "£4",   "+£1",    "-£7"],
            ["4", "£8",   "+£1",    "-£15"],
            ["5", "£16",  "+£1",    "-£31"],
            ["6", "£32",  "+£1",    "-£63"],
            ["7", "£64",  "+£1",    "-£127"],
            ["8", "£128", "+£1",    "-£255"],
        ]

        # Column x positions
        col_xs = [-4.5, -1.8, 0.5, 3.2]

        # --- Header ---
        header_cells = VGroup()
        for i, h in enumerate(headers):
            colour = C_GREEN if i == 2 else (C_RED if i == 3 else C_DARK)
            cell = Text(h, font_size=HEADER_FS, color=colour, weight=BOLD)
            cell.move_to([col_xs[i], 3.2, 0])
            header_cells.add(cell)

        underline = Line(
            [-5.5, 2.85, 0], [5.5, 2.85, 0],
            color=C_DARK, stroke_width=1.5
        )

        intro_title = Text("A better approach.", font_size=34,
                           color=C_DARK, weight=BOLD)
        intro_title.move_to(UP * 1.0)
        intro_ul = Line(
            intro_title.get_corner(DL) + DOWN * 0.08,
            intro_title.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        intro_sub = Text("Changing bet size based off past information.",
                         font_size=26, color=C_GREY)
        intro_sub.next_to(intro_title, DOWN, buff=0.4)

        self.play(FadeIn(intro_title), Create(intro_ul))
        self.play(FadeIn(intro_sub, shift=UP * 0.1))
        self.wait(2.5)
        self.play(FadeOut(VGroup(intro_title, intro_ul, intro_sub)))
        self.wait(0.3)

        self.play(FadeIn(header_cells), Create(underline))
        # --- Data rows ---
        all_row_objects = VGroup()
        for idx, row in enumerate(rows):
            y_pos = 2.4 - idx * ROW_HEIGHT
            cells = VGroup()
            for col_idx, cell_text in enumerate(row):
                if col_idx == 2:
                    colour = C_GREEN
                elif col_idx == 3:
                    colour = C_RED
                else:
                    colour = C_DARK
                cell = Text(cell_text, font_size=ROW_FS, color=colour)
                cell.move_to([col_xs[col_idx], y_pos, 0])
                cells.add(cell)
            all_row_objects.add(cells)

        # First 3 rows: slow, one at a time
        for cells in all_row_objects[:3]:
            self.play(FadeIn(cells), run_time=0.35)
            self.wait(5.0)

        # Remaining rows: all at once
        remaining = VGroup(*all_row_objects[3:])
        self.play(FadeIn(remaining), run_time=0.35)
        self.wait(ROW_PAUSE)

        # --- Scroll everything up so rows go off screen ---
        table_group = VGroup(header_cells, underline, all_row_objects)
        self.play(
            table_group.animate.shift(UP * 3.0),
            run_time=2.0,
            rate_func=smooth,
        )

        # --- Ellipsis dots appear in centre ---
        dots = Text("⋮", font_size=60, color=C_DARK)
        dots.move_to(ORIGIN)
        self.play(FadeIn(dots))
        self.wait(10.0)

        # --- LIMIT REACHED banner crashes down ---
        banner = Text("LIMIT REACHED", font_size=BANNER_FS, color=C_RED, weight=BOLD)
        banner_bg = SurroundingRectangle(
            banner, color=C_RED, fill_color=C_RED, fill_opacity=0.15, buff=0.25
        )
        banner_group = VGroup(banner_bg, banner)
        banner_group.move_to([0, 5.5, 0])

        self.play(FadeOut(dots), run_time=0.2)
        self.play(
            banner_group.animate.move_to(ORIGIN),
            run_time=0.7,
            rate_func=rush_into,
        )
        self.wait(HOLD_TIME)

# ═══════════════════════════════════════════════════════════════
# SECTION 3
# ═══════════════════════════════════════════════════════════════

class S3_RandomWalkWithMean(Scene):
    """
    SCRIPT CUE: [Random walk draws. Mean line appears. Graph shrinks and shifts
    left. Annotation fades in. Then martingale definition builds below it.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        N_STEPS       = 40
        SEED          = 3
        STEP_DURATION = 0.06
        AXIS_X_RANGE  = [0, 42, 10]
        AXIS_Y_RANGE  = [-8, 8, 4]
        AXIS_X_LEN    = 9.0
        AXIS_Y_LEN    = 5.0
        HOLD_TIME     = 2.0
        SHIFT_LEFT    = 2.8
        FONT_SIZE     = 48
        STEP_PAUSE    = 0.5
        PULSE_SCALE   = 1.1
        PULSE_TIME    = 0.3
        # ───────────────────────────────────────────────────

        # Title + underline
        title = Text("Martingale Definition", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=BLACK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))

        profit = simple_random_walk(N_STEPS, seed=SEED)

        axes = Axes(
            x_range=AXIS_X_RANGE,
            y_range=AXIS_Y_RANGE,
            x_length=AXIS_X_LEN,
            y_length=AXIS_Y_LEN,
            axis_config={"color": C_DARK},
        )
        axes.move_to(ORIGIN + DOWN * 0.3)

        x_label = MathTex(r"n", font_size=28)
        x_label.next_to(axes, DOWN, buff=0.45)

        y_label = MathTex(r"M_n", font_size=28)
        y_label.rotate(PI / 2)
        y_label.next_to(axes, LEFT, buff=0.45)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        # Draw walk
        segs = VGroup()
        for i in range(N_STEPS):
            seg = VMobject(stroke_color=C_BLUE, stroke_width=2.5, fill_opacity=0)
            seg.set_points_as_corners([
                axes.c2p(i,     profit[i]),
                axes.c2p(i + 1, profit[i + 1]),
            ])
            segs.add(seg)
            self.play(Create(seg), run_time=STEP_DURATION)

        mean_line  = axes.plot(lambda x: 0, color=C_RED, stroke_width=3)
        mean_label = MathTex(r"\mathbb{E}[M_n] = 0", font_size=24, color=C_RED)
        mean_label.next_to(mean_line, UP, buff=0.15).shift(RIGHT * 2)
        self.play(Create(mean_line), FadeIn(mean_label))
        self.wait(HOLD_TIME)

        # Shrink and shift left
        graph_group = VGroup(axes, segs, mean_line, mean_label, x_label, y_label)
        self.play(ScaleInPlace(graph_group, 0.8), run_time=0.6)
        self.play(ApplyMethod(graph_group.shift, LEFT * SHIFT_LEFT), run_time=1.0)
        self.wait(2.0)

        # Annotation top-right
        annotation = MathTex(
            r"M_n \sim \text{total profit after } n \text{ rounds}",
            font_size=34,
        )
        annotation.move_to(RIGHT * 3.8 + UP * 1.2)
        self.play(FadeIn(annotation, shift=LEFT * 0.2))
        self.wait(4.0)

        # Martingale definition builds below annotation
        parts = [
            MathTex(r"\mathbb{E}[",       font_size=FONT_SIZE),
            MathTex(r"M_{n+1}",           font_size=FONT_SIZE),
            MathTex(r"\mid \text{past}]",  font_size=FONT_SIZE),
            MathTex(r"=",                 font_size=FONT_SIZE),
            MathTex(r"M_n",               font_size=FONT_SIZE),
        ]
        eq = VGroup(*parts)
        eq.arrange(RIGHT, buff=0.15)
        eq.next_to(annotation, DOWN, buff=0.6)

        for part in parts:
            self.play(FadeIn(part, shift=UP * 0.1), run_time=0.4)
            self.wait(STEP_PAUSE)

        self.play(eq.animate.scale(PULSE_SCALE), run_time=PULSE_TIME)
        self.play(eq.animate.scale(1 / PULSE_SCALE), run_time=PULSE_TIME)

        box = SurroundingRectangle(eq, color=C_YELLOW, buff=0.2, corner_radius=0.1)
        self.play(Create(box), run_time=0.8)
        self.wait(HOLD_TIME)

class S3_ConservationLawInset(Scene):
    """
    SCRIPT CUE: [Ball follows true parabolic projectile arc. Energy conservation
    equations appear on the right. Caption 'no dynamics' fades in.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        EQ_FS     = 50
        HOLD_TIME = 3.0
        VX        = 2.5
        VY        = 4.0
        G         = 4.0
        # ───────────────────────────────────────────────────

        # ── Axes ──
        axes = Axes(
            x_range=[0, 6, 2],
            y_range=[0, 4, 2],
            x_length=4.5,
            y_length=3.0,
            axis_config={"color": C_DARK, "include_tip": False},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)

        x_lbl = MathTex(r"x", font_size=24).next_to(axes, DOWN, buff=0.25)
        y_lbl = MathTex(r"y", font_size=24).next_to(axes, LEFT, buff=0.25)
        ground = Line(axes.c2p(0, 0), axes.c2p(6, 0),
                      color=C_DARK, stroke_width=2)

        self.play(
            Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), Create(ground),
            run_time=0.5,
        )

        # ── Pure projectile trajectory ──
        t_flight = 2 * VY / G
        n_pts    = 60
        t_vals   = np.linspace(0, t_flight, n_pts)
        x_vals   = VX * t_vals
        y_vals   = VY * t_vals - 0.5 * G * t_vals ** 2

        traj_pts = [axes.c2p(x, y) for x, y in zip(x_vals, y_vals)]

        traj_mob = VMobject(stroke_color=C_BLUE, stroke_width=2, fill_opacity=0)
        traj_mob.set_points_as_corners(traj_pts)
        traj_dashed = DashedVMobject(traj_mob, num_dashes=25)

        ball = Dot(radius=0.15, color=C_YELLOW).move_to(traj_pts[0])
        self.play(Create(traj_dashed), FadeIn(ball), run_time=0.5)

        for i in range(1, n_pts):
            self.play(ball.animate.move_to(traj_pts[i]), run_time=0.015)

        self.wait(0.3)

        # ── Peak height marker ──
        t_peak = VY / G
        x_peak = VX * t_peak
        y_peak = VY * t_peak - 0.5 * G * t_peak ** 2

        peak_line = DashedLine(
            axes.c2p(x_peak, 0),
            axes.c2p(x_peak, y_peak),
            color=C_GREY, stroke_width=1.5,
        )
        peak_lbl = MathTex(r"h_{max}", font_size=22, color=C_GREY)
        peak_lbl.next_to(axes.c2p(x_peak, y_peak / 2), RIGHT, buff=0.1)

        # v_i: angled upward-right from launch point
        v_i_arrow = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(VX * 0.3, VY * 0.3),
            color=C_GREEN, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.2,
        )
        # v_f: angled downward-right at landing point
        v_f_arrow = Arrow(
            start=axes.c2p(x_vals[-1], 0),
            end=axes.c2p(x_vals[-1] + VX * 0.3, -VY * 0.3),
            color=C_RED, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.2,
        )
        v_i_lbl = MathTex(r"v_i", font_size=22, color=C_GREEN)
        v_f_lbl = MathTex(r"v_f", font_size=22, color=C_RED)
        v_i_lbl.next_to(v_i_arrow, LEFT, buff=0.1)
        v_f_lbl.next_to(v_f_arrow, RIGHT, buff=0.1)

        self.play(
            Create(peak_line), FadeIn(peak_lbl),
            GrowArrow(v_i_arrow), FadeIn(v_i_lbl),
            GrowArrow(v_f_arrow), FadeIn(v_f_lbl),
            run_time=0.5,
        )

        # ── Title centred at top ──
        eq_title = Text("Conservation of Energy", font_size=30, weight=BOLD)
        eq_title.to_edge(UP, buff=0.4)
        eq_underline = Line(
            eq_title.get_corner(DL) + DOWN * 0.08,
            eq_title.get_corner(DR) + DOWN * 0.08,
            color=BLACK, stroke_width=1.5,
        )
        self.play(FadeIn(eq_title), Create(eq_underline), run_time=0.5)

        # ── Equations on the right ──
        eq1 = MathTex(
            r"\tfrac{1}{2}mv_i^2 = \tfrac{1}{2}mv_f^2 + mgh_{max}",
            font_size=EQ_FS,
        )
        eq2 = MathTex(
            r"v_i^2 = v_f^2 + 2gh_{max}",
            font_size=EQ_FS,
        )
        eq3 = MathTex(
            r"v_f = \sqrt{v_i^2 - 2gh_{max}}",
            font_size=EQ_FS, color=C_GREEN,
        )

        eqs = VGroup(eq1, eq2, eq3)
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        eqs.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)

        self.play(FadeIn(eq1), run_time=0.2); self.wait(0.5)
        self.play(FadeIn(eq2), run_time=0.2); self.wait(0.5)
        self.play(FadeIn(eq3), run_time=0.2); self.wait(0.5)

        # ── Caption ──
        caption = Text("no dynamics required! we are using a conservation law",
                       font_size=28, color=C_GREY)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(HOLD_TIME)

# class S3_RandomWalkDefinition(Scene):
    """
    SCRIPT CUE: [Random walk graph fades in. Definition appears.
    +1/-1 flash. Expectation chain builds. OST. Quote at bottom.]
    """
    def construct(self):
        self.camera.background_color = BG
        
        
        # ── tuneable constants ──────────────────────────────
        FONT_SIZE   = 36
        FLASH_REPS  = 3
        FLASH_TIME  = 0.3
        HOLD_TIME   = 2.5
        SEED        = 17
        N_STEPS     = 40
        # ───────────────────────────────────────────────────
        title = Text("Random Walks: the Optional Stopping Theorem", font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=BLACK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))
        # ── Small random walk graph, left side ──
        profit = simple_random_walk(N_STEPS, seed=SEED)

        axes = Axes(
            x_range=[0, 42, 10],
            y_range=[-8, 8, 4],
            x_length=4.5,
            y_length=3.0,
            axis_config={"color": C_DARK, "include_tip": False},
        ).shift(LEFT*1.5 +DOWN * 0.5)

        walk_path = VMobject(stroke_color=C_BLUE, stroke_width=2, fill_opacity=0)
        walk_path.set_points_as_corners(
            [axes.c2p(i, profit[i]) for i in range(N_STEPS + 1)]
        )

        x_lbl = MathTex(r"n",   font_size=22).next_to(axes, DOWN, buff=0.2)
        y_lbl = MathTex(r"X_n", font_size=22).rotate(PI/2).next_to(axes, LEFT, buff=0.2)

        self.play(
            FadeIn(axes), FadeIn(walk_path),
            FadeIn(x_lbl), FadeIn(y_lbl),
            run_time=0.8,
        )

        # ── Definition — right side ──
        part_lhs  = MathTex(r"X_{n+1}", font_size=FONT_SIZE)
        part_eq   = MathTex(r"=", font_size=FONT_SIZE)
        part_xn   = MathTex(r"X_n", font_size=FONT_SIZE)
        part_plus = MathTex(r"+", font_size=FONT_SIZE)
        part_xi   = MathTex(r"\xi_{n+1},", font_size=FONT_SIZE)
        part_dist = MathTex(r"\xi_{n+1} \sim \pm 1 \ (p = \tfrac{1}{2})", font_size=FONT_SIZE)

        walk_def = VGroup(part_lhs, part_eq, part_xn, part_plus, part_xi)
        walk_def.arrange(RIGHT, buff=0.2)
        dist_lbl = part_dist
        dist_lbl.next_to(walk_def, DOWN, buff=0.3)

        walk_def_group = VGroup(walk_def, dist_lbl)
        walk_def_group.move_to(RIGHT * 1.5 + UP * 2.5)

        self.play(Write(walk_def), run_time=1.0)
        self.play(FadeIn(dist_lbl), run_time=0.5)
        self.wait(0.4)

        # ── Annotation phase ──
        def make_underline(mob):
            return Line(
                mob.get_corner(DL) + DOWN * 0.05,
                mob.get_corner(DR) + DOWN * 0.05,
                stroke_width=2.5,
            )

        # Annotate X_{n+1}
        ul_lhs = make_underline(part_lhs)
        ul_lhs.set_color(C_GREEN)
        arr_lhs = Arrow(part_lhs.get_bottom() + DOWN * 0.3,
                        part_lhs.get_bottom() + DOWN * 0.9 + RIGHT * 0.8,
                        color=C_GREEN, buff=0, stroke_width=2)
        txt_lhs = Text("value of next step", font_size=22, color=C_GREEN)
        txt_lhs.next_to(arr_lhs.get_end(), RIGHT, buff=0.1)
        self.play(Create(ul_lhs), GrowArrow(arr_lhs), FadeIn(txt_lhs), run_time=0.5)
        self.wait(0.8)

        # Annotate X_n
        ul_xn = make_underline(part_xn)
        ul_xn.set_color(C_GREEN)
        arr_xn = Arrow(part_xn.get_bottom() + DOWN * 0.3,
                       part_xn.get_bottom() + DOWN * 0.9,
                       color=C_GREEN, buff=0, stroke_width=2)
        txt_xn = Text("current value", font_size=22, color=C_GREEN)
        txt_xn.next_to(arr_xn.get_end(), RIGHT, buff=0.1)
        self.play(Create(ul_xn), GrowArrow(arr_xn), FadeIn(txt_xn), run_time=0.5)
        self.wait(0.8)

        # Annotate xi_{n+1}
        ul_xi = make_underline(part_xi)
        ul_xi.set_color(C_RED)
        arr_xi = Arrow(part_xi.get_bottom() + DOWN * 0.3,
                       part_xi.get_bottom() + DOWN * 0.9 + LEFT * 0.5,
                       color=C_RED, buff=0, stroke_width=2)
        txt_xi = Text("step direction", font_size=22, color=C_RED)
        txt_xi.next_to(arr_xi.get_end(), RIGHT, buff=0.1)
        self.play(Create(ul_xi), GrowArrow(arr_xi), FadeIn(txt_xi), run_time=0.5)
        self.wait(0.8)

        # Fade out all annotations
        annotations = VGroup(
            ul_lhs, arr_lhs, txt_lhs,
            ul_xn,  arr_xn,  txt_xn,
            ul_xi,  arr_xi,  txt_xi,
        )
        self.play(FadeOut(annotations), run_time=0.5)
        self.wait(0.3)
        # Flash +1 / -1
        plus_one  = MathTex(r"+1", font_size=FONT_SIZE + 8, color=C_GREEN)
        minus_one = MathTex(r"-1", font_size=FONT_SIZE + 8, color=C_RED)
        plus_one.next_to(walk_def, DOWN, buff=0.4)
        minus_one.move_to(plus_one)

        for _ in range(FLASH_REPS):
            self.play(FadeIn(plus_one),   run_time=FLASH_TIME)
            self.play(FadeOut(plus_one),  run_time=FLASH_TIME)
            self.play(FadeIn(minus_one),  run_time=FLASH_TIME)
            self.play(FadeOut(minus_one), run_time=FLASH_TIME)

        # ── Expectation chain ──
        exp1 = MathTex(
            r"\mathbb{E}[X_{n+1} \mid \text{past}] = X_n",
            font_size=FONT_SIZE,
        )
        exp1.next_to(walk_def, DOWN, buff=0.5)
        self.play(FadeIn(exp1, shift=UP * 0.1), run_time=0.5)
        self.wait(0.4)

        exp2 = MathTex(
            r"\mathbb{E}[X_n \mid \text{past}] = X_{n-1}",
            font_size=FONT_SIZE,
        )
        exp2.next_to(exp1, DOWN, buff=0.35)
        self.play(FadeIn(exp2, shift=UP * 0.1), run_time=0.5)
        self.wait(0.4)

        vdots = MathTex(r"\vdots", font_size=FONT_SIZE)
        vdots.next_to(exp2, DOWN, buff=0.25)
        self.play(FadeIn(vdots), run_time=0.4)
        self.wait(0.3)

        # ── OST ──
        therefore = MathTex(r"\therefore", font_size=FONT_SIZE, color=C_YELLOW)
        arrow = Arrow(
            start=ORIGIN, end=RIGHT * 0.7,
            color=C_YELLOW, buff=0,
        )
        ost = MathTex(
            r"\mathbb{E}[M_T] = \mathbb{E}[M_0]",
            font_size=FONT_SIZE + 4,
        )
        ost_row = VGroup(therefore, arrow, ost)
        ost_row.arrange(RIGHT, buff=0.2)
        ost_row.next_to(vdots, DOWN, buff=0.35)

        box = SurroundingRectangle(
            ost, color=C_YELLOW, buff=0.2, corner_radius=0.1
        )

        self.play(FadeIn(therefore))
        self.play(GrowArrow(arrow))
        self.play(FadeIn(ost, scale=0.8))
        self.play(Create(box))
        self.wait(1.0)

        # ── Quote at bottom ──
        quote = Text(
            "On average, nothing can be gained by playing a fair game.",
            font_size=26, color=C_GREY,
        )
        quote.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(quote, shift=UP * 0.15), run_time=0.6)
        self.wait(HOLD_TIME)

class S3_RandomWalkDefinition(Scene):
    """
    SCRIPT CUE: [Random walk graph top-left. Definition top-right.
    Annotations point to each term. Then expectation chain and OST.]
    """
    def construct(self):
        self.camera.background_color = BG

        # ── tuneable constants ──────────────────────────────
        FONT_SIZE  = 34
        HOLD_TIME  = 2.5
        SEED       = 17
        N_STEPS    = 40
        STEP_TIME  = 0.12   # duration per step during walk replay
        # ───────────────────────────────────────────────────

        # ── Title ──
        title = Text("Simple Random Walk: Optional Stopping Theorem", font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=BLACK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))

        # ── Random walk graph — top left ──
        profit = simple_random_walk(N_STEPS, seed=SEED)
        steps  = np.diff(profit)          # the individual +1 / -1 moves

        axes = Axes(
            x_range=[0, 42, 10],
            y_range=[-8, 8, 4],
            x_length=4.0,
            y_length=2.8,
            axis_config={"color": C_DARK, "include_tip": False},
        ).move_to(LEFT * 3.2 + UP * 0.8)

        walk_path = VMobject(stroke_color=C_BLUE, stroke_width=2, fill_opacity=0)
        walk_path.set_points_as_corners(
            [axes.c2p(i, profit[i]) for i in range(N_STEPS+1)]
        )
        x_lbl = MathTex(r"n",   font_size=20).next_to(axes, DOWN, buff=0.15)
        y_lbl = MathTex(r"X_n", font_size=20).rotate(PI/2).next_to(axes, LEFT, buff=0.15)

        self.play(
            FadeIn(axes), FadeIn(walk_path),
            FadeIn(x_lbl), FadeIn(y_lbl),
            run_time=0.8,
        )

        # ── Definition parts — top right ──
        part_lhs  = MathTex(r"X_{n+1}",  font_size=FONT_SIZE)
        part_eq   = MathTex(r"=",         font_size=FONT_SIZE)
        part_xn   = MathTex(r"X_n",       font_size=FONT_SIZE)
        part_plus = MathTex(r"+",          font_size=FONT_SIZE)
        part_xi   = MathTex(r"\xi_{n+1}", font_size=FONT_SIZE)

        walk_def = VGroup(part_lhs, part_eq, part_xn, part_plus, part_xi)
        walk_def.arrange(RIGHT, buff=0.18)
        walk_def.move_to(RIGHT * 2.2 + UP * 2.5)

        dist_lbl = MathTex(
            r"\xi_{n+1} \sim \pm 1, \quad p = \tfrac{1}{2}",
            font_size=FONT_SIZE - 4,
            color=C_GREY,
        )
        dist_lbl.next_to(walk_def, DOWN, buff=0.25)

        self.play(Write(walk_def), run_time=0.8)
        self.play(FadeIn(dist_lbl), run_time=0.4)
        self.wait(7)

        # ── Annotations ──
        def make_ul(mob, colour):
            return Line(
                mob.get_corner(DL) + DOWN * 0.05,
                mob.get_corner(DR) + DOWN * 0.05,
                stroke_width=2.5, color=colour,
            )

        txt_lhs = Text("value of\nnext step", font_size=18, color=C_GREEN)
        txt_xn  = Text("current\nvalue",      font_size=18, color=C_GREEN)
        txt_xi  = Text("step\ndirection",     font_size=18, color=C_RED)

        label_row = VGroup(txt_lhs, txt_xn, txt_xi)
        label_row.arrange(RIGHT, buff=0.8)
        label_row.next_to(dist_lbl, DOWN, buff=1.4)

        ul_lhs = make_ul(part_lhs, C_GREEN)
        ul_xn  = make_ul(part_xn,  C_GREEN)
        ul_xi  = make_ul(part_xi,  C_RED)

        arr_lhs = Arrow(part_lhs.get_bottom(), txt_lhs.get_top(),
                        color=C_GREEN, buff=0.1, stroke_width=2,
                        max_tip_length_to_length_ratio=0.15)
        arr_xn  = Arrow(part_xn.get_bottom(),  txt_xn.get_top(),
                        color=C_GREEN, buff=0.1, stroke_width=2,
                        max_tip_length_to_length_ratio=0.15)
        arr_xi  = Arrow(part_xi.get_bottom(),  txt_xi.get_top(),
                        color=C_RED,   buff=0.1, stroke_width=2,
                        max_tip_length_to_length_ratio=0.15)

        self.play(Create(ul_lhs), GrowArrow(arr_lhs), FadeIn(txt_lhs), run_time=0.5)
        self.wait(2)
        self.play(Create(ul_xn),  GrowArrow(arr_xn),  FadeIn(txt_xn),  run_time=0.5)
        self.wait(1.5)
        self.play(Create(ul_xi),  GrowArrow(arr_xi),  FadeIn(txt_xi),  run_time=0.5)
        self.wait(1.5)

        annotations = VGroup(
            ul_lhs, arr_lhs, txt_lhs,
            ul_xn,  arr_xn,  txt_xn,
            ul_xi,  arr_xi,  txt_xi,
        )
        self.play(FadeOut(annotations), run_time=0.5)
        self.wait(0.3)

        # ── Animated walk replay with tracker dot + flash labels ──
        # Yellow vertical dashed line tracking current n position
        tracker_line = DashedLine(
            axes.c2p(0, -8), axes.c2p(0, 8),
            color=C_YELLOW, stroke_width=2, dash_length=0.08,
        )
        tracker_dot = Dot(radius=0.12, color=C_YELLOW)
        tracker_dot.move_to(axes.c2p(0, profit[0]))

        plus_one  = MathTex(r"+1", font_size=FONT_SIZE + 8, color=C_GREEN)
        minus_one = MathTex(r"-1", font_size=FONT_SIZE + 8, color=C_RED)
        flash_pos = dist_lbl.get_center() + DOWN * 0.7
        plus_one.move_to(flash_pos)
        minus_one.move_to(flash_pos)

        self.play(FadeIn(tracker_line), FadeIn(tracker_dot), run_time=0.3)

        for i in range(10):
            new_x = i + 1
            new_y = profit[i + 1]
            new_line = DashedLine(
                axes.c2p(new_x, -8), axes.c2p(new_x, 8),
                color=C_YELLOW, stroke_width=2, dash_length=0.08,
            )
            flash = plus_one if steps[i] == 1 else minus_one
            self.play(
                Transform(tracker_line, new_line),
                tracker_dot.animate.move_to(axes.c2p(new_x, new_y)),
                FadeIn(flash),
                run_time=STEP_TIME,
            )
            self.play(FadeOut(flash), run_time=STEP_TIME * 0.5)

        self.play(FadeOut(tracker_line), FadeOut(tracker_dot), run_time=0.4)
        self.wait(0.3)

        # ── Expectation chain — bottom right ──
        exp1 = MathTex(
            r"\mathbb{E}[X_{n+1} \mid \text{past}] = X_n",
            font_size=FONT_SIZE,
        )
        exp1.next_to(dist_lbl, DOWN, buff=0.5)

        exp2 = MathTex(
            r"\mathbb{E}[X_n \mid \text{past}] = X_{n-1}",
            font_size=FONT_SIZE,
        )
        exp2.next_to(exp1, DOWN, buff=0.3)

        vdots = MathTex(r"\vdots", font_size=FONT_SIZE)
        vdots.next_to(exp2, DOWN, buff=0.2)

        self.play(FadeIn(exp1, shift=UP * 0.1), run_time=0.5); self.wait(7)
        self.play(FadeIn(exp2, shift=UP * 0.1), run_time=0.5); self.wait(0.4)
        self.play(FadeIn(vdots),                run_time=0.4); self.wait(0.3)

        # ── OST ──
        therefore = MathTex(r"\therefore", font_size=FONT_SIZE, color=C_YELLOW)
        arrow     = Arrow(ORIGIN, RIGHT * 0.7, color=C_YELLOW, buff=0)
        ost       = MathTex(r"\mathbb{E}[M_T] = \mathbb{E}[M_0]",
                            font_size=FONT_SIZE + 4)
        ost_row   = VGroup(therefore, arrow, ost)
        ost_row.arrange(RIGHT, buff=0.2)
        ost_row.next_to(vdots, DOWN, buff=0.3)

        box = SurroundingRectangle(ost, color=C_YELLOW, buff=0.2, corner_radius=0.1)

        self.play(FadeIn(therefore))
        self.play(GrowArrow(arrow))
        self.play(FadeIn(ost, scale=0.8))
        self.play(Create(box))
        self.wait(1.0)
        # ── Annotate T in OST ──
        t_annotation = Text("where T is the stopping time", font_size=22, color=C_GREEN)
        t_annotation.next_to(ost_row, DOWN, buff=0.5)
        t_arrow = Arrow(
            t_annotation.get_top(),
            ost[0][3].get_bottom(),   # index into the T glyph in E[M_T]
            color=C_GREEN, buff=0.1, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(FadeIn(t_annotation), GrowArrow(t_arrow), run_time=0.5)
        self.wait(2.0)
        
        # ── Quote ──
        quote = Text(
            "On average, nothing can be gained by playing a fair game.",
            font_size=24, color=C_GREY,
        )
        quote.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(quote, shift=UP * 0.15), run_time=0.6)
        self.wait(HOLD_TIME)

# ═══════════════════════════════════════════════════════════════
# SECTION 4 — THE DRUNK MAN
# ═══════════════════════════════════════════════════════════════

class S4_NumberLine(Scene):
    """
    SCRIPT CUE: [Number line → balance equation built visually →
    rearranged → boundary conditions explained.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        LINE_WIDTH  = 10.0
        DOT_RADIUS  = 0.12
        LABEL_FS    = 26
        EQ_FS       = 32
        SMALL_FS    = 22
        HOLD_TIME   = 3.0
        ARR_COLOUR  = "#E8A87C"
        TEXT_COLOUR = "#C47A3A"
        BANNER_FS   = 64
        # ───────────────────────────────────────────────────

        def p2x(p): return (p / 100) * LINE_WIDTH - LINE_WIDTH / 2
        LINE_Y = -0.8

        # ── Title ──
        title = Text("Random Walk Example", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=BLACK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))

        # ── Problem statement ──
        problem = Text(
            '"A drunk man is at the 17th metre of a 100-metre walk to Bridge.\nEach second he staggers one metre forward or backward, equally likely."',
            font_size=24, color=C_DARK, line_spacing=1.4,
        )
        problem.next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(problem), run_time=0.7)
        self.wait(0.8)

        # ── Number line ──
        line     = Line([p2x(0), LINE_Y, 0], [p2x(100), LINE_Y, 0], color=C_DARK, stroke_width=3)
        tick_0   = Line([p2x(0),   LINE_Y-0.2, 0], [p2x(0),   LINE_Y+0.2, 0], color=C_DARK, stroke_width=2)
        tick_100 = Line([p2x(100), LINE_Y-0.2, 0], [p2x(100), LINE_Y+0.2, 0], color=C_DARK, stroke_width=2)
        lbl_0    = Text("0\nHome",            font_size=LABEL_FS, color=C_DARK)
        lbl_100  = Text("100\nBridge (club)", font_size=LABEL_FS, color=C_GREEN)
        lbl_0.next_to(  [p2x(0),   LINE_Y-0.2, 0], DOWN, buff=0.15)
        lbl_100.next_to([p2x(100), LINE_Y-0.2, 0], DOWN, buff=0.15)

        dot = Dot(point=[p2x(17), LINE_Y, 0], radius=DOT_RADIUS, color=C_YELLOW)
        here_arrow = Arrow(
            start=[p2x(17), LINE_Y+1.0, 0],
            end=  [p2x(17), LINE_Y+0.18, 0],
            color=C_YELLOW, buff=0, stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )
        here_lbl = Text("I am here", font_size=22, color=C_YELLOW)
        here_lbl.next_to(here_arrow, UP, buff=0.1)

        self.play(Create(line), Create(tick_0), Create(tick_100))
        self.play(FadeIn(lbl_0), FadeIn(lbl_100))
        self.play(FadeIn(dot))
        self.play(GrowArrow(here_arrow))
        self.play(FadeIn(here_lbl, shift=DOWN * 0.1))

        question = Text(
            "What is the probability he reaches Bridge before stumbling home?",
            font_size=24, color=C_GREY,
        )
        question.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.6)
        self.wait(HOLD_TIME)

        # ── Clear everything except the number line elements ──
        self.play(
            FadeOut(problem), FadeOut(question),
            FadeOut(here_arrow), FadeOut(here_lbl),
            FadeOut(title), FadeOut(underline),
            run_time=0.5,
        )

        # Move number line to top
        nl_group = VGroup(line, tick_0, tick_100, lbl_0, lbl_100, dot)
        self.play(nl_group.animate.shift(UP * 2.8), run_time=0.7)
        self.wait(0.3)

        # ── New title ──
        title2 = Text("The Harder Way", font_size=36, color=C_RED, weight=BOLD)
        title2.to_edge(UP, buff=0.3)
        underline2 = Line(
            title2.get_corner(DL) + DOWN * 0.08,
            title2.get_corner(DR) + DOWN * 0.08,
            color=C_RED, stroke_width=2,
        )
        self.play(FadeIn(title2), Create(underline2))
        self.wait(4)

        # ── Balance equation — split into parts for reliable highlighting ──
        eq_lhs   = MathTex(r"P(x)",               font_size=EQ_FS)
        eq_eq    = MathTex(r"=",                   font_size=EQ_FS)
        eq_right = MathTex(r"\tfrac{1}{2}P(x+1)", font_size=EQ_FS)
        eq_plus  = MathTex(r"+",                   font_size=EQ_FS)
        eq_left  = MathTex(r"\tfrac{1}{2}P(x-1)", font_size=EQ_FS)

        eq_balance = VGroup(eq_lhs, eq_eq, eq_right, eq_plus, eq_left)
        eq_balance.arrange(RIGHT, buff=0.2)
        eq_balance.move_to(ORIGIN + UP * 0.5)
        self.play(FadeIn(eq_balance), run_time=0.6)
        # Highlight P(x) — the thing we're solving for
        px_box = SurroundingRectangle(eq_lhs, color=C_YELLOW, buff=0.06, corner_radius=0.05)
        px_txt = Text(
            "chance he reaches\nBridge before home",
            font_size=SMALL_FS, color=C_YELLOW, line_spacing=1.2,
        )
        
        px_txt.next_to(eq_balance, DOWN, buff=0.5)
        px_arr = Arrow(
            px_txt.get_top(), px_box.get_bottom(),
            color=C_YELLOW, buff=0.08, stroke_width=1.8,
            max_tip_length_to_length_ratio=0.1, tip_length=0.12,
        )
        self.play(Create(px_box), GrowArrow(px_arr), FadeIn(px_txt), run_time=0.5)
        self.wait(3.0)
        self.play(FadeOut(px_box), FadeOut(px_arr), FadeOut(px_txt), run_time=0.4)
        self.wait(0.2)
        self.wait(0.4)

        # Highlight right-step term
        right_box = SurroundingRectangle(eq_right, color=C_BLUE, buff=0.06, corner_radius=0.05)
        right_txt = Text(
            "man steps right\nfrom position x",
            font_size=SMALL_FS, color=C_BLUE, line_spacing=1.2,
        )
        right_txt.next_to(eq_balance, DOWN, buff=0.5).shift(LEFT * 1.5)
        right_arr = Arrow(
            right_txt.get_top(), right_box.get_bottom(),
            color=C_BLUE, buff=0.08, stroke_width=1.8,
            max_tip_length_to_length_ratio=0.1, tip_length=0.12,
        )

        # Dot moves right 15 steps
        dot_start = dot.get_center()
        dot_right = [p2x(17 + 15) + (dot_start[0] - p2x(17)), dot_start[1], 0]

        self.play(Create(right_box), GrowArrow(right_arr), FadeIn(right_txt),
                  dot.animate.move_to(dot_right), run_time=0.7)
        self.wait(3.0)
        self.play(FadeOut(right_box), FadeOut(right_arr), FadeOut(right_txt),
                  dot.animate.move_to(dot_start), run_time=0.5)

        # Highlight left-step term
        left_box = SurroundingRectangle(eq_left, color=C_RED, buff=0.06, corner_radius=0.05)
        left_txt = Text(
            "man steps left\nfrom position x",
            font_size=SMALL_FS, color=C_RED, line_spacing=1.2,
        )
        left_txt.next_to(eq_balance, DOWN, buff=0.5).shift(RIGHT * 1.5)
        left_arr = Arrow(
            left_txt.get_top(), left_box.get_bottom(),
            color=C_RED, buff=0.08, stroke_width=1.8,
            max_tip_length_to_length_ratio=0.1, tip_length=0.12,
        )

        # Dot moves left 15 steps
        dot_left = [p2x(17 - 15) + (dot_start[0] - p2x(17)), dot_start[1], 0]

        self.play(Create(left_box), GrowArrow(left_arr), FadeIn(left_txt),
                  dot.animate.move_to(dot_left), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(left_box), FadeOut(left_arr), FadeOut(left_txt),
                  dot.animate.move_to(dot_start), run_time=0.5)
        self.wait(3.0)

        # ── Rearrange live in place ──
        eq_recursion = MathTex(
            r"P(x+1) - 2P(x) + P(x-1) = 0",
            font_size=EQ_FS,
        )
        eq_recursion.move_to(eq_balance.get_center())

        self.play(TransformMatchingShapes(eq_balance, eq_recursion), run_time=0.8)
        self.wait(0.3)

        # Annotation appears below, then disappears
        rec_lbl = Text("second order recursion", font_size=22, color=TEXT_COLOUR, font="Georgia")
        rec_lbl.next_to(eq_recursion, DOWN, buff=0.4)
        self.play(FadeIn(rec_lbl, shift=UP * 0.1), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(rec_lbl), run_time=0.4)
        self.wait(0.3)

        # ── Boundary conditions ──
        bc1 = MathTex(r"P(0) = 0", font_size=EQ_FS)
        bc2 = MathTex(r"P(100) = 1", font_size=EQ_FS)
        bcs = VGroup(bc1, bc2)
        bcs.arrange(RIGHT, buff=1.2)
        bcs.next_to(eq_recursion, DOWN, buff=0.6)

        self.play(FadeIn(bcs), run_time=0.5)
        self.wait(0.3)

        # BC1 explanation — home absorbing
        bc1_box = SurroundingRectangle(bc1, color=C_DARK, buff=0.1, corner_radius=0.06)
        bc1_txt = Text("Welcome home, son", font_size=SMALL_FS,
                       color=C_DARK, line_spacing=1.2)
        bc1_txt.next_to(bc1, DOWN, buff=0.35)
        bc1_arr = Arrow(bc1_txt.get_top(), bc1_box.get_bottom(),
                        color=C_DARK, buff=0.06, stroke_width=1.5,
                        max_tip_length_to_length_ratio=0.1, tip_length=0.1)

        # BC2 explanation — bridge absorbing
        bc2_box = SurroundingRectangle(bc2, color=C_GREEN, buff=0.1, corner_radius=0.06)
        bc2_txt = Text("Made it to bridge", font_size=SMALL_FS,
                       color=C_GREEN, line_spacing=1.2)
        bc2_txt.next_to(bc2, DOWN, buff=1.1)
        bc2_arr = Arrow(bc2_txt.get_top(), bc2_box.get_bottom(),
                        color=C_GREEN, buff=0.06, stroke_width=1.5,
                        max_tip_length_to_length_ratio=0.1, tip_length=0.1)

        self.play(
            Create(bc1_box), GrowArrow(bc1_arr), FadeIn(bc1_txt),
            Create(bc2_box), GrowArrow(bc2_arr), FadeIn(bc2_txt),
            run_time=0.6,
        )
        self.wait(1.5)

        # ── Caption ──
        caption = Text(
            "Solving a second-order recursion with boundary conditions isn't straightforward.",
            font_size=22, color=C_GREY,
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)

        self.wait(HOLD_TIME)


class S4_MartingaleWayPanel(Scene):
    """
    SCRIPT CUE: [Number line. X_T piecewise with dot animations.
    OST invoked. Equations morph. Boxed answer.]
    """
    def construct(self):
        self.camera.background_color = BG
        # ── tuneable constants ──────────────────────────────
        TITLE_FS   = 36
        EQ_FS      = 32
        SMALL_FS   = 21
        LINE_PAUSE = 2.5
        HOLD_TIME  = 3.0
        # ───────────────────────────────────────────────────

        def pos_to_x(p): return (p / 100) * 8.0 - 4.0
        LINE_Y = 2.0

        # ── Title ──
        title = Text("The Easier Way (using Martingales)",
                     font_size=TITLE_FS, color=C_GREEN, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=C_GREEN, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))

        # ── Number line ──
        line     = Line([pos_to_x(0), LINE_Y, 0], [pos_to_x(100), LINE_Y, 0],
                        color=C_DARK, stroke_width=2)
        tick_0   = Line([pos_to_x(0),   LINE_Y-0.15, 0], [pos_to_x(0),   LINE_Y+0.15, 0],
                        color=C_DARK, stroke_width=2)
        tick_100 = Line([pos_to_x(100), LINE_Y-0.15, 0], [pos_to_x(100), LINE_Y+0.15, 0],
                        color=C_DARK, stroke_width=2)
        lbl_0   = Text("0\nHome",     font_size=18, color=C_DARK)
        lbl_100 = Text("100\nBridge", font_size=18, color=C_GREEN)
        lbl_0.next_to(  [pos_to_x(0),   LINE_Y-0.15, 0], DOWN, buff=0.1)
        lbl_100.next_to([pos_to_x(100), LINE_Y-0.15, 0], DOWN, buff=0.1)

        dot = Dot([pos_to_x(17), LINE_Y, 0], radius=0.13, color=C_YELLOW)
        lbl_17 = Text("17", font_size=18, color=C_YELLOW)
        lbl_17.next_to(dot, UP, buff=0.12)

        self.play(Create(line), Create(tick_0), Create(tick_100),
                  FadeIn(lbl_0), FadeIn(lbl_100))
        self.play(FadeIn(dot), FadeIn(lbl_17))
        self.wait(0.5)

        # ── X_T intro line ──
        xt_intro = MathTex(r"X_T \ \sim \ \text{where I end up}",
                           font_size=EQ_FS)
        xt_intro.next_to(line, DOWN, buff=0.5)
        self.play(FadeIn(xt_intro, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)

        # ── Piecewise definition ──
        brace    = MathTex(r"\left\{", font_size=EQ_FS * 2.5)
        pw1_val  = MathTex(r"100", font_size=EQ_FS, color=C_GREEN)
        pw1_prob = MathTex(r"\text{with probability } p", font_size=EQ_FS, color=C_GREEN)
        pw2_val  = MathTex(r"0",   font_size=EQ_FS, color=C_RED)
        pw2_prob = MathTex(r"\text{with probability } (1-p)", font_size=EQ_FS, color=C_RED)

        pw1_row = VGroup(pw1_val, pw1_prob)
        pw1_row.arrange(RIGHT, buff=0.4)
        pw2_row = VGroup(pw2_val, pw2_prob)
        pw2_row.arrange(RIGHT, buff=0.4)
        pw2_val.align_to(pw1_val, LEFT)
        pw2_prob.align_to(pw1_prob, LEFT)

        rows = VGroup(pw1_row, pw2_row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        brace.next_to(rows, LEFT, buff=0.15)
        xt_label = MathTex(r"X_T =", font_size=EQ_FS)
        xt_label.next_to(brace, LEFT, buff=0.2)

        piecewise = VGroup(xt_label, brace, rows)
        piecewise.next_to(xt_intro, DOWN, buff=0.4)

        self.play(FadeIn(xt_label), FadeIn(brace), run_time=0.4)
        self.wait(0.2)

        # Animate 100 then p — dot travels to bridge
        self.play(FadeIn(pw1_val), run_time=0.4)
        self.play(dot.animate.move_to([pos_to_x(100), LINE_Y, 0]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(pw1_prob), run_time=0.4)
        self.wait(LINE_PAUSE)
        self.play(dot.animate.move_to([pos_to_x(17), LINE_Y, 0]), run_time=0.4)

        # Animate 0 then (1-p) — dot travels home
        self.play(FadeIn(pw2_val), run_time=0.4)
        self.play(dot.animate.move_to([pos_to_x(0), LINE_Y, 0]), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(pw2_prob), run_time=0.4)
        self.wait(LINE_PAUSE)
        self.play(dot.animate.move_to([pos_to_x(17), LINE_Y, 0]), run_time=0.4)
        self.wait(0.5)

        # ── OST invocation — split so we can circle X_0 ──
        ost_lbl = Text("Optional Stopping Theorem:",
                       font_size=24, color=C_YELLOW, weight=BOLD)
        ost_lhs     = MathTex(r"\mathbb{E}[X_T]",  font_size=EQ_FS, color=C_YELLOW)
        ost_rhs_eq  = MathTex(r"=",                 font_size=EQ_FS, color=C_YELLOW)
        ost_rhs_x0  = MathTex(r"\mathbb{E}[X_0]",  font_size=EQ_FS, color=C_YELLOW)
        ost_eq_split = VGroup(ost_lhs, ost_rhs_eq, ost_rhs_x0)
        ost_eq_split.arrange(RIGHT, buff=0.15)
        
        ost_group = VGroup(ost_lbl, ost_eq_split)
        ost_group.arrange(RIGHT, buff=0.3)
        ost_group.next_to(piecewise, DOWN, buff=0.45)

        self.play(FadeIn(ost_lbl), FadeIn(ost_lhs), FadeIn(ost_rhs_eq), FadeIn(ost_rhs_x0), run_time=0.5)
        self.wait(3)

        # Circle E[X_0] — the RHS
        x0_box = SurroundingRectangle(ost_rhs_x0, color=C_BLUE, buff=0.06, corner_radius=0.05)
        x0_txt = Text("our starting point: 17", font_size=SMALL_FS, color=C_BLUE)
        x0_txt.next_to(ost_group, RIGHT, buff=0.3)
        x0_arr = Arrow(x0_txt.get_left(), x0_box.get_right(),
                       color=C_BLUE, buff=0.05, stroke_width=1.8,
                       max_tip_length_to_length_ratio=0.1, tip_length=0.1)
        self.play(Create(x0_box), GrowArrow(x0_arr), FadeIn(x0_txt), run_time=0.4)
        self.wait(LINE_PAUSE)
        self.play(FadeOut(x0_box), FadeOut(x0_arr), FadeOut(x0_txt), run_time=0.3)

        # ── Equation chain — all morphing in place ──
        eq1 = MathTex(r"\mathbb{E}[X_T] = 17", font_size=EQ_FS)
        eq1.next_to(ost_group, DOWN, buff=0.4)
        self.play(FadeIn(eq1), run_time=0.4)
        self.wait(0.8)

        # Intermediate: expand E[X_T] using piecewise
        eq1b = MathTex(r"\mathbb{E}[X_T] = 100 \cdot p + 0 \cdot (1-p)",
                       font_size=EQ_FS)
        eq1b.move_to(eq1.get_center())
        self.play(TransformMatchingShapes(eq1, eq1b), run_time=0.8)
        self.wait(0.5)

        # Set equal to 17
        eq2_lhs  = MathTex(r"100 \cdot p", font_size=EQ_FS)
        eq2_zero = MathTex(r"+ 0 \cdot (1-p)", font_size=EQ_FS)
        eq2_rhs  = MathTex(r"= 17", font_size=EQ_FS)
        eq2_group = VGroup(eq2_lhs, eq2_zero, eq2_rhs)
        eq2_group.arrange(RIGHT, buff=0.2)
        eq2_group.move_to(eq1b.get_center())
        self.play(TransformMatchingShapes(eq1b, eq2_group), run_time=0.7)
        self.wait(0.3)

        # Circle the zero term
        zero_box = SurroundingRectangle(eq2_zero, color=C_GREY, buff=0.06, corner_radius=0.05)
        zero_txt = Text("this term vanishes", font_size=SMALL_FS, color=C_GREY)
        zero_txt.next_to(eq2_group, DOWN, buff=0.3)
        zero_arr = Arrow(zero_txt.get_top(), eq2_zero.get_bottom(),
                         color=C_GREY, buff=0.05, stroke_width=1.8,
                         max_tip_length_to_length_ratio=0.1, tip_length=0.1)
        self.play(Create(zero_box), GrowArrow(zero_arr), FadeIn(zero_txt), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(zero_box), FadeOut(zero_arr), FadeOut(zero_txt), run_time=0.3)

        # Drop the zero term
        eq3 = MathTex(r"100p = 17", font_size=EQ_FS)
        eq3.move_to(eq2_group.get_center())
        self.play(TransformMatchingShapes(eq2_group, eq3), run_time=0.7)
        self.wait(0.5)
        
        # Final answer on line below with implies
        implies = MathTex(r"\Rightarrow", font_size=EQ_FS, color=C_GREEN)
        eq4     = MathTex(r"p = 0.17", font_size=EQ_FS + 6, color=C_GREEN)
        final_row = VGroup(implies, eq4)
        final_row.arrange(RIGHT, buff=0.3)
        final_row.next_to(eq3, DOWN, buff=0.35)

        box = SurroundingRectangle(eq4, color=C_GREEN, buff=0.2, corner_radius=0.1)
        self.play(FadeIn(implies), FadeIn(eq4), run_time=0.5)
        self.play(Create(box), run_time=0.5)
        self.wait(HOLD_TIME)

# ═══════════════════════════════════════════════════════════════
# SECTION 5 — X² − n  IS A MARTINGALE
# ═══════════════════════════════════════════════════════════════

class S5_SpreadGrowth(Scene):
    """
    SCRIPT CUE: [Walks fan out. Mean line. Spread envelope. Question about
    E[X_n^2]. Graph shrinks left. Right panel builds the martingale engineering.]
    """
    def construct(self):
        self.camera.background_color = BG
        N_WALKS      = 12
        N_STEPS      = 60
        SEED         = 99
        AXIS_X_RANGE = [0, 62, 10]
        AXIS_Y_RANGE = [-14, 14, 4]
        AXIS_X_LEN   = 10.0
        AXIS_Y_LEN   = 5.5
        HOLD_TIME    = 1.25
        WALK_OPACITY = 0.35
        EQ_FS        = 30
        SMALL_FS     = 22
        STEP_PAUSE   = 1.5

        axes = Axes(
            x_range=AXIS_X_RANGE, y_range=AXIS_Y_RANGE,
            x_length=AXIS_X_LEN,  y_length=AXIS_Y_LEN,
            axis_config={
                "color": BLACK,
                "include_tip": False,
                "include_numbers": False,
            },
        ).move_to(ORIGIN)

        x_labels = VGroup()
        for val in range(0, 63, 10):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(axes.c2p(val, 0), DOWN, buff=0.15)
            x_labels.add(lbl)

        y_labels = VGroup()
        for val in range(-12, 13, 4):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(axes.c2p(0, val), LEFT, buff=0.15)
            y_labels.add(lbl)

        x_label = Text("Round number", font_size=22)
        x_label.next_to(axes, DOWN, buff=0.55)

        y_label = Text("Cumulative profit £", font_size=22)
        y_label.rotate(PI / 2)
        y_label.next_to(axes, LEFT, buff=0.65)

        title = Text("Recall:", font_size=28, color=C_DARK)
        title.next_to(axes, UP, buff=0.25)

        self.play(
            Create(axes),
            FadeIn(title),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(x_labels),
            FadeIn(y_labels),
        )

        walks   = random_walk_ensemble(N_WALKS, N_STEPS, seed=SEED)
        colours = color_gradient([C_BLUE, "#E91E63", "#4CAF50", "#FF9800"], N_WALKS)
        walk_group = VGroup()
        for i in range(N_WALKS):
            profit = walks[i]
            path  = VMobject(stroke_color=colours[i], stroke_width=1.8, fill_opacity=0)
            path.set_points_as_corners(
                [axes.c2p(x, y) for x, y in enumerate(profit)]
            )
            path.set_opacity(WALK_OPACITY)
            walk_group.add(path)

        self.play(FadeIn(walk_group), run_time=0.5)

        mean_line = axes.plot(lambda x: 0, x_range=[0, 60],
                              color=C_RED, stroke_width=2.5)
        mean_line = DashedVMobject(mean_line, num_dashes=30)
        mean_lbl  = MathTex(r"\mathbb{E}[X_n] = 0", font_size=28, color=C_RED)
        mean_lbl.next_to(axes.c2p(60, 0), RIGHT, buff=0.5)
        self.play(Create(mean_line), FadeIn(mean_lbl), run_time=0.5)
        self.wait(1.0)

        sq_pos = DashedVMobject(
            axes.plot(lambda x: np.sqrt(max(x, 0.001)),
                      x_range=[0.1, 60], color=C_DARK, stroke_width=2.5),
            num_dashes=30,
        )
        sq_neg = DashedVMobject(
            axes.plot(lambda x: -np.sqrt(max(x, 0.001)),
                      x_range=[0.1, 60], color=C_DARK, stroke_width=2.5),
            num_dashes=30,
        )
        self.play(Create(sq_pos), Create(sq_neg), run_time=0.75)

        spread_lbl = MathTex(r"\text{spread} \sim \sqrt{n}",
                             font_size=30, color=C_DARK)
        spread_lbl.next_to(axes.c2p(60, np.sqrt(60)), RIGHT, buff=0.1)
        self.play(FadeIn(spread_lbl), run_time=0.5)
        self.wait(HOLD_TIME)

        # ── Question fades in, then we shrink graph left ──
        question = MathTex(r"\text{What about } \mathbb{E}[X_n^2]\text{?}",
                           font_size=34, color=C_DARK)
        question.to_corner(DR, buff=0.4)
        self.play(FadeIn(question, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)

        # Bundle everything graph-related
        graph_group = VGroup(
            axes, walk_group, mean_line, mean_lbl,
            sq_pos, sq_neg, spread_lbl,
            x_labels, y_labels, x_label, y_label, title,
        )

        self.play(
            FadeOut(question),
            graph_group.animate.scale(0.55).to_edge(LEFT, buff=0.3),
            run_time=0.8,
        )

        panel_title = Text("Constructing a martingale:", font_size=28, color=C_DARK, weight=BOLD)
        panel_title.to_corner(UR, buff=0.4)
        self.play(FadeIn(panel_title)); self.wait(0.3)

        # ── Right panel ──
        # Arrow pointing at spread envelope on the graph
        envelope_point = axes.c2p(50, np.sqrt(50))  # after scale this is approximate
        # We'll anchor arrows to text instead since scale shifts c2p

        beat1 = MathTex(r"X_n \text{ is a martingale}", font_size=EQ_FS, color=C_GREEN)
        beat1.move_to(RIGHT * 2.5 + UP * 2.5)
        self.play(FadeIn(beat1, shift=UP * 0.1)); self.wait(10)

        beat2_a = MathTex(r"X_n^2 \text{ is not}", font_size=EQ_FS, color=C_RED)
        beat2_b = Text("— it drifts up by 1 each step", font_size=SMALL_FS, color=C_RED)
        beat2 = VGroup(beat2_a, beat2_b)
        beat2.arrange(RIGHT, buff=0.2)
        beat2.next_to(beat1, DOWN, buff=0.45)
        beat2.set_x(2.5)

        # Arrow from text pointing left toward the fanning walks
        # Arrow pointing down-left toward the spread envelope on the graph
        spread_arr = Arrow(
            beat2_a.get_bottom() + DOWN * 0.05,
            beat2_a.get_bottom() + DOWN * 0.05 + LEFT * 0.8 + DOWN * 0.8,
            color=C_RED, buff=0.05, stroke_width=1.8,
            max_tip_length_to_length_ratio=0.1, tip_length=0.12,
        )
        self.play(FadeIn(beat2_a), GrowArrow(spread_arr), run_time=0.4)

        # Flash the envelope gold
        self.play(
            sq_pos.animate.set_color(C_YELLOW),
            sq_neg.animate.set_color(C_YELLOW),
            run_time=0.3,
        )
        self.play(
            sq_pos.animate.set_color(C_DARK),
            sq_neg.animate.set_color(C_DARK),
            run_time=0.3,
        )
        self.play(FadeIn(beat2_b)); self.wait(STEP_PAUSE)

        beat3 = Text("so subtract the drift:", font_size=SMALL_FS, color=C_GREY)
        beat3.next_to(beat2, DOWN, buff=0.45)
        beat3.set_x(beat2.get_x())
        self.play(FadeIn(beat3, shift=UP * 0.1)); self.wait(0.6)

        defn = MathTex(r"M_n = X_n^2 - n", font_size=EQ_FS + 6)
        defn.next_to(beat3, DOWN, buff=0.35)
        defn.set_x(beat3.get_x())
        box = SurroundingRectangle(defn, color=C_YELLOW, buff=0.2, corner_radius=0.1)
        self.play(FadeIn(defn, scale=0.85)); self.wait(0.3)
        self.play(Create(box)); self.wait(5)

        concl = MathTex(r"M_n \text{ is also a martingale}",
                        font_size=EQ_FS, color=C_YELLOW)
        concl.next_to(box, DOWN, buff=0.4)
        concl.set_x(defn.get_x())
        self.play(FadeIn(concl, scale=0.9), run_time=0.5)
        self.play(box.animate.set_stroke(color=C_GREEN, width=4), run_time=0.3)
        self.play(box.animate.set_stroke(color=C_YELLOW, width=2), run_time=0.3)
        self.wait(2.5)
# ═══════════════════════════════════════════════════════════════
# SECTION 6 — EXPECTED CROSSING TIME
# ═══════════════════════════════════════════════════════════════
class S6_ExpectedTimeDerivation(Scene):
    """
    SCRIPT CUE: [Number line, man wanders, question. Fade. Walk simulation
    hits barrier. Piecewise X_T^2. Morph to E[T].]
    """
    def construct(self):
        self.camera.background_color = BG
        EQ_FS      = 32
        SMALL_FS   = 22
        STEP_PAUSE = 3
        HOLD_TIME  = 2.5

        def p2x(p): return (p / 100) * 10.0 - 5.0
        LINE_Y = 0.0

        # ── Title ──
        title = Text("Expected crossing time using  ", font_size=30, color=C_DARK, weight=BOLD)
        title_eq = MathTex(r"X_n^2 - n", font_size=30, color=C_YELLOW)
        title_row = VGroup(title, title_eq)
        title_row.arrange(RIGHT, buff=0.1)
        title_row.to_edge(UP, buff=0.3)
        underline = Line(
            title_row.get_corner(DL) + DOWN * 0.08,
            title_row.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        self.play(FadeIn(title_row), Create(underline))

        # ── Number line ──
        nl_line   = Line([p2x(0), LINE_Y, 0], [p2x(100), LINE_Y, 0],
                         color=C_DARK, stroke_width=3)
        tick_0    = Line([p2x(0),   LINE_Y-0.2, 0], [p2x(0),   LINE_Y+0.2, 0],
                         color=C_DARK, stroke_width=2)
        tick_100  = Line([p2x(100), LINE_Y-0.2, 0], [p2x(100), LINE_Y+0.2, 0],
                         color=C_DARK, stroke_width=2)
        lbl_0     = Text("0\nHome",   font_size=22, color=C_DARK)
        lbl_100   = Text("100\nBridge", font_size=22, color=C_GREEN)
        lbl_0.next_to(  [p2x(0),   LINE_Y-0.2, 0], DOWN, buff=0.15)
        lbl_100.next_to([p2x(100), LINE_Y-0.2, 0], DOWN, buff=0.15)
        dot = Dot([p2x(17), LINE_Y, 0], radius=0.13, color=C_YELLOW)
        lbl_17 = Text("17m", font_size=20, color=C_YELLOW)
        lbl_17.next_to(dot, UP, buff=0.15)

        self.play(Create(nl_line), Create(tick_0), Create(tick_100),
                  FadeIn(lbl_0), FadeIn(lbl_100))
        self.play(FadeIn(dot), FadeIn(lbl_17))
        self.wait(0.5)

        # Dot wanders left and right a few times
        wander = [19, 15, 18, 14, 19, 15, 20, 16]
        for pos in wander:
            self.play(dot.animate.move_to([p2x(pos), LINE_Y, 0]),
                      run_time=0.25)
        self.play(dot.animate.move_to([p2x(17), LINE_Y, 0]), run_time=0.3)
        self.wait(0.3)

        question = Text("How long will it take him to stop wandering?",
                        font_size=26, color=C_GREY)
        question.next_to(nl_line, DOWN, buff=1.0)
        self.play(FadeIn(question, shift=UP * 0.1))
        self.wait(5.0)

        self.play(FadeOut(VGroup(
            title_row, underline, nl_line, tick_0, tick_100,
            lbl_0, lbl_100, dot, lbl_17, question,
        )))
        self.wait(0.3)

        # ── Title reappears ──
        title2 = Text("Expected crossing time using  ", font_size=30, color=C_DARK, weight=BOLD)
        title2_eq = MathTex(r"X_n^2 - n", font_size=30, color=C_YELLOW)
        title2_row = VGroup(title2, title2_eq)
        title2_row.arrange(RIGHT, buff=0.1)
        title2_row.to_edge(UP, buff=0.3)
        underline2 = Line(
            title2_row.get_corner(DL) + DOWN * 0.08,
            title2_row.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        self.play(FadeIn(title2_row), Create(underline2))

        # ── Walk simulation on left ──
        SEED      = 42
        walk      = simple_random_walk(3000, start=17, seed=SEED)
        T_stop    = first_exit_index(walk, lower=0, upper=100)
        walk_plot = walk[:T_stop + 1]
        n_plot    = len(walk_plot)

        ax = Axes(
            x_range=[0, n_plot + 2, max(1, n_plot // 5)],
            y_range=[-5, 110, 20],
            x_length=5.5,
            y_length=5.0,
            axis_config={"color": BLACK, "include_tip": False, "include_numbers": False},
        )
        ax.to_edge(LEFT, buff=1.2).shift(DOWN * 0.3)

        # Axis labels
        x_lbl = Text("step n", font_size=18, color=C_DARK)
        x_lbl.next_to(ax, DOWN, buff=0.4)
        y_lbl = Text("position", font_size=18, color=C_DARK)
        y_lbl.rotate(PI / 2)
        y_lbl.next_to(ax, LEFT, buff=0.4)

        # Barrier lines
        home_line   = ax.plot(lambda x: 0,   x_range=[0, n_plot], color=C_RED,   stroke_width=2)
        bridge_line = ax.plot(lambda x: 100, x_range=[0, n_plot], color=C_GREEN, stroke_width=2)
        home_lbl    = Text("Home (0)",    font_size=16, color=C_RED)
        bridge_lbl  = Text("Bridge (100)", font_size=16, color=C_GREEN)
        home_lbl.next_to(ax.c2p(0, 0),   RIGHT, buff=0.1).shift(DOWN * 0.25)
        bridge_lbl.next_to(ax.c2p(0, 100), RIGHT, buff=0.1).shift(UP * 0.25)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(home_line), Create(bridge_line),
                  FadeIn(home_lbl), FadeIn(bridge_lbl))

        # Draw walk in chunks for performance
        FAST = 3.0 / n_plot
        CHUNK_SIZE = 50
        sim_dot = Dot(ax.c2p(0, walk_plot[0]), radius=0.08, color=C_YELLOW)
        self.add(sim_dot)

        path_so_far = VMobject(stroke_color=C_BLUE, stroke_width=2, fill_opacity=0)
        path_so_far.set_points_as_corners([ax.c2p(0, walk_plot[0]),
                                           ax.c2p(1, walk_plot[1])])
        self.add(path_so_far)

        for chunk_start in range(0, n_plot - 1, CHUNK_SIZE):
            chunk_end = min(chunk_start + CHUNK_SIZE, n_plot - 1)
            new_path  = VMobject(stroke_color=C_BLUE, stroke_width=2, fill_opacity=0)
            new_path.set_points_as_corners(
                [ax.c2p(i, walk_plot[i]) for i in range(chunk_end + 1)]
            )
            self.remove(path_so_far)
            path_so_far = new_path
            self.add(path_so_far)
            sim_dot.move_to(ax.c2p(chunk_end, walk_plot[chunk_end]))
            self.wait(FAST * CHUNK_SIZE)
        # Flash stopping dot
        stop_dot = Dot(ax.c2p(T_stop, walk_plot[-1]), radius=0.14, color=C_RED)
        self.play(FadeIn(stop_dot, scale=1.5), run_time=0.4)

        T_label = MathTex(r"T = " + str(T_stop), font_size=26, color=C_RED)
        T_label.next_to(stop_dot, DOWN, buff=0.15)
        self.play(FadeIn(T_label))
        self.wait(4)

        # ── Right panel — algebra ──
        on_avg = Text("On average:", font_size=26, color=C_DARK, weight=BOLD)
        on_avg.move_to(RIGHT * 2.8 + UP * 2.3)
        self.play(FadeIn(on_avg, shift=UP * 0.1))
        self.wait(0.5)

        # OST on M_n
        ost = MathTex(r"\mathbb{E}[M_T] = \mathbb{E}[M_0]",
                      font_size=EQ_FS, color=C_YELLOW)
        ost.next_to(on_avg, DOWN, buff=0.35)
        ost.set_x(on_avg.get_x())
        self.play(FadeIn(ost)); self.wait(STEP_PAUSE)

        # Expand M_0
        m0a = MathTex(r"M_0 = X_0^2 - 0", font_size=EQ_FS)
        m0a.next_to(ost, DOWN, buff=0.35)
        m0a.set_x(on_avg.get_x())
        self.play(FadeIn(m0a)); self.wait(0.6)

        m0b = MathTex(r"M_0 = 17^2 - 0", font_size=EQ_FS)
        m0b.move_to(m0a.get_center())
        self.play(TransformMatchingShapes(m0a, m0b), run_time=0.6)
        self.wait(0.4)

        m0 = MathTex(r"M_0 = 289", font_size=EQ_FS)
        m0.move_to(m0b.get_center())
        self.play(TransformMatchingShapes(m0b, m0), run_time=0.6)
        self.wait(0.6)

        box_289 = SurroundingRectangle(m0, color=C_YELLOW, buff=0.1, corner_radius=0.08)
        self.play(Create(box_289)); self.wait(0.6)

        # Expand M_T
        mt = MathTex(r"\mathbb{E}[X_T^2 - T] = 289",
                     font_size=EQ_FS)
        mt.next_to(m0, DOWN, buff=0.35)
        mt.set_x(on_avg.get_x())
        self.play(FadeIn(mt)); self.wait(STEP_PAUSE)

        # Rearrange
        rearr = MathTex(r"\mathbb{E}[T] = \mathbb{E}[X_T^2] - 289",
                        font_size=EQ_FS)
        rearr.move_to(mt.get_center())
        self.play(TransformMatchingShapes(mt, rearr), run_time=0.7)
        self.wait(STEP_PAUSE)

        # ── Piecewise X_T^2 ──
        pw_lbl   = MathTex(r"X_T^2 =", font_size=EQ_FS)
        pw_brace = MathTex(r"\left\{", font_size=EQ_FS * 2.2)
        pw1_val  = MathTex(r"100^2 = 10000", font_size=EQ_FS, color=C_GREEN)
        pw1_prob = MathTex(r"\text{with } p=0.17", font_size=EQ_FS, color=C_GREEN)
        pw2_val  = MathTex(r"0^2 = 0",       font_size=EQ_FS, color=C_RED)
        pw2_prob = MathTex(r"\text{with } p=0.83", font_size=EQ_FS, color=C_RED)

        pw1_row = VGroup(pw1_val, pw1_prob)
        pw1_row.arrange(RIGHT, buff=0.35)
        pw2_row = VGroup(pw2_val, pw2_prob)
        pw2_row.arrange(RIGHT, buff=0.35)
        pw2_val.align_to(pw1_val, LEFT)
        pw2_prob.align_to(pw1_prob, LEFT)

        rows = VGroup(pw1_row, pw2_row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        pw_brace.next_to(rows, LEFT, buff=0.12)
        pw_lbl.next_to(pw_brace, LEFT, buff=0.15)

        piecewise = VGroup(pw_lbl, pw_brace, rows)
        piecewise.next_to(rearr, DOWN, buff=0.4)
        piecewise.set_x(on_avg.get_x())

        self.play(FadeIn(pw_lbl), FadeIn(pw_brace))
        self.wait(0.6)
        self.play(FadeIn(pw1_val), run_time=0.3)
        self.play(FadeIn(pw1_prob), run_time=0.3)
        self.wait(0.5)
        self.play(FadeIn(pw2_val), run_time=0.3)

        # Circle 0^2 — it vanishes
        zero_box = SurroundingRectangle(pw2_val, color=C_GREY, buff=0.06, corner_radius=0.05)
        zero_txt = Text("this is zero", font_size=SMALL_FS, color=C_GREY)
        zero_txt.next_to(pw2_val, DOWN, buff=0.2)
        zero_arr = Arrow(zero_txt.get_top(), zero_box.get_bottom(),
                         color=C_GREY, buff=0.05, stroke_width=1.5,
                         max_tip_length_to_length_ratio=0.1, tip_length=0.1)
        self.play(FadeIn(pw2_prob), run_time=0.3)
        self.play(Create(zero_box), GrowArrow(zero_arr), FadeIn(zero_txt), run_time=0.3)
        self.wait(STEP_PAUSE)
        self.play(FadeOut(zero_box), FadeOut(zero_arr), FadeOut(zero_txt), run_time=0.2)

        # ── Morph to E[X_T^2] = 1700 ──
        ext2 = MathTex(r"\mathbb{E}[X_T^2] = 10000 \times 0.17 = 1700",
                       font_size=EQ_FS)
        ext2.next_to(piecewise, DOWN, buff=0.35)
        ext2.set_x(on_avg.get_x())
        self.play(FadeIn(ext2)); self.wait(STEP_PAUSE)

        # ── Final answer morphs from rearr ──
        final = MathTex(r"\mathbb{E}[T] = 1700 - 289 = 1411",
                        font_size=EQ_FS + 4, color=C_GREEN)
        final.next_to(ext2, DOWN, buff=0.4)
        final.set_x(on_avg.get_x())
        final_box = SurroundingRectangle(final, color=C_GREEN, buff=0.2, corner_radius=0.1)

        self.play(FadeIn(final, shift=UP * 0.1))
        self.play(Create(final_box))
        self.wait(HOLD_TIME)


# ═══════════════════════════════════════════════════════════════
# SECTION 7 — BROWNIAN MOTION
# ═══════════════════════════════════════════════════════════════
class S7_RandomWalkToBrownian(Scene):
    """
    SCRIPT CUE: [Discrete walk animates. Redraws 4 times with finer steps
    until smooth. Graph shrinks right. Left panel: BM properties with
    ensemble of paths and confidence intervals.]
    """
    def construct(self):
        self.camera.background_color = BG
        STEPS_SEQUENCE = [15, 60, 250, 1200]
        SEED           = 17
        AXIS_X_LEN     = 10.0
        AXIS_Y_LEN     = 5.0
        ZOOM_TIME      = 0.7
        HOLD_TIME      = 2.5
        N_BM           = 40
        N_BM_STEPS     = 1200

        np.random.seed(SEED)

        def make_walk_path(n, colour, axes, stroke=2.5):
            profit = rescaled_random_walk(n, scale=4)   # continues the seeded stream
            xs    = np.linspace(0, 10, n + 1)
            path = VMobject(stroke_color=colour, stroke_width=stroke, fill_opacity=0)
            path.set_points_as_corners(
                [axes.c2p(x, y) for x, y in zip(xs, profit)]
            )
            return path

        # ── Title ──
        title = Text("From Random Walk to Brownian Motion",
                     font_size=30, color=C_DARK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))

        # ── Axes (full width initially) ──
        axes = Axes(
            x_range=[0, 10.5, 2], y_range=[-5, 5, 2],
            x_length=AXIS_X_LEN,  y_length=AXIS_Y_LEN,
            axis_config={"color": BLACK, "include_tip": False, "include_numbers": False},
        ).shift(DOWN * 0.3)

        x_labels = VGroup()
        for val in range(0, 11, 2):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(axes.c2p(val, 0), DOWN, buff=0.15)
            x_labels.add(lbl)

        x_lbl = Text("time", font_size=22, color=C_DARK)
        x_lbl.next_to(axes, DOWN, buff=0.5)
        y_lbl = Text("position", font_size=22, color=C_DARK)
        y_lbl.rotate(PI / 2)
        y_lbl.next_to(axes, LEFT, buff=0.5)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(x_labels))

        step_lbl = Text(f"{STEPS_SEQUENCE[0]} steps", font_size=24, color=C_BLUE)
        step_lbl.to_corner(UL, buff=0.5).shift(DOWN * 0.8)

        colours = [C_BLUE, "#9C27B0", C_GREEN, C_DARK]
        path = make_walk_path(STEPS_SEQUENCE[0], colours[0], axes)
        self.play(FadeIn(step_lbl), Create(path), run_time=1.2)
        self.wait(1.5)

        pause_times = [1.2, 1.0, 0.6]
        for i, (n, col) in enumerate(zip(STEPS_SEQUENCE[1:], colours[1:])):
            new_path = make_walk_path(n, col, axes)
            new_lbl  = Text(f"{n} steps", font_size=24, color=col)
            new_lbl.to_corner(UL, buff=0.5).shift(DOWN * 0.8)
            self.play(
                FadeOut(path), FadeOut(step_lbl),
                FadeIn(new_path), FadeIn(new_lbl),
                run_time=ZOOM_TIME,
            )
            path     = new_path
            step_lbl = new_lbl
            self.wait(pause_times[i])

        self.play(FadeOut(step_lbl))

        # ── Brownian motion label ──
        bm_label = MathTex(r"B_t : \text{ Brownian motion}", font_size=30, color=C_DARK)
        bm_label.next_to(title, DOWN, buff=0.15)
        bm_label.set_x(0)
        self.play(FadeIn(bm_label)); self.wait(0.8)
        self.play(FadeOut(bm_label))

        # ── Shrink graph to right half ──
        graph_group = VGroup(axes, path, x_lbl, y_lbl, x_labels)
        self.play(
            graph_group.animate.scale(0.6).to_edge(RIGHT, buff=0.3),
            run_time=0.8,
        )
        self.wait(0.3)

        # ── Left panel axes for properties ──
        SMALL_FS = 20
        EQ_FS    = 28

        # ── Line 1: E[B_t] = 0 ──
        eq1 = MathTex(r"\mathbb{E}[B_t] = 0", font_size=EQ_FS, color=C_DARK)
        eq1.move_to(LEFT * 3.2 + UP * 1.8)
        lbl1 = Text("no drift — still a martingale",
                    font_size=SMALL_FS, color=C_GREY)
        lbl1.next_to(eq1, DOWN, buff=0.2)
        lbl1.set_x(eq1.get_x())

        self.play(FadeIn(eq1, shift=UP * 0.1), run_time=0.4)
        self.wait(0.5)
        self.play(FadeIn(lbl1), run_time=0.3)

        # Add E[B_t]=0 line onto graph
        mean_line = axes.plot(lambda x: 0, x_range=[0, 10],
                              color=C_RED, stroke_width=2)
        mean_line = DashedVMobject(mean_line, num_dashes=20)
        self.play(Create(mean_line), run_time=0.4)
        self.wait(1.0)

        # ── Line 2: E[B_t²] = t ──
        eq2 = MathTex(r"\mathbb{E}[B_t^2] = t", font_size=EQ_FS, color=C_DARK)
        eq2.next_to(lbl1, DOWN, buff=0.5)
        eq2.set_x(eq1.get_x())
        lbl2 = Text("variance grows linearly —\n" + r"B_t² − t still a martingale",
                    font_size=SMALL_FS, color=C_GREY, line_spacing=1.3)
        lbl2.next_to(eq2, DOWN, buff=0.2)
        lbl2.set_x(eq2.get_x())

        self.play(FadeIn(eq2, shift=UP * 0.1), run_time=0.4)
        self.wait(0.5)
        self.play(FadeIn(lbl2), run_time=0.3)
        self.wait(0.8)

        # ── Ensemble of BM paths on graph ──
        np.random.seed(99)
        ensemble = VGroup()
        for _ in range(N_BM):
            p = make_walk_path(N_BM_STEPS, C_BLUE, axes, stroke=1.0)
            p.set_opacity(0.08)
            ensemble.add(p)
        self.play(FadeIn(ensemble), run_time=0.5)
        self.wait(0.5)

        # ── Confidence interval bands ──
        # 1-sigma: ±1√t, 2-sigma: ±2√t
        # After scale(0.6), axes.c2p still works correctly
        t_vals = np.linspace(0.01, 10, 200)

        def sigma_band(k, fill_col, fill_op):
            upper_pts = [axes.c2p(t,  k * np.sqrt(t) * 4 / np.sqrt(N_BM_STEPS) * np.sqrt(N_BM_STEPS))
                         for t in t_vals]
            lower_pts = [axes.c2p(t, -k * np.sqrt(t) * 4 / np.sqrt(N_BM_STEPS) * np.sqrt(N_BM_STEPS))
                         for t in t_vals]
            # Build closed polygon
            band = Polygon(
                *upper_pts, *lower_pts[::-1],
                fill_color=fill_col, fill_opacity=fill_op,
                stroke_width=0,
            )
            return band

        # Use simpler direct scaling: walk is scaled by 4/sqrt(n)*sqrt(n)=4
        # so 1-sigma at time t (normalised) = sqrt(t)*4/sqrt(10) to match axis
        def sigma_band_simple(k, fill_col, fill_op):
            scale_y = 4.0 / np.sqrt(10)
            upper_pts = [axes.c2p(t,  k * np.sqrt(t) * scale_y) for t in t_vals]
            lower_pts = [axes.c2p(t, -k * np.sqrt(t) * scale_y) for t in t_vals]
            band = Polygon(
                *upper_pts, *lower_pts[::-1],
                fill_color=fill_col, fill_opacity=fill_op,
                stroke_width=0,
            )
            return band

        band2 = sigma_band_simple(2, "#1565C0", 0.12)   # 2-sigma lighter blue
        band1 = sigma_band_simple(1, "#1565C0", 0.25)   # 1-sigma deeper blue

        self.play(FadeIn(band2), run_time=0.4)
        self.play(FadeIn(band1), run_time=0.4)

        # Sigma labels
        sig1_lbl = MathTex(r"1\sigma", font_size=18, color="#1565C0")
        sig2_lbl = MathTex(r"2\sigma", font_size=18, color="#1565C0")
        t_label  = 9.5
        scale_y  = 4.0 / np.sqrt(10)
        sig1_lbl.move_to(axes.c2p(t_label,  1 * np.sqrt(t_label) * scale_y) + UP * 0.2)
        sig2_lbl.move_to(axes.c2p(t_label,  2 * np.sqrt(t_label) * scale_y) + UP * 0.2)
        self.play(FadeIn(sig1_lbl), FadeIn(sig2_lbl), run_time=0.3)

        self.wait(HOLD_TIME)

class S7_BrownianProperties(Scene):
    def construct(self):
        self.camera.background_color = BG
        HOLD_TIME = 20.0
        TITLE_FS  = 15
        SMALL_FS  = 16

        TL_C = np.array([-3.6,  2.0, 0])
        TR_C = np.array([ 3.6,  2.0, 0])
        BL_C = np.array([-3.6, -2.0, 0])
        BR_C = np.array([ 3.6, -2.0, 0])
        PW, PH = 6.6, 3.4

        def panel_rect(c):
            r = Rectangle(width=PW, height=PH,
                           stroke_color=C_GREY, stroke_width=1.5,
                           fill_opacity=0)
            r.move_to(c)
            return r

        def panel_title(txt, c):
            t = Text(txt, font_size=TITLE_FS, color=C_DARK)
            t.move_to(c + np.array([0, PH/2 - 0.22, 0]))
            return t

        rect_tl = panel_rect(TL_C)
        rect_tr = panel_rect(TR_C)
        rect_bl = panel_rect(BL_C)
        rect_br = panel_rect(BR_C)

        ttl_tl = panel_title("Pollen grain jostled by water molecules — Einstein 1905", TL_C)
        ttl_tr = panel_title("Tangled polymer chain in solution", TR_C)
        ttl_bl = panel_title("Voltage fluctuations across a resistor: Johnson noise", BL_C)
        ttl_br = panel_title("S&P 500 — Geometric Brownian Motion", BR_C)

        # ══════════════════════════════════════
        # TL — pollen particle with reflection
        # ══════════════════════════════════════
        np.random.seed(42)
        N_POLLEN      = 2000
        POLLEN_MARGIN = 2.6
        pollen_steps  = np.random.randn(N_POLLEN, 2) * 0.09
        pollen_pos    = np.cumsum(pollen_steps, axis=0)
        pollen_idx    = [0]

        pollen_dot  = Dot(TL_C.copy(), radius=0.13, color=C_YELLOW)
        pollen_path = VMobject(stroke_color=C_BLUE, stroke_width=1.0,
                               fill_opacity=0, stroke_opacity=0.35)
        pollen_path.set_points_as_corners([TL_C.copy(), TL_C.copy()])

        def reflect(v, margin):
            r = 2 * margin
            v = v % r
            if v > margin:
                v = r - v
            return v - margin

        def update_pollen(m, dt):
            idx = pollen_idx[0]
            if idx >= N_POLLEN - 1:
                return
            steps_this_frame = max(1, int(dt * 18))
            new_idx = min(idx + steps_this_frame, N_POLLEN - 1)
            pollen_idx[0] = new_idx
            cx = reflect(pollen_pos[new_idx, 0] + POLLEN_MARGIN, POLLEN_MARGIN)
            cy = reflect(pollen_pos[new_idx, 1] + POLLEN_MARGIN, POLLEN_MARGIN)
            # Further clamp to panel
            cx = np.clip(cx, -POLLEN_MARGIN, POLLEN_MARGIN)
            cy = np.clip(cy, -1.3, 1.3)
            pollen_dot.move_to(TL_C + np.array([cx, cy, 0]))
            trail_pts = []
            for j in range(0, new_idx + 1, 3):
                rx = np.clip(reflect(pollen_pos[j, 0] + POLLEN_MARGIN,
                                     POLLEN_MARGIN), -POLLEN_MARGIN, POLLEN_MARGIN)
                ry = np.clip(reflect(pollen_pos[j, 1] + POLLEN_MARGIN,
                                     POLLEN_MARGIN), -1.3, 1.3)
                trail_pts.append(TL_C + np.array([rx, ry, 0]))
            if len(trail_pts) >= 2:
                pollen_path.set_points_as_corners(trail_pts)

        # ══════════════════════════════════════
        # TR — polymer chain 3D projected
        # ══════════════════════════════════════
        N_POLY     = 40
        BOND_LEN   = 0.22
        poly_seed  = [7]
        poly_timer = [0.0]
        POLY_REDRAW = 2.5

        def gen_polymer_3d(seed):
            np.random.seed(seed)
            theta    = np.random.uniform(0, np.pi,   N_POLY)
            phi      = np.random.uniform(0, 2*np.pi, N_POLY)
            dx = np.sin(theta) * np.cos(phi)
            dy = np.sin(theta) * np.sin(phi)
            dz = np.cos(theta)
            xs = np.cumsum(dx) * BOND_LEN
            ys = np.cumsum(dy) * BOND_LEN
            zs = np.cumsum(dz) * BOND_LEN
            # Isometric projection
            xs_p = xs - zs * 0.4
            ys_p = ys + zs * 0.25
            xs_p -= xs_p.mean(); ys_p -= ys_p.mean()
            xs_p  = np.clip(xs_p, -2.6, 2.6)
            ys_p  = np.clip(ys_p, -1.2, 1.2)
            return xs_p, ys_p

        px0, py0 = gen_polymer_3d(poly_seed[0])
        polymer_mob = VMobject(stroke_color=C_GREEN, stroke_width=2.5,
                               fill_opacity=0)
        polymer_mob.set_points_as_corners(
            [TR_C + np.array([px0[i], py0[i], 0]) for i in range(N_POLY)]
        )
        poly_beads = VGroup(*[
            Dot(TR_C + np.array([px0[i], py0[i], 0]),
                radius=0.07, color=C_GREEN)
            for i in range(N_POLY)
        ])

        def update_polymer(m, dt):
            poly_timer[0] += dt
            if poly_timer[0] < POLY_REDRAW:
                return
            poly_timer[0] = 0.0
            poly_seed[0] += 1
            xs, ys = gen_polymer_3d(poly_seed[0])
            pts = [TR_C + np.array([xs[i], ys[i], 0]) for i in range(N_POLY)]
            m.set_points_as_corners(pts)
            for j, bead in enumerate(poly_beads):
                bead.move_to(TR_C + np.array([xs[j], ys[j], 0]))

        # ══════════════════════════════════════
        # BL — Johnson noise with axes
        # ══════════════════════════════════════
        np.random.seed(13)
        N_NOISE      = 300
        noise_buffer = list(np.random.randn(N_NOISE) * 0.55)
        noise_timer  = [0.0]
        NOISE_SPEED  = 12

        bl_ax = Axes(
            x_range=[0, N_NOISE, 50],
            y_range=[-2, 2, 1],
            x_length=5.8, y_length=2.6,
            axis_config={"color": C_DARK, "include_tip": False,
                         "include_numbers": False},
        ).move_to(BL_C + np.array([0, -0.1, 0]))

        bl_x_lbl = Text("time", font_size=13, color=C_DARK)
        bl_x_lbl.next_to(bl_ax, DOWN, buff=0.15)
        bl_y_lbl = Text("V", font_size=13, color=C_DARK)
        bl_y_lbl.next_to(bl_ax, LEFT, buff=0.1)
        bl_y_ticks = VGroup()
        for v in [-1, 0, 1]:
            lbl = MathTex(str(v), font_size=13)
            lbl.next_to(bl_ax.c2p(0, v), LEFT, buff=0.08)
            bl_y_ticks.add(lbl)

        noise_mob = VMobject(stroke_color=C_RED, stroke_width=1.5,
                             fill_opacity=0)
        noise_mob.set_points_as_corners([bl_ax.c2p(0, 0), bl_ax.c2p(1, 0)])

        def update_noise(m, dt):
            noise_timer[0] += dt
            steps = int(noise_timer[0] * NOISE_SPEED)
            if steps < 1:
                return
            noise_timer[0] = 0.0
            noise_buffer.extend(list(np.random.randn(steps) * 0.55))
            visible = noise_buffer[-N_NOISE:]
            n = len(visible)
            if n < 2:
                return
            pts = [bl_ax.c2p(i, np.clip(visible[i], -1.9, 1.9))
                   for i in range(n)]
            m.set_points_as_corners(pts)

        # ══════════════════════════════════════
        # BR — GBM stock with axes, floor, fast
        # ══════════════════════════════════════
        np.random.seed(99)
        N_STOCK  = 500
        dt_s     = 1.0 / 252
        MU_S     = 0.15
        SIG_S    = 0.16
        S_FLOOR  = 10.0

        price_init        = 100.0
        stock_displayed   = [[price_init]]
        stock_timer       = [0.0]
        p_min_init        = 60.0
        p_max_init        = 180.0

        br_ax = Axes(
            x_range=[0, N_STOCK, 100],
            y_range=[p_min_init, p_max_init, 30],
            x_length=5.8, y_length=2.6,
            axis_config={"color": C_DARK, "include_tip": False,
                         "include_numbers": False},
        ).move_to(BR_C + np.array([0, -0.1, 0]))

        br_x_lbl = Text("trading days", font_size=13, color=C_DARK)
        br_x_lbl.next_to(br_ax, DOWN, buff=0.15)
        br_y_lbl = Text("price", font_size=13, color=C_DARK)
        br_y_lbl.next_to(br_ax, LEFT, buff=0.1)
        br_y_ticks = VGroup()
        for v in [80, 100, 120, 140, 160]:
            lbl = MathTex(str(v), font_size=11)
            lbl.next_to(br_ax.c2p(0, v), LEFT, buff=0.08)
            br_y_ticks.add(lbl)

        stock_mob = VMobject(stroke_color=C_GREEN, stroke_width=2,
                             fill_opacity=0)
        stock_mob.set_points_as_corners([br_ax.c2p(0, price_init),
                                          br_ax.c2p(1, price_init)])

        def update_stock(m, dt):
            stock_timer[0] += dt
            steps = int(stock_timer[0] * 25)
            if steps < 1:
                return
            stock_timer[0] = 0.0
            cur = max(stock_displayed[0][-1], S_FLOOR)
            news = []
            for _ in range(steps):
                cur = max(
                    cur * np.exp((MU_S - 0.5*SIG_S**2)*dt_s
                                 + SIG_S*np.sqrt(dt_s)*np.random.randn()),
                    S_FLOOR,
                )
                news.append(cur)
            stock_displayed[0].extend(news)
            visible = stock_displayed[0][-N_STOCK:]
            n = len(visible)
            if n < 2:
                return
            pts = [br_ax.c2p(i,
                              np.clip(visible[i], p_min_init, p_max_init))
                   for i in range(n)]
            m.set_points_as_corners(pts)

        # ══════════════════════════════════════
        # Build panels sequentially
        # ══════════════════════════════════════

        # Panel 1 — pollen
        self.play(Create(rect_tl), FadeIn(ttl_tl), run_time=0.3)
        self.add(pollen_path, pollen_dot)
        pollen_dot.add_updater(update_pollen)
        self.wait(4.0)

        # Panel 2 — polymer
        self.play(Create(rect_tr), FadeIn(ttl_tr), run_time=0.3)
        self.add(polymer_mob, poly_beads)
        polymer_mob.add_updater(update_polymer)
        self.wait(4.0)

        # Panel 3 — Johnson noise
        self.play(
            Create(rect_bl), FadeIn(ttl_bl),
            Create(bl_ax), FadeIn(bl_x_lbl), FadeIn(bl_y_lbl),
            FadeIn(bl_y_ticks), run_time=0.4,
        )
        self.add(noise_mob)
        noise_mob.add_updater(update_noise)
        self.wait(4.0)

        # Panel 4 — stock
        self.play(
            Create(rect_br), FadeIn(ttl_br),
            Create(br_ax), FadeIn(br_x_lbl), FadeIn(br_y_lbl),
            FadeIn(br_y_ticks), run_time=0.4,
        )
        self.add(stock_mob)
        stock_mob.add_updater(update_stock)

        # All four running
        self.wait(HOLD_TIME)

        # ── Clear updaters before transform ──
        pollen_dot.clear_updaters()
        polymer_mob.clear_updaters()
        noise_mob.clear_updaters()
        stock_mob.clear_updaters()

        all_panels = VGroup(
            rect_tl, rect_tr, rect_bl, rect_br,
            ttl_tl, ttl_tr, ttl_bl, ttl_br,
            polymer_mob, poly_beads,
            noise_mob, bl_ax, bl_x_lbl, bl_y_lbl, bl_y_ticks,
            stock_mob, br_ax, br_x_lbl, br_y_lbl, br_y_ticks,
            pollen_dot, pollen_path,
        )

        self.play(
            all_panels.animate.scale(0.72).shift(UP * 0.9),
            run_time=0.8,
        )

        summary = Text(
            "coin flip game  →  random walk  →  Brownian motion",
            font_size=26, color=C_DARK,
        )
        summary.to_edge(DOWN, buff=0.6)
        sub = Text("martingale property carries through at every scale",
                   font_size=19, color=C_GREY)
        sub.next_to(summary, DOWN, buff=0.2)

        self.play(FadeIn(summary, shift=UP * 0.1))
        self.play(FadeIn(sub))
        self.wait(3.0)

# ═══════════════════════════════════════════════════════════════
# SECTION 8 — HITTING TIMES AND LÉVY DISTRIBUTION
# ═══════════════════════════════════════════════════════════════

class S8_BrownianHittingSetup(Scene):
    """
    SCRIPT CUE: [Brownian path traces to first crossing. Vertical line drops.
    Right panel: recall E[T_a]=a², but now ask about distribution.]
    """
    def construct(self):
        self.camera.background_color = BG
        SEED    = 55
        A_LEVEL = 1.8
        SCALE   = 2.5
        EQ_FS      = 32
        SMALL_FS   = 22
        STEP_PAUSE = 1.5
        HOLD_TIME  = 2.5

        # Simulate, then cut the path at the first hit of the level
        MAX_STEPS  = 5000
        dt         = 1.0 / 500
        t_raw, B_raw = brownian_path(MAX_STEPS, dt, scale=SCALE, seed=SEED)
        hit_idx    = first_hitting_index(B_raw, A_LEVEL)

        B      = B_raw[:hit_idx + 1]
        t_vals = t_raw[:hit_idx + 1]

        # Rescale t_vals to fit axis nicely
        t_max  = t_vals[-1]
        t_vals = t_vals / t_max * 10.0   # always fills x-axis to 10

        # ── Title ──
        title = Text("Brownian Hitting Time  ", font_size=30,
                     color=C_DARK, weight=BOLD)
        title_eq = MathTex(r"T_a = \inf\{t : B_t \geq a\}",
                           font_size=30, color=C_YELLOW)
        title_row = VGroup(title, title_eq)
        title_row.arrange(RIGHT, buff=0.1)
        title_row.to_edge(UP, buff=0.3)
        underline = Line(
            title_row.get_corner(DL) + DOWN * 0.08,
            title_row.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        self.play(FadeIn(title_row), Create(underline))
        # ── Axes ──
        ax = Axes(
            x_range=[0, 10.5, 2], y_range=[-3.5, 3.5, 1],
            x_length=5.5, y_length=5.0,
            axis_config={"color": BLACK, "include_tip": False,
                         "include_numbers": False},
        )
        ax.to_edge(LEFT, buff=1.2).shift(DOWN * 0.3)

        x_labels = VGroup()
        for val in range(0, 11, 2):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(ax.c2p(val, 0), DOWN, buff=0.15)
            x_labels.add(lbl)
        y_labels = VGroup()
        for val in range(-3, 4, 1):
            lbl = MathTex(str(val), font_size=18)
            lbl.next_to(ax.c2p(0, val), LEFT, buff=0.15)
            y_labels.add(lbl)

        x_lbl = Text("time  t", font_size=18, color=C_DARK)
        x_lbl.next_to(ax, DOWN, buff=0.4)
        y_lbl = Text("position", font_size=18, color=C_DARK)
        y_lbl.rotate(PI / 2)
        y_lbl.next_to(ax, LEFT, buff=0.4)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl),
                  FadeIn(x_labels), FadeIn(y_labels))

        # ── Level a ──
        a_line = Line(
            ax.c2p(0, A_LEVEL), ax.c2p(10, A_LEVEL),
            color=C_YELLOW, stroke_width=2.5,
        )
        a_tick = Line(
            ax.c2p(0, A_LEVEL) + LEFT * 0.18,
            ax.c2p(0, A_LEVEL) + RIGHT * 0.18,
            color=C_YELLOW, stroke_width=2.5,
        )
        a_lbl = MathTex(r"a", font_size=26, color=C_YELLOW)
        a_lbl.next_to(ax.c2p(0, A_LEVEL), LEFT, buff=0.25)
        self.play(Create(a_line), Create(a_tick), FadeIn(a_lbl))

        # ── Path in chunks ──
        path_pts   = [ax.c2p(t_vals[i], B[i]) for i in range(hit_idx + 1)]
        CHUNK      = 30
        total_time = 2.5
        chunk_time = total_time * CHUNK / max(hit_idx, 1)

        path_so_far = VMobject(stroke_color=C_BLUE, stroke_width=2.5,
                               fill_opacity=0)
        path_so_far.set_points_as_corners(path_pts[:2])
        self.add(path_so_far)

        for chunk_start in range(0, hit_idx, CHUNK):
            chunk_end = min(chunk_start + CHUNK, hit_idx)
            new_path  = VMobject(stroke_color=C_BLUE, stroke_width=2.5,
                                 fill_opacity=0)
            new_path.set_points_as_corners(path_pts[:chunk_end + 1])
            self.remove(path_so_far)
            path_so_far = new_path
            self.add(path_so_far)
            self.wait(chunk_time)

        # ── Crossing marker ──
        t_hit   = t_vals[hit_idx]
        v_line  = DashedLine(
            ax.c2p(t_hit, 0), ax.c2p(t_hit, A_LEVEL),
            color=C_GREEN, stroke_width=2, dash_length=0.12,
        )
        ta_lbl  = MathTex(r"T_a", font_size=26, color=C_GREEN)
        ta_lbl.next_to(ax.c2p(t_hit, 0), DOWN, buff=0.2)
        hit_dot = Dot(ax.c2p(t_hit, A_LEVEL), radius=0.11, color=C_GREEN)

        self.play(Create(v_line), FadeIn(ta_lbl), FadeIn(hit_dot))
        self.play(hit_dot.animate.scale(2.0), run_time=0.2)
        self.play(hit_dot.animate.scale(0.5), run_time=0.2)

        cross_ann = Text("first crossing", font_size=SMALL_FS - 2, color=C_GREEN)
        cross_ann.next_to(hit_dot, UR, buff=0.12)
        self.play(FadeIn(cross_ann))
        self.wait(0.5)

        on_avg = Text("Recall:", font_size=26, color=C_DARK, weight=BOLD)
        on_avg.move_to(RIGHT * 3.2 + UP * 2.3)
        self.play(FadeIn(on_avg, shift=UP * 0.1))
        self.wait(0.4)

        # The drunk man result verbatim
        recall_eq = MathTex(r"\mathbb{E}[T] = 1700 - 289 = 1411",
                            font_size=EQ_FS - 2, color=C_DARK)
        recall_eq.next_to(on_avg, DOWN, buff=0.35)
        recall_eq.set_x(on_avg.get_x())
        recall_box = SurroundingRectangle(recall_eq, color=C_GREEN,
                                          buff=0.15, corner_radius=0.08)
        self.play(FadeIn(recall_eq), run_time=0.4)
        self.play(Create(recall_box), run_time=0.3)
        self.wait(0.4)

        # Implies E[T_a] ∝ a²
        implies_row_lhs = MathTex(r"\Rightarrow", font_size=EQ_FS, color=C_GREEN)
        implies_row_rhs = MathTex(r"\mathbb{E}[T_a] \propto a^2",
                                  font_size=EQ_FS, color=C_GREEN)
        implies_row = VGroup(implies_row_lhs, implies_row_rhs)
        implies_row.arrange(RIGHT, buff=0.2)
        implies_row.next_to(recall_eq, DOWN, buff=0.3)
        implies_row.set_x(on_avg.get_x())

        recall_lbl = Text("same martingale argument,\ncontinuous time",
                          font_size=SMALL_FS - 2, color=C_GREY, line_spacing=1.3)
        recall_lbl.next_to(implies_row, DOWN, buff=0.2)
        recall_lbl.set_x(on_avg.get_x())

        self.play(FadeIn(implies_row), run_time=0.4)
        self.play(FadeIn(recall_lbl), run_time=0.3)
        self.wait(STEP_PAUSE)

        self.wait(HOLD_TIME)
        # ── Clear right panel, run more simulations ──
        self.play(
            FadeOut(VGroup(
                on_avg, recall_eq, recall_box, implies_row, recall_lbl,
            )),
            run_time=0.5,
        )
        self.wait(0.3)

        # Run 4 more simulations, each until they hit A_LEVEL
        SIM_SEEDS  = [101, 303, 404, 505]
        SIM_COLORS = [C_RED, C_GREEN, "#9C27B0", "#FF9800"]
        sim_paths  = []
        sim_hits   = []   # (t_hit_rescaled, B_hit_val)

        for sim_seed, sim_col in zip(SIM_SEEDS, SIM_COLORS):
            t_s, B_s = brownian_path(MAX_STEPS, dt, scale=SCALE, seed=sim_seed)
            h_idx    = first_hitting_index(B_s, A_LEVEL)

            sim_paths.append((B_s[:h_idx + 1], t_s[:h_idx + 1], h_idx, sim_col))
            sim_hits.append(t_s[h_idx])

        # Find longest simulation to set x axis
        t_max_all  = max(sim_hits + [t_vals[-1] / 10.0 * t_raw[hit_idx]])
        # Rescale: original path used t_vals rescaled to 10
        # New sims rescale to same pixel width proportionally
        x_max_new  = max(10.0, t_max_all / (dt * hit_idx) * 10.0 * 1.1)
        # Simpler: just find the longest in raw dt units and rescale all to x_max_new
        raw_hit_original = dt * hit_idx
        x_max_new  = max(raw_hit_original, max(sim_hits)) * 1.1

        # Rescale all t arrays to same screen scale as original
        screen_scale = 10.0 / raw_hit_original   # pixels per raw time unit

        # Extend x axis if needed
        x_axis_end = x_max_new * screen_scale
        if x_axis_end > 10.5:
            new_ax = Axes(
                x_range=[0, x_axis_end * 1.05, max(2, round(x_axis_end / 5))],
                y_range=[-3.5, 3.5, 1],
                x_length=5.5, y_length=5.0,
                axis_config={"color": BLACK, "include_tip": False,
                                "include_numbers": False},
            )
            new_ax.to_edge(LEFT, buff=1.2).shift(DOWN * 0.3)

            # Rebuild a_line on new axes
            new_a_line = Line(
                new_ax.c2p(0, A_LEVEL),
                new_ax.c2p(x_axis_end * 1.05, A_LEVEL),
                color=C_YELLOW, stroke_width=2.5,
            )
            self.play(
                Transform(ax, new_ax),
                Transform(a_line, new_a_line),
                run_time=0.5,
            )
            working_ax = new_ax
        else:
            working_ax = ax
            x_axis_end = 10.0

        # Draw each simulation path then drop stopping time
        t_max_all = max(sim_hits)

        for B_s, t_s, _, sim_col in sim_paths:
            t_rescaled = t_s / t_max_all * 10.0
            pts = [working_ax.c2p(t_rescaled[i], np.clip(B_s[i], -3.5, 3.5))
                    for i in range(len(B_s))]

            if len(pts) < 2:
                continue

            n_s     = len(pts)
            CHUNK_S = max(50, n_s // 20)   # at most 20 chunks per path
            total_s = 1.5
            chunk_s = total_s * CHUNK_S / n_s

            sim_path_mob = VMobject(stroke_color=sim_col, stroke_width=2.0,
                                    fill_opacity=0, stroke_opacity=0.7)
            sim_path_mob.set_points_as_corners(pts[:2])
            self.add(sim_path_mob)

            for cs in range(0, n_s - 1, CHUNK_S):
                ce      = min(cs + CHUNK_S, n_s - 1)
                new_p   = VMobject(stroke_color=sim_col, stroke_width=2.0,
                                    fill_opacity=0, stroke_opacity=0.7)
                new_p.set_points_as_corners(pts[:ce + 1])
                self.remove(sim_path_mob)
                sim_path_mob = new_p
                self.add(sim_path_mob)
                self.wait(chunk_s)

            t_hit_s   = t_rescaled[-1]
            hit_dot_s = Dot(working_ax.c2p(t_hit_s, A_LEVEL),
                            radius=0.10, color=sim_col)
            drop_line = DashedLine(
                working_ax.c2p(t_hit_s, 0),
                working_ax.c2p(t_hit_s, A_LEVEL),
                color=sim_col, stroke_width=1.8, dash_length=0.10,
            )
            tick_s = Line(
                working_ax.c2p(t_hit_s, 0) + DOWN * 0.12,
                working_ax.c2p(t_hit_s, 0) + UP   * 0.12,
                color=sim_col, stroke_width=2,
            )
            self.play(FadeIn(hit_dot_s), Create(drop_line), Create(tick_s),
                        run_time=0.4)
            self.wait(0.3)

        # Also drop original T_a
        orig_tick = Line(
            working_ax.c2p(t_vals[-1], 0) + DOWN * 0.12,
            working_ax.c2p(t_vals[-1], 0) + UP   * 0.12,
            color=C_BLUE, stroke_width=2,
        )
        self.play(Create(orig_tick), run_time=0.3)
        self.wait(0.5)

        # ── Question: is there a distribution? ──
        dist_q = Text("Is there stopping time distribution?",
                        font_size=24, color=C_DARK)
        dist_q.move_to(RIGHT * 2.8 + UP * 2.5)
        self.play(FadeIn(dist_q, shift=UP * 0.1))
        self.wait(1.0)

        dist_q2 = MathTex(r"T_a \sim \;?", font_size=36, color=C_YELLOW)
        dist_q2.next_to(dist_q, DOWN, buff=0.4)
        dist_q2.set_x(dist_q.get_x())
        self.play(FadeIn(dist_q2, shift=UP * 0.1))
        self.play(dist_q2.animate.scale(1.2), run_time=0.2)
        self.play(dist_q2.animate.scale(1/1.2), run_time=0.2)
        self.wait(HOLD_TIME)

class S8_ExponentialMartingale(Scene):
    """
    SCRIPT CUE: [Exponential martingale. Both annotations appear together for
    10s. OST morphing derivation with disclaimer. Levy formula. Distribution
    with mode, mean, median. Tail zoom with highlight and bridge probability.]
    """
    def construct(self):
        self.camera.background_color = BG
        EQ_FS      = 34
        SMALL_FS   = 21
        STEP_PAUSE = 0.5
        HOLD_TIME  = 2.5

        # ── Title ──
        title = Text("The Exponential Martingale", font_size=32,
                     color=C_DARK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))

        # ── Main formula — anchored to underline so it never overlaps title ──
        formula = MathTex(
            r"M_t(\alpha) = \exp\!\Big(",
            r"\alpha B_t",
            r"-",
            r"\tfrac{1}{2}\alpha^2 t",
            r"\Big)",
            font_size=EQ_FS + 4,
        )
        formula[1].set_color(C_BLUE)
        formula[3].set_color(C_RED)
        formula.next_to(underline, DOWN, buff=0.5)
        formula.set_x(0)
        self.play(FadeIn(formula, scale=0.85)); self.wait(0.5)
        self.play(FadeOut(title), FadeOut(underline), run_time=0.3)
        # ── Both annotations simultaneously, no overlaps ──
        # Blue label ABOVE formula, arrow points DOWN into αB_t
        blue_box = SurroundingRectangle(formula[1], color=C_BLUE,
                                        buff=0.06, corner_radius=0.05)
        blue_lbl = Text("signal: grows when B_t rises",
                        font_size=SMALL_FS, color=C_BLUE)
        blue_lbl.next_to(formula, UP, buff=0.55).shift(LEFT * 1.2)
        blue_arr = Arrow(
            blue_lbl.get_bottom(), blue_box.get_top(),
            color=C_BLUE, buff=0.05, stroke_width=1.5,
            max_tip_length_to_length_ratio=0.08, tip_length=0.1,
        )

        # Red label BELOW formula, arrow points UP into −½α²t
        red_box = SurroundingRectangle(formula[3], color=C_RED,
                                       buff=0.06, corner_radius=0.05)
        red_lbl = Text("drift correction, same move as  ",
                       font_size=SMALL_FS, color=C_RED)
        red_tex = MathTex(r"X_n^2 - n", font_size=SMALL_FS, color=C_RED)
        red_row = VGroup(red_lbl, red_tex)
        red_row.arrange(RIGHT, buff=0.1)
        red_row.next_to(formula, DOWN, buff=0.55).shift(RIGHT * 0.4)
        red_arr = Arrow(
            red_row.get_top(), red_box.get_bottom(),
            color=C_RED, buff=0.05, stroke_width=1.5,
            max_tip_length_to_length_ratio=0.08, tip_length=0.1,
        )

        self.play(
            Create(blue_box), GrowArrow(blue_arr), FadeIn(blue_lbl),
            Create(red_box),  GrowArrow(red_arr),  FadeIn(red_row),
            run_time=0.5,
        )
        self.wait(15.0)
        self.play(
            FadeOut(blue_box), FadeOut(blue_arr), FadeOut(blue_lbl),
            FadeOut(red_box),  FadeOut(red_arr),  FadeOut(red_row),
            run_time=0.3,
        )
        self.wait(0.3)

        # ── OST header ──
        ost_title = Text("Apply Optional Stopping Theorem at  ",
                         font_size=SMALL_FS, color=C_YELLOW)
        ost_tex   = MathTex(r"T = T_a", font_size=SMALL_FS, color=C_YELLOW)
        ost_row   = VGroup(ost_title, ost_tex)
        ost_row.arrange(RIGHT, buff=0.1)
        ost_row.next_to(formula, DOWN, buff=0.5)
        ost_row.set_x(0)
        self.play(FadeIn(ost_row)); self.wait(0.5)

        # ── Disclaimer — green text, right side ──
        disclaimer = Text(
            "Disclaimer: This is just algebraic\nmanipulation, you do not need\n to follow every step",
            font_size=SMALL_FS - 2, color=C_GREEN, line_spacing=1.3,
        )
        disclaimer.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)
        self.play(FadeIn(disclaimer, shift=LEFT * 0.1)); self.wait(0.3)

        # ── Morphing derivation — annotations as MathTex so LaTeX renders ──
        deriv_steps = [
            (
                MathTex(r"\mathbb{E}[M_{T_a}] = M_0 = 1", font_size=EQ_FS),
                MathTex(r"\text{martingale preserves expectation}",
                        font_size=SMALL_FS - 2, color=C_GREY),
            ),
            (
                MathTex(r"\mathbb{E}\!\left[\exp\!\left(\alpha a - \tfrac{1}{2}\alpha^2 T_a\right)\right] = 1",
                        font_size=EQ_FS),
                MathTex(r"B_{T_a} = a \text{ at hitting time}",
                        font_size=SMALL_FS - 2, color=C_GREY),
            ),
            (
                MathTex(r"e^{\alpha a} \cdot \mathbb{E}\!\left[e^{-\frac{1}{2}\alpha^2 T_a}\right] = 1",
                        font_size=EQ_FS),
                MathTex(r"e^{\alpha a} \text{ is deterministic — factor out}",
                        font_size=SMALL_FS - 2, color=C_GREY),
            ),
            (
                MathTex(r"\mathbb{E}\!\left[e^{-\frac{1}{2}\alpha^2 T_a}\right] = e^{-\alpha a}",
                        font_size=EQ_FS),
                MathTex(r"\text{set } \lambda = \tfrac{1}{2}\alpha^2,\quad \alpha = \sqrt{2\lambda}",
                        font_size=SMALL_FS - 2, color=C_GREY),
            ),
        ]

        current, ann_mob = deriv_steps[0]
        current.next_to(ost_row, DOWN, buff=0.45)
        current.set_x(0)
        ann_mob.next_to(current, DOWN, buff=0.2)
        ann_mob.set_x(0)
        self.play(FadeIn(current)); self.wait(0.2)
        self.play(FadeIn(ann_mob)); self.wait(STEP_PAUSE)

        for next_eq, next_ann in deriv_steps[1:]:
            next_eq.move_to(current.get_center())
            next_ann.next_to(next_eq, DOWN, buff=0.2)
            next_ann.set_x(0)
            self.play(
                TransformMatchingShapes(current, next_eq),
                FadeOut(ann_mob),
                run_time=0.7,
            )
            self.play(FadeIn(next_ann)); self.wait(STEP_PAUSE)
            current = next_eq
            ann_mob = next_ann

        self.play(FadeOut(ann_mob), FadeOut(disclaimer), run_time=0.3)

        # ── Final boxed result ──
        result = MathTex(
            r"\mathbb{E}\!\left[e^{-\lambda T_a}\right] = e^{-a\sqrt{2\lambda}}",
            font_size=EQ_FS + 6,
        )
        result.move_to(current.get_center())
        self.play(TransformMatchingShapes(current, result), run_time=0.7)
        result_box = SurroundingRectangle(result, color=C_YELLOW,
                                          buff=0.2, corner_radius=0.1)
        self.play(Create(result_box)); self.wait(0.5)

        lbl1 = Text("Laplace transform of  ", font_size=SMALL_FS, color=C_GREY)
        lbl1_tex = MathTex(r"T_a", font_size=SMALL_FS, color=C_GREY)
        lbl1_row = VGroup(lbl1, lbl1_tex)
        lbl1_row.arrange(RIGHT, buff=0.1)
        lbl1_row.next_to(result_box, DOWN, buff=0.25)
        lbl1_row.set_x(0)
        self.play(FadeIn(lbl1_row)); self.wait(STEP_PAUSE)

        # ── Shrink to top — anchor to underline so no title overlap ──
        top_group = VGroup(formula, result, result_box)
        self.play(
            FadeOut(VGroup(ost_row, lbl1_row)),
            top_group.animate.scale(0.58).next_to(underline, DOWN, buff=0.2),
            run_time=0.7,
        )
        self.wait(0.3)

        # ── Lévy formula ──
        A_VAL    = 1.8
        E_Ta     = A_VAL ** 2        # mean   = 3.24
        t_peak   = A_VAL ** 2 / 3.0  # mode   = 1.08
        t_median = 7.122             # median for a=1.8

        levy_formula = MathTex(
            r"f_{T_a}(t) = \frac{a}{\sqrt{2\pi}}\, t^{-3/2}\, e^{-a^2/2t}",
            font_size=EQ_FS - 2,
        )
        levy_formula.next_to(top_group, DOWN, buff=0.28)
        levy_formula.set_x(0)

        skip_lbl = Text(
            "(We skipped a few steps... \nbut martingales did shortcut)",
            font_size=SMALL_FS - 2, color=C_GREY, line_spacing=1.3,
        )
        skip_lbl.next_to(levy_formula, RIGHT, buff=0.3)

        self.play(FadeIn(levy_formula, scale=0.85)); self.wait(0.4)
        self.play(FadeIn(skip_lbl)); self.wait(STEP_PAUSE)
        self.play(FadeOut(skip_lbl), run_time=0.3)

        # ── Distribution axes ──
        dist_ax = Axes(
            x_range=[0, 12, 2], y_range=[0, 1.2, 0.4],
            x_length=9.5, y_length=3.2,
            axis_config={"color": BLACK, "include_tip": False,
                         "include_numbers": False},
        )
        dist_ax.next_to(levy_formula, DOWN, buff=0.3)
        dist_ax.set_x(0)

        x_labels = VGroup()
        for val in range(0, 13, 2):
            lbl = MathTex(str(val), font_size=15)
            lbl.next_to(dist_ax.c2p(val, 0), DOWN, buff=0.1)
            x_labels.add(lbl)
        y_labels = VGroup()
        for val in [0.4, 0.8, 1.2]:
            lbl = MathTex(str(val), font_size=13)
            lbl.next_to(dist_ax.c2p(0, val), LEFT, buff=0.1)
            y_labels.add(lbl)

        dist_x_lbl = Text("crossing time  t", font_size=15, color=C_DARK)
        dist_x_lbl.next_to(dist_ax, DOWN, buff=0.2)
        dist_y_lbl = Text("density", font_size=15, color=C_DARK)
        dist_y_lbl.rotate(PI / 2)
        dist_y_lbl.next_to(dist_ax, LEFT, buff=0.28)

        self.play(Create(dist_ax), FadeIn(x_labels), FadeIn(y_labels),
                  FadeIn(dist_x_lbl), FadeIn(dist_y_lbl))

        def levy_pdf(t, a=A_VAL):
            if t <= 0:
                return 0
            return (a / np.sqrt(2 * np.pi)) * t**(-1.5) * np.exp(-a**2 / (2*t))

        f_peak = levy_pdf(t_peak)
        norm   = 1.0 / f_peak

        levy_curve = dist_ax.plot(
            lambda t: min(levy_pdf(t) * norm, 1.15),
            x_range=[0.05, 12, 0.05],
            color=C_BLUE, stroke_width=2.5,
        )
        self.play(Create(levy_curve), run_time=1.2)

        # Mode
        mode_line = DashedLine(
            dist_ax.c2p(t_peak, 0), dist_ax.c2p(t_peak, 1.0),
            color=C_RED, stroke_width=2, dash_length=0.12,
        )
        mode_lbl = Text("mode", font_size=12, color=C_RED)
        mode_lbl.next_to(dist_ax.c2p(t_peak, 1.0), UP, buff=0.06)
        self.play(Create(mode_line), FadeIn(mode_lbl)); self.wait(0.5)

        # Median
        median_line = DashedLine(
            dist_ax.c2p(t_median, 0),
            dist_ax.c2p(t_median, levy_pdf(t_median) * norm),
            color=C_YELLOW, stroke_width=2, dash_length=0.12,
        )
        median_dot = Dot(dist_ax.c2p(t_median, levy_pdf(t_median) * norm),
                         radius=0.08, color=C_YELLOW)
        median_lbl = Text("median", font_size=12, color=C_YELLOW)
        median_lbl.next_to(dist_ax.c2p(t_median, levy_pdf(t_median) * norm),
                            UP, buff=0.06)
        self.play(Create(median_line), FadeIn(median_dot), FadeIn(median_lbl))
        self.wait(0.5)

        # Mean
        e_ta_line = DashedLine(
            dist_ax.c2p(E_Ta, 0),
            dist_ax.c2p(E_Ta, levy_pdf(E_Ta) * norm),
            color=C_GREEN, stroke_width=2, dash_length=0.12,
        )
        e_ta_dot = Dot(dist_ax.c2p(E_Ta, levy_pdf(E_Ta) * norm),
                       radius=0.08, color=C_GREEN)
        e_ta_lbl = MathTex(r"\mathbb{E}[T_a]", font_size=13, color=C_GREEN)
        e_ta_lbl.next_to(dist_ax.c2p(E_Ta, levy_pdf(E_Ta) * norm), UP, buff=0.06)
        e_ta_caveat = Text("(two-sided stopping condition)",
                           font_size=11, color=C_GREY)
        e_ta_caveat.next_to(e_ta_lbl, RIGHT, buff=0.15)
        self.play(Create(e_ta_line), FadeIn(e_ta_dot), FadeIn(e_ta_lbl), FadeIn(e_ta_caveat))
        self.wait(STEP_PAUSE)

        # Heavy tail
        tail_ann = Text("heavy tail:\noccasional very long crossings",
                        font_size=12, color=C_GREY, line_spacing=1.2)
        tail_ann.move_to(dist_ax.c2p(9.5, 0.34))
        tail_arr = Arrow(
            tail_ann.get_left(),
            dist_ax.c2p(7.5, levy_pdf(7.5) * norm + 0.04),
            color=C_GREY, buff=0.05, stroke_width=1.5,
            max_tip_length_to_length_ratio=0.08, tip_length=0.1,
        )
        self.play(FadeIn(tail_ann), GrowArrow(tail_arr))
        self.wait(STEP_PAUSE)

        # ── Tail zoom ──
        zoom_lbl = Text("zooming into tail…", font_size=14, color=C_GREY)
        zoom_lbl.to_corner(DR, buff=0.3)
        self.play(
            FadeIn(zoom_lbl),
            FadeOut(tail_ann), FadeOut(tail_arr),
            FadeOut(e_ta_line), FadeOut(e_ta_dot), FadeOut(e_ta_lbl),FadeOut(e_ta_caveat),
            FadeOut(median_line), FadeOut(median_dot), FadeOut(median_lbl),
            FadeOut(mode_line), FadeOut(mode_lbl),
            run_time=0.4,
        )
        self.wait(0.3)

        tail_ax = Axes(
            x_range=[4, 28, 4], y_range=[0, 0.07, 0.02],
            x_length=9.5, y_length=3.2,
            axis_config={"color": BLACK, "include_tip": False,
                         "include_numbers": False},
        )
        tail_ax.move_to(dist_ax.get_center())

        tail_x_labels = VGroup()
        for val in range(4, 29, 4):
            lbl = MathTex(str(val), font_size=15)
            lbl.next_to(tail_ax.c2p(val, 0), DOWN, buff=0.1)
            tail_x_labels.add(lbl)
        tail_y_labels = VGroup()
        for val in [0.02, 0.04, 0.06]:
            lbl = MathTex(f"{val:.2f}", font_size=13)
            lbl.next_to(tail_ax.c2p(4, val), LEFT, buff=0.1)
            tail_y_labels.add(lbl)

        tail_curve = tail_ax.plot(
            lambda t: levy_pdf(t),
            x_range=[4.1, 28, 0.1],
            color=C_BLUE, stroke_width=2.5,
        )
        power_raw = tail_ax.plot(
            lambda t: 0.42 * t**(-1.5),
            x_range=[4.1, 28, 0.1],
            color=C_RED, stroke_width=1.8,
        )
        power_law = DashedVMobject(power_raw, num_dashes=22)

        self.play(
            FadeOut(levy_curve), FadeOut(dist_ax),
            FadeOut(x_labels), FadeOut(y_labels),
            run_time=0.3,
        )
        self.play(
            FadeIn(tail_ax), FadeIn(tail_curve),
            FadeIn(tail_x_labels), FadeIn(tail_y_labels),
            FadeOut(zoom_lbl),
            run_time=0.6,
        )

        power_lbl = MathTex(r"f(t) \sim t^{-3/2}", font_size=20, color=C_RED)
        power_lbl.next_to(tail_ax.c2p(18, 0.012), UP, buff=0.1)
        self.play(Create(power_law), FadeIn(power_lbl)); self.wait(0.5)

        # ── Yellow tail highlight ──
        t_hi_start = 20.0
        t_hi_end   = 27.8
        shade_top  = [tail_ax.c2p(t, levy_pdf(t))
                      for t in np.linspace(t_hi_start, t_hi_end, 40)]
        shade_bot  = [tail_ax.c2p(t, 0)
                      for t in np.linspace(t_hi_end, t_hi_start, 40)]
        tail_shade = Polygon(
            *shade_top, *shade_bot,
            fill_color=C_YELLOW, fill_opacity=0.4,
            stroke_width=0,
        )
        self.play(FadeIn(tail_shade)); self.wait(0.5)

        # ── Bridge probability ──
        # a = 83 (17 to 100), t = 86400
        # P(T_83 > 86400) = erfc(83/sqrt(2*86400)) ≈ 77.8%
        prob_lbl1 = Text("drunk man example: starts 17m from home",
                         font_size=13, color=C_DARK)
        prob_eq = MathTex(
            r"P(T_{17} > 86{,}400) \approx 4.612\%",
            font_size=EQ_FS - 2, color=C_YELLOW,
        )
        prob_lbl2 = Text("still outside after 24 hours",
                         font_size=13, color=C_GREY)
        prob_group = VGroup(prob_lbl1, prob_eq, prob_lbl2)
        prob_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        prob_group.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)
        prob_arrow = Arrow(
            prob_group.get_left(),
            tail_ax.c2p(24, levy_pdf(24) * 0.5),
            color=C_YELLOW, buff=0.05, stroke_width=1.8,
            max_tip_length_to_length_ratio=0.08, tip_length=0.12,
        )
        
        self.play(FadeIn(prob_lbl1), FadeIn(prob_arrow)); self.wait(0.2)
        self.play(FadeIn(prob_eq, scale=0.85)); self.wait(0.3)
        self.play(FadeIn(prob_lbl2))
        self.wait(HOLD_TIME)


# ═══════════════════════════════════════════════════════════════
# SECTION 9 — FINANCE
# ═══════════════════════════════════════════════════════════════
class S9_Finance(Scene):
    """
    SCRIPT CUE: [Option as hitting problem. Graph LEFT, number line RIGHT,
    synced step-by-step. First case: slow then fast. Second case: fast only.
    Martingale framing. Black-Scholes formula.]
    """
    def construct(self):
        self.camera.background_color = BG
        EQ_FS     = 32
        SMALL_FS  = 22
        HOLD_TIME = 2.5

        # ─────────────────────────────────────────────
        # TITLE
        # ─────────────────────────────────────────────
        title = Text("Martingales in Finance", font_size=32,
                     color=C_DARK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.08,
            title.get_corner(DR) + DOWN * 0.08,
            color=C_DARK, stroke_width=2,
        )
        self.play(FadeIn(title), Create(underline))
        self.wait(0.4)

        # ─────────────────────────────────────────────
        # "AN OPTION IS A BET" TEXT BLOCK
        # ─────────────────────────────────────────────
        intro = Text("An option is a bet.", font_size=34,
                     color=C_DARK, weight=BOLD)
        intro.move_to(UP * 1.5)
        self.play(FadeIn(intro, scale=0.9))
        self.wait(13)

        martingale_lbl = Text("The stock price is a martingale.",
                              font_size=28, color=C_DARK)
        martingale_lbl.next_to(intro, DOWN, buff=0.5)
        martingale_lbl.set_x(0)
        self.play(FadeIn(martingale_lbl, shift=UP * 0.1))
        self.wait(2.0)
        self.play(FadeOut(martingale_lbl), run_time=0.3)
        self.wait(0.3)

        familiar = Text("Sound Familiar?", font_size=40,
                        color=C_YELLOW, weight=BOLD)
        familiar.move_to(DOWN * 1.8)
        
        self.play(FadeIn(familiar, scale=0.8)); self.wait(1.5)
        self.play(FadeOut(VGroup(intro, familiar)), run_time=0.5)
        self.wait(0.3)

        # ─────────────────────────────────────────────
        # SIMULATIONS
        # ─────────────────────────────────────────────
        N_STEPS = 200
        STRIKE  = 100
        START   = 50
        Y_MIN   = -5
        Y_MAX   = 110

        # Sim A: manually constructed to guaranteed hit strike at step 80
        # starts at 50, noisy but trending up, hits 100 at step 80
        rng = np.random.default_rng(0)
        base = np.linspace(50, 102, 81)
        noise = rng.normal(0, 3, 81)
        noise[0] = 0
        walk_a_raw = base + noise
        walk_a_raw = np.clip(walk_a_raw, Y_MIN, Y_MAX)
        # find first crossing
        hits = np.where(walk_a_raw >= STRIKE)[0]
        T_hit_a = int(hits[0])
        walk_a = walk_a_raw[:T_hit_a + 1]

        # Sim B: stays below strike entire time
        walk_b = np.array([float(START)] * (N_STEPS + 1))
        for seed in range(500):
            wb = simple_random_walk(N_STEPS, start=START, seed=seed + 100)
            wb = np.clip(wb, Y_MIN, Y_MAX)
            if np.max(wb) < STRIKE:
                walk_b = wb
                break

        n_a = len(walk_a)
        n_b = len(walk_b)

        # ─────────────────────────────────────────────
        # GRAPH — LEFT PANEL
        # ─────────────────────────────────────────────
        ax = Axes(
            x_range=[0, N_STEPS + 10, 50],
            y_range=[Y_MIN, Y_MAX, 20],
            x_length=5.8,
            y_length=4.4,
            axis_config={"color": BLACK, "include_tip": False,
                         "include_numbers": False},
        )
        ax.to_edge(LEFT, buff=1.1).shift(DOWN * 0.4)

        x_lbl = Text("Step  n", font_size=15, color=C_DARK)
        x_lbl.next_to(ax, DOWN, buff=0.28)
        y_lbl = Text("Price  £", font_size=15, color=C_DARK)
        y_lbl.rotate(PI / 2)
        y_lbl.next_to(ax, LEFT, buff=0.28)

        for val in [0, 50, 100]:
            lbl = MathTex(str(val), font_size=13)
            lbl.next_to(ax.c2p(0, val), LEFT, buff=0.1)
            self.add(lbl)

        expiry_tick = Line(
            ax.c2p(N_STEPS, Y_MIN),
            ax.c2p(N_STEPS, Y_MIN) + DOWN * 0.25,
            color=C_BLUE, stroke_width=2,
        )
        expiry_lbl = Text("Expiry", font_size=13, color=C_BLUE)
        expiry_lbl.next_to(ax.c2p(N_STEPS, Y_MIN), DOWN, buff=0.28)

        strike_line = DashedLine(
            ax.c2p(0, STRIKE), ax.c2p(N_STEPS + 10, STRIKE),
            color=C_GREEN, stroke_width=2, dash_length=0.15,
        )
        strike_graph_lbl = Text("Strike £100", font_size=13, color=C_GREEN)
        strike_graph_lbl.next_to(ax.c2p(0, STRIKE), LEFT, buff=0.08)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(strike_line), FadeIn(strike_graph_lbl))
        self.play(Create(expiry_tick), FadeIn(expiry_lbl))

        # ─────────────────────────────────────────────
        # NUMBER LINE — RIGHT PANEL
        # ─────────────────────────────────────────────
        NL_X_LEFT  = 0.8
        NL_X_RIGHT = 5.2
        NL_Y       = 1.2

        def price_to_nl(p):
            return NL_X_LEFT + (p / 100.0) * (NL_X_RIGHT - NL_X_LEFT)

        nl_line  = Line([NL_X_LEFT, NL_Y, 0], [NL_X_RIGHT, NL_Y, 0],
                        color=C_DARK, stroke_width=3)
        tick_0   = Line([price_to_nl(0),   NL_Y - 0.2, 0],
                        [price_to_nl(0),   NL_Y + 0.2, 0],
                        color=C_DARK, stroke_width=2)
        tick_100 = Line([price_to_nl(100), NL_Y - 0.2, 0],
                        [price_to_nl(100), NL_Y + 0.2, 0],
                        color=C_GREEN, stroke_width=2)

        lbl_0 = Text("£0", font_size=16, color=C_DARK)
        lbl_0.next_to([price_to_nl(0), NL_Y, 0], DOWN, buff=0.22)

        lbl_100 = Text("£100\nStrike Price", font_size=16,
                       color=C_GREEN, line_spacing=1.2)
        lbl_100.next_to([price_to_nl(100), NL_Y, 0], DOWN, buff=0.22)

        dot = Dot([price_to_nl(START), NL_Y, 0], radius=0.14, color=C_YELLOW)
        dot_lbl = Text("Stock Price Today: £50", font_size=15, color=C_YELLOW)
        dot_lbl.next_to(dot, UP, buff=0.18)

        self.play(Create(nl_line), Create(tick_0), Create(tick_100))
        self.play(FadeIn(lbl_0), FadeIn(lbl_100))
        self.play(FadeIn(dot), FadeIn(dot_lbl))
        self.wait(5)

        # ─────────────────────────────────────────────
        # SIM A — slow first, then fast, graph + NL synced
        # Key: every step, update graph path AND dot position together
        # using self.play(..., run_time=dt) so they move simultaneously
        # ─────────────────────────────────────────────
        SLOW_STEPS = 8    # first N steps one-by-one slowly
        SLOW_DT    = 0.45  # seconds per slow step
        FAST_DT    = 0.012 # seconds per fast step (via self.wait after batch)
        FAST_CHUNK = 5    # steps per fast batch

        # Start graph path and dot
        graph_dot_a = Dot(ax.c2p(0, walk_a[0]), radius=0.09, color=C_BLUE)
        self.add(graph_dot_a)

        path_pts = [ax.c2p(0, walk_a[0])]
        path_obj = VMobject(stroke_color=C_BLUE, stroke_width=2.5, fill_opacity=0)
        path_obj.set_points_as_corners([ax.c2p(0, walk_a[0]),
                                        ax.c2p(0, walk_a[0])])
        self.add(path_obj)

        def update_both(step_idx):
            """Move graph dot + NL dot + extend path to walk_a[step_idx]."""
            nonlocal path_obj
            new_pt = ax.c2p(step_idx, walk_a[step_idx])
            path_pts.append(new_pt)
            new_path = VMobject(stroke_color=C_BLUE, stroke_width=2.5,
                                fill_opacity=0)
            new_path.set_points_as_corners(path_pts)
            self.remove(path_obj)
            path_obj = new_path
            self.add(path_obj)
            nl_x = price_to_nl(float(np.clip(walk_a[step_idx], 0, 100)))
            graph_dot_a.move_to(new_pt)
            dot.move_to([nl_x, NL_Y, 0])

        # Slow phase: remove/add path each step, animate dots with self.play
        for i in range(1, min(SLOW_STEPS + 1, n_a)):
            new_pt = ax.c2p(i, walk_a[i])
            path_pts.append(new_pt)
            new_path = VMobject(stroke_color=C_BLUE, stroke_width=2.5,
                                fill_opacity=0)
            new_path.set_points_as_corners(list(path_pts))
            nl_x = price_to_nl(float(np.clip(walk_a[i], 0, 100)))
            self.remove(path_obj)
            path_obj = new_path
            self.add(path_obj)
            self.play(
                graph_dot_a.animate.move_to(new_pt),
                dot.animate.move_to([nl_x, NL_Y, 0]),
                run_time=SLOW_DT,
            )

        # Fast phase: batched, no animation — just jump + wait
        i = SLOW_STEPS + 1
        while i < n_a:
            end = min(i + FAST_CHUNK, n_a - 1)
            for j in range(i, end + 1):
                path_pts.append(ax.c2p(j, walk_a[j]))
            new_path = VMobject(stroke_color=C_BLUE, stroke_width=2.5,
                                fill_opacity=0)
            new_path.set_points_as_corners(list(path_pts))
            self.remove(path_obj)
            path_obj = new_path
            self.add(path_obj)
            nl_x = price_to_nl(float(np.clip(walk_a[end], 0, 100)))
            graph_dot_a.move_to(ax.c2p(end, walk_a[end]))
            dot.move_to([nl_x, NL_Y, 0])
            self.wait(FAST_DT * FAST_CHUNK)
            i = end + 1

        # Flash green — hit
        dot.set_color(C_GREEN)
        dot.move_to([price_to_nl(100), NL_Y, 0])
        hit_flash = Dot(ax.c2p(T_hit_a, STRIKE), radius=0.14, color=C_GREEN)
        self.play(FadeIn(hit_flash, scale=1.5), run_time=0.2)
        self.play(hit_flash.animate.scale(1.4), run_time=0.15)
        self.play(hit_flash.animate.scale(1/1.4), run_time=0.15)

        hit_cap = Text("Option Pays Out", font_size=19,
                       color=C_GREEN, weight=BOLD)
        hit_cap.move_to([price_to_nl(50), NL_Y - 1.2, 0])
        self.play(FadeIn(hit_cap)); self.wait(1.8)

        # Reset
        self.play(
            FadeOut(hit_cap),
            FadeOut(path_obj), FadeOut(graph_dot_a), FadeOut(hit_flash),
            dot.animate.move_to([price_to_nl(START), NL_Y, 0]).set_color(C_YELLOW),
            run_time=0.4,
        )
        self.wait(0.3)

        # ─────────────────────────────────────────────
        # SIM B — fast only, same sync logic
        # ─────────────────────────────────────────────
        graph_dot_b = Dot(ax.c2p(0, walk_b[0]), radius=0.09, color=C_RED)
        self.add(graph_dot_b)

        path_pts_b = [ax.c2p(0, walk_b[0])]
        path_obj_b = VMobject(stroke_color=C_RED, stroke_width=2.5, fill_opacity=0)
        path_obj_b.set_points_as_corners([ax.c2p(0, walk_b[0]),
                                          ax.c2p(0, walk_b[0])])
        self.add(path_obj_b)

        i = 1
        while i < n_b:
            end = min(i + FAST_CHUNK, n_b - 1)
            for j in range(i, end + 1):
                path_pts_b.append(ax.c2p(j, walk_b[j]))
            new_path_b = VMobject(stroke_color=C_RED, stroke_width=2.5,
                                  fill_opacity=0)
            new_path_b.set_points_as_corners(list(path_pts_b))
            self.remove(path_obj_b)
            path_obj_b = new_path_b
            self.add(path_obj_b)
            nl_x = price_to_nl(float(np.clip(walk_b[end], 0, 100)))
            graph_dot_b.move_to(ax.c2p(end, walk_b[end]))
            dot.move_to([nl_x, NL_Y, 0])
            self.wait(FAST_DT * FAST_CHUNK)
            i = end + 1

        # Flash red — expired
        dot.set_color(C_RED)
        expiry_flash = Dot(ax.c2p(N_STEPS, walk_b[N_STEPS]),
                           radius=0.14, color=C_RED)
        self.play(FadeIn(expiry_flash, scale=1.5), run_time=0.2)
        self.play(expiry_flash.animate.scale(1.4), run_time=0.15)
        self.play(expiry_flash.animate.scale(1/1.4), run_time=0.15)

        miss_cap = Text("Option Expires Worthless", font_size=19,
                        color=C_RED, weight=BOLD)
        miss_cap.move_to([price_to_nl(50), NL_Y - 1.2, 0])
        self.play(FadeIn(miss_cap)); self.wait(1.8)
        self.play(FadeOut(miss_cap)); self.wait(0.4)

        # ─────────────────────────────────────────────
        # HITTING PROBABILITY CAPTION — right side
        # ─────────────────────────────────────────────
        hit_prob = Text(
            "Probability of payout\n = A Hitting Probability.",
            font_size=19, color=C_DARK, line_spacing=1.3,
        )
        hit_prob.move_to(RIGHT * 3.5 + DOWN * 2.8)
        self.play(FadeIn(hit_prob, shift=UP * 0.1)); self.wait(2.5)
        self.play(FadeOut(hit_prob)); self.wait(5)
        # ─────────────────────────────────────────────
        # DISCOUNTED STOCK PRICE — right side
        # ─────────────────────────────────────────────
        disc_lbl = Text("In reality, the martingale is:",
                        font_size=19, color=C_GREY)
        disc_eq  = MathTex(
            r"\tilde{S}_t = e^{-rt} S_t",
            font_size=EQ_FS, color=C_DARK,
        )
        disc_sub = Text("the discounted stock price.",
                        font_size=17, color=C_GREY)
        disc_group = VGroup(disc_lbl, disc_eq, disc_sub)
        disc_group.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        disc_group.move_to(RIGHT * 3.2 + DOWN * 2.0)

        self.play(FadeIn(disc_lbl))
        self.play(FadeIn(disc_eq, scale=0.9)); self.wait(0.5)
        self.play(FadeIn(disc_sub))
        self.wait(5)
        self.play(FadeOut(disc_group)); self.wait(0.3)

        # ─────────────────────────────────────────────
        # BLACK-SCHOLES — right side
        # ─────────────────────────────────────────────
        bs_lbl = Text("Black–Scholes:", font_size=19, color=C_GREY)
        bs_eq  = MathTex(
            r"C = S_0\,N(d_1) - K e^{-rT} N(d_2)",
            font_size=EQ_FS - 4, color=C_DARK,
        )
        bs_sub = Text("Optional Stopping Theorem,\nWith A Risk-Free Rate.",
                      font_size=17, color=C_GREY, line_spacing=1.3)
        bs_group = VGroup(bs_lbl, bs_eq, bs_sub)
        bs_group.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        bs_group.move_to(RIGHT * 3.2 + DOWN * 2.0)

        self.play(FadeIn(bs_lbl))
        self.play(FadeIn(bs_eq, scale=0.9)); self.wait(0.5)
        self.play(FadeIn(bs_sub))
        self.wait(HOLD_TIME)
# ═══════════════════════════════════════════════════════════════
# CLOSING
# ═══════════════════════════════════════════════════════════════

class Closing_SummaryLines(Scene):
    """
    SCRIPT CUE: [Four lines appear one at a time. Fade out. Thank you.]
    """
    def construct(self):
        self.camera.background_color = BG
        TITLE_FS  = 44
        LINE_FS   = 32
        LINE_GAP  = 0.6
        LINE_WAIT = 0.8
        HOLD_TIME = 2.5

        title = Text(
            "Martingales: Get Even or Get Even Worse",
            font_size=TITLE_FS,
            color=C_DARK,
            t2c={"[17:21]": C_GREEN, "[29:39]": C_RED}
        )
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title))
        summary_lines = [
            "Random walks",
            "Stopping time distributions,",
            "Brownian motion,",
            "and the trillion-dollar derivatives markets.",
        ]

        line_objects = VGroup()
        for i, text in enumerate(summary_lines):
            t = Text(text, font_size=LINE_FS - 4, color=C_DARK)
            if i == 0:
                t.next_to(title, DOWN, buff=0.8)
            else:
                t.next_to(line_objects[-1], DOWN, buff=LINE_GAP)
            t.set_x(0)
            line_objects.add(t)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=1)
            self.wait(LINE_WAIT)

        self.wait(HOLD_TIME)
        self.play(FadeOut(line_objects))
        self.wait(1.2)

        thank_you = Text("Thank you.", font_size=TITLE_FS, color=C_DARK)
        thank_you.move_to(ORIGIN)
        self.play(FadeIn(thank_you, shift=UP * 0.1))
        self.wait(3.0)