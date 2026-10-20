"""
benchmark_search.py — Comprehensive Search Algorithm Benchmark Engine
====================================================================
Evaluates A* Search, Simulated Annealing, and Genetic Algorithm across:
  - Tier 1 Micro-Benchmarks (N <= 15): Computes exact Optimality Gap (%) vs A* ground truth.
  - Tier 2 Medium Sprites (N = 50 ~ 200): Evaluates scalable metaheuristics (SA, GA).
"""

import os
import json
import time
from typing import List, Dict, Any

from sample_patterns import TIER1_MICRO_PATTERNS
from parser import load_pattern_from_image
from search_astar import run_astar
from search_sa import run_simulated_annealing
from search_ga import run_genetic_algorithm
from baseline_color_scan import run_baseline_color_scan

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "benchmark_results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_tier1_micro_benchmarks():
    print("=" * 95)
    print("TIER 1 MICRO-VALIDATION: A* (GROUND TRUTH) vs SA vs GA (N <= 15)")
    print("=" * 95)

    header = f"| {'Pattern':<14} | {'N':<3} | {'A* Opt J*':<10} | {'Nodes':<7} | {'SA Cost':<10} | {'SA Gap':<8} | {'GA Cost':<10} | {'GA Gap':<8} |"
    divider = f"|:{'-'*14}-|-{'-'*3}:|-{'-'*10}:|-{'-'*7}:|-{'-'*10}:|-{'-'*8}:|-{'-'*10}:|-{'-'*8}:|"
    print(header)
    print(divider)

    tier1_results = []

    for name, pattern in TIER1_MICRO_PATTERNS.items():
        N = len(pattern)

        # 1. A* Exact Search
        res_astar = run_astar(pattern)
        j_star = res_astar["f_thread"]
        nodes_exp = res_astar["nodes_expanded"]

        # 2. Simulated Annealing
        res_sa = run_simulated_annealing(pattern, seed=42)
        j_sa = res_sa["f_thread"]
        gap_sa = ((j_sa - j_star) / j_star) * 100.0

        # 3. Genetic Algorithm
        res_ga = run_genetic_algorithm(pattern, generations=60, seed=42)
        j_ga = res_ga["f_thread"]
        gap_ga = ((j_ga - j_star) / j_star) * 100.0

        row = f"| {name:<14} | {N:<3} | {j_star:10.2f} | {nodes_exp:7d} | {j_sa:10.2f} | {gap_sa:7.2f}% | {j_ga:10.2f} | {gap_ga:7.2f}% |"
        print(row)

        tier1_results.append({
            "name": name,
            "N": N,
            "astar": res_astar,
            "sa": res_sa,
            "ga": res_ga,
            "gap_sa_pct": round(gap_sa, 2),
            "gap_ga_pct": round(gap_ga, 2)
        })

    return tier1_results


def run_tier2_macro_benchmarks():
    print("\n" + "=" * 95)
    print("TIER 2 MACRO-VALIDATION: BASELINE 2 vs SIMULATED ANNEALING vs GENETIC ALGORITHM")
    print("=" * 95)

    header = f"| {'Sprite Instance':<22} | {'N':<3} | {'B2 Thread':<10} | {'SA Thread':<10} | {'SA Imprv':<9} | {'GA Thread':<10} | {'GA Imprv':<9} |"
    divider = f"|:{'-'*22}-|-{'-'*3}:|-{'-'*10}:|-{'-'*10}:|-{'-'*9}:|-{'-'*10}:|-{'-'*9}:|"
    print(header)
    print(divider)

    sprite_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("sprite_") and f.endswith(".png")])
    tier2_results = []

    for fname in sprite_files:
        path = os.path.join(DATA_DIR, fname)
        stitches = load_pattern_from_image(path, normalize_origin=True)
        name = fname.replace(".png", "")
        N = len(stitches)

        # Baseline 2
        res_b2 = run_baseline_color_scan(stitches)
        cost_b2 = res_b2["f_thread"]

        # Simulated Annealing
        res_sa = run_simulated_annealing(stitches, seed=42, alpha=0.992)
        cost_sa = res_sa["f_thread"]
        imprv_sa = ((cost_b2 - cost_sa) / cost_b2) * 100.0

        # Genetic Algorithm
        res_ga = run_genetic_algorithm(stitches, generations=80, seed=42)
        cost_ga = res_ga["f_thread"]
        imprv_ga = ((cost_b2 - cost_ga) / cost_b2) * 100.0

        row = f"| {name:<22} | {N:<3} | {cost_b2:10.2f} | {cost_sa:10.2f} | {imprv_sa:8.2f}% | {cost_ga:10.2f} | {imprv_ga:8.2f}% |"
        print(row)

        tier2_results.append({
            "name": name,
            "N": N,
            "b2": res_b2,
            "sa": res_sa,
            "ga": res_ga,
            "imprv_sa_pct": round(imprv_sa, 2),
            "imprv_ga_pct": round(imprv_ga, 2)
        })

    return tier2_results


if __name__ == "__main__":
    t1 = run_tier1_micro_benchmarks()
    t2 = run_tier2_macro_benchmarks()

    out_json = os.path.join(RESULTS_DIR, "phase3_search_summary.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"tier1_micro": t1, "tier2_macro": t2}, f, indent=2)
    print(f"\nSaved Phase 3 search summary to: {out_json}")
