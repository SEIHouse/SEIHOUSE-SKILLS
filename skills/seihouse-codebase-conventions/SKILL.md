---
name: seihouse-codebase-conventions
description: Locate the existing owner of behavior in SEIHouse repositories and preserve its architecture, data, and public contracts. Use for unfamiliar domain flows, cross-layer changes, or requests to reuse existing SEIHouse systems.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# SEIHouse Codebase Conventions

The current repository is the implementation source of truth. Product references
explain responsibilities; they do not prove that a path, API, or migration still
exists. Find the current owner before adding a parallel service, store, component,
persistence path, or media lifecycle.

## Orient only as far as needed

1. Read applicable repository guidance and inspect the relevant entry point,
   implementation, imports, and checks. Search by behavior and domain terms as well
   as the user's label.
2. Identify the UI surface, domain owner, authoritative state, persistence/media
   owners, and directly affected consumers. Trace a representative flow when the
   change crosses these boundaries.
3. Establish the inputs, outputs, compatibility constraints, and targeted validation.
   Reuse prior findings when still valid; avoid broad archaeology for a local change.

## Preserve ownership and contracts

- Extend established systems and shared primitives instead of duplicating them.
- Keep domain truth, transient UI state, derived values, caches, and durable data
  distinct. Avoid competing authoritative state or write paths.
- Verify the active Firebase, Postgres, and object-storage split before changing it.
  Preserve existing data and retained compatibility identifiers; do not expand an
  old persistence system simply because it is convenient.
- Preserve stable product terminology and directly affected loading, error,
  accessibility, responsive, and resource-lifecycle behavior.
- Keep generated content tied to its story, source context, and media records.
  Protect existing canonical data and user edits during regeneration.
- Preserve shared canon and media relationships without building speculative future
  product surfaces or generalizing a local component unnecessarily.

## Load references by need

- Read relevant sections of [the system map](references/system_map.md) when product
  concepts or responsibility boundaries are unfamiliar: Library, generation, Reader
  Chamber, Codex, Harmony, media, profiles, rewards, Workshop, and audio.
- Read [engineering conventions](references/conventions.md) for affected state,
  persistence, API, synchronization, or shared-component decisions.
- Use the relevant part of [the change protocol](references/change_protocol.md) to
  select checks for UI, state, generation, media, schema, or performance changes.

Implement through the verified owner, validate the requested behavior and nearest
likely regression, and explain the outcome and any material limitation concisely.
