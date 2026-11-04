/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Two facts every effect asks before it moves: is this a static render
 * (?static=1 sets html.landing-static for screenshot tooling), and can the
 * browser run CSS scroll-driven animations at all.
 */

export const isStatic = (): boolean =>
  typeof document !== 'undefined' && document.documentElement.classList.contains('landing-static');

export const supportsScrollTimeline = (): boolean =>
  typeof CSS !== 'undefined' && typeof CSS.supports === 'function' && CSS.supports('animation-timeline: view()');
