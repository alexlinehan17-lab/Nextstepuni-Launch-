/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import { FRENCH_ATTEMPT_ID, frenchMarks, frenchScoreId } from '../components/MarkBank/frenchRubric';
import { CARDS as frenchHigher } from '../components/MarkBank/cards/french/higher';
import { CARDS as frenchOrdinary } from '../components/MarkBank/cards/french/ordinary';
import type { SecRubricCard } from '../types/markBank';

/* "If Content = 0, Language = 0": a criterion may name another whose 0 forces
 * it to 0 (zeroWhenZero). The rule is opt-in, set only where a scheme prints
 * it; a card without it scores exactly as before. */
const card = (zeroWhenZero?: string) => ({
  kind: 'rubric',
  id: 'test-writing',
  totalMarks: 20,
  rubric: {
    system: 'french',
    taskRequirements: [],
    criteria: [
      { id: 'content', label: 'Content', maxMarks: 10, permittedMarks: [0, 2, 4, 6, 8, 10], guidance: [] },
      { id: 'language', label: 'Language', maxMarks: 10, permittedMarks: [0, 2, 4, 6, 8, 10], guidance: [],
        ...(zeroWhenZero ? { zeroWhenZero } : {}) },
    ],
  },
}) as unknown as SecRubricCard;

describe('French-shape rubric: a criterion zeroed by another', () => {
  it('scores Language 0 while Content is 0, and normally once Content is above 0', () => {
    const gated = card('content');
    expect(frenchMarks(gated, { [frenchScoreId('content')]: 0, [frenchScoreId('language')]: 8 })).toBe(0);
    expect(frenchMarks(gated, { [frenchScoreId('language')]: 8 })).toBe(0);
    expect(frenchMarks(gated, { [frenchScoreId('content')]: 4, [frenchScoreId('language')]: 8 })).toBe(12);
  });

  it('leaves a card without the rule exactly as it was', () => {
    expect(frenchMarks(card(), { [frenchScoreId('content')]: 0, [frenchScoreId('language')]: 8 })).toBe(8);
  });

  it('is set on no shipped French card (the French schemes print an attempt rule instead)', () => {
    const withRule = [...frenchHigher, ...frenchOrdinary]
      .filter(c => c.kind === 'rubric' && c.rubric.system === 'french')
      .filter(c => (c as SecRubricCard & { rubric: { criteria: { zeroWhenZero?: string }[] } }).rubric.criteria
        .some(criterion => criterion.zeroWhenZero));
    expect(withRule.map(c => c.id)).toEqual([]);
    expect(FRENCH_ATTEMPT_ID).toBe('french:communicative-task-attempted');
  });
});
