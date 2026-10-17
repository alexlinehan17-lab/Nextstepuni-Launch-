/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your study time is up": one local notification per timed session, kept in
 * step with the session (start, pause, resume, keep going, finish, sign-out),
 * asked for in the study room and never on launch (Oct 2026).
 */

import React, { useState } from 'react';
import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { StudySessionProvider, useSharedStudySession } from '@/contexts/StudySessionContext';
import { SettingsContext, useSettingsContext } from '@/contexts/SettingsContext';
import StudyNotifyOffer from '@/components/study/StudyNotifyOffer';
import YourSetupView from '@/components/setup/YourSetupView';
import {
  NOTICE_IDS,
  notificationSupport,
  onNotificationOpen,
  resetNotificationsForTests,
} from '@/services/notifications';
import { planStudyNotice, studyActivityState, studyTimerCopy, type StudyTimerSnapshot } from '@/services/studyTimerAlerts';
import type { NotificationPreferences, UserSettings } from '@/types';
import type * as CapacitorCore from '@capacitor/core';

const native = vi.hoisted(() => ({
  platform: 'ios' as 'ios' | 'android' | 'web',
  display: 'granted' as 'granted' | 'denied' | 'prompt',
  exact: 'granted' as 'granted' | 'denied',
  api: {} as Record<string, ReturnType<typeof vi.fn>>,
}));

vi.mock('@capacitor/core', async original => {
  const actual = await original<typeof CapacitorCore>();
  return {
    ...actual,
    Capacitor: {
      ...actual.Capacitor,
      isNativePlatform: () => native.platform !== 'web',
      getPlatform: () => native.platform,
      isPluginAvailable: () => native.platform !== 'web',
    },
  };
});
vi.mock('@capacitor/local-notifications', () => ({ LocalNotifications: native.api }));
vi.mock('@/firebase', () => ({ db: {} }));
const progress = vi.hoisted(() => ({
  studySessions: [], progressLoaded: true, updateDemoProgress: () => undefined,
  addStudySession: () => undefined, reloadProgress: () => undefined, rawProgressDoc: {},
}));
vi.mock('@/contexts/ProgressContext', () => ({ useProgress: () => progress }));
vi.mock('@/components/NotificationBell', () => ({ default: () => null }));

const UID = 'student-1';
const MINUTE = 60_000;
const NOW = new Date('2026-10-14T16:00:00Z').getTime(); // 17:00 in Dublin
const BASE_SETTINGS: UserSettings = { language: 'en', avatar: '', darkMode: false, cardStyle: 'default', defaultWorkMinutes: 25 };

function resetApi() {
  // Same object the mock handed out; only its methods are replaced.
  Object.assign(native.api, {
    checkPermissions: vi.fn(async () => ({ display: native.display })),
    requestPermissions: vi.fn(async () => ({ display: native.display })),
    schedule: vi.fn(async () => ({ notifications: [{ id: NOTICE_IDS.studyTimer }] })),
    cancel: vi.fn(async () => undefined),
    removeDeliveredNotificationsById: vi.fn(async () => undefined),
    createChannel: vi.fn(async () => undefined),
    checkExactNotificationSetting: vi.fn(async () => ({ exact_alarm: native.exact })),
    addListener: vi.fn(async () => ({ remove: vi.fn() })),
  });
}
const api = () => native.api;
const flush = () => act(async () => { for (let i = 0; i < 20; i++) await Promise.resolve(); });
const scheduled = () => api().schedule.mock.calls.map(([options]) => options.notifications[0]);

/** Settings with a real updateSetting, and a probe of what was saved. */
function SettingsHost({ preferences, children }: { preferences?: NotificationPreferences; children: React.ReactNode }) {
  const [settings, setSettings] = useState<UserSettings>({ ...BASE_SETTINGS, notifications: preferences });
  const updateSetting = <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => setSettings(current => ({ ...current, [key]: value }));
  return <SettingsContext.Provider value={{ settings, updateSetting, unlockedThemes: [], unlockedCardStyles: [] }}>{children}</SettingsContext.Provider>;
}
function SavedChoice() {
  const value = useSettingsContext()?.settings.notifications?.studyTimer;
  return <span aria-label="saved choice">{value === undefined ? 'unasked' : String(value)}</span>;
}

