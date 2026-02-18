/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
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
            className="relative w-full max-w-xl max-h-[85vh] overflow-y-auto bg-zinc-50 dark:bg-zinc-950 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-serif text-lg font-semibold text-zinc-900 dark:text-white">Edit My North Star</h2>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                <X size={18} className="text-zinc-500" />
              </button>
            </div>
            <NorthStarOnboarding
              onComplete={(ns) => { onSave(ns); onClose(); }}
              initialData={currentNorthStar}
            />
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default NorthStarEditModal;
