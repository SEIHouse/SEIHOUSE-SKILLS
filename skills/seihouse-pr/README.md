# SEIHouse PR

Use `seihouse-pr` after implementation to verify the final change, commit and push
the task branch, and create or update its PR. Local-only instructions override
publishing. Planning and review-only tasks do not trigger publication.

The workflow uses `seihouse-verification` and reuses its completed checks. After
publishing, monitor checks and comments, fix actionable feedback on the same branch,
and report pending or blocked conditions accurately. It does not authorize a merge
or deployment.
