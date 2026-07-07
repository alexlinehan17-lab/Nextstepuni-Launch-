/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Sunday Debrief (F11) — composer unit tests.
 */
import { beforeEach, describe, expect, it } from 'vitest';
import { composeDebrief, debriefSeen, markDebriefSeen, weekKey } from '../components/PaperTrail/debrief';
import { setMark } from '../components/PaperTrail/attemptStore';

const UID = 'debrief-test';
const NOW = 1_750_000_000_000;

beforeEach(() => localStorage.clear());

describe('composeDebrief', () => {
  it('returns null for a week with no signal', () => {
    expect(composeDebrief(UID, NOW)).toBeNull();
  });

  it('recaps this week self-marks and proposes a weak-topic focus only with signal', () => {
    setMark(`${UID}|business|2022|higher|ev|f1`, '1', { score: 50, max: 100, gap: 'content', ts: NOW - 1000 });
    setMark(`${UID}|business|2022|higher|ev|f1`, '2', { score: 100, max: 100, ts: NOW - 2000 });
    const d = composeDebrief(UID, NOW);
    expect(d).not.toBeNull();
    expect(d!.weekMarks).toBe(2);
    expect(d!.lines[0]).toContain('2 questions');
    expect(d!.lines[0]).toContain('75%');
  });

  it('ignores marks older than a week', () => {
    setMark(`${UID}|business|2022|higher|ev|f1`, '1', { score: 50, max: 100, ts: NOW - 8 * 86_400_000 });
    expect(composeDebrief(UID, NOW)).toBeNull();
  });
});

describe('once-per-week dismissal', () => {
  it('is unseen until marked, then seen for the same week only', () => {
    expect(debriefSeen(UID, NOW)).toBe(false);
    markDebriefSeen(UID, NOW);
    expect(debriefSeen(UID, NOW)).toBe(true);
    const nextWeek = NOW + 8 * 86_400_000;
    expect(weekKey(nextWeek)).not.toBe(weekKey(NOW));
    expect(debriefSeen(UID, nextWeek)).toBe(false);
  });
});
