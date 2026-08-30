/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { MotionButton } from '../Motion';

interface JourneyProgressPillProps {
  tileCount: number;
  decoCount: number;
  pointsBalance: number;
  stageName: string;
  stageProgress: number;
  nextStageName?: string;
  modulesToNext?: number;
  onTap: () => void;
}

const JourneyProgressPill: React.FC<JourneyProgressPillProps> = ({ tileCount, decoCount, pointsBalance, stageName, stageProgress, nextStageName, modulesToNext = 0, onTap }) => {
  const firstAddition = tileCount === 0 && decoCount === 0;

  return (
    <MotionButton
      type="button"
      aria-label="Open Journey shop and progress"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      onClick={onTap}
      // Mobile: sit above the fixed bottom nav (h-16 = 64px) plus the home-indicator
      // safe-area inset. md+: use the smaller bottom-6 inset (no fixed nav there).
      className="absolute bottom-[calc(80px+var(--sab,0px))] left-4 right-4 z-[80] flex cursor-pointer justify-center rounded-2xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/80 md:bottom-6"
    >
      <div className="w-full max-w-md rounded-2xl border-2 border-[#343230] bg-[#FFFDF8]/95 px-4 py-3 text-left shadow-[0_4px_0_#343230] backdrop-blur-lg dark:border-[#D8D1C8] dark:bg-[#201F1D]/95 dark:shadow-[0_4px_0_#D8D1C8] sm:max-w-none sm:rounded-full sm:px-5">
        <div className="flex items-center gap-3">
          <div className="min-w-0 flex-1 sm:min-w-[110px]">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-[#756F69] dark:text-[#D6CEC4]">{stageName}</span>
              <span className="font-mono text-[9px] text-[#A0978D]">{Math.round(stageProgress * 100)}%</span>
            </div>
            <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-[#E5DED5] dark:bg-[#403D39]"><div className="h-full rounded-full bg-[#F26B1F]" style={{ width: `${stageProgress * 100}%` }} /></div>
          </div>
          <div className="h-7 w-px bg-[#D8D1C8] dark:bg-[#57524C]" />
          <span className="shrink-0 text-sm font-bold text-[var(--accent-hex)]">{pointsBalance} JP</span>
        </div>
        <div className="mt-2 flex items-center justify-between gap-3 border-t border-[#E5DED5] pt-2 dark:border-[#403D39] sm:hidden">
          <span className="truncate text-xs font-semibold text-zinc-800 dark:text-zinc-200">
            {firstAddition ? 'Shape your first path' : `${tileCount} tile${tileCount === 1 ? '' : 's'} · ${decoCount} detail${decoCount === 1 ? '' : 's'}`}
          </span>
          <span className="shrink-0 text-[10px] font-semibold text-[#756F69] dark:text-[#D6CEC4]">
            {nextStageName && modulesToNext > 0 ? `${modulesToNext} to ${nextStageName}` : 'Open journey shop'}
          </span>
        </div>
      </div>
    </MotionButton>
  );
};

export default JourneyProgressPill;
