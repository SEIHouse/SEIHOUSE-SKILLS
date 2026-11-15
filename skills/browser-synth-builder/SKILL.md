---
name: browser-synth-builder
description: Build a playable browser synthesizer with Web Audio, an onscreen keyboard, touch/mouse/computer-keyboard input, and working sound controls. Use for web instruments that run without a DAW or native plugins; not native VST/AU development or hardware MIDI integration.
metadata:
  version: "2.0.0"
  last_updated: "2026-11-14"
---

# Browser Synth Builder

Deliver a runnable instrument, usually a self-contained HTML page or small static
site with no external audio or runtime network dependencies. In an existing app,
use its tooling rather than forcing a separate architecture. Choose a concept,
visual identity, and synthesis approach suited to the request; plain Web Audio is
sufficient and does not require a plugin host or a particular framework.

## Playable baseline

- A musical default patch sounds after the first pointer or keyboard gesture that
  creates/resumes the AudioContext. Show an actionable failure if audio cannot start.
- Provide a piano-style keyboard with two octaves, or one octave and octave shifting,
  and visible pressed feedback for touch, mouse, and computer-keyboard input.
- Include octave controls, master volume, and at least four useful sound-shaping
  controls. Every displayed control must work and continuous changes should be smooth.
- Make the instrument readable and playable around 360px portrait width. Use one
  octave plus shifting when needed instead of squeezing two octaves into tiny keys.
  Keep primary controls reachable and secondary controls accessible through sensible
  reflow or scrolling. Preserve zoom outside the playing surface.

## Audio and input safeguards

Read [Web Audio patterns](references/web-audio-patterns.md) before implementing the
engine or input handling. Preserve these invariants while choosing the sound design:

- Resume audio from a user gesture and verify actual playback when tools allow it.
- Namespace pointer and keyboard identities and retain one consistent voice record.
- Release on pointerup, cancellation, lost capture, keyup, blur, and page hiding.
  Handle overlapping inputs and voice stealing without cutting gain abruptly.
- For captured-pointer glissando, hit-test coordinates during pointermove; do not
  depend on sibling pointerenter events. Keep pressed feedback correct when several
  inputs hold the same pitch.
- Use bounded polyphony, gain headroom, a compressor, click-resistant envelopes,
  and cleanup of stopped voices. A compressor does not guarantee distortion-free output.
- Scope touch-action to the playing surface. Do not hijack typing, form controls,
  modifier shortcuts, or normal page interactions.

## Verify and deliver

Run relevant project checks and exercise the actual preview when available. Verify
input modes, glissando, overlapping/repeated notes, release outside the keys,
cancellation, blur/backgrounding, octave changes, sound controls, volume, mobile
layout, and console errors. Listen for clicks, stuck notes, silence, and distortion
when audible testing is available; a simulated audio graph does not prove sound quality.

Deliver the page through the available preview mechanism and explain how to open
and play it. State which browser, touch, audible, and device checks actually ran and
which remain unverified; do not claim physical-device results from emulation.
