/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { beforeEach, describe, expect, it, vi } from 'vitest';

const callable = vi.fn((_payload: unknown) => Promise.resolve({ data: { accepted: 1 } }));
vi.mock('firebase/functions', () => ({
  getFunctions: () => ({}),
  httpsCallable: () => callable,
}));

vi.stubEnv('VITE_PROGRAMME_MEASUREMENT_ENABLED', 'true');
const analytics = await import('../utils/programmeAnalytics');

describe('programme analytics client', () => {
  beforeEach(() => {
    callable.mockReset();
    callable.mockResolvedValue({ data: { accepted: 1 } });
    window.sessionStorage.clear();
    analytics.resetProgrammeAnalyticsSession();
  });

  it('sends only the structured event contract', async () => {
    analytics.trackProgrammeEvent('module_started', {
      moduleId: 'growth-mindset',
      source: 'module',
    });
    await Promise.resolve();

    expect(callable).toHaveBeenCalledTimes(1);
    const payload = callable.mock.calls[0][0] as { events: Array<Record<string, unknown>> };
    expect(payload.events).toHaveLength(1);
    expect(Object.keys(payload.events[0]).sort()).toEqual([
      'appVersion', 'clientEventId', 'moduleId', 'name', 'platform', 'sessionId', 'source',
    ].sort());
    const serialised = JSON.stringify(payload);
    for (const forbidden of ['email', 'studentName', 'reflection', 'answerText']) {
      expect(serialised).not.toContain(forbidden);
    }
  });

  it('records one session-start event per browser session', async () => {
    analytics.trackProgrammeSessionStarted();
    analytics.trackProgrammeSessionStarted();
    analytics.trackProgrammeSessionStarted();
    await Promise.resolve();
    expect(callable).toHaveBeenCalledTimes(1);
  });

  it('deduplicates feature exposure within the session', async () => {
    analytics.trackProgrammeExposures(['mark-bank', 'paper-trail']);
    analytics.trackProgrammeExposures(['mark-bank', 'paper-trail']);
    await Promise.resolve();
    expect(callable).toHaveBeenCalledTimes(1);
    const payload = callable.mock.calls[0][0] as { events: Array<{ featureId: string }> };
    expect(payload.events.map(event => event.featureId)).toEqual(['mark-bank', 'paper-trail']);
  });

  it('uses broad duration bands rather than exact durations', () => {
    expect(analytics.analyticsDurationBucket(301)).toBe('5_14m');
    expect(analytics.analyticsDurationBucket(1_801)).toBe('30_59m');
  });

  it('resets module-level guards for the next student on a shared device', async () => {
    analytics.trackProgrammeSessionStarted();
    analytics.trackProgrammeExposures(['mark-bank']);
    await Promise.resolve();
    expect(callable).toHaveBeenCalledTimes(2);

    analytics.resetProgrammeAnalyticsSession();
    callable.mockClear();
    analytics.trackProgrammeSessionStarted();
    analytics.trackProgrammeExposures(['mark-bank']);
    await Promise.resolve();
    expect(callable).toHaveBeenCalledTimes(2);
  });

  it('retries a transient delivery failure without blocking the student action', async () => {
    vi.useFakeTimers();
    callable.mockRejectedValueOnce(new Error('offline'));
    analytics.trackProgrammeEvent('module_started', { moduleId: 'growth-mindset', source: 'module' });
    expect(callable).toHaveBeenCalledTimes(1);

    await vi.advanceTimersByTimeAsync(1_000);
    expect(callable).toHaveBeenCalledTimes(2);
    vi.useRealTimers();
  });
});
