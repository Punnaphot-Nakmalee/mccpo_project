"""
generate_100_distinct_motifs.py — 100 Genuinely Individual Embroidery Motifs
=============================================================================
Defines 100 dedicated, non-repeating procedural drawing routines.
Every single pattern (all 35 Small, all 35 Medium, and all 30 Large) has its
own unique silhouette, distinct semantic anatomy, and custom palette.
Zero generic modulo loops.
"""

import os
import sys
import json
import math
import numpy as np
from PIL import Image, ImageDraw
from typing import Tuple, Dict, Any, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "data", "benchmark_100")
MANIFEST_PATH = os.path.join(OUT_DIR, "manifest_100.json")

for sub in ["small", "medium", "large"]:
    os.makedirs(os.path.join(OUT_DIR, sub), exist_ok=True)


def _canvas(size: int) -> Tuple[Image.Image, ImageDraw.Draw]:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _count(img: Image.Image) -> Tuple[int, int]:
    arr = np.array(img)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    active = alpha > 128
    N = int(np.sum(active))
    unique_cols = set()
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            if alpha[r, c] > 128:
                unique_cols.add(tuple(rgb[r, c]))
    return N, len(unique_cols)


# ===========================================================================
# 35 INDIVIDUAL TIER S DRAWERS (16x16)
# ===========================================================================
def s01():  # Pixel Heart
    im, d = _canvas(16)
    d.polygon([(8,14), (1,7), (1,3), (4,1), (7,3), (8,5), (9,3), (12,1), (15,3), (15,7)], fill=(220,30,50,255))
    d.point([(4,3), (5,3), (4,4)], fill=(255,160,180,255))
    return im

def s02():  # Golden Star
    im, d = _canvas(16)
    d.polygon([(8,1), (10,6), (15,6), (11,10), (13,15), (8,12), (3,15), (5,10), (1,6), (6,6)], fill=(245,200,30,255))
    d.polygon([(8,4), (8,12), (10,6), (11,10)], fill=(210,140,15,255))
    return im

def s03():  # Vintage Key
    im, d = _canvas(16)
    d.ellipse([4,2, 11,8], outline=(200,160,50,255), width=2)
    d.line([(8,8), (8,14)], fill=(200,160,50,255), width=2)
    d.line([(8,12), (11,12)], fill=(200,160,50,255), width=1)
    d.line([(8,14), (11,14)], fill=(130,90,25,255), width=1)
    return im

def s04():  # Music Note
    im, d = _canvas(16)
    d.ellipse([2,9, 7,14], fill=(40,40,50,255))
    d.ellipse([9,7, 14,12], fill=(40,40,50,255))
    d.line([(6,11), (6,3)], fill=(90,120,220,255), width=1)
    d.line([(13,9), (13,2)], fill=(90,120,220,255), width=1)
    d.line([(6,3), (13,2)], fill=(90,120,220,255), width=2)
    return im

def s05():  # Red Apple
    im, d = _canvas(16)
    d.ellipse([3,4, 12,14], fill=(215,35,40,255))
    d.line([(8,4), (9,1)], fill=(110,60,30,255), width=1)
    d.polygon([(9,2), (13,2), (11,4)], fill=(50,160,60,255))
    return im

def s06():  # Coffee Mug
    im, d = _canvas(16)
    d.rectangle([3,6, 10,13], fill=(225,220,215,255))
    d.ellipse([3,5, 10,7], fill=(110,65,35,255))
    d.arc([8,7, 13,12], 270, 90, fill=(225,220,215,255), width=2)
    d.line([(5,2), (5,4)], fill=(160,190,220,255), width=1)
    return im

def s07():  # Magic Potion
    im, d = _canvas(16)
    d.rectangle([7,2, 9,4], fill=(140,95,45,255))
    d.ellipse([3,5, 13,14], fill=(200,225,245,255))
    d.ellipse([4,7, 12,13], fill=(180,40,200,255))
    return im

def s08():  # Knight Sword
    im, d = _canvas(16)
    d.line([(13,2), (5,10)], fill=(210,220,230,255), width=2)
    d.line([(3,9), (7,13)], fill=(190,150,40,255), width=2)
    d.line([(4,11), (2,13)], fill=(140,90,30,255), width=1)
    return im

def s09():  # Wooden Shield
    im, d = _canvas(16)
    d.polygon([(3,3), (12,3), (12,9), (8,14), (3,9)], fill=(140,80,40,255))
    d.rectangle([7,3, 8,13], fill=(120,130,140,255))
    d.ellipse([6,6, 9,9], fill=(210,170,40,255))
    return im

def s10():  # Skull
    im, d = _canvas(16)
    d.ellipse([4,2, 12,10], fill=(235,235,230,255))
    d.rectangle([6,10, 10,13], fill=(235,235,230,255))
    d.point([(5,6), (6,6), (10,6), (11,6), (8,8)], fill=(30,30,35,255))
    return im

def s11():  # Lucky Clover
    im, d = _canvas(16)
    for px, py in [(8,4), (4,8), (12,8), (8,11)]:
        d.ellipse([px-2, py-2, px+2, py+2], fill=(40,150,60,255))
    d.arc([8,10, 11,15], 90, 270, fill=(80,200,90,255), width=1)
    return im

def s12():  # Rain Cloud
    im, d = _canvas(16)
    d.ellipse([3,4, 8,8], fill=(170,185,205,255))
    d.ellipse([7,2, 13,8], fill=(170,185,205,255))
    d.rectangle([4,6, 12,9], fill=(170,185,205,255))
    d.polygon([(7,10), (9,10), (7,12), (10,12), (6,15), (8,12), (6,12)], fill=(245,215,30,255))
    return im

def s13():  # Crescent Moon
    im, d = _canvas(16)
    d.ellipse([2,2, 13,13], fill=(245,220,80,255))
    d.ellipse([5,1, 15,13], fill=(0,0,0,0))
    d.point([(12,3), (11,8)], fill=(210,230,255,255))
    return im

def s14():  # Flying Bird
    im, d = _canvas(16)
    d.polygon([(2,7), (7,4), (13,2), (9,8), (14,10), (8,10), (4,12)], fill=(50,130,210,255))
    d.ellipse([6,6, 9,9], fill=(240,245,255,255))
    return im

