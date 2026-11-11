"""
search_alns.py — Adaptive Large Neighborhood Search (ALNS) for MCCPO
====================================================================
State-of-the-Art Modern Metaheuristic (2023-2024 Operations Research).

Key Mechanics:
  1. Multi-Armed Bandit / Adaptive Roulette-Wheel operator selection.
  2. Destroy Operators:
     - D1: Color-Boundary Destroy (removes stitches causing color switches)
     - D2: Worst-Cut Destroy (removes transitions with Cut & Tie-Off penalties)
     - D3: Spatial Cluster Destroy (removes localized Euclidean clusters)
     - D4: Random Substring Destroy (breaks local entrapment)
  3. Repair Operators:
     - R1: Color-Affinity Greedy Repair (preserves monochromatic blocks)
     - R2: Cheapest Insertion (Two-Tier Action cost evaluation)
     - R3: Regret-2 Insertion (prioritizes high-regret stitches)
  4. Dynamic Reward System:
     - Sigma 1 (+10): New global best found
     - Sigma 2 (+4):  Improving solution accepted
     - Sigma 3 (+1):  Non-improving solution accepted (SA criterion)
"""

import time
import math
import random
from typing import List, Dict, Any, Tuple, Optional

from evaluator import evaluate_order, euclidean_distance, DEFAULT_D_MAX, DEFAULT_C_TRIM
from baseline_color_scan import solve_color_scan


