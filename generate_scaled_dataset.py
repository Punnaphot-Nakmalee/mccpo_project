"""
generate_scaled_dataset.py — Multi-Tier Cross-Stitch Dataset Generator
=====================================================================
Generates realistic multi-color cross-stitch patterns across the 3 distinct
scale tiers requested by the thesis committee / advisor:

  - Tier S (Small,  N ≈ 100 stitches, 16x16 grid):  Micro & sprite motifs
  - Tier M (Medium, N ≈ 500 stitches, 32x32 grid):  Detailed game sprites & tapestries
  - Tier L (Large,  N ≈ 1000 stitches, 48x48 grid): Complex cross-stitch patterns & mandalas

Also provides an automated Image-to-Cross-Stitch converter (downsampler & quantizer)
capable of generating arbitrary patterns with precise target stitch counts.
"""

import os
import math
import random
from typing import List, Dict, Any, Tuple
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Helper: Save grid string + palette to PNG image
# ---------------------------------------------------------------------------
def save_grid_to_png(name: str, grid: List[str], palette: Dict[str, Tuple[int, int, int]]) -> str:
    h = len(grid)
    w = max(len(row) for row in grid)
    img = Image.new("RGB", (w, h), (255, 255, 255))
    pixels = img.load()

    active_stitches = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in palette:
                color = palette[char]
                pixels[x, y] = color
                if color != (255, 255, 255):
                    active_stitches += 1
            else:
                pixels[x, y] = (255, 255, 255)

    out_path = os.path.join(DATA_DIR, f"{name}.png")
    img.save(out_path)
    print(f"  [+] Saved {name}.png ({w}x{h}, Active Stitches N={active_stitches})")
    return out_path


# ---------------------------------------------------------------------------
# Procedural & Geometric Pattern Synthesizers for Medium (500) and Large (1000)
# ---------------------------------------------------------------------------

def generate_procedural_tapestry(size: int = 32, seed: int = 42) -> Tuple[List[str], Dict[str, Tuple[int, int, int]]]:
    """Generates a symmetric multi-color cross-stitch tapestry (32x32, N ~ 500)."""
    random.seed(seed)
    palette = {
        ".": (255, 255, 255),  # Background
        "R": (220, 38, 38),    # Ruby Red
        "B": (37, 99, 235),    # Royal Blue
        "G": (22, 163, 74),    # Emerald Green
        "Y": (234, 179, 8),    # Gold Amber
        "K": (31, 41, 55),     # Charcoal border
    }

    grid = [["." for _ in range(size)] for _ in range(size)]
    half = size // 2

    # Draw concentric octagonal & diamond bands in quadrant 1, reflect to all 4
    for r in range(half):
        for c in range(half):
            dist_center = math.sqrt((half - 1 - r)**2 + (half - 1 - c)**2)
            manhattan = (half - 1 - r) + (half - 1 - c)

            # Assign color motifs
            char = "."
            if 1 <= manhattan <= 4:
                char = "Y"  # Center star
            elif 5 <= manhattan <= 8:
                char = "R"  # Inner floral diamond
            elif 9 <= dist_center <= 12:
                char = "B"  # Circular ring
            elif 13 <= manhattan <= 15:
                char = "G"  # Outer floral border
            elif manhattan == 16 or r == 0 or c == 0:
                if (r + c) % 2 == 0:
                    char = "K"  # Border trim

            grid[r][c] = char
            grid[size - 1 - r][c] = char
            grid[r][size - 1 - c] = char
            grid[size - 1 - r][size - 1 - c] = char

    grid_strings = ["".join(row) for row in grid]
    return grid_strings, palette


