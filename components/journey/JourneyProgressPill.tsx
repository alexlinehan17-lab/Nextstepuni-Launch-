/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion } from 'framer-motion';

const MotionDiv = motion.div as any;

interface JourneyProgressPillProps {
  tileCount: number;
  decoCount: number;
  pointsBalance: number;
  onTap: () => void;
}

const JourneyProgressPill: React.FC<JourneyProgressPillProps> = ({ tileCount, decoCount, pointsBalance, onTap }) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      onClick={onTap}
      className="absolute bottom-20 md:bottom-6 left-0 right-0 z-[80] flex justify-center cursor-pointer"
    >
      <div className="flex items-center gap-3 px-5 py-3 rounded-full bg-white/90 dark:bg-zinc-900/90 backdrop-blur-lg border border-zinc-200 dark:border-zinc-800 shadow-lg">
        <span className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">
          {tileCount} tiles · {decoCount} items
        </span>
        <div className="w-px h-4 bg-zinc-200 dark:bg-zinc-700" />
        <span className="text-sm font-bold text-[var(--accent-hex)]">
          {pointsBalance} pts
        </span>
      </div>
    </MotionDiv>
  );
};

export default JourneyProgressPill;
