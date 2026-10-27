/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * French answers as claimable rows (cards/french/answers.ts): the shapes the
 * parser reads, the cards it must leave alone, and how the rows score.
 */
import { describe, expect, it } from 'vitest';
import { FRENCH_LISTENING_CARDS } from '../components/MarkBank/cards/french/listening';
import { FRENCH_READING_CARDS } from '../components/MarkBank/cards/french/reading';
import { FRENCH_CLOZE_CARDS } from '../components/MarkBank/cards/french/cloze';
import { frenchAnswerSource, parseFrenchAnswers } from '../components/MarkBank/cards/french/answers';
import { frenchAllocationMarks, frenchMarks, frenchRowScoreId } from '../components/MarkBank/frenchRubric';
import type { FrenchAllocation } from '../types/markBank';

const cards = [...FRENCH_LISTENING_CARDS, ...FRENCH_READING_CARDS, ...FRENCH_CLOZE_CARDS];
const byId = (id: string) => {
  const card = cards.find(candidate => candidate.id === id);
  if (!card) throw new Error(`no card ${id}`);
  return card;
};
const allocationOf = (id: string): FrenchAllocation => {
  const allocation = byId(id).rubric.allocation;
  if (!allocation) throw new Error(`${id} is not structured`);
  return allocation;
};
const rowMarks = (allocation: FrenchAllocation) => allocation.rows.map(row => [row.text, row.marks] as const);

