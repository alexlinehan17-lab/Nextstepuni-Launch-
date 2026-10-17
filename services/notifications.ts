/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Local notifications for every platform, in one place. The first one is the
 * study timer's "your time is up" (a student said the timer is pointless if they
 * have to unlock the iPad to check it; another wanted to know when time was up
 * while working in their notes app, Oct 2026). Later notifications plug in by
 * adding an id to NOTICE_IDS and a key to NotificationPreferences.
 *
 *   native (iOS, Android) @capacitor/local-notifications. The operating system
 *                         delivers it at the set time, even if the app has been
 *                         closed.
 *   web                   The browser Notification API, fired from this page
 *                         while it is still open. No server push.
 *   none                  Nothing is offered. iPhone and iPad Safari tabs have no
 *                         Notification API, and a Home Screen web app is
 *                         suspended in the background, so its timer could never
 *                         fire either.
 *
 * Nothing here asks for permission on its own. The student asks, by tapping
 * "Notify me when time's up" or a settings switch (hooks/useStudyNotifications).
 */

import { Capacitor } from '@capacitor/core';
import { LocalNotifications } from '@capacitor/local-notifications';
import { logError } from '../utils/logError';
import type { NotificationPreferences } from '../types';

export type NotificationSupport = 'native' | 'web' | 'none';
export type NotificationPermission = 'granted' | 'denied' | 'prompt' | 'unsupported';
export type NotificationKind = keyof NotificationPreferences;
/** Where tapping a notification takes the student. */
export type NotificationRoute = 'study-session';

/** Stable ids, so a reschedule replaces the earlier notification. */
export const NOTICE_IDS = {
  studyTimer: 4201,
} as const satisfies Record<NotificationKind, number>;

export interface LocalNotice {
  id: number;
  title: string;
  body: string;
  /** Wall-clock time to show it, in milliseconds. */
  at: number;
  route: NotificationRoute;
  /**
   * Show it while the app is open and in front. False when the student is
   * already looking at what the notification would tell them.
   */
  showInForeground: boolean;
}

/** Android channel for the study timer: important enough to pop up. */
const STUDY_CHANNEL_ID = 'study-timer';
const WEB_ICON = '/icons/north-star-icon-192x192.png';
const SESSION_CLEARED_EVENT = 'nextstepuni:session-cleared';

// ── Platform ───────────────────────────────────────────────

/** iPhone, iPod or iPad (which reports itself as a Mac with touch). */
function isAppleMobileWeb(): boolean {
  if (typeof navigator === 'undefined') return false;
  if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) return true;
  return /Macintosh/i.test(navigator.userAgent) && navigator.maxTouchPoints > 1;
}

export function notificationSupport(): NotificationSupport {
  if (Capacitor.isNativePlatform()) {
    return Capacitor.isPluginAvailable('LocalNotifications') ? 'native' : 'none';
  }
  if (typeof window === 'undefined' || typeof window.Notification === 'undefined') return 'none';
  return isAppleMobileWeb() ? 'none' : 'web';
}

/** One line on turning notifications back on, for the platform in hand. */
export function notificationSettingsHint(support: NotificationSupport = notificationSupport()): string {
  if (support === 'native') {
    return Capacitor.getPlatform() === 'android'
      ? 'Notifications are off for NextStepUni. To turn them on, open Settings, then Apps, then NextStepUni, then Notifications.'
      : 'Notifications are off for NextStepUni. To turn them on, open Settings, then Notifications, then NextStepUni.';
  }
  return 'Notifications are blocked for this site. To turn them on, allow notifications for NextStepUni in your browser’s site settings.';
}

// ── Permission (a tiny store, so every screen agrees) ──────

export interface PermissionSnapshot {
  support: NotificationSupport;
  permission: NotificationPermission;
  /** False until the platform has been asked what the permission is. */
  checked: boolean;
}

let snapshot: PermissionSnapshot | null = null;
const permissionListeners = new Set<() => void>();

function initialSnapshot(): PermissionSnapshot {
  const support = notificationSupport();
  if (support === 'none') return { support, permission: 'unsupported', checked: true };
  if (support === 'web') return { support, permission: webPermission(), checked: true };
  return { support, permission: 'prompt', checked: false };
}

function webPermission(): NotificationPermission {
  const value = window.Notification.permission;
  return value === 'default' ? 'prompt' : value;
}

function setSnapshot(next: PermissionSnapshot): void {
  const current = getPermissionSnapshot();
  if (current.support === next.support && current.permission === next.permission && current.checked === next.checked) return;
  snapshot = next;
  permissionListeners.forEach(listener => listener());
}

