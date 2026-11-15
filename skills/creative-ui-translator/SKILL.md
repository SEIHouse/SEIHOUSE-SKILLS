---
name: creative-ui-translator
description: Translate a loosely described visual interaction, animation, or material effect into an actionable frontend implementation prompt. Use for creative specifications, technical vocabulary, and copy-paste implementation briefs; honor explicit requests to implement the idea.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# Creative UI Translator

Preserve the user's creative intent while turning it into a precise, practical
interaction specification for a coding agent. Default to a prompt when translation
is requested; if the user explicitly requests implementation, use the specification
to implement within the task's authorized scope and active mode.

## Interpret the experience

Identify the target, intended meaning, material behavior, interaction trigger,
physical response, completion/reset behavior, and explicit exclusions. Consider
touch, keyboard, reduced motion, scrolling, and the existing visual identity.

Inspect available product context before asking about missing details. Ask only
when a missing decision could materially change the experience; make routine
technical choices independently.

## Choose the rendering approach

Use the lowest-complexity technique that can deliver the intended effect. Prefer
DOM/CSS for simple transitions, SVG or Canvas for localized procedural motion, and
GPU rendering when the visual behavior warrants it. Reuse the project's existing
stack where suitable.

Read [rendering tiers](references/rendering-tiers.md) when choosing or specifying a
rendering mechanism. The tiers are examples and decision aids, not a requirement to
introduce a particular framework or an advanced renderer.

## Build the brief

Write a concise implementation prompt covering the relevant parts of:

1. Primary outcome, exact component scope, and existing behavior to preserve.
2. Rendering approach and the physical or mathematical mechanism.
3. Visual treatment, interaction, partial/completed states, and reset behavior.
4. Responsive behavior, accessibility, and performance safeguards.
5. Explicit exclusions and observable acceptance criteria.

For an existing application, require the implementer to locate the current owner,
reuse existing primitives, and verify the affected mobile and desktop behavior.
Keep backend, authentication, and persistence changes outside a visual task unless
the requested behavior actually requires them.

Favor meaningful localized effects, touch accuracy, and the user's chosen
atmosphere. Do not replace the idea with generic design conventions, decorative
clutter, extra settings, or speculative architecture.

## Deliver

For translation, return a short concept statement and the complete copy-paste
prompt, with a brief rendering rationale only when useful. For implementation,
complete the requested change and report validation rather than stopping at a brief.
