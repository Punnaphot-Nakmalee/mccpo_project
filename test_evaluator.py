"""
test_evaluator.py
Unit tests and demonstration comparing different stitching sequences on the 10-stitch toy pattern.
"""

from sample_patterns import TOY_PATTERN_10, print_pattern_ascii
from evaluator import evaluate_sequence

def run_demonstration():
    print("=" * 60)
    print("MCCPO EVALUATION ENGINE - DEMONSTRATION")
    print("=" * 60)
    
    # 1. Display Pattern
    print_pattern_ascii(TOY_PATTERN_10)

    # 2. Candidate Sequence 1: Color-by-Color Strategy
    # Visit all 6 Red stitches, then switch to Blue and visit all 4 Blue stitches
    seq_color_by_color = [
        TOY_PATTERN_10[0], # R (1,3)
        TOY_PATTERN_10[1], # R (2,4)
        TOY_PATTERN_10[2], # R (3,4)
        TOY_PATTERN_10[3], # R (4,3)
        TOY_PATTERN_10[4], # R (3,2)
        TOY_PATTERN_10[5], # R (2,2)
        TOY_PATTERN_10[6], # B (2,1) -> Color Change!
        TOY_PATTERN_10[7], # B (3,1)
        TOY_PATTERN_10[9], # B (4,0)
        TOY_PATTERN_10[8], # B (1,0)
    ]
    
    # 3. Candidate Sequence 2: Alternating / Chaotic Strategy
    # Alternates between Red and Blue stitches (High color change penalty)
    seq_alternating = [
        TOY_PATTERN_10[0], # R
        TOY_PATTERN_10[8], # B -> Switch
        TOY_PATTERN_10[1], # R -> Switch
        TOY_PATTERN_10[6], # B -> Switch
        TOY_PATTERN_10[2], # R -> Switch
        TOY_PATTERN_10[7], # B -> Switch
        TOY_PATTERN_10[3], # R -> Switch
        TOY_PATTERN_10[9], # B -> Switch
        TOY_PATTERN_10[4], # R -> Switch
        TOY_PATTERN_10[5], # R
    ]

    # Evaluate both sequences with d_max = 3.16, C_trim = 10.0
    res_color = evaluate_sequence(seq_color_by_color, d_max=3.162, c_trim=10.0)
    res_alt = evaluate_sequence(seq_alternating, d_max=3.162, c_trim=10.0)

    print("\n[Strategy 1: Color-by-Color]")
    print(f"  * Total Thread Cost (f_thread): {res_color['f_thread']}")
    print(f"  * Total Color Changes (f_switch): {res_color['f_switch']}")
    print(f"  * Pure Carried Distance:        {res_color['carried_distance']}")
    print(f"  * Cut & Tie-Off Count:          {res_color['cut_tie_count']}")

    print("\n[Strategy 2: Alternating Colors (Worst Case)]")
    print(f"  * Total Thread Cost (f_thread): {res_alt['f_thread']}")
    print(f"  * Total Color Changes (f_switch): {res_alt['f_switch']}")
    print(f"  * Pure Carried Distance:        {res_alt['carried_distance']}")
    print(f"  * Cut & Tie-Off Count:          {res_alt['cut_tie_count']}")

    print("\n--- Detailed Step Breakdown for Strategy 1 (Color-by-Color) ---")
    for t in res_color["transitions"]:
        action_desc = "CARRY" if t["action"] == "CONTINUOUS_CARRY" else "CUT & TIE"
        print(f"  Step {t['step']}: Stitch {t['from_id']} ({t['from_color']}) -> Stitch {t['to_id']} ({t['to_color']}) "
              f"| Dist: {t['distance']:<5} | Action: {action_desc:<9} | Cost: {t['cost']}")

    print("\nConclusion:")
    diff_thread = res_alt['f_thread'] - res_color['f_thread']
    print(f"  -> Color-by-Color saves {diff_thread:.2f} thread units and avoids {res_alt['f_switch'] - res_color['f_switch']} color changes!")
    print("=" * 60)

if __name__ == "__main__":
    run_demonstration()
