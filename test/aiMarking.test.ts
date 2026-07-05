/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the AI-marking scaffold (feature E11): the pure tally helper adds up
 * awarded vs available marks, and — critically for the compliance posture — the
 * request function is INERT (throws, never calls a model).
 */
import { describe, it, expect } from 'vitest';
import { tallyMarking, requestAnswerMarking, AI_MARKING_LIVE, type MarkedPoint } from '../data/aiMarking';

describe('AI marking — scaffold', () => {
  it('tallies awarded vs available marks', () => {
    const points: MarkedPoint[] = [
      { text: 'States the principle', marks: 2, awarded: true },
      { text: 'Correct worked example', marks: 3, awarded: false },
      { text: 'Units', marks: 1, awarded: true },
    ];
    expect(tallyMarking(points)).toEqual({ awarded: 3, max: 6 });
  });

  it('is inert: the feature is gated off and the request never calls a model', async () => {
    expect(AI_MARKING_LIVE).toBe(false);
    await expect(requestAnswerMarking({ questionRef: 'x', studentAnswer: 'y' })).rejects.toThrow(/not enabled/i);
  });
});
