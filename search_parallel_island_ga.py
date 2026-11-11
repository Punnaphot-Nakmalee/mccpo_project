"""
search_parallel_island_ga.py — Multi-Core Island Genetic Algorithm
===================================================================
Uses ALL 10-12 CPU threads simultaneously to solve ONE single pattern.

Architecture:
  - Spawns multiple isolated "Islands" (sub-populations) across CPU cores.
  - Each island runs on its own process/core with unique random seeds & crossover rates.
  - Periodically performs "Ring Migration" exchanging elite chromosomes.
  - Utilizes 100% of all CPU cores!
"""

import os
import time
import random
from typing import List, Dict, Any, Tuple
from concurrent.futures import ProcessPoolExecutor

from parser import load_pattern_from_image
from evaluator import evaluate_order, DEFAULT_D_MAX, DEFAULT_C_TRIM
from search_ga import GeneticAlgorithmMCCPO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _run_island_subpopulation(
    stitches: List[Dict[str, Any]],
    island_id: int,
    generations: int,
    pop_size: int,
    seed: int,
    init_order: List[int] = None,
) -> Dict[str, Any]:
    """Runs a dedicated evolutionary island on a single CPU core."""
    ga = GeneticAlgorithmMCCPO(
        stitches=stitches,
        pop_size=pop_size,
        generations=generations,
        crossover_rate=0.85 + (island_id % 3) * 0.05,
        mutation_rate=0.15 + (island_id % 4) * 0.03,
        seed=seed,
    )
    res = ga.search(init_order=init_order)
    return {
        "island_id": island_id,
        "best_order": res["order"],
        "cost": res["best_cost"],
        "f_thread": res["f_thread"],
        "f_switch": res["f_switch"],
    }


def solve_parallel_island_ga(
    stitches: List[Dict[str, Any]],
    num_islands: int = None,
    epochs: int = 4,
    gens_per_epoch: int = 15,
    island_pop_size: int = 25,
) -> Dict[str, Any]:
    """
    Main coordinator: mobilizes all CPU cores to cooperatively solve ONE pattern.
    """
    if num_islands is None:
        num_islands = max(2, min(10, (os.cpu_count() or 4) - 1))

    N = len(stitches)
    print("=" * 75)
    print(f"PARALLEL ISLAND GA: Solving Pattern (N={N}) across {num_islands} CPU Cores")
    print(f"Configuration: {num_islands} Islands x {island_pop_size} Pop x {epochs * gens_per_epoch} Total Gens")
    print("=" * 75)

    start_time = time.perf_counter()
    elite_migrants = [None] * num_islands
    global_best = None
    global_best_cost = float("inf")

    with ProcessPoolExecutor(max_workers=num_islands) as executor:
        for epoch in range(1, epochs + 1):
            t_epoch = time.perf_counter()
            # Launch all islands in parallel on separate cores
            futures = []
            for i in range(num_islands):
                seed = 100 * epoch + i
                init_cand = elite_migrants[(i - 1) % num_islands]  # Ring migration from neighbor
                f = executor.submit(
                    _run_island_subpopulation,
                    stitches,
                    i,
                    gens_per_epoch,
                    island_pop_size,
                    seed,
                    init_cand,
                )
                futures.append(f)

            # Collect results from all cores
            island_results = [f.result() for f in futures]
            epoch_time = time.perf_counter() - t_epoch

            # Update best & prepare ring migration
            for res in island_results:
                elite_migrants[res["island_id"]] = res["best_order"]
                if res["cost"] < global_best_cost:
                    global_best_cost = res["cost"]
                    global_best = res

            print(f"Epoch {epoch}/{epochs} ({epoch_time:.2f}s) | Global Best Thread: {global_best['f_thread']:.2f} | Switches: {global_best['f_switch']}")

    total_time = time.perf_counter() - start_time
    print(f"\n[DONE] Parallel Island GA finished in {total_time:.2f}s using all {num_islands} CPU cores!")
    return global_best


if __name__ == "__main__":
    file_path = os.path.join(DATA_DIR, "pattern_tapestry_32x32.png")
    stitches = load_pattern_from_image(file_path, normalize_origin=True)
    res = solve_parallel_island_ga(stitches, num_islands=8, epochs=4, gens_per_epoch=15)
