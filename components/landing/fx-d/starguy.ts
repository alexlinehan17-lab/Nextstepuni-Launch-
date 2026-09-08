/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The starguy reaction contract, from the section's side: fire and forget.
 * The traveller (starguy/Traveller.tsx) listens when he is live and ignores
 * everything otherwise — on phones, under reduced motion, in static mode.
 * "Answer like an examiner" is the only section allowed to make him react
 * to typing.
 */

export type StarguyDetail =
  | { kind: 'watch'; el: HTMLElement }
  | { kind: 'unwatch' }
  | { kind: 'nod' }
  | { kind: 'tilt' }
  | { kind: 'cheer' };

export const starguy = (detail: StarguyDetail): void => {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(new CustomEvent<StarguyDetail>('starguy', { detail }));
};

/**
 * The marking reaction: one nod per earned point, staggered so each reads as
 * its own; a tilt when nothing earned; a hop after the nods at full marks.
 * Returns a cancel for when the visitor marks again before it finishes.
 */
export const reactToMarks = (matched: number, total: number, stagger = 320): (() => void) => {
  const timers: number[] = [];
  if (matched === 0) {
    starguy({ kind: 'tilt' });
    return () => undefined;
  }
  for (let i = 0; i < matched; i++) timers.push(window.setTimeout(() => starguy({ kind: 'nod' }), i * stagger));
  if (matched === total) timers.push(window.setTimeout(() => starguy({ kind: 'cheer' }), matched * stagger + 120));
  return () => timers.forEach(t => window.clearTimeout(t));
};
