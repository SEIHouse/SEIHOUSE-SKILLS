# Web Audio Patterns for Browser Synths

Practical, battle-tested patterns for the safeguards in SKILL.md. Adapt freely to whatever synthesis design you choose.

## Contents

- AudioContext lifecycle (autoplay policy)
- Signal chain and headroom
- Note frequency math
- Click-free envelopes
- Voice management (polyphony, stealing, stuck notes)
- Continuous parameter smoothing (zipper noise)
- Pointer/touch keyboard input
- Computer keyboard input
- Mobile layout essentials
- Minimal voice example

## AudioContext lifecycle (autoplay policy)

Browsers block audio until a user gesture. Create the context lazily and resume it inside the gesture handler:

```js
let ctx;
function ensureAudio() {
  if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
  if (ctx.state === 'suspended') ctx.resume(); // must be called from a user-gesture handler
  return ctx;
}
```

Call `ensureAudio()` at the top of every pointerdown/keydown handler. On iOS Safari, resuming inside `touchstart`/`pointerdown` is required.

## Signal chain and headroom

Route every voice through a shared master chain:

```
voice → voice gain (envelope) → [filter etc.] → master gain → DynamicsCompressor → destination
```

- Set master gain to ~0.7–0.8, not 1.0.
- Scale per-voice peak gain by polyphony, e.g. `voicePeak = 0.6 / Math.sqrt(activeVoices)` or a fixed safe value like 0.15–0.25 per voice for 8-voice polyphony.
- Use the DynamicsCompressor as a gentle limiter (threshold ~ -12 dB, ratio ~ 12) to catch peaks, not as a substitute for proper gain staging.

## Note frequency math

```js
const freq = midi => 440 * Math.pow(2, (midi - 69) / 12);
```

Middle C = MIDI 60. Map the leftmost onscreen key to a base MIDI note (default 60) and shift it with octave buttons.

## Click-free envelopes

Instant gain changes cause clicks. Always ramp:

```js
const t = ctx.currentTime;
// attack: start from near-zero, ramp up
g.gain.setValueAtTime(0.0001, t);
g.gain.linearRampToValueAtTime(peak, t + attack);
// release: ramp down, then stop the oscillator AFTER the tail
g.gain.cancelScheduledValues(t);
g.gain.setValueAtTime(g.gain.value, t);
g.gain.exponentialRampToValueAtTime(0.0001, t + release);
osc.stop(t + release + 0.05);
```

- Never `exponentialRampToValueAtTime(0, ...)` — exponential ramps cannot reach zero; use 0.0001.
- Never call `osc.stop()` without a release ramp first.
- If attack/decay times are user-adjustable, clamp minimums to ~0.003 s to guarantee click-freedom.

## Voice management (polyphony, stealing, stuck notes)

Track every sounding note in a Map keyed by input identity (pointer ID or key code), not by note name — the same note can be triggered twice:

```js
const active = new Map(); // inputId -> { voice, midi }
function noteOn(inputId, midi) {
  if (active.has(inputId)) return;
  if (active.size >= MAX_VOICES) stealOldest();
  active.set(inputId, startVoice(midi));
}
function noteOff(inputId) {
  const n = active.get(inputId);
  if (n) { releaseVoice(n.voice); active.delete(inputId); }
}
```

- `MAX_VOICES` of 8–16 is safe; `stealOldest()` fades the oldest voice quickly (~50 ms) rather than cutting it.
- Safety net: on window `blur` and `visibilitychange`, release ALL active notes — this kills stuck notes when the user switches tabs or apps mid-note.

## Continuous parameter smoothing (zipper noise)

Knob/slider changes that jump straight to a parameter cause zipper noise. Smooth them:

```js
// instead of filter.frequency.value = x
filter.frequency.setTargetAtTime(x, ctx.currentTime, 0.02); // 20 ms smoothing
```

## Pointer/touch keyboard input

Use Pointer Events (covers mouse + touch + pen with one code path):

- On each key element: `pointerdown` → `setPointerCapture(e.pointerId)`, `noteOn(e.pointerId, midi)`, add a pressed CSS class.
- `pointerup` / `pointercancel` → `noteOff(e.pointerId)`, remove the class.
- Support glissando: on `pointerenter` while a pointer is captured/down, release that pointer's previous note and trigger the new one.
- CSS on keys: `touch-action: none; user-select: none; -webkit-user-select: none;` and call `e.preventDefault()` on pointerdown so the page never scrolls or zooms while playing.

## Computer keyboard input

```js
const KEYMAP = { a: 0, w: 1, s: 2, e: 3, d: 4, f: 5, t: 6, g: 7, y: 8, h: 9, u: 10, j: 11, k: 12 };
window.addEventListener('keydown', e => {
  if (e.repeat) return;                       // ignore auto-repeat
  if (e.target.matches('input, textarea')) return; // don't hijack typing
  const s = KEYMAP[e.key.toLowerCase()];
  if (s !== undefined) noteOn('kbd:' + e.key.toLowerCase(), baseMidi + s);
});
window.addEventListener('keyup', e => noteOff('kbd:' + e.key.toLowerCase()));
```

Use `e.key` (layout-independent letters) with a `kbd:` prefix as the input ID. Show the mapped letter on each onscreen key so the mapping is discoverable. Reserve keys like `z`/`x` for octave down/up.

## Mobile layout essentials

- Test at 360px width portrait. Prefer a horizontal key strip sized to fit: `flex` row of keys with white keys ~44px+ wide at minimum, black keys overlaid absolutely.
- Keep critical controls visible without scrolling; group secondary controls in a collapsible panel if needed.
- No hover-only affordances; all feedback must work on touch.
- Prevent double-tap zoom: `touch-action: manipulation` on the page, `touch-action: none` on keys.

## Minimal voice example

```js
function startVoice(midi) {
  const t = ctx.currentTime;
  const osc = ctx.createOscillator();
  osc.type = patch.wave;
  osc.frequency.value = freq(midi);
  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.setTargetAtTime(patch.cutoff, t, 0.02);
  const g = ctx.createGain();
  g.gain.setValueAtTime(0.0001, t);
  g.gain.linearRampToValueAtTime(voicePeak, t + patch.attack);
  osc.connect(filter).connect(g).connect(masterGain);
  osc.start(t);
  return { osc, g };
}
```

Extend freely — detuned oscillator pairs, sub-oscillators, FM, LFOs, delay/reverb sends — but keep this envelope and chain structure so the safeguards hold.