def s15():  # Cat Face with Whiskers & Collar
    im, d = _canvas(16)
    d.ellipse([3,5, 13,13], fill=(70,70,80,255))
    d.polygon([(3,6), (5,1), (7,6)], fill=(70,70,80,255))
    d.polygon([(9,6), (11,1), (13,6)], fill=(70,70,80,255))
    d.polygon([(4,5), (5,2), (6,5)], fill=(240,160,180,255))
    d.polygon([(10,5), (11,2), (12,5)], fill=(240,160,180,255))
    d.point([(5,8), (11,8)], fill=(100,220,120,255))
    d.point([(8,10)], fill=(240,140,160,255))
    d.line([(1,9), (4,9)], fill=(230,230,240,255), width=1)
    d.line([(12,9), (15,9)], fill=(230,230,240,255), width=1)
    d.line([(5,14), (11,14)], fill=(220,30,40,255), width=1)
    return im

def s16():  # Goldfish
    im, d = _canvas(16)
    d.ellipse([4,5, 12,11], fill=(240,110,30,255))
    d.polygon([(11,8), (15,4), (14,8), (15,12)], fill=(245,180,60,255))
    d.point([(5,7)], fill=(20,20,30,255))
    return im

def s17():  # Mushroom
    im, d = _canvas(16)
    d.ellipse([2,3, 13,10], fill=(210,35,35,255))
    d.rectangle([6,9, 10,14], fill=(235,230,220,255))
    d.point([(5,5), (9,5), (7,7)], fill=(235,230,220,255))
    return im

def s18():  # Daisy Flower
    im, d = _canvas(16)
    d.line([(8,8), (8,15)], fill=(50,150,60,255), width=2)
    for px, py in [(8,4), (4,8), (12,8), (8,12), (5,5), (11,5), (5,11), (11,11)]:
        d.point([(px, py)], fill=(245,245,250,255))
    d.ellipse([6,6, 10,10], fill=(245,195,30,255))
    return im

def s19():  # Pine Tree
    im, d = _canvas(16)
    d.polygon([(8,1), (4,6), (12,6)], fill=(30,110,50,255))
    d.polygon([(8,4), (3,9), (13,9)], fill=(30,110,50,255))
    d.polygon([(8,7), (2,13), (14,13)], fill=(30,110,50,255))
    d.rectangle([7,13, 9,15], fill=(110,65,30,255))
    return im

def s20():  # Cherry Pair
    im, d = _canvas(16)
    d.ellipse([2,8, 7,13], fill=(195,20,40,255))
    d.ellipse([8,9, 13,14], fill=(195,20,40,255))
    d.line([(5,8), (8,2)], fill=(70,130,50,255), width=1)
    d.line([(10,9), (8,2)], fill=(70,130,50,255), width=1)
    return im

def s21():  # Campfire
    im, d = _canvas(16)
    d.line([(3,13), (13,13)], fill=(120,70,30,255), width=2)
    d.polygon([(8,3), (12,11), (4,11)], fill=(240,90,20,255))
    d.polygon([(8,6), (10,11), (6,11)], fill=(250,220,40,255))
    return im

def s22():  # Diamond Gem
    im, d = _canvas(16)
    d.polygon([(5,3), (11,3), (14,6), (8,14), (2,6)], fill=(60,210,230,255))
    d.polygon([(5,3), (8,3), (8,6), (5,6)], fill=(190,245,255,255))
    d.polygon([(8,6), (14,6), (8,14)], fill=(20,130,170,255))
    return im

def s23():  # Sailboat
    im, d = _canvas(16)
    d.polygon([(2,11), (14,11), (12,14), (4,14)], fill=(140,85,45,255))
    d.polygon([(8,2), (8,10), (13,10)], fill=(240,240,245,255))
    d.polygon([(7,4), (7,10), (3,10)], fill=(240,240,245,255))
    return im

def s24():  # Anchor
    im, d = _canvas(16)
    d.line([(8,3), (8,13)], fill=(70,100,130,255), width=2)
    d.ellipse([6,1, 10,5], outline=(210,160,40,255), width=1)
    d.arc([3,7, 13,14], 0, 180, fill=(70,100,130,255), width=2)
    return im

def s25():  # Compass
    im, d = _canvas(16)
    d.ellipse([2,2, 13,13], fill=(235,230,220,255), outline=(190,145,40,255), width=1)
    d.polygon([(8,4), (9,8), (7,8)], fill=(210,30,30,255))
    d.polygon([(8,12), (9,8), (7,8)], fill=(40,70,140,255))
    return im

def s26():  # Wine Glass
    im, d = _canvas(16)
    d.polygon([(4,2), (12,2), (11,8), (5,8)], fill=(160,20,50,255))
    d.line([(8,8), (8,13)], fill=(200,220,240,255), width=1)
    d.line([(5,14), (11,14)], fill=(200,220,240,255), width=1)
    return im

def s27():  # Cupcake
    im, d = _canvas(16)
    d.polygon([(4,9), (12,9), (10,14), (6,14)], fill=(210,150,90,255))
    d.ellipse([3,5, 13,10], fill=(245,160,190,255))
    d.ellipse([7,3, 9,5], fill=(215,25,40,255))
    return im

def s28():  # Pizza Slice
    im, d = _canvas(16)
    d.polygon([(2,3), (14,3), (8,14)], fill=(245,205,40,255))
    d.line([(2,3), (14,3)], fill=(205,140,60,255), width=2)
    d.point([(6,6), (10,7), (7,9)], fill=(190,35,30,255))
    return im

def s29():  # Tennis Racket with Crossed Strings
    im, d = _canvas(16)
    d.ellipse([3,1, 13,9], outline=(220,50,50,255), width=1)
    d.line([(5,5), (11,5)], fill=(210,230,245,255), width=1)
    d.line([(8,2), (8,8)], fill=(210,230,245,255), width=1)
    d.line([(8,9), (8,15)], fill=(130,75,30,255), width=2)
    d.rectangle([7,12, 9,15], fill=(235,235,240,255))
    return im

def s30():  # Paper Airplane
    im, d = _canvas(16)
    d.polygon([(1,8), (14,2), (8,14)], fill=(240,245,250,255))
    d.polygon([(1,8), (8,8), (8,14)], fill=(170,185,205,255))
    return im

def s31():  # Ghost
    im, d = _canvas(16)
    d.ellipse([3,2, 12,11], fill=(240,245,255,255))
    d.polygon([(3,9), (12,9), (12,14), (10,12), (8,14), (6,12), (3,14)], fill=(240,245,255,255))
    d.point([(5,6), (6,6), (9,6), (10,6)], fill=(30,40,70,255))
    return im

def s32():  # Helm Wheel
    im, d = _canvas(16)
    d.ellipse([3,3, 12,12], outline=(150,95,45,255), width=2)
    d.line([(8,1), (8,14)], fill=(150,95,45,255), width=1)
    d.line([(1,8), (14,8)], fill=(150,95,45,255), width=1)
    d.ellipse([6,6, 9,9], fill=(215,175,45,255))
    return im

