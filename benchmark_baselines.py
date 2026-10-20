"""
benchmark_baselines.py — Baseline Benchmark Execution Engine
============================================================
Runs all 4 baseline algorithms across:
  - 5 Tier 1 Micro-Benchmark Patterns (N <= 15)
  - 5 Tier 2 Medium Retro Sprites (N = 50 ~ 200)

Records and outputs:
  - f_thread (Total thread consumed: distance + trim penalty)
  - f_switch (Discrete color switches)
  - cut_tie_count (Total thread cut operations)
  - runtime (Execution time in milliseconds)
"""

import os
import time
import json
from typing import Dict, Any, List

from sample_patterns import TIER1_MICRO_PATTERNS
from parser import load_pattern_from_image
from baseline_raster import run_baseline_raster
from baseline_color_scan import run_baseline_color_scan
from baseline_greedy import run_baseline_greedy
from baseline_uncolored_tsp import run_baseline_uncolored_tsp
from visualizer import visualize_trajectory

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "benchmark_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

BASELINES = [
    ("B1: Raster Scan", run_baseline_raster),
    ("B2: Color-by-Color", run_baseline_color_scan),
    ("B3: Greedy NN", run_baseline_greedy),
    ("B4: Uncolored 2-Opt TSP", run_baseline_uncolored_tsp),
]


def load_all_benchmark_patterns() -> List[Dict[str, Any]]:
    """Loads all Tier 1 micro-patterns and Tier 2 sprite patterns."""
    dataset = []

    # 1. Tier 1: Micro-patterns
    for name, stitches in TIER1_MICRO_PATTERNS.items():
        dataset.append({
            "name": name,
            "tier": "Tier 1 (Micro)",
            "stitches": stitches,
            "N": len(stitches),
            "colors": len(set(s["color"] for s in stitches)),
        })

    # 2. Tier 2: Medium Sprites
    sprite_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("sprite_") and f.endswith(".png")])
    for fname in sprite_files:
        path = os.path.join(DATA_DIR, fname)
        stitches = load_pattern_from_image(path, normalize_origin=True)
        name = fname.replace(".png", "")
        dataset.append({
            "name": name,
            "tier": "Tier 2 (Medium)",
            "stitches": stitches,
            "N": len(stitches),
            "colors": len(set(s["color"] for s in stitches)),
        })

    return dataset


def run_all_benchmarks(d_max: float = 3.162, c_trim: float = 10.0) -> List[Dict[str, Any]]:
    dataset = load_all_benchmark_patterns()
    all_results = []

    print("=" * 80)
    print(f"RUNNING BASELINE BENCHMARKS ACROSS {len(dataset)} TEST INSTANCES")
    print(f"Parameters: d_max = {d_max:.3f}, C_trim = {c_trim:.1f}")
    print("=" * 80)

    for item in dataset:
        p_name = item["name"]
        tier = item["tier"]
        stitches = item["stitches"]
        N = item["N"]
        K = item["colors"]

        print(f"\n--> Instance: {p_name:<26} [{tier}] (N={N:3d}, Colors={K})")
        pattern_record = {
            "instance": p_name,
            "tier": tier,
            "N": N,
            "colors": K,
            "baseline_results": {}
        }

        for algo_name, algo_fn in BASELINES:
            t0 = time.perf_counter()
            res = algo_fn(stitches, d_max=d_max, c_trim=c_trim)
            elapsed_ms = (time.perf_counter() - t0) * 1000.0

            res_summary = {
                "f_thread": res["f_thread"],
                "f_switch": res["f_switch"],
                "cut_tie_count": res["cut_tie_count"],
                "carried_dist": res["carried_distance"],
                "runtime_ms": round(elapsed_ms, 2),
                "order": res["order"]
            }
            pattern_record["baseline_results"][algo_name] = res_summary

            print(f"    {algo_name:<24} | f_thread: {res['f_thread']:8.2f} | f_switch: {res['f_switch']:3d} | Cuts: {res['cut_tie_count']:3d} | Time: {elapsed_ms:6.2f}ms")

        all_results.append(pattern_record)

    # Save complete JSON record
    json_path = os.path.join(RESULTS_DIR, "baseline_benchmark_summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved raw JSON benchmark data to: {json_path}")

    # Generate visual comparison for a sample pattern (checker_8 and sprite_flower_16x16)
    _generate_sample_comparison_plots(dataset, all_results)

    return all_results


def _generate_sample_comparison_plots(dataset, all_results):
    """Generates side-by-side trajectory comparison plots for key patterns."""
    for target_name in ["checker_8", "sprite_flower_16x16"]:
        item = next((p for p in dataset if p["name"] == target_name), None)
        record = next((r for r in all_results if r["instance"] == target_name), None)
        if not item or not record:
            continue

        stitches = item["stitches"]
        for algo_name, res_summary in record["baseline_results"].items():
            safe_algo = algo_name.split(":")[0].strip().replace(" ", "_")
            save_name = f"comparison_{target_name}_{safe_algo}.png"
            save_path = os.path.join(RESULTS_DIR, save_name)

            from evaluator import evaluate_order
            detailed_res = evaluate_order(stitches, res_summary["order"])
            title = f"{target_name} - {algo_name}\nf_thread={detailed_res['f_thread']:.1f}, f_switch={detailed_res['f_switch']}"
            visualize_trajectory(stitches, detailed_res["transitions"], title=title, save_path=save_path)


def print_markdown_summary_table(all_results: List[Dict[str, Any]]):
    """Prints a comparative Markdown summary table."""
    print("\n" + "=" * 95)
    print("COMPARATIVE BASELINE BENCHMARK SUMMARY TABLE")
    print("=" * 95)
    
    header = f"| {'Instance':<24} | {'N':<3} | {'Metric':<10} | {'B1: Raster':<12} | {'B2: ColorScan':<13} | {'B3: GreedyNN':<12} | {'B4: 2-Opt TSP':<13} |"
    divider = f"|:{'-'*24}-|-{'-'*3}:|-{'-'*10}:|-{'-'*12}:|-{'-'*13}:|-{'-'*12}:|-{'-'*13}:|"
    print(header)
    print(divider)

    for rec in all_results:
        inst = rec["instance"]
        N = rec["N"]
        b = rec["baseline_results"]

        f_thread_row = f"| {inst:<24} | {N:<3} | f_thread   | {b['B1: Raster Scan']['f_thread']:12.2f} | {b['B2: Color-by-Color']['f_thread']:13.2f} | {b['B3: Greedy NN']['f_thread']:12.2f} | {b['B4: Uncolored 2-Opt TSP']['f_thread']:13.2f} |"
        f_switch_row = f"| {'':<24} | {'':<3} | f_switch   | {b['B1: Raster Scan']['f_switch']:12d} | {b['B2: Color-by-Color']['f_switch']:13d} | {b['B3: Greedy NN']['f_switch']:12d} | {b['B4: Uncolored 2-Opt TSP']['f_switch']:13d} |"
        print(f_thread_row)
        print(f_switch_row)
        print(f"| {'':<24} | {'':<3} | {'-'*10} | {'-'*12} | {'-'*13} | {'-'*12} | {'-'*13} |")


if __name__ == "__main__":
    results = run_all_benchmarks()
    print_markdown_summary_table(results)
