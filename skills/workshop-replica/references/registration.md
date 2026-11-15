# Workshop registration and provenance

## One feature, one discovery entry

Inspect the current manifest, registry/router, workspace wrapper, and homepage
discovery contracts. Register one stable preview ID with a direct URL and one card
per feature. Update the existing entry when refining a feature; do not add parallel
V2, V3, Revised, or Experimental entries or folders for visual iterations.

Keep a single feature folder with a `reference/` and `development/` split, adapting
the surrounding paths and filenames to current repository conventions. For example:

```text
<feature>/
  reference/<Component>.tsx
  development/<Component>.tsx
  shared/                    # only if shared code is needed
  README.md
<preview-root>/<feature>/
  <Workspace>.tsx
  previewData.ts
  previewStates.ts
```

Separate reusable presentation from preview wrappers, simulator state, mock data,
and Workshop navigation. Reuse the current workspace primitive when present.
Do not reorganize unrelated previews to force this example's exact paths.

## Verify the registration contract

Record source repository, repository-relative path, export, inspected branch/commit,
and last-comparison date using the current metadata schema. If the schema supports
only a subset, retain the other provenance in the feature README; do not invent
unsupported manifest fields. Build imports against verified current exports.

Verify the direct URL, registry entry, and discovery card refer to the same preview.
Check directly affected existing previews after changes to shared registration.

## Feature README

Keep provenance near the top:

```markdown
# <Feature>

- **Source repository:** <owner/repository>
- **Source revision:** <inspected commit and branch, when applicable>
- **Source location/export:** <verified path and symbol>
- **Workshop preview:** <actual direct URL or route>
- **Replica created:** YYYY-MM-DD
- **Last Workshop update:** YYYY-MM-DD
- **Last source comparison:** YYYY-MM-DD
- **Replica status:** faithful replica | under refinement | approved | transferred back
```

Use the real current date from task context. Preserve the original creation date;
do not invent a missing historical date. Mark unknown history honestly.

On a material replica change, update Last Workshop update and append a concise
Workshop history entry. Update Last source comparison only after actually inspecting
the source again. Change status only when the real lifecycle supports it; do not
claim approval or transfer that did not happen. Skip formatting-only history noise.

Also document what was copied or reconstructed, what was mocked, available states,
reusable dependencies, excluded production dependencies, known visual differences,
verified transfer files, and transfer cautions. Keep this feature-local documentation
useful rather than duplicating the entire skill.
