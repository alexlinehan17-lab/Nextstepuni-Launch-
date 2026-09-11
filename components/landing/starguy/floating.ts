import { CANVAS } from '../fx-char/control';

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

/** Keep the whole character, including his sway, in the empty outer margin.
 * Narrow desktop layouts use the existing mark in the nav instead. */
export function floatingHome(contentLeft: number, navBottom: number, viewportHeight: number) {
  if (contentLeft < 96) return null;
  const width = Math.min(88, contentLeft - 40);
  const top = navBottom + 72;
  if (top + width * CANVAS.height / CANVAS.width + 40 > viewportHeight) return null;
  return { left: (contentLeft - width) / 2, top, width };
}

/** A slow buoyant orbit; scroll gives Rive's star-pivoted rig more energy. */
export function floatingMotion(timeMs: number, scrollVelocity: number) {
  const phase = timeMs / 4800 * Math.PI * 2;
  const energy = clamp(Math.abs(scrollVelocity) / 1800, 0, 1);
  return {
    x: Math.sin(phase * 0.75) * 2.5,
    y: Math.sin(phase) * (5 + energy * 3),
    lean: Math.sin(phase + 0.6) * 2 + clamp(scrollVelocity / 550, -3, 3),
    squash: Math.sin(phase + 1) * 0.055,
    speed: 14 + energy * 50,
  };
}
