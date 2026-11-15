---
name: seihouse-planning
description: Inspect an existing system and prepare a proportional implementation plan when the user requests planning, requirements need clarification, or a change crosses important contracts. Supports authorized implementation without imposing a separate approval gate.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# SEIHouse Planning

Establish the intended outcome, the current owner of the behavior, the affected
contracts, and the smallest complete implementation. Match planning effort to the
change; a local correction may need only a short internal plan.

## Respect the active task mode

- When the user requests a plan before implementation, provide the plan and wait
  for authorization to implement it. Follow any stricter active environment mode.
- During already-authorized implementation, inspect and plan as needed, then
  continue. This skill does not introduce a separate approval requirement.
- Ask only for missing decisions that materially affect the outcome and cannot be
  resolved from the repository or existing instructions.
- If new evidence changes the approach, revise it and continue within the authorized
  scope. Ask when the revision needs a new product decision or exceeds that scope.

## Ground the plan

Read applicable repository instructions and inspect the relevant entry point,
implementation, callers, and existing checks. Trace state, persistence, or network
boundaries when the change crosses them. Reuse prior task findings that remain valid.

Identify:

- the requested behavior and observable success criteria;
- the existing owner and directly affected consumers;
- public APIs, stored data, and behaviors that must remain compatible;
- required environment constraints and verified risks;
- unresolved decisions, separated from discoverable repository facts.

Avoid broad repository exploration when a focused trace establishes the boundary.

## Produce an implementable plan

Group work by behavior or subsystem and order it by dependency. State what changes,
why it belongs there, and how to verify it. Include compatibility or migration work
only when an affected contract requires it. Surface material risks and open product
questions before dependent implementation.

For a user-facing plan, normally include:

1. Outcome and boundaries.
2. Implementation steps and important interface changes.
3. Relevant tests and acceptance criteria.
4. Assumptions or decisions still needed.

Follow the active environment's required plan format. Keep the plan concise enough
to review and specific enough to implement without inventing product behavior.