def s33():  # Hourglass
    im, d = _canvas(16)
    d.rectangle([3,2, 12,3], fill=(140,85,40,255))
    d.rectangle([3,12, 12,13], fill=(140,85,40,255))
    d.polygon([(4,4), (11,4), (8,8)], fill=(235,195,60,255))
    d.polygon([(8,8), (11,12), (4,12)], fill=(235,195,60,255))
    return im

def s34():  # Gamepad
    im, d = _canvas(16)
    d.rectangle([2,5, 13,11], fill=(60,65,80,255))
    d.line([(4,7), (4,9)], fill=(30,30,35,255), width=1)
    d.line([(3,8), (5,8)], fill=(30,30,35,255), width=1)
    d.point([(10,8), (12,8)], fill=(225,40,60,255))
    return im

def s35():  # Gothic Cross
    im, d = _canvas(16)
    d.rectangle([7,2, 9,14], fill=(215,170,35,255))
    d.rectangle([3,5, 13,7], fill=(215,170,35,255))
    d.ellipse([6,4, 10,8], fill=(180,25,35,255))
    return im


# ===========================================================================
# 35 INDIVIDUAL TIER M DRAWERS (32x32)
# ===========================================================================
def m01():  # Blue Butterfly
    im, d = _canvas(32)
    # Background garden disc
    d.ellipse([3,3, 28,28], fill=(235,245,235,255))
    # Butterfly wings
    d.ellipse([6,6, 16,18], fill=(45,120,225,255))
    d.ellipse([16,6, 26,18], fill=(45,120,225,255))
    d.ellipse([8,14, 16,25], fill=(60,160,240,255))
    d.ellipse([16,14, 24,25], fill=(60,160,240,255))
    # Body & spots
    d.rectangle([15,8, 17,23], fill=(30,30,40,255))
    d.point([(10,11), (22,11), (11,19), (21,19)], fill=(245,210,40,255))
    return im

def m02():  # Barn Owl
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,235,225,255))
    # Owl body & head
    d.ellipse([8,8, 24,26], fill=(135,85,45,255))
    d.ellipse([10,12, 22,23], fill=(220,195,150,255))
    # Heart face mask & big eyes
    d.ellipse([10,8, 16,14], fill=(245,240,235,255))
    d.ellipse([16,8, 22,14], fill=(245,240,235,255))
    d.ellipse([11,9, 15,13], fill=(245,210,40,255))
    d.ellipse([17,9, 21,13], fill=(245,210,40,255))
    d.point([(13,11), (19,11)], fill=(25,25,30,255))
    return im

def m03():  # Red Fox Profile
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(230,240,245,255))
    # Fox head & ears
    d.polygon([(6,16), (20,8), (26,16), (20,24)], fill=(220,85,30,255))
    d.polygon([(16,8), (18,2), (21,8)], fill=(220,85,30,255))
    d.polygon([(11,11), (13,4), (16,10)], fill=(220,85,30,255))
    # White muzzle & chest
    d.polygon([(6,16), (14,16), (18,24), (10,24)], fill=(245,235,220,255))
    d.point([(7,16)], fill=(25,25,30,255))
    d.point([(16,13)], fill=(25,25,30,255))
    return im

def m04():  # Sea Turtle
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(220,240,250,255))
    # Shell carapace
    d.ellipse([9,9, 23,23], fill=(45,130,110,255))
    d.ellipse([12,12, 20,20], fill=(160,210,180,255))
    # Flippers & head
    d.ellipse([13,4, 19,10], fill=(45,130,110,255))
    d.polygon([(5,8), (11,12), (8,16)], fill=(45,130,110,255))
    d.polygon([(27,8), (21,12), (24,16)], fill=(45,130,110,255))
    return im

def m05():  # Chameleon
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,235,220,255))
    # Curved body & spiral tail
    d.ellipse([8,10, 22,22], fill=(65,175,75,255))
    d.arc([16,14, 26,24], 0, 270, fill=(65,175,75,255), width=3)
    # Head & eye turret
    d.ellipse([6,10, 14,17], fill=(85,200,95,255))
    d.ellipse([8,11, 12,15], fill=(230,180,40,255))
    d.point([(10,13)], fill=(20,30,20,255))
    return im

def m06():  # Bonsai Tree
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,240,240,255))
    # Pot
    d.polygon([(8,23), (24,23), (21,27), (11,27)], fill=(140,80,40,255))
    # Twisted trunk
    d.line([(16,23), (16,16), (12,12), (18,10)], fill=(80,50,25,255), width=3)
    # Foliage pads
    d.ellipse([6,9, 14,15], fill=(40,120,60,255))
    d.ellipse([14,6, 23,12], fill=(40,120,60,255))
    d.ellipse([18,11, 26,16], fill=(50,145,70,255))
    return im

def m07():  # Crimson Rose
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(235,245,235,255))
    # Stem & leaves
    d.line([(16,18), (16,28)], fill=(40,120,50,255), width=2)
    d.polygon([(16,22), (23,19), (18,24)], fill=(50,150,65,255))
    # Rose petals
    d.ellipse([9,7, 23,20], fill=(200,30,50,255))
    d.ellipse([11,9, 21,18], fill=(235,70,90,255))
    d.ellipse([13,11, 19,16], fill=(255,140,160,255))
    return im

def m08():  # Layered Desert Saguaro & Sun
    im, d = _canvas(32)
    # Terracotta patch disc
    d.ellipse([3,3, 28,28], fill=(235,215,185,255))
    # Golden Sun
    d.ellipse([20,6, 26,12], fill=(245,180,30,255))
    # Sand dunes
    d.polygon([(3,22), (16,18), (28,22), (28,28), (3,28)], fill=(210,150,90,255))
    # Saguaro Cactus Body & Arms
    d.rectangle([13,10, 18,26], fill=(45,130,60,255))
    d.line([(13,16), (9,16), (9,11)], fill=(45,130,60,255), width=2)
    d.line([(18,18), (22,18), (22,13)], fill=(45,130,60,255), width=2)
    # Cactus flowers
    d.ellipse([8,9, 11,12], fill=(235,60,110,255))
    d.ellipse([21,11, 24,14], fill=(235,60,110,255))
    d.ellipse([14,8, 17,11], fill=(235,60,110,255))
    return im

def m09():  # Coastal Lighthouse
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(220,230,245,255))
    # Tower
    d.polygon([(12,26), (20,26), (18,8), (14,8)], fill=(245,245,250,255))
    d.rectangle([13,13, 19,17], fill=(215,45,45,255))
    d.rectangle([14,21, 18,25], fill=(215,45,45,255))
    # Lantern room & beam
    d.rectangle([14,5, 18,8], fill=(245,215,40,255))
    d.polygon([(18,6), (28,2), (28,11)], fill=(255,240,150,255))
    return im

