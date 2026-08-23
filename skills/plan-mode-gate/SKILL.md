---
name: plan-mode-gate
description: Enforces a mandatory plan mode before any non-trivial code change. The agent must complete four phases — Reconnaissance, Specification & Constraints, Blast Radius & Impact Analysis, and an Actionable Checklist — and present the plan for approval before editing any file. Use when the user asks to modify, refactor, extend, debug, or add features to an existing codebase; when a change touches multiple files or shared interfaces; when the user says "plan first", "don't code yet", "think before you change anything", "enter plan mode", or "analyze the impact"; or whenever skipping impact analysis risks breaking existing behavior. Not for greenfield scaffolding, one-line fixes, or pure questions about code.
---

# Plan Mode Gate

Before modifying any code in an existing codebase, run the four phases below in order and deliver a plan. **Do not edit, create, or delete any file until the user approves the plan** (or explicitly waives it). Reading, searching, and running read-only commands are always allowed; mutations are not.

If the user says "just do it" or pushes back on planning, compress the four phases into a short summary and proceed — never skip Reconnaissance entirely.

If requirements are ambiguous, contradictory, or missing critical detail (target behavior, scope boundaries, environment), ask the user before or during Phase 2 — do not guess constraints.

## Phase 1 — Reconnaissance (Exploration)

Build a mental model of the territory. **Propose nothing yet.**

1. Scan the codebase map: directory tree, entry points, build/config files, package manifests, README/docs.
2. Read the interfaces relevant to the request: public APIs, exported types, function signatures, component props, route definitions, event contracts.
3. Trace data flows end-to-end for the affected feature: where state lives, who writes it, who reads it, how it crosses module/network/storage boundaries.
4. Note existing conventions: naming, state management, error handling, testing patterns.

**Output:** a findings list only — what exists, where, and how it connects. Any sentence proposing a change is a phase violation.

## Phase 2 — Specification & Constraints

Pin down what cannot move and what the change must satisfy.

- **Locked foundations:** architecture decisions, frameworks, core modules, public APIs, or files that must not change (from user instruction, code ownership, or obvious fragility).
- **User invariants:** behaviors, outputs, contracts, and design principles the user has declared untouchable (check prior instructions and project conventions).
- **Environment configuration:** runtime, package versions, env vars, build tooling, deployment targets, feature flags.
- **Schemas:** data models, database schemas, API payloads, file formats, serialization contracts the change must stay compatible with.

**Output:** an explicit constraint list. Anything uncertain → ask the user now, not mid-implementation.

## Phase 3 — Blast Radius & Impact Analysis

Map everything the change could break.

1. **Dependent files:** grep/trace importers, re-exports, callers, subclasses, config references, tests, and docs for every file in scope.
2. **Breaking changes:** signature changes, behavior changes, schema changes, removed exports — flag each as safe / risky / breaking, and say why.
3. **Edge cases:** missing or weak handling the change must address — empty/null states, error paths, concurrency, large inputs, offline, permissions, migration of existing data.
4. **Second-order effects:** caches, persisted data, analytics, deep links, cross-feature shared state.

**Output:** an impact table — file/system → relationship → risk level → required handling.

## Phase 4 — Actionable Checklist

Convert the analysis into an execution plan.

- One checklist item = one atomic change (a single file or one coherent logical unit, independently verifiable).
- Order items by dependency: foundations and types first, consumers last. No item may depend on a later item.
- Each item states: what changes, which file(s), how to verify it (test, build, manual check).
- Include test updates and cleanup as their own items — never fold them silently into implementation items.
- Flag any item that needs a user decision, and surface open questions instead of hiding assumptions in the plan.

## Plan Output Format

Present the completed plan in this structure:

```markdown
## Recon Findings
- (what exists, where, how it connects)

## Constraints & Invariants
- Locked: ...
- Must satisfy: ...

## Blast Radius
| File / System | Relationship | Risk | Handling |
|---|---|---|---|

## Execution Plan
1. [ ] <atomic step> — <file(s)> — verify: <how>
2. [ ] ...

## Open Questions (if any)
- ...
```

End by asking the user to approve, adjust, or waive the plan. Only then begin implementation, checking off items in order. If implementation reveals the plan was wrong, stop, re-run the affected phase, and get re-approval before continuing.
