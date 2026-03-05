---
name: x-post-image
description: >
  Generate companion images for X (Twitter) posts using Python (matplotlib + Pillow).
  Use when user says "generate image", "配图", "做图", "make a chart", "create a graphic",
  "生成配图", "画个图", or when an X post needs a visual.
  Supports: cost comparison charts, Valentine/holiday cards, announcement graphics,
  data visualizations, text-heavy social media images.
  Triggers alongside x-news-post when images are needed for posts.
---

# X Post Image Generator

Generate publication-ready images for social media posts using Python's matplotlib and Pillow (PIL). No external APIs needed — everything runs locally using system fonts.

## Dependencies

- **Python 3** (system default)
- **Pillow (PIL)** — `pip3 install Pillow` (usually pre-installed)
- **matplotlib** — `pip3 install matplotlib`

Check availability before generating:
```bash
python3 -c "import matplotlib; from PIL import Image; print('OK')"
```
If missing, install: `python3 -m pip install matplotlib Pillow --quiet`

## Image Types

### 1. Data Comparison Chart (matplotlib)

**Use for:** Cost comparisons, benchmark scores, performance metrics, any numeric data.

**Template pattern:**
- Dark theme (`#0d1117` background) for tech/AI content
- Horizontal bar chart for clear label readability
- Color coding: highlight key bars (red for expensive, blue for cheap, green for winner)
- Title + subtitle at top, data labels on bars
- Resolution: `figsize=(12, 6.75)` at `dpi=200` → 2400x1350px

**Key settings:**
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — ALWAYS set this
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6.75))
fig.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')
# ... build chart ...
plt.savefig(path, dpi=200, facecolor='#0d1117', bbox_inches='tight', pad_inches=0.4)
plt.close()  # Always close to free memory
```

**Style rules:**
- Remove top and right spines
- Grid lines: subtle (`#21262d`), behind bars
- Font: Arial (always available on macOS)
- Y-axis labels: white, 17pt; X-axis: `#8b949e`, 12pt
- Data labels: white, bold, 18pt, positioned right of bars

### 2. Text Card / Announcement Graphic (Pillow)

**Use for:** Valentine's cards, memorial cards, announcement graphics, quote cards, any text-heavy image.

**Template pattern:**
- Gradient background (draw line-by-line for smooth gradient)
- Layered fonts for hierarchy (title → heading → body → caption)
- Center-aligned text with manual vertical spacing
- Resolution: 2400x1350 (render at 2x for sharpness on retina/high-DPI)

**Key settings:**
```python
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1350  # Always 2x for sharpness
img = Image.new('RGB', (W, H), '#1a0a0a')
draw = ImageDraw.Draw(img)

# Gradient background
for y in range(H):
    r = int(base_r + (y/H) * delta_r)
    # ...
    draw.line([(0, y), (W, y)], fill=(r, g, b))
```

**Center-text helper:**
```python
def center_text(draw, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=fill, font=font)
```

### 3. Shapes with Pillow

For simple icons (hearts, stars, arrows), build from geometric primitives:
- Ellipses + polygons for hearts
- Use RGBA layers for compositing: `Image.new('RGBA', ...)` + `Image.alpha_composite()`
- Draw on separate layer, paste with mask

## Available Fonts (macOS)

### Serif (elegant, formal)
| Font | File | Variants | Best for |
|------|------|----------|----------|
| **Didot** | `Didot.ttc` | index 0=Regular, 1=Bold, 2=Italic | Headlines, cards |
| **Baskerville** | `Baskerville.ttc` | Multiple weights | Body text |
| **Bodoni 72** | `Bodoni 72.ttc` | Regular, Bold, Book | Fashion/luxury |
| **Georgia** | `Georgia.ttf` / `Georgia Bold.ttf` / `Georgia Italic.ttf` | Separate files | Body, dates |

### Sans-serif (clean, modern)
| Font | File | Best for |
|------|------|----------|
| **Arial** | `Arial.ttf` / `Arial Bold.ttf` | Charts, data labels |
| **Arial Narrow** | `Arial Narrow.ttf` | Compact labels |
| **Helvetica** | `Helvetica.ttc` | Clean headings |

### Script (handwritten)
| Font | File | Best for |
|------|------|----------|
| **Snell Roundhand** | `SnellRoundhand.ttc` | Invitations, signatures |
| **Brush Script** | `Brush Script.ttf` | Casual handwriting |
| **Zapfino** | `Zapfino.ttf` | Decorative calligraphy |

**Font path prefix:** `/System/Library/Fonts/Supplemental/`

**Loading .ttc (collection) fonts:**
```python
# .ttc files contain multiple faces — use index parameter
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Didot.ttc', 108, index=1)  # Bold
```

**Caution with script fonts:** Snell Roundhand and Zapfino can make alphanumeric strings (like "GPT-4o") illegible. Use serif fonts for anything that must be instantly readable; reserve script fonts for natural-language phrases ("Dear friend,", "With love,").

## Color Palettes

### Dark Tech (AI, data, engineering)
```
Background:  #0d1117
Surface:     #161b22
Border:      #30363d
Grid:        #21262d
Text primary: #ffffff
Text secondary: #8b949e
Accent blue:  #58a6ff
Accent red:   #f85149
Accent green: #3fb950
Accent orange: #d29922
```

### Dark Warm (emotional, editorial, Valentine's)
```
Background:  #1a0a0a
Border:      #3d1515
Heart red:   #8b2233
Text primary: #ffffff
Text warm:   #e8c4c4
Text muted:  #8b949e
Text ghost:  #4a2828
```

## Output Checklist

- [ ] Resolution at least 2400px wide (2x for sharpness)
- [ ] Saved as PNG with `quality=95` (PIL) or `dpi=200` (matplotlib)
- [ ] `matplotlib.use('Agg')` set before any pyplot import
- [ ] `plt.close()` called after saving (prevent memory leaks)
- [ ] Text is legible at thumbnail size (test by squinting)
- [ ] Colors have sufficient contrast (white text on dark bg)
- [ ] No orphaned text (single words on their own line)
- [ ] File saved to user-specified location (default: `~/Downloads/`)

## Aspect Ratios

| Platform | Ratio | Pixels (2x) |
|----------|-------|-------------|
| X (Twitter) timeline | 16:9 | 2400 x 1350 |
| X summary card | 2:1 | 2400 x 1200 |
| LinkedIn post | 1.91:1 | 2400 x 1256 |
| Square (Instagram) | 1:1 | 2400 x 2400 |
