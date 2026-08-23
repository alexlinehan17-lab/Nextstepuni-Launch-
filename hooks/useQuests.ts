/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import { doc, increment, runTransaction } from 'firebase/firestore';
import { db } from '../firebase';
import { awaitWriteOrTimeout } from '../utils/firestoreWrite';
import { useProgress } from '../contexts/ProgressContext';
import { type UserProgress } from '../types';
import { type StreakData } from './useStreak';
import { type StudentSubjectProfile, toDateKey } from '../components/subjectData';
import { type CourseData } from '../components/Library';
import {
  ONBOARDING_QUESTS,
  PERSONALIZED_TEMPLATES,
  hashSeed,
  type QuestDefinition,
  type PersonalizedQuestTemplate,
} from '../questData';
import { normaliseDailyQuestJP } from '../journeyEconomyConfig';
import { DEMO_STUDENT_UID } from '../data/devStudent';

// ── Types ──────────────────────────────────────────────────

export interface QuestState {
  quest: QuestDefinition;
  current: number;
  isCompleted: boolean;
  isClaimed: boolean;
  dayNumber: number;
  isOnboarding: boolean;
}

// ── Helpers ────────────────────────────────────────────────

function getDayNumber(createdAt: string | undefined): number {
  if (!createdAt) return 1;
  const created = new Date(createdAt);
  const now = new Date();
  const diff = now.getTime() - created.getTime();
  return Math.max(1, Math.ceil(diff / 86400000));
}

function fillTemplate(
  template: PersonalizedQuestTemplate,
  subject: string,
  moduleName: string,
): QuestDefinition {
  const todayKey = toDateKey(new Date());
  return {
    id: `${template.id}-${todayKey}`,
    title: template.titleTemplate
      .replace('{subject}', subject)
      .replace('{module}', moduleName),
    description: template.descTemplate
      .replace('{subject}', subject)
      .replace('{module}', moduleName),
    metric: template.metric,
    target: template.target,
    rewardPoints: template.rewardPoints,
    subjectName: subject || undefined,
  };
}

// ── Hook ───────────────────────────────────────────────────

