/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { type AthleteRank, ATHLETE_RANKS } from '../gamificationConfig';
import {
  Footprints, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain,
  Star, X, ChevronRight,
} from 'lucide-react';
import { useModal } from '../hooks/useModal';

const RANK_ICON_MAP: Record<string, React.FC<{ size?: number; strokeWidth?: number; style?: React.CSSProperties }>> = {
  Footprints, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain, Star,
};

const RANK_DESCRIPTIONS: Record<string, string> = {
  newcomer: 'Your journey starts here. Every expert was once a beginner.',
  beginner: "You're in motion now. That matters more than you think.",
  consistent: "You keep showing up. That's rarer than talent.",
  dedicated: "The work is compounding. You can feel it.",
  driven: "Most people stop here. You didn't.",
  elite: "Top 5%. You've outworked almost everyone.",
  master: "This took real commitment. Every point was earned.",
  legend: "The highest rank. You did what most only talk about.",
};

const _RANK_UNLOCKS: Record<string, string> = {
  newcomer: 'Weekly goals unlocked',
  beginner: 'Strategy tracking enabled',
  consistent: 'Personal bests tracking active',
  dedicated: 'Advanced study insights unlocked',
  driven: 'Streak shields available',
  elite: 'Elite achievement tier unlocked',
  master: 'Master challenge tier unlocked',
  legend: 'All ranks completed',
};

const needsDarkText = (hex: string): boolean => {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return (r * 299 + g * 587 + b * 114) / 1000 > 160;
};

// Darken a hex color by mixing with black
const darkenHex = (hex: string, amount: number): string => {
  const r = Math.max(0, parseInt(hex.slice(1, 3), 16) - amount);
  const g = Math.max(0, parseInt(hex.slice(3, 5), 16) - amount);
  const b = Math.max(0, parseInt(hex.slice(5, 7), 16) - amount);
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
};

interface RankUpModalProps {
  isOpen: boolean;
  newRank: AthleteRank | null;
  onClose: () => void;
  onGoToJourney?: () => void;
}

