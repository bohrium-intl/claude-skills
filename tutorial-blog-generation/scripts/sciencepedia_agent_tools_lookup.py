#!/usr/bin/env python3
"""
SciencePedia Agent-Tools Lookup: query -> Bohrium tool detail URL.

Usage:
  python sciencepedia_agent_tools_lookup.py --refresh
  python sciencepedia_agent_tools_lookup.py "gromacs" "lammps"
  python sciencepedia_agent_tools_lookup.py --top 5 "quantum espresso"
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

DATA_DIR = Path(__file__).parent / "sp_agent_tools_data"
SLUGS_FILE = DATA_DIR / "slugs.txt"
INDEX_FILE = DATA_DIR / "index.json"


def _curl_text(url: str) -> str:
    # Keep curl usage aligned with existing sciencepedia skill behavior.
    p = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=90)
    if p.returncode != 0:
        raise RuntimeError(f"curl failed: {url}")
    return p.stdout


def download_slugs() -> list[str]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out: list[str] = []

    for url in SITEMAP_URLS:
        try:
            xml = _curl_text(url)
            slugs = re.findall(r"/sciencepedia/agent-tools/([^<]+)", xml)
            out.extend(slugs)
            print(f"{url}: {len(slugs)} entries", file=sys.stderr)
        except Exception as exc:
            print(f"WARN {url}: {exc}", file=sys.stderr)

    # Deduplicate while preserving order.
    deduped = list(dict.fromkeys(out))
    SLUGS_FILE.write_text("\n".join(deduped) + "\n", encoding="utf-8")
    build_index(deduped)
    print(f"Total agent-tools entries: {len(deduped)}", file=sys.stderr)
    return deduped


def slug_to_name(slug: str) -> str:
    return slug.replace("_", " ").replace("-", " ")


def build_index(slugs: list[str]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for slug in slugs:
        name = slug_to_name(slug)
        tokens = sorted(set(re.findall(r"[a-z0-9]+", name.lower())))
        index[slug] = {"name": name, "tokens": tokens}
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return index


def load_index() -> dict[str, dict]:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    if SLUGS_FILE.exists():
        slugs = [x.strip() for x in SLUGS_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]
        return build_index(slugs)
    slugs = download_slugs()
    if not slugs:
        return {}
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def _format(hits: list[tuple[str, str, str, float]]) -> list[dict]:
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


def search_one(query: str, index: dict[str, dict], top_n: int = 3) -> list[dict]:
    q = query.strip().lower()
    q_slug = re.sub(r"[\s\-]+", "_", q)
    q_tokens = set(re.findall(r"[a-z0-9]+", q))

    if not q:
        return [{"query": query, "status": "NOT_FOUND"}]

    # Layer 1: direct slug variants.
    direct_variants = [q_slug, f"{q_slug}_{q_slug}"]
    direct_hits = []
    for v in direct_variants:
        if v in index:
            direct_hits.append((v, index[v]["name"], "EXACT", 1.0))
    if direct_hits:
        return _format(direct_hits[:top_n])

    # Layer 2: prefix/suffix strong hint, useful for gromacs/lammps base tools.
    strong = []
    for slug, meta in index.items():
        if slug.startswith(q_slug + "_") or slug.endswith("_" + q_slug):
            strong.append((slug, meta["name"], "SLUG_PREFIX_SUFFIX", 0.98))
    if strong:
        # Prefer exact duplicated slug first (e.g., gromacs_gromacs).
        strong.sort(key=lambda x: (0 if x[0] == f"{q_slug}_{q_slug}" else 1, x[0]))
        return _format(strong[:top_n])

    # Layer 3: exact human name.
    exact_name = [(s, m["name"], "EXACT_NAME", 1.0) for s, m in index.items() if m["name"].lower() == q]
    if exact_name:
        return _format(exact_name[:top_n])

    # Layer 4: substring match.
    contains = []
    for slug, meta in index.items():
        name_l = meta["name"].lower()
        if q in name_l:
            score = len(q) / max(len(name_l), 1)
            contains.append((slug, meta["name"], "CONTAINS", score))
    if contains:
        contains.sort(key=lambda x: -x[3])
        return _format(contains[:top_n])

    # Layer 5: token overlap (F1).
    token_hits = []
    for slug, meta in index.items():
        t = set(meta["tokens"])
        ov = q_tokens & t
        if not ov:
            continue
        precision = len(ov) / max(len(q_tokens), 1)
        recall = len(ov) / max(len(t), 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-9)
        if f1 >= 0.3:
            token_hits.append((slug, meta["name"], "TOKEN_OVERLAP", f1))
    if token_hits:
        token_hits.sort(key=lambda x: -x[3])
        return _format(token_hits[:top_n])

    # Layer 6: fuzzy over names.
    names = {slug: meta["name"] for slug, meta in index.items()}
    close = difflib.get_close_matches(q, [n.lower() for n in names.values()], n=top_n, cutoff=0.55)
    if close:
        rev = {v.lower(): k for k, v in names.items()}
        hits = []
        for nm in close:
            slug = rev[nm]
            score = difflib.SequenceMatcher(None, q, nm).ratio()
            hits.append((slug, names[slug], "FUZZY", score))
        return _format(hits)

    return [{"query": query, "status": "NOT_FOUND", "suggestion": "Try a broader tool phrase."}]


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print('Usage: python sciencepedia_agent_tools_lookup.py [--refresh] [--top N] "query1" ...')
        sys.exit(1)

    if "--refresh" in args:
        download_slugs()
        args.remove("--refresh")
        if not args:
            return

    top_n = 3
    if "--top" in args:
        i = args.index("--top")
        top_n = int(args[i + 1])
        args = args[:i] + args[i + 2 :]

    index = load_index()
    if not index:
        print(json.dumps({"error": "No index available. Try --refresh."}, ensure_ascii=False))
        sys.exit(1)

    out = {q: search_one(q, index, top_n=top_n) for q in args}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
