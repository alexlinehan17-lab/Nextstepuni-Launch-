/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { collection, query, where, getDocs } from 'firebase/firestore';
import { db } from '../firebase';
import { type IslandPlacement, type NorthStarCategory } from '../types';

/**
 * PeerIsland is the in-memory shape exposed to consumers of this hook.
 * It is derived from the /islandPublic/{uid} projection (see
 * compliance/PEER_ISLAND_REFACTOR_PLAN.md and
 * functions/src/islandProjection.ts).
 *
 * The `islandState` field is deliberately a thin subset — only `category`
 * and `placements`, which are the only fields the peer-view UI renders.
 */
export interface PeerIsland {
  uid: string;
  name: string;
  avatar: string;
  islandState: {
    category: NorthStarCategory;
    placements: IslandPlacement[];
  };
  northStarCategory: NorthStarCategory;
  placementCount: number;
  score: number;
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
        // Single same-school query against the public projection.
        // Server-side (Cloud Function) ensures only student-role users
        // appear here — staff accounts are excluded by the projection
        // builder, so no client-side filtering by role is needed.
        const islandRef = collection(db, 'islandPublic');
        const q = query(islandRef, where('school', '==', school));
        const snapshot = await getDocs(q);

        const validPeers: PeerIsland[] = snapshot.docs
          .filter(d => d.id !== uid)
          .map(d => {
            const data = d.data();
            const category = data.category as NorthStarCategory;
            return {
              uid: d.id,
              name: typeof data.name === 'string' ? data.name : 'Student',
              avatar: typeof data.avatar === 'string' ? data.avatar : 'James',
              islandState: {
                category,
                placements: (data.placements ?? []) as IslandPlacement[],
              },
              northStarCategory: category,
              placementCount: typeof data.placementCount === 'number' ? data.placementCount : 0,
              score: typeof data.score === 'number' ? data.score : 0,
            };
          });

        if (cancelled) return;

        setPeers(validPeers);
      } catch (err) {
        if (!cancelled) {
          setError('Could not load peer islands');
          console.error('[PeerIslands] Failed to load:', err);
        }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [uid, school, reloadKey]);

  return { peers, isLoading, error, reload };
}