def m10():  # Old Windmill
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(235,240,245,255))
    # Tower
    d.polygon([(11,26), (21,26), (19,12), (13,12)], fill=(160,95,45,255))
    d.rectangle([14,21, 18,26], fill=(80,45,20,255))
    # 4 Blades
    d.line([(6,6), (26,26)], fill=(230,230,235,255), width=2)
    d.line([(6,26), (26,6)], fill=(230,230,235,255), width=2)
    d.ellipse([14,14, 18,18], fill=(200,40,40,255))
    return im

def m11():  # Vintage Camera
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,235,225,255))
    # Camera body
    d.rectangle([6,11, 26,24], fill=(45,50,60,255))
    d.rectangle([6,11, 26,14], fill=(180,185,195,255))
    # Big lens
    d.ellipse([11,13, 21,23], fill=(180,185,195,255))
    d.ellipse([13,15, 19,21], fill=(25,120,180,255))
    d.point([(10,12)], fill=(220,50,50,255))
    return im

def m12():  # Acoustic Guitar
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,240,230,255))
    # Guitar body (figure 8)
    d.ellipse([9,15, 23,27], fill=(210,140,55,255))
    d.ellipse([11,10, 21,17], fill=(210,140,55,255))
    # Sound hole & neck
    d.ellipse([14,14, 18,18], fill=(50,30,15,255))
    d.line([(16,11), (16,3)], fill=(120,70,30,255), width=2)
    return im

def m13():  # Hot Air Balloon
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(225,240,250,255))
    # Balloon envelope
    d.ellipse([8,4, 24,20], fill=(235,60,60,255))
    d.ellipse([11,4, 21,20], fill=(245,210,40,255))
    d.ellipse([14,4, 18,20], fill=(40,130,210,255))
    # Basket
    d.rectangle([13,24, 19,27], fill=(140,85,40,255))
    d.line([(11,19), (14,24)], fill=(80,80,80,255), width=1)
    d.line([(21,19), (18,24)], fill=(80,80,80,255), width=1)
    return im

def m14():  # Steam Locomotive
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(235,235,240,255))
    # Cab & Boiler
    d.rectangle([6,12, 13,22], fill=(40,70,130,255))
    d.rectangle([13,15, 24,22], fill=(45,50,60,255))
    # Smokestack & wheels
    d.rectangle([20,10, 23,15], fill=(30,30,35,255))
    d.ellipse([8,22, 13,27], fill=(210,160,40,255))
    d.ellipse([14,22, 19,27], fill=(210,160,40,255))
    d.ellipse([19,22, 24,27], fill=(210,160,40,255))
    return im

def m15():  # Retro Beetle Car
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,245,235,255))
    # Curved roof & body
    d.ellipse([7,11, 25,23], fill=(220,50,50,255))
    d.rectangle([6,17, 26,22], fill=(220,50,50,255))
    d.ellipse([11,12, 21,17], fill=(200,225,245,255))
    # Wheels
    d.ellipse([8,20, 13,25], fill=(35,35,40,255))
    d.ellipse([19,20, 24,25], fill=(35,35,40,255))
    return im

def m16():  # Pocketwatch
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,240,230,255))
    d.ellipse([6,7, 26,27], fill=(215,170,40,255))
    d.ellipse([8,9, 24,25], fill=(245,245,240,255))
    # Hands & top loop
    d.line([(16,17), (16,12)], fill=(30,30,40,255), width=1)
    d.line([(16,17), (20,17)], fill=(30,30,40,255), width=1)
    d.ellipse([14,3, 18,7], outline=(215,170,40,255), width=1)
    return im

def m17():  # Artist Palette
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,240,245,255))
    d.ellipse([6,8, 26,24], fill=(210,160,100,255))
    d.ellipse([20,16, 24,20], fill=(240,240,245,255))  # Thumb hole
    # Paint dollops
    d.ellipse([9,11, 12,14], fill=(220,30,40,255))
    d.ellipse([14,9, 17,12], fill=(40,110,220,255))
    d.ellipse([19,10, 22,13], fill=(240,200,30,255))
    d.ellipse([9,16, 12,19], fill=(40,150,60,255))
    return im

def m18():  # Quill & Inkwell
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,235,225,255))
    # Inkwell
    d.rectangle([18,18, 26,26], fill=(40,45,60,255))
    d.rectangle([20,15, 24,18], fill=(180,140,50,255))
    # Feather quill
    d.line([(7,5), (21,21)], fill=(240,240,245,255), width=2)
    d.polygon([(7,5), (15,6), (17,13), (12,13)], fill=(120,60,160,255))
    return im

def m19():  # Brass Lantern
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(230,235,245,255))
    # Top & base
    d.polygon([(11,9), (21,9), (19,6), (13,6)], fill=(190,145,40,255))
    d.rectangle([11,23, 21,25], fill=(190,145,40,255))
    # Glass & flame
    d.rectangle([12,9, 20,23], fill=(245,245,230,255))
    d.polygon([(16,12), (18,17), (14,17)], fill=(240,90,20,255))
    return im

def m20():  # Interwoven Celtic Triquetra Knot
    im, d = _canvas(32)
    # Deep navy backing disc
    d.ellipse([3,3, 28,28], fill=(30,45,60,255))
    # Interwoven Triquetra ribbons
    d.arc([7,7, 23,23], 0, 360, fill=(215,175,45,255), width=3)
    d.arc([5,12, 19,26], 30, 270, fill=(40,150,80,255), width=3)
    d.arc([13,12, 27,26], 270, 150, fill=(40,150,80,255), width=3)
    d.arc([9,5, 23,19], 150, 30, fill=(40,150,80,255), width=3)
    # Central knot ruby
    d.ellipse([14,14, 18,18], fill=(220,40,60,255))
    return im

def m21():  # Torii Gate
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,235,235,255))
    # Lintels
    d.line([(5,8), (27,8)], fill=(215,40,40,255), width=3)
    d.line([(7,12), (25,12)], fill=(215,40,40,255), width=2)
    # Pillars
    d.line([(10,8), (10,26)], fill=(215,40,40,255), width=2)
    d.line([(22,8), (22,26)], fill=(215,40,40,255), width=2)
    d.rectangle([14,8, 18,12], fill=(30,30,35,255))
    return im

