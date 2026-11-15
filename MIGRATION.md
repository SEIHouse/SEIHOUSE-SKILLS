# SEIHouse Skills 2.0 migration — 2026-11-14

Version 2.0 provides ten model-neutral skills. Update saved prompts and workflow
instructions that invoke these retired names:

| Retired invocation | Replacement |
|---|---|
| `plan-mode-gate` | `seihouse-planning` |
| `seihouse-gemini-verification-loop` | `seihouse-verification` |
| `seihouse-pr-review` | `seihouse-verification` |

No alias skills remain. The other eight invocation names are unchanged.

Planning requires a separate approval when the user requests planning before edits
or the active environment requires it. Authorized implementation can otherwise
continue after proportional planning.

Verification combines implementation checks and pre-PR self-review. Checks depend on
the project and changed behavior; there is no universal JavaScript build requirement.

The PR skill defaults to committing, pushing, and creating or updating a PR after
implementation, then monitoring checks and resolving review feedback on the same
branch. A user request for local-only work overrides that default. Publishing does
not authorize merging, deployment, or unrelated changes.

The 2.0.0 source, both plugin manifests, and dated download bundle are maintained
together. See [the changelog](CHANGELOG.md) and
[downloads](https://github.com/SEIHouse/SEIHOUSE-SKILLS/blob/main/zip/README.md) for version
and date information. Historical downloads are retained separately and are not the
current plugin.

Updating source or downloading a bundle does not refresh a host-managed plugin
cache. Existing loaded sessions may retain old instructions until the plugin is
reloaded through the host's supported mechanism; host reload behavior is not tested
by this release's validation.
