/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChevronLeft, ChevronRight, BookOpen, RotateCcw, Target,
  Clock, Calendar, TrendingUp, Settings, HelpCircle, X, ArrowRight, AlertTriangle, CalendarOff,
  CheckCircle, Flame, BarChart3, Star, ShoppingBag, BookMarked,
} from 'lucide-react';
import {
  type StudentSubjectProfile, type StudyBlock, DAYS_OF_WEEK, LC_SUBJECTS, getPointsForGrade, type Grade,
  type TimetableCompletions, type TimetableStreak, getBlockId, toDateKey,
} from './subjectData';
import {
  computeSubjectPriorities, allocateSessions, generateWeeklyTimetable,
  computeWeeksUntilExam, computeIntensityFactor,
  type SessionAllocation, type SubjectPriority,
} from './timetableAlgorithm';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

interface SpacedRepetitionTimetableProps {
  profile: StudentSubjectProfile;
  onOpenSettings: () => void;
  onRestDaysChange?: (restDays: string[]) => void;
  completions?: TimetableCompletions;
  streak?: TimetableStreak;
  onToggleCompletion?: (dateKey: string, blockId: string, completed: boolean) => void;
  points?: number;
  onOpenShop?: () => void;
  onOpenJournal?: () => void;
  skippedSessions?: string[];
}

// ─── Subject Color Map (literal Tailwind strings for CDN constraint) ────────