def m22():  # Royal Crown
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,235,245,255))
    # Gold base
    d.rectangle([8,20, 24,24], fill=(225,180,30,255))
    # Spikes & velvet
    d.polygon([(8,20), (8,11), (12,16), (16,8), (20,16), (24,11), (24,20)], fill=(225,180,30,255))
    d.ellipse([12,13, 20,20], fill=(160,30,50,255))
    d.point([(9,22), (16,22), (23,22)], fill=(40,120,220,255))
    return im

def m23():  # Bumblebee
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(255,250,230,255))
    # Body stripes
    d.ellipse([10,11, 22,23], fill=(245,200,30,255))
    d.rectangle([10,14, 22,17], fill=(30,30,35,255))
    d.rectangle([10,20, 22,22], fill=(30,30,35,255))
    # Wings
    d.ellipse([6,6, 14,14], fill=(220,235,250,255))
    d.ellipse([18,6, 26,14], fill=(220,235,250,255))
    return im

def m24():  # Sunflower
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(235,245,250,255))
    # Ray petals
    for a in range(0, 360, 45):
        rad = math.radians(a)
        px = int(16 + 10 * math.cos(rad))
        py = int(16 + 10 * math.sin(rad))
        d.ellipse([px-3, py-3, px+3, py+3], fill=(245,190,20,255))
    # Center core
    d.ellipse([11,11, 21,21], fill=(90,50,25,255))
    d.ellipse([13,13, 19,19], fill=(130,80,35,255))
    return im

def m25():  # Sacred Lotus
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(225,240,245,255))
    # Water leaf
    d.ellipse([6,20, 26,27], fill=(40,130,70,255))
    # Petals
    d.ellipse([12,9, 20,22], fill=(240,140,170,255))
    d.ellipse([8,12, 16,21], fill=(245,180,200,255))
    d.ellipse([16,12, 24,21], fill=(245,180,200,255))
    d.point([(16,16)], fill=(250,220,50,255))
    return im

def m26():  # Dragonfly
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(235,245,245,255))
    # Long body
    d.line([(16,6), (16,26)], fill=(50,140,160,255), width=2)
    d.ellipse([14,5, 18,9], fill=(30,70,80,255))
    # Wings
    d.line([(5,10), (27,10)], fill=(180,225,240,255), width=2)
    d.line([(7,14), (25,14)], fill=(180,225,240,255), width=2)
    return im

def m27():  # Autumn Maple Leaf
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,245,235,255))
    d.polygon([(16,5), (20,12), (27,13), (22,18), (25,24), (16,21), (7,24), (10,18), (5,13), (12,12)], fill=(225,75,30,255))
    d.line([(16,5), (16,27)], fill=(140,40,15,255), width=1)
    return im

def m28():  # Hummingbird
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,245,245,255))
    # Long beak
    d.line([(7,12), (14,14)], fill=(30,30,35,255), width=1)
    # Body & wing
    d.ellipse([13,12, 22,20], fill=(50,150,110,255))
    d.polygon([(16,14), (24,6), (22,17)], fill=(30,90,140,255))
    d.ellipse([14,12, 17,16], fill=(210,40,60,255))  # Ruby throat
    return im

def m29():  # Scarab Amulet
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,240,230,255))
    d.ellipse([11,10, 21,24], fill=(35,130,150,255))
    d.line([(16,10), (16,24)], fill=(210,170,40,255), width=1)
    d.ellipse([13,6, 19,10], fill=(210,170,40,255))  # Sun disk
    return im

def m30():  # Victorian Teapot
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(245,245,240,255))
    d.ellipse([10,12, 22,24], fill=(235,235,240,255))
    d.arc([5,11, 12,20], 90, 270, fill=(210,165,40,255), width=2)  # Spout
    d.arc([20,13, 27,23], 270, 90, fill=(210,165,40,255), width=2)  # Handle
    d.ellipse([14,9, 18,12], fill=(210,165,40,255))  # Lid
    return im

def m31():  # Mountain & Moon
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(35,45,75,255))
    d.polygon([(6,27), (16,11), (26,27)], fill=(80,95,120,255))
    d.polygon([(13,16), (16,11), (19,16)], fill=(240,245,255,255))
    d.ellipse([20,6, 26,12], fill=(245,220,70,255))
    return im

def m32():  # Saturn
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(25,30,55,255))
    d.ellipse([5,13, 27,19], outline=(225,190,110,255), width=2)  # Rings
    d.ellipse([10,10, 22,22], fill=(215,160,80,255))  # Sphere
    d.arc([5,13, 27,19], 0, 180, fill=(225,190,110,255), width=2)  # Front ring
    return im

def m33():  # Jellyfish
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(25,50,90,255))
    d.ellipse([9,7, 23,17], fill=(210,120,220,255))
    d.line([(11,16), (11,26)], fill=(160,200,245,255), width=1)
    d.line([(14,16), (14,27)], fill=(160,200,245,255), width=1)
    d.line([(18,16), (18,27)], fill=(160,200,245,255), width=1)
    d.line([(21,16), (21,26)], fill=(160,200,245,255), width=1)
    return im

def m34():  # Medieval Crossbow
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(240,235,225,255))
    d.line([(16,7), (16,26)], fill=(120,70,30,255), width=3)  # Stock
    d.arc([7,9, 25,19], 180, 360, fill=(160,170,180,255), width=3)  # Bow
    d.line([(7,14), (25,14)], fill=(220,220,225,255), width=1)  # String
    return im

def m35():  # Yin-Yang Koi
    im, d = _canvas(32)
    d.ellipse([3,3, 28,28], fill=(230,240,245,255))
    d.arc([9,9, 23,23], 0, 180, fill=(225,60,40,255), width=3)
    d.ellipse([11,11, 15,15], fill=(225,60,40,255))
    d.arc([9,9, 23,23], 180, 360, fill=(40,40,50,255), width=3)
    d.ellipse([17,17, 21,21], fill=(40,40,50,255))
    return im


# ===========================================================================
# 30 INDIVIDUAL TIER L DRAWERS (48x48)
# ===========================================================================
def l_wrap(name: str, fn) -> Image.Image:
    im, d = _canvas(48)
    # Master backing emblem shield / disc
    d.ellipse([4,4, 43,43], fill=(242,240,235,255))
    d.ellipse([6,6, 41,41], outline=(200,165,50,255), width=1)
    fn(d)
    return im

def l01():  # Lion Rampant
    def draw(d):
        d.ellipse([16,12, 28,22], fill=(210,150,30,255))  # Head
        d.polygon([(18,20), (28,20), (26,36), (16,36)], fill=(210,150,30,255))  # Torso
        d.line([(26,22), (36,15)], fill=(210,150,30,255), width=3)  # Foreleg
        d.line([(26,34), (36,38)], fill=(210,150,30,255), width=3)  # Hindleg
        d.arc([10,24, 20,38], 90, 270, fill=(180,40,40,255), width=2)  # Tail
        d.polygon([(19,10), (25,10), (22,7)], fill=(220,40,40,255))  # Crown
    return l_wrap("Lion", draw)

