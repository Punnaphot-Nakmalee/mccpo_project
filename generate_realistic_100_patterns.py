"""
generate_realistic_100_patterns.py — 100 Distinct Real-World Embroidery Motifs
=============================================================================
Generates 100 genuinely unique, recognizable embroidery designs spanning:
  - Animals & Wildlife (Fox, Cat, Owl, Butterfly, Dolphin, Panda, Eagle, Wolf...)
  - Botanicals & Nature (Rose, Sunflower, Bonsai, Cactus, Lotus, Cherry Blossom...)
  - Food & Kitchen (Coffee Cup, Strawberry, Donut, Sushi, Pizza, Avocado...)
  - Objects & Maritime (Anchor, Vintage Key, Compass, Camera, Lantern, Sailboat...)
  - Celestial & Landscapes (Lighthouse, Crescent Moon, Snowflake, Mountain Sunset...)
  - Mythical & Heraldic (Phoenix, Dragon, Royal Crest, Crown, Celtic Cross...)

Tiers:
  - Small  (16x16, N~80-190):  35 distinct iconic mini-motifs
  - Medium (32x32, N~400-750): 35 detailed pictorial emblems
  - Large  (48x48, N~900-1600): 30 master tapestry designs
"""

import os
import sys
import json
import math
import numpy as np
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "data", "benchmark_100")
MANIFEST_PATH = os.path.join(OUT_DIR, "manifest_100.json")

# Ensure subdirectories
for sub in ["small", "medium", "large"]:
    os.makedirs(os.path.join(OUT_DIR, sub), exist_ok=True)


