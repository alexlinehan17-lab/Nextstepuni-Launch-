/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles } from 'lucide-react';

const MotionDiv = motion.div as any;

interface PurchaseCelebrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  itemName: string | null;
}

const PurchaseCelebrationModal: React.FC<PurchaseCelebrationModalProps> = ({ isOpen, onClose, itemName }) => {
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
              <div className="mx-auto w-16 h-16 rounded-2xl flex items-center justify-center mb-5 bg-[rgba(var(--accent),0.15)] text-[var(--accent-hex)]">
                <Sparkles size={32} />
              </div>

              <h3 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-2">
                {itemName}
              </h3>

              <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed mb-4">
                Added to your island!
              </p>

              <button
                onClick={onClose}
                className="w-full py-3 rounded-xl bg-[var(--accent-hex)] text-white font-semibold text-sm hover:opacity-90 transition-opacity"
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

export default PurchaseCelebrationModal;
