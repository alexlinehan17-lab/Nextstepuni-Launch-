/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { X, Check, Lock } from 'lucide-react';
import { useModal } from '../hooks/useModal';
import { type CategoryType } from './KnowledgeTree';
import { type CourseData } from './Library';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface StudyPassportModalProps {
  isOpen: boolean;
  onClose: () => void;
  userProgress: UserProgress;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
}

// Category display order and stamp colors (literal Tailwind classes for CDN)
const CATEGORY_ORDER: { key: CategoryType; stampBg: string; stampRing: string }[] = [
  { key: 'architecture-mindset', stampBg: 'bg-blue-500', stampRing: 'ring-blue-500/30' },
  { key: 'science-growth', stampBg: 'bg-amber-500', stampRing: 'ring-amber-500/30' },
  { key: 'learning-cheat-codes', stampBg: 'bg-teal-500', stampRing: 'ring-teal-500/30' },
  { key: 'subject-specific-science', stampBg: 'bg-slate-500', stampRing: 'ring-slate-500/30' },
  { key: 'exam-zone', stampBg: 'bg-red-500', stampRing: 'ring-red-500/30' },
];

const StudyPassportModal: React.FC<StudyPassportModalProps> = ({
  isOpen,
  onClose,
  userProgress,
  allCourses,
  categoryTitles,
}) => {
  useModal(isOpen, onClose);
  const totalModules = allCourses.length;
  const completedModules = allCourses.filter(course => {
    const progress = userProgress[course.id];
    return progress && progress.unlockedSection >= course.sectionsCount;
  }).length;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-lg shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[85vh] overflow-y-auto"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-2 sticky top-0 bg-white dark:bg-zinc-900 z-10">
              <div>
                <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                  Study Passport
                </h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
                  <span className="font-semibold text-zinc-900 dark:text-white">{completedModules}</span>
                  {' '}of {totalModules} stamps collected
                </p>
              </div>
              <button
                onClick={onClose}
                aria-label="Close"
                className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Progress bar */}
            <div className="px-6 pt-2 pb-4">
              <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                <MotionDiv
                  className="h-full bg-[var(--accent-hex)] rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${totalModules > 0 ? (completedModules / totalModules) * 100 : 0}%` }}
                  transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
                />
              </div>
            </div>

            {/* Stamp grid by category */}
            <div className="px-6 pb-6 space-y-6">
              {CATEGORY_ORDER.map(({ key, stampBg, stampRing }) => {
                const categoryCourses = allCourses.filter(c => c.category === key);
                if (categoryCourses.length === 0) return null;

                const categoryComplete = categoryCourses.filter(c => {
                  const p = userProgress[c.id];
                  return p && p.unlockedSection >= c.sectionsCount;
                }).length;

                return (
                  <div key={key}>
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                        {categoryTitles[key]}
                      </h3>
                      <span className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500">
                        {categoryComplete}/{categoryCourses.length}
                      </span>
                    </div>
                    <div className="grid grid-cols-4 sm:grid-cols-6 gap-3">
                      {categoryCourses.map((course, i) => {
                        const progress = userProgress[course.id];
                        const isComplete = progress && progress.unlockedSection >= course.sectionsCount;

                        return (
                          <MotionDiv
                            key={course.id}
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3, delay: i * 0.03 }}
                            className="flex flex-col items-center gap-1.5"
                          >
                            <div
                              className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                                isComplete
                                  ? `${stampBg} text-white ring-4 ${stampRing}`
                                  : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-300 dark:text-zinc-600'
                              }`}
                              title={course.title}
                            >
                              {isComplete ? (
                                <Check size={18} strokeWidth={2.5} />
                              ) : (
                                <Lock size={12} />
                              )}
                            </div>
                            <p className={`text-[9px] font-medium text-center leading-tight line-clamp-2 ${
                              isComplete ? 'text-zinc-700 dark:text-zinc-300' : 'text-zinc-400 dark:text-zinc-600'
                            }`}>
                              {course.title}
                            </p>
                          </MotionDiv>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default StudyPassportModal;
