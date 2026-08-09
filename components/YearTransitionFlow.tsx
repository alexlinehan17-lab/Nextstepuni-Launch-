/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, GraduationCap, Sparkles, X } from 'lucide-react';
import { type YearGroup } from './subjectData';
import { nextYearAction, yearGroupLabel } from '../utils/authUtils';

// ─── Year transition flow (Phase 8) ─────────────────────────────────────────
//
// Modal-based forward-progression UI. Three flavours:
//
//   1. Quiet bump (1st→2nd, 2nd→3rd, TY→5th, 5th→6th)
//      — single confirm modal, then `onConfirmBump(nextYearGroup)` fires
//        a Firestore write + brief "Welcome to X Year" toast (handled in
//        the parent). Curriculum stays the same.
//
//   2. JC→senior crossover (3rd → TY or 5th)
//      — picker modal with two chunky cards (TY vs 5th). Confirming either
//        fires `onConfirmJCtoSenior(targetYear)` which the parent uses to
//        archive JC data and open the re-onboarding flow (Subjects →
//        Grades → North Star).
//
//   3. Graduation (6th → graduated)
//      — confirm modal with tightened copy ("Have you ACTUALLY sat your
//        LC exams? Tap this only after the exams are completely
//        finished.") and the cancel button styled as the primary action
//        to bias away from accidental clicks.
//
// Confirmation flow is the only safety net — there's no undo. The
// pastJCData archive on the user doc is the manual rollback path for
// genuine mistakes (out of scope here).

interface YearTransitionFlowProps {
  isOpen: boolean;
  onClose: () => void;
  currentYearGroup: YearGroup | undefined;
  /** Quiet bump within a curriculum — parent writes the new yearGroup
   *  and shows a brief celebratory toast. */
  onConfirmBump: (next: YearGroup) => Promise<void>;
  /** JC → senior crossover — parent archives JC data + opens the
   *  TransitionToSenior re-onboarding flow. */
  onConfirmJCtoSenior: (target: 'TY' | '5th') => Promise<void>;
  /** 6th-year → graduated — parent writes yearGroup='graduated' and the
   *  Settings UI flips to the soft post-LC label on next render. No
   *  sign-out, no special screen. */
  onConfirmGraduate: () => Promise<void>;
}

type Phase = 'confirm-bump' | 'pick-senior' | 'confirm-graduate' | 'submitting';

