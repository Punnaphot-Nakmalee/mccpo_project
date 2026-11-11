"""
search_parallel_alns.py — Multi-Core Parallel ALNS (Ensemble ALNS)
==================================================================
Runs multiple parallel ALNS workers concurrently across 8-10 CPU cores
to solve ONE single pattern. Each worker explores diverse search trajectories
with randomized operator weights and seeds.
"""

import os
import time
from typing import List, Dict, Any
from concurrent.futures import ProcessPoolExecutor

from parser import load_pattern_from_image
from evaluator import evaluate_order, DEFAULT_D_MAX, DEFAULT_C_TRIM
from search_alns import ALNSMCCPO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _run_single_alns_worker(
    stitches: List[Dict[str, Any]],
    worker_id: int,
    iterations: int,
    seed: int,
    weight_switch: float,
) -> Dict[str, Any]:
    solver = ALNSMCCPO(
        stitches=stitches,
        weight_switch=weight_switch,
        max_iterations=iterations,
        destroy_fraction=0.10 + (worker_id % 4) * 0.03,
        seed=seed,
    )
    res = solver.search()
    res["worker_id"] = worker_id
    return res


def solve_parallel_alns(
    stitches: List[Dict[str, Any]],
    num_workers: int = None,
    iterations_per_worker: int = 180,
    weight_switch: float = 10.0,
) -> Dict[str, Any]:
    if num_workers is None:
        num_workers = max(2, min(10, (os.cpu_count() or 4) - 1))

    N = len(stitches)
    print("=" * 75)
    print(f"PARALLEL ENSEMBLE ALNS: Solving Pattern (N={N}) across {num_workers} CPU Cores")
    print("=" * 75)

    start_time = time.perf_counter()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(num_workers):
            seed = 42 + i * 17
            f = executor.submit(
                _run_single_alns_worker,
                stitches,
                i,
                iterations_per_worker,
                seed,
                weight_switch,
            )
            futures.append(f)

        results = [f.result() for f in futures]

    total_time = time.perf_counter() - start_time

    # Find best across all workers
    best_res = min(results, key=lambda r: r["cost"])

    print(f"\n[SUMMARY of {num_workers} Parallel Workers in {total_time:.2f}s]")
    for r in sorted(results, key=lambda x: x["f_thread"]):
        print(f"  Worker {r['worker_id']:2d}: Thread = {r['f_thread']:7.2f} | Switches = {r['f_switch']:2d} | Cuts = {r['cut_tie_count']:2d} | Time = {r['runtime_ms']/1000:5.2f}s")

    print(f"\n>> WINNING WORKER {best_res['worker_id']}: Thread = {best_res['f_thread']:.2f} | Switches = {best_res['f_switch']}")
    return best_res


if __name__ == "__main__":
    file_path = os.path.join(DATA_DIR, "pattern_tapestry_32x32.png")
    stitches = load_pattern_from_image(file_path, normalize_origin=True)
    solve_parallel_alns(stitches, num_workers=8, iterations_per_worker=180)
