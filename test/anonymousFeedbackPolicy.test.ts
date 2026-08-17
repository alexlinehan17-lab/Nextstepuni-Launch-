/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, test } from 'vitest';

import {
  feedbackLimitReached,
  feedbackRateLimitId,
  isEligibleFeedbackUser,
  validateFeedbackRequest,
} from '@/functions/src/anonymousFeedbackPolicy';

describe('anonymous feedback backend policy', () => {
  test('accepts only bounded product fields and drops identity-shaped extras', () => {
    const result = validateFeedbackRequest({
      category: 'broken',
      message: '  The continue button\u0000 does not respond.  ',
      context: {
        surface: 'module',
        moduleId: 'growth-mindset',
        moduleTitle: 'Growth Mindset',
        uid: 'must-not-survive',
      },
      platform: 'ios',
      appVersion: '1.2.3',
      uid: 'must-not-survive',
      email: 'student@example.com',
    } as Record<string, unknown>);

    expect(result).toEqual({
      ok: true,
      value: {
        category: 'broken',
        message: 'The continue button does not respond.',
        context: {
          surface: 'module',
          moduleId: 'growth-mindset',
          moduleTitle: 'Growth Mindset',
        },
        platform: 'ios',
        appVersion: '1.2.3',
      },
    });
  });

  test('rejects invalid categories, platforms, and message lengths', () => {
    expect(validateFeedbackRequest({
      category: 'praise', message: 'A valid length message', platform: 'web', appVersion: '1',
    })).toEqual({ ok: false, reason: 'category' });
    expect(validateFeedbackRequest({
      category: 'broken', message: 'short', platform: 'web', appVersion: '1',
    })).toEqual({ ok: false, reason: 'message' });
    expect(validateFeedbackRequest({
      category: 'broken', message: 'A valid length message', platform: 'desktop', appVersion: '1',
    })).toEqual({ ok: false, reason: 'platform' });
    expect(validateFeedbackRequest({
      category: 'broken', message: 'x'.repeat(2001), platform: 'web', appVersion: '1',
    })).toEqual({ ok: false, reason: 'message' });
  });

  test('rotates a non-plain account bucket each UTC day and caps the sixth write', () => {
    const firstDay = feedbackRateLimitId('student-123', '2026-08-13');
    expect(firstDay).toHaveLength(64);
    expect(firstDay).not.toContain('student-123');
    expect(feedbackRateLimitId('student-123', '2026-08-14')).not.toBe(firstDay);
    expect(feedbackRateLimitId('student-456', '2026-08-13')).not.toBe(firstDay);
    expect(feedbackLimitReached(4)).toBe(false);
    expect(feedbackLimitReached(5)).toBe(true);
  });

  test('accepts verified-school students and rejects missing, unbound, and staff profiles', () => {
    expect(isEligibleFeedbackUser({ school: 'school-a' })).toBe(true);
    expect(isEligibleFeedbackUser(undefined)).toBe(false);
    expect(isEligibleFeedbackUser({ name: 'No school yet' })).toBe(false);
    expect(isEligibleFeedbackUser({ school: 'school-a', role: 'gc' })).toBe(false);
    expect(isEligibleFeedbackUser({ school: 'school-a', isAdmin: true })).toBe(false);
  });
});
