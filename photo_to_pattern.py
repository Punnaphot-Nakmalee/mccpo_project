"""
photo_to_pattern.py — Real Image / Photo to Embroidery Pattern Converter
========================================================================
Converts any photograph, artwork, or sprite into a clean, multi-color
cross-stitch embroidery pattern suitable for the MCCPO optimization pipeline.

Pipeline:
  1. Downsamples image to target stitch grid (e.g. 16x16, 32x32, 48x48).
  2. Identifies and removes background (transparency or border-dominant color).
  3. Quantizes remaining active foreground pixels to K thread colors using K-Means.
  4. Saves clean RGBA pixel-art pattern PNG.

Usage:
  python photo_to_pattern.py <input_image> --size 32 --colors 5 --output pattern.png
"""

import os
import sys
import argparse
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from typing import Tuple, Optional, List, Dict, Any


def convert_image_to_pattern(
    image_input,
    target_size: Tuple[int, int] = (32, 32),
    num_colors: int = 5,
    remove_bg: bool = True,
    bg_threshold: float = 240.0,
    output_path: Optional[str] = None
) -> Image.Image:
    """
    Converts an input PIL Image or image file path into a quantized cross-stitch pattern.

    Parameters
    ----------
    image_input : str or PIL.Image.Image
        Path to image file or PIL Image instance.
    target_size : tuple (width, height)
        Grid dimensions in stitches (e.g. (16, 16), (32, 32), (48, 48)).
    num_colors : int
        Number of distinct thread colors (K).
    remove_bg : bool
        If True, auto-detects and masks out background (near-white or dominant border color).
    bg_threshold : float
        Luminance threshold above which pixels are treated as white background (0-255).
    output_path : str, optional
        Where to save the resulting PNG.

    Returns
    -------
    PIL.Image.Image (RGBA)
    """
    if isinstance(image_input, str):
        img = Image.open(image_input).convert("RGBA")
    else:
        img = image_input.convert("RGBA")

    # 1. Resize to target stitch grid
    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    img_small = img.resize(target_size, resample=resample_filter)
    arr = np.array(img_small)  # (H, W, 4)

    h, w, _ = arr.shape
    rgb = arr[:, :, :3].astype(np.float64)
    alpha = arr[:, :, 3]

    # 2. Build foreground mask
    if remove_bg:
        # Check alpha channel transparency first
        mask_fg = alpha > 128
        luminance = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]

        from scipy.ndimage import label

        # Detect border-connected black/dark background
        is_dark = luminance < 22.0
        lbl_dark, _ = label(is_dark)
        border_dark_lbls = set(np.unique(np.concatenate([lbl_dark[0, :], lbl_dark[-1, :], lbl_dark[:, 0], lbl_dark[:, -1]])))
        if 0 in border_dark_lbls: border_dark_lbls.remove(0)
        is_border_dark_bg = np.isin(lbl_dark, list(border_dark_lbls)) if border_dark_lbls else np.zeros_like(is_dark)

        # Detect border-connected white/light background
        is_white = luminance >= bg_threshold
        lbl_white, _ = label(is_white)
        border_white_lbls = set(np.unique(np.concatenate([lbl_white[0, :], lbl_white[-1, :], lbl_white[:, 0], lbl_white[:, -1]])))
        if 0 in border_white_lbls: border_white_lbls.remove(0)
        is_border_white_bg = np.isin(lbl_white, list(border_white_lbls)) if border_white_lbls else np.zeros_like(is_white)

        # Active foreground: alpha high AND not border-connected black/white background
        mask_fg = mask_fg & (~is_border_dark_bg) & (~is_border_white_bg)

        # Fallback: if mask removed too much (> 85%), keep all non-zero alpha
        if np.sum(mask_fg) < 0.10 * (h * w):
            mask_fg = alpha > 128
    else:
        mask_fg = alpha > 128

    fg_pixels = rgb[mask_fg]

    if len(fg_pixels) < num_colors:
        # Trivial or almost empty foreground: return as is
        result_img = Image.fromarray(arr, mode="RGBA")
        if output_path:
            result_img.save(output_path)
        return result_img

    # 3. K-Means Color Quantization on Foreground Pixels
    effective_k = min(num_colors, len(fg_pixels))
    kmeans = KMeans(n_clusters=effective_k, random_state=42, n_init=5)
    labels = kmeans.fit_predict(fg_pixels)
    palette = np.round(kmeans.cluster_centers_).astype(np.uint8)

    # 4. Reconstruct Output RGBA Image
    out_arr = np.zeros((h, w, 4), dtype=np.uint8)
    fg_indices = np.where(mask_fg)
    for idx, (r, c) in enumerate(zip(fg_indices[0], fg_indices[1])):
        color_idx = labels[idx]
        out_arr[r, c, :3] = palette[color_idx]
        out_arr[r, c, 3] = 255  # Fully opaque active stitch

    result_img = Image.fromarray(out_arr, mode="RGBA")
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        result_img.save(output_path)

    return result_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert photo/image to embroidery pattern.")
    parser.add_argument("input", help="Path to input image file (jpg, png, webp, etc.).")
    parser.add_argument("--size", type=int, default=32, help="Target grid dimension (e.g. 16, 24, 32, 48). Default: 32.")
    parser.add_argument("--colors", type=int, default=5, help="Number of thread colors K (default: 5).")
    parser.add_argument("--output", default="my_custom_pattern.png", help="Path to save pattern PNG.")
    parser.add_argument("--optimize", action="store_true", help="Run ALNS optimizer immediately on the generated pattern.")
    args = parser.parse_args()

    print(f"Converting '{args.input}' to embroidery pattern (Size: {args.size}x{args.size}, K={args.colors} colors)...")
    res_img = convert_image_to_pattern(
        args.input,
        target_size=(args.size, args.size),
        num_colors=args.colors,
        output_path=args.output
    )
    print(f"Success! Pattern generated and saved to: {args.output}")

    if args.optimize:
        from parser import load_pattern_from_image
        from baseline_color_scan import solve_color_scan
        from evaluator import evaluate_order, compute_normalized_objective
        from search_alns import ALNSMCCPO

        print("\n" + "=" * 65)
        print("RUNNING EMBROIDERY PATH OPTIMIZATION (NORMALIZED ALNS)")
        print("=" * 65)
        stitches = load_pattern_from_image(args.output, normalize_origin=True)
        N = len(stitches)
        print(f"Loaded {N} active stitches.")

        # Baseline Human Crafter (Reference)
        ord_human = solve_color_scan(stitches)
        res_human = evaluate_order(stitches, ord_human)
        j_human_raw = res_human["f_thread"] + 10.0 * res_human["f_switch"]
        j_human_norm = compute_normalized_objective(
            res_human["f_thread"], res_human["f_switch"],
            res_human["f_thread"], res_human["f_switch"], w1=0.5, w2=0.5
        )

        # Proposed ALNS (Normalized Multi-Objective Mode)
        iters = 150 if N < 300 else (200 if N < 800 else 250)
        solver = ALNSMCCPO(stitches, max_iterations=iters, seed=42, normalized=True, w1=0.5, w2=0.5)
        res_alns = solver.search()
        j_alns_raw = res_alns["f_thread"] + 10.0 * res_alns["f_switch"]
        j_alns_norm = compute_normalized_objective(
            res_alns["f_thread"], res_alns["f_switch"],
            res_human["f_thread"], res_human["f_switch"], w1=0.5, w2=0.5
        )

        thread_saving = ((res_human["f_thread"] - res_alns["f_thread"]) / res_human["f_thread"]) * 100.0
        total_saving_raw = ((j_human_raw - j_alns_raw) / j_human_raw) * 100.0
        total_saving_norm = (1.0 - j_alns_norm) * 100.0

        print(f"\n1. PHYSICAL THREAD COST (f_thread):")
        print(f"   - Human Crafter : {res_human['f_thread']:.2f} units")
        print(f"   - ALNS (Our AI) : {res_alns['f_thread']:.2f} units (saves {thread_saving:.2f}% | {res_human['f_thread'] - res_alns['f_thread']:.2f} units saved)")

        print(f"\n2. COLOR SPOOL SWITCHES (f_switch):")
        print(f"   - Human Crafter : {res_human['f_switch']} switches")
        print(f"   - ALNS (Our AI) : {res_alns['f_switch']} switches (strictly locked at K-1)")

        print(f"\n3. TOTAL OBJECTIVE FUNCTION J(pi) = f_thread + 10.0 * f_switch:")
        print(f"   - Human Crafter : {j_human_raw:.2f} units")
        print(f"   - ALNS (Our AI) : {j_alns_raw:.2f} units (saves {total_saving_raw:.2f}% total cost)")

        print(f"\n4. NORMALIZED OBJECTIVE J_norm(pi) = 0.5 * (f_t/ref) + 0.5 * (f_s/ref):")
        print(f"   - Human Baseline: {j_human_norm:.4f} (Standard 1.0000 Reference)")
        print(f"   - ALNS (Our AI) : {j_alns_norm:.4f} (Reduced by {total_saving_norm:.2f}%!)")
        print("=" * 65)
