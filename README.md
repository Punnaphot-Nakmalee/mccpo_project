# MCCPO — Multi-Color Cross-Stitch Path Optimization

Complete implementation of the MCCPO research project (Phases 1–4 complete).

## Directory Structure

```text
mccpo_project/
├── data/                             # Benchmark retro pixel art sprites (Tier 2, N=50~200)
├── benchmark_results/                # Generated publication plots, JSON data & trajectories
│   ├── pareto_curve_smiley_13.png
│   ├── pareto_curve_sprite_flower.png
│   ├── scalability_runtime_curve.png
│   ├── pareto_sweep_data.json
│   ├── scalability_data.json
│   └── statistical_rigor_summary.json
├── evaluator.py                      # Two-Tier Action Space cost evaluation engine
├── test_evaluator.py                 # Validation tests comparing stitching strategies
├── parser.py                         # Image parser loading pixel art into stitch lists
├── visualizer.py                     # Matplotlib 2D trajectory & animated GIF generator
├── sample_patterns.py                # Tier 1 micro-benchmarks (N <= 15, 2 colors)
├── generate_dataset.py               # Generates Tier 2 medium sprites and validates them
├── baseline_raster.py                # Baseline 1: Standard Raster Scan
├── baseline_color_scan.py            # Baseline 2: Color-by-Color Sequential Scan
├── baseline_greedy.py                # Baseline 3: Spatial Greedy Nearest Neighbor
├── baseline_uncolored_tsp.py         # Baseline 4: Uncolored 2-Opt TSP
├── benchmark_baselines.py            # Automated baseline benchmark runner across all 10 patterns
├── search_astar.py                   # Tier 1: Informed A* Search Engine (MST + Color Lower Bound)
├── search_sa.py                      # Tier 2: Simulated Annealing (2-opt, color shift, insertion)
├── search_ga.py                      # Tier 2: Genetic Algorithm (OX1 crossover, elitism)
├── benchmark_search.py               # Comprehensive Phase 3 benchmark (Optimality Gap & Improvement)
├── experiment_pareto_sweep.py        # Phase 4: C_trim parameter sweeps & Pareto curve plots
├── experiment_scalability.py         # Phase 4: Dual-panel runtime scaling analysis (A* vs SA vs GA)
├── experiment_statistical_rigor.py   # Phase 4: Multi-seed statistical validation (10 seeds, Mean ± Std)
└── README.md                         # Documentation
```

## Running the Experiments

### 1. Run Pareto Frontier Parameter Sweeps
```bash
python experiment_pareto_sweep.py
```

### 2. Run Scalability Profiling ($N$ vs Runtime)
```bash
python experiment_scalability.py
```

### 3. Run Multi-Seed Statistical Validation
```bash
python experiment_statistical_rigor.py
```
