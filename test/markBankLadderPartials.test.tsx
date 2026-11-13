/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ladder partials: a menu priced by a descending tariff (perOptionSteps) whose
 * options may carry a lower price of their own (optionMarks), "N.B. X = 1 mark
 * only" under a "3 + 1" menu or a "[2]" partial inside a "4 + 3 + 3" one. The
 * claimed answers, sorted by their cap, are paired with the steps in falling
 * order and each earns the lesser of its step and its cap (ladderGroupMarks).
 */

import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import SessionScreen, { marksClaimed } from '@/components/MarkBank/SessionScreen';
import { LEVELS, SUBJECTS, loadCards } from '@/components/MarkBank/deck';
import { anyNHeading } from '@/components/MarkBank/sessionText';
import { groupMarks, ladderGroupMarks, rowId, type MarkRow, type SecCard, type SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const threeOne = { claimMax: 2, perOption: 3, perOptionSteps: [3, 1], options: ['Full answer A', 'Full answer B', 'X'], optionMarks: [3, 3, 1] };
const fourThreeThree = { claimMax: 3, perOption: 4, perOptionSteps: [4, 3, 3], options: ['a', 'b', 'c', 'partial'], optionMarks: [4, 4, 4, 2] };

describe('a 3 + 1 menu with a "1 mark only" option', () => {
  test('the capped option alone earns 1', () => {
    expect(ladderGroupMarks(threeOne, [2])).toBe(1);
  });
  test('a full answer with the capped option earns 3 + 1, in either click order', () => {
    expect(ladderGroupMarks(threeOne, [0, 2])).toBe(4);
    expect(ladderGroupMarks(threeOne, [2, 0])).toBe(4);
  });
  test('two full answers earn 3 + 1, and the group is worth 4', () => {
    expect(ladderGroupMarks(threeOne, [0, 1])).toBe(4);
    expect(groupMarks(threeOne)).toBe(4);
  });
});

describe('a 4 + 3 + 3 menu with a [2] partial', () => {
  test('the partial alone earns 2', () => {
    expect(ladderGroupMarks(fourThreeThree, [3])).toBe(2);
  });
  test('with two full answers it earns 4 + 3 + 2', () => {
    expect(ladderGroupMarks(fourThreeThree, [0, 3, 1])).toBe(9);
    expect(ladderGroupMarks(fourThreeThree, [3, 1, 0])).toBe(9);
  });
  test('claimMax holds: a fourth claim adds nothing', () => {
    expect(ladderGroupMarks(fourThreeThree, [0, 1, 2, 3])).toBe(10);
  });
  test('a partial of an answer counts once with that answer (optionOf)', () => {
    const g = { ...fourThreeThree, optionOf: [null, null, null, 0] };
    expect(ladderGroupMarks(g, [0, 3])).toBe(4);
    expect(ladderGroupMarks(g, [3])).toBe(2);
  });
});

describe('the heading states the steps', () => {
  test('a ladder with option prices reads its steps, each option showing its own price', () => {
    expect(anyNHeading(threeOne)).toBe('Any 2 of these — 3 then 1 marks');
    expect(anyNHeading(fourThreeThree)).toBe('Any 3 of these — 4 then 3 then 3 marks');
  });
});

describe('on screen', () => {
  test('the capped option alone shows 1 of the card\'s 4 marks', () => {
    const c = {
      source: 'sec', kind: 'question', id: 'ladder-fixture', subjectId: 'german', level: 'ordinary',
      topicId: 'german-1', conceptId: 'ladder', year: 2015, paperFileid: null, section: 'T3',
      questionRef: '2015 OL Section T3 Q1', questionText: 'Give two reasons.',
      tariffModel: { kind: 'fixed' }, totalMarks: 4,
      rows: [{ id: 'm', kind: 'anyN', verbatim: 'Reasons', marks: 4, group: threeOne } as MarkRow],
      schemeCitation: 'fixture', specVersion: 'fixture', qa: { gates: [], humanReviewedBy: 'x', humanReviewedAt: '2026-11-13' },
    } as unknown as SecQuestionCard;
    render(<SessionScreen cards={[c]} subjectLabel="German" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /^X/ }));
    expect(document.getElementById('mark-bank-grade-guidance')?.textContent).toContain('You claimed 1 of 4 marks');
    fireEvent.click(screen.getByRole('button', { name: /^Full answer A/ }));
    expect(document.getElementById('mark-bank-grade-guidance')?.textContent).toContain('You claimed 4 of 4 marks');
  });
});

describe('every shipped step menu without option prices scores as before', () => {
  test('first steps as printed, for every number of picks, in every deck', async () => {
    const before = (steps: number[], claimMax: number, k: number) =>
      steps.slice(0, Math.min(k, claimMax)).reduce((n, m) => n + m, 0);
    let menus = 0;
    for (const subject of SUBJECTS) {
      for (const level of LEVELS) {
        const cards: SecCard[] = await loadCards(subject.id, level);
        for (const card of cards) {
          if (!('rows' in card) || !Array.isArray(card.rows)) continue;
          (card.rows as MarkRow[]).forEach((row, i) => {
            const g = row.group;
            if (row.kind !== 'anyN' || !g?.perOptionSteps || g.optionMarks) return;
            menus++;
            for (let k = 0; k <= g.options.length; k++) {
              const picked = g.options.map((_o, j) => j).slice(0, k);
              expect(ladderGroupMarks({ ...g, perOptionSteps: g.perOptionSteps }, picked), `${card.id} ${row.id} k=${k}`)
                .toBe(before(g.perOptionSteps, g.claimMax, k));
              if ((card as SecQuestionCard).tariffModel?.kind === 'fixed') {
                const solo = { ...card, rows: [row] } as SecQuestionCard;
                expect(marksClaimed(solo, {}, { [rowId(row, i)]: picked }), `${card.id} ${row.id} k=${k} on screen`)
                  .toBe(before(g.perOptionSteps, g.claimMax, k));
              }
            }
          });
        }
      }
    }
    expect(menus).toBeGreaterThan(1500);
  }, 600_000);
});
