/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * CategoryJourney — stacking card deck with 3D depth.
 *
 * Cards stack as you scroll, with previous cards shrinking and offsetting
 * so 2-3 are always visible behind the current one (like a fanned deck).
 * Each card has a thick bottom/right shadow border for tactile depth.
 * No emojis. Compact hero. Dense, beautiful cards.
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Check, Clock, ChevronDown, Sparkles } from 'lucide-react';
import { type CourseData } from './Library';
import { type UserProgress } from '../types';

const MotionDiv = motion.div as any;
const EASE = [0.16, 1, 0.3, 1] as number[];
const SERIF = "'Source Serif 4', serif";

// ── Unique SVG backgrounds — abstract, architectural, no emojis ──

const CARD_SHAPES: React.ReactNode[] = [
  /* 01 */ <><circle cx="420" cy="140" r="200" fill="rgba(42,125,111,0.04)" /><circle cx="420" cy="140" r="120" fill="rgba(42,125,111,0.03)" /></>,
  /* 02 */ <><path d="M350 0 Q500 200 350 400" stroke="rgba(42,125,111,0.06)" strokeWidth="1.5" fill="none" /><path d="M380 0 Q530 200 380 400" stroke="rgba(42,125,111,0.04)" strokeWidth="1.5" fill="none" /></>,
  /* 03 */ <><rect x="320" y="60" width="220" height="280" rx="110" fill="rgba(42,125,111,0.035)" transform="rotate(-15 430 200)" /></>,
  /* 04 */ <><circle cx="450" cy="200" r="160" fill="none" stroke="rgba(42,125,111,0.05)" strokeWidth="1" /><circle cx="450" cy="200" r="100" fill="none" stroke="rgba(42,125,111,0.04)" strokeWidth="1" /><circle cx="450" cy="200" r="40" fill="rgba(42,125,111,0.04)" /></>,
  /* 05 */ <><path d="M300 50 L550 200 L300 350 Z" fill="rgba(42,125,111,0.03)" stroke="rgba(42,125,111,0.04)" strokeWidth="1" /></>,
  /* 06 */ <><ellipse cx="430" cy="200" rx="180" ry="120" fill="rgba(42,125,111,0.035)" transform="rotate(20 430 200)" /></>,
  /* 07 */ <><line x1="300" y1="0" x2="550" y2="400" stroke="rgba(42,125,111,0.04)" strokeWidth="60" strokeLinecap="round" /><line x1="550" y1="0" x2="300" y2="400" stroke="rgba(42,125,111,0.03)" strokeWidth="40" strokeLinecap="round" /></>,
  /* 08 */ <><rect x="340" y="80" width="160" height="240" rx="6" fill="rgba(42,125,111,0.03)" /><rect x="370" y="110" width="160" height="200" rx="6" fill="rgba(42,125,111,0.03)" /></>,
  /* 09 */ <><path d="M320 200 Q420 60 520 200 Q420 340 320 200Z" fill="rgba(42,125,111,0.04)" /></>,
  /* 10 */ <><path d="M300 300 Q400 100 500 300" fill="none" stroke="rgba(42,125,111,0.05)" strokeWidth="2" /><path d="M300 320 Q400 120 500 320" fill="none" stroke="rgba(42,125,111,0.04)" strokeWidth="2" /><path d="M300 340 Q400 140 500 340" fill="none" stroke="rgba(42,125,111,0.03)" strokeWidth="2" /></>,
  /* 11 */ <><polygon points="430,60 530,180 490,320 370,320 330,180" fill="rgba(42,125,111,0.03)" stroke="rgba(42,125,111,0.04)" strokeWidth="1" /></>,
  /* 12 */ <><circle cx="380" cy="150" r="80" fill="rgba(42,125,111,0.03)" /><circle cx="470" cy="250" r="80" fill="rgba(42,125,111,0.035)" /><circle cx="360" cy="280" r="60" fill="rgba(42,125,111,0.03)" /></>,
  /* 13 */ <><circle cx="430" cy="200" r="130" fill="rgba(42,125,111,0.04)" /><line x1="430" y1="70" x2="430" y2="330" stroke="rgba(42,125,111,0.05)" strokeWidth="1" /><line x1="300" y1="200" x2="560" y2="200" stroke="rgba(42,125,111,0.05)" strokeWidth="1" /></>,
];

// ── Scroll-driven stacking card ────────────────────────────

