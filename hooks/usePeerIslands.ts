/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { collection, query, where, getDocs, doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { IslandState, NorthStarCategory } from '../types';
import { createStarterState } from './useIslandShop';

export interface PeerIsland {
  uid: string;
  name: string;
  avatar: string;
  islandState: IslandState;
  northStarCategory: NorthStarCategory;
}

export function usePeerIslands(uid?: string, school?: string) {
  const [peers, setPeers] = useState<PeerIsland[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  const reload = useCallback(() => setReloadKey(k => k + 1), []);

  useEffect(() => {
    if (!uid || !school) {
      setPeers([]);
      return;
    }

    let cancelled = false;
    setIsLoading(true);
    setError(null);

    (async () => {
      try {
        // Query users in the same school
        const usersRef = collection(db, 'users');
        const q = query(usersRef, where('school', '==', school));
        const snapshot = await getDocs(q);

        // Filter out self, GCs, and admins
        const candidates = snapshot.docs.filter(d => {
          if (d.id === uid) return false;
          const data = d.data();
          if (data.role === 'gc' || data.role === 'admin' || data.isAdmin) return false;
          return true;
        });

        // Fetch progress for each candidate in parallel
        const results = await Promise.allSettled(
          candidates.map(async (userDoc) => {
            const userData = userDoc.data();
            const progressSnap = await getDoc(doc(db, 'progress', userDoc.id));
            if (!progressSnap.exists()) return null;

            const progressData = progressSnap.data();
            const northStar = progressData?.northStar;
            const islandState = progressData?.islandState as IslandState | undefined;

            const category = (northStar?.category || islandState?.category) as NorthStarCategory | undefined;

            // Need at least a category to determine which island to show
            if (!category) return null;

            // If they have a northStar but haven't opened Journey yet, generate starter island
            const effectiveIsland = (islandState?.placements?.length)
              ? islandState
              : createStarterState(category);

            return {
              uid: userDoc.id,
              name: userData.name || 'Student',
              avatar: userData.avatar || 'James',
              islandState: effectiveIsland,
              northStarCategory: category,
            } as PeerIsland;
          })
        );

        if (cancelled) return;

        const validPeers = results
          .filter((r): r is PromiseFulfilledResult<PeerIsland | null> => r.status === 'fulfilled')
          .map(r => r.value)
          .filter((p): p is PeerIsland => p !== null);

        setPeers(validPeers);
      } catch {
        if (!cancelled) {
          setError('Could not load peer islands');
          console.error('[PeerIslands] Failed to load:');
        }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [uid, school, reloadKey]);

  return { peers, isLoading, error, reload };
}
