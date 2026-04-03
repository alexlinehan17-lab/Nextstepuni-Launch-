/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { ArrowLeft, ArrowRight, Check } from 'lucide-react';
import { type CourseData } from './Library';
import { type UserProgress } from '../types';

const SERIF = "'Source Serif 4', serif";

// ── Module visual config ───────────────────────────────────

interface VisualConfig {
  pillLabel: string;
  pillBg: string;
  pillText: string;
  tint: string;
  icon?: string; // path to isometric icon PNG
}

// Subtitle-based mapping for architecture-mindset
const SUBTITLE_VISUALS: Record<string, VisualConfig> = {
  'Taking the Wheel of Your Education':   { pillLabel: 'Ownership',   pillBg: '#E6F1FB', pillText: '#185FA5', tint: '#378ADD', icon: '/icons/modules/01-compass.png' },
  "Your Brain's Engineering Manual":      { pillLabel: 'Brain',       pillBg: '#EEEDFE', pillText: '#534AB7', tint: '#7F77DD', icon: '/icons/modules/02-brain.png' },
  'The Psychological Shield':             { pillLabel: 'Shield',      pillBg: '#FAEEDA', pillText: '#854F0B', tint: '#BA7517', icon: '/icons/modules/03-shield.png' },
  'The Future-Proofing Playbook':         { pillLabel: 'Vision',      pillBg: '#EAF3DE', pillText: '#3B6D11', tint: '#639922', icon: '/icons/modules/04-rocket.png' },
  'The Language of Resilience':           { pillLabel: 'Resilience',  pillBg: '#FAECE7', pillText: '#993C1D', tint: '#D85A30', icon: '/icons/modules/05-diamond.png' },
  'The Attribution Retraining Guide':     { pillLabel: 'Attribution', pillBg: '#E1F5EE', pillText: '#0F6E56', tint: '#1D9E75', icon: '/icons/modules/06-target.png' },
  'The Narrative Identity Playbook':      { pillLabel: 'Narrative',   pillBg: '#FBEAF0', pillText: '#993556', tint: '#D4537E', icon: '/icons/modules/07-star.png' },
  'The Architecture of Agency':           { pillLabel: 'Agency',      pillBg: '#EEEDFE', pillText: '#534AB7', tint: '#7F77DD', icon: '/icons/modules/08-lightning.png' },
  'The Architecture of Delay':            { pillLabel: 'Delay',       pillBg: '#F1EFE8', pillText: '#5F5E5A', tint: '#888780', icon: '/icons/modules/09-hourglass.png' },
  'The CBT Toolkit':                      { pillLabel: 'CBT',         pillBg: '#FCEBEB', pillText: '#A32D2D', tint: '#E24B4A', icon: '/icons/modules/10-head.png' },
  'The Stress Management Toolkit':        { pillLabel: 'Stress',      pillBg: '#EAF3DE', pillText: '#3B6D11', tint: '#639922', icon: '/icons/modules/11-heart.png' },
  'The Outcome-Based Approach':           { pillLabel: 'Outcome',     pillBg: '#E6F1FB', pillText: '#185FA5', tint: '#378ADD', icon: '/icons/modules/12-chart.png' },
  'The Intention-Action Blueprint':       { pillLabel: 'Intention',   pillBg: '#EEEDFE', pillText: '#534AB7', tint: '#7F77DD', icon: '/icons/modules/13-checklist.png' },
};

