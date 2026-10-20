"""
search_ga.py — Tier 2 Genetic Algorithm Engine (N = 50 ~ 1,500)
==============================================================
Population-based evolutionary metaheuristic for multi-color cross-stitch
path optimization.

Key Architecture:
  1. Chromosome Representation:
     - Permutation array pi of stitch indices [0, 1, ..., N-1].
  2. Population Seeding:
     - Includes heuristic seeds (Baseline 2, Baseline 3) + randomized permutations
       to balance exploitation and genetic diversity.
  3. Fitness Evaluation:
     - Fitness = 1.0 / (Cost + 1e-6), where Cost = f_thread + lambda * f_switch.
  4. Selection:
     - Tournament selection (size k=3).
  5. Crossover:
     - Order Crossover (OX1): Preserves sub-tours from parent 1 while filling
       remaining relative orders from parent 2. Guarantees valid permutations.
  6. Mutation Operators:
     - Swap mutation (exchanges two genes).
     - Inversion mutation (reverses sub-string, 2-opt style).
  7. Elitism:
     - Clones top elite individuals directly to next generation.
"""

import random
import time
from typing import List, Dict, Any, Tuple, Optional

from evaluator import evaluate_order, DEFAULT_D_MAX, DEFAULT_C_TRIM
from baseline_color_scan import solve_color_scan
from baseline_greedy import solve_greedy_nn


class GeneticAlgorithmMCCPO:
    def __init__(
        self,
        stitches: List[Dict[str, Any]],
        d_max: float = DEFAULT_D_MAX,
        c_trim: float = DEFAULT_C_TRIM,
        weight_switch: float = 0.0,
        pop_size: int = 50,
        generations: int = 100,
        crossover_rate: float = 0.85,
        mutation_rate: float = 0.20,
        tournament_size: int = 3,
        elitism_count: int = 2,
        seed: Optional[int] = 42,
    ):
        self.stitches = stitches
        self.N = len(stitches)
        self.d_max = d_max
        self.c_trim = c_trim
        self.weight_switch = weight_switch
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism_count = elitism_count
        self.rng = random.Random(seed)

    def _cost(self, order: List[int]) -> Tuple[float, Dict[str, Any]]:
        res = evaluate_order(self.stitches, order, d_max=self.d_max, c_trim=self.c_trim)
        cost = res["f_thread"] + (self.weight_switch * res["f_switch"])
        return cost, res

    def _initialize_population(self) -> List[List[int]]:
        population = []
        
        # Seed 1: Baseline 2 (Color-by-Color)
        b2 = solve_color_scan(self.stitches)
        population.append(b2)
        
        # Seed 2: Baseline 3 (Greedy NN)
        b3 = solve_greedy_nn(self.stitches)
        population.append(b3)

        # Mutated seeds around B2 and B3
        for seed_tour in [b2, b3]:
            for _ in range(5):
                mutated = seed_tour.copy()
                self._mutate_inversion(mutated)
                population.append(mutated)

        # Remaining random permutations
        base_indices = list(range(self.N))
        while len(population) < self.pop_size:
            ind = base_indices.copy()
            self.rng.shuffle(ind)
            population.append(ind)

        return population[:self.pop_size]

    def _tournament_select(self, population: List[List[int]], costs: List[float]) -> List[int]:
        candidates = self.rng.sample(range(len(population)), self.tournament_size)
        best_cand = min(candidates, key=lambda idx: costs[idx])
        return population[best_cand].copy()

    def _order_crossover_ox1(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """
        Standard Order Crossover (OX1):
        Copies slice from parent1, fills remaining slots with order from parent2.
        """
        if self.N <= 2:
            return parent1.copy()

        i = self.rng.randint(0, self.N - 2)
        j = self.rng.randint(i + 1, self.N - 1)

        child = [-1] * self.N
        # Copy slice
        child[i:j + 1] = parent1[i:j + 1]
        copied_set = set(child[i:j + 1])

        # Fill remaining from parent2 in cyclic order starting at j+1
        p2_idx = (j + 1) % self.N
        child_idx = (j + 1) % self.N

        for _ in range(self.N):
            val = parent2[p2_idx]
            if val not in copied_set:
                child[child_idx] = val
                child_idx = (child_idx + 1) % self.N
            p2_idx = (p2_idx + 1) % self.N

        return child

    def _mutate_swap(self, individual: List[int]):
        i, j = self.rng.sample(range(self.N), 2)
        individual[i], individual[j] = individual[j], individual[i]

    def _mutate_inversion(self, individual: List[int]):
        i = self.rng.randint(0, self.N - 2)
        j = self.rng.randint(i + 1, self.N - 1)
        individual[i:j + 1] = reversed(individual[i:j + 1])

    def search(self) -> Dict[str, Any]:
        start_time = time.perf_counter()

        if self.N <= 1:
            res = evaluate_order(self.stitches, list(range(self.N)), d_max=self.d_max, c_trim=self.c_trim)
            return {
                "order": list(range(self.N)),
                "f_thread": res["f_thread"],
                "f_switch": res["f_switch"],
                "runtime_ms": 0.0,
                "generations": 0
            }

        population = self._initialize_population()
        evals = [self._cost(ind) for ind in population]
        costs = [e[0] for e in evals]

        best_idx = min(range(len(costs)), key=lambda i: costs[i])
        best_cost = costs[best_idx]
        best_order = population[best_idx].copy()
        best_eval = evals[best_idx][1]

        for gen in range(self.generations):
            # Sort for elitism
            sorted_indices = sorted(range(len(population)), key=lambda i: costs[i])
            new_population = [population[i].copy() for i in sorted_indices[:self.elitism_count]]

            while len(new_population) < self.pop_size:
                p1 = self._tournament_select(population, costs)
                p2 = self._tournament_select(population, costs)

                if self.rng.random() < self.crossover_rate:
                    child = self._order_crossover_ox1(p1, p2)
                else:
                    child = p1.copy()

                if self.rng.random() < self.mutation_rate:
                    if self.rng.random() < 0.5:
                        self._mutate_inversion(child)
                    else:
                        self._mutate_swap(child)

                new_population.append(child)

            population = new_population
            evals = [self._cost(ind) for ind in population]
            costs = [e[0] for e in evals]

            cur_best_idx = min(range(len(costs)), key=lambda i: costs[i])
            if costs[cur_best_idx] < best_cost:
                best_cost = costs[cur_best_idx]
                best_order = population[cur_best_idx].copy()
                best_eval = evals[cur_best_idx][1]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "order": best_order,
            "f_thread": best_eval["f_thread"],
            "f_switch": best_eval["f_switch"],
            "cut_tie_count": best_eval["cut_tie_count"],
            "best_cost": round(best_cost, 3),
            "generations": self.generations,
            "runtime_ms": round(elapsed_ms, 2),
            "algorithm": "Genetic Algorithm"
        }


