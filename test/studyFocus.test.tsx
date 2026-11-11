import { act, cleanup, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import type * as FocusService from '../services/studyFocus';

const mock = vi.hoisted(() => ({ platform: 'ios', available: true, sync: vi.fn(), configure: vi.fn(), setEnabled: vi.fn() }));
vi.mock('@capacitor/core', () => ({
  Capacitor: { getPlatform: () => mock.platform, isPluginAvailable: () => mock.available },
  registerPlugin: () => mock,
}));
const off = { available: true, authorized: true, enabled: false, active: false, selectionCount: 2 };
const on = { ...off, enabled: true, active: true };
let focus: typeof FocusService;

beforeEach(async () => {
  vi.resetModules();
  mock.platform = 'ios'; mock.available = true;
  mock.sync.mockReset().mockResolvedValue(off);
  mock.configure.mockReset().mockResolvedValue({ ...on, active: false });
  mock.setEnabled.mockReset().mockResolvedValue(off);
  focus = await import('../services/studyFocus');
});
afterEach(cleanup);

test.each(['web', 'android'])('%s never calls the Screen Time plugin or displays the control', async platform => {
  mock.platform = platform;
  await focus.syncStudyFocus('student', 1234);
  await focus.configureStudyFocus();
  await focus.setStudyFocusEnabled(true);
  expect(mock.sync).not.toHaveBeenCalled();
  expect(mock.configure).not.toHaveBeenCalled();
  expect(focus.getStudyFocusSnapshot().available).toBe(false);
});

test('older native builds without the plugin remain usable', async () => {
  mock.available = false;
  await focus.syncStudyFocus('student', 1234);
  expect(mock.sync).not.toHaveBeenCalled();
  expect(focus.getStudyFocusSnapshot().available).toBe(false);
});

test('session sync never requests permission; only the explicit choice does', async () => {
  await focus.syncStudyFocus('student', null);
  expect(mock.configure).not.toHaveBeenCalled();
  await focus.configureStudyFocus();
  expect(mock.configure).toHaveBeenCalledWith({ owner: 'student' });
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: 'student', deadline: null });
});

test('countdown, extension and stopwatch share the real session deadlines', () => {
  const session = { phase: 'active' as const, openEnded: false, startedAt: 1_000, totalDuration: 1500, endsAt: 1_501_000 };
  expect(focus.studyFocusDeadline(session)).toBe(1_501_000);
  expect(focus.studyFocusDeadline({ ...session, endsAt: 1_801_000 })).toBe(1_801_000);
  expect(focus.studyFocusDeadline({ ...session, openEnded: true, totalDuration: 14400 })).toBe(14_401_000);
  for (const phase of ['paused', 'complete', 'idle'] as const) expect(focus.studyFocusDeadline({ ...session, phase })).toBeNull();
});

test('start, pause, resume and finish produce bounded native leases', async () => {
  await focus.syncStudyFocus('student', 1_500_000);
  await focus.syncStudyFocus('student', null);
  await focus.syncStudyFocus('student', 2_100_000);
  await focus.syncStudyFocus('student', null);
  expect(mock.sync.mock.calls.map(([value]) => value)).toEqual([
    { owner: 'student', deadline: 1_500_000 }, { owner: 'student', deadline: null },
    { owner: 'student', deadline: 2_100_000 }, { owner: 'student', deadline: null },
  ]);
});

test('a queued start is superseded by an immediate pause', async () => {
  await Promise.all([focus.syncStudyFocus('student', 10000), focus.syncStudyFocus('student', null)]);
  expect(mock.sync).toHaveBeenCalledTimes(1);
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: 'student', deadline: null });
});

test('sign-out releases while the native picker is still open', async () => {
  await focus.syncStudyFocus('first', 10000);
  let resolvePicker!: (value: typeof on) => void;
  mock.configure.mockImplementationOnce(() => new Promise(resolve => { resolvePicker = resolve; }));
  const choosing = focus.configureStudyFocus();
  await Promise.resolve();
  await focus.syncStudyFocus(undefined, null);
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: null, deadline: null });
  resolvePicker(on);
  await choosing;
  expect(focus.getStudyFocusSnapshot().enabled).toBe(false);
});

test('old picker results cannot cross sign-out and sign-in to the same account', async () => {
  await focus.syncStudyFocus('same', 10000);
  let resolvePicker!: (value: typeof on) => void;
  mock.configure.mockImplementationOnce(() => new Promise(resolve => { resolvePicker = resolve; }));
  const choosing = focus.configureStudyFocus();
  await Promise.resolve();
  await focus.syncStudyFocus(undefined, null);
  await focus.syncStudyFocus('same', null);
  resolvePicker(on);
  await choosing;
  expect(focus.getStudyFocusSnapshot().enabled).toBe(false);
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: 'same', deadline: null });
});

