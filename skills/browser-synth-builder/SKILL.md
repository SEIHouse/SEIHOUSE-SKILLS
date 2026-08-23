---
name: browser-synth-builder
description: Build a complete, runnable, playable browser-based synthesizer ("VST-style synth in the browser") from requests like "make me a playable VST synth", "build a synthesizer with a working keyboard", "create a web instrument / playable piano / Web Audio synth", or any ask for a sound-producing music instrument page with a modern instrument design. Use when the deliverable must produce sound immediately in a browser preview without a DAW, plugins, or installation. Covers Web Audio implementation, onscreen keyboards with touch/mouse/computer-keyboard input, sound controls, and polished instrument UI. Not for native/DAW plugin development (VST3/AU), MIDI hardware integrations, or DAW host compatibility.
---

# Browser Synth Builder

Build a synthesizer that runs entirely in the browser using the Web Audio API — no build step, no external audio files, no network dependencies. A single self-contained HTML file (or a small static site) is the ideal shape so it opens and plays immediately in any web preview.

## Creative Freedom — Keep the Prompt Open-Ended

The point of this task is creative range. Choose your own:

- **Concept and identity** — name, personality, and visual language of the instrument.
- **Synthesis method** — subtractive, FM, additive, wavetable-ish, physical-modeling-flavored, sample-free drum/keys hybrids, or any Web Audio technique.
- **Controls, layout, and aesthetics** — knobs, sliders, pads, sequencer extras, theme, typography.

Do NOT require or suggest WAM, WebAssembly, Faust, DAW integration, plugin-host compatibility, external libraries, or any fixed architecture. Plain Web Audio API is sufficient and preferred.

## Non-Negotiable Requirements

Every delivered synth must:

1. **Produce sound immediately** — a musical default patch; notes audible on the first key press after one user gesture (browser autoplay policy requires a gesture: resume the AudioContext inside a pointer/key handler).
2. **Include a working onscreen keyboard** — piano-style keys spanning at least two octaves (or one octave plus octave-shift buttons), with pressed-state visual feedback.
3. **Support three input modes** — touch, mouse, and computer keyboard (e.g. A W S E D F T G Y H U J K across an octave). Include octave up/down controls so the full range is reachable.
4. **Provide useful sound controls** — at least four controls that audibly shape the sound (e.g. oscillator/waveform, filter cutoff, resonance, ADSR stages, detune, delay/reverb amount), plus a master volume. Every visible control must actually work.
5. **Present a polished, modern instrument interface** — deliberate visual design, readable labels, coherent color/type, and a layout that remains fully usable at mobile portrait width (~360px).

## Safeguards (Must Pass All)

Guard against the six classic failures. Implementation patterns for each are in [references/web-audio-patterns.md](references/web-audio-patterns.md) — read it before writing the audio engine.

- **Silent audio** — create/resume `AudioContext` on the first user gesture; verify the default patch is audible at moderate volume.
- **Stuck notes** — release notes on `pointerup`/`pointercancel`/window `blur` and `keyup`; track active notes by pointer ID and key code; cap polyphony with voice stealing.
- **Clicks and pops** — never switch gain instantly; use short attack/release ramps and stop oscillators only after the release tail.
- **Excessive volume** — scale per-voice gain by active voice count, keep master headroom, route through a gentle limiter (`DynamicsCompressor`).
- **Broken controls** — wire every knob/slider/button to a real audio parameter; smooth continuous changes to avoid zipper noise.
- **Unusable mobile layout** — `touch-action: none` on keys, preventDefault on key touches so the page doesn't scroll, touch-sized keys, no hover-only interactions.

## Workflow

1. Pick a concept, synthesis approach, and control set (your creative choice).
2. Build the audio engine following references/web-audio-patterns.md.
3. Build the onscreen keyboard and all three input modes.
4. Design the interface; verify it at desktop and ~360px mobile widths.
5. Run the acceptance checklist below before delivering.
6. Deliver as a browser-openable page (single `index.html` or static site) through the environment's web preview/versioning mechanism.

## Acceptance Checklist

Verify in the actual preview before delivery:

- Pressing a key with mouse, touch, and computer keyboard each produces sound with visible key feedback.
- Sliding a finger/cursor across keys plays a clean glissando with no stuck notes afterward.
- Releasing all inputs (including window blur mid-note) leaves no ringing notes.
- Fast repeated note on/off produces no audible clicks.
- Every control audibly changes the sound; master volume reaches silence at minimum and stays undistorted at maximum.
- At 360px portrait width, all keys and controls are reachable and playable.
- No console errors.