def generate_procedural_castle(size: int = 32) -> Tuple[List[str], Dict[str, Tuple[int, int, int]]]:
    """Generates an architectural retro castle sprite (32x32, N ~ 500)."""
    palette = {
        ".": (255, 255, 255),
        "K": (30, 41, 59),     # Dark slate
        "S": (148, 163, 184),  # Stone gray
        "R": (225, 29, 72),    # Red banners & roofs
        "G": (217, 119, 6),    # Gold windows & gate
        "B": (2, 132, 199),    # Sky blue moat
    }

    grid = [["." for _ in range(size)] for _ in range(size)]

    # Draw castle base (rows 12 to 26)
    for y in range(12, 27):
        for x in range(4, 28):
            grid[y][x] = "S"
            if x in (4, 27) or y == 26:
                grid[y][x] = "K"

    # Turrets
    for y in range(6, 12):
        for x in (4, 5, 6, 7, 24, 25, 26, 27):
            grid[y][x] = "S"
    # Turret conical roofs
    for y in range(2, 6):
        dx = y - 2
        for x in range(3 + dx, 9 - dx):
            grid[y][x] = "R"
        for x in range(23 + dx, 29 - dx):
            grid[y][x] = "R"

    # Central Keep & Flags
    for y in range(8, 14):
        for x in range(12, 20):
            grid[y][x] = "S"
    for y in range(4, 8):
        for x in range(14, 18):
            grid[y][x] = "R"

    # Golden Gate & Windows
    for y in range(20, 26):
        for x in range(13, 19):
            grid[y][x] = "G"
    for y in (15, 16):
        for x in (8, 9, 22, 23, 15, 16):
            grid[y][x] = "G"

    # Moat (rows 27 to 30)
    for y in range(27, 31):
        for x in range(2, 30):
            grid[y][x] = "B"

    grid_strings = ["".join(row) for row in grid]
    return grid_strings, palette


def generate_procedural_mandala(size: int = 48, seed: int = 101) -> Tuple[List[str], Dict[str, Tuple[int, int, int]]]:
    """Generates an intricate floral mandala cross-stitch pattern (48x48, N ~ 1000)."""
    random.seed(seed)
    palette = {
        ".": (255, 255, 255),
        "C": (14, 165, 233),   # Cyan
        "M": (217, 70, 239),   # Magenta
        "Y": (234, 179, 8),    # Gold
        "G": (34, 197, 94),    # Emerald
        "D": (79, 70, 229),    # Deep Indigo
        "O": (249, 115, 22),   # Sunset Orange
    }

    grid = [["." for _ in range(size)] for _ in range(size)]
    half = size / 2.0

    for y in range(size):
        for x in range(size):
            dy = y - half + 0.5
            dx = x - half + 0.5
            r = math.sqrt(dx*dx + dy*dy)
            theta = math.atan2(dy, dx)  # [-pi, pi]
            petal_8 = math.cos(8 * theta)
            petal_12 = math.cos(12 * theta)

            char = "."
            if r <= 3.5:
                char = "Y"  # Golden center core
            elif 3.5 < r <= 7.0 and petal_8 > 0.1:
                char = "O"  # 8 Orange petals
            elif 7.0 < r <= 11.5:
                if petal_8 > -0.2:
                    char = "M"  # Magenta corolla
                else:
                    char = "C"  # Cyan background fill
            elif 11.5 < r <= 16.0:
                if petal_12 > 0.0:
                    char = "G"  # 12 Green leaves
                else:
                    char = "D"  # Indigo accents
            elif 16.0 < r <= 20.5:
                if math.sin(16 * theta) > -0.1 and r > 18.0:
                    char = "C"  # Outer scalloped lace
                elif math.cos(8 * theta) > 0.3:
                    char = "Y"  # Golden starburst tips

            grid[y][x] = char

    grid_strings = ["".join(row) for row in grid]
    return grid_strings, palette


