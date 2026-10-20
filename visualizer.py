"""
visualizer.py — 2D Trajectory Visualizer for MCCPO
=====================================================
Renders a stitching trajectory on a 2D grid:
  - Colored squares/X markers for each stitch.
  - Solid thin lines for Continuous Carry moves.
  - Dashed red lines for Cut & Tie-off jumps.

Usage:
    from visualizer import visualize_trajectory
    result = evaluate_sequence(stitches, order, ...)
    visualize_trajectory(stitches, result["transitions"], title="My Run")
"""

import matplotlib
matplotlib.use("Agg")   # non-interactive backend; change to "TkAgg" if you want a popup
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


# ---------------------------------------------------------------------------
# Color palette (maps color label → hex display color)
# ---------------------------------------------------------------------------

_DISPLAY_COLORS = [
    "#E53935",  # color_0 — red
    "#1E88E5",  # color_1 — blue
    "#43A047",  # color_2 — green
    "#FB8C00",  # color_3 — orange
    "#8E24AA",  # color_4 — purple
    "#F4511E",  # color_5 — deep-orange
    "#00ACC1",  # color_6 — cyan
    "#FFB300",  # color_7 — amber
]

def _color_for(label):
    """Map 'color_N' label to a display hex color."""
    try:
        idx = int(label.split("_")[-1]) % len(_DISPLAY_COLORS)
    except (ValueError, IndexError):
        idx = 0
    return _DISPLAY_COLORS[idx]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def visualize_trajectory(
    stitches,
    transitions,
    title="Stitching Trajectory",
    save_path=None,
    show=False,
    annotate_ids=True,
):
    """
    Draw the stitching trajectory.

    Parameters
    ----------
    stitches : list of dict
        From sample_patterns.py or parser.py: [{"id", "x", "y", "color"}, ...]
    transitions : list of dict
        From evaluator.py result["transitions"]:
        [{"from_id", "to_id", "type", "cost", "color"}, ...]
    title : str
        Plot title.
    save_path : str or None
        If given, save the figure to this path (PNG recommended).
        Defaults to "<title>.png" in the current directory.
    show : bool
        If True, call plt.show() (requires an interactive backend).
    annotate_ids : bool
        If True, label each stitch with its ID number.

    Returns
    -------
    str
        Path where the figure was saved.
    """
    stitch_by_id = {s["id"]: s for s in stitches}

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    ax.invert_yaxis()   # pixel-art convention: y=0 at top

    # --- Draw transitions first (so markers sit on top) ---
    for t in transitions:
        s_from = stitch_by_id[t["from_id"]]
        s_to   = stitch_by_id[t["to_id"]]
        x0, y0 = s_from["x"], s_from["y"]
        x1, y1 = s_to["x"],   s_to["y"]

        action_type = t.get("action", t.get("type"))
        if action_type == "CONTINUOUS_CARRY":
            c = _color_for(t.get("color", t.get("from_color", s_from["color"])))
            ax.plot([x0, x1], [y0, y1],
                    color=c, linewidth=1.5, alpha=0.7, zorder=1)
        else:  # CUT_AND_TIE
            ax.plot([x0, x1], [y0, y1],
                    color="red", linewidth=1.2, linestyle="--",
                    alpha=0.6, dashes=(4, 4), zorder=1)

    # --- Draw stitch markers ---
    for s in stitches:
        c = _color_for(s["color"])
        ax.scatter(s["x"], s["y"], color=c, s=120, zorder=3,
                   edgecolors="black", linewidths=0.5, marker="s")
        if annotate_ids:
            ax.annotate(
                str(s["id"]),
                (s["x"], s["y"]),
                fontsize=6, ha="center", va="center",
                color="white", fontweight="bold", zorder=4,
            )

    # --- Mark start / end ---
    if stitches:
        s0 = stitch_by_id[transitions[0]["from_id"]] if transitions else stitches[0]
        ax.scatter(s0["x"], s0["y"], marker="*", s=300,
                   color="gold", edgecolors="black", linewidths=0.8, zorder=5)

    # --- Legend ---
    legend_items = []
    seen_colors = {}
    for s in stitches:
        lbl = s["color"]
        if lbl not in seen_colors:
            seen_colors[lbl] = _color_for(lbl)
            legend_items.append(
                mpatches.Patch(color=seen_colors[lbl], label=lbl)
            )
    legend_items += [
        plt.Line2D([0], [0], color="gray",   linewidth=1.5, label="Continuous Carry"),
        plt.Line2D([0], [0], color="red",    linewidth=1.2, linestyle="--",
                   dashes=(4, 4), label="Cut & Tie-off"),
        plt.Line2D([0], [0], marker="*", color="gold", markersize=10,
                   linestyle="None", label="Start"),
    ]
    ax.legend(handles=legend_items, loc="upper right", fontsize=8)

    # --- Labels & grid ---
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("x (column)")
    ax.set_ylabel("y (row)")
    ax.grid(True, linewidth=0.4, alpha=0.4)

    # --- Save ---
    if save_path is None:
        safe_name = title.replace(" ", "_").replace("/", "-")
        save_path = f"{safe_name}.png"
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {save_path}")
    return save_path


