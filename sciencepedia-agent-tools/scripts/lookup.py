#!/usr/bin/env python3
"""
SciencePedia Agent-Tools Lookup: query -> Bohrium tool detail URL.

Usage:
    python3 lookup.py --refresh
    python3 lookup.py "gromacs" "lammps"
    python3 lookup.py --top 5 "quantum espresso"
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

BASE_URL = "https://www.bohrium.com/en/sciencepedia/agent-tools/"
SITEMAP_URLS = [
    "https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_1.xml",
    "https://cdn.bohrium.com/bohrium/web/static/sitemap/sp-tools/sitemap_2.xml",
]

DATA_DIR = Path(__file__).parent.parent / "data"
SLUGS_FILE = DATA_DIR / "slugs.txt"
INDEX_FILE = DATA_DIR / "index.json"


def curl_text(url: str) -> str:
    result = subprocess.run(
        ["curl", "-s", url],
        capture_output=True,
        text=True,
        timeout=90,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed for {url}")
    return result.stdout


def build_index(slugs: list[str]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for slug in slugs:
        name = slug.replace("_", " ").replace("-", " ")
        tokens = sorted(set(re.findall(r"[a-z0-9]+", name.lower())))
        index[slug] = {"name": name, "tokens": tokens}

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return index


def download_slugs() -> list[str]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_slugs: list[str] = []

    for url in SITEMAP_URLS:
        try:
            xml = curl_text(url)
            slugs = re.findall(r"/sciencepedia/agent-tools/([^<]+)", xml)
            all_slugs.extend(slugs)
            print(f"{url}: {len(slugs)} entries", file=sys.stderr)
        except Exception as exc:
            print(f"WARN {url}: {exc}", file=sys.stderr)

    deduped = list(dict.fromkeys(all_slugs))
    SLUGS_FILE.write_text("\n".join(deduped) + "\n", encoding="utf-8")
    build_index(deduped)
    print(f"Total agent-tools entries: {len(deduped)}", file=sys.stderr)
    return deduped


def load_index() -> dict[str, dict]:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    if SLUGS_FILE.exists():
        slugs = [
            line.strip()
            for line in SLUGS_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return build_index(slugs)
    slugs = download_slugs()
    return build_index(slugs) if slugs else {}


def format_hits(hits: list[tuple[str, str, str, float]]) -> list[dict]:
    return [
        {
            "slug": slug,
            "name": name,
            "url": BASE_URL + slug,
            "match_type": match_type,
            "score": round(score, 3),
        }
        for slug, name, match_type, score in hits
    ]


def search(query: str, index: dict[str, dict], top_n: int = 3) -> list[dict]:
    query_clean = query.strip().lower()
    if not query_clean:
        return [{"query": query, "status": "NOT_FOUND"}]

    query_slug = re.sub(r"[\s\-]+", "_", query_clean)
    query_tokens = set(re.findall(r"[a-z0-9]+", query_clean))

    exact_variants = [query_slug, f"{query_slug}_{query_slug}"]
    exact_hits = []
    for variant in exact_variants:
        if variant in index:
            exact_hits.append((variant, index[variant]["name"], "EXACT", 1.0))
    if exact_hits:
        return format_hits(exact_hits[:top_n])

    strong_hits = []
    for slug, meta in index.items():
        if slug.startswith(query_slug + "_") or slug.endswith("_" + query_slug):
            strong_hits.append((slug, meta["name"], "SLUG_PREFIX_SUFFIX", 0.98))
    if strong_hits:
        strong_hits.sort(key=lambda x: (0 if x[0] == f"{query_slug}_{query_slug}" else 1, x[0]))
        return format_hits(strong_hits[:top_n])

    exact_name_hits = []
    for slug, meta in index.items():
        if meta["name"].lower() == query_clean:
            exact_name_hits.append((slug, meta["name"], "EXACT_NAME", 1.0))
    if exact_name_hits:
        return format_hits(exact_name_hits[:top_n])

    contains_hits = []
    for slug, meta in index.items():
        name_lower = meta["name"].lower()
        if query_clean in name_lower:
            score = len(query_clean) / max(len(name_lower), 1)
            contains_hits.append((slug, meta["name"], "CONTAINS", score))
    if contains_hits:
        contains_hits.sort(key=lambda x: -x[3])
        return format_hits(contains_hits[:top_n])

    token_hits = []
    for slug, meta in index.items():
        entry_tokens = set(meta["tokens"])
        overlap = query_tokens & entry_tokens
        if not overlap:
            continue
        precision = len(overlap) / max(len(query_tokens), 1)
        recall = len(overlap) / max(len(entry_tokens), 1)
        score = 2 * precision * recall / max(precision + recall, 1e-9)
        if score >= 0.3:
            token_hits.append((slug, meta["name"], "TOKEN_OVERLAP", score))
    if token_hits:
        token_hits.sort(key=lambda x: -x[3])
        return format_hits(token_hits[:top_n])

    all_names = {slug: meta["name"] for slug, meta in index.items()}
    close_matches = difflib.get_close_matches(
        query_clean,
        [name.lower() for name in all_names.values()],
        n=top_n,
        cutoff=0.55,
    )
    if close_matches:
        name_to_slug = {name.lower(): slug for slug, name in all_names.items()}
        hits = []
        for match in close_matches:
            slug = name_to_slug[match]
            score = difflib.SequenceMatcher(None, query_clean, match).ratio()
            hits.append((slug, all_names[slug], "FUZZY", score))
        return format_hits(hits[:top_n])

    return [{"query": query, "status": "NOT_FOUND", "suggestion": "Try a broader tool phrase."}]


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print('Usage: python3 lookup.py [--refresh] [--top N] "query1" ...')
        sys.exit(1)

    if "--refresh" in args:
        download_slugs()
        args.remove("--refresh")
        if not args:
            return

    top_n = 3
    if "--top" in args:
        idx = args.index("--top")
        top_n = int(args[idx + 1])
        args = args[:idx] + args[idx + 2 :]

    index = load_index()
    if not index:
        print(json.dumps({"error": "No index available. Try --refresh."}, ensure_ascii=False))
        sys.exit(1)

    output = {query: search(query, index, top_n=top_n) for query in args}
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
