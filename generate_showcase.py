"""
generate_showcase.py — Phase 5: Visual Demonstration Showcase Generator
=======================================================================
Generates high-impact presentation visuals:
  1. Side-by-side comparative trajectory panels (Baseline 1 vs B2 vs B4 vs SA).
  2. Animated GIF demonstrating Simulated Annealing untangling a path over cooling.
"""

import os
import io
import math
import random
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sample_patterns import TOY_PATTERN_10
from parser import load_pattern_from_image
from evaluator import evaluate_order, DEFAULT_D_MAX, DEFAULT_C_TRIM
from baseline_raster import solve_raster_scan
from baseline_color_scan import solve_color_scan
from baseline_uncolored_tsp import solve_uncolored_2opt_tsp
from search_sa import SimulatedAnnealingMCCPO
from visualizer import _color_for

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
SHOWCASE_DIR = os.path.join(BASE_DIR, "showcase")
os.makedirs(SHOWCASE_DIR, exist_ok=True)


def generate_side_by_side_comparison(pattern_name: str = "sprite_flower_16x16"):
    """
    Creates a 4-panel side-by-side trajectory comparison:
      [Top-Left]  Baseline 1: Standard Raster Scan (High switch chaos)
      [Top-Right] Baseline 4: Uncolored 2-Opt TSP (Geometric crossing chaos)
      [Bottom-Left] Baseline 2: Color-by-Color (Rigid color blocks)
      [Bottom-Right] Simulated Annealing (Optimized Pareto compromise)
    """
    img_path = os.path.join(DATA_DIR, f"{pattern_name}.png")
    stitches = load_pattern_from_image(img_path, normalize_origin=True)
    N = len(stitches)
    stitch_by_id = {s["id"]: s for s in stitches}

    # Solve with all 4 methods
    order_b1 = solve_raster_scan(stitches)
    order_b4 = solve_uncolored_2opt_tsp(stitches)
    order_b2 = solve_color_scan(stitches)
    
    sa_solver = SimulatedAnnealingMCCPO(stitches, seed=42, alpha=0.992)
    sa_res = sa_solver.search(init_method="color_scan")
    order_sa = sa_res["order"]

    methods = [
        ("Baseline 1: Raster Scan", order_b1),
        ("Baseline 4: Uncolored 2-Opt TSP", order_b4),
        ("Baseline 2: Color-by-Color", order_b2),
        ("Simulated Annealing (SA Optimized)", order_sa),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    axes = axes.flatten()

    for idx, (title, order) in enumerate(methods):
        ax = axes[idx]
        ax.set_aspect("equal")
        ax.invert_yaxis()

        eval_res = evaluate_order(stitches, order)
        transitions = eval_res["transitions"]

        # Draw transitions
        for t in transitions:
            s_from = stitch_by_id[t["from_id"]]
            s_to = stitch_by_id[t["to_id"]]
            action = t.get("action", t.get("type"))
            if action == "CONTINUOUS_CARRY":
                c = _color_for(t.get("from_color", s_from["color"]))
                ax.plot([s_from["x"], s_to["x"]], [s_from["y"], s_to["y"]],
                        color=c, linewidth=1.4, alpha=0.75, zorder=1)
            else:
                ax.plot([s_from["x"], s_to["x"]], [s_from["y"], s_to["y"]],
                        color="red", linewidth=1.1, linestyle="--", alpha=0.6, dashes=(3, 3), zorder=1)

        # Draw stitch points
        for s in stitches:
            c = _color_for(s["color"])
            ax.scatter(s["x"], s["y"], color=c, s=55, edgecolors="black", linewidths=0.3, marker="s", zorder=3)

        # Start position
        s0 = stitch_by_id[order[0]]
        ax.scatter(s0["x"], s0["y"], marker="*", s=220, color="gold", edgecolors="black", linewidths=0.8, zorder=5)

        subtitle = f"{title}\nf_thread = {eval_res['f_thread']:.1f} | f_switch = {eval_res['f_switch']} | Cuts = {eval_res['cut_tie_count']}"
        ax.set_title(subtitle, fontsize=11, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.3)

    plt.suptitle(f"MCCPO Trajectory Comparison: {pattern_name} (N={N})", fontsize=15, fontweight="bold", y=0.99)
    plt.tight_layout()
    out_path = os.path.join(SHOWCASE_DIR, f"showcase_comparison_{pattern_name}.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved side-by-side comparison: {out_path}")


def generate_sa_cooling_animation(pattern_name: str = "smiley_13", num_snapshots: int = 16):
    """
    Generates an animated GIF capturing the Simulated Annealing trajectory
    as it cools from high-temperature chaos to optimal convergence.
    """
    if pattern_name == "smiley_13":
        stitches = TOY_PATTERN_10  # use toy pattern or smiley
    else:
        stitches = load_pattern_from_image(os.path.join(DATA_DIR, f"{pattern_name}.png"), normalize_origin=True)

    N = len(stitches)
    stitch_by_id = {s["id"]: s for s in stitches}

    # Start from random permutation to clearly show untangling
    curr_order = list(range(N))
    random.seed(42)
    random.shuffle(curr_order)

    solver = SimulatedAnnealingMCCPO(stitches, t_start=60.0, alpha=0.990, seed=42)
    curr_cost, curr_eval = solver._cost(curr_order)

    snapshots = [(curr_order.copy(), solver.t_start, curr_cost, curr_eval)]

    t = solver.t_start
    step_count = 0
    record_interval = 200

    while t > solver.t_min and len(snapshots) < num_snapshots:
        for _ in range(solver.steps_per_temp):
            step_count += 1
            cand_order = solver._neighbor(curr_order)
            cand_cost, cand_eval = solver._cost(cand_order)
            delta = cand_cost - curr_cost

            if delta <= 0 or random.random() < math.exp(-delta / t):
                curr_order = cand_order
                curr_cost = cand_cost
                curr_eval = cand_eval

            if step_count % record_interval == 0:
                snapshots.append((curr_order.copy(), t, curr_cost, curr_eval))
                if len(snapshots) >= num_snapshots - 1:
                    break
        t *= solver.alpha

    # Add final best state
    snapshots.append((curr_order.copy(), t, curr_cost, curr_eval))

    frames = []
    print(f"Rendering {len(snapshots)} animation frames for SA cooling...")

    for frame_idx, (order, temp, cost, eval_res) in enumerate(snapshots):
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.set_aspect("equal")
        ax.invert_yaxis()

        transitions = eval_res["transitions"]
        for tr in transitions:
            s_from = stitch_by_id[tr["from_id"]]
            s_to = stitch_by_id[tr["to_id"]]
            action = tr.get("action", tr.get("type"))
            if action == "CONTINUOUS_CARRY":
                c = _color_for(tr.get("from_color", s_from["color"]))
                ax.plot([s_from["x"], s_to["x"]], [s_from["y"], s_to["y"]],
                        color=c, linewidth=1.8, alpha=0.8, zorder=1)
            else:
                ax.plot([s_from["x"], s_to["x"]], [s_from["y"], s_to["y"]],
                        color="red", linewidth=1.3, linestyle="--", alpha=0.7, dashes=(4, 4), zorder=1)

        for s in stitches:
            c = _color_for(s["color"])
            ax.scatter(s["x"], s["y"], color=c, s=120, edgecolors="black", linewidths=0.5, marker="s", zorder=3)
            ax.annotate(str(s["id"]), (s["x"], s["y"]), fontsize=6, ha="center", va="center",
                        color="white", fontweight="bold", zorder=4)

        ax.set_title(f"Simulated Annealing Cooling (Frame {frame_idx+1}/{len(snapshots)})\nTemp T={temp:.2f} | Cost={cost:.1f} | Switches={eval_res['f_switch']}",
                     fontsize=11, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).copy())
        buf.close()

    gif_path = os.path.join(SHOWCASE_DIR, "sa_path_untangling_showcase.gif")
    if frames:
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=350,
            loop=0
        )
        print(f"Saved SA Cooling Animation: {gif_path}")


if __name__ == "__main__":
    generate_side_by_side_comparison("sprite_flower_16x16")
    generate_sa_cooling_animation("smiley_13")
