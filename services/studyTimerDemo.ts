/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Simulator check for the study timer's device alerts, without signing in to a
 * real account. It only runs in a DEBUG native build launched with
 *
 *   xcrun simctl launch booted com.nextstepuni.app \
 *     -NSUStudyTimerDemo '{"notifyIn":45,"remaining":1110,"mode":"running","roomOpen":false}'
 *
 * (NextStepBridgeViewController injects the setting; Release builds compile
 * that out and report Capacitor.DEBUG false, so this never runs for students).
 * It drives the same services the study session uses: a sample "Time's up"
 * notification after `notifyIn` seconds and a sample Live Activity
 * (`mode`: running, paused, countup or done).
 */

import { Capacitor } from '@capacitor/core';
import { onNotificationOpen, requestNotificationPermission, scheduleLocalNotice } from './notifications';
import { liveActivityAvailable, syncStudyActivity } from './studyLiveActivity';
import { studyActivityState, studyTimerNotice, type StudyTimerSnapshot } from './studyTimerAlerts';

interface DemoOptions {
  notifyIn?: number;
  remaining?: number;
  mode?: 'running' | 'paused' | 'countup' | 'done';
  subject?: string;
  /** As if the student were looking at the study room: no banner in front. */
  roomOpen?: boolean;
}

declare global {
  interface Window { __NSU_STUDY_TIMER_DEMO__?: DemoOptions }
}

async function runDemo(options: DemoOptions): Promise<void> {
  const now = Date.now();
  const total = 25 * 60;
  const remaining = Math.max(1, Math.min(total, options.remaining ?? 18 * 60 + 30));
  const elapsed = total - remaining;
  const mode = options.mode ?? 'running';
  const countup = mode === 'countup';
  const snapshot: StudyTimerSnapshot = {
    phase: mode === 'paused' ? 'paused' : mode === 'done' ? 'complete' : 'active',
    subject: options.subject ?? 'Biology',
    sessionType: 'practice',
    openEnded: countup,
    endsAt: countup ? null : now + remaining * 1000,
    startedAt: now - elapsed * 1000,
    plannedMinutes: countup ? 0 : 25,
    extendedMinutes: 0,
    elapsedSeconds: mode === 'done' ? total : elapsed,
    totalDuration: countup ? 240 * 60 : total,
  };
  console.info('[studyTimerDemo] plugins', JSON.stringify({
    LocalNotifications: Capacitor.isPluginAvailable('LocalNotifications'),
    StudyLiveActivity: Capacitor.isPluginAvailable('StudyLiveActivity'),
    SignInWithApple: Capacitor.isPluginAvailable('SignInWithApple'),
  }));

  const available = await liveActivityAvailable();
  await syncStudyActivity(studyActivityState(snapshot));
  console.info('[studyTimerDemo] live activity', JSON.stringify({ mode, available }));

  if (options.notifyIn) {
    const permission = await requestNotificationPermission();
    const notice = studyTimerNotice({ ...snapshot, phase: 'active', openEnded: false, endsAt: now + options.notifyIn * 1000, plannedMinutes: 25 },
      { enabled: true, roomOpen: Boolean(options.roomOpen) });
    const scheduled = notice ? await scheduleLocalNotice(notice) : false;
    console.info('[studyTimerDemo] notification', JSON.stringify({ permission, scheduled, inSeconds: options.notifyIn, showInForeground: notice?.showInForeground }));
  }
}

export function installStudyTimerDemo(): void {
  if (typeof window === 'undefined' || !Capacitor.isNativePlatform() || !Capacitor.DEBUG) return;
  const options = window.__NSU_STUDY_TIMER_DEMO__;
  if (!options) return;
  // Taps on the notification or the Live Activity, for the simulator log.
  onNotificationOpen(route => console.info('[studyTimerDemo] opened', route));
  // A signed-out launch clears the device's alerts (sign-out hygiene), so run
  // just after that, or after a few seconds if it never comes.
  let started = false;
  const start = () => {
    if (started) return;
    started = true;
    void runDemo(options).catch(error => console.error('[studyTimerDemo]', error));
  };
  window.addEventListener('nextstepuni:session-cleared', () => window.setTimeout(start, 1500), { once: true });
  window.setTimeout(start, 8000);
}

installStudyTimerDemo();
