"""
baseline_color_scan.py — Baseline 2: Color-by-Color Sequential Scan
==================================================================
Simulates conventional single-needle crafter behavior:
  - Partitions stitches by color.
  - Finishes all stitches of one color before switching to the next color.
  - Within each color, stitches are ordered via greedy nearest neighbor
    to avoid haphazard internal jumping.

Guaranteed Property:
  f_switch = K - 1 (the theoretical minimum number of color switches),
  where K is the number of distinct colors present in the pattern.
"""

from typing import List, Dict, Any
import math
from evaluator import evaluate_order, euclidean_distance


def solve_color_scan(stitches: List[Dict[str, Any]]) -> List[int]:
    """
    Returns permutation order corresponding to Color-by-Color sequential traversal.
    Within each color group, stitches are sequenced using greedy nearest-neighbor.
    """
    # 1. Group indices by color
    color_groups: Dict[str, List[int]] = {}
    for idx, s in enumerate(stitches):
        c = s["color"]
        if c not in color_groups:
            color_groups[c] = []
        color_groups[c].append(idx)

    # Sort color groups by appearance or descending size to stabilize order
    sorted_colors = sorted(color_groups.keys(), key=lambda c: -len(color_groups[c]))

    overall_order = []
    current_pos_stitch = None

    for color in sorted_colors:
        group = color_groups[color].copy()
        
        # Pick start stitch in this color group: closest to last stitch, or top-left
        if current_pos_stitch is None:
            group.sort(key=lambda idx: (stitches[idx]["y"], stitches[idx]["x"], idx))
            curr_idx = group.pop(0)
        else:
            group.sort(key=lambda idx: (euclidean_distance(current_pos_stitch, stitches[idx]), idx))
            curr_idx = group.pop(0)

        overall_order.append(curr_idx)
        current_pos_stitch = stitches[curr_idx]

        # Greedy nearest-neighbor traversal within the current color
        while group:
            next_idx = min(group, key=lambda idx: (euclidean_distance(current_pos_stitch, stitches[idx]), idx))
            group.remove(next_idx)
            overall_order.append(next_idx)
            current_pos_stitch = stitches[next_idx]

    return overall_order


def run_baseline_color_scan(stitches: List[Dict[str, Any]], d_max: float = 3.162, c_trim: float = 10.0) -> Dict[str, Any]:
    """Runs and evaluates the Color-by-Color baseline."""
    order = solve_color_scan(stitches)
    results = evaluate_order(stitches, order, d_max=d_max, c_trim=c_trim)
    results["order"] = order
    results["algorithm"] = "Baseline 2: Color-by-Color"
    
    # Mathematical sanity assertion
    distinct_colors = len(set(s["color"] for s in stitches))
    expected_switches = max(0, distinct_colors - 1)
    assert results["f_switch"] == expected_switches, (
        f"Expected f_switch={expected_switches}, got {results['f_switch']}"
    )
    return results


if __name__ == "__main__":
    from sample_patterns import TOY_PATTERN_10
    res = run_baseline_color_scan(TOY_PATTERN_10)
    print(f"Color-by-Color on TOY_PATTERN_10:")
    print(f"  f_thread = {res['f_thread']:.3f}")
    print(f"  f_switch = {res['f_switch']} (Minimum possible: {len(set(s['color'] for s in TOY_PATTERN_10))-1})")
    print(f"  cut_ties = {res['cut_tie_count']}")
