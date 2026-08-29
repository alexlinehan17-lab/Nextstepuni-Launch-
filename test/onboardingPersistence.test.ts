import { describe, expect, it } from 'vitest';
import { progressNeedsOnboarding } from '../services/progressRepository';

describe('onboarding persistence', () => {
  it('requires setup for a new or empty progress document', () => {
    expect(progressNeedsOnboarding(null)).toBe(true);
    expect(progressNeedsOnboarding({})).toBe(true);
  });

  it('respects an explicitly skipped setup after refresh', () => {
    expect(progressNeedsOnboarding({ onboardingSkippedAt: '2026-08-29T20:00:00.000Z' })).toBe(false);
  });

  it('treats a saved subject profile as completed setup', () => {
    expect(progressNeedsOnboarding({ subjectProfile: {} as never })).toBe(false);
  });
});
