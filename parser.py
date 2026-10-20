"""
parser.py — Image Grid Parser for MCCPO
=========================================
Loads a PNG pixel-art image and converts it into a list of stitch dicts
compatible with evaluator.py.

Stitch format:
    {"id": int, "x": int, "y": int, "color": str}

Usage:
    from parser import load_pattern_from_image
    stitches = load_pattern_from_image("my_pattern.png")
"""

from PIL import Image
import math


# ---------------------------------------------------------------------------
# Helper: Euclidean distance in RGB space
# ---------------------------------------------------------------------------

def _rgb_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


# ---------------------------------------------------------------------------
# Helper: Quantize a raw RGB list to a small palette
# ---------------------------------------------------------------------------

def _quantize_colors(raw_colors, max_colors=16):
    """
    Simple greedy k-means-style palette builder.
    Returns a list of representative RGB tuples (the palette).
    """
    palette = []
    for color in raw_colors:
        if not palette:
            palette.append(color)
            continue
        # Find closest existing palette entry
        closest_dist = min(_rgb_distance(color, p) for p in palette)
        # If it's too far from all existing palette entries, it's a new color
        if closest_dist > 30 and len(palette) < max_colors:
            palette.append(color)
    return palette


def _assign_palette_index(color, palette):
    """Return the index of the nearest palette entry to `color`."""
    return min(range(len(palette)), key=lambda i: _rgb_distance(color, palette[i]))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_pattern_from_image(
    path,
    bg_color=(255, 255, 255),
    bg_tolerance=30,
    max_colors=16,
    normalize_origin=True,
):
    """
    Load a PNG pixel-art image and extract stitches.

    Parameters
    ----------
    path : str
        Absolute or relative path to the PNG file.
    bg_color : tuple of int
        RGB of the background color to ignore (default: white).
    bg_tolerance : int
        Maximum RGB distance from bg_color to still be treated as background.
    max_colors : int
        Maximum palette size (colors beyond this are merged to nearest).
    normalize_origin : bool
        If True, shifts coordinates so min(x)=0 and min(y)=0 (removes whitespace border).

    Returns
    -------
    list of dict
        Each dict: {"id": int, "x": int, "y": int, "color": str}
        where "color" is "color_0", "color_1", ... matching palette index.
    """
    img = Image.open(path).convert("RGB")
    width, height = img.size
    try:
        pixels = list(img.get_flattened_data())
    except AttributeError:
        pixels = list(img.getdata())

    # --- Pass 1: collect all non-background raw colors ---
    raw_fg_colors = []
    for idx, px in enumerate(pixels):
        if _rgb_distance(px, bg_color) > bg_tolerance:
            raw_fg_colors.append(px)

    if not raw_fg_colors:
        raise ValueError(f"No foreground pixels found in '{path}' (bg_tolerance={bg_tolerance}).")

    # --- Build palette ---
    palette = _quantize_colors(raw_fg_colors, max_colors=max_colors)

    # --- Pass 2: extract stitches ---
    stitches = []
    stitch_id = 0
    for idx, px in enumerate(pixels):
        if _rgb_distance(px, bg_color) <= bg_tolerance:
            continue  # background pixel — skip
        x = idx % width
        y = idx // width
        palette_idx = _assign_palette_index(px, palette)
        stitches.append({
            "id": stitch_id,
            "x": x,
            "y": y,
            "color": f"color_{palette_idx}",
        })
        stitch_id += 1

    # --- Coordinate offset normalization ---
    if normalize_origin and stitches:
        min_x = min(s["x"] for s in stitches)
        min_y = min(s["y"] for s in stitches)
        for s in stitches:
            s["x"] -= min_x
            s["y"] -= min_y

    return stitches


def describe_pattern(stitches):
    """Print a compact summary of a parsed stitch list."""
    colors = {}
    for s in stitches:
        colors[s["color"]] = colors.get(s["color"], 0) + 1
    xs = [s["x"] for s in stitches]
    ys = [s["y"] for s in stitches]
    print(f"Stitches : {len(stitches)}")
    print(f"Colors   : {len(colors)} -> {colors}")
    print(f"Bounds   : x=[{min(xs)},{max(xs)}]  y=[{min(ys)},{max(ys)}]")


# ---------------------------------------------------------------------------
# Quick self-test (runs when executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    # Generate a tiny test PNG programmatically and parse it back
    test_path = "test_parser_sprite.png"

    # Create a small 5×5 test image: red top-left 3×3, blue bottom-right 3×3
    img = Image.new("RGB", (5, 5), (255, 255, 255))  # white background
    pixels = img.load()
    for y in range(3):
        for x in range(3):
            pixels[x, y] = (200, 30, 30)   # red region
    for y in range(2, 5):
        for x in range(2, 5):
            pixels[x, y] = (30, 30, 200)   # blue region (overlaps at (2,2))

    img.save(test_path)
    print(f"Saved test image: {test_path}")

    stitches = load_pattern_from_image(test_path)
    describe_pattern(stitches)
    print("\nFirst 5 stitches:")
    for s in stitches[:5]:
        print(f"  {s}")

    os.remove(test_path)
    print("\nSelf-test passed.")
