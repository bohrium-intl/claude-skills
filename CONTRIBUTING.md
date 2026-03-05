# Contributing Guide

## For Everyone: How to Add or Update Skills

### Step 1: Create Your Branch

Each person works on their own branch. Branch naming convention:

```
<your-name>/<what-you-are-doing>
```

Examples:
- `june/add-decoder-post-skill`
- `ashley/update-paper-post-for-codex`

### Step 2: Add Your Skill

Each skill is a folder with at least a `SKILL.md` file:

```
your-skill-name/
  SKILL.md          # Required: the skill prompt/instructions
  scripts/          # Optional: helper scripts
  README.md         # Optional: design notes, creation process
```

### Step 3: Document Your Skill

Add your skill to the **Skills Registry** table in the root `README.md`:
- Which account/pillar does it serve?
- What does it do (one sentence)?
- Your GitHub username as author
- Which platform: Claude Code or Codex CLI?

### Step 4: Push and Open a PR

Push your branch and open a Pull Request to `main`. Someone will review and merge.

---

## For Codex CLI Users: Push Without Knowing Git

If you use OpenAI Codex CLI and are not familiar with git, you can ask Codex to do it for you. Just tell Codex:

```
I need to push a new skill to our team's GitHub repo.

Here's what to do:
1. Clone the repo: git clone https://github.com/bohrium-intl/claude-skills.git
2. Create a new branch with my name: git checkout -b <your-name>/<skill-description>
3. Copy my skill folder into the repo (I'll tell you the path)
4. Add my skill to the Skills Registry table in README.md
5. Commit and push: git add . && git commit -m "Add <skill-name>" && git push -u origin <branch-name>
6. Open a PR on GitHub

My GitHub username is: <your-username>
My skill is at: <path-to-your-skill-folder>
```

Codex will handle the git operations for you.

> **Important:** Make sure you have git configured with your GitHub credentials. If Codex asks for authentication, you may need to set up a Personal Access Token (ask @1021ju for help).

---

## For Claude Code Users: Push Your Skills

Same process, but you can ask Claude Code directly:

```
Help me push my skill <skill-name> from ~/.claude/skills/<skill-name>
to the bohrium-intl/claude-skills repo. Create a branch and PR.
```

---

## Platform Variants (Claude Code vs Codex)

Sometimes the same skill needs adjustments for different platforms. Handle this with branches:

- `main` — the canonical version (usually Claude Code)
- `codex/<skill-name>` — Codex-adapted variant

When a skill has been adapted for Codex, note this in the skill's own README with what was changed and why.

---

## Skill Design Notes (Optional)

If your skill has an interesting creation process or design decisions worth sharing, add a `README.md` inside your skill folder. This is optional — simple skills don't need it.

Example of what to include:
- What problem does this skill solve?
- How did you iterate on the prompt? (e.g., "started with Perplexity research, then refined through testing")
- What are the key design decisions?
- Known limitations or edge cases

This helps teammates learn from each other's approaches.

---

## Questions?

Ask @1021ju or open an issue.
