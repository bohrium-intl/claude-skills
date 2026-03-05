---
name: bohrium-outreach-generator
description: Generate concise personalized outreach messages for shortlisted creators based on platform, topic, and relevance rationale. Use after tiering when users need ready-to-send outreach drafts.
---

# Bohrium Outreach Generator

Generate short natural-language outreach messages tailored to the creator.

## Input

- `name`
- `platform`
- `recent_topic`
- `reason_relevant`

## Requirements

1. Keep message length at or below `120` words.
2. Personalize directly using the provided relevance reason.
3. Avoid generic marketing language.

## Output Format

Return:

- `outreach_message`
