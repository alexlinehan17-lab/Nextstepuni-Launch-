/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The funnel is instrumentation, so its failure mode is the opposite of most
 * code: it must never affect the flow it measures. These tests pin the two
 * properties that matter — it cannot throw into a student's path, and it
 * cannot inflate its own numbers — plus the payload carrying no personal data.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

type EventPayload = Record<string, unknown>;

const addDoc = vi.fn((_ref: { path: string }, _payload: EventPayload) =>
  Promise.resolve({ id: 'evt' }));

vi.mock('firebase/firestore', () => ({
  addDoc: (ref: { path: string }, payload: EventPayload) => addDoc(ref, payload),
  collection: (_db: unknown, path: string) => ({ path }),
  serverTimestamp: () => 'SERVER_TS',
}));

const { trackFunnel, FUNNEL_STEPS, __testing } = await import('../utils/funnel');

describe('funnel instrumentation', () => {
  beforeEach(() => {
    addDoc.mockClear();
    addDoc.mockImplementation(() => Promise.resolve({ id: 'evt' }));
    window.sessionStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('writes an event with no personal data in it', () => {
    trackFunnel('register_succeeded');

    expect(addDoc).toHaveBeenCalledTimes(1);
    const [ref, payload] = addDoc.mock.calls[0];
    expect(ref.path).toBe('funnelEvents');
    // The exact key set the Firestore rules allow — nothing more may be added
    // without a matching rules change, and nothing here identifies a student.
    expect(Object.keys(payload).sort()).toEqual(['at', 'day', 'platform', 'sessionId', 'step'].sort());
    const serialised = JSON.stringify(payload);
    for (const forbidden of ['uid', 'email', 'name', 'school']) {
      expect(serialised).not.toContain(forbidden);
    }
  });

  it('records each step once per session, so a re-render cannot inflate it', () => {
    trackFunnel('onboarding_started');
    trackFunnel('onboarding_started');
    trackFunnel('onboarding_started');
    expect(addDoc).toHaveBeenCalledTimes(1);

    trackFunnel('onboarding_completed');
    expect(addDoc).toHaveBeenCalledTimes(2);
  });

  it('never throws when the write is rejected', async () => {
    addDoc.mockImplementation(() => Promise.reject(new Error('permission-denied')));
    expect(() => trackFunnel('first_tool_opened')).not.toThrow();
    // Let the rejection settle: an unhandled rejection here would fail the run.
    await new Promise(resolve => setTimeout(resolve, 0));
  });

  it('never throws when storage is unavailable (Safari private mode)', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('denied'); });
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('denied'); });
    expect(() => trackFunnel('onboarding_skipped')).not.toThrow();
    expect(addDoc).toHaveBeenCalledTimes(1);
  });

  it('stamps the LOCAL calendar day, not the UTC one', () => {
    // 00:30 Irish time on 3 June is still 2 June in UTC. The exam countdown,
    // the study week and these counters must all agree on the Irish day.
    const localMidnightish = new Date(2026, 5, 3, 0, 30);
    expect(__testing.localDay(localMidnightish)).toBe('2026-06-03');
  });

  it('keeps the step list stable and unique', () => {
    expect(new Set(FUNNEL_STEPS).size).toBe(FUNNEL_STEPS.length);
    expect(FUNNEL_STEPS).toContain('register_succeeded');
    expect(FUNNEL_STEPS).toContain('first_tool_opened');
  });
});
