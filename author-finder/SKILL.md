---
name: author-finder
description: "Find researcher profiles on LinkedIn and X (Twitter) for @mentioning in posts. Use when user says 'find author', '找作者', 'author LinkedIn', 'author X account', 'find social profiles', or when preparing Paper of the Day posts and needing to tag paper authors. Takes author names and institutions, returns profile URLs using a multi-strategy search approach."
---

# Author Finder — Researcher Social Profile Lookup

Find LinkedIn and X profiles for paper authors to @mention in Bohrium's Paper of the Day posts. The goal: tag authors so they see and engage with our coverage.

## Input

Provide any combination of:
- **Author names** (required)
- **Institutions/affiliations** (strongly recommended)
- **Paper title** (helps disambiguation)
- **GitHub repo URL** (best source — check this first)
- **Paper PDF/arXiv link** (for extracting homepage links)

## Search Strategy (Follow This Order)

### Layer 1: GitHub Repo (Highest Signal)

If a repo URL is available, check it first — authors often link their own profiles:

```
Web search: site:github.com {repo URL}
```

Look in:
- **README.md** — "Authors", "Team", "Contact" sections often have personal links
- **GitHub profile pages** of repo contributors — bio, website field, social links
- **Paper's project page** linked from README — often has author cards with social links

### Layer 2: Paper / arXiv Page

```
Web search: "{paper title}" site:arxiv.org
```

On the arXiv page:
- Check author homepage links (the small 🏠 icons next to author names on arXiv)
- Author homepages often list LinkedIn/X/Google Scholar links

### Layer 3: Direct Profile Search

For **LinkedIn**:
```
Web search: "{author name}" "{institution}" site:linkedin.com
```

For **X / Twitter**:
```
Web search: "{author name}" site:x.com OR site:twitter.com
Web search: "{author name}" "{institution}" twitter OR x.com
```

### Layer 4: Google Scholar → Homepage

```
Web search: "{author name}" "{institution}" site:scholar.google.com
```

Google Scholar profiles sometimes link to personal websites, which then link to social profiles.

### Layer 5: Institution Page

```
Web search: "{author name}" site:{institution domain}
```

University/lab pages sometimes link to researchers' social accounts.

## Verification Rules

- **LinkedIn**: Verify the profile matches by checking institution, research area, and recent activity. LinkedIn URLs look like `linkedin.com/in/username`
- **X/Twitter**: Verify by checking bio (should mention institution or research area), recent posts (should be research-related), and follower count (active researchers typically have 500+). X handles look like `@username`
- **Confidence levels**:
  - **Confirmed** ✅ — Profile clearly matches (institution + research area + recent paper-related posts)
  - **Likely** 🟡 — Name and institution match but limited activity or verification
  - **Uncertain** ❓ — Name matches but can't confirm institution or research area
- **Never guess handles.** If you can't verify, report "not found" rather than risk tagging the wrong person

## Output Format

```
## Author Profiles for "{Paper Title}"

| Author | Institution | LinkedIn | X/Twitter | Confidence |
|--------|------------|----------|-----------|------------|
| Jane Smith | MIT CSAIL | [linkedin.com/in/janesmith](url) | [@janesmith_ml](url) | ✅ Confirmed |
| John Doe | Stanford | [linkedin.com/in/johndoe](url) | Not found | 🟡 Likely |
| Wei Zhang | Tsinghua | Not found | Not found | — |

### Search Notes
- Jane Smith: Found via GitHub repo README, verified by recent LinkedIn post about this paper
- John Doe: Found via Google Scholar homepage link, LinkedIn matches institution
- Wei Zhang: No English social profiles found. Checked GitHub, arXiv, Scholar
```

## Reality Check

- **Many authors have no findable social profiles** — this is completely normal, especially for researchers outside North America/Europe
- **Zero taggable authors is a valid outcome.** Don't invent or guess handles. Report honestly and move on
- Finding even **one taggable person or institution** is a win — that's enough for the post to have engagement potential
- **Don't over-invest time.** Run through the 5 search layers above. If nothing surfaces, report "not found" and let the user decide
- **Hot papers are still worth posting without @mentions.** Author tagging is a bonus, not a requirement

## Tips for Bohrium Posts

- **LinkedIn posts**: Use full names, tag with LinkedIn @mention format. Prioritize first/corresponding authors
- **X posts**: Use @handles. Tag 2-4 max — too many looks spammy
- **Corresponding author is most valuable** — they're most likely to engage
- **First author (often PhD student) is often the most active on social media** — they're building their profile
- **Institution accounts are backup tags** — if you can't find any personal profiles, tag the institution (@Stanford_AI, @MIT_CSAIL, @CNIO_Cancer etc.). This still gets visibility
- **Check if authors already posted about this paper** — if they did, replying/quoting their post gets more engagement than cold-tagging
