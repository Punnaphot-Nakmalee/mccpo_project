"""
baseline_uncolored_tsp.py — Baseline 4: Uncolored 2-Opt TSP
==========================================================
Solves spatial path minimization ignoring color boundaries using 2-opt local search:
  1. Initializes tour via greedy nearest-neighbor.
  2. Iteratively performs 2-opt edge swaps (reversing sub-paths) to eliminate
     crossing edges and minimize pure Euclidean distance.
  3. Evaluates the resulting uncolored geometric tour post-hoc under the
     Two-Tier Action Space cost model.

Demonstrates that pure geometric TSP optimization performs poorly on multi-color
crafts because crossing color boundaries repeatedly incurs massive C_trim penalties.
"""

from typing import List, Dict, Any
from evaluator import evaluate_order, euclidean_distance
from baseline_greedy import solve_greedy_nn


def _tour_euclidean_length(tour: List[int], stitches: List[Dict[str, Any]]) -> float:
    """Computes pure uncolored path length."""
    return sum(
        euclidean_distance(stitches[tour[i]], stitches[tour[i + 1]])
        for i in range(len(tour) - 1)
    )


def solve_uncolored_2opt_tsp(stitches: List[Dict[str, Any]], max_iterations: int = 1000) -> List[int]:
    """
    Computes an uncolored 2-opt TSP path.
    """
    N = len(stitches)
    if N <= 2:
        return list(range(N))

    # Initialize with greedy tour
    tour = solve_greedy_nn(stitches)
    
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        # 1. Prefix reversals (i = 0)
        for j in range(1, N - 1):
            p_j = stitches[tour[j]]
            p_0 = stitches[tour[0]]
            p_next = stitches[tour[j + 1]]
            d_old = euclidean_distance(p_j, p_next)
            d_new = euclidean_distance(p_0, p_next)
            if d_new < d_old - 1e-6:
                tour[0:j + 1] = list(reversed(tour[0:j + 1]))
                improved = True
                break

        if improved:
            continue

        # 2. Internal and suffix reversals
        for i in range(1, N - 1):
            for j in range(i + 1, N):
                p_prev = stitches[tour[i - 1]]
                p_i = stitches[tour[i]]
                p_j = stitches[tour[j]]
                p_next = stitches[tour[j + 1]] if (j + 1 < N) else None

                d_old = euclidean_distance(p_prev, p_i)
                d_new = euclidean_distance(p_prev, p_j)

                if p_next is not None:
                    d_old += euclidean_distance(p_j, p_next)
                    d_new += euclidean_distance(p_i, p_next)

                if d_new < d_old - 1e-6:
                    tour[i:j + 1] = list(reversed(tour[i:j + 1]))
                    improved = True
                    break
            if improved:
                break

    return tour


def run_baseline_uncolored_tsp(stitches: List[Dict[str, Any]], d_max: float = 3.162, c_trim: float = 10.0) -> Dict[str, Any]:
    """Runs and evaluates the Uncolored 2-Opt TSP baseline."""
    order = solve_uncolored_2opt_tsp(stitches)
    results = evaluate_order(stitches, order, d_max=d_max, c_trim=c_trim)
    results["order"] = order
    results["algorithm"] = "Baseline 4: Uncolored 2-Opt TSP"
    return results


if __name__ == "__main__":
    from sample_patterns import TOY_PATTERN_10
    res = run_baseline_uncolored_tsp(TOY_PATTERN_10)
    print(f"Uncolored 2-Opt TSP on TOY_PATTERN_10:")
    print(f"  f_thread = {res['f_thread']:.3f}")
    print(f"  f_switch = {res['f_switch']}")
    print(f"  cut_ties = {res['cut_tie_count']}")
