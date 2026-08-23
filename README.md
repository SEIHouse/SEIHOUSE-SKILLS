# 🏛️ SEIHOUSE-SKILLS

Official AI Agent Skills Suite for **SEIHouse Productions**.

This repository contains the specialized prompt instructions, architectural conventions, UI translation tools, verification loops, and PR review workflows used by coding agents (Antigravity, Codex, Claude, Gemini, Kimi, Cursor) across the SEIHouse ecosystem.

---

## 📦 Skills Directory

| Skill | Description | Category |
|---|---|---|
| [`browser-synth-builder`](file:///skills/browser-synth-builder) | Build complete, playable Web Audio synthesizers & instruments in the browser with modern UI. | Audio & Creative |
| [`creative-ui-translator`](file:///skills/creative-ui-translator) | Translate creative UI, animation, motion, and shader ideas into actionable frontend graphics specifications. | Creative UI & Graphics |
| [`plan-mode-gate`](file:///skills/plan-mode-gate) | Mandatory planning and blast-radius impact analysis before non-trivial code modifications. | Safety & Planning |
| [`seihouse-codebase-conventions`](file:///skills/seihouse-codebase-conventions) | System orientation, product maps, and architectural consistency rules for SEIHouse repositories. | Architecture & Core |
| [`seihouse-components-performance`](file:///skills/seihouse-components-performance) | Optimize runtime performance, asset loading, resilience, and device adaptability. | Performance & QA |
| [`seihouse-gemini-verification-loop`](file:///skills/seihouse-gemini-verification-loop) | Deep multi-pass verification protocol to validate changes and eliminate regressions. | Verification & QA |
| [`seihouse-layout-optimization`](file:///skills/seihouse-layout-optimization) | Ensure layout hierarchy, visual quality, and responsiveness across all screen dimensions. | UI/UX & Layout |
| [`seihouse-pr`](file:///skills/seihouse-pr) | Check branch scope, prepare changes, commit, and open/update pull requests cleanly. | Git & Release |
| [`seihouse-pr-review`](file:///skills/seihouse-pr-review) | Focused, token-efficient pre-PR self-review to catch defects before code review. | Code Quality |
| [`sensei-skill`](file:///skills/sensei-skill) | Communication protocol tailored for SENSEI as founder & product owner (plain language, product outcomes). | Communication |
| [`workshop-replica`](file:///skills/workshop-replica) | Create isolated, faithful SEN Workshop replicas of app components for visual refinement. | UI Development |

---

## 🚀 How to Use These Skills

### In Antigravity IDE (Global Configuration)
Place or symlink desired skills into your global configuration directory:
```text
~/.gemini/config/skills/<skill-name>/
```
Each skill directory must contain a `SKILL.md` file with standard YAML frontmatter (`name`, `description`).

### In a Project Workspace (`.agents`)
To enable skills per-project, add them to your workspace customization root:
```text
<project-root>/.agents/skills/<skill-name>/SKILL.md
```

### In Claude Code, Codex, or Cursor
Each skill folder contains a standalone `SKILL.md` (and any accompanying references in `references/`) formatted for direct ingestion into AI context windows, system prompts, or agent rules.

---

## 🏛️ Ecosystem Architecture Principles

1. **Natural Product Communication**: All agent communication defaults to plain language and product outcomes for SENSEI.
2. **Validate Broadly, Modify Narrowly**: Verify full blast radius before making surgical, minimal edits.
3. **Preserve Production Compatibility**: Respect naming authorities, data stores, and backward compatibility across SEIHouse applications.
4. **Pre-PR Self-Review**: Perform rigorous code reviews prior to opening or merging PRs.

---

## 📄 License

Internal proprietary & open components by **SEIHouse Productions LLC**.
