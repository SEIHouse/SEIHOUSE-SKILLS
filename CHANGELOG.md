# Changelog

Dates use `YYYY-MM-DD`. Skill update dates describe instruction changes; release
dates describe the version recorded here.

## [2.0.0] - 2026-11-14

- Redesigned the suite as ten model-neutral skills with shorter entry points and
  focused references for rendering and Workshop extraction, registration, and transfer.
- Replaced the planning gate with proportional planning and consolidated
  implementation verification and pre-PR self-review. See the migration guide for
  retired invocation names and replacements.
- Added PR check/review follow-through on the existing branch while honoring local-only
  requests and avoiding implicit merge or deployment authorization.
- Repaired synth voice records, input identity, glissando, release handling, keyboard
  mapping, and mobile guidance, with ten simulated lifecycle checks.
- Synchronized both plugin manifests, repository documentation, skill version/update
  metadata, and a reproducible version-and-date-named download.
- Kept old ZIPs in a labeled archive; their contents are not part of the current bundle.

## [1.0.0] - 2026-08-22

- Initial repository plugin manifest, recorded by source commit `61de1ad`.
- Historical ZIPs predate that manifest; their filenames are preserved separately
  without inferring additional release dates from internal file timestamps.
