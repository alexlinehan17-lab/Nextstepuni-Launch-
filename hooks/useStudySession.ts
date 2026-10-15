/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { useProgress } from '../contexts/ProgressContext';
import { type StudyConfidenceLabel, type UserProgress } from '../types';
import { type CourseData } from '../components/Library';
import { toDateKey } from '../utils/weekDates';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import {
  type StrategyPrompt,
  type StudySessionRecord,
  STRATEGY_PROMPTS,
  STUDY_SESSION_POINTS,
  SESSION_EXTENSION_MINUTES,
  OPEN_ENDED_CAP_MINUTES,
  PROMPT_INTERVAL_SECONDS,
  PROMPT_AUTO_DISMISS_SECONDS,
} from '../studySessionData';
import type { StudyTopicAllocation, StudyTopicSelection } from '../types/studyTopics';
import { equalTopicAllocations, sameStudySubject, validTopicAllocations, sessionTopicAllocations } from '../services/studyTopicHistory';
import { analyticsDurationBucket, trackProgrammeEvent } from '../utils/programmeAnalytics';
import { readActiveStudySession, recordStudySession, writeActiveStudySession, type ActiveStudySession } from '../services/studySessionStore';

// ── Types ──────────────────────────────────────────────────

export type SessionPhase = 'idle' | 'active' | 'paused' | 'complete';

export interface SessionReflectionMetadata {
  confidenceAfter: number;
  confidenceLabel: StudyConfidenceLabel;
  reflectionMode: 'quick' | 'full';
}

/**
 * Five minutes is the shortest session the setup screen offers. Keep the same
 * floor at the persistence boundary so an accidental start (or a caller that
 * bypasses the UI) cannot create a zero-minute session or earn debrief JP.
 */
export const MIN_STUDY_SESSION_MINUTES = 5;
export const MIN_RECORDABLE_SESSION_SECONDS = MIN_STUDY_SESSION_MINUTES * 60;

/** Seconds the clock runs to: the plan plus any "Keep going" time, or the
 *  open-ended cap for a stopwatch session. */
const sessionLengthSeconds = (plannedMinutes: number, extendedMinutes: number, openEnded: boolean) =>
  (openEnded ? OPEN_ENDED_CAP_MINUTES : plannedMinutes + extendedMinutes) * 60;

/** A session saved by this tab before a reload, brought up to date. */
function restoreActiveSession(uid: string | undefined): ActiveStudySession | null {
  const saved = uid ? readActiveStudySession(uid) : null;
  if (!saved || !saved.startedAt || (!saved.plannedMinutes && !saved.openEnded)) return null;
  if (saved.phase !== 'active') return saved;
  const total = sessionLengthSeconds(saved.plannedMinutes, saved.extendedMinutes ?? 0, Boolean(saved.openEnded));
  const elapsed = Math.min(total, Math.max(0, Math.round((Date.now() - saved.startedAt) / 1000)));
  return { ...saved, elapsedSeconds: elapsed, phase: elapsed >= total ? 'complete' : 'active' };
}

// Fisher-Yates shuffle
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── Hook ───────────────────────────────────────────────────

