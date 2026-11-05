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

import ReligiousEducationRubricPanel, { bandHeading, religiousEducationMarks } from '@/components/MarkBank/ReligiousEducationRubricPanel';
import { reAnswerBandId, reAnswerScoreId, reCeilingScoreId, reWayScoreId } from '@/components/MarkBank/religiousEducationScoring';
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

  test('the grid must cover 0 to the answer maximum and make the card total', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(tariffReconciles({ ...card, totalMarks: 10 })).toBe(false);
    const gap = { ...card, rubric: { ...rubric, bands: bands.filter(band => band.label !== 'FAIR') } };
    expect(tariffReconciles(gap)).toBe(false);
  });

  test('the chosen mark is the pressed one with the tick; bands over a ticked ceiling are disabled', () => {
    render(<ReligiousEducationRubricPanel card={card} scores={{ [reAnswerScoreId(0)]: 9, [reCeilingScoreId]: 1 }} onScore={() => undefined} />);
    const first = screen.getByRole('region', { name: 'Answer 1 of 2' });
    const chosen = within(first).getByRole('button', { name: `Clear 9 marks for ${bandHeading('EXCELLENT', '10-8')}` });
    expect(chosen).toHaveAttribute('aria-pressed', 'true');
    expect(chosen.querySelector('svg')).not.toBeNull();
    expect(within(first).getByRole('button', { name: `Claim 7 marks for ${bandHeading('VERY GOOD', '7')}` })).toBeDisabled();
    expect(within(first).getByRole('button', { name: `Claim 4 marks for ${bandHeading('FAIR', '4')}` })).not.toBeDisabled();
    expect(screen.getByText('5 / 20')).toBeInTheDocument();
  });

  test('a band heading holds its printed range together and to its label', () => {
    const heading = bandHeading('EXCELLENT', '34 - 40');
    expect(heading).toBe('EXCELLENT\u00a0·\u00a034\u00a0-\u2060\u00a040');
    expect(heading).not.toMatch(/ /);
    expect(bandHeading('VERY GOOD', '28 – 33')).toBe('VERY GOOD\u00a0·\u00a028\u00a0–\u2060\u00a033');
  });

  test('an answer not yet placed shows no chosen mark, and 0 is a mark it can be placed at', () => {
    const { unmount } = render(<ReligiousEducationRubricPanel card={card} scores={{}} onScore={() => undefined} />);
    const first = screen.getByRole('region', { name: 'Answer 1 of 2' });
    expect(within(first).queryAllByRole('button', { pressed: true })).toHaveLength(0);
    unmount();
    render(<ReligiousEducationRubricPanel card={card} scores={{ [reAnswerScoreId(0)]: 0 }} onScore={() => undefined} />);
    const placedAtZero = screen.getByRole('region', { name: 'Answer 1 of 2' });
    expect(within(placedAtZero).getByRole('button', { name: `Clear 0 marks for ${bandHeading('POOR', '1-0')}` })).toHaveAttribute('aria-pressed', 'true');
  });

  test('placing a mark reports it under the answer it belongs to', () => {
    const calls: Array<[string, number]> = [];
    render(<ReligiousEducationRubricPanel card={card} scores={{}} onScore={(id, marks) => calls.push([id, marks])} />);
    const second = screen.getByRole('region', { name: 'Answer 2 of 2' });
    fireEvent.click(within(second).getByRole('button', { name: `Claim 6 marks for ${bandHeading('GOOD', '6-5')}` }));
    expect(calls).toEqual([[reAnswerScoreId(1), 6]]);
  });

  describe('a grid printing two marks rows', () => {
    // 2022's shape: "40 Marks" for the answer whole, "20 Marks x2" for it in
    // two, on the same band cells. The card's own way is the one its head
    // names first; the student picks the way they wrote.
    const whole = [
      { label: 'EXCELLENT', printed: '40 - 34', marks: [34, 35, 36, 37, 38, 39, 40], descriptor: ['Relevance: completely & clearly relevant'] },
      { label: 'GOOD', printed: '33 - 10', marks: Array.from({ length: 24 }, (_, i) => i + 10) },
      { label: 'WEAK', printed: '9 - 0', marks: Array.from({ length: 10 }, (_, i) => i) },
    ];
    const twoWays: ReligiousEducationRubric = {
      ...rubric, answers: 1, answerMax: 40, gridHead: '40 Marks', bands: whole, ceilings: undefined,
      otherWay: {
        gridHead: '20 Marksx2', answers: 2, answerMax: 20,
        bands: [
          { printed: '20 - 17', marks: [17, 18, 19, 20] },
          { printed: '16 - 5', marks: Array.from({ length: 12 }, (_, i) => i + 5) },
          { printed: '4 - 0', marks: [0, 1, 2, 3, 4] },
        ],
      },
    };
    const wayCard = { ...card, totalMarks: 40, rubric: twoWays } as typeof card;

    test('the first-named way is chosen until the student picks the other, under the printed heads', () => {
      const calls: Array<[string, number]> = [];
      render(<ReligiousEducationRubricPanel card={wayCard} scores={{}} onScore={(id, marks) => calls.push([id, marks])} />);
      const group = screen.getByRole('radiogroup', { name: 'Marks row' });
      const [first, second] = within(group).getAllByRole('radio');
      expect(first).toHaveAccessibleName(/^40 Marks/);
      expect(second).toHaveAccessibleName(/^20 Marksx2/);
      expect(first).toHaveAttribute('aria-checked', 'true');
      expect(second).toHaveAttribute('aria-checked', 'false');
      expect(screen.getByRole('region', { name: 'Your answer' })).toBeInTheDocument();
      expect(screen.queryByRole('region', { name: 'Answer 1 of 2' })).toBeNull();
      fireEvent.click(second);
      expect(calls).toEqual([[reWayScoreId, 1]]);
    });

    test('the other way shows its own ladders at its own ranges, with the same band cells', () => {
      render(<ReligiousEducationRubricPanel card={wayCard} scores={{ [reWayScoreId]: 1 }} onScore={() => undefined} />);
      expect(within(screen.getByRole('radiogroup', { name: 'Marks row' })).getAllByRole('radio')[1]).toHaveAttribute('aria-checked', 'true');
      const second = screen.getByRole('region', { name: 'Answer 2 of 2' });
      expect(within(second).getByRole('button', { name: `Claim 20 marks for ${bandHeading('EXCELLENT', '20 - 17')}` })).toBeInTheDocument();
      expect(within(second).getByText(/completely & clearly relevant/)).toBeInTheDocument();
      expect(screen.queryByRole('region', { name: 'Your answer' })).toBeNull();
    });

    test('only the chosen way scores', () => {
      const scores = {
        [reAnswerScoreId(0)]: 36,
        [reAnswerScoreId(0, 1)]: 18, [reAnswerScoreId(1, 1)]: 12,
      };
      expect(religiousEducationMarks(wayCard, scores)).toBe(36);
      expect(religiousEducationMarks(wayCard, { ...scores, [reWayScoreId]: 1 })).toBe(30);
      // a mark placed on the first way is not carried over to the other
      expect(religiousEducationMarks(wayCard, { [reAnswerScoreId(0)]: 15, [reWayScoreId]: 1 })).toBe(0);
    });

    test('the other row must cover its own maximum and make the same total; it carries no ceiling', () => {
      expect(tariffReconciles(wayCard)).toBe(true);
      const short = { ...wayCard, rubric: { ...twoWays, otherWay: { ...twoWays.otherWay!, answers: 1 } } };
      expect(tariffReconciles(short)).toBe(false);
      const gap = { ...wayCard, rubric: { ...twoWays, otherWay: { ...twoWays.otherWay!, bands: twoWays.otherWay!.bands.slice(0, 2).concat([{ printed: '4 - 1', marks: [1, 2, 3, 4] }]) } } };
      expect(tariffReconciles(gap)).toBe(false);
      const capped = { ...wayCard, rubric: { ...twoWays, ceilings: [{ when: 'If a candidate', max: 10 }] } };
      expect(tariffReconciles(capped)).toBe(false);
    });
  });

  describe('bands that print the same mark', () => {
    // 2019 Higher I(b)(i) prints 9-10, 6-8, 4-5, 3-4, 2-3, 1-2, 0-1: 1 to 4
    // each sit in two bands. The student places the answer in the band they
    // judge it fits; the mark is what scores.
    const overlapping = [
      { label: 'EXCELLENT', printed: '9 - 10', marks: [9, 10] },
      { label: 'VERY GOOD', printed: '6 - 8', marks: [6, 7, 8] },
      { label: 'GOOD', printed: '4 - 5', marks: [4, 5] },
      { label: 'FAIR', printed: '3 - 4', marks: [3, 4] },
      { label: 'WEAK', printed: '2 - 3', marks: [2, 3] },
      { label: 'VERY WEAK', printed: '1 - 2', marks: [1, 2] },
      { label: 'NO GRADE', printed: '0 - 1', marks: [0, 1] },
    ];
    const overlapRubric: ReligiousEducationRubric = {
      ...rubric, answers: 1, answerMax: 10, gridHead: '10M', bands: overlapping, ceilings: undefined,
    };
    const overlapCard = { ...card, totalMarks: 10, rubric: overlapRubric } as typeof card;
    const good = bandHeading('GOOD', '4 - 5');
    const fair = bandHeading('FAIR', '3 - 4');

    test('the grid reconciles though a mark sits in two bands', () => {
      expect(tariffReconciles(overlapCard)).toBe(true);
    });

    test('the same mark is placeable in either band, and the band is remembered', () => {
      const calls: Array<[string, number]> = [];
      render(<ReligiousEducationRubricPanel card={overlapCard} scores={{}} onScore={(id, marks) => calls.push([id, marks])} />);
      fireEvent.click(screen.getByRole('button', { name: `Claim 4 marks for ${fair}` }));
      fireEvent.click(screen.getByRole('button', { name: `Claim 4 marks for ${good}` }));
      expect(calls).toEqual([
        [reAnswerBandId(0), 3], [reAnswerScoreId(0), 4],
        [reAnswerBandId(0), 2], [reAnswerScoreId(0), 4],
      ]);
    });

    test('only the band it was placed in shows the mark as chosen, and it scores the same either way', () => {
      const inFair = { [reAnswerScoreId(0)]: 4, [reAnswerBandId(0)]: 3 };
      const { unmount } = render(<ReligiousEducationRubricPanel card={overlapCard} scores={inFair} onScore={() => undefined} />);
      expect(screen.getByRole('button', { name: `Clear 4 marks for ${fair}` })).toHaveAttribute('aria-pressed', 'true');
      expect(screen.getByRole('button', { name: `Claim 4 marks for ${good}` })).toHaveAttribute('aria-pressed', 'false');
      expect(screen.getAllByRole('button', { pressed: true })).toHaveLength(1);
      unmount();
      const inGood = { [reAnswerScoreId(0)]: 4, [reAnswerBandId(0)]: 2 };
      render(<ReligiousEducationRubricPanel card={overlapCard} scores={inGood} onScore={() => undefined} />);
      expect(screen.getByRole('button', { name: `Clear 4 marks for ${good}` })).toHaveAttribute('aria-pressed', 'true');
      expect(screen.getByRole('button', { name: `Claim 4 marks for ${fair}` })).toHaveAttribute('aria-pressed', 'false');
      expect(religiousEducationMarks(overlapCard, inFair)).toBe(4);
      expect(religiousEducationMarks(overlapCard, inGood)).toBe(4);
    });

    test('a mark printed in one band only needs no band of its own', () => {
      const calls: Array<[string, number]> = [];
      render(<ReligiousEducationRubricPanel card={overlapCard} scores={{}} onScore={(id, marks) => calls.push([id, marks])} />);
      fireEvent.click(screen.getByRole('button', { name: `Claim 7 marks for ${bandHeading('VERY GOOD', '6 - 8')}` }));
      expect(calls).toEqual([[reAnswerScoreId(0), 7]]);
    });
  });
});
