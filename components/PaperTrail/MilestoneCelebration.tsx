/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — milestone celebration (feature E5). The one place we spend a real
 * animated moment: a brief, on-palette confetti burst behind a card announcing a
 * genuine learning milestone, with a shareable card to download. Restrained by
 * design (short, tasteful, reduced-motion aware) so it reads as earned, not
 * gamey.
 */

import React, { useEffect, useRef } from 'react';
import { useReducedMotion } from '../Motion';
import { downloadMilestoneCard, type Milestone } from './milestones';
import { Sheet } from '../ui/Sheet';
import { Button } from '../ui/Button';
import { FramePortal } from '../ui/Frame';

/** The burst in the system's colours: ink, and green for something done (no orange on a
 *  passing effect). Read from the tokens so it follows the theme. */
const confettiColours = () => {
  const css = getComputedStyle(document.documentElement);
  return ['--ink-primary', '--success-hex', '--ink-secondary']
    .map(name => css.getPropertyValue(name).trim())
    .filter(Boolean);
};

interface Props {
  milestone: Milestone;
  dateIso: string;
  onClose: () => void;
}

const MilestoneCelebration: React.FC<Props> = ({ milestone, dateIso, onClose }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const reduceMotion = useReducedMotion();

  useEffect(() => {
    if (reduceMotion) return;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;
    const CONFETTI = confettiColours();
    if (!CONFETTI.length) return;
    const W = (canvas.width = canvas.offsetWidth);
    const H = (canvas.height = canvas.offsetHeight);
    const parts = Array.from({ length: 90 }, () => ({
      x: Math.random() * W,
      y: -Math.random() * H * 0.4,
      vx: (Math.random() - 0.5) * 2.4,
      vy: 2 + Math.random() * 3.2,
      rot: Math.random() * Math.PI,
      vr: (Math.random() - 0.5) * 0.3,
      size: 5 + Math.random() * 5,
      color: CONFETTI[(Math.random() * CONFETTI.length) | 0],
    }));
    let frame = 0;
    let raf = 0;
    const tick = () => {
      frame += 1;
      ctx.clearRect(0, 0, W, H);
      ctx.globalAlpha = frame > 90 ? Math.max(0, 1 - (frame - 90) / 30) : 1;
      for (const p of parts) {
        p.x += p.vx;
        p.y += p.vy;
        p.rot += p.vr;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.55);
        ctx.restore();
      }
      if (frame < 120) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [reduceMotion, milestone.id]);

  // The shared Sheet (from the bottom on a phone): its own words and its own way out, Share card
  // and Nice. The burst falls once over the top, then is gone; it never takes a tap.
  return (
    <>
      <FramePortal><canvas ref={canvasRef} className="frame-takeover pt-milestone-burst" aria-hidden /></FramePortal>
      <Sheet open bare title={`Milestone: ${milestone.title}`} onClose={onClose} className="pt-milestone"
        footer={
          <div className="ui-pair">
            <Button size="lg" onClick={() => downloadMilestoneCard(milestone, dateIso)}>Share card</Button>
            <Button kind="main" size="lg" onClick={onClose}>Nice</Button>
          </div>
        }>
        <p className="t-label pt-milestone-label">Milestone reached</p>
        <h2 className="t-title pt-milestone-title">{milestone.title}</h2>
        <p className="t-sub">{milestone.blurb}</p>
      </Sheet>
    </>
  );
};

export default MilestoneCelebration;