def run_genetic_algorithm(
    stitches: List[Dict[str, Any]],
    d_max: float = DEFAULT_D_MAX,
    c_trim: float = DEFAULT_C_TRIM,
    weight_switch: float = 0.0,
    pop_size: int = 50,
    generations: int = 100,
    seed: Optional[int] = 42,
) -> Dict[str, Any]:
    solver = GeneticAlgorithmMCCPO(
        stitches,
        d_max=d_max,
        c_trim=c_trim,
        weight_switch=weight_switch,
        pop_size=pop_size,
        generations=generations,
        seed=seed
    )
    return solver.search()


if __name__ == "__main__":
    from sample_patterns import TOY_PATTERN_10
    from parser import load_pattern_from_image

    print("=" * 65)
    print("TESTING GENETIC ALGORITHM ON MICRO & MEDIUM INSTANCES")
    print("=" * 65)

    # 1. Micro
    res_micro = run_genetic_algorithm(TOY_PATTERN_10, generations=50)
    print(f"TOY_PATTERN_10  (N=10) | f_thread: {res_micro['f_thread']:6.2f} | f_switch: {res_micro['f_switch']} | Time: {res_micro['runtime_ms']:6.2f}ms")

    # 2. Medium
    stitches_medium = load_pattern_from_image("data/sprite_flower_16x16.png")
    res_medium = run_genetic_algorithm(stitches_medium, generations=100)
    print(f"sprite_flower   (N={len(stitches_medium)})| f_thread: {res_medium['f_thread']:6.2f} | f_switch: {res_medium['f_switch']} | Time: {res_medium['runtime_ms']:6.2f}ms")