test('turning off releases through the plugin and does not ask permission', async () => {
  mock.sync.mockResolvedValueOnce(on);
  await focus.syncStudyFocus('student', 10000);
  await focus.setStudyFocusEnabled(false);
  expect(mock.setEnabled).toHaveBeenCalledWith({ owner: 'student', enabled: false });
  expect(mock.configure).not.toHaveBeenCalled();
  expect(focus.getStudyFocusSnapshot().active).toBe(false);
});

test('a missing selection opens the picker before enabling', async () => {
  mock.sync.mockResolvedValueOnce({ ...off, selectionCount: 0 });
  await focus.syncStudyFocus('student', null);
  await focus.setStudyFocusEnabled(true);
  expect(mock.configure).toHaveBeenCalledOnce();
  expect(mock.setEnabled).not.toHaveBeenCalled();
});

test('a failed turn-off stays visible instead of being overwritten by an automatic resync', async () => {
  mock.sync.mockResolvedValueOnce(on);
  await focus.syncStudyFocus('student', 10000);
  mock.setEnabled.mockRejectedValueOnce(new Error('bridge unavailable'));
  await focus.setStudyFocusEnabled(false);
  expect(focus.getStudyFocusSnapshot().error).toContain('Could not change');
  expect(focus.getStudyFocusSnapshot().busy).toBe(false);
  expect(mock.sync).toHaveBeenCalledTimes(1);
});

test('denial or picker failure leaves a useful error and clears busy state', async () => {
  await focus.syncStudyFocus('student', null);
  mock.configure.mockRejectedValueOnce(new Error('denied'));
  await focus.configureStudyFocus();
  expect(focus.getStudyFocusSnapshot()).toMatchObject({ active: false, enabled: false, busy: false });
  expect(focus.getStudyFocusSnapshot().error).toContain('not enabled');
});

test('monitoring failure never claims apps are blocked, and a successful retry clears the error', async () => {
  mock.sync.mockRejectedValueOnce(new Error('too many intervals'));
  await focus.syncStudyFocus('student', 10000);
  expect(focus.getStudyFocusSnapshot().active).toBe(false);
  expect(focus.getStudyFocusSnapshot().error).toContain('Could not confirm');
  mock.sync.mockResolvedValueOnce(on);
  await focus.syncStudyFocus('student', 10000);
  expect(focus.getStudyFocusSnapshot()).toMatchObject({ active: true, error: null });
});

test('session hook refreshes on return and releases on unmount', async () => {
  const { useStudyFocusSession } = await import('../hooks/useStudyFocus');
  type Session = Parameters<typeof useStudyFocusSession>[0];
  const session = { phase: 'active', openEnded: false, startedAt: 1000, totalDuration: 1500, endsAt: 1_501_000 } as Session;
  const rendered = renderHook(({ value }) => useStudyFocusSession(value, 'student'), { initialProps: { value: session } });
  await act(async () => {});
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: 'student', deadline: 1_501_000 });
  await act(async () => { document.dispatchEvent(new Event('visibilitychange')); });
  expect(mock.sync).toHaveBeenCalledTimes(2);
  await act(async () => { rendered.rerender({ value: { ...session, phase: 'paused' } }); });
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: 'student', deadline: null });
  await act(async () => { rendered.unmount(); });
  expect(mock.sync).toHaveBeenLastCalledWith({ owner: null, deadline: null });
});

test('auth restoration does not erase the native selection before the student is known', async () => {
  const { useStudyFocusSession } = await import('../hooks/useStudyFocus');
  type Session = Parameters<typeof useStudyFocusSession>[0];
  const session = { phase: 'active', openEnded: false, startedAt: 1000, totalDuration: 1500, endsAt: 1_501_000 } as Session;
  const rendered = renderHook(({ uid, ready }) => useStudyFocusSession(session, uid, ready), {
    initialProps: { uid: undefined as string | undefined, ready: false },
  });
  await act(async () => {});
  expect(mock.sync).not.toHaveBeenCalled();
  await act(async () => { rendered.rerender({ uid: 'restored-student', ready: true }); });
  expect(mock.sync).toHaveBeenCalledTimes(1);
  expect(mock.sync).toHaveBeenCalledWith({ owner: 'restored-student', deadline: 1_501_000 });
});
