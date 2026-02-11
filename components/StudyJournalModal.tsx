/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, BookOpen, Target, RotateCcw, Star, BookMarked } from 'lucide-react';
import { type StudyReflection } from '../types';

const MotionDiv = motion.div as any;

const SESSION_ICONS: Record<string, React.ElementType> = {
  'new-learning': BookOpen,
  'practice': Target,
  'revision': RotateCcw,
};

const SESSION_LABELS: Record<string, string> = {
  'new-learning': 'New Learning',
  'practice': 'Practice',
  'revision': 'Revision',
};

interface StudyJournalModalProps {
  isOpen: boolean;
  onClose: () => void;
  reflections: StudyReflection[];
}

const StudyJournalModal: React.FC<StudyJournalModalProps> = ({ isOpen, onClose, reflections }) => {
  const [subjectFilter, setSubjectFilter] = useState<string | null>(null);

  const subjects = useMemo(() => {
    const set = new Set(reflections.map(r => r.subjectName));
    return Array.from(set).sort();
  }, [reflections]);

  const filtered = useMemo(() => {
    const list = subjectFilter
      ? reflections.filter(r => r.subjectName === subjectFilter)
      : reflections;
    return [...list].sort((a, b) => b.timestamp - a.timestamp);
  }, [reflections, subjectFilter]);

  // Group by dateKey
  const grouped = useMemo(() => {
    const map = new Map<string, StudyReflection[]>();
    for (const r of filtered) {
      const existing = map.get(r.dateKey) || [];
      existing.push(r);
      map.set(r.dateKey, existing);
    }
    return Array.from(map.entries());
  }, [filtered]);

  const formatDate = (dateKey: string): string => {
    const parts = dateKey.split('-');
    const d = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    return d.toLocaleDateString('en-IE', { weekday: 'short', month: 'short', day: 'numeric' });
  };

  const totalPoints = reflections.reduce((sum, r) => sum + r.pointsEarned, 0);

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
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-lg shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[85vh] flex flex-col"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-4 flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center">
                  <BookMarked size={20} className="text-indigo-600 dark:text-indigo-400" />
                </div>
                <div>
                  <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                    Study Journal
                  </h2>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">
                    {reflections.length} reflections &middot; {totalPoints} pts earned
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Filter chips */}
            {subjects.length > 1 && (
              <div className="px-6 pb-3 flex-shrink-0">
                <div className="flex flex-wrap gap-1.5">
                  <button
                    onClick={() => setSubjectFilter(null)}
                    className={`px-2.5 py-1 rounded-full text-[10px] font-bold transition-all ${
                      !subjectFilter
                        ? 'bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 ring-1 ring-indigo-300 dark:ring-indigo-600'
                        : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                    }`}
                  >
                    All
                  </button>
                  {subjects.map(s => (
                    <button
                      key={s}
                      onClick={() => setSubjectFilter(subjectFilter === s ? null : s)}
                      className={`px-2.5 py-1 rounded-full text-[10px] font-bold transition-all ${
                        subjectFilter === s
                          ? 'bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 ring-1 ring-indigo-300 dark:ring-indigo-600'
                          : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Content */}
            <div className="flex-1 overflow-y-auto px-6 pb-6">
              {grouped.length === 0 ? (
                <div className="text-center py-16">
                  <BookMarked size={32} className="text-zinc-300 dark:text-zinc-600 mx-auto mb-3" />
                  <p className="text-sm font-semibold text-zinc-400 dark:text-zinc-500">No reflections yet</p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">
                    Complete study sessions to build your journal.
                  </p>
                </div>
              ) : (
                <div className="space-y-5">
                  {grouped.map(([dateKey, entries]) => (
                    <div key={dateKey}>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">
                        {formatDate(dateKey)}
                      </p>
                      <div className="space-y-2">
                        {entries.map((entry, i) => {
                          const Icon = SESSION_ICONS[entry.sessionType] || BookOpen;
                          return (
                            <div
                              key={`${entry.blockId}-${i}`}
                              className="p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]"
                            >
                              <div className="flex items-center justify-between mb-1.5">
                                <div className="flex items-center gap-2">
                                  <Icon size={12} className="text-zinc-400 dark:text-zinc-500 flex-shrink-0" />
                                  <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">{entry.subjectName}</span>
                                  <span className="text-[9px] text-zinc-400 dark:text-zinc-500">{SESSION_LABELS[entry.sessionType]}</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <Star size={10} className="text-amber-500" />
                                  <span className="text-[10px] font-bold text-amber-600 dark:text-amber-400">+{entry.pointsEarned}</span>
                                </div>
                              </div>
                              <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">{entry.reflection}</p>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default StudyJournalModal;
