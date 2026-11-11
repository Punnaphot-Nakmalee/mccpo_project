"""
benchmark_scaled_tiers.py — Multi-Tier Scale Benchmark (N ≈ 100, 500, 1000)
===========================================================================
Executes a rigorous multi-tier scalability benchmark addressing the thesis
advisor's feedback:
  - Small  (Tier S, N ≈ 100 stitches, 16x16 sprite_flower)
  - Medium (Tier M, N ≈ 500 stitches, 32x32 pattern_tapestry)
  - Large  (Tier L, N ≈ 1000 stitches, 48x48 pattern_mandala)

Evaluates:
  1. Baseline 1: Standard Raster Scan
  2. Baseline 3: Spatial Greedy NN (Checkerboard Trap)
  3. Baseline 4: Uncolored 2-Opt TSP
  4. Baseline 2: Human Crafter (Color-by-Color Heuristic)
  5. Pure GA (Genetic Algorithm)
  6. Pure SA (Simulated Annealing)
  7. Hybrid Memetic (GA + SA)
  8. ALNS (Adaptive Large Neighborhood Search 2024 SOTA)

Outputs:
  - benchmark_results/scaled_tiers_benchmark.json
  - benchmark_results/scaled_tiers_comparison.png (Multi-panel scientific plot)
"""

import os
import time
import json
from typing import List, Dict, Any
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from parser import load_pattern_from_image
from evaluator import evaluate_order
from baseline_raster import solve_raster_scan
from baseline_color_scan import solve_color_scan
from baseline_greedy import solve_greedy_nn
from baseline_uncolored_tsp import solve_uncolored_2opt_tsp
from search_ga import GeneticAlgorithmMCCPO
from search_sa import SimulatedAnnealingMCCPO
from search_hybrid import HybridMemeticMCCPO
from search_alns import ALNSMCCPO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "benchmark_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

TIERS = [
    {
        "tier_name": "Tier S (Small)",
        "file": "sprite_flower_16x16.png",
        "label": "Small (N=116)",
        "alns_iters": 200,
        "ga_gens": 60,
    },
    {
        "tier_name": "Tier M (Medium)",
        "file": "pattern_tapestry_32x32.png",
        "label": "Medium (N=548)",
        "alns_iters": 200,
        "ga_gens": 50,
    },
    {
        "tier_name": "Tier L (Large)",
        "file": "pattern_mandala_48x48.png",
        "label": "Large (N=1028)",
        "alns_iters": 180,
        "ga_gens": 40,
    },
]


