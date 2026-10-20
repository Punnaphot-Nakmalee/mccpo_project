"""
baseline_raster.py — Baseline 1: Standard Raster Scan
======================================================
Simulates a naive raster traversal (top-to-bottom, left-to-right),
analogous to a conventional printer carriage.

Sorts stitches primarily by y (row) and secondarily by x (column).
"""

from typing import List, Dict, Any
from evaluator import evaluate_order


def solve_raster_scan(stitches: List[Dict[str, Any]], reverse_y: bool = False) -> List[int]:
    """
    Returns permutation order corresponding to raster scan.
    
    Parameters
    ----------
    stitches : list of dict
        [{"id": int, "x": int, "y": int, "color": str}, ...]
    reverse_y : bool
        If True, traverses from highest y to lowest y (top-down in standard cartesian).
        If False, traverses from lowest y to highest y (standard image raster if y=0 at top).
        
    Returns
    -------
    list of int
        Permutation order of stitch indices.
    """
    # Sort indices by (y, x)
    indexed_stitches = list(enumerate(stitches))
    if reverse_y:
        indexed_stitches.sort(key=lambda item: (-item[1]["y"], item[1]["x"]))
    else:
        indexed_stitches.sort(key=lambda item: (item[1]["y"], item[1]["x"]))
        
    order = [idx for idx, s in indexed_stitches]
    return order


def run_baseline_raster(stitches: List[Dict[str, Any]], d_max: float = 3.162, c_trim: float = 10.0) -> Dict[str, Any]:
    """Runs and evaluates the Raster Scan baseline."""
    order = solve_raster_scan(stitches)
    results = evaluate_order(stitches, order, d_max=d_max, c_trim=c_trim)
    results["order"] = order
    results["algorithm"] = "Baseline 1: Raster Scan"
    return results


if __name__ == "__main__":
    from sample_patterns import TOY_PATTERN_10
    res = run_baseline_raster(TOY_PATTERN_10)
    print(f"Raster Scan on TOY_PATTERN_10:")
    print(f"  f_thread = {res['f_thread']:.3f}")
    print(f"  f_switch = {res['f_switch']}")
    print(f"  cut_ties = {res['cut_tie_count']}")
