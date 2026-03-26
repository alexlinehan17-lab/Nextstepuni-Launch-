/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, BookOpen, Target, RotateCcw, Play, Pause, Clock, Sparkles, Zap, X, ChevronRight, Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck, Trophy, CalendarCheck } from 'lucide-react';
import { doc, updateDoc, arrayUnion, getDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { type SessionUser } from '../Auth';
import { type StudentSubjectProfile } from '../subjectData';
import { type UserProgress, type StrategyMasteryMap, type MasteryTier } from '../../types';
import { type CourseData } from '../Library';
import { STRATEGY_REGISTRY, PROMPT_AUTO_DISMISS_SECONDS } from '../../studySessionData';
import { type StreakData } from '../../hooks/useStreak';
import { useStudySession } from '../../hooks/useStudySession';
import { getSubjectColor, getSubjectStroke, DURATION_PRESETS } from '../../studySessionData';
import StrategyPickerStep from './StrategyPickerStep';
import ReflectionModal from '../ReflectionModal';
import { scoreReflection, REFLECTION_TIER_POINTS } from '../ReflectionModal';
import StudyDebrief, { type DebriefEntry } from '../StudyDebrief';
import { type WeeklyChallengeState } from '../../hooks/useWeeklyChallenge';
import { useTeachBack } from '../../hooks/useTeachBack';
import { TeachBackReadCard, TeachBackWriteCard } from './TeachBackCard';
import { computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from '../timetableAlgorithm';
import { getBlockId, toDateKey } from '../subjectData';
import { processDebriefSideEffects } from '../../hooks/useDebriefSideEffects';
import { getSyllabusTopics } from '../syllabusTopics';
import XPPopup from '../XPPopup';

const MotionDiv = motion.div as any;

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
  streak,
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
  const [blockCompleteBanner, setBlockCompleteBanner] = useState<{ done: number; total: number } | null>(null);

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
  const [debriefOpen, setDebriefOpen] = useState(false);
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
    } catch {
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
  const debriefTopics = useMemo(() => {
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
      const alreadyDone = todayBlocks.filter(b =>
        b.blockId === timetableBlock.blockId || b.blockId !== timetableBlock.blockId
      );
      // Count how many are done (this block is now done, others we don't know — but we can show total)
      const totalToday = todayBlocks.length;
      // We know at least this one is done, estimate from remaining
      const doneCount = todayBlocks.filter(b => b.blockId === timetableBlock.blockId).length;
      setBlockCompleteBanner({ done: doneCount, total: totalToday });
    }
  };

  const handleSaveWithReflection = async (reflectionText: string) => {
    const quality = scoreReflection(reflectionText);
    const bonus = REFLECTION_TIER_POINTS[quality.tier];
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

  const handleDebriefSubmit = async (entry: Omit<DebriefEntry, 'id' | 'date'>) => {
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
    } catch (e) {
      console.error('Failed to save debrief:', e);
    }
    // Process side effects: update topic mastery + SM-2 state
    processDebriefSideEffects(user.uid, fullEntry).catch(e => console.error('Debrief side effects error:', e));
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
  const ringOffset = ringCircumference * (1 - progress);
  const timeRemaining = Math.max(0, session.totalDuration - session.elapsedSeconds);

  // ── SETUP PHASE ──
  if (session.phase === 'idle') {
    return (
      <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col">
        {/* Header — minimal */}
        <div className="shrink-0 px-6 pt-6 pb-2">
          <button onClick={onBack} className="p-2 -ml-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors">
            <ArrowLeft size={20} className="text-zinc-400" />
          </button>
        </div>

        {/* Centered content */}
        <div className="flex-1 flex items-center justify-center px-6 pb-28">
          <div className="w-full max-w-md space-y-10">
            {/* First-visit intro card */}
            <AnimatePresence>
              {!dismissedGuides?.['study-session-intro'] && (
                <MotionDiv
                  key="study-session-intro"
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8, transition: { duration: 0.2 } }}
                  className="bg-[rgba(var(--accent),0.04)] border border-[rgba(var(--accent),0.15)] rounded-2xl p-5 mb-6"
                >
                  <div className="flex items-start gap-3">
                    <Sparkles size={18} className="text-[rgba(var(--accent),1)] shrink-0 mt-0.5" />
                    <div className="space-y-2">
                      <p className="font-semibold text-sm text-zinc-800 dark:text-white">Welcome to Study Sessions</p>
                      <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                        During sessions you'll see strategy prompts from modules you've completed. Tap "Done" to track your engagement — this feeds your mastery progress visible below.
                      </p>
                      <button
                        onClick={() => onDismissGuide?.('study-session-intro')}
                        className="mt-1 text-sm font-medium text-[rgba(var(--accent),1)] hover:underline"
                      >
                        Got it
                      </button>
                    </div>
                  </div>
                </MotionDiv>
              )}
            </AnimatePresence>
            {/* Title + today summary */}
            <div className="text-center space-y-3">
              <h1 className="text-3xl font-bold text-zinc-800 dark:text-white tracking-tight">Study Session</h1>
              {session.todaySessions.length > 0 ? (
                <p className="text-sm text-zinc-400 dark:text-zinc-500">
                  {session.todaySessions.length} session{session.todaySessions.length !== 1 ? 's' : ''} today &middot; {session.todayTotalMinutes} min total
                </p>
              ) : (
                <p className="text-sm text-zinc-400 dark:text-zinc-500">Choose a subject and start studying</p>
              )}
            </div>

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
                  <div className="px-4 py-3 rounded-xl" style={{ backgroundColor: '#FAF7F4', border: '0.5px solid rgba(0,0,0,0.07)', borderRadius: 12 }}>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-1.5" style={{ color: '#9A9590' }}>Last time you studied {selectedSubject}</p>
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
                    <input
                      type="number"
                      min={5}
                      max={180}
                      placeholder="Custom"
                      value={!DURATION_PRESETS.some(p => p.minutes === selectedMinutes) && selectedMinutes > 0 ? selectedMinutes : ''}
                      onChange={(e) => {
                        const v = parseInt(e.target.value, 10);
                        if (!isNaN(v) && v >= 1 && v <= 180) setSelectedMinutes(v);
                        else if (e.target.value === '') setSelectedMinutes(0);
                      }}
                      className={`w-full px-4 py-3 rounded-xl text-[13px] font-semibold text-center transition-all bg-white dark:bg-zinc-900 text-zinc-500 dark:text-zinc-400 border ${
                        !DURATION_PRESETS.some(p => p.minutes === selectedMinutes) && selectedMinutes > 0
                          ? 'border-[rgba(var(--accent),0.3)] ring-1 ring-inset ring-[rgba(var(--accent),0.2)] text-[var(--accent-hex)]'
                          : 'border-transparent hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                      } outline-none`}
                    />
                    <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[11px] text-zinc-400 pointer-events-none">min</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Start button */}
            <button
              onClick={handleStart}
              disabled={!canStart}
              className={`w-full py-4 rounded-2xl text-[15px] font-bold tracking-wide transition-all ${
                canStart
                  ? 'bg-[var(--accent-hex)] text-white shadow-lg shadow-[rgba(var(--accent),0.2)] hover:shadow-[rgba(var(--accent),0.35)] active:scale-[0.98]'
                  : 'bg-zinc-100 dark:bg-zinc-900 text-zinc-300 dark:text-zinc-700 cursor-not-allowed'
              }`}
            >
              Start Session
            </button>

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
      </div>
    );
  }

  // ── ACTIVE / PAUSED PHASE ──
  if (session.phase === 'active' || session.phase === 'paused') {
    const subjectColors = getSubjectColor(session.subject);
    const strokeColor = getSubjectStroke(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];

    const handleQuit = () => {
      if (window.confirm('End this session and go back? Any time studied will be lost.')) {
        session.endSession();
        session.resetSession();
      }
    };

    return (
      <div className="fixed inset-0 z-[100] bg-zinc-950 flex flex-col items-center justify-center">
        {/* Subject + type — clean top bar */}
        <div className="absolute top-0 left-0 right-0 flex items-center justify-between px-6 py-5">
          <button
            onClick={session.endSession}
            className="text-xs font-medium text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            End session
          </button>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
            <span className="text-sm font-medium text-zinc-300">{session.subject}</span>
            <span className="text-zinc-600 mx-0.5">·</span>
            <span className="text-sm text-zinc-500">{typeConfig.label}</span>
          </div>
          <div className="w-16" />
        </div>

        {/* Timer — large, centered, minimal */}
        <div className="flex flex-col items-center">
          {/* Time display — the hero element */}
          <div className="relative">
            {/* Outer ring — progress */}
            <svg className="w-64 h-64 md:w-80 md:h-80 -rotate-90" viewBox="0 0 200 200">
              {/* Track */}
              <circle
                cx="100" cy="100" r="90"
                fill="none"
                strokeWidth="2"
                stroke="rgba(255,255,255,0.06)"
              />
              {/* Progress arc */}
              <motion.circle
                cx="100" cy="100" r="90"
                fill="none"
                strokeWidth="3"
                strokeLinecap="round"
                stroke="#2A7D6F"
                strokeDasharray={2 * Math.PI * 90}
                strokeDashoffset={2 * Math.PI * 90 * (1 - progress)}
                style={{ transition: 'stroke-dashoffset 1s ease' }}
              />
            </svg>

            {/* Center content */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-6xl md:text-7xl font-light text-white tabular-nums tracking-tighter" style={{ letterSpacing: '-0.04em' }}>
                {formatTime(timeRemaining)}
              </span>
              <div className="flex items-center gap-3 mt-3 text-xs text-zinc-500">
                <span>{Math.round(progress * 100)}% complete</span>
                <span className="w-1 h-1 rounded-full bg-zinc-700" />
                <span>{formatTime(session.elapsedSeconds)} elapsed</span>
              </div>
            </div>
          </div>

          {/* Pause/Play — single clean button */}
          <div className="mt-10">
            <button
              onClick={session.phase === 'active' ? session.pauseSession : session.resumeSession}
              className="w-14 h-14 rounded-full flex items-center justify-center transition-all"
              style={{
                backgroundColor: session.phase === 'paused' ? '#2A7D6F' : 'rgba(255,255,255,0.08)',
                border: session.phase === 'paused' ? 'none' : '1px solid rgba(255,255,255,0.1)',
              }}
            >
              {session.phase === 'active' ? (
                <Pause size={22} className="text-zinc-300" />
              ) : (
                <Play size={22} className="text-white ml-0.5" />
              )}
            </button>
          </div>
        </div>

        {/* Bottom card area: coaching prompts OR teach-back cards */}
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
                // Auto-dismiss success after 2s
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
              className="absolute bottom-12 left-4 right-4 max-w-md mx-auto"
            >
              <div className="bg-zinc-900 border border-emerald-500/30 rounded-xl p-4 shadow-2xl text-center">
                <p className="text-sm font-semibold text-emerald-400">Sent! A classmate will see your explanation.</p>
              </div>
            </MotionDiv>
          )}

          {/* Coaching prompt (only when no teach-back is showing) */}
          {teachBackPhase === 'none' && session.currentPrompt && (
            <MotionDiv
              key={session.currentPrompt.prompt}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
              className="absolute bottom-12 left-4 right-4 max-w-md mx-auto"
            >
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-2xl overflow-hidden relative">
                {/* Auto-dismiss countdown bar */}
                <motion.div
                  className="absolute top-0 left-0 h-0.5 bg-amber-400/60"
                  initial={{ width: '100%' }}
                  animate={{ width: '0%' }}
                  transition={{ duration: PROMPT_AUTO_DISMISS_SECONDS, ease: 'linear' }}
                />
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles size={14} className="text-amber-400" />
                  <span className="text-xs font-bold uppercase tracking-widest text-amber-400">
                    {session.currentPrompt.strategyName}
                  </span>
                </div>
                <p className="text-sm text-zinc-300 leading-relaxed">
                  {session.currentPrompt.prompt}
                </p>
                <div className="flex items-center gap-3 mt-3">
                  <button
                    onClick={session.completePrompt}
                    className="text-xs font-semibold text-teal-400 hover:text-teal-300 transition-colors"
                  >
                    Done
                  </button>
                  <button
                    onClick={session.dismissPrompt}
                    className="text-xs text-zinc-500 hover:text-zinc-400 transition-colors"
                  >
                    Skip
                  </button>
                </div>
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>

        {/* Paused indicator — subtle, not an overlay */}
        {session.phase === 'paused' && (
          <div className="absolute bottom-24 left-0 right-0 flex justify-center pointer-events-none">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-widest">Paused</span>
          </div>
        )}
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
          onContinue={(ids) => {
            setSelectedStrategies(ids);
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
          {/* Header */}
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-amber-50 dark:bg-amber-500/10 mb-4">
              <Sparkles size={32} className="text-amber-500" />
            </div>
            <h2 className="text-2xl font-bold text-zinc-800 dark:text-white">Session Complete!</h2>
          </div>

          {/* XP Popup */}
          <XPPopup
            points={xpPopup.points}
            isVisible={xpPopup.visible}
            onComplete={() => setXpPopup(prev => ({ ...prev, visible: false }))}
          />

          {/* Stats card */}
          <div className="bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.06] rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Duration</span>
              <span className="text-sm font-bold text-zinc-800 dark:text-white">{actualMinutes} min</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Subject</span>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
                <span className="text-sm font-medium text-zinc-800 dark:text-white">{session.subject}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Type</span>
              <span className="text-sm font-medium text-zinc-800 dark:text-white">{typeConfig.label}</span>
            </div>
            <div className="border-t border-zinc-100 dark:border-zinc-800 pt-3 flex items-center justify-between">
              <span className="text-sm text-zinc-500">Points Earned</span>
              <span className="text-base font-bold text-[var(--accent-hex)]">+{session.basePointsEarned}</span>
            </div>
          </div>

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
              onClick={() => setDebriefOpen(true)}
              disabled={isSaving}
              className="w-full py-3.5 rounded-xl text-sm font-bold bg-teal-500 text-white shadow-lg shadow-teal-500/25 hover:shadow-teal-500/40 active:scale-[0.98] transition-all disabled:opacity-50"
            >
              Quick Debrief (+10 pts)
            </button>
            <button
              onClick={() => setReflectionOpen(true)}
              disabled={isSaving}
              className="w-full py-3 rounded-xl text-sm font-medium text-[var(--accent-hex)] bg-[rgba(var(--accent),0.08)] hover:bg-[rgba(var(--accent),0.15)] transition-all disabled:opacity-50"
            >
              Write a Reflection (+10-20 pts)
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

        {/* Study Debrief Modal */}
        <StudyDebrief
          isOpen={debriefOpen}
          subject={session.subject}
          sessionType={session.sessionType}
          durationMinutes={actualMinutes}
          syllabusTopics={debriefTopics}
          onSubmit={handleDebriefSubmit}
          onSkip={() => { setDebriefOpen(false); handleSkipReflection(); }}
        />

        {/* Reflection Modal */}
        <ReflectionModal
          isOpen={reflectionOpen}
          subjectName={session.subject}
          sessionType={session.sessionType}
          basePoints={session.basePointsEarned + REFLECTION_TIER_POINTS.basic}
          streakMultiplier={1}
          onSubmit={(text) => handleSaveWithReflection(text)}
          onCancel={() => setReflectionOpen(false)}
        />
      </div>
    );
  }

  return null;
};

export default StudySessionView;
