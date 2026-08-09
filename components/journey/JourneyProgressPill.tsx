/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { MotionDiv } from '../Motion';

interface JourneyProgressPillProps {
  tileCount: number;
  decoCount: number;
  pointsBalance: number;
  stageName: string;
  stageProgress: number;
  onTap: () => void;
}

const JourneyProgressPill: React.FC<JourneyProgressPillProps> = ({ tileCount, decoCount, pointsBalance, stageName, stageProgress, onTap }) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      onClick={onTap}
      // Mobile: sit above the fixed bottom nav (h-16 = 64px) plus the home-indicator
      // safe-area inset. md+: use the smaller bottom-6 inset (no fixed nav there).
      className="absolute md:bottom-6 left-0 right-0 z-[80] flex justify-center cursor-pointer"
      style={{ bottom: 'calc(80px + var(--sab, 0px))' }}
    >
      <div className="flex items-center gap-3 px-5 py-3 rounded-full bg-[#FFFDF8]/95 dark:bg-[#201F1D]/95 backdrop-blur-lg border-2 border-[#343230] dark:border-[#D8D1C8] shadow-[0_4px_0_#343230] dark:shadow-[0_4px_0_#D8D1C8]">
        <div className="hidden sm:block min-w-[82px]">
          <div className="flex items-center justify-between gap-2">
            <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-[#756F69] dark:text-[#D6CEC4]">{stageName}</span>
            <span className="font-mono text-[9px] text-[#A0978D]">{Math.round(stageProgress * 100)}%</span>
          </div>
          <div className="mt-1 h-1 overflow-hidden rounded-full bg-[#E5DED5] dark:bg-[#403D39]"><div className="h-full rounded-full bg-[#F26B1F]" style={{ width: `${stageProgress * 100}%` }} /></div>
        </div>
        <div className="hidden sm:block w-px h-5 bg-[#D8D1C8] dark:bg-[#57524C]" />
        <span className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">
          {tileCount} tiles · {decoCount} items
        </span>
        <div className="w-px h-4 bg-zinc-200 dark:bg-zinc-700" />
        <span className="text-sm font-bold text-[var(--accent-hex)]">
          {pointsBalance} JP
        </span>
      </div>
    </MotionDiv>
  );
};

export default JourneyProgressPill;
