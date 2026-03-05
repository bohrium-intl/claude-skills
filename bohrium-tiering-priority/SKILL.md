---
name: bohrium-tiering-priority
description: Segment creators into outreach tiers and assign collaboration priority/model using audience size, engagement, and scoring outputs. Use when users need action-oriented prioritization after relevance and conversion scoring.
---

# Bohrium Tiering Priority

Map scored creators into practical outreach decisions.

## Input

- `followers`
- `engagement_rate`
- `relevance_score`
- `conversion_score`
- `growth_trend`

## Tasks

1. Assign `tier`: `KOC`, `Micro`, `Mid`, or `Macro`.
2. Assign `priority`: `High`, `Medium`, or `Low`.
3. Recommend `collaboration_model`:
- `affiliate`
- `free trial`
- `sponsored`
- `CPA-only`
4. Provide brief `reasoning`.

## Output Format

Return:

- `tier`
- `priority`
- `collaboration_model`
- `reasoning`
