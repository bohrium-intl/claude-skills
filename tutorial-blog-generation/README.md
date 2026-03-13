# Article Skill Bundle

This bundle contains the non-image skills and helper scripts used to produce the `GROMACS vs LAMMPS` article pipeline sample.

## Included

- `skills/sciencepedia`
  SciencePedia keyword lookup via local sitemap cache.
- `skills/bohrium-lookup`
  Bohrium paper URL lookup by DOI or title.
- `scripts/sciencepedia_agent_tools_lookup.py`
  Lookup for SciencePedia `agent-tools` pages such as `gromacs_gromacs` and `lammps_lammps`.
- `scripts/pipeline_bohrium_paper_resolver.py`
  Resolver that prefers Bohrium paper URLs and falls back when needed.
- `examples/bohrium-blog-pipeline-v2.md`
  Pipeline design document used for this article workflow.
- `examples/gromacs-vs-lammps-comparison-trial.md`
  Final trial article.
- `examples/gromacs-vs-lammps-fact-sheet-2026-03-10.json`
  Verified fact sheet for the article.
- `examples/gromacs-vs-lammps-qa-report-2026-03-10.json`
  QA scoring output for the article.

## Excluded

- Any image-generation skills.
- `nanobanana-image`
- `gpugeek-gemini-3-pro-image`
- Generated cover/infographic image files

## Suggested Usage Order

1. Use `sciencepedia` for keyword terms.
2. Use `sciencepedia_agent_tools_lookup.py` for tool entity pages.
3. Use `bohrium-lookup` for paper URL lookup.
4. Use `pipeline_bohrium_paper_resolver.py` inside the fact-sheet step.
5. Generate article draft.
6. Run QA against the draft.

## Notes

- `sciencepedia` uses sitemap-backed local cache files.
- `bohrium-lookup` in this bundle uses the standalone built-in-key version that was tested during this article workflow.
- The article sample was validated against sources available on March 10, 2026.
