/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Throw exam papers at him. Under the Paper Trail chapter — the chapter
 * about the papers themselves, with 200px of clear page beneath it — a
 * floor is the chapter's own closing rule. Six real first pages (the
 * same renders the Subjects stack uses, nothing drawn) wait in a tray at the
 * left; starguy stands at the right end. Drag one and fling it: a paper that
 * reaches him below the catch speed sticks to his front (he leans back and
 * squashes) and he sets it down beside him; a fast one sails past and lands
 * on the floor, where they pile up. "Tidy" clears the floor.
 *
 * Lives on the page as an absolutely positioned overlay measured from the
 * chapter, so the chapter file stays untouched; six papers at most.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Bodies, Body, Events, type IEventCollision, type Engine } from 'matter-js';
import { animate } from 'framer-motion';
import { STACK_PAPERS, type StackPaper } from '../fx-c/papers';
import { CANVAS, starguy } from './control';
import { createWorld, wake, type World } from './physics';

const NAV = 68;
const ZONE_H = 150;
const PAPER = { w: 46, h: 65 } as const;
const HIM = 52;
const RATIO = CANVAS.height / CANVAS.width;
/** Matter velocity is px per 60Hz step; a throw slower than this at his front is a catch. */
const CATCH_SPEED = 13;
const MAX = 6;

export const credit = (p: StackPaper): string => `SEC Leaving Certificate ${p.subject} ${p.year} ${p.level} — © State Examinations Commission`;

interface Zone { left: number; top: number; width: number; floor: number }
interface Paper { id: string; src: string; body: Body; el: HTMLDivElement | null; state: 'flying' | 'held' | 'down'; flop: 0 | 1 | -1 }

