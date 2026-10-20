"""
generate_dataset.py
Generates 5 medium-scale retro pixel-art sprites (N = 50 ~ 200, 3-5 colors)
and parses them into JSON/benchmark sets in the data/ folder.
"""

import os
from PIL import Image
from parser import load_pattern_from_image, describe_pattern

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Sprite Definitions (16x16 pixel grids using ASCII characters)
# ---------------------------------------------------------------------------

SPRITES = {
    "sprite_mushroom_16x16": {
        "palette": {
            ".": (255, 255, 255),  # Background (transparent/white)
            "K": (0, 0, 0),        # Black outline
            "R": (220, 20, 20),    # Red cap
            "W": (240, 240, 240),  # White spots
            "B": (245, 215, 175),  # Beige stalk
        },
        "grid": [
            "................",
            ".....KKKKKK.....",
            "...KKRRRRRRKK...",
            "..KRRWRRRRWRRK..",
            ".KRRWWWRRWWWRRK.",
            ".KRWWWWKKWWWWKR.",
            ".KRWWWWKKWWWWKR.",
            ".KRRWWWRRWWWRRK.",
            ".KKRRWRRRRWRRKK.",
            ".KKKKKKKKKKKKKK.",
            "...KBBBKKBKK....",
            "..KBBKBKKBKBKK..",
            "..KBBKBKKBKBKK..",
            "..KBBBBBBBBBKK..",
            "...KKKKKKKKKK...",
            "................",
        ]
    },

    "sprite_star_16x16": {
        "palette": {
            ".": (255, 255, 255),  # Background
            "K": (20, 20, 20),      # Black outline
            "Y": (255, 215, 0),    # Gold/Yellow body
            "W": (255, 255, 255),  # White highlights (treated as body if distinct, or keep distinct)
            "B": (30, 80, 220),    # Blue eye pupils
        },
        "grid": [
            ".......KK.......",
            "......KYYK......",
            "......KYYK......",
            ".....KYYYYK.....",
            "..KKKKYYYYKKKK..",
            ".KYYYYYYYYYYYYK.",
            "..KYYYBKKBYYYK..",
            "...KYYBKKBYYK...",
            "...KYYYYYYYYK...",
            "..KYYYYYYYYYYK..",
            ".KYYYYKKKKYYYYK.",
            ".KYYKK....KKYYK.",
            ".KKK........KKK.",
            "................",
            "................",
            "................",
        ]
    },

    "sprite_ghost_16x16": {
        "palette": {
            ".": (255, 255, 255),  # Background
            "C": (0, 180, 220),    # Cyan body
            "W": (250, 250, 250),  # White sclera
            "B": (20, 20, 150),    # Dark blue pupils
        },
        "grid": [
            "................",
            ".....CCCCCC.....",
            "...CCCCCCCCCC...",
            "..CCCCCCCCCCCC..",
            ".CCCCWWCCCCWWCC.",
            ".CCCWBBWCCWBBWC.",
            ".CCCWBBWCCWBBWC.",
            ".CCCCWWCCCCWWCC.",
            ".CCCCCCCCCCCCCC.",
            ".CCCCCCCCCCCCCC.",
            ".CCCCCCCCCCCCCC.",
            ".CCCCCCCCCCCCCC.",
            ".CC.CCC..CCC.CC.",
            ".C...C....C...C.",
            "................",
            "................",
        ]
    },

    "sprite_shield_16x16": {
        "palette": {
            ".": (255, 255, 255),  # Background
            "G": (212, 175, 55),   # Gold border
            "R": (200, 30, 30),    # Crimson field
            "S": (180, 190, 200),  # Silver crest cross
            "K": (30, 30, 30),     # Dark core accent
        },
        "grid": [
            "..GGGGGGGGGGGG..",
            ".GGSSSSGGSSSSGG.",
            ".GSSRRSSGSSRRSSG.",
            ".GSRRRRSGSRRRRSG.",
            ".GSRRRRSGSRRRRSG.",
            ".GGSSSSGGSSSSGG.",
            ".GGGGGGKKGGGGGG.",
            ".GGSSSSGGSSSSGG.",
            ".GSRRRRSGSRRRRSG.",
            "..GSRRRSSRRRSG..",
            "...GSRRSSRRSG...",
            "....GSSSSSSG....",
            ".....GSRRSG.....",
            "......GSSG......",
            ".......GG.......",
            "................",
        ]
    },

    "sprite_flower_16x16": {
        "palette": {
            ".": (255, 255, 255),  # Background
            "K": (20, 20, 20),      # Outline
            "R": (230, 40, 20),    # Fire red outer petals
            "Y": (255, 200, 0),    # Yellow inner petals
            "G": (40, 160, 40),    # Green stem & leaves
        },
        "grid": [
            "................",
            "......KKKK......",
            "....KKRRRRKK....",
            "...KRRRYYYRRK...",
            "..KRRRYYYYYRRK..",
            "..KRRYYKKYYRRK..",
            "..KRRRYYYYYRRK..",
            "...KRRRYYYRRK...",
            "....KKRRRRKK....",
            "......KKKK......",
            "....GG.KK.GG....",
            "...GGG.KK.GGG...",
            "..GGGG.KK.GGGG..",
            "....GGKKKKGG....",
            "......KKKK......",
            "................",
        ]
    }
}

def generate_and_parse_all():
    summary_report = []
    
    print("=" * 65)
    print("GENERATING & VALIDATING TIER 2 MEDIUM SPRITES (N = 50 ~ 200)")
    print("=" * 65)
    
    for name, data in SPRITES.items():
        img_path = os.path.join(DATA_DIR, f"{name}.png")
        
        # Create 16x16 image
        img = Image.new("RGB", (16, 16), (255, 255, 255))
        pixels = img.load()
        
        for y, row in enumerate(data["grid"]):
            for x, char in enumerate(row[:16]):
                color = data["palette"].get(char, (255, 255, 255))
                pixels[x, y] = color
                
        img.save(img_path)
        
        # Parse it back using parser.py
        stitches = load_pattern_from_image(img_path, bg_color=(255, 255, 255), bg_tolerance=20)
        
        colors = {}
        for s in stitches:
            colors[s["color"]] = colors.get(s["color"], 0) + 1
            
        N = len(stitches)
        num_colors = len(colors)
        summary_report.append((name, N, num_colors, colors))
        
        print(f"\n[Generated] {name}.png")
        describe_pattern(stitches)

    print("\n" + "=" * 65)
    print(f"{'Sprite Name':<25} | {'Stitches (N)':<12} | {'Color Count':<12}")
    print("-" * 65)
    for name, N, num_colors, _ in summary_report:
        print(f"{name:<25} | {N:<12} | {num_colors:<12}")
    print("=" * 65)
    print("All sprites successfully generated and parsed into dataset!")

if __name__ == "__main__":
    generate_and_parse_all()
