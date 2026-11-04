/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * He breaks the frame. Once per visit, when the headline has arrived and the
 * visitor has sat at the top of the page for a couple of seconds without
 * scrolling, the headline topples: every word becomes a body at its own
 * laid-out box and falls onto the line the CTA row stands on, tumbling into
 * a pile. Then starguy walks along that line and puts it back — each word in
 * reading order springs to its exact place as he reaches it — and the real
 * h1 shows again, pixel for pixel where it was.
 *
 * The words that fall are clones: absolutely positioned, aria-hidden spans
 * measured from the live h1 and given its computed type. The h1 itself only
 * has its ink made transparent, so screen readers, the layout and the nav's
 * sentinel never notice. A scroll mid-sequence finishes it quickly rather than
 * aborting it.
 */

import { useEffect, type FC } from 'react';
import { Bodies, Body } from 'matter-js';
import { animate } from 'framer-motion';
import { CANVAS, starguy } from './control';
import { angleDelta, createWorld } from './physics';

const KEY = 'nsu-landing-toppled';
/** The headline's rise (LineRise) ends about here after the traveller goes live. */
const INTRO_MS = 700;
const IDLE_MS = 2500;
/** A word's body: the glyph band inside its inline box (the box carries ascender and descender space). */
const BODY_TOP = 0.22;
const BODY_BOTTOM = 0.8;
const RATIO = CANVAS.height / CANVAS.width;

const FONT_PROPS = [
  'font-family', 'font-size', 'font-weight', 'font-style', 'font-variation-settings', 'font-optical-sizing', 'font-kerning',
  'font-feature-settings', 'letter-spacing', 'line-height', 'color', 'text-rendering', '-webkit-font-smoothing',
] as const;

interface Word { el: HTMLSpanElement; body: Body; cx: number; cy: number; line: number; homed: boolean }

const sleep = (ms: number) => new Promise<void>(r => window.setTimeout(r, ms));

/** Wait until he is standing on his claim, or give up after `max` ms. */
const arrival = (max: number) => new Promise<void>(resolve => {
  const t0 = performance.now();
  const poll = () => {
    const w = starguy.where();
    if ((w && w.arrived) || performance.now() - t0 > max) resolve(); else requestAnimationFrame(poll);
  };
  requestAnimationFrame(poll);
});

let running = false;

