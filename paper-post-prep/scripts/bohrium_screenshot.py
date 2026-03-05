#!/usr/bin/env python3
"""Take a screenshot of a Bohrium paper page using Playwright.

Usage:
    python3 bohrium_screenshot.py "https://www.bohrium.com/en/paper-details/..." [--output ~/Downloads/POTD-0216-bohrium.png]
"""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def take_screenshot(url: str, output: str = "", wait_ms: int = 3000):
    """Open a Bohrium paper page and take a screenshot.

    Args:
        url: Bohrium paper URL.
        output: Output file path. Defaults to ~/Downloads/bohrium-screenshot.png.
        wait_ms: Time to wait for page to load (ms).
    """
    if not output:
        output = str(Path.home() / "Downloads" / "bohrium-screenshot.png")

    output = str(Path(output).expanduser().resolve())

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})

        print(f"Loading {url} ...")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Extra wait for dynamic content to render
        page.wait_for_timeout(wait_ms)

        # Try to dismiss cookie banners or popups
        for selector in ["button:has-text('Accept')", "button:has-text('Got it')", ".modal-close", "[aria-label='Close']"]:
            try:
                el = page.query_selector(selector)
                if el and el.is_visible():
                    el.click()
                    page.wait_for_timeout(500)
            except Exception:
                pass

        # Crop out the left sidebar and top nav by clipping the main content area
        # Sidebar is ~220px wide, top nav is ~50px tall on Bohrium paper pages
        clip_x = 220
        clip_y = 0
        clip_width = 1600 - clip_x
        clip_height = 940

        page.screenshot(path=output, full_page=False, clip={
            "x": clip_x, "y": clip_y,
            "width": clip_width, "height": clip_height
        })
        browser.close()

    print(f"Screenshot saved: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Screenshot a Bohrium paper page")
    parser.add_argument("url", help="Bohrium paper URL")
    parser.add_argument("--output", "-o", default="", help="Output file path")
    parser.add_argument("--wait", type=int, default=3000, help="Wait time in ms (default: 3000)")
    args = parser.parse_args()
    take_screenshot(args.url, args.output, args.wait)
