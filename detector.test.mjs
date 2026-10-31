// Tests for the UFO detector page, run with: node --test
//
// script.js is a page script, not a library, so these tests load it
// the way the browser does: fresh page objects first (a document
// with the two elements index.html carries, a window that may or
// may not have the CDN libraries on it, and timers I capture
// instead of letting run), then the module itself. Each load
// imports a copy of script.js under a fresh temp file name, because
// Node caches a module by its path: a second import of the same
// path hands back the first page's already running loop instead of
// starting a new one, which is exactly how the first version of
// this suite failed.
//
// script.js looks its globals up when each callback runs, not when
// it loads, so every step in a test re-installs that page's stubs
// first (page.activate). The steps themselves are synchronous, so
// two pages loaded in the same process cannot cross wires mid-step.
// Real timers never run a roll here; I invoke the captured
// callbacks by hand and pin Math.random per test.
//
// The CSS test at the end pins the blip centering fix: the dot is
// centered with negative margins, not a translate transform, so the
// transform GSAP writes during the pulse cannot replace the
// centering while a detection shows.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { copyFileSync, mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
let caseId = 0;

async function loadPage({ gsap = true, howler = false, playThrows = false } = {}) {
    const message = { textContent: 'Scanning for UFOs...' };
    const blip = { style: {} };
    const intervals = [];
    const timeouts = [];
    const gsapTweens = [];
    const howls = [];
    const win = {};
    if (gsap) {
        win.gsap = {
            to(el, vars) {
                gsapTweens.push({ el, vars });
                if (vars.onComplete) vars.onComplete();
            }
        };
    }
    if (howler) {
        win.Howl = class {
            constructor(opts) {
                this.opts = opts;
                this.plays = 0;
                howls.push(this);
            }
            play() {
                this.plays += 1;
                if (playThrows) throw new Error('audio blocked');
            }
        };
    }
    const doc = {
        getElementById: (id) => (id === 'message' ? message : blip)
    };
    const fakeSetInterval = (fn, ms) => { intervals.push({ fn, ms }); return 1; };
    const fakeSetTimeout = (fn, ms) => { timeouts.push({ fn, ms }); return 1; };
    const page = { message, blip, intervals, timeouts, gsapTweens, howls };
    page.activate = () => {
        globalThis.window = win;
        globalThis.document = doc;
        globalThis.setInterval = fakeSetInterval;
        globalThis.setTimeout = fakeSetTimeout;
    };
    page.activate();
    const realLog = console.log;
    console.log = () => {};
    try {
        caseId += 1;
        const dir = mkdtempSync(join(tmpdir(), 'ufo-detector-test-'));
        const copyPath = join(dir, `script-${caseId}.mjs`);
        copyFileSync(join(HERE, 'script.js'), copyPath);
        await import(pathToFileURL(copyPath).href);
    } finally {
        console.log = realLog;
    }
    return page;
}

async function withRandom(value, body) {
    const realRandom = Math.random;
    Math.random = () => value;
    try {
        await body();
    } finally {
        Math.random = realRandom;
    }
}

function tickAndRoll(page) {
    page.activate();
    page.intervals[0].fn();
    const roll = page.timeouts.shift();
    assert.equal(roll.ms, 500);
    roll.fn();
}

function tick(page) {
    page.activate();
    page.intervals[0].fn();
}

function runTimeout(page, ms) {
    page.activate();
    const entry = page.timeouts.find((t) => t.ms === ms);
    assert.ok(entry, `expected a ${ms} ms timeout to be pending`);
    entry.fn();
}

test('scan loop checks every 3.5 seconds and rolls 0.5 seconds later', async () => {
    const page = await loadPage();
    assert.equal(page.intervals.length, 1);
    assert.equal(page.intervals[0].ms, 3500);
    tick(page);
    assert.equal(page.timeouts.length, 1);
    assert.equal(page.timeouts[0].ms, 500);
});

