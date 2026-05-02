/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * LearningPathsView — editorial library of curated module paths.
 *
 * Layout per card: hand-drawn icon → uppercase eyebrow → serif title →
 * italic subtitle → muted description → thin progress line → text-style
 * CTA → quiet expand toggle that reveals the module list. No saturated
 * tiles or numbered badges; accent colours appear only in tiny details
 * (progress fill, terracotta CTA arrow).
 */

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowLeft, Check, ChevronDown } from 'lucide-react';
import { type CourseData } from './Library';
import { LEARNING_PATHS, type LearningPath } from '../learningPaths';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface LearningPathsViewProps {
  allCourses: CourseData[];
  userProgress: UserProgress;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
}

// Editorial metadata layered on top of LEARNING_PATHS — eyebrow label,
// hand-drawn icon path, and a muted accent reserved for tiny details
// (progress fill + CTA arrow). The bright accentHex from learningPaths.ts
// is intentionally overridden — saturated blocks don't fit this surface.
//
// `iconScale` compensates for per-PNG internal padding so all four icons
// read at roughly equal visual weight. exam-prep's content sits in a
// shorter portion of its canvas (wide horizontal layout), so it gets
// scaled up; the others fill their canvas already.
const PATH_META: Record<string, { eyebrow: string; iconPath: string; accent: string; iconScale: number }> = {
  'getting-started':      { eyebrow: 'Foundation Path', iconPath: '/assets/learning-paths/getting-started.png', accent: '#5B7DB0', iconScale: 1.0  },
  'exam-prep-sprint':     { eyebrow: 'Exam Path',       iconPath: '/assets/learning-paths/exam-prep.png',     accent: '#D85F47', iconScale: 1.35 },
  'build-your-mindset':   { eyebrow: 'Mindset Path',    iconPath: '/assets/learning-paths/mindset.png',       accent: '#8B82B8', iconScale: 1.0  },
  'master-your-learning': { eyebrow: 'Learning Path',   iconPath: '/assets/learning-paths/master-learning.png', accent: '#7DA37A', iconScale: 1.0 },
};

