---
name: workshop-replica
description: Extract or synchronize a faithful application page, component, or flow in the SEIHouse visual Workshop using isolated mock state, verified source linkage, and portable presentation code. Use for safe visual refinement before a separately authorized production transfer.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# Workshop Replica

Create a trustworthy visual comparison point and an isolated development copy of
the real target. Replace production behavior with local mock state while keeping
presentation portable. Extraction does not authorize editing the source application
or transferring refinements into production.

## Establish the target and owners

Resolve the target, source repository, intended source branch/commit, and destination
Workshop from the request and available repositories. Ask only for unresolved
identifiers or product decisions. Inspect current repository instructions and
interfaces; historical repository names, paths, and exports are not authority.

Use the verified production name for shared concepts. Developer-facing renames do
not authorize changing stored values, API routes, database fields, or storage keys.

## Extract and simulate

Read [extraction](references/extraction.md) before building or updating the replica.
Preserve meaningful layout, typography, imagery, animation, interaction hierarchy,
and visual states. Do not redesign during extraction unless requested.

Keep production APIs, authentication, databases, object-storage operations, generation,
payments, real user data, secrets, and production environment dependencies out of the
replica. Use local fixtures, timers, and explicit preview states. Keep mock behavior
and Workshop controls outside reusable presentation code.

## Register and document

Read [registration and provenance](references/registration.md) when adding a preview
or changing its registry or metadata. Reuse current Workshop systems and registration
interfaces, preserve a reference/development split, and expose one discovery entry
per feature. Verify source paths against the named repository and revision.

Read [synchronization and transfer](references/transfer.md) when a source name/path
changes or a transfer is requested. Preserve reference integrity and compatibility
identifiers; production integration requires its own task authorization.

## Verify and deliver

Build with the Workshop's actual tooling and open the direct preview. Check all
meaningful simulated states, affected mobile/tablet/desktop layouts, long and missing
content, and reduced motion. Verify that no production API calls or secrets entered
the dependency chain and that affected existing previews still work.

Report the preview route, available states, verified source revision/path/export,
what was mocked, relevant changes, build/interaction results, and visual differences
or limitations. Report provenance dates and retained compatibility identifiers when
they changed or affect transfer. Claim visual parity only to the extent observed.