def export_animation(
    stitches,
    transitions,
    output_path="trajectory.gif",
    title_prefix="Step",
    duration=300,
    annotate_ids=True,
):
    """
    Exports a step-by-step animated GIF showing the path development.
    Uses PIL to assemble in-memory rendered frames into a single .gif file.
    """
    import io
    from PIL import Image

    stitch_by_id = {s["id"]: s for s in stitches}
    frames = []

    # Total frames = initial state (step 0) + 1 frame per transition
    total_steps = len(transitions)
    for step in range(total_steps + 1):
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.set_aspect("equal")
        ax.invert_yaxis()

        # Transitions up to current step
        for t in transitions[:step]:
            s_from = stitch_by_id[t["from_id"]]
            s_to   = stitch_by_id[t["to_id"]]
            action_type = t.get("action", t.get("type"))
            if action_type == "CONTINUOUS_CARRY":
                c = _color_for(t.get("color", t.get("from_color", s_from["color"])))
                ax.plot([s_from["x"], s_to["x"]], [s_from["y"], s_to["y"]],
                        color=c, linewidth=1.8, alpha=0.8, zorder=1)
            else:
                ax.plot([s_from["x"], s_to["x"]], [s_from["y"], s_to["y"]],
                        color="red", linewidth=1.4, linestyle="--",
                        alpha=0.7, dashes=(4, 4), zorder=1)

        # Draw all stitch markers
        for s in stitches:
            c = _color_for(s["color"])
            ax.scatter(s["x"], s["y"], color=c, s=120, zorder=3,
                       edgecolors="black", linewidths=0.5, marker="s")
            if annotate_ids:
                ax.annotate(str(s["id"]), (s["x"], s["y"]),
                            fontsize=6, ha="center", va="center",
                            color="white", fontweight="bold", zorder=4)

        # Highlight current needle position
        if step > 0:
            curr_s = stitch_by_id[transitions[step - 1]["to_id"]]
            ax.scatter(curr_s["x"], curr_s["y"], marker="o", s=250,
                       facecolors="none", edgecolors="lime", linewidths=2.5, zorder=5)

        ax.set_title(f"{title_prefix} {step}/{total_steps}", fontsize=11, fontweight="bold")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, linewidth=0.3, alpha=0.4)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).copy())
        buf.close()

    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
        print(f"Animated GIF saved: {output_path} ({len(frames)} frames)")
    return output_path



# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from sample_patterns import TOY_PATTERN_10
    from evaluator import evaluate_order

    stitches = TOY_PATTERN_10
    order = list(range(len(stitches)))  # identity order

    result = evaluate_order(stitches, order)
    out = visualize_trajectory(
        stitches,
        result["transitions"],
        title="TOY_PATTERN_10 Identity Order",
        save_path="test_visualizer_output.png",
    )
    print(f"f_thread={result['f_thread']:.3f}  f_switch={result['f_switch']}")
    print("Self-test passed.")
