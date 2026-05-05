/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import { doc, increment, runTransaction } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { type UserProgress, type TopicMasteryMap } from '../types';
import { type StreakData } from './useStreak';
import { type StudentSubjectProfile, toDateKey } from '../components/subjectData';
import { type CourseData } from '../components/Library';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { type DebriefEntry } from '../components/StudyDebrief';
import {
  ONBOARDING_QUESTS,
  PERSONALIZED_TEMPLATES,
  hashSeed,
  type QuestDefinition,
  type PersonalizedQuestTemplate,
} from '../questData';

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
    topicMastery,
    unifiedMockResults: mockResults,
    questRewards: firestoreRewards,
    progressLoaded,
    reloadProgress,
  } = useProgress();
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

    const dayNumber = getDayNumber(studentProfile?.createdAt);
    const todayKey = toDateKey(new Date());
    const isOnboarding = dayNumber >= 1 && dayNumber <= 7;

    // Pick quest definition
    let quest: QuestDefinition;

    if (isOnboarding) {
      quest = ONBOARDING_QUESTS[dayNumber - 1];
    } else {
      // Determine condition context
      const hasShaky = topicMastery
        ? Object.values(topicMastery).some(subjects =>
            Object.values(subjects).some(t => t.confidence === 'shaky')
          )
        : false;

      const inProgressModule = courses.find(c => {
        const p = userProgress[c.id];
        return p && p.unlockedSection > 0 && p.unlockedSection < c.sectionsCount;
      });

      const hasSubjects = !!studentProfile && studentProfile.subjects.length > 0;
      const streakActive = streak.currentStreak > 0;

      // Filter eligible templates
      const eligible = PERSONALIZED_TEMPLATES.filter(t => {
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
      if (topicMastery) {
        let worstCount = -1;
        for (const [subject, topics] of Object.entries(topicMastery)) {
          const shakyCount = Object.values(topics).filter(t => t.confidence === 'shaky').length;
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
        if (topicMastery) {
          const todayStart = new Date(todayKey + 'T00:00:00').getTime();
          let count = 0;
          for (const subjects of Object.values(topicMastery)) {
            for (const entry of Object.values(subjects)) {
              if (entry.updatedAt >= todayStart) count++;
            }
          }
          current = count;
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

    return { quest, current, isCompleted, isClaimed, dayNumber, isOnboarding };
  }, [isLoaded, uid, studentProfile, topicMastery, courses, userProgress, sessions, debriefs, streak, timetableCompletions, questRewards, mockResults]);

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
      // Transaction: read the questRewards map; bail if this questId is already
      // claimed (covers the multi-tab race where two tabs both pass the optimistic
      // gate). Firestore rules also reject overwrites, but failing fast here
      // avoids a useless round-trip and a confusing rules error in the console.
      await runTransaction(db, async (txn) => {
        const ref = doc(db, 'progress', uid);
        const snap = await txn.get(ref);
        const existing = (snap.data()?.questRewards ?? {}) as Record<string, string>;
        if (existing[questId]) return; // Already claimed in another tab
        txn.set(ref, {
          pointsData: { totalEarned: increment(rewardPoints) },
          questRewards: { [questId]: new Date().toISOString() },
        }, { merge: true });
      });
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
  }, [uid, questState]);

  return { questState, claimReward, reload };
}
