/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { collection, doc, getDocs, increment, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { getWeekNumber, getWeekStartDate } from '../gamificationConfig';
import { getWeeklyChallenge, type WeeklyChallengeDefinition } from '../weeklyChallengeData';
import { type StudySessionRecord } from '../utils/strategyRegistry';

export interface WeeklyChallengeState {
  /** Null when no challenge is available for the user's curriculum level
   *  (Phase 5: JC users see no challenges yet — challenge content lands later). */
  challenge: WeeklyChallengeDefinition | null;
  current: number;
  isCompleted: boolean;
  isClaimed: boolean;
  isLoaded: boolean;
  claimReward: () => Promise<void>;
  reload: () => void;
}

export function useWeeklyChallenge(uid: string | undefined): WeeklyChallengeState {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const weekNumber = getWeekNumber();
  // Phase 5: filter to user's curriculum. JC has no senior-tagged challenges
  // to surface; treat as "no challenge this week" rather than crashing.
  const curriculumLevel = rawProgressDoc?.subjectProfile?.curriculumLevel ?? 'senior';
  const challenge = getWeeklyChallenge(weekNumber, curriculumLevel);
  const weekStart = getWeekStartDate();

  const [current, setCurrent] = useState(0);
  const [isClaimed, setIsClaimed] = useState(false);
  const isMountedRef = useRef(true);
  useEffect(() => () => { isMountedRef.current = false; }, []);
  const [isLoaded, setIsLoaded] = useState(false);
  const [version, setVersion] = useState(0);

  const reload = useCallback(() => {
    setVersion(v => v + 1);
  }, []);

  useEffect(() => {
    if (!progressLoaded) return;

    if (!uid || !challenge) {
      setCurrent(0);
      setIsClaimed(false);
      setIsLoaded(true);
      return;
    }

    let cancelled = false;
    const load = async () => {
      // Sessions live in the /progress/{uid}/sessions subcollection (migrated
      // from the dead rawProgressDoc.studySessions array). Reading the legacy
      // array here meant study-session-based weekly challenges never
      // progressed — audit 2026-06-01. reload() bumps `version`, re-running
      // this effect so a just-saved session is counted immediately.
      let sessions: StudySessionRecord[] = [];
      try {
        const snap = await getDocs(collection(db, 'progress', uid, 'sessions'));
        sessions = snap.docs.map(d => d.data() as StudySessionRecord);
      } catch (err) {
        console.error('Failed to load sessions for weekly challenge:', err);
      }
      if (cancelled) return;

      const rewards: Record<string, string> = rawProgressDoc.weeklyChallengeRewards || {};

      // Check if already claimed
      setIsClaimed(!!rewards[challenge.id]);

      // Filter sessions to current week
      const weekSessions = sessions.filter(s => s.date >= weekStart);

      // Compute progress based on metric
      let progress = 0;
      switch (challenge.metric) {
        case 'strategy-sessions': {
          const moduleId = challenge.strategyModuleId;
          if (moduleId) {
            progress = weekSessions.filter(
              s => s.strategiesShown?.includes(moduleId)
            ).length;
          }
          break;
        }
        case 'strategy-subjects': {
          const moduleId = challenge.strategyModuleId;
          if (moduleId) {
            const subjects = new Set(
              weekSessions
                .filter(s => s.strategiesShown?.includes(moduleId))
                .map(s => s.subject)
            );
            progress = subjects.size;
          }
          break;
        }
        case 'total-sessions': {
          progress = weekSessions.length;
          break;
        }
        case 'reflection-sessions': {
          progress = weekSessions.filter(s => s.hadReflection).length;
          break;
        }
      }

      setCurrent(progress);
      setIsLoaded(true);
    };
    load();
    return () => { cancelled = true; };
  }, [uid, version, challenge?.id, challenge?.metric, challenge?.strategyModuleId, weekStart, progressLoaded, rawProgressDoc]);

  const claimReward = useCallback(async () => {
    if (!uid || isClaimed || !challenge) return;
    try {
      await setDoc(doc(db, 'progress', uid), {
        pointsData: { totalEarned: increment(challenge.rewardPoints) },
        weeklyChallengeRewards: { [challenge.id]: new Date().toISOString() },
      }, { merge: true });
      if (isMountedRef.current) setIsClaimed(true);
    } catch (err) {
      console.error('Failed to claim weekly challenge reward:', err);
    }
  }, [uid, isClaimed, challenge?.id, challenge?.rewardPoints]);

  const isCompleted = challenge ? current >= challenge.target : false;

  return { challenge, current, isCompleted, isClaimed, isLoaded, claimReward, reload };
}
