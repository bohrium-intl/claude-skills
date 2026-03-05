---
name: bohrium-discovery
description: Screen candidate creators for initial Bohrium fit using profile metadata and recent content. Use when users need a first-pass filter to decide whether a creator should proceed to deeper relevance/conversion scoring.
---

# Bohrium Discovery

Act as a growth analyst for Bohrium focused on science and research creators.

## Input

- `name`
- `platform`
- `bio`
- `followers`
- `recent_post_titles`

## Tasks

1. Assign `research_relevance_score` from `0-10`.
2. Decide `move_to_scoring` as `true` or `false`.
3. Provide a concise `reason`.

## Output Format

Return JSON-like fields:

- `research_relevance_score`
- `move_to_scoring`
- `reason`
