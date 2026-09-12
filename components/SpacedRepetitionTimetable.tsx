/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ChevronLeft, ChevronRight, BookOpen, RotateCcw, Target, Settings, HelpCircle, X, ArrowRight, AlertTriangle, CalendarOff, Flame, CalendarDays, Play, type LucideIcon } from 'lucide-react';
import ToolMasthead from './launchpad/ToolMasthead';
import ModalFrame from './ui/ModalFrame';
import PrimaryActionButton from './ui/PrimaryActionButton';
import HorizontalTabs from './ui/HorizontalTabs';
import { type SchoolEvent } from './gc/GCKeyEvents';
import {
  type StudentSubjectProfile, type StudyBlock, DAYS_OF_WEEK, LC_SUBJECTS, getPointsForGrade,
  type TimetableCompletions, type TimetableStreak, getBlockId, toDateKey,
  computeBargains,
} from './subjectData';
import {
  computeSubjectPrioritiesForCurriculum,
  allocateSessions, generateWeeklyTimetable,
  computeWeeksUntilExam, computeIntensityFactor, computeWeeklyStudyTarget,
  type SessionAllocation, type SubjectSM2State,
} from './timetableAlgorithm';
import { useAuth } from '../contexts/AuthContext';
import { type DebriefEntry, computeStrategyHints, type SubjectStrategyHint } from './StudyDebrief';
import { COLORS } from '../design/tokens';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useInnovationData } from '../contexts/InnovationDataContext';
import { useOptionalProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { usePlanCues } from '../hooks/usePlanCues';
import { PLAN_TRIGGERS, PLAN_WHY, defaultThen } from '../planIntentionData';
import { getSubjectFill, SUBJECT_FILL_INK } from '../utils/subjectColors';

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
  onOpenJournal?: () => void;
  skippedSessions?: string[];
  onStudyNow?: (block: TimetableBlockInfo) => void;
  onBlockDurationChange?: (subjectName: string, sessionType: string, newDuration: number) => void;
  schoolEvents?: SchoolEvent[];
}

// ─── Subject colours: the shared ten-fill palette (utils/subjectColors) ───────

/** Block fills come from the shared ten-colour palette; every fill carries white text. */
const getSubjectHexColor = getSubjectFill;

// ─── Session Type Icons ─────────────────────────────────────────────────────

const SESSION_TYPE_CONFIG: Record<StudyBlock['sessionType'], { icon: LucideIcon; label: string }> = {
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
  block: StudyBlock; completed?: boolean; skipped?: boolean; onToggle?: () => void;
  bargainPts?: number; strategyHint?: SubjectStrategyHint; isToday?: boolean; hasStudyFlow?: boolean; onStudyNow?: () => void;
}> = ({ block, completed, skipped, onToggle, strategyHint, onStudyNow, hasStudyFlow }) => {
  const config = SESSION_TYPE_CONFIG[block.sessionType];
  const colour = getSubjectHexColor(block.subjectName);
  return <article className="lp-study-card" data-completed={completed || undefined}>
    <div className="lp-study-card-heading" style={{ backgroundColor: colour, color: SUBJECT_FILL_INK }}>
      <span>{config.label} · {block.durationMinutes} min</span><span>{skipped ? 'Skipped' : completed ? 'Completed' : 'Planned'}</span>
    </div>
    <div className="lp-study-card-body">
      <h3>{block.subjectName}</h3>
      {block.suggestedTopics?.length ? <p>{block.suggestedTopics.join(', ')}.</p> : <p>{config.label} at your own pace, one focused block at a time.</p>}
      {strategyHint && <p className="lp-study-hint">Try: {strategyHint.label}</p>}
      {!skipped && <div className="lp-action-row">
        {onStudyNow && !completed && <button className="lp-button" onClick={onStudyNow} aria-label={`Study ${block.subjectName} now`}>Start this block <ArrowRight size={17} /></button>}
        {onToggle && <button className={onStudyNow && !completed ? 'lp-study-secondary' : 'lp-button secondary'} onClick={onToggle} aria-label={`${completed ? 'Mark incomplete' : hasStudyFlow ? 'View block' : 'Mark complete'}: ${block.subjectName}, ${config.label}, ${block.durationMinutes} minutes`}>{completed ? 'Undo completion' : onStudyNow ? 'Block options' : hasStudyFlow ? 'View block' : 'Mark complete'} <ArrowRight size={16} /></button>}
      </div>}
    </div>
  </article>;
};

