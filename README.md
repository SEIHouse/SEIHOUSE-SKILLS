# SEIHouse Skills

Official AI agent skills for SEIHouse development, design, verification, and delivery.

**Current version: 2.0.0 · Updated: 2026-11-14 (November 14, 2026)**

Start with the [dated changelog](CHANGELOG.md), [2.0 migration guide](MIGRATION.md),
or [current and historical downloads](https://github.com/SEIHouse/SEIHOUSE-SKILLS/blob/main/zip/README.md).

## Skills

| Skill | Purpose |
|---|---|
| [browser-synth-builder](skills/browser-synth-builder/SKILL.md) | Playable Web Audio instruments and robust input handling. |
| [creative-ui-translator](skills/creative-ui-translator/SKILL.md) | Creative interaction briefs and explicitly requested implementations. |
| [seihouse-planning](skills/seihouse-planning/SKILL.md) | Proportional planning that respects task authorization and active modes. |
| [seihouse-codebase-conventions](skills/seihouse-codebase-conventions/SKILL.md) | Existing ownership, domain boundaries, and compatibility. |
| [seihouse-components-performance](skills/seihouse-components-performance/SKILL.md) | Evidence-based runtime, loading, and resilience improvements. |
| [seihouse-verification](skills/seihouse-verification/SKILL.md) | Implementation validation and focused pre-PR self-review. |
| [seihouse-layout-optimization](skills/seihouse-layout-optimization/SKILL.md) | Responsive composition, hierarchy, and reachable controls. |
| [seihouse-pr](skills/seihouse-pr/SKILL.md) | PR publishing, check monitoring, and same-branch review fixes. |
| [sensei-skill](skills/sensei-skill/SKILL.md) | Clear outcomes and meaningful product consequences. |
| [workshop-replica](skills/workshop-replica/SKILL.md) | Isolated visual replicas with verified source provenance. |

## Use the plugin

The repository includes a general `plugin.json` and a Codex-specific
`.codex-plugin/plugin.json`. Their shared package metadata stays synchronized.
The ten entry points live under `skills/`; keep each skill's linked references with
it. The PR workflow also links to the verification skill, so keep both when copying
those skills individually.

Use your host's supported plugin loading or skill installation mechanism. This
repository does not claim that every host supports the same discovery paths.
Updating this source does not automatically refresh installed caches or running
sessions.

## Dates and versions

Releases use semantic versions and ISO dates (`YYYY-MM-DD`). The changelog records
release dates, and each skill's `metadata.last_updated` records its instruction
update date. Dates must reflect actual changes; archive member timestamps alone
are not evidence of a release date. Older downloads keep their known identifiers
and are labeled historical.

## Validate or rebuild a download

Use Python 3.12 or newer and Node.js 24 or newer:

```text
python -m pip install -r requirements-dev.txt
python -B scripts/validate_plugin.py
python -B tests/test_release_tools.py
node tests/synth-lifecycle.cjs
python -B scripts/build_release.py --check
```

The `--check` command expects the committed download in a repository checkout. If
working from an extracted bundle, run the build command first to create that ZIP.
After intentional source changes, run `python -B scripts/build_release.py` to rebuild
the version-and-date-named ZIP, then run the checks again. The archive is generated
deterministically and excludes historical downloads and local caches.

The synth tests simulate DOM and Web Audio objects; they do not establish audible
quality, real browser input behavior, or physical-device performance.

## License metadata

Both plugin manifests retain the repository's existing `MIT` license declaration.
This update does not change licensing terms for historical archive contents.
