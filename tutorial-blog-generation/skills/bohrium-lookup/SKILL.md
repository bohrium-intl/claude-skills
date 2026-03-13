---
name: bohrium-lookup
description: "Look up paper links on Bohrium (玻尔) by DOI or title. Use when the user wants to find a paper on Bohrium, get a Bohrium paper URL, or says things like '查论文链接', 'bohrium link', '玻尔链接', 'find paper on bohrium', '论文在玻尔上有吗', 'get bohrium url'. Also trigger when the user provides a DOI or paper title and wants to know if it's on Bohrium."
---

# Bohrium Paper Lookup

Find papers on bohrium.com and return their direct URL + metadata. Everything is self-contained — no external config files or credentials needed.

## When to Use

- User wants a Bohrium paper link
- User provides a DOI or paper title and wants the Bohrium URL
- User asks if a paper exists on Bohrium

## How to Run

The lookup script is bundled with this skill. Only dependency is Python `requests` (usually pre-installed).

```bash
# By DOI (preferred, more precise)
python3 ~/.claude/skills/bohrium-lookup/scripts/bohrium_lookup.py --doi "10.1234/example"

# By title (fallback if no DOI)
python3 ~/.claude/skills/bohrium-lookup/scripts/bohrium_lookup.py --title "Paper Title Here"

# Both (tries DOI first, falls back to title)
python3 ~/.claude/skills/bohrium-lookup/scripts/bohrium_lookup.py --doi "10.1234/example" --title "Paper Title"
```

## Input

User provides one or more of:
- **DOI** (e.g., `10.1038/s41586-024-07892`)
- **Paper title** (English)
- **arXiv link** — extract the paper title or DOI from the arXiv page first, then look up on Bohrium

If the user gives an arXiv link, fetch the arXiv page to get the title and DOI, then use those for the Bohrium lookup.

## Output

Present results clearly:

**If found:**
```
论文在 Bohrium 上找到了：

标题: {title}
Bohrium 链接: {bohrium_url}
作者: {authors}
期刊: {journal}
引用数: {citations}
DOI: {doi}
```

**If not found:**
```
这篇论文在 Bohrium 上没有找到。可以手动去 bohrium.com 搜索确认。
```

## Troubleshooting

If `requests` is not installed, run `pip install requests`.
