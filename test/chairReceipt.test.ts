/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Examiner's Chair — end-of-session receipt layout (the pure composed model,
 * not the canvas).
 */

import { describe, expect, it } from 'vitest';
import {
  composeReceipt,
  receiptDateLabel,
  receiptFilename,
  type ReceiptStats,
} from '../components/ExaminersChair/receipt';

// 2026-07-07T12:00:00Z
const NOW = Date.UTC(2026, 6, 7, 12, 0, 0);

const stats = (overrides: Partial<ReceiptStats> = {}): ReceiptStats => ({
  sessionTitle: 'The two-mark link',
  subjectLabel: 'Business',
  levelLabel: 'Higher',
  scriptsMarked: 3,
  agreement: 0.78,
  streak: 4,
  ...overrides,
});

describe('composeReceipt', () => {
  it('composes header, title, context and the stat rows', () => {
    const m = composeReceipt(stats(), NOW);
    expect(m.header).toBe('THE EXAMINER’S CHAIR · MARKING RECEIPT');
    expect(m.title).toBe('The two-mark link');
    expect(m.context).toBe('Business · Higher · 7 July 2026');
    expect(m.rows.map(r => [r.label, r.value])).toEqual([
      ['Scripts marked', '3'],
      ['Agreement with the examiner', '78%'],
      ['Calibration', 'Well calibrated'],
      ['Daily Mark streak', '4 days'],
    ]);
    expect(m.footnote.length).toBeGreaterThan(10);
  });

  it('colours agreement with success only at ≥75%, accent below', () => {
    const good = composeReceipt(stats({ agreement: 0.8 }), NOW);
    expect(good.rows[1].tone).toBe('success');
    expect(good.rows[2].tone).toBe('success');
    const low = composeReceipt(stats({ agreement: 0.6 }), NOW);
    expect(low.rows[1].tone).toBe('accent');
    expect(low.rows[1].value).toBe('60%');
    expect(low.rows[2].value).toBe('Getting there');
  });

  it('omits the streak row at streak 0 and singularises 1 day', () => {
    const none = composeReceipt(stats({ streak: 0 }), NOW);
    expect(none.rows.some(r => r.label === 'Daily Mark streak')).toBe(false);
    const one = composeReceipt(stats({ streak: 1 }), NOW);
    expect(one.rows.find(r => r.label === 'Daily Mark streak')?.value).toBe('1 day');
  });

  it('labels drills and the daily mark in the header', () => {
    expect(composeReceipt(stats({ kind: 'borderline-drill' }), NOW).header).toContain('BORDERLINE DRILL');
    expect(composeReceipt(stats({ kind: 'daily-mark' }), NOW).header).toContain('THE DAILY MARK');
  });

  it('is anonymous by construction — nothing beyond the given stats appears', () => {
    const m = composeReceipt(stats(), NOW);
    const everything = [m.header, m.title, m.context, m.footnote, ...m.rows.flatMap(r => [r.label, r.value])].join(' ');
    // The model has no name/uid input, so no identifying text can surface.
    expect(everything).not.toMatch(/uid|@|user/i);
  });
});

describe('date helpers', () => {
  it('formats a deterministic UTC date label', () => {
    expect(receiptDateLabel(NOW)).toBe('7 July 2026');
    expect(receiptDateLabel(Date.UTC(2026, 0, 31))).toBe('31 January 2026');
  });

  it('builds a zero-padded filename', () => {
    expect(receiptFilename(NOW)).toBe('examiners-chair-receipt-2026-07-07.png');
    expect(receiptFilename(Date.UTC(2026, 11, 1))).toBe('examiners-chair-receipt-2026-12-01.png');
  });
});
