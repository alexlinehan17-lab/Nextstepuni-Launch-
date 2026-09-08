/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How the page talks to starguy. Two doors:
 *
 *  1. The public bus, for any section: a window CustomEvent named 'starguy'
 *     whose detail is a StarguyEvent (watch / unwatch / nod / tilt / cheer).
 *     Fire and forget; nothing happens when he is not live.
 *
 *  2. The control, for the character effects in this folder: a temporary
 *     "claim" on where he stands (a place that beats every slot while it is
 *     held), pulses on his channels, and the swap that hides the rig so the
 *     two PNG layers can stand in for it during physics. Traveller.tsx
 *     installs the implementation while the traveller is live; every call
 *     before or after that is a no-op, which is exactly the contract.
 */

export type StarguyEvent =
  | { kind: 'watch'; el: HTMLElement }
  | { kind: 'unwatch' }
  | { kind: 'nod' }
  | { kind: 'tilt' }
  | { kind: 'cheer' };

export const say = (detail: StarguyEvent): void => {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(new CustomEvent<StarguyEvent>('starguy', { detail }));
};

export interface Box { left: number; top: number; width: number }

/** A temporary place to stand. Viewport coordinates, refreshed by the claimant as often as it likes. */
export interface Claim {
  box: Box;
  /** Higher wins when two claims are held at once. */
  priority: number;
  /** Where to look instead of the pointer; null keeps the pointer look. */
  look?: { x: number; y: number } | null;
  /** Extra squash (+) or stretch (−) held while the claim stands. */
  squash?: number;
  /** Extra lean, degrees, held while the claim stands. */
  lean?: number;
  /** Whether taking this claim is a move worth a hop; false for a stand-in that must not move him at all. */
  hop?: boolean;
}

export type Pulse = 'nod' | 'tilt' | 'cheer' | 'squash';

export interface StarguyControl {
  claim: (id: string, claim: Claim) => void;
  release: (id: string) => void;
  pulse: (kind: Pulse) => void;
  /** Hide the rig (the ragdoll draws him instead) and show it again. */
  hide: () => void;
  show: () => void;
  /** The traveller's box right now, viewport coordinates. */
  box: () => (Box & { height: number }) | null;
  /** The slot or claim he is on, and whether the springs have settled onto it. */
  where: () => { id: string; arrived: boolean } | null;
  /** The look the rig currently shows, −1…1, so a stand-in can start from the same pose. */
  look: () => { x: number; y: number };
}

let impl: StarguyControl | null = null;
let grab: ((e: PointerEvent) => void) | null = null;

export const installControl = (c: StarguyControl | null): void => { impl = c; };
/** Who answers when the star at his foot is grabbed in the hero. */
export const onGrab = (fn: ((e: PointerEvent) => void) | null): void => { grab = fn; };
export const fireGrab = (e: PointerEvent): void => { grab?.(e); };

export const starguy: StarguyControl = {
  claim: (id, c) => impl?.claim(id, c),
  release: id => impl?.release(id),
  pulse: k => impl?.pulse(k),
  hide: () => impl?.hide(),
  show: () => impl?.show(),
  box: () => impl?.box() ?? null,
  where: () => impl?.where() ?? null,
  look: () => impl?.look() ?? { x: 0, y: 0 },
};

export const isLive = (): boolean => impl !== null;

/** The drawing's geometry, in its 1030×1193 canvas, shared by the ragdoll and the grab handle. */
export const CANVAS = { width: 1030, height: 1193 } as const;
export const STAR = { x: 638.6, y: 1025.98 } as const;
export const HEAD_PIVOT = { x: 360, y: 355 } as const;
/** Alpha bounds of the head layer (public/assets/landing/starguy-head.png). */
export const HEAD_BOUNDS = { left: 271, top: 142, right: 496, bottom: 378 } as const;