export function useQuests(
  uid: string | undefined,
  userProgress: UserProgress,
  courses: CourseData[],
  streak: StreakData,
  studentProfile: StudentSubjectProfile | null,
  timetableCompletions: Record<string, string[]> | undefined,
): { questState: QuestState | null; claimReward: () => Promise<void>; reload: () => void } {
  const {
    studySessions: sessions,
    studyDebriefs: debriefs,
    topicMasteryV2,
    unifiedMockResults: mockResults,
    questRewards: firestoreRewards,
    progressLoaded,
    reloadProgress,
    updateDemoProgress,
  } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const isMountedRef = useRef(true);
  useEffect(() => () => { isMountedRef.current = false; }, []);

  const [localClaimedIds, setLocalClaimedIds] = useState<Record<string, string>>({});
  const questRewards = { ...firestoreRewards, ...localClaimedIds };
  const isLoaded = progressLoaded;

  const reload = useCallback(() => {
    reloadProgress();
  }, [reloadProgress]);

  // Determine which quest to show
  const questState = useMemo((): QuestState | null => {
    if (!isLoaded || !uid) return null;

    // Phase 5 plumbing: JC users see no quests for now. Existing onboarding
    // quests + personalized templates default to senior. JC-specific quest
    // content is deferred to a later phase.
    const curriculumLevel = studentProfile?.curriculumLevel ?? 'senior';
    const passesCurriculum = (c: 'junior' | 'senior' | 'both' | undefined) => {
      const tag = c ?? 'senior';
      return tag === 'both' || tag === curriculumLevel;
    };

    const dayNumber = getDayNumber(studentProfile?.createdAt);
    const todayKey = toDateKey(new Date());
    const isOnboarding = dayNumber >= 1 && dayNumber <= 7;

    // Pick quest definition
    let quest: QuestDefinition;

    if (isOnboarding) {
      const candidate = ONBOARDING_QUESTS[dayNumber - 1];
      if (!candidate || !passesCurriculum(candidate.curriculum)) return null;
      quest = candidate;
    } else {
      // Determine condition context
      const canonicalMastery = Object.values(topicMasteryV2.topics);
      const hasShaky = canonicalMastery.some(topic => topic.confidence === 'shaky');

      const inProgressModule = courses.find(c => {
        const p = userProgress[c.id];
        return p && p.unlockedSection > 0 && p.unlockedSection < c.sectionsCount;
      });

      const hasSubjects = !!studentProfile && studentProfile.subjects.length > 0;
      const streakActive = streak.currentStreak > 0;

      // Filter eligible templates (also gated by curriculum — Phase 5).
      const eligible = PERSONALIZED_TEMPLATES.filter(t => {
        if (!passesCurriculum(t.curriculum)) return false;
        switch (t.condition) {
          case 'has-shaky-topics': return hasShaky;
          case 'has-in-progress-module': return !!inProgressModule;
          case 'streak-active': return streakActive;
          case 'has-subjects': return hasSubjects;
          case 'always': return true;
          default: return true;
        }
      });

      if (eligible.length === 0) return null;

      // Deterministic selection
      const seed = hashSeed(todayKey + uid);
      const selected = eligible[seed % eligible.length];

      // Find weakest subject (most shaky topics)
      let weakestSubject = studentProfile?.subjects[0]?.subjectName ?? '';
      if (canonicalMastery.length > 0) {
        let worstCount = -1;
        const bySubject = new Map<string, typeof canonicalMastery>();
        for (const entry of canonicalMastery) {
          const entries = bySubject.get(entry.subjectName) ?? [];
          entries.push(entry);
          bySubject.set(entry.subjectName, entries);
        }
        for (const [subject, topics] of bySubject) {
          const shakyCount = topics.filter(topic => topic.confidence === 'shaky').length;
          if (shakyCount > worstCount) {
            worstCount = shakyCount;
            weakestSubject = subject;
          }
        }
      }

      const inProgressName = inProgressModule?.title ?? '';

      quest = fillTemplate(selected, weakestSubject, inProgressName);
    }

    // Compute current progress
    let current = 0;
    switch (quest.metric) {
      case 'study-session': {
        current = sessions.filter(s => s.date === todayKey).length;
        break;
      }
      case 'subject-session': {
        current = sessions.filter(s => s.date === todayKey && s.subject === quest.subjectName).length;
        break;
      }
      case 'debrief': {
        current = debriefs.filter(d => d.date === todayKey).length;
        break;
      }
      case 'timetable-block': {
        current = timetableCompletions?.[todayKey]?.length ?? 0;
        break;
      }
      case 'module-start': {
        const started = Object.values(userProgress).some(p => p.unlockedSection > 0);
        current = started ? 1 : 0;
        break;
      }
      case 'module-complete': {
        current = courses.filter(c => {
          const p = userProgress[c.id];
          return p && p.unlockedSection >= c.sectionsCount;
        }).length;
        break;
      }
      case 'specific-module': {
        // Check if any in-progress module is now complete
        const completed = courses.some(c => {
          const p = userProgress[c.id];
          return p && p.unlockedSection >= c.sectionsCount;
        });
        current = completed ? 1 : 0;
        break;
      }
      case 'streak-hit': {
        current = streak.currentStreak;
        break;
      }
      case 'topic-update': {
        if (Object.keys(topicMasteryV2.topics).length > 0) {
          const todayStart = new Date(todayKey + 'T00:00:00').getTime();
          current = Object.values(topicMasteryV2.topics)
            .filter(entry => entry.updatedAt >= todayStart).length;
        }
        break;
      }
      case 'mock-entry': {
        current = mockResults.filter((m: any) => m.date === todayKey).length;
        break;
      }
      default:
        current = 0;
    }

    const isCompleted = current >= quest.target;
    const isClaimed = !!questRewards[quest.id];

    const liveQuest = {
      ...quest,
      rewardPoints: normaliseDailyQuestJP(quest.rewardPoints, isOnboarding),
    };

    return { quest: liveQuest, current, isCompleted, isClaimed, dayNumber, isOnboarding };
  }, [isLoaded, uid, studentProfile, topicMasteryV2, courses, userProgress, sessions, debriefs, streak, timetableCompletions, questRewards, mockResults]);

  // Claim reward — set questRewards IMMEDIATELY (before the write) to prevent
  // the button from being clickable during the Firestore round-trip
  const claimingRef = useRef(false);
  const claimReward = useCallback(async () => {
    if (!uid || !questState || questState.isClaimed || !questState.isCompleted) return;
    if (claimingRef.current) return;
    claimingRef.current = true;
    // Optimistic: mark as claimed immediately so the UI hides the button
    const questId = questState.quest.id;
    const rewardPoints = questState.quest.rewardPoints;
    setLocalClaimedIds(prev => ({ ...prev, [questId]: new Date().toISOString() }));
    try {
      if (isDemo) {
        const claimedAt = new Date().toISOString();
        updateDemoProgress(current => ({
          ...current,
          pointsData: {
            ...current.pointsData,
            totalEarned: (current.pointsData?.totalEarned ?? 0) + rewardPoints,
          },
          questRewards: { ...(current.questRewards ?? {}), [questId]: claimedAt },
        }));
        return;
      }
      // Transaction: read the questRewards map; bail if this questId is already
      // claimed (covers the multi-tab race where two tabs both pass the optimistic
      // gate). Firestore rules also reject overwrites, but failing fast here
      // avoids a useless round-trip and a confusing rules error in the console.
      // Bounded: a transaction needs a server round-trip, so offline it can
      // stall long past any useful UI deadline — which would leave claimingRef
      // latched and the Claim button dead for the rest of the session.
      const outcome = await awaitWriteOrTimeout(runTransaction(db, async (txn) => {
        const ref = doc(db, 'progress', uid);
        const snap = await txn.get(ref);
        const existing = (snap.data()?.questRewards ?? {}) as Record<string, string>;
        if (existing[questId]) return; // Already claimed in another tab
        txn.set(ref, {
          pointsData: { totalEarned: increment(rewardPoints) },
          questRewards: { [questId]: new Date().toISOString() },
        }, { merge: true });
      }), 'useQuests.claimReward');
      // 'pending' means queued — treat it as claimed; only a real rejection
      // unwinds the optimistic update below.
      if (outcome === 'failed') throw new Error('useQuests.claimReward: rejected');
    } catch (err) {
      console.error('Failed to claim quest reward:', err);
      // Roll back optimistic update
      if (isMountedRef.current) setLocalClaimedIds(prev => {
        const next = { ...prev };
        delete next[questId];
        return next;
      });
    } finally {
      claimingRef.current = false;
    }
  }, [uid, questState, isDemo, updateDemoProgress]);

  return { questState, claimReward, reload };
}
