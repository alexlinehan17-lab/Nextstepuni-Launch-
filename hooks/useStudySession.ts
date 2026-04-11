/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { doc, updateDoc, increment, arrayUnion } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { type UserProgress } from '../types';
import { type CourseData } from '../components/Library';
import {
  type StrategyPrompt,
  type StudySessionRecord,
  STRATEGY_PROMPTS,
  STUDY_SESSION_POINTS,
  PROMPT_INTERVAL_SECONDS,
  PROMPT_AUTO_DISMISS_SECONDS,
} from '../studySessionData';

// ── Types ──────────────────────────────────────────────────

export type SessionPhase = 'idle' | 'active' | 'paused' | 'complete';

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
  const { rawProgressDoc, progressLoaded } = useProgress();

  const [phase, setPhase] = useState<SessionPhase>('idle');
  const [subject, setSubject] = useState('');
  const [sessionType, setSessionType] = useState<'new-learning' | 'practice' | 'revision'>('new-learning');
  const [plannedMinutes, setPlannedMinutes] = useState(25);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [currentPrompt, setCurrentPrompt] = useState<StrategyPrompt | null>(null);
  const [todaySessions, setTodaySessions] = useState<StudySessionRecord[]>([]);

  const [promptShownAt, setPromptShownAt] = useState<number>(0); // timestamp when current prompt appeared

  const intervalRef = useRef<number | null>(null);
  const startTimeRef = useRef<number>(0);
  const expectedEndRef = useRef<number>(0);
  const promptQueueRef = useRef<StrategyPrompt[]>([]);
  const promptIndexRef = useRef<number>(0);
  const nextPromptTimeRef = useRef<number>(0); // elapsed seconds when next prompt should show
  const autoDismissRef = useRef<number | null>(null);
  const completedPromptsRef = useRef<Set<string>>(new Set()); // moduleIds user marked "Done"

  const totalDuration = plannedMinutes * 60;

  // ── Load today's sessions from context ──

  useEffect(() => {
    if (!progressLoaded) return;
    const sessions: StudySessionRecord[] = rawProgressDoc.studySessions || [];
    const today = new Date().toISOString().slice(0, 10);
    setTodaySessions(sessions.filter(s => s.date === today));
  }, [progressLoaded, rawProgressDoc]);

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

  // ── Start ──

  const startSession = useCallback((subj: string, type: 'new-learning' | 'practice' | 'revision', minutes: number) => {
    setSubject(subj);
    setSessionType(type);
    setPlannedMinutes(minutes);
    setElapsedSeconds(0);
    setCurrentPrompt(null);
    setPromptShownAt(0);

    buildPromptQueue();

    const now = Date.now();
    startTimeRef.current = now;
    expectedEndRef.current = now + minutes * 60 * 1000;
    setPhase('active');

    // Show first prompt immediately
    showNextPrompt();

    // Start interval
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = window.setInterval(() => {
      const elapsed = Math.round((Date.now() - startTimeRef.current) / 1000);
      const total = minutes * 60;
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
  }, [buildPromptQueue, showNextPrompt, updatePrompt]);

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

    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = window.setInterval(() => {
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
    }, 1000);
  }, [totalDuration, elapsedSeconds, updatePrompt]);

  // ── End Early ──

  const endSession = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setPhase('complete');
  }, []);

  // ── Complete Prompt (user marked "Done") ──

  const completePrompt = useCallback(() => {
    if (currentPrompt) {
      completedPromptsRef.current.add(currentPrompt.moduleId);
      setCurrentPrompt(null);
      setPromptShownAt(0);
      if (autoDismissRef.current) {
        clearTimeout(autoDismissRef.current);
        autoDismissRef.current = null;
      }
    }
  }, [currentPrompt]);

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

  // ── Cleanup on unmount ──

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (autoDismissRef.current) clearTimeout(autoDismissRef.current);
    };
  }, []);

  // ── Points calculation ──

  const basePointsEarned = Math.floor(elapsedSeconds / 600) * STUDY_SESSION_POINTS.PER_10_MINUTES;

  // ── Save session to Firestore ──

  const saveSession = useCallback(async (reflectionPoints: number = 0, extraStrategies?: string[]): Promise<void> => {
    if (!uid) return;

    const now = Date.now();
    // Merge auto-tracked (prompt "Done") with self-reported strategies, deduplicated
    const merged = new Set(completedPromptsRef.current);
    if (extraStrategies) {
      for (const id of extraStrategies) merged.add(id);
    }
    const shownModuleIds = [...merged];

    const record: StudySessionRecord = {
      id: `ss_${now}`,
      date: new Date().toISOString().slice(0, 10),
      subject,
      sessionType,
      plannedMinutes,
      actualSeconds: elapsedSeconds,
      startedAt: startTimeRef.current,
      completedAt: now,
      pointsEarned: basePointsEarned + reflectionPoints,
      hadReflection: reflectionPoints > 0,
      ...(shownModuleIds.length > 0 ? { strategiesShown: shownModuleIds } : {}),
    };

    const totalPoints = basePointsEarned + reflectionPoints;

    // Update local state immediately (optimistic)
    setTodaySessions(prev => [...prev, record]);

    // Fire-and-forget Firestore write — queues offline via persistence
    try {
      const progressDocRef = doc(db, 'progress', uid);
      const updates: Record<string, any> = {
        studySessions: arrayUnion(record),
      };
      if (totalPoints > 0) {
        updates['pointsData.totalEarned'] = increment(totalPoints);
      }
      updateDoc(progressDocRef, updates).catch(err => {
        console.error('Failed to save study session:');
      });
    } catch (err) {
      console.error('Failed to save study session:');
    }
  }, [uid, subject, sessionType, plannedMinutes, elapsedSeconds, basePointsEarned]);

  // ── Reset to idle ──

  const resetSession = useCallback(() => {
    setPhase('idle');
    setElapsedSeconds(0);
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
    sessionType,
    plannedMinutes,
    elapsedSeconds,
    totalDuration,
    currentPrompt,
    promptShownAt,
    basePointsEarned,
    todaySessions,
    todayTotalMinutes,
    startSession,
    pauseSession,
    resumeSession,
    endSession,
    saveSession,
    resetSession,
    dismissPrompt,
    completePrompt,
    getTrackedStrategies: () => [...completedPromptsRef.current],
  };
}