/** The session's controls, as buttons. */
function Controls() {
  const session = useSharedStudySession();
  if (!session) return null;
  return <>
    <p>phase:{session.phase}</p>
    <button onClick={() => session.startSession('Chemistry', 'practice', 25)}>Start 25</button>
    <button onClick={() => session.startSession('Chemistry', 'practice', 0, undefined, { openEnded: true })}>Start open-ended</button>
    <button onClick={session.pauseSession}>Pause</button>
    <button onClick={session.resumeSession}>Resume</button>
    <button onClick={() => session.extendSession(10)}>Keep going 10</button>
    <button onClick={() => session.endSession()}>End early</button>
    <button onClick={session.resetSession}>Saved</button>
    <button onClick={session.cancelSession}>Discard</button>
  </>;
}

function app({ uid = UID, roomOpen = false, preferences = { studyTimer: true } as NotificationPreferences | undefined, offer = false } = {}) {
  const tree = (props: { uid?: string; roomOpen?: boolean }) => (
    <SettingsHost preferences={preferences}>
      <StudySessionProvider uid={props.uid} userProgress={{}} allCourses={[]} roomOpen={props.roomOpen}>
        <Controls />
        {offer && <StudyNotifyOffer />}
        <SavedChoice />
      </StudySessionProvider>
    </SettingsHost>
  );
  const view = render(tree({ uid, roomOpen }));
  return { ...view, rerenderWith: (props: { uid?: string; roomOpen?: boolean }) => view.rerender(tree({ uid, roomOpen, ...props })) };
}

const click = (name: string | RegExp) => fireEvent.click(screen.getByRole('button', { name }));

let visibility: DocumentVisibilityState = 'visible';

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(NOW);
  native.platform = 'ios';
  native.display = 'granted';
  native.exact = 'granted';
  resetApi();
  resetNotificationsForTests();
  window.localStorage.clear();
  window.sessionStorage.clear();
  visibility = 'visible';
  Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => visibility });
});
afterEach(() => {
  vi.useRealTimers();
  Reflect.deleteProperty(window, 'Notification');
});

describe('The rules (pure)', () => {
  const running: StudyTimerSnapshot = {
    phase: 'active', subject: 'Irish', sessionType: 'revision', openEnded: false, endsAt: NOW + 25 * MINUTE,
    startedAt: NOW, plannedMinutes: 25, extendedMinutes: 0, elapsedSeconds: 0, totalDuration: 1500,
  };
  const on = { enabled: true, roomOpen: false };

  test('copy is short, specific and has no emoji', () => {
    expect(studyTimerCopy(running)).toEqual({
      title: 'Time’s up: Irish',
      body: 'That’s 25 minutes of Irish done. Tap to log it, or keep going.',
    });
    expect(studyTimerCopy({ ...running, extendedMinutes: 10 }).body).toBe('That’s 35 minutes of Irish in total. Tap to log it and collect your bonus.');
    const all = Object.values(studyTimerCopy(running)).join(' ');
    expect(all).not.toMatch(/\p{Extended_Pictographic}/u);
  });

  test('schedules once, then keeps the same notification', () => {
    const first = planStudyNotice(undefined, running, on);
    expect(first).toMatchObject({ action: 'schedule', notice: { at: NOW + 25 * MINUTE, showInForeground: true, route: 'study-session' } });
    expect(planStudyNotice(first.action === 'schedule' ? first.key : null, running, on)).toEqual({ action: 'keep' });
  });

  test('no banner on top of the study room’s own “Time’s up”', () => {
    expect(planStudyNotice(undefined, running, { enabled: true, roomOpen: true })).toMatchObject({ notice: { showInForeground: false } });
  });

  test('pause cancels; running out leaves it to fire; nothing when off or open-ended', () => {
    expect(planStudyNotice('k', { ...running, phase: 'paused', endsAt: null }, on)).toEqual({ action: 'cancel' });
    expect(planStudyNotice('k', { ...running, phase: 'complete', endsAt: null, elapsedSeconds: 1500 }, on)).toEqual({ action: 'keep' });
    expect(planStudyNotice('k', { ...running, phase: 'complete', endsAt: null, elapsedSeconds: 700 }, on)).toEqual({ action: 'cancel' });
    expect(planStudyNotice(undefined, running, { enabled: false, roomOpen: false })).toEqual({ action: 'cancel' });
    expect(planStudyNotice(null, { ...running, openEnded: true, endsAt: null }, on)).toEqual({ action: 'keep' });
  });

  test('the Live Activity state counts down, pauses with the time left, and says when time is up', () => {
    expect(studyActivityState(running)).toMatchObject({ phase: 'running', countsDown: true, endsAt: NOW + 25 * MINUTE, detail: '25 min · Revision' });
    expect(studyActivityState({ ...running, phase: 'paused', elapsedSeconds: 600 })).toMatchObject({ phase: 'paused', pausedSeconds: 900, endsAt: null });
    expect(studyActivityState({ ...running, phase: 'complete', elapsedSeconds: 1500 })).toMatchObject({ phase: 'done', doneLabel: 'Time’s up' });
    expect(studyActivityState({ ...running, openEnded: true, endsAt: null, plannedMinutes: 0, totalDuration: 14400 })).toMatchObject({ countsDown: false, detail: 'Open-ended · Revision' });
    expect(studyActivityState({ ...running, phase: 'idle' })).toBeNull();
  });
});

