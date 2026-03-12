---
name: tutorial-cover-image
description: >
  Generate Bohrium tutorial and tool-comparison cover images with Gemini image models.
  Use when the user asks for a tutorial cover, tool-comparison cover, blog cover image,
  "cover-image", "封面图", "教程封面", "工具对比封面", or wants a 16:9 pastel editorial
  illustration for a Bohrium article. Tuned for minimal line-art covers with soft,
  low-saturation backgrounds and no text.
---

# Tutorial Cover Image

Generate 16:9 cover images for Bohrium tutorial and tool-comparison articles.

The bundled script is tuned for this house style:
- soft low-saturation pastel background
- coordinated foreground/background colors
- centered editorial motif
- black hand-drawn linework
- no text

## When To Use

Use this skill when the task is to create or refresh a cover image for:
- `content/tutorials/<slug>/index.md`
- tool-comparison articles
- tutorial-like article covers that should match the Bohrium editorial card style

## Command

```bash
python scripts/generate_cover.py path/to/index.md
```

Default output is `cover-image.png` next to the article.

## Common Options

```bash
python scripts/generate_cover.py path/to/index.md \
  --api-key "$GEMINI_API_KEY" \
  --api-base https://api.gpugeek.com \
  --provider gpugeek \
  --model Vendor2/Gemini-3-Pro-Image
```

- `--output path.png` override output path
- `--dry-run` preview chosen motif/background without calling the API
- `--provider google` for Google Gemini public endpoint
- `--provider gpugeek` for GpuGeek image inference

## Dependencies

- Python 3
- `PyYAML`
- `Pillow`

Quick check:

```bash
python -c "import yaml; from PIL import Image; print('OK')"
```

## Workflow

1. Read frontmatter and article body from `index.md`.
2. Infer a motif from title, summary, tags, and headings.
3. Pick a stable low-saturation background color from the built-in palette.
4. Generate one PNG cover image.
5. Save only the PNG file.

## Style Constraints

- Output must be `16:9`
- Background can be pale lavender, pink, blue, yellow, red, orange, or similar muted pastels
- Colors must feel unified; no harsh foreground/background clashes
- No text, captions, logos, screenshots, or realistic scenes

## Output

- `cover-image.png`

If the result is too busy, edit the script's style notes or motif rules and rerun.
