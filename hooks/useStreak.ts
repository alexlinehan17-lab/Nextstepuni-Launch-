/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useProgress } from '../contexts/ProgressContext';

export interface StreakData {
  currentStreak: number;
  lastActiveDate: string; // YYYY-MM-DD
  longestStreak: number;
}

export function useStreak(_uid?: string) {
  const { streak, progressLoaded } = useProgress();
  return { streak, isLoaded: progressLoaded };
}
