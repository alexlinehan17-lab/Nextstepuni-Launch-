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
import { Share2, Check } from 'lucide-react';
import { MotionDiv, useReducedMotion } from '../Motion';
import { downloadMilestoneCard, type Milestone } from './milestones';

const CONFETTI = ['#F26B1F', '#3A8D5F', '#33658A', '#B54D14', '#8C3A0E'];

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

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center px-6" role="dialog" aria-modal="true" aria-label={`Milestone: ${milestone.title}`}>
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <canvas ref={canvasRef} className="pointer-events-none absolute inset-0 w-full h-full" aria-hidden />
      <MotionDiv
        initial={reduceMotion ? { opacity: 0 } : { opacity: 0, scale: 0.85, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.28, ease: 'easeOut' }}
        className="relative w-full max-w-sm rounded-2xl border-2 border-[#1a1a1a] bg-white dark:bg-zinc-900 dark:border-zinc-700 shadow-[6px_6px_0_0_#1a1a1a] dark:shadow-[6px_6px_0_0_#3f3f46] px-7 py-8 text-center"
      >
        <div className="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center text-[30px]" style={{ backgroundColor: '#FDEEDF' }}>
          {milestone.kind === 'streak' ? '🔥' : '🎯'}
        </div>
        <p className="text-[10.5px] font-bold uppercase tracking-[0.14em] mb-1" style={{ color: '#9e9186' }}>Milestone reached</p>
        <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{milestone.title}</h2>
        <p className="text-[14px] leading-relaxed mb-6" style={{ color: '#5a5550' }}>{milestone.blurb}</p>
        <div className="flex items-center justify-center gap-2.5">
          <button
            onClick={() => downloadMilestoneCard(milestone, dateIso)}
            className="inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-[13px] font-semibold border-2 transition-transform active:translate-y-0.5"
            style={{ borderColor: 'rgba(242,107,31,0.35)', color: '#F26B1F' }}
          >
            <Share2 size={14} /> Share card
          </button>
          <button
            onClick={onClose}
            className="inline-flex items-center gap-1.5 rounded-full px-5 py-2 text-[13px] font-semibold text-white transition-transform active:translate-y-0.5"
            style={{ backgroundColor: '#F26B1F', boxShadow: '0 3px 0 #B54D14' }}
          >
            <Check size={14} /> Nice
          </button>
        </div>
      </MotionDiv>
    </div>
  );
};

export default MilestoneCelebration;
