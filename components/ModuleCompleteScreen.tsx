/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { CheckCircle2 } from 'lucide-react';

const SERIF = "'Source Serif 4', serif";

const needsDarkText = (hex: string): boolean => {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return (r * 299 + g * 587 + b * 114) / 1000 > 160;
};

interface ModuleCompleteScreenProps {
  isOpen: boolean;
  moduleTitle: string;
  moduleSubtitle?: string;
  categoryColor: string;
  modulesCompleted?: number;
  totalModules?: number;
  sectionsCount: number;
  northStarStatement?: string;
  onContinue: () => void;
  onReview?: () => void;
}

const ModuleCompleteScreen: React.FC<ModuleCompleteScreenProps> = ({
  isOpen, moduleTitle, moduleSubtitle, categoryColor, modulesCompleted, totalModules,
  sectionsCount, northStarStatement, onContinue, onReview,
}) => {
  const darkText = needsDarkText(categoryColor);
  const heroText = darkText ? '#1C1917' : '#FFFFFF';
  const heroTextMuted = darkText ? 'rgba(28,25,23,0.45)' : 'rgba(255,255,255,0.65)';
  const blobLight = darkText ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.07)';
  const blobMid = darkText ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.1)';
  const blobDark = darkText ? 'rgba(0,0,0,0.05)' : 'rgba(0,0,0,0.06)';
  const blobDarkSmall = darkText ? 'rgba(0,0,0,0.04)' : 'rgba(0,0,0,0.05)';
  const blobAccent = darkText ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.06)';

  const d = (step: number) => 0.1 + step * 0.065;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.35 }}
          className="fixed inset-0 z-[300] overflow-y-auto bg-[#FDF8F0] dark:bg-zinc-950"
        >
          {/* ═══ Colour environment — top section ═══ */}
          <div className="relative" style={{ backgroundColor: categoryColor }}>

            {/* Decorative blobs */}
            <MotionDiv
              className="absolute pointer-events-none"
              style={{ top: -120, right: -100, width: 340, height: 340, borderRadius: '50%', background: blobLight }}
              animate={{ y: [0, -6, 0] }}
              transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
            />
            <MotionDiv
              className="absolute pointer-events-none"
              style={{ top: 20, right: -30, width: 180, height: 180, borderRadius: '50%', background: blobMid }}
              animate={{ y: [0, 8, 0], x: [0, -4, 0] }}
              transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
            />
            <MotionDiv
              className="absolute pointer-events-none"
              style={{ top: 60, left: -90, width: 240, height: 240, borderRadius: '50%', background: blobDark }}
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 9, repeat: Infinity, ease: 'easeInOut' }}
            />
            <MotionDiv
              className="absolute pointer-events-none"
              style={{ top: 140, left: 10, width: 100, height: 100, borderRadius: '50%', background: blobDarkSmall }}
              animate={{ y: [0, -5, 0], x: [0, 3, 0] }}
              transition={{ duration: 7, repeat: Infinity, ease: 'easeInOut' }}
            />
            <MotionDiv
              className="absolute pointer-events-none"
              style={{ bottom: 10, right: 20, width: 130, height: 130, borderRadius: '50%', background: blobAccent }}
              animate={{ y: [0, -7, 0] }}
              transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
            />
            <MotionDiv
              className="absolute pointer-events-none"
              style={{ bottom: 140, left: '60%', width: 44, height: 44, borderRadius: '50%', background: blobLight }}
              animate={{ y: [0, 5, 0] }}
              transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
            />

            {/* Content */}
            <div className="relative z-10 flex flex-col items-center justify-center text-center px-8 pt-20 pb-24 md:pt-28 md:pb-32 max-w-lg mx-auto">

              {/* Label */}
              <MotionDiv
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: d(0), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
              >
                <p className="text-[11px] font-bold uppercase" style={{ letterSpacing: '0.2em', color: heroTextMuted }}>
                  Module Complete
                </p>
              </MotionDiv>

              {/* Checkmark icon */}
              <MotionDiv
                initial={{ scale: 0.4, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: d(2), duration: 0.6, type: 'spring', stiffness: 200, damping: 15 }}
                className="my-6"
              >
                <div
                  className="w-[72px] h-[72px] rounded-full flex items-center justify-center"
                  style={{ backgroundColor: darkText ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.15)', backdropFilter: 'blur(8px)' }}
                >
                  <CheckCircle2 size={34} style={{ color: heroText }} />
                </div>
              </MotionDiv>

              {/* Title */}
              <MotionDiv
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: d(4), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
              >
                <h1
                  className="font-serif font-bold"
                  style={{ fontSize: 'clamp(32px, 9vw, 52px)', lineHeight: 1.1, color: heroText }}
                >
                  {moduleTitle}
                </h1>
              </MotionDiv>

              {/* Subtitle */}
              {moduleSubtitle && (
                <MotionDiv
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: d(6), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
                >
                  <p className="text-base mt-3" style={{ color: heroTextMuted }}>
                    {moduleSubtitle}
                  </p>
                </MotionDiv>
              )}
            </div>

            {/* Wavy edge */}
            <div className="absolute bottom-0 left-0 right-0" style={{ transform: 'translateY(1px)' }}>
              <svg viewBox="0 0 1440 40" preserveAspectRatio="none" className="block w-full" style={{ height: 40 }}>
                <path
                  d="M0,20 C80,42 160,8 240,28 C320,48 400,12 480,24 L480,40 L0,40 Z"
                  className="fill-[#FDF8F0] dark:fill-zinc-950"
                />
              </svg>
            </div>
          </div>

          {/* ═══ Cream section — stats + CTA ═══ */}
          <div className="px-8 pb-12 max-w-md mx-auto bg-[#FDF8F0] dark:bg-zinc-950">

            {/* Stats row */}
            {modulesCompleted !== undefined && totalModules !== undefined && (
              <MotionDiv
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: d(10), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
                className="flex justify-center gap-12 pt-6 pb-8"
              >
                <div className="text-center">
                  <p className="text-3xl font-bold text-zinc-800 dark:text-white font-apercu tabular-nums">
                    {modulesCompleted} <span className="text-zinc-300 dark:text-zinc-600 font-light text-lg">/</span> <span className="text-lg text-zinc-400">{totalModules}</span>
                  </p>
                  <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mt-1">
                    modules complete
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-3xl font-bold text-zinc-800 dark:text-white font-apercu tabular-nums">
                    {sectionsCount}
                  </p>
                  <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mt-1">
                    sections finished
                  </p>
                </div>
              </MotionDiv>
            )}

            {/* North Star quote */}
            {northStarStatement && (
              <MotionDiv
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: d(13), duration: 0.6 }}
                className="text-center mb-8"
              >
                <p className="font-serif italic text-base leading-relaxed text-zinc-500 dark:text-zinc-400">
                  &ldquo;{northStarStatement}&rdquo;
                </p>
              </MotionDiv>
            )}

            {/* CTA */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: d(15), duration: 0.5, ease: [0.25, 1, 0.5, 1] }}
              className="space-y-3"
            >
              <button
                onClick={onContinue}
                className="w-full py-4 rounded-xl text-base font-semibold text-white transition-all active:scale-[0.98]"
                style={{ backgroundColor: categoryColor }}
              >
                Continue
              </button>
              {onReview && (
                <button
                  onClick={onReview}
                  className="w-full py-3 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                >
                  Review module
                </button>
              )}
            </MotionDiv>
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default ModuleCompleteScreen;