export function getPermissionSnapshot(): PermissionSnapshot {
  if (!snapshot) snapshot = initialSnapshot();
  return snapshot;
}

function mapNativePermission(display: string): NotificationPermission {
  if (display === 'granted') return 'granted';
  if (display === 'denied') return 'denied';
  return 'prompt';
}

/** Ask the platform what the permission is now (it can change in Settings). */
export async function refreshNotificationPermission(): Promise<NotificationPermission> {
  const support = notificationSupport();
  let permission: NotificationPermission = 'unsupported';
  try {
    if (support === 'web') permission = webPermission();
    else if (support === 'native') permission = mapNativePermission((await LocalNotifications.checkPermissions()).display);
  } catch (error) {
    logError('notifications.checkPermission', error);
    permission = 'prompt';
  }
  setSnapshot({ support, permission, checked: true });
  return permission;
}

/** Shows the system prompt if the student has not answered it before. */
export async function requestNotificationPermission(): Promise<NotificationPermission> {
  const support = notificationSupport();
  let permission: NotificationPermission = 'unsupported';
  try {
    if (support === 'web') {
      const answer = await window.Notification.requestPermission();
      permission = answer === 'default' ? 'prompt' : answer;
    } else if (support === 'native') {
      permission = mapNativePermission((await LocalNotifications.requestPermissions()).display);
    }
  } catch (error) {
    logError('notifications.requestPermission', error);
    permission = support === 'none' ? 'unsupported' : 'prompt';
  }
  setSnapshot({ support, permission, checked: true });
  return permission;
}

let watchingVisibility = false;
export function subscribePermission(listener: () => void): () => void {
  permissionListeners.add(listener);
  if (!watchingVisibility && typeof document !== 'undefined') {
    // A student who turned notifications on in Settings comes back to a page
    // that should already know.
    watchingVisibility = true;
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') void refreshNotificationPermission();
    });
  }
  if (!getPermissionSnapshot().checked) void refreshNotificationPermission();
  return () => { permissionListeners.delete(listener); };
}

/** The student's choice for one kind. Undefined means not asked yet. */
export const notificationPreference = (
  preferences: NotificationPreferences | undefined,
  kind: NotificationKind,
): boolean | undefined => preferences?.[kind];

// ── Scheduling ─────────────────────────────────────────────

// Native calls are asynchronous; run them strictly in order, so a cancel can
// never land after the reschedule that followed it.
let queue: Promise<unknown> = Promise.resolve();
function serial<T>(task: () => Promise<T>): Promise<T> {
  const run = queue.then(task, task);
  queue = run.catch(() => undefined);
  return run;
}

let androidChannelReady: Promise<void> | null = null;
function ensureAndroidChannel(): Promise<void> {
  if (Capacitor.getPlatform() !== 'android') return Promise.resolve();
  androidChannelReady ??= LocalNotifications.createChannel({
    id: STUDY_CHANNEL_ID,
    name: 'Study timer',
    description: 'When your study time is up',
    importance: 4,
    visibility: 1,
  }).catch(error => {
    androidChannelReady = null;
    logError('notifications.createChannel', error);
  });
  return androidChannelReady;
}

/** Android only: exact alarms need a setting the student may not have granted. */
async function canScheduleExact(): Promise<boolean> {
  if (Capacitor.getPlatform() !== 'android') return true;
  try {
    return (await LocalNotifications.checkExactNotificationSetting()).exact_alarm === 'granted';
  } catch {
    return false;
  }
}

/**
 * Schedule (or reschedule) one notification. Never prompts: if permission has
 * not been granted it does nothing and resolves false.
 */
export function scheduleLocalNotice(notice: LocalNotice): Promise<boolean> {
  return serial(async () => {
    const support = notificationSupport();
    if (support === 'none' || notice.at <= Date.now()) return false;
    if (support === 'web') return scheduleWeb(notice);
    try {
      // Since 8.3, schedule() requests permission itself. Check first so the
      // system prompt only ever follows the student's own tap.
      if (mapNativePermission((await LocalNotifications.checkPermissions()).display) !== 'granted') return false;
      await clearNative(notice.id);
      await ensureAndroidChannel();
      // Without exact-alarm access Android would open the Alarms settings
      // screen on every schedule; fall back to an inexact alarm instead.
      const exact = await canScheduleExact();
      await LocalNotifications.schedule({
        notifications: [{
          id: notice.id,
          title: notice.title,
          body: notice.body,
          schedule: { at: new Date(notice.at), allowWhileIdle: true },
          extra: { route: notice.route },
          foreground: notice.showInForeground,
          channelId: STUDY_CHANNEL_ID,
          isExactNotification: exact,
          autoCancel: true,
        }],
      });
      return true;
    } catch (error) {
      logError('notifications.schedule', error);
      return false;
    }
  });
}