const SERIF: React.CSSProperties = { fontFamily: "'Source Serif 4', serif" };
const SANS: React.CSSProperties = { fontFamily: "'DM Sans', system-ui, sans-serif" };

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
    return p && p.unlockedSection >= course.sectionsCount;
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
    <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950 pt-16 md:pt-20 pb-32 px-4 sm:px-6 transition-colors duration-500">
      <div className="max-w-5xl mx-auto">
        {/* ── Header row: back arrow + serif title ── */}
        <div className="flex items-center gap-4 mb-12">
          <button
            onClick={onBack}
            aria-label="Back"
            className="w-10 h-10 rounded-xl flex items-center justify-center bg-white border border-[#EDEBE8] hover:bg-[#F8F4EC] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(42,125,111,0.35)]"
            style={{ boxShadow: '0 1px 2px rgba(28,25,23,0.04)' }}
          >
            <ArrowLeft size={18} className="text-[#1a1a1a]" />
          </button>
          <h1
            style={{
              ...SERIF,
              fontSize: 'clamp(32px, 5vw, 44px)',
              fontWeight: 500,
              letterSpacing: '-0.6px',
              color: '#1a1a1a',
              margin: 0,
              lineHeight: 1.05,
            }}
          >
            Learning Paths
          </h1>
        </div>

        {/* ── Card grid ── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
          {LEARNING_PATHS.map((path, i) => {
            const meta = PATH_META[path.id] ?? { eyebrow: 'Path', iconPath: '/assets/worlds/learn-book.png', accent: '#7DA37A', iconScale: 1.0 };
            const completed = path.moduleIds.filter(id => isModuleComplete(id)).length;
            const total = path.moduleIds.length;
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            const isExpanded = expandedPathId === path.id;
            const firstIncomplete = getFirstIncomplete(path);
            const isComplete = !firstIncomplete;

            return (
              <MotionDiv
                key={path.id}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.08, ease: [0.16, 1, 0.3, 1] as number[] }}
                className="overflow-hidden"
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E8E2D8',
                  borderRadius: 22,
                  boxShadow: '0 4px 28px rgba(28,25,23,0.06), 0 1px 3px rgba(28,25,23,0.04)',
                }}
              >
                <div className="p-7 md:p-8">
                  {/* Hand-drawn icon — naked PNG, no tile, no blob.
                      Per-path iconScale compensates for varying internal
                      padding so all four icons read at the same weight. */}
                  <div className="relative" style={{ width: 56, height: 56, marginBottom: 18 }}>
                    <img
                      src={meta.iconPath}
                      alt=""
                      style={{
                        position: 'absolute',
                        left: '50%',
                        top: '50%',
                        transform: `translate(-50%, -50%) scale(${meta.iconScale})`,
                        width: '100%',
                        height: '100%',
                        objectFit: 'contain',
                      }}
                      draggable={false}
                    />
                  </div>

                  {/* Eyebrow */}
                  <p
                    className="uppercase"
                    style={{
                      ...SANS,
                      fontSize: 11,
                      fontWeight: 500,
                      letterSpacing: '1.6px',
                      color: 'rgba(0,0,0,0.45)',
                      margin: 0,
                    }}
                  >
                    {meta.eyebrow}
                  </p>

                  {/* Title */}
                  <h3
                    style={{
                      ...SERIF,
                      fontSize: 24,
                      fontWeight: 500,
                      letterSpacing: '-0.4px',
                      color: '#1a1a1a',
                      margin: 0,
                      marginTop: 8,
                      lineHeight: 1.15,
                    }}
                  >
                    {path.title}
                  </h3>

                  {/* Subtitle (italic) */}
                  <p
                    style={{
                      ...SERIF,
                      fontStyle: 'italic',
                      fontSize: 14,
                      color: 'rgba(0,0,0,0.55)',
                      margin: 0,
                      marginTop: 6,
                    }}
                  >
                    {path.subtitle}
                  </p>

                  {/* Description */}
                  <p
                    style={{
                      ...SANS,
                      fontSize: 14,
                      lineHeight: 1.55,
                      color: 'rgba(0,0,0,0.6)',
                      margin: 0,
                      marginTop: 14,
                    }}
                  >
                    {path.description}
                  </p>

                  {/* Progress — thin muted track + restrained accent fill */}
                  <div className="flex items-center gap-3" style={{ marginTop: 22 }}>
                    <div
                      className="flex-1 overflow-hidden"
                      style={{ height: 2, borderRadius: 999, background: 'rgba(0,0,0,0.08)' }}
                    >
                      <MotionDiv
                        style={{ height: '100%', borderRadius: 999, background: meta.accent, opacity: 0.85 }}
                        initial={{ width: 0 }}
                        animate={{ width: `${pct}%` }}
                        transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
                      />
                    </div>
                    <span
                      style={{
                        ...SANS,
                        fontSize: 12,
                        color: 'rgba(0,0,0,0.5)',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {completed} / {total} complete
                    </span>
                  </div>

                  {/* CTA row — text-style continue/start + subtle expand */}
                  <div className="flex items-center justify-between" style={{ marginTop: 22 }}>
                    {isComplete ? (
                      <span
                        className="inline-flex items-center gap-1.5"
                        style={{
                          ...SANS,
                          fontSize: 13,
                          fontWeight: 500,
                          color: meta.accent,
                        }}
                      >
                        <Check size={14} strokeWidth={2} />
                        Path complete
                      </span>
                    ) : (
                      <button
                        onClick={() => firstIncomplete && onSelectModule(firstIncomplete)}
                        className="group inline-flex items-center gap-1.5 transition-colors hover:opacity-80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(42,125,111,0.35)] rounded-md"
                        style={{
                          ...SANS,
                          fontSize: 14,
                          fontWeight: 500,
                          color: '#1a1a1a',
                        }}
                      >
                        {completed > 0 ? 'Continue' : 'Start'}
                        <span
                          className="transition-transform group-hover:translate-x-0.5"
                          style={{ color: meta.accent, fontSize: 16, lineHeight: 1 }}
                        >
                          →
                        </span>
                      </button>
                    )}

                    <button
                      onClick={() => setExpandedPathId(isExpanded ? null : path.id)}
                      className="inline-flex items-center gap-1.5 transition-colors hover:opacity-80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(42,125,111,0.35)] rounded-md"
                      style={{
                        ...SANS,
                        fontSize: 12,
                        color: 'rgba(0,0,0,0.5)',
                      }}
                      aria-expanded={isExpanded}
                    >
                      {isExpanded ? 'Hide modules' : 'View modules'}
                      <ChevronDown
                        size={14}
                        strokeWidth={1.6}
                        className={`transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
                      />
                    </button>
                  </div>
                </div>

                {/* Expanded module list — quiet hairline divider, plain rows */}
                <AnimatePresence>
                  {isExpanded && (
                    <MotionDiv
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] as number[] }}
                      className="overflow-hidden"
                    >
                      <div
                        className="px-7 md:px-8 py-5"
                        style={{ borderTop: '1px solid rgba(0,0,0,0.06)' }}
                      >
                        <ul className="space-y-1">
                          {path.moduleIds.map((moduleId, idx) => {
                            const done = isModuleComplete(moduleId);
                            return (
                              <li key={moduleId}>
                                <button
                                  onClick={() => onSelectModule(moduleId)}
                                  className="w-full flex items-center gap-3 py-2 px-2 rounded-lg hover:bg-[#F4EFE5] transition-colors text-left group"
                                >
                                  {/* Tiny status dot — accent for done, muted for pending */}
                                  <span
                                    className="shrink-0 inline-flex items-center justify-center"
                                    style={{
                                      width: 18,
                                      height: 18,
                                      borderRadius: 999,
                                      background: done ? meta.accent : 'transparent',
                                      border: done ? 'none' : '1px solid rgba(0,0,0,0.18)',
                                      color: done ? '#fff' : 'rgba(0,0,0,0.4)',
                                      fontSize: 10,
                                      fontWeight: 600,
                                      ...SANS,
                                    }}
                                  >
                                    {done ? <Check size={11} strokeWidth={2.5} /> : idx + 1}
                                  </span>
                                  <span
                                    style={{
                                      ...SANS,
                                      fontSize: 14,
                                      color: done ? 'rgba(0,0,0,0.4)' : 'rgba(0,0,0,0.78)',
                                      textDecoration: done ? 'line-through' : 'none',
                                    }}
                                  >
                                    {getModuleTitle(moduleId)}
                                  </span>
                                  <span
                                    className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity"
                                    style={{ ...SANS, fontSize: 14, color: meta.accent }}
                                  >
                                    →
                                  </span>
                                </button>
                              </li>
                            );
                          })}
                        </ul>
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
