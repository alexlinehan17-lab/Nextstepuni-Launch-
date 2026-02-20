/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Star } from 'lucide-react';
import { NorthStar } from '../types';
import NorthStarOnboarding from './NorthStarOnboarding';

const MotionDiv = motion.div as any;

interface NorthStarEditModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (northStar: NorthStar) => void;
  currentNorthStar: NorthStar | null;
}

const NorthStarEditModal: React.FC<NorthStarEditModalProps> = ({ isOpen, onClose, onSave, currentNorthStar }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[200] flex items-center justify-center p-4"
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />

          {/* Modal */}
          <MotionDiv
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="relative w-full max-w-xl max-h-[85vh] overflow-y-auto bg-zinc-50 dark:bg-zinc-950 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl"
          >
            {/* Gradient header */}
            <div className="relative overflow-hidden rounded-t-2xl bg-gradient-to-br from-[#CC785C]/20 via-amber-400/10 to-transparent px-6 pt-6 pb-8">
              <div className="absolute top-3 right-3">
                <button onClick={onClose} className="p-2 rounded-xl bg-white/50 dark:bg-zinc-800/50 hover:bg-white/80 dark:hover:bg-zinc-800/80 transition-colors backdrop-blur-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#CC785C]/50">
                  <X size={18} className="text-zinc-600 dark:text-zinc-400" />
                </button>
              </div>
              <div className="flex items-center gap-3">
                <MotionDiv
                  animate={{ rotate: [0, 10, -10, 0], scale: [1, 1.1, 1] }}
                  transition={{ duration: 3, repeat: Infinity, repeatDelay: 2, ease: 'easeInOut' }}
                  className="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-400 to-[#CC785C] flex items-center justify-center shadow-lg shadow-amber-400/20"
                >
                  <Star size={22} className="text-white" fill="white" />
                </MotionDiv>
                <div>
                  <p className="text-[10px] font-semibold uppercase tracking-widest text-[#CC785C] mb-0.5">Your Vision</p>
                  <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white">Edit My North Star</h2>
                </div>
              </div>
            </div>

            <div className="px-6 pb-6 pt-2">
              <NorthStarOnboarding
                onComplete={(ns) => { onSave(ns); onClose(); }}
                initialData={currentNorthStar}
              />
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default NorthStarEditModal;
