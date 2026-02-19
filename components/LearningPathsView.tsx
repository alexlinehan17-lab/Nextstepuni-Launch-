/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Check, ChevronRight, ChevronDown } from 'lucide-react';
import { CourseData } from './Library';
import { LEARNING_PATHS, LearningPath } from '../learningPaths';

const MotionDiv = motion.div as any;

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface LearningPathsViewProps {
  allCourses: CourseData[];
  userProgress: UserProgress;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
}

const LearningPathsView: React.FC<LearningPathsViewProps> = ({
  allCourses,
  userProgress,
  onSelectModule,
  onBack,
}) => {
  const [expandedPathId, setExpandedPathId] = useState<string | null>(null);

  const isModuleComplete = (moduleId: string) => {
    const course = allCourses.find(c => c.id === moduleId);
    if (!course) return false;
    const p = userProgress[moduleId];
    return p && p.unlockedSection >= course.sectionsCount - 1;
  };

  const getFirstIncomplete = (path: LearningPath): string | null => {
    for (const id of path.moduleIds) {
      if (!isModuleComplete(id)) return id;
    }
    return null;
  };

  const getModuleTitle = (moduleId: string): string => {
    const course = allCourses.find(c => c.id === moduleId);
    return course?.title ?? moduleId;
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 pt-16 md:pt-24 pb-40 md:pb-32 px-4 sm:px-6 transition-colors duration-500">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-10">
          <button
            onClick={onBack}
            className="w-10 h-10 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-zinc-500 hover:text-zinc-900 dark:hover:text-white transition-colors"
          >
            <ArrowLeft size={18} />
          </button>
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-zinc-900 dark:text-white tracking-tight">
            Learning Paths
          </h1>
        </div>

        {/* Path cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {LEARNING_PATHS.map((path, i) => {
            const completed = path.moduleIds.filter(id => isModuleComplete(id)).length;
            const total = path.moduleIds.length;
            const pct = Math.round((completed / total) * 100);
            const isExpanded = expandedPathId === path.id;
            const firstIncomplete = getFirstIncomplete(path);

            return (
              <MotionDiv
                key={path.id}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden"
              >
                <div className="p-6">
                  {/* Icon + title */}
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center mb-4"
                    style={{ backgroundColor: path.accentHex + '15', color: path.accentHex }}
                  >
                    <span className="text-lg font-bold">{i + 1}</span>
                  </div>
                  <h3 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">{path.title}</h3>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1 mb-3">{path.subtitle}</p>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed mb-5">{path.description}</p>

                  {/* Progress bar */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className="flex-1 h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                      <MotionDiv
                        className="h-full rounded-full"
                        style={{ backgroundColor: path.accentHex }}
                        initial={{ width: 0 }}
                        animate={{ width: `${pct}%` }}
                        transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
                      />
                    </div>
                    <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500 shrink-0">{completed}/{total}</span>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    {firstIncomplete ? (
                      <button
                        onClick={() => onSelectModule(firstIncomplete)}
                        className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium text-white transition-colors"
                        style={{ backgroundColor: path.accentHex }}
                      >
                        {completed > 0 ? 'Continue' : 'Start'}
                        <ChevronRight size={14} />
                      </button>
                    ) : (
                      <div className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400">
                        <Check size={14} /> Completed
                      </div>
                    )}
                    <button
                      onClick={() => setExpandedPathId(isExpanded ? null : path.id)}
                      className="w-10 h-10 rounded-lg border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                    >
                      <ChevronDown size={16} className={`transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`} />
                    </button>
                  </div>
                </div>

                {/* Expanded module list */}
                <AnimatePresence>
                  {isExpanded && (
                    <MotionDiv
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.25 }}
                      className="overflow-hidden"
                    >
                      <div className="border-t border-zinc-100 dark:border-zinc-800 px-6 py-4 space-y-1">
                        {path.moduleIds.map((moduleId, idx) => {
                          const done = isModuleComplete(moduleId);
                          return (
                            <button
                              key={moduleId}
                              onClick={() => onSelectModule(moduleId)}
                              className="w-full flex items-center gap-3 py-2 px-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors group text-left"
                            >
                              <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-xs font-bold ${
                                done
                                  ? 'text-white'
                                  : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500'
                              }`}
                                style={done ? { backgroundColor: path.accentHex } : undefined}
                              >
                                {done ? <Check size={12} /> : idx + 1}
                              </div>
                              <span className={`text-sm font-medium ${
                                done ? 'text-zinc-400 dark:text-zinc-500' : 'text-zinc-700 dark:text-zinc-300'
                              }`}>
                                {getModuleTitle(moduleId)}
                              </span>
                              <ChevronRight size={12} className="ml-auto text-zinc-300 dark:text-zinc-600 group-hover:text-zinc-500 dark:group-hover:text-zinc-400 shrink-0 transition-colors" />
                            </button>
                          );
                        })}
                      </div>
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </MotionDiv>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default LearningPathsView;