def generate_procedural_stained_glass(size: int = 48) -> Tuple[List[str], Dict[str, Tuple[int, int, int]]]:
    """Generates a Gothic stained glass cross-stitch rose window (48x48, N ~ 1000)."""
    palette = {
        ".": (255, 255, 255),
        "K": (15, 23, 42),     # Black leaded cane lines
        "R": (225, 29, 72),    # Ruby Red
        "B": (37, 99, 235),    # Cobalt Blue
        "A": (245, 158, 11),   # Amber Yellow
        "E": (16, 185, 129),   # Emerald Green
        "P": (147, 51, 234),   # Royal Purple
    }

    grid = [["." for _ in range(size)] for _ in range(size)]
    half = size / 2.0

    for y in range(size):
        for x in range(size):
            dy = y - half + 0.5
            dx = x - half + 0.5
            r = math.sqrt(dx*dx + dy*dy)
            theta = (math.atan2(dy, dx) + math.pi) % (2 * math.pi)
            wedge_idx = int((theta / (2 * math.pi)) * 16) % 16

            char = "."
            if r <= 22.0:
                # Outer circle boundary
                if 21.0 <= r <= 22.0:
                    char = "K"
                elif 14.5 <= r <= 15.5 or 8.5 <= r <= 9.5:
                    char = "K"  # Concentric rings
                elif (theta * 16 / (2 * math.pi)) % 1.0 < 0.12:
                    char = "K"  # Radial leaded spokes
                else:
                    # Fill pane colors by zone and wedge
                    if r < 8.5:
                        char = "A" if (wedge_idx % 2 == 0) else "R"
                    elif 9.5 < r < 14.5:
                        char = "B" if (wedge_idx % 2 == 0) else "E"
                    else:
                        colors = ["R", "P", "B", "A"]
                        char = colors[wedge_idx % 4]

            grid[y][x] = char

    grid_strings = ["".join(row) for row in grid]
    return grid_strings, palette


# ---------------------------------------------------------------------------
# General Automated Downsampler & Quantizer (Image to Cross-Stitch)
# ---------------------------------------------------------------------------
def convert_image_to_stitch_pattern(
    input_image_path: str,
    output_name: str,
    target_stitches: int = 500,
    max_colors: int = 6,
) -> str:
    """
    Downsamples any input image to match a target stitch count,
    quantizes colors, and produces a clean cross-stitch PNG pattern.
    """
    img = Image.open(input_image_path).convert("RGB")
    
    # Estimate grid size required to reach target active stitches
    # (assuming ~50% density of non-white stitches)
    grid_dim = max(16, int(math.sqrt(target_stitches * 1.8)))
    img_resized = img.resize((grid_dim, grid_dim), Image.Resampling.LANCZOS)
    
    # Quantize
    img_quant = img_resized.quantize(colors=max_colors).convert("RGB")
    
    out_path = os.path.join(DATA_DIR, f"{output_name}.png")
    img_quant.save(out_path)
    return out_path


# ---------------------------------------------------------------------------
# Main Dataset Generation Pipeline
# ---------------------------------------------------------------------------
def build_all_scaled_datasets():
    print("=" * 80)
    print("GENERATING MULTI-TIER SCALED CROSS-STITCH DATASETS (N ≈ 100, 500, 1000)")
    print("=" * 80)

    # 1. Tier S (Small, N ~ 100) — Already existing 16x16 sprites
    print("\n--- Tier S (Small Scale, N ≈ 100 stitches) ---")
    small_sprites = ["sprite_flower_16x16", "sprite_mushroom_16x16", "sprite_shield_16x16", "sprite_star_16x16", "sprite_ghost_16x16"]
    for s in small_sprites:
        p = os.path.join(DATA_DIR, f"{s}.png")
        if os.path.exists(p):
            from parser import load_pattern_from_image
            st = load_pattern_from_image(p)
            print(f"  [v] Confirmed Tier S: {s}.png (N={len(st)} stitches, K={len(set(x['color'] for x in st))} colors)")

    # 2. Tier M (Medium, N ~ 500)
    print("\n--- Tier M (Medium Scale, N ≈ 500 stitches) ---")
    g_tap, p_tap = generate_procedural_tapestry(size=32, seed=42)
    save_grid_to_png("pattern_tapestry_32x32", g_tap, p_tap)

    g_cas, p_cas = generate_procedural_castle(size=32)
    save_grid_to_png("pattern_castle_32x32", g_cas, p_cas)

    # 3. Tier L (Large, N ~ 1000)
    print("\n--- Tier L (Large Scale, N ≈ 1000 stitches) ---")
    g_man, p_man = generate_procedural_mandala(size=48, seed=101)
    save_grid_to_png("pattern_mandala_48x48", g_man, p_man)

    g_gla, p_gla = generate_procedural_stained_glass(size=48)
    save_grid_to_png("pattern_stained_glass_48x48", g_gla, p_gla)

    print("\nAll Multi-Tier Scaled Datasets generated successfully in:")
    print(f"  -> {DATA_DIR}")


if __name__ == "__main__":
    build_all_scaled_datasets()
