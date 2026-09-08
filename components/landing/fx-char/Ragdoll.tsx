/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * His star is a physics object. In the hero the star at his foot can be
 * grabbed; yank it and it pulls him over. For as long as that lasts the rig
 * hides and the two layers the drawing was cut into — body and head, each a
 * full 1030×1193 canvas — stand in for it, following two matter bodies: a
 * trapezoid for the body, a disc for the head, pinned at the neck, with the
 * star held to the foot by a stiff constraint and the pointer pulling the
 * star. The hero's box is walled so he never leaves it.
 *
 * On release he lies still for a beat, then gets up: both layers tween back
 * to upright over the same box, the rig returns in exactly that place, and
 * he gives an amused nod. The swap is exact because the layers are the
 * drawing, and while he is a ragdoll the traveller holds his look at rest.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Bodies, Body, Constraint, Vector, Vertices } from 'matter-js';
import { animate } from 'framer-motion';
import { CANVAS, HEAD_PIVOT, STAR, onGrab, starguy } from './control';
import { angleDelta, createWorld, type World } from './physics';

const NAV = 68;
/** The body's outline in canvas px, shoulders to the star's base. Convex, so matter keeps it as one part. */
const BODY_VERTS = [{ x: 250, y: 330 }, { x: 480, y: 330 }, { x: 760, y: 1040 }, { x: 400, y: 1040 }];
/** The head as a disc: the layer's alpha bounds are 271–496 × 142–378. */
const HEAD = { x: 383, y: 260, r: 113 };
const STAR_R = 42;
/** The rig's look, in the same units StarguyFigure uses: degrees of head turn and px of nod at full look. */
const LOOK_TURN = 7;
const LOOK_NOD = 5;
/** Lie still this long after release before getting up. */
const BEAT_MS = 550;
const RISE_MS = 720;

interface Pose { x: number; y: number; a: number }
interface Piece { body: Body; origin: Vector; el: HTMLImageElement | null }

