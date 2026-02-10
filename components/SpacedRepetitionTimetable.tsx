/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChevronLeft, ChevronRight, BookOpen, RotateCcw, Target,
  Clock, Calendar, TrendingUp, Settings, HelpCircle, X, ArrowRight,
} from 'lucide-react';
import { type StudentSubjectProfile, type StudyBlock, DAYS_OF_WEEK } from './subjectData';
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

const StudyBlockCard: React.FC<{ block: StudyBlock }> = ({ block }) => {
  const color = getSubjectColor(block.subjectName);
  const typeConfig = SESSION_TYPE_CONFIG[block.sessionType];
  const TypeIcon = typeConfig.icon;

  return (
    <div className={`p-2 rounded-lg ${color.bg} border ${color.border} transition-colors`}>
      <div className="flex items-center gap-1.5 mb-0.5">
        <div className={`w-2 h-2 rounded-full ${color.dot} flex-shrink-0`} />
        <p className={`text-[10px] font-bold truncate ${color.text}`}>{block.subjectName}</p>
      </div>
      <div className="flex items-center gap-1 ml-3.5">
        <TypeIcon size={9} className="text-zinc-400 dark:text-zinc-500" />
        <span className="text-[9px] text-zinc-400 dark:text-zinc-500">{typeConfig.label}</span>
        <span className="text-[9px] text-zinc-300 dark:text-zinc-600 ml-auto">{block.durationMinutes}m</span>
      </div>
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

const SpacedRepetitionTimetable: React.FC<SpacedRepetitionTimetableProps> = ({ profile, onOpenSettings }) => {
  const [weekOffset, setWeekOffset] = useState(0);
  const [selectedDay, setSelectedDay] = useState(0); // For mobile view
  const [showExplainer, setShowExplainer] = useState(false);

  const weeksUntilExam = computeWeeksUntilExam(profile.examStartDate);

  const priorities = useMemo(() => computeSubjectPriorities(profile.subjects), [profile.subjects]);

  const allocations = useMemo(
    () => allocateSessions(priorities, Math.max(0, weeksUntilExam - weekOffset)),
    [priorities, weeksUntilExam, weekOffset]
  );

  const timetable = useMemo(
    () => generateWeeklyTimetable(allocations, weeksUntilExam, weekOffset),
    [allocations, weeksUntilExam, weekOffset]
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Spaced Repetition Timetable</h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            Week of {formatDateShort(weekStart)} — {formatDateShort(weekEnd)}
          </p>
        </div>
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

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30">
            <TrendingUp size={12} className="text-purple-600 dark:text-purple-400" />
            <span className="text-xs font-bold text-purple-600 dark:text-purple-400">{totalSessions} sessions</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700/30">
            <Clock size={12} className="text-blue-600 dark:text-blue-400" />
            <span className="text-xs font-bold text-blue-600 dark:text-blue-400">{totalHours}h {remainingMins}m</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700/30">
            <Calendar size={12} className="text-amber-600 dark:text-amber-400" />
            <span className="text-xs font-bold text-amber-600 dark:text-amber-400">{daysUntilExam} days left</span>
          </div>
        </div>

        <MotionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setWeekOffset(o => o + 1)}
          className="p-2 rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
        >
          <ChevronRight size={16} className="text-zinc-600 dark:text-zinc-300" />
        </MotionButton>
      </div>

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
                <StudyBlockCard key={bi} block={block} />
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
                  <StudyBlockCard key={bi} block={block} />
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
                    <p className="text-[10px] font-bold uppercase tracking-widest text-amber-600 dark:text-amber-400 mb-1">Difficulty Multiplier</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      Subjects where you're currently weaker get a boost. Moving from H7 to H5 is harder than H2 to H1 — the multiplier reflects this diminishing-returns curve.
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
                            {p.difficultyMultiplier.toFixed(2)} difficulty
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
                              ? `Currently at ${p.currentGrade}, so the difficulty multiplier is high (${p.difficultyMultiplier.toFixed(2)}) — each grade jump requires more effort from this starting point.`
                              : p.difficultyMultiplier >= 0.5
                                ? `At ${p.currentGrade}, the difficulty multiplier is moderate (${p.difficultyMultiplier.toFixed(2)}) — grade jumps are achievable but take consistent work.`
                                : `Starting from ${p.currentGrade}, the difficulty multiplier is lower (${p.difficultyMultiplier.toFixed(2)}) because improvement is relatively easier from a strong base.`
                          }
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

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
