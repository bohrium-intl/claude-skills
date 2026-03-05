#!/usr/bin/env python3
"""
SciencePedia Word Card Generator

Generates word card images with category-matched abstract illustrations.
Each card includes: title, explanation, illustration, QR code, short URL, branding.

Usage:
    python generate_wordcard.py <url_or_keyword> [--style dark|light|gradient] [--utm SOURCE]
    python generate_wordcard.py "monte_carlo_simulation" --style dark --utm twitter
    echo -e "fourier_transform\ngraph_neural_network" | python generate_wordcard.py --batch

The illustration is auto-selected based on keyword category. Override with --illust <type>.
Types: scatter, wave, network, hexgrid, orbit, field, spiral, dots (or 'none')
"""

import subprocess, sys, os, textwrap, argparse, re, math, random, json, html

def ensure_deps():
    for pkg, mod in [("qrcode", "qrcode"), ("Pillow", "PIL")]:
        try:
            __import__(mod)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

ensure_deps()

import qrcode
from PIL import Image, ImageDraw, ImageFont

# ── Config ─────────────────────────────────────────────────
BASE_URL = "https://www.bohrium.com/en/sciencepedia/feynman/keyword"
CARD_W, CARD_H = 1560, 960  # 紧凑高清尺寸
QR_SIZE = 210
PAD = 96
BRAND = "SciencePedia  ·  Bohrium"

STYLES = {
    "light": {  # Default — matches Bohrium website (white bg, indigo accents)
        "bg": (255, 255, 255), "title": (25, 25, 38), "text": (65, 68, 90),  # 加深对比
        "accent": (74, 78, 181), "brand": (120, 120, 150), "url": (74, 78, 181),
        "divider": (210, 212, 230), "qr_fill": (59, 63, 140), "qr_bg": (248, 248, 253),
        "illust": (74, 78, 181), "illust_dim": (170, 172, 215),
        "sep": (220, 220, 235), "illust_panel": (240, 241, 250),  # 原版风格分隔线
    },
    "dark": {  # Deep indigo dark mode
        "bg": (20, 20, 35), "title": (255, 255, 255), "text": (180, 182, 220),
        "accent": (74, 78, 181), "brand": (80, 80, 110), "url": (100, 105, 200),
        "divider": (45, 45, 65), "qr_fill": (59, 63, 140), "qr_bg": (255, 255, 255),
        "illust": (100, 105, 200), "illust_dim": (180, 182, 220),
        "sep": (40, 40, 55), "illust_panel": None,
    },
    "gradient": {  # Indigo gradient — eye-catching for standalone posts
        "bg": None, "title": (255, 255, 255), "text": (210, 210, 235),
        "accent": (180, 182, 220), "brand": (150, 150, 185), "url": (180, 182, 220),
        "divider": (255, 255, 255, 40), "qr_fill": (59, 63, 140), "qr_bg": (255, 255, 255),
        "illust": (180, 182, 220), "illust_dim": (100, 100, 140),
        "sep": (255, 255, 255, 25), "illust_panel": None,
    },
}

# ── Keyword → Illustration Category Mapping ────────────────
CATEGORY_KEYWORDS = {
    # ── Original 15 ──
    "scatter": ["monte_carlo", "random", "sampling", "stochastic", "probability",
                "bayesian", "markov", "noise", "statistical", "regression"],
    "wave": ["fourier", "wave", "frequency", "spectral", "harmonic",
             "acoustic", "sound"],
    "network": ["graph", "neural", "network", "deep_learning", "machine_learning",
                "transformer", "attention", "convolution", "gnn", "reinforcement",
                "clustering", "classification", "perceptron"],
    "hexgrid": ["density_functional", "solid_state",
                "material", "polymer", "molecular_dynamic",
                "periodic_table", "alloy", "semiconductor", "catalyst"],
    "orbit": ["quantum", "schrodinger", "electron", "orbital", "atom",
              "photon", "spin", "entangle", "superposition", "bohr"],
    "field": ["gradient_field", "potential", "force_field", "vector_field"],
    "spiral": ["dna", "double_helix", "phylogen", "genome"],
    "dots": ["thermodynamic", "temperature", "pressure",
             "kinetic_theory", "equilibrium", "phase_transition"],
    "bifurcation": ["chaos", "logistic", "lyapunov", "bifurcat", "attractor",
                    "nonlinear", "dynamical_system", "lorenz", "strange"],
    "flow": ["fluid", "navier", "turbulen", "laminar", "viscosi", "reynolds",
             "aerodynamic", "hydrodynamic", "compressib"],
    "distribution": ["distribut", "gaussian", "normal_distribut", "central_limit",
                     "variance", "standard_deviation", "histogram", "poisson",
                     "chi_square", "hypothesis_test"],
    "tree": ["decision_tree", "random_forest", "xgboost", "boosting", "bagging",
             "dendrogram"],
    "matrix": ["matrix", "linear_algebra", "eigenvalue", "eigenvector", "singular_value",
               "determinant", "vector_space", "linear_transform", "pca",
               "dimensionality_reduction"],
    "pendulum": ["classical_mechanic", "newton", "lagrangian", "hamiltonian",
                 "pendulum", "rigid_body", "kepler", "celestial", "phase_space"],
    "contour": ["optimi", "gradient_descent", "loss_function", "backpropagat",
                "learning_rate", "convergence", "convex", "stochastic_gradient",
                "adam_optimizer", "cost_function"],
    # ── New 35 ──
    "helix": ["protein_fold", "amino_acid", "helix", "coil", "spring_const",
              "alpha_helix", "beta_sheet", "prion", "collagen"],
    "circuit": ["circuit", "logic_gate", "transistor", "resistor", "capacitor",
                "amplifier", "digital", "boolean", "cpu", "vlsi", "fpga"],
    "layers": ["stratigraphy", "sediment", "geological", "atmosphere", "layer",
               "crust", "mantle", "lithosphere", "neural_network_layer", "stack"],
    "fractal": ["fractal", "mandelbrot", "julia_set", "self_similar", "recursion",
                "recursive", "branching", "fern", "sierpinski", "cantor"],
    "cycle": ["cycle", "krebs", "carbon_cycle", "water_cycle", "nitrogen_cycle",
              "feedback", "loop", "circadian", "cell_cycle", "catalytic_cycle"],
    "spectrum": ["spectrum", "spectroscop", "emission", "absorption",
                 "infrared", "ultraviolet", "raman", "chromatograph"],
    "lattice": ["lattice", "crystal", "bravais", "unit_cell", "reciprocal",
                "phonon", "brillouin"],
    "topology": ["topology", "topological", "manifold", "homeomorphism",
                 "euler_characteristic", "genus", "homotopy", "betti"],
    "constellation": ["star", "galaxy", "cosmic", "astrono", "celestial",
                      "pulsar", "quasar", "nebula", "supernova", "redshift"],
    "lens": ["lens", "refract", "optic", "microscop", "telescop",
             "focal", "aperture", "diffract", "holograph"],
    "membrane": ["membrane", "cell_membrane", "lipid", "osmosis", "permeable",
                 "vesicle", "endocytosis", "ion_channel", "bilayer"],
    "gear": ["gear", "mechanism", "mechanical", "torque", "rotation",
             "engine", "turbine", "lever", "pulley", "machine"],
    "venn": ["set_theory", "venn", "intersection", "union", "boolean_algebra",
             "logic", "predicate", "proposition", "syllogism"],
    "axis": ["function", "calculus", "derivat", "integral", "coordinate",
             "cartesian", "parametric", "plot", "graph_theory"],
    "hierarchy": ["taxonom", "hierarch", "classif", "ontology", "pyramid",
                  "maslow", "food_chain", "trophic", "clade", "kingdom"],
    "radioactive": ["radioact", "decay", "half_life", "isotope", "nuclear",
                    "fission", "fusion", "alpha_particle", "beta_decay",
                    "gamma_ray", "uranium", "plutonium"],
    "electrode": ["electrochem", "electrode", "capacitor", "battery", "anode",
                  "cathode", "electrolysis", "galvanic", "voltaic"],
    "spring": ["spring", "elastic", "hooke", "harmonic_oscillator", "vibrat",
               "resonanc", "damping", "oscillat"],
    "prism": ["prism", "dispers", "refract", "rainbow", "snell",
              "brewster", "polariz"],
    "interference": ["interferen", "diffract", "double_slit", "young",
                     "fresnel", "fraunhofer", "coherence"],
    "diffusion": ["diffusion", "osmosis", "brownian", "fick", "concentrat",
                  "permeab", "transport_phenom", "entropy", "energy"],
    "bond": ["chemical_bond", "covalent", "ionic", "metallic_bond",
             "molecular", "lewis", "valence", "hybridization", "vsepr"],
    "oscillator": ["damped", "underdamp", "overdamp", "reson", "ringing",
                   "lrc", "rlc", "anharmonic"],
    "parabola": ["projectile", "parabola", "trajectory", "ballistic",
                 "kinematics", "freefall", "launch"],
    "tessellation": ["tessellat", "tiling", "penrose", "symmetry_group",
                     "wallpaper_group", "aperiodic"],
    "pipeline": ["pipeline", "workflow", "etl", "data_flow", "dag",
                 "compiler", "scheduler", "mapreduce"],
    "crosssection": ["cross_section", "anatomy", "tomograph", "ct_scan",
                     "mri", "earth_interior", "core", "shell_model"],
    "dipole": ["dipole", "magnet", "electrostatic", "charge", "coulomb",
               "electric_field", "magnetic_field", "maxwell", "gauss_law"],
    "pulse": ["pulse", "impulse", "spike", "ecg", "eeg", "action_potential",
              "neuron_firing", "signal_processing", "defibrillat"],
    "bridge": ["bridge", "truss", "structural", "beam", "cantilever",
               "civil_engineer", "architect", "load", "stress_strain"],
    "polar": ["polar_coordin", "rose_curve", "cardioid", "lemniscate",
              "limacon", "radar_chart", "antenna_pattern"],
    "knot": ["knot_theory", "topological_knot", "braid", "link",
             "jones_polynomial", "trefoil"],
    "cascade": ["cascade", "waterfall", "sequential", "chain_reaction",
                "domino", "signaling_pathway", "phosphorylation"],
    "symmetry": ["symmetry", "group_theory", "isometry", "reflection",
                 "rotation_group", "crystallograph", "point_group",
                 "space_group", "kaleidoscope"],
    "cloud": ["cloud", "probabilit", "wavefunction", "orbital_cloud",
              "electron_cloud", "uncertainty", "heisenberg", "fuzzy"],
}


def guess_category(slug):
    slug_lower = slug.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in slug_lower:
                return cat
    return "dots"  # default fallback


