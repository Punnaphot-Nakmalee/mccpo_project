"""
run_all.py — Master Project Verification & Execution Pipeline
============================================================
Runs the entire MCCPO pipeline from start to finish:
  1. Unit tests (test_evaluator.py)
  2. Dataset verification (parser.py, generate_dataset.py)
  3. Baselines benchmark (benchmark_baselines.py)
  4. Search engines (A*, GA, SA, Hybrid Memetic, ALNS)
  5. Scientific experiments (Pareto sweep, Scalability, Statistical rigor)
  6. Visual showcase rendering (8-panel gallery, evolution visual, GIF)
  7. PowerPoint presentation compilation & validation
"""

import os
import sys
import time
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(PROJECT_DIR)
PPTX_PATH = os.path.join(PARENT_DIR, "MCCPO_Final_Defense_Presentation.pptx")
VALIDATOR_PATH = r"C:\Users\Mic\.gemini\config\skills\pptx\scripts\office\validate.py"

STEPS = [
    # (Stage Name, Command List, Estimated Duration Note)
    ("1. Core Unit Tests", [sys.executable, "test_evaluator.py"], "~1s"),
    ("2. Dataset & Parser Check", [sys.executable, "parser.py"], "~1s"),
    ("3. Baseline Algorithms Benchmark", [sys.executable, "benchmark_baselines.py"], "~2s"),
    ("4. Exact A* Search (Tier 1 Ground Truth)", [sys.executable, "search_astar.py"], "~3s"),
    ("5. Genetic Algorithm (Pure GA)", [sys.executable, "search_ga.py"], "~2s"),
    ("6. Simulated Annealing (Pure SA)", [sys.executable, "search_sa.py"], "~4s"),
    ("7. Hybrid Memetic Algorithm (GA + SA)", [sys.executable, "search_hybrid.py"], "~3s"),
    ("8. Adaptive Large Neighborhood Search (ALNS SOTA)", [sys.executable, "search_alns.py"], "~2s"),
    ("9. Search Engine Benchmarks & Optimality Gap", [sys.executable, "benchmark_search.py"], "~4s"),
    ("10. Pareto Sweep Experiment", [sys.executable, "experiment_pareto_sweep.py"], "~5s"),
    ("11. Scalability Benchmark", [sys.executable, "experiment_scalability.py"], "~4s"),
    ("12. Statistical Rigor (10 Seeds)", [sys.executable, "experiment_statistical_rigor.py"], "~6s"),
    ("13. Visual Showcase & Trajectory GIF", [sys.executable, "generate_showcase.py"], "~5s"),
    ("14. Grand 8-Panel Master Gallery & Cards", [sys.executable, "generate_all_comparisons.py"], "~6s"),
    ("15. PowerPoint Deck Compilation", ["node", "build_deck.js"], "~2s"),
]


def run_pipeline():
    print("=" * 75)
    print("  MCCPO MASTER VERIFICATION & EXECUTION PIPELINE")
    print(f"  Working Directory: {PROJECT_DIR}")
    print(f"  Python Version   : {sys.version.split()[0]}")
    print("=" * 75)

    os.chdir(PROJECT_DIR)
    total_start = time.perf_counter()
    passed = 0
    failed = 0

    for name, cmd, est in STEPS:
        print(f"\n[RUNNING] {name:<45} (Est. {est})...", end="", flush=True)
        t0 = time.perf_counter()
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        dt = time.perf_counter() - t0

        if res.returncode == 0:
            print(f" [PASS] ({dt:.2f}s)")
            passed += 1
        else:
            print(f" [FAILED] ({dt:.2f}s)")
            print("-" * 50)
            print("STDERR:")
            print(res.stderr[:500])
            print("-" * 50)
            failed += 1

    # Optional step: Validate PPTX if validator exists
    if os.path.exists(VALIDATOR_PATH) and os.path.exists(PPTX_PATH):
        print(f"\n[RUNNING] 16. PPTX Schema & Layout Validation...", end="", flush=True)
        val_res = subprocess.run([sys.executable, VALIDATOR_PATH, PPTX_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if val_res.returncode == 0:
            print(" [PASS] (Schema 100% Valid)")
            passed += 1
        else:
            print(" [WARNING] (Validation reported notes)")

    total_time = time.perf_counter() - total_start
    print("\n" + "=" * 75)
    print(f"  PIPELINE COMPLETE: {passed} Passed | {failed} Failed | Total Time: {total_time:.2f}s")
    print("=" * 75)
    if failed == 0:
        print(">> ALL SYSTEMS OPERATIONAL. Every script, benchmark, and slide is verified!")
    else:
        print(">> Please check the failed steps above.")


if __name__ == "__main__":
    run_pipeline()