const RankUpModal: React.FC<RankUpModalProps> = ({ isOpen, newRank, onClose, onGoToJourney }) => {
  useModal(isOpen, onClose);
  if (!newRank) return null;

  const rankIndex = ATHLETE_RANKS.findIndex(r => r.id === newRank.id);
  const isMaxRank = rankIndex === ATHLETE_RANKS.length - 1;
  const _nextRank = isMaxRank ? null : ATHLETE_RANKS[rankIndex + 1];
  const IconComponent = RANK_ICON_MAP[newRank.icon] || Star;
  const darkText = needsDarkText(newRank.colorHex);
  const heroText = darkText ? '#1C1917' : '#FFFFFF';
  const heroTextMuted = darkText ? 'rgba(28,25,23,0.45)' : 'rgba(255,255,255,0.65)';
  const _blobLight = darkText ? 'rgba(255,255,255,0.25)' : 'rgba(255,255,255,0.12)';
  const _blobDark = darkText ? 'rgba(0,0,0,0.06)' : 'rgba(0,0,0,0.08)';
  const btnColor = darkenHex(newRank.colorHex, 15);

  const d = (step: number) => 0.1 + step * 0.065;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.35 }}
          className="fixed inset-0 z-[300] overflow-y-auto bg-[#FDF8F0] dark:bg-zinc-950"
        >
          {/* ═══ Colour environment — top section ═══ */}
          <div className="relative" style={{ backgroundColor: newRank.colorHex }}>

            {/* ── Decorative blobs — layered, overlapping, varied ── */}
            {/* Massive blob — top right, mostly off-screen, very faint */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{
                top: -120, right: -100,
                width: 340, height: 340,
                borderRadius: '50%',
                background: darkText ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.07)',
              }}
              animate={{ y: [0, -6, 0] }}
              transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
            />
            {/* Overlapping mid blob — sits partly behind the massive one */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{
                top: 20, right: -30,
                width: 180, height: 180,
                borderRadius: '50%',
                background: darkText ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.1)',
              }}
              animate={{ y: [0, 8, 0], x: [0, -4, 0] }}
              transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
            />
            {/* Left cluster — large, mostly off-screen */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{
                top: 60, left: -90,
                width: 240, height: 240,
                borderRadius: '50%',
                background: darkText ? 'rgba(0,0,0,0.05)' : 'rgba(0,0,0,0.06)',
              }}
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 9, repeat: Infinity, ease: 'easeInOut' }}
            />
            {/* Left cluster — smaller, overlaps the large one */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{
                top: 140, left: 10,
                width: 100, height: 100,
                borderRadius: '50%',
                background: darkText ? 'rgba(0,0,0,0.04)' : 'rgba(0,0,0,0.05)',
              }}
              animate={{ y: [0, -5, 0], x: [0, 3, 0] }}
              transition={{ duration: 7, repeat: Infinity, ease: 'easeInOut' }}
            />
            {/* Bottom-right — medium, overlaps the wave edge */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{
                bottom: 10, right: 20,
                width: 130, height: 130,
                borderRadius: '50%',
                background: darkText ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.06)',
              }}
              animate={{ y: [0, -7, 0] }}
              transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
            />
            {/* Tiny accent — floating near title area */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{
                bottom: 140, left: '60%',
                width: 44, height: 44,
                borderRadius: '50%',
                background: darkText ? 'rgba(255,255,255,0.18)' : 'rgba(255,255,255,0.09)',
              }}
              animate={{ y: [0, 5, 0], x: [0, -3, 0] }}
              transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
            />

            {/* ── Content on colour ── */}
            <div className="relative z-10 px-6 pt-6 pb-16 max-w-md mx-auto">
              {/* Close + level */}
              <MotionDiv
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: d(0), duration: 0.4 }}
                className="flex items-center justify-between mb-10"
              >
                <span
                  className="text-[11px] font-semibold uppercase tracking-[0.14em]"
                  style={{ color: heroTextMuted }}
                >
                  Level {rankIndex + 1} of {ATHLETE_RANKS.length}
                </span>
                <button
                  onClick={onClose}
                  aria-label="Close"
                  className="w-9 h-9 flex items-center justify-center rounded-full transition-opacity hover:opacity-70"
                  style={{ backgroundColor: darkText ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.15)', color: heroText }}
                >
                  <X size={16} strokeWidth={2} />
                </button>
              </MotionDiv>

              {/* Icon — large, in frosted circle */}
              <MotionDiv
                initial={{ scale: 0.4, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: d(2), duration: 0.55, ease: [0.25, 1, 0.5, 1] }}
                className="mb-6"
              >
                <div
                  className="w-[72px] h-[72px] rounded-full flex items-center justify-center"
                  style={{
                    backgroundColor: darkText ? 'rgba(0,0,0,0.07)' : 'rgba(255,255,255,0.18)',
                  }}
                >
                  <IconComponent size={34} strokeWidth={1.5} style={{ color: heroText }} />
                </div>
              </MotionDiv>

              {/* Title */}
              <MotionDiv
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: d(4), duration: 0.6, ease: [0.25, 1, 0.5, 1] }}
                className="mb-3"
              >
                <h1
                  className="font-serif font-bold leading-[0.95]"
                  style={{
                    fontSize: 'clamp(48px, 13vw, 68px)',
                    letterSpacing: '-0.03em',
                    color: heroText,
                  }}
                >
                  {newRank.title}
                </h1>
              </MotionDiv>

              {/* Description */}
              <MotionDiv
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: d(6), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
              >
                <p
                  className="text-[16px] leading-relaxed"
                  style={{ color: heroTextMuted, maxWidth: 280 }}
                >
                  {RANK_DESCRIPTIONS[newRank.id]}
                </p>
              </MotionDiv>
            </div>

            {/* ── Wavy bottom edge ── */}
            <div className="absolute bottom-0 left-0 right-0" style={{ transform: 'translateY(1px)' }}>
              <svg
                viewBox="0 0 480 40"
                preserveAspectRatio="none"
                className="block w-full"
                style={{ height: 40 }}
              >
                <path
                  d="M0,20 C80,42 160,8 240,28 C320,48 400,12 480,24 L480,40 L0,40 Z"
                  className="fill-[#FDF8F0] dark:fill-zinc-950"
                />
              </svg>
            </div>
          </div>

          {/* ═══ Cream section — journey + milestone + CTA ═══ */}
          <div className="px-6 pb-10 max-w-md mx-auto bg-[#FDF8F0] dark:bg-zinc-950">

            {/* ── Journey progress ── */}
            <MotionDiv
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: d(9), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
              className="mb-5 pt-2"
            >
              <p
                className="text-[11px] font-semibold uppercase tracking-[0.12em] mb-3 text-[#A8A29E] dark:text-zinc-500"
              >
                Your journey
              </p>

              <div
                className="rounded-2xl px-5 py-5 bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800"
                style={{ boxShadow: '0 1px 4px rgba(28, 25, 23, 0.04)' }}
              >
                {/* Colour-coded segments with inline labels */}
                <div className="flex gap-1.5">
                  {ATHLETE_RANKS.map((rank, i) => {
                    const isCompleted = i <= rankIndex;
                    const isCurrent = i === rankIndex;
                    const isFirst = i === 0;
                    const isLast = i === ATHLETE_RANKS.length - 1;
                    const showLabel = isFirst || isCurrent || (isLast && !isCurrent);
                    return (
                      <div key={rank.id} className="flex-1 flex flex-col items-center">
                        <MotionDiv
                          className="w-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-700"
                          style={{
                            height: isCurrent ? 10 : 7,
                            borderRadius: 5,
                          }}
                          initial={{ scaleX: 0 }}
                          animate={{ scaleX: 1 }}
                          transition={{
                            delay: d(10) + i * 0.04,
                            duration: 0.25,
                            ease: 'easeOut',
                          }}
                        >
                          {isCompleted && (
                            <MotionDiv
                              className="h-full"
                              style={{
                                backgroundColor: rank.colorHex,
                                borderRadius: 5,
                              }}
                              initial={{ width: 0 }}
                              animate={{ width: '100%' }}
                              transition={{
                                delay: d(10) + i * 0.04 + 0.12,
                                duration: 0.4,
                                ease: [0.25, 1, 0.5, 1],
                              }}
                            />
                          )}
                        </MotionDiv>
                        {showLabel && (
                          <span
                            className="text-[9px] mt-1.5 whitespace-nowrap"
                            style={{
                              color: isCurrent ? newRank.colorHex : isCompleted ? rank.colorHex : '#C4C0BC',
                              fontWeight: isCurrent ? 700 : 500,
                            }}
                          >
                            {rank.title}
                          </span>
                        )}
                        {!showLabel && <div className="h-[18px]" />}
                      </div>
                    );
                  })}
                </div>
              </div>
            </MotionDiv>

            {/* ── Achievement card — saturated rank colour ── */}
            <MotionDiv
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: d(13), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
              className="mb-6"
            >
              <div
                className="rounded-2xl overflow-hidden relative"
                style={{
                  backgroundColor: newRank.colorHex,
                  boxShadow: `0 4px 20px ${newRank.colorHex}40`,
                }}
              >
                {/* Decorative blobs */}
                <div
                  className="absolute pointer-events-none"
                  style={{
                    top: -30, right: -30,
                    width: 100, height: 100,
                    borderRadius: '50%',
                    background: darkText ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.1)',
                  }}
                />
                <div
                  className="absolute pointer-events-none"
                  style={{
                    bottom: -20, left: -15,
                    width: 70, height: 70,
                    borderRadius: '50%',
                    background: darkText ? 'rgba(0,0,0,0.04)' : 'rgba(255,255,255,0.07)',
                  }}
                />

                <div className="relative px-5 py-5">
                  <div className="flex items-start gap-4">
                    {/* Icon badge — frosted */}
                    <div
                      className="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0"
                      style={{ backgroundColor: darkText ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.2)' }}
                    >
                      <Mountain size={24} strokeWidth={1.5} style={{ color: heroText }} />
                    </div>

                    <div className="flex-1 min-w-0">
                      <p
                        className="text-[11px] font-semibold uppercase tracking-[0.1em] mb-1"
                        style={{ color: heroText }}
                      >
                        Your island is growing
                      </p>
                      <p className="text-sm leading-relaxed" style={{ color: heroTextMuted }}>
                        3 new tiles added to your island. Visit My Journey to see it expand.
                      </p>
                    </div>
                  </div>

                  {onGoToJourney && (
                    <div
                      className="mt-4 pt-3"
                      style={{ borderTop: `1px solid ${darkText ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.2)'}` }}
                    >
                      <button
                        onClick={() => { onClose(); onGoToJourney(); }}
                        className="w-full flex items-center justify-center gap-1.5 text-xs font-semibold py-1 transition-opacity hover:opacity-70"
                        style={{ color: heroText }}
                      >
                        View My Journey
                        <ChevronRight size={14} />
                      </button>
                    </div>
                  )}
                  {!onGoToJourney && isMaxRank && (
                    <div
                      className="mt-4 pt-3 text-center"
                      style={{ borderTop: `1px solid ${darkText ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.2)'}` }}
                    >
                      <span className="text-xs font-bold" style={{ color: heroText }}>
                        Final rank reached
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </MotionDiv>

            {/* ── Continue button — uses rank colour ── */}
            <MotionDiv
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: d(15), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
            >
              <motion.button
                onClick={onClose}
                whileTap={{ scale: 0.98 }}
                className="w-full py-4 text-[15px] font-bold text-white transition-colors"
                style={{
                  backgroundColor: newRank.colorHex,
                  borderRadius: 14,
                  boxShadow: `0 4px 16px ${newRank.colorHex}30`,
                  color: needsDarkText(newRank.colorHex) ? '#1C1917' : '#FFFFFF',
                }}
                onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.backgroundColor = btnColor; }}
                onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.backgroundColor = newRank.colorHex; }}
              >
                Continue
              </motion.button>
            </MotionDiv>
          </div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default RankUpModal;
