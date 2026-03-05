#!/usr/bin/env python3
"""Extract the best figures from a paper PDF using PyMuPDF.

Usage:
    python3 extract_figures.py paper.pdf
    python3 extract_figures.py paper.pdf --top 4
    python3 extract_figures.py paper.pdf --all

By default, picks the top 2 figures from the main body of the paper
(not appendix sample grids). Uses a scoring heuristic that favors
large images from earlier pages with reasonable aspect ratios.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF


def score_figure(img: dict, total_pages: int) -> float:
    """Score a figure for social-media-post suitability.

    Favors:
    - Larger file size (more detail / not an icon)
    - Earlier pages (main body figures, not appendix sample grids)
    - Reasonable aspect ratio (not ultra-wide strips or tiny squares)
    """
    size_score = min(img["size_kb"] / 500, 1.0)  # caps at 500 KB

    # Pages in the first 60% of the paper get full score, then decay
    main_body_cutoff = max(int(total_pages * 0.6), 8)
    if img["page"] <= main_body_cutoff:
        page_score = 1.0
    else:
        # Linear decay for appendix pages
        page_score = max(0, 1.0 - (img["page"] - main_body_cutoff) / (total_pages - main_body_cutoff + 1))

    # Reasonable aspect ratio: 0.3 to 3.0 is ideal
    ratio = img["width"] / max(img["height"], 1)
    if 0.4 <= ratio <= 3.0:
        ratio_score = 1.0
    else:
        ratio_score = 0.5

    # Minimum resolution — prefer images with at least one side > 800px
    max_dim = max(img["width"], img["height"])
    res_score = min(max_dim / 800, 1.0)

    return size_score * 0.3 + page_score * 0.4 + ratio_score * 0.15 + res_score * 0.15


def extract_figures(
    pdf_path: str,
    output_dir: Optional[str] = None,
    min_size: int = 150,
    top_n: int = 2,
    keep_all: bool = False,
    prefix: str = "",
):
    """Extract and rank images from a PDF.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save images. Defaults to ~/Downloads/
        min_size: Minimum width or height in pixels to keep.
        top_n: Number of top figures to save (default 2).
        keep_all: If True, save all figures (ignore top_n).
        prefix: Filename prefix (e.g. "POTD-0216"). Defaults to PDF stem.
    """
    pdf_path = Path(pdf_path).expanduser().resolve()
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if output_dir is None:
        if keep_all:
            output_dir = Path.home() / "Downloads" / f"{pdf_path.stem}_figures"
        else:
            output_dir = Path.home() / "Downloads"
    else:
        output_dir = Path(output_dir).expanduser().resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    if not prefix:
        prefix = pdf_path.stem

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    candidates = []

    for page_num in range(total_pages):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_idx, img_info in enumerate(image_list):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue
            if base_image is None:
                continue

            width = base_image["width"]
            height = base_image["height"]

            if width < min_size and height < min_size:
                continue

            candidates.append({
                "xref": xref,
                "page": page_num + 1,
                "img_idx": img_idx + 1,
                "width": width,
                "height": height,
                "ext": base_image["ext"],
                "bytes": base_image["image"],
                "size_kb": len(base_image["image"]) / 1024,
            })

    doc.close()

    if not candidates:
        print("No figures found (all images were below minimum size threshold).")
        return

    # Score and rank
    for img in candidates:
        img["score"] = score_figure(img, total_pages)

    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Decide which to keep
    to_save = candidates if keep_all else candidates[:top_n]

    # Save
    saved = []
    for i, img in enumerate(to_save, 1):
        if keep_all:
            filename = f"page{img['page']}_img{img['img_idx']}_{img['width']}x{img['height']}.{img['ext']}"
        else:
            filename = f"{prefix}-fig{i}-p{img['page']}.{img['ext']}"

        filepath = output_dir / filename
        with open(filepath, "wb") as f:
            f.write(img["bytes"])
        img["file"] = str(filepath)
        saved.append(img)

    # Print summary
    print(f"\nScanned {len(candidates)} images from {pdf_path.name} ({total_pages} pages)")
    print(f"Saved top {len(saved)} figure{'s' if len(saved) != 1 else ''}:\n")

    for i, img in enumerate(saved, 1):
        print(f"  {i}. {Path(img['file']).name}")
        print(f"     Page {img['page']} | {img['width']}x{img['height']} | {img['size_kb']:.0f} KB | score {img['score']:.2f}")

    if not keep_all and len(candidates) > top_n:
        print(f"\n  ({len(candidates) - top_n} other images skipped. Use --all to save everything.)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract best figures from a paper PDF")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: ~/Downloads/)")
    parser.add_argument("--top", type=int, default=2, help="Number of top figures to keep (default: 2)")
    parser.add_argument("--all", action="store_true", help="Save all figures instead of just top N")
    parser.add_argument("--prefix", "-p", default="", help="Filename prefix (default: PDF filename stem)")
    parser.add_argument("--min-size", type=int, default=150, help="Minimum pixel dimension (default: 150)")
    args = parser.parse_args()
    extract_figures(args.pdf, args.output_dir, args.min_size, args.top, args.all, args.prefix)