const PaperThrow: React.FC = () => {
  const [zone, setZone] = useState<Zone | null>(null);
  const [thrown, setThrown] = useState<string[]>([]);
  const host = useRef<HTMLDivElement>(null);
  const world = useRef<World | null>(null);
  const papers = useRef<Paper[]>([]);
  const dragging = useRef<{ paper: Paper; samples: { x: number; y: number; t: number }[] } | null>(null);
  const claimed = useRef(false);
  const busy = useRef(false);
  const zoneRef = useRef<Zone | null>(null);
  /** How he holds himself: at rest he watches the tray; with a paper on his front he leans back and squashes. */
  const pose = useRef<'rest' | 'catch'>('rest');

  // Measure the chapter and lay the floor under it; re-measure on resize.
  useEffect(() => {
    const measure = () => {
      const art = document.getElementById('chapter-papertrail');
      if (!art) { setZone(null); return; }
      const r = art.getBoundingClientRect();
      // The floor is the chapter's own rule: the ink line between it and the next chapter.
      const next = art.nextElementSibling;
      const rule = next instanceof HTMLHRElement ? next.getBoundingClientRect().top : r.bottom + 112;
      const z = { left: r.left, top: rule + window.scrollY - (ZONE_H - 24), width: r.width, floor: ZONE_H - 24 };
      zoneRef.current = z;
      setZone(z);
    };
    measure();
    const t = window.setTimeout(measure, 1500);
    window.addEventListener('resize', measure);
    return () => { window.clearTimeout(t); window.removeEventListener('resize', measure); };
  }, []);

  const draw = useCallback(() => {
    for (const p of papers.current) {
      // Paper does not stand on its edge: a sheet that has come to rest
      // upright tips onto its long side, the way it is already leaning.
      const tilt = Math.sin(p.body.angle);
      if (p.flop === 0 && p.state === 'down' && !p.body.isStatic && p.body.speed < 0.3 && Math.abs(tilt) < 0.6) p.flop = tilt >= 0 ? 1 : -1;
      if (p.flop !== 0) {
        if (Math.abs(tilt) < 0.85) { wake(p.body); Body.setAngularVelocity(p.body, p.flop * 0.07); } else p.flop = 0;
      }
      if (!p.el) continue;
      p.el.style.transform = `translate(${(p.body.position.x - PAPER.w / 2).toFixed(2)}px, ${(p.body.position.y - PAPER.h / 2).toFixed(2)}px) rotate(${p.body.angle.toFixed(4)}rad)`;
    }
  }, []);

  /** Where he stands, in zone coordinates: the right end of the floor. */
  const standAt = useCallback((z: Zone) => ({ left: z.width - 40 - HIM, top: z.floor - HIM * RATIO, width: HIM }), []);

  const setDown = useCallback((p: Paper, z: Zone) => {
    const w = world.current;
    if (!w) return;
    const stand = standAt(z);
    const downCount = papers.current.filter(q => q.state === 'down').length;
    const to = { x: stand.left - 30 - downCount * 9, y: z.floor - PAPER.h / 2 + 2, a: -0.08 + downCount * 0.03 };
    const from = { x: p.body.position.x, y: p.body.position.y, a: p.body.angle };
    busy.current = true;
    animate(0, 1, {
      duration: 0.42, ease: [0.2, 0.8, 0.2, 1],
      onUpdate: t => { Body.setPosition(p.body, { x: from.x + (to.x - from.x) * t, y: from.y + (to.y - from.y) * t }); Body.setAngle(p.body, from.a + (to.a - from.a) * t); },
    }).then(() => {
      p.state = 'down';
      Body.setStatic(p.body, false);
      wake(p.body);
      Body.setVelocity(p.body, { x: 0, y: 0 });
      Body.setAngularVelocity(p.body, 0);
      busy.current = false;
    });
  }, [standAt]);

  // The world: floor, walls, and the catch zone in front of him.
  useEffect(() => {
    if (!zone) return;
    const w = createWorld({ gravity: { x: 0, y: 1, scale: 0.0012 } });
    const stand = standAt(zone);
    const catchZone = Bodies.rectangle(stand.left + HIM * 0.2, stand.top + HIM * RATIO * 0.55, HIM * 0.7, HIM * RATIO * 0.8, { isStatic: true, isSensor: true, label: 'catch' });
    w.add(
      Bodies.rectangle(zone.width / 2, zone.floor + 30, zone.width + 200, 60, { isStatic: true, friction: 0.6, label: 'floor' }),
      Bodies.rectangle(-30, zone.floor - 300, 60, 800, { isStatic: true }),
      Bodies.rectangle(zone.width + 30, zone.floor - 300, 60, 800, { isStatic: true }),
      catchZone,
    );
    const onCollide = (e: IEventCollision<Engine>) => {
      for (const pair of e.pairs) {
        const floorHit = pair.bodyA.label === 'floor' ? pair.bodyB : pair.bodyB.label === 'floor' ? pair.bodyA : null;
        const landed = floorHit && papers.current.find(q => q.body === floorHit && q.state === 'flying' && dragging.current?.paper !== q);
        if (landed) landed.state = 'down';
        const other = pair.bodyA === catchZone ? pair.bodyB : pair.bodyB === catchZone ? pair.bodyA : null;
        if (!other) continue;
        const p = papers.current.find(q => q.body === other && q.state === 'flying');
        if (!p || busy.current || dragging.current?.paper === p) continue;
        const speed = Body.getSpeed(p.body);
        if (host.current) host.current.dataset.lastSpeed = speed.toFixed(1);
        if (speed > CATCH_SPEED) continue;
        // A catch: it sticks to his front, he leans away from it and squashes, then sets it down.
        p.state = 'held';
        Body.setStatic(p.body, true);
        const chest = { x: stand.left + HIM * 0.3, y: stand.top + HIM * RATIO * 0.5 };
        Body.setPosition(p.body, chest);
        Body.setAngle(p.body, -0.18);
        pose.current = 'catch';
        window.setTimeout(() => { pose.current = 'rest'; setDown(p, zoneRef.current ?? zone); }, 650);
      }
    };
    Events.on(w.engine, 'collisionStart', onCollide);
    Events.on(w.engine, 'collisionActive', onCollide);
    world.current = w;
    w.run(draw);
    return () => { Events.off(w.engine, 'collisionStart', onCollide); Events.off(w.engine, 'collisionActive', onCollide); w.dispose(); world.current = null; papers.current = []; };
  }, [zone, draw, standAt, setDown]);

  // He stands at the floor's end while the floor is on screen.
  useEffect(() => {
    if (!zone) return;
    let raf = 0;
    const tick = () => {
      raf = requestAnimationFrame(tick);
      const el = host.current;
      if (!el) return;
      const r = el.getBoundingClientRect();
      const on = r.top < window.innerHeight - 60 && r.bottom > NAV + 40;
      if (on) {
        const s = standAt(zone);
        const box = { left: r.left + s.left, top: r.top + s.top, width: s.width };
        if (pose.current === 'catch') starguy.claim('papers', { box, priority: 5, look: { x: -0.4, y: 0.6 }, lean: 9, squash: 0.45 });
        else starguy.claim('papers', { box, priority: 5, look: { x: -0.8, y: 0.15 } });
        claimed.current = true;
      } else if (claimed.current) { starguy.release('papers'); claimed.current = false; }
    };
    raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); if (claimed.current) starguy.release('papers'); claimed.current = false; };
  }, [zone, standAt]);

  const onPick = (paper: StackPaper) => (e: React.PointerEvent<HTMLButtonElement>) => {
    const w = world.current;
    const el = host.current;
    if (!w || !el || dragging.current || papers.current.length >= MAX) return;
    e.preventDefault();
    const r = el.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    const body = Bodies.rectangle(x, y, PAPER.w, PAPER.h, { friction: 0.4, frictionAir: 0.018, restitution: 0.1, density: 0.001, chamfer: { radius: 1 } });
    Body.setStatic(body, true);
    const p: Paper = { id: paper.id, src: paper.src, body, el: null, state: 'flying', flop: 0 };
    papers.current = [...papers.current, p];
    w.add(body);
    dragging.current = { paper: p, samples: [{ x, y, t: performance.now() }] };
    setThrown(t => [...t, paper.id]);
  };

  useEffect(() => {
    const onMove = (e: PointerEvent) => {
      const d = dragging.current, el = host.current;
      if (!d || !el) return;
      const r = el.getBoundingClientRect();
      const x = e.clientX - r.left, y = e.clientY - r.top;
      Body.setPosition(d.paper.body, { x, y });
      d.samples.push({ x, y, t: performance.now() });
      if (d.samples.length > 6) d.samples.shift();
    };
    const onUp = () => {
      const d = dragging.current;
      if (!d) return;
      dragging.current = null;
      const s = d.samples;
      const a = s[0], b = s[s.length - 1];
      const dt = Math.max(16, b.t - a.t);
      // px/ms → px per step, damped a little so a flick reads as a throw, not a shot.
      const vx = ((b.x - a.x) / dt) * 16.67 * 0.85, vy = ((b.y - a.y) / dt) * 16.67 * 0.85;
      Body.setStatic(d.paper.body, false);
      wake(d.paper.body);
      Body.setVelocity(d.paper.body, { x: Math.max(-40, Math.min(40, vx)), y: Math.max(-40, Math.min(40, vy)) });
      Body.setAngularVelocity(d.paper.body, (Math.random() - 0.5) * 0.2);
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    return () => { window.removeEventListener('pointermove', onMove); window.removeEventListener('pointerup', onUp); window.removeEventListener('pointercancel', onUp); };
  }, []);

  const tidy = () => {
    const w = world.current;
    if (!w) return;
    for (const p of papers.current) w.remove(p.body);
    papers.current = [];
    setThrown([]);
  };

  if (!zone) return null;
  const left = STACK_PAPERS.filter(p => !thrown.includes(p.id));
  return createPortal(
    <div ref={host} className="fx-char-papers" style={{ left: zone.left, top: zone.top, width: zone.width, height: ZONE_H }} data-fx-char="papers">
      {/* The tray: the papers still to throw, fanned at the left end of the floor. */}
      <div className="fx-char-tray" style={{ left: 0, top: zone.floor - PAPER.h - 6 }}>
        {left.map((p, i) => (
          <button
            key={p.id}
            type="button"
            aria-label={`Throw the ${p.subject} ${p.year} ${p.level} paper`}
            title={credit(p)}
            style={{ width: PAPER.w, height: PAPER.h, rotate: `${(i - left.length / 2) * 1.5}deg` }}
            onPointerDown={onPick(p)}
          >
            <img src={p.src} alt="" draggable={false} />
          </button>
        ))}
      </div>
      <div className="fx-char-caption" style={{ left: 0, top: zone.floor + 12 }}>
        {left.length > 0 ? 'Throw one at him' : 'All thrown'}
        {thrown.length > 0 && <>{' · '}<button type="button" className="fx-char-tidy" onClick={tidy}>Tidy</button></>}
      </div>
      <div className="fx-char-caption" style={{ right: 0, top: zone.floor + 12 }}>First pages of six SEC papers · © State Examinations Commission</div>
      {/* The papers in the world, drawn where their bodies are. */}
      {thrown.map(id => {
        const paper = STACK_PAPERS.find(p => p.id === id);
        if (!paper) return null;
        return (
          <div
            key={id}
            className="fx-char-paper"
            aria-hidden="true"
            title={credit(paper)}
            ref={el => { const p = papers.current.find(q => q.id === id); if (p) p.el = el; }}
            style={{ width: PAPER.w, height: PAPER.h }}
          >
            <img src={paper.src} alt="" draggable={false} />
          </div>
        );
      })}
    </div>,
    document.body,
  );
};

export default PaperThrow;
