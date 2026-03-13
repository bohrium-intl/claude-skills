#!/usr/bin/env python3
"""
SciencePedia Lookup — fuzzy keyword → URL matcher.

Usage:
    python3 lookup.py "protein folding" "CRISPR" "base editing"
    python3 lookup.py --top 5 "quantum"
    python3 lookup.py --refresh          # re-download sitemaps

Searches 145K+ SciencePedia entries using layered matching:
  Layer 1: Exact match
  Layer 2: Substring / token overlap
  Layer 3: Fuzzy match (difflib)
"""

import sys
import os
import json
import difflib
import re
import subprocess
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────

BASE_URL = "https://www.bohrium.com/en/sciencepedia/feynman/keyword/"
SITEMAP_URLS = [
    f"https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_keyword_{i}.xml"
    for i in range(1, 5)  # 1-4
]
DATA_DIR = Path(__file__).parent.parent / "data"
SLUGS_FILE = DATA_DIR / "slugs.txt"
INDEX_FILE = DATA_DIR / "index.json"  # precomputed search index

# ── Data Loading ────────────────────────────────────────────────────────────

def download_slugs():
    """Download all slugs from sitemaps via curl + grep."""
    print("Downloading sitemaps...", file=sys.stderr)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_slugs = []

    for url in SITEMAP_URLS:
        try:
            result = subprocess.run(
                ["curl", "-s", url],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                # extract slugs from XML
                slugs = re.findall(r'feynman/keyword/([^<]+)', result.stdout)
                all_slugs.extend(slugs)
                print(f"  {url.split('_')[-1]}: {len(slugs)} entries", file=sys.stderr)
        except Exception as e:
            print(f"  WARN: failed to fetch {url}: {e}", file=sys.stderr)

    if all_slugs:
        SLUGS_FILE.write_text("\n".join(all_slugs) + "\n")
        # rebuild index
        build_index(all_slugs)
        print(f"Total: {len(all_slugs)} entries saved.", file=sys.stderr)
    else:
        print("ERROR: no slugs downloaded. CDN might be down.", file=sys.stderr)

    return all_slugs


def build_index(slugs):
    """Build a search index: slug → human-readable name + tokens."""
    index = {}
    for slug in slugs:
        # decode URL encoding (e.g., %28 → (, %29 → ))
        decoded = slug.replace('%28', '(').replace('%29', ')').replace('%2C', ',')
        # convert to human-readable
        human = decoded.replace('_', ' ')
        # tokenize: split on spaces, remove parens, lowercase
        tokens = set(re.findall(r'[a-z0-9]+', human.lower()))
        index[slug] = {
            "name": human,
            "tokens": list(tokens),
        }

    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False))
    return index


def load_index():
    """Load or build the search index."""
    # try precomputed index first
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())

    # fallback to slugs file
    if SLUGS_FILE.exists():
        slugs = [s.strip() for s in SLUGS_FILE.read_text().splitlines() if s.strip()]
        return build_index(slugs)

    # nothing cached — download
    slugs = download_slugs()
    if not slugs:
        return {}
    return json.loads(INDEX_FILE.read_text())


# ── Search Engine ───────────────────────────────────────────────────────────

