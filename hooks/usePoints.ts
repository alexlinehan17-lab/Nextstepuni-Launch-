/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useProgress } from '../contexts/ProgressContext';

export interface PointsData {
  totalEarned: number;
  totalSpent: number;
  balance: number;
  isLoaded: boolean;
}

export function usePoints(_uid?: string): PointsData & { reload: () => void } {
  const { pointsData, progressLoaded } = useProgress();
  return {
    totalEarned: pointsData.totalEarned,
    totalSpent: pointsData.totalSpent,
    balance: pointsData.balance,
    isLoaded: progressLoaded,
    reload: pointsData.reload,
  };
}
