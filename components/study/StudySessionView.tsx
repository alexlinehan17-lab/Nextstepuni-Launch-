/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, BookOpen, Target, RotateCcw, Play, Pause, Clock, Sparkles, X, ChevronRight, Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck, Trophy, CalendarCheck } from 'lucide-react';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import PointsExplainer from '../PointsExplainer';
import { doc, updateDoc, arrayUnion, getDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { type SessionUser } from '../../utils/authUtils';
import { type StudentSubjectProfile } from '../subjectData';
import { type UserProgress, type StrategyMasteryMap, type MasteryTier } from '../../types';
import { type CourseData } from '../Library';
import { STRATEGY_REGISTRY, PROMPT_AUTO_DISMISS_SECONDS } from '../../studySessionData';
import { type StreakData } from '../../hooks/useStreak';
import { useStudySession } from '../../hooks/useStudySession';
import { getSubjectColor, getSubjectHex, DURATION_PRESETS } from '../../studySessionData';
import StrategyPickerStep from './StrategyPickerStep';
import ReflectionModal from '../ReflectionModal';
import { QUICK_DEBRIEF_POINTS, FULL_REFLECTION_POINTS } from '../ReflectionModal';
import { type DebriefEntry } from '../StudyDebrief';
import { type WeeklyChallengeState } from '../../hooks/useWeeklyChallenge';
import { useTeachBack } from '../../hooks/useTeachBack';
import { TeachBackReadCard, TeachBackWriteCard } from './TeachBackCard';
import { computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from '../timetableAlgorithm';
import { getBlockId, toDateKey } from '../subjectData';
import { processDebriefSideEffects } from '../../hooks/useDebriefSideEffects';
import { getSyllabusTopics } from '../syllabusTopics';
import XPPopup from '../XPPopup';

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

const STRATEGY_ICONS: Record<string, React.ElementType> = {
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

const SESSION_TYPE_CONFIG: Record<string, { icon: React.ElementType; label: string }> = {
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
  _streak,
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
  const teachBack = useTeachBack(user.uid, user.school);

  // Setup selections — pre-fill from timetable block if provided
  const [selectedSubject, setSelectedSubject] = useState(timetableBlock?.subject ?? '');
  const [selectedType, setSelectedType] = useState<'new-learning' | 'practice' | 'revision' | ''>(timetableBlock?.sessionType ?? '');
  const [selectedMinutes, setSelectedMinutes] = useState<number>(timetableBlock?.durationMinutes ?? 0);
  const [_blockCompleteBanner, setBlockCompleteBanner] = useState<{ done: number; total: number } | null>(null);

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

  // XP popup state
  const [xpPopup, setXpPopup] = useState<{ points: number; visible: boolean }>({ points: 0, visible: false });

  // Previous debrief notes — surface "whatWorked" back to the student
  const [prevDebriefs, setPrevDebriefs] = useState<DebriefEntry[]>([]);
  useEffect(() => {
    if (!user.uid) return;
    let cancelled = false;
    getDoc(doc(db, 'progress', user.uid)).then(snap => {
      if (cancelled) return;
      const data = snap.data();
      if (data?.studyDebriefs) setPrevDebriefs(data.studyDebriefs);
    }).catch(() => {});
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

  // Teach-back state
  const [teachBackPhase, setTeachBackPhase] = useState<'none' | 'reading' | 'writing' | 'write-done'>('none');
  const teachBackReadShownRef = useRef(false);
  const teachBackWriteShownRef = useRef(false);
  const teachBackDoneTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (teachBackDoneTimerRef.current) clearTimeout(teachBackDoneTimerRef.current);
    };
  }, []);

  const subjects = studentProfile?.subjects ?? [];

  // Compute today's remaining timetable blocks for quick-start shortcuts
  const computedTodayBlocks = useMemo((): TimetableBlockContext[] => {
    if (!studentProfile || todayBlocks.length > 0) return todayBlocks;
    try {
      const today = new Date();
      const todayKey = toDateKey(today);
      const jsDay = today.getDay();
      const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;
      const priorities = computeSubjectPriorities(studentProfile.subjects, undefined);
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
    teachBack.fetchTeachBack(selectedSubject);
    teachBackReadShownRef.current = false;
    teachBackWriteShownRef.current = false;
    setTeachBackPhase('none');
    session.startSession(selectedSubject, selectedType, selectedMinutes);
  };

  // Show teach-back cards at timed intervals during active session
  const tbReadTime = Math.min(480, Math.floor(session.totalDuration * 0.35));  // ~8 min or 35%
  const tbWriteTime = Math.min(1080, Math.floor(session.totalDuration * 0.70)); // ~18 min or 70%

  useEffect(() => {
    if (session.phase !== 'active') return;

    // Show read card at ~35% / 8 min if a teach-back is available
    if (
      !teachBackReadShownRef.current &&
      session.elapsedSeconds >= tbReadTime &&
      teachBack.teachBackToRead &&
      teachBackPhase === 'none'
    ) {
      teachBackReadShownRef.current = true;
      setTeachBackPhase('reading');
      session.dismissPrompt();
    }

    // Show write card at ~70% / 18 min (only for sessions >= 15 min)
    if (
      !teachBackWriteShownRef.current &&
      session.elapsedSeconds >= tbWriteTime &&
      session.totalDuration >= 900 &&
      teachBackPhase === 'none'
    ) {
      teachBackWriteShownRef.current = true;
      setTeachBackPhase('writing');
      session.dismissPrompt();
    }
  }, [session.elapsedSeconds, session.phase, teachBack.teachBackToRead, teachBackPhase, tbReadTime, tbWriteTime, session.totalDuration]);

  // Auto-complete timetable block after saving session
  const completeTimetableBlock = () => {
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

  const handleSaveWithReflection = async (_reflectionText: string) => {
    const bonus = reflectionMode === 'quick' ? QUICK_DEBRIEF_POINTS : FULL_REFLECTION_POINTS;
    setIsSaving(true);
    await session.saveSession(bonus, selectedStrategies);
    completeTimetableBlock();
    pointsReload();
    onStrategyMasteryRecompute?.();
    weeklyChallenge?.reload();
    setReflectionOpen(false);
    setIsSaving(false);
    setPickerDone(false);
    setSelectedStrategies([]);
    session.resetSession();
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
      date: new Date().toISOString().split('T')[0],
    };
    // Save session first (with a small reflection bonus for completing debrief)
    await session.saveSession(10, selectedStrategies);
    // Save debrief entry
    try {
      await updateDoc(doc(db, 'progress', user.uid), {
        studyDebriefs: arrayUnion(fullEntry),
      });
    } catch (err) {
      console.error('Failed to save debrief:', err);
    }
    // Process side effects: update topic mastery + SM-2 state
    processDebriefSideEffects(user.uid, fullEntry).catch(err => console.error('Debrief side effects error:', err));
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
      <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950 flex flex-col">
        {/* ── Coloured hero banner ── */}
        <div className="relative shrink-0" style={{ backgroundColor: '#2A7D6F' }}>
          {/* Decorative blobs */}
          <div className="absolute pointer-events-none" style={{ top: -60, right: -40, width: 180, height: 180, borderRadius: '50%', background: 'rgba(255,255,255,0.07)' }} />
          <div className="absolute pointer-events-none" style={{ top: 10, right: 20, width: 90, height: 90, borderRadius: '50%', background: 'rgba(255,255,255,0.05)' }} />
          <div className="absolute pointer-events-none" style={{ bottom: 30, left: -30, width: 120, height: 120, borderRadius: '50%', background: 'rgba(0,0,0,0.05)' }} />

          <div className="relative z-10 px-6 pt-6 pb-8 max-w-md mx-auto">
            <button onClick={onBack} className="p-2 -ml-2 rounded-xl transition-colors mb-8" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <ArrowLeft size={20} style={{ color: '#fff' }} />
            </button>

            <h1 className="font-serif font-bold text-white mb-2" style={{ fontSize: 'clamp(32px, 8vw, 44px)', letterSpacing: '-0.03em', lineHeight: 1 }}>
              Study Session
            </h1>
            {session.todaySessions.length > 0 ? (
              <p className="text-sm" style={{ color: 'rgba(255,255,255,0.6)' }}>
                {session.todaySessions.length} session{session.todaySessions.length !== 1 ? 's' : ''} today &middot; {session.todayTotalMinutes} min total
              </p>
            ) : (
              <p className="text-sm" style={{ color: 'rgba(255,255,255,0.6)' }}>Choose a subject and start studying</p>
            )}
          </div>

        </div>

        {/* Centered content */}
        <div className="flex-1 px-6 pb-28 bg-[#FDF8F0] dark:bg-zinc-950">
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
                    <Sparkles size={18} className="text-[#2A7D6F] shrink-0 mt-0.5" />
                    <div className="space-y-2">
                      <p className="font-semibold text-sm text-[#1A1A1A] dark:text-white">Welcome to Study Sessions</p>
                      <p className="text-sm text-[#78716C] dark:text-zinc-400 leading-relaxed">
                        During sessions you'll see strategy prompts from modules you've completed. Tap "Done" to track your engagement — this feeds your mastery progress visible below.
                      </p>
                      <button
                        onClick={() => onDismissGuide?.('study-session-intro')}
                        className="mt-1 text-sm font-medium hover:underline"
                        style={{ color: '#2A7D6F' }}
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
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${colors.bg} border ${colors.border} hover:shadow-sm active:scale-[0.98]`}
                      >
                        <span className={`w-2.5 h-2.5 rounded-full ${colors.dot} shrink-0`} />
                        <div className="flex-1 min-w-0">
                          <span className={`text-[13px] font-bold block ${colors.text}`}>{block.subject}</span>
                          <span className="text-[11px] text-zinc-400 dark:text-zinc-500 flex items-center gap-1">
                            <TypeIcon size={10} />
                            {typeConfig.label} · {block.durationMinutes}m
                          </span>
                        </div>
                        <span className="text-xs font-semibold text-[var(--accent-hex)]">Study Now</span>
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
                    <button
                      key={s.subjectName}
                      onClick={() => setSelectedSubject(s.subjectName)}
                      className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-full text-[13px] font-medium transition-all ${
                        isActive
                          ? `${colors.bg} ${colors.text} shadow-sm ring-1 ring-inset`
                          : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                      }`}
                      style={isActive ? { ['--tw-ring-color' as any]: 'rgba(var(--accent), 0.25)' } : undefined}
                    >
                      <span className={`w-2 h-2 rounded-full shrink-0 ${colors.dot}`} />
                      {s.subjectName}
                    </button>
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
                      <button
                        key={type}
                        onClick={() => setSelectedType(type)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-[13px] font-medium transition-all ${
                          isActive
                            ? 'bg-[rgba(var(--accent),0.08)] text-[var(--accent-hex)] shadow-sm ring-1 ring-inset ring-[rgba(var(--accent),0.2)]'
                            : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                        }`}
                      >
                        <Icon size={16} strokeWidth={isActive ? 2 : 1.5} />
                        <span>{config.label}</span>
                      </button>
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
                      <button
                        key={preset.minutes}
                        onClick={() => setSelectedMinutes(preset.minutes)}
                        className={`w-full flex items-center justify-center px-4 py-3 rounded-xl text-[13px] font-semibold transition-all ${
                          isActive
                            ? 'bg-[rgba(var(--accent),0.08)] text-[var(--accent-hex)] shadow-sm ring-1 ring-inset ring-[rgba(var(--accent),0.2)]'
                            : 'bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                        }`}
                      >
                        {preset.minutes} min
                      </button>
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
      </div>
    );
  }

  // ── ACTIVE / PAUSED PHASE (Headspace-inspired) ──
  if (session.phase === 'active' || session.phase === 'paused') {
    const _subjectColors = getSubjectColor(session.subject);
    const subjectHex = getSubjectHex(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];

    // Generate 4 arc layers — each lighter/more saturated moving outward
    // Colors shift from deep base → lighter toward the edges
    const arcLayers = [
      { scale: 1.0,  yOffset: '62%', opacity: 1.0, lighten: 0 },
      { scale: 1.35, yOffset: '55%', opacity: 0.92, lighten: 15 },
      { scale: 1.7,  yOffset: '48%', opacity: 0.85, lighten: 28 },
      { scale: 2.1,  yOffset: '42%', opacity: 0.78, lighten: 40 },
    ];

    // Helper to lighten a hex color
    const lightenHex = (hex: string, amount: number) => {
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      const nr = Math.min(255, r + amount);
      const ng = Math.min(255, g + amount);
      const nb = Math.min(255, b + amount);
      return `#${nr.toString(16).padStart(2, '0')}${ng.toString(16).padStart(2, '0')}${nb.toString(16).padStart(2, '0')}`;
    };

    const _handleQuit = () => {
      if (window.confirm('End this session and go back? Any time studied will be lost.')) {
        session.endSession();
        session.resetSession();
      }
    };

    return (
      <div
        className="fixed inset-0 z-[100] flex flex-col"
        style={{ background: lightenHex(subjectHex, 55) }}
      >
        {/* Concentric arcs — layered from back to front */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {[...arcLayers].reverse().map((layer, i) => (
            <motion.div
              key={i}
              className="absolute left-1/2 rounded-full"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{
                scale: session.phase === 'paused' ? layer.scale * 0.97 : layer.scale,
                opacity: layer.opacity,
              }}
              transition={{ duration: 1.2, delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
              style={{
                width: '140vw',
                height: '140vw',
                top: layer.yOffset,
                transform: 'translateX(-50%)',
                background: lightenHex(subjectHex, layer.lighten),
              }}
            />
          ))}
        </div>

        {/* Top bar — X button + subject info */}
        <div className="relative z-20 flex items-center justify-between px-5 pt-5 pb-2">
          <button
            onClick={session.endSession}
            className="w-9 h-9 rounded-full flex items-center justify-center transition-all"
            style={{ backgroundColor: 'rgba(0,0,0,0.08)' }}
          >
            <X size={18} style={{ color: 'rgba(0,0,0,0.5)' }} />
          </button>
          <div />
        </div>

        {/* Title area */}
        <div className="relative z-20 text-center mt-4 px-6">
          <motion.h1
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="text-2xl md:text-3xl font-bold"
            style={{ color: 'rgba(0,0,0,0.8)' }}
          >
            {session.subject}
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="text-sm mt-1.5"
            style={{ color: 'rgba(0,0,0,0.45)' }}
          >
            {typeConfig.label} · {Math.ceil(session.totalDuration / 60)} min
          </motion.p>
        </div>

        {/* Center — giant play/pause */}
        <div className="relative z-20 flex-1 flex items-center justify-center">
          <motion.button
            onClick={session.phase === 'active' ? session.pauseSession : session.resumeSession}
            className="relative w-20 h-20 md:w-24 md:h-24 rounded-full flex items-center justify-center transition-shadow duration-500 ease-in-out hover:shadow-[0_0_60px_20px_rgba(255,255,255,0.6),0_0_120px_40px_rgba(255,255,255,0.2)]"
            style={{ backgroundColor: 'rgba(0,0,0,0.75)', boxShadow: '0 0 0px 0px rgba(255,255,255,0)' }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.93 }}
          >
            {session.phase === 'active' ? (
              <Pause size={32} className="text-white" />
            ) : (
              <Play size={32} className="text-white" style={{ marginLeft: 3 }} />
            )}
          </motion.button>
        </div>

        {/* Bottom — progress bar + times */}
        <div className="relative z-20 px-6 pb-8 pt-4">
          {/* Paused label — absolute so it doesn't shift layout */}
          <AnimatePresence>
            {session.phase === 'paused' && teachBackPhase === 'none' && !session.currentPrompt && (
              <MotionDiv
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute left-0 right-0 -top-6 text-center pointer-events-none"
              >
                <span
                  className="text-xs font-bold uppercase tracking-[0.25em]"
                  style={{ color: 'rgba(0,0,0,0.35)' }}
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
              style={{ backgroundColor: 'rgba(0,0,0,0.12)' }}
            >
              <motion.div
                className="h-full rounded-full"
                style={{
                  backgroundColor: 'rgba(0,0,0,0.5)',
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
                backgroundColor: 'rgba(0,0,0,0.6)',
                transition: 'left 1s ease',
              }}
            />
          </div>

          {/* Elapsed / Remaining */}
          <div className="flex justify-between mt-3 max-w-lg mx-auto">
            <span
              className="text-xs font-medium tabular-nums"
              style={{ color: 'rgba(0,0,0,0.4)' }}
            >
              {formatTime(session.elapsedSeconds)}
            </span>
            <span
              className="text-xs font-medium tabular-nums"
              style={{ color: 'rgba(0,0,0,0.4)' }}
            >
              {formatTime(timeRemaining)}
            </span>
          </div>
        </div>

        {/* Coaching prompts / Teach-back cards — overlay from bottom */}
        <AnimatePresence mode="wait">
          {/* Teach-back read card */}
          {teachBackPhase === 'reading' && teachBack.teachBackToRead && (
            <TeachBackReadCard
              key="tb-read"
              subject={session.subject}
              explanation={teachBack.teachBackToRead.explanation}
              onHelpful={() => {
                teachBack.markHelpful(teachBack.teachBackToRead!.id);
                setTeachBackPhase('none');
              }}
              onSkip={() => {
                teachBack.markSeen(teachBack.teachBackToRead!.id);
                setTeachBackPhase('none');
              }}
            />
          )}

          {/* Teach-back write card */}
          {teachBackPhase === 'writing' && (
            <TeachBackWriteCard
              key="tb-write"
              subject={session.subject}
              isSubmitting={teachBack.isSubmitting}
              onSubmit={async (text) => {
                await teachBack.submitTeachBack(session.subject, text);
                setTeachBackPhase('write-done');
                teachBackDoneTimerRef.current = setTimeout(() => setTeachBackPhase('none'), 2000);
              }}
              onSkip={() => setTeachBackPhase('none')}
            />
          )}

          {/* Teach-back write success */}
          {teachBackPhase === 'write-done' && (
            <MotionDiv
              key="tb-done"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="fixed bottom-24 left-4 right-4 z-30 max-w-md mx-auto"
            >
              <div className="bg-white/90 backdrop-blur-xl border border-white/60 rounded-2xl p-4 shadow-2xl text-center">
                <p className="text-sm font-semibold text-emerald-600">Sent! A classmate will see your explanation.</p>
              </div>
            </MotionDiv>
          )}

          {/* Coaching prompt */}
          {teachBackPhase === 'none' && session.currentPrompt && (
            <MotionDiv
              key={session.currentPrompt.prompt}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="fixed bottom-24 left-4 right-4 z-30 max-w-md mx-auto"
            >
              <div
                className="rounded-2xl p-4 shadow-2xl overflow-hidden relative"
                style={{
                  backgroundColor: 'rgba(255,255,255,0.85)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255,255,255,0.6)',
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
            setXpPopup({ points: session.basePointsEarned, visible: true });
          }}
          onSkip={() => {
            setSelectedStrategies([]);
            setPickerDone(true);
            setXpPopup({ points: session.basePointsEarned, visible: true });
          }}
        />
      );
    }

    const subjectColors = getSubjectColor(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];
    const actualMinutes = Math.round(session.elapsedSeconds / 60);

    return (
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col items-center justify-center px-4">
        <MotionDiv
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="w-full max-w-sm space-y-6"
        >
          {/* Header — points as hero */}
          <div className="text-center">
            <MotionDiv
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              <Sparkles size={28} className="text-amber-500 mx-auto mb-3" />
            </MotionDiv>
            <h2 className="text-xl font-bold text-zinc-800 dark:text-white mb-4">Session Complete</h2>

            {/* Big animated points */}
            <MotionDiv
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="inline-flex items-baseline gap-1.5 px-6 py-3 rounded-2xl"
              style={{ backgroundColor: 'rgba(var(--accent),0.08)' }}
            >
              <CountUpNumber value={session.basePointsEarned} delay={600} />
              <span className="text-sm font-semibold text-[var(--accent-hex)] opacity-70">pts earned</span>
            </MotionDiv>
          </div>

          {/* XP Popup */}
          <XPPopup
            points={xpPopup.points}
            isVisible={xpPopup.visible}
            onComplete={() => setXpPopup(prev => ({ ...prev, visible: false }))}
          />

          {/* Session details — compact chips instead of receipt table */}
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.4 }}
            className="flex flex-wrap justify-center gap-2"
          >
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06]">
              <Clock size={13} className="text-zinc-400" />
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{actualMinutes} min</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06]">
              <span className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{session.subject}</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06]">
              {React.createElement(typeConfig.icon, { size: 13, className: 'text-zinc-400' })}
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{typeConfig.label}</span>
            </div>
          </MotionDiv>

          {/* Timetable block complete banner */}
          {timetableBlock && (
            <div className="flex items-center gap-3 p-3 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200/60 dark:border-emerald-800/30">
              <CalendarCheck size={16} className="text-emerald-500 shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-emerald-700 dark:text-emerald-300">
                  Timetable block marked complete — {actualMinutes} min studied
                </p>
              </div>
            </div>
          )}

          {/* Weekly Challenge nudge */}
          {weeklyChallenge?.isLoaded && !weeklyChallenge?.isClaimed && (
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
            <button
              onClick={() => { setReflectionMode('quick'); setReflectionOpen(true); }}
              disabled={isSaving}
              className="w-full py-3.5 rounded-xl text-sm font-bold text-white active:scale-[0.98] transition-all disabled:opacity-50"
              style={{ backgroundColor: '#2A7D6F' }}
            >
              Quick Debrief (+{QUICK_DEBRIEF_POINTS} pts)
            </button>
            <button
              onClick={() => { setReflectionMode('full'); setReflectionOpen(true); }}
              disabled={isSaving}
              className="w-full py-3 rounded-xl text-sm font-medium transition-all disabled:opacity-50"
              style={{ backgroundColor: 'rgba(42,125,111,0.08)', color: '#2A7D6F' }}
            >
              Write a Reflection (+{FULL_REFLECTION_POINTS} pts)
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
