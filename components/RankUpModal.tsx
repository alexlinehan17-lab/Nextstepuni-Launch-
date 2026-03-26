/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { type AthleteRank, ATHLETE_RANKS } from '../gamificationConfig';

const RANK_DESCRIPTIONS: Record<string, string> = {
  newcomer: 'Your journey starts here.',
  beginner: "You're building momentum. Keep showing up.",
  consistent: "Consistency beats talent. You're proving it.",
  dedicated: "Your dedication is paying off. Feel the difference.",
  driven: "Nothing can stop you now. You're unstoppable.",
  elite: "Top tier. Most students never get here.",
  master: "True mastery. You've earned every point.",
  legend: "Legendary. You're an inspiration.",
};

interface RankUpModalProps {
  isOpen: boolean;
  newRank: AthleteRank | null;
  onClose: () => void;
}

const RankUpModal: React.FC<RankUpModalProps> = ({ isOpen, newRank, onClose }) => {
  if (!newRank) return null;

  // Find next rank for progress bar
  const nextRank = useMemo(() => {
    const idx = ATHLETE_RANKS.findIndex(r => r.id === newRank.id);
    return idx < ATHLETE_RANKS.length - 1 ? ATHLETE_RANKS[idx + 1] : null;
  }, [newRank]);

  // Generate particles
  const particles = useMemo(() =>
    Array.from({ length: 32 }, (_, i) => {
      const angle = (i / 32) * Math.PI * 2;
      const distance = 120 + Math.random() * 140;
      return {
        x: Math.cos(angle) * distance,
        y: Math.sin(angle) * distance,
        size: 3 + Math.random() * 6,
        delay: Math.random() * 0.4,
        color: i % 3 === 0 ? newRank.colorHex : i % 3 === 1 ? '#F59E0B' : '#4CC9F0',
      };
    }), [newRank]);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[300] flex flex-col items-center justify-center"
          style={{ backgroundColor: '#FAFAF7' }}
        >
          {/* Gradient wash — rank color dominates the top half */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background: `radial-gradient(ellipse at 50% 30%, ${newRank.colorHex}25 0%, transparent 60%), linear-gradient(180deg, ${newRank.colorHex}15 0%, transparent 50%)`,
            }}
          />

          {/* Particle burst */}
          <div className="absolute pointer-events-none" style={{ top: '30%', left: '50%' }}>
            {particles.map((p, i) => (
              <motion.div
                key={i}
                className="absolute rounded-full"
                style={{
                  width: p.size,
                  height: p.size,
                  backgroundColor: p.color,
                  left: 0,
                  top: 0,
                }}
                initial={{ x: 0, y: 0, opacity: 1, scale: 0 }}
                animate={{ x: p.x, y: p.y, opacity: 0, scale: 1.5 }}
                transition={{ duration: 1, delay: 0.3 + p.delay, ease: 'easeOut' }}
              />
            ))}
          </div>

          {/* Content */}
          <div className="relative z-10 flex flex-col items-center text-center px-6 max-w-md">
            {/* "RANK UP" label */}
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-[11px] font-bold uppercase tracking-[0.3em] mb-4"
              style={{ color: newRank.colorHex }}
            >
              Rank Up
            </motion.p>

            {/* Giant rank name — the hero with glow */}
            <motion.div
              initial={{ opacity: 0, scale: 0.7, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
              className="relative mb-6"
            >
              {/* Glow behind text */}
              <div
                className="absolute inset-0 blur-3xl opacity-30"
                style={{ background: newRank.colorHex, borderRadius: '50%', transform: 'scale(1.5, 2)' }}
              />
              <h1
                className="relative font-serif font-bold leading-none"
                style={{ fontSize: 'clamp(64px, 18vw, 100px)', color: newRank.colorHex, letterSpacing: '-0.03em' }}
              >
                {newRank.title}
              </h1>
            </motion.div>

            {/* Description */}
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7, duration: 0.5 }}
              className="text-lg text-zinc-500 leading-relaxed mb-10"
            >
              {RANK_DESCRIPTIONS[newRank.id] || 'Keep pushing forward.'}
            </motion.p>

            {/* Progress to next rank */}
            {nextRank && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9, duration: 0.5 }}
                className="w-full max-w-xs mb-10"
              >
                <div className="flex justify-between mb-2">
                  <span className="text-xs font-semibold" style={{ color: newRank.colorHex }}>{newRank.title}</span>
                  <span className="text-xs font-medium text-zinc-400">{nextRank.title}</span>
                </div>
                <div className="w-full h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'rgba(0,0,0,0.06)' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ backgroundColor: newRank.colorHex }}
                    initial={{ width: 0 }}
                    animate={{ width: '8%' }}
                    transition={{ delay: 1.1, duration: 0.8, ease: 'easeOut' }}
                  />
                </div>
                <p className="text-[10px] text-zinc-400 mt-1.5 text-center">
                  {nextRank.minPoints - newRank.minPoints} pts to {nextRank.title}
                </p>
              </motion.div>
            )}

            {/* Continue button */}
            <motion.button
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.1, duration: 0.5 }}
              onClick={onClose}
              className="px-10 py-3.5 rounded-full text-sm font-bold text-white transition-all hover:scale-[1.02] active:scale-[0.98]"
              style={{ backgroundColor: '#1a1a2e' }}
            >
              Continue
            </motion.button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default RankUpModal;