# ── Font Helper (支持字体层级) ─────────────────────────────────
_SKILL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")
FONT_PATHS = {
    "title": [  # Plus Jakarta Sans Bold — 品牌字体，标题用
        os.path.join(_SKILL_DIR, "PlusJakartaSans-Bold.ttf"),
        os.path.expanduser("~/Library/Fonts/PlusJakartaSans-Bold.ttf"),
        "/Library/Fonts/PlusJakartaSans-Bold.ttf",
        # 备选
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "body": [  # Plus Jakarta Sans Regular — 品牌字体，正文用
        os.path.join(_SKILL_DIR, "PlusJakartaSans-Regular.ttf"),
        os.path.expanduser("~/Library/Fonts/PlusJakartaSans-Regular.ttf"),
        "/Library/Fonts/PlusJakartaSans-Regular.ttf",
        # 备选
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "mono": [  # 等宽字体 — URL用，技术感
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
}

def _font(size, role="body"):
    """role: 'title' | 'body' | 'mono'"""
    paths = FONT_PATHS.get(role, FONT_PATHS["body"])
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _rounded_rect(draw, xy, r, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    for cx, cy, sa, ea in [
        (x0, y0, 180, 270), (x1 - 2 * r, y0, 270, 360),
        (x0, y1 - 2 * r, 90, 180), (x1 - 2 * r, y1 - 2 * r, 0, 90),
    ]:
        draw.pieslice([cx, cy, cx + 2 * r, cy + 2 * r], sa, ea, fill=fill)


# ── Smart Truncate (改动 3) ─────────────────────────────────
def smart_truncate(text, wrap_width, max_lines):
    """Truncate text at sentence/clause boundaries when it exceeds max_lines."""
    lines = textwrap.wrap(text, width=wrap_width)
    if len(lines) <= max_lines:
        return lines
    # Text is too long — find a good cut point
    merged = " ".join(lines[:max_lines])
    min_pos = len(merged) // 2  # don't cut before 50%
    # Try sentence boundary first
    cut = merged.rfind(". ", min_pos)
    if cut != -1:
        return textwrap.wrap(merged[:cut + 1] + "...", width=wrap_width)
    # Try comma boundary
    cut = merged.rfind(", ", min_pos)
    if cut != -1:
        return textwrap.wrap(merged[:cut + 1] + "...", width=wrap_width)
    # Fall back to word boundary
    cut = merged.rfind(" ", min_pos)
    if cut != -1:
        return textwrap.wrap(merged[:cut] + "...", width=wrap_width)
    return textwrap.wrap(merged + "...", width=wrap_width)


# ── Illustration Drawing Functions ──────────────────────────
def _draw_scatter(draw, cx, cy, sz, c1, c2, seed=0):
    """Monte Carlo: random dots inside/outside quarter circle."""
    rng = random.Random(42 + seed)
    r = sz // 2
    for _ in range(160):
        px, py = rng.uniform(-1, 1), rng.uniform(-1, 1)
        inside = (px ** 2 + py ** 2) <= 1.0
        color = (*c1, 200) if inside else (*c2, 120)
        sx, sy = cx + int(px * r), cy + int(py * r)
        draw.ellipse([(sx - 5, sy - 5), (sx + 5, sy + 5)], fill=color)
    prev = None
    for a in range(91):
        rad = math.radians(a)
        pt = (cx - r + int(sz * math.cos(rad)), cy + r - int(sz * math.sin(rad)))
        if prev:
            draw.line([prev, pt], fill=(*c1, 100), width=3)
        prev = pt


def _draw_wave(draw, cx, cy, sz, c1, c2, seed=0):
    """Fourier: overlapping sine waves."""
    rng = random.Random(42 + seed)
    r = sz // 2
    for wi in range(3):
        freq, amp = 2 + wi * 1.5, r * (0.6 - wi * 0.15)
        alpha = 220 - wi * 50
        color = (c1[0] + wi * 30, c1[1], c1[2], alpha)
        phase = wi * 0.8 + rng.uniform(-0.3, 0.3)
        pts = [(cx - r + int(t / 99 * sz), cy + int(amp * math.sin(freq * math.pi * t / 99 + phase)))
               for t in range(100)]
        for j in range(1, len(pts)):
            draw.line([pts[j - 1], pts[j]], fill=color, width=3)


def _draw_network(draw, cx, cy, sz, c1, c2, seed=0):
    """Graph: nodes and edges."""
    rng = random.Random(77 + seed)
    r = sz // 2
    nodes = [(cx + int(rng.uniform(0.2, 0.9) * r * math.cos(a)),
              cy + int(rng.uniform(0.2, 0.9) * r * math.sin(a)))
             for a in [rng.uniform(0, 2 * math.pi) for _ in range(12)]]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            d = math.dist(nodes[i], nodes[j])
            if d < r * 0.8:
                draw.line([nodes[i], nodes[j]], fill=(*c1, max(30, int(120 - d))), width=2)
    for nx, ny in nodes:
        draw.ellipse([(nx - 7, ny - 7), (nx + 7, ny + 7)], fill=(*c1, 200))
        draw.ellipse([(nx - 4, ny - 4), (nx + 4, ny + 4)], fill=(min(c1[0] + 80, 255), min(c1[1] + 60, 255), 255, 255))


def _draw_hexgrid(draw, cx, cy, sz, c1, c2, seed=0):
    """Molecular: hexagonal lattice."""
    r, hr = sz // 2, 18
    rng = random.Random(42 + seed)
    offset_x = rng.randint(-5, 5)
    offset_y = rng.randint(-5, 5)
    for row in range(-4, 5):
        for col in range(-3, 4):
            hx = cx + int(col * hr * 1.75) + offset_x
            hy = cy + int(row * hr * 1.5) + (hr if col % 2 else 0) + offset_y
            dist = math.dist((hx, hy), (cx, cy))
            if dist > r * 1.1:
                continue
            alpha = max(50, int(190 - dist * 0.8))
            pts = [(hx + int(hr * 0.8 * math.cos(math.radians(60 * i + 30))),
                    hy + int(hr * 0.8 * math.sin(math.radians(60 * i + 30)))) for i in range(6)]
            for i in range(6):
                draw.line([pts[i], pts[(i + 1) % 6]], fill=(*c1, alpha), width=2)


def _draw_orbit(draw, cx, cy, sz, c1, c2, seed=0):
    """Atomic: concentric elliptical orbits."""
    rng = random.Random(33 + seed)
    r = sz // 2
    for i in range(3):
        orb_r = int(r * (0.35 + i * 0.25))
        tilt = 15 + i * 20
        bbox = [cx - orb_r, cy - orb_r // 2 - tilt + i * 12, cx + orb_r, cy + orb_r // 2 - tilt + i * 12]
        draw.ellipse(bbox, outline=(*c1, 60 + i * 20), width=2)
        a = rng.uniform(0, 2 * math.pi)
        ex, ey = cx + int(orb_r * math.cos(a)), cy - tilt + i * 12 + int(orb_r // 2 * math.sin(a))
        draw.ellipse([(ex - 7, ey - 7), (ex + 7, ey + 7)], fill=(*c1, 220))
    draw.ellipse([(cx - 9, cy - 9), (cx + 9, cy + 9)], fill=(*c1, 200))


def _draw_field(draw, cx, cy, sz, c1, c2, seed=0):
    """Vector field: arrows showing force directions."""
    rng = random.Random(42 + seed)
    r = sz // 2
    step = 28
    angle_offset = rng.uniform(0, 0.5)
    for gx in range(-4, 5):
        for gy in range(-4, 5):
            px, py = cx + gx * step, cy + gy * step
            if math.dist((px, py), (cx, cy)) > r:
                continue
            dx, dy = -(py - cy), (px - cx)
            mag = max(math.sqrt(dx * dx + dy * dy), 1)
            dx, dy = dx / mag * 10, dy / mag * 10
            dist = math.dist((px, py), (cx, cy))
            alpha = max(60, int(180 - dist * 0.7))
            draw.line([(px, py), (px + dx, py + dy)], fill=(*c1, alpha), width=2)
            draw.ellipse([(px + dx - 3, py + dy - 3), (px + dx + 3, py + dy + 3)], fill=(*c1, alpha))


def _draw_spiral(draw, cx, cy, sz, c1, c2, seed=0):
    """DNA-like double helix spiral."""
    rng = random.Random(42 + seed)
    r = sz // 2
    phase = rng.uniform(0, math.pi)
    prev1, prev2 = None, None
    for t in range(200):
        frac = t / 199
        y = cy - r + int(frac * sz)
        x1 = cx + int(30 * math.sin(frac * 6 * math.pi + phase))
        x2 = cx - int(30 * math.sin(frac * 6 * math.pi + phase))
        alpha = int(80 + 100 * abs(math.sin(frac * 6 * math.pi + phase)))
        if prev1:
            draw.line([prev1, (x1, y)], fill=(*c1, alpha), width=3)
            draw.line([prev2, (x2, y)], fill=(*c1, max(40, alpha - 60)), width=3)
        if t % 12 == 0:
            draw.line([(x1, y), (x2, y)], fill=(*c2, 50), width=2)
        prev1, prev2 = (x1, y), (x2, y)


def _draw_dots(draw, cx, cy, sz, c1, c2, seed=0):
    """Particle cloud with varying density (thermodynamics)."""
    rng = random.Random(55 + seed)
    r = sz // 2
    for _ in range(120):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.gauss(0, r * 0.4)
        px, py = cx + int(d * math.cos(a)), cy + int(d * math.sin(a))
        dist = math.dist((px, py), (cx, cy))
        if dist > r:
            continue
        size = rng.uniform(3, 7)
        alpha = max(70, int(220 - dist * 0.8))
        draw.ellipse([(px - size, py - size), (px + size, py + size)], fill=(*c1, alpha))


def _draw_bifurcation(draw, cx, cy, sz, c1, c2, seed=0):
    """Chaos theory: logistic map bifurcation diagram."""
    rng = random.Random(42 + seed)
    r = sz // 2
    x0, y0 = cx - r, cy - r
    init_x = 0.5 + rng.uniform(-0.1, 0.1)
    for i in range(300):
        r_val = 2.5 + 1.5 * (i / 299)
        x = init_x
        for _ in range(50):
            x = r_val * x * (1 - x)
        for _ in range(40):
            x = r_val * x * (1 - x)
            px = x0 + int((i / 299) * sz)
            py = cy + r - int(x * sz)
            draw.point((px, py), fill=(*c1, rng.randint(100, 220)))


def _draw_flow(draw, cx, cy, sz, c1, c2, seed=0):
    """Fluid dynamics: flow field streamlines."""
    rng = random.Random(88 + seed)
    r = sz // 2
    for _ in range(25):
        px = cx + rng.uniform(-r * 0.8, r * 0.8)
        py = cy + rng.uniform(-r * 0.8, r * 0.8)
        pts = [(px, py)]
        for _ in range(30):
            angle = math.sin(px * 0.03) * 2 + math.cos(py * 0.025) * 2.5
            px += math.cos(angle) * 4
            py += math.sin(angle) * 4
            if math.dist((px, py), (cx, cy)) > r:
                break
            pts.append((px, py))
        if len(pts) > 2:
            alpha = rng.randint(90, 180)
            for j in range(1, len(pts)):
                draw.line([pts[j - 1], pts[j]], fill=(*c1, alpha), width=2)


def _draw_distribution(draw, cx, cy, sz, c1, c2, seed=0):
    """Statistics: bell curve with histogram bars."""
    r = sz // 2
    rng = random.Random(66 + seed)
    n_bars = 20
    bar_w = sz // n_bars
    counts = [0] * n_bars
    for _ in range(800):
        v = rng.gauss(0.5, 0.15)
        idx = int(v * n_bars)
        if 0 <= idx < n_bars:
            counts[idx] += 1
    max_c = max(counts)
    for i, c in enumerate(counts):
        h = int((c / max_c) * r * 0.85)
        bx = cx - r + i * bar_w
        alpha = int(70 + 110 * (c / max_c))
        draw.rectangle([(bx + 1, cy + r // 2 - h), (bx + bar_w - 1, cy + r // 2)], fill=(*c1, alpha))
    pts = []
    for i in range(100):
        t = i / 99
        x = cx - r + t * sz
        gauss_y = math.exp(-0.5 * ((t - 0.5) / 0.15) ** 2)
        y = cy + r // 2 - int(gauss_y * r * 0.85)
        pts.append((x, y))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 230), width=3)


def _draw_tree(draw, cx, cy, sz, c1, c2, seed=0):
    """Decision tree / recursive branching."""
    def branch(x, y, angle, length, depth):
        if depth <= 0 or length < 3:
            return
        ex = x + length * math.cos(angle)
        ey = y - length * math.sin(angle)
        alpha = min(255, 70 + depth * 35)
        draw.line([(x, y), (ex, ey)], fill=(*c1, alpha), width=max(1, depth // 2 + 1))
        spread = 0.45 + random.Random(int(x * 100 + y) + seed).uniform(-0.1, 0.1)
        branch(ex, ey, angle + spread, length * 0.68, depth - 1)
        branch(ex, ey, angle - spread, length * 0.68, depth - 1)
    branch(cx, cy + sz // 3, math.pi / 2, sz * 0.28, 7)


def _draw_matrix(draw, cx, cy, sz, c1, c2, seed=0):
    """Linear algebra: matrix heatmap with brackets."""
    rng = random.Random(99 + seed)
    r = sz // 2
    cell = 32
    rows, cols = 7, 7
    ox = cx - (cols * cell) // 2
    oy = cy - (rows * cell) // 2
    for row in range(rows):
        for col in range(cols):
            val = rng.uniform(0, 1)
            alpha = int(30 + val * 150)
            x, y = ox + col * cell, oy + row * cell
            draw.rectangle([(x + 1, y + 1), (x + cell - 2, y + cell - 2)], fill=(*c1, alpha))
    draw.line([(ox - 6, oy - 4), (ox - 6, oy + rows * cell + 2)], fill=(*c1, 120), width=3)
    draw.line([(ox - 6, oy - 4), (ox + 4, oy - 4)], fill=(*c1, 120), width=3)
    draw.line([(ox - 6, oy + rows * cell + 2), (ox + 4, oy + rows * cell + 2)], fill=(*c1, 120), width=3)
    rx = ox + cols * cell + 4
    draw.line([(rx, oy - 4), (rx, oy + rows * cell + 2)], fill=(*c1, 120), width=3)
    draw.line([(rx, oy - 4), (rx - 10, oy - 4)], fill=(*c1, 120), width=3)
    draw.line([(rx, oy + rows * cell + 2), (rx - 10, oy + rows * cell + 2)], fill=(*c1, 120), width=3)


def _draw_pendulum(draw, cx, cy, sz, c1, c2, seed=0):
    """Classical mechanics: stroboscopic pendulum."""
    rng = random.Random(42 + seed)
    r = sz // 2
    pivot_x, pivot_y = cx, cy - r * 0.55
    rod_len = r * 0.85
    # Pendulum positions (angles in radians, symmetric swing)
    angles = [-0.7, -0.45, -0.2, 0.0, 0.2, 0.45, 0.7]
    phase_offset = rng.uniform(-0.1, 0.1)
    angles = [a + phase_offset for a in angles]
    n = len(angles)
    # Draw pivot point
    draw.ellipse([(pivot_x - 5, pivot_y - 5), (pivot_x + 5, pivot_y + 5)], fill=(*c1, 220))
    # Draw arc trajectory at bottom (dashed)
    arc_pts = []
    for i in range(60):
        a = -0.8 + phase_offset + (1.6 * i / 59)
        ax = pivot_x + rod_len * math.sin(a)
        ay = pivot_y + rod_len * math.cos(a)
        arc_pts.append((ax, ay))
    for j in range(1, len(arc_pts)):
        if (j // 3) % 2 == 0:  # dashed
            draw.line([arc_pts[j - 1], arc_pts[j]], fill=(*c1, 60), width=2)
    # Draw each pendulum position (increasing opacity toward center)
    for idx, angle in enumerate(angles):
        bob_x = pivot_x + rod_len * math.sin(angle)
        bob_y = pivot_y + rod_len * math.cos(angle)
        # Alpha: more opaque near center position
        dist_from_center = abs(idx - n // 2)
        alpha = max(60, 220 - dist_from_center * 50)
        # Rod
        draw.line([(pivot_x, pivot_y), (bob_x, bob_y)], fill=(*c1, alpha), width=2)
        # Bob
        bob_r = 10
        draw.ellipse([(bob_x - bob_r, bob_y - bob_r), (bob_x + bob_r, bob_y + bob_r)],
                     fill=(*c1, alpha))
    # Gravity arrows (small downward arrows on right side)
    for i in range(3):
        gx = cx + r * 0.55
        gy = cy - r * 0.15 + i * 28
        arr_len = 18
        draw.line([(gx, gy), (gx, gy + arr_len)], fill=(*c2, 100), width=2)
        draw.line([(gx - 4, gy + arr_len - 5), (gx, gy + arr_len)], fill=(*c2, 100), width=2)
        draw.line([(gx + 4, gy + arr_len - 5), (gx, gy + arr_len)], fill=(*c2, 100), width=2)


def _draw_contour(draw, cx, cy, sz, c1, c2, seed=0):
    """Optimization: contour lines with gradient descent path."""
    r = sz // 2
    for i in range(6):
        rr = int(r * (0.15 + i * 0.15))
        alpha = max(20, 100 - i * 15)
        tilt = 20
        bbox = [cx - rr, cy - int(rr * 0.6) - tilt, cx + rr, cy + int(rr * 0.6) - tilt]
        draw.ellipse(bbox, outline=(*c1, alpha), width=2)
    rng = random.Random(44 + seed)
    px, py = cx + r * 0.6, cy - r * 0.1
    pts = [(px, py)]
    for _ in range(12):
        dx = -(px - cx) * 0.25 + rng.uniform(-3, 3)
        dy = -(py - (cy - 20)) * 0.25 + rng.uniform(-3, 3)
        px, py = px + dx, py + dy
        pts.append((px, py))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 200), width=3)
        draw.ellipse([(pts[j][0] - 3, pts[j][1] - 3), (pts[j][0] + 3, pts[j][1] + 3)], fill=(*c1, 220))
    draw.ellipse([(cx - 4, cy - 24), (cx + 4, cy - 16)], fill=(*c2, 255))


# ── New Illustration Types (16-50) ─────────────────────────

def _draw_helix(draw, cx, cy, sz, c1, c2, seed=0):
    """Double helix – airy, with depth transparency."""
    rng = random.Random(42 + seed)
    r = sz // 2
    amp = r * 0.38
    n_pts = 200
    prev_a, prev_b = None, None
    for t in range(n_pts):
        frac = t / (n_pts - 1)
        y = cy - r * 0.85 + int(frac * r * 1.7)
        phase = frac * 5.5 * math.pi
        x_a = cx + int(amp * math.sin(phase))
        x_b = cx - int(amp * math.sin(phase))
        depth_a = 0.5 + 0.5 * math.cos(phase)
        depth_b = 1.0 - depth_a
        if prev_a:
            draw.line([prev_a, (x_a, y)], fill=(*c1, int(60 + 120 * depth_a)), width=2)
            draw.line([prev_b, (x_b, y)], fill=(*c1, int(60 + 120 * depth_b)), width=2)
        if t % 12 == 0:
            rung_alpha = int(35 + 50 * min(depth_a, depth_b))
            draw.line([(x_a, y), (x_b, y)], fill=(*c2, rung_alpha), width=1)
            draw.ellipse([(x_a - 3, y - 3), (x_a + 3, y + 3)], fill=(*c1, int(120 * depth_a)))
            draw.ellipse([(x_b - 3, y - 3), (x_b + 3, y + 3)], fill=(*c1, int(120 * depth_b)))
        prev_a, prev_b = (x_a, y), (x_b, y)


def _draw_circuit(draw, cx, cy, sz, c1, c2, seed=0):
    """Circuit diagram: orthogonal paths + nodes."""
    rng = random.Random(71 + seed)
    r = sz // 2
    nodes = []
    for _ in range(8):
        nodes.append((cx + rng.randint(-r + 20, r - 20), cy + rng.randint(-r + 20, r - 20)))
    for i in range(len(nodes)):
        j = (i + 1) % len(nodes)
        x0, y0 = nodes[i]
        x1, y1 = nodes[j]
        mid_x = x1 if rng.random() < 0.5 else x0
        mid_y = y0 if mid_x == x1 else y1
        draw.line([(x0, y0), (mid_x, mid_y)], fill=(*c1, 130), width=2)
        draw.line([(mid_x, mid_y), (x1, y1)], fill=(*c1, 130), width=2)
    for nx, ny in nodes:
        draw.ellipse([(nx - 6, ny - 6), (nx + 6, ny + 6)], fill=(*c1, 200))
        draw.ellipse([(nx - 3, ny - 3), (nx + 3, ny + 3)], fill=(*c2, 180))


def _draw_layers(draw, cx, cy, sz, c1, c2, seed=0):
    """Horizontal strata layers (geology, atmosphere)."""
    rng = random.Random(55 + seed)
    r = sz // 2
    n_layers = 6
    for i in range(n_layers):
        y_base = cy - r + int((i + 0.5) * sz / n_layers)
        alpha = int(40 + 130 * (1 - i / n_layers))
        pts = []
        for t in range(50):
            x = cx - r + int(t / 49 * sz)
            y = y_base + int(rng.gauss(0, 4) + 8 * math.sin(t * 0.15 + i * 1.2))
            pts.append((x, y))
        for j in range(1, len(pts)):
            draw.line([pts[j - 1], pts[j]], fill=(*c1, alpha), width=2)


def _draw_fractal(draw, cx, cy, sz, c1, c2, seed=0):
    """Koch snowflake – light, airy fractal."""
    rng = random.Random(42 + seed)
    r = sz // 2
    _depth_counter = [0]

    def koch(x0, y0, x1, y1, depth):
        if depth == 0:
            # Vary alpha slightly for visual texture
            _depth_counter[0] += 1
            a = 100 + (_depth_counter[0] % 5) * 15
            draw.line([(int(x0), int(y0)), (int(x1), int(y1))],
                      fill=(*c1, a), width=1)
            return
        dx, dy = (x1 - x0) / 3, (y1 - y0) / 3
        ax, ay = x0 + dx, y0 + dy
        bx, by = x0 + 2 * dx, y0 + 2 * dy
        px = (ax + bx) / 2 - (by - ay) * 0.866
        py = (ay + by) / 2 + (bx - ax) * 0.866
        koch(x0, y0, ax, ay, depth - 1)
        koch(ax, ay, px, py, depth - 1)
        koch(px, py, bx, by, depth - 1)
        koch(bx, by, x1, y1, depth - 1)

    scale = r * 0.8
    t1 = (cx - scale, cy + scale * 0.5)
    t2 = (cx + scale, cy + scale * 0.5)
    t3 = (cx, cy - scale * 0.65)
    koch(t1[0], t1[1], t2[0], t2[1], 4)
    koch(t2[0], t2[1], t3[0], t3[1], 4)
    koch(t3[0], t3[1], t1[0], t1[1], 4)


def _draw_cycle(draw, cx, cy, sz, c1, c2, seed=0):
    """Circular arrows / feedback loop."""
    rng = random.Random(33 + seed)
    r_cycle = sz // 2 * 0.55
    n_nodes = rng.choice([3, 4, 5, 6])
    nodes = []
    for i in range(n_nodes):
        a = 2 * math.pi * i / n_nodes - math.pi / 2
        nodes.append((cx + int(r_cycle * math.cos(a)), cy + int(r_cycle * math.sin(a))))
    # Curved arrows between nodes
    for i in range(n_nodes):
        x0, y0 = nodes[i]
        x1, y1 = nodes[(i + 1) % n_nodes]
        # Draw arc
        steps = 20
        for t in range(steps):
            frac = t / steps
            frac2 = (t + 1) / steps
            px = x0 + (x1 - x0) * frac + (cy - (y0 + y1) / 2) * 0.15 * math.sin(frac * math.pi)
            py = y0 + (y1 - y0) * frac - (cx - (x0 + x1) / 2) * 0.15 * math.sin(frac * math.pi)
            px2 = x0 + (x1 - x0) * frac2 + (cy - (y0 + y1) / 2) * 0.15 * math.sin(frac2 * math.pi)
            py2 = y0 + (y1 - y0) * frac2 - (cx - (x0 + x1) / 2) * 0.15 * math.sin(frac2 * math.pi)
            draw.line([(px, py), (px2, py2)], fill=(*c1, 140), width=2)
    for nx, ny in nodes:
        draw.ellipse([(nx - 8, ny - 8), (nx + 8, ny + 8)], fill=(*c1, 180))


def _draw_spectrum(draw, cx, cy, sz, c1, c2, seed=0):
    """Vertical bars / frequency spectrum."""
    rng = random.Random(88 + seed)
    r = sz // 2
    n_bars = 28
    bar_w = int(sz * 0.8 / n_bars)
    for i in range(n_bars):
        x = cx - int(sz * 0.4) + i * bar_w
        h = int(rng.uniform(0.15, 0.85) * r)
        alpha = int(80 + 120 * (h / r))
        draw.rectangle([(x, cy + r * 0.4 - h), (x + bar_w - 2, cy + r * 0.4)], fill=(*c1, alpha))
    # Envelope curve
    pts = []
    for i in range(n_bars):
        x = cx - int(sz * 0.4) + i * bar_w + bar_w // 2
        h = int(rng.uniform(0.15, 0.85) * r)
        pts.append((x, cy + r * 0.4 - h - 5))


def _draw_lattice(draw, cx, cy, sz, c1, c2, seed=0):
    """Square lattice with connections."""
    rng = random.Random(42 + seed)
    r = sz // 2
    step = int(r * 0.33)
    for gx in range(-3, 4):
        for gy in range(-3, 4):
            px, py = cx + gx * step, cy + gy * step
            if math.dist((px, py), (cx, cy)) > r * 0.95:
                continue
            alpha = max(60, int(180 - math.dist((px, py), (cx, cy)) * 0.6))
            draw.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=(*c1, alpha))
            if gx < 3:
                nx = cx + (gx + 1) * step
                if math.dist((nx, py), (cx, cy)) <= r * 0.95:
                    draw.line([(px, py), (nx, py)], fill=(*c1, alpha - 40), width=1)
            if gy < 3:
                ny = cy + (gy + 1) * step
                if math.dist((px, ny), (cx, cy)) <= r * 0.95:
                    draw.line([(px, py), (px, ny)], fill=(*c1, alpha - 40), width=1)


def _draw_topology(draw, cx, cy, sz, c1, c2, seed=0):
    """Deformed loops / Möbius-like curves."""
    rng = random.Random(77 + seed)
    r = sz // 2
    for loop in range(3):
        lr = r * (0.25 + loop * 0.2) + rng.uniform(-10, 10)
        offset_x = rng.uniform(-r * 0.15, r * 0.15)
        offset_y = rng.uniform(-r * 0.15, r * 0.15)
        deform = rng.uniform(0.3, 0.7)
        alpha = int(80 + 60 * (2 - loop))
        pts = []
        for t in range(80):
            a = 2 * math.pi * t / 79
            dx = lr * math.cos(a) * (1 + deform * math.sin(2 * a))
            dy = lr * math.sin(a) * (1 + deform * math.cos(3 * a))
            pts.append((cx + offset_x + int(dx), cy + offset_y + int(dy)))
        for j in range(1, len(pts)):
            draw.line([pts[j - 1], pts[j]], fill=(*c1, alpha), width=2)
        draw.line([pts[-1], pts[0]], fill=(*c1, alpha), width=2)


def _draw_constellation(draw, cx, cy, sz, c1, c2, seed=0):
    """Star field with constellation lines."""
    rng = random.Random(99 + seed)
    r = sz // 2
    stars = [(cx + rng.randint(-r, r), cy + rng.randint(-r, r)) for _ in range(30)]
    bright = stars[:8]
    # Dim stars
    for sx, sy in stars[8:]:
        size = rng.uniform(1, 3)
        draw.ellipse([(sx - size, sy - size), (sx + size, sy + size)], fill=(*c2, rng.randint(50, 100)))
    # Constellation lines
    for i in range(len(bright) - 1):
        d = math.dist(bright[i], bright[i + 1])
        if d < r * 0.8:
            draw.line([bright[i], bright[i + 1]], fill=(*c1, 80), width=1)
    # Bright stars
    for sx, sy in bright:
        size = rng.uniform(4, 8)
        draw.ellipse([(sx - size, sy - size), (sx + size, sy + size)], fill=(*c1, rng.randint(150, 220)))


def _draw_lens(draw, cx, cy, sz, c1, c2, seed=0):
    """Optical lens with refraction rays."""
    rng = random.Random(42 + seed)
    r = sz // 2
    lens_h = r * 0.8
    # Lens shape (two arcs)
    draw.arc([cx - 30, cy - lens_h, cx + 60, cy + lens_h], 90, 270, fill=(*c1, 160), width=2)
    draw.arc([cx - 60, cy - lens_h, cx + 30, cy + lens_h], 270, 90, fill=(*c1, 160), width=2)
    # Incoming parallel rays
    for i in range(5):
        y = cy - lens_h * 0.6 + i * (lens_h * 1.2 / 4)
        draw.line([(cx - r * 0.9, y), (cx - 10, y)], fill=(*c1, 100), width=2)
        # Refracted (converge to focal point)
        focal_x = cx + r * 0.6
        draw.line([(cx + 10, y), (focal_x, cy)], fill=(*c1, 70 + i * 15), width=2)
    draw.ellipse([(focal_x - 4, cy - 4), (focal_x + 4, cy + 4)], fill=(*c1, 200))


def _draw_membrane(draw, cx, cy, sz, c1, c2, seed=0):
    """Lipid bilayer membrane – wavy lines with tails."""
    rng = random.Random(42 + seed)
    r = sz // 2
    # Two wavy parallel lines (outer and inner leaflet)
    for layer in [-1, 1]:
        y_base = cy + layer * 24
        pts = []
        for t in range(70):
            x = cx - r * 0.85 + t * (r * 1.7 / 69)
            y = y_base + 8 * math.sin(t * 0.18 + layer * 0.5)
            pts.append((x, y))
        for j in range(1, len(pts)):
            draw.line([pts[j - 1], pts[j]], fill=(*c1, 160), width=2)
    # Lipid tails – short lines perpendicular to membrane, pointing inward
    for t in range(3, 70, 4):
        x = cx - r * 0.85 + t * (r * 1.7 / 69)
        for layer in [-1, 1]:
            y = cy + layer * 24 + 8 * math.sin(t * 0.18 + layer * 0.5)
            tail_len = 14
            draw.line([(x, y), (x, y - layer * tail_len)], fill=(*c1, 100), width=1)
    # Channel gap
    ch_x = cx + rng.randint(-15, 15)
    draw.line([(ch_x - 7, cy - 32), (ch_x - 7, cy + 32)], fill=(*c1, 130), width=1)
    draw.line([(ch_x + 7, cy - 32), (ch_x + 7, cy + 32)], fill=(*c1, 130), width=1)


def _draw_gear(draw, cx, cy, sz, c1, c2, seed=0):
    """Interlocking gears – light outlines with hub detail."""
    rng = random.Random(42 + seed)
    r = sz // 2

    def draw_gear(gx, gy, gr, teeth, alpha, phase=0):
        pts = []
        for i in range(teeth * 2):
            a = 2 * math.pi * i / (teeth * 2) + phase
            rr = gr if i % 2 == 0 else gr * 0.78
            pts.append((gx + int(rr * math.cos(a)), gy + int(rr * math.sin(a))))
        for i in range(len(pts)):
            draw.line([pts[i], pts[(i + 1) % len(pts)]], fill=(*c1, alpha), width=2)
        # Hub circle only
        hub_r = gr * 0.2
        draw.ellipse([(gx - hub_r, gy - hub_r), (gx + hub_r, gy + hub_r)],
                     outline=(*c1, alpha - 30), width=1)

    draw_gear(cx - r * 0.22, cy - r * 0.12, r * 0.5, 11, 150, phase=0)
    draw_gear(cx + r * 0.38, cy + r * 0.18, r * 0.35, 8, 110, phase=math.pi / 8)
    draw_gear(cx - r * 0.08, cy + r * 0.52, r * 0.22, 7, 80, phase=0.3)


def _draw_venn(draw, cx, cy, sz, c1, c2, seed=0):
    """Overlapping Venn diagram – clean circles, no dots."""
    rng = random.Random(42 + seed)
    r = sz // 2
    cr = r * 0.42
    offset = r * 0.24
    centers = [
        (cx - offset, cy - int(offset * 0.5)),
        (cx + offset, cy - int(offset * 0.5)),
        (cx, cy + int(offset * 0.7)),
    ]
    for i, (vx, vy) in enumerate(centers):
        alpha = 80 + i * 25
        draw.ellipse([(vx - cr, vy - cr), (vx + cr, vy + cr)], outline=(*c1, alpha), width=2)


def _draw_axis(draw, cx, cy, sz, c1, c2, seed=0):
    """Coordinate axes with a curve."""
    rng = random.Random(42 + seed)
    r = sz // 2
    ox, oy = cx - r * 0.6, cy + r * 0.5
    # Axes
    draw.line([(ox, oy), (ox + r * 1.3, oy)], fill=(*c1, 120), width=2)
    draw.line([(ox, oy), (ox, oy - r * 1.1)], fill=(*c1, 120), width=2)
    # Arrow tips
    draw.line([(ox + r * 1.25, oy - 4), (ox + r * 1.3, oy)], fill=(*c1, 120), width=2)
    draw.line([(ox + r * 1.25, oy + 4), (ox + r * 1.3, oy)], fill=(*c1, 120), width=2)
    draw.line([(ox - 4, oy - r * 1.05), (ox, oy - r * 1.1)], fill=(*c1, 120), width=2)
    draw.line([(ox + 4, oy - r * 1.05), (ox, oy - r * 1.1)], fill=(*c1, 120), width=2)
    # Curve
    func_seed = rng.uniform(0.5, 2.0)
    pts = []
    for t in range(60):
        x = ox + t * (r * 1.2 / 59)
        frac = t / 59
        y = oy - r * 0.8 * (math.sin(frac * math.pi * func_seed) ** 2) * (1 - 0.3 * frac)
        pts.append((x, y))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 180), width=3)
    # Scatter points along curve
    for t in range(0, 60, 8):
        x, y = pts[t]
        draw.ellipse([(x - 4, y - 4), (x + 4, y + 4)], fill=(*c1, 160))


def _draw_hierarchy(draw, cx, cy, sz, c1, c2, seed=0):
    """Pyramid / hierarchical layers – clean trapezoids only."""
    rng = random.Random(42 + seed)
    r = sz // 2
    n_levels = 4
    for lv in range(n_levels):
        y = cy - r * 0.55 + lv * (r * 0.32)
        w = r * (0.15 + lv * 0.25)
        alpha = 160 - lv * 30
        y2 = y + r * 0.24
        w2 = r * (0.15 + (lv + 1) * 0.25)
        pts = [(cx - w, y), (cx + w, y), (cx + w2, y2), (cx - w2, y2)]
        for i in range(4):
            draw.line([pts[i], pts[(i + 1) % 4]], fill=(*c1, alpha), width=2)


def _draw_radioactive(draw, cx, cy, sz, c1, c2, seed=0):
    """Decay curve with emitted rays – no endpoint dots."""
    rng = random.Random(42 + seed)
    r = sz // 2
    # Exponential decay curve
    pts = []
    for t in range(80):
        frac = t / 79
        x = cx - r * 0.7 + frac * r * 1.4
        y = cy + r * 0.4 - r * 0.8 * math.exp(-3 * frac)
        pts.append((x, y))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 140), width=2)
    # Emitted rays
    for i in range(7):
        t = rng.randint(8, 65)
        x, y = pts[t]
        angle = rng.uniform(-math.pi * 0.75, -math.pi * 0.25)
        length = rng.uniform(r * 0.12, r * 0.3)
        ex, ey = x + length * math.cos(angle), y + length * math.sin(angle)
        draw.line([(x, y), (ex, ey)], fill=(*c1, 100), width=1)


def _draw_electrode(draw, cx, cy, sz, c1, c2, seed=0):
    """Parallel plate capacitor with charges."""
    rng = random.Random(42 + seed)
    r = sz // 2
    plate_h = r * 0.7
    gap = r * 0.5
    # Two plates
    for sign in [-1, 1]:
        px = cx + sign * int(gap / 2)
        draw.line([(px, cy - plate_h), (px, cy + plate_h)], fill=(*c1, 180), width=3)
    # + and - charges
    for _ in range(8):
        y = rng.uniform(cy - plate_h * 0.8, cy + plate_h * 0.8)
        # Positive (left plate)
        px = cx - gap // 2 - rng.uniform(5, 25)
        draw.text((px - 4, y - 6), "+", fill=(*c1, 140), font=None)
        # Negative (right plate)
        px = cx + gap // 2 + rng.uniform(5, 25)
        draw.text((px - 4, y - 6), "−", fill=(*c1, 140), font=None)
    # Field lines
    for i in range(5):
        y = cy - plate_h * 0.6 + i * (plate_h * 1.2 / 4)
        draw.line([(cx - gap // 2 + 5, y), (cx + gap // 2 - 5, y)], fill=(*c1, 60), width=1)
        # Arrow
        draw.line([(cx + 5, y), (cx, y - 3)], fill=(*c1, 80), width=1)
        draw.line([(cx + 5, y), (cx, y + 3)], fill=(*c1, 80), width=1)


def _draw_spring(draw, cx, cy, sz, c1, c2, seed=0):
    """Zigzag spring / harmonic oscillator."""
    rng = random.Random(42 + seed)
    r = sz // 2
    n_coils = 8
    amp = r * 0.25
    # Wall
    draw.line([(cx - r * 0.7, cy - amp), (cx - r * 0.7, cy + amp)], fill=(*c1, 140), width=3)
    # Spring zigzag
    pts = [(cx - r * 0.7, cy)]
    for i in range(n_coils * 2):
        frac = (i + 1) / (n_coils * 2)
        x = cx - r * 0.7 + frac * r * 1.1
        y = cy + amp * (1 if i % 2 == 0 else -1)
        pts.append((x, y))
    pts.append((cx + r * 0.4, cy))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 150), width=2)
    # Mass block
    bx = cx + r * 0.4
    draw.rectangle([(bx, cy - 18), (bx + 36, cy + 18)], outline=(*c1, 180), width=2)
    # Arrow showing motion
    draw.line([(bx + 50, cy), (bx + 75, cy)], fill=(*c1, 100), width=2)
    draw.line([(bx + 70, cy - 4), (bx + 75, cy)], fill=(*c1, 100), width=2)
    draw.line([(bx + 70, cy + 4), (bx + 75, cy)], fill=(*c1, 100), width=2)


def _draw_prism(draw, cx, cy, sz, c1, c2, seed=0):
    """Prism with light dispersion – elegant, airy."""
    r = sz // 2
    # Triangle prism (medium size, not overpowering)
    tri = [(cx - r * 0.25, cy + r * 0.35), (cx + r * 0.25, cy + r * 0.35), (cx, cy - r * 0.35)]
    for i in range(3):
        draw.line([tri[i], tri[(i + 1) % 3]], fill=(*c1, 150), width=2)
    # Incoming beam
    beam_entry = (cx - r * 0.1, cy + r * 0.05)
    draw.line([(cx - r * 0.85, cy - r * 0.05), beam_entry], fill=(*c1, 120), width=2)
    # Dispersed rays – fanning out lightly
    exit_pt = (cx + r * 0.18, cy + r * 0.05)
    for i in range(7):
        angle = -0.25 + i * 0.1
        length = r * 0.7
        ex = exit_pt[0] + length * math.cos(angle)
        ey = exit_pt[1] + length * math.sin(angle)
        alpha = 50 + i * 18
        draw.line([exit_pt, (ex, ey)], fill=(*c1, alpha), width=1)
        draw.ellipse([(ex - 2, ey - 2), (ex + 2, ey + 2)], fill=(*c1, alpha + 30))


def _draw_interference(draw, cx, cy, sz, c1, c2, seed=0):
    """Wave interference: two sources, concentric ripples."""
    r = sz // 2
    # Sources offset, rings constrained to panel
    s1 = (cx - r * 0.32, cy + r * 0.05)
    s2 = (cx + r * 0.32, cy - r * 0.05)
    for src in [s1, s2]:
        for i in range(1, 8):
            cr = i * r * 0.11
            alpha = max(30, 110 - i * 10)
            draw.ellipse([(src[0] - cr, src[1] - cr), (src[0] + cr, src[1] + cr)],
                         outline=(*c1, alpha), width=1)


def _draw_diffusion(draw, cx, cy, sz, c1, c2, seed=0):
    """Concentration gradient: dense to sparse."""
    rng = random.Random(42 + seed)
    r = sz // 2
    for _ in range(100):
        x = rng.gauss(-r * 0.3, r * 0.35)
        y = rng.uniform(-r * 0.8, r * 0.8)
        if abs(x) > r or abs(y) > r:
            continue
        # Density decreases left to right
        density = max(0, 1 - (x + r) / (2 * r))
        if rng.random() > density * 1.5:
            continue
        size = rng.uniform(3, 6)
        alpha = int(60 + 140 * density)
        draw.ellipse([(cx + x - size, cy + y - size), (cx + x + size, cy + y + size)], fill=(*c1, alpha))
    # Gradient arrow
    draw.line([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy + r * 0.7)], fill=(*c1, 80), width=2)
    draw.line([(cx + r * 0.65, cy + r * 0.66), (cx + r * 0.7, cy + r * 0.7)], fill=(*c1, 80), width=2)
    draw.line([(cx + r * 0.65, cy + r * 0.74), (cx + r * 0.7, cy + r * 0.7)], fill=(*c1, 80), width=2)


def _draw_bond(draw, cx, cy, sz, c1, c2, seed=0):
    """Chemical bonds: atoms connected by single/double bonds."""
    rng = random.Random(42 + seed)
    r = sz // 2
    atoms = [(cx + rng.randint(-int(r * 0.6), int(r * 0.6)),
              cy + rng.randint(-int(r * 0.6), int(r * 0.6))) for _ in range(6)]
    # Bonds
    for i in range(len(atoms)):
        j = (i + 1) % len(atoms)
        x0, y0 = atoms[i]
        x1, y1 = atoms[j]
        d = math.dist(atoms[i], atoms[j])
        if d > r:
            continue
        n_lines = rng.choice([1, 2, 3])
        perp_x, perp_y = -(y1 - y0) / max(d, 1) * 4, (x1 - x0) / max(d, 1) * 4
        for b in range(n_lines):
            off = (b - (n_lines - 1) / 2)
            draw.line([(x0 + perp_x * off, y0 + perp_y * off),
                       (x1 + perp_x * off, y1 + perp_y * off)], fill=(*c1, 130), width=2)
    # Atoms
    for ax, ay in atoms:
        ar = rng.uniform(10, 18)
        draw.ellipse([(ax - ar, ay - ar), (ax + ar, ay + ar)], outline=(*c1, 160), width=2)
        draw.ellipse([(ax - 4, ay - 4), (ax + 4, ay + 4)], fill=(*c1, 140))


def _draw_oscillator(draw, cx, cy, sz, c1, c2, seed=0):
    """Damped oscillation waveform."""
    rng = random.Random(42 + seed)
    r = sz // 2
    freq = rng.uniform(3, 5)
    decay = rng.uniform(1.5, 3.0)
    # Axis
    draw.line([(cx - r * 0.85, cy), (cx + r * 0.85, cy)], fill=(*c1, 60), width=1)
    # Waveform
    pts = []
    for t in range(120):
        frac = t / 119
        x = cx - r * 0.8 + frac * r * 1.6
        amp = r * 0.5 * math.exp(-decay * frac)
        y = cy - amp * math.sin(freq * 2 * math.pi * frac)
        pts.append((x, y))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 180), width=3)
    # Envelope
    for sign in [1, -1]:
        env = []
        for t in range(120):
            frac = t / 119
            x = cx - r * 0.8 + frac * r * 1.6
            amp = r * 0.5 * math.exp(-decay * frac)
            env.append((x, cy - sign * amp))
        for j in range(1, len(env)):
            draw.line([env[j - 1], env[j]], fill=(*c2, 60), width=1)


def _draw_parabola(draw, cx, cy, sz, c1, c2, seed=0):
    """Parabolic trajectory / projectile."""
    rng = random.Random(42 + seed)
    r = sz // 2
    # Ground line
    draw.line([(cx - r * 0.85, cy + r * 0.4), (cx + r * 0.85, cy + r * 0.4)], fill=(*c2, 60), width=1)
    # Trajectory
    pts = []
    for t in range(80):
        frac = t / 79
        x = cx - r * 0.7 + frac * r * 1.4
        y = cy + r * 0.4 - r * 0.9 * (4 * frac * (1 - frac))
        pts.append((x, y))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 180), width=3)
    # Dots along trajectory
    for t in range(0, 80, 10):
        x, y = pts[t]
        draw.ellipse([(x - 4, y - 4), (x + 4, y + 4)], fill=(*c1, 160))
    # Velocity arrows at a few points
    for t in [10, 30, 50]:
        x, y = pts[t]
        dx = (pts[t + 1][0] - pts[t - 1][0]) * 0.8
        dy = (pts[t + 1][1] - pts[t - 1][1]) * 0.8
        draw.line([(x, y), (x + dx, y + dy)], fill=(*c1, 100), width=2)


def _draw_tessellation(draw, cx, cy, sz, c1, c2, seed=0):
    """Tiling / tessellation pattern."""
    rng = random.Random(42 + seed)
    r = sz // 2
    cell = int(r * 0.28)
    shape = rng.choice(["triangle", "diamond"])
    for row in range(-4, 5):
        for col in range(-4, 5):
            if shape == "triangle":
                bx = cx + col * cell + (row % 2) * cell // 2
                by = cy + int(row * cell * 0.86)
                if math.dist((bx, by), (cx, cy)) > r:
                    continue
                alpha = max(40, int(150 - math.dist((bx, by), (cx, cy)) * 0.5))
                up = (row + col) % 2 == 0
                if up:
                    pts = [(bx, by - cell // 2), (bx - cell // 2, by + cell // 2), (bx + cell // 2, by + cell // 2)]
                else:
                    pts = [(bx - cell // 2, by - cell // 2), (bx + cell // 2, by - cell // 2), (bx, by + cell // 2)]
                for i in range(3):
                    draw.line([pts[i], pts[(i + 1) % 3]], fill=(*c1, alpha), width=1)
            else:
                bx = cx + col * cell + (row % 2) * cell // 2
                by = cy + row * cell
                if math.dist((bx, by), (cx, cy)) > r:
                    continue
                alpha = max(40, int(150 - math.dist((bx, by), (cx, cy)) * 0.5))
                h = cell // 2
                pts = [(bx, by - h), (bx + h, by), (bx, by + h), (bx - h, by)]
                for i in range(4):
                    draw.line([pts[i], pts[(i + 1) % 4]], fill=(*c1, alpha), width=1)


def _draw_pipeline(draw, cx, cy, sz, c1, c2, seed=0):
    """Flowchart / pipeline nodes."""
    rng = random.Random(42 + seed)
    r = sz // 2
    n_cols = 3
    n_rows = rng.choice([2, 3])
    nodes = []
    for row in range(n_rows):
        for col in range(n_cols):
            x = cx - r * 0.55 + col * (r * 0.55)
            y = cy - r * 0.4 + row * (r * 0.4)
            nodes.append((int(x), int(y)))
    # Connections (left to right, top to bottom)
    for row in range(n_rows):
        for col in range(n_cols - 1):
            i = row * n_cols + col
            draw.line([nodes[i], nodes[i + 1]], fill=(*c1, 100), width=2)
    for row in range(n_rows - 1):
        col = rng.randint(0, n_cols - 1)
        i = row * n_cols + col
        draw.line([nodes[i], nodes[i + n_cols]], fill=(*c1, 80), width=2)
    # Node boxes
    for nx, ny in nodes:
        draw.rounded_rectangle([(nx - 16, ny - 10), (nx + 16, ny + 10)], radius=4,
                                outline=(*c1, 160), width=2)


def _draw_crosssection(draw, cx, cy, sz, c1, c2, seed=0):
    """Concentric ring cross-section."""
    rng = random.Random(42 + seed)
    r = sz // 2
    n_rings = rng.choice([4, 5, 6])
    for i in range(n_rings, 0, -1):
        cr = r * (i / n_rings) * 0.8
        alpha = int(40 + 140 * (1 - i / n_rings))
        draw.ellipse([(cx - cr, cy - cr), (cx + cr, cy + cr)], outline=(*c1, alpha + 30), width=2)
        if i < n_rings:
            # Fill region hint
            for _ in range(3):
                a = rng.uniform(0, 2 * math.pi)
                d = rng.uniform(cr * 0.7, cr * 0.95)
                px, py = cx + int(d * math.cos(a)), cy + int(d * math.sin(a))
                draw.ellipse([(px - 2, py - 2), (px + 2, py + 2)], fill=(*c1, alpha))
    draw.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=(*c1, 200))


def _draw_dipole(draw, cx, cy, sz, c1, c2, seed=0):
    """Magnetic/electric dipole field lines."""
    r = sz // 2
    # Two poles
    p1 = (cx - r * 0.3, cy)
    p2 = (cx + r * 0.3, cy)
    draw.ellipse([(p1[0] - 6, p1[1] - 6), (p1[0] + 6, p1[1] + 6)], fill=(*c1, 200))
    draw.ellipse([(p2[0] - 6, p2[1] - 6), (p2[0] + 6, p2[1] + 6)], fill=(*c1, 200))
    # Field lines (arcs from p1 to p2)
    for i in range(5):
        bulge = r * (0.15 + i * 0.12) * (1 if i % 2 == 0 else -1)
        pts = []
        for t in range(40):
            frac = t / 39
            x = p1[0] + frac * (p2[0] - p1[0])
            y = cy + bulge * math.sin(frac * math.pi)
            pts.append((x, y))
        for j in range(1, len(pts)):
            draw.line([pts[j - 1], pts[j]], fill=(*c1, 80 + abs(i) * 10), width=2)


def _draw_pulse(draw, cx, cy, sz, c1, c2, seed=0):
    """Pulse / spike signal."""
    rng = random.Random(42 + seed)
    r = sz // 2
    # Baseline
    draw.line([(cx - r * 0.85, cy), (cx + r * 0.85, cy)], fill=(*c2, 50), width=1)
    # Pulse waveform
    pts = [(cx - r * 0.8, cy)]
    n_pulses = rng.choice([3, 4, 5])
    seg = r * 1.6 / n_pulses
    for i in range(n_pulses):
        base_x = cx - r * 0.8 + i * seg
        h = rng.uniform(r * 0.2, r * 0.7)
        w = seg * 0.25
        pts.append((base_x + seg * 0.3, cy))
        pts.append((base_x + seg * 0.35, cy - h))
        pts.append((base_x + seg * 0.35 + w, cy - h))
        pts.append((base_x + seg * 0.35 + w, cy + h * 0.15))
        pts.append((base_x + seg * 0.55, cy))
    pts.append((cx + r * 0.8, cy))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 180), width=2)


def _draw_bridge(draw, cx, cy, sz, c1, c2, seed=0):
    """Arch bridge – light, elegant structure."""
    r = sz // 2
    x_left = cx - r * 0.8
    x_right = cx + r * 0.8
    y_deck = cy + r * 0.15
    # Deck line
    draw.line([(x_left, y_deck), (x_right, y_deck)], fill=(*c1, 140), width=2)
    # Parabolic arch
    arch_pts = []
    for i in range(60):
        frac = i / 59
        x = x_left + frac * (x_right - x_left)
        y = y_deck - r * 0.75 * (1 - (2 * frac - 1) ** 2)
        arch_pts.append((x, y))
    for j in range(1, len(arch_pts)):
        draw.line([arch_pts[j - 1], arch_pts[j]], fill=(*c1, 130), width=2)
    # Vertical hangers – thin
    n_hangers = 8
    for i in range(n_hangers):
        frac = (i + 1) / (n_hangers + 1)
        x = x_left + frac * (x_right - x_left)
        y_arch = y_deck - r * 0.75 * (1 - (2 * frac - 1) ** 2)
        draw.line([(x, y_arch), (x, y_deck)], fill=(*c1, 70), width=1)
    # Tiny support marks
    for px in [x_left, x_right]:
        draw.line([(px, y_deck), (px, y_deck + r * 0.12)], fill=(*c1, 100), width=2)


def _draw_polar(draw, cx, cy, sz, c1, c2, seed=0):
    """Polar coordinate rose curve."""
    rng = random.Random(42 + seed)
    r = sz // 2
    petals = rng.choice([3, 4, 5, 7])
    # Grid circles
    for i in range(1, 4):
        cr = r * i * 0.25
        draw.ellipse([(cx - cr, cy - cr), (cx + cr, cy + cr)], outline=(*c2, 40), width=1)
    # Axes
    for a in range(0, 360, 45):
        rad = math.radians(a)
        draw.line([(cx, cy), (cx + int(r * 0.75 * math.cos(rad)), cy + int(r * 0.75 * math.sin(rad)))],
                  fill=(*c2, 30), width=1)
    # Rose curve
    pts = []
    for t in range(360):
        a = math.radians(t)
        rr = r * 0.7 * abs(math.cos(petals * a / 2))
        pts.append((cx + int(rr * math.cos(a)), cy + int(rr * math.sin(a))))
    for j in range(1, len(pts)):
        draw.line([pts[j - 1], pts[j]], fill=(*c1, 160), width=2)


def _draw_knot(draw, cx, cy, sz, c1, c2, seed=0):
    """Trefoil knot – elegant with depth crossings."""
    rng = random.Random(42 + seed)
    r = sz // 2
    scale = r * 0.26
    n_pts = 250
    pts = []
    depths = []
    for t in range(n_pts):
        a = 2 * math.pi * t / (n_pts - 1)
        x = math.sin(a) + 2 * math.sin(2 * a)
        y = math.cos(a) - 2 * math.cos(2 * a)
        pts.append((cx + int(x * scale), cy + int(y * scale)))
        depths.append(math.sin(3 * a))
    # Two-pass: back dim, front bright
    for j in range(1, n_pts):
        if depths[j] < 0:
            draw.line([pts[j - 1], pts[j]], fill=(*c1, 55), width=2)
    for j in range(1, n_pts):
        if depths[j] >= 0:
            draw.line([pts[j - 1], pts[j]], fill=(*c1, 150), width=2)


def _draw_cascade_steps(draw, cx, cy, sz, c1, c2, seed=0):
    """Staircase / cascade steps."""
    rng = random.Random(42 + seed)
    r = sz // 2
    n_steps = rng.choice([5, 6, 7])
    step_w = r * 1.4 / n_steps
    step_h = r * 1.0 / n_steps
    x = cx - r * 0.7
    y = cy - r * 0.45
    for i in range(n_steps):
        x2 = x + step_w
        y2 = y + step_h
        alpha = int(100 + 80 * (i / n_steps))
        draw.line([(x, y), (x2, y)], fill=(*c1, alpha), width=2)  # horizontal
        draw.line([(x2, y), (x2, y2)], fill=(*c1, alpha), width=2)  # vertical drop
        # Arrow on step
        mid_x = (x + x2) / 2
        draw.line([(mid_x, y - 8), (mid_x + 6, y - 5)], fill=(*c1, 60), width=1)
        draw.line([(mid_x, y - 8), (mid_x + 6, y - 11)], fill=(*c1, 60), width=1)
        draw.line([(mid_x, y - 8), (mid_x + 14, y - 8)], fill=(*c1, 60), width=1)
        x = x2
        y = y2


def _draw_symmetry(draw, cx, cy, sz, c1, c2, seed=0):
    """Kaleidoscope / rotational symmetry pattern."""
    rng = random.Random(42 + seed)
    r = sz // 2
    n_fold = rng.choice([4, 5, 6, 8])
    # Draw one sector, repeat
    sector_pts = []
    for _ in range(rng.randint(4, 7)):
        d = rng.uniform(r * 0.1, r * 0.7)
        a = rng.uniform(0, 2 * math.pi / n_fold)
        sector_pts.append((d, a))
    for k in range(n_fold):
        rot = k * (2 * math.pi / n_fold)
        alpha = 100 + (k * 15) % 60
        transformed = []
        for d, a in sector_pts:
            ta = a + rot
            transformed.append((cx + int(d * math.cos(ta)), cy + int(d * math.sin(ta))))
        for j in range(1, len(transformed)):
            draw.line([transformed[j - 1], transformed[j]], fill=(*c1, alpha), width=2)
        if len(transformed) > 2:
            draw.line([transformed[-1], transformed[0]], fill=(*c1, alpha - 30), width=1)


def _draw_cloud(draw, cx, cy, sz, c1, c2, seed=0):
    """Wispy overlapping arcs – nebula / probability cloud."""
    rng = random.Random(42 + seed)
    r = sz // 2
    for _ in range(18):
        # Each wisp is a smooth arc
        acx = cx + rng.uniform(-r * 0.35, r * 0.35)
        acy = cy + rng.uniform(-r * 0.35, r * 0.35)
        arc_r = rng.uniform(r * 0.2, r * 0.55)
        start_a = rng.uniform(0, 2 * math.pi)
        sweep = rng.uniform(0.8, 2.2)
        alpha = rng.randint(40, 110)
        pts = []
        for t in range(30):
            a = start_a + sweep * t / 29
            px = acx + arc_r * math.cos(a)
            py = acy + arc_r * math.sin(a)
            pts.append((px, py))
        for j in range(1, len(pts)):
            draw.line([pts[j - 1], pts[j]], fill=(*c1, alpha), width=1)


# ── Generative Primitive Art (semantic-driven) ─────────────

# Semantic parameter schema for _draw_generative():
#   primitives: list of 1-3 from ["lines","arcs","dots","ellipses","polygons","curves","grid"]
#   layout:     "radial" | "horizontal" | "vertical" | "diagonal" | "scattered" | "layered"
#   density:    "dense" | "medium" | "sparse"
#   symmetry:   "radial" | "bilateral" | "none"
#
# Style constraints (auto-enforced to match the 15 base illustrations):
#   - Line width: 2-3px
#   - Element count: 8-80 (sparse to dense, never hundreds)
#   - Alpha range: 40-230
#   - Edge fade: elements near boundary get transparent
#   - No trails, no particle blobs, no fill-heavy regions

_GEN_DEFAULTS = {
    "primitives": ["lines", "dots"],
    "layout": "radial",
    "density": "medium",
    "symmetry": "none",
}

_DENSITY_COUNT = {"dense": 60, "medium": 35, "sparse": 15}


def _draw_generative(draw, cx, cy, sz, c1, c2, seed=0, params=None):
    """Geometric-primitive composition matching the 15 base illustration styles."""
    p = {**_GEN_DEFAULTS, **(params or {})}
    rng = random.Random(seed)
    r = sz // 2
    n = _DENSITY_COUNT.get(p["density"], 35)
    prims = p["primitives"] if isinstance(p["primitives"], list) else [p["primitives"]]
    layout = p["layout"]
    sym = p["symmetry"]

    # ── Generate anchor points based on layout ──
    anchors = []
    if layout == "horizontal":
        for i in range(n):
            x = -r * 0.9 + (i / max(n - 1, 1)) * r * 1.8
            y = rng.gauss(0, r * 0.12)
            anchors.append((x, y))
    elif layout == "vertical":
        for i in range(n):
            x = rng.gauss(0, r * 0.12)
            y = -r * 0.9 + (i / max(n - 1, 1)) * r * 1.8
            anchors.append((x, y))
    elif layout == "diagonal":
        for i in range(n):
            t = i / max(n - 1, 1)
            x = -r * 0.8 + t * r * 1.6 + rng.gauss(0, r * 0.06)
            y = -r * 0.8 + t * r * 1.6 + rng.gauss(0, r * 0.06)
            anchors.append((x, y))
    elif layout == "scattered":
        for _ in range(n):
            x = rng.uniform(-r * 0.85, r * 0.85)
            y = rng.uniform(-r * 0.85, r * 0.85)
            anchors.append((x, y))
    elif layout == "layered":
        n_layers = rng.choice([3, 4, 5])
        per_layer = n // n_layers
        for li in range(n_layers):
            y_base = -r * 0.7 + li * (r * 1.4 / (n_layers - 1))
            for _ in range(per_layer):
                x = rng.uniform(-r * 0.8, r * 0.8)
                y = y_base + rng.gauss(0, r * 0.04)
                anchors.append((x, y))
    else:  # radial
        for i in range(n):
            a = rng.uniform(0, 2 * math.pi)
            d = rng.uniform(r * 0.05, r * 0.85)
            anchors.append((d * math.cos(a), d * math.sin(a)))

    # ── Apply symmetry ──
    if sym == "bilateral":
        mirrored = [(- x, y) for x, y in anchors]
        anchors = anchors + mirrored
    elif sym == "radial":
        arms = rng.choice([3, 4, 5, 6])
        base = list(anchors)
        anchors = []
        for x, y in base:
            a0 = math.atan2(y, x)
            d = math.sqrt(x * x + y * y)
            for k in range(arms):
                angle = a0 + k * (2 * math.pi / arms)
                anchors.append((d * math.cos(angle), d * math.sin(angle)))

    # ── Helper: alpha with edge fade ──
    def _alpha(x, y, base=180):
        dist = math.sqrt(x * x + y * y)
        fade = max(0.15, 1.0 - (dist / r) ** 1.5)
        return max(40, int(base * fade))

    # ── Draw primitives ──
    for prim in prims:
        if prim == "dots":
            for x, y in anchors:
                sx, sy = cx + int(x), cy + int(y)
                size = rng.uniform(4, 8)
                a = _alpha(x, y, 200)
                draw.ellipse([(sx - size, sy - size), (sx + size, sy + size)], fill=(*c1, a))

        elif prim == "lines":
            for i, (x, y) in enumerate(anchors):
                sx, sy = cx + int(x), cy + int(y)
                angle = rng.uniform(0, 2 * math.pi)
                length = rng.uniform(r * 0.08, r * 0.25)
                ex = sx + int(length * math.cos(angle))
                ey = sy + int(length * math.sin(angle))
                a = _alpha(x, y, 160)
                draw.line([(sx, sy), (ex, ey)], fill=(*c1, a), width=2)

        elif prim == "arcs":
            for x, y in anchors:
                sx, sy = cx + int(x), cy + int(y)
                arc_r = rng.uniform(r * 0.06, r * 0.2)
                start = rng.uniform(0, 360)
                span = rng.uniform(60, 200)
                a = _alpha(x, y, 140)
                bbox = [sx - arc_r, sy - arc_r, sx + arc_r, sy + arc_r]
                draw.arc(bbox, start, start + span, fill=(*c1, a), width=2)

        elif prim == "ellipses":
            for x, y in anchors:
                sx, sy = cx + int(x), cy + int(y)
                rx = rng.uniform(r * 0.05, r * 0.18)
                ry = rng.uniform(r * 0.03, r * 0.12)
                a = _alpha(x, y, 100)
                draw.ellipse([(sx - rx, sy - ry), (sx + rx, sy + ry)], outline=(*c1, a), width=2)

        elif prim == "polygons":
            for x, y in anchors:
                sx, sy = cx + int(x), cy + int(y)
                sides = rng.choice([3, 4, 5, 6])
                pr = rng.uniform(r * 0.04, r * 0.12)
                rot = rng.uniform(0, 2 * math.pi)
                pts = [(sx + int(pr * math.cos(rot + 2 * math.pi * k / sides)),
                        sy + int(pr * math.sin(rot + 2 * math.pi * k / sides)))
                       for k in range(sides)]
                a = _alpha(x, y, 130)
                for k in range(sides):
                    draw.line([pts[k], pts[(k + 1) % sides]], fill=(*c1, a), width=2)

        elif prim == "curves":
            # Smooth curves through anchor subsets
            sorted_a = sorted(anchors, key=lambda p: p[0] if layout == "horizontal"
                              else p[1] if layout == "vertical" else math.atan2(p[1], p[0]))
            chunk = max(4, len(sorted_a) // 3)
            for start_idx in range(0, len(sorted_a), chunk):
                subset = sorted_a[start_idx:start_idx + chunk]
                if len(subset) < 3:
                    continue
                for j in range(1, len(subset)):
                    x0, y0 = subset[j - 1]
                    x1, y1 = subset[j]
                    a = _alpha(x0, y0, 150)
                    draw.line([(cx + int(x0), cy + int(y0)),
                               (cx + int(x1), cy + int(y1))], fill=(*c1, a), width=2)

        elif prim == "grid":
            # Small local grid patterns at some anchor positions
            used = anchors[:min(8, len(anchors))]
            for x, y in used:
                sx, sy = cx + int(x), cy + int(y)
                cell = rng.uniform(r * 0.03, r * 0.06)
                rows, cols = rng.choice([3, 4]), rng.choice([3, 4])
                a = _alpha(x, y, 110)
                for row in range(rows):
                    for col in range(cols):
                        gx = sx + int((col - cols / 2) * cell)
                        gy = sy + int((row - rows / 2) * cell)
                        draw.rectangle([(gx, gy), (gx + int(cell * 0.7), gy + int(cell * 0.7))],
                                       fill=(*c1, a + rng.randint(-30, 20)))

    # ── Optional: light connections between nearby anchors ──
    if len(prims) > 1 or rng.random() < 0.4:
        pts = [(cx + int(x), cy + int(y)) for x, y in anchors]
        for i in range(min(len(pts), 60)):
            for j in range(i + 1, min(i + 4, len(pts))):
                d = math.dist(pts[i], pts[j])
                if d < r * 0.35:
                    a = max(20, int(50 - d * 0.3))
                    draw.line([pts[i], pts[j]], fill=(*c2, a), width=1)


ILLUST_FUNCS = {
    # Original 15
    "scatter": _draw_scatter, "wave": _draw_wave, "network": _draw_network,
    "hexgrid": _draw_hexgrid, "orbit": _draw_orbit, "field": _draw_field,
    "spiral": _draw_spiral, "dots": _draw_dots,
    "bifurcation": _draw_bifurcation, "flow": _draw_flow,
    "distribution": _draw_distribution, "tree": _draw_tree,
    "matrix": _draw_matrix, "pendulum": _draw_pendulum, "contour": _draw_contour,
    # New 35
    "helix": _draw_helix, "circuit": _draw_circuit, "layers": _draw_layers,
    "fractal": _draw_fractal, "cycle": _draw_cycle, "spectrum": _draw_spectrum,
    "lattice": _draw_lattice, "topology": _draw_topology,
    "constellation": _draw_constellation, "lens": _draw_lens,
    "membrane": _draw_membrane, "gear": _draw_gear, "venn": _draw_venn,
    "axis": _draw_axis, "hierarchy": _draw_hierarchy,
    "radioactive": _draw_radioactive, "electrode": _draw_electrode,
    "spring": _draw_spring, "prism": _draw_prism, "interference": _draw_interference,
    "diffusion": _draw_diffusion, "bond": _draw_bond, "oscillator": _draw_oscillator,
    "parabola": _draw_parabola, "tessellation": _draw_tessellation,
    "pipeline": _draw_pipeline, "crosssection": _draw_crosssection,
    "dipole": _draw_dipole, "pulse": _draw_pulse, "bridge": _draw_bridge,
    "polar": _draw_polar, "knot": _draw_knot, "cascade": _draw_cascade_steps,
    "symmetry": _draw_symmetry, "cloud": _draw_cloud,
    # Generative fallback
    "generative": _draw_generative,
}


# ── URL / Scraping ──────────────────────────────────────────
def _lookup_slug(query):
    """Use sciencepedia lookup.py for smart slug resolution (5-layer fuzzy matching)."""
    lookup_script = os.path.join(os.path.dirname(__file__), "..", "..", "sciencepedia", "scripts", "lookup.py")
    if not os.path.exists(lookup_script):
        return None
    try:
        result = subprocess.run(
            [sys.executable, lookup_script, "--top", "1", query],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            hits = data.get(query, [])
            if hits and hits[0].get("slug"):
                hit = hits[0]
                print(f"  Lookup: '{query}' → {hit['name']} ({hit['match_type']}, score={hit['score']})", file=sys.stderr)
                return hit["slug"]
    except Exception as e:
        print(f"  Lookup fallback: {e}", file=sys.stderr)
    return None


def parse_input(raw):
    raw = raw.strip().rstrip("/")
    if raw.startswith("http"):
        return raw.split("/")[-1], raw
    # Try smart lookup first, fall back to simple slug conversion
    slug = _lookup_slug(raw)
    if not slug:
        slug = raw.lower().replace(" ", "_").replace("-", "_")
    return slug, f"{BASE_URL}/{slug}"


def slug_to_title(slug):
    # 如果有 "-"，只取最后一部分（去掉课程分类前缀）
    if "-" in slug:
        slug = slug.split("-")[-1]
    return slug.replace("_", " ").title()


def fetch_description(url):
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        for pat in [r'<meta\s+name="description"\s+content="([^"]{20,})"',
                    r'<meta\s+property="og:description"\s+content="([^"]{20,})"']:
            m = re.search(pat, page)
            if m:
                return html.unescape(m.group(1))
        m = re.search(r'Key Takeaways.*?<li[^>]*>(.*?)</li>', page, re.DOTALL)
        if m:
            t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if len(t) > 20:
                return html.unescape(t)
    except Exception as e:
        print(f"  ⚠ Fetch failed ({e})")
    return None


def _make_qr(url, fill, bg):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill, back_color=bg).convert("RGBA").resize((QR_SIZE, QR_SIZE), Image.LANCZOS)


def _draw_gradient_bg(img):
    d = ImageDraw.Draw(img)
    for y in range(CARD_H):
        t = y / CARD_H
        d.line([(0, y), (CARD_W, y)],
               fill=(int(30 + 30 * t), int(30 + 25 * t), int(75 + 55 * t)))


# ── Main Generator ──────────────────────────────────────────
def generate_card(keyword, description=None, style_name="light", output=None, utm=None, illust_type=None, qr_label="url", gen_params=None):
    slug, url = parse_input(keyword)
    title = slug_to_title(slug)

    if not description:
        print(f"  Fetching description for '{title}'...")
        description = fetch_description(url)
    if not description:
        description = "A key concept in scientific research and computational modeling."

    qr_url = url
    if utm:
        qr_url = f"{url}{'&' if '?' in url else '?'}utm_source={utm}&utm_medium=wordcard&utm_campaign=comment_marketing"

    cat = illust_type or guess_category(slug)
    # If no category matched and no explicit type, use generative mode
    if cat == "dots" and illust_type is None and guess_category(slug) == "dots":
        matched = any(kw in slug.lower() for kws in CATEGORY_KEYWORDS.values() for kw in kws)
        if not matched:
            cat = "generative"
    illust_fn = ILLUST_FUNCS.get(cat, _draw_dots)
    s = STYLES.get(style_name, STYLES["light"])
    kw_seed = hash(slug) & 0xFFFFFF  # 改动 5: keyword-hash seed

    # ── Create image ──
    img = Image.new("RGBA", (CARD_W, CARD_H), s["bg"] or (0, 0, 0, 0))
    if style_name == "gradient":
        _draw_gradient_bg(img)
    draw = ImageDraw.Draw(img)

    # ── Illustration panel bg (light mode gets a subtle rounded rect) ──
    if s.get("illust_panel"):
        _rounded_rect(draw, (CARD_W - 620, 40, CARD_W - 40, CARD_H - 40), 24, s["illust_panel"])

    # ── Illustration (right side) ──
    illust_cx = CARD_W - 315
    illust_cy = (40 + CARD_H - PAD - 60) // 2 + 30
    if cat != "none":
        if cat == "generative":
            illust_fn(draw, illust_cx, illust_cy, 440, s["illust"], s["illust_dim"], seed=kw_seed, params=gen_params)
        else:
            illust_fn(draw, illust_cx, illust_cy, 440, s["illust"], s["illust_dim"], seed=kw_seed)

    # ── Text (left side) ──
    x, y = PAD, PAD
    # 标题左边的竖线装饰
    draw.rectangle([(x, y), (x + 8, y + 76)], fill=s["accent"])
    # 标题 — 用 title 字体
    draw.text((x + 32, y + 8), title, font=_font(52, "title"), fill=s["title"])
    y += 112
    # 横向分隔线 (短一点)
    draw.line([(x, y), (x + 560, y)], fill=s["divider"], width=2)
    y += 44
    # 正文 — 用 sans-serif 字体 (smart truncate, wrap_width=44, max_lines=6)
    for line in smart_truncate(description, wrap_width=44, max_lines=6):
        draw.text((x, y), line, font=_font(34, "body"), fill=s["text"])
        y += 60

    # ── QR (bottom-left) ──
    qr_x, qr_y = x, CARD_H - PAD - QR_SIZE
    _rounded_rect(draw, (qr_x - 8, qr_y - 8, qr_x + QR_SIZE + 8, qr_y + QR_SIZE + 8), 8, s["qr_bg"])
    img.paste(_make_qr(qr_url, s["qr_fill"], s["qr_bg"]), (qr_x, qr_y))

    # ── URL or CTA (next to QR) ──
    url_x = qr_x + QR_SIZE + 32
    if qr_label == "scan":
        draw.text((url_x, qr_y + 95), "Scan to Explore", font=_font(24, "mono"), fill=s["url"])
    else:
        url_font = _font(24, "mono")
        full_path = f"bohrium.com/en/sciencepedia/feynman/keyword/{slug}"
        url_lines = textwrap.wrap(full_path, width=30)
        for i, uline in enumerate(url_lines[:3]):
            draw.text((url_x, qr_y + 40 + i * 44), uline, font=url_font, fill=s["url"])

    # ── Brand (bottom-right, centered in illust panel) — 用标题字体 ──
    panel_left, panel_right = CARD_W - 620, CARD_W - 40
    brand_font = _font(26, "title")
    brand_bbox = draw.textbbox((0, 0), BRAND, font=brand_font)
    brand_w = brand_bbox[2] - brand_bbox[0]
    brand_x = (panel_left + panel_right) // 2 - brand_w // 2
    draw.text((brand_x, CARD_H - PAD - 40), BRAND, font=brand_font, fill=s["brand"])

    # ── Save ──
    if not output:
        os.makedirs("wordcards", exist_ok=True)
        output = f"wordcards/{slug}.png"
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    img.save(output, "PNG")
    extra = ""
    if cat == "generative" and gen_params:
        extra = f", params={gen_params}"
    print(f"  ✅ Saved: {output}  [style={style_name}, illust={cat}{extra}]")
    return output


# ── CLI ─────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Generate SciencePedia word cards with illustrations")
    p.add_argument("keyword", nargs="?", help="URL or keyword slug")
    p.add_argument("-o", "--output", help="Output path")
    p.add_argument("-s", "--style", choices=["light", "dark", "gradient"], default="light")
    p.add_argument("-d", "--description", help="Override description text")
    p.add_argument("--utm", help="UTM source (e.g. twitter, reddit)")
    p.add_argument("--illust", choices=list(ILLUST_FUNCS.keys()) + ["none"], help="Override illustration type")
    p.add_argument("--gen-params", type=str, help='JSON string of generative params, e.g. \'{"motion":"spiral","force":"vortex","trail":true}\'')
    p.add_argument("--batch", action="store_true", help="Read keywords from stdin, one per line")
    p.add_argument("--qr-label", choices=["url", "scan"], default="url", help="QR label style: 'url' (full path) or 'scan' (Scan to Explore)")
    args = p.parse_args()

    gp = json.loads(args.gen_params) if args.gen_params else None
    # If gen_params provided, auto-set illust to generative
    if gp and not args.illust:
        args.illust = "generative"

    if args.batch:
        for line in sys.stdin:
            kw = line.strip()
            if kw:
                generate_card(kw, style_name=args.style, utm=args.utm, illust_type=args.illust, qr_label=args.qr_label, gen_params=gp)
    elif args.keyword:
        generate_card(args.keyword, description=args.description, style_name=args.style,
                      output=args.output, utm=args.utm, illust_type=args.illust, qr_label=args.qr_label, gen_params=gp)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
