"""
experiment_statistical_rigor.py — Phase 4: Multi-Seed Statistical Validation
=============================================================================
Runs Simulated Annealing (SA) and Genetic Algorithm (GA) across 10 fixed
reproducible random seeds (Fibonacci sequence: [1, 2, 3, 5, 8, 13, 21, 34, 55, 89])
to prevent random seed cherry-picking and data leakage.

Reports results as:
  Mean ± Standard Deviation
Computes exact statistical Optimality Gap (%) on Tier 1 micro-instances:
  Gap(%) = ((Cost_algo - Cost_A*) / Cost_A*) * 100%
"""

import os
import json
import math
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

SEEDS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]  # 10 fixed seeds


def mean_and_std(values: List[float]) -> Tuple[float, float]:
    n = len(values)
    if n == 0:
        return 0.0, 0.0
    m = sum(values) / n
    var = sum((x - m) ** 2 for x in values) / (n - 1) if n > 1 else 0.0
    return m, math.sqrt(var)


def run_statistical_experiment():
    print("=" * 80)
    print(f"EXPERIMENT 4.4: STATISTICAL RIGOR ACROSS {len(SEEDS)} REPRODUCIBLE SEEDS")
    print(f"Seeds: {SEEDS}")
    print("=" * 80)

    # 1. Tier 1 Micro Instances
    print("\n--- Evaluating Tier 1 Micro Instances ---")
    tier1_stats = []

    header = f"| {'Instance':<14} | {'N':<3} | {'A* (Ground Truth)':<18} | {'SA (Mean +/- Std)':<18} | {'SA Gap (%)':<10} | {'GA (Mean +/- Std)':<18} | {'GA Gap (%)':<10} |"
    divider = f"|:{'-'*14}-|-{'-'*3}:|-{'-'*18}:|-{'-'*18}:|-{'-'*10}:|-{'-'*18}:|-{'-'*10}:|"
    print(header)
    print(divider)

    for name, pattern in TIER1_MICRO_PATTERNS.items():
        N = len(pattern)
        res_a = run_astar(pattern)
        j_star = res_a["f_thread"]

        sa_costs = []
        for s in SEEDS:
            r = run_simulated_annealing(pattern, seed=s)
            sa_costs.append(r["f_thread"])

        ga_costs = []
        for s in SEEDS:
            r = run_genetic_algorithm(pattern, generations=60, seed=s)
            ga_costs.append(r["f_thread"])

        sa_m, sa_s = mean_and_std(sa_costs)
        ga_m, ga_s = mean_and_std(ga_costs)

        sa_gap = ((sa_m - j_star) / j_star) * 100.0
        ga_gap = ((ga_m - j_star) / j_star) * 100.0

        sa_str = f"{sa_m:.2f} +/- {sa_s:.2f}"
        ga_str = f"{ga_m:.2f} +/- {ga_s:.2f}"

        row = f"| {name:<14} | {N:<3} | {j_star:18.2f} | {sa_str:<18} | {sa_gap:9.2f}% | {ga_str:<18} | {ga_gap:9.2f}% |"
        print(row)

        tier1_stats.append({
            "instance": name,
            "N": N,
            "astar_j_star": j_star,
            "sa_mean": sa_m,
            "sa_std": sa_s,
            "sa_gap_pct": sa_gap,
            "ga_mean": ga_m,
            "ga_std": ga_s,
            "ga_gap_pct": ga_gap,
            "sa_raw": sa_costs,
            "ga_raw": ga_costs,
        })

    # 2. Tier 2 Medium Instances
    print("\n--- Evaluating Tier 2 Medium Sprite Instances ---")
    sprite_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("sprite_") and f.endswith(".png")])
    tier2_stats = []

    header2 = f"| {'Sprite Instance':<22} | {'N':<3} | {'SA Thread (Mean +/- Std)':<25} | {'GA Thread (Mean +/- Std)':<25} |"
    divider2 = f"|:{'-'*22}-|-{'-'*3}:|-{'-'*25}:|-{'-'*25}:|"
    print(header2)
    print(divider2)

    for fname in sprite_files:
        path = os.path.join(DATA_DIR, fname)
        stitches = load_pattern_from_image(path, normalize_origin=True)
        name = fname.replace(".png", "")
        N = len(stitches)

        sa_costs = []
        for s in SEEDS:
            r = run_simulated_annealing(stitches, seed=s, alpha=0.992)
            sa_costs.append(r["f_thread"])

        ga_costs = []
        for s in SEEDS:
            r = run_genetic_algorithm(stitches, generations=60, pop_size=40, seed=s)
            ga_costs.append(r["f_thread"])

        sa_m, sa_s = mean_and_std(sa_costs)
        ga_m, ga_s = mean_and_std(ga_costs)

        sa_str = f"{sa_m:.2f} +/- {sa_s:.2f}"
        ga_str = f"{ga_m:.2f} +/- {ga_s:.2f}"

        row = f"| {name:<22} | {N:<3} | {sa_str:<24} | {ga_str:<24} |"
        print(row)

        tier2_stats.append({
            "instance": name,
            "N": N,
            "sa_mean": sa_m,
            "sa_std": sa_s,
            "ga_mean": ga_m,
            "ga_std": ga_s,
            "sa_raw": sa_costs,
            "ga_raw": ga_costs,
        })

    # Save complete JSON
    out_path = os.path.join(RESULTS_DIR, "statistical_rigor_summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "seeds": SEEDS,
            "tier1_micro": tier1_stats,
            "tier2_medium": tier2_stats,
        }, f, indent=2)
    print(f"\nSaved statistical summary to: {out_path}")


if __name__ == "__main__":
    from typing import Tuple
    run_statistical_experiment()
