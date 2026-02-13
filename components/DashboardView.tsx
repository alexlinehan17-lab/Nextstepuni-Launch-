/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, BookOpen, Flame, Coins, ChevronRight, Waves, Scale, Zap, CloudRain } from 'lucide-react';
import { CategoryType } from './KnowledgeTree';
import { CourseData } from './Library';
import { MoodEntry } from '../hooks/useMood';
import { StreakData } from '../hooks/useStreak';
import { FocusRecommendation } from '../hooks/useTodaysFocus';
import { categoryColorMap } from '../courseData';

const MotionDiv = motion.div as any;

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface DashboardViewProps {
  userProgress: UserProgress;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  moodEntries: MoodEntry[];
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  pointsBalance: number;
}

const MOOD_ICONS: Record<string, { icon: typeof Waves; label: string }> = {
  calm: { icon: Waves, label: 'Calm' },
  balanced: { icon: Scale, label: 'Balanced' },
  energized: { icon: Zap, label: 'Energized' },
  stressed: { icon: CloudRain, label: 'Stressed' },
};

const DAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const CATEGORY_ORDER: { key: CategoryType; barColor: string }[] = [
  { key: 'architecture-mindset', barColor: 'bg-blue-500' },
  { key: 'science-growth', barColor: 'bg-amber-500' },
  { key: 'learning-cheat-codes', barColor: 'bg-teal-500' },
  { key: 'subject-specific-science', barColor: 'bg-slate-500' },
  { key: 'exam-zone', barColor: 'bg-red-500' },
];

const DashboardView: React.FC<DashboardViewProps> = ({
  userProgress,
  allCourses,
  categoryTitles,
  streak,
  recommendation,
  moodEntries,
  onSelectModule,
  onBack,
  pointsBalance,
}) => {
  const completedCount = allCourses.filter(c => {
    const p = userProgress[c.id];
    return p && p.unlockedSection >= c.sectionsCount - 1;
  }).length;

  // Build 7-day mood timeline
  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return d.toISOString().slice(0, 10);
  });

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 pt-16 md:pt-24 pb-32 px-4 sm:px-6 transition-colors duration-500">
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
            My Progress
          </h1>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-500/10 flex items-center justify-center">
                <BookOpen size={18} className="text-blue-500" />
              </div>
              <div>
                <p className="text-2xl font-bold text-zinc-900 dark:text-white">{completedCount}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">Modules Completed</p>
              </div>
            </div>
          </MotionDiv>

          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.15 }}
            className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center">
                <Flame size={18} className="text-orange-500" />
              </div>
              <div>
                <p className="text-2xl font-bold text-zinc-900 dark:text-white">{streak.currentStreak}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">Day Streak</p>
              </div>
            </div>
          </MotionDiv>

          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center">
                <Coins size={18} className="text-amber-500" />
              </div>
              <div>
                <p className="text-2xl font-bold text-zinc-900 dark:text-white">{pointsBalance}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">Points Balance</p>
              </div>
            </div>
          </MotionDiv>
        </div>

        {/* Category progress */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.25 }}
          className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6 mb-8"
        >
          <h2 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-5">Category Progress</h2>
          <div className="space-y-4">
            {CATEGORY_ORDER.map(({ key, barColor }) => {
              const categoryCourses = allCourses.filter(c => c.category === key);
              if (categoryCourses.length === 0) return null;
              const completed = categoryCourses.filter(c => {
                const p = userProgress[c.id];
                return p && p.unlockedSection >= c.sectionsCount - 1;
              }).length;
              const pct = Math.round((completed / categoryCourses.length) * 100);

              return (
                <div key={key}>
                  <div className="flex items-center justify-between mb-1.5">
                    <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 truncate pr-4">{categoryTitles[key]}</p>
                    <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500 shrink-0">{completed}/{categoryCourses.length}</span>
                  </div>
                  <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                    <MotionDiv
                      className={`h-full ${barColor} rounded-full`}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </MotionDiv>

        {/* Today's Focus */}
        {recommendation && recommendation.reason !== 'all-complete' && (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6 mb-8"
          >
            <h2 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-4">Today's Focus</h2>
            <button
              onClick={() => onSelectModule(recommendation.moduleId)}
              className="w-full flex items-center justify-between p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors group"
            >
              <div className="text-left">
                <p className="text-sm font-semibold text-zinc-900 dark:text-white">{recommendation.title}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                  {recommendation.reason === 'in-progress' ? 'Continue where you left off' : 'Start this module'}
                </p>
              </div>
              <ChevronRight size={16} className="text-zinc-400 dark:text-zinc-500 shrink-0 group-hover:translate-x-0.5 transition-transform" />
            </button>
          </MotionDiv>
        )}

        {/* 7-day mood timeline */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.35 }}
          className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6"
        >
          <h2 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-5">7-Day Mood</h2>
          <div className="flex items-end justify-between gap-2">
            {last7Days.map((dateStr) => {
              const entry = moodEntries.find(e => e.date === dateStr);
              const dayOfWeek = new Date(dateStr + 'T12:00:00').getDay();
              const moodInfo = entry ? MOOD_ICONS[entry.mood] : null;
              const Icon = moodInfo?.icon;

              return (
                <div key={dateStr} className="flex flex-col items-center gap-2 flex-1">
                  <div className={`w-9 h-9 rounded-full flex items-center justify-center ${
                    Icon
                      ? 'bg-[#CC785C]/10 text-[#CC785C]'
                      : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-300 dark:text-zinc-600'
                  }`}>
                    {Icon ? <Icon size={16} /> : <div className="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-600" />}
                  </div>
                  <span className="text-[10px] font-medium text-zinc-400 dark:text-zinc-500">
                    {DAY_LABELS[dayOfWeek]}
                  </span>
                </div>
              );
            })}
          </div>
        </MotionDiv>
      </div>
    </div>
  );
};

export default DashboardView;
