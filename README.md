# Bohrium International Claude Skills

<p align="center"><img src="banner.png" width="360"></p>

Shared AI agent skills for the Bohrium international content operations team. These skills work with **Claude Code** and **OpenAI Codex CLI**, powering content workflows across Bohrium's social accounts and platforms.

## Skills Registry

### Account-Specific Skills

| Skill | Account / Pillar | What It Does | Author | Platform |
|-------|-----------------|--------------|--------|----------|
| `x-news-post` | [@BohriumNews](https://x.com/BohriumNews) | Drafts X posts for science/tech news stories | @1021ju | Claude Code |
| `x-post-image` | [@BohriumNews](https://x.com/BohriumNews) | Generates companion images (charts, graphics) for X posts | @1021ju | Claude Code |
| `review` | [@BohriumNews](https://x.com/BohriumNews) / [@BohriumDecoder](https://x.com/BohriumDecoder) | Verifies X post claims, analyzes media context, and generates bilingual reply drafts in multiple styles | @Laurence | OpenAI Codex CLI |
| `sciencepedia-wordcard` | [@BohriumSP](https://x.com/BohriumSP) | Generates PNG word cards for SciencePedia concepts, used as reply attachments | @1021ju | Claude Code |
| `paper-scout` | Paper of the Day ([@Bohrium_AI4S](https://x.com/Bohrium_AI4S) / may move to @BohriumDecoder) | Discovers and ranks trending papers for social posting | @1021ju | Claude Code |
| `paper-post-prep` | Paper of the Day ([@Bohrium_AI4S](https://x.com/Bohrium_AI4S) / may move to @BohriumDecoder) + LinkedIn | Prepares all assets for Paper of the Day posts (includes Bohrium link lookup) | @1021ju | Claude Code |
| `phdpal-daily-science-stories` | [@BohriumPhDPal](https://x.com/BohriumPhDPal) | Creates daily science-history slice stories with verifiable sources and emotional translation | @yinyi1216-cmyk | Codex CLI |
| `phdpal-phd-survive-guide` | [@BohriumPhDPal](https://x.com/BohriumPhDPal) | Produces practical PhD survival guide content (Scene/Pain/Laugh/Do framework) | @yinyi1216-cmyk | Codex CLI |
| `phd-lite-knowledge` | [@BohriumPhDPal](https://x.com/BohriumPhDPal) | Transforms curated sources into traceable PhD light-knowledge posts | @yinyi1216-cmyk | Codex CLI |
### Utility Skills (used across accounts)

| Skill | What It Does | Author | Platform |
|-------|--------------|--------|----------|
| `sciencepedia` | Looks up SciencePedia concept URLs (~145k entries). Many content workflows need to link back to SP entries — this is the shared lookup tool. | @1021ju | Claude Code |
| `author-finder` | Finds researcher LinkedIn/X profiles for @mentioning in posts | @1021ju | Claude Code |
| `bohrium-lookup` | Looks up Bohrium paper-detail URLs by DOI or title using the standalone utility skill | @Laurence | Claude Code |
| `sciencepedia-agent-tools` | Looks up Bohrium SciencePedia tool-detail pages for software like GROMACS, LAMMPS, VASP, and OpenMM | @Laurence | Claude Code |
| `tutorial-cover-image` | Generates 16:9 pastel editorial cover images for Bohrium tutorial and tool-comparison articles | @Laurence | OpenAI Codex CLI |

> **Note on Bohrium Link Lookup:** The `paper-post-prep` skill contains a built-in script (`scripts/bohrium_lookup.py`) that can look up any paper's URL on Bohrium by DOI or title. This is a general-purpose utility embedded within `paper-post-prep`.

## Platform Compatibility

Skills in this repo may have variants optimized for different AI coding tools:

- **Claude Code** — Anthropic's CLI tool
- **OpenAI Codex CLI** — OpenAI's CLI tool

If a skill has been adapted for a different platform, the variant lives on a separate branch (see [Contributing](#contributing)).

## Installation

Copy the skills you need into your local config directory:

**For Claude Code:**
```bash
# Install one skill
cp -r <skill-name> ~/.claude/skills/

# Install all skills
for dir in */; do
  [ -f "$dir/SKILL.md" ] && cp -r "$dir" ~/.claude/skills/
done
```

**For Codex CLI:** Follow the Codex-specific instructions in the skill's branch README (if a Codex variant exists).

## Contributing

We use a **branch model** for collaboration. Everyone pushes to their own branch, then opens a PR to `main`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, including how to use Codex CLI to push your skills.