// ─── Priority Row ───────────────────────────────────────────────────────────

const _PRIORITY_BAR_COLORS: Record<string, string> = {
  High: '',
  Medium: '',
  Low: '',
};

const _PRIORITY_BAR_INLINE: Record<string, React.CSSProperties> = {
  High: { backgroundColor: COLORS.success },
  Medium: { backgroundColor: COLORS.success },
  Low: { backgroundColor: COLORS.success },
};

const PRIORITY_BADGE_INLINE: Record<string, React.CSSProperties> = {
  High: { backgroundColor: '#FDF3E7', color: '#C4873B' },
  Medium: { backgroundColor: COLORS.successTint, color: COLORS.success },
  Low: {},
};

const PRIORITY_BADGE_CLASS: Record<string, string> = {
  High: '',
  Medium: '',
  Low: 'bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700/40 text-[#A8A29E] dark:text-zinc-500',
};

const PriorityRow: React.FC<{ alloc: SessionAllocation; maxSessions: number }> = ({ alloc, maxSessions }) => {
  const barWidth = maxSessions > 0 ? (alloc.sessions / maxSessions) * 100 : 0;

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-2 w-28 flex-shrink-0">
        <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: getSubjectFill(alloc.subjectName) }} />
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

// ─── Per-block "if-then" cue editor (The Intention Engine) ───────────────────
// Self-contained so it re-seeds per block (keyed by blockId in the modal): pick a
// fixed situational trigger + write the "…then I'll…" line, bound to the block.
// Implementation intentions ~double follow-through (Gollwitzer & Sheeran 2006).
const BlockCueEditor: React.FC<{ subject: string; saved?: { trigger: string; then: string }; onSave: (cue: { trigger: string; then: string }) => void }> = ({ subject, saved, onSave }) => {
  const [open, setOpen] = useState(!!saved);
  const [trigger, setTrigger] = useState(saved?.trigger ?? PLAN_TRIGGERS[0]);
  const [thenText, setThenText] = useState(saved?.then ?? defaultThen(subject));
  const [savedOk, setSavedOk] = useState(!!saved);

  if (!open) {
    return (
      <button type="button" onClick={() => setOpen(true)} className="w-full py-2.5 rounded-xl text-sm font-semibold inline-flex items-center justify-center gap-1.5" style={{ backgroundColor: COLORS.accentTint, color: COLORS.accentDarkText, border: '1px solid rgba(242,107,31,0.2)' }}>
        + Add your if-then
      </button>
    );
  }
  return (
    <div className="rounded-xl p-3 text-left" style={{ backgroundColor: '#FFFFFF', border: '0.5px solid rgba(0,0,0,0.07)' }}>
      <p className="text-[10px] font-bold uppercase tracking-widest mb-2" style={{ color: COLORS.accentDarkText }}>Your if-then for this block</p>
      <div className="flex flex-wrap gap-1.5 mb-2">
        {PLAN_TRIGGERS.map(t => {
          const on = trigger === t;
          return (
            <button key={t} type="button" onClick={() => { setTrigger(t); setSavedOk(false); }} className="text-[11px] font-medium px-2 py-1 rounded-full transition-colors" style={on ? { backgroundColor: COLORS.accent, color: '#fff' } : { backgroundColor: '#fff', color: '#5a544e', border: '1px solid #d0cdc8' }}>
              {t}
            </button>
          );
        })}
      </div>
      <textarea value={thenText} onChange={e => { setThenText(e.target.value); setSavedOk(false); }} rows={2} className="w-full text-[13px] rounded-lg p-2 outline-none resize-none border" style={{ borderColor: '#d0cdc8', backgroundColor: '#fff', color: '#2a2622' }} placeholder="…then I’ll…" />
      <p className="text-[11px] italic mt-1.5" style={{ color: COLORS.accentDarkText }}>“{trigger}, {thenText}”</p>
      <button type="button" onClick={() => { onSave({ trigger, then: thenText.trim() }); setSavedOk(true); }} disabled={!thenText.trim()} className="w-full mt-2 py-2 rounded-lg text-[13px] font-bold text-white disabled:opacity-40" style={{ backgroundColor: COLORS.accent }}>
        {savedOk ? 'Saved' : 'Save my if-then'}
      </button>
      <p className="text-[10px] leading-snug mt-2" style={{ color: '#7a7068' }}>{PLAN_WHY.text} <span className="block mt-0.5" style={{ color: '#A8A29E' }}>{PLAN_WHY.source}</span></p>
    </div>
  );
};

