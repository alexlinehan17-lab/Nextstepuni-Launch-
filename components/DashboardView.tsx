/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { MotionDiv } from './Motion';
import { ArrowLeft, BookOpen, ChevronRight, TrendingUp } from 'lucide-react';
import { type CategoryType } from './KnowledgeTree';
import { type CourseData } from './Library';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface DashboardViewProps {
  userProgress: UserProgress;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  pointsBalance: number;
}

const CATEGORY_ORDER: { key: CategoryType; color: string }[] = [
  { key: 'architecture-mindset', color: '#3B82F6' },
  { key: 'science-growth', color: '#F59E0B' },
  { key: 'learning-cheat-codes', color: '#2A7D6F' },
  { key: 'subject-specific-science', color: '#64748B' },
  { key: 'exam-zone', color: '#EF4444' },
];

const stagger = (i: number) => ({
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { delay: i * 0.06, duration: 0.4, ease: [0.16, 1, 0.3, 1] as number[] },
});

const DashboardView: React.FC<DashboardViewProps> = ({
  userProgress,
  allCourses,
  categoryTitles,
  streak,
  recommendation,
  onSelectModule,
  onBack,
  pointsBalance,
}) => {
  const completedCount = allCourses.filter(c => {
    const p = userProgress[c.id];
    return p && p.unlockedSection >= c.sectionsCount;
  }).length;

  const totalPct = allCourses.length > 0 ? Math.round((completedCount / allCourses.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950">

      {/* ── Coloured hero ── */}
      <div className="relative" style={{ backgroundColor: '#2A7D6F' }}>
        {/* Decorative blobs */}
        <div className="absolute pointer-events-none" style={{ top: -80, right: -60, width: 240, height: 240, borderRadius: '50%', background: 'rgba(255,255,255,0.07)' }} />
        <div className="absolute pointer-events-none" style={{ top: 30, right: -20, width: 120, height: 120, borderRadius: '50%', background: 'rgba(255,255,255,0.05)' }} />
        <div className="absolute pointer-events-none" style={{ bottom: 20, left: -40, width: 160, height: 160, borderRadius: '50%', background: 'rgba(0,0,0,0.06)' }} />

        <div className="relative z-10 px-6 pt-6 pb-16 max-w-2xl mx-auto">
          {/* Header */}
          <div className="flex items-center gap-3 mb-10">
            <button onClick={onBack} className="w-9 h-9 rounded-xl flex items-center justify-center transition-colors" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <ArrowLeft size={18} style={{ color: '#fff' }} />
            </button>
            <h1 className="font-serif text-lg font-semibold text-white">My Progress</h1>
          </div>

          {/* Overall progress */}
          <MotionDiv {...stagger(0)} className="mb-8">
            <p className="text-[11px] uppercase tracking-[0.14em] font-semibold mb-2" style={{ color: 'rgba(255,255,255,0.5)' }}>Overall Completion</p>
            <div className="flex items-baseline gap-2">
              <span className="font-serif font-bold text-white" style={{ fontSize: 'clamp(40px, 10vw, 56px)', letterSpacing: '-0.03em', lineHeight: 1 }}>{totalPct}%</span>
              <span className="text-sm font-medium" style={{ color: 'rgba(255,255,255,0.6)' }}>{completedCount}/{allCourses.length} modules</span>
            </div>
          </MotionDiv>

          {/* Stat pills — translucent white on colour */}
          <MotionDiv {...stagger(1)} className="grid grid-cols-3 gap-3">
            <div className="rounded-2xl px-4 py-3 text-center" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <p className="text-xl font-apercu font-bold text-white">{completedCount}</p>
              <p className="text-[10px] uppercase tracking-widest font-semibold mt-0.5" style={{ color: 'rgba(255,255,255,0.7)' }}>Completed</p>
            </div>
            <div className="rounded-2xl px-4 py-3 text-center" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <p className="text-xl font-apercu font-bold text-white">{streak.currentStreak}</p>
              <p className="text-[10px] uppercase tracking-widest font-semibold mt-0.5" style={{ color: 'rgba(255,255,255,0.7)' }}>Day Streak</p>
            </div>
            <div className="rounded-2xl px-4 py-3 text-center" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <p className="text-xl font-apercu font-bold text-white">{pointsBalance}</p>
              <p className="text-[10px] uppercase tracking-widest font-semibold mt-0.5" style={{ color: 'rgba(255,255,255,0.7)' }}>Points</p>
            </div>
          </MotionDiv>
        </div>

      </div>

      {/* ── Cream section ── */}
      <div className="px-6 pb-24 max-w-2xl mx-auto">

        {/* Category progress */}
        <MotionDiv {...stagger(2)} className="mt-8">
          <p className="text-xs uppercase tracking-[0.2em] font-semibold mb-4 text-[#A8A29E] dark:text-zinc-500">Category Progress</p>
          <div className="rounded-2xl bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 px-5 py-2" style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}>
            {CATEGORY_ORDER.map(({ key, color }, ci) => {
              const categoryCourses = allCourses.filter(c => c.category === key);
              if (categoryCourses.length === 0) return null;
              const completed = categoryCourses.filter(c => {
                const p = userProgress[c.id];
                return p && p.unlockedSection >= c.sectionsCount;
              }).length;
              const pct = Math.round((completed / categoryCourses.length) * 100);

              return (
                <div key={key} className={`py-4 ${ci < CATEGORY_ORDER.length - 1 ? 'border-b border-[#F0EFED] dark:border-zinc-800' : ''}`}>
                  <div className="flex items-center gap-3 mb-2.5">
                    <div className="w-8 h-8 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: `${color}14` }}>
                      <TrendingUp size={16} style={{ color }} />
                    </div>
                    <p className="text-sm font-medium flex-1 text-[#1A1A1A] dark:text-white truncate">{categoryTitles[key]}</p>
                    <span className="text-xs font-semibold tabular-nums" style={{ color }}>{completed}/{categoryCourses.length}</span>
                  </div>
                  <div className="w-full h-2 rounded-full overflow-hidden ml-11" style={{ backgroundColor: `${color}15`, width: 'calc(100% - 2.75rem)' }}>
                    <MotionDiv
                      className="h-full rounded-full"
                      style={{ backgroundColor: color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 1, delay: 0.3 + ci * 0.08, ease: 'easeOut' }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </MotionDiv>

        {/* Today's Focus */}
        {recommendation && recommendation.reason !== 'all-complete' && (
          <MotionDiv {...stagger(3)} className="mt-8">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold mb-4 text-[#A8A29E] dark:text-zinc-500">Today's Focus</p>
            <div
              className="rounded-2xl overflow-hidden relative"
              style={{
                backgroundColor: '#2A7D6F',
                boxShadow: '0 4px 20px rgba(42,125,111,0.25)',
              }}
            >
              {/* Decorative blob */}
              <div className="absolute pointer-events-none" style={{ top: -20, right: -20, width: 80, height: 80, borderRadius: '50%', background: 'rgba(255,255,255,0.08)' }} />

              <button
                onClick={() => onSelectModule(recommendation.moduleId)}
                className="relative w-full px-5 py-5 flex items-center gap-4 group text-left"
              >
                <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(255,255,255,0.18)' }}>
                  <BookOpen size={18} style={{ color: '#fff' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-white">{recommendation.title}</p>
                  <p className="text-xs mt-0.5" style={{ color: 'rgba(255,255,255,0.6)' }}>
                    {recommendation.reason === 'in-progress' ? 'Continue where you left off' : 'Start this module'}
                  </p>
                </div>
                <ChevronRight size={16} className="text-white/60 shrink-0 group-hover:translate-x-0.5 transition-transform" />
              </button>
            </div>
          </MotionDiv>
        )}
      </div>
    </div>
  );
};

export default DashboardView;
