# Web Audio patterns for browser synths

These connected examples illustrate a simple eight-voice patch and robust input
lifecycle. Adapt the sound engine freely while preserving input identity, bounded
voices, gain continuity, and cleanup. The snippets share scope; initialize the DOM
bindings after the page's keyboard exists. They are not a complete instrument UI.

## Audio lifecycle and headroom

Create and resume a single context inside a user gesture. Handle resume failures
in the actual interface. Route voices through master gain and a compressor; choose
headroom for the real patch and voice limit, then listen for distortion.

```js
let ctx;
let masterGain;
const MAX_VOICES = 8;
const patch = { wave: 'sine', cutoff: 4000, attack: 0.01, release: 0.15 };
const freq = midi => 440 * Math.pow(2, (midi - 69) / 12);

function ensureAudio() {
  if (!ctx) {
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    masterGain = ctx.createGain();
    masterGain.gain.value = 0.7;
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -12;
    compressor.ratio.value = 12;
    masterGain.connect(compressor).connect(ctx.destination);
  }
  if (ctx.state === 'suspended' || ctx.state === 'interrupted') {
    ctx.resume().catch(error => {
      // Replace with visible retry feedback in the instrument UI.
      console.error('Audio could not start', error);
    });
  }
  return ctx;
}
```

Use a conservative fixed per-voice peak here. If normalizing dynamically, smooth
existing voices too; scaling only newly created voices by the active count does not
normalize a chord. Account for release tails when evaluating peak output. Smooth
live parameters with AudioParam automation, such as
`filter.frequency.setTargetAtTime(value, ctx.currentTime, 0.02)`. Wire master volume
to master gain, including zero. The example patch is a baseline, not the required
four-control instrument implementation.

## Consistent voice records and click-resistant release

The Map stores `{ voice, midi }` for every input. A voice owns its nodes and release
state. The fallback release calculation below matches this example's linear attack
and constant sustain; a full ADSR engine must track its own envelope segments.

```js
const active = new Map();

function startVoice(midi) {
  ensureAudio();
  const t = ctx.currentTime;
  const attack = Math.max(0.003, patch.attack);
  const peak = 0.08;
  const osc = ctx.createOscillator();
  const filter = ctx.createBiquadFilter();
  const gain = ctx.createGain();
  osc.type = patch.wave;
  osc.frequency.value = freq(midi);
  filter.type = 'lowpass';
  filter.frequency.value = patch.cutoff;
  gain.gain.setValueAtTime(0, t);
  gain.gain.linearRampToValueAtTime(peak, t + attack);
  osc.connect(filter).connect(gain).connect(masterGain);
  const voice = { osc, filter, gain, startedAt: t, attack, peak, released: false };
  osc.onended = () => {
    osc.disconnect();
    filter.disconnect();
    gain.disconnect();
  };
  osc.start(t);
  return voice;
}

function releaseVoice(voice, duration = patch.release) {
  if (voice.released) return;
  voice.released = true;
  const t = ctx.currentTime;
  const param = voice.gain.gain;
  if (typeof param.cancelAndHoldAtTime === 'function') {
    param.cancelAndHoldAtTime(t);
  } else {
    const level = voice.peak * Math.min(1, Math.max(0,
      (t - voice.startedAt) / voice.attack));
    param.cancelScheduledValues(t);
    param.setValueAtTime(level, t);
  }
  const end = t + Math.max(0.003, duration);
  param.linearRampToValueAtTime(0, end);
  voice.osc.stop(end + 0.01);
}

function noteOn(inputId, midi) {
  if (active.has(inputId)) return;
  if (active.size >= MAX_VOICES) noteOff(active.keys().next().value, 0.03);
  active.set(inputId, { voice: startVoice(midi), midi });
  syncPressedKeys();
}

function noteOff(inputId, duration) {
  const record = active.get(inputId);
  if (!record) return;
  active.delete(inputId);
  releaseVoice(record.voice, duration);
  syncPressedKeys();
}

function releaseAll() {
  for (const inputId of [...active.keys()]) noteOff(inputId);
}
```

The active-input limit excludes fading release tails; rapid retriggering and stealing
can briefly leave more audio nodes alive. If the patch needs a strict total voice
budget, track release tails and bound them with a short fade as well. Never stop an
oscillator abruptly or ramp exponentially to zero. Disconnect nodes after the tail.

## Captured-pointer glissando and shared pitch feedback

Give each key a numeric `data-midi` attribute. Use `#keyboard` for the playing surface,
and `[data-octave-shift="-1"]` / `[data-octave-shift="1"]` on octave buttons.
The surface must contain only the playable keys; place other controls outside it.
Capture on the stable surface, then hit-test coordinates because captured events
target that surface even when the pointer crosses other keys.

