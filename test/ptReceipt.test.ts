/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the end-of-loop receipt's PURE layout: the exact text lines composed
 * for given stats, the success-vs-accent score rule, duration and gap
 * formatting — and that the layout is anonymous by construction.
 */
import { describe, it, expect } from 'vitest';
import {
  composeReceipt,
  formatDuration,
  formatGaps,
  prettyDate,
  type LoopReceiptStats,
} from '../components/PaperTrail/receipt';

const stats = (over: Partial<LoopReceiptStats> = {}): LoopReceiptStats => ({
  dateIso: '2026-07-07',
  paperTitle: 'Biology · 2023',
  paperDetail: 'Paper One · Higher',
  questionsWorked: 8,
  questionsTotal: 10,
  totalSec: 25 * 60,
  avgPct: 72,
  gaps: { careless: 3, timing: 1 },
  ...over,
});

describe('Paper Trail — loop receipt layout', () => {
  it('composes the full receipt for a marked session', () => {
    const r = composeReceipt(stats());
    expect(r.header).toBe('THE FULL LOOP · RECEIPT');
    expect(r.date).toBe('7 July 2026');
    expect(r.title).toBe('Biology · 2023');
    expect(r.detail).toBe('Paper One · Higher');
    expect(r.score).toBe('72%');
    expect(r.rows).toEqual([
      { label: 'Questions worked', value: '8 of 10' },
      { label: 'Time', value: '25 min' },
      { label: 'Average self-mark', value: '72%' },
      { label: 'Gaps flagged', value: '3× careless, 1× timing' },
    ]);
    expect(r.footer).toContain('Paper Trail');
  });

  it('uses success only at a genuinely good average (>= 66)', () => {
    expect(composeReceipt(stats({ avgPct: 66 })).scoreIsGood).toBe(true);
    expect(composeReceipt(stats({ avgPct: 65 })).scoreIsGood).toBe(false);
    expect(composeReceipt(stats({ avgPct: null })).scoreIsGood).toBe(false);
  });

  it('reads honestly when nothing was marked', () => {
    const r = composeReceipt(stats({ avgPct: null, questionsWorked: 0, gaps: {}, totalSec: 0 }));
    expect(r.score).toBe('—');
    expect(r.rows).toContainEqual({ label: 'Average self-mark', value: '—' });
    expect(r.rows).toContainEqual({ label: 'Gaps flagged', value: 'none flagged' });
    expect(r.rows).toContainEqual({ label: 'Time', value: '—' });
  });

  it('carries no student identity anywhere in the layout', () => {
    const r = composeReceipt(stats());
    const text = JSON.stringify(r);
    // The layout is built ONLY from the stats fields — spot-check that nothing
    // uid-shaped or name-shaped can appear beyond what was passed in.
    expect(text).not.toMatch(/uid|user|name|@/i);
  });

  it('formats durations across the ranges', () => {
    expect(formatDuration(0)).toBe('—');
    expect(formatDuration(20)).toBe('under a minute');
    expect(formatDuration(90)).toBe('2 min');
    expect(formatDuration(3600)).toBe('1 h');
    expect(formatDuration(3660)).toBe('1 h 1 min');
  });

  it('formats gaps by frequency, and degrades gracefully', () => {
    expect(formatGaps({ timing: 1, content: 4 })).toBe('4× content, 1× timing');
    expect(formatGaps({})).toBe('none flagged');
  });

  it('falls back to the raw string for a malformed date', () => {
    expect(prettyDate('yesterday')).toBe('yesterday');
    expect(prettyDate('2026-01-01')).toBe('1 January 2026');
  });
});