describe('Native: the session drives one scheduled notification', () => {
  test('start, pause, resume, run out, keep going, save', async () => {
    app();
    await flush();
    // Its first pass clears anything left from before a relaunch.
    expect(api().cancel).toHaveBeenCalledWith({ notifications: [{ id: NOTICE_IDS.studyTimer }] });
    expect(api().schedule).not.toHaveBeenCalled();

    click('Start 25');
    await flush();
    expect(scheduled()).toHaveLength(1);
    expect(scheduled()[0]).toMatchObject({
      id: NOTICE_IDS.studyTimer,
      title: 'Time’s up: Chemistry',
      body: 'That’s 25 minutes of Chemistry done. Tap to log it, or keep going.',
      extra: { route: 'study-session' },
      foreground: true,
    });
    expect(scheduled()[0].schedule.at).toEqual(new Date(NOW + 25 * MINUTE));
    expect(api().requestPermissions).not.toHaveBeenCalled();

    act(() => { vi.advanceTimersByTime(10 * MINUTE); });
    const cancelsBeforePause = api().cancel.mock.calls.length;
    click('Pause');
    await flush();
    expect(api().cancel.mock.calls.length).toBe(cancelsBeforePause + 1);
    expect(api().removeDeliveredNotificationsById).toHaveBeenLastCalledWith({ ids: [NOTICE_IDS.studyTimer] });

    act(() => { vi.advanceTimersByTime(5 * MINUTE); });
    click('Resume');
    await flush();
    expect(scheduled()).toHaveLength(2);
    expect(scheduled()[1].schedule.at).toEqual(new Date(NOW + 30 * MINUTE));

    // The clock rounds, so it can flip to "complete" just before the scheduled
    // time; that must not cancel the notification that is about to fire.
    const cancelsBeforeEnd = api().cancel.mock.calls.length;
    act(() => { vi.advanceTimersByTime(15 * MINUTE); });
    await flush();
    expect(screen.getByText('phase:complete')).toBeInTheDocument();
    expect(api().cancel.mock.calls.length).toBe(cancelsBeforeEnd);

    click('Keep going 10');
    await flush();
    expect(scheduled()).toHaveLength(3);
    expect(scheduled()[2]).toMatchObject({ title: 'Extra time done: Chemistry' });
    expect(scheduled()[2].schedule.at).toEqual(new Date(NOW + 40 * MINUTE));

    act(() => { vi.advanceTimersByTime(10 * MINUTE); });
    await flush();
    const cancelsBeforeSave = api().cancel.mock.calls.length;
    click('Saved');
    await flush();
    // Logged: the delivered "Time's up" is cleared off the screen too.
    expect(api().cancel.mock.calls.length).toBe(cancelsBeforeSave + 1);
    expect(scheduled()).toHaveLength(3);
  });

  test('ending early or discarding cancels it', async () => {
    app();
    click('Start 25');
    await flush();
    act(() => { vi.advanceTimersByTime(6 * MINUTE); });
    const before = api().cancel.mock.calls.length;
    click('End early');
    await flush();
    expect(api().cancel.mock.calls.length).toBe(before + 1);

    click('Discard');
    click('Start 25');
    await flush();
    const again = api().cancel.mock.calls.length;
    click('Discard');
    await flush();
    expect(api().cancel.mock.calls.length).toBe(again + 1);
  });

  test('leaving or opening the study room moves the banner rule, not the time', async () => {
    const view = app({ roomOpen: true });
    click('Start 25');
    await flush();
    expect(scheduled()[0].foreground).toBe(false);
    view.rerenderWith({ roomOpen: false });
    await flush();
    expect(scheduled()).toHaveLength(2);
    expect(scheduled()[1]).toMatchObject({ foreground: true });
    expect(scheduled()[1].schedule.at).toEqual(scheduled()[0].schedule.at);
  });

  test('signing out cancels it, and the next student starts with nothing scheduled', async () => {
    const view = app();
    click('Start 25');
    await flush();
    const before = api().cancel.mock.calls.length;
    view.rerenderWith({ uid: undefined });
    await flush();
    expect(api().cancel.mock.calls.length).toBe(before + 1);

    view.rerenderWith({ uid: 'student-2' });
    await flush();
    expect(api().cancel.mock.calls.length).toBe(before + 2);
    expect(scheduled()).toHaveLength(1);
  });

  test('the sign-out wipe cancels it even without a React update', async () => {
    window.dispatchEvent(new Event('nextstepuni:session-cleared'));
    await flush();
    expect(api().cancel).toHaveBeenCalledWith({ notifications: [{ id: NOTICE_IDS.studyTimer }] });
  });

  test('open-ended sessions, a student who said no, and a missing permission get nothing', async () => {
    app();
    click('Start open-ended');
    await flush();
    expect(api().schedule).not.toHaveBeenCalled();
  });

  test('turned off: nothing is scheduled', async () => {
    app({ preferences: { studyTimer: false } });
    click('Start 25');
    await flush();
    expect(api().schedule).not.toHaveBeenCalled();
  });

  test('never prompts by itself: no permission, no schedule and no system prompt', async () => {
    native.display = 'prompt';
    app();
    click('Start 25');
    await flush();
    expect(api().schedule).not.toHaveBeenCalled();
    expect(api().requestPermissions).not.toHaveBeenCalled();
  });

  test('Android: a channel that can pop up, and no trip to the Alarms screen', async () => {
    native.platform = 'android';
    native.exact = 'denied';
    app();
    click('Start 25');
    await flush();
    expect(api().createChannel).toHaveBeenCalledWith(expect.objectContaining({ id: 'study-timer', importance: 4 }));
    expect(scheduled()[0]).toMatchObject({ channelId: 'study-timer', isExactNotification: false });
  });

  test('a tap opens the study room, even one that launched the app', async () => {
    let tap: ((action: unknown) => void) | undefined;
    api().addListener.mockImplementation(async (_event: string, handler: (action: unknown) => void) => { tap = handler; return { remove: vi.fn() }; });
    const opened: string[] = [];
    const stop = onNotificationOpen(route => opened.push(route));
    await flush();
    tap?.({ actionId: 'tap', notification: { id: NOTICE_IDS.studyTimer, extra: { route: 'study-session' } } });
    tap?.({ actionId: 'dismiss', notification: { id: NOTICE_IDS.studyTimer, extra: { route: 'study-session' } } });
    expect(opened).toEqual(['study-session']);
    stop();
    tap?.({ actionId: 'tap', notification: { id: NOTICE_IDS.studyTimer, extra: { route: 'study-session' } } });
    const late: string[] = [];
    onNotificationOpen(route => late.push(route));
    expect(late).toEqual(['study-session']);
  });
});