// Tag-based fallback for other categories
const TAG_VISUALS: Record<string, VisualConfig> = {
  'Mindset':            { pillLabel: 'Mindset',       pillBg: '#EEEDFE', pillText: '#534AB7', tint: '#7F77DD' },
  'Motivation':         { pillLabel: 'Motivation',    pillBg: '#E6F1FB', pillText: '#185FA5', tint: '#378ADD' },
  'Brain Science':      { pillLabel: 'Brain Science', pillBg: '#E1F5EE', pillText: '#0F6E56', tint: '#1D9E75' },
  'Resilience':         { pillLabel: 'Resilience',    pillBg: '#FAECE7', pillText: '#993C1D', tint: '#D85A30' },
  'Productivity':       { pillLabel: 'Productivity',  pillBg: '#FAEEDA', pillText: '#854F0B', tint: '#BA7517' },
  'Performance Psych':  { pillLabel: 'Performance',   pillBg: '#EAF3DE', pillText: '#3B6D11', tint: '#639922' },
  'Learning Strategy':  { pillLabel: 'Learning',      pillBg: '#E6F1FB', pillText: '#185FA5', tint: '#378ADD' },
  'Subject Strategy':   { pillLabel: 'Subject',       pillBg: '#FBEAF0', pillText: '#993556', tint: '#D4537E' },
  'Exam Tactics':       { pillLabel: 'Exam Tactics',  pillBg: '#FCEBEB', pillText: '#A32D2D', tint: '#E24B4A' },
  'Points Maximisation': { pillLabel: 'Points',       pillBg: '#FAEEDA', pillText: '#854F0B', tint: '#BA7517' },
  'Creativity':         { pillLabel: 'Creativity',    pillBg: '#EEEDFE', pillText: '#534AB7', tint: '#7F77DD' },
};

const DEFAULT_VIS: VisualConfig = { pillLabel: 'Module', pillBg: '#F1EFE8', pillText: '#5F5E5A', tint: '#888780' };

function getVisual(course: CourseData): VisualConfig {
  if (course.subtitle && SUBTITLE_VISUALS[course.subtitle]) return SUBTITLE_VISUALS[course.subtitle];
  const tag = (course.tags && course.tags.length > 0) ? String(course.tags[0]) : '';
  return TAG_VISUALS[tag] || DEFAULT_VIS;
}


// ── Aurora gradient positions per card ──────────────────────
// Each card gets the login-page aurora gradient but positioned
// differently — bottom-left, top-right, bottom-right, etc.
// Uses the same soft purples, pinks, blues at reduced opacity.

