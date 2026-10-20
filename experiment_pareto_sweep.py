"""
experiment_pareto_sweep.py — Phase 4: Pareto Trade-off & Parameter Sweep Engine
==============================================================================
Sweeps C_trim in {1, 2, 5, 10, 20, 50} and trade-off weights to construct
empirical Pareto Frontier trade-off curves:
  - X-axis: f_thread (Total thread consumed: distance + trim waste)
  - Y-axis: f_switch (Discrete color changes / human re-threading stops)

Evaluates and overlays:
  - Baseline 1: Standard Raster Scan
  - Baseline 2: Color-by-Color Scan
  - Baseline 3: Spatial Greedy NN
  - Baseline 4: Uncolored 2-Opt TSP
  - Simulated Annealing (Multi-operator metaheuristic)
  - Genetic Algorithm (OX1 crossover metaheuristic)
"""

import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List, Dict, Any

from sample_patterns import TIER1_MICRO_PATTERNS
from parser import load_pattern_from_image
from baseline_raster import run_baseline_raster
from baseline_color_scan import run_baseline_color_scan
from baseline_greedy import run_baseline_greedy
from baseline_uncolored_tsp import run_baseline_uncolored_tsp
from search_sa import run_simulated_annealing
from search_ga import run_genetic_algorithm

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "benchmark_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

C_TRIM_VALUES = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
ALGO_STYLES = {
    "B1: Raster Scan": {"color": "#9E9E9E", "marker": "x", "linestyle": ":", "label": "B1: Raster Scan"},
    "B2: Color-by-Color": {"color": "#2196F3", "marker": "s", "linestyle": "--", "label": "B2: Color-by-Color"},
    "B3: Greedy NN": {"color": "#FF9800", "marker": "^", "linestyle": ":", "label": "B3: Greedy NN"},
    "B4: Uncolored 2-Opt": {"color": "#9C27B0", "marker": "d", "linestyle": "-.", "label": "B4: Uncolored 2-Opt"},
    "Simulated Annealing": {"color": "#E91E63", "marker": "o", "linestyle": "-", "label": "Simulated Annealing (SA)"},
    "Genetic Algorithm": {"color": "#4CAF50", "marker": "*", "linestyle": "-", "label": "Genetic Algorithm (GA)"},
}


def run_pareto_sweep_on_pattern(pattern_name: str, stitches: List[Dict[str, Any]]) -> Dict[str, Any]:
    print(f"\n---> Running Pareto Parameter Sweep on '{pattern_name}' (N={len(stitches)})")
    pattern_records = {algo: [] for algo in ALGO_STYLES.keys()}

    for c_trim in C_TRIM_VALUES:
        print(f"  Evaluating C_trim = {c_trim:4.1f}...", end=" ", flush=True)

        # Baselines
        r_b1 = run_baseline_raster(stitches, c_trim=c_trim)
        pattern_records["B1: Raster Scan"].append((r_b1["f_thread"], r_b1["f_switch"], c_trim))

        r_b2 = run_baseline_color_scan(stitches, c_trim=c_trim)
        pattern_records["B2: Color-by-Color"].append((r_b2["f_thread"], r_b2["f_switch"], c_trim))

        r_b3 = run_baseline_greedy(stitches, c_trim=c_trim)
        pattern_records["B3: Greedy NN"].append((r_b3["f_thread"], r_b3["f_switch"], c_trim))

        r_b4 = run_baseline_uncolored_tsp(stitches, c_trim=c_trim)
        pattern_records["B4: Uncolored 2-Opt"].append((r_b4["f_thread"], r_b4["f_switch"], c_trim))

        # SA and GA: evaluate with trade-off parameter
        weight_switch = c_trim  # In bi-objective optimization, switch weight scales with trim cost
        r_sa = run_simulated_annealing(stitches, c_trim=c_trim, weight_switch=weight_switch, seed=42, alpha=0.992)
        pattern_records["Simulated Annealing"].append((r_sa["f_thread"], r_sa["f_switch"], c_trim))

        r_ga = run_genetic_algorithm(stitches, c_trim=c_trim, weight_switch=weight_switch, generations=70, seed=42)
        pattern_records["Genetic Algorithm"].append((r_ga["f_thread"], r_ga["f_switch"], c_trim))

        print("Done.")

    return pattern_records


def plot_pareto_curves(pattern_name: str, N: int, records: Dict[str, Any], save_path: str):
    fig, ax = plt.subplots(figsize=(9, 7))

    for algo_name, data in records.items():
        style = ALGO_STYLES[algo_name]
        threads = [pt[0] for pt in data]
        switches = [pt[1] for pt in data]
        
        ax.plot(
            threads,
            switches,
            marker=style["marker"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=2.0,
            markersize=8,
            label=style["label"],
            alpha=0.85
        )

        # Annotate C_trim points on SA and GA
        if algo_name in ["Simulated Annealing", "B2: Color-by-Color"]:
            for pt in [data[0], data[-1]]:
                ax.annotate(
                    f"C={pt[2]:.0f}",
                    (pt[0], pt[1]),
                    textcoords="offset points",
                    xytext=(0, 7),
                    ha="center",
                    fontsize=7,
                    fontweight="bold",
                    color=style["color"]
                )

    ax.set_title(f"Pareto Trade-off Frontier: {pattern_name} (N={N})\nSweeping C_trim in [1, 50]", fontsize=13, fontweight="bold")
    ax.set_xlabel("Thread Consumption (f_thread: distance + trim penalty)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Discrete Color Switches (f_switch: manual re-threadings)", fontsize=11, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved Pareto Frontier Plot: {save_path}")


def run_experiment_pareto():
    print("=" * 80)
    print("EXPERIMENT 4.1 & 4.2: PARETO TRADE-OFF PARAMETER SWEEPS")
    print("=" * 80)

    # 1. Representative Micro Instance: smiley_13 (N=13)
    p_smiley = TIER1_MICRO_PATTERNS["smiley_13"]
    rec_smiley = run_pareto_sweep_on_pattern("smiley_13", p_smiley)
    plot_pareto_curves("smiley_13", len(p_smiley), rec_smiley, os.path.join(RESULTS_DIR, "pareto_curve_smiley_13.png"))

    # 2. Representative Medium Instance: sprite_flower_16x16 (N=116)
    p_flower = load_pattern_from_image(os.path.join(DATA_DIR, "sprite_flower_16x16.png"), normalize_origin=True)
    rec_flower = run_pareto_sweep_on_pattern("sprite_flower_16x16", p_flower)
    plot_pareto_curves("sprite_flower_16x16", len(p_flower), rec_flower, os.path.join(RESULTS_DIR, "pareto_curve_sprite_flower.png"))

    # Save summary JSON
    summary_path = os.path.join(RESULTS_DIR, "pareto_sweep_data.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "c_trim_values": C_TRIM_VALUES,
            "smiley_13": {k: [list(item) for item in v] for k, v in rec_smiley.items()},
            "sprite_flower_16x16": {k: [list(item) for item in v] for k, v in rec_flower.items()},
        }, f, indent=2)
    print(f"Saved complete Pareto sweep data to: {summary_path}")


if __name__ == "__main__":
    run_experiment_pareto()
