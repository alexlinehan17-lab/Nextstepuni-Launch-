/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A Religious Education card is marked the way the SEC marks every RE answer:
 * one mark inside one band of the printed grid, per answer; a ticked ceiling
 * holds each answer at its printed maximum.
 */
import { describe, expect, test } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';

import ReligiousEducationRubricPanel, { religiousEducationMarks } from '@/components/MarkBank/ReligiousEducationRubricPanel';
import { reAnswerScoreId, reCeilingScoreId } from '@/components/MarkBank/religiousEducationScoring';
import { tariffReconciles, type ReligiousEducationRubric, type SecRubricCard } from '@/types/markBank';

const bands = [
  { label: 'EXCELLENT', printed: '10-8', marks: [8, 9, 10], descriptor: ['Relevance: completely & clearly relevant'] },
  { label: 'VERY GOOD', printed: '7', marks: [7] },
  { label: 'GOOD', printed: '6-5', marks: [5, 6] },
  { label: 'FAIR', printed: '4', marks: [4] },
  { label: 'WEAK', printed: '3-2', marks: [2, 3] },
  { label: 'POOR', printed: '1-0', marks: [0, 1] },
];
const rubric: ReligiousEducationRubric = {
  system: 'religious-education',
  criteria: 'An excellent answer will show an understanding of God.',
  points: ['God as Shepherd etc.'], openList: true,
  answers: 2, answerMax: 10, gridHead: '10 Marks x2', bands,
  ceilings: [{ when: 'If a candidate gives only one image', max: 5 }],
  directions: ['Note: Allow descriptive answers.'],
  markingGuideNote: 'Place the whole answer in one band.',
  schemePages: [8], schemeFileid: 'LC223ALP000EV.pdf',
};
const card = {
  id: 're-test', subjectId: 'religious-education', source: 'sec', kind: 'rubric', level: 'higher',
  year: 2025, section: 'A', questionRef: '2025 HL Section A Q2(b)(i)', topicId: 're-a', conceptId: 'x',
  questionText: 'Outline two images of God that you have studied.', totalMarks: 20, paperFileid: 'LC223ALP000EV',
  schemeCitation: 'x', specVersion: 'x', qa: { gates: [], humanReviewedBy: 'x', humanReviewedAt: 'x' }, rubric,
} as unknown as SecRubricCard & { rubric: ReligiousEducationRubric };

describe('Religious Education band grid', () => {
  test('two answers add; a mark outside every band counts nothing', () => {
    expect(religiousEducationMarks(card, { [reAnswerScoreId(0)]: 9, [reAnswerScoreId(1)]: 6 })).toBe(15);
    expect(religiousEducationMarks(card, { [reAnswerScoreId(0)]: 11 })).toBe(0);
  });

  test('a ticked ceiling holds every answer at its maximum', () => {
    expect(religiousEducationMarks(card, { [reAnswerScoreId(0)]: 9, [reAnswerScoreId(1)]: 3, [reCeilingScoreId]: 1 })).toBe(8);
  });

  test('the grid must cover 0 to the answer maximum exactly once and make the card total', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(tariffReconciles({ ...card, totalMarks: 10 })).toBe(false);
    const gap = { ...card, rubric: { ...rubric, bands: bands.filter(band => band.label !== 'FAIR') } };
    expect(tariffReconciles(gap)).toBe(false);
  });

  test('the chosen mark is the pressed one with the tick; bands over a ticked ceiling are disabled', () => {
    render(<ReligiousEducationRubricPanel card={card} scores={{ [reAnswerScoreId(0)]: 9, [reCeilingScoreId]: 1 }} onScore={() => undefined} />);
    const first = screen.getByRole('region', { name: 'Answer 1 of 2' });
    const chosen = within(first).getByRole('button', { name: 'Clear 9 marks for EXCELLENT · 10-8' });
    expect(chosen).toHaveAttribute('aria-pressed', 'true');
    expect(chosen.querySelector('svg')).not.toBeNull();
    expect(within(first).getByRole('button', { name: 'Claim 7 marks for VERY GOOD · 7' })).toBeDisabled();
    expect(within(first).getByRole('button', { name: 'Claim 4 marks for FAIR · 4' })).not.toBeDisabled();
    expect(screen.getByText('5 / 20')).toBeInTheDocument();
  });

  test('placing a mark reports it under the answer it belongs to', () => {
    const calls: Array<[string, number]> = [];
    render(<ReligiousEducationRubricPanel card={card} scores={{}} onScore={(id, marks) => calls.push([id, marks])} />);
    const second = screen.getByRole('region', { name: 'Answer 2 of 2' });
    fireEvent.click(within(second).getByRole('button', { name: 'Claim 6 marks for GOOD · 6-5' }));
    expect(calls).toEqual([[reAnswerScoreId(1), 6]]);
  });
});
