#!/usr/bin/env python3
"""Look up paper info on Bohrium by DOI or title.

Usage:
    python3 bohrium_lookup.py --doi "10.1234/example"
    python3 bohrium_lookup.py --title "Attention Is All You Need"
    python3 bohrium_lookup.py --doi "10.1234/example" --title "Fallback Title"

Returns JSON with paper URL, metadata, and author info from Bohrium's database.
Credentials are built-in — no external .env file needed.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests not installed. Run: pip install requests"}))
    sys.exit(1)

# Built-in credentials
ACCESS_KEY = "CPCMd3FEV1VONLrNOfN3VujPlN1xbIlj"
ACCESS_SECRET = "41aILE5MFU9ufWkKTXeOsT7igiNRQqhS"
API_BASE = "https://security.bohrium.com/paper/pass"


def get_digester(access_key: str, access_secret: str) -> str:
    """Generate SHA-512 digest for Bohrium API authentication."""
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    current_minutes = now.strftime("%Y%m%d%H%M")
    data = access_key + access_secret[:10] + current_minutes
    return hashlib.sha512(data.encode()).hexdigest()


def lookup_by_doi(doi: str) -> dict:
    """Look up paper by DOI."""
    digester = get_digester(ACCESS_KEY, ACCESS_SECRET)
    payload = {
        "accessKey": ACCESS_KEY,
        "digester": digester,
        "dois": [doi],
    }
    resp = requests.post(f"{API_BASE}/dois", json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("data", {}) or {}
    return data.get(doi, {}) or {}


def lookup_by_title(title: str) -> dict:
    """Look up paper by English title."""
    digester = get_digester(ACCESS_KEY, ACCESS_SECRET)
    payload = {
        "accessKey": ACCESS_KEY,
        "digester": digester,
        "titles": [{"enName": title}],
    }
    resp = requests.post(f"{API_BASE}/title", json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("data", {}) or {}
    return data.get(title, {}) or {}


def format_result(raw: dict) -> dict:
    """Format raw API response into clean output."""
    if not raw:
        return {"found": False}

    title = raw.get("enName", "")
    slug = raw.get("title", "")  # API returns slug in "title" field
    paper_id = raw.get("paperId", "")
    pub_id = raw.get("publicationId", "")

    bohrium_url = ""
    if slug and paper_id and pub_id:
        bohrium_url = f"https://www.bohrium.com/en/paper-details/{slug}/{paper_id}-{pub_id}"

    authors = raw.get("authors", [])
    if isinstance(authors, list):
        author_names = [a.get("name", a) if isinstance(a, dict) else str(a) for a in authors]
    else:
        author_names = []

    return {
        "found": True,
        "title": title,
        "bohrium_url": bohrium_url,
        "doi_url": raw.get("paperUrl", ""),
        "authors": author_names,
        "journal": raw.get("publicationEnName", ""),
        "publication_date": raw.get("coverDateStart", ""),
        "citations": int(raw.get("citationNums", 0) or 0),
        "popularity": raw.get("popularity", 0),
        "has_pdf": bool(raw.get("pdfFlag")),
        "open_access": str(raw.get("openAccess", "0")) == "1",
        "doi": raw.get("doi", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Look up paper on Bohrium")
    parser.add_argument("--doi", help="Paper DOI")
    parser.add_argument("--title", help="Paper English title")
    args = parser.parse_args()

    if not args.doi and not args.title:
        parser.error("Provide at least one of --doi or --title")

    result = {}

    # Try DOI first (more precise)
    if args.doi:
        try:
            raw = lookup_by_doi(args.doi)
            result = format_result(raw)
        except Exception as e:
            result = {"error": f"DOI lookup failed: {e}"}

    # Fall back to title if DOI didn't work
    if (not result or not result.get("found")) and args.title:
        try:
            raw = lookup_by_title(args.title)
            result = format_result(raw)
        except Exception as e:
            if not result or "error" not in result:
                result = {"error": f"Title lookup failed: {e}"}

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
