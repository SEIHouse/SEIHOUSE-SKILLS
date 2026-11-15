const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');

const reference = fs.readFileSync(path.join(__dirname, '../skills/browser-synth-builder/references/web-audio-patterns.md'), 'utf8').replace(/\r\n/g, '\n');
const blocks = [...reference.matchAll(/```js\n([\s\S]*?)```/g)].map(match => match[1]);
assert.equal(blocks.length, 4);
const source = blocks.join('\n');

function environment({ hold = true } = {}) {
  const nodes = [];
  const keys = [60, 61, 62].map(midi => {
    const key = {
      dataset: { midi: String(midi) }, pressed: false,
      closest(selector) { return selector === '[data-midi]' ? this : null; },
      classList: { toggle(name, value) { if (name === 'pressed') key.pressed = value; } },
    };
    return key;
  });
  const events = () => ({
    listeners: new Map(),
    addEventListener(type, fn) { this.listeners.set(type, fn); },
    dispatch(type, event = {}) { this.listeners.get(type)?.(event); },
  });
  const capture = new Set();
  const keyboard = Object.assign(events(), {
    contains(key) { return keys.includes(key); },
    querySelectorAll() { return keys; },
    setPointerCapture(id) { capture.add(id); },
    hasPointerCapture(id) { return capture.has(id); },
    releasePointerCapture(id) { capture.delete(id); this.dispatch('lostpointercapture', { pointerId: id }); },
  });
  const octaveButtons = [-1, 1].map(delta => Object.assign(events(), { dataset: { octaveShift: String(delta) } }));
  const doc = Object.assign(events(), {
    hidden: false,
    querySelector() { return keyboard; },
    querySelectorAll() { return octaveButtons; },
    elementFromPoint(x, y) { return y >= 0 && y < 100 && x >= 0 && x < 90 ? keys[Math.floor(x / 30)] : null; },
  });
  function param() {
    const value = {
      value: 0, operations: [],
      setValueAtTime(v, t) { this.operations.push(['set', v, t]); },
      linearRampToValueAtTime(v, t) { this.operations.push(['ramp', v, t]); },
      cancelScheduledValues(t) { this.operations.push(['cancel', t]); },
    };
    if (hold) value.cancelAndHoldAtTime = t => value.operations.push(['hold', t]);
    return value;
  }
  function node(type) {
    const n = {
      kind: type, gain: param(), frequency: param(), threshold: param(), ratio: param(),
      connected: [], stops: [], disconnected: false,
      connect(other) { this.connected.push(other); return other; },
      disconnect() { this.disconnected = true; },
      start(t) { this.startedAt = t; },
      stop(t) { this.stops.push(t); },
    };
    nodes.push(n);
    return n;
  }
  class AudioContext {
    constructor() { this.currentTime = 0; this.state = 'suspended'; this.destination = {}; this.resumes = 0; }
    createGain() { return node('gain'); }
    createDynamicsCompressor() { return node('compressor'); }
    createOscillator() { return node('osc'); }
    createBiquadFilter() { return node('filter'); }
    resume() { this.resumes++; this.state = 'running'; return Promise.resolve(); }
  }
  const win = Object.assign(events(), { AudioContext });
  const context = vm.createContext({ window: win, document: doc, console });
  vm.runInContext(source, context, { filename: 'web-audio-patterns-extracted.js' });
  return { context, nodes, keys, keyboard, win, doc, octaveButtons, capture, run: code => vm.runInContext(code, context) };
}

let count = 0;
function test(name, fn) {
  fn(); count++;
  console.log('PASS ' + name);
}
const pointer = (pointerId, clientX, clientY = 20) => ({ pointerId, clientX, clientY, button: 0, preventDefault() {} });
const keyEvent = (code, extra = {}) => ({ code, repeat: false, target: {}, preventDefault() {}, ...extra });

test('first note resumes audio, stores a consistent record, and stops only after release', () => {
  const e = environment();
  e.run("noteOn('kbd:KeyA', 60)");
  assert.equal(e.run('ctx.resumes'), 1);
  assert.equal(e.run("active.get('kbd:KeyA').midi"), 60);
  assert.equal(e.run("active.get('kbd:KeyA').voice.osc.frequency.value"), 261.6255653005986);
  assert(e.keys[0].pressed);
  e.run("noteOff('kbd:KeyA')");
  assert.equal(e.run('active.size'), 0);
  const osc = e.nodes.find(n => n.kind === 'osc');
  assert.equal(osc.stops.length, 1);
  assert(osc.stops[0] >= 0.15);
  assert(!e.keys[0].pressed);
  osc.onended();
  assert(osc.disconnected);
  assert(e.nodes.filter(n => ['filter', 'gain'].includes(n.kind)).slice(1).every(n => n.disconnected));
});

test('overlapping pointer/keyboard inputs at one pitch retain independent ownership and feedback', () => {
  const e = environment();
  e.keyboard.dispatch('pointerdown', pointer(1, 10));
  e.win.dispatch('keydown', keyEvent('KeyA'));
  assert.equal(e.run('active.size'), 2);
  e.keyboard.dispatch('pointerup', pointer(1, 10));
  assert.equal(e.run('active.size'), 1);
  assert(e.keys[0].pressed);
  e.win.dispatch('keyup', keyEvent('KeyA'));
  assert.equal(e.run('active.size'), 0);
  assert(!e.keys[0].pressed);
});

