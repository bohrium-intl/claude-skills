# LinkedIn Post Style Guide — Paper of the Day

## Format & Length

- **Mainpost length**: 1200-1800 characters
- **Language**: English
- **Structure**: Mainpost + 1 Reply (paper link + SP concept links, all in one reply)
- **Hashtag format**: `#PaperOfTheDay` (always first), then 3-5 topic-specific tags
- **No links in mainpost** — all links go in replies to keep the mainpost clean

## Structure Template

### Mainpost
```
[1-2 emoji] [Hook line — provocative question, surprising claim, or stakes statement]

[Context paragraph: 1-2 sentences on the problem/challenge this paper addresses.
Be specific about WHY this problem matters.]

@AuthorName1, @AuthorName2, and @AuthorName3 ([Institution]) [verb: took/showed/designed/built] [what they did — one clear sentence].

[Mechanism paragraph: 2-3 sentences explaining HOW it works. More technical detail
than X version. Use specific numbers, method names, benchmarks.]

[Impact paragraph: What this means. Be concrete about implications.
Avoid vague "transforms the field" language.]

#PaperOfTheDay #Topic1 #Topic2 #Topic3
```

### Reply (论文 + SP 词条, all in one reply)
```
📄 Paper on Bohrium
{Bohrium paper URL}

💻 Code
{GitHub repo URL}

🔬 {Concept 1 name}
{SciencePedia URL 1}

🔬 {Concept 2 name}
{SciencePedia URL 2}

🔬 {Concept 3 name}
{SciencePedia URL 3}
```

**Important**: Only use Bohrium paper links in replies, NOT arXiv links. Drive traffic to Bohrium.

## Opening Emoji

**Don't default to 🚨 every time.** Pick 1-2 emojis that fit the paper's content and tone. No fixed mapping — use your judgement.

## Voice & Tone

- **Professional but accessible** — more formal than X, less formal than a journal abstract
- **Explain mechanisms** — LinkedIn audience expects more depth than X
- **Authors get full attribution** — full names, LinkedIn @tags, institution in parentheses
- **First person plural OK** — "we" / "our" for Bohrium voice is acceptable
- **Confidence without hype** — state results directly, let the numbers speak

## Author Attribution

- **Write as `@Name (Institution)`** in the mainpost text — this format makes it easy to find and tag the right person when posting on LinkedIn
- **Corresponding author and first author** are most important to tag
- **Natural integration**: "@Cheng Qian, @Dilek Hakkani-Tür, and @Heng Ji (UIUC) took a different approach..."
- If >4 authors, name 2-3 key authors + "et al."
- **Provide a separate 艾特备注 table** mapping each @Name to their actual LinkedIn profile URL, so the poster can quickly find and tag them

## What Makes LinkedIn Different from X

| Aspect | X Post | LinkedIn Post |
|--------|--------|---------------|
| Length | 650-1400 chars | 1200-1800 chars |
| Depth | One core insight | Mechanism + impact |
| Tone | Smart friend sharing | Professional colleague explaining |
| Structure | Mainpost + 1 thread (links + ¹²³ concepts) | Mainpost + 1 reply (links + concepts) |
| Author tags | @handles | @FullName (Institution) |
| Hashtag style | #CamelCase | #CamelCase |
| Annotations | Superscript ¹ ² ³ for concepts | None |
| Links | In thread replies only | In replies only |

## Anti-Patterns (Fix These)

### Formulaic Templates
**Problem**: Every post using "milestone study", "breakthrough transforms", "charts a new path" — readers recognize the pattern after 3 posts.

**Fix**: Vary your framing verbs and impact language:
- Instead of "milestone study" → "the first systematic attempt to...", "a direct challenge to...", "a clean demonstration that..."
- Instead of "breakthrough transforms" → "this changes the math on...", "the practical upshot:", "what this actually means:"
- Instead of "charts a new path" → end with a specific implication, an open question, or what comes next concretely

### Parallel Sentence Structure
**Problem**: "This X. This Y. This Z." or "By doing A... By doing B... By doing C..." — mechanical repetition signals AI writing.

**Fix**: Vary sentence openers and lengths. Mix declarative statements with questions or conditional framing.

### Vague Impact Statements
**Problem**: "This transforms the field of X" — says nothing specific.

**Fix**: Name the specific change. "Until now, pancreatic cancer trials failed because blocking KRAS alone triggered escape pathways. This triple-hit approach closes the exits."

### Frontloading All Authors
**Problem**: "In this study, Author1, Author2, Author3, Author4, Author5, Author6 and Author7 (Institution) reveal..." — a wall of names before the reader knows why they should care.

**Fix**: If >3 authors, lead with what happened, then attribute: "A triple-drug strategy eliminated pancreatic tumors in mice with no recurrence over 200 days. The team behind it — Barbacid, Liaki, and Barrambana et al. (CNIO) — hit three targets simultaneously."

## Good LinkedIn Post Example (Rewritten)

**Before** (AI-sounding):
```
🚨 Scientists may have discovered a cure for pancreatic cancer in mice
by neutralizing the survival network!

Pancreatic ductal adenocarcinoma (PDAC) is infamous for its survival
compensation mechanism...

In this milestone study, [authors] ([institution]) reveal a triple-hit
strategy that completely eliminated tumors...

This breakthrough transforms the battle with pancreatic cancer...
```

**After** (more natural, with reply structure):

**Mainpost:**
```
💊🔬 Pancreatic cancer tumors — gone. 200 days, no recurrence.

Pancreatic ductal adenocarcinoma has a nasty trick: block one driver
like KRAS, and the cancer reroutes through EGFR or STAT3. Every
targeted therapy has failed here for the same reason.

@Mariano Barbacid, @Vasiliki Liaki and @Sara Barrambana et al. (CNIO)
went after all three at once. Daraxonrasib on KRAS G12D, afatinib on
pan-ErbB, SD-36 on STAT3 — shutting down the main driver and both
escape routes simultaneously.

In both GEM and patient-derived xenograft models, tumors were
completely eliminated. Not shrunk. Eliminated. And the combination
was well-tolerated — minimal toxicity across all arms.

The key insight: single-target therapies kept failing not because the
drugs were weak, but because the cancer's backup network was faster.
This is the first demonstration that closing all three exits at once
can achieve what looks like full eradication in preclinical models.

Clinical trials are the obvious next step. The tolerance data is
encouraging.

#PaperOfTheDay #PancreaticCancer #CancerResearch #KRAS #PrecisionOncology
```

**Reply:** 📄 Bohrium paper link + code repo + 🔬 3 SciencePedia concept URLs
