/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail focus grove (feature E7): sessions accumulate, today's
 * minutes are counted by local day, and totals aggregate.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { addSession, loadGrove, focusStats } from '../components/PaperTrail/focusStore';

const NOON = (y: number, m: number, d: number) => Date.UTC(y, m - 1, d, 12);

describe('Paper Trail — focus grove', () => {
  beforeEach(() => localStorage.clear());

  it('accumulates sessions newest-first', () => {
    addSession('u1', 25, 1, NOON(2026, 7, 4));
    addSession('u1', 15, 2, NOON(2026, 7, 5));
    const grove = loadGrove('u1');
    expect(grove).toHaveLength(2);
    expect(grove[0].minutes).toBe(15); // newest first
  });

  it('counts today by local day and aggregates totals', () => {
    addSession('u1', 25, 1, NOON(2026, 7, 5));
    addSession('u1', 20, 2, NOON(2026, 7, 5));
    addSession('u1', 45, 3, NOON(2026, 7, 4));
    const s = focusStats('u1', NOON(2026, 7, 5));
    expect(s.todayMinutes).toBe(45); // 25 + 20 today
    expect(s.totalMinutes).toBe(90);
    expect(s.sessions).toBe(3);
  });

  it('is empty for a new student', () => {
    expect(focusStats('u2', NOON(2026, 7, 5))).toEqual({ todayMinutes: 0, sessions: 0, totalMinutes: 0 });
  });
});
