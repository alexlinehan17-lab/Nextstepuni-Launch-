/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, setDoc, increment } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { getWeekNumber, getWeekStartDate } from '../gamificationConfig';
import { getWeeklyChallenge, type WeeklyChallengeDefinition } from '../weeklyChallengeData';
import { type StudySessionRecord } from '../utils/strategyRegistry';

export interface WeeklyChallengeState {
  challenge: WeeklyChallengeDefinition;
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
  const challenge = getWeeklyChallenge(weekNumber);
  const weekStart = getWeekStartDate();

  const [current, setCurrent] = useState(0);
  const [isClaimed, setIsClaimed] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const [version, setVersion] = useState(0);

  const reload = useCallback(() => {
    setVersion(v => v + 1);
  }, []);

  useEffect(() => {
    if (!progressLoaded) return;

    if (!uid) {
      setCurrent(0);
      setIsClaimed(false);
      setIsLoaded(true);
      return;
    }

    const data = rawProgressDoc;
    const sessions: StudySessionRecord[] = data.studySessions || [];
    const rewards: Record<string, string> = data.weeklyChallengeRewards || {};

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
  }, [uid, version, challenge.id, challenge.metric, challenge.strategyModuleId, weekStart, progressLoaded, rawProgressDoc]);

  const claimReward = useCallback(async () => {
    if (!uid || isClaimed) return;
    try {
      await setDoc(doc(db, 'progress', uid), {
        pointsData: { totalEarned: increment(challenge.rewardPoints) },
        weeklyChallengeRewards: { [challenge.id]: new Date().toISOString() },
      }, { merge: true });
      setIsClaimed(true);
    } catch (err) {
      console.error('Failed to claim weekly challenge reward:');
    }
  }, [uid, isClaimed, challenge.id, challenge.rewardPoints]);

  const isCompleted = current >= challenge.target;

  return { challenge, current, isCompleted, isClaimed, isLoaded, claimReward, reload };
}