test('a missed roll leaves the page scanning', () => withRandom(0.9, async () => {
    const page = await loadPage();
    tickAndRoll(page);
    assert.equal(page.message.textContent, 'Scanning for UFOs...');
    assert.equal(page.gsapTweens.length, 0);
    tick(page);
    assert.equal(page.timeouts.length, 1);
}));

test('a hit shows the detection, pulses the blip with GSAP, and resets after 3 seconds', () => withRandom(0.1, async () => {
    const page = await loadPage();
    tickAndRoll(page);
    assert.equal(page.message.textContent, 'UFO DETECTED!');
    assert.equal(page.gsapTweens.length, 2);
    const pulse = page.gsapTweens[0].vars;
    assert.equal(pulse.opacity, 1);
    assert.equal(pulse.scale, 2.5);
    assert.equal(pulse.duration, 0.3);
    assert.equal(pulse.repeat, 3);
    assert.equal(pulse.yoyo, true);
    const fade = page.gsapTweens[1].vars;
    assert.equal(fade.opacity, 0);
    assert.equal(fade.duration, 0.5);
    runTimeout(page, 3000);
    assert.equal(page.message.textContent, 'Scanning for UFOs...');
}));

test('without GSAP the blip is shown and hidden directly', () => withRandom(0.1, async () => {
    const page = await loadPage({ gsap: false });
    tickAndRoll(page);
    assert.equal(page.message.textContent, 'UFO DETECTED!');
    assert.equal(page.blip.style.opacity, '1');
    runTimeout(page, 1200);
    assert.equal(page.blip.style.opacity, '0');
}));

test('ticks during a detection are dropped, not queued', () => withRandom(0.1, async () => {
    const page = await loadPage();
    tickAndRoll(page);
    assert.equal(page.message.textContent, 'UFO DETECTED!');
    const pending = page.timeouts.length;
    tick(page);
    assert.equal(page.timeouts.length, pending);
    runTimeout(page, 3000);
    tick(page);
    assert.equal(page.timeouts.length, pending + 1);
}));

test('with Howler, both sounds are built and the ambient loop plays at load', () => withRandom(0.1, async () => {
    const page = await loadPage({ howler: true });
    assert.equal(page.howls.length, 2);
    assert.equal(page.howls[1].opts.loop, true);
    assert.equal(page.howls[1].plays, 1);
    tickAndRoll(page);
    assert.equal(page.howls[0].plays, 1);
}));

test('without Howler the page still detects', () => withRandom(0.1, async () => {
    const page = await loadPage({ howler: false });
    tickAndRoll(page);
    assert.equal(page.message.textContent, 'UFO DETECTED!');
}));

test('a sound that throws on play does not break the detection', () => withRandom(0.1, async () => {
    const page = await loadPage({ howler: true, playThrows: true });
    tickAndRoll(page);
    assert.equal(page.message.textContent, 'UFO DETECTED!');
    assert.ok(page.timeouts.some((t) => t.ms === 3000));
}));

test('the blip is centered with margins, not a translate GSAP could replace', () => {
    const css = readFileSync(join(HERE, 'style.css'), 'utf8');
    const block = css.match(/#blip\s*{([^}]*)}/)[1];
    assert.match(block, /margin-left:\s*-5px/);
    assert.match(block, /margin-top:\s*-5px/);
    assert.ok(!css.includes('translate(-50%, -50%)'));
});

test('index.html carries the ids, module, and CDN scripts script.js expects', () => {
    const html = readFileSync(join(HERE, 'index.html'), 'utf8');
    assert.ok(html.includes('id="message"'));
    assert.ok(html.includes('id="blip"'));
    assert.ok(html.includes('type="module" src="script.js"'));
    assert.ok(html.includes('gsap/3.12.5/gsap.min.js'));
    assert.ok(html.includes('howler/2.2.4/howler.min.js'));
});
