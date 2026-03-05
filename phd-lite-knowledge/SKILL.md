---
name: phd-lite-knowledge
description: Create PhDPal "PhD Lite Knowledge" posts by extracting verifiable facts and viewpoints from a provided source table (X, Instagram, LinkedIn, web), converting them into a structured outline, and writing original, traceable, non-plagiarized short-form content. Use when the user asks to produce PhD light-knowledge posts, summarize curated PhD-related links, or transform mixed article/image-card sources into an X-ready post with key points and source mapping.
---

# PhD Lite Knowledge

Produce rigorous, readable, and traceable PhD knowledge posts for PhDPal.

## Inputs

Required:
- Topic or angle for the current post
- Source table or source links

Optional:
- Audience level (applicants, early PhD, late PhD)
- Tone preferences
- Extra length constraints

If no source list is provided, ask for sources first.

## Workflow

### 1. Find and Screen Sources

1. Use user-provided sources as the primary pool.
2. Screen each source by:
   - Credibility: identifiable author or organization
   - Verifiability: claims can be traced to original pages
   - Timeliness: prioritize recent 3-5 years for fast-changing topics
   - Transformability: includes clear claims, mechanisms, conclusions, or applications
3. If evidence is insufficient, add sources in this priority order:
   1. Official institutions, universities, research institutes
   2. Journals, publishers, or author-owned public pages
   3. Reputable science media sections
   4. High-quality science communication accounts

Use:
- `references/source-priority.md`
- `references/default-source-map.md`

### 2. Extract and Normalize Information

Handle source types differently:

- Article/text sources:
  - Extract claims, core terms, mechanisms, and caveats.
  - Rewrite immediately; do not preserve original sentence frames.
- Image-card/poster/screenshot sources:
  - Transcribe text first.
  - If content is incomplete, verify with the original source page.

Normalize each candidate insight into:

- One-sentence topic
- Core conclusion
- Why it works (mechanism or logic chain)
- One example or scenario (optional)
- Boundary or caution (optional)
- Source note (source id plus URL)

Discard any statement that cannot be traced.

### 3. Write the Post

Write for PhDPal with clear logic and practical readability.

Rules:
- Prioritize evidence-based retelling and synthesis.
- Do not over-claim beyond source evidence.
- Mark added inference as `possible` or `inference`.
- Do not copy source sentence style, metaphors, or paragraph order.
- Rebuild structure as needed, for example:
  - source: phenomenon -> explanation -> conclusion
  - output: conclusion -> why -> example

### 4. Run Compliance Checks

Before final output, verify all items:

1. No direct sentence reuse from source text.
2. No one-to-one paragraph skeleton copying.
3. Numbers, ratios, and findings match source context.
4. Inferences are explicitly labeled and do not conflict with sources.
5. Every key statement maps to at least one source link.

### 5. Deliver Output

Output exactly three sections:

1. `Final Post`
2. `Key Information Points` (3-6 bullets)
3. `Source Mapping` (point-to-source mapping with id and URL)

Use template:
- `references/output-template.md`

## Output Constraints

- English only for all generated posts and lists.
- Professional and natural tone.
- No fabricated studies, numbers, institutions, or quotes.
- State limitations when evidence is weak.