test('repeated note-on and repeated release do not duplicate voices or stops', () => {
  const e = environment();
  e.run("noteOn('ptr:9', 60); noteOn('ptr:9', 60); noteOff('ptr:9'); noteOff('ptr:9')");
  assert.equal(e.nodes.filter(n => n.kind === 'osc').length, 1);
  assert.equal(e.nodes.find(n => n.kind === 'osc').stops.length, 1);
});

test('captured glissando uses coordinates, releases outside, and retriggers on re-entry', () => {
  const e = environment();
  e.keyboard.dispatch('pointerdown', pointer(7, 10));
  assert(e.capture.has(7));
  e.keyboard.dispatch('pointermove', pointer(7, 40));
  assert.equal(e.run("active.get('ptr:7').midi"), 61);
  assert(!e.keys[0].pressed && e.keys[1].pressed);
  e.keyboard.dispatch('pointermove', pointer(7, 120));
  assert.equal(e.run('active.size'), 0);
  e.keyboard.dispatch('pointermove', pointer(7, 70));
  assert.equal(e.run("active.get('ptr:7').midi"), 62);
  e.keyboard.dispatch('pointerup', pointer(7, 120));
  assert.equal(e.run('active.size'), 0);
  assert.equal(e.run('downPointers.size'), 0);
});

test('pointercancel and lostpointercapture cleanup are idempotent', () => {
  const e = environment();
  e.keyboard.dispatch('pointerdown', pointer(4, 10));
  e.keyboard.dispatch('pointercancel', pointer(4, 10));
  e.keyboard.dispatch('lostpointercapture', pointer(4, 10));
  e.keyboard.dispatch('pointermove', pointer(4, 40));
  assert.equal(e.run('active.size'), 0);
  assert.equal(e.nodes.find(n => n.kind === 'osc').stops.length, 1);
});

test('blur and page hiding release all inputs, captures, and feedback', () => {
  const e = environment();
  for (const type of ['blur', 'visibilitychange']) {
    e.keyboard.dispatch('pointerdown', pointer(2, 40));
    e.win.dispatch('keydown', keyEvent('KeyA'));
    if (type === 'blur') e.win.dispatch(type);
    else { e.doc.hidden = true; e.doc.dispatch(type); }
    assert.equal(e.run('active.size'), 0);
    assert.equal(e.run('downPointers.size'), 0);
    assert.equal(e.capture.size, 0);
    assert(e.keys.every(k => !k.pressed));
  }
});

test('voice stealing fades the oldest input and keeps the active limit', () => {
  const e = environment();
  e.run("for (let i = 0; i < 9; i++) noteOn('kbd:' + i, 60 + i)");
  assert.equal(e.run('active.size'), 8);
  assert(!e.run("active.has('kbd:0')"));
  assert.equal(e.nodes.filter(n => n.kind === 'osc')[0].stops[0], 0.04);
});

test('fallback release during attack holds the calculated envelope level', () => {
  const e = environment({ hold: false });
  e.run("noteOn('kbd:KeyA', 60); ctx.currentTime = 0.005; noteOff('kbd:KeyA')");
  const ops = e.nodes.filter(n => n.kind === 'gain')[1].gain.operations;
  assert(ops.some(op => op[0] === 'set' && op[1] === 0.04 && op[2] === 0.005));
  assert(ops.some(op => op[0] === 'ramp' && op[1] === 0));
});

test('typing, controls, modifier shortcuts, and auto-repeat do not start notes', () => {
  const e = environment();
  for (const extra of [{ repeat: true }, { ctrlKey: true }, { altKey: true }, { metaKey: true },
    { shiftKey: true }, { target: { closest: () => ({}) } }, { target: { isContentEditable: true } }]) {
    e.win.dispatch('keydown', keyEvent('KeyA', extra));
  }
  assert.equal(e.nodes.length, 0);
  e.win.dispatch('keydown', keyEvent('KeyA'));
  e.win.dispatch('keyup', keyEvent('KeyA', { ctrlKey: true, target: { isContentEditable: true } }));
  assert.equal(e.run('active.size'), 0);
});

test('octave buttons reset held notes, shift key hit targets, and enforce limits', () => {
  const e = environment();
  e.win.dispatch('keydown', keyEvent('KeyA'));
  e.octaveButtons[1].dispatch('click');
  assert.equal(e.run('baseMidi'), 72);
  assert.equal(e.run('active.size'), 0);
  assert.equal(e.keys[0].dataset.midi, '72');
  e.keyboard.dispatch('pointerdown', pointer(1, 10));
  assert.equal(e.run("active.get('ptr:1').midi"), 72);
  e.run('shiftOctave(1); shiftOctave(1)');
  assert.equal(e.run('baseMidi'), 84);
  e.run('for (let i = 0; i < 8; i++) shiftOctave(-1)');
  assert.equal(e.run('baseMidi'), 24);
  assert.equal(e.keys[0].dataset.midi, '24');
});

console.log(`${count} synth lifecycle checks passed. Audio and DOM were simulated; no audible or physical-device test was performed.`);
