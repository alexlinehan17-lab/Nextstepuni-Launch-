/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { type AchievementDefinition } from '../gamificationConfig';

interface AchievementToastProps {
  achievement: AchievementDefinition | null;
  onDismiss: () => void;
}

const AchievementToast: React.FC<AchievementToastProps> = ({ achievement, onDismiss }) => {
  // Use ref for onDismiss to avoid resetting the timer on every render
  const onDismissRef = useRef(onDismiss);
  onDismissRef.current = onDismiss;

  const isVisible = achievement !== null;

  // Give the quieter editorial card enough time to be read without letting it
  // linger over the page. Only re-trigger when the achievement itself changes.
  useEffect(() => {
    if (!isVisible) return;
    const timer = setTimeout(() => onDismissRef.current(), 4500);
    return () => clearTimeout(timer);
  }, [isVisible, achievement?.id]);

  return (
    <AnimatePresence>
      {achievement && (
        <MotionDiv
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
          role="status"
          aria-live="polite"
          aria-atomic="true"
          className="mt-2 ml-auto w-[286px] max-w-[calc(100vw-2rem)]"
        >
          <button
            type="button"
            onClick={onDismiss}
            aria-label={`Dismiss achievement: ${achievement.title}`}
            className="group w-full overflow-hidden rounded-2xl border border-[#DEDAD3] bg-white text-left shadow-[0_10px_30px_rgba(28,25,23,0.10)] transition-[transform,border-color,box-shadow] duration-200 hover:-translate-y-0.5 hover:border-[#C8C2B9] hover:shadow-[0_14px_34px_rgba(28,25,23,0.13)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#F26B1F]/45 dark:border-zinc-700 dark:bg-zinc-900 dark:hover:border-zinc-600"
          >
            <div className="flex items-center justify-between gap-4 px-4 pt-3.5 pb-2.5">
              <span className="flex min-w-0 items-center gap-2 text-[9px] font-bold uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">
                <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-[#F26B1F]" aria-hidden="true" />
                Achievement unlocked
              </span>
              {achievement.bonusPoints > 0 && (
                <span className="shrink-0 text-[11px] font-bold tabular-nums text-[#F26B1F]">
                  +{achievement.bonusPoints} JP
                </span>
              )}
            </div>
            <div className="mx-4 h-px bg-[#ECE8E2] dark:bg-zinc-800" />
            <div className="px-4 pt-2.5 pb-3.5">
              <p
                className="truncate text-[17px] font-semibold leading-tight text-[#1A1A1A] dark:text-zinc-50"
                style={{ fontFamily: "'Source Serif 4', serif" }}
              >
                {achievement.title}
              </p>
              <p className="mt-1 text-[10px] font-medium text-zinc-400 dark:text-zinc-500">
                Added to My Progress
              </p>
            </div>
          </button>
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default AchievementToast;
