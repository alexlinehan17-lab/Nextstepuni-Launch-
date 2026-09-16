/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { BookOpen, Target, RotateCcw, type LucideIcon } from 'lucide-react';
import StudySessionSetup from './StudySessionSetup';
import StudySessionTimer from './StudySessionTimer';
import StudyBreak from './StudyBreak';
import StudySessionFinish from './StudySessionFinish';
import { useStudyTimerAppearance } from '../../hooks/useStudyTimerAppearance';
import { getSubjectFill } from '../../utils/subjectColors';
import PointsExplainer from '../PointsExplainer';
import { doc, updateDoc, arrayUnion, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { saveInBackground } from '../../utils/firestoreWrite';
import { type SessionUser } from '../../utils/authUtils';
import { type StudentSubjectProfile } from '../subjectData';
import { type UserProgress, type StrategyMasteryMap, type StudyConfidenceLabel, type StudyReflection } from '../../types';
import { type CourseData } from '../Library';
import { STRATEGY_REGISTRY } from '../../studySessionData';
import { type StreakData } from '../../hooks/useStreak';
import { MIN_STUDY_SESSION_MINUTES, useStudySession } from '../../hooks/useStudySession';
import StrategyPickerStep from './StrategyPickerStep';
import { QUICK_DEBRIEF_POINTS, FULL_REFLECTION_POINTS } from '../ReflectionModal';
import StudyJournalModal from '../StudyJournalModal';
import { type DebriefEntry } from '../StudyDebrief';
import { type WeeklyChallengeState } from '../../hooks/useWeeklyChallenge';
import { computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from '../timetableAlgorithm';
import { getBlockId, toDateKey } from '../subjectData';
import { processDebriefSideEffects } from '../../hooks/useDebriefSideEffects';
import { getSyllabusTopics } from '../syllabusTopics';
import { logError } from '../../utils/logError';
import { useProgress } from '../../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../../data/devStudent';
import { useModal } from '../../hooks/useModal';

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
  onGoToProgress?: () => void;
  dismissedGuides?: Record<string, string>;
  onDismissGuide?: (id: string) => void;
  weeklyChallenge?: WeeklyChallengeState;
  timetableBlock?: TimetableBlockContext | null;
  onTimetableBlockComplete?: (dateKey: string, blockId: string, actualMinutes: number) => void;
  todayBlocks?: TimetableBlockContext[];
  onStudyBlock?: (block: TimetableBlockContext) => void;
  onSetUpProfile?: () => void;
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
  onGoToProgress,
  dismissedGuides,
  onDismissGuide,
  weeklyChallenge,
  timetableBlock,
  onTimetableBlockComplete,
  todayBlocks = [],
  onStudyBlock,
  onSetUpProfile,
}) => {
  const session = useStudySession(user.uid, userProgress, allCourses);
  const [timerAppearance, setTimerAppearance] = useStudyTimerAppearance(user.uid);
  const { rawProgressDoc, updateDemoProgress } = useProgress();
  const isDemo = user.uid === DEMO_STUDENT_UID;

  // Setup selections — pre-fill from timetable block if provided
  const [selectedSubject, setSelectedSubject] = useState(timetableBlock?.subject ?? '');
  const [selectedType, setSelectedType] = useState<'new-learning' | 'practice' | 'revision' | ''>(timetableBlock?.sessionType ?? '');
  const [selectedMinutes, setSelectedMinutes] = useState<number>(timetableBlock?.durationMinutes ?? 0);
  const [_blockCompleteBanner, setBlockCompleteBanner] = useState<{ done: number; total: number } | null>(null);
  const [confirmQuit, setConfirmQuit] = useState(false);
  const exitDialogRef = useRef<HTMLDivElement>(null);
  useModal(confirmQuit, () => setConfirmQuit(false), exitDialogRef);

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

  // Inline session debrief
  const [_debriefOpen, setDebriefOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Reflection journal (view past reflections)
  const [reflections, setReflections] = useState<StudyReflection[]>([]);
  const [journalOpen, setJournalOpen] = useState(false);
  const loadReflections = () => {
    if (!user.uid) return;
    if (isDemo) {
      setReflections(rawProgressDoc.reflections ?? []);
      return;
    }
    getDoc(doc(db, 'progress', user.uid))
      .then(snap => setReflections((snap.data()?.reflections as StudyReflection[] | undefined) ?? []))
      .catch((e) => logError('StudySessionView.loadReflections', e));
  };

  // XP popup state

  // Previous debrief notes — surface "whatWorked" back to the student
  const [prevDebriefs, setPrevDebriefs] = useState<DebriefEntry[]>([]);
  useEffect(() => {
    if (!user.uid) return;
    if (isDemo) {
      setPrevDebriefs(rawProgressDoc.studyDebriefs ?? []);
      setReflections(rawProgressDoc.reflections ?? []);
      return;
    }
    let cancelled = false;
    getDoc(doc(db, 'progress', user.uid)).then(snap => {
      if (cancelled) return;
      const data = snap.data();
      if (data?.studyDebriefs) setPrevDebriefs(data.studyDebriefs);
      if (data?.reflections) setReflections(data.reflections as StudyReflection[]);
    }).catch((e) => logError('StudySessionView.loadPrevDebriefs', e));
    return () => { cancelled = true; };
  }, [user.uid, isDemo, rawProgressDoc.studyDebriefs, rawProgressDoc.reflections]);

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

  const canStart = Boolean(
    selectedSubject
    && selectedType
    && selectedMinutes >= MIN_STUDY_SESSION_MINUTES,
  );
  const startHint = !selectedSubject
    ? 'Choose a subject to continue'
    : !selectedType
      ? 'Choose how you want to study'
      : selectedMinutes < MIN_STUDY_SESSION_MINUTES
        ? `Choose at least ${MIN_STUDY_SESSION_MINUTES} minutes`
        : null;

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
    if (!session.canRecordSession) {
      session.cancelSession();
      return;
    }
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
      if (isDemo) {
        updateDemoProgress(current => ({
          ...current,
          reflections: [...(current.reflections ?? []), reflection],
        }));
      } else {
        saveInBackground(
          setDoc(doc(db, 'progress', user.uid), {
            reflections: arrayUnion(reflection),
          }, { merge: true }),
          'StudySessionView.saveReflection',
          () => setReflections(previous => previous.filter(entry => entry.timestamp !== timestamp)),
        );
      }

      await session.saveSession(bonus, selectedStrategies, {
        confidenceAfter,
        confidenceLabel,
        reflectionMode,
      });
      completeTimetableBlock();
      pointsReload();
      onStrategyMasteryRecompute?.();
      weeklyChallenge?.reload();
      setPickerDone(false);
      setSelectedStrategies([]);
      session.resetSession();
    } catch (error) {
      logError('StudySessionView.saveReflection', error);
      throw error;
    } finally {
      setIsSaving(false);
    }
  };

  const handleSkipReflection = async () => {
    if (!session.canRecordSession) {
      session.cancelSession();
      return;
    }
    setIsSaving(true);
    try {
      await session.saveSession(0, selectedStrategies);
      completeTimetableBlock();
      pointsReload();
      onStrategyMasteryRecompute?.();
      weeklyChallenge?.reload();
      setPickerDone(false);
      setSelectedStrategies([]);
      session.resetSession();
    } finally { setIsSaving(false); }

  };

  const _handleDebriefSubmit = async (entry: Omit<DebriefEntry, 'id' | 'date'>) => {
    if (!session.canRecordSession) {
      setDebriefOpen(false);
      session.cancelSession();
      return;
    }
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

  // ── SETUP PHASE ──
  if (session.phase === 'idle') {
    return (
      <div className="ss-view">
        <StudySessionSetup
          colourfulTimer={timerAppearance === 'layers'}
          onColourfulTimerChange={value => setTimerAppearance(value ? 'layers' : 'ink')}
          subjects={subjects}
          selectedSubject={selectedSubject}
          selectedType={selectedType}
          selectedMinutes={selectedMinutes}
          onSubject={setSelectedSubject}
          onType={setSelectedType}
          onMinutes={setSelectedMinutes}
          todayBlocks={computedTodayBlocks}
          onBlock={block => {
            if (onStudyBlock) onStudyBlock(block);
            else {
              setSelectedSubject(block.subject);
              setSelectedType(block.sessionType);
              setSelectedMinutes(block.durationMinutes);
            }
          }}
          sessionCount={session.todaySessions.length}
          todayMinutes={session.todayTotalMinutes}
          reflectionCount={reflections.length}
          lastNote={lastSubjectNote?.whatWorked}
          strategyMastery={strategyMastery}
          onProgress={onGoToProgress}
          onReflections={() => { loadReflections(); setJournalOpen(true); }}
          onBack={onBack}
          onSetUpProfile={onSetUpProfile}
          onStart={handleStart}
          canStart={canStart}
          startHint={startHint}
        />

        {/* Points Explainer (first visit) */}
        <PointsExplainer
          isOpen={!dismissedGuides?.['points-explainer']}
          onDismiss={() => {
            onDismissGuide?.('points-explainer');
            onDismissGuide?.('study-session-intro');
          }}
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
    const subjectHex = getSubjectFill(session.subject);
    const typeConfig = SESSION_TYPE_CONFIG[session.sessionType];

    const handleEndEarly = () => {
      if (!session.canRecordSession) return;
      session.endSession();
      setConfirmQuit(false);
    };

    const handleDiscard = () => {
      session.cancelSession();
      setConfirmQuit(false);
    };

    return (
      <div className="ss-timer-view">
        {session.phase === 'paused' ? <StudyBreak subject={session.subject} elapsedSeconds={session.elapsedSeconds} onResume={session.resumeSession} onLeave={() => setConfirmQuit(true)} /> : <StudySessionTimer
          appearance={timerAppearance}
          subject={session.subject}
          subjectColor={subjectHex}
          type={typeConfig.label}
          totalSeconds={session.totalDuration}
          elapsedSeconds={session.elapsedSeconds}
          paused={false}
          onLeave={() => setConfirmQuit(true)}
          onTogglePause={session.pauseSession}
          prompt={session.currentPrompt}
          onCompletePrompt={session.completePrompt}
          onSkipPrompt={session.dismissPrompt}
        />}

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
              tabIndex={-1}
              ref={exitDialogRef}
            >
              <MotionDiv
                initial={{ opacity: 0, y: 12, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.98 }}
                transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
                className="ss-exit-panel"
              >
                <p className="mb-2 text-[10px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">Leave session</p>
                <h2 id="study-exit-title" className="font-serif text-2xl font-bold text-[#1A1A1A]">End this study session?</h2>
                <p className="mt-2 text-sm leading-relaxed text-[#7A7068]">
                  {session.canRecordSession
                    ? 'End early to record the time you have studied and continue to your debrief, or discard the session without saving it.'
                    : `Study for at least ${MIN_STUDY_SESSION_MINUTES} minutes to record this session. You can keep studying or discard this start.`}
                </p>
                <div className="mt-6 grid gap-2">
                  <button
                    type="button"
                    onClick={() => setConfirmQuit(false)}
                    className="ss-keep-studying"
                  >
                    Keep studying
                  </button>
                  <button
                    type="button"
                    onClick={handleEndEarly}
                    disabled={!session.canRecordSession}
                    className="ss-end-early"
                  >
                    {session.canRecordSession
                      ? 'End early and debrief'
                      : `End early after ${MIN_STUDY_SESSION_MINUTES} min`}
                  </button>
                  <button
                    type="button"
                    onClick={handleDiscard}
                    className="ss-discard"
                  >
                    Discard without saving
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

    return <StudySessionFinish
      subject={session.subject} elapsedSeconds={session.elapsedSeconds}
      plannedSeconds={session.totalDuration} practice={SESSION_TYPE_CONFIG[session.sessionType].label}
      character={user.avatar} basePoints={session.basePointsEarned}
      strategies={[...new Set([...session.getTrackedStrategies(), ...selectedStrategies])].map(id => STRATEGY_REGISTRY.find(strategy => strategy.moduleId === id)?.strategyName ?? id)}
      isSaving={isSaving} mode={reflectionMode} onModeChange={setReflectionMode}
      onSave={handleSaveWithReflection} onSkip={handleSkipReflection}
    />;
  }

  return null;
};

export default StudySessionView;
