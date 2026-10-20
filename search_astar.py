"""
search_astar.py — Tier 1 Exact A* Search Engine (N <= 15)
=========================================================
Implements an informed A* search algorithm for the Multi-Color Cross-Stitch
Path Optimization (MCCPO) problem.

Solves micro-instances (N <= 15) to mathematical optimality to obtain:
  - Ground-truth optimal cost J* = (f_thread*, f_switch*)
  - Reference benchmark for computing the Optimality Gap of metaheuristics (SA, GA)

State Representation:
  State = (v_curr, unvisited_mask, c_curr)
    - v_curr: Index of the most recently visited stitch (or -1 at start)
    - unvisited_mask: Integer bitmask of remaining unvisited stitch indices
    - c_curr: Current active thread color (or None at start)

Heuristic Function:
  h(s) = max(h_dist(s), h_trim(s)) + lambda * S_min(s)
    - h_dist(s): Minimum Spanning Tree (MST) on {v_curr} U U with edge weights
                 w(u, v) = min(dist(u, v), C_trim).
    - h_trim(s): S_min(s) * C_trim (minimum mandatory cut penalties for color switches).
    - S_min(s): max(0, |K_rem| - I[c_curr in K_rem]) (minimum remaining color switches).
  Both components are provably admissible lower bounds; taking their maximum
  provides the tightest admissible estimate without double-counting.
"""

import time
import heapq
import math
from typing import List, Dict, Any, Tuple, Optional
from evaluator import evaluate_order, euclidean_distance, DEFAULT_D_MAX, DEFAULT_C_TRIM


# ---------------------------------------------------------------------------
# Precomputed Distance Matrix & Fast MST
# ---------------------------------------------------------------------------

def _build_distance_matrix(stitches: List[Dict[str, Any]], c_trim: float) -> List[List[float]]:
    N = len(stitches)
    dist_mat = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            d = euclidean_distance(stitches[i], stitches[j])
            dist_mat[i][j] = d
            dist_mat[j][i] = d
    return dist_mat


def _compute_mst_weight(nodes: List[int], dist_mat: List[List[float]], c_trim: float) -> float:
    """
    Computes MST weight on the given subset of nodes using Prim's algorithm.
    Edge weight is min(d(u, v), c_trim) to ensure strict admissibility.
    """
    k = len(nodes)
    if k <= 1:
        return 0.0
    if k == 2:
        return min(dist_mat[nodes[0]][nodes[1]], c_trim)

    visited_first = nodes[0]
    unvisited = list(nodes[1:])
    min_dists = [min(dist_mat[visited_first][v], c_trim) for v in unvisited]
    total_weight = 0.0

    for _ in range(k - 1):
        min_idx = min(range(len(unvisited)), key=lambda i: min_dists[i])
        u = unvisited.pop(min_idx)
        w = min_dists.pop(min_idx)
        total_weight += w

        for i, v in enumerate(unvisited):
            d = min(dist_mat[u][v], c_trim)
            if d < min_dists[i]:
                min_dists[i] = d

    return total_weight


# ---------------------------------------------------------------------------
# A* Search Class
# ---------------------------------------------------------------------------

