---
name: seihouse-components-performance
description: Diagnose and optimize a specified UI surface's runtime performance, loading, and resilience while preserving its design and functionality. Use for slow interactions, excessive work, resource leaks, or poor behavior on constrained devices and networks.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# SEIHouse Components Performance

Focus on the named component and the paths directly responsible for its performance.
Preserve its visual identity, product behavior, accessibility, and intended effects.
For an audit-only request, report evidence and recommendations without implementing.

## Establish the bottleneck

Observe a baseline or inspect concrete evidence before optimizing. Check the likely
causes for the affected path:

- repeated rendering, expensive computation, layout measurement, or main-thread work;
- heavy animation, particles, filters, blur, and work continuing while hidden;
- oversized assets, duplicate requests, blocked loading, or excess payloads;
- leaked timers, listeners, observers, subscriptions, and audio/graphics resources;
- broken cache, retry, stale-data, offline, timeout, or re-entry behavior.

Separate measured findings from plausible risks. Do not claim an improvement from a
code change alone or expand into a repository-wide audit without a verified cause.

## Optimize through existing systems

Prioritize the highest-impact verified problem. Reuse the project's caches, loaders,
asset pipelines, state systems, and shared utilities. Defer nonessential work and
clean up resources at the correct lifecycle boundary.

Where appropriate, adapt effect density, update frequency, or asset quality to
device capability and visibility. Preserve the intended atmosphere and functional
parity rather than removing an effect solely because it has a cost. Add dependencies
only when they solve the verified problem and fit the existing stack.

Keep network failures recoverable using established UI and retry patterns. Avoid
duplicate work, repeated restarts, or blocking primary content on secondary assets.

## Validate and report

Compare the affected behavior with the baseline using available project tools.
Select relevant checks for desktop/mobile, slow or failed requests, cached data,
remount/re-entry, backgrounding, reduced motion, and cleanup. Check directly affected
Library integration when applicable; do not assume every component belongs to it.

Report the verified bottleneck, changes, supporting measurements or observations,
and limitations. Do not claim physical-device or poor-network results from static
inspection. Flag significant layout work separately unless it is required to fix
the performance defect.
