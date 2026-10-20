/**
 * build_deck.js
 * Generates the master defense presentation deck for MCCPO using pptxgenjs.
 * Strictly adheres to pptx skill rules:
 *   - No "#" in hex colors (e.g. "1E40AF", not "#1E40AF")
 *   - Fresh option objects per add* call
 *   - No accent underlines or AI decorative stripes
 *   - Speaker notes included on every slide
 *   - High-contrast visual hierarchy (Dark/Light sandwich structure)
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10.0" x 5.625"

// ---------------------------------------------------------------------------
// Design Palette (Hex without #)
// ---------------------------------------------------------------------------
const C = {
  bgDark: "0F172A",      // Dark Slate 900
  bgLight: "F8FAFC",     // Off-white Slate 50
  cardBg: "FFFFFF",      // Pure White Card
  cardBorder: "E2E8F0",  // Slate 200 border
  textDark: "0F172A",    // Slate 900
  textMuted: "64748B",   // Slate 500
  textLight: "F8FAFC",   // Off-white
  primary: "1E40AF",     // Royal Blue 800
  accentRose: "E11D48",  // Rose 600
  accentEmerald: "059669",// Emerald 600
  accentAmber: "D97706", // Amber 600
  badgeBg: "EEF2FF",     // Indigo 50
};

const BASE_DIR = __dirname;
const IMG_SHOWCASE = path.join(BASE_DIR, "showcase", "showcase_comparison_sprite_flower_16x16.png");
const IMG_PARETO = path.join(BASE_DIR, "benchmark_results", "pareto_curve_sprite_flower.png");
const IMG_SCALE = path.join(BASE_DIR, "benchmark_results", "scalability_runtime_curve.png");


// ===========================================================================
// SLIDE 1: Title Slide (Dark Theme)
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgDark };

  // Category Tag
  slide.addText("ADVANCED SEARCH & HEURISTIC OPTIMIZATION — FINAL DEFENSE", {
    x: 0.8, y: 0.9, w: 8.4, h: 0.35,
    fontSize: 11, bold: true, color: "93C5FD", charSpacing: 2, margin: 0
  });

  // Main Title
  slide.addText("Multi-Color Cross-Stitch Path Optimization", {
    x: 0.8, y: 1.35, w: 8.4, h: 1.1,
    fontSize: 32, bold: true, color: C.textLight, margin: 0, fontFace: "Arial"
  });

  // Subtitle
  slide.addText("Resolving the Pareto Trade-Off Between Thread Waste and Discrete Stoppage in Single-Needle Systems", {
    x: 0.8, y: 2.55, w: 8.4, h: 0.7,
    fontSize: 14, color: "CBD5E1", margin: 0
  });

  // Authors Card Container
  slide.addShape(pres.ShapeType.rect, {
    x: 0.8, y: 3.6, w: 8.4, h: 1.3,
    fill: { color: "1E293B" }, line: { color: "334155", width: 1 }
  });

  slide.addText([
    { text: "Investigators: ", options: { bold: true, color: "93C5FD", fontSize: 12 } },
    { text: "Punnaphot Nakmalee (6709616632)  |  Sirasa Choomalee (6709681156)\n", options: { color: C.textLight, fontSize: 12 } },
    { text: "Core Algorithms: ", options: { bold: true, color: "93C5FD", fontSize: 11 } },
    { text: "Informed A* Search (Tier 1 Exact)  •  Simulated Annealing & Genetic Algorithm (Tier 2 Metaheuristics)\n", options: { color: "CBD5E1", fontSize: 11 } },
    { text: "Course: ", options: { bold: true, color: "93C5FD", fontSize: 11 } },
    { text: "Advanced Search & Heuristic Optimization — Academic Project Defense (2026)", options: { color: "94A3B8", fontSize: 11 } }
  ], { x: 1.1, y: 3.75, w: 7.8, h: 1.0, margin: 0 });

  slide.addNotes("Good morning/afternoon professor. Today we present our research on Multi-Color Cross-Stitch Path Optimization (MCCPO). We address a critical physical trade-off in single-needle computer embroidery that has been ignored in classical TSP literature: the tension between physical thread waste and manual color-change stoppage.");
}


// ===========================================================================
// SLIDE 2: The Physical Craft Dilemma & Scoping
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("PROBLEM FORMULATION & SCOPING", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.primary, charSpacing: 1.5, margin: 0
  });
  slide.addText("The Physical Dilemma in Single-Needle Systems", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Left Card: Physical Dilemma
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("The Operational Bottleneck", {
    x: 0.9, y: 1.7, w: 3.65, h: 0.35,
    fontSize: 14, bold: true, color: C.accentRose, margin: 0
  });
  slide.addText([
    { text: "Single-Needle Systems Scope:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Home machines (Brother SE600, Janome) and hand crafters possess exactly one needle. Industrial multi-needle machines are explicitly out of scope.", options: { fontSize: 10, breakLine: true } },
    { text: "The Discrete Color-Change Penalty:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Every color change is a physical stoppage (30–60s) requiring spool cutting, re-threading, and anchoring.", options: { fontSize: 10, breakLine: true } },
    { text: "The Jump Distance Limit (d_max):", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Carrying thread over long distances (D > 3.16) causes severe fabric puckering and snagging, forcing a cut & tie-off.", options: { fontSize: 10 } }
  ], { x: 0.9, y: 2.15, w: 3.65, h: 2.7, bullet: true, paraSpaceAfter: 8, margin: 0 });

  // Right Card: Prior Literature Gap
  slide.addShape(pres.ShapeType.rect, {
    x: 5.15, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("Prior Literature & Research Gap", {
    x: 5.45, y: 1.7, w: 3.65, h: 0.35,
    fontSize: 14, bold: true, color: C.primary, margin: 0
  });
  slide.addText([
    { text: "Prior Work (Biedl 2005, Arkin 2008):", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Focused exclusively on monochrome (single-color) Euler tours and uncolored TSP. Multi-color physics were ignored.", options: { fontSize: 10, breakLine: true } },
    { text: "The Dead-End Graph Fallacy:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Treating jump limits as hard constraints creates disconnected graphs with no valid Hamiltonian paths (NP-complete).", options: { fontSize: 10, breakLine: true } },
    { text: "Our Innovation:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "We model manual Cut & Tie-off as an explicit fallback action, keeping the search graph 100% complete and metric.", options: { fontSize: 10 } }
  ], { x: 5.45, y: 2.15, w: 3.65, h: 2.7, bullet: true, paraSpaceAfter: 8, margin: 0 });

  slide.addNotes("Why single needle? Industrial machines have 15 automated needles and switch in 2 seconds. In home machines and hand crafting, color changing requires 30 to 60 seconds of manual human labor. Literature previously treated long jumps as impossible dead ends; we model them as fallback cut-and-tie operations.");
}


// ===========================================================================
// SLIDE 3: Two-Tier Action Space Mathematical Formulation
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("MATHEMATICAL MODELING", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.primary, charSpacing: 1.5, margin: 0
  });
  slide.addText("Two-Tier Action Space & Bi-Objective Cost Model", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Action 1 Box
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 1.45, w: 4.25, h: 1.7,
    fill: { color: C.cardBg }, line: { color: C.accentEmerald, width: 1.5 }
  });
  slide.addText("Action 1: Continuous Carry", {
    x: 0.85, y: 1.6, w: 3.75, h: 0.3,
    fontSize: 13, bold: true, color: C.accentEmerald, margin: 0
  });
  slide.addText("Condition: same_color AND Euclidean Distance D <= d_max (3.162)\nCost = D (fabric thread consumed on back of fabric)\nEffect: Zero color switches; continuous uninterrupted stitching.", {
    x: 0.85, y: 1.95, w: 3.75, h: 1.05,
    fontSize: 10, color: C.textDark, margin: 0
  });

  // Action 2 Box
  slide.addShape(pres.ShapeType.rect, {
    x: 5.15, y: 1.45, w: 4.25, h: 1.7,
    fill: { color: C.cardBg }, line: { color: C.accentRose, width: 1.5 }
  });
  slide.addText("Action 2: Cut & Tie-Off", {
    x: 5.4, y: 1.6, w: 3.75, h: 0.3,
    fontSize: 13, bold: true, color: C.accentRose, margin: 0
  });
  slide.addText("Condition: different_color OR D > d_max (long jump)\nCost = C_trim (10.0 grid units operational thread penalty)\nEffect: Increments cut count; increments f_switch if color changed.", {
    x: 5.4, y: 1.95, w: 3.75, h: 1.05,
    fontSize: 10, color: C.textDark, margin: 0
  });

  // Bi-Objective Formulation Box below
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 3.35, w: 8.8, h: 1.75,
    fill: { color: "F1F5F9" }, line: { color: "CBD5E1", width: 1 }
  });
  slide.addText("Bi-Objective Optimization Formulation", {
    x: 0.9, y: 3.5, w: 8.2, h: 0.3,
    fontSize: 13, bold: true, color: C.textDark, margin: 0
  });
  slide.addText([
    { text: "Primary Objective 1 (Thread Minimization): ", options: { bold: true, fontSize: 10 } },
    { text: "Minimize f_thread(pi) = Carried Distance + (Cut Count * C_trim)\n", options: { fontSize: 10 } },
    { text: "Primary Objective 2 (Stoppage Minimization): ", options: { bold: true, fontSize: 10 } },
    { text: "Minimize f_switch(pi) = Total discrete thread spool changes\n", options: { fontSize: 10 } },
    { text: "Strict Admissible A* Heuristic: ", options: { bold: true, fontSize: 10 } },
    { text: "h(s) = max(MST_distance, Color_Switch_Bound * C_trim) + lambda * S_min", options: { fontSize: 10, color: C.primary, bold: true } }
  ], { x: 0.9, y: 3.85, w: 8.2, h: 1.15, margin: 0 });

  slide.addNotes("Here is our Two-Tier Action Space: when two stitches are the same color and within 3.16 units, you carry the thread. If either condition fails, you cut and tie off. Notice our admissible heuristic for A*: taking the maximum of the spatial MST and the color switch lower bound guarantees no double-counting.");
}


// ===========================================================================
// SLIDE 4: Algorithms Evaluated — Two-Tier Architecture
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("EXPERIMENTAL DESIGN", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.primary, charSpacing: 1.5, margin: 0
  });
  slide.addText("Algorithms Evaluated: Two-Tier Benchmark Structure", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Card 1: Baselines
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 1.45, w: 2.75, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("Conventional Baselines", {
    x: 0.75, y: 1.65, w: 2.45, h: 0.3,
    fontSize: 12, bold: true, color: C.textMuted, margin: 0
  });
  slide.addText([
    { text: "B1: Raster Scan", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Naïve top-to-bottom row scan; printer carriage order.", options: { fontSize: 9, breakLine: true } },
    { text: "B2: Color-by-Color", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Traditional crafter order; minimizes color changes (K-1).", options: { fontSize: 9, breakLine: true } },
    { text: "B3: Greedy NN", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Spatial nearest neighbor jump, ignoring stitch color.", options: { fontSize: 9, breakLine: true } },
    { text: "B4: Uncolored 2-Opt", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Classic TSP solver untangling spatial edges.", options: { fontSize: 9 } }
  ], { x: 0.75, y: 2.05, w: 2.45, h: 2.8, bullet: true, paraSpaceAfter: 6, margin: 0 });

  // Card 2: Tier 1 A*
  slide.addShape(pres.ShapeType.rect, {
    x: 3.62, y: 1.45, w: 2.75, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.primary, width: 1.5 }
  });
  slide.addText("Tier 1: Exact A* Search", {
    x: 3.77, y: 1.65, w: 2.45, h: 0.3,
    fontSize: 12, bold: true, color: C.primary, margin: 0
  });
  slide.addText([
    { text: "Scope: N <= 15 Only", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Used exclusively to find ground truth J* on micro-motifs.", options: { fontSize: 9, breakLine: true } },
    { text: "State Representation:", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "(v_curr, unvisited_mask, c_curr) with priority queue.", options: { fontSize: 9, breakLine: true } },
    { text: "Fast Prim MST:", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Precomputed metric graph with LRU memoization.", options: { fontSize: 9, breakLine: true } },
    { text: "Role in Research:", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Gold-standard baseline to compute true Optimality Gaps.", options: { fontSize: 9 } }
  ], { x: 3.77, y: 2.05, w: 2.45, h: 2.8, bullet: true, paraSpaceAfter: 6, margin: 0 });

  // Card 3: Tier 2 SA & GA
  slide.addShape(pres.ShapeType.rect, {
    x: 6.65, y: 1.45, w: 2.75, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.accentEmerald, width: 1.5 }
  });
  slide.addText("Tier 2: Metaheuristics", {
    x: 6.8, y: 1.65, w: 2.45, h: 0.3,
    fontSize: 12, bold: true, color: C.accentEmerald, margin: 0
  });
  slide.addText([
    { text: "Scope: N = 50 ~ 200+ Sprites", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Scalable solvers for real production embroidery files.", options: { fontSize: 9, breakLine: true } },
    { text: "Simulated Annealing:", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "3 operators: 2-opt edge swap, color-block shift, single insertion.", options: { fontSize: 9, breakLine: true } },
    { text: "Genetic Algorithm:", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "Order Crossover (OX1), swap/inversion mutations, elitism.", options: { fontSize: 9, breakLine: true } },
    { text: "Statistical Protocol:", options: { bold: true, fontSize: 10, breakLine: true } },
    { text: "10 fixed random seeds; Mean +/- Std reported.", options: { fontSize: 9 } }
  ], { x: 6.8, y: 2.05, w: 2.45, h: 2.8, bullet: true, paraSpaceAfter: 6, margin: 0 });

  slide.addNotes("We structured the algorithms into two tiers: 4 conventional baselines, Tier 1 exact A* search to establish ground truth, and Tier 2 metaheuristics (SA and GA) as the real practical solvers for real pixel-art sprites.");
}


// ===========================================================================
// SLIDE 5: The "Checkerboard Trap" (Key Empirical Finding 1)
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("KEY EMPIRICAL FINDING 1", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.accentRose, charSpacing: 1.5, margin: 0
  });
  slide.addText("The 'Checkerboard Trap': Why Standard TSP Fails", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Left side: Callout metrics on checker_8
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("Evidence: Checkerboard Pattern (N=8, 2 Colors)", {
    x: 0.85, y: 1.7, w: 3.75, h: 0.35,
    fontSize: 12, bold: true, color: C.textDark, margin: 0
  });

  // Stat Comparison Box
  slide.addShape(pres.ShapeType.rect, {
    x: 0.85, y: 2.15, w: 3.75, h: 1.1,
    fill: { color: "FEF2F2" }, line: { color: "FCA5A5", width: 1 }
  });
  slide.addText("Baselines 3 & 4 (Greedy & 2-Opt TSP):\nTotal Thread Cost: 70.00  |  Color Switches: 7\nSwitched thread spools at nearly EVERY single step!", {
    x: 0.95, y: 2.25, w: 3.55, h: 0.9,
    fontSize: 10, bold: true, color: C.accentRose, margin: 0
  });

  slide.addShape(pres.ShapeType.rect, {
    x: 0.85, y: 3.4, w: 3.75, h: 1.1,
    fill: { color: "ECFDF5" }, line: { color: "6EE7B7", width: 1 }
  });
  slide.addText("Color-Aware Solvers (B2, A*, SA, GA):\nTotal Thread Cost: 18.48  |  Color Switches: 1\nSaves 51.5 thread units (73.6% reduction)!", {
    x: 0.95, y: 3.5, w: 3.55, h: 0.9,
    fontSize: 10, bold: true, color: C.accentEmerald, margin: 0
  });

  // Right side: Why it happens
  slide.addShape(pres.ShapeType.rect, {
    x: 5.15, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("Theoretical Mechanism & Insight", {
    x: 5.4, y: 1.7, w: 3.75, h: 0.35,
    fontSize: 13, bold: true, color: C.primary, margin: 0
  });
  slide.addText([
    { text: "Geometric Proximity vs. Color Penalty:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "A standard TSP solver untangles lines in Euclidean space. In pixel art, nearest neighbors are often alternating colors.", options: { fontSize: 10, breakLine: true } },
    { text: "The Disastrous Trade-Off:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Saving 0.41 units of fabric travel while triggering a color switch incurs a mandatory C_trim penalty of +10.0!", options: { fontSize: 10, breakLine: true } },
    { text: "Why This Matters for AI:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Standard spatial heuristics cannot solve counted needlework without explicit color-aware multi-objective modeling.", options: { fontSize: 10 } }
  ], { x: 5.4, y: 2.15, w: 3.75, h: 2.7, bullet: true, paraSpaceAfter: 8, margin: 0 });

  slide.addNotes("This slide shows the Checkerboard Trap. On an 8-stitch alternating pattern, 2-Opt TSP and Greedy switched colors 7 times, costing 70 thread units. Color-aware algorithms grouped each color and cost only 18.48 units. That is a 73.6% savings. Pure spatial TSP fails on multi-color art.");
}


// ===========================================================================
// SLIDE 6: Tier 1 Validation & The Exponential Wall of A*
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("KEY EMPIRICAL FINDING 2", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.primary, charSpacing: 1.5, margin: 0
  });
  slide.addText("Tier 1 Ground Truth & The Exponential Wall of A*", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Left: Table / Data of A* Ground Truth
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 1.45, w: 4.6, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("Tier 1 Exact Optimality Gaps (N <= 15)", {
    x: 0.85, y: 1.65, w: 4.1, h: 0.3,
    fontSize: 12, bold: true, color: C.textDark, margin: 0
  });
  slide.addText([
    { text: "heart_10 (N=10): ", options: { bold: true, fontSize: 10 } },
    { text: "A* Opt J* = 20.07 | SA Gap: 0.00% | GA Gap: 0.00%\n", options: { fontSize: 10 } },
    { text: "cross_12 (N=12): ", options: { bold: true, fontSize: 10 } },
    { text: "A* Opt J* = 21.24 | SA Gap: 0.00% | GA Gap: 0.00%\n", options: { fontSize: 10 } },
    { text: "checker_8 (N=8): ", options: { bold: true, fontSize: 10 } },
    { text: "A* Opt J* = 18.48 | SA Gap: 0.00% | GA Gap: 0.00%\n", options: { fontSize: 10 } },
    { text: "letter_a_14 (N=14): ", options: { bold: true, fontSize: 10 } },
    { text: "A* Opt J* = 22.83 | SA Gap: 0.00% | GA Gap: 0.00%\n", options: { fontSize: 10 } },
    { text: "smiley_13 (N=13): ", options: { bold: true, fontSize: 10 } },
    { text: "A* Opt J* = 23.83 | SA Gap: 0.00% | GA Gap: 0.00%\n", options: { fontSize: 10 } },
    { text: "Key Takeaway: ", options: { bold: true, color: C.accentEmerald, fontSize: 10 } },
    { text: "Metaheuristics achieved 0.00% error across all 10 random seeds on micro-benchmarks.", options: { fontSize: 10, color: C.accentEmerald, bold: true } }
  ], { x: 0.85, y: 2.05, w: 4.1, h: 2.8, margin: 0 });

  // Right: Embedded Scalability Plot Image
  slide.addImage({
    path: IMG_SCALE,
    x: 5.4, y: 1.45, w: 4.0, h: 3.1
  });
  slide.addText("Figure: Runtime vs Pattern Size N. Note A* exponential wall at N=15 (14,746 nodes) vs polynomial scaling of SA & GA.", {
    x: 5.4, y: 4.65, w: 4.0, h: 0.45,
    fontSize: 8.5, color: C.textMuted, margin: 0
  });

  slide.addNotes("On this slide, we prove two key theorems. First: SA and GA achieved an exact 0.00% Optimality Gap on all Tier 1 micro-patterns. Second: look at the plot on the right. At N=15, A* exploded to 14,746 node expansions in 0.64 seconds, while SA and GA scale up to N=170 in just a few seconds.");
}


// ===========================================================================
// SLIDE 7: Macro-Scale Performance & Pareto Trade-Off
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("KEY EMPIRICAL FINDING 3", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.primary, charSpacing: 1.5, margin: 0
  });
  slide.addText("Pareto Trade-Off Frontier on Real Sprites", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Left: Embedded Pareto Plot
  slide.addImage({
    path: IMG_PARETO,
    x: 0.6, y: 1.45, w: 4.3, h: 3.5
  });

  // Right: Text explanation of Pareto Dominance
  slide.addShape(pres.ShapeType.rect, {
    x: 5.15, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.cardBorder, width: 1 }
  });
  slide.addText("Analysis of the Pareto Frontier", {
    x: 5.4, y: 1.7, w: 3.75, h: 0.35,
    fontSize: 13, bold: true, color: C.primary, margin: 0
  });
  slide.addText([
    { text: "Strict Dominance over Baselines:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "SA and GA establish the lower-left Pareto frontier across all values of C_trim in [1, 50].", options: { fontSize: 10, breakLine: true } },
    { text: "Beating Conventional Crafters (+9.16%):", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "On sprite_flower (N=116), SA reduced thread consumption from 197.45 down to 179.36 thread units.", options: { fontSize: 10, breakLine: true } },
    { text: "Tuning the Objective:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Crafters can dial in their preferred trade-off: prioritize physical thread savings (SA) or minimize manual re-threading stops (GA).", options: { fontSize: 10 } }
  ], { x: 5.4, y: 2.15, w: 3.75, h: 2.7, bullet: true, paraSpaceAfter: 8, margin: 0 });

  slide.addNotes("On this slide, we show the empirical Pareto Frontier. Notice how Simulated Annealing and Genetic Algorithms form the lower-left frontier. When C_trim is 10, SA beats Baseline 2 by 9.16%, saving over 18 units of thread without excessive color switches.");
}


// ===========================================================================
// SLIDE 8: Visual Demonstration Showcase
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("VISUAL DEMONSTRATION", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.primary, charSpacing: 1.5, margin: 0
  });
  slide.addText("Visual Trajectory Showcase: sprite_flower (N=116)", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Center: Large 4-panel comparison image
  slide.addImage({
    path: IMG_SHOWCASE,
    x: 0.6, y: 1.35, w: 8.8, h: 3.8
  });

  slide.addNotes("Here is the visual proof. Look at the top-left: Baseline 1 (Raster) is chaotic with 36 color changes. Top-right: 2-Opt TSP creates clean geometry but cuts across colors 34 times. Bottom-left: Baseline 2 is rigid with 3 color switches. Bottom-right: Simulated Annealing finds continuous loops within colors, shaving thread cost down to 179.3.");
}


// ===========================================================================
// SLIDE 9: Critical Academic Evaluation & "Color Barrier Trap"
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgLight };

  slide.addText("CRITICAL EVALUATION & RESEARCH REFLECTION", {
    x: 0.6, y: 0.4, w: 8.8, h: 0.25,
    fontSize: 10, bold: true, color: C.accentAmber, charSpacing: 1.5, margin: 0
  });
  slide.addText("Honest Analysis: Successes vs. Real Limitations", {
    x: 0.6, y: 0.7, w: 8.8, h: 0.55,
    fontSize: 22, bold: true, color: C.textDark, margin: 0
  });

  // Left Card: What Succeeded
  slide.addShape(pres.ShapeType.rect, {
    x: 0.6, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.accentEmerald, width: 1.5 }
  });
  slide.addText("What Worked (Validated Successes)", {
    x: 0.85, y: 1.7, w: 3.75, h: 0.35,
    fontSize: 13, bold: true, color: C.accentEmerald, margin: 0
  });
  slide.addText([
    { text: "Metric Formulation:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Two-Tier Action Space prevented dead ends and enabled clean bi-objective evaluation.", options: { fontSize: 10, breakLine: true } },
    { text: "Exact Micro Solvability:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "A* with admissible heuristic established guaranteed ground truth; SA/GA achieved 0.00% gap.", options: { fontSize: 10, breakLine: true } },
    { text: "Pareto Dominance:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "SA & GA strictly dominated all 4 standard baselines on multi-color pixel art.", options: { fontSize: 10 } }
  ], { x: 0.85, y: 2.15, w: 3.75, h: 2.7, bullet: true, paraSpaceAfter: 8, margin: 0 });

  // Right Card: Limitations & The Color Barrier
  slide.addShape(pres.ShapeType.rect, {
    x: 5.15, y: 1.45, w: 4.25, h: 3.65,
    fill: { color: C.cardBg }, line: { color: C.accentRose, width: 1.5 }
  });
  slide.addText("Real Limitations & The 'Color Barrier'", {
    x: 5.4, y: 1.7, w: 3.75, h: 0.35,
    fontSize: 13, bold: true, color: C.accentRose, margin: 0
  });
  slide.addText([
    { text: "The 'Color Barrier Trap':", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Seeding SA exclusively with Baseline 2 traps it in local optima because C_trim=10 heavily penalizes crossing color boundaries.", options: { fontSize: 10, breakLine: true } },
    { text: "The Random Restart Solution:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Starting SA from random broke the barrier on sprite_shield (finding 292.46 vs 294.37).", options: { fontSize: 10, breakLine: true } },
    { text: "Physical Craft Abstraction:", options: { bold: true, fontSize: 11, breakLine: true } },
    { text: "Our model optimizes stitch centers (x,y); entry/exit hole orientations are left for CAD compilers.", options: { fontSize: 10 } }
  ], { x: 5.4, y: 2.15, w: 3.75, h: 2.7, bullet: true, paraSpaceAfter: 8, margin: 0 });

  slide.addNotes("To be completely honest and transparent: on sprite_shield, SA initially tied Baseline 2 at 294.37. Why? Because when you switch colors, C_trim is 10. Random 2-opt swaps hesitate to break color boundaries. But when we initialized SA from random, it broke free and found 292.46. This shows the importance of color-aware operators.");
}


// ===========================================================================
// SLIDE 10: Conclusion & Direct Answer to Research Question (Dark Theme)
// ===========================================================================
{
  const slide = pres.addSlide();
  slide.background = { color: C.bgDark };

  slide.addText("CONCLUSION & DEFENSE SUMMARY", {
    x: 0.8, y: 0.6, w: 8.4, h: 0.3,
    fontSize: 11, bold: true, color: "93C5FD", charSpacing: 2, margin: 0
  });
  slide.addText("Final Answer to the Research Question", {
    x: 0.8, y: 0.95, w: 8.4, h: 0.6,
    fontSize: 26, bold: true, color: C.textLight, margin: 0
  });

  // 3 Key Takeaways in horizontal cards
  const cardW = 2.65;
  const gap = 0.22;
  const topY = 1.75;
  const cardH = 2.7;

  // Takeaway 1
  slide.addShape(pres.ShapeType.rect, {
    x: 0.8, y: topY, w: cardW, h: cardH,
    fill: { color: "1E293B" }, line: { color: "3B82F6", width: 1.5 }
  });
  slide.addText("1. A* Exact Search", {
    x: 0.95, y: topY + 0.2, w: cardW - 0.3, h: 0.3,
    fontSize: 13, bold: true, color: "93C5FD", margin: 0
  });
  slide.addText("Guarantees 100% mathematical optimality on N <= 15 with our admissible MST+trim heuristic.\n\nStrictly bounded by O(b^d) memory wall — serves as the gold-standard benchmark, not a production solver.", {
    x: 0.95, y: topY + 0.6, w: cardW - 0.3, h: 1.9,
    fontSize: 10, color: "CBD5E1", margin: 0
  });

  // Takeaway 2
  slide.addShape(pres.ShapeType.rect, {
    x: 0.8 + cardW + gap, y: topY, w: cardW, h: cardH,
    fill: { color: "1E293B" }, line: { color: "10B981", width: 1.5 }
  });
  slide.addText("2. Simulated Annealing", {
    x: 0.8 + cardW + gap + 0.15, y: topY + 0.2, w: cardW - 0.3, h: 0.3,
    fontSize: 13, bold: true, color: "6EE7B7", margin: 0
  });
  slide.addText("Best overall thread-saving optimizer (+9.16% thread reduction over human baselines).\n\nUtilizes color-block shifts and stochastic acceptance to discover non-intuitive embroidery loops in ~4 seconds.", {
    x: 0.8 + cardW + gap + 0.15, y: topY + 0.6, w: cardW - 0.3, h: 1.9,
    fontSize: 10, color: "CBD5E1", margin: 0
  });

  // Takeaway 3
  slide.addShape(pres.ShapeType.rect, {
    x: 0.8 + 2 * (cardW + gap), y: topY, w: cardW, h: cardH,
    fill: { color: "1E293B" }, line: { color: "F59E0B", width: 1.5 }
  });
  slide.addText("3. Genetic Algorithm", {
    x: 0.8 + 2 * (cardW + gap) + 0.15, y: topY + 0.2, w: cardW - 0.3, h: 0.3,
    fontSize: 13, bold: true, color: "FCD34D", margin: 0
  });
  slide.addText("Fastest interactive solver (solves N=170 in < 0.8 seconds).\n\nOrder Crossover (OX1) maintains robust color clustering, making it ideal for desktop design software plugins (e.g. Ink/Stitch).", {
    x: 0.8 + 2 * (cardW + gap) + 0.15, y: topY + 0.6, w: cardW - 0.3, h: 1.9,
    fontSize: 10, color: "CBD5E1", margin: 0
  });

  // Footer Note
  slide.addText("MCCPO Research Project — Code, benchmarks, and data archived at github.com/punnaphot/mccpo", {
    x: 0.8, y: 4.75, w: 8.4, h: 0.35,
    fontSize: 10, color: "64748B", align: "center", margin: 0
  });

  slide.addNotes("To conclude: A* provides our mathematical verification on micro motifs. Simulated Annealing is the best commercial solver when maximum thread savings are required. Genetic Algorithm provides real-time sub-second execution ideal for desktop CAD software. Thank you, and we welcome any questions.");
}

// ---------------------------------------------------------------------------
// Save Presentation Deck
// ---------------------------------------------------------------------------
const OUTPUT_PPTX = path.join(path.dirname(BASE_DIR), "MCCPO_Final_Defense_Presentation.pptx");

pres.writeFile({ fileName: OUTPUT_PPTX })
  .then(() => {
    console.log(`Presentation successfully created at: ${OUTPUT_PPTX}`);
  })
  .catch((err) => {
    console.error("Error creating presentation:", err);
    process.exit(1);
  });
