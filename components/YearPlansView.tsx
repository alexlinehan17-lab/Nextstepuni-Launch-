/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * YearPlansView — the year-by-year curriculum, 1st through 6th.
 *
 * Deliberately the same editorial card language as LearningPathsView:
 * eyebrow → serif title → italic subtitle → muted description → thin
 * progress line → text CTA → quiet expand toggle revealing the ordered
 * module list. In place of the hand-drawn PNGs, each card carries a large
 * ghost serif year numeral.
 */

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Check, ChevronDown } from 'lucide-react';
import PageHeader from './ui/PageHeader';
import { type CourseData } from './Library';
import { YEAR_PLANS, type YearPlan } from '../yearPlans';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface YearPlansViewProps {
  allCourses: CourseData[];
  userProgress: UserProgress;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  /** LCA students see the two LCA year plans instead of the six LC/JC years. */
  isLca?: boolean;
}

// Muted per-cycle accents in the LearningPathsView register — tiny details
// only (progress fill, CTA arrow, ghost numeral).
const CYCLE_META: Record<YearPlan['cycle'], { eyebrow: string; accent: string }> = {
  junior: { eyebrow: 'Junior Cycle', accent: '#5B7DB0' },
  ty: { eyebrow: 'Transition Year', accent: '#8B82B8' },
  senior: { eyebrow: 'Senior Cycle', accent: '#D85F47' },
  lca: { eyebrow: 'Leaving Cert Applied', accent: '#7DA37A' },
};

const SERIF: React.CSSProperties = { fontFamily: "'Source Serif 4', serif" };
const SANS: React.CSSProperties = { fontFamily: "'DM Sans', system-ui, sans-serif" };

const YearPlansView: React.FC<YearPlansViewProps> = ({
  allCourses,
  userProgress,
  onSelectModule,
  onBack,
  isLca = false,
}) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const plans = YEAR_PLANS.filter(p => (isLca ? p.cycle === 'lca' : p.cycle !== 'lca'));

  const isModuleComplete = (moduleId: string) => {
    const course = allCourses.find(c => c.id === moduleId);
    if (!course) return false;
    const p = userProgress[moduleId];
    return p && p.unlockedSection >= course.sectionsCount;
  };

  const getFirstIncomplete = (plan: YearPlan): string | null => {
    for (const id of plan.moduleIds) {
      if (!isModuleComplete(id)) return id;
    }
    return null;
  };

  const getModuleTitle = (moduleId: string): string => {
    const course = allCourses.find(c => c.id === moduleId);
    return course?.title ?? moduleId;
  };

  return (
    <div className="min-h-screen theme-compat bg-[#FAFBF6] dark:bg-zinc-950 pt-16 md:pt-20 pb-32 px-4 sm:px-6 transition-colors duration-500">
      <div className="max-w-5xl mx-auto">
        <PageHeader onBack={onBack} eyebrow="Plan ahead" title="Year Plans" className="mb-4" />
        <p
          className="mb-12"
          style={{ ...SANS, fontSize: 14.5, lineHeight: 1.6, color: 'rgba(0,0,0,0.55)', maxWidth: '56ch' }}
        >
          A curated set of modules for every year of secondary school — in the order they teach best. Pick your
          year and work through it; subject-specific modules live in Decoding the Subjects.
        </p>

        {/* ── Card grid ── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
          {plans.map((plan, i) => {
            const meta = CYCLE_META[plan.cycle];
            const completed = plan.moduleIds.filter(id => isModuleComplete(id)).length;
            const total = plan.moduleIds.length;
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            const isExpanded = expandedId === plan.id;
            const firstIncomplete = getFirstIncomplete(plan);
            const isComplete = total > 0 && !firstIncomplete;

            return (
              <MotionDiv
                key={plan.id}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.08, ease: [0.16, 1, 0.3, 1] as number[] }}
                className="overflow-hidden relative"
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E8E2D8',
                  borderRadius: 22,
                  boxShadow: '0 4px 28px rgba(28,25,23,0.06), 0 1px 3px rgba(28,25,23,0.04)',
                }}
              >
                {/* Hand-drawn year numeral — upper right, marker-style PNG */}
                <img
                  src={`/assets/year-plans/${plan.year}.png`}
                  alt=""
                  aria-hidden
                  draggable={false}
                  className="absolute pointer-events-none select-none"
                  style={{ top: 14, right: 20, height: 76, width: 'auto' }}
                />

                <div className="p-7 md:p-8">
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
                    {plan.title}
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
                    {plan.subtitle}
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
                    {plan.description}
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
                        style={{ ...SANS, fontSize: 13, fontWeight: 500, color: meta.accent }}
                      >
                        <Check size={14} strokeWidth={2} />
                        Year complete
                      </span>
                    ) : (
                      <button
                        onClick={() => firstIncomplete && onSelectModule(firstIncomplete)}
                        className="group inline-flex items-center gap-1.5 transition-colors hover:opacity-80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(242,107,31,0.35)] rounded-md"
                        style={{ ...SANS, fontSize: 14, fontWeight: 500, color: '#1a1a1a' }}
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
                      onClick={() => setExpandedId(isExpanded ? null : plan.id)}
                      className="inline-flex items-center gap-1.5 transition-colors hover:opacity-80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(242,107,31,0.35)] rounded-md"
                      style={{ ...SANS, fontSize: 12, color: 'rgba(0,0,0,0.5)' }}
                      aria-expanded={isExpanded}
                    >
                      {isExpanded ? 'Hide modules' : `View modules (${total})`}
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
                          {plan.moduleIds.map((moduleId, idx) => {
                            const done = isModuleComplete(moduleId);
                            return (
                              <li key={moduleId}>
                                <button
                                  onClick={() => onSelectModule(moduleId)}
                                  className="w-full flex items-center gap-3 py-2 px-2 rounded-lg hover:bg-[#F4EFE5] transition-colors text-left group"
                                >
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

export default YearPlansView;
