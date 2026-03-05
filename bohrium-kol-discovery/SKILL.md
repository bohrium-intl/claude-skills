---
name: bohrium-kol-discovery
description: End-to-end pipeline for discovering, evaluating, prioritizing, and engaging science/tech creators for Bohrium outreach. Use when users ask to find KOLs, score creator fit, assign outreach priority tiers, or generate personalized outreach messages for identified candidates.
---

# Bohrium KOL Discovery

Run the five sub-skills in order for deterministic output:

1. `bohrium-discovery`
2. `bohrium-relevance-scoring`
3. `bohrium-conversion-scoring`
4. `bohrium-tiering-priority`
5. `bohrium-outreach-generator`

## Pipeline Contract

Pass these fields across steps whenever available:

- `name`
- `platform`
- `profile_url`
- `bio`
- `followers`
- `recent_posts`
- `engagement_rate`
- `growth_trend`

## Final Output

Return a ranked table containing:

- `name`
- `platform`
- `relevance_score`
- `conversion_score`
- `tier`
- `priority`
- `collaboration_model`
- `outreach_message`
- `reason`
