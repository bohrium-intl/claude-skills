---
name: sciencepedia
description: Look up SciencePedia URLs for scientific concepts from Bohrium's knowledge base. Use when user asks for SciencePedia links, SP URLs, or Bohrium concept references. Triggers on phrases like "find sciencepedia link for [concept]", "get sp url for [concept]", "sciencepedia [concept]", or "refresh sciencepedia index".
---

# SciencePedia URL Lookup

Look up URLs for scientific concepts in Bohrium's SciencePedia database (~145k concepts).

## Lookup Concepts

```bash
python3 scripts/lookup.py "concept1" "concept2" "concept3"
python3 scripts/lookup.py --top 5 "quantum"
```

Searches 145K+ SciencePedia entries using 5-layer matching:
1. Exact slug match
2. Exact name match (case-insensitive)
3. Substring / token overlap
4. Token overlap (F1 scored)
5. Fuzzy match (difflib)

**Output:** JSON with slug, name, url, match_type, and score for each query.

**Options:**
- `--top N` - Number of results per query (default: 3)
- `--refresh` - Re-download sitemaps and rebuild index

## Refresh Index

Update the local concept cache:

```bash
python3 scripts/lookup.py --refresh
```

Downloads sitemaps from Bohrium CDN and rebuilds `data/index.json`.

## URL Pattern

All concept URLs follow: `https://www.bohrium.com/en/sciencepedia/feynman/keyword/{slug}`

Where `{slug}` is lowercase with underscores (e.g., `density_functional_theory`).
