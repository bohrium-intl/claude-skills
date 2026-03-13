---
name: sciencepedia-agent-tools
description: "Look up Bohrium SciencePedia agent-tools pages for scientific software and utilities. Use when the user wants the Bohrium tool detail URL for tools like GROMACS, LAMMPS, VASP, OpenMM, or asks whether a software tool has a SciencePedia tool page."
---

# SciencePedia Agent-Tools Lookup

Find Bohrium SciencePedia tool detail pages under `sciencepedia/agent-tools`.

This skill is complementary to `sciencepedia`:

- `sciencepedia` resolves concept keyword pages such as `feynman/keyword/...`
- `sciencepedia-agent-tools` resolves tool entity pages such as `agent-tools/gromacs_gromacs`

## When to Use

- User asks for the Bohrium tool page for a software package
- User wants tool-detail links for GROMACS, LAMMPS, VASP, OpenMM, Quantum ESPRESSO, etc.
- A blog/article pipeline needs to link product or software entities, not just scientific concepts

## How to Run

```bash
# Refresh local cache from Bohrium sitemap
python3 scripts/lookup.py --refresh

# Look up one or more tools
python3 scripts/lookup.py "gromacs" "lammps"

# Return more candidates
python3 scripts/lookup.py --top 5 "quantum espresso"
```

## Data Source

The script builds a local lookup cache from Bohrium sitemap files:

- `https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_1.xml`
- `https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_2.xml`

Resolved URLs follow this pattern:

- `https://www.bohrium.com/en/sciencepedia/agent-tools/{slug}`

## Output

The script returns JSON with:

- `slug`
- `name`
- `url`
- `match_type`
- `score`

## Notes

- Exact duplicated slugs like `gromacs_gromacs` and `lammps_lammps` are preferred when available.
- The first run may take a bit longer because it downloads and caches sitemap data.