def search(query, index, top_n=3):
    """
    Layered search:
      1. Exact slug match
      2. Exact name match (case-insensitive)
      3. Substring match (query in name or name in query)
      4. Token overlap (scored by % of query tokens found)
      5. Fuzzy match (difflib on human-readable names)

    Returns list of (slug, name, url, match_type, score).
    """
    query_clean = query.strip().lower()
    # normalize: hyphens → underscores for slug matching, spaces too
    query_slug = re.sub(r'[\s\-]+', '_', query_clean)
    query_tokens = set(re.findall(r'[a-z0-9]+', query_clean))

    # minimum slug length to avoid matching garbage like "n", "gl", "1"
    MIN_SLUG_LEN = 3

    results = []

    # ── Layer 1: Exact slug match ──
    if query_slug in index:
        entry = index[query_slug]
        results.append((query_slug, entry["name"], "EXACT", 1.0))
        return _format_results(results[:top_n])

    # ── Layer 2: Exact name match (case-insensitive) ──
    for slug, entry in index.items():
        if entry["name"].lower() == query_clean:
            results.append((slug, entry["name"], "EXACT", 1.0))
    if results:
        return _format_results(results[:top_n])

    # ── Layer 2.5: Try slug with hyphens/variants ──
    # e.g., "GLP-1" → try "glp_1", "glp-1", "glp1"
    slug_variants = [
        query_slug,
        query_slug.replace('-', '_'),
        re.sub(r'[_\-]', '', query_slug),  # no separators
        re.sub(r'[_\-]', ' ', query_slug).replace(' ', '_'),  # normalized
    ]
    for variant in slug_variants:
        if variant in index and variant not in [r[0] for r in results]:
            entry = index[variant]
            results.append((variant, entry["name"], "EXACT", 1.0))
    if results:
        return _format_results(results[:top_n])

    # ── Layer 3: Substring match ──
    substring_hits = []
    for slug, entry in index.items():
        if len(slug) < MIN_SLUG_LEN:
            continue  # skip tiny slugs like "n", "gl", "1"
        name_lower = entry["name"].lower()
        if query_clean in name_lower:
            # prefer shorter names (more specific matches)
            score = len(query_clean) / max(len(name_lower), 1)
            substring_hits.append((slug, entry["name"], "CONTAINS", score))
        elif len(name_lower) >= MIN_SLUG_LEN and name_lower in query_clean:
            score = len(name_lower) / max(len(query_clean), 1)
            # only keep if the matched name is meaningfully long
            if score >= 0.3:
                substring_hits.append((slug, entry["name"], "CONTAINED_IN", score))

    if substring_hits:
        substring_hits.sort(key=lambda x: -x[3])
        return _format_results(substring_hits[:top_n])

    # ── Layer 4: Token overlap ──
    token_hits = []
    if query_tokens:
        for slug, entry in index.items():
            if len(slug) < MIN_SLUG_LEN:
                continue
            entry_tokens = set(entry["tokens"])
            overlap = query_tokens & entry_tokens
            if overlap:
                # score = (overlap / query tokens) * (overlap / entry tokens)
                precision = len(overlap) / len(query_tokens)
                recall = len(overlap) / max(len(entry_tokens), 1)
                score = 2 * precision * recall / max(precision + recall, 0.001)  # F1
                if score >= 0.3:  # threshold
                    token_hits.append((slug, entry["name"], "TOKEN_OVERLAP", round(score, 3)))

    if token_hits:
        token_hits.sort(key=lambda x: -x[3])
        return _format_results(token_hits[:top_n])

    # ── Layer 5: Fuzzy match (difflib) ──
    all_names = {slug: entry["name"] for slug, entry in index.items()}
    # get close matches on human-readable names
    close = difflib.get_close_matches(
        query_clean,
        [n.lower() for n in all_names.values()],
        n=top_n,
        cutoff=0.5
    )

    if close:
        # map back to slugs
        name_to_slug = {entry["name"].lower(): slug for slug, entry in index.items()}
        for match_name in close:
            slug = name_to_slug.get(match_name)
            if slug:
                score = difflib.SequenceMatcher(None, query_clean, match_name).ratio()
                results.append((slug, index[slug]["name"], "FUZZY", round(score, 3)))
        return _format_results(results[:top_n])

    return [{"query": query, "status": "NOT_FOUND", "suggestion": "Try synonyms or broader terms."}]


def _format_results(hits):
    """Format results with URLs."""
    return [
        {
            "slug": slug,
            "name": name,
            "url": BASE_URL + slug,
            "match_type": match_type,
            "score": score,
        }
        for slug, name, match_type, score in hits
    ]


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python3 lookup.py \"concept1\" \"concept2\" ...")
        print("       python3 lookup.py --refresh")
        print("       python3 lookup.py --top 5 \"quantum\"")
        sys.exit(1)

    # handle --refresh
    if "--refresh" in args:
        download_slugs()
        print("Cache refreshed.", file=sys.stderr)
        args.remove("--refresh")
        if not args:
            sys.exit(0)

    # handle --top N
    top_n = 3
    if "--top" in args:
        idx = args.index("--top")
        top_n = int(args[idx + 1])
        args = args[:idx] + args[idx + 2:]

    # load index
    index = load_index()
    if not index:
        print("ERROR: No data. Run with --refresh first.", file=sys.stderr)
        sys.exit(1)

    # search each query
    all_results = {}
    for query in args:
        all_results[query] = search(query, index, top_n=top_n)

    # output
    print(json.dumps(all_results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
