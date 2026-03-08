/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Gift } from 'lucide-react';

const MotionDiv = motion.div as any;

interface MilestoneRewardModalProps {
  isOpen: boolean;
  onClose: () => void;
  itemName: string | null;
  modulesCompleted: number;
}

const MilestoneRewardModal: React.FC<MilestoneRewardModalProps> = ({ isOpen, onClose, itemName, modulesCompleted }) => {
  if (!itemName) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-[95]"
            onClick={onClose}
          />
          <MotionDiv
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed inset-0 z-[96] flex items-center justify-center p-6 pointer-events-none"
          >
            <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl p-8 max-w-sm w-full text-center pointer-events-auto">
              <div className="mx-auto w-16 h-16 rounded-2xl flex items-center justify-center mb-5 bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400">
                <Gift size={32} />
              </div>

              <p className="text-xs font-bold uppercase tracking-widest text-amber-500 mb-2">
                North Star Reward!
              </p>

              <h3 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">
                {itemName}
              </h3>

              <span className="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 mb-3">
                FREE
              </span>

              <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed mb-6">
                You've completed {modulesCompleted} modules!
              </p>

              <button
                onClick={onClose}
                className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-semibold text-sm transition-colors"
              >
                Continue
              </button>
            </div>
          </MotionDiv>
        </>
      )}
    </AnimatePresence>
  );
};

export default MilestoneRewardModal;
