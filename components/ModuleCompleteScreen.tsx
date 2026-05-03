/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { CheckCircle2, BookOpen, Layers, Compass, ArrowRight, Star } from 'lucide-react';

interface ModuleCompleteScreenProps {
  isOpen: boolean;
  moduleTitle: string;
  moduleSubtitle?: string;
  categoryColor: string;
  modulesCompleted?: number;
  totalModules?: number;
  sectionsCount: number;
  northStarStatement?: string;
  onContinue: () => void;
  onReview?: () => void;
}

const d = (step: number) => 0.15 + step * 0.07;

const ModuleCompleteScreen: React.FC<ModuleCompleteScreenProps> = ({
  isOpen, moduleTitle, moduleSubtitle, _categoryColor, modulesCompleted, totalModules,
  sectionsCount, northStarStatement, onContinue, onReview,
}) => {

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.35 }}
          className="fixed inset-0 z-[300] overflow-y-auto bg-[#FAFBF6] dark:bg-zinc-950"
        >
          <div className="min-h-screen flex flex-col items-center justify-center px-6 py-16">
            <div className="max-w-md w-full text-center">

              {/* Label */}
              <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: d(0), duration: 0.4 }}>
                <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider" style={{ backgroundColor: '#6EE7B7', border: '2px solid #059669', color: '#064E3B', boxShadow: '2px 2px 0px 0px #059669' }}>
                  <Star size={12} /> Module Complete
                </span>
              </MotionDiv>

              {/* Big checkmark */}
              <MotionDiv
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: d(2), duration: 0.6, type: 'spring', stiffness: 200, damping: 12 }}
                className="my-8 flex justify-center"
              >
                <div className="w-24 h-24 rounded-full flex items-center justify-center" style={{ backgroundColor: '#6EE7B7', border: '3px solid #059669', boxShadow: '5px 5px 0px 0px #059669' }}>
                  <CheckCircle2 size={44} style={{ color: '#064E3B' }} />
                </div>
              </MotionDiv>

              {/* Title */}
              <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: d(4), duration: 0.5 }}>
                <h1 className="font-serif font-bold text-zinc-900 dark:text-white" style={{ fontSize: 'clamp(28px, 8vw, 44px)', lineHeight: 1.15, letterSpacing: '-0.025em' }}>
                  {moduleTitle}
                </h1>
              </MotionDiv>

              {moduleSubtitle && (
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: d(6), duration: 0.4 }}>
                  <p className="text-base text-zinc-500 dark:text-zinc-400 mt-2">{moduleSubtitle}</p>
                </MotionDiv>
              )}

              {/* Stats — chunky cards */}
              {modulesCompleted !== undefined && totalModules !== undefined && (
                <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: d(8), duration: 0.5 }} className="flex justify-center gap-4 mt-8">
                  <div className="px-6 py-4 text-center" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '3px 3px 0px 0px #2563EB' }}>
                    <div className="flex items-center justify-center gap-1.5 mb-1">
                      <BookOpen size={14} style={{ color: '#1E3A8A' }} />
                      <span className="text-xl font-bold" style={{ color: '#1E3A8A' }}>{modulesCompleted}/{totalModules}</span>
                    </div>
                    <p className="text-[9px] font-bold uppercase tracking-widest" style={{ color: '#1E3A8A' }}>Modules</p>
                  </div>
                  <div className="px-6 py-4 text-center" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '3px 3px 0px 0px #D97706' }}>
                    <div className="flex items-center justify-center gap-1.5 mb-1">
                      <Layers size={14} style={{ color: '#78350F' }} />
                      <span className="text-xl font-bold" style={{ color: '#78350F' }}>{sectionsCount}</span>
                    </div>
                    <p className="text-[9px] font-bold uppercase tracking-widest" style={{ color: '#78350F' }}>Sections</p>
                  </div>
                </MotionDiv>
              )}

              {/* North Star */}
              {northStarStatement && (
                <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: d(11), duration: 0.5 }} className="mt-8">
                  <div className="rounded-2xl px-6 py-5 bg-[#FAF7F4] dark:bg-zinc-800/60">
                    <div className="flex items-center justify-center gap-1.5 mb-2">
                      <Compass size={12} className="text-zinc-400" />
                      <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400">Your North Star</p>
                    </div>
                    <p className="font-serif italic text-base leading-relaxed text-zinc-600 dark:text-zinc-400">
                      &ldquo;{northStarStatement}&rdquo;
                    </p>
                  </div>
                </MotionDiv>
              )}

              {/* CTA */}
              <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: d(14), duration: 0.5 }} className="mt-8 space-y-3">
                <motion.button
                  onClick={onContinue}
                  className="w-full py-4 rounded-2xl text-base font-bold text-white flex items-center justify-center gap-2"
                  style={{
                    backgroundColor: '#2A7D6F',
                    border: '2.5px solid #1F5F54',
                    boxShadow: '4px 4px 0px 0px #1F5F54',
                  }}
                  whileHover={{ x: -2, y: -2, boxShadow: '6px 6px 0px 0px #1F5F54' }}
                  whileTap={{ x: 2, y: 2, boxShadow: '1px 1px 0px 0px #1F5F54' }}
                  transition={{ type: 'spring', stiffness: 400, damping: 25 }}
                >
                  Continue <ArrowRight size={18} />
                </motion.button>
                {onReview && (
                  <button onClick={onReview} className="w-full py-3 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
                    Review module
                  </button>
                )}
              </MotionDiv>
            </div>
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default ModuleCompleteScreen;
