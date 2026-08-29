/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { X, Check, Lock, ChevronDown } from 'lucide-react';
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
  onSelectModule?: (moduleId: string) => void;
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
  onSelectModule,
}) => {
  useModal(isOpen, onClose);
  const [filter, setFilter] = useState<'all' | 'remaining' | 'complete'>('all');
  const [openCategories, setOpenCategories] = useState<Set<CategoryType>>(() => new Set(['architecture-mindset']));
  const totalModules = allCourses.length;
  const completedModules = allCourses.filter(course => {
    const progress = userProgress[course.id];
    return progress && progress.unlockedSection >= course.sectionsCount;
  }).length;
  const titleCounts = useMemo(() => {
    const counts = new Map<string, number>();
    allCourses.forEach(course => counts.set(course.title, (counts.get(course.title) ?? 0) + 1));
    return counts;
  }, [allCourses]);

  const toggleCategory = (category: CategoryType) => {
    setOpenCategories(current => {
      const next = new Set(current);
      if (next.has(category)) next.delete(category);
      else next.add(category);
      return next;
    });
  };

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="theme-compat fixed inset-0 bg-[#1A1A1A]/55 flex items-end sm:items-center justify-center z-[200] p-0 sm:p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            role="dialog"
            aria-modal="true"
            aria-labelledby="study-passport-title"
            tabIndex={-1}
            className="relative bg-[#FAFBF6] dark:bg-zinc-900 border-[1.5px] border-[#383838] dark:border-zinc-600 rounded-t-[24px] sm:rounded-[24px] w-full max-w-lg shadow-[5px_5px_0_0_#383838] overflow-hidden max-h-[92dvh] overflow-y-auto"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-4 sticky top-0 bg-[#FAFBF6] dark:bg-zinc-900 z-10 border-b border-[#DDD8D2] dark:border-zinc-700">
              <div>
                <h2 id="study-passport-title" className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white tracking-tight">
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
                className="flex h-9 w-9 items-center justify-center rounded-xl border border-[#CFC9C2] bg-white text-[#6F6861] transition-colors hover:border-[#383838] hover:text-[#1A1A1A] dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300"
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
              <div className="mt-4 flex rounded-xl border border-[#DDD8D2] bg-white p-1 dark:border-zinc-700 dark:bg-zinc-800" role="group" aria-label="Filter passport stamps">
                {([
                  ['all', 'All'],
                  ['remaining', 'Remaining'],
                  ['complete', 'Complete'],
                ] as const).map(([id, label]) => (
                  <button
                    key={id}
                    type="button"
                    aria-pressed={filter === id}
                    onClick={() => setFilter(id)}
                    className={`min-h-9 flex-1 rounded-lg px-2 text-[11px] font-semibold ${filter === id ? 'bg-[#1A1A1A] text-white dark:bg-white dark:text-zinc-900' : 'text-zinc-500 dark:text-zinc-400'}`}
                  >
                    {label}
                  </button>
                ))}
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
                const visibleCourses = categoryCourses.filter(course => {
                  const progress = userProgress[course.id];
                  const complete = Boolean(progress && progress.unlockedSection >= course.sectionsCount);
                  return filter === 'all' || (filter === 'complete' ? complete : !complete);
                });
                const isExpanded = openCategories.has(key);

                return (
                  <div key={key}>
                    <button
                      type="button"
                      onClick={() => toggleCategory(key)}
                      aria-expanded={isExpanded}
                      className="mb-3 flex min-h-11 w-full items-center justify-between rounded-xl px-2 text-left hover:bg-white dark:hover:bg-zinc-800"
                    >
                      <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-500 dark:text-zinc-400">{categoryTitles[key]}</h3>
                      <span className="flex items-center gap-2 text-[10px] font-bold text-zinc-400 dark:text-zinc-500">
                        {categoryComplete}/{categoryCourses.length}
                        <ChevronDown size={15} className={`transition-transform ${isExpanded ? 'rotate-180' : ''}`} aria-hidden="true" />
                      </span>
                    </button>
                    {isExpanded && (visibleCourses.length > 0 ? <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                      {visibleCourses.map((course, i) => {
                        const progress = userProgress[course.id];
                        const isComplete = progress && progress.unlockedSection >= course.sectionsCount;
                        const displayTitle = (titleCounts.get(course.title) ?? 0) > 1 && course.subtitle
                          ? `${course.title} · ${course.subtitle}`
                          : course.title;

                        return (
                          <MotionDiv
                            key={course.id}
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3, delay: i * 0.03 }}
                            className="min-w-0"
                          >
                            <button
                              type="button"
                              onClick={() => { onClose(); onSelectModule?.(course.id); }}
                              aria-label={`Open ${displayTitle}`}
                              className="flex h-full w-full min-w-0 items-center gap-2.5 rounded-xl border border-[#E2DDD6] bg-white px-2.5 py-2.5 text-left transition-colors hover:border-[#383838] dark:border-zinc-700 dark:bg-zinc-800 dark:hover:border-zinc-500"
                            >
                            <div
                              className={`h-9 w-9 shrink-0 rounded-full flex items-center justify-center transition-all ${
                                isComplete
                                  ? `${stampBg} text-white ring-4 ${stampRing}`
                                  : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-300 dark:text-zinc-600'
                              }`}
                              title={displayTitle}
                            >
                              {isComplete ? (
                                <Check size={18} strokeWidth={2.5} />
                              ) : (
                                <Lock size={12} />
                              )}
                            </div>
                            <p className={`min-w-0 text-[11px] font-medium leading-snug ${
                              isComplete ? 'text-zinc-700 dark:text-zinc-300' : 'text-zinc-400 dark:text-zinc-600'
                            }`}>
                              {displayTitle}
                            </p>
                            </button>
                          </MotionDiv>
                        );
                      })}
                    </div> : <p className="rounded-xl border border-dashed border-zinc-300 px-4 py-5 text-center text-xs text-zinc-400 dark:border-zinc-700">No {filter === 'complete' ? 'completed' : 'remaining'} stamps in this world.</p>)}
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
