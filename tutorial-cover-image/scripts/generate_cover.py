#!/usr/bin/env python3
"""Generate a Bohrium tutorial cover image from an article index.md."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image
import yaml

PALETTE = [
    "#EDE7F6",
    "#F6EAF2",
    "#EAF4FF",
    "#FFF7DB",
    "#EEF3EC",
    "#F3EEF9",
    "#F9E3E3",
    "#FBE8EF",
    "#FDEBDD",
]

STYLE_NOTES = (
    "minimal editorial cover illustration, flat vector-like composition, "
    "single calm pastel background, one centered symbolic motif, black hand-drawn ink lines, "
    "paper-cut off-white geometric accents, lots of negative space, quiet premium design, "
    "thumbnail-friendly, no text, no logos, no UI screenshots, no photorealism, no 3D render, "
    "no clutter, no saturated colors, no gradient-heavy lighting"
)

FALLBACK_MOTIF = "an open notebook with a small connected-node diagram held by simple abstract hands"

MOTIF_RULES = [
    (("code", "coding", "programming", "debug", "review", "repo", "git"), "curly braces and a magnifying glass"),
    (("agent", "workflow", "automation", "orchestration"), "a simple node graph emerging from an open notebook"),
    (("data", "analysis", "analytics", "benchmark", "metrics"), "clean chart axes with a rising line and a guiding hand"),
    (("research", "paper", "literature", "citation", "study"), "an open paper with a tiny knowledge graph"),
    (("finance", "risk", "compliance"), "a stepped block shape with a black hand-drawn upward path"),
    (("search", "retrieval", "rag"), "stacked documents connected to a retrieval node"),
    (("vision", "image", "multimodal"), "an abstract eye with geometric overlays"),
    (("tool", "plugin", "integration", "comparison"), "a modular block diagram inside an open book"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", help="Path to article index.md")
    parser.add_argument(
        "--provider",
        default="auto",
        choices=["auto", "google", "gpugeek"],
        help="Image backend. 'auto' uses gpugeek when api-base contains gpugeek, otherwise google.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GEMINI_API_KEY", ""),
        help="API key. Defaults to GEMINI_API_KEY env var.",
    )
    parser.add_argument(
        "--api-base",
        default="https://api.gpugeek.com",
        help="API base URL. Google Gemini: https://generativelanguage.googleapis.com/v1beta. GpuGeek: https://api.gpugeek.com.",
    )
    parser.add_argument(
        "--model",
        default="Vendor2/Gemini-3-Pro-Image",
        help="Image model name.",
    )
    parser.add_argument(
        "--image-size",
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Requested size for Google Gemini image models.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Output image path. Defaults to <article-dir>/cover-image.png",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview chosen motif/background without calling the image API.",
    )
    return parser.parse_args()


def load_article(article_path: Path) -> tuple[dict[str, Any], str]:
    raw = article_path.read_text(encoding="utf-8").lstrip("\ufeff")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No frontmatter found in {article_path}")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    return frontmatter, body


def first_paragraph(body: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    for paragraph in paragraphs:
        if not paragraph.startswith("#") and not paragraph.startswith("!"):
            return re.sub(r"\s+", " ", paragraph)
    return ""


def extract_headings(body: str, limit: int = 4) -> list[str]:
    headings = re.findall(r"^##+\s+(.+?)(?:\{#.*?\})?$", body, flags=re.MULTILINE)
    cleaned: list[str] = []
    for heading in headings:
        heading = re.sub(r"\{#.*?\}", "", heading).strip()
        if heading:
            cleaned.append(heading)
    return cleaned[:limit]


def choose_background(slug: str) -> str:
    digest = hashlib.md5(slug.encode("utf-8")).hexdigest()
    return PALETTE[int(digest[:8], 16) % len(PALETTE)]


def choose_motif(text: str) -> str:
    lower = text.lower()
    for keywords, motif in MOTIF_RULES:
        if any(keyword in lower for keyword in keywords):
            return motif
    return FALLBACK_MOTIF


def build_prompt(frontmatter: dict[str, Any], body: str, article_path: Path) -> dict[str, Any]:
    title = (
        frontmatter.get("page_h1_title")
        or frontmatter.get("title")
        or article_path.parent.name.replace("-", " ")
    )
    summary = frontmatter.get("summary") or frontmatter.get("meta_description") or first_paragraph(body)
    tags = frontmatter.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    headings = extract_headings(body)
    slug = frontmatter.get("url_slug") or article_path.parent.name
    background = choose_background(slug)
    motif = choose_motif(" ".join([title, summary, " ".join(tags), " ".join(headings)]))

    prompt = textwrap.dedent(
        f"""
        Create a 16:9 tutorial or tool-comparison cover image for a science/AI blog.

        Style lock:
        - {STYLE_NOTES}
        - overall palette must stay harmonious and unified, using low-saturation pastel tones only
        - background may be softly designed in pale lavender, pale pink, pale blue, pale yellow, pale red, or pale orange tones
        - use {background} as the dominant background color
        - foreground and background colors must feel coordinated; no abrupt contrast or clashing accent colors
        - central motif should be: {motif}
        - motif should feel conceptual, editorial, and lightly academic rather than literal
        - keep composition simple: one main motif centered slightly above middle, generous empty space around it
        - use a subtle off-white cut-paper shape behind the motif to anchor it
        - linework should look like confident hand-drawn ink strokes

        Article context:
        - title: {title}
        - summary: {summary}
        - tags: {", ".join(tags) if tags else "none"}
        - section cues: {", ".join(headings) if headings else "none"}

        Avoid:
        - any text, letters, captions, UI panels, browser chrome, code screenshots
        - multiple competing objects
        - bright or saturated accent colors
        - realistic humans, faces, or photographic scenes
        - dark background
        """
    ).strip()

    return {
        "background": background,
        "motif": motif,
        "prompt": prompt,
    }


def call_google(api_base: str, model: str, api_key: str, prompt: str, image_size: str) -> dict[str, Any]:
    url = f"{api_base.rstrip('/')}/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["Image"],
            "imageConfig": {
                "aspectRatio": "16:9",
                "imageSize": image_size,
            },
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google Gemini API error {exc.code}: {body}") from exc


def extract_google_image_bytes(response: dict[str, Any]) -> bytes:
    for candidate in response.get("candidates") or []:
        for part in ((candidate.get("content") or {}).get("parts") or []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and inline_data.get("data"):
                return base64.b64decode(inline_data["data"])
    raise RuntimeError("No inline image data found in Google Gemini response")


def call_gpugeek(api_base: str, model: str, api_key: str, prompt: str) -> dict[str, Any]:
    url = f"{api_base.rstrip('/')}/predictions"
    payload = {
        "model": model,
        "input": {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
        },
    }
    last_error: Exception | None = None
    for attempt in range(3):
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "Stream": "false",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in (502, 503, 504) and attempt < 2:
                time.sleep(3 * (attempt + 1))
                last_error = RuntimeError(f"GpuGeek transient error {exc.code}: {body}")
                continue
            raise RuntimeError(f"GpuGeek API error {exc.code}: {body}") from exc
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"GpuGeek request failed after retries: {last_error}")


def extract_gpugeek_image_bytes(response: dict[str, Any]) -> bytes:
    if response.get("status") != "succeeded":
        raise RuntimeError(f"GpuGeek prediction did not succeed: {json.dumps(response, ensure_ascii=False)}")
    output = response.get("output")
    if isinstance(output, str) and output.startswith("http"):
        with urllib.request.urlopen(output, timeout=180) as response_stream:
            return response_stream.read()
    if isinstance(output, list):
        for item in output:
            if isinstance(item, str) and item.startswith("http"):
                with urllib.request.urlopen(item, timeout=180) as response_stream:
                    return response_stream.read()
            if isinstance(item, str) and item.startswith("data:image/") and ";base64," in item:
                _, encoded = item.split(";base64,", 1)
                return base64.b64decode(encoded)
            if isinstance(item, str):
                try:
                    return base64.b64decode(item)
                except Exception:
                    pass
    raise RuntimeError("No downloadable image found in GpuGeek response")


def normalize_to_cover(image_bytes: bytes, target_width: int = 1600, target_height: int = 900) -> bytes:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    source_ratio = image.width / image.height
    target_ratio = target_width / target_height
    if source_ratio > target_ratio:
        crop_width = int(image.height * target_ratio)
        left = max((image.width - crop_width) // 2, 0)
        image = image.crop((left, 0, left + crop_width, image.height))
    elif source_ratio < target_ratio:
        crop_height = int(image.width / target_ratio)
        top = max((image.height - crop_height) // 2, 0)
        image = image.crop((0, top, image.width, top + crop_height))
    image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def main() -> int:
    args = parse_args()
    article_path = Path(args.article).resolve()
    if not article_path.exists():
        print(f"Article not found: {article_path}", file=sys.stderr)
        return 1
    if article_path.name != "index.md":
        print("Expected an article index.md path", file=sys.stderr)
        return 1

    frontmatter, body = load_article(article_path)
    brief = build_prompt(frontmatter, body, article_path)
    output_image = Path(args.output).resolve() if args.output else article_path.parent / "cover-image.png"
    output_image.parent.mkdir(parents=True, exist_ok=True)

    print(f"Background: {brief['background']}")
    print(f"Motif: {brief['motif']}")

    if args.dry_run:
        print("Dry run complete; API not called.")
        return 0

    if not args.api_key:
        print("Missing API key. Pass --api-key or set GEMINI_API_KEY.", file=sys.stderr)
        return 1

    provider = args.provider
    if provider == "auto":
        provider = "gpugeek" if "gpugeek" in args.api_base.lower() else "google"

    if provider == "google":
        response = call_google(args.api_base, args.model, args.api_key, brief["prompt"], args.image_size)
        image_bytes = extract_google_image_bytes(response)
    else:
        response = call_gpugeek(args.api_base, args.model, args.api_key, brief["prompt"])
        image_bytes = extract_gpugeek_image_bytes(response)

    output_image.write_bytes(normalize_to_cover(image_bytes))
    print(f"Image saved: {output_image}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
