"""
sample_patterns.py
Defines benchmark cross-stitch patterns for micro-validation and unit testing.

Includes:
- Tier 1: 5 Tiny Toy Patterns (N <= 15, 2 colors) for exact A* validation.
  1. PATTERN_HEART_10 (N=10)
  2. PATTERN_CROSS_12 (N=12)
  3. PATTERN_CHECKER_8 (N=8)
  4. PATTERN_LETTER_A_14 (N=14)
  5. PATTERN_SMILEY_13 (N=13)
"""

from typing import List, Dict, Any

# ===========================================================================
# 1. Mini Heart (N=10, 2 colors: 6 red, 4 blue)
# ===========================================================================
PATTERN_HEART_10 = [
    # Red stitches (heart body)
    {"id": 0, "x": 1, "y": 3, "color": "red"},
    {"id": 1, "x": 2, "y": 4, "color": "red"},
    {"id": 2, "x": 3, "y": 4, "color": "red"},
    {"id": 3, "x": 4, "y": 3, "color": "red"},
    {"id": 4, "x": 3, "y": 2, "color": "red"},
    {"id": 5, "x": 2, "y": 2, "color": "red"},
    # Blue stitches (accent base)
    {"id": 6, "x": 2, "y": 1, "color": "blue"},
    {"id": 7, "x": 3, "y": 1, "color": "blue"},
    {"id": 8, "x": 1, "y": 0, "color": "blue"},
    {"id": 9, "x": 4, "y": 0, "color": "blue"}
]
TOY_PATTERN_10 = PATTERN_HEART_10  # Backwards compatibility alias


# ===========================================================================
# 2. Celtic Cross (N=12, 2 colors: 4 gold core, 8 blue arms)
# ===========================================================================
PATTERN_CROSS_12 = [
    # Gold core (2x2 center)
    {"id": 0, "x": 2, "y": 2, "color": "gold"},
    {"id": 1, "x": 3, "y": 2, "color": "gold"},
    {"id": 2, "x": 2, "y": 3, "color": "gold"},
    {"id": 3, "x": 3, "y": 3, "color": "gold"},
    # Blue arms (north, south, east, west)
    {"id": 4, "x": 2, "y": 4, "color": "blue"},
    {"id": 5, "x": 3, "y": 4, "color": "blue"},
    {"id": 6, "x": 2, "y": 1, "color": "blue"},
    {"id": 7, "x": 3, "y": 1, "color": "blue"},
    {"id": 8, "x": 1, "y": 2, "color": "blue"},
    {"id": 9, "x": 1, "y": 3, "color": "blue"},
    {"id": 10, "x": 4, "y": 2, "color": "blue"},
    {"id": 11, "x": 4, "y": 3, "color": "blue"}
]


# ===========================================================================
# 3. Interleaved Checkerboard (N=8, 2 colors: 4 black, 4 white)
# Tests spatial interleaving stress where spatial proximity conflicts with color
# ===========================================================================
PATTERN_CHECKER_8 = [
    # Black stitches
    {"id": 0, "x": 0, "y": 0, "color": "black"},
    {"id": 1, "x": 2, "y": 0, "color": "black"},
    {"id": 2, "x": 1, "y": 1, "color": "black"},
    {"id": 3, "x": 3, "y": 1, "color": "black"},
    # White/Cyan stitches
    {"id": 4, "x": 1, "y": 0, "color": "cyan"},
    {"id": 5, "x": 3, "y": 0, "color": "cyan"},
    {"id": 6, "x": 0, "y": 1, "color": "cyan"},
    {"id": 7, "x": 2, "y": 1, "color": "cyan"}
]


# ===========================================================================
# 4. Monogram Letter 'A' (N=14, 2 colors: 10 navy frame, 4 orange bar)
# ===========================================================================
PATTERN_LETTER_A_14 = [
    # Navy vertical legs and apex
    {"id": 0, "x": 1, "y": 0, "color": "navy"},
    {"id": 1, "x": 1, "y": 1, "color": "navy"},
    {"id": 2, "x": 1, "y": 2, "color": "navy"},
    {"id": 3, "x": 1, "y": 3, "color": "navy"},
    {"id": 4, "x": 2, "y": 4, "color": "navy"},
    {"id": 5, "x": 3, "y": 4, "color": "navy"},
    {"id": 6, "x": 4, "y": 3, "color": "navy"},
    {"id": 7, "x": 4, "y": 2, "color": "navy"},
    {"id": 8, "x": 4, "y": 1, "color": "navy"},
    {"id": 9, "x": 4, "y": 0, "color": "navy"},
    # Orange crossbar
    {"id": 10, "x": 2, "y": 2, "color": "orange"},
    {"id": 11, "x": 3, "y": 2, "color": "orange"},
    {"id": 12, "x": 2, "y": 1, "color": "orange"},
    {"id": 13, "x": 3, "y": 1, "color": "orange"}
]


# ===========================================================================
# 5. Smiley Face (N=13, 2 colors: 4 green eyes, 9 yellow smile)
# ===========================================================================
PATTERN_SMILEY_13 = [
    # Green eyes (2x1 each)
    {"id": 0, "x": 1, "y": 4, "color": "green"},
    {"id": 1, "x": 1, "y": 3, "color": "green"},
    {"id": 2, "x": 4, "y": 4, "color": "green"},
    {"id": 3, "x": 4, "y": 3, "color": "green"},
    # Yellow smile arc
    {"id": 4, "x": 0, "y": 2, "color": "yellow"},
    {"id": 5, "x": 1, "y": 1, "color": "yellow"},
    {"id": 6, "x": 2, "y": 0, "color": "yellow"},
    {"id": 7, "x": 3, "y": 0, "color": "yellow"},
    {"id": 8, "x": 4, "y": 1, "color": "yellow"},
    {"id": 9, "x": 5, "y": 2, "color": "yellow"},
    {"id": 10, "x": 2, "y": 1, "color": "yellow"},
    {"id": 11, "x": 3, "y": 1, "color": "yellow"},
    {"id": 12, "x": 0, "y": 3, "color": "yellow"}
]


# Registry dictionary of all Tier 1 micro-benchmark patterns
TIER1_MICRO_PATTERNS = {
    "heart_10": PATTERN_HEART_10,
    "cross_12": PATTERN_CROSS_12,
    "checker_8": PATTERN_CHECKER_8,
    "letter_a_14": PATTERN_LETTER_A_14,
    "smiley_13": PATTERN_SMILEY_13
}


def print_pattern_ascii(stitches: List[Dict[str, Any]], width: int = 6, height: int = 6):
    """Utility to print an ASCII grid representation of any pattern."""
    grid = [["." for _ in range(width)] for _ in range(height)]
    for s in stitches:
        char = s["color"][0].upper()
        if 0 <= s["y"] < height and 0 <= s["x"] < width:
            grid[s["y"]][s["x"]] = char
        
    print("\n--- Pattern Layout (ASCII Grid) ---")
    for y in reversed(range(height)):
        row_str = " ".join(grid[y])
        print(f"y={y:2d} | {row_str}")
    print("      " + " ".join(f"{x%10}" for x in range(width)))
    print("----------------------------------\n")


if __name__ == "__main__":
    for name, pattern in TIER1_MICRO_PATTERNS.items():
        print(f"\nPattern: {name} (N={len(pattern)})")
        xs = [s["x"] for s in pattern]
        ys = [s["y"] for s in pattern]
        print_pattern_ascii(pattern, width=max(xs)+2, height=max(ys)+2)
