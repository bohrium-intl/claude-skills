---
name: bohrium-relevance-scoring
description: Score creator content relevance to Bohrium's target science/research audience across audience fit and technical depth dimensions. Use after discovery when users need a structured relevance score and justification.
---

# Bohrium Relevance Scoring

Evaluate creator content relevance using four dimensions.

## Input

- `bio`
- `recent_posts`

## Tasks

1. Score each dimension `0-10`:
- `audience_match`
- `research_depth`
- `scientific_credibility`
- `content_specificity`
2. Compute `overall_score` (`0-10`).
3. Provide a concise `reason`.

## Output Format

Return:

- `audience_match`
- `research_depth`
- `scientific_credibility`
- `content_specificity`
- `overall_score`
- `reason`
