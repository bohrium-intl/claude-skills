---
name: sciencepedia-wordcard
description: Generate beautiful word cards (词卡) for scientific concepts from Bohrium's SciencePedia. Use when user says "generate a word card", "make a card for [concept]", "词卡", "生成词卡", "create a card", or wants a visual card for a scientific keyword. Also triggers when user provides a list of concepts to batch-generate cards. Works alongside the sciencepedia skill for URL lookups.
---

# SciencePedia Word Card Generator

Generate 1560×960 PNG word cards for scientific concepts with title, description, illustration, QR code, and SciencePedia URL.

## Quick Start

```bash
python3 scripts/generate_wordcard.py "density_functional_theory"
```

Auto-fetches description from SciencePedia. Output: `wordcard_density_functional_theory.png`

## Options

```bash
python3 scripts/generate_wordcard.py "concept_slug" \
  -d "Custom description text" \
  -s light|dark|gradient \
  -o output_path.png \
  --illust TYPE \
  --qr-label url|scan
```

- `-d` — Override auto-fetched description
- `-s` — Card style (default: light)
- `--illust` — Override illustration type (see below)
- `--qr-label url` — Show URL text; `scan` — Show "Scan to Explore"

## Illustration Types (50)

The script auto-matches concepts to illustrations via keyword matching, falling back to `dots`. When auto-matching fails or is wrong, use `--illust TYPE` to override.

### Semantic Matching Guide

When generating a card, think about which illustration best **metaphorically** represents the concept:

| Type | Visual | Best for |
|---|---|---|
| scatter | Random dots, varying alpha | Randomness, probability, sampling |
| wave | Sine curves stacked | Waves, frequency, signals |
| network | Nodes + edges | Graphs, neural nets, connections |
| hexgrid | Honeycomb grid | Materials, crystals, periodic structures |
| orbit | Concentric elliptical orbits | Quantum, atoms, orbits |
| field | Arrow vector field | Force fields, gradients, potentials |
| spiral | Logarithmic spiral | DNA, growth, phylogeny |
| dots | Soft scattered dots | Default / thermodynamics |
| bifurcation | Logistic map diagram | Chaos, nonlinear dynamics |
| flow | Streamlines | Fluids, flow, turbulence |
| distribution | Histogram + bell curve | Statistics, distributions |
| tree | Recursive branching | Decision trees, hierarchical branching |
| matrix | Heatmap grid with brackets | Linear algebra, matrices |
| pendulum | Stroboscopic pendulum | Classical mechanics |
| contour | Topographic contour lines | Optimization, loss landscapes |
| helix | Double helix with rungs | Proteins, DNA structure |
| circuit | Orthogonal paths + nodes | Circuits, logic, electronics |
| layers | Wavy horizontal strata | Geology, atmosphere, layered systems |
| fractal | Koch snowflake | Fractals, self-similarity, recursion |
| cycle | Circular arrows | Cycles, feedback loops |
| spectrum | Gradient bars | Spectroscopy, emission, wavelengths |
| lattice | Crystal lattice grid | Crystals, phonons, solid state |
| topology | Möbius-like curve | Topology, manifolds |
| constellation | Star points + connecting lines | Astronomy, stars, cosmos |
| lens | Convex lens with light rays | Optics, microscopy, refraction |
| membrane | Wavy bilayer with tails | Cell membranes, lipid bilayers |
| gear | Interlocking gear outlines | Mechanisms, engineering, machines |
| venn | Overlapping circles | Set theory, logic, classification |
| axis | Coordinate axes with curve | Functions, calculus, plotting |
| hierarchy | Stacked trapezoids (pyramid) | Taxonomy, hierarchy, food chains |
| radioactive | Decay curve with emitted rays | Radioactivity, decay, nuclear |
| electrode | Parallel plates with field lines | Electrochemistry, capacitors |
| spring | Coiled spring oscillation | Elasticity, harmonic motion |
| prism | Triangle with dispersed rays | Light dispersion, refraction |
| interference | Overlapping concentric ripples | Wave interference, diffraction |
| diffusion | Dense-to-sparse gradient | Diffusion, concentration, entropy |
| bond | Molecular structure (atoms + bonds) | Chemical bonds, molecular structure |
| oscillator | Damped sine wave | Oscillators, damping, resonance |
| parabola | Parabolic arc with tangent | Projectiles, trajectories |
| tessellation | Repeating tile pattern | Tiling, symmetry groups |
| pipeline | Connected processing boxes | Workflows, data pipelines, compilers |
| crosssection | Concentric rings (Earth-like) | Cross-sections, anatomy, CT |
| dipole | Field lines between ±poles | Dipoles, magnetic/electric fields |
| pulse | Sharp spike waveform | Neural signals, ECG, impulses |
| bridge | Arch bridge with hangers | Structural engineering, bridges |
| polar | Rose curve on polar grid | Polar coordinates, antenna patterns |
| knot | Trefoil with depth crossings | Knot theory, topology |
| cascade | Staircase steps with flow | Cascades, chain reactions, waterfalls |
| symmetry | Bilateral mirrored pattern | Symmetry, group theory |
| cloud | Overlapping wispy arcs | Probability clouds, wavefunctions |

### Choosing the Right Type

If keyword auto-match gives `dots` (default), pick the illustration that best captures the concept's **essence**:

- Concept about **connections/relationships** → `network`
- Concept about **branching/selection** → `tree`
- Concept about **periodicity/repetition** → `wave`, `lattice`, `tessellation`
- Concept about **growth/decay** → `spiral`, `radioactive`, `cascade`
- Concept about **structure/anatomy** → `crosssection`, `layers`, `bond`
- Concept about **duality/opposition** → `dipole`, `venn`, `interference`
- Concept about **process/flow** → `flow`, `pipeline`, `cycle`
- Concept about **measurement/analysis** → `axis`, `spectrum`, `distribution`

## Batch Mode

```bash
python3 scripts/generate_wordcard.py --batch
```

Reads `keywords.txt` (one slug per line) from the working directory.

## Dependencies

- Python 3, Pillow, qrcode
- Fonts: Plus Jakarta Sans Bold/Regular (fallback to system fonts)
- Network access for auto-fetching descriptions from SciencePedia
