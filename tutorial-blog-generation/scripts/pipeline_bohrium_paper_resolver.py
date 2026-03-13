#!/usr/bin/env python3
"""Resolve paper citations to Bohrium URLs when credentials are available.

Usage:
  python pipeline_bohrium_paper_resolver.py --in papers.json --out resolved.json
  python pipeline_bohrium_paper_resolver.py --in papers.json --out resolved.json --env C:/path/.env

Input schema (JSON list):
[
  {"title": "...", "doi": "...", "url": "https://arxiv.org/abs/..."}
]

Output adds:
- bohrium_url
- resolution_status: "bohrium" | "fallback"
- resolution_reason
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

API_BASE = "https://security.bohrium.com/paper/pass"
DEFAULT_ENV_PATH = Path.home() / "content_writer" / "blog" / ".env"


def load_env_file(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    out: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def get_credentials(env_path: Optional[Path]) -> Dict[str, str]:
    key = os.getenv("DOI_API_ACCESS_KEY", "").strip()
    secret = os.getenv("DOI_API_ACCESS_SECRET", "").strip()
    if key and secret:
        return {"key": key, "secret": secret, "source": "environment variables"}

    path = env_path or DEFAULT_ENV_PATH
    data = load_env_file(path)
    key = data.get("DOI_API_ACCESS_KEY", "").strip()
    secret = data.get("DOI_API_ACCESS_SECRET", "").strip()
    if key and secret:
        return {"key": key, "secret": secret, "source": str(path)}

    return {"key": "", "secret": "", "source": str(path)}


def get_digester(access_key: str, access_secret: str) -> str:
    # Keep the same signing logic as the skill script: Asia/Shanghai minute granularity.
    tz = timezone(timedelta(hours=8))
    current_minutes = datetime.now(tz).strftime("%Y%m%d%H%M")
    msg = access_key + access_secret[:10] + current_minutes
    return hashlib.sha512(msg.encode("utf-8")).hexdigest()


def bohrium_lookup_by_doi(doi: str, access_key: str, access_secret: str) -> Dict[str, Any]:
    payload = {
        "accessKey": access_key,
        "digester": get_digester(access_key, access_secret),
        "dois": [doi],
    }
    resp = requests.post(f"{API_BASE}/dois", json=payload, timeout=30)
    resp.raise_for_status()
    data = (resp.json().get("data") or {}).get(doi) or {}
    return data


def bohrium_lookup_by_title(title: str, access_key: str, access_secret: str) -> Dict[str, Any]:
    payload = {
        "accessKey": access_key,
        "digester": get_digester(access_key, access_secret),
        "titles": [{"enName": title}],
    }
    resp = requests.post(f"{API_BASE}/title", json=payload, timeout=30)
    resp.raise_for_status()
    data = (resp.json().get("data") or {}).get(title) or {}
    return data


def build_bohrium_url(raw: Dict[str, Any]) -> str:
    slug = str(raw.get("title") or "").strip()
    paper_id = str(raw.get("paperId") or "").strip()
    pub_id = str(raw.get("publicationId") or "").strip()
    if slug and paper_id and pub_id:
        return f"https://www.bohrium.com/en/paper-details/{slug}/{paper_id}-{pub_id}"
    return ""


def resolve_one(p: Dict[str, Any], creds: Dict[str, str]) -> Dict[str, Any]:
    out = dict(p)
    out.setdefault("bohrium_url", "")

    if not creds["key"] or not creds["secret"]:
        out["resolution_status"] = "fallback"
        out["resolution_reason"] = "missing_credentials"
        return out

    doi = str(p.get("doi") or "").strip()
    title = str(p.get("title") or "").strip()

    try:
        raw: Dict[str, Any] = {}
        if doi:
            raw = bohrium_lookup_by_doi(doi, creds["key"], creds["secret"])
        if not raw and title:
            raw = bohrium_lookup_by_title(title, creds["key"], creds["secret"])
        url = build_bohrium_url(raw)
        if url:
            out["bohrium_url"] = url
            out["resolution_status"] = "bohrium"
            out["resolution_reason"] = "matched"
        else:
            out["resolution_status"] = "fallback"
            out["resolution_reason"] = "not_found"
    except Exception as exc:
        out["resolution_status"] = "fallback"
        out["resolution_reason"] = f"lookup_error:{exc.__class__.__name__}"

    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", required=True, help="Input JSON file")
    ap.add_argument("--out", dest="outfile", required=True, help="Output JSON file")
    ap.add_argument("--env", dest="envfile", default="", help="Optional .env path")
    args = ap.parse_args()

    infile = Path(args.infile)
    outfile = Path(args.outfile)
    envfile = Path(args.envfile) if args.envfile else None

    papers: List[Dict[str, Any]] = json.loads(infile.read_text(encoding="utf-8-sig"))
    creds = get_credentials(envfile)

    resolved = [resolve_one(p, creds) for p in papers]
    outfile.write_text(json.dumps(resolved, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "total": len(resolved),
        "bohrium": sum(1 for x in resolved if x.get("resolution_status") == "bohrium"),
        "fallback": sum(1 for x in resolved if x.get("resolution_status") == "fallback"),
        "credential_source": creds.get("source", ""),
        "credentials_present": bool(creds.get("key") and creds.get("secret")),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
