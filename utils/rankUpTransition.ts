/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import type { AthleteRank } from '../gamificationConfig';

export interface RankUpTracker {
  uid: string | null;
  rank: AthleteRank | null;
}

interface RankObservation {
  tracker: RankUpTracker;
  rankUp: AthleteRank | null;
}

export function isRankBaselineReady(
  uid: string | null,
  loadedDataUid: string | null,
  progressLoadedSuccessfully: boolean,
  gamificationLoaded: boolean,
  currentPoints: number,
  persistedPoints: number,
): boolean {
  return uid !== null
    && loadedDataUid === uid
    && progressLoadedSuccessfully
    && gamificationLoaded
    && currentPoints === persistedPoints;
}

/**
 * Tracks upward rank transitions for one authenticated session. A new user
 * must first present a fully hydrated points total before their saved rank
 * becomes the baseline, so login and logout can never look like rank-ups.
 */
export function observeRankForSession(
  previous: RankUpTracker,
  uid: string | null,
  currentRank: AthleteRank,
  baselineReady: boolean,
): RankObservation {
  if (!uid) {
    return { tracker: { uid: null, rank: null }, rankUp: null };
  }

  if (previous.uid !== uid) {
    return {
      tracker: { uid, rank: baselineReady ? currentRank : null },
      rankUp: null,
    };
  }

  if (!previous.rank) {
    return {
      tracker: { uid, rank: baselineReady ? currentRank : null },
      rankUp: null,
    };
  }

  return {
    tracker: { uid, rank: currentRank },
    rankUp: currentRank.minPoints > previous.rank.minPoints ? currentRank : null,
  };
}