const Ragdoll: React.FC = () => {
  const [box, setBox] = useState<{ left: number; top: number; width: number; height: number } | null>(null);
  const bodyImg = useRef<HTMLImageElement>(null);
  const headImg = useRef<HTMLImageElement>(null);
  const world = useRef<World | null>(null);
  const pieces = useRef<{ body: Piece; head: Piece } | null>(null);
  const drag = useRef<Constraint | null>(null);
  const pointer = useRef<Vector>({ x: 0, y: 0 });
  const phase = useRef<'idle' | 'down' | 'lying' | 'rising'>('idle');

  const draw = useCallback(() => {
    const p = pieces.current;
    if (!p) return;
    for (const piece of [p.body, p.head]) {
      if (!piece.el) continue;
      const dx = piece.body.position.x - piece.origin.x, dy = piece.body.position.y - piece.origin.y;
      piece.el.style.transform = `translate(${dx.toFixed(2)}px, ${dy.toFixed(2)}px) rotate(${piece.body.angle.toFixed(4)}rad)`;
    }
  }, []);

  const finish = useCallback(() => {
    world.current?.dispose();
    world.current = null;
    pieces.current = null;
    drag.current = null;
    phase.current = 'idle';
    starguy.show();
    starguy.release('ragdoll');
    setBox(null);
    window.setTimeout(() => starguy.pulse('nod'), 180);
  }, []);

  const getUp = useCallback(() => {
    const p = pieces.current;
    const w = world.current;
    if (!p || !w) return;
    phase.current = 'rising';
    w.stop();
    const from: Record<'body' | 'head', Pose> = {
      body: { x: p.body.body.position.x - p.body.origin.x, y: p.body.body.position.y - p.body.origin.y, a: p.body.body.angle },
      head: { x: p.head.body.position.x - p.head.origin.x, y: p.head.body.position.y - p.head.origin.y, a: p.head.body.angle },
    };
    const da = { body: angleDelta(from.body.a, 0), head: angleDelta(from.head.a, 0) };
    animate(0, 1, {
      duration: RISE_MS / 1000,
      ease: [0.3, 0.9, 0.2, 1],
      onUpdate: t => {
        for (const k of ['body', 'head'] as const) {
          const el = p[k].el;
          if (!el) continue;
          el.style.transform = `translate(${(from[k].x * (1 - t)).toFixed(2)}px, ${(from[k].y * (1 - t)).toFixed(2)}px) rotate(${(from[k].a + da[k] * t).toFixed(4)}rad)`;
        }
      },
    }).then(() => { if (phase.current === 'rising') finish(); });
  }, [finish]);

  const start = useCallback((e: PointerEvent) => {
    const b = starguy.box();
    const hero = document.getElementById('top');
    if (!b || !hero || phase.current !== 'idle') return;
    const s = b.width / CANVAS.width;
    const toScreen = (v: { x: number; y: number }) => ({ x: b.left + v.x * s, y: b.top + v.y * s });
    const w = createWorld({ gravity: { x: 0, y: 1, scale: 0.0012 } });
    const verts = BODY_VERTS.map(toScreen);
    const centroid = Vertices.centre(verts);
    const body = Bodies.fromVertices(centroid.x, centroid.y, [verts], { friction: 0.6, frictionAir: 0.02, restitution: 0.05, density: 0.004 });
    // fromVertices recentres on the true centroid; keep our origin as where that landed.
    const bodyOrigin = { x: body.position.x, y: body.position.y };
    const headC = toScreen(HEAD);
    const head = Bodies.circle(headC.x, headC.y, HEAD.r * s, { friction: 0.4, frictionAir: 0.03, restitution: 0.1, density: 0.002 });
    const neck = toScreen(HEAD_PIVOT);
    // Start the head where the rig has it this frame (turned toward the
    // pointer, nodded a little), pivoting at the neck the way the rig does.
    const look = starguy.look();
    const turn = (look.x * LOOK_TURN * Math.PI) / 180;
    const arm = Vector.sub(headC, neck);
    Body.setPosition(head, { x: neck.x + arm.x * Math.cos(turn) - arm.y * Math.sin(turn), y: neck.y + arm.x * Math.sin(turn) + arm.y * Math.cos(turn) + look.y * LOOK_NOD * s });
    Body.setAngle(head, turn);
    const starC = toScreen(STAR);
    // The star is the handle the pointer pulls; it collides with nothing, so it never props him up.
    const star = Bodies.circle(starC.x, starC.y, STAR_R * s, { frictionAir: 0.01, density: 0.003, collisionFilter: { mask: 0 } });
    const pin = Constraint.create({ bodyA: body, pointA: Vector.sub(neck, body.position), bodyB: head, pointB: Vector.sub(neck, head.position), length: 0, stiffness: 1 });
    const crownA = toScreen({ x: HEAD.x, y: HEAD.y - HEAD.r });
    // A soft "muscle" from the crown to the shoulders keeps the head from spinning freely while still letting it loll.
    const muscle = Constraint.create({ bodyA: body, pointA: Vector.sub(crownA, body.position), bodyB: head, pointB: Vector.sub(crownA, head.position), length: 0, stiffness: 0.03, damping: 0.08 });
    const foot = Constraint.create({ bodyA: body, pointA: Vector.sub(starC, body.position), bodyB: star, length: 0, stiffness: 0.9, damping: 0.05 });
    const heroRect = hero.getBoundingClientRect();
    // The floor is where the body's base already rests, so nothing drops at the swap.
    const floorY = toScreen({ x: 0, y: BODY_VERTS[2].y }).y;
    const left = heroRect.left, right = heroRect.right;
    w.add(
      body, head, star, pin, muscle, foot,
      Bodies.rectangle((left + right) / 2, floorY + 40, right - left + 200, 80, { isStatic: true, friction: 0.8 }),
      Bodies.rectangle(left - 40, floorY - 400, 80, 1200, { isStatic: true }),
      Bodies.rectangle(right + 40, floorY - 400, 80, 1200, { isStatic: true }),
      Bodies.rectangle((left + right) / 2, NAV - 40, right - left + 200, 80, { isStatic: true }),
    );
    pointer.current = { x: e.clientX, y: e.clientY };
    const pull = Constraint.create({ pointA: pointer.current, bodyB: star, pointB: { x: 0, y: 0 }, length: 0, stiffness: 0.25, damping: 0.05 });
    w.add(pull);
    drag.current = pull;
    world.current = w;
    pieces.current = {
      body: { body, origin: bodyOrigin, el: null },
      head: { body: head, origin: headC, el: null },
    };
    phase.current = 'down';
    starguy.claim('ragdoll', { box: { left: b.left, top: b.top, width: b.width }, priority: 30, look: { x: 0, y: 0 }, hop: false });
    starguy.hide();
    setBox({ left: b.left, top: b.top, width: b.width, height: b.height });
    w.run(() => {
      if (drag.current) drag.current.pointA = { x: pointer.current.x, y: pointer.current.y };
      draw();
    });
  }, [draw]);

  // The layers mount a frame after the world; wire them up as soon as they exist.
  useEffect(() => {
    const p = pieces.current;
    if (!box || !p) return;
    p.body.el = bodyImg.current;
    p.head.el = headImg.current;
    draw();
  }, [box, draw]);

  useEffect(() => {
    onGrab(start);
    const onMove = (e: PointerEvent) => { pointer.current = { x: e.clientX, y: e.clientY }; };
    const onUp = () => {
      if (phase.current !== 'down') return;
      const w = world.current;
      if (w && drag.current) { w.remove(drag.current); drag.current = null; }
      phase.current = 'lying';
      // Let him land, then lie still for a beat, then get up.
      const t0 = performance.now();
      const wait = () => {
        if (phase.current !== 'lying') return;
        if ((w && w.resting()) || performance.now() - t0 > 1400) window.setTimeout(() => { if (phase.current === 'lying') getUp(); }, BEAT_MS);
        else window.setTimeout(wait, 80);
      };
      wait();
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    return () => {
      onGrab(null);
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
      world.current?.dispose();
    };
  }, [start, getUp]);

  if (!box) return null;
  const s = box.width / CANVAS.width;
  const layer = (src: string, ref: React.RefObject<HTMLImageElement | null>, origin: { x: number; y: number }) => (
    <img
      ref={ref}
      src={src}
      alt=""
      draggable={false}
      style={{ left: box.left, top: box.top, width: box.width, height: box.height, transformOrigin: `${(origin.x - box.left) / s / CANVAS.width * 100}% ${(origin.y - box.top) / s / CANVAS.height * 100}%` }}
    />
  );
  const p = pieces.current;
  return createPortal(
    <div className="fx-char-ragdoll" aria-hidden="true">
      {p && layer('/assets/landing/starguy-body.png', bodyImg, p.body.origin)}
      {p && layer('/assets/landing/starguy-head.png', headImg, p.head.origin)}
    </div>,
    document.body,
  );
};

export default Ragdoll;