describe('French scheme lines become claimable rows', () => {
  it('cuts a full/partial listening scheme into priced rows, one answer asked', () => {
    const allocation = allocationOf('fr-2026-hl-listening-la-q1');
    expect(allocation.count).toBe(1);
    expect(rowMarks(allocation)).toEqual([
      ['Go out in nature', 3],
      ['Mountain hikes / Mountain walks / Hillwalking', 3],
      ['Camping (in the mountains)', 3],
      ['Sleep under the stars / Sleep outdoors', 3],
      ['Go outdoors', 2],
      ['Hiking/Walking', 2],
      ['Nature', 1],
      ['Mountains/Hills', 1],
    ]);
    expect(allocation.rows.filter(row => row.partial).map(row => row.text)).toEqual(['Go outdoors', 'Hiking/Walking', 'Nature', 'Mountains/Hills']);
  });

  it('asks for two details when the full mark goes twice into the total, and keeps 0-mark answers as rows', () => {
    const allocation = allocationOf('fr-2026-hl-listening-la-q2');
    expect(allocation.count).toBe(2);
    expect(rowMarks(allocation)).toEqual([
      ['Have a lie-in', 3], ['Meet (up with) friends', 3], ['Visit (her) parents', 3],
      ['(Go) visiting', 2], ['Friends', 0], ['(Her) parents', 0],
    ]);
  });

  it('reads a header ladder: any two earn 5, any one earns 3', () => {
    const allocation = allocationOf('fr-2025-ol-listening-la-q2b');
    expect(allocation.ladder).toEqual([3, 5]);
    expect(allocation.count).toBe(2);
    expect(allocation.rows.map(row => row.text)).toEqual(['Surfing', 'Windsurfing', '(Deep sea / Scuba) diving']);
    expect(frenchAllocationMarks(5, allocation, { [frenchRowScoreId('r1')]: 1 })).toBe(3);
    expect(frenchAllocationMarks(5, allocation, { [frenchRowScoreId('r1')]: 1, [frenchRowScoreId('r3')]: 1 })).toBe(5);
  });

  it('reads the 2010–2015 Ordinary "7+1" rule into a ladder when the rows print no price', () => {
    const allocation = allocationOf('fr-2015-ol-reading-a1-q1');
    expect(allocation.ladder).toEqual([7, 8]);
    expect(allocation.rows).toHaveLength(3);
    expect(frenchAllocationMarks(8, allocation, { [frenchRowScoreId('r1')]: 1 })).toBe(7);
    expect(frenchAllocationMarks(8, allocation, { [frenchRowScoreId('r1')]: 1, [frenchRowScoreId('r3')]: 1 })).toBe(8);
  });

  it('prices unpriced stroke alternatives from the one the scheme prices, and asterisks on their own', () => {
    expect(rowMarks(allocationOf('fr-2019-ol-reading-a2-q3'))).toEqual([
      ['At the market', 4], ['in (small) farms / from farmers', 4], ['Locally', 4], ['Local shop', 1],
    ]);
    // "Either of the following 5 marks" prices each stroke line; the asterisk keeps its own 3.
    expect(rowMarks(allocationOf('fr-2018-ol-listening-la-q2i'))).toEqual([
      ['Music festival', 5], ['A lot of famous groups will play there', 5], ['a lot of groups will play', 3],
    ]);
    // "Accept any two of the following: — 4+4 marks": 4 each, two asked.
    const two = allocationOf('fr-2019-ol-reading-a1-q6');
    expect(two.count).toBe(2);
    expect(two.rows.slice(0, 8).every(row => row.marks === 4)).toBe(true);
    expect(two.rows.slice(8).map(row => row.marks)).toEqual([2, 2]);
  });

  it('takes the paper tariff for a stroke card that prints no price at all', () => {
    expect(rowMarks(allocationOf('fr-2012-ol-reading-a1-q1-i'))).toEqual([
      ['Wear a tie / a jacket', 4], ['Do not have studs / piercings', 4], ['Do not wear earrings', 0],
    ]);
    expect(rowMarks(allocationOf('fr-2026-ol-reading-a4-q3'))).toEqual([['Mon/Ma/Mes', 4]]);
  });

  it('keeps deductions and priced conditions as rows, and unpriced notes as directions', () => {
    const deduction = allocationOf('fr-2019-hl-listening-lb-q2ii');
    expect(rowMarks(deduction)).toEqual([
      ['She’d injure herself (her face) / (Her face) would get injured', 3],
      ['Incorrect body part', -1],
    ]);
    const mcq = allocationOf('fr-2026-ol-reading-a4-q6');
    expect(rowMarks(mcq)).toEqual([
      ['Son père (troisième réponse)', 4],
      ['If candidate clearly identifies / highlights correct answer, without using a tick', 4],
      ['If more than one answer offered', 0],
    ]);
    expect(rowMarks(allocationOf('fr-2024-hl-listening-la-q2'))).toEqual([
      ['Monday and Friday', 3], ['Monday', 2], ['Friday', 2], ['One correct day plus one incorrect day', 1],
    ]);
    const noted = allocationOf('fr-2019-hl-listening-lc-q2');
    expect(noted.directions).toEqual(['➢ Accept Security guards.']);
    expect(noted.rows.at(-1)).toMatchObject({ text: 'Police', marks: -1 });
  });

  it('labels rows with the scheme’s own sub-part headings and applies the aural higher-segment rule', () => {
    const allocation = allocationOf('fr-2015-hl-listening-ld-q4');
    expect(allocation.scoring).toBe('higher-segment-both');
    expect(allocation.rows.map(row => row.part)).toEqual(['(a)', '(a)', '(a)', '(a)', '(b)']);
    // One detail at 3 and the other at 1: the higher mark goes to both.
    expect(frenchAllocationMarks(6, allocation, { [frenchRowScoreId('r1')]: 1, [frenchRowScoreId('r4')]: 1 })).toBe(6);
    expect(frenchAllocationMarks(6, allocation, { [frenchRowScoreId('r4')]: 1 })).toBe(2);
    // The ordinary two-detail task next to it sums.
    expect(allocationOf('fr-2026-hl-listening-la-q2').scoring).toBeUndefined();
  });

  it('gives each cloze gap one stepped row: 3, or 2 after the careless-transcription deduction', () => {
    const allocation = allocationOf('fr-2020-ol-cloze-b1a-gap-2');
    expect(allocation.rows).toEqual([{ id: 'r1', text: 'passe/serai', marks: 3, steps: [3, 2] }]);
    expect(allocation.directions).toEqual(['10 gaps for 3 marks each', 'Careless transcription, including accents, deduct 1 mark. Accept capital letters.']);
    expect(allocationOf('fr-2019-ol-cloze-b1a-gap-6').rows[0].text).toBe('travaille');
    expect(allocationOf('fr-2022-ol-cloze-b1a-gap-10').rows[0].text).toBe('On pourrait faire __du____ vélo');
    const card = byId('fr-2020-ol-cloze-b1a-gap-2');
    expect(frenchMarks(card, { [frenchRowScoreId('r1')]: 3 })).toBe(3);
    expect(frenchMarks(card, { [frenchRowScoreId('r1')]: 2 })).toBe(2);
    expect(frenchMarks(card, { [frenchRowScoreId('r1')]: 1 })).toBe(0);
  });

  it('prices an opinion question’s accepted points as the total shared equally, placed at the partial mark where the scheme gives one', () => {
    // "Any two of:" over the points the scheme accepts, priced only in its general rule: 10 marks is two points at 5.
    const higher = allocationOf('fr-2026-hl-reading-a1-q6');
    expect(higher.count).toBe(2);
    expect(higher.ladder).toBeUndefined();
    expect(higher.rows.every(row => row.marks === 5 && !row.steps)).toBe(true);
    expect([...new Set(higher.rows.map(row => row.part))]).toEqual(['Agree:', 'Disagree:']);
    // Ordinary Q8: 8 marks is two points at 4, each placed at 2 where the answer is partially correct.
    const ordinary = allocationOf('fr-2026-ol-reading-a3-q8');
    expect(ordinary.count).toBe(2);
    expect(ordinary.rows.every(row => row.marks === 4 && row.steps?.join() === '2,4')).toBe(true);
    expect(ordinary.directions.some(note => /Award 2 marks if answer is partially correct/i.test(note))).toBe(true);
    expect(frenchAllocationMarks(8, ordinary, { [frenchRowScoreId('r1')]: 4, [frenchRowScoreId('r2')]: 2 })).toBe(6);
    // 2015 Higher Q6: the ledger permits even marks only, so two points at 5 is not a step it allows.
    expect(parseFrenchAnswers(frenchAnswerSource(byId('fr-2015-hl-reading-a1-q6')))).toEqual({ ok: false, reason: 'opinion points at 5 each are not a permitted mark' });
  });
});