const AURORA_POSITIONS: { layers: string[] }[] = [
  { layers: [ // bottom-left
    'radial-gradient(ellipse 80% 70% at 0% 100%, rgba(140,120,210,0.24) 0%, transparent 60%)',
    'radial-gradient(ellipse 60% 50% at 10% 85%, rgba(225,110,160,0.19) 0%, transparent 55%)',
    'radial-gradient(ellipse 50% 40% at 20% 95%, rgba(240,150,120,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // top-right
    'radial-gradient(ellipse 80% 70% at 100% 0%, rgba(120,145,225,0.24) 0%, transparent 60%)',
    'radial-gradient(ellipse 55% 50% at 90% 15%, rgba(155,135,225,0.19) 0%, transparent 55%)',
    'radial-gradient(ellipse 45% 35% at 85% 5%, rgba(225,110,160,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // bottom-right
    'radial-gradient(ellipse 80% 70% at 100% 100%, rgba(225,110,160,0.24) 0%, transparent 60%)',
    'radial-gradient(ellipse 55% 50% at 90% 85%, rgba(240,150,120,0.19) 0%, transparent 55%)',
    'radial-gradient(ellipse 50% 40% at 80% 95%, rgba(140,120,210,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // top-centre
    'radial-gradient(ellipse 90% 60% at 50% 0%, rgba(155,135,225,0.24) 0%, transparent 55%)',
    'radial-gradient(ellipse 60% 40% at 45% 10%, rgba(120,145,225,0.19) 0%, transparent 50%)',
    'radial-gradient(ellipse 50% 35% at 55% 5%, rgba(225,110,160,0.11) 0%, transparent 50%)',
  ]},
  { layers: [ // left-centre
    'radial-gradient(ellipse 60% 80% at 0% 50%, rgba(140,120,210,0.24) 0%, transparent 60%)',
    'radial-gradient(ellipse 45% 60% at 5% 45%, rgba(225,110,160,0.16) 0%, transparent 55%)',
    'radial-gradient(ellipse 40% 45% at 10% 55%, rgba(120,145,225,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // bottom-centre
    'radial-gradient(ellipse 90% 60% at 50% 100%, rgba(225,110,160,0.24) 0%, transparent 55%)',
    'radial-gradient(ellipse 60% 40% at 55% 90%, rgba(240,150,120,0.19) 0%, transparent 50%)',
    'radial-gradient(ellipse 50% 35% at 45% 95%, rgba(155,135,225,0.11) 0%, transparent 50%)',
  ]},
  { layers: [ // top-left
    'radial-gradient(ellipse 80% 70% at 0% 0%, rgba(155,135,225,0.24) 0%, transparent 60%)',
    'radial-gradient(ellipse 55% 50% at 10% 15%, rgba(120,145,225,0.19) 0%, transparent 55%)',
    'radial-gradient(ellipse 45% 35% at 15% 5%, rgba(240,150,120,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // right-centre
    'radial-gradient(ellipse 60% 80% at 100% 50%, rgba(120,145,225,0.24) 0%, transparent 60%)',
    'radial-gradient(ellipse 45% 55% at 95% 55%, rgba(155,135,225,0.16) 0%, transparent 55%)',
    'radial-gradient(ellipse 40% 45% at 90% 45%, rgba(225,110,160,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // bottom-left wider
    'radial-gradient(ellipse 90% 65% at 10% 95%, rgba(140,120,210,0.22) 0%, transparent 55%)',
    'radial-gradient(ellipse 65% 50% at 0% 80%, rgba(225,110,160,0.16) 0%, transparent 50%)',
    'radial-gradient(ellipse 50% 40% at 25% 100%, rgba(120,145,225,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // top-right wider
    'radial-gradient(ellipse 85% 65% at 90% 5%, rgba(225,110,160,0.22) 0%, transparent 55%)',
    'radial-gradient(ellipse 60% 45% at 100% 20%, rgba(155,135,225,0.16) 0%, transparent 50%)',
    'radial-gradient(ellipse 50% 40% at 80% 0%, rgba(240,150,120,0.14) 0%, transparent 50%)',
  ]},
  { layers: [ // corner diagonal bottom-left to top-right
    'radial-gradient(ellipse 70% 55% at 5% 90%, rgba(140,120,210,0.19) 0%, transparent 55%)',
    'radial-gradient(ellipse 60% 50% at 95% 10%, rgba(120,145,225,0.16) 0%, transparent 50%)',
  ]},
  { layers: [ // centre glow
    'radial-gradient(ellipse 70% 60% at 50% 50%, rgba(155,135,225,0.16) 0%, transparent 55%)',
    'radial-gradient(ellipse 50% 40% at 55% 55%, rgba(225,110,160,0.11) 0%, transparent 50%)',
    'radial-gradient(ellipse 40% 35% at 45% 45%, rgba(120,145,225,0.08) 0%, transparent 50%)',
  ]},
  { layers: [ // bottom spread
    'radial-gradient(ellipse 100% 50% at 50% 100%, rgba(140,120,210,0.22) 0%, transparent 55%)',
    'radial-gradient(ellipse 70% 35% at 30% 90%, rgba(225,110,160,0.14) 0%, transparent 50%)',
    'radial-gradient(ellipse 60% 30% at 70% 95%, rgba(240,150,120,0.14) 0%, transparent 50%)',
  ]},
];

// ── Component ──────────────────────────────────────────────

interface CategoryCarouselProps {
  title: string;
  courses: CourseData[];
  onSelectCourse: (courseId: string) => void;
  onBack: () => void;
  userProgress: UserProgress;
}