export const YearTransitionFlow: React.FC<YearTransitionFlowProps> = ({
  isOpen, onClose, currentYearGroup, onConfirmBump, onConfirmJCtoSenior, onConfirmGraduate,
}) => {
  const action = currentYearGroup ? nextYearAction(currentYearGroup) : null;
  // Derive phase from `action` every render. Previously this was a
  // useState lazy initializer that locked phase at first mount — when
  // action was still null (currentYearGroup populated late) — leaving
  // the modal empty for 3rd-year users whose real phase was 'pick-senior'.
  const phase: Phase = !action
    ? 'confirm-bump'
    : action.kind === 'pick-senior'
      ? 'pick-senior'
      : action.kind === 'graduate'
        ? 'confirm-graduate'
        : 'confirm-bump';
  const [isSubmitting, setIsSubmitting] = useState(false);

  const close = () => { if (!isSubmitting) onClose(); };

  const handleBumpConfirm = async () => {
    if (!action || action.kind !== 'bump') return;
    setIsSubmitting(true);
    try {
      await onConfirmBump(action.next);
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSeniorPick = async (target: 'TY' | '5th') => {
    setIsSubmitting(true);
    try {
      await onConfirmJCtoSenior(target);
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGraduate = async () => {
    setIsSubmitting(true);
    try {
      await onConfirmGraduate();
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!action || action.kind === 'terminal') return null;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[300] flex items-end sm:items-center justify-center bg-[#1A1A1A]/55 p-0 sm:p-4"
          onClick={close}
        >
          <MotionDiv
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
            className="bg-[#FDF8F0] dark:bg-zinc-900 rounded-t-[24px] sm:rounded-[24px] border-[1.5px] border-[#383838] shadow-[5px_5px_0_0_#383838] max-w-md w-full p-6"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Close button */}
            <div className="flex items-start justify-between mb-4">
              <div className="w-11 h-11 rounded-xl flex items-center justify-center bg-[rgba(242,107,31,0.12)]">
                {phase === 'confirm-graduate'
                  ? <GraduationCap size={22} className="text-[#F26B1F]" />
                  : <Sparkles size={22} className="text-[#F26B1F]" />}
              </div>
              <button
                onClick={close}
                disabled={isSubmitting}
                className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 disabled:opacity-40 transition-colors"
                aria-label="Close"
              >
                <X size={18} className="text-zinc-500" />
              </button>
            </div>

            {phase === 'confirm-bump' && action.kind === 'bump' && (
              <>
                <h2 className="font-serif text-2xl font-bold text-[#1A1A1A] dark:text-white mb-2">
                  Moving up to {yearGroupLabel(action.next)}?
                </h2>
                <p className="text-sm text-[#78716C] dark:text-zinc-400 leading-relaxed mb-6">
                  You'll start seeing content tuned to {yearGroupLabel(action.next)}.
                  This is a one-way step — your data stays put, you just shift forward.
                </p>
                <div className="flex flex-col gap-2">
                  <button
                    onClick={handleBumpConfirm}
                    disabled={isSubmitting}
                    className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-150"
                  >
                    {isSubmitting ? 'Saving…' : `Yes, I'm in ${yearGroupLabel(action.next)}`}
                    {!isSubmitting && <ArrowRight size={14} />}
                  </button>
                  <button
                    onClick={close}
                    disabled={isSubmitting}
                    className="w-full py-2 rounded-xl text-sm font-semibold text-[#78716C] hover:text-[#1A1A1A] dark:hover:text-white disabled:opacity-40 transition-colors"
                  >
                    Not yet
                  </button>
                </div>
              </>
            )}

            {phase === 'pick-senior' && (
              <>
                <h2 className="font-serif text-2xl font-bold text-[#1A1A1A] dark:text-white mb-2">
                  Starting Senior Cycle
                </h2>
                <p className="text-sm text-[#78716C] dark:text-zinc-400 leading-relaxed mb-5">
                  Pick what's next. You'll then set up your senior subjects,
                  grades, and a fresh North Star — your JC profile gets quietly
                  archived (you can pick it up again later if needed).
                </p>
                <div className="flex flex-col gap-3 mb-2">
                  <button
                    onClick={() => handleSeniorPick('TY')}
                    disabled={isSubmitting}
                    className="text-left px-4 py-4 rounded-2xl border-2 border-[#1A1A1A] bg-[#FDF8F0] text-[#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-150"
                  >
                    <p className="font-bold mb-1">Transition Year (4th)</p>
                    <p className="text-xs text-[#78716C]">
                      A year for exploration, work experience, and trying new subjects.
                    </p>
                  </button>
                  <button
                    onClick={() => handleSeniorPick('5th')}
                    disabled={isSubmitting}
                    className="text-left px-4 py-4 rounded-2xl border-2 border-[#1A1A1A] bg-[#FDF8F0] text-[#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-150"
                  >
                    <p className="font-bold mb-1">Straight to 5th Year</p>
                    <p className="text-xs text-[#78716C]">
                      Skip TY and start Leaving Cert prep right away.
                    </p>
                  </button>
                </div>
                <button
                  onClick={close}
                  disabled={isSubmitting}
                  className="w-full py-2 rounded-xl text-sm font-semibold text-[#78716C] hover:text-[#1A1A1A] dark:hover:text-white disabled:opacity-40 transition-colors mt-2"
                >
                  Not yet
                </button>
              </>
            )}

            {phase === 'confirm-graduate' && (
              <>
                <h2 className="font-serif text-2xl font-bold text-[#1A1A1A] dark:text-white mb-2">
                  Mark as graduated?
                </h2>
                <p className="text-sm text-[#78716C] dark:text-zinc-400 leading-relaxed mb-1">
                  <span className="font-bold text-[#1A1A1A] dark:text-white">Have you actually sat your Leaving Cert exams?</span>
                </p>
                <p className="text-sm text-[#78716C] dark:text-zinc-400 leading-relaxed mb-6">
                  Tap this only after the exams are completely finished — not before.
                  You'll still have full access to everything in the app.
                </p>
                {/* Cancel is the primary-styled button to bias away from
                    accidental graduation. Confirm is a subdued text link. */}
                <div className="flex flex-col gap-2">
                  <button
                    onClick={close}
                    disabled={isSubmitting}
                    className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-150"
                  >
                    Not yet
                  </button>
                  <button
                    onClick={handleGraduate}
                    disabled={isSubmitting}
                    className="w-full py-2 rounded-xl text-sm font-semibold text-[#78716C] hover:text-[#1A1A1A] dark:hover:text-white disabled:opacity-40 transition-colors"
                  >
                    {isSubmitting ? 'Saving…' : 'Yes, exams are done'}
                  </button>
                </div>
              </>
            )}
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default YearTransitionFlow;
