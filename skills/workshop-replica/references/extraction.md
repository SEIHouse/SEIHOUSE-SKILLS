# Workshop extraction

## Inspect both repositories

Locate the source route or entry point and its current exported symbol. Inspect the
presentation files and visual dependencies, then separate production dependencies
that need local replacements. Identify the destination's current preview wrapper,
component placement, tokens, assets, and registration contracts before adding files.
Present a concise file plan when useful; it is not an additional approval gate.

Before recording a source path:

1. Verify the file exists in the named source repository at the intended revision.
2. Verify its export and whether it was renamed or moved.
3. Use the actual repository-relative path, including any real source subdirectories.

A successful Workshop build does not verify a cross-repository path. Do not derive
the production path from the Workshop folder or a remembered name.

## Preserve presentation, replace production behavior

Copy or reconstruct the relevant layout and responsive proportions, typography,
spacing, colors, borders, icons, imagery, animation structure, controls, progress,
and surrounding presentation that materially affects visual judgment. Include the
target's meaningful loading, empty, success, and failure states.

Do not import chains of business logic to make a mock run. Replace authentication,
database/storage access, production APIs, generation, payments, real persistence,
account data, and production routing with local fixtures and explicit state.
Retain compatibility strings only when needed to model the visible behavior; they
must not trigger real calls. Reuse safe local assets or mock media where required,
and document differences. Do not fetch private production assets through copied
credentials or signed URLs.

## Simulate only meaningful states

Use names from the real flow. A target may need idle, opening, loading, generating,
progressing, completed, revealed, insufficient-resources, or error states; this is a
menu of examples, not a required union. Support deliberate switching and reset so
the relevant states can be inspected repeatedly. Clean up timers and local effects.

Keep preview controls, mock data, and the simulator outside reusable components.
The reference copy is the faithful baseline. Refine the development copy, preserving
an honest visual comparison. Record known deviations rather than claiming fidelity
because the component compiles.

## Reuse deliberately

Reuse verified Workshop typography, tokens, Library glyphs, safe assets, shared
effects, reduced-motion handling, and presentation primitives where they fit.
Confirm current exports and lifecycle needs. Do not force a familiar effect onto a
target with a different visual identity or create duplicate infrastructure.
