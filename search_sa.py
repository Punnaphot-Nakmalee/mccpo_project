"""
search_sa.py — Tier 2 Simulated Annealing Engine (N = 50 ~ 1,500)
================================================================
Scalable stochastic metaheuristic for multi-color cross-stitch path optimization.

Key Architecture:
  1. Initialization:
     - Warm-start from Baseline 2 (Color-by-Color) or Baseline 3 (Greedy NN).
  2. Perturbation Operators:
     - Operator A (2-opt sub-sequence reversal): Untangles spatial crossings.
     - Operator B (Color-block shift): Relocates a cluster of same-color stitches.
     - Operator C (Single-stitch insertion): Moves an isolated stitch to a better slot.
  3. Metropolis Acceptance Criterion:
     - Delta = Cost_new - Cost_curr
     - Accept if Delta <= 0, else accept with probability exp(-Delta / T).
  4. Cooling Schedule:
     - Geometric cooling: T_{k+1} = alpha * T_k (default alpha = 0.995).
"""

import math
import random
import time
from typing import List, Dict, Any, Tuple, Optional

from evaluator import evaluate_order, DEFAULT_D_MAX, DEFAULT_C_TRIM
from baseline_color_scan import solve_color_scan
from baseline_greedy import solve_greedy_nn


class SimulatedAnnealingMCCPO:
    def __init__(
        self,
        stitches: List[Dict[str, Any]],
        d_max: float = DEFAULT_D_MAX,
        c_trim: float = DEFAULT_C_TRIM,
        weight_switch: float = 0.0,
        t_start: float = 50.0,
        t_min: float = 1e-4,
        alpha: float = 0.995,
        steps_per_temp: int = 10,
        seed: Optional[int] = 42,
    ):
        self.stitches = stitches
        self.N = len(stitches)
        self.d_max = d_max
        self.c_trim = c_trim
        self.weight_switch = weight_switch
        self.t_start = t_start
        self.t_min = t_min
        self.alpha = alpha
        self.steps_per_temp = steps_per_temp
        self.rng = random.Random(seed)

    def _cost(self, order: List[int]) -> Tuple[float, Dict[str, Any]]:
        res = evaluate_order(self.stitches, order, d_max=self.d_max, c_trim=self.c_trim)
        total_cost = res["f_thread"] + (self.weight_switch * res["f_switch"])
        return total_cost, res

    def _perturb_2opt(self, order: List[int]) -> List[int]:
        """Operator A: 2-opt sub-sequence reversal."""
        if self.N <= 2:
            return order.copy()
        i = self.rng.randint(0, self.N - 2)
        j = self.rng.randint(i + 1, self.N - 1)
        new_order = order.copy()
        new_order[i:j + 1] = reversed(new_order[i:j + 1])
        return new_order

    def _perturb_color_block_shift(self, order: List[int]) -> List[int]:
        """Operator B: Relocates a contiguous cluster of same-color stitches."""
        if self.N <= 3:
            return self._perturb_2opt(order)

        # Find contiguous blocks of same color
        blocks = []
        start = 0
        while start < self.N:
            c = self.stitches[order[start]]["color"]
            end = start
            while end + 1 < self.N and self.stitches[order[end + 1]]["color"] == c:
                end += 1
            blocks.append((start, end))
            start = end + 1

        if len(blocks) <= 1:
            return self._perturb_2opt(order)

        # Pick a random block to relocate
        b_idx = self.rng.randint(0, len(blocks) - 1)
        b_start, b_end = blocks[b_idx]
        block = order[b_start:b_end + 1]

        # Remaining order
        rem_order = order[:b_start] + order[b_end + 1:]
        # Insert at a random insertion point
        insert_pos = self.rng.randint(0, len(rem_order))
        return rem_order[:insert_pos] + block + rem_order[insert_pos:]

    def _perturb_single_insertion(self, order: List[int]) -> List[int]:
        """Operator C: Removes a single stitch and re-inserts it elsewhere."""
        if self.N <= 2:
            return order.copy()
        idx_from = self.rng.randint(0, self.N - 1)
        idx_to = self.rng.randint(0, self.N - 2)
        new_order = order.copy()
        val = new_order.pop(idx_from)
        new_order.insert(idx_to, val)
        return new_order

    def _neighbor(self, order: List[int]) -> List[int]:
        r = self.rng.random()
        if r < 0.50:
            return self._perturb_2opt(order)
        elif r < 0.80:
            return self._perturb_color_block_shift(order)
        else:
            return self._perturb_single_insertion(order)

    def search(self, init_method: str = "color_scan") -> Dict[str, Any]:
        start_time = time.perf_counter()

        if self.N <= 1:
            res = evaluate_order(self.stitches, list(range(self.N)), d_max=self.d_max, c_trim=self.c_trim)
            return {
                "order": list(range(self.N)),
                "f_thread": res["f_thread"],
                "f_switch": res["f_switch"],
                "runtime_ms": 0.0,
                "iterations": 0
            }

        # 1. Initialize solution
        if init_method == "color_scan":
            curr_order = solve_color_scan(self.stitches)
        elif init_method == "greedy":
            curr_order = solve_greedy_nn(self.stitches)
        else:
            curr_order = list(range(self.N))
            self.rng.shuffle(curr_order)

        curr_cost, curr_eval = self._cost(curr_order)
        best_order = curr_order.copy()
        best_cost = curr_cost
        best_eval = curr_eval

        t = self.t_start
        iteration = 0
        accepted_moves = 0

        while t > self.t_min:
            for _ in range(self.steps_per_temp):
                iteration += 1
                cand_order = self._neighbor(curr_order)
                cand_cost, cand_eval = self._cost(cand_order)

                delta = cand_cost - curr_cost

                # Metropolis acceptance
                if delta <= 0:
                    accept = True
                else:
                    prob = math.exp(-delta / t)
                    accept = (self.rng.random() < prob)

                if accept:
                    curr_order = cand_order
                    curr_cost = cand_cost
                    curr_eval = cand_eval
                    accepted_moves += 1

                    if curr_cost < best_cost:
                        best_cost = curr_cost
                        best_order = curr_order.copy()
                        best_eval = curr_eval

            t *= self.alpha

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "order": best_order,
            "f_thread": best_eval["f_thread"],
            "f_switch": best_eval["f_switch"],
            "cut_tie_count": best_eval["cut_tie_count"],
            "best_cost": round(best_cost, 3),
            "iterations": iteration,
            "accepted_moves": accepted_moves,
            "runtime_ms": round(elapsed_ms, 2),
            "algorithm": "Simulated Annealing"
        }


