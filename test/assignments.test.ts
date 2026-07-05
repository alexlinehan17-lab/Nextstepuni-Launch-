/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the assignments status logic (feature E9): done wins, an overdue open
 * task is flagged by date, and the summary tallies correctly. Pure helpers only
 * (the Firestore accessors are ship-gated).
 */
import { describe, it, expect } from 'vitest';
import { assignmentStatus, summariseAssignments, type Assignment } from '../data/assignments';

const A = (id: string, dueIso?: string): Assignment => ({ id, title: id, kind: 'topic', dueIso, createdTs: 0 });

describe('Assignments — status', () => {
  it('done wins regardless of due date', () => {
    expect(assignmentStatus(A('a', '2020-01-01'), 123, '2026-07-05')).toBe('done');
  });

  it('a past due date with no completion is overdue', () => {
    expect(assignmentStatus(A('a', '2026-07-01'), undefined, '2026-07-05')).toBe('overdue');
  });

  it('a future or absent due date is open', () => {
    expect(assignmentStatus(A('a', '2026-07-10'), undefined, '2026-07-05')).toBe('open');
    expect(assignmentStatus(A('a'), undefined, '2026-07-05')).toBe('open');
  });

  it('summarises a set against a completion map', () => {
    const items = [A('a', '2026-07-01'), A('b', '2026-07-10'), A('c')];
    const s = summariseAssignments(items, { c: 999 }, '2026-07-05');
    expect(s).toEqual({ overdue: 1, open: 1, done: 1 });
  });
});
