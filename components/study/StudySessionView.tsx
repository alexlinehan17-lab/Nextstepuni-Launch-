/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, BookOpen, Target, RotateCcw, Play, Pause, Clock, Sparkles, X, ChevronRight, Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck, Trophy, CalendarCheck, type LucideIcon } from 'lucide-react';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import ChoiceControl from '../ui/ChoiceControl';
import { ResultStatGrid, StatusNotice } from '../ui/ProductPatterns';
import PointsExplainer from '../PointsExplainer';
import { doc, updateDoc, arrayUnion, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { saveInBackground } from '../../utils/firestoreWrite';
import { type SessionUser } from '../../utils/authUtils';
import { type StudentSubjectProfile } from '../subjectData';
import { type UserProgress, type StrategyMasteryMap, type MasteryTier, type StudyConfidenceLabel, type StudyReflection } from '../../types';
import { type CourseData } from '../Library';
import { STRATEGY_REGISTRY, PROMPT_AUTO_DISMISS_SECONDS } from '../../studySessionData';
import { type StreakData } from '../../hooks/useStreak';
import { useStudySession } from '../../hooks/useStudySession';
import { getSubjectColor, getSubjectHex, DURATION_PRESETS } from '../../studySessionData';
import StrategyPickerStep from './StrategyPickerStep';
import ReflectionModal from '../ReflectionModal';
import { QUICK_DEBRIEF_POINTS, FULL_REFLECTION_POINTS } from '../ReflectionModal';
import StudyJournalModal from '../StudyJournalModal';
import { type DebriefEntry } from '../StudyDebrief';
import { type WeeklyChallengeState } from '../../hooks/useWeeklyChallenge';
import { computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from '../timetableAlgorithm';
import { getBlockId, toDateKey } from '../subjectData';
import { processDebriefSideEffects } from '../../hooks/useDebriefSideEffects';
import { getSyllabusTopics } from '../syllabusTopics';
import { logError } from '../../utils/logError';

const TIER_COLORS: Record<MasteryTier, { text: string; bar: string }> = {
  none: { text: 'text-zinc-400 dark:text-zinc-500', bar: 'bg-zinc-200 dark:bg-zinc-700' },
  learned: { text: 'text-blue-500', bar: 'bg-blue-500' },
  practiced: { text: 'text-teal-500', bar: 'bg-teal-500' },
  applied: { text: 'text-amber-500', bar: 'bg-amber-500' },
  habitual: { text: 'text-purple-500', bar: 'bg-purple-500' },
};

const TIER_LABELS: Record<MasteryTier, string> = {
  none: 'Not Started', learned: 'Learned', practiced: 'Practiced', applied: 'Applied', habitual: 'Habitual',
};

const TIER_ORDER: MasteryTier[] = ['learned', 'practiced', 'applied', 'habitual'];

const CONFIDENCE_SCORE: Record<StudyConfidenceLabel, number> = {
  lost: 1,
  shaky: 2,
  okay: 3,
  good: 4,
  confident: 5,
};

const confidenceLabelFromScore = (score: number): StudyConfidenceLabel => {
  if (score <= 1) return 'lost';
  if (score === 2) return 'shaky';
  if (score === 3) return 'okay';
  if (score === 4) return 'good';
  return 'confident';
};

const STRATEGY_ICONS: Record<string, LucideIcon> = {
  'mastering-active-recall-protocol': Brain,
  'mastering-spaced-repetition-protocol': Repeat,
  'mastering-interleaving-protocol': Shuffle,
  'elaborative-interrogation-protocol': HelpCircle,
  'agency-protocol': Compass,
  'growth-mindset-protocol': Sprout,
  'digital-distraction-protocol': Shield,
  'learning-radar-protocol': Radar,
  'exam-hall-strategies-protocol': ClipboardCheck,
};

// Animated count-up number for points
const CountUpNumber: React.FC<{ value: number; delay?: number }> = ({ value, delay = 0 }) => {
  const [display, setDisplay] = React.useState(0);
  React.useEffect(() => {
    const timer = setTimeout(() => {
      const duration = 800;
      const start = performance.now();
      const step = (now: number) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        setDisplay(Math.round(eased * value));
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }, delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return <span className="text-3xl font-bold text-[var(--accent-hex)] tabular-nums">+{display}</span>;
};

const SESSION_TYPE_CONFIG: Record<string, { icon: LucideIcon; label: string }> = {
  'new-learning': { icon: BookOpen, label: 'New Learning' },
  'practice': { icon: Target, label: 'Practice' },
  'revision': { icon: RotateCcw, label: 'Revision' },
};

export interface TimetableBlockContext {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  dateKey: string;
  blockId: string;
}

interface StudySessionViewProps {
  user: SessionUser;
  studentProfile: StudentSubjectProfile | null;
  userProgress: UserProgress;
  allCourses: CourseData[];
  pointsReload: () => void;
  streak: StreakData;
  onBack: () => void;
  onStrategyMasteryRecompute?: () => Promise<void>;
  strategyMastery?: StrategyMasteryMap;
  onGoToTrainingHub?: () => void;
  dismissedGuides?: Record<string, string>;
  onDismissGuide?: (id: string) => void;
  weeklyChallenge?: WeeklyChallengeState;
  timetableBlock?: TimetableBlockContext | null;
  onTimetableBlockComplete?: (dateKey: string, blockId: string, actualMinutes: number) => void;
  todayBlocks?: TimetableBlockContext[];
  onStudyBlock?: (block: TimetableBlockContext) => void;
}

const StudySessionView: React.FC<StudySessionViewProps> = ({
  user,
  studentProfile,
  userProgress,
  allCourses,
  pointsReload,
  streak: _streak,
  onBack,
  onStrategyMasteryRecompute,
  strategyMastery,
  onGoToTrainingHub,
  dismissedGuides,
  onDismissGuide,
  weeklyChallenge,
  timetableBlock,
  onTimetableBlockComplete,
  todayBlocks = [],
  onStudyBlock,
}) => {
  const session = useStudySession(user.uid, userProgress, allCourses);

  // Setup selections — pre-fill from timetable block if provided
  const [selectedSubject, setSelectedSubject] = useState(timetableBlock?.subject ?? '');
  const [selectedType, setSelectedType] = useState<'new-learning' | 'practice' | 'revision' | ''>(timetableBlock?.sessionType ?? '');
  const [selectedMinutes, setSelectedMinutes] = useState<number>(timetableBlock?.durationMinutes ?? 0);
  const [_blockCompleteBanner, setBlockCompleteBanner] = useState<{ done: number; total: number } | null>(null);
  const [confirmQuit, setConfirmQuit] = useState(false);

  // Re-sync selections when timetable block changes
  useEffect(() => {
    if (timetableBlock) {
      setSelectedSubject(timetableBlock.subject);
      setSelectedType(timetableBlock.sessionType);
      setSelectedMinutes(timetableBlock.durationMinutes);
    }
  }, [timetableBlock]);

  // Strategy picker
  const [pickerDone, setPickerDone] = useState(false);
  const [selectedStrategies, setSelectedStrategies] = useState<string[]>([]);

  // Reflection modal
  const [reflectionOpen, setReflectionOpen] = useState(false);
  const [_debriefOpen, setDebriefOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Reflection journal (view past reflections)
  const [reflections, setReflections] = useState<StudyReflection[]>([]);
  const [journalOpen, setJournalOpen] = useState(false);
  const loadReflections = () => {
    if (!user.uid) return;
    getDoc(doc(db, 'progress', user.uid))
      .then(snap => setReflections((snap.data()?.reflections as StudyReflection[] | undefined) ?? []))
      .catch((e) => logError('StudySessionView.loadReflections', e));
  };

  // XP popup state

  // Previous debrief notes — surface "whatWorked" back to the student
  const [prevDebriefs, setPrevDebriefs] = useState<DebriefEntry[]>([]);
  useEffect(() => {
    if (!user.uid) return;
    let cancelled = false;
    getDoc(doc(db, 'progress', user.uid)).then(snap => {
      if (cancelled) return;
      const data = snap.data();
      if (data?.studyDebriefs) setPrevDebriefs(data.studyDebriefs);
      if (data?.reflections) setReflections(data.reflections as StudyReflection[]);
    }).catch((e) => logError('StudySessionView.loadPrevDebriefs', e));
    return () => { cancelled = true; };
  }, [user.uid]);

  // Get the most recent debrief note for the selected subject
  const lastSubjectNote = useMemo(() => {
    if (!selectedSubject || prevDebriefs.length === 0) return null;
    const subjectDebriefs = prevDebriefs
      .filter(d => d.subject === selectedSubject && d.whatWorked && d.whatWorked.trim().length > 0)
      .sort((a, b) => b.date.localeCompare(a.date));
    return subjectDebriefs[0] || null;
  }, [selectedSubject, prevDebriefs]);

  const subjects = studentProfile?.subjects ?? [];

  // Compute today's remaining timetable blocks for quick-start shortcuts
  const computedTodayBlocks = useMemo((): TimetableBlockContext[] => {
    if (!studentProfile || todayBlocks.length > 0) return todayBlocks;
    try {
      const today = new Date();
      const todayKey = toDateKey(today);
      const jsDay = today.getDay();
      const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;
      const priorities = computeSubjectPriorities(studentProfile.subjects, undefined, studentProfile.examStartDate);
      const weeksUntilExam = computeWeeksUntilExam(studentProfile.examStartDate);
      const allocations = allocateSessions(priorities, weeksUntilExam);
      const restDaysArray = studentProfile.restDays || [];
      const blockDuration = studentProfile.defaultBlockDuration ?? 45;
      const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDaysArray, blockDuration, undefined, undefined);
      const blocks = timetable[todayDayIndex]?.blocks ?? [];
      return blocks.map((block, bi) => ({
        subject: block.subjectName,
        sessionType: block.sessionType,
        durationMinutes: block.durationMinutes,
        dateKey: todayKey,
        blockId: getBlockId(block, bi),
      }));
    } catch (err) {
      console.error('Failed to build timetable blocks:', err);
      return [];
    }
  }, [studentProfile, todayBlocks]);

  const learnedStrategyIds = STRATEGY_REGISTRY
    .filter(s => {
      const course = allCourses.find(c => c.id === s.moduleId);
      const progress = userProgress[s.moduleId];
      return course && progress && progress.unlockedSection >= course.sectionsCount;
    })
    .map(s => s.moduleId);

  // Compute syllabus topics for the current session subject (used in debrief)
  const _debriefTopics = useMemo(() => {
    if (!session.subject) return [];
    return getSyllabusTopics(session.subject);
  }, [session.subject]);

  const canStart = selectedSubject && selectedType && selectedMinutes > 0;

  const handleStart = () => {
    if (!canStart || !selectedType) return;
    session.startSession(selectedSubject, selectedType, selectedMinutes);
  };

  // Auto-complete timetable block after saving session
  const completeTimetableBlock = () => {
    // Ending early still records the study session and opens reflection, but it
    // must not claim that the scheduled timetable block was completed.
    if (session.elapsedSeconds < session.totalDuration) return;
    if (timetableBlock && onTimetableBlockComplete) {
      const actualMinutes = Math.round(session.elapsedSeconds / 60);
      onTimetableBlockComplete(timetableBlock.dateKey, timetableBlock.blockId, actualMinutes);

      // Compute X/Y blocks done today for banner
      const _alreadyDone = todayBlocks.filter(b =>
        b.blockId === timetableBlock.blockId || b.blockId !== timetableBlock.blockId
      );
      // Count how many are done (this block is now done, others we don't know — but we can show total)
      const totalToday = todayBlocks.length;
      // We know at least this one is done, estimate from remaining
      const doneCount = todayBlocks.filter(b => b.blockId === timetableBlock.blockId).length;
      setBlockCompleteBanner({ done: doneCount, total: totalToday });
    }
  };

  const [reflectionMode, setReflectionMode] = useState<'quick' | 'full'>('quick');

  const handleSaveWithReflection = async (reflectionText: string) => {
    const bonus = reflectionMode === 'quick' ? QUICK_DEBRIEF_POINTS : FULL_REFLECTION_POINTS;
    const timestamp = Date.now();
    const [confidence, ...reflectionParts] = reflectionText.split('|');
    const confidenceCandidate = confidence.toLowerCase() as StudyConfidenceLabel;
    const confidenceLabel = Object.hasOwn(CONFIDENCE_SCORE, confidenceCandidate) ? confidenceCandidate : 'okay';
    const confidenceAfter = CONFIDENCE_SCORE[confidenceLabel] ?? 3;
    const writtenReflection = reflectionParts.join('|').trim();
    const journalText = writtenReflection
      || `${confidence.charAt(0).toUpperCase()}${confidence.slice(1)}`;
    const reflection: StudyReflection = {
      dateKey: toDateKey(new Date(timestamp)),
      blockId: timetableBlock?.blockId ?? `reflection_${timestamp}`,
      subjectName: session.subject,
      sessionType: session.sessionType,
      reflection: journalText,
      pointsEarned: bonus,
      timestamp,
      confidenceAfter,
      confidenceLabel,
      reflectionMode,
    };

    setIsSaving(true);
    try {
      setReflections(previous => [...previous, reflection]);
      // `setDoc(..., { merge: true })` also handles the rare case where a
      // student's parent progress document has not been created yet. Keep the
      // UI offline-safe: Firestore queues this locally and flushes on reconnect.
      saveInBackground(
        setDoc(doc(db, 'progress', user.uid), {
          reflections: arrayUnion(reflection),
        }, { merge: true }),
        'StudySessionView.saveReflection',
        () => setReflections(previous => previous.filter(entry => entry.timestamp !== timestamp)),
      );

      await session.saveSession(bonus, selectedStrategies, {
        confidenceAfter,
        confidenceLabel,
        reflectionMode,
      });
      completeTimetableBlock();
      pointsReload();
      onStrategyMasteryRecompute?.();
      weeklyChallenge?.reload();
      setReflectionOpen(false);
      setPickerDone(false);
      setSelectedStrategies([]);
      session.resetSession();
    } catch (error) {
      logError('StudySessionView.saveReflection', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSkipReflection = async () => {
    setIsSaving(true);
    await session.saveSession(0, selectedStrategies);
    completeTimetableBlock();
    pointsReload();
    onStrategyMasteryRecompute?.();
    weeklyChallenge?.reload();
    setIsSaving(false);
    setPickerDone(false);
    setSelectedStrategies([]);
    session.resetSession();
  };

  const _handleDebriefSubmit = async (entry: Omit<DebriefEntry, 'id' | 'date'>) => {
    setIsSaving(true);
    const fullEntry: DebriefEntry = {
      ...entry,
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
      date: toDateKey(new Date()),
    };
    // Save session first (with a small reflection bonus for completing debrief)
    await session.saveSession(10, selectedStrategies, {
      confidenceAfter: entry.confidenceAfter,
      confidenceLabel: confidenceLabelFromScore(entry.confidenceAfter),
      reflectionMode: 'full',
    });
    // Save debrief entry
    try {
      // Fired, not awaited: a student finishing a debrief on bad wifi would
      // otherwise never reach the completion screen below.
      saveInBackground(updateDoc(doc(db, 'progress', user.uid), {
        studyDebriefs: arrayUnion(fullEntry),
      }), 'StudySessionView.saveDebrief');
    } catch (err) {
      console.error('Failed to save debrief:', err);
    }
    // Process side effects: update topic mastery + SM-2 state
    processDebriefSideEffects(user.uid, fullEntry, studentProfile?.examStartDate)
      .catch(err => console.error('Debrief side effects error:', err));
    completeTimetableBlock();
    pointsReload();
    onStrategyMasteryRecompute?.();
    weeklyChallenge?.reload();
    setDebriefOpen(false);
    setIsSaving(false);
    setPickerDone(false);
    setSelectedStrategies([]);
    session.resetSession();
  };

  // ── Format time ──
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  // ── SVG ring calculations ──
  const ringRadius = 120;
  const ringCircumference = 2 * Math.PI * ringRadius;
  const progress = session.totalDuration > 0 ? session.elapsedSeconds / session.totalDuration : 0;
  const _ringOffset = ringCircumference * (1 - progress);
  const timeRemaining = Math.max(0, session.totalDuration - session.elapsedSeconds);

  // ── SETUP PHASE ──
  if (session.phase === 'idle') {
    return (
      <div className="min-h-screen bg-[#FAFBF6] dark:bg-zinc-950 flex flex-col">
        {/* ── Editorial header — replaces the old teal hero banner ── */}
        <div className="shrink-0 px-6 pt-6 max-w-md mx-auto w-full">
          <div className="flex items-center justify-between">
            <button
              onClick={onBack}
              aria-label="Back"
              className="w-10 h-10 rounded-xl flex items-center justify-center bg-white border border-[#EDEBE8] hover:bg-[#F8F4EC] transition-colors"
              style={{ boxShadow: '0 1px 2px rgba(28,25,23,0.04)' }}
            >
              <ArrowLeft size={18} className="text-[#1a1a1a]" />
            </button>
            <button
              onClick={() => { loadReflections(); setJournalOpen(true); }}
              className="inline-flex items-center gap-1.5 h-10 px-3.5 rounded-xl bg-white border border-[#EDEBE8] hover:bg-[#F8F4EC] transition-colors text-[13px] font-semibold text-[#1a1a1a]"
              style={{ boxShadow: '0 1px 2px rgba(28,25,23,0.04)' }}
            >
              <BookOpen size={15} className="text-[#1a1a1a]" />
              My reflections{reflections.length > 0 ? ` (${reflections.length})` : ''}
            </button>
          </div>

          <div className="flex items-center gap-4 md:gap-5 mt-7">
            {/* Painted blob + hand-drawn study icon */}
            <div className="relative shrink-0" style={{ width: 96, height: 96 }}>
              <svg
                className="absolute pointer-events-none"
                viewBox="0 0 100 100"
                aria-hidden="true"
                preserveAspectRatio="xMidYMid meet"
                style={{
                  width: '92%',
                  height: '92%',
                  left: '50%',
                  top: '50%',
                  transform: 'translate(-50%, -50%)',
                  zIndex: 0,
                }}
              >
                <path
                  d="M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z"
                  fill="#B8DDC8"
                  opacity="0.85"
                />
              </svg>
              <img
                src="/assets/study/study-session.png"
                alt=""
                style={{
                  position: 'absolute',
                  left: '50%',
                  top: '50%',
                  transform: 'translate(-50%, -50%)',
                  width: '126%',
                  height: '126%',
                  objectFit: 'contain',
                  zIndex: 1,
                }}
                draggable={false}
              />
            </div>

            {/* Title + subtitle */}
            <div className="min-w-0">
              <h1
                style={{
                  fontFamily: "'Source Serif 4', serif",
                  fontSize: 'clamp(32px, 6vw, 44px)',
                  fontWeight: 500,
                  letterSpacing: '-0.6px',
                  lineHeight: 1.05,
                  color: '#1a1a1a',
                  margin: 0,
                }}
              >
                Study Session
              </h1>
              <p
                style={{
                  fontFamily: "'DM Sans', system-ui, sans-serif",
                  fontSize: 14,
                  color: 'rgba(0,0,0,0.55)',
                  margin: 0,
                  marginTop: 6,
                }}
              >
                {session.todaySessions.length > 0
                  ? `${session.todaySessions.length} session${session.todaySessions.length !== 1 ? 's' : ''} today · ${session.todayTotalMinutes} min total`
                  : 'Choose a subject and start studying'}
              </p>
            </div>
          </div>
        </div>

        {/* Centered content */}
        <div className="flex-1 px-6 pb-28 bg-[#FAFBF6] dark:bg-zinc-950">
          <div className="w-full max-w-md mx-auto space-y-10 pt-6">
            {/* First-visit intro card */}
            <AnimatePresence>
              {!dismissedGuides?.['study-session-intro'] && (
                <MotionDiv
                  key="study-session-intro"
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8, transition: { duration: 0.2 } }}
                  className="rounded-2xl p-5 mb-6 bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800"
                  style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}
                >
                  <div className="flex items-start gap-3">
                    <Sparkles size={18} className="text-[#F26B1F] shrink-0 mt-0.5" />
                    <div className="space-y-2">
                      <p className="font-semibold text-sm text-[#1A1A1A] dark:text-white">Welcome to Study Sessions</p>
                      <p className="text-sm text-[#78716C] dark:text-zinc-400 leading-relaxed">
                        During sessions you'll see strategy prompts from modules you've completed. Tap "Done" to track your engagement — this feeds your mastery progress visible below.
                      </p>
                      <button
                        onClick={() => onDismissGuide?.('study-session-intro')}
                        className="mt-1 text-sm font-medium hover:underline"
                        style={{ color: '#F26B1F' }}
                      >
                        Got it
                      </button>
                    </div>
                  </div>
                </MotionDiv>
              )}
            </AnimatePresence>

            {/* Today's timetable blocks — quick-start shortcuts */}
            {computedTodayBlocks.length > 0 && (
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Today's Timetable</p>
                <div className="space-y-2">
                  {computedTodayBlocks.map((block) => {
                    const colors = getSubjectColor(block.subject);
                    const typeConfig = SESSION_TYPE_CONFIG[block.sessionType];
                    const TypeIcon = typeConfig.icon;
                    return (
                      <button
                        key={block.blockId}
                        onClick={() => {
                          if (onStudyBlock) {
                            onStudyBlock(block);
                          } else {
                            // Pre-fill selections from the block
                            setSelectedSubject(block.subject);
                            setSelectedType(block.sessionType);
                            setSelectedMinutes(block.durationMinutes);
                          }
                        }}
                        className="group w-full min-h-[68px] flex items-center gap-3.5 px-4 py-3 rounded-2xl text-left bg-white dark:bg-zinc-900 border border-[#E5E1DB] dark:border-zinc-700 transition-[border-color,box-shadow,transform] hover:border-[rgba(var(--accent),0.28)] hover:shadow-[0_6px_18px_rgba(28,25,23,0.06)] active:translate-y-px focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.38)] focus-visible:ring-offset-2"
                      >
                        <span className={`w-1.5 self-stretch min-h-10 rounded-full ${colors.dot} shrink-0 opacity-85`} />
                        <div className="flex-1 min-w-0">
                          <span className="text-[14px] font-semibold block text-[var(--text-primary)]">{block.subject}</span>
                          <span className="mt-1 text-xs text-[var(--text-muted)] flex items-center gap-1.5">
                            <TypeIcon size={14} strokeWidth={1.8} />
                            {typeConfig.label} · {block.durationMinutes}m
                          </span>
                        </div>
                        <span className="shrink-0 inline-flex items-center gap-1.5 rounded-full bg-[var(--accent-hex)] px-3 py-2 text-xs font-semibold text-white shadow-[0_3px_0_var(--accent-dark-hex)] transition-transform group-hover:-translate-y-0.5 group-active:translate-y-0">
                          <Play size={13} fill="currentColor" strokeWidth={2} />
                          <span className="hidden sm:inline">Start</span>
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Subject picker */}
            <div className="space-y-3">
              <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Subject</p>
              <div className="flex flex-wrap gap-2">
                {subjects.map(s => {
                  const colors = getSubjectColor(s.subjectName);
                  const isActive = selectedSubject === s.subjectName;
                  return (
                    <ChoiceControl
                      key={s.subjectName}
                      onClick={() => setSelectedSubject(s.subjectName)}
                      label={s.subjectName}
                      selected={isActive}
                      markerClassName={colors.dot}
                    />
                  );
                })}
                {subjects.length === 0 && (
                  <p className="text-sm text-zinc-400 dark:text-zinc-500">No subjects set up yet. Complete onboarding first.</p>
                )}
              </div>
            </div>

            {/* Last session note — surfaces whatWorked from previous debrief */}
            <AnimatePresence>
              {lastSubjectNote && selectedSubject && (
                <MotionDiv
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="overflow-hidden"
                >
                  <div className="px-4 py-3 rounded-xl bg-[#FAF7F4] dark:bg-zinc-900" style={{ border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-1.5 text-[#A8A29E] dark:text-zinc-500">Last time you studied {selectedSubject}</p>
                    <p className="text-xs text-zinc-600 dark:text-zinc-400 italic leading-relaxed">"{lastSubjectNote.whatWorked}"</p>
                  </div>
                </MotionDiv>
              )}
            </AnimatePresence>

            {/* Session type + Duration — side by side */}
            <div className="grid grid-cols-2 gap-8">
              {/* Session type */}
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Type</p>
                <div className="space-y-2">
                  {(['new-learning', 'practice', 'revision'] as const).map(type => {
                    const config = SESSION_TYPE_CONFIG[type];
                    const Icon = config.icon;
                    const isActive = selectedType === type;
                    return (
                      <ChoiceControl
                        key={type}
                        onClick={() => setSelectedType(type)}
                        className="w-full justify-start"
                        label={config.label}
                        selected={isActive}
                        icon={<Icon size={17} strokeWidth={isActive ? 2 : 1.75} />}
                      />
                    );
                  })}
                </div>
              </div>

              {/* Duration */}
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Duration</p>
                <div className="space-y-2">
                  {DURATION_PRESETS.map(preset => {
                    const isActive = selectedMinutes === preset.minutes;
                    return (
                      <ChoiceControl
                        key={preset.minutes}
                        onClick={() => setSelectedMinutes(preset.minutes)}
                        className="w-full"
                        label={`${preset.minutes} min`}
                        selected={isActive}
                      />
                    );
                  })}
                  {/* Custom duration input */}
                  <div className="relative">
                    {(() => {
                      const isCustomActive = !DURATION_PRESETS.some(p => p.minutes === selectedMinutes) && selectedMinutes > 0;
                      return (
                        <>
                          <input
                            type="number"
                            min={5}
                            max={180}
                            placeholder="Custom"
                            value={isCustomActive ? selectedMinutes : ''}
                            onChange={(e) => {
                              const v = parseInt(e.target.value, 10);
                              if (!isNaN(v) && v >= 1 && v <= 180) setSelectedMinutes(v);
                              else if (e.target.value === '') setSelectedMinutes(0);
                            }}
                            className={`w-full px-4 py-3 rounded-xl text-[13px] font-semibold text-center transition-all outline-none ${
                              isCustomActive
                                ? 'bg-[rgba(var(--accent),0.08)] text-[var(--accent-hex)] border border-[rgba(var(--accent),0.25)] ring-1 ring-inset ring-[rgba(var(--accent),0.15)]'
                                : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 border border-dashed border-zinc-300 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-600'
                            }`}
                          />
                          <span className={`absolute right-3 top-1/2 -translate-y-1/2 text-[11px] pointer-events-none ${isCustomActive ? 'text-[var(--accent-hex)] opacity-60' : 'text-zinc-400'}`}>min</span>
                        </>
                      );
                    })()}
                  </div>
                </div>
              </div>
            </div>

            {/* Start button */}
            <div className="flex justify-center">
              <PrimaryActionButton label="Start Session" onClick={handleStart} icon={Play} disabled={!canStart} />
            </div>

            {/* Strategy Mastery Summary */}
            {strategyMastery && Object.keys(strategyMastery).length > 0 && (
              <div className="space-y-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">Strategy Mastery</p>
                <div className="space-y-2">
                  {STRATEGY_REGISTRY.map(strategy => {
                    const record = strategyMastery[strategy.moduleId];
                    const tier = record?.tier ?? 'none';
                    const tierIndex = TIER_ORDER.indexOf(tier);
                    const colors = TIER_COLORS[tier];
                    const Icon = STRATEGY_ICONS[strategy.moduleId] || Brain;

                    return (
                      <div key={strategy.moduleId} className="flex items-center gap-3">
                        <Icon size={14} className={colors.text} />
                        <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400 w-24 truncate">{strategy.strategyName}</span>
                        <div className="flex-1 grid grid-cols-4 gap-0.5">
                          {TIER_ORDER.map((t, i) => (
                            <div
                              key={t}
                              className={`h-1.5 rounded-full ${i <= tierIndex ? (
                                t === 'learned' ? 'bg-blue-500'
                                : t === 'practiced' ? 'bg-teal-500'
                                : t === 'applied' ? 'bg-amber-500'
                                : 'bg-purple-500'
                              ) : 'bg-zinc-200 dark:bg-zinc-700'}`}
                            />
                          ))}
                        </div>
                        <span className={`text-[10px] font-semibold w-16 text-right ${colors.text}`}>{TIER_LABELS[tier]}</span>
                      </div>
                    );
                  })}
                </div>
                {onGoToTrainingHub && (
                  <button
                    onClick={onGoToTrainingHub}
                    className="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-xs font-medium text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-colors"
                  >
                    View all in Training Hub
                    <ChevronRight size={12} />
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Points Explainer (first visit) */}
        <PointsExplainer
          isOpen={!dismissedGuides?.['points-explainer']}
          onDismiss={() => onDismissGuide?.('points-explainer')}
        />

        {/* Reflection journal — view past reflections */}
        <StudyJournalModal
          isOpen={journalOpen}
          onClose={() => setJournalOpen(false)}
          reflections={reflections}
        />
      </div>
    );
  }

  // ── ACTIVE / PAUSED PHASE ──
  if (session.phase === 'active' || session.phase === 'paused') {
    const subjectHex = getSubjectHex(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];

    const lightenHex = (hex: string, amount: number) => {
      const red = parseInt(hex.slice(1, 3), 16);
      const green = parseInt(hex.slice(3, 5), 16);
      const blue = parseInt(hex.slice(5, 7), 16);
      const channel = (value: number) => Math.min(255, value + amount).toString(16).padStart(2, '0');
      return `#${channel(red)}${channel(green)}${channel(blue)}`;
    };

    const colourBands = [
      { scale: 1, top: '61%', lighten: 0 },
      { scale: 1.34, top: '54%', lighten: 15 },
      { scale: 1.7, top: '47%', lighten: 29 },
      { scale: 2.08, top: '40%', lighten: 43 },
    ];

    const handleQuit = () => {
      session.endSession();
      setConfirmQuit(false);
    };

    return (
      <div
        className="fixed inset-0 z-[100] flex flex-col"
        style={{ background: lightenHex(subjectHex, 58) }}
      >
        <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
          {[...colourBands].reverse().map((band, index) => (
            <motion.div
              key={band.lighten}
              className="absolute left-1/2 rounded-[50%]"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{
                scale: session.phase === 'paused' ? band.scale * 0.84 : band.scale,
                top: session.phase === 'paused' ? `calc(${band.top} + 4%)` : band.top,
                opacity: 1,
              }}
              transition={{ duration: 0.9, delay: index * 0.06, ease: [0.16, 1, 0.3, 1] }}
              style={{
                width: '140vw',
                height: '140vw',
                transform: 'translateX(-50%)',
                backgroundColor: lightenHex(subjectHex, band.lighten),
              }}
            />
          ))}
        </div>

        {/* Top bar — X button + subject info */}
        <div className="relative z-20 flex items-center justify-between px-5 py-4">
          <button
            onClick={() => setConfirmQuit(true)}
            aria-label="Leave study session"
            className="w-10 h-10 rounded-full flex items-center justify-center transition-all hover:bg-black/10"
          >
            <X size={18} className="text-[#3A3530]" />
          </button>
          <div className="flex items-center gap-2 text-xs font-semibold text-[#292522]">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: subjectHex }} />
            {typeConfig.label}
          </div>
        </div>

        {/* Title area */}
        <div className="relative z-20 text-center mt-10 px-6">
          <motion.h1
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="font-serif text-3xl md:text-4xl font-bold"
            style={{ color: '#1A1A1A' }}
          >
            {session.subject}
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="text-xs mt-2 font-bold uppercase tracking-[0.16em]"
            style={{ color: 'rgba(26,26,26,.68)' }}
          >
            {typeConfig.label} · {Math.ceil(session.totalDuration / 60)} min
          </motion.p>
        </div>

        {/* Center — giant play/pause */}
        <div className="relative z-20 flex-1 flex flex-col items-center justify-center px-6">
          <motion.p
            initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
            className="font-mono text-6xl md:text-7xl font-bold tabular-nums tracking-[-0.06em] text-[#1A1A1A] mb-3"
          >
            {formatTime(timeRemaining)}
          </motion.p>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-[#292522] mb-8">
            {session.phase === 'paused' ? 'Session paused' : 'Time remaining'}
          </p>
          <motion.button
            onClick={session.phase === 'active' ? session.pauseSession : session.resumeSession}
            className="relative w-20 h-20 md:w-24 md:h-24 rounded-full flex items-center justify-center bg-[#383431] text-white shadow-[0_16px_36px_rgba(38,32,27,.18)]"
            animate={{ scale: session.phase === 'paused' ? 0.92 : 1 }}
            whileHover={{ scale: session.phase === 'paused' ? 0.96 : 1.04 }}
            whileTap={{ scale: 0.9 }}
          >
            {session.phase === 'active' ? (
              <Pause size={30} />
            ) : (
              <Play size={30} style={{ marginLeft: 3 }} />
            )}
          </motion.button>
        </div>

        {/* Bottom — progress bar + times */}
        <div className="relative z-20 px-6 pb-8 pt-4">
          {/* Paused label — absolute so it doesn't shift layout */}
          <AnimatePresence>
            {session.phase === 'paused' && !session.currentPrompt && (
              <MotionDiv
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute left-0 right-0 -top-6 text-center pointer-events-none"
              >
                <span
                  className="text-xs font-bold uppercase tracking-[0.25em]"
                  style={{ color: 'rgba(26,26,26,.68)' }}
                >
                  Paused
                </span>
              </MotionDiv>
            )}
          </AnimatePresence>

          {/* Progress track */}
          <div className="relative w-full max-w-lg mx-auto">
            <div
              className="w-full h-1 rounded-full overflow-hidden"
              style={{ backgroundColor: 'rgba(26,26,26,.16)' }}
            >
              <motion.div
                className="h-full rounded-full"
                style={{
                  backgroundColor: 'rgba(26,26,26,.58)',
                  width: `${Math.min(100, progress * 100)}%`,
                  transition: 'width 1s ease',
                }}
              />
            </div>
            {/* Scrubber dot */}
            <div
              className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full"
              style={{
                left: `${Math.min(100, progress * 100)}%`,
                transform: `translate(-50%, -50%)`,
                backgroundColor: '#1A1A1A',
                transition: 'left 1s ease',
              }}
            />
          </div>

          {/* Elapsed / Remaining */}
          <div className="flex justify-between mt-3 max-w-lg mx-auto">
            <span
              className="text-xs font-medium tabular-nums"
              style={{ color: 'rgba(26,26,26,.72)' }}
            >
              {formatTime(session.elapsedSeconds)} elapsed
            </span>
            <span
              className="text-xs font-medium tabular-nums"
              style={{ color: 'rgba(26,26,26,.72)' }}
            >
              {formatTime(timeRemaining)} remaining
            </span>
          </div>
        </div>

        {/* Coaching prompts — overlay from bottom */}
        <AnimatePresence mode="wait">
          {/* Coaching prompt */}
          {session.currentPrompt && (
            <MotionDiv
              key={session.currentPrompt.prompt}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="fixed bottom-16 left-4 right-4 z-30 max-w-md mx-auto"
            >
              <div
                className="rounded-2xl p-4 overflow-hidden relative"
                style={{
                  backgroundColor: '#FFFFFF',
                  border: '1.5px solid #383838',
                  boxShadow: '0 14px 34px rgba(38,32,27,.12)',
                }}
              >
                {/* Auto-dismiss countdown bar */}
                <motion.div
                  className="absolute top-0 left-0 h-0.5 rounded-full"
                  style={{ backgroundColor: 'rgba(0,0,0,0.15)' }}
                  initial={{ width: '100%' }}
                  animate={{ width: '0%' }}
                  transition={{ duration: PROMPT_AUTO_DISMISS_SECONDS, ease: 'linear' }}
                />
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles size={14} style={{ color: subjectHex }} />
                  <span className="text-[10px] font-bold uppercase tracking-widest" style={{ color: subjectHex }}>
                    {session.currentPrompt.strategyName}
                  </span>
                </div>
                <p className="text-sm leading-relaxed" style={{ color: 'rgba(0,0,0,0.7)' }}>
                  {session.currentPrompt.prompt}
                </p>
                <div className="flex items-center gap-3 mt-3">
                  <button
                    onClick={session.completePrompt}
                    className="text-xs font-semibold transition-colors"
                    style={{ color: subjectHex }}
                  >
                    Done
                  </button>
                  <button
                    onClick={session.dismissPrompt}
                    className="text-xs transition-colors"
                    style={{ color: 'rgba(0,0,0,0.35)' }}
                  >
                    Skip
                  </button>
                </div>
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {confirmQuit && (
            <MotionDiv
              className="fixed inset-0 z-[200] flex items-end sm:items-center justify-center bg-[#1A1A1A]/55 p-0 sm:p-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              role="dialog"
              aria-modal="true"
              aria-labelledby="study-exit-title"
            >
              <MotionDiv
                initial={{ opacity: 0, y: 12, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.98 }}
                transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
                className="w-full max-w-sm rounded-t-[24px] sm:rounded-[24px] border-[1.5px] border-[#383838] bg-[#FAFBF6] p-6 shadow-[5px_5px_0_0_#383838]"
              >
                <p className="mb-2 text-[10px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">Leave session</p>
                <h2 id="study-exit-title" className="font-serif text-2xl font-bold text-[#1A1A1A]">End this study session?</h2>
                <p className="mt-2 text-sm leading-relaxed text-[#7A7068]">The time from this unfinished session won’t be recorded.</p>
                <div className="mt-6 grid gap-2">
                  <button
                    type="button"
                    onClick={() => setConfirmQuit(false)}
                    className="min-h-12 rounded-xl border-2 border-[#1A1A1A] bg-[#F26B1F] px-4 font-semibold text-white shadow-[3px_3px_0_0_#1A1A1A] transition-transform active:translate-x-[3px] active:translate-y-[3px] active:shadow-none"
                  >
                    Keep studying
                  </button>
                  <button
                    type="button"
                    onClick={handleQuit}
                    className="min-h-12 rounded-xl border border-[#D0CDC8] bg-white px-4 font-semibold text-[#3A3530] hover:bg-[#F8F4EC]"
                  >
                    End session
                  </button>
                </div>
              </MotionDiv>
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>
    );
  }

  // ── COMPLETE PHASE ──
  if (session.phase === 'complete') {
    // Show strategy picker before stats — all strategies shown regardless of module completion
    if (!pickerDone) {
      return (
        <StrategyPickerStep
          learnedStrategyIds={learnedStrategyIds}
          autoTrackedIds={session.getTrackedStrategies()}
          subject={session.subject}
          durationSeconds={session.elapsedSeconds}
          pointsEarned={session.basePointsEarned}
          onContinue={(ids) => {
            setSelectedStrategies(ids);
            setPickerDone(true);
          }}
          onSkip={() => {
            setSelectedStrategies([]);
            setPickerDone(true);
          }}
        />
      );
    }

    const subjectColors = getSubjectColor(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];
    const actualMinutes = Math.round(session.elapsedSeconds / 60);
    const isEarlyEnd = session.elapsedSeconds < session.totalDuration;

    return (
      <div className="min-h-screen bg-[#FAF9F7] dark:bg-zinc-950 flex flex-col items-center justify-center px-4 py-12">
        <MotionDiv
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="w-full max-w-lg space-y-6 rounded-[24px] border-[1.5px] border-[#383838] bg-[#FAFBF6] p-6 shadow-[5px_5px_0_0_#383838] sm:p-8"
        >
          {/* Header — points as hero */}
          <div className="text-center">
            <MotionDiv
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
              className={`mx-auto mb-5 flex h-[76px] w-[76px] items-center justify-center rounded-full border-2 border-[#383838] shadow-[3px_3px_0_0_#383838] ${isEarlyEnd ? 'bg-[#FFF0E7] text-[#F26B1F]' : 'bg-[#E8F2EC] text-[#3A8D5F]'}`}
            >
              <svg width="38" height="38" viewBox="0 0 40 40" fill="none" aria-hidden="true">
                <path d="M10 20.5l6.5 6.5L30.5 13" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </MotionDiv>
            <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-[#9E9186] mb-1.5">{isEarlyEnd ? 'Session ended early' : 'Session complete'}</p>
            <h2 className="font-serif text-[32px] leading-tight font-bold text-[#1A1A1A] dark:text-white mb-2">{isEarlyEnd ? 'The work still counts.' : 'Focused work, finished.'}</h2>
            <p className="text-sm text-[#7A7068] mb-5">{isEarlyEnd ? `You studied for ${actualMinutes} minutes. Take a moment to capture what was useful before you leave.` : 'Your study time has been recorded.'}</p>

            {/* Big animated points */}
            <MotionDiv
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="inline-flex items-baseline gap-1.5 rounded-xl border-[1.5px] border-[#383838] bg-white px-6 py-3 shadow-[2px_2px_0_0_#383838]"
            >
              <CountUpNumber value={session.basePointsEarned} delay={600} />
              <span className="text-sm font-semibold text-[var(--accent-hex)] opacity-70">JP earned</span>
            </MotionDiv>
          </div>

          {/* Session details — one aligned result surface. */}
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.4 }}
            className="w-full"
          >
            <ResultStatGrid items={[
              { label: 'Duration', value: `${actualMinutes} min`, icon: <Clock size={14} /> },
              { label: 'Subject', value: session.subject, icon: <span className={`w-2.5 h-2.5 rounded-full ${subjectColors.dot}`} /> },
              { label: 'Session', value: typeConfig.label, icon: React.createElement(typeConfig.icon, { size: 14 }) },
            ]} />
          </MotionDiv>

          {/* Timetable block complete banner */}
          {timetableBlock && !isEarlyEnd && (
            <StatusNotice title="Timetable block complete" tone="success">
              <span className="inline-flex items-center gap-2"><CalendarCheck size={14} /> {actualMinutes} min studied</span>
            </StatusNotice>
          )}

          {/* Weekly Challenge nudge */}
          {weeklyChallenge?.isLoaded && weeklyChallenge?.challenge && !weeklyChallenge?.isClaimed && (
            <div className="flex items-center gap-3 p-3 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200/60 dark:border-amber-800/30">
              <Trophy size={16} className="text-amber-500 shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 truncate">
                  Weekly Challenge: {weeklyChallenge.challenge.title}
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex-1 h-1.5 bg-amber-200 dark:bg-amber-800/40 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-amber-500 rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(100, Math.round((weeklyChallenge.current / weeklyChallenge.challenge.target) * 100))}%` }}
                    />
                  </div>
                  <span className="text-[10px] font-bold text-amber-600 dark:text-amber-400 tabular-nums">
                    {weeklyChallenge.current}/{weeklyChallenge.challenge.target}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="space-y-3">
            <PrimaryActionButton
              label={`Quick debrief (+${QUICK_DEBRIEF_POINTS} pts)`}
              onClick={() => { setReflectionMode('quick'); setReflectionOpen(true); }}
              disabled={isSaving}
              className="w-full"
            />
            <button
              onClick={() => { setReflectionMode('full'); setReflectionOpen(true); }}
              disabled={isSaving}
              className="w-full py-3 rounded-xl text-sm font-semibold transition-all disabled:opacity-50 bg-white border border-[#D0CDC8] text-[#3A3530] hover:border-[#1A1A1A]"
            >
              Write a reflection (+{FULL_REFLECTION_POINTS} pts)
            </button>
            <button
              onClick={handleSkipReflection}
              disabled={isSaving}
              className="w-full py-3 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-all disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Skip'}
            </button>
          </div>
        </MotionDiv>

        {/* Reflection Modal (quick or full mode) */}
        <ReflectionModal
          isOpen={reflectionOpen}
          subjectName={session.subject}
          sessionType={session.sessionType}
          mode={reflectionMode}
          onSubmit={(text) => handleSaveWithReflection(text)}
          onCancel={() => setReflectionOpen(false)}
        />
      </div>
    );
  }

  return null;
};

export default StudySessionView;
