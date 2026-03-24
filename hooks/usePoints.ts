/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';

export interface PointsData {
  totalEarned: number;
  totalSpent: number;
  balance: number;
  isLoaded: boolean;
}

const DEFAULT: PointsData = { totalEarned: 0, totalSpent: 0, balance: 0, isLoaded: false };

export function usePoints(uid?: string): PointsData & { reload: () => void } {
  const [points, setPoints] = useState<PointsData>(DEFAULT);
  const [version, setVersion] = useState(0);

  const reload = useCallback(() => {
    setVersion(v => v + 1);
  }, []);

  useEffect(() => {
    if (!uid) {
      setPoints({ ...DEFAULT, isLoaded: true });
      return;
    }

    let cancelled = false;

    const load = async () => {
      try {
        const progressDoc = await getDoc(doc(db, 'progress', uid));
        if (cancelled) return;
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
      if (!cancelled) setPoints({ ...DEFAULT, isLoaded: true });
    };

    load();
    return () => { cancelled = true; };
  }, [uid, version]);

  return { ...points, reload };
}
