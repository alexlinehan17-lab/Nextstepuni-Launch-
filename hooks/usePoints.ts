/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';

export interface PointsData {
  totalEarned: number;
  totalSpent: number;
  balance: number;
  isLoaded: boolean;
}

const DEFAULT: PointsData = { totalEarned: 0, totalSpent: 0, balance: 0, isLoaded: false };

export function usePoints(uid?: string): PointsData {
  const [points, setPoints] = useState<PointsData>(DEFAULT);

  useEffect(() => {
    if (!uid) {
      setPoints({ ...DEFAULT, isLoaded: true });
      return;
    }

    const load = async () => {
      try {
        const progressDoc = await getDoc(doc(db, 'progress', uid));
        if (progressDoc.exists()) {
          const data = progressDoc.data();
          const pd = data.pointsData;
          if (pd) {
            setPoints({
              totalEarned: pd.totalEarned ?? 0,
              totalSpent: pd.totalSpent ?? 0,
              balance: (pd.totalEarned ?? 0) - (pd.totalSpent ?? 0),
              isLoaded: true,
            });
            return;
          }
        }
      } catch (err) {
        console.error('Failed to load points:', err);
      }
      setPoints({ ...DEFAULT, isLoaded: true });
    };

    load();
  }, [uid]);

  return points;
}
