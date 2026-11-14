/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The languages lane's ladder partials (coordinator go-ahead, 14 Nov 2026,
 * once #366 was live): a menu the scheme pays in falling steps ("3, 2") whose
 * scheme prices one answer lower ("N.B. Problem = 1 mark only", "Leaves a tip
 * [2] of 100 million"). That answer is an option at its own printed price
 * (optionMarks beside perOptionSteps), the N.B. is quoted in the row note and
 * not in the option, and the menu pays by the ladder (ladderGroupMarks): the
 * capped option alone earns its cap, full answers earn the scheme's steps.
 */

import { describe, expect, test } from 'vitest';

import { CARDS as GERMAN_HIGHER } from '@/components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '@/components/MarkBank/cards/german/ordinary';
import { CARDS as SPANISH_HIGHER } from '@/components/MarkBank/cards/spanish/higher';
import { groupMarks, ladderGroupMarks, tariffReconciles } from '@/types/markBank';
import type { SecCard, SecQuestionCard } from '@/types/markBank';

const deck: SecCard[] = [...GERMAN_HIGHER, ...GERMAN_ORDINARY, ...SPANISH_HIGHER];

/** card id, row id, the capped answer, its price, the steps, what the scheme quotes in the note (null: none). */
const LADDERS: Array<[string, string, string, number, number[], string | null]> = [
  ['de-2015-ol-t3-1', 'r-2', 'he asks himself questions', 1, [3, 1], '“Allow global “he asks himself questions” = 1 mark”'],
  ['de-2015-ol-t3-4', 'r-1', 'Problem', 1, [3, 2], '“N.B. Problem = 1 mark only”'],
  ['de-2016-ol-t2-2-a', 'r-1', 'Mother had no job', 1, [3, 2], '“N.B. : Mother had no job = 1 mark only”'],
  ['de-2016-ol-l1-1-i', 'r-1', 'He has 2 children', 1, [4, 2], '“N.B.: He has 2 children = 1 mark only”'],
  ['de-2014-ol-t2-3', 'r-1', 'They deliver/bring coffee to the staff room/teachers', 2, [5, 3], '“N.B. If “during break” is missing: 2 marks only”'],
  ['de-2012-ol-l3-2', 'r-1', 'For 4 days', 2, [6, 3], '“N. B: For 4 days = 2 marks only”'],
  ['de-2012-ol-l3-3', 'r-1', 'She is worried', 1, [6, 2], '“N. B: She is worried = 1 mark only”'],
  ['es-2015-hl-a1a-3', 'r-1', 'Leaves a tip', 2, [4, 3, 3], null],
];

const ladderOf = (id: string, rowId: string) => {
  const card = deck.find(c => c.id === id) as SecQuestionCard | undefined;
  if (!card) throw new Error(`no live card ${id}`);
  const row = card.rows.find(r => r.id === rowId);
  if (!row?.group?.perOptionSteps || !row.group.optionMarks) throw new Error(`${id} ${rowId} is not a ladder`);
  return { card, row, g: { ...row.group, perOptionSteps: row.group.perOptionSteps, optionMarks: row.group.optionMarks } };
};

describe('ladder partials in the language decks', () => {
  test.each(LADDERS)('%s: "%s" alone earns its cap; full answers earn the steps', (id, rowId, capped, cap, steps, quoted) => {
    const { card, row, g } = ladderOf(id, rowId);
    expect(g.perOptionSteps).toEqual(steps);
    const k = g.options.indexOf(capped);
    expect(k).toBeGreaterThanOrEqual(0);
    expect(g.optionMarks[k]).toBe(cap);
    // The capped option alone earns its cap, never a step.
    expect(ladderGroupMarks(g, [k])).toBe(cap);
    // Full answers (every option priced at the top step, none a partial of
    // another) earn the scheme's steps, claimMax of them.
    const full = g.options.map((_o, i) => i).filter(i => g.optionMarks[i] === Math.max(...steps) && g.optionOf?.[i] == null);
    const scheme = steps.reduce((sum, n) => sum + n, 0);
    expect(ladderGroupMarks(g, full.slice(0, g.claimMax))).toBe(scheme);
    expect(groupMarks(g)).toBe(scheme);
    // With one full answer beside it (where the menu takes two or more), the
    // capped answer takes the next step, at most its cap.
    if (g.claimMax >= 2) {
      const other = full.find(i => i !== g.optionOf?.[k]) as number;
      expect(ladderGroupMarks(g, [k, other])).toBe(steps[0] + Math.min(steps[1], cap));
    }
    // The N.B. is in the row note, quoted, and in no option.
    expect(g.options.some(o => /N\.?\s?B\b/.test(o))).toBe(false);
    if (quoted) expect(row.contextNote).toContain(quoted);
    expect(tariffReconciles(card)).toBe(true);
  });
});
