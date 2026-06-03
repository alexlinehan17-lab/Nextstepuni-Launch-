/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * College Compass completion model. The student tool and the GC dashboard both
 * derive progress through `computeCompassProgress` / `itemStatus`, so these
 * tests are the regression guard on the "student marks == GC sees" promise.
 */
import { describe, test, expect } from 'vitest';
import { computeCompassProgress, itemStatus, JOURNEY_STOPS } from '@/collegeCompassData';

// Two distinct item keys from the real trail.
const allKeys: string[] = [];
for (const stop of JOURNEY_STOPS) for (const it of stop.checklistItems) allKeys.push(`${stop.id}:${it.id}`);
const k0 = allKeys[0];
const k1 = allKeys[1];

describe('College Compass completion model', () => {
  test('itemStatus reads new statuses and tolerates the legacy boolean true', () => {
    expect(itemStatus({ [k0]: 'done' }, k0)).toBe('done');
    expect(itemStatus({ [k0]: 'in-progress' }, k0)).toBe('in-progress');
    expect(itemStatus({ [k0]: true }, k0)).toBe('done'); // legacy docs
    expect(itemStatus({}, k0)).toBe('not-started');
    expect(itemStatus(undefined, k0)).toBe('not-started');
  });

  test('legacy boolean checklist yields the SAME progress as the equivalent string map', () => {
    const legacy = computeCompassProgress({ checklist: { [k0]: true } });
    const modern = computeCompassProgress({ checklist: { [k0]: 'done' } });
    expect(modern.doneItems).toBe(legacy.doneItems);
    expect(modern.percentDone).toBe(legacy.percentDone);
    expect(modern.doneItems).toBe(1);
  });

  test('CONSISTENCY: the same state always derives identical progress (student == GC)', () => {
    const state = { checklist: { [k0]: 'done' as const, [k1]: 'in-progress' as const }, updatedAt: '2026-06-03T00:00:00Z' };
    const studentView = computeCompassProgress(state);
    const gcView = computeCompassProgress(state);
    expect(gcView).toEqual(studentView); // byte-for-byte identical, by construction
    expect(studentView.doneItems).toBe(1);
    expect(studentView.inProgressItems).toBe(1);
    expect(studentView.percentDone).toBe(Math.round((1 / studentView.totalItems) * 100));
  });

  test('dismissed stops are excluded from the denominator and flagged', () => {
    const first = JOURNEY_STOPS[0];
    const full = computeCompassProgress({ checklist: {} });
    const dismissed = computeCompassProgress({ checklist: {}, dismissedStops: [first.id] });
    expect(dismissed.totalItems).toBe(full.totalItems - first.checklistItems.length);
    expect(dismissed.stops.find(s => s.stopId === first.id)?.dismissed).toBe(true);
  });

  test('empty / missing state is safe', () => {
    expect(computeCompassProgress(null).doneItems).toBe(0);
    expect(computeCompassProgress(undefined).percentDone).toBe(0);
    expect(computeCompassProgress({}).stops.length).toBe(JOURNEY_STOPS.length);
  });
});