class AStarMCCPO:
    def __init__(
        self,
        stitches: List[Dict[str, Any]],
        d_max: float = DEFAULT_D_MAX,
        c_trim: float = DEFAULT_C_TRIM,
        weight_switch: float = 0.0,
    ):
        self.stitches = stitches
        self.N = len(stitches)
        self.d_max = d_max
        self.c_trim = c_trim
        self.weight_switch = weight_switch  # lambda trade-off factor

        self.dist_mat = _build_distance_matrix(stitches, c_trim)
        self.colors = [s["color"] for s in stitches]
        self.all_colors = set(self.colors)

        # Memoization cache for MST calculations (mask -> mst_weight)
        self._mst_cache: Dict[Tuple[int, int], float] = {}

    def _heuristic(self, v_curr: int, unvisited_mask: int, c_curr: Optional[str]) -> float:
        if unvisited_mask == 0:
            return 0.0

        # 1. Collect unvisited nodes and remaining colors
        unvisited_nodes = [i for i in range(self.N) if (unvisited_mask & (1 << i))]
        k_rem = {self.colors[i] for i in unvisited_nodes}

        # 2. Minimum remaining color switches
        if c_curr is not None and c_curr in k_rem:
            s_min = max(0, len(k_rem) - 1)
        else:
            s_min = len(k_rem)

        # 3. Trim cost lower bound
        h_trim = s_min * self.c_trim

        # 4. MST spatial distance lower bound
        cache_key = (v_curr, unvisited_mask)
        if cache_key in self._mst_cache:
            h_dist = self._mst_cache[cache_key]
        else:
            nodes_for_mst = ([v_curr] + unvisited_nodes) if (v_curr >= 0) else unvisited_nodes
            h_dist = _compute_mst_weight(nodes_for_mst, self.dist_mat, self.c_trim)
            self._mst_cache[cache_key] = h_dist

        # Combined strictly admissible lower bound
        h_thread = max(h_dist, h_trim)
        h_total = h_thread + (self.weight_switch * s_min)
        return h_total

    def search(self, max_nodes: int = 1_000_000) -> Dict[str, Any]:
        """
        Executes A* search to find the optimal stitching sequence.
        """
        start_time = time.perf_counter()

        if self.N == 0:
            return {"order": [], "f_thread": 0.0, "f_switch": 0, "nodes_expanded": 0, "runtime_ms": 0.0}
        if self.N == 1:
            return {"order": [0], "f_thread": 0.0, "f_switch": 0, "nodes_expanded": 1, "runtime_ms": 0.0}

        # Priority queue entry: (f, g, h, v_curr, unvisited_mask, c_curr, path)
        # Tie-breaker counter
        counter = 0
        pq = []

        full_mask = (1 << self.N) - 1

        # Initial states: start at any stitch i in 0..N-1
        for start_idx in range(self.N):
            c_start = self.colors[start_idx]
            rem_mask = full_mask & ~(1 << start_idx)
            g = 0.0  # cost to first stitch is 0 (or first color thread load)
            h = self._heuristic(start_idx, rem_mask, c_start)
            f = g + h
            heapq.heappush(pq, (f, g, h, counter, start_idx, rem_mask, c_start, [start_idx]))
            counter += 1

        # Best g-cost table: (v_curr, unvisited_mask, c_curr) -> best_g
        visited_best_g: Dict[Tuple[int, int, str], float] = {}

        nodes_expanded = 0

        while pq and nodes_expanded < max_nodes:
            f, g, h, _, v_curr, unvisited_mask, c_curr, path = heapq.heappop(pq)
            nodes_expanded += 1

            # Goal test
            if unvisited_mask == 0:
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                eval_res = evaluate_order(self.stitches, path, d_max=self.d_max, c_trim=self.c_trim)
                return {
                    "order": path,
                    "f_thread": eval_res["f_thread"],
                    "f_switch": eval_res["f_switch"],
                    "cut_tie_count": eval_res["cut_tie_count"],
                    "nodes_expanded": nodes_expanded,
                    "runtime_ms": round(elapsed_ms, 2),
                    "algorithm": "A* Search (Optimal Ground Truth)"
                }

            state_key = (v_curr, unvisited_mask, c_curr)
            if state_key in visited_best_g and visited_best_g[state_key] <= g:
                continue
            visited_best_g[state_key] = g

            # Expand successors: try visiting each unvisited stitch next_idx
            for next_idx in range(self.N):
                if not (unvisited_mask & (1 << next_idx)):
                    continue

                dist = self.dist_mat[v_curr][next_idx]
                c_next = self.colors[next_idx]
                same_color = (c_curr == c_next)
                within_dmax = (dist <= self.d_max)

                # Two-Tier Action Space cost
                if same_color and within_dmax:
                    step_cost = dist
                    step_switch = 0
                else:
                    step_cost = self.c_trim
                    step_switch = 1 if not same_color else 0

                next_g = g + step_cost + (self.weight_switch * step_switch)
                next_mask = unvisited_mask & ~(1 << next_idx)

                next_state_key = (next_idx, next_mask, c_next)
                if next_state_key in visited_best_g and visited_best_g[next_state_key] <= next_g:
                    continue

                next_h = self._heuristic(next_idx, next_mask, c_next)
                next_f = next_g + next_h

                heapq.heappush(
                    pq,
                    (next_f, next_g, next_h, counter, next_idx, next_mask, c_next, path + [next_idx])
                )
                counter += 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "order": [],
            "error": "Node limit exceeded",
            "nodes_expanded": nodes_expanded,
            "runtime_ms": round(elapsed_ms, 2),
        }


def run_astar(
    stitches: List[Dict[str, Any]],
    d_max: float = DEFAULT_D_MAX,
    c_trim: float = DEFAULT_C_TRIM,
    weight_switch: float = 0.0,
) -> Dict[str, Any]:
    solver = AStarMCCPO(stitches, d_max=d_max, c_trim=c_trim, weight_switch=weight_switch)
    return solver.search()


if __name__ == "__main__":
    from sample_patterns import TIER1_MICRO_PATTERNS
    print("=" * 65)
    print("RUNNING A* EXACT OPTIMIZATION ON TIER 1 MICRO PATTERNS (N <= 15)")
    print("=" * 65)

    for name, pattern in TIER1_MICRO_PATTERNS.items():
        res = run_astar(pattern)
        print(f"Pattern: {name:<14} (N={len(pattern):2d}) | Opt f_thread: {res['f_thread']:6.2f} | Switches: {res['f_switch']} | Expanded: {res['nodes_expanded']:6d} | Time: {res['runtime_ms']:6.2f}ms")