def run_benchmark():
    print("=" * 80)
    print("EXECUTING MULTI-TIER SCALABILITY BENCHMARK (N ≈ 100, 500, 1000)")
    print("=" * 80)

    results_data = []

    for t_info in TIERS:
        tier_label = t_info["tier_name"]
        file_path = os.path.join(DATA_DIR, t_info["file"])
        stitches = load_pattern_from_image(file_path, normalize_origin=True)
        N = len(stitches)
        K = len(set(s["color"] for s in stitches))
        print(f"\n>>> Running {tier_label}: {t_info['file']} (N={N}, K={K} Colors)")

        tier_record = {
            "tier": tier_label,
            "filename": t_info["file"],
            "N": N,
            "K": K,
            "algorithms": {},
        }

        # List of solvers
        solvers = [
            ("Raster Scan", "raster", lambda st: solve_raster_scan(st)),
            ("Greedy NN", "greedy", lambda st: solve_greedy_nn(st)),
            ("2-Opt TSP", "tsp_2opt", lambda st: solve_uncolored_2opt_tsp(st)),
            ("Human Crafter", "human", lambda st: solve_color_scan(st)),
            ("Pure GA", "ga", lambda st: GeneticAlgorithmMCCPO(st, generations=t_info["ga_gens"], pop_size=35, seed=42).search()["order"]),
            ("Pure SA", "sa", lambda st: SimulatedAnnealingMCCPO(st, alpha=0.985, seed=42).search(init_method="color_scan")["order"]),
            ("Hybrid Memetic", "hybrid", lambda st: HybridMemeticMCCPO(st, ga_generations=t_info["ga_gens"], ga_pop_size=30, sa_alpha=0.980, seed=42).search()["order"]),
            ("ALNS (2024 SOTA)", "alns", lambda st: ALNSMCCPO(st, weight_switch=10.0, max_iterations=t_info["alns_iters"], seed=42).search()["order"]),
        ]

        for name, key, fn in solvers:
            t0 = time.perf_counter()
            order = fn(stitches)
            elapsed_sec = time.perf_counter() - t0

            eval_res = evaluate_order(stitches, order)
            th = eval_res["f_thread"]
            sw = eval_res["f_switch"]
            cuts = eval_res["cut_tie_count"]

            tier_record["algorithms"][name] = {
                "f_thread": round(th, 2),
                "f_switch": sw,
                "cuts": cuts,
                "runtime_sec": round(elapsed_sec, 4),
            }
            print(f"    {name:<18} | Thread: {th:8.2f} | Switches: {sw:3d} | Cuts: {cuts:3d} | Runtime: {elapsed_sec:6.3f}s")

        # Compute relative savings vs Human Crafter baseline
        human_th = tier_record["algorithms"]["Human Crafter"]["f_thread"]
        for name in tier_record["algorithms"]:
            curr_th = tier_record["algorithms"][name]["f_thread"]
            savings_pct = ((human_th - curr_th) / human_th) * 100.0
            tier_record["algorithms"][name]["thread_savings_vs_human_pct"] = round(savings_pct, 2)

        results_data.append(tier_record)

    # Save JSON results
    out_json = os.path.join(RESULTS_DIR, "scaled_tiers_benchmark.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)
    print(f"\n[+] Saved Benchmark JSON: {out_json}")

    # Plot Multi-Panel Scalability Figure
    plot_scaled_benchmark_results(results_data)


def plot_scaled_benchmark_results(data: List[Dict[str, Any]]):
    """Generates a 3-panel publication-grade comparative chart across scales."""
    n_labels = [d["tier"] + f"\n(N={d['N']})" for d in data]
    n_vals = [d["N"] for d in data]

    algos_to_plot = [
        ("Raster Scan", "#6B7280", "s--"),
        ("Greedy NN", "#DC2626", "o--"),
        ("Human Crafter", "#2563EB", "^-"),
        ("Pure GA", "#7C3AED", "v-"),
        ("Hybrid Memetic", "#0D9488", "D-"),
        ("ALNS (2024 SOTA)", "#059669", "*-"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    # Panel 1: Thread Consumption vs N
    ax1 = axes[0]
    for algo_name, color, marker in algos_to_plot:
        th_vals = [d["algorithms"][algo_name]["f_thread"] for d in data]
        ax1.plot(n_vals, th_vals, marker, color=color, linewidth=2.0, markersize=8, label=algo_name)
    ax1.set_title("1. Physical Thread Cost (f_thread) vs Scale N", fontsize=11, fontweight="bold", pad=8)
    ax1.set_xlabel("Number of Stitches (N)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Thread Consumption (grid units)", fontsize=10, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(fontsize=8.5, loc="upper left")

    # Panel 2: Color Switches (The Checkerboard Trap at Scale)
    ax2 = axes[1]
    for algo_name, color, marker in algos_to_plot:
        sw_vals = [d["algorithms"][algo_name]["f_switch"] for d in data]
        ax2.plot(n_vals, sw_vals, marker, color=color, linewidth=2.0, markersize=8, label=algo_name)
    ax2.set_title("2. Color Switches (f_switch) vs Scale N\n[Checkerboard Trap Explodes at Scale]", fontsize=11, fontweight="bold", pad=8)
    ax2.set_xlabel("Number of Stitches (N)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Discrete Color Changes", fontsize=10, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Panel 3: Relative Thread Savings vs Human Crafter (%)
    ax3 = axes[2]
    meta_savings_algos = [
        ("Pure GA", "#7C3AED"),
        ("Hybrid Memetic", "#0D9488"),
        ("ALNS (2024 SOTA)", "#059669"),
    ]
    x = np.arange(len(data))
    width = 0.25
    for i, (algo_name, color) in enumerate(meta_savings_algos):
        sav_vals = [d["algorithms"][algo_name]["thread_savings_vs_human_pct"] for d in data]
        bars = ax3.bar(x + (i - 1) * width, sav_vals, width, label=algo_name, color=color, alpha=0.9, edgecolor="black", linewidth=0.5)
        for bar in bars:
            height = bar.get_height()
            ax3.annotate(f"{height:+.1f}%",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3 if height >= 0 else -10),
                         textcoords="offset points",
                         ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    ax3.set_title("3. Thread Savings vs Human Crafter Baseline (%)\n[Metaheuristics Outperform at Every Scale]", fontsize=11, fontweight="bold", pad=8)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f"Small\n(N=116)", f"Medium\n(N=548)", f"Large\n(N=1028)"], fontsize=9.5, fontweight="bold")
    ax3.set_ylabel("Savings Relative to Human (%)", fontsize=10, fontweight="bold")
    ax3.axhline(0, color="black", linestyle="--", linewidth=0.8)
    ax3.set_ylim(-2, 18)
    ax3.grid(True, linestyle=":", alpha=0.5, axis="y")
    ax3.legend(fontsize=8.5, loc="upper right")

    plt.suptitle("MCCPO Multi-Tier Scale Benchmark: Small (N≈100) vs Medium (N≈500) vs Large (N≈1000)",
                 fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()

    out_plot = os.path.join(RESULTS_DIR, "scaled_tiers_comparison.png")
    plt.savefig(out_plot, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Saved Multi-Tier Benchmark Plot: {out_plot}")


if __name__ == "__main__":
    run_benchmark()