def run_simulated_annealing(
    stitches: List[Dict[str, Any]],
    d_max: float = DEFAULT_D_MAX,
    c_trim: float = DEFAULT_C_TRIM,
    weight_switch: float = 0.0,
    seed: Optional[int] = 42,
    alpha: float = 0.995,
) -> Dict[str, Any]:
    solver = SimulatedAnnealingMCCPO(
        stitches,
        d_max=d_max,
        c_trim=c_trim,
        weight_switch=weight_switch,
        alpha=alpha,
        seed=seed
    )
    return solver.search()


if __name__ == "__main__":
    from sample_patterns import TOY_PATTERN_10
    from parser import load_pattern_from_image

    print("=" * 65)
    print("TESTING SIMULATED ANNEALING ON MICRO & MEDIUM INSTANCES")
    print("=" * 65)

    # 1. Micro
    res_micro = run_simulated_annealing(TOY_PATTERN_10)
    print(f"TOY_PATTERN_10  (N=10) | f_thread: {res_micro['f_thread']:6.2f} | f_switch: {res_micro['f_switch']} | Time: {res_micro['runtime_ms']:6.2f}ms")

    # 2. Medium
    stitches_medium = load_pattern_from_image("data/sprite_flower_16x16.png")
    res_medium = run_simulated_annealing(stitches_medium)
    print(f"sprite_flower   (N={len(stitches_medium)})| f_thread: {res_medium['f_thread']:6.2f} | f_switch: {res_medium['f_switch']} | Time: {res_medium['runtime_ms']:6.2f}ms")
