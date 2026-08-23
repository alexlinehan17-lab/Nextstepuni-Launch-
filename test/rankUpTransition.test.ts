/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, test } from 'vitest';
import { ATHLETE_RANKS } from '@/gamificationConfig';
import { isRankBaselineReady, observeRankForSession, type RankUpTracker } from '@/utils/rankUpTransition';

const rank = (id: string) => {
  const match = ATHLETE_RANKS.find(item => item.id === id);
  if (!match) throw new Error(`Unknown test rank: ${id}`);
  return match;
};

describe('rank-up session tracking', () => {
  test('uses the saved login rank as a baseline without celebrating it', () => {
    let tracker: RankUpTracker = { uid: null, rank: null };

    const eagerLoginReady = isRankBaselineReady('student-1', null, false, true, 0, 0);
    expect(eagerLoginReady).toBe(false);
    let observation = observeRankForSession(tracker, 'student-1', rank('newcomer'), eagerLoginReady);
    tracker = observation.tracker;
    expect(observation.rankUp).toBeNull();
    expect(tracker.rank).toBeNull();

    const failedReadReady = isRankBaselineReady('student-1', 'student-1', false, true, 0, 0);
    expect(failedReadReady).toBe(false);
    observation = observeRankForSession(tracker, 'student-1', rank('newcomer'), failedReadReady);
    tracker = observation.tracker;
    expect(observation.rankUp).toBeNull();
    expect(tracker.rank).toBeNull();

    const hydratedLoginReady = isRankBaselineReady('student-1', 'student-1', true, true, 2400, 2400);
    expect(hydratedLoginReady).toBe(true);
    observation = observeRankForSession(tracker, 'student-1', rank('dedicated'), hydratedLoginReady);
    tracker = observation.tracker;
    expect(observation.rankUp).toBeNull();

    observation = observeRankForSession(tracker, 'student-1', rank('driven'), false);
    expect(observation.rankUp).toEqual(rank('driven'));
  });

  test('resets on logout and does not celebrate the next account saved rank', () => {
    let tracker: RankUpTracker = { uid: 'student-1', rank: rank('consistent') };

    let observation = observeRankForSession(tracker, null, rank('newcomer'), true);
    tracker = observation.tracker;
    expect(observation).toEqual({ tracker: { uid: null, rank: null }, rankUp: null });

    observation = observeRankForSession(tracker, 'student-2', rank('elite'), true);
    expect(observation.rankUp).toBeNull();
    expect(observation.tracker.rank).toEqual(rank('elite'));
  });

  test('does not celebrate a downward correction', () => {
    const observation = observeRankForSession(
      { uid: 'student-1', rank: rank('driven') },
      'student-1',
      rank('dedicated'),
      false,
    );

    expect(observation.rankUp).toBeNull();
    expect(observation.tracker.rank).toEqual(rank('dedicated'));
  });
});