def l02():  # Phoenix
    def draw(d):
        d.polygon([(24,12), (10,22), (14,32), (24,24), (34,32), (38,22)], fill=(235,60,30,255))  # Wings
        d.ellipse([21,14, 27,30], fill=(250,180,25,255))  # Body
        d.line([(24,30), (20,42)], fill=(240,110,20,255), width=2)  # Tail plume
        d.line([(24,30), (24,43)], fill=(255,220,40,255), width=2)
        d.line([(24,30), (28,42)], fill=(240,110,20,255), width=2)
    return l_wrap("Phoenix", draw)

def l03():  # Forest Stag
    def draw(d):
        d.ellipse([18,20, 30,32], fill=(135,85,45,255))  # Body
        d.polygon([(18,22), (14,14), (20,14)], fill=(135,85,45,255))  # Head
        # Antlers
        d.line([(16,14), (12,7)], fill=(220,190,140,255), width=2)
        d.line([(14,10), (10,9)], fill=(220,190,140,255), width=1)
        d.line([(18,14), (22,7)], fill=(220,190,140,255), width=2)
        d.line([(20,10), (24,9)], fill=(220,190,140,255), width=1)
    return l_wrap("Stag", draw)

def l04():  # Imperial Dragon
    def draw(d):
        d.arc([12,12, 36,36], 30, 240, fill=(40,140,70,255), width=4)  # Coiled body
        d.ellipse([28,10, 36,18], fill=(40,140,70,255))  # Head
        d.polygon([(34,14), (40,12), (37,17)], fill=(220,40,40,255))  # Whiskers/Fire
        d.ellipse([20,26, 26,32], fill=(230,180,30,255))  # Pearl
    return l_wrap("Dragon", draw)

def l05():  # Stained Glass
    def draw(d):
        d.ellipse([10,10, 38,38], outline=(30,30,40,255), width=2)
        for a in range(0, 360, 45):
            rad = math.radians(a)
            d.line([(24,24), (int(24+14*math.cos(rad)), int(24+14*math.sin(rad)))], fill=(30,30,40,255), width=1)
        d.ellipse([16,16, 32,32], fill=(210,40,60,255))
        d.ellipse([20,20, 28,28], fill=(40,120,220,255))
    return l_wrap("Glass", draw)

def l06():  # Ocean Wave
    def draw(d):
        d.polygon([(8,38), (8,26), (22,14), (32,22), (40,38)], fill=(35,90,165,255))
        d.arc([16,12, 34,28], 180, 360, fill=(240,245,255,255), width=4)  # Crest foam
        d.ellipse([30,10, 38,18], fill=(225,50,40,255))  # Sun
    return l_wrap("Wave", draw)

def l07():  # Medieval Castle
    def draw(d):
        d.rectangle([14,24, 34,38], fill=(120,125,135,255))  # Wall
        d.rectangle([12,16, 18,38], fill=(90,95,105,255))   # Left tower
        d.rectangle([30,16, 36,38], fill=(90,95,105,255))   # Right tower
        d.polygon([(12,16), (15,10), (18,16)], fill=(190,40,40,255))
        d.polygon([(30,16), (33,10), (36,16)], fill=(190,40,40,255))
        d.rectangle([21,30, 27,38], fill=(40,30,20,255))    # Portcullis
    return l_wrap("Castle", draw)

def l08():  # Pirate Galleon
    def draw(d):
        d.polygon([(8,30), (40,30), (34,38), (14,38)], fill=(130,75,35,255))  # Hull
        d.line([(24,10), (24,30)], fill=(80,45,20,255), width=2)  # Mast
        d.polygon([(16,12), (24,12), (24,20), (16,20)], fill=(240,240,245,255))  # Sail
        d.polygon([(24,14), (32,14), (32,22), (24,22)], fill=(240,240,245,255))
        d.line([(24,10), (20,10)], fill=(200,30,30,255), width=1)  # Pennant
    return l_wrap("Galleon", draw)

def l09():  # Wolf Aurora
    def draw(d):
        d.arc([8,8, 40,30], 180, 360, fill=(60,210,160,255), width=3)  # Aurora
        d.polygon([(8,38), (22,30), (22,38)], fill=(45,55,75,255))  # Cliff
        # Howling wolf
        d.polygon([(16,30), (18,22), (22,25)], fill=(25,30,45,255))
    return l_wrap("Wolf", draw)

def l10():  # Tree of Life
    def draw(d):
        d.line([(24,22), (24,34)], fill=(110,65,30,255), width=4)  # Trunk
        d.ellipse([10,10, 38,24], fill=(50,140,65,255))  # Canopy
        d.ellipse([14,12, 34,22], fill=(70,175,85,255))
        d.arc([14,30, 34,42], 0, 180, fill=(110,65,30,255), width=3)  # Roots
    return l_wrap("Tree", draw)

def l11():  # Carnival Mask
    def draw(d):
        d.ellipse([12,18, 36,30], fill=(215,170,40,255))
        d.ellipse([16,22, 22,26], fill=(30,30,35,255))  # Left eye
        d.ellipse([26,22, 32,26], fill=(30,30,35,255))  # Right eye
        # Crown feathers
        d.polygon([(24,18), (14,8), (24,10)], fill=(160,40,150,255))
        d.polygon([(24,18), (24,6), (28,10)], fill=(40,140,210,255))
        d.polygon([(24,18), (34,8), (28,12)], fill=(220,50,60,255))
    return l_wrap("Mask", draw)

def l12():  # Solar Eclipse
    def draw(d):
        d.ellipse([10,10, 38,38], fill=(245,200,30,255))  # Corona rays
        d.ellipse([13,13, 35,35], fill=(25,25,35,255))    # Moon occluder
        d.arc([11,11, 37,37], 30, 150, fill=(255,245,210,255), width=2)
    return l_wrap("Eclipse", draw)

def l13():  # Bald Eagle
    def draw(d):
        d.polygon([(10,18), (24,24), (38,18), (24,36)], fill=(80,50,30,255))  # Wings
        d.ellipse([20,14, 28,24], fill=(245,245,250,255))  # White head
        d.polygon([(22,18), (18,20), (22,21)], fill=(245,190,30,255))  # Beak
    return l_wrap("Eagle", draw)

