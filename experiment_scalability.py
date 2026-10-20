"""
experiment_scalability.py — Phase 4: Scalability & Complexity Verification
==========================================================================
Empirically profiles algorithm runtime across increasing pattern size N:
  - Exact A* Search: N in [4, 6, 8, 10, 12, 14, 16]
  - Simulated Annealing (SA): N in [8, 14, 50, 116, 138, 170]
  - Genetic Algorithm (GA): N in [8, 14, 50, 116, 138, 170]

Generates dual-panel plot:
  - Left panel: Linear runtime (seconds) vs N
  - Right panel: Logarithmic runtime (log10 seconds) vs N
Demonstrates the exponential wall of exact search vs polynomial scaling of metaheuristics.
"""

import os
import time
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List, Dict, Any

from sample_patterns import TIER1_MICRO_PATTERNS
from parser import load_pattern_from_image
from search_astar import run_astar
from search_sa import run_simulated_annealing
from search_ga import run_genetic_algorithm

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "benchmark_results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def get_sub_pattern(full_pattern: List[Dict[str, Any]], target_n: int) -> List[Dict[str, Any]]:
    """Extracts a contiguous sub-pattern of exact size target_n."""
    sub = full_pattern[:target_n].copy()
    for i, s in enumerate(sub):
        sub[i] = {"id": i, "x": s["x"], "y": s["y"], "color": s["color"]}
    return sub


def run_scalability_experiment():
    print("=" * 80)
    print("EXPERIMENT 4.3: RUNTIME COMPLEXITY & SCALABILITY VERIFICATION")
    print("=" * 80)

    # Base large pattern to slice from
    base_pattern = load_pattern_from_image(os.path.join(DATA_DIR, "sprite_shield_16x16.png"), normalize_origin=True)

    # 1. A* scaling (N = 4 to 15, plus attempt at 16 with timeout)
    astar_n_vals = [4, 6, 8, 10, 12, 14, 15]
    astar_times = []
    astar_nodes = []

    print("\n--- Profiling A* Search ---")
    for n in astar_n_vals:
        sub = get_sub_pattern(base_pattern, n)
        t0 = time.perf_counter()
        res = run_astar(sub)
        elapsed = time.perf_counter() - t0
        astar_times.append(elapsed)
        astar_nodes.append(res["nodes_expanded"])
        print(f"  A* [N={n:2d}]: {elapsed:7.4f}s | Nodes expanded: {res['nodes_expanded']:7d}")

    # 2. SA & GA scaling (N = 8, 14, 50, 116, 138, 170)
    meta_n_vals = [8, 14, 50, 116, 138, 170]
    sa_times = []
    ga_times = []

    print("\n--- Profiling Simulated Annealing & Genetic Algorithm ---")
    for n in meta_n_vals:
        sub = get_sub_pattern(base_pattern, n)
        
        # SA
        t0 = time.perf_counter()
        res_sa = run_simulated_annealing(sub, seed=42, alpha=0.992)
        elapsed_sa = time.perf_counter() - t0
        sa_times.append(elapsed_sa)

        # GA
        t0 = time.perf_counter()
        res_ga = run_genetic_algorithm(sub, generations=60, pop_size=40, seed=42)
        elapsed_ga = time.perf_counter() - t0
        ga_times.append(elapsed_ga)

        print(f"  Metaheuristics [N={n:3d}]: SA = {elapsed_sa:6.3f}s | GA = {elapsed_ga:6.3f}s")

    # 3. Plotting Dual-Panel Curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Linear Scale
    ax1.plot(astar_n_vals, astar_times, "r-o", linewidth=2.2, label="A* Search (Exact)")
    ax1.plot(meta_n_vals, sa_times, "b-s", linewidth=2.0, label="Simulated Annealing (SA)")
    ax1.plot(meta_n_vals, ga_times, "g-^", linewidth=2.0, label="Genetic Algorithm (GA)")
    ax1.axvline(x=15, color="red", linestyle="--", alpha=0.7, label="A* Practical Memory Wall (N=15)")
    ax1.set_title("Runtime vs Pattern Size N (Linear Scale)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Pattern Size N (stitches)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Runtime (seconds)", fontsize=10, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=9)

    # Right: Logarithmic Scale
    ax2.semilogy(astar_n_vals, astar_times, "r-o", linewidth=2.2, label="A* Search (O(b^d))")
    ax2.semilogy(meta_n_vals, sa_times, "b-s", linewidth=2.0, label="Simulated Annealing (O(k·N))")
    ax2.semilogy(meta_n_vals, ga_times, "g-^", linewidth=2.0, label="Genetic Algorithm (O(G·P·N))")
    ax2.axvline(x=15, color="red", linestyle="--", alpha=0.7, label="A* Cutoff (N=15)")
    ax2.set_title("Runtime vs Pattern Size N (Logarithmic Scale)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Pattern Size N (stitches)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Runtime (log10 seconds)", fontsize=10, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    save_path = os.path.join(RESULTS_DIR, "scalability_runtime_curve.png")
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved Scalability Plot: {save_path}")

    # Save JSON summary
    summary = {
        "astar": {"N": astar_n_vals, "runtime_sec": astar_times, "nodes": astar_nodes},
        "sa": {"N": meta_n_vals, "runtime_sec": sa_times},
        "ga": {"N": meta_n_vals, "runtime_sec": ga_times},
    }
    json_path = os.path.join(RESULTS_DIR, "scalability_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved scalability data: {json_path}")


if __name__ == "__main__":
    run_scalability_experiment()
