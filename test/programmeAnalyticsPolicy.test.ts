/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, it } from 'vitest';
import {
  academicYearFor,
  durationBucket,
  reportableProgrammeCell,
  reportableProgrammeRatio,
  validateProgrammeEventBatch,
} from '@/functions/src/programmeAnalyticsPolicy';

const validEvent = {
  clientEventId: '2f37d95b-2f06-4cb9-8d33-997f2d28d66a',
  name: 'feature_started',
  sessionId: 'c907415e-56ad-48aa-accc-fb31cded41c5',
  platform: 'web',
  appVersion: '0.0.0',
  featureId: 'mark-bank',
  source: 'launchpad',
};

describe('programme analytics policy', () => {
  it('accepts the bounded, structured event contract', () => {
    const result = validateProgrammeEventBatch({ events: [validEvent] });
    expect(result.ok).toBe(true);
  });

  it('rejects unknown fields so names, text and email cannot drift into analytics', () => {
    for (const field of ['nameText', 'email', 'feedbackText', 'answer']) {
      const result = validateProgrammeEventBatch({
        events: [{ ...validEvent, [field]: 'personal information' }],
      });
      expect(result).toEqual({ ok: false, reason: 'unknown-field' });
    }
  });

  it('rejects free-form identifiers and out-of-range confidence', () => {
    expect(validateProgrammeEventBatch({ events: [{ ...validEvent, featureId: 'A name with spaces' }] }).ok).toBe(false);
    expect(validateProgrammeEventBatch({ events: [{
      clientEventId: validEvent.clientEventId,
      name: 'study_session_completed',
      sessionId: validEvent.sessionId,
      platform: validEvent.platform,
      appVersion: validEvent.appVersion,
      source: 'study',
      sessionType: 'practice',
      durationBucket: '15_29m',
      confidenceScore: 6,
    }] }).ok).toBe(false);
  });

  it('enforces the field contract for each event type', () => {
    expect(validateProgrammeEventBatch({ events: [{ ...validEvent, featureId: undefined }] }))
      .toEqual({ ok: false, reason: 'event-required-field' });
    expect(validateProgrammeEventBatch({ events: [{ ...validEvent, topicId: 'bio-2-6' }] }))
      .toEqual({ ok: false, reason: 'event-field' });
    expect(validateProgrammeEventBatch({ events: [{ ...validEvent, source: 'study' }] }))
      .toEqual({ ok: false, reason: 'event-source' });
  });

  it('caps each call to 25 events', () => {
    expect(validateProgrammeEventBatch({ events: Array.from({ length: 26 }, () => validEvent) }))
      .toEqual({ ok: false, reason: 'batch-size' });
  });

  it('uses stable duration buckets rather than retaining exact study time in events', () => {
    expect(durationBucket(60)).toBe('under_5m');
    expect(durationBucket(5 * 60)).toBe('5_14m');
    expect(durationBucket(29 * 60)).toBe('15_29m');
    expect(durationBucket(61 * 60)).toBe('60m_plus');
  });

  it('rolls the academic year in August', () => {
    expect(academicYearFor(new Date('2026-07-31T12:00:00Z'))).toBe('2025-2026');
    expect(academicYearFor(new Date('2026-08-01T12:00:00Z'))).toBe('2026-2027');
  });

  it('suppresses both small denominators and small non-zero numerators', () => {
    expect(reportableProgrammeRatio(3, 3)).toMatchObject({ suppressed: true, numerator: null });
    expect(reportableProgrammeRatio(3, 10)).toMatchObject({ suppressed: true, numerator: null });
    expect(reportableProgrammeRatio(5, 6)).toMatchObject({ suppressed: true, numerator: null });
    expect(reportableProgrammeRatio(0, 10)).toEqual({
      suppressed: false,
      numerator: 0,
      denominator: 10,
      percentage: 0,
    });
    expect(reportableProgrammeRatio(5, 10)).toEqual({
      suppressed: false,
      numerator: 5,
      denominator: 10,
      percentage: 50,
    });
  });

  it('shows zero and aggregate cells while hiding values from one to four', () => {
    expect(reportableProgrammeCell(0)).toBe(0);
    expect(reportableProgrammeCell(1)).toBeNull();
    expect(reportableProgrammeCell(4)).toBeNull();
    expect(reportableProgrammeCell(5)).toBe(5);
  });
});