def l14():  # Tiger in Bamboo
    def draw(d):
        # Bamboo stalks
        d.line([(12,8), (12,40)], fill=(80,160,70,255), width=2)
        d.line([(36,8), (36,40)], fill=(80,160,70,255), width=2)
        # Tiger face
        d.ellipse([16,16, 32,32], fill=(235,130,30,255))
        d.point([(20,22), (28,22)], fill=(25,25,30,255))  # Eyes
        d.line([(18,18), (22,18)], fill=(25,25,30,255), width=1)  # Stripes
        d.line([(26,18), (30,18)], fill=(25,25,30,255), width=1)
    return l_wrap("Tiger", draw)

def l15():  # Winged Pegasus
    def draw(d):
        d.ellipse([16,22, 32,34], fill=(235,235,245,255))  # Body
        d.polygon([(28,24), (34,16), (36,22)], fill=(235,235,245,255))  # Neck/Head
        d.polygon([(20,24), (14,10), (26,16)], fill=(180,210,245,255))  # Wing
    return l_wrap("Pegasus", draw)

def l16():  # Alchemist Lab
    def draw(d):
        d.rectangle([10,34, 38,38], fill=(120,70,35,255))  # Table
        # Flask
        d.polygon([(16,34), (24,34), (22,24), (22,20), (18,20), (18,24)], fill=(180,225,250,255))
        d.ellipse([17,28, 23,34], fill=(180,40,190,255))  # Potion
    return l_wrap("Alchemist", draw)

def l17():  # Astrolabe
    def draw(d):
        d.ellipse([12,12, 36,36], outline=(205,160,40,255), width=3)
        d.ellipse([16,16, 32,32], outline=(160,120,30,255), width=1)
        d.line([(12,24), (36,24)], fill=(205,160,40,255), width=2)
        d.line([(24,12), (24,36)], fill=(205,160,40,255), width=2)
    return l_wrap("Astrolabe", draw)

def l18():  # Griffin
    def draw(d):
        d.polygon([(18,18), (30,18), (28,34), (16,34)], fill=(180,120,40,255))  # Body
        d.polygon([(18,18), (12,14), (18,12)], fill=(220,170,40,255))  # Eagle beak
        d.polygon([(20,20), (14,8), (24,14)], fill=(210,50,50,255))    # Wing
    return l_wrap("Griffin", draw)

def l19():  # Kraken
    def draw(d):
        d.ellipse([16,14, 32,26], fill=(160,40,70,255))  # Head
        for tx in [14, 20, 28, 34]:
            d.line([(tx, 24), (tx-2, 38)], fill=(160,40,70,255), width=2)  # Tentacles
        d.point([(20,20), (28,20)], fill=(245,210,40,255))
    return l_wrap("Kraken", draw)

def l20():  # Japanese Pagoda
    def draw(d):
        d.polygon([(16,14), (32,14), (24,10)], fill=(180,40,40,255))  # Roof 1
        d.polygon([(14,22), (34,22), (24,18)], fill=(180,40,40,255))  # Roof 2
        d.polygon([(12,30), (36,30), (24,26)], fill=(180,40,40,255))  # Roof 3
        d.rectangle([20,30, 28,38], fill=(60,50,45,255))
    return l_wrap("Pagoda", draw)

def l21():  # Aztec Sun Stone
    def draw(d):
        d.ellipse([12,12, 36,36], fill=(215,150,40,255))
        d.ellipse([16,16, 32,32], fill=(160,85,30,255))
        d.ellipse([20,20, 28,28], fill=(245,210,50,255))
    return l_wrap("Aztec", draw)

def l22():  # Norse Valknut
    def draw(d):
        d.polygon([(24,12), (18,22), (30,22)], outline=(60,110,180,255), width=2)
        d.polygon([(18,18), (12,28), (24,28)], outline=(60,110,180,255), width=2)
        d.polygon([(30,18), (24,28), (36,28)], outline=(60,110,180,255), width=2)
    return l_wrap("Valknut", draw)

def l23():  # Renaissance Tapestry
    def draw(d):
        d.rectangle([10,10, 38,38], outline=(160,50,70,255), width=2)
        d.ellipse([16,16, 32,32], fill=(235,210,160,255))
        d.ellipse([20,20, 28,28], fill=(160,50,70,255))
    return l_wrap("Tapestry", draw)

def l24():  # Knight on Horseback
    def draw(d):
        d.ellipse([14,24, 34,36], fill=(140,80,40,255))  # Horse
        d.rectangle([20,16, 26,26], fill=(160,170,185,255))  # Knight
        d.line([(24,18), (40,10)], fill=(200,205,215,255), width=2)  # Lance
    return l_wrap("Knight", draw)

def l25():  # Desert Pyramids
    def draw(d):
        d.polygon([(6,36), (22,18), (34,36)], fill=(215,160,70,255))   # Big pyramid
        d.polygon([(26,36), (36,24), (44,36)], fill=(185,130,50,255))  # Small pyramid
        d.ellipse([10,10, 18,18], fill=(245,110,35,255))  # Sunset
    return l_wrap("Pyramids", draw)

def l26():  # Space Nebula
    def draw(d):
        d.ellipse([10,12, 38,34], fill=(80,30,120,255))
        d.ellipse([14,16, 32,30], fill=(40,130,200,255))
        d.ellipse([20,20, 28,26], fill=(245,140,180,255))
    return l_wrap("Nebula", draw)

def l27():  # Mermaid
    def draw(d):
        d.ellipse([18,12, 26,22], fill=(240,200,170,255))  # Torso
        d.arc([16,22, 34,38], 0, 180, fill=(40,150,130,255), width=4)  # Tail
        d.polygon([(14,34), (18,40), (14,38)], fill=(40,150,130,255))
    return l_wrap("Mermaid", draw)

def l28():  # Gargoyle
    def draw(d):
        d.polygon([(14,34), (34,34), (28,38), (14,38)], fill=(100,105,115,255))  # Ledge
        d.ellipse([18,20, 30,34], fill=(75,80,90,255))  # Stone body
        d.polygon([(20,22), (12,12), (24,18)], fill=(60,65,75,255))  # Stone wing
    return l_wrap("Gargoyle", draw)

def l29():  # Greenhouse
    def draw(d):
        d.polygon([(12,20), (24,10), (36,20)], outline=(50,80,60,255), width=2)
        d.rectangle([12,20, 36,36], outline=(50,80,60,255), width=2)
        d.ellipse([18,24, 30,36], fill=(50,160,80,255))  # Palm leaf
    return l_wrap("Greenhouse", draw)

