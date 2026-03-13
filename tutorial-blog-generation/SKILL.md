---
name: tutorial-blog-generation
description: >
  Generate Bohrium-style tutorial and comparison blog articles without image generation.
  Use when the user wants a reusable workflow for topic-to-article production, including
  SciencePedia concept links, SciencePedia agent-tool links, Bohrium paper URL resolution,
  fact-sheet assembly, QA scoring, and example outputs for a tutorial or tool-comparison post.
---

# Tutorial Blog Generation

This skill packages the non-image workflow used to produce a full Bohrium tutorial or
tool-comparison article from source discovery through QA.

## Included

- `skills/sciencepedia`
  Concept URL lookup backed by a local sitemap cache.
- `skills/bohrium-lookup`
  Bohrium paper-details lookup by DOI or title.
- `scripts/sciencepedia_agent_tools_lookup.py`
  Lookup for SciencePedia tool pages such as `gromacs_gromacs` and `lammps_lammps`.
- `scripts/pipeline_bohrium_paper_resolver.py`
  Paper resolver that prefers Bohrium URLs and falls back when needed.
- `examples/`
  Working pipeline doc, article draft, fact sheet, and QA report from the GROMACS vs LAMMPS trial.

## When To Use

Use this skill when the task is to:
- generate a tutorial or comparison blog post with Bohrium-compatible references
- resolve SciencePedia concept links and tool links
- resolve paper citations to Bohrium paper-details URLs
- validate output with a fact sheet and QA pass
- study or adapt the sample workflow before automating it further

## Suggested Workflow

1. Use `skills/sciencepedia` to resolve concept terms.
2. Use `scripts/sciencepedia_agent_tools_lookup.py` to resolve tool detail pages.
3. Use `skills/bohrium-lookup` and `scripts/pipeline_bohrium_paper_resolver.py` to map papers to Bohrium URLs.
4. Build the article draft and fact sheet.
5. Run QA and update the final article metadata.

## Notes

- This bundle intentionally excludes image generation.
- The included examples were validated against sources checked on March 10, 2026.
- If you want to productionize the workflow, treat the sample files in `examples/` as test fixtures.
