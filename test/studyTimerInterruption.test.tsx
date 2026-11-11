import { act, cleanup, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { useStudySession } from '@/hooks/useStudySession';
import { readActiveStudySession, writeActiveStudySession } from '@/services/studySessionStore';
import { OPEN_ENDED_CAP_MINUTES } from '@/studySessionData';

const env = vi.hoisted(() => ({ native: false, sessions: [], add: vi.fn() }));
vi.mock('@capacitor/core', () => ({ Capacitor: { isNativePlatform: () => env.native, getPlatform: () => env.native ? 'ios' : 'web' } }));
vi.mock('@/contexts/ProgressContext', () => ({ useProgress: () => ({ studySessions: env.sessions, progressLoaded: true, updateDemoProgress: vi.fn(), addStudySession: env.add, reloadProgress: vi.fn() }) }));
vi.mock('@/utils/programmeAnalytics', () => ({ trackProgrammeEvent: vi.fn(), analyticsDurationBucket: vi.fn() }));
const NOW = new Date('2026-11-10T12:00:00Z').getTime();
const MIN = 60_000;
const uid = 'timer-feedback4-audit';
function visibility(state: 'visible' | 'hidden') { Object.defineProperty(document, 'visibilityState', { configurable: true, value: state }); document.dispatchEvent(new Event('visibilitychange')); }
beforeEach(() => { vi.useFakeTimers(); vi.setSystemTime(NOW); env.native = false; sessionStorage.clear(); localStorage.clear(); visibility('visible'); });
afterEach(() => { cleanup(); vi.useRealTimers(); delete (document as unknown as Record<string, unknown>).visibilityState; });
for (const native of [false, true]) for (const openEnded of [false, true]) {
 const label = `${native ? 'native storage' : 'web storage'} / ${openEnded ? 'stopwatch' : 'countdown'}`;
 test(`${label}: catches up after suspended callbacks and returning from another app`, () => {
  env.native = native;
  const { result } = renderHook(() => useStudySession(uid, {}, []));
  act(() => result.current.startSession('Biology', 'practice', openEnded ? 0 : 25, undefined, { openEnded }));
  act(() => vi.advanceTimersByTime(2 * MIN));
  act(() => visibility('hidden'));
  // Clock advances without firing JS intervals, as when the OS suspends the app.
  vi.setSystemTime(NOW + 14 * MIN);
  expect(result.current.elapsedSeconds).toBe(120);
  act(() => visibility('visible'));
  expect(result.current.elapsedSeconds).toBe(840);
  expect(result.current.phase).toBe('active');
  act(() => result.current.pauseSession());
  act(() => visibility('hidden'));
  vi.setSystemTime(NOW + 60 * MIN);
  act(() => visibility('visible'));
  expect(result.current.elapsedSeconds).toBe(840);
  act(() => result.current.resumeSession());
  act(() => vi.advanceTimersByTime(2 * MIN));
  expect(result.current.elapsedSeconds).toBe(960);
 });
 test(`${label}: reload/relaunch counts time away without changing the saved session`, () => {
  env.native = native;
  const first = renderHook(() => useStudySession(uid, {}, []));
  act(() => first.result.current.startSession('Biology', 'practice', openEnded ? 0 : 25, undefined, { openEnded }));
  act(() => vi.advanceTimersByTime(2 * MIN));
  first.unmount();
  if (native) sessionStorage.clear(); // A new native WebView has a fresh session store.
  vi.setSystemTime(NOW + 14 * MIN);
  const second = renderHook(() => useStudySession(uid, {}, []));
  expect(second.result.current.elapsedSeconds).toBe(840);
  expect(second.result.current.subject).toBe('Biology');
  expect(second.result.current.openEnded).toBe(openEnded);
  expect(second.result.current.phase).toBe('active');
 });
 test(`${label}: paused reload does not count the break, then resumes accurately`, () => {
  env.native = native;
  const first = renderHook(() => useStudySession(uid, {}, []));
  act(() => first.result.current.startSession('Biology', 'practice', openEnded ? 0 : 25, undefined, { openEnded }));
  act(() => vi.advanceTimersByTime(7 * MIN));
  act(() => first.result.current.pauseSession());
  first.unmount();
  if (native) sessionStorage.clear();
  vi.setSystemTime(NOW + 60 * MIN);
  const second = renderHook(() => useStudySession(uid, {}, []));
  expect(second.result.current.phase).toBe('paused');
  expect(second.result.current.elapsedSeconds).toBe(420);
  act(() => second.result.current.resumeSession());
  act(() => vi.advanceTimersByTime(2 * MIN));
  expect(second.result.current.elapsedSeconds).toBe(540);
 });
}
for (const openEnded of [false, true]) test(`${openEnded ? 'stopwatch cap' : 'countdown end'}: long suspension completes at the correct limit`, () => {
 const { result } = renderHook(() => useStudySession(uid, {}, []));
 act(() => result.current.startSession('Biology', 'practice', openEnded ? 0 : 25, undefined, { openEnded }));
 act(() => visibility('hidden'));
 vi.setSystemTime(NOW + 10 * 60 * MIN);
 act(() => visibility('visible'));
 expect(result.current.phase).toBe('complete');
 expect(result.current.elapsedSeconds).toBe((openEnded ? OPEN_ENDED_CAP_MINUTES : 25) * 60);
 expect(readActiveStudySession(uid)?.phase).toBe('complete');
});
test('extension catches up after suspension and relaunch without counting the completed-session gap', () => {
 env.native = true;
 const first = renderHook(() => useStudySession(uid, {}, []));
 act(() => first.result.current.startSession('Biology', 'practice', 25));
 act(() => vi.advanceTimersByTime(25 * MIN));
 vi.setSystemTime(NOW + 40 * MIN);
 act(() => first.result.current.extendSession(10));
 first.unmount(); sessionStorage.clear();
 vi.setSystemTime(NOW + 44 * MIN);
 const second = renderHook(() => useStudySession(uid, {}, []));
 expect(second.result.current.elapsedSeconds).toBe(29 * 60);
 expect(second.result.current.totalDuration).toBe(35 * 60);
});
test('an early finish survives relaunch without becoming a fully completed countdown', () => {
 env.native = true;
 writeActiveStudySession(uid, { subject: 'Biology', sessionType: 'practice', plannedMinutes: 25, startedAt: NOW - 10 * MIN, phase: 'complete', elapsedSeconds: 600, completedPrompts: [] });
 const { result } = renderHook(() => useStudySession(uid, {}, []));
 expect(result.current.elapsedSeconds).toBe(600);
 expect(result.current.phase).toBe('complete');
 expect(result.current.extendSession(5)).toBe(false);
});

// Both previously reproduced defects must remain fixed.
test('rapid Keep going actions must claim a completion once', () => {
 const { result } = renderHook(() => useStudySession(uid, {}, []));
 act(() => result.current.startSession('Biology', 'practice', 25));
 act(() => vi.advanceTimersByTime(25 * MIN));
 let first = false, second = false;
 act(() => { first = result.current.extendSession(5); second = result.current.extendSession(5); });
 const extendedMinutes = result.current.extendedMinutes;
 act(() => vi.advanceTimersByTime(5 * MIN));
 expect({ first, second, extendedMinutes, phase: result.current.phase, elapsedSeconds: result.current.elapsedSeconds, totalDuration: result.current.totalDuration }).toEqual({ first: true, second: false, extendedMinutes: 5, phase: 'complete', elapsedSeconds: 1800, totalDuration: 1800 });
});
test('the native stopwatch receives the same limit as the session engine', async () => {
 const { studyActivityState } = await import('@/services/studyTimerAlerts');
 const { result } = renderHook(() => useStudySession(uid, {}, []));
 act(() => result.current.startSession('Biology', 'practice', 0, undefined, { openEnded: true }));
 const activity = studyActivityState(result.current);
 expect(activity?.totalSeconds).toBe(OPEN_ENDED_CAP_MINUTES * 60);
});
