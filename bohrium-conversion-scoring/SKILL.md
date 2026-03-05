---
name: bohrium-conversion-scoring
description: Estimate creator conversion and collaboration potential for Bohrium campaigns by evaluating recommendation behavior and monetization signals. Use after relevance scoring when users need partnership-likelihood scoring.
---

# Bohrium Conversion Scoring

Evaluate whether a creator is likely to drive action and accept collaboration.

## Input

- `recent_posts`

## Tasks

1. Score `tool_recommendation_score` (`1-10`).
2. Score `collaboration_likelihood` (`1-10`).
3. Compute `overall_conversion_score` (`1-10`).
4. Provide concise `reason`.

## Output Format

Return:

- `tool_recommendation_score`
- `collaboration_likelihood`
- `overall_conversion_score`
- `reason`
