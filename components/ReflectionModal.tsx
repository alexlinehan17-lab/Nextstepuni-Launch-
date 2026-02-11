/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Star, BookOpen, Target, RotateCcw } from 'lucide-react';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

interface ReflectionModalProps {
  isOpen: boolean;
  subjectName: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  basePoints: number;
  streakMultiplier: number;
  onSubmit: (reflectionText: string) => void;
  onCancel: () => void;
}

const SESSION_TYPE_LABELS: Record<string, { label: string; icon: React.ElementType }> = {
  'new-learning': { label: 'New Learning', icon: BookOpen },
  'practice': { label: 'Practice', icon: Target },
  'revision': { label: 'Revision', icon: RotateCcw },
};

const MIN_CHARS = 15;

const ReflectionModal: React.FC<ReflectionModalProps> = ({
  isOpen, subjectName, sessionType, basePoints, streakMultiplier, onSubmit, onCancel,
}) => {
  const [text, setText] = useState('');
  const totalPoints = Math.round(basePoints * streakMultiplier);
  const typeConfig = SESSION_TYPE_LABELS[sessionType] || SESSION_TYPE_LABELS['new-learning'];
  const TypeIcon = typeConfig.icon;
  const isValid = text.trim().length >= MIN_CHARS;

  const handleSubmit = () => {
    if (!isValid) return;
    onSubmit(text.trim());
    setText('');
  };

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4"
          onClick={onCancel}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-md shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-0">
              <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                Quick Reflection
              </h2>
              <button
                onClick={onCancel}
                className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-6 space-y-5">
              {/* Subject + Session info */}
              <div className="flex items-center gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200/50 dark:border-white/[0.08]">
                <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/40 flex items-center justify-center flex-shrink-0">
                  <TypeIcon size={20} className="text-purple-600 dark:text-purple-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200 truncate">{subjectName}</p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">{typeConfig.label} session</p>
                </div>
              </div>

              {/* Points preview */}
              <div className="flex items-center justify-center gap-3 p-3 rounded-xl bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30">
                <Star size={16} className="text-amber-500" />
                <span className="text-sm font-bold text-amber-700 dark:text-amber-300">
                  +{totalPoints} pts
                </span>
                {streakMultiplier > 1 && (
                  <span className="text-[10px] text-amber-500 dark:text-amber-400 font-semibold">
                    ({basePoints} x {streakMultiplier} streak)
                  </span>
                )}
              </div>

              {/* Reflection textarea */}
              <div>
                <label className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2 block">
                  What did you learn or work on?
                </label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="e.g. Practiced integration by parts — struggled with choosing u and dv but got better after 3 examples..."
                  className="w-full bg-zinc-50 dark:bg-white/[0.05] border border-zinc-200/50 dark:border-white/[0.1] rounded-xl py-3 px-4 text-zinc-900 dark:text-white/90 text-sm font-sans placeholder:text-zinc-400 dark:placeholder:text-white/30 focus:outline-none focus:border-purple-400/60 focus:ring-1 focus:ring-purple-400/30 transition-colors resize-none h-24"
                  autoFocus
                />
                <p className={`text-[10px] mt-1.5 font-medium ${
                  isValid ? 'text-emerald-500' : 'text-zinc-400 dark:text-zinc-500'
                }`}>
                  {text.trim().length}/{MIN_CHARS} characters minimum
                </p>
              </div>

              {/* Submit */}
              <MotionButton
                onClick={handleSubmit}
                disabled={!isValid}
                whileHover={isValid ? { scale: 1.02 } : {}}
                whileTap={isValid ? { scale: 0.98 } : {}}
                className={`w-full py-3 rounded-xl text-sm font-bold transition-all ${
                  isValid
                    ? 'bg-purple-600 text-white hover:bg-purple-700 shadow-lg shadow-purple-500/20'
                    : 'bg-zinc-100 dark:bg-white/[0.06] text-zinc-400 dark:text-white/20 cursor-not-allowed'
                }`}
              >
                Complete & Earn {totalPoints} pts
              </MotionButton>
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default ReflectionModal;
