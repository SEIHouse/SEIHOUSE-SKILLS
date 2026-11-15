---
name: seihouse-pr
description: Prepare completed implementation changes, create or update the appropriate GitHub pull request, and follow checks and review feedback through resolution on the same branch. Honor local-only instructions and preserve unrelated work.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# SEIHouse PR

For implementation work, default to verifying, committing, pushing, and creating or
updating a PR. Explicit task instructions override this default, including local-only
delivery. Skip publishing for audits, research, planning, and tasks with no repository
changes. Follow active environment restrictions. This workflow does not authorize
merging, deploying, or modifying unrelated systems.

## Prepare the change

Inspect repository instructions, status, branch, final diff, and recent commits.
Confirm the intended base and check for an existing PR for the task. Keep fixes to an
existing PR on its branch; do not create a second PR for them.

Include only the task's files or hunks. Preserve legitimate work from other tasks;
avoid destructive cleanup, broad staging, or rewriting shared history. When isolation
is necessary, use a suitable task branch or worktree without discarding other work.
If there is no Git checkout, establish the authoritative repository before publishing;
do not initialize an unrelated directory and guess its history or remote.

Perform [SEIHouse Verification](../seihouse-verification/SKILL.md), reusing checks
already completed for the current changes. Correct known in-scope errors before
publishing. If a required check fails and cannot be fixed safely, report the blocker
instead of declaring the implementation ready.

## Publish

Commit the relevant changes with a concise message and push the task branch. Update
the existing PR, or create one against the verified base when none exists. Describe
the concrete resulting behavior, validation results, and material limitations using
the repository's template when provided. Keep the title and description aligned with
the final scope. An open PR is an intermediate result, not proof of completion.

## Follow checks and feedback

After each push, monitor checks for the latest commit and refresh PR review
submissions, inline threads, and conversation comments. Prefer available GitHub
tools; use the supported CLI when needed. Poll at reasonable intervals (normally
30–60 seconds), respecting rate limits, and report only meaningful changes.

- Inspect failing checks and actionable feedback against the actual changes.
- Fix confirmed in-scope defects, run affected validation, and push to the same branch.
- Reply with the resolution or evidence explaining why a suggested change does not
  apply. Resolve a thread only after its concern is actually addressed; do not use
  dismissal as a substitute for a fix.
- Explain unrelated requests or scope-changing decisions instead of silently
  implementing them. Surface genuinely blocked decisions to the user.
- Recheck the new commit, checks, and reviews after fixes; a previous green commit
  does not validate the updated head.

Continue until required checks pass, requested automated reviews finish, and the
latest feedback refresh shows no unresolved actionable concern. If a review or check
is still pending, keep following it; if progress is blocked by access, infrastructure,
or a required human decision, report the exact pending condition without calling the
work complete. Elapsed time alone is not success. Do not manufacture reviewer
approval or promise that future comments cannot arrive.

Unless task instructions require continued monitoring, stop after 30 minutes with
no state change and report the exact pending item without marking the work complete.
Explicit instructions to follow a PR until its checks and feedback are resolved
override this default wait limit.

## Report

Give the branch, PR link, latest check/review status, and any blocker. Distinguish
implementation completion from pending human approval or merge. Do not merge or
deploy unless separately authorized by the task.