export const runTopple = async (): Promise<void> => {
  if (running) return;
  const h1 = document.querySelector<HTMLElement>('h1.landing-hero-title');
  const hero = document.getElementById('top');
  const floorEl = hero?.querySelector<HTMLElement>('[data-hero-floor]') ?? hero?.querySelector<HTMLElement>('[data-hero-cta]');
  const words = h1 ? Array.from(h1.querySelectorAll<HTMLElement>('.landing-hl')) : [];
  if (!h1 || !hero || !floorEl || words.length === 0) return;
  running = true;
  const heroRect = hero.getBoundingClientRect();
  const h1Rect = h1.getBoundingClientRect();
  const floorY = floorEl.getBoundingClientRect().top - heroRect.top - 2;
  const overlay = document.createElement('div');
  overlay.className = 'fx-char-topple';
  overlay.setAttribute('aria-hidden', 'true');
  hero.appendChild(overlay);

  // Clone every word at its measured box, then correct the clone onto the
  // original to the pixel (the inline box and the absolute box can differ by
  // a subpixel of baseline placement).
  const world = createWorld({ gravity: { x: 0, y: 1, scale: 0.0011 } });
  const items: Word[] = [];
  let lineTop = -1, line = -1;
  for (const w of words) {
    const r = w.getBoundingClientRect();
    if (Math.abs(r.top - lineTop) > 4) { line += 1; lineTop = r.top; }
    const el = document.createElement('span');
    el.className = 'fx-char-word';
    el.textContent = w.textContent;
    const cs = getComputedStyle(w);
    for (const p of FONT_PROPS) el.style.setProperty(p, cs.getPropertyValue(p));
    el.style.left = `${r.left - heroRect.left}px`;
    el.style.top = `${r.top - heroRect.top}px`;
    el.style.transformOrigin = `50% ${((BODY_TOP + BODY_BOTTOM) / 2) * 100}%`;
    overlay.appendChild(el);
    const c = el.getBoundingClientRect();
    el.style.left = `${r.left - heroRect.left + (r.left - c.left)}px`;
    el.style.top = `${r.top - heroRect.top + (r.top - c.top)}px`;
    const top = r.top - heroRect.top + r.height * BODY_TOP;
    const height = r.height * (BODY_BOTTOM - BODY_TOP);
    const cx = r.left - heroRect.left + r.width / 2, cy = top + height / 2;
    // Built dynamic and then parked: a body born static has no mass to give back when it is released.
    const body = Bodies.rectangle(cx, cy, r.width, height, { friction: 0.32, frictionStatic: 0.5, restitution: 0.18, density: 0.002, chamfer: { radius: 4 } });
    Body.setStatic(body, true);
    items.push({ el, body, cx, cy, line, homed: false });
  }
  const left = h1Rect.left - heroRect.left, right = h1Rect.right - heroRect.left;
  world.add(
    Bodies.rectangle((left + right) / 2, floorY + 30, right - left + 400, 60, { isStatic: true, friction: 0.7 }),
    Bodies.rectangle(left - 30, floorY - 300, 60, 800, { isStatic: true }),
    Bodies.rectangle(right + 30, floorY - 300, 60, 800, { isStatic: true }),
    ...items.map(i => i.body),
  );
  // Transparent ink rather than opacity: the h1 stays in the accessibility
  // tree either way, but an opacity change makes Chrome re-rasterise the
  // type, and the restored headline would no longer match to the pixel.
  h1.style.color = 'transparent';
  const marks = Array.from(h1.querySelectorAll<SVGElement>('svg'));
  for (const m of marks) m.style.visibility = 'hidden';
  const draw = () => {
    for (const { el, body, cx, cy, homed } of items) {
      if (homed) continue;
      el.style.transform = `translate(${(body.position.x - cx).toFixed(2)}px, ${(body.position.y - cy).toFixed(2)}px) rotate(${body.angle.toFixed(4)}rad)`;
    }
  };
  world.run(draw);

  // The topple: the top line goes first and each line follows a beat later,
  // every word shoved sideways and spun so nothing falls flat.
  const lines = Math.max(...items.map(i => i.line));
  for (let l = 0; l <= lines; l++) {
    const row = items.filter(i => i.line === l);
    for (const [k, it] of row.entries()) {
      Body.setStatic(it.body, false);
      const dir = (k + l) % 2 === 0 ? 1 : -1;
      Body.setVelocity(it.body, { x: dir * (2 + Math.random() * 2), y: -1 });
      Body.setAngularVelocity(it.body, dir * (0.09 + Math.random() * 0.08));
    }
    await sleep(110);
  }
  // Let the pile settle: nothing moving for a third of a second, or four seconds, whichever first.
  const t0 = performance.now();
  let calmSince = 0;
  while (performance.now() - t0 < 4000) {
    await sleep(60);
    if (!world.calm()) calmSince = 0;
    else if (!calmSince) calmSince = performance.now();
    else if (performance.now() - calmSince > 320) break;
  }

  // The restack. He stands on the floor line beside each word in reading
  // order; as he arrives the word springs home and he squashes with the
  // push. A scroll away turns the rest into one quick spring.
  const scrolled = () => window.scrollY > 60 || hero.getBoundingClientRect().bottom < 200;
  const width = starguy.box()?.width ?? 52;
  const height = width * RATIO;
  const home = (it: Word, ms: number) => {
    it.homed = true;
    world.remove(it.body);
    const b = it.body;
    const from = { x: b.position.x - it.cx, y: b.position.y - it.cy, a: b.angle };
    const da = angleDelta(from.a, 0);
    return animate(0, 1, {
      duration: ms / 1000,
      ease: [0.2, 0.8, 0.2, 1],
      onUpdate: t => { it.el.style.transform = `translate(${(from.x * (1 - t)).toFixed(2)}px, ${(from.y * (1 - t)).toFixed(2)}px) rotate(${(from.a + da * t).toFixed(4)}rad)`; },
    }).then(() => { it.el.style.transform = ''; });
  };
  let fast = false;
  const pending = [...items];
  while (pending.length) {
    if (!fast && scrolled()) fast = true;
    if (fast) {
      await Promise.all(pending.splice(0).map(it => home(it, 380)));
      break;
    }
    const it = pending.shift() as Word;
    const bx = it.body.position.x + heroRect.left;
    const standLeft = Math.min(Math.max(bx - width * 0.5, h1Rect.left), h1Rect.right - width);
    starguy.claim('topple', { box: { left: standLeft, top: hero.getBoundingClientRect().top + floorY - height, width }, priority: 20, look: { x: bx > standLeft + width * 0.5 ? 0.8 : -0.8, y: 0.5 } });
    await arrival(1100);
    starguy.pulse('squash');
    await home(it, 460);
    await sleep(90);
  }
  world.dispose();
  overlay.remove();
  h1.style.color = '';
  for (const m of marks) m.style.visibility = '';
  starguy.release('topple');
  running = false;
  try { sessionStorage.setItem(KEY, '1'); } catch { /* private mode: it will simply run again next visit */ }
  window.setTimeout(() => starguy.pulse('nod'), 250);
};

/** Arms the topple: after the intro, ~2.5s at the top of the page with no scroll. Once per session. */
const Topple: FC = () => {
  useEffect(() => {
    let done = false;
    try { done = sessionStorage.getItem(KEY) === '1'; } catch { done = false; }
    let timer = 0;
    const fire = () => {
      if (done) return;
      const w = starguy.where();
      if (window.scrollY > 8 || !w || w.id !== 'hero' || !w.arrived) { arm(); return; }
      done = true;
      void runTopple();
    };
    const arm = () => {
      window.clearTimeout(timer);
      if (done) return;
      timer = window.setTimeout(fire, IDLE_MS);
    };
    const onScroll = () => arm();
    const onDev = (e: Event) => { if ((e as CustomEvent<{ kind: string }>).detail?.kind === 'topple') { done = true; window.clearTimeout(timer); void runTopple(); } };
    const start = window.setTimeout(arm, INTRO_MS);
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('starguy-dev', onDev);
    return () => { window.clearTimeout(start); window.clearTimeout(timer); window.removeEventListener('scroll', onScroll); window.removeEventListener('starguy-dev', onDev); };
  }, []);
  return null;
};

export default Topple;