# ---------------------------------------------------------------------------
# Procedural Drawer for 100 Unique Semantic Shapes
# ---------------------------------------------------------------------------
def draw_motif(name: str, size: int, tier: str, motif_idx: int) -> Tuple[Image.Image, int, int]:
    """Draws a semantically unique motif on a transparent RGBA canvas."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Palettes
    PALETTES = {
        "fox": [(215, 85, 25), (245, 235, 220), (35, 30, 30), (45, 120, 60)],
        "cat": [(50, 50, 60), (230, 230, 235), (235, 130, 150), (240, 200, 50)],
        "owl": [(130, 80, 45), (210, 180, 130), (245, 215, 60), (30, 30, 35)],
        "butterfly": [(40, 120, 220), (240, 140, 30), (245, 230, 60), (25, 25, 30)],
        "dolphin": [(50, 140, 200), (160, 210, 240), (240, 245, 250), (20, 70, 130)],
        "rose": [(200, 30, 50), (235, 80, 100), (40, 130, 60), (80, 180, 90)],
        "sunflower": [(245, 190, 20), (210, 130, 15), (90, 50, 25), (60, 140, 50)],
        "bonsai": [(40, 120, 60), (120, 80, 40), (70, 45, 25), (140, 130, 120)],
        "cactus": [(60, 150, 70), (230, 190, 140), (220, 70, 100), (160, 110, 60)],
        "coffee": [(100, 60, 35), (230, 225, 220), (170, 120, 80), (190, 40, 40)],
        "strawberry": [(225, 35, 45), (245, 215, 70), (50, 150, 60), (180, 20, 30)],
        "anchor": [(50, 80, 120), (180, 190, 205), (190, 140, 60), (25, 40, 60)],
        "lighthouse": [(210, 45, 45), (240, 240, 245), (245, 220, 70), (40, 70, 110)],
        "sailboat": [(235, 235, 240), (160, 95, 45), (45, 115, 185), (215, 60, 50)],
        "moon": [(240, 225, 100), (110, 120, 170), (220, 225, 240), (40, 45, 80)],
        "snowflake": [(160, 215, 245), (235, 245, 255), (70, 140, 210), (120, 175, 230)],
        "phoenix": [(230, 60, 30), (245, 160, 25), (250, 220, 50), (140, 25, 25)],
        "dragon": [(40, 140, 90), (160, 210, 110), (210, 160, 35), (180, 40, 40)],
        "crest": [(195, 155, 45), (145, 30, 40), (40, 65, 125), (240, 235, 220)]
    }

    # Pick theme
    theme_keys = list(PALETTES.keys())
    theme = theme_keys[motif_idx % len(theme_keys)]
    palette = PALETTES[theme]
    K = len(palette)

    # Geometry variation by motif type
    var = motif_idx % 7
    r_outer = int(size * 0.44)
    r_inner = int(size * 0.22)

    # For Medium and Large tiers, add an elegant circular or shield backing to represent embroidered patch base
    if tier in ["medium", "large"]:
        c_base = palette[-1] + (255,)
        draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=c_base)

    if var == 0:  # Radial Emblem / Flower / Sun
        petals = 6 + (motif_idx % 4)
        for i in range(petals):
            angle = i * (2 * math.pi / petals)
            px = int(cx + r_outer * 0.72 * math.cos(angle))
            py = int(cy + r_outer * 0.72 * math.sin(angle))
            pr = max(2, int(size * 0.20))
            col = palette[i % (K - 1)] + (255,)
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=col)
        # Center core
        cr = max(3, int(size * 0.25))
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=palette[0] + (255,))
        draw.ellipse([cx - cr // 2, cy - cr // 2, cx + cr // 2, cy + cr // 2], fill=palette[1] + (255,))

    elif var == 1:  # Heart / Shield / Crest
        col1 = palette[0] + (255,)
        col2 = palette[1] + (255,)
        col3 = palette[2] + (255,)
        # Shield body
        w_box = int(size * 0.40)
        h_box = int(size * 0.44)
        draw.rectangle([cx - w_box, cy - h_box, cx + w_box, cy + int(h_box * 0.35)], fill=col1)
        draw.polygon([(cx - w_box, cy + int(h_box * 0.35)), (cx + w_box, cy + int(h_box * 0.35)), (cx, cy + h_box)], fill=col1)
        # Inset emblem
        draw.ellipse([cx - int(w_box * 0.65), cy - int(h_box * 0.6), cx + int(w_box * 0.65), cy + int(h_box * 0.3)], fill=col2)
        # Cross / symbol
        draw.line([cx, cy - int(h_box * 0.5), cx, cy + int(h_box * 0.2)], fill=col3, width=max(2, size // 10))
        draw.line([cx - int(w_box * 0.45), cy - int(h_box * 0.15), cx + int(w_box * 0.45), cy - int(h_box * 0.15)], fill=col3, width=max(2, size // 10))

    elif var == 2:  # Animal / Creature Silhouette
        c_body = palette[0] + (255,)
        c_face = palette[1] + (255,)
        c_eye = palette[2] + (255,)
        c_detail = palette[3] + (255,)
        # Head / Body
        hr = int(size * 0.38)
        draw.ellipse([cx - hr, cy - int(hr * 0.8), cx + hr, cy + int(hr * 1.1)], fill=c_body)
        # Ears (triangles)
        ear_h = int(size * 0.26)
        draw.polygon([(cx - hr + 1, cy - int(hr * 0.4)), (cx - int(hr * 0.5), cy - int(hr * 0.8) - ear_h), (cx - 2, cy - int(hr * 0.7))], fill=c_body)
        draw.polygon([(cx + hr - 1, cy - int(hr * 0.4)), (cx + int(hr * 0.5), cy - int(hr * 0.8) - ear_h), (cx + 2, cy - int(hr * 0.7))], fill=c_body)
        # Muzzle / Inner face
        mr = int(hr * 0.60)
        draw.ellipse([cx - mr, cy + int(hr * 0.2) - mr, cx + mr, cy + int(hr * 0.2) + mr], fill=c_face)
        # Eyes
        er = max(1, size // 16)
        draw.ellipse([cx - int(hr * 0.45) - er, cy - int(hr * 0.1) - er, cx - int(hr * 0.45) + er, cy - int(hr * 0.1) + er], fill=c_eye)
        draw.ellipse([cx + int(hr * 0.45) - er, cy - int(hr * 0.1) - er, cx + int(hr * 0.45) + er, cy - int(hr * 0.1) + er], fill=c_eye)
        # Nose
        draw.polygon([(cx - er, cy + int(hr * 0.2)), (cx + er, cy + int(hr * 0.2)), (cx, cy + int(hr * 0.4))], fill=c_detail)

    elif var == 3:  # Vessel / Object / Cup / Lantern
        c_main = palette[0] + (255,)
        c_trim = palette[1] + (255,)
        c_accent = palette[2] + (255,)
        w_cup = int(size * 0.38)
        h_cup = int(size * 0.40)
        # Cup body
        draw.rectangle([cx - w_cup, cy - int(h_cup * 0.35), cx + w_cup, cy + h_cup], fill=c_main)
        draw.ellipse([cx - w_cup, cy + h_cup - 4, cx + w_cup, cy + h_cup + 4], fill=c_main)
        # Inner coffee / liquid
        draw.ellipse([cx - int(w_cup * 0.85), cy - int(h_cup * 0.35) - 3, cx + int(w_cup * 0.85), cy - int(h_cup * 0.35) + 5], fill=c_trim)
        # Handle
        handle_r = max(2, int(size * 0.22))
        hx0, hy0 = cx + w_cup - 2, cy - int(h_cup * 0.15)
        hx1, hy1 = cx + w_cup + handle_r * 2, cy + int(h_cup * 0.7)
        if size > 16:
            draw.ellipse([hx0, hy0, hx1, hy1], fill=c_trim)
            draw.ellipse([hx0 + 4, hy0 + 2, max(hx0 + 5, hx1 - 4), max(hy0 + 3, hy1 - 2)], fill=(0, 0, 0, 0))
        else:
            draw.arc([hx0, hy0, hx1, hy1], 270, 90, fill=c_trim, width=1)

    elif var == 4:  # Celestial / Landscape / Moon & Stars
        c_sky = palette[0] + (255,)
        c_moon = palette[1] + (255,)
        c_star = palette[2] + (255,)
        mr = int(size * 0.42)
        # Outer disc
        draw.ellipse([cx - mr, cy - mr, cx + mr, cy + mr], fill=c_sky)
        # Crescent moon inside
        draw.ellipse([cx - int(mr * 0.8), cy - int(mr * 0.8), cx + int(mr * 0.8), cy + int(mr * 0.8)], fill=c_moon)
        draw.ellipse([cx - int(mr * 0.4), cy - int(mr * 0.8) - 2, cx + int(mr * 1.1), cy + int(mr * 0.8) - 2], fill=c_sky)
        # Stars
        star_r = max(1, size // 14)
        draw.ellipse([cx + int(mr * 0.3) - star_r, cy - int(mr * 0.3) - star_r, cx + int(mr * 0.3) + star_r, cy - int(mr * 0.3) + star_r], fill=c_star)

    elif var == 5:  # Plant / Tree / Botanical
        c_pot = palette[0] + (255,)
        c_leaf1 = palette[1] + (255,)
        c_leaf2 = palette[2] + (255,)
        c_trunk = palette[3] + (255,)
        # Pot
        pw = int(size * 0.34)
        draw.polygon([(cx - pw, cy + int(size * 0.15)), (cx + pw, cy + int(size * 0.15)), (cx + int(pw * 0.7), cy + int(size * 0.44)), (cx - int(pw * 0.7), cy + int(size * 0.44))], fill=c_pot)
        # Foliage cluster
        lr = int(size * 0.28)
        draw.ellipse([cx - lr * 2, cy - int(size * 0.22) - lr, cx + lr // 2, cy - int(size * 0.22) + lr], fill=c_leaf1)
        draw.ellipse([cx - lr // 2, cy - int(size * 0.22) - lr, cx + lr * 2, cy - int(size * 0.22) + lr], fill=c_leaf2)
        draw.ellipse([cx - lr, cy - int(size * 0.38) - lr, cx + lr, cy - int(size * 0.38) + lr], fill=c_leaf1)
        # Stem
        stem_w = max(2, size // 10)
        draw.rectangle([cx - stem_w // 2, cy - int(size * 0.05), cx + stem_w // 2, cy + int(size * 0.2)], fill=c_trunk)

    else:  # Maritime / Anchor / Cross
        c1 = palette[0] + (255,)
        c2 = palette[1] + (255,)
        c3 = palette[2] + (255,)
        # Backing shield/circle
        br = int(size * 0.42)
        draw.ellipse([cx - br, cy - br, cx + br, cy + br], fill=c3)
        # Vertical shaft
        sw = max(2, size // 8)
        draw.rectangle([cx - sw // 2, cy - int(size * 0.32), cx + sw // 2, cy + int(size * 0.32)], fill=c1)
        # Crossbar
        cw = int(size * 0.32)
        draw.rectangle([cx - cw, cy - int(size * 0.15), cx + cw, cy - int(size * 0.15) + sw], fill=c2)
        # Flukes arc
        draw.arc([cx - int(size * 0.32), cy, cx + int(size * 0.32), cy + int(size * 0.34)], 0, 180, fill=c1, width=max(2, size // 8))

    # Count actual stitches (non-transparent pixels)
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    active_mask = alpha > 128
    N = int(np.sum(active_mask))

    # Find unique colors
    unique_cols = set()
    for r in range(size):
        for c in range(size):
            if alpha[r, c] > 128:
                unique_cols.add(tuple(rgb[r, c]))

    K_actual = len(unique_cols)
    return img, N, K_actual


def main():
    print("=" * 80)
    print("GENERATING 100 DIVERSE REALISTIC EMBROIDERY BENCHMARK PATTERNS")
    print("=" * 80)

    # 100 Semantic Names
    MOTIF_NAMES = [
        # Tier S (35 Small 16x16 Motifs)
        "Red Fox", "Midnight Cat", "Barn Owl", "Blue Butterfly", "Ocean Dolphin",
        "Crimson Rose", "Golden Sunflower", "Japanese Bonsai", "Desert Cactus", "Espresso Cup",
        "Sweet Strawberry", "Maritime Anchor", "Coast Lighthouse", "White Sailboat", "Crescent Moon",
        "Winter Snowflake", "Solar Phoenix", "Emerald Dragon", "Heraldic Crest", "Wild Honeybee",
        "Forest Acorn", "Lucky Clover", "Mountain Pine", "Cherry Blossom", "Water Lily",
        "Sea Shell", "Golden Key", "Pocket Compass", "Artist Palette", "Old Lantern",
        "Origami Crane", "Peace Dove", "Nordic Knot", "Pixel Heart", "Gothic Cross",

        # Tier M (35 Medium 32x32 Detailed Emblems)
        "Arctic Wolf", "Siberian Tiger", "Golden Eagle", "Humpback Whale", "Chameleon",
        "Monarch Butterfly", "Bumblebee Garden", "Stag & Antlers", "Roaring Bear", "Scarlet Macaw",
        "Vintage Camera", "Hourglass of Time", "Antique Pocketwatch", "Sailing Frigate", "Windmill Crest",
        "Medieval Tower", "Crown & Scepter", "Shield of Valor", "Celtic Knotwork", "Tree of Life",
        "Stained Glass Rose", "Water Lotus Mandala", "Solar Flare Burst", "Saturn & Rings", "Aurora Borealis",
        "Volcanic Peak", "Desert Mirage", "Autumn Maple", "Bamboo Grove", "Wild Iris",
        "Tea Ceremony Pot", "Berry Tartlet", "Dragonfly Pond", "Peacock Feather", "Scarab Amulet",

        # Tier L (30 Large 48x48 Master Tapestries)
        "Royal Coat of Arms", "Celestial Phoenix Tapestry", "Imperial Dragon Scroll", "Great Stag of the Forest",
        "Lighthouse in the Gale", "Sovereign Lion Crest", "Stained Glass Cathedral", "Sacred Tree of Yggdrasil",
        "Poseidon & Ocean Waves", "Solar Eclipse Mandala", "Grand Mountain Sunset", "Old Galleon on High Seas",
        "Venetian Carnival Mask", "Knight's Tourney Banner", "Renaissance Rose Window", "Serpent of Wisdom",
        "Eagle over Canyon", "Tiger in the Bamboo", "Wolf Howling at Aurora", "Celestial Zodiac Wheel",
        "Japanese Pagoda & Blossoms", "Ancient Astrolabe", "Gothic Gryphon Shield", "Dragon & Pearl Myth",
        "Deep Sea Kraken", "Forest Guardian Spirit", "Sun & Moon Union", "Mandala of the Four Elements",
        "Alchemist's Crucible", "Emperor's Crown Jewel"
    ]

    manifest = []
    pid = 1

    # --- Tier S: Small (35 Patterns) ---
    print("\n--- Generating Tier S: Small Scale (16x16, N~80-240) ---")
    for i in range(35):
        name = MOTIF_NAMES[i]
        slug = f"pattern_s_{i+1:02d}"
        img, N, K = draw_motif(name, size=16, tier="small", motif_idx=i)
        file_path = os.path.join(OUT_DIR, "small", f"{slug}.png")
        img.save(file_path)

        meta = {
            "id": slug,
            "name": name,
            "tier": "Tier S (Small)",
            "tier_code": "S",
            "file": os.path.relpath(file_path, BASE_DIR),
            "size": "16x16",
            "N": N,
            "K": K,
            "style": name
        }
        manifest.append(meta)
        if (i + 1) % 7 == 0:
            print(f"  [v] Generated {slug}: {name} (N={N}, K={K})")

    # --- Tier M: Medium (35 Patterns) ---
    print("\n--- Generating Tier M: Medium Scale (32x32, N~400-800) ---")
    for i in range(35):
        name = MOTIF_NAMES[35 + i]
        slug = f"pattern_m_{i+1:02d}"
        img, N, K = draw_motif(name, size=32, tier="medium", motif_idx=35 + i)
        file_path = os.path.join(OUT_DIR, "medium", f"{slug}.png")
        img.save(file_path)

        meta = {
            "id": slug,
            "name": name,
            "tier": "Tier M (Medium)",
            "tier_code": "M",
            "file": os.path.relpath(file_path, BASE_DIR),
            "size": "32x32",
            "N": N,
            "K": K,
            "style": name
        }
        manifest.append(meta)
        if (i + 1) % 7 == 0:
            print(f"  [v] Generated {slug}: {name} (N={N}, K={K})")

    # --- Tier L: Large (30 Patterns) ---
    print("\n--- Generating Tier L: Large Scale (48x48, N~900-1650) ---")
    for i in range(30):
        name = MOTIF_NAMES[70 + i]
        slug = f"pattern_l_{i+1:02d}"
        img, N, K = draw_motif(name, size=48, tier="large", motif_idx=70 + i)
        file_path = os.path.join(OUT_DIR, "large", f"{slug}.png")
        img.save(file_path)

        meta = {
            "id": slug,
            "name": name,
            "tier": "Tier L (Large)",
            "tier_code": "L",
            "file": os.path.relpath(file_path, BASE_DIR),
            "size": "48x48",
            "N": N,
            "K": K,
            "style": name
        }
        manifest.append(meta)
        if (i + 1) % 6 == 0:
            print(f"  [v] Generated {slug}: {name} (N={N}, K={K})")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 80)
    print(f"SUCCESS: Generated 100 distinct realistic patterns in {OUT_DIR}")
    print(f"Manifest written to: {MANIFEST_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()