def l30():  # Double-Headed Eagle
    def draw(d):
        d.ellipse([18,18, 30,34], fill=(40,40,45,255))  # Body
        d.ellipse([16,12, 22,18], fill=(40,40,45,255))  # Left head
        d.ellipse([26,12, 32,18], fill=(40,40,45,255))  # Right head
        d.polygon([(10,18), (18,22), (18,32)], fill=(40,40,45,255))  # Left wing
        d.polygon([(38,18), (30,22), (30,32)], fill=(40,40,45,255))  # Right wing
        d.ellipse([21,8, 27,12], fill=(215,170,40,255))  # Crown
    return l_wrap("Imperial", draw)


# ===========================================================================
# DISPATCHER ARRAYS
# ===========================================================================
S_FUNCS = [
    ("Pixel Heart", s01), ("Golden Star", s02), ("Vintage Key", s03), ("Music Note", s04), ("Red Apple", s05),
    ("Coffee Mug", s06), ("Magic Potion", s07), ("Knight Sword", s08), ("Wooden Shield", s09), ("Skull", s10),
    ("Lucky Clover", s11), ("Rain Cloud", s12), ("Crescent Moon", s13), ("Flying Bird", s14), ("Cat Face", s15),
    ("Goldfish", s16), ("Mushroom", s17), ("Daisy Flower", s18), ("Pine Tree", s19), ("Cherry Pair", s20),
    ("Campfire", s21), ("Diamond Gem", s22), ("Sailboat", s23), ("Anchor", s24), ("Old Compass", s25),
    ("Wine Glass", s26), ("Cupcake", s27), ("Pizza Slice", s28), ("Tennis Racket", s29), ("Paper Airplane", s30),
    ("Ghost Sprite", s31), ("Helm Wheel", s32), ("Hourglass", s33), ("Gamepad", s34), ("Gothic Cross", s35)
]

M_FUNCS = [
    ("Blue Butterfly", m01), ("Barn Owl", m02), ("Red Fox", m03), ("Sea Turtle", m04), ("Chameleon", m05),
    ("Bonsai Tree", m06), ("Crimson Rose", m07), ("Desert Cactus", m08), ("Coast Lighthouse", m09), ("Old Windmill", m10),
    ("Vintage Camera", m11), ("Acoustic Guitar", m12), ("Hot Air Balloon", m13), ("Steam Locomotive", m14), ("Retro Beetle Car", m15),
    ("Antique Pocketwatch", m16), ("Artist Palette", m17), ("Quill & Inkwell", m18), ("Brass Lantern", m19), ("Celtic Knot", m20),
    ("Torii Gate", m21), ("Royal Crown", m22), ("Bumblebee", m23), ("Sunflower", m24), ("Sacred Lotus", m25),
    ("Dragonfly", m26), ("Autumn Maple Leaf", m27), ("Hummingbird", m28), ("Scarab Amulet", m29), ("Victorian Teapot", m30),
    ("Mountain & Moon", m31), ("Saturn Rings", m32), ("Deep Sea Jellyfish", m33), ("Medieval Crossbow", m34), ("Yin-Yang Koi", m35)
]

L_FUNCS = [
    ("Lion Rampant", l01), ("Rising Phoenix", l02), ("Forest Stag", l03), ("Imperial Dragon", l04), ("Stained Glass", l05),
    ("Ocean Wave", l06), ("Medieval Castle", l07), ("Pirate Galleon", l08), ("Wolf Aurora", l09), ("Tree of Life", l10),
    ("Carnival Mask", l11), ("Solar Eclipse", l12), ("Bald Eagle", l13), ("Tiger in Bamboo", l14), ("Winged Pegasus", l15),
    ("Alchemist Lab", l16), ("Astrolabe", l17), ("Griffin", l18), ("Kraken", l19), ("Japanese Pagoda", l20),
    ("Aztec Sun Stone", l21), ("Norse Valknut", l22), ("Renaissance Tapestry", l23), ("Knight on Horseback", l24), ("Desert Pyramids", l25),
    ("Space Nebula", l26), ("Mermaid", l27), ("Gargoyle", l28), ("Greenhouse", l29), ("Double-Headed Eagle", l30)
]


def main():
    print("=" * 80)
    print("GENERATING 100 FULLY INDIVIDUAL, NON-GENERIC EMBROIDERY BENCHMARK PATTERNS")
    print("=" * 80)

    manifest = []

    # 1. Tier S
    print("\n--- Generating Tier S (35 Dedicated Handcrafted Motifs, 16x16) ---")
    for i, (name, fn) in enumerate(S_FUNCS):
        slug = f"pattern_s_{i+1:02d}"
        img = fn()
        N, K = _count(img)
        fpath = os.path.join(OUT_DIR, "small", f"{slug}.png")
        img.save(fpath)
        manifest.append({
            "id": slug, "name": name, "tier": "Tier S (Small)", "tier_code": "S",
            "file": os.path.relpath(fpath, BASE_DIR), "size": "16x16", "N": N, "K": K, "style": name
        })
        if (i + 1) % 7 == 0:
            print(f"  [v] {slug}: {name} (N={N}, K={K})")

    # 2. Tier M
    print("\n--- Generating Tier M (35 Dedicated Handcrafted Motifs, 32x32) ---")
    for i, (name, fn) in enumerate(M_FUNCS):
        slug = f"pattern_m_{i+1:02d}"
        img = fn()
        N, K = _count(img)
        fpath = os.path.join(OUT_DIR, "medium", f"{slug}.png")
        img.save(fpath)
        manifest.append({
            "id": slug, "name": name, "tier": "Tier M (Medium)", "tier_code": "M",
            "file": os.path.relpath(fpath, BASE_DIR), "size": "32x32", "N": N, "K": K, "style": name
        })
        if (i + 1) % 7 == 0:
            print(f"  [v] {slug}: {name} (N={N}, K={K})")

    # 3. Tier L
    print("\n--- Generating Tier L (30 Dedicated Handcrafted Motifs, 48x48) ---")
    for i, (name, fn) in enumerate(L_FUNCS):
        slug = f"pattern_l_{i+1:02d}"
        img = fn()
        N, K = _count(img)
        fpath = os.path.join(OUT_DIR, "large", f"{slug}.png")
        img.save(fpath)
        manifest.append({
            "id": slug, "name": name, "tier": "Tier L (Large)", "tier_code": "L",
            "file": os.path.relpath(fpath, BASE_DIR), "size": "48x48", "N": N, "K": K, "style": name
        })
        if (i + 1) % 6 == 0:
            print(f"  [v] {slug}: {name} (N={N}, K={K})")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 80)
    print("SUCCESS: 100 Individual, distinct motifs generated with 100 separate functions!")
    print(f"Manifest written to: {MANIFEST_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()
