/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — focus-session artifact (feature E7). A calm, procedural plant
 * that grows with a focus session's progress. Deliberately restrained and
 * organic (no cartoon mascot): a curved stem, leaves that unfurl as time passes,
 * and a single accent bloom at completion. Deterministic per seed so a saved
 * session always redraws the same shape in the grove.
 */

const prng = (seed: number): (() => number) => {
  let a = seed >>> 0 || 1;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

const drawLeaf = (ctx: CanvasRenderingContext2D, x: number, y: number, angle: number, len: number) => {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle - Math.PI / 2);
  ctx.fillStyle = '#4a9d6f';
  ctx.beginPath();
  ctx.ellipse(0, -len / 2, len * 0.28, len * 0.5, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
};

/** Draw the plant at `progress` (0–1) for a given seed into a w×h context. */
export function drawPlant(ctx: CanvasRenderingContext2D, w: number, h: number, progress: number, seed: number): void {
  const rnd = prng(seed);
  ctx.clearRect(0, 0, w, h);
  const p = Math.max(0, Math.min(1, progress));
  const baseX = w / 2;
  const baseY = h * 0.92;
  const stemH = h * 0.72 * p;
  const topX = baseX + Math.sin(seed) * w * 0.05;
  const topY = baseY - stemH;

  // Stem (gently curved).
  ctx.strokeStyle = '#3A8D5F';
  ctx.lineWidth = Math.max(2, w * 0.014);
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(baseX, baseY);
  ctx.quadraticCurveTo(baseX + (topX - baseX) * 0.3, baseY - stemH * 0.55, topX, topY);
  ctx.stroke();

  // Leaves unfurl along the stem as progress passes each node.
  const nLeaves = 4;
  for (let i = 0; i < nLeaves; i++) {
    const t = (i + 1) / (nLeaves + 1);
    if (p < t * 0.9) continue;
    const ly = baseY - stemH * t;
    const lx = baseX + (topX - baseX) * t;
    const side = i % 2 === 0 ? 1 : -1;
    const angle = side * (0.5 + rnd() * 0.3);
    const grow = Math.min(1, (p - t * 0.9) / 0.12 + 0.4);
    drawLeaf(ctx, lx, ly, angle, w * 0.17 * (0.7 + rnd() * 0.4) * grow);
  }

  // Bloom on completion.
  if (p >= 0.98) {
    ctx.fillStyle = '#F26B1F';
    ctx.beginPath();
    ctx.arc(topX, topY, w * 0.055, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#FDEEDF';
    ctx.beginPath();
    ctx.arc(topX, topY, w * 0.024, 0, Math.PI * 2);
    ctx.fill();
  }
}
