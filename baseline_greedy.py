"""
baseline_greedy.py — Baseline 3: Spatial Greedy Nearest Neighbor
==============================================================
Classic unconstrained TSP heuristic:
  - Starts at stitch 0 (or top-left stitch).
  - Greedily transitions to the closest unvisited stitch in Euclidean space,
    completely ignoring color.
  - Demonstrates the trade-off of naive distance minimization:
    frequently triggers color changes and Cut & Tie-off penalties.
"""

from typing import List, Dict, Any
from evaluator import evaluate_order, euclidean_distance


def solve_greedy_nn(stitches: List[Dict[str, Any]], start_idx: int = 0) -> List[int]:
    """
    Computes a nearest-neighbor tour ignoring stitch color.
    
    Parameters
    ----------
    stitches : list of dict
        List of stitches.
    start_idx : int
        Index of the initial stitch (default: 0).
        
    Returns
    -------
    list of int
        Permutation order.
    """
    N = len(stitches)
    if N <= 1:
        return list(range(N))

    unvisited = set(range(N))
    order = [start_idx]
    unvisited.remove(start_idx)
    current_idx = start_idx

    while unvisited:
        curr_s = stitches[current_idx]
        next_idx = min(unvisited, key=lambda idx: (euclidean_distance(curr_s, stitches[idx]), idx))
        order.append(next_idx)
        unvisited.remove(next_idx)
        current_idx = next_idx

    return order


def run_baseline_greedy(stitches: List[Dict[str, Any]], d_max: float = 3.162, c_trim: float = 10.0) -> Dict[str, Any]:
    """Runs and evaluates the Spatial Greedy Nearest Neighbor baseline."""
    order = solve_greedy_nn(stitches)
    results = evaluate_order(stitches, order, d_max=d_max, c_trim=c_trim)
    results["order"] = order
    results["algorithm"] = "Baseline 3: Greedy Nearest Neighbor"
    return results


if __name__ == "__main__":
    from sample_patterns import TOY_PATTERN_10
    res = run_baseline_greedy(TOY_PATTERN_10)
    print(f"Greedy NN on TOY_PATTERN_10:")
    print(f"  f_thread = {res['f_thread']:.3f}")
    print(f"  f_switch = {res['f_switch']}")
    print(f"  cut_ties = {res['cut_tie_count']}")