interface StackCardProps {
  course: CourseData;
  index: number;
  total: number;
  isCompleted: boolean;
  isStarted: boolean;
  progressPct: number;
  isRecommended: boolean;
  onSelect: () => void;
}

const StackCard: React.FC<StackCardProps> = ({
  course, index, total, isCompleted, isStarted, progressPct, isRecommended, onSelect,
}) => {
  const num = String(index + 1).padStart(2, '0');
  const shapes = CARD_SHAPES[index % CARD_SHAPES.length];

  return (
    <div
      className="sticky flex items-center justify-center px-4 md:px-8"
      style={{
        top: 12 + index * 6,
        zIndex: index + 1,
        height: 'auto',
        paddingTop: index === 0 ? 8 : 4,
        paddingBottom: 4,
      }}
    >
      <div
        onClick={onSelect}
        className="relative w-full max-w-lg overflow-hidden cursor-pointer group transition-shadow duration-300 hover:shadow-[0_12px_40px_rgba(0,0,0,0.08)]"
        style={{
          borderRadius: 20,
          backgroundColor: '#FAF7F4',
          boxShadow: '4px 5px 0 0 #d6d0c8, 0 2px 12px rgba(0,0,0,0.04)',
          border: '1.5px solid #e8e3dc',
        }}
      >
        {/* SVG background art */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 600 400" preserveAspectRatio="xMaxYMid slice">
          {shapes}
        </svg>

        <div className="relative z-10 p-6 md:p-8">
          {/* Top row: status + counter */}
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-3">
              {isCompleted ? (
                <div className="w-7 h-7 rounded-full flex items-center justify-center" style={{ backgroundColor: '#2A7D6F' }}>
                  <Check size={13} color="white" strokeWidth={2.5} />
                </div>
              ) : isRecommended ? (
                <div className="relative">
                  <div className="w-7 h-7 rounded-full flex items-center justify-center" style={{ border: '2px solid #2A7D6F' }}>
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#2A7D6F' }} />
                  </div>
                </div>
              ) : (
                <div className="w-7 h-7 rounded-full border-2 border-zinc-300" />
              )}
              <span className="text-sm font-medium tabular-nums" style={{ color: '#a09a8f' }}>
                {num} <span className="text-zinc-300">/</span> {total}
              </span>
            </div>

            {isRecommended && (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full" style={{ backgroundColor: 'rgba(42,125,111,0.08)' }}>
                <Sparkles size={11} style={{ color: '#2A7D6F' }} />
                <span className="text-[10px] font-semibold" style={{ color: '#2A7D6F' }}>Up next</span>
              </div>
            )}

            {isCompleted && (
              <span className="text-[11px] font-medium" style={{ color: '#2A7D6F' }}>Complete</span>
            )}
          </div>

          {/* Subtitle */}
          <p className="text-[10px] font-semibold uppercase tracking-[0.1em] mb-1.5" style={{ color: '#b5b0a5' }}>
            {course.subtitle}
          </p>

          {/* Title */}
          <h2
            className="mb-3 group-hover:translate-x-0.5 transition-transform duration-200"
            style={{ fontFamily: SERIF, fontSize: 24, fontWeight: 600, color: '#1a1a1a', lineHeight: 1.25 }}
          >
            {course.title}
          </h2>

          {/* Description */}
          <p className="text-[13px] leading-relaxed mb-5" style={{ color: '#78716c' }}>
            {course.description}
          </p>

          {/* Progress bar */}
          {isStarted && !isCompleted && (
            <div className="mb-5">
              <div className="w-full h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: 'rgba(42,125,111,0.08)' }}>
                <div className="h-full rounded-full" style={{ width: `${progressPct}%`, backgroundColor: '#2A7D6F', transition: 'width 0.6s ease-out' }} />
              </div>
              <p className="text-[10px] font-semibold mt-1.5" style={{ color: '#2A7D6F' }}>{progressPct}%</p>
            </div>
          )}

          {/* Bottom row */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-[12px]" style={{ color: '#a09a8f' }}>
              <span className="flex items-center gap-1"><Clock size={12} /> ~20 min</span>
              <span>{course.sectionsCount} sections</span>
            </div>

            <div
              className="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-150 active:scale-[0.96] group-hover:gap-3"
              style={{
                backgroundColor: isCompleted ? 'transparent' : '#2A7D6F',
                color: isCompleted ? '#2A7D6F' : 'white',
                border: isCompleted ? '1.5px solid rgba(42,125,111,0.25)' : '1.5px solid #2A7D6F',
                boxShadow: isCompleted ? 'none' : '2px 3px 0 0 #1F5F54',
              }}
            >
              {isCompleted ? 'Review' : isStarted ? 'Continue' : 'Start'}
              <ArrowRight size={14} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ── Main Component ──────────────────────────────────────────

interface CategoryJourneyProps {
  title: string;
  courses: CourseData[];
  onSelectCourse: (courseId: string) => void;
  onBack: () => void;
  userProgress: UserProgress;
}

const CategoryJourney: React.FC<CategoryJourneyProps> = ({
  title, courses, onSelectCourse, onBack, userProgress,
}) => {
  const moduleStates = useMemo(() => {
    let foundRecommended = false;
    return courses.map((course) => {
      const progress = userProgress[course.id];
      const sections = course.sectionsCount;
      const unlocked = progress?.unlockedSection ?? 0;
      const isCompleted = unlocked >= sections;
      const isStarted = unlocked > 0;
      const pct = sections > 0 ? Math.round((unlocked / sections) * 100) : 0;
      let isRecommended = false;
      if (!isCompleted && !foundRecommended) {
        isRecommended = true;
        foundRecommended = true;
      }
      return { course, isCompleted, isStarted, progressPct: pct, isRecommended };
    });
  }, [courses, userProgress]);

  const completedCount = moduleStates.filter(m => m.isCompleted).length;
  const totalCount = moduleStates.length;

  return (
    <div className="bg-zinc-50 dark:bg-zinc-950">
      {/* ═══ COMPACT HERO ═══ */}
      <div className="relative px-6 pt-16 pb-8 text-center">
        {/* Back */}
        <button
          onClick={onBack}
          className="absolute top-4 left-4 w-10 h-10 rounded-xl bg-white/80 backdrop-blur-sm flex items-center justify-center hover:bg-white transition-colors z-10"
          style={{ border: '0.5px solid rgba(0,0,0,0.08)' }}
        >
          <ArrowLeft size={18} className="text-zinc-600" />
        </button>

        {/* Progress counter */}
        <MotionDiv
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: EASE }}
          className="flex items-baseline justify-center gap-1 mb-3"
        >
          <span className="font-apercu text-3xl font-bold" style={{ color: '#2A7D6F' }}>{completedCount}</span>
          <span className="text-base text-zinc-300">/</span>
          <span className="font-apercu text-base text-zinc-400">{totalCount}</span>
        </MotionDiv>

        {/* Title */}
        <MotionDiv
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1, ease: EASE }}
        >
          <h1 style={{ fontFamily: SERIF, fontSize: 28, fontWeight: 600, color: '#1a1a1a', lineHeight: 1.2 }}>
            {title}
          </h1>
        </MotionDiv>

        {/* Segmented progress */}
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="flex justify-center gap-1 mt-4 mb-2"
        >
          {moduleStates.map((m, i) => (
            <div
              key={i}
              className="rounded-full"
              style={{
                width: 4,
                height: m.isRecommended ? 20 : 14,
                backgroundColor: m.isCompleted ? '#2A7D6F' : m.isRecommended ? 'rgba(42,125,111,0.3)' : '#e0dbd2',
                transition: 'all 0.4s',
              }}
            />
          ))}
        </MotionDiv>

        <MotionDiv
          animate={{ y: [0, 4, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          className="mt-4"
        >
          <ChevronDown size={16} className="mx-auto text-zinc-300" />
        </MotionDiv>
      </div>

      {/* ═══ STACKING CARD DECK ═══ */}
      <div className="pb-40">
        {moduleStates.map((m, i) => (
          <StackCard
            key={m.course.id}
            course={m.course}
            index={i}
            total={totalCount}
            isCompleted={m.isCompleted}
            isStarted={m.isStarted}
            progressPct={m.progressPct}
            isRecommended={m.isRecommended}
            onSelect={() => onSelectCourse(m.course.id)}
          />
        ))}
      </div>

      {/* ═══ FOOTER ═══ */}
      <div className="text-center pb-20 px-6">
        <p className="text-xs" style={{ color: '#b5b0a5', fontFamily: SERIF, fontStyle: 'italic' }}>
          {completedCount === totalCount
            ? 'You\'ve built the architecture. Now build on it.'
            : `${totalCount - completedCount} to go — no rush, no barriers.`}
        </p>
      </div>

      <style>{`
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
          }
        }
      `}</style>
    </div>
  );
};

export default CategoryJourney;