describe('Asked in context, once', () => {
  test('the study room offers it; a tap asks the device, saves the choice and schedules', async () => {
    native.display = 'prompt';
    api().requestPermissions.mockImplementation(async () => { native.display = 'granted'; return { display: 'granted' }; });
    app({ preferences: undefined, offer: true });
    await flush();
    // Never on launch: nothing is asked before a session starts.
    expect(screen.queryByRole('button', { name: /Notify me when time’s up/ })).not.toBeInTheDocument();
    expect(api().requestPermissions).not.toHaveBeenCalled();

    click('Start 25');
    await flush();
    click(/Notify me when time’s up/);
    await flush();
    expect(api().requestPermissions).toHaveBeenCalledTimes(1);
    expect(screen.getByRole('status')).toHaveTextContent('We’ll let you know at 17:25.');
    expect(screen.getByLabelText('saved choice')).toHaveTextContent('true');
    expect(scheduled()).toHaveLength(1);

    act(() => { vi.advanceTimersByTime(7000); });
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  test('“Not now” is remembered and the room stops asking', async () => {
    native.display = 'prompt';
    app({ preferences: undefined, offer: true });
    click('Start 25');
    await flush();
    click('Not now');
    expect(screen.getByLabelText('saved choice')).toHaveTextContent('false');
    expect(screen.queryByRole('button', { name: /Notify me/ })).not.toBeInTheDocument();
    expect(api().requestPermissions).not.toHaveBeenCalled();
  });

  test('a refusal explains how to turn it back on', async () => {
    native.display = 'prompt';
    api().requestPermissions.mockImplementation(async () => { native.display = 'denied'; return { display: 'denied' }; });
    app({ preferences: undefined, offer: true });
    click('Start 25');
    await flush();
    click(/Notify me when time’s up/);
    await flush();
    expect(screen.getByRole('status')).toHaveTextContent('open Settings, then Notifications, then NextStepUni');
    click('OK');
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  test('not offered for open-ended sessions or once already on', async () => {
    native.display = 'prompt';
    app({ preferences: undefined, offer: true });
    click('Start open-ended');
    await flush();
    expect(screen.queryByRole('button', { name: /Notify me/ })).not.toBeInTheDocument();
  });
});

describe('Web', () => {
  class FakeNotification {
    static permission: NotificationPermission = 'granted';
    static requestPermission = vi.fn(async () => FakeNotification.permission);
    static shown: FakeNotification[] = [];
    onclick: (() => void) | null = null;
    close = vi.fn();
    constructor(public title: string, public options: NotificationOptions) { FakeNotification.shown.push(this); }
  }
  beforeEach(() => {
    native.platform = 'web';
    FakeNotification.shown = [];
    FakeNotification.permission = 'granted';
    Object.defineProperty(window, 'Notification', { configurable: true, writable: true, value: FakeNotification });
  });

  test('fires when time is up while the page is hidden, and a click opens the room', async () => {
    app({ roomOpen: true });
    const opened: string[] = [];
    onNotificationOpen(route => opened.push(route));
    click('Start 25');
    await flush();
    visibility = 'hidden';
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    expect(FakeNotification.shown).toHaveLength(1);
    expect(FakeNotification.shown[0].title).toBe('Time’s up: Chemistry');
    FakeNotification.shown[0].onclick?.();
    expect(opened).toEqual(['study-session']);
  });

  test('stays quiet while the student is looking at the study room', async () => {
    app({ roomOpen: true });
    click('Start 25');
    await flush();
    act(() => { vi.advanceTimersByTime(25 * MINUTE); });
    expect(FakeNotification.shown).toHaveLength(0);
  });

  test('pausing cancels the timer', async () => {
    app();
    click('Start 25');
    await flush();
    click('Pause');
    await flush();
    visibility = 'hidden';
    act(() => { vi.advanceTimersByTime(60 * MINUTE); });
    expect(FakeNotification.shown).toHaveLength(0);
  });
});

describe('Where it is offered', () => {
  const ua = (value: string, touch = 0) => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue(value);
    Object.defineProperty(navigator, 'maxTouchPoints', { configurable: true, get: () => touch });
  };
  afterEach(() => vi.restoreAllMocks());

  test('iPhone and iPad Safari tabs have no Notification API: not offered', () => {
    native.platform = 'web';
    ua('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/26.0 Safari/605.1.15', 5);
    expect(notificationSupport()).toBe('none');
    // A Home Screen web app has the API but is suspended in the background.
    Object.defineProperty(window, 'Notification', { configurable: true, writable: true, value: class {} });
    expect(notificationSupport()).toBe('none');
  });

  test('desktop browsers with the API, and the native apps', () => {
    native.platform = 'web';
    ua('Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/141.0 Safari/537.36');
    Object.defineProperty(window, 'Notification', { configurable: true, writable: true, value: class {} });
    expect(notificationSupport()).toBe('web');
    native.platform = 'ios';
    expect(notificationSupport()).toBe('native');
  });

  test('Your setup shows the switch only where it can work', async () => {
    const props = {
      profile: null, northStar: null, darkMode: false, onBack: vi.fn(), onFinishSetup: vi.fn(), onEditSubjects: vi.fn(),
      onEditNorthStar: vi.fn(), onOpenSettings: vi.fn(), onOpenPlanner: vi.fn(), onSetDarkMode: vi.fn(),
    };
    native.display = 'denied';
    const view = render(<SettingsHost preferences={{ studyTimer: true }}><YourSetupView {...props} /></SettingsHost>);
    await flush();
    expect(screen.getByRole('tablist', { name: 'Study timer notifications' })).toBeInTheDocument();
    expect(screen.getByText(/open Settings, then Notifications, then NextStepUni/)).toBeInTheDocument();
    view.unmount();

    native.platform = 'web';
    resetNotificationsForTests();
    render(<SettingsHost><YourSetupView {...props} /></SettingsHost>);
    expect(screen.queryByRole('tablist', { name: 'Study timer notifications' })).not.toBeInTheDocument();
  });
});
