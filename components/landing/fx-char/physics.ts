/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A small matter-js world with its own frame loop. Every character effect
 * makes one for as long as it runs and disposes it after: fixed 60Hz steps,
 * capped catch-up so a hidden tab does not explode on return, and a render
 * callback per animation frame.
 */

import { Composite, Engine, Sleeping, type Body, type Constraint, type IEngineDefinition } from 'matter-js';

export interface World {
  engine: Engine;
  add: (...items: (Body | Constraint)[]) => void;
  remove: (...items: (Body | Constraint)[]) => void;
  /** Start stepping; `render` runs after each animation frame's steps. */
  run: (render: () => void) => void;
  stop: () => void;
  /** True once every dynamic body in the world is asleep (needs enableSleeping). */
  resting: () => boolean;
  /** True while nothing dynamic is moving to speak of — quicker to say yes than sleeping is. */
  calm: () => boolean;
  dispose: () => void;
}

const STEP = 1000 / 60;

export const createWorld = (opts: IEngineDefinition = {}): World => {
  const engine = Engine.create({ enableSleeping: true, ...opts });
  let raf = 0;
  let last = 0;
  let acc = 0;
  let running = false;
  const stop = () => { running = false; cancelAnimationFrame(raf); raf = 0; };
  return {
    engine,
    add: (...items) => Composite.add(engine.world, items),
    remove: (...items) => items.forEach(i => Composite.remove(engine.world, i)),
    run: render => {
      if (running) return;
      running = true;
      last = performance.now(); acc = 0;
      const tick = (now: number) => {
        if (!running) return;
        raf = requestAnimationFrame(tick);
        acc += Math.min(100, now - last); last = now;
        while (acc >= STEP) { Engine.update(engine, STEP); acc -= STEP; }
        render();
      };
      raf = requestAnimationFrame(tick);
    },
    stop,
    resting: () => Composite.allBodies(engine.world).every(b => b.isStatic || b.isSleeping),
    calm: () => Composite.allBodies(engine.world).every(b => b.isStatic || b.isSleeping || (b.speed < 0.08 && b.angularSpeed < 0.008)),
    dispose: () => { stop(); Composite.clear(engine.world, false, true); Engine.clear(engine); },
  };
};

/** Wake a body that sleeping may have parked, before moving it. */
export const wake = (b: Body): void => Sleeping.set(b, false);

/** Shortest signed distance from angle a to angle b, radians. */
export const angleDelta = (a: number, b: number): number => {
  let d = (b - a) % (Math.PI * 2);
  if (d > Math.PI) d -= Math.PI * 2;
  if (d < -Math.PI) d += Math.PI * 2;
  return d;
};

export const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
/** The page's own ease: fast out, soft landing. */
export const easeOut = (t: number): number => 1 - Math.pow(1 - t, 3);
