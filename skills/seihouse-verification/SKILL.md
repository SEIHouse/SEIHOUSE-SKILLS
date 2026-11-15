---
name: seihouse-verification
description: Verify implementation changes or perform a focused self-review before creating or updating a pull request. Check requirements, affected integrations, and relevant failure cases without expanding the task or repeating completed validation.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# SEIHouse Verification

Verify the requested behavior through the final changes and their affected paths.
Review deeply enough to find meaningful defects; modify only within the task boundary.
For a review-only request, report findings without editing unless fixes are authorized.

## Review the actual changes

Inspect the final diff and the original requirements. When no Git history is
available, compare against a saved baseline or inspect the changed files directly
and state the limitation. Preserve unrelated work from other tasks.

Check that the change:

- satisfies every requested outcome without adding unrequested features;
- uses the existing owner and updates directly affected callers and contracts;
- preserves relevant state, persistence, synchronization, and resource lifecycles;
- handles affected loading, empty, error, accessibility, and responsive behavior;
- contains no accidental secrets, broken references, placeholders, or debug artifacts.

Trace only the dependencies needed to assess a concrete risk. Use deeper review for
shared contracts, migrations, authorization, accounting, or destructive operations.

## Validate observable behavior

Choose checks from the repository's actual tooling and the changed behavior.
Examples include targeted tests, type checking, compilation, document or package
validation, and focused browser interaction. Do not assume a JavaScript project or
run a broad build for an instruction-only change.

Exercise relevant failure cases, such as repeated interaction, missing data,
request failure, navigation, stale state, or the smallest supported viewport.
Reuse passing checks for unchanged code; rerun affected checks after fixes.
Static inspection, simulated interaction, audible playback, and physical-device
testing are different evidence. Report only what was actually verified.

## Fix and finish

During authorized implementation, fix a confirmed defect when it is required by the
request, introduced by the current change, or necessary to preserve directly affected
behavior. Report unrelated pre-existing issues without silently expanding scope.
For a review-only task, present actionable findings with evidence instead.

After fixes, reinspect the final changes and rerun the relevant validation. Stop when
requirements are satisfied and a final review finds no new material in-scope defect.
Do not call work complete with known errors or failing required checks. If a defect
cannot be fixed safely, explain the blocker and what evidence or decision is needed.

## Report

Summarize the outcome, checks and results, corrected issues, and material limitations.
For a PR, include a concise self-review summary of scope, validation, and remaining
risks in the existing description or repository template. Avoid duplicate reporting
or exposing internal deliberation.
