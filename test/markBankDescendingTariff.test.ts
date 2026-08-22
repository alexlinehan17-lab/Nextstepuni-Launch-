/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A menu whose options are not all worth the same.
 *
 * Economics is built on this shape: "Discuss two economic consequences of an
 * increasing population" pays 6 for the first and 4 for the second, and it is
 * the commonest tariff on the paper — four of the five long parts of one 2024
 * question. Before `perOptionSteps` the choice was to print a per-option value
 * that is wrong for one of the two, or to card half of every question.
 *
 * Three things have to agree about it or a student is shown a total that is not
 * the paper's: the type's arithmetic, the build's tariff check, and the session
 * screen's running score.
 */
import { describe, expect, it } from 'vitest';

import { groupMarks, tariffReconciles, type SecCard } from '../types/markBank';
import { rowMarks as sessionRowMarks } from '../components/MarkBank/SessionScreen';

const descending = { claimMax: 2, perOption: 6, perOptionSteps: [6, 4], options: ['a', 'b', 'c'] };
const flat = { claimMax: 3, perOption: 5, options: ['a', 'b', 'c', 'd'] };

describe('a descending per-option tariff', () => {
  it('is worth the sum of its steps, not claimMax times one value', () => {
    expect(groupMarks(descending)).toBe(10);
    expect(groupMarks(descending)).not.toBe(descending.claimMax * descending.perOption);
  });

  it('leaves a flat tariff alone', () => {
    expect(groupMarks(flat)).toBe(15);
  });

  it('counts the same in the type and in the session screen', () => {
    const row = { id: 'r-1', kind: 'anyN' as const, verbatim: 'x', marks: null, group: descending };
    // The session screen is where a student sees the number, so it is the one
    // that must not drift from the type's arithmetic.
    expect(sessionRowMarks(row)).toBe(groupMarks(descending));
    expect(sessionRowMarks(row)).toBe(10);
  });

  it('reconciles against the printed tariff', () => {
    const card = {
      id: 'econ-test', subjectId: 'economics', level: 'higher', topicId: 't', conceptId: 'c',
      year: 2024, section: 'B', questionRef: 'ref', questionText: 'q',
      tariffModel: { kind: 'fixed' }, totalMarks: 10,
      rows: [{ id: 'r-1', kind: 'anyN', verbatim: 'x', marks: null, group: descending }],
    } as unknown as SecCard;
    expect(tariffReconciles(card)).toBe(true);
    // The old arithmetic would have made this 12 against a 10-mark question.
    expect(tariffReconciles({ ...card, totalMarks: 12 } as SecCard)).toBe(false);
  });

  it('keeps perOption as the FIRST step, so a reader of only that is never wrong by more than the tail', () => {
    expect(descending.perOption).toBe(descending.perOptionSteps[0]);
  });
});
