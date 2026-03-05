---
name: paper-scout
description: "Discover and rank trending papers for Paper of the Day posts. Use when user says 'find papers', 'paper scout', '今天有什么论文', '筛选论文', 'trending papers', 'what papers are hot', or wants to find candidate papers for social media posts. Helps identify papers with high social engagement potential — especially AI/ML papers from recent conferences, under-covered papers with strong results, and papers whose authors are active on LinkedIn/X."
---

# Paper Scout — Trending Paper Discovery

Find candidate papers for Bohrium's daily Paper of the Day posts on LinkedIn and X. Prioritize papers where **authors are likely to engage** (repost, comment, claim).

## High-Value Paper Categories

Rank candidates by engagement potential (best first):

1. **Conference acceptances** — Authors actively promote newly accepted papers (AAAI, NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, KDD, etc.). Search for "accepted", "oral", "spotlight", "best paper", "outstanding paper"
2. **Under-covered strong results** — Papers with impressive results that mainstream tech media hasn't picked up yet. Authors of these are hungry for visibility
3. **Papers with active author social presence** — If the author already posts on LinkedIn/X, they're far more likely to engage with our coverage
4. **Open-source releases** — Papers with fresh GitHub repos get more engagement. Authors want visibility for their code
5. **Cross-disciplinary surprises** — AI applied to unexpected domains (cancer, materials, climate). These get shares beyond the AI bubble

## Discovery Sources

### AI Papers: 跟机器之心，当天或前 1-2 天

**Primary source for AI papers is 机器之心.** They have a strong editorial filter. We follow behind their coverage — so look at their content from **today and the past 1-2 days only**, not further back.

#### Tier 1: 机器之心 + 中文 AI 媒体 (today ~ 2 days ago)
```
Web search: "机器之心" site:mp.weixin.qq.com {today or yesterday's date}
Web search: "量子位" OR "新智元" 论文 {today or yesterday}
Web search: site:huggingface.co/papers  (check trending tab for last 2-3 days)
```

#### Tier 2: Conference & arXiv (for conference-specific hunting)
```
Web search: "{conference name} 2025 2026 accepted papers best paper"
Web search: site:arxiv.org {topic} {this week}
```

#### Tier 3: Social Signal (author self-promotion)
```
Web search: site:x.com "new paper" OR "our paper" OR "accepted at" {topic} {past 3 days}
Web search: site:linkedin.com "excited to share" OR "our paper" {topic} {past 3 days}
```

### Non-AI Papers: Science/Medicine/Materials 等跨学科

These are the papers like the pancreatic cancer post that break out of the AI bubble. Sources:

#### Tier A: Science News Aggregators
```
Web fetch: https://www.sciencedaily.com/news/  (daily feed of university press releases by topic)
Web search: site:eurekalert.org {topic} {this week}  (AAAS press release platform — almost every major paper gets one)
Web search: site:phys.org {topic} {past 3 days}  (physics, materials, space, biology)
```

#### Tier B: Top Journal News Sections
```
Web search: site:nature.com/news OR site:nature.com/articles "research highlight" {this week}
Web search: site:science.org/news {this week}
Web search: site:newscientist.com {topic} {this week}
```

#### Tier C: Biomedical Specifically
```
Web search: site:statnews.com {this week}  (pharma, biotech, drug discovery)
Web search: site:medicalxpress.com {topic} {past 3 days}
```

**Cross-disciplinary selection tip**: Look for science papers where AI/computation was a key enabler (like DrugCLIP, AlphaFold applications, AI-guided synthesis). These bridge both audiences.

## Evaluation Criteria

For each candidate, assess (score 1-5 each):

| Criterion | What to check |
|-----------|--------------|
| **Science quality** | Clear contribution, strong results, reproducible |
| **Story angle** | Is there a "wait, what?" moment? Can we explain it to a smart non-expert? |
| **Author reachability** | Can we find the authors on LinkedIn/X? Do they post actively? (Nice-to-have, NOT a dealbreaker — hot papers are worth posting even if no authors are taggable) |
| **Visual assets** | Does the paper/repo have good figures, demos, or GIFs? |
| **Timeliness** | Fresh (this week) beats old. Conference acceptance timing matters |
| **Bohrium fit** | Can we find it on bohrium.com? Are there relevant SciencePedia concepts? |

## Output Format

Present candidates as a ranked table:

```
## Paper of the Day Candidates — {date}

### 1. [Paper Title]
- Authors: [names] | Institution: [inst]
- Source: [arXiv link / conference]
- Repo: [GitHub link if available]
- Why this paper: [1-2 sentences on the angle]
- Author social: [any LinkedIn/X links found during discovery]
- Score: Science ⭐⭐⭐⭐ | Story ⭐⭐⭐⭐⭐ | Reachability ⭐⭐⭐ | Visuals ⭐⭐⭐⭐ | Timeliness ⭐⭐⭐⭐⭐

### 2. [Next candidate...]
...
```

After presenting, ask the user which paper to go with. If the user has the `paper-post-prep` skill, suggest using it for the next step.

## Tips

- **AI papers: 机器之心 is the primary filter** — only look at today and the past 1-2 days. We follow behind their coverage, so no need to go further back
- **Conference deadline seasons matter** — after AAAI/NeurIPS/ICML notification dates, there's a flood of "accepted!" posts. Great hunting ground
- **Don't ignore non-AI papers** — The pancreatic cancer post got huge engagement. Science papers where AI researchers wouldn't normally look can be goldmines
- **Cross-disciplinary sweet spot** — Papers where AI/computation enables a scientific breakthrough (AI for drug discovery, ML for materials, etc.) bridge both audiences
- **GitHub stars as signal** — A fresh repo with 500+ stars in a week means the community cares
- **ScienceDaily / EurekAlert for non-AI discoveries** — University press releases surface papers that mainstream tech media won't cover. These are the "under-covered" goldmines
- **Nature/Science news sections** — When Nature or Science writes a "News" article about a paper, it's usually significant and well-explained
