---
name: seihouse-pr-review
description: Perform a focused, token-efficient self-review immediately before opening or updating a pull request. Intended for implementation agents such as Codex, Claude, Kimi/Cami, and similar coding agents.
---

# SEIHouse PR Review

Use this skill immediately before opening or updating a pull request.

## Objective

Perform a focused, token-efficient review of your own implementation. Catch and fix likely defects before the code reaches external review.

Do not restart the task, broadly re-explore the repository, or repeat analysis already completed during implementation. Reuse the context gathered while making the change.

## Review Procedure

1. Inspect the complete final diff.
2. Verify that every changed file directly supports the assigned task.
3. Confirm that the implementation:
   - fulfills the requested behavior
   - preserves existing behavior outside the intended scope
   - follows established repository patterns
   - avoids unnecessary abstraction, duplication, or unrelated cleanup
4. Check specifically for:
   - incorrect assumptions
   - broken imports, references, types, contracts, or interfaces
   - incomplete call-site updates
   - regressions in directly affected flows
   - missing loading, empty, error, or fallback states where relevant
   - persistence, synchronization, caching, or state-management mistakes
   - temporary code, debug output, placeholders, dead code, or stale comments
   - accidental exposure of secrets or sensitive values
5. Run the smallest relevant validation set for the change:
   - targeted tests
   - type checking
   - linting
   - focused build or compilation checks
   - repository-specific validation commands

Do not run broad or redundant checks unless the scope or risk of the change justifies them.

6. Fix every issue discovered during review.
7. Reinspect the final diff after fixes.
8. Only then open or update the pull request.

## Review Depth

Match review effort to implementation risk.

Use a deeper review when the change affects:

- shared architecture
- authentication or authorization
- database schemas, migrations, or persistence
- synchronization or caching
- API contracts
- payments or usage accounting
- generation pipelines
- security boundaries
- destructive operations
- broadly reused components or utilities

For isolated, low-risk changes, keep the review narrow and efficient.

## Efficiency Rules

- Review the diff first.
- Inspect only directly affected code unless a dependency or contract requires broader context.
- Reuse implementation context instead of rediscovering it.
- Do not narrate routine reasoning.
- Do not produce a file-by-file retelling of the implementation.
- Do not run redundant checks.
- Do not perform unrelated cleanup.
- Stop once the changed behavior is validated and material risks are addressed.

## PR Self-Review Summary

Add this concise section to the pull request description:

### Self-Review

- **Scope reviewed:** [affected systems or flows]
- **Validation:** [checks run and outcomes]
- **Issues corrected:** [brief summary, or “None found”]
- **Risk:** Low / Medium / High — [one-sentence explanation]
- **Remaining concerns:** [known concern, or “None”]

Do not include internal chain-of-thought or lengthy narration.
