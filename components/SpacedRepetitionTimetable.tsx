/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import {
  ChevronLeft, ChevronRight, BookOpen, RotateCcw, Target,
  Settings, HelpCircle, X, ArrowRight, AlertTriangle, CalendarOff,
  CheckCircle, Flame, CalendarDays,
  Play,
} from 'lucide-react';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { type SchoolEvent } from './gc/GCKeyEvents';
import {
  type StudentSubjectProfile, type StudyBlock, DAYS_OF_WEEK, LC_SUBJECTS, getPointsForGrade,
  type TimetableCompletions, type TimetableStreak, getBlockId, toDateKey,
  computeBargains,
} from './subjectData';
import {
  computeSubjectPriorities, allocateSessions, generateWeeklyTimetable,
  computeWeeksUntilExam, computeIntensityFactor,
  type SessionAllocation,
} from './timetableAlgorithm';
import { type DebriefEntry, computeStrategyHints, type SubjectStrategyHint } from './StudyDebrief';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useInnovationData } from '../contexts/InnovationDataContext';

export interface TimetableBlockInfo {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  dateKey: string;
  blockId: string;
}

interface SpacedRepetitionTimetableProps {
  profile: StudentSubjectProfile;
  uid?: string;
  onOpenSettings: () => void;
  onRestDaysChange?: (restDays: string[]) => void;
  completions?: TimetableCompletions;
  streak?: TimetableStreak;
  onToggleCompletion?: (dateKey: string, blockId: string, completed: boolean) => void;
  points?: number;
  onSpendPoints?: (type: 'skip-session' | 'rest-day-pass', detail?: string) => void;
  onOpenJournal?: () => void;
  skippedSessions?: string[];
  onStudyNow?: (block: TimetableBlockInfo) => void;
  onBlockDurationChange?: (subjectName: string, sessionType: string, newDuration: number) => void;
  schoolEvents?: SchoolEvent[];
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

const SUBJECT_HEX: Record<string, string> = {
  'English': '#3b82f6', 'Irish': '#10b981', 'Mathematics': '#6366f1',
  'French': '#0ea5e9', 'German': '#eab308', 'Spanish': '#f97316',
  'Italian': '#ef4444', 'Japanese': '#ec4899', 'Physics': '#06b6d4',
  'Chemistry': '#14b8a6', 'Biology': '#84cc16', 'Applied Maths': '#8b5cf6',
  'Computer Science': '#d946ef', 'Ag Science': '#22c55e', 'Accounting': '#f59e0b',
  'Business': '#d97706', 'Economics': '#ca8a04', 'History': '#a855f7',
  'Geography': '#059669', 'Politics & Society': '#f43f5e',
  'Religious Education': '#71717a', 'Classical Studies': '#78716c',
  'Home Economics': '#fb923c', 'Construction Studies': '#64748b',
  'Engineering': '#6b7280', 'DCG': '#737373', 'Technology': '#2563eb',
  'Art': '#fb7185', 'Music': '#f472b6',
  'Design & Communication Graphics': '#818cf8',
};

function getSubjectHexColor(name: string): string {
  return SUBJECT_HEX[name] || '#71717a';
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

// ─── StudyBlockCard (day-focused full-width design) ─────────────────────────

const StudyBlockCard: React.FC<{
  block: StudyBlock;
  completed?: boolean;
  skipped?: boolean;
  onToggle?: () => void;
  bargainPts?: number;
  strategyHint?: SubjectStrategyHint;
  isToday?: boolean;
  onStudyNow?: () => void;
}> = ({ block, completed, skipped, onToggle, _bargainPts, strategyHint, isToday, onStudyNow }) => {
  const _color = getSubjectColor(block.subjectName);
  const typeConfig = SESSION_TYPE_CONFIG[block.sessionType];

  if (skipped) {
    return (
      <div
        className="py-3 px-4 rounded-xl opacity-50 bg-[#FAF7F4] dark:bg-zinc-900"
        style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-400 dark:bg-zinc-500 flex-shrink-0" />
            <span className="text-sm font-medium text-zinc-400 dark:text-zinc-500 line-through">{block.subjectName}</span>
          </div>
          <span className="text-xs text-zinc-400 dark:text-zinc-500 italic">Skipped</span>
        </div>
      </div>
    );
  }

  const hex = getSubjectHexColor(block.subjectName);
  const TypeIcon = typeConfig.icon;

  const inner = completed ? (
    <div
      className="rounded-xl transition-all"
      style={{ backgroundColor: '#EDF2EE', border: '1.5px solid rgba(107,143,113,0.25)', borderRadius: 12, opacity: 0.7 }}
    >
      <div className="flex items-center justify-between px-3 py-2.5">
        <div className="flex items-center gap-2 min-w-0 flex-1">
          <CheckCircle size={14} style={{ color: '#6B8F71' }} className="flex-shrink-0" />
          <span className="text-sm font-medium line-through" style={{ color: '#6B8F71' }}>{block.subjectName}</span>
        </div>
        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full" style={{ backgroundColor: 'rgba(107,143,113,0.12)', color: '#6B8F71' }}>{typeConfig.label}</span>
      </div>
    </div>
  ) : (
    <div className="rounded-xl overflow-hidden" style={{ border: `1px solid ${hex}20`, borderRadius: 12 }}>
      {/* Coloured header strip */}
      <div className="flex items-center justify-between px-3 py-2" style={{ backgroundColor: hex }}>
        <span className="text-[13px] font-bold text-white truncate">{block.subjectName}</span>
        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ml-2" style={{ backgroundColor: 'rgba(255,255,255,0.2)', color: '#fff' }}>
          <span className="flex items-center gap-1"><TypeIcon size={10} />{typeConfig.label}</span>
        </span>
      </div>
      {/* Details row */}
      <div className="flex items-center justify-between px-3 py-2" style={{ backgroundColor: `${hex}08` }}>
        <span className="text-xs text-[#78716C] dark:text-zinc-400">{block.durationMinutes} min</span>
        <div className="flex items-center gap-2">
          {strategyHint && (
            <span className="text-[10px] text-[#A8A29E] dark:text-zinc-500">Try: {strategyHint.label}</span>
          )}
          {isToday && onStudyNow && (
            <button
              onClick={(e) => { e.stopPropagation(); onStudyNow(); }}
              className="flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-lg"
              style={{ backgroundColor: hex, color: '#fff' }}
            >
              Study <ArrowRight size={10} />
            </button>
          )}
        </div>
      </div>
      {block.suggestedTopics && block.suggestedTopics.length > 0 && (
        <p className="text-[10px] px-3 py-1.5 text-[#A8A29E] dark:text-zinc-500" style={{ backgroundColor: `${hex}05` }}>
          Focus: {block.suggestedTopics.join(', ')}
        </p>
      )}
    </div>
  );

  if (onToggle) {
    return (
      <MotionButton
        whileTap={{ scale: 0.98 }}
        onClick={onToggle}
        className="w-full text-left"
      >
        {inner}
      </MotionButton>
    );
  }

  return inner;
};

// ─── Priority Row ───────────────────────────────────────────────────────────

const _PRIORITY_BAR_COLORS: Record<string, string> = {
  High: '',
  Medium: '',
  Low: '',
};

const _PRIORITY_BAR_INLINE: Record<string, React.CSSProperties> = {
  High: { backgroundColor: '#2A7D6F' },
  Medium: { backgroundColor: '#2A7D6F' },
  Low: { backgroundColor: '#2A7D6F' },
};

const PRIORITY_BADGE_INLINE: Record<string, React.CSSProperties> = {
  High: { backgroundColor: '#FDF3E7', color: '#C4873B' },
  Medium: { backgroundColor: '#EDF5F3', color: '#2A7D6F' },
  Low: {},
};

const PRIORITY_BADGE_CLASS: Record<string, string> = {
  High: '',
  Medium: '',
  Low: 'bg-[#FAF7F4] dark:bg-zinc-900 text-[#A8A29E] dark:text-zinc-500',
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
      <div className="flex-1 h-3 rounded-full overflow-hidden" style={{ backgroundColor: '#EDEAE6' }}>
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: getSubjectHexColor(alloc.subjectName) }}
          initial={{ width: 0 }}
          animate={{ width: `${barWidth}%` }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        />
      </div>
      <span className="text-xs font-mono font-bold text-zinc-500 dark:text-zinc-400 w-6 text-right">{alloc.sessions}</span>
      <span className={`text-[9px] font-bold w-14 text-right px-1.5 py-0.5 rounded-full ${PRIORITY_BADGE_CLASS[alloc.priorityLabel] || ''}`} style={PRIORITY_BADGE_INLINE[alloc.priorityLabel]}>{alloc.priorityLabel}</span>
    </div>
  );
};