```js
const keyboard = document.querySelector('#keyboard');
const downPointers = new Set();

function syncPressedKeys() {
  const pitches = new Set([...active.values()].map(record => record.midi));
  for (const key of keyboard.querySelectorAll('[data-midi]')) {
    key.classList.toggle('pressed', pitches.has(Number(key.dataset.midi)));
  }
}

function keyAt(x, y) {
  const key = document.elementFromPoint(x, y)?.closest('[data-midi]');
  return key && keyboard.contains(key) ? key : null;
}

function movePointer(event) {
  const id = `ptr:${event.pointerId}`;
  const key = keyAt(event.clientX, event.clientY);
  const midi = key ? Number(key.dataset.midi) : null;
  if (active.get(id)?.midi === midi) return;
  noteOff(id);
  if (midi !== null) noteOn(id, midi);
}

keyboard.addEventListener('pointerdown', event => {
  if (event.button !== 0 || !keyAt(event.clientX, event.clientY)) return;
  ensureAudio();
  event.preventDefault();
  downPointers.add(event.pointerId);
  keyboard.setPointerCapture(event.pointerId);
  movePointer(event);
});
keyboard.addEventListener('pointermove', event => {
  if (downPointers.has(event.pointerId)) movePointer(event);
});

function endPointer(event) {
  downPointers.delete(event.pointerId);
  noteOff(`ptr:${event.pointerId}`);
}
for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) {
  keyboard.addEventListener(type, endPointer);
}

function resetInputs() {
  for (const pointerId of downPointers) {
    if (keyboard.hasPointerCapture(pointerId)) keyboard.releasePointerCapture(pointerId);
  }
  downPointers.clear();
  releaseAll();
}
window.addEventListener('blur', resetInputs);
document.addEventListener('visibilitychange', () => {
  if (document.hidden) resetInputs();
});
```

After pointerup/cancel, the browser releases capture; repeated lost-capture cleanup
is harmless because noteOff is idempotent. Moving outside the keys releases the note
while retaining the down-pointer state so re-entry can play. Multiple inputs holding
one pitch keep it visibly pressed until the final holder releases.

For background context, see [W3C Pointer Events](https://www.w3.org/TR/pointerevents/).

## Computer keyboard and octave changes

This mapping uses physical `event.code` positions, matching a familiar US-layout
instrument pattern. Letters on other layouts can differ; label controls appropriately
or add layout-aware labels when needed. `event.key` represents the interpreted key
value, including the active layout and modifiers; it is not layout-independent.

```js
const KEYMAP = { KeyA: 0, KeyW: 1, KeyS: 2, KeyE: 3, KeyD: 4, KeyF: 5,
  KeyT: 6, KeyG: 7, KeyY: 8, KeyH: 9, KeyU: 10, KeyJ: 11, KeyK: 12 };
let baseMidi = 60;

function shiftOctave(delta) {
  const next = Math.min(84, Math.max(24, baseMidi + delta * 12));
  if (next === baseMidi) return;
  resetInputs();
  for (const key of keyboard.querySelectorAll('[data-midi]')) {
    key.dataset.midi = String(Number(key.dataset.midi) + next - baseMidi);
  }
  baseMidi = next;
  syncPressedKeys();
  // Update displayed pitch/octave labels in the instrument UI as well.
}

function ignoresPlayingKeys(event) {
  return event.ctrlKey || event.metaKey || event.altKey || event.shiftKey ||
    event.target?.closest?.('input, textarea, select, button, [contenteditable]:not([contenteditable="false"]), [role="slider"], [role="spinbutton"], [role="textbox"]') ||
    event.target?.isContentEditable;
}

window.addEventListener('keydown', event => {
  if (event.repeat || ignoresPlayingKeys(event)) return;
  if (event.code === 'KeyZ' || event.code === 'KeyX') {
    event.preventDefault();
    shiftOctave(event.code === 'KeyZ' ? -1 : 1);
    return;
  }
  const step = KEYMAP[event.code];
  if (step === undefined) return;
  event.preventDefault();
  noteOn(`kbd:${event.code}`, baseMidi + step);
});
window.addEventListener('keyup', event => noteOff(`kbd:${event.code}`));
for (const button of document.querySelectorAll('[data-octave-shift]')) {
  button.addEventListener('click', () => shiftOctave(Number(button.dataset.octaveShift)));
}
```

Release keyup identities even if focus or modifiers changed since keydown. This
example ends held notes before shifting octaves; another design may keep sounding
pitches, but must retain the original note identity through release.

## Mobile layout and cleanup

Use `touch-action: none` and `user-select: none` on the playing surface and keys,
with `-webkit-user-select: none` where needed. Do not disable browser zoom globally.
At 360px, seven white keys can fit with useful touch width; a second octave may need
shifting or a carefully designed scrollable keyboard. Keep black keys visibly and
physically distinguishable without shrinking the whole interface.

Use touch-sized octave buttons, readable labels, and no hover-only controls. Reflow
or scroll secondary controls instead of claiming they must all fit above the fold.
When unmounting in an application, remove registered listeners, reset inputs, and
dispose of audio resources according to the owning application's lifecycle.
