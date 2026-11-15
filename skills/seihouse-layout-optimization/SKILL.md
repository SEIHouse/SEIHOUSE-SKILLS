---
name: seihouse-layout-optimization
description: Audit and refine a specified UI surface's responsive composition, hierarchy, and usability across viewport sizes and content states. Use for overflow, clipping, cramped or unbalanced layouts, and inaccessible controls while preserving functionality and visual identity.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# SEIHouse Layout Optimization

Focus on the named surface and directly affected layout code. Preserve its identity,
product behavior, meaningful content, and accessibility. For an audit-only request,
report findings and recommendations without implementing.

## Inspect the composition

Identify the focal element, supporting content, required controls, decorative layers,
anchoring, and relationship to the surrounding page. Inspect:

- overflow, clipping, overlap, accidental scrolling, and empty or cramped space;
- text wrapping, hierarchy, long values, missing content, and asset framing;
- fixed/sticky/absolute elements, overlays, menus, and animation containment;
- safe areas, browser chrome, virtual keyboards, and limited vertical space;
- touch targets, focus visibility, larger text, and zoom.

Evaluate tablet as a distinct range. Check intermediate widths and landscape or
short screens instead of relying only on named device presets.

## Refine deliberately

Decide what should scale, reflow, stack, reposition, or use an alternate composition.
Prefer intrinsic sizing, flexible layout, bounded dimensions, and CSS over viewport
JavaScript when CSS handles the behavior reliably. Choose breakpoints where the
content's composition needs to change, following existing project conventions.

Keep the focal element anchored and controls reachable. Do not solve fit by shrinking
everything, hiding meaningful content, or flattening hierarchy. Keep decorative
effects contained, preserve reduced motion, and avoid unrelated redesign or a new
global design system unless a verified shared defect requires a shared fix.

## Validate and report

Select representative small/large mobile, tablet portrait/landscape, laptop/desktop,
wide, narrow-window, and short-height viewports relevant to the component. Check
intermediate widths around changed breakpoints.

Exercise affected loading, empty, error, populated, expanded, overlay, and animation
states, along with long text and larger text/zoom. Confirm intentional spacing and
hierarchy, no inaccessible controls or accidental overflow, and no surrounding-page
regression. Browser resizing does not prove physical-device behavior.

Report the main layout defects, what reflows across important ranges, validation,
and material limitations. Flag substantial runtime or loading work separately unless
it directly causes the layout defect.