const SpacedRepetitionTimetable: React.FC<SpacedRepetitionTimetableProps> = ({ profile, uid, onOpenSettings, onRestDaysChange, completions = {}, streak = { currentStreak: 0, lastActiveDate: '', longestStreak: 0 }, onToggleCompletion, onOpenJournal: _onOpenJournal, skippedSessions = [], onStudyNow, onBlockDurationChange: _onBlockDurationChange, schoolEvents = [] }) => {
  const { cues: planCues, setCue: setPlanCue } = usePlanCues(uid);
  // ─── Curriculum flags (Phase 2 JC support) ────────────────────────────────
  // isJunior: branch points-vs-bands UI and priority algorithm.
  // isPreExamJunior: 1st/2nd-year JC users have no imminent exam; we frame
  // the timetable as "weekly study plan" with no exam countdown ribbon.
  const { user } = useAuth();
  const progress = useOptionalProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const curriculumLevel = user?.curriculumLevel ?? profile.curriculumLevel ?? 'senior';
  const isJunior = curriculumLevel === 'junior';
  const yearGroup = user?.yearGroup ?? profile.yearGroup;
  const isPreExamJunior = isJunior && (yearGroup === '1st' || yearGroup === '2nd');

  const skippedSet = useMemo(() => new Set(skippedSessions), [skippedSessions]);
  const [showPlanSettings, setShowPlanSettings] = useState(false);
  const [weekOffset, setWeekOffset] = useState(0);
  const [showExplainer, setShowExplainer] = useState(false);
  // Four active days is the minimum needed to distribute a credible weekly
  // workload without turning one evening into a cramming session.
  const [restDays, setRestDays] = useState<Set<string>>(() => new Set((profile.restDays || []).slice(0, 3)));
  const [studyHoursRange, setStudyHoursRange] = useState<'week' | 'month' | 'all'>('week');
  const [blockActionModal, setBlockActionModal] = useState<{ block: StudyBlock; dayIndex: number; blockIndex: number } | null>(null);

  // Topic mastery from context -> feeds into timetable weighting
  const { topicMastery: topicMasteryHook } = useInnovationData();
  const topicMastery = topicMasteryHook.mastery;

  // Strategy hints from Learning DNA (per-subject best strategy)
  const [strategyHints, setStrategyHints] = useState<Record<string, SubjectStrategyHint>>({});
  const [sm2States, setSm2States] = useState<SubjectSM2State[]>([]);
  useEffect(() => {
    if (!uid) return;
    if (isDemo) {
      const data = progress?.rawProgressDoc.studyDebriefs as DebriefEntry[] | undefined;
      if (data) setStrategyHints(computeStrategyHints(data));
      else setStrategyHints({});
      setSm2States((progress?.rawProgressDoc.sm2States as SubjectSM2State[] | undefined) ?? []);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const progress = snap.data();
        const data = progress?.studyDebriefs as DebriefEntry[] | undefined;
        if (!cancelled) {
          if (data) setStrategyHints(computeStrategyHints(data));
          setSm2States((progress?.sm2States as SubjectSM2State[] | undefined) ?? []);
        }
      } catch (err) { console.error('Failed to load strategy hints:', err); }
    })();
    return () => { cancelled = true; };
  }, [uid, isDemo, progress?.rawProgressDoc.studyDebriefs, progress?.rawProgressDoc.sm2States]);

  const toggleRestDay = (day: string) => {
    setRestDays(prev => {
      const next = new Set(prev);
      if (next.has(day)) next.delete(day); else next.add(day);
      if (next.size > 3) return prev; // keep at least four active study days
      onRestDaysChange?.(Array.from(next));
      return next;
    });
  };

  // Pre-exam JC (1st/2nd year): no real exam countdown. The placeholder LC
  // June date that Phase 1 writes would yield a 22-month figure — meaningless
  // here. Synthesise a "school-term cadence" weeks value (~18 weeks ≈ one
  // term) so the intensity factor stays low and the sustainability caps
  // resolve to the "far from exams" base values. The UI ribbon below is
  // hidden for this case.
  const weeksUntilExam = isPreExamJunior
    ? 22 // school-term cadence: the lower building-phase workload
    : (profile.examStartDate ? computeWeeksUntilExam(profile.examStartDate) : 22);

  const priorities = useMemo(
    () => computeSubjectPrioritiesForCurriculum(profile.subjects, topicMastery, curriculumLevel, profile.examStartDate),
    [profile.subjects, topicMastery, curriculumLevel, profile.examStartDate]
  );

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
    return totalBlocks * (profile.defaultBlockDuration ?? 45);
  }, [completions, studyHoursRange, profile.defaultBlockDuration]);

  const studiedHours = Math.floor(studiedMinutes / 60);
  const studiedRemainingMins = studiedMinutes % 60;
  const studyHoursRangeLabel = studyHoursRange === 'week' ? 'this week' : studyHoursRange === 'month' ? 'this month' : 'all time';

  const blockDuration = profile.defaultBlockDuration ?? 45;
  const effectiveWeeksUntilExam = Math.max(0, weeksUntilExam - weekOffset);
  const weeklyTarget = useMemo(
    () => computeWeeklyStudyTarget(effectiveWeeksUntilExam),
    [effectiveWeeksUntilExam]
  );

  const allocations = useMemo(
    () => allocateSessions(priorities, effectiveWeeksUntilExam, sm2States, blockDuration),
    [priorities, effectiveWeeksUntilExam, sm2States, blockDuration]
  );

  const timetable = useMemo(
    () => generateWeeklyTimetable(allocations, weeksUntilExam, weekOffset, restDaysArray, blockDuration, sm2States, topicMastery),
    [allocations, weeksUntilExam, weekOffset, restDaysArray, blockDuration, sm2States, topicMastery]
  );

  const weekStart = getWeekStartDate(weekOffset);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6);

  const totalSessions = timetable.reduce((sum, day) => sum + day.blocks.length, 0);
  const totalMinutes = totalSessions * blockDuration;
  const totalHours = Math.floor(totalMinutes / 60);
  const remainingMins = totalMinutes % 60;

  const _daysUntilExam = profile.examStartDate
    ? Math.max(0, Math.ceil((new Date(profile.examStartDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)))
    : 0;
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

  // Today's completion stats
  const todayCompletedIds = completions[todayKey] ?? [];
  const todayBlocks = todaySchedule?.blocks ?? [];
  const todayCompletedCount = todayBlocks.filter((block, bi) => {
    const blockId = getBlockId(block, bi);
    return todayCompletedIds.includes(blockId);
  }).length;
  const todayTotalCount = todayBlocks.length;

  // "Next Up" -- first uncompleted session today

  // View mode: day-focused or week overview
  const [viewMode, setViewMode] = useState<'day' | 'week'>('day');
  // Day-focused view: selected day for both mobile and desktop
  const [selectedDay, setSelectedDay] = useState<number>(isCurrentWeek ? todayDayIndex : 0);

  if (!profile || profile.subjects.length === 0) {
    return (
      <div className="text-center py-16 space-y-4">
        <div className="w-16 h-16 mx-auto flex items-center justify-center bg-white dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
          <CalendarDays size={32} style={{ color: COLORS.accent }} />
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
    <div className="lp-planner space-y-5">
      <ToolMasthead tool="planner" eyebrow="The Planner" title="Your day, in order." subtitle={`${new Date().toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })} · ${todayTotalCount} ${todayTotalCount === 1 ? 'block' : 'blocks'} today.`} />
      <div className="lp-planner-layout"><section className="lp-planner-agenda space-y-5"><div className="flex items-center justify-between"><h2 className="lp-title">{selectedDay === todayDayIndex && isCurrentWeek ? 'Today' : DAYS_OF_WEEK[selectedDay]}</h2><button className="lp-button secondary" onClick={() => setShowPlanSettings(true)}><Settings size={15} /> Plan settings</button></div>
      <ModalFrame open={showPlanSettings} onClose={() => setShowPlanSettings(false)} title="Plan settings">
        <div className="p-5 space-y-5"><h3 className="lp-title">Make room for rest.</h3>
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
                className={`flex-1 py-1 rounded-md text-[10px] font-bold transition-all ${!isRest ? 'bg-white dark:bg-zinc-900 text-[#A8A29E] dark:text-zinc-500' : ''}`}
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
      <p className="text-[10px] text-[#A8A29E] dark:text-zinc-500 -mt-1">
        Choose up to three rest days. Keeping four active days lets us spread the work without overloading one evening.
      </p>

          <button className="lp-button secondary" onClick={() => { setShowPlanSettings(false); onOpenSettings(); }}>Edit subjects and grades <ArrowRight size={16} /></button>
        </div>
      </ModalFrame>
      {/* ── Week navigation + view toggle ── */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-zinc-600 dark:text-zinc-300">
            {formatDateShort(weekStart)} — {formatDateShort(weekEnd)}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setWeekOffset(o => o - 1)}
              aria-label="Previous timetable week"
              disabled={weekOffset <= 0}
              className="p-1.5 rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              style={{ backgroundColor: 'rgba(0,0,0,0.03)', borderRadius: 8 }}
            >
              <ChevronLeft size={14} className="text-zinc-500 dark:text-zinc-400" />
            </button>
            <button
              onClick={() => setWeekOffset(o => o + 1)}
              aria-label="Next timetable week"
              className="p-1.5 rounded-lg transition-colors"
              style={{ backgroundColor: 'rgba(0,0,0,0.03)', borderRadius: 8 }}
            >
              <ChevronRight size={14} className="text-zinc-500 dark:text-zinc-400" />
            </button>
          </div>
        </div>
        {/* Day / Week toggle */}
        <HorizontalTabs
          variant="pill"
          size="sm"
          label="Timetable view"
          value={viewMode}
          onChange={next => setViewMode(next as 'day' | 'week')}
          options={[{ value: 'day', label: 'Day' }, { value: 'week', label: 'Week' }]}
        />
      </div>

      {/* ── DAY VIEW ── */}
      {viewMode === 'day' && (<>
      {/* ── Day Tabs (horizontal pill selector) ── */}
      <div className="flex w-full items-center gap-1 overflow-x-auto rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-1">
        {DAY_SHORTS.map((day, i) => {
          const dayName = DAYS_OF_WEEK[i];
          const isDayRest = restDays.has(dayName);
          const isActive = selectedDay === i;
          const _isTodayTab = isCurrentWeek && i === todayDayIndex;


          return (
            <button
              key={day}
              onClick={() => setSelectedDay(i)}
              className={`flex-1 min-w-0 min-h-9 whitespace-nowrap rounded-lg border px-1 py-1.5 text-center text-[13px] font-semibold transition-colors ${
                isActive
                  ? 'border-[#1a1a1a] bg-[#1a1a1a] text-white [&_span]:text-white'
                  : 'border-transparent text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'
              }`}
            >
              <span className="block">
                <span className="relative inline-block">
                  {day}
                  {getEventsForDay(i).length > 0 && (
                    <span className="absolute -top-0.5 -right-1.5 w-1.5 h-1.5 rounded-full" style={{ backgroundColor: '#C4873B' }} />
                  )}
                </span>
              </span>
              <span className={`block text-[10px] font-medium mt-0.5 text-[var(--ink-muted)] ${isDayRest ? 'italic' : ''}`}>
                {new Date(weekStart.getFullYear(), weekStart.getMonth(), weekStart.getDate() + i).getDate()}
              </span>
            </button>
          );
        })}
      </div>

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
                  hasStudyFlow={Boolean(onStudyNow)}
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
        <span className="font-medium">
          {totalHours}h {remainingMins > 0 ? `${remainingMins}m ` : ''}planned
        </span>
        <span className="text-[#A8A29E] dark:text-zinc-500">·</span>
        <button
          onClick={() => setStudyHoursRange(r => r === 'week' ? 'month' : r === 'month' ? 'all' : 'week')}
          className="font-medium transition-colors cursor-pointer"
          style={{ color: COLORS.accent }}
          title="Click to cycle: this week / this month / all time"
        >
          {studiedHours}h {studiedRemainingMins}m completed {studyHoursRangeLabel}
        </button>
      </div>

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
                      style={isTodayCol ? { color: COLORS.accent } : undefined}
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
                              <span className={`text-[11px] font-bold truncate block ${isCompleted ? 'line-through' : ''}`} style={{ color: isCompleted ? '#4F7256' : SUBJECT_FILL_INK }}>
                                {block.subjectName}
                              </span>
                              <span className="text-[9px] block" style={{ color: isCompleted ? '#4F7256' : 'rgba(255,255,255,0.7)' }}>
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

      </section>
      {/* ── Why this week looks like this ── */}
      <div
        className="lp-planner-week lp-panel"
        style={{ backgroundColor: '#FFFFFF', border: '1px solid #D8D2CB' }}
      >
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] mb-1" style={{ color: COLORS.accent }}>
            This week's workload
          </p>
          <p className="text-lg font-bold text-[#1C1917] dark:text-white">
            {totalSessions} focused blocks · {totalHours}h{remainingMins > 0 ? ` ${remainingMins}m` : ''}
          </p>
          <p className="text-xs text-[#78716C] dark:text-zinc-300 mt-1 leading-relaxed">{weeklyTarget.explanation}</p>
        </div>
        <div className="lp-body mt-5 border-t border-[var(--outline-soft)] pt-5">
          <p>
            We balance work across your available days first, then space repeat sessions for the same subject apart.
            A weekend may carry one extra block, but one day should never absorb the whole week.
          </p>
          <p className="mt-2">
            {isJunior
              ? 'Subjects furthest below your target band receive more practice; every subject still receives maintenance time.'
              : 'Subjects with the strongest combination of grade gap, achievable marks and shaky topics receive more time; every subject still receives maintenance time.'}
          </p>
        </div>
      </div>

      </div>
      {/* ── Priority Breakdown ── */}
      <div className="p-5 rounded-xl bg-white dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-xs uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">Priority Breakdown</h3>
          {/* The deep-dive explainer is senior-only — it documents the CAO
              points-gain × efficiency formula, which doesn't apply to JC.
              JC priority is band-deficit driven and shown via session count
              in the list below. */}
          {!isJunior && (
            <button
              onClick={() => setShowExplainer(!showExplainer)}
              className="flex items-center gap-1.5 text-xs font-semibold transition-colors"
              style={{ color: COLORS.accent }}
            >
              <HelpCircle size={14} />
              {showExplainer ? 'Hide explanation' : 'How is this calculated?'}
            </button>
          )}
        </div>
        <div className="space-y-2.5">
          {allocations
            .sort((a, b) => b.sessions - a.sessions)
            .map(alloc => (
              <PriorityRow key={alloc.subjectName} alloc={alloc} maxSessions={maxSessions} />
            ))}
        </div>
      </div>

      {/* ── Priority Explainer ── (senior-only — CAO-points-flavoured) */}
      <AnimatePresence>
        {showExplainer && !isJunior && (
          <MotionDiv
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden"
          >
            <div className="p-5 rounded-xl space-y-6 bg-white dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
              {/* How it works */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-bold text-xs uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">How Your Timetable Is Built</h4>
                  <button onClick={() => setShowExplainer(false)} className="transition-colors text-[#A8A29E] dark:text-zinc-500">
                    <X size={16} />
                  </button>
                </div>
                <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed mb-4">
                  Each subject gets a <span className="font-bold" style={{ color: COLORS.accent }}>priority score</span> that determines how many study sessions it receives each week. The score combines two factors:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                  <div className="p-4 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: COLORS.accent }}>Best-six CAO gain</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      The CAO points difference between your target grade and current grade. Bigger gaps = more room to grow = higher priority.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: '#C4873B' }}>Efficiency Multiplier</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                      The timetable values points that would change your best-six total, then favours targets requiring fewer grade steps. Every subject still receives maintenance time.
                    </p>
                  </div>
                </div>
                <div className="p-3 rounded-xl text-center" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                  <p className="text-xs font-mono font-bold text-zinc-600 dark:text-zinc-300">
                    Priority = Best-six Gain <span style={{ color: COLORS.accent }}>x</span> Target Attainability <span style={{ color: COLORS.accent }}>x</span> Syllabus Need
                  </p>
                </div>
              </div>

              {/* Per-subject breakdown */}
              <div>
                <h4 className="font-bold text-xs uppercase tracking-widest mb-3 text-[#A8A29E] dark:text-zinc-500">Your Subject Scores</h4>
                <div className="space-y-2">
                  {priorities.map(p => {
                    const maxPriority = Math.max(...priorities.map(pr => pr.priorityScore), 1);
                    const barPct = (p.priorityScore / maxPriority) * 100;

                    return (
                      <div key={p.subjectName} className="p-3 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.6)', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: getSubjectFill(p.subjectName) }} />
                            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{p.subjectName}</span>
                          </div>
                          <span className="text-sm font-mono font-bold" style={{ color: COLORS.accent }}>
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
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-bold" style={{ backgroundColor: 'rgba(242,107,31,0.1)', color: COLORS.accent }}>
                            +{p.bestSixPointsGain ?? p.pointsGain} best-six pts{p.isMaths ? ' (incl. bonus)' : ''}
                          </span>
                          <span className="font-mono text-[#A8A29E] dark:text-zinc-500">x</span>
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-bold" style={{ backgroundColor: 'rgba(196,135,59,0.1)', color: '#C4873B' }}>
                            {p.difficultyMultiplier.toFixed(2)} attainability
                          </span>
                          <span className="font-mono text-[#A8A29E] dark:text-zinc-500">=</span>
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full font-bold bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700/40" style={{ color: COLORS.accent }}>
                            {Math.round(p.priorityScore)}
                          </span>
                        </div>

                        {/* Explanation sentence */}
                        <p className="text-[10px] mt-2 leading-relaxed text-[#A8A29E] dark:text-zinc-500">
                          {(p.bestSixPointsGain ?? p.pointsGain) === 0
                            ? `Already at your target — this subject receives minimum sessions to maintain.`
                            : `${p.currentGrade} → ${p.targetGrade} requires ${p.targetGradeSteps ?? 0} grade ${p.targetGradeSteps === 1 ? 'step' : 'steps'} and could add ${p.bestSixPointsGain ?? p.pointsGain} points to your present best-six total.`
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
                      <p className="text-[10px] font-bold uppercase tracking-widest mb-2" style={{ color: '#4F7256' }}>Projected CAO Points (Best 6)</p>
                      <div className="flex items-baseline gap-2 mb-3">
                        <p className="text-4xl font-bold font-mono" style={{ color: COLORS.accent }}>{projectedTotal}</p>
                        <p className="text-sm font-semibold text-[#A8A29E] dark:text-zinc-500">/ 625</p>
                      </div>
                      <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                        If you hit your target grade in every subject, your <span className="font-bold">best 6</span> will total <span className="font-bold" style={{ color: COLORS.accent }}>{projectedTotal} points</span>. Only your top 6 subjects count for CAO.
                      </p>
                      <div className="mt-3 space-y-0">
                        {best6.map((s, i) => (
                          <div key={s.subjectName} className="flex items-center justify-between text-xs py-2 px-1" style={{ borderBottom: i < best6.length - 1 ? '0.5px solid rgba(0,0,0,0.05)' : 'none' }}>
                            <div className="flex items-center gap-2">
                              <span className="text-[10px] font-bold w-3 text-[#A8A29E] dark:text-zinc-500">{i + 1}.</span>
                              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: getSubjectFill(s.subjectName) }} />
                              <span className="font-semibold text-zinc-700 dark:text-zinc-300">{s.subjectName}</span>
                              {s.isMaths && <span className="text-[9px] font-bold" style={{ color: COLORS.accent }}>+25</span>}
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="font-medium text-[#A8A29E] dark:text-zinc-500">{s.targetGrade}</span>
                              <span className="font-mono font-bold" style={{ color: COLORS.accent }}>{s.targetPoints}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Deprioritise suggestion */}
                    {deprioritiseCandidates.length > 0 && (
                      <div className="rounded-2xl overflow-hidden" style={{ backgroundColor: '#FFFFFF', border: '2px solid #1A1A1A' }}>
                        {/* Header — token system (was a banned raw-amber panel) */}
                        <div className="relative px-5 pt-5 pb-4">
                          <div className="flex items-center gap-2 mb-2">
                            <AlertTriangle size={16} style={{ color: COLORS.accent }} />
                            <p className="text-[11px] font-bold uppercase tracking-[0.1em]" style={{ color: COLORS.accentDarkText }}>Subjects Outside Your Best 6</p>
                          </div>
                          <p className="text-[13px] leading-relaxed text-zinc-600 dark:text-zinc-300">
                            Based on your target grades, <span className="font-bold text-[#1A1A1A] dark:text-white">{deprioritiseCandidates.map(s => s.subjectName).join(' and ')}</span> {deprioritiseCandidates.length === 1 ? 'falls' : 'fall'} outside your top 6.
                          </p>
                        </div>

                        {/* Subject rows on white */}
                        <div className="bg-white mx-3 rounded-xl mb-3">
                          {deprioritiseCandidates.map((s, si) => (
                            <div key={s.subjectName} className="flex items-center justify-between text-xs px-3 py-2.5" style={{ borderBottom: si < deprioritiseCandidates.length - 1 ? '0.5px solid rgba(0,0,0,0.06)' : 'none' }}>
                              <div className="flex items-center gap-2">
                                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: getSubjectFill(s.subjectName) }} />
                                <span className="font-semibold text-[#1A1A1A] dark:text-white">{s.subjectName}</span>
                              </div>
                              <span className="font-mono font-bold" style={{ color: COLORS.accentDarkText }}>{s.targetGrade} — {s.targetPoints} pts</span>
                            </div>
                          ))}
                        </div>

                        {/* Warning callout on white */}
                        <div className="bg-white mx-3 mb-3 px-3 py-2.5 rounded-xl">
                          <p className="text-[10px] leading-relaxed" style={{ color: COLORS.accentDarkText }}>
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
                <p className="text-[10px] font-bold uppercase tracking-widest mb-1" style={{ color: COLORS.accent }}>Session Allocation</p>
                <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
                  Sessions are split by priority score, with maintenance time retained for every subject. The recommended workload starts at about <span className="font-bold">6 focused hours</span> a week, rises gradually through the year and is capped at <span className="font-bold">12 hours</span> close to the exam. Your current week contains <span className="font-bold" style={{ color: COLORS.accent }}>{totalSessions} sessions · {totalHours}h{remainingMins > 0 ? ` ${remainingMins}m` : ''}</span>.
                </p>
              </div>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* ── Intensity indicator ── */}
      {/* Pre-exam JC (1st/2nd year) has no real exam countdown, so suppress
          the "weeks to exam" label entirely. 3rd-year JC and senior still
          see it; 3rd-year JC sees "Junior Cert" framing. */}
      {weekOffset > 0 && !isPreExamJunior && (
        <div className="text-center">
          <p className="text-xs text-[#A8A29E] dark:text-zinc-500">
            Intensity: {Math.round(computeIntensityFactor(Math.max(0, weeksUntilExam - weekOffset)) * 100)}% — {
              Math.max(0, weeksUntilExam - weekOffset)
            } weeks to {isJunior ? 'Junior Cert' : 'exam'}
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
            className="fixed inset-0 z-[200] bg-[#1A1A1A]/55 flex items-end sm:items-center justify-center p-0 sm:p-4"
            onClick={() => setBlockActionModal(null)}
          >
            <MotionDiv
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
              className="w-full max-w-sm space-y-5 rounded-t-[24px] border-[1.5px] border-[#383838] bg-white p-6 shadow-[5px_5px_0_0_#383838] sm:rounded-[24px] dark:border-zinc-600 dark:bg-zinc-900"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              {/* Block info */}
              <div className="text-center space-y-2">
                <div className="flex items-center justify-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: getSubjectFill(blockActionModal.block.subjectName) }} />
                  <h3 className="text-lg font-bold text-zinc-800 dark:text-white">{blockActionModal.block.subjectName}</h3>
                </div>
                <p className="text-sm text-[#A8A29E] dark:text-zinc-500">
                  {SESSION_TYPE_CONFIG[blockActionModal.block.sessionType].label} · {blockActionModal.block.durationMinutes} min
                </p>
              </div>

              {/* Bind a when-then cue to this block (The Intention Engine) */}
              <BlockCueEditor
                key={getBlockId(blockActionModal.block, blockActionModal.blockIndex)}
                subject={blockActionModal.block.subjectName}
                saved={planCues[getBlockId(blockActionModal.block, blockActionModal.blockIndex)]}
                onSave={(cue) => setPlanCue(getBlockId(blockActionModal.block, blockActionModal.blockIndex), cue)}
              />

              {/* Actions */}
              <div className="space-y-3">
                <div className="flex justify-center">
                  <PrimaryActionButton label="Study Now" onClick={handleStudyNow} icon={Play} />
                </div>
                <button
                  onClick={handleAlreadyStudied}
                  className="w-full py-3 rounded-xl border border-[#CFC9C2] text-sm font-medium transition-all bg-white dark:bg-zinc-900 text-[#6F6861] dark:text-zinc-400"
                >
                  Already studied (+5 JP)
                </button>
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