// ─── Main Component ─────────────────────────────────────────────────────────

const SpacedRepetitionTimetable: React.FC<SpacedRepetitionTimetableProps> = ({ profile, uid, onOpenSettings, onRestDaysChange, completions = {}, streak = { currentStreak: 0, lastActiveDate: '', longestStreak: 0 }, onToggleCompletion, points = 0, onSpendPoints, _onOpenJournal, skippedSessions = [], onStudyNow, _onBlockDurationChange, schoolEvents = [] }) => {
  const skippedSet = useMemo(() => new Set(skippedSessions), [skippedSessions]);
  const [weekOffset, setWeekOffset] = useState(0);
  const [showExplainer, setShowExplainer] = useState(false);
  const [restDays, setRestDays] = useState<Set<string>>(() => new Set(profile.restDays || []));
  const [studyHoursRange, setStudyHoursRange] = useState<'week' | 'month' | 'all'>('week');
  const [blockActionModal, setBlockActionModal] = useState<{ block: StudyBlock; dayIndex: number; blockIndex: number } | null>(null);

  // Topic mastery from context -> feeds into timetable weighting
  const { topicMastery: topicMasteryHook } = useInnovationData();
  const topicMastery = topicMasteryHook.mastery;

  // Strategy hints from Learning DNA (per-subject best strategy)
  const [strategyHints, setStrategyHints] = useState<Record<string, SubjectStrategyHint>>({});
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const data = snap.data()?.studyDebriefs as DebriefEntry[] | undefined;
        if (!cancelled && data) setStrategyHints(computeStrategyHints(data));
      } catch (err) { console.error('Failed to load strategy hints:', err); }
    })();
    return () => { cancelled = true; };
  }, [uid]);

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

  const priorities = useMemo(() => computeSubjectPriorities(profile.subjects, topicMastery), [profile.subjects, topicMastery]);

  // Top 3 bargain subjects (for badge display on study blocks)
  const bargainMap = useMemo(() => {
    const bargains = computeBargains(profile);
    const map: Record<string, number> = {};
    bargains.slice(0, 3).forEach(b => { map[b.subjectName] = b.pointsGain; });
    return map;
  }, [profile]);

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
      // 'week' -- current Mon-Sun
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

  const blockDuration = profile.defaultBlockDuration ?? 45;

  const timetable = useMemo(
    () => generateWeeklyTimetable(allocations, weeksUntilExam, weekOffset, restDaysArray, blockDuration, undefined, topicMastery),
    [allocations, weeksUntilExam, weekOffset, restDaysArray, blockDuration, topicMastery]
  );

  const weekStart = getWeekStartDate(weekOffset);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6);

  const totalSessions = timetable.reduce((sum, day) => sum + day.blocks.length, 0);
  const totalMinutes = totalSessions * 45;
  const _totalHours = Math.floor(totalMinutes / 60);
  const _remainingMins = totalMinutes % 60;

  const _daysUntilExam = Math.max(0, Math.ceil((new Date(profile.examStartDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)));
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

    if (completed) {
      // Un-completing: just toggle off directly
      onToggleCompletion(dateKey, blockId, false);
    } else if (onStudyNow) {
      // Show "Study Now / Already Studied" modal
      setBlockActionModal({ block, dayIndex, blockIndex });
    } else {
      // Fallback: direct toggle (old behavior)
      onToggleCompletion(dateKey, blockId, true);
    }
  };

  const handleStudyNow = () => {
    if (!blockActionModal || !onStudyNow) return;
    const { block, dayIndex, blockIndex } = blockActionModal;
    const dateKey = getDateKeyForDay(dayIndex);
    const blockId = getBlockId(block, blockIndex);
    setBlockActionModal(null);
    onStudyNow({
      subject: block.subjectName,
      sessionType: block.sessionType,
      durationMinutes: block.durationMinutes,
      dateKey,
      blockId,
    });
  };

  const handleAlreadyStudied = () => {
    if (!blockActionModal || !onToggleCompletion) return;
    const { block, dayIndex, blockIndex } = blockActionModal;
    const dateKey = getDateKeyForDay(dayIndex);
    const blockId = getBlockId(block, blockIndex);
    setBlockActionModal(null);
    onToggleCompletion(dateKey, blockId, true);
  };

  const handleSkipSession = () => {
    if (!blockActionModal || !onSpendPoints) return;
    const { block, dayIndex, blockIndex } = blockActionModal;
    const blockId = getBlockId(block, blockIndex);
    const dateKey = getDateKeyForDay(dayIndex);
    const fullId = `${dateKey}::${blockId}`;
    onSpendPoints('skip-session', fullId);
    setBlockActionModal(null);
  };

  // Helper: get school events for a specific day index
  const getEventsForDay = (dayIndex: number): SchoolEvent[] => {
    if (!schoolEvents.length) return [];
    const dateKey = getDateKeyForDay(dayIndex);
    return schoolEvents.filter(e => e.date === dateKey);
  };

  const EVENT_CAT_COLORS: Record<string, { bg: string; text: string; dot: string }> = {
    exams: { bg: 'bg-red-100 dark:bg-red-900/30', text: 'text-red-700 dark:text-red-300', dot: 'bg-red-500' },
    deadlines: { bg: 'bg-amber-100 dark:bg-amber-900/30', text: 'text-amber-700 dark:text-amber-300', dot: 'bg-amber-500' },
    school: { bg: 'bg-blue-100 dark:bg-blue-900/30', text: 'text-blue-700 dark:text-blue-300', dot: 'bg-blue-500' },
    other: { bg: 'bg-zinc-100 dark:bg-zinc-800', text: 'text-zinc-700 dark:text-zinc-300', dot: 'bg-zinc-500' },
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

  // "Next Up" -- first uncompleted session today
  const nextUpIndex = todayBlocks.findIndex((block, bi) => {
    const blockId = getBlockId(block, bi);
    return !todayCompletedIds.includes(blockId);
  });
  const nextUpBlock = nextUpIndex >= 0 ? todayBlocks[nextUpIndex] : null;

  // View mode: day-focused or week overview
  const [viewMode, setViewMode] = useState<'day' | 'week'>('day');
  // Day-focused view: selected day for both mobile and desktop
  const [selectedDay, setSelectedDay] = useState<number>(isCurrentWeek ? todayDayIndex : 0);

  if (!profile || profile.subjects.length === 0) {
    return (
      <div className="text-center py-16 space-y-4">
        <div className="w-16 h-16 mx-auto flex items-center justify-center bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
          <CalendarDays size={32} style={{ color: '#2A7D6F' }} />
        </div>
        <h3 className="text-lg font-bold text-zinc-800 dark:text-white">Your study plan, built around your life</h3>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto leading-relaxed">
          A weekly timetable weighted by your weakest subjects, with rest days respected and spaced repetition built in.
        </p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500">Complete your subject profile to generate your first timetable.</p>
      </div>
    );
  }

  // Check if selected day is a rest day
  const selectedDayIsRest = restDays.has(DAYS_OF_WEEK[selectedDay]);
  const selectedDayBlocks = timetable[selectedDay]?.blocks ?? [];

  return (
    <div className="space-y-5">
      <div className="flex justify-end">
        <button
          onClick={onOpenSettings}
          className="p-2 rounded-lg transition-colors bg-[#FAF7F4] dark:bg-zinc-900"
          style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}
          title="Edit subjects"
        >
          <Settings size={16} className="text-[#A8A29E] dark:text-zinc-500" />
        </button>
      </div>

      {/* ── Week navigation + view toggle ── */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-zinc-600 dark:text-zinc-300">
            {formatDateShort(weekStart)} — {formatDateShort(weekEnd)}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setWeekOffset(o => o - 1)}
              disabled={weekOffset <= 0}
              className="p-1.5 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              style={{ backgroundColor: 'rgba(0,0,0,0.03)', borderRadius: 8 }}
            >
              <ChevronLeft size={14} className="text-zinc-500 dark:text-zinc-400" />
            </button>
            <button
              onClick={() => setWeekOffset(o => o + 1)}
              className="p-1.5 rounded-lg transition-colors"
              style={{ backgroundColor: 'rgba(0,0,0,0.03)', borderRadius: 8 }}
            >
              <ChevronRight size={14} className="text-zinc-500 dark:text-zinc-400" />
            </button>
          </div>
        </div>
        {/* Day / Week toggle */}
        <div className="flex items-center gap-1 p-1 rounded-lg" style={{ backgroundColor: 'rgba(0,0,0,0.04)' }}>
          <button
            onClick={() => setViewMode('day')}
            className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
              viewMode === 'day'
                ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm'
                : 'text-zinc-400 dark:text-zinc-500'
            }`}
          >
            Day
          </button>
          <button
            onClick={() => setViewMode('week')}
            className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
              viewMode === 'week'
                ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm'
                : 'text-zinc-400 dark:text-zinc-500'
            }`}
          >
            Week
          </button>
        </div>
      </div>

      {/* ── Key stats line ── */}
      <div className="flex items-center justify-center gap-2 flex-wrap text-xs text-zinc-500 dark:text-zinc-400">
        {streak.currentStreak > 0 && (
          <span className="flex items-center gap-1">
            <Flame size={13} style={{ color: '#C4873B' }} />
            <span className="font-semibold" style={{ color: '#C4873B' }}>{streak.currentStreak}-day streak</span>
          </span>
        )}
        {streak.currentStreak > 0 && <span className="text-[#A8A29E] dark:text-zinc-500">·</span>}
        <span className="font-medium">{todayCompletedCount}/{todayTotalCount} blocks today</span>
        <span className="text-[#A8A29E] dark:text-zinc-500">·</span>
        <button
          onClick={() => setStudyHoursRange(r => r === 'week' ? 'month' : r === 'month' ? 'all' : 'week')}
          className="font-medium transition-colors cursor-pointer"
          style={{ color: '#2A7D6F' }}
          title="Click to cycle: this week / this month / all time"
        >
          {studiedHours}h {studiedRemainingMins}m {studyHoursRangeLabel}
        </button>
      </div>

      {/* ── DAY VIEW ── */}
      {viewMode === 'day' && (<>
      {/* ── Day Tabs (horizontal pill selector) ── */}
      <div className="flex gap-1 p-1 rounded-xl overflow-x-auto" style={{ backgroundColor: 'rgba(0,0,0,0.04)' }}>
        {DAY_SHORTS.map((day, i) => {
          const dayName = DAYS_OF_WEEK[i];
          const isDayRest = restDays.has(dayName);
          const isActive = selectedDay === i;
          const _isTodayTab = isCurrentWeek && i === todayDayIndex;
          const dayBlockCount = timetable[i].blocks.length;

          return (
            <button
              key={day}
              onClick={() => setSelectedDay(i)}
              className={`flex-1 min-w-0 py-2 px-1 rounded-lg text-center transition-all ${
                isActive
                  ? 'shadow-sm'
                  : ''
              }`}
              style={isActive ? { backgroundColor: '#1C1917', borderRadius: 12 } : undefined}
            >
              <span
                className={`block text-xs font-bold ${
                  isActive
                    ? ''
                    : isDayRest
                      ? 'text-zinc-400 dark:text-zinc-500'
                      : 'text-zinc-500 dark:text-zinc-400'
                }`}
                style={isActive ? { color: '#fff', fontWeight: 700 } : undefined}
              >
                <span className="relative inline-block">
                  {day}
                  {getEventsForDay(i).length > 0 && (
                    <span className="absolute -top-0.5 -right-1.5 w-1.5 h-1.5 rounded-full" style={{ backgroundColor: '#C4873B' }} />
                  )}
                </span>
              </span>
              <span
                className={`block text-[10px] mt-0.5 ${isActive ? '' : isDayRest ? 'text-zinc-400 dark:text-zinc-500 italic' : 'text-zinc-400 dark:text-zinc-500'}`}
                style={isActive ? { color: 'rgba(255,255,255,0.7)' } : undefined}
              >
                {isDayRest ? 'rest' : dayBlockCount}
              </span>
            </button>
          );
        })}
      </div>

      {/* ── Rest day toggle (long-press hint) ── */}
      <div className="flex items-center gap-2">
        <CalendarOff size={13} className="flex-shrink-0 text-[#A8A29E] dark:text-zinc-500" />
        <span className="text-[10px] font-bold uppercase tracking-wider flex-shrink-0 text-[#A8A29E] dark:text-zinc-500">Rest</span>
        <div className="flex gap-1 flex-1">
          {DAY_SHORTS.map((short, i) => {
            const dayName = DAYS_OF_WEEK[i];
            const isRest = restDays.has(dayName);
            return (
              <button
                key={dayName}
                onClick={() => toggleRestDay(dayName)}
                className={`flex-1 py-1 rounded-md text-[10px] font-bold transition-all ${!isRest ? 'bg-[#FAF7F4] dark:bg-zinc-900 text-[#A8A29E] dark:text-zinc-500' : ''}`}
                style={isRest
                  ? { backgroundColor: 'rgba(196,135,59,0.1)', border: '0.5px solid rgba(196,135,59,0.3)', color: '#C4873B', textDecoration: 'line-through' }
                  : { border: '0.5px solid rgba(0,0,0,0.07)' }
                }
                title={isRest ? `${dayName}: rest day` : `${dayName}: study day`}
              >
                {short}
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Today Summary Card (shown when today is selected) ── */}
      {showTodayView && selectedDay === todayDayIndex && (
        <MotionDiv
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 rounded-xl bg-[#FAF7F4] dark:bg-zinc-900"
          style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}
        >
          <div className="flex items-center gap-4">
            {/* Progress Ring */}
            <div className="relative w-14 h-14 flex-shrink-0">
              <svg viewBox="0 0 48 48" className="w-14 h-14 -rotate-90">
                <circle cx="24" cy="24" r="20" fill="none" strokeWidth="3"
                  stroke="rgba(0,0,0,0.06)" />
                <motion.circle
                  cx="24" cy="24" r="20" fill="none" strokeWidth="3"
                  strokeLinecap="round"
                  initial={{ strokeDashoffset: 2 * Math.PI * 20 }}
                  animate={{ strokeDashoffset: 2 * Math.PI * 20 * (1 - todayProgress) }}
                  transition={{ duration: 0.6, ease: 'easeOut' }}
                  style={{ strokeDasharray: 2 * Math.PI * 20, stroke: '#2A7D6F' }}
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
              <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Today</p>
              {todayAllDone ? (
                <div>
                  <p className="text-sm font-bold" style={{ color: '#6B8F71' }}>All done for today!</p>
                  <p className="text-xs mt-0.5 text-[#A8A29E] dark:text-zinc-500">Great work. Rest up and come back tomorrow.</p>
                </div>
              ) : nextUpBlock ? (
                <div>
                  <p className="text-xs mb-1 text-[#A8A29E] dark:text-zinc-500">Next up</p>
                  <div className="flex items-center gap-2">
                    <div className={`w-2.5 h-2.5 rounded-full ${getSubjectColor(nextUpBlock.subjectName).dot} flex-shrink-0`} />
                    <span className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">{nextUpBlock.subjectName}</span>
                    <span className="text-xs text-[#A8A29E] dark:text-zinc-500">{SESSION_TYPE_CONFIG[nextUpBlock.sessionType].label} · {nextUpBlock.durationMinutes}m</span>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
          {getEventsForDay(todayDayIndex).length > 0 && (
            <div className="mt-3 space-y-1.5">
              {getEventsForDay(todayDayIndex).map(ev => {
                const cat = EVENT_CAT_COLORS[ev.category] || EVENT_CAT_COLORS.other;
                return (
                  <div key={ev.id} className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${cat.bg}`}>
                    <div className={`w-2 h-2 rounded-full flex-shrink-0 ${cat.dot}`} />
                    <CalendarDays size={12} className={cat.text} />
                    <span className={`text-xs font-semibold ${cat.text}`}>{ev.title}</span>
                  </div>
                );
              })}
            </div>
          )}
        </MotionDiv>
      )}

      {/* ── Day Content: Full-width block cards ── */}
      <AnimatePresence mode="wait">
        <MotionDiv
          key={selectedDay}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
          className="space-y-2"
        >
          {/* School events for this day */}
          {getEventsForDay(selectedDay).map(ev => {
            const cat = EVENT_CAT_COLORS[ev.category] || EVENT_CAT_COLORS.other;
            return (
              <div key={ev.id} className={`flex items-center gap-2 px-3 py-2 rounded-xl ${cat.bg}`} style={{ borderRadius: 12 }}>
                <div className={`w-2 h-2 rounded-full flex-shrink-0 ${cat.dot}`} />
                <CalendarDays size={13} className={cat.text} />
                <span className={`text-xs font-semibold ${cat.text}`}>{ev.title}</span>
              </div>
            );
          })}

          {/* Blocks or rest state */}
          {selectedDayIsRest || selectedDayBlocks.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 space-y-3">
              <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(0,0,0,0.03)' }}>
                <CalendarOff size={24} className="text-[#A8A29E] dark:text-zinc-500" />
              </div>
              <p className="text-sm font-medium text-[#A8A29E] dark:text-zinc-500">Rest day — recharge for tomorrow</p>
            </div>
          ) : (
            selectedDayBlocks.map((block, bi) => {
              const isDayToday = isCurrentWeek && selectedDay === todayDayIndex;
              const blockCompleted = isBlockCompleted(selectedDay, bi, block);
              return (
                <StudyBlockCard
                  key={bi}
                  block={block}
                  completed={blockCompleted}
                  skipped={isBlockSkipped(selectedDay, bi, block)}
                  onToggle={onToggleCompletion ? () => handleBlockToggle(selectedDay, bi, block) : undefined}
                  bargainPts={bargainMap[block.subjectName]}
                  strategyHint={strategyHints[block.subjectName]}
                  isToday={isDayToday}
                  onStudyNow={isDayToday && !blockCompleted && onStudyNow ? () => {
                    const dateKey = getDateKeyForDay(selectedDay);
                    const blockId = getBlockId(block, bi);
                    onStudyNow({
                      subject: block.subjectName,
                      sessionType: block.sessionType,
                      durationMinutes: block.durationMinutes,
                      dateKey,
                      blockId,
                    });
                  } : undefined}
                />
              );
            })
          )}
        </MotionDiv>
      </AnimatePresence>
      </>)}

      {/* ── WEEK VIEW ── */}
      {viewMode === 'week' && (
        <div className="overflow-x-auto">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 6 }}>
            {DAY_SHORTS.map((day, i) => {
              const dayName = DAYS_OF_WEEK[i];
              const isDayRest = restDays.has(dayName);
              const isTodayCol = isCurrentWeek && i === todayDayIndex;
              const dayBlocks = timetable[i]?.blocks ?? [];
              const dateKey = getDateKeyForDay(i);
              const dayCompletions = completions[dateKey] || [];

              return (
                <div key={day} className="min-w-0">
                  {/* Day header */}
                  <div className={`text-center py-2 mb-2 rounded-lg ${isTodayCol ? 'font-bold' : ''}`}>
                    <span
                      className={`text-xs font-bold ${isTodayCol ? '' : 'text-zinc-500 dark:text-zinc-400'}`}
                      style={isTodayCol ? { color: '#2A7D6F' } : undefined}
                    >
                      {day}
                    </span>
                    <span className="block text-[10px] text-zinc-400 dark:text-zinc-500">
                      {isDayRest ? 'rest' : `${dayBlocks.length}`}
                    </span>
                  </div>

                  {/* Blocks */}
                  {isDayRest ? (
                    <div className="py-6 text-center">
                      <span className="text-[10px] italic text-[#A8A29E] dark:text-zinc-500">Rest</span>
                    </div>
                  ) : dayBlocks.length === 0 ? (
                    <div className="py-6 text-center">
                      <span className="text-[10px] text-[#A8A29E] dark:text-zinc-500">—</span>
                    </div>
                  ) : (
                    <div className="space-y-1.5">
                      {dayBlocks.map((block, bi) => {
                        const blockId = getBlockId(block, bi);
                        const isCompleted = dayCompletions.includes(blockId);
                        const _subjectColor = getSubjectColor(block.subjectName);

                        return (
                          <button
                            key={blockId}
                            onClick={() => { setViewMode('day'); setSelectedDay(i); }}
                            className="w-full text-left rounded-lg transition-all hover:opacity-90 overflow-hidden"
                            style={{
                              backgroundColor: isCompleted ? 'rgba(107,143,113,0.1)' : getSubjectHexColor(block.subjectName),
                              borderRadius: 8,
                              opacity: isCompleted ? 0.6 : 1,
                            }}
                          >
                            <div className="px-2 py-1.5">
                              <span className={`text-[11px] font-bold truncate block ${isCompleted ? 'line-through' : ''}`} style={{ color: isCompleted ? '#6B8F71' : '#fff' }}>
                                {block.subjectName}
                              </span>
                              <span className="text-[9px] block" style={{ color: isCompleted ? '#6B8F71' : 'rgba(255,255,255,0.7)' }}>
                                {SESSION_TYPE_CONFIG[block.sessionType].label}
                              </span>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Priority Breakdown ── */}
      <div className="p-5 rounded-xl bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-xs uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">Priority Breakdown</h3>
          <button
            onClick={() => setShowExplainer(!showExplainer)}
            className="flex items-center gap-1.5 text-xs font-semibold transition-colors"
            style={{ color: '#2A7D6F' }}
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

      {/* ── Priority Explainer ── */}
      <AnimatePresence>
        {showExplainer && (
          <MotionDiv
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden"
          >
            <div className="p-5 rounded-xl space-y-6 bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
              {/* How it works */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-bold text-xs uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">How Your Timetable Is Built</h4>
                  <button onClick={() => setShowExplainer(false)} className="transition-colors text-[#A8A29E] dark:text-zinc-500">
                    <X size={16} />
                  </button>
                </div>
                <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed mb-4">
                  Each subject gets a <span className="font-bold" style={{ color: '#2A7D6F' }}>priority score</span> that determines how many study sessions it receives each week. The score combines two factors:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                  <div className="p-4 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: '#2A7D6F' }}>Points Gain</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      The CAO points difference between your target grade and current grade. Bigger gaps = more room to grow = higher priority.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: '#C4873B' }}>Efficiency Multiplier</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      Subjects where you're currently weaker get a boost. Going from H2 to H1 is much harder than H7 to H5 — your study time is better spent where grade jumps come more easily.
                    </p>
                  </div>
                </div>
                <div className="p-3 rounded-xl text-center" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                  <p className="text-xs font-mono font-bold text-zinc-600 dark:text-zinc-300">
                    Priority Score = Points Gain <span style={{ color: '#2A7D6F' }}>x</span> Difficulty Multiplier
                  </p>
                </div>
              </div>

              {/* Per-subject breakdown */}
              <div>
                <h4 className="font-bold text-xs uppercase tracking-widest mb-3 text-[#A8A29E] dark:text-zinc-500">Your Subject Scores</h4>
                <div className="space-y-2">
                  {priorities.map(p => {
                    const color = getSubjectColor(p.subjectName);
                    const maxPriority = Math.max(...priorities.map(pr => pr.priorityScore), 1);
                    const barPct = (p.priorityScore / maxPriority) * 100;

                    return (
                      <div key={p.subjectName} className="p-3 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <div className={`w-2.5 h-2.5 rounded-full ${color.dot} flex-shrink-0`} />
                            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{p.subjectName}</span>
                          </div>
                          <span className="text-sm font-mono font-bold" style={{ color: '#2A7D6F' }}>
                            {Math.round(p.priorityScore)}
                          </span>
                        </div>

                        {/* Score visualisation bar — uses subject colour */}
                        <div className="h-1.5 rounded-full overflow-hidden mb-2.5" style={{ backgroundColor: '#EDEAE6' }}>
                          <motion.div
                            className="h-full rounded-full"
                            style={{ backgroundColor: getSubjectHexColor(p.subjectName) }}
                            initial={{ width: 0 }}
                            animate={{ width: `${barPct}%` }}
                            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                          />
                        </div>

                        {/* Breakdown chips */}
                        <div className="flex flex-wrap items-center gap-2 text-[10px]">
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-semibold text-[#A8A29E] dark:text-zinc-500" style={{ backgroundColor: 'rgba(0,0,0,0.04)' }}>
                            {p.currentGrade} <ArrowRight size={8} /> {p.targetGrade}
                          </span>
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-bold" style={{ backgroundColor: 'rgba(42,125,111,0.1)', color: '#2A7D6F' }}>
                            +{p.pointsGain} pts{p.isMaths ? ' (incl. bonus)' : ''}
                          </span>
                          <span className="font-mono text-[#A8A29E] dark:text-zinc-500">x</span>
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-bold" style={{ backgroundColor: 'rgba(196,135,59,0.1)', color: '#C4873B' }}>
                            {p.difficultyMultiplier.toFixed(2)} efficiency
                          </span>
                          <span className="font-mono text-[#A8A29E] dark:text-zinc-500">=</span>
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full font-bold bg-[#FAF7F4] dark:bg-zinc-900" style={{ color: '#2A7D6F' }}>
                            {Math.round(p.priorityScore)}
                          </span>
                        </div>

                        {/* Explanation sentence */}
                        <p className="text-[10px] mt-2 leading-relaxed text-[#A8A29E] dark:text-zinc-500">
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

              {/* Projected CAO Points -- Best 6 */}
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
                    <div className="p-4 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                      <p className="text-[10px] font-bold uppercase tracking-widest mb-2" style={{ color: '#6B8F71' }}>Projected CAO Points (Best 6)</p>
                      <div className="flex items-baseline gap-2 mb-3">
                        <p className="text-4xl font-bold font-mono" style={{ color: '#2A7D6F' }}>{projectedTotal}</p>
                        <p className="text-sm font-semibold text-[#A8A29E] dark:text-zinc-500">/ 625</p>
                      </div>
                      <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                        If you hit your target grade in every subject, your <span className="font-bold">best 6</span> will total <span className="font-bold" style={{ color: '#2A7D6F' }}>{projectedTotal} points</span>. Only your top 6 subjects count for CAO.
                      </p>
                      <div className="mt-3 space-y-0">
                        {best6.map((s, i) => (
                          <div key={s.subjectName} className="flex items-center justify-between text-xs py-2 px-1" style={{ borderBottom: i < best6.length - 1 ? '0.5px solid rgba(0,0,0,0.05)' : 'none' }}>
                            <div className="flex items-center gap-2">
                              <span className="text-[10px] font-bold w-3 text-[#A8A29E] dark:text-zinc-500">{i + 1}.</span>
                              <div className={`w-2.5 h-2.5 rounded-full ${getSubjectColor(s.subjectName).dot}`} />
                              <span className="font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                              {s.isMaths && <span className="text-[9px] font-bold" style={{ color: '#2A7D6F' }}>+25</span>}
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="font-medium text-[#A8A29E] dark:text-zinc-500">{s.targetGrade}</span>
                              <span className="font-mono font-bold" style={{ color: '#2A7D6F' }}>{s.targetPoints}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Deprioritise suggestion */}
                    {deprioritiseCandidates.length > 0 && (
                      <div className="rounded-2xl overflow-hidden" style={{ backgroundColor: '#F59E0B', boxShadow: '0 4px 16px rgba(245,158,11,0.15)' }}>
                        {/* Amber header */}
                        <div className="relative px-5 pt-5 pb-4">
                          {/* Decorative blob */}
                          <div className="absolute pointer-events-none" style={{ top: -20, right: -15, width: 80, height: 80, borderRadius: '50%', background: 'rgba(255,255,255,0.1)' }} />
                          <div className="relative z-10">
                            <div className="flex items-center gap-2 mb-2">
                              <AlertTriangle size={16} style={{ color: 'rgba(0,0,0,0.5)' }} />
                              <p className="text-[11px] font-bold uppercase tracking-[0.1em]" style={{ color: 'rgba(0,0,0,0.5)' }}>Subjects Outside Your Best 6</p>
                            </div>
                            <p className="text-[13px] leading-relaxed" style={{ color: 'rgba(0,0,0,0.7)' }}>
                              Based on your target grades, <span className="font-bold" style={{ color: 'rgba(0,0,0,0.85)' }}>{deprioritiseCandidates.map(s => s.subjectName).join(' and ')}</span> {deprioritiseCandidates.length === 1 ? 'falls' : 'fall'} outside your top 6.
                            </p>
                          </div>
                        </div>

                        {/* Subject rows on white */}
                        <div className="bg-white mx-3 rounded-xl mb-3">
                          {deprioritiseCandidates.map((s, si) => (
                            <div key={s.subjectName} className="flex items-center justify-between text-xs px-3 py-2.5" style={{ borderBottom: si < deprioritiseCandidates.length - 1 ? '0.5px solid rgba(0,0,0,0.06)' : 'none' }}>
                              <div className="flex items-center gap-2">
                                <div className={`w-2.5 h-2.5 rounded-full ${getSubjectColor(s.subjectName).dot}`} />
                                <span className="font-semibold text-[#1A1A1A] dark:text-white">{s.subjectName}</span>
                              </div>
                              <span className="font-mono font-bold" style={{ color: '#92400E' }}>{s.targetGrade} — {s.targetPoints} pts</span>
                            </div>
                          ))}
                        </div>

                        {/* Warning callout on white */}
                        <div className="bg-white mx-3 mb-3 px-3 py-2.5 rounded-xl">
                          <p className="text-[10px] leading-relaxed" style={{ color: '#92400E' }}>
                            <span className="font-bold">High-risk strategy.</span> Only deprioritise a subject if you're confident you're significantly stronger in at least 6 others. The timetable still allocates minimum sessions to every subject for safety.
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })()}

              {/* Session count & intensity note */}
              <div className="p-4 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: '#2A7D6F' }}>Session Allocation</p>
                <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                  Sessions are split proportionally by priority score, with a minimum of 1 per subject. The total number of sessions per week ramps from <span className="font-bold">14</span> (2/day) to <span className="font-bold">21</span> (3/day) as exams approach. Right now you're at <span className="font-bold" style={{ color: '#2A7D6F' }}>{totalSessions} sessions</span> this week.
                </p>
              </div>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* ── Intensity indicator ── */}
      {weekOffset > 0 && (
        <div className="text-center">
          <p className="text-xs text-[#A8A29E] dark:text-zinc-500">
            Intensity: {Math.round(computeIntensityFactor(Math.max(0, weeksUntilExam - weekOffset)) * 100)}% — {
              Math.max(0, weeksUntilExam - weekOffset)
            } weeks to exam
          </p>
        </div>
      )}

      {/* ── Study Now / Already Studied modal ── */}
      <AnimatePresence>
        {blockActionModal && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[200] bg-black/40 flex items-center justify-center p-4"
            onClick={() => setBlockActionModal(null)}
          >
            <MotionDiv
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="w-full max-w-xs space-y-5 p-6"
              style={{ backgroundColor: '#fff', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 16 }}
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              {/* Block info */}
              <div className="text-center space-y-2">
                <div className="flex items-center justify-center gap-2">
                  <div className={`w-3 h-3 rounded-full ${getSubjectColor(blockActionModal.block.subjectName).dot}`} />
                  <h3 className="text-lg font-bold text-zinc-800 dark:text-white">{blockActionModal.block.subjectName}</h3>
                </div>
                <p className="text-sm text-[#A8A29E] dark:text-zinc-500">
                  {SESSION_TYPE_CONFIG[blockActionModal.block.sessionType].label} · {blockActionModal.block.durationMinutes} min
                </p>
              </div>

              {/* Actions */}
              <div className="space-y-3">
                <div className="flex justify-center">
                  <PrimaryActionButton label="Study Now" onClick={handleStudyNow} icon={Play} />
                </div>
                <button
                  onClick={handleAlreadyStudied}
                  className="w-full py-3 rounded-xl text-sm font-medium transition-all bg-[#FAF7F4] dark:bg-zinc-900 text-[#A8A29E] dark:text-zinc-500"
                  style={{ borderRadius: 12 }}
                >
                  Already Studied (+5 pts)
                </button>
                {onSpendPoints && points >= 20 && (
                  <button
                    onClick={handleSkipSession}
                    className="w-full py-3 rounded-xl text-sm font-medium transition-all text-[#2A7D6F]"
                    style={{ borderRadius: 12, backgroundColor: '#e8f5f2', border: '1px solid rgba(42,125,111,0.2)' }}
                  >
                    Skip Session (20 pts)
                  </button>
                )}
                <button
                  onClick={() => setBlockActionModal(null)}
                  className="w-full py-2 text-sm transition-colors text-[#A8A29E] dark:text-zinc-500"
                >
                  Cancel
                </button>
              </div>
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

export default SpacedRepetitionTimetable;
