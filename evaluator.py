"""
evaluator.py
Core Evaluation Engine for Multi-Color Cross-Stitch Path Optimization (MCCPO).
Implements the Two-Tier Action Space cost model:
  - Action 1: Continuous Carry (same color AND distance <= d_max) -> cost = Euclidean distance
  - Action 2: Cut & Tie-Off   (different color OR distance > d_max) -> cost = C_trim penalty
"""

import math
from typing import List, Dict, Any, Tuple

# Default physical craft parameters
DEFAULT_D_MAX = 3.162    # sqrt(10) ≈ 3.16 grid units (max ~3 diagonal or 3 orthogonal squares)
DEFAULT_C_TRIM = 10.0    # 10 grid units equivalent for thread cutting, tail waste, and re-anchoring

def euclidean_distance(s1: Dict[str, Any], s2: Dict[str, Any]) -> float:
    """Computes Euclidean distance between stitch s1 and stitch s2."""
    return math.sqrt((s1["x"] - s2["x"])**2 + (s1["y"] - s2["y"])**2)

def evaluate_sequence(
    sequence: List[Dict[str, Any]], 
    d_max: float = DEFAULT_D_MAX, 
    c_trim: float = DEFAULT_C_TRIM
) -> Dict[str, Any]:
    """
    Evaluates a candidate stitching trajectory sequence pi = (pi_0, pi_1, ..., pi_{N-1}).
    
    Returns a dictionary containing:
      - f_thread: Total thread consumed (carried thread distance + trim penalty waste)
      - f_switch: Total discrete color-switch stoppages
      - carried_distance: Pure continuous travel distance across back of fabric
      - cut_tie_count: Total number of cut & tie-off operations executed
      - transitions: Step-by-step breakdown of actions taken
      - is_valid: Boolean verifying all stitches in sequence are unique and valid
    """
    N = len(sequence)
    if N <= 1:
        return {
            "f_thread": 0.0,
            "f_switch": 0,
            "carried_distance": 0.0,
            "cut_tie_count": 0,
            "transitions": [],
            "is_valid": True
        }
    
    # Check permutation validity (no duplicate stitch IDs)
    visited_ids = set()
    for s in sequence:
        visited_ids.add(s["id"])
    is_valid = (len(visited_ids) == N)

    total_carried_dist = 0.0
    total_trim_penalties = 0.0
    color_switches = 0
    cut_tie_count = 0
    transitions = []

    for k in range(N - 1):
        curr_stitch = sequence[k]
        next_stitch = sequence[k + 1]
        
        dist = euclidean_distance(curr_stitch, next_stitch)
        same_color = (curr_stitch["color"] == next_stitch["color"])
        within_jump_limit = (dist <= d_max)

        if same_color and within_jump_limit:
            # Action 1: Continuous Carry
            action = "CONTINUOUS_CARRY"
            step_cost = dist
            total_carried_dist += dist
        else:
            # Action 2: Cut & Tie-Off (Mandatory due to color change or long distance)
            action = "CUT_AND_TIE"
            step_cost = c_trim
            total_trim_penalties += c_trim
            cut_tie_count += 1
            if not same_color:
                color_switches += 1

        transitions.append({
            "step": k + 1,
            "from_id": curr_stitch["id"],
            "to_id": next_stitch["id"],
            "from_pos": (curr_stitch["x"], curr_stitch["y"]),
            "to_pos": (next_stitch["x"], next_stitch["y"]),
            "from_color": curr_stitch["color"],
            "to_color": next_stitch["color"],
            "distance": round(dist, 3),
            "action": action,
            "cost": round(step_cost, 3)
        })

    f_thread = total_carried_dist + total_trim_penalties

    return {
        "f_thread": round(f_thread, 3),
        "f_switch": color_switches,
        "carried_distance": round(total_carried_dist, 3),
        "cut_tie_count": cut_tie_count,
        "total_trim_cost": round(total_trim_penalties, 3),
        "is_valid": is_valid,
        "transitions": transitions
    }

def evaluate_order(
    stitches: List[Dict[str, Any]],
    order: List[int],
    d_max: float = DEFAULT_D_MAX,
    c_trim: float = DEFAULT_C_TRIM
) -> Dict[str, Any]:
    """
    Evaluates a candidate trajectory defined as a permutation order of indices into stitches.
    Validates that `order` is a strict, complete permutation of [0, ..., N-1].
    """
    N = len(stitches)
    if len(order) != N or set(order) != set(range(N)):
        raise ValueError(f"Invalid permutation order: length={len(order)}, expected={N}, unique={len(set(order))}")
    sequence = [stitches[i] for i in order]
    return evaluate_sequence(sequence, d_max=d_max, c_trim=c_trim)