export function useStudySession(
  uid: string | undefined,
  userProgress: UserProgress,
  allCourses: CourseData[],
) {
  const { studySessions, progressLoaded, updateDemoProgress, addStudySession, reloadProgress } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;

  // A session survives the page reloading underneath it (iPad Safari reloads
  // a backgrounded tab), and time away in another app still counts.
  const [restored] = useState(() => restoreActiveSession(uid));
  const [phase, setPhase] = useState<SessionPhase>(restored?.phase ?? 'idle');
  const [subject, setSubject] = useState(restored?.subject ?? '');
  const [topicSelection, setTopicSelection] = useState<StudyTopicSelection | undefined>(restored?.topicSelection);
  const [sessionType, setSessionType] = useState<'new-learning' | 'practice' | 'revision'>(restored?.sessionType ?? 'new-learning');
  const [plannedMinutes, setPlannedMinutes] = useState(restored?.plannedMinutes ?? 25);
  const [elapsedSeconds, setElapsedSeconds] = useState(restored?.elapsedSeconds ?? 0);
  const [extendedMinutes, setExtendedMinutes] = useState(restored?.extendedMinutes ?? 0);
  const [openEnded, setOpenEnded] = useState(Boolean(restored?.openEnded));
  const [currentPrompt, setCurrentPrompt] = useState<StrategyPrompt | null>(null);
  const [todaySessions, setTodaySessions] = useState<StudySessionRecord[]>([]);

  const [promptShownAt, setPromptShownAt] = useState<number>(0); // timestamp when current prompt appeared

  const intervalRef = useRef<number | null>(null);
  const startTimeRef = useRef<number>(restored?.startedAt ?? 0);
  const expectedEndRef = useRef<number>(0);
  const promptQueueRef = useRef<StrategyPrompt[]>([]);
  const promptIndexRef = useRef<number>(0);
  const nextPromptTimeRef = useRef<number>(0); // elapsed seconds when next prompt should show
  const autoDismissRef = useRef<number | null>(null);
  const completedPromptsRef = useRef<Set<string>>(new Set(restored?.completedPrompts)); // moduleIds user marked "Done"

  const totalDuration = sessionLengthSeconds(plannedMinutes, extendedMinutes, openEnded);
  /** The original plan, before any "Keep going" time. */
  const plannedSeconds = openEnded ? 0 : plannedMinutes * 60;

  // ── Load today's sessions from context ──

  useEffect(() => {
    if (!progressLoaded) return;
    // Local calendar day, the same key saved sessions carry (toISOString is
    // UTC, which dropped sessions logged just after midnight in Ireland).
    const today = toDateKey(new Date());
    setTodaySessions(studySessions.filter(s => s.date === today));
  }, [progressLoaded, studySessions]);

  // ── Build shuffled prompt queue from completed strategies ──

  const buildPromptQueue = useCallback(() => {
    const completedModuleIds = new Set<string>();
    for (const course of allCourses) {
      const progress = userProgress[course.id];
      if (progress && progress.unlockedSection >= course.sectionsCount) {
        completedModuleIds.add(course.id);
      }
    }

    const available = STRATEGY_PROMPTS.filter(p => completedModuleIds.has(p.moduleId));
    promptQueueRef.current = shuffle(available);
    promptIndexRef.current = 0;
    nextPromptTimeRef.current = 0; // show first prompt immediately
    completedPromptsRef.current = new Set();
  }, [userProgress, allCourses]);

  // ── Show next prompt from queue ──

  const showNextPrompt = useCallback(() => {
    const queue = promptQueueRef.current;
    const idx = promptIndexRef.current;
    if (idx >= queue.length) return; // no more prompts

    setCurrentPrompt(queue[idx]);
    setPromptShownAt(Date.now());
    promptIndexRef.current = idx + 1;
    nextPromptTimeRef.current += PROMPT_INTERVAL_SECONDS;

    // Auto-dismiss after 30s
    if (autoDismissRef.current) clearTimeout(autoDismissRef.current);
    autoDismissRef.current = window.setTimeout(() => {
      setCurrentPrompt(null);
      setPromptShownAt(0);
      autoDismissRef.current = null;
    }, PROMPT_AUTO_DISMISS_SECONDS * 1000);
  }, []);

  // ── Timer tick — show prompts based on elapsed time (every ~5 min) ──

  const updatePrompt = useCallback((elapsed: number) => {
    if (elapsed >= nextPromptTimeRef.current) {
      showNextPrompt();
    }
  }, [showNextPrompt]);

  // ── Ticking ──

  const startTicking = useCallback((total: number) => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = window.setInterval(() => {
      const elapsed = Math.round((Date.now() - startTimeRef.current) / 1000);
      const clamped = Math.min(elapsed, total);
      setElapsedSeconds(clamped);
      updatePrompt(clamped);

      if (clamped >= total) {
        if (intervalRef.current) clearInterval(intervalRef.current);
        intervalRef.current = null;
        if (autoDismissRef.current) clearTimeout(autoDismissRef.current);
        setPhase('complete');
      }
    }, 1000);
  }, [updatePrompt]);

  // ── Start ──

  const startSession = useCallback((subj: string, type: 'new-learning' | 'practice' | 'revision', minutes: number, topics?: StudyTopicSelection, options: { openEnded?: boolean } = {}) => {
    if (topics && (!sameStudySubject(subj, topics.subjectId) || !validTopicAllocations(topics, equalTopicAllocations(topics.topicIds, 0), 0))) {
      throw new Error('Choose topics from the selected subject.');
    }
    setTopicSelection(topics ? { ...topics, topicIds: [...topics.topicIds] } : undefined);
    setSubject(subj);
    setSessionType(type);
    const stopwatch = Boolean(options.openEnded);
    setOpenEnded(stopwatch);
    setExtendedMinutes(0);
    setPlannedMinutes(stopwatch ? 0 : minutes);
    setElapsedSeconds(0);
    setCurrentPrompt(null);
    setPromptShownAt(0);

    buildPromptQueue();

    const now = Date.now();
    startTimeRef.current = now;
    const length = sessionLengthSeconds(minutes, 0, stopwatch);
    expectedEndRef.current = now + length * 1000;
    setPhase('active');
    if (uid && !isDemo) {
      trackProgrammeEvent('study_session_started', { source: 'study', sessionType: type });
    }

    // Show first prompt immediately
    showNextPrompt();
    startTicking(length);
  }, [buildPromptQueue, showNextPrompt, startTicking, uid, isDemo]);

  // ── Pause ──

  const pauseSession = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setPhase('paused');
  }, []);

  // ── Resume ──

  const resumeSession = useCallback(() => {
    setPhase('active');
    // Recalculate expected end based on remaining time
    const remaining = totalDuration - elapsedSeconds;
    startTimeRef.current = Date.now() - elapsedSeconds * 1000;
    expectedEndRef.current = Date.now() + remaining * 1000;
    startTicking(totalDuration);
  }, [totalDuration, elapsedSeconds, startTicking]);

  // ── Keep going ──

  /** When a countdown has run out, add time to the same session. */
  const extendSession = useCallback((minutes: number): boolean => {
    if (phase !== 'complete' || openEnded || elapsedSeconds < totalDuration) return false;
    if (!(SESSION_EXTENSION_MINUTES as readonly number[]).includes(minutes)) return false;
    const nextTotal = totalDuration + minutes * 60;
    setExtendedMinutes(current => current + minutes);
    startTimeRef.current = Date.now() - elapsedSeconds * 1000;
    expectedEndRef.current = Date.now() + minutes * 60 * 1000;
    setPhase('active');
    startTicking(nextTotal);
    return true;
  }, [phase, openEnded, elapsedSeconds, totalDuration, startTicking]);

  // ── End Early ──

  const canRecordSession = elapsedSeconds >= MIN_RECORDABLE_SESSION_SECONDS;

  const endSession = useCallback((): boolean => {
    if (elapsedSeconds < MIN_RECORDABLE_SESSION_SECONDS) return false;
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setPhase('complete');
    return true;
  }, [elapsedSeconds]);

  // Abandoning an unfinished session is deliberately different from ending
  // early: it returns to setup without creating a session, points or debrief.
  const cancelSession = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (autoDismissRef.current) {
      clearTimeout(autoDismissRef.current);
      autoDismissRef.current = null;
    }
    promptQueueRef.current = [];
    completedPromptsRef.current = new Set();
    startTimeRef.current = 0;
    expectedEndRef.current = 0;
    setElapsedSeconds(0);
    setExtendedMinutes(0);
    setOpenEnded(false);
    setCurrentPrompt(null);
    setPromptShownAt(0);
    setPhase('idle');
    setTopicSelection(undefined);
  }, []);

  // ── Complete Prompt (user marked "Done") ──

  const completePrompt = useCallback(() => {
    if (currentPrompt) {
      completedPromptsRef.current.add(currentPrompt.moduleId);
      const saved = uid ? readActiveStudySession(uid) : null;
      if (uid && saved) writeActiveStudySession(uid, { ...saved, completedPrompts: [...completedPromptsRef.current] });
      setCurrentPrompt(null);
      setPromptShownAt(0);
      if (autoDismissRef.current) {
        clearTimeout(autoDismissRef.current);
        autoDismissRef.current = null;
      }
    }
  }, [currentPrompt, uid]);

  // ── Visibility change correction ──

  useEffect(() => {
    const handleVisibility = () => {
      if (document.visibilityState === 'visible' && phase === 'active' && startTimeRef.current > 0) {
        const elapsed = Math.round((Date.now() - startTimeRef.current) / 1000);
        const clamped = Math.min(elapsed, totalDuration);
        setElapsedSeconds(clamped);
        updatePrompt(clamped);

        if (clamped >= totalDuration) {
          if (intervalRef.current) clearInterval(intervalRef.current);
          intervalRef.current = null;
          if (autoDismissRef.current) clearTimeout(autoDismissRef.current);
          setPhase('complete');
        }
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    return () => document.removeEventListener('visibilitychange', handleVisibility);
  }, [phase, totalDuration, updatePrompt]);

  // ── Keep the running session safe across reloads ──

  useEffect(() => {
    if (!uid) return;
    writeActiveStudySession(uid, phase === 'idle' ? null : {
      subject, sessionType, plannedMinutes, topicSelection,
      startedAt: startTimeRef.current,
      phase,
      elapsedSeconds,
      completedPrompts: [...completedPromptsRef.current],
      ...(extendedMinutes ? { extendedMinutes } : {}),
      ...(openEnded ? { openEnded } : {}),
    });
    // elapsedSeconds is read, not tracked: while active it is derived from
    // startedAt, and pause/complete each change phase with it already set.
  }, [uid, phase, subject, sessionType, plannedMinutes, topicSelection, extendedMinutes, openEnded]);

  useEffect(() => {
    if (restored?.phase !== 'active') return;
    buildPromptQueue();
    // buildPromptQueue starts a fresh "Done" set; keep the ones already marked.
    completedPromptsRef.current = new Set(restored.completedPrompts);
    // Carry on from the next prompt slot rather than replaying the first one.
    nextPromptTimeRef.current = Math.ceil(restored.elapsedSeconds / PROMPT_INTERVAL_SECONDS) * PROMPT_INTERVAL_SECONDS;
    const length = sessionLengthSeconds(restored.plannedMinutes, restored.extendedMinutes ?? 0, Boolean(restored.openEnded));
    expectedEndRef.current = restored.startedAt + length * 1000;
    startTicking(length);
    // Once, for the session this hook was restored with.
  }, []);

  // ── Cleanup on unmount ──

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (autoDismissRef.current) clearTimeout(autoDismissRef.current);
    };
  }, []);

  // ── Points calculation ──

  const basePointsEarned = Math.floor(elapsedSeconds / 600) * STUDY_SESSION_POINTS.PER_10_MINUTES;
  /** Earned by finishing the time added with "Keep going"; ending it early forfeits it. */
  const extensionBonus = !openEnded && extendedMinutes > 0 && elapsedSeconds >= totalDuration
    ? STUDY_SESSION_POINTS.EXTENSION_COMPLETED
    : 0;

  // ── Save session to Firestore ──

  const saveSession = useCallback(async (
    reflectionPoints: number = 0,
    extraStrategies?: string[],
    reflectionMetadata?: SessionReflectionMetadata,
    allocations?: StudyTopicAllocation[],
  ): Promise<boolean> => {
    if (!uid || elapsedSeconds < MIN_RECORDABLE_SESSION_SECONDS) return false;
    const topicAllocations = sessionTopicAllocations(topicSelection, elapsedSeconds, allocations);

    const now = Date.now();
    // Merge auto-tracked (prompt "Done") with self-reported strategies, deduplicated
    const merged = new Set(completedPromptsRef.current);
    if (extraStrategies) {
      for (const id of extraStrategies) merged.add(id);
    }
    const shownModuleIds = [...merged];

    const record: StudySessionRecord = {
      id: `ss_${now}`,
      date: toDateKey(new Date(now)),
      subject,
      sessionType,
      // An open-ended session had no plan, so it records the time it took.
      plannedMinutes: openEnded ? Math.round(elapsedSeconds / 60) : plannedMinutes,
      actualSeconds: elapsedSeconds,
      startedAt: startTimeRef.current,
      completedAt: now,
      pointsEarned: basePointsEarned + reflectionPoints + extensionBonus,
      hadReflection: reflectionPoints > 0,
      ...(shownModuleIds.length > 0 ? { strategiesShown: shownModuleIds } : {}),
      ...(reflectionMetadata ?? {}),
      ...(topicSelection ? { subjectId: topicSelection.subjectId, specificationId: topicSelection.specificationId, topicAllocations } : {}),
      ...(extendedMinutes > 0 ? { extendedMinutes, extensionBonus } : {}),
      ...(openEnded ? { openEnded: true } : {}),
    };

    const totalPoints = basePointsEarned + reflectionPoints + extensionBonus;

    if (!isDemo) {
      trackProgrammeEvent('study_session_completed', {
        source: 'study',
        sessionType,
        durationBucket: analyticsDurationBucket(elapsedSeconds),
        ...(reflectionMetadata?.confidenceAfter
          ? { confidenceScore: Math.max(1, Math.min(5, Math.round(reflectionMetadata.confidenceAfter))) }
          : {}),
      });
    }

    // Update local state immediately (optimistic)
    setTodaySessions(prev => [...prev, record]);
    writeActiveStudySession(uid, null);

    if (isDemo) {
      updateDemoProgress(current => ({
        ...current,
        studySessions: [...(current.studySessions ?? []), record],
        pointsData: {
          ...current.pointsData,
          totalEarned: (current.pointsData?.totalEarned ?? 0) + totalPoints,
        },
      }));
      return true;
    }

    // Each session is its own subcollection doc so /progress/{uid} doesn't grow
    // unboundedly. Not awaited: a student on bad wifi still reaches the
    // completion screen. The Firestore cache is memory-only, so the record
    // waits in this tab's outbox until the write is acknowledged; a reload
    // before then retries it (ProgressContext) instead of losing it.
    addStudySession(record);
    void recordStudySession(uid, { record, points: totalPoints }).then(saved => {
      if (saved) reloadProgress();
    });
    return true;
  }, [uid, subject, sessionType, plannedMinutes, elapsedSeconds, basePointsEarned, extensionBonus, extendedMinutes, openEnded, isDemo, updateDemoProgress, topicSelection, addStudySession, reloadProgress]);

  // ── Reset to idle ──

  const resetSession = useCallback(() => {
    setPhase('idle');
    setTopicSelection(undefined);
    setElapsedSeconds(0);
    setExtendedMinutes(0);
    setOpenEnded(false);
    setCurrentPrompt(null);
    setPromptShownAt(0);
    startTimeRef.current = 0;
    expectedEndRef.current = 0;
    if (autoDismissRef.current) {
      clearTimeout(autoDismissRef.current);
      autoDismissRef.current = null;
    }
  }, []);

  // ── Today stats ──

  const todayTotalMinutes = Math.round(
    todaySessions.reduce((acc, s) => acc + s.actualSeconds, 0) / 60
  );

  // Dismiss prompt (user taps "Skip") — also clear auto-dismiss
  const dismissPrompt = useCallback(() => {
    setCurrentPrompt(null);
    setPromptShownAt(0);
    if (autoDismissRef.current) {
      clearTimeout(autoDismissRef.current);
      autoDismissRef.current = null;
    }
  }, []);

  return {
    phase,
    subject,
    topicSelection,
    sessionType,
    plannedMinutes,
    plannedSeconds,
    elapsedSeconds,
    totalDuration,
    extendedMinutes,
    extensionBonus,
    openEnded,
    currentPrompt,
    promptShownAt,
    basePointsEarned,
    canRecordSession,
    todaySessions,
    todayTotalMinutes,
    startSession,
    pauseSession,
    resumeSession,
    endSession,
    extendSession,
    cancelSession,
    saveSession,
    resetSession,
    dismissPrompt,
    completePrompt,
    getTrackedStrategies: () => [...completedPromptsRef.current],
  };
}