const SUBJECT_COLORS: Record<string, { dot: string; bg: string; border: string; text: string }> = {
  'English': { dot: 'bg-blue-500', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Irish': { dot: 'bg-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Mathematics': { dot: 'bg-indigo-500', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
  'French': { dot: 'bg-sky-500', bg: 'bg-sky-50 dark:bg-sky-900/20', border: 'border-sky-200 dark:border-sky-800/40', text: 'text-sky-700 dark:text-sky-300' },
  'German': { dot: 'bg-yellow-500', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'Spanish': { dot: 'bg-orange-500', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Italian': { dot: 'bg-red-500', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
  'Japanese': { dot: 'bg-pink-500', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Physics': { dot: 'bg-cyan-500', bg: 'bg-cyan-50 dark:bg-cyan-900/20', border: 'border-cyan-200 dark:border-cyan-800/40', text: 'text-cyan-700 dark:text-cyan-300' },
  'Chemistry': { dot: 'bg-teal-500', bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300' },
  'Biology': { dot: 'bg-lime-500', bg: 'bg-lime-50 dark:bg-lime-900/20', border: 'border-lime-200 dark:border-lime-800/40', text: 'text-lime-700 dark:text-lime-300' },
  'Applied Maths': { dot: 'bg-violet-500', bg: 'bg-violet-50 dark:bg-violet-900/20', border: 'border-violet-200 dark:border-violet-800/40', text: 'text-violet-700 dark:text-violet-300' },
  'Computer Science': { dot: 'bg-fuchsia-500', bg: 'bg-fuchsia-50 dark:bg-fuchsia-900/20', border: 'border-fuchsia-200 dark:border-fuchsia-800/40', text: 'text-fuchsia-700 dark:text-fuchsia-300' },
  'Ag Science': { dot: 'bg-green-500', bg: 'bg-green-50 dark:bg-green-900/20', border: 'border-green-200 dark:border-green-800/40', text: 'text-green-700 dark:text-green-300' },
  'Accounting': { dot: 'bg-amber-500', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Business': { dot: 'bg-amber-600', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Economics': { dot: 'bg-yellow-600', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'History': { dot: 'bg-purple-500', bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300' },
  'Geography': { dot: 'bg-emerald-600', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Politics & Society': { dot: 'bg-rose-500', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300' },
  'Religious Education': { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' },
  'Classical Studies': { dot: 'bg-stone-500', bg: 'bg-stone-50 dark:bg-stone-800/40', border: 'border-stone-200 dark:border-stone-700/40', text: 'text-stone-700 dark:text-stone-300' },
  'Home Economics': { dot: 'bg-orange-400', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Construction Studies': { dot: 'bg-slate-500', bg: 'bg-slate-50 dark:bg-slate-800/40', border: 'border-slate-200 dark:border-slate-700/40', text: 'text-slate-700 dark:text-slate-300' },
  'Engineering': { dot: 'bg-gray-500', bg: 'bg-gray-50 dark:bg-gray-800/40', border: 'border-gray-200 dark:border-gray-700/40', text: 'text-gray-700 dark:text-gray-300' },
  'DCG': { dot: 'bg-neutral-500', bg: 'bg-neutral-50 dark:bg-neutral-800/40', border: 'border-neutral-200 dark:border-neutral-700/40', text: 'text-neutral-700 dark:text-neutral-300' },
  'Technology': { dot: 'bg-blue-600', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Art': { dot: 'bg-rose-400', bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300' },
  'Music': { dot: 'bg-pink-400', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Design & Communication Graphics': { dot: 'bg-indigo-400', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
};

const DEFAULT_COLOR = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

function getSubjectColor(name: string) {
  return SUBJECT_COLORS[name] || DEFAULT_COLOR;
}

// ─── Session Type Icons ─────────────────────────────────────────────────────

const SESSION_TYPE_CONFIG: Record<StudyBlock['sessionType'], { icon: React.ElementType; label: string }> = {
  'new-learning': { icon: BookOpen, label: 'Learn' },
  'practice': { icon: Target, label: 'Practice' },
  'revision': { icon: RotateCcw, label: 'Revise' },
};

// ─── Helper ─────────────────────────────────────────────────────────────────

function getWeekStartDate(weekOffset: number): Date {
  const now = new Date();
  const day = now.getDay(); // 0=Sun, 1=Mon
  const mondayOffset = day === 0 ? -6 : 1 - day;
  const monday = new Date(now);
  monday.setDate(now.getDate() + mondayOffset + weekOffset * 7);
  monday.setHours(0, 0, 0, 0);
  return monday;
}

function formatDateShort(date: Date): string {
  return date.toLocaleDateString('en-IE', { month: 'short', day: 'numeric' });
}

// ─── StudyBlockCard ─────────────────────────────────────────────────────────

const StudyBlockCard: React.FC<{ block: StudyBlock; completed?: boolean; skipped?: boolean; onToggle?: () => void }> = ({ block, completed, skipped, onToggle }) => {
  const color = getSubjectColor(block.subjectName);
  const typeConfig = SESSION_TYPE_CONFIG[block.sessionType];
  const TypeIcon = typeConfig.icon;

  if (skipped) {
    return (
      <div className="p-2 rounded-lg border-2 border-dashed border-zinc-300 dark:border-zinc-600 bg-zinc-50/50 dark:bg-zinc-800/30 opacity-60">
        <div className="flex items-center gap-1.5 mb-0.5">
          <div className="w-2 h-2 rounded-full bg-zinc-400 dark:bg-zinc-500 flex-shrink-0" />
          <p className="text-[10px] font-bold truncate text-zinc-400 dark:text-zinc-500 line-through">{block.subjectName}</p>
        </div>
        <div className="flex items-center gap-1 ml-3.5">
          <span className="text-[9px] text-zinc-400 dark:text-zinc-500 italic">Skipped</span>
        </div>
      </div>
    );
  }

  const inner = (
    <>
      <div className="flex items-center gap-1.5 mb-0.5">
        {completed
          ? <CheckCircle size={10} className="text-emerald-500 dark:text-emerald-400 flex-shrink-0" />
          : <div className={`w-2 h-2 rounded-full ${color.dot} flex-shrink-0`} />
        }
        <p className={`text-[10px] font-bold truncate ${completed ? 'line-through text-emerald-600 dark:text-emerald-400' : color.text}`}>{block.subjectName}</p>
      </div>
      <div className="flex items-center gap-1 ml-3.5">
        <TypeIcon size={9} className={completed ? 'text-emerald-400 dark:text-emerald-500' : 'text-zinc-400 dark:text-zinc-500'} />
        <span className={`text-[9px] ${completed ? 'text-emerald-400 dark:text-emerald-500' : 'text-zinc-400 dark:text-zinc-500'}`}>{typeConfig.label}</span>
        <span className={`text-[9px] ml-auto ${completed ? 'text-emerald-300 dark:text-emerald-600' : 'text-zinc-300 dark:text-zinc-600'}`}>{block.durationMinutes}m</span>
      </div>
    </>
  );

  if (onToggle) {
    return (
      <MotionButton
        whileTap={{ scale: 0.97 }}
        onClick={onToggle}
        className={`w-full text-left p-2 rounded-lg border transition-all ${
          completed
            ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800/40 opacity-75'
            : `${color.bg} ${color.border}`
        }`}
      >
        {inner}
      </MotionButton>
    );
  }

  return (
    <div className={`p-2 rounded-lg ${color.bg} border ${color.border} transition-colors`}>
      {inner}
    </div>
  );
};

// ─── Priority Row ───────────────────────────────────────────────────────────

const PRIORITY_BAR_COLORS: Record<string, string> = {
  High: 'bg-rose-500',
  Medium: 'bg-amber-500',
  Low: 'bg-emerald-500',
};

const PRIORITY_TEXT_COLORS: Record<string, string> = {
  High: 'text-rose-600 dark:text-rose-400',
  Medium: 'text-amber-600 dark:text-amber-400',
  Low: 'text-emerald-600 dark:text-emerald-400',
};

const PriorityRow: React.FC<{ alloc: SessionAllocation; maxSessions: number }> = ({ alloc, maxSessions }) => {
  const color = getSubjectColor(alloc.subjectName);
  const barWidth = maxSessions > 0 ? (alloc.sessions / maxSessions) * 100 : 0;

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-2 w-28 flex-shrink-0">
        <div className={`w-2.5 h-2.5 rounded-full ${color.dot} flex-shrink-0`} />
        <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 truncate">{alloc.subjectName}</span>
      </div>
      <div className="flex-1 h-3 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${PRIORITY_BAR_COLORS[alloc.priorityLabel]}`}
          initial={{ width: 0 }}
          animate={{ width: `${barWidth}%` }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        />
      </div>
      <span className="text-xs font-mono font-bold text-zinc-500 dark:text-zinc-400 w-6 text-right">{alloc.sessions}</span>
      <span className={`text-[9px] font-bold w-12 text-right ${PRIORITY_TEXT_COLORS[alloc.priorityLabel]}`}>{alloc.priorityLabel}</span>
    </div>
  );
};

// ─── Main Component ─────────────────────────────────────────────────────────

const SpacedRepetitionTimetable: React.FC<SpacedRepetitionTimetableProps> = ({ profile, onOpenSettings, onRestDaysChange, completions = {}, streak = { currentStreak: 0, lastActiveDate: '', longestStreak: 0 }, onToggleCompletion, points = 0, onOpenShop, onOpenJournal, skippedSessions = [] }) => {
  const skippedSet = useMemo(() => new Set(skippedSessions), [skippedSessions]);
  const [weekOffset, setWeekOffset] = useState(0);
  const [selectedDay, setSelectedDay] = useState(0); // For mobile view
  const [showExplainer, setShowExplainer] = useState(false);
  const [restDays, setRestDays] = useState<Set<string>>(() => new Set(profile.restDays || []));
  const [studyHoursRange, setStudyHoursRange] = useState<'week' | 'month' | 'all'>('week');

  const toggleRestDay = (day: string) => {
    setRestDays(prev => {
      const next = new Set(prev);
      if (next.has(day)) next.delete(day); else next.add(day);
      if (next.size >= 7) return prev; // must keep at least 1 study day
      onRestDaysChange?.(Array.from(next));
      return next;
    });
  };

  const weeksUntilExam = computeWeeksUntilExam(profile.examStartDate);

  const priorities = useMemo(() => computeSubjectPriorities(profile.subjects), [profile.subjects]);

  const restDaysArray = useMemo(() => Array.from(restDays), [restDays]);

  // Compute total studied minutes from completions based on selected range
  const studiedMinutes = useMemo(() => {
    const now = new Date();
    const allDateKeys = Object.keys(completions);

    let filteredKeys: string[];
    if (studyHoursRange === 'all') {
      filteredKeys = allDateKeys;
    } else if (studyHoursRange === 'month') {
      const y = now.getFullYear();
      const m = String(now.getMonth() + 1).padStart(2, '0');
      const monthPrefix = `${y}-${m}`;
      filteredKeys = allDateKeys.filter(k => k.startsWith(monthPrefix));
    } else {
      // 'week' — current Mon–Sun
      const weekStartDate = getWeekStartDate(0);
      const weekEndDate = new Date(weekStartDate);
      weekEndDate.setDate(weekStartDate.getDate() + 6);
      const startKey = toDateKey(weekStartDate);
      const endKey = toDateKey(weekEndDate);
      filteredKeys = allDateKeys.filter(k => k >= startKey && k <= endKey);
    }

    let totalBlocks = 0;
    for (const key of filteredKeys) {
      totalBlocks += completions[key].length;
    }
    return totalBlocks * 45;
  }, [completions, studyHoursRange]);

  const studiedHours = Math.floor(studiedMinutes / 60);
  const studiedRemainingMins = studiedMinutes % 60;
  const studyHoursRangeLabel = studyHoursRange === 'week' ? 'this week' : studyHoursRange === 'month' ? 'this month' : 'all time';

  const allocations = useMemo(
    () => allocateSessions(priorities, Math.max(0, weeksUntilExam - weekOffset)),
    [priorities, weeksUntilExam, weekOffset]
  );

  const timetable = useMemo(
    () => generateWeeklyTimetable(allocations, weeksUntilExam, weekOffset, restDaysArray),
    [allocations, weeksUntilExam, weekOffset, restDaysArray]
  );

  const weekStart = getWeekStartDate(weekOffset);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6);

  const totalSessions = timetable.reduce((sum, day) => sum + day.blocks.length, 0);
  const totalMinutes = totalSessions * 45;
  const totalHours = Math.floor(totalMinutes / 60);
  const remainingMins = totalMinutes % 60;

  const daysUntilExam = Math.max(0, Math.ceil((new Date(profile.examStartDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)));
  const maxSessions = Math.max(...allocations.map(a => a.sessions), 1);

  const DAY_SHORTS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  // Helper: get date key for a day index (0=Mon) in the current week view
  const getDateKeyForDay = (dayIndex: number): string => {
    const d = new Date(weekStart);
    d.setDate(weekStart.getDate() + dayIndex);
    return toDateKey(d);
  };

  // Helper: check if a block is completed for a given day
  const isBlockCompleted = (dayIndex: number, blockIndex: number, block: StudyBlock): boolean => {
    const dateKey = getDateKeyForDay(dayIndex);
    const blockId = getBlockId(block, blockIndex);
    return completions[dateKey]?.includes(blockId) ?? false;
  };

  // Helper: check if a block is skipped (earned rest)
  const isBlockSkipped = (dayIndex: number, blockIndex: number, block: StudyBlock): boolean => {
    const dateKey = getDateKeyForDay(dayIndex);
    const blockId = getBlockId(block, blockIndex);
    return skippedSet.has(`${dateKey}|${blockId}`);
  };

  // Helper: toggle handler for a block
  const handleBlockToggle = (dayIndex: number, blockIndex: number, block: StudyBlock) => {
    if (!onToggleCompletion) return;
    const dateKey = getDateKeyForDay(dayIndex);
    const blockId = getBlockId(block, blockIndex);
    const completed = completions[dateKey]?.includes(blockId) ?? false;
    onToggleCompletion(dateKey, blockId, !completed);
  };

  // Today focus: compute today's day index within this week
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayKey = toDateKey(today);
  const jsDay = today.getDay(); // 0=Sun
  const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1; // 0=Mon
  const isCurrentWeek = weekOffset === 0;
  const todaySchedule = isCurrentWeek ? timetable[todayDayIndex] : null;
  const todayHasSessions = todaySchedule ? todaySchedule.blocks.length > 0 : false;
  const showTodayView = isCurrentWeek && todayHasSessions;

  // Today's completion stats
  const todayCompletedIds = completions[todayKey] ?? [];
  const todayBlocks = todaySchedule?.blocks ?? [];
  const todayCompletedCount = todayBlocks.filter((block, bi) => {
    const blockId = getBlockId(block, bi);
    return todayCompletedIds.includes(blockId);
  }).length;
  const todayTotalCount = todayBlocks.length;
  const todayAllDone = todayTotalCount > 0 && todayCompletedCount >= todayTotalCount;
  const todayProgress = todayTotalCount > 0 ? todayCompletedCount / todayTotalCount : 0;

  // "Next Up" — first uncompleted session today
  const nextUpIndex = todayBlocks.findIndex((block, bi) => {
    const blockId = getBlockId(block, bi);
    return !todayCompletedIds.includes(blockId);
  });
  const nextUpBlock = nextUpIndex >= 0 ? todayBlocks[nextUpIndex] : null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Spaced Repetition Timetable</h2>
        <button
          onClick={onOpenSettings}
          className="p-2.5 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
          title="Edit subjects"
        >
          <Settings size={16} className="text-zinc-500 dark:text-zinc-400" />
        </button>
      </div>

      {/* Week navigation */}
      <div className="flex items-center justify-between">
        <MotionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setWeekOffset(o => o - 1)}
          disabled={weekOffset <= 0}
          className="p-2 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <ChevronLeft size={16} className="text-zinc-600 dark:text-zinc-300" />
        </MotionButton>

        <span className="text-sm font-semibold text-zinc-600 dark:text-zinc-300">
          {formatDateShort(weekStart)} — {formatDateShort(weekEnd)}
        </span>

        <MotionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setWeekOffset(o => o + 1)}
          className="p-2 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
        >
          <ChevronRight size={16} className="text-zinc-600 dark:text-zinc-300" />
        </MotionButton>
      </div>

      {/* Stats dashboard */}
      <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-4">
        <div className="flex items-center gap-4">
          {/* Stats grid */}
          <div className="flex-1 grid grid-cols-3 gap-x-6 gap-y-3">
            {/* Row 1 */}
            <div className="flex items-center gap-2">
              <TrendingUp size={14} className="text-purple-500 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{totalSessions}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">sessions</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Clock size={14} className="text-blue-500 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{totalHours}h {remainingMins}m</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">planned</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Calendar size={14} className="text-amber-500 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{daysUntilExam}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">days left</p>
              </div>
            </div>
            {/* Row 2 */}
            <div className="flex items-center gap-2">
              <Flame size={14} className="text-orange-500 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{streak.currentStreak} day{streak.currentStreak !== 1 ? 's' : ''}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">streak</p>
              </div>
            </div>
            <button
              onClick={() => setStudyHoursRange(r => r === 'week' ? 'month' : r === 'month' ? 'all' : 'week')}
              className="flex items-center gap-2 hover:bg-zinc-100 dark:hover:bg-white/5 -m-1 p-1 rounded-lg transition-colors cursor-pointer text-left"
              title="Click to cycle: this week / this month / all time"
            >
              <BarChart3 size={14} className="text-emerald-500 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{studiedHours}h {studiedRemainingMins}m</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">studied {studyHoursRangeLabel}</p>
              </div>
            </button>
            <div className="flex items-center gap-2">
              <Star size={14} className="text-yellow-500 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{points}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">points</p>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          {(onOpenShop || onOpenJournal) && (
            <div className="flex flex-col gap-2 border-l border-zinc-200 dark:border-white/10 pl-4">
              {onOpenShop && (
                <button
                  onClick={onOpenShop}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30 hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors"
                  title="Reward Shop"
                >
                  <ShoppingBag size={14} className="text-purple-600 dark:text-purple-400" />
                  <span className="text-xs font-bold text-purple-600 dark:text-purple-400">Shop</span>
                </button>
              )}
              {onOpenJournal && (
                <button
                  onClick={onOpenJournal}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-700/30 hover:bg-indigo-100 dark:hover:bg-indigo-900/30 transition-colors"
                  title="Study Journal"
                >
                  <BookMarked size={14} className="text-indigo-600 dark:text-indigo-400" />
                  <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">Journal</span>
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Rest day toggles */}
      <div className="flex items-center gap-2">
        <CalendarOff size={14} className="text-zinc-400 dark:text-zinc-500 flex-shrink-0" />
        <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 flex-shrink-0">Rest</span>
        <div className="flex gap-1 flex-1">
          {DAY_SHORTS.map((short, i) => {
            const dayName = DAYS_OF_WEEK[i];
            const isRest = restDays.has(dayName);
            return (
              <button
                key={dayName}
                onClick={() => toggleRestDay(dayName)}
                className={`flex-1 py-1 rounded-md text-[10px] font-bold transition-all border ${
                  isRest
                    ? 'bg-rose-100 dark:bg-rose-900/30 border-rose-300 dark:border-rose-600 text-rose-600 dark:text-rose-400 line-through'
                    : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-500 dark:text-zinc-400 hover:border-rose-300 dark:hover:border-rose-600'
                }`}
                title={isRest ? `${dayName}: rest day` : `${dayName}: study day`}
              >
                {short}
              </button>
            );
          })}
        </div>
      </div>

      {/* Today Focus View */}
      {showTodayView && (
        <MotionDiv
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-5"
        >
          <div className="flex items-center gap-4">
            {/* Progress Ring */}
            <div className="relative w-16 h-16 flex-shrink-0">
              <svg viewBox="0 0 48 48" className="w-16 h-16 -rotate-90">
                <circle cx="24" cy="24" r="20" fill="none" strokeWidth="3"
                  className="stroke-zinc-200 dark:stroke-white/10" />
                <motion.circle
                  cx="24" cy="24" r="20" fill="none" strokeWidth="3"
                  strokeLinecap="round"
                  className="stroke-emerald-500"
                  initial={{ strokeDashoffset: 2 * Math.PI * 20 }}
                  animate={{ strokeDashoffset: 2 * Math.PI * 20 * (1 - todayProgress) }}
                  transition={{ duration: 0.6, ease: 'easeOut' }}
                  style={{ strokeDasharray: 2 * Math.PI * 20 }}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-sm font-bold font-mono text-zinc-700 dark:text-zinc-200">
                  {todayCompletedCount}/{todayTotalCount}
                </span>
              </div>
            </div>

            {/* Today Info */}
            <div className="flex-1 min-w-0">
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1">Today</p>
              {todayAllDone ? (
                <div>
                  <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400">All done for today!</p>
                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Great work. Rest up and come back tomorrow.</p>
                </div>
              ) : nextUpBlock ? (
                <div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-1">Next up</p>
                  <div className="flex items-center gap-2">
                    <div className={`w-2.5 h-2.5 rounded-full ${getSubjectColor(nextUpBlock.subjectName).dot} flex-shrink-0`} />
                    <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200 truncate">{nextUpBlock.subjectName}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 flex-shrink-0">{SESSION_TYPE_CONFIG[nextUpBlock.sessionType].label} · {nextUpBlock.durationMinutes}m</span>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </MotionDiv>
      )}

      {/* Mobile: Day selector tabs */}
      <div className="md:hidden flex gap-1 overflow-x-auto pb-1">
        {DAY_SHORTS.map((day, i) => (
          <button
            key={day}
            onClick={() => setSelectedDay(i)}
            className={`flex-1 min-w-0 px-2 py-2 rounded-lg text-xs font-bold text-center transition-colors ${
              selectedDay === i
                ? 'bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 border border-purple-300 dark:border-purple-600'
                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700'
            }`}
          >
            {day}
            <span className="block text-[9px] font-normal mt-0.5">{timetable[i].blocks.length}</span>
          </button>
        ))}
      </div>

      {/* Mobile: Single day view */}
      <div className="md:hidden">
        <AnimatePresence mode="wait">
          <MotionDiv
            key={selectedDay}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
            className="space-y-2"
          >
            {timetable[selectedDay].blocks.length > 0 ? (
              timetable[selectedDay].blocks.map((block, bi) => (
                <StudyBlockCard
                  key={bi}
                  block={block}
                  completed={isBlockCompleted(selectedDay, bi, block)}
                  skipped={isBlockSkipped(selectedDay, bi, block)}
                  onToggle={onToggleCompletion ? () => handleBlockToggle(selectedDay, bi, block) : undefined}
                />
              ))
            ) : (
              <div className="text-center py-8 text-zinc-400 dark:text-zinc-500 text-sm">Rest day</div>
            )}
          </MotionDiv>
        </AnimatePresence>
      </div>

      {/* Desktop: 7-column grid */}
      <div className="hidden md:grid grid-cols-7 gap-2">
        {timetable.map((day, di) => (
          <div key={day.day} className="min-w-0">
            <div className="text-center mb-2">
              <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">{DAY_SHORTS[di]}</p>
              <p className="text-[9px] text-zinc-300 dark:text-zinc-600">{day.blocks.length} sessions</p>
            </div>
            <div className="space-y-1.5 min-h-[120px]">
              {day.blocks.length > 0 ? (
                day.blocks.map((block, bi) => (
                  <StudyBlockCard
                    key={bi}
                    block={block}
                    completed={isBlockCompleted(di, bi, block)}
                    skipped={isBlockSkipped(di, bi, block)}
                    onToggle={onToggleCompletion ? () => handleBlockToggle(di, bi, block) : undefined}
                  />
                ))
              ) : (
                <div className="flex items-center justify-center h-24 text-[10px] text-zinc-300 dark:text-zinc-600 italic">Rest</div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Priority Breakdown */}
      <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400">Priority Breakdown</h3>
          <button
            onClick={() => setShowExplainer(!showExplainer)}
            className="flex items-center gap-1.5 text-xs font-semibold text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 transition-colors"
          >
            <HelpCircle size={14} />
            {showExplainer ? 'Hide explanation' : 'How is this calculated?'}
          </button>
        </div>
        <div className="space-y-2.5">
          {allocations
            .sort((a, b) => b.sessions - a.sessions)
            .map(alloc => (
              <PriorityRow key={alloc.subjectName} alloc={alloc} maxSessions={maxSessions} />
            ))}
        </div>
      </div>

      {/* Priority Explainer */}
      <AnimatePresence>
        {showExplainer && (
          <MotionDiv
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden"
          >
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-6 space-y-6">
              {/* How it works */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400">How Your Timetable Is Built</h4>
                  <button onClick={() => setShowExplainer(false)} className="text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
                    <X size={16} />
                  </button>
                </div>
                <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed mb-4">
                  Each subject gets a <span className="font-bold text-purple-600 dark:text-purple-400">priority score</span> that determines how many study sessions it receives each week. The score combines two factors:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                  <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-900/15 border border-blue-200 dark:border-blue-700/30">
                    <p className="text-[10px] font-bold uppercase tracking-widest text-blue-600 dark:text-blue-400 mb-1">Points Gain</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      The CAO points difference between your target grade and current grade. Bigger gaps = more room to grow = higher priority.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30">
                    <p className="text-[10px] font-bold uppercase tracking-widest text-amber-600 dark:text-amber-400 mb-1">Efficiency Multiplier</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      Subjects where you're currently weaker get a boost. Going from H2 to H1 is much harder than H7 to H5 — your study time is better spent where grade jumps come more easily.
                    </p>
                  </div>
                </div>
                <div className="p-3 rounded-lg bg-zinc-100 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700/30 text-center">
                  <p className="text-xs font-mono font-bold text-zinc-600 dark:text-zinc-300">
                    Priority Score = Points Gain <span className="text-purple-500">x</span> Difficulty Multiplier
                  </p>
                </div>
              </div>

              {/* Per-subject breakdown */}
              <div>
                <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3">Your Subject Scores</h4>
                <div className="space-y-2">
                  {priorities.map(p => {
                    const color = getSubjectColor(p.subjectName);
                    const maxPriority = Math.max(...priorities.map(pr => pr.priorityScore), 1);
                    const barPct = (p.priorityScore / maxPriority) * 100;

                    return (
                      <div key={p.subjectName} className="p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <div className={`w-2.5 h-2.5 rounded-full ${color.dot} flex-shrink-0`} />
                            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{p.subjectName}</span>
                          </div>
                          <span className="text-sm font-mono font-bold text-purple-600 dark:text-purple-400">
                            {Math.round(p.priorityScore)}
                          </span>
                        </div>

                        {/* Score visualisation bar */}
                        <div className="h-1.5 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden mb-2.5">
                          <motion.div
                            className="h-full rounded-full bg-purple-500"
                            initial={{ width: 0 }}
                            animate={{ width: `${barPct}%` }}
                            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                          />
                        </div>

                        {/* Breakdown chips */}
                        <div className="flex flex-wrap items-center gap-2 text-[10px]">
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 font-semibold">
                            {p.currentGrade} <ArrowRight size={8} /> {p.targetGrade}
                          </span>
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-bold">
                            +{p.pointsGain} pts{p.isMaths ? ' (incl. bonus)' : ''}
                          </span>
                          <span className="text-zinc-400 dark:text-zinc-500 font-mono">x</span>
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 font-bold">
                            {p.difficultyMultiplier.toFixed(2)} efficiency
                          </span>
                          <span className="text-zinc-400 dark:text-zinc-500 font-mono">=</span>
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 font-bold">
                            {Math.round(p.priorityScore)}
                          </span>
                        </div>

                        {/* Explanation sentence */}
                        <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-2 leading-relaxed">
                          {p.pointsGain === 0
                            ? `Already at your target — this subject receives minimum sessions to maintain.`
                            : p.difficultyMultiplier >= 0.7
                              ? `Currently at ${p.currentGrade}, so the efficiency multiplier is high (${p.difficultyMultiplier.toFixed(2)}) — grade jumps are more achievable from this level, so your study time goes further here.`
                              : p.difficultyMultiplier >= 0.5
                                ? `At ${p.currentGrade}, the efficiency multiplier is moderate (${p.difficultyMultiplier.toFixed(2)}) — improvement is possible but takes consistent work.`
                                : `Starting from ${p.currentGrade}, the efficiency multiplier is lower (${p.difficultyMultiplier.toFixed(2)}) because you're already strong — each further grade jump is harder to achieve (diminishing returns).`
                          }
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Projected CAO Points — Best 6 */}
              {(() => {
                // Compute target points per subject
                const subjectTargetPoints = priorities.map(p => {
                  const lcSubject = LC_SUBJECTS.find(s => s.name === p.subjectName);
                  const isMaths = lcSubject?.isMaths || false;
                  return {
                    subjectName: p.subjectName,
                    targetGrade: p.targetGrade,
                    targetPoints: getPointsForGrade(p.targetGrade, isMaths),
                    isMaths,
                  };
                });

                // Sort by target points descending to find best 6
                const sorted = [...subjectTargetPoints].sort((a, b) => b.targetPoints - a.targetPoints);
                const best6 = sorted.slice(0, 6);
                const outside = sorted.slice(6);
                const projectedTotal = best6.reduce((sum, s) => sum + s.targetPoints, 0);

                // Non-maths subjects outside best 6 are candidates for deprioritization
                const deprioritiseCandidates = outside.filter(s => !s.isMaths);

                return (
                  <div className="space-y-3">
                    {/* Projected total */}
                    <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-900/15 border border-emerald-200 dark:border-emerald-700/30">
                      <p className="text-[10px] font-bold uppercase tracking-widest text-emerald-600 dark:text-emerald-400 mb-2">Projected CAO Points (Best 6)</p>
                      <div className="flex items-baseline gap-2 mb-3">
                        <p className="text-4xl font-bold font-mono text-emerald-600 dark:text-emerald-400">{projectedTotal}</p>
                        <p className="text-sm text-emerald-500 dark:text-emerald-500 font-semibold">/ 625</p>
                      </div>
                      <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                        If you hit your target grade in every subject, your <span className="font-bold">best 6</span> will total <span className="font-bold text-emerald-600 dark:text-emerald-400">{projectedTotal} points</span>. Only your top 6 subjects count for CAO.
                      </p>
                      <div className="mt-3 space-y-1">
                        {best6.map((s, i) => (
                          <div key={s.subjectName} className="flex items-center justify-between text-xs">
                            <div className="flex items-center gap-2">
                              <span className="text-[10px] font-bold text-emerald-500 dark:text-emerald-400 w-3">{i + 1}.</span>
                              <div className={`w-2 h-2 rounded-full ${getSubjectColor(s.subjectName).dot}`} />
                              <span className="font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                              {s.isMaths && <span className="text-[9px] text-indigo-500 dark:text-indigo-400 font-bold">+25</span>}
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-zinc-400 dark:text-zinc-500 font-medium">{s.targetGrade}</span>
                              <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">{s.targetPoints}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Deprioritise suggestion */}
                    {deprioritiseCandidates.length > 0 && (
                      <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30">
                        <div className="flex items-start gap-2 mb-2">
                          <AlertTriangle size={14} className="text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
                          <p className="text-[10px] font-bold uppercase tracking-widest text-amber-600 dark:text-amber-400">Subjects Outside Your Best 6</p>
                        </div>
                        <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed mb-3">
                          Based on your target grades, <span className="font-bold">{deprioritiseCandidates.map(s => s.subjectName).join(' and ')}</span> {deprioritiseCandidates.length === 1 ? 'falls' : 'fall'} outside your top 6. Since only your best 6 count for CAO, you could consider focusing less time here and more on your counting subjects.
                        </p>

                        <div className="space-y-1 mb-3">
                          {deprioritiseCandidates.map(s => (
                            <div key={s.subjectName} className="flex items-center justify-between text-xs p-2 rounded-lg bg-amber-100/50 dark:bg-amber-900/20">
                              <div className="flex items-center gap-2">
                                <div className={`w-2 h-2 rounded-full ${getSubjectColor(s.subjectName).dot}`} />
                                <span className="font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                              </div>
                              <span className="font-mono text-amber-600 dark:text-amber-400 font-bold">{s.targetGrade} — {s.targetPoints} pts</span>
                            </div>
                          ))}
                        </div>

                        <div className="p-3 rounded-lg bg-rose-50 dark:bg-rose-900/15 border border-rose-200 dark:border-rose-700/30">
                          <div className="flex items-start gap-2">
                            <AlertTriangle size={12} className="text-rose-500 dark:text-rose-400 flex-shrink-0 mt-0.5" />
                            <p className="text-[10px] text-rose-700 dark:text-rose-300 leading-relaxed">
                              <span className="font-bold">High-risk strategy.</span> Only deprioritise a subject if you're confident you're significantly stronger in at least 6 others. Unexpected results on exam day can mean a "safe" subject becomes the one you need. The timetable still allocates minimum sessions to every subject for safety.
                            </p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })()}

              {/* Session count & intensity note */}
              <div className="p-4 rounded-xl bg-purple-50 dark:bg-purple-900/15 border border-purple-200 dark:border-purple-700/30">
                <p className="text-[10px] font-bold uppercase tracking-widest text-purple-600 dark:text-purple-400 mb-1">Session Allocation</p>
                <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                  Sessions are split proportionally by priority score, with a minimum of 1 per subject. The total number of sessions per week ramps from <span className="font-bold">14</span> (2/day) to <span className="font-bold">21</span> (3/day) as exams approach. Right now you're at <span className="font-bold text-purple-600 dark:text-purple-400">{totalSessions} sessions</span> this week.
                </p>
              </div>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Intensity indicator */}
      {weekOffset > 0 && (
        <div className="text-center">
          <p className="text-xs text-zinc-400 dark:text-zinc-500">
            Intensity: {Math.round(computeIntensityFactor(Math.max(0, weeksUntilExam - weekOffset)) * 100)}% — {
              Math.max(0, weeksUntilExam - weekOffset)
            } weeks to exam
          </p>
        </div>
      )}
    </div>
  );
};

export default SpacedRepetitionTimetable;