class ALNSMCCPO:
    def __init__(
        self,
        stitches: List[Dict[str, Any]],
        d_max: float = DEFAULT_D_MAX,
        c_trim: float = DEFAULT_C_TRIM,
        weight_switch: float = 0.0,
        max_iterations: int = 350,
        destroy_fraction: float = 0.15,
        decay_factor: float = 0.85,
        t_start: float = 15.0,
        cooling_rate: float = 0.985,
        seed: Optional[int] = 42,
        w1: float = 0.5,
        w2: float = 0.5,
        normalized: bool = False,
    ):
        self.stitches = stitches
        self.N = len(stitches)
        self.d_max = d_max
        self.c_trim = c_trim
        self.weight_switch = weight_switch
        self.max_iterations = max_iterations
        self.destroy_fraction = destroy_fraction
        # Cap q_destroy between 2 and 18 for high efficiency and focused neighborhood search
        self.q_destroy = max(2, min(18, int(self.N * destroy_fraction)))
        self.decay_factor = decay_factor
        self.t_start = t_start
        self.cooling_rate = cooling_rate
        self.w1 = w1
        self.w2 = w2
        self.normalized = normalized

        # Setup reference metrics for normalized multi-objective mode
        if self.normalized:
            from baseline_color_scan import solve_color_scan
            ref_order = solve_color_scan(self.stitches)
            ref_res = evaluate_order(self.stitches, ref_order, d_max=self.d_max, c_trim=self.c_trim)
            self.ref_f_thread = max(1e-6, ref_res["f_thread"])
            unique_colors = len(set(s["color"] for s in self.stitches))
            self.ref_f_switch = max(1, unique_colors - 1)
            # Rescale initial temperature if left at unnormalized default
            if t_start == 15.0:
                self.t_start = 0.05

        if seed is not None:
            random.seed(seed)

        self.stitch_by_id = {s["id"]: s for s in self.stitches}

        # Operator definitions
        self.destroy_ops = [
            ("Color-Boundary", self._destroy_color_boundary),
            ("Worst-Cut", self._destroy_worst_cuts),
            ("Spatial-Cluster", self._destroy_spatial_cluster),
            ("Random-Substring", self._destroy_random),
        ]
        self.repair_ops = [
            ("Color-Affinity", self._repair_color_affinity),
            ("Cheapest-Insertion", self._repair_cheapest),
            ("Regret-2", self._repair_regret2),
        ]

        num_d = len(self.destroy_ops)
        num_r = len(self.repair_ops)
        self.d_weights = [1.0] * num_d
        self.r_weights = [1.0] * num_r
        self.d_scores = [0.0] * num_d
        self.r_scores = [0.0] * num_r
        self.d_counts = [0] * num_d
        self.r_counts = [0] * num_r

    def _eval(self, order: List[int]) -> Tuple[float, Dict[str, Any]]:
        res = evaluate_order(self.stitches, order, d_max=self.d_max, c_trim=self.c_trim)
        if self.normalized:
            norm_thread = res["f_thread"] / self.ref_f_thread
            norm_switch = res["f_switch"] / self.ref_f_switch
            cost = self.w1 * norm_thread + self.w2 * norm_switch
        else:
            cost = res["f_thread"] + self.weight_switch * res["f_switch"]
        return cost, res

    def _select_operator(self, weights: List[float]) -> int:
        total = sum(weights)
        r = random.uniform(0, total)
        cum = 0.0
        for idx, w in enumerate(weights):
            cum += w
            if r <= cum:
                return idx
        return len(weights) - 1

    # --- DESTROY OPERATORS ---
    def _destroy_color_boundary(self, order: List[int], q: int) -> Tuple[List[int], List[int]]:
        """Removes stitches situated around color transition boundaries."""
        removed = set()
        boundary_indices = []
        for i in range(len(order) - 1):
            s1 = self.stitches[order[i]]
            s2 = self.stitches[order[i + 1]]
            if s1["color"] != s2["color"]:
                boundary_indices.extend([i, i + 1])

        if boundary_indices:
            random.shuffle(boundary_indices)
            for idx in boundary_indices:
                if len(removed) >= q:
                    break
                removed.add(order[idx])

        # Fill remaining if needed
        while len(removed) < q and len(removed) < len(order):
            removed.add(random.choice(order))

        remaining = [x for x in order if x not in removed]
        return remaining, list(removed)

    def _destroy_worst_cuts(self, order: List[int], q: int) -> Tuple[List[int], List[int]]:
        """Removes stitches participating in Cut & Tie-off jumps."""
        _, eval_res = self._eval(order)
        cut_candidates = []
        for tr in eval_res["transitions"]:
            if tr.get("action") == "CUT_AND_TIE" or tr.get("type") == "CUT_AND_TIE":
                cut_candidates.append(tr["from_id"])
                cut_candidates.append(tr["to_id"])

        removed = set()
        random.shuffle(cut_candidates)
        for s_id in cut_candidates:
            if len(removed) >= q:
                break
            removed.add(s_id)

        while len(removed) < q and len(removed) < len(order):
            removed.add(random.choice(order))

        remaining = [x for x in order if x not in removed]
        return remaining, list(removed)

    def _destroy_spatial_cluster(self, order: List[int], q: int) -> Tuple[List[int], List[int]]:
        """Picks a seed stitch and removes its nearest spatial neighbors."""
        seed_id = random.choice(order)
        seed_s = self.stitches[seed_id]
        sorted_by_dist = sorted(order, key=lambda s_id: euclidean_distance(seed_s, self.stitches[s_id]))
        removed = set(sorted_by_dist[:q])
        remaining = [x for x in order if x not in removed]
        return remaining, list(removed)

    def _destroy_random(self, order: List[int], q: int) -> Tuple[List[int], List[int]]:
        """Removes a contiguous or random block of stitches."""
        if random.random() < 0.5 and len(order) > q:
            start = random.randint(0, len(order) - q)
            removed = set(order[start : start + q])
        else:
            removed = set(random.sample(order, q))
        remaining = [x for x in order if x not in removed]
        return remaining, list(removed)

    def _transition_cost(self, id1: Optional[int], id2: Optional[int]) -> float:
        """Computes O(1) two-tier action cost between two stitches."""
        if id1 is None or id2 is None:
            return 0.0
        s1 = self.stitches[id1]
        s2 = self.stitches[id2]
        if s1["color"] == s2["color"]:
            d = euclidean_distance(s1, s2)
            if d <= self.d_max:
                return d
        return self.c_trim

    def _insertion_delta(self, sol: List[int], pos: int, stitch_id: int) -> float:
        """Computes exact O(1) change in cost when inserting stitch_id at index pos."""
        prev_id = sol[pos - 1] if pos > 0 else None
        next_id = sol[pos] if pos < len(sol) else None

        cost_before = self._transition_cost(prev_id, next_id)
        cost_after = self._transition_cost(prev_id, stitch_id) + self._transition_cost(stitch_id, next_id)
        return cost_after - cost_before

    # --- REPAIR OPERATORS ---
    def _repair_color_affinity(self, remaining: List[int], unassigned: List[int]) -> List[int]:
        """Inserts unassigned stitches next to matching color stitches with minimal delta."""
        sol = list(remaining)
        random.shuffle(unassigned)
        for s_id in unassigned:
            s_color = self.stitches[s_id]["color"]
            best_pos = len(sol)
            best_delta = float("inf")

            matching_positions = [
                i for i, existing_id in enumerate(sol)
                if self.stitches[existing_id]["color"] == s_color
            ]
            if not matching_positions:
                cand_pos = list(range(len(sol) + 1))
            else:
                cand_pos = set()
                for p in matching_positions:
                    cand_pos.add(p)
                    cand_pos.add(p + 1)
                cand_pos = sorted(cand_pos)

            for p in cand_pos:
                delta = self._insertion_delta(sol, p, s_id)
                if delta < best_delta:
                    best_delta = delta
                    best_pos = p

            sol.insert(best_pos, s_id)
        return sol

    def _get_candidate_positions(self, sol: List[int], stitch_id: int) -> List[int]:
        """Finds promising insertion positions (prioritizing same-color boundaries)."""
        s_color = self.stitches[stitch_id]["color"]
        matching = [i for i, eid in enumerate(sol) if self.stitches[eid]["color"] == s_color]
        if not matching:
            return list(range(len(sol) + 1))
        
        cand = set()
        for p in matching:
            cand.add(p)
            cand.add(p + 1)
        # Add head and tail
        cand.add(0)
        cand.add(len(sol))
        return sorted([p for p in cand if 0 <= p <= len(sol)])

    def _repair_cheapest(self, remaining: List[int], unassigned: List[int]) -> List[int]:
        """Standard Cheapest Insertion using color-focused candidate positions."""
        sol = list(remaining)
        random.shuffle(unassigned)
        for s_id in unassigned:
            cand_pos = self._get_candidate_positions(sol, s_id)
            best_pos = cand_pos[0] if cand_pos else 0
            best_delta = float("inf")
            for p in cand_pos:
                delta = self._insertion_delta(sol, p, s_id)
                if delta < best_delta:
                    best_delta = delta
                    best_pos = p
            sol.insert(best_pos, s_id)
        return sol

    def _repair_regret2(self, remaining: List[int], unassigned: List[int]) -> List[int]:
        """Regret-2 Insertion heuristic using color-focused candidate positions."""
        sol = list(remaining)
        pool = list(unassigned)

        while pool:
            best_stitch = None
            max_regret = -1.0
            best_insertion_pos = 0

            for s_id in pool:
                cand_pos = self._get_candidate_positions(sol, s_id)
                deltas = []
                for p in cand_pos:
                    d = self._insertion_delta(sol, p, s_id)
                    deltas.append((d, p))
                deltas.sort(key=lambda x: x[0])

                best_d, best_p = deltas[0]
                second_best_d = deltas[1][0] if len(deltas) > 1 else best_d
                regret = second_best_d - best_d

                if regret > max_regret:
                    max_regret = regret
                    best_stitch = s_id
                    best_insertion_pos = best_p

            if best_stitch is None:
                best_stitch = pool[0]
                best_insertion_pos = len(sol)

            sol.insert(best_insertion_pos, best_stitch)
            pool.remove(best_stitch)

        return sol

    # --- MAIN SEARCH LOOP ---
    def search(self, init_method: str = "color_scan") -> Dict[str, Any]:
        start_time = time.perf_counter()

        if init_method == "color_scan":
            curr_order = solve_color_scan(self.stitches)
        else:
            curr_order = list(range(self.N))
            random.shuffle(curr_order)

        curr_cost, curr_eval = self._eval(curr_order)
        best_order = list(curr_order)
        best_cost = curr_cost
        best_eval = curr_eval

        temp = self.t_start
        segment_length = 25

        for it in range(1, self.max_iterations + 1):
            # Select operators via roulette wheel
            d_idx = self._select_operator(self.d_weights)
            r_idx = self._select_operator(self.r_weights)
            self.d_counts[d_idx] += 1
            self.r_counts[r_idx] += 1

            d_name, d_fn = self.destroy_ops[d_idx]
            r_name, r_fn = self.repair_ops[r_idx]

            # Apply destroy & repair
            remaining, unassigned = d_fn(curr_order, self.q_destroy)
            cand_order = r_fn(remaining, unassigned)
            cand_cost, cand_eval = self._eval(cand_order)

            delta = cand_cost - curr_cost
            reward = 0.0

            # Acceptance criterion (Simulated Annealing criterion)
            if cand_cost < best_cost:
                best_order = list(cand_order)
                best_cost = cand_cost
                best_eval = cand_eval
                curr_order = list(cand_order)
                curr_cost = cand_cost
                curr_eval = cand_eval
                reward = 10.0  # Sigma 1: New global best
            elif delta <= 0:
                curr_order = list(cand_order)
                curr_cost = cand_cost
                curr_eval = cand_eval
                reward = 4.0   # Sigma 2: Better than current
            elif temp > 0.001 and random.random() < math.exp(-delta / temp):
                curr_order = list(cand_order)
                curr_cost = cand_cost
                curr_eval = cand_eval
                reward = 1.0   # Sigma 3: Accepted worse

            self.d_scores[d_idx] += reward
            self.r_scores[r_idx] += reward

            # Dynamic weight update at segment end
            if it % segment_length == 0:
                for i in range(len(self.d_weights)):
                    if self.d_counts[i] > 0:
                        self.d_weights[i] = (
                            self.decay_factor * self.d_weights[i]
                            + (1.0 - self.decay_factor) * (self.d_scores[i] / self.d_counts[i])
                        )
                        self.d_scores[i] = 0.0
                        self.d_counts[i] = 0

                for j in range(len(self.r_weights)):
                    if self.r_counts[j] > 0:
                        self.r_weights[j] = (
                            self.decay_factor * self.r_weights[j]
                            + (1.0 - self.decay_factor) * (self.r_scores[j] / self.r_counts[j])
                        )
                        self.r_scores[j] = 0.0
                        self.r_counts[j] = 0

            temp *= self.cooling_rate

        runtime_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "order": best_order,
            "cost": best_cost,
            "f_thread": best_eval["f_thread"],
            "f_switch": best_eval["f_switch"],
            "cut_tie_count": best_eval["cut_tie_count"],
            "runtime_ms": runtime_ms,
            "iterations": self.max_iterations,
        }


if __name__ == "__main__":
    from parser import load_pattern_from_image
    import os
    data_path = os.path.join(os.path.dirname(__file__), "data", "sprite_flower_16x16.png")
    stitches = load_pattern_from_image(data_path, normalize_origin=True)
    solver = ALNSMCCPO(stitches, max_iterations=200, seed=42)
    res = solver.search()
    print("=== ALNS MCCPO BENCHMARK ===")
    print(f"Thread Cost : {res['f_thread']:.2f}")
    print(f"Switches    : {res['f_switch']}")
    print(f"Runtime (ms): {res['runtime_ms']:.2f} ms")