const CategoryCarousel: React.FC<CategoryCarouselProps> = ({
  title, courses, onSelectCourse, onBack, userProgress,
}) => {
  const total = courses.length;

  const initialIndex = useMemo(() => {
    const idx = courses.findIndex(c => {
      const p = userProgress[c.id];
      return !p || p.unlockedSection < c.sectionsCount;
    });
    return idx >= 0 ? idx : 0;
  }, [courses, userProgress]);

  const [current, setCurrent] = useState(initialIndex);

  const goTo = useCallback((idx: number) => {
    if (idx >= 0 && idx < total) setCurrent(idx);
  }, [total]);

  const goPrev = useCallback(() => goTo(current - 1), [current, goTo]);
  const goNext = useCallback(() => goTo(current + 1), [current, goTo]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') goPrev();
      if (e.key === 'ArrowRight') goNext();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [goPrev, goNext]);

  const touchRef = useRef<{ x: number } | null>(null);
  const onTouchStart = useCallback((e: React.TouchEvent) => {
    touchRef.current = { x: e.touches[0].clientX };
  }, []);
  const onTouchEnd = useCallback((e: React.TouchEvent) => {
    if (!touchRef.current) return;
    const dx = e.changedTouches[0].clientX - touchRef.current.x;
    if (Math.abs(dx) > 50) { dx < 0 ? goNext() : goPrev(); }
    touchRef.current = null;
  }, [goNext, goPrev]);

  const trackOffset = -(current * 70) + 15;

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col">

      {/* ── Header ── */}
      <div className="relative px-5 pt-5 pb-4">
        <button
          onClick={onBack}
          className="absolute top-5 left-4 w-9 h-9 rounded-xl bg-white dark:bg-zinc-900 border border-stone-200 dark:border-zinc-800 flex items-center justify-center hover:bg-stone-50 dark:hover:bg-zinc-800 transition-colors"
        >
          <ArrowLeft size={16} className="text-zinc-600 dark:text-zinc-300" />
        </button>
        <div className="text-center pt-1">
          <h1 className="text-zinc-800 dark:text-white" style={{ fontFamily: SERIF, fontSize: 20, fontWeight: 500 }}>
            {title}
          </h1>
          <p className="text-[13px] text-zinc-400 dark:text-zinc-500 mt-0.5">{total} modules</p>
        </div>
      </div>

      {/* ── Carousel ── */}
      <div
        className="flex-1 flex flex-col justify-center overflow-hidden"
        onTouchStart={onTouchStart}
        onTouchEnd={onTouchEnd}
      >
        <div
          className="flex items-stretch"
          style={{
            transform: `translateX(${trackOffset}%)`,
            transition: 'transform 0.4s cubic-bezier(0.25, 0.1, 0.25, 1)',
          }}
        >
          {courses.map((course, i) => {
            const progress = userProgress[course.id];
            const sections = course.sectionsCount;
            const unlocked = progress?.unlockedSection ?? 0;
            const isCompleted = unlocked >= sections;
            const isStarted = unlocked > 0;
            const pct = sections > 0 ? Math.round((unlocked / sections) * 100) : 0;
            const vis = getVisual(course);
            const dist = Math.abs(i - current);
            const isActive = i === current;
            const isSide = dist === 1;
            const num = String(i + 1).padStart(2, '0');

            return (
              <div
                key={course.id}
                className="shrink-0 px-2"
                style={{
                  width: '70%',
                  opacity: isActive ? 1 : isSide ? 0.35 : 0.12,
                  transition: 'opacity 0.4s cubic-bezier(0.25, 0.1, 0.25, 1)',
                  pointerEvents: isActive || isSide ? 'auto' : 'none',
                }}
                onClick={isSide ? () => goTo(i) : undefined}
              >
                <div
                  className={`relative overflow-hidden flex flex-col h-full rounded-xl p-5 transition-all duration-300 ${
                    isActive
                      ? 'border border-stone-300 dark:border-zinc-700 shadow-sm'
                      : 'border border-stone-200 dark:border-zinc-800'
                  }`}
                  style={{
                    backgroundColor: '#ffffff',
                    backgroundImage: AURORA_POSITIONS[i % AURORA_POSITIONS.length].layers.join(', '),
                    cursor: isSide ? 'pointer' : undefined,
                  }}
                >
                  {/* Card content */}
                  <div className="relative z-10 flex flex-col flex-1">

                    {/* Top row: pill + counter */}
                    <div className="flex items-center justify-between mb-4">
                      <span
                        className="inline-block text-[11px] font-medium rounded-full"
                        style={{ padding: '4px 10px', background: vis.pillBg, color: vis.pillText }}
                      >
                        {vis.pillLabel}
                      </span>
                      <span className="text-[12px] tabular-nums text-zinc-400 dark:text-zinc-500">
                        {num} <span className="text-zinc-300 dark:text-zinc-700">/</span> {total}
                      </span>
                    </div>

                    {/* Title */}
                    <h2
                      className="mb-2 text-zinc-800 dark:text-white"
                      style={{ fontFamily: SERIF, fontSize: 17, fontWeight: 500, lineHeight: 1.35 }}
                    >
                      {course.title}
                    </h2>

                    {/* Description */}
                    <p className="text-[13px] leading-relaxed text-zinc-500 dark:text-zinc-400 flex-1 mb-5">
                      {course.description}
                    </p>

                    {/* Progress bar */}
                    {isStarted && !isCompleted && (
                      <div className="mb-4">
                        <div className="w-full h-1 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
                          <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: '#2A7D6F', transition: 'width 0.5s ease-out' }} />
                        </div>
                        <p className="text-[10px] font-medium mt-1" style={{ color: '#2A7D6F' }}>{pct}% complete</p>
                      </div>
                    )}

                    {/* Bottom row */}
                    <div className="flex items-center justify-between mt-auto">
                      <span className="text-[12px] text-zinc-400 dark:text-zinc-500">
                        {sections} sections
                      </span>
                      {isActive && (
                        isCompleted ? (
                          <button
                            onClick={(e) => { e.stopPropagation(); onSelectCourse(course.id); }}
                            className="flex items-center gap-1.5 px-4 py-2 rounded-full text-[13px] font-medium transition-colors"
                            style={{ border: '1.5px solid rgba(42,125,111,0.25)', color: '#2A7D6F' }}
                          >
                            <Check size={13} /> Review
                          </button>
                        ) : (
                          <button
                            onClick={(e) => { e.stopPropagation(); onSelectCourse(course.id); }}
                            className="flex items-center gap-1.5 px-4 py-2 rounded-full text-[13px] font-medium text-white transition-colors hover:opacity-90 active:scale-[0.97]"
                            style={{ backgroundColor: '#2A7D6F' }}
                          >
                            {isStarted ? 'Continue' : 'Start'} <ArrowRight size={13} />
                          </button>
                        )
                      )}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Navigation controls ── */}
      <div className="flex items-center justify-center gap-5 pb-8 pt-4">
        <button
          onClick={goPrev}
          disabled={current === 0}
          className="w-9 h-9 rounded-full bg-white dark:bg-zinc-900 border border-stone-300 dark:border-zinc-700 flex items-center justify-center transition-colors hover:bg-stone-50 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <ArrowLeft size={14} className="text-zinc-600 dark:text-zinc-300" />
        </button>
        <span className="text-sm tabular-nums">
          <span className="font-medium text-zinc-800 dark:text-white">{String(current + 1).padStart(2, '0')}</span>
          <span className="text-zinc-300 dark:text-zinc-700"> / </span>
          <span className="text-zinc-400 dark:text-zinc-500">{total}</span>
        </span>
        <button
          onClick={goNext}
          disabled={current === total - 1}
          className="w-9 h-9 rounded-full bg-white dark:bg-zinc-900 border border-stone-300 dark:border-zinc-700 flex items-center justify-center transition-colors hover:bg-stone-50 dark:hover:bg-zinc-800 disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <ArrowRight size={14} className="text-zinc-600 dark:text-zinc-300" />
        </button>
      </div>
    </div>
  );
};

export default CategoryCarousel;
