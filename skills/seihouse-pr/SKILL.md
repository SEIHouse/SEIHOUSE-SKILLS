---
name: seihouse-pr
description: Check branch scope, prepare completed repository changes, and create or update a pull request.
---

# SEIHouse PR

Use this skill after completing a task that changes repository files.

Skip it for audits, research, planning, or other tasks that produce no repository changes.

## Prepare the Pull Request

1. Check the current branch, repository status, final diff, and recent commits.
2. Confirm the branch is appropriate for the current task.
3. Make sure the pull request primarily contains changes related to the task being completed.
4. Watch for changes from another active task or agent that may have landed on the same branch.
5. Remove leftover junk, obsolete files, temporary code, or unrelated artifacts when clearly appropriate.
6. Avoid accidentally modifying or including legitimate work that belongs to a separate active task.
7. When necessary, separate the current task's changes onto a more appropriate branch before pushing.

Use reasonable judgment. Do not turn minor branch noise into a blocker when the intended PR scope is clear.

## Create or Update the Pull Request

1. Commit the completed changes with a concise, relevant message.
2. Push the appropriate branch.
3. If a pull request already exists for the branch, update it rather than creating a duplicate.
4. Otherwise, create a pull request against the appropriate base branch.
5. Include a concise description of:
   - what changed
   - what was validated
   - any known issue or limitation

## Final Response

Report:

- the branch used
- whether the PR was created or updated
- the PR link or number
- any blocker or notable concern

Unless explicitly instructed otherwise, do not leave completed implementation work only in the local repository.