describe('French rows score', () => {
  it('sums up to the asked count, taking the highest-valued claims, and never exceeds the total', () => {
    const allocation = allocationOf('fr-2026-hl-listening-la-q2');
    const r = (ids: string[]) => Object.fromEntries(ids.map(id => [frenchRowScoreId(id), 1]));
    expect(frenchAllocationMarks(6, allocation, r(['r1']))).toBe(3);
    expect(frenchAllocationMarks(6, allocation, r(['r1', 'r4']))).toBe(5);
    expect(frenchAllocationMarks(6, allocation, r(['r4', 'r5']))).toBe(2);
    expect(frenchAllocationMarks(6, allocation, r(['r1', 'r2', 'r3']))).toBe(6);
  });

  it('applies a claimed deduction and floors at zero', () => {
    const allocation = allocationOf('fr-2019-hl-listening-lb-q2ii');
    expect(frenchAllocationMarks(3, allocation, { [frenchRowScoreId('r1')]: 1, [frenchRowScoreId('r2')]: 1 })).toBe(2);
    expect(frenchAllocationMarks(3, allocation, { [frenchRowScoreId('r2')]: 1 })).toBe(0);
  });

  it('routes a structured card through frenchMarks and ignores the legacy criterion id', () => {
    const card = byId('fr-2026-hl-listening-la-q1');
    expect(frenchMarks(card, { [frenchRowScoreId('r1')]: 1 })).toBe(3);
    expect(frenchMarks(card, { 'french:response': 3 })).toBe(0);
  });
});