/** Cancel a pending notification and take a delivered one off the screen. */
export function cancelLocalNotice(id: number): Promise<void> {
  return serial(async () => {
    const support = notificationSupport();
    if (support === 'web') cancelWeb(id);
    else if (support === 'native') await clearNative(id).catch(error => logError('notifications.cancel', error));
  });
}

async function clearNative(id: number): Promise<void> {
  await LocalNotifications.cancel({ notifications: [{ id }] });
  await LocalNotifications.removeDeliveredNotificationsById({ ids: [id] });
}

// ── Web ────────────────────────────────────────────────────

interface WebEntry { timer?: number; shown?: Notification }
const webEntries = new Map<number, WebEntry>();

function scheduleWeb(notice: LocalNotice): boolean {
  cancelWeb(notice.id);
  if (webPermission() !== 'granted') return false;
  // One timer, not an interval: browsers throttle repeating timers in hidden
  // tabs far harder than a single one.
  const timer = window.setTimeout(() => fireWeb(notice), notice.at - Date.now());
  webEntries.set(notice.id, { timer });
  return true;
}

function fireWeb(notice: LocalNotice): void {
  const entry = webEntries.get(notice.id) ?? {};
  entry.timer = undefined;
  webEntries.set(notice.id, entry);
  if (webPermission() !== 'granted') return;
  if (document.visibilityState === 'visible' && !notice.showInForeground) return;
  const options = { body: notice.body, tag: `nextstepuni-${notice.id}`, icon: WEB_ICON };
  try {
    const shown = new window.Notification(notice.title, options);
    shown.onclick = () => {
      window.focus();
      shown.close();
      openFromDevice(notice.route);
    };
    entry.shown = shown;
  } catch {
    // Android browsers only show notifications through the service worker.
    void navigator.serviceWorker?.getRegistration()
      .then(registration => registration?.showNotification(notice.title, options))
      .catch(error => logError('notifications.webFallback', error));
  }
}

function cancelWeb(id: number): void {
  const entry = webEntries.get(id);
  if (!entry) return;
  if (entry.timer !== undefined) window.clearTimeout(entry.timer);
  entry.shown?.close();
  webEntries.delete(id);
}

// ── Taps ───────────────────────────────────────────────────

const openListeners = new Set<(route: NotificationRoute) => void>();
let pendingOpen: NotificationRoute | null = null;
let listeningForTaps = false;

/** Something on the device (a notification, the Live Activity) was tapped. */
export function openFromDevice(route: NotificationRoute): void {
  if (openListeners.size === 0) {
    pendingOpen = route;
    return;
  }
  openListeners.forEach(listener => listener(route));
}

const isRoute = (value: unknown): value is NotificationRoute => value === 'study-session';

/**
 * Called with the route when the student taps one of our notifications. A tap
 * that launched the app before anything subscribed is delivered on subscribe.
 */
export function onNotificationOpen(listener: (route: NotificationRoute) => void): () => void {
  openListeners.add(listener);
  if (!listeningForTaps && notificationSupport() === 'native') {
    listeningForTaps = true;
    void LocalNotifications.addListener('localNotificationActionPerformed', action => {
      if (action.actionId === 'dismiss') return;
      const route = (action.notification.extra as { route?: unknown } | undefined)?.route;
      if (isRoute(route)) openFromDevice(route);
    }).catch(error => {
      listeningForTaps = false;
      logError('notifications.listen', error);
    });
  }
  if (pendingOpen) {
    const route = pendingOpen;
    pendingOpen = null;
    listener(route);
  }
  return () => { openListeners.delete(listener); };
}

// ── Leaving a shared device ────────────────────────────────

/** Cancel everything this app schedules (sign-out, account change). */
export function cancelAllLocalNotices(): Promise<void> {
  return Promise.all(Object.values(NOTICE_IDS).map(id => cancelLocalNotice(id))).then(() => undefined);
}

if (typeof window !== 'undefined') {
  // Fired by clearLocalSessionData on sign-out and on a signed-out launch: the
  // next person on a school iPad must not get the last student's reminder.
  window.addEventListener(SESSION_CLEARED_EVENT, () => { void cancelAllLocalNotices(); });
}

/** Test seam: forget cached platform state between tests. */
export function resetNotificationsForTests(): void {
  snapshot = null;
  pendingOpen = null;
  listeningForTaps = false;
  androidChannelReady = null;
  queue = Promise.resolve();
  webEntries.forEach((_entry, id) => cancelWeb(id));
  openListeners.clear();
  permissionListeners.clear();
}
