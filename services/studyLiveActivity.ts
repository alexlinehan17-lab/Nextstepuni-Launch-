/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The study timer on the iPhone Lock Screen and in the Dynamic Island (an iOS
 * Live Activity). A thin, typed wrapper over the app's own native plugin
 * (ios/App/App/StudyLiveActivityPlugin.swift); on the web and on Android every
 * call is a no-op.
 *
 * sync(state) is idempotent: it starts the activity, updates it, or (with
 * null) ends it, so the caller just says what should be showing.
 */

import { Capacitor, registerPlugin } from '@capacitor/core';
import { logError } from '../utils/logError';
import { openFromDevice } from './notifications';
import type { StudyActivityState } from './studyTimerAlerts';

interface StudyLiveActivityPlugin {
  isAvailable(): Promise<{ available: boolean }>;
  sync(options: { state: StudyActivityState | null }): Promise<{ active: boolean }>;
  endAll(): Promise<void>;
  addListener(event: 'open', listener: (event: { route?: string }) => void): Promise<{ remove: () => Promise<void> }>;
}

const StudyLiveActivity = registerPlugin<StudyLiveActivityPlugin>('StudyLiveActivity');

/** iOS app with the plugin registered (iOS 16.1+ is checked natively). */
export const liveActivitySupported = (): boolean =>
  Capacitor.getPlatform() === 'ios' && Capacitor.isPluginAvailable('StudyLiveActivity');

/** Whether this device will show it (iOS 16.1+, Live Activities allowed). */
export async function liveActivityAvailable(): Promise<boolean> {
  if (!liveActivitySupported()) return false;
  try {
    return (await StudyLiveActivity.isAvailable()).available;
  } catch {
    return false;
  }
}

let queue: Promise<unknown> = Promise.resolve();

/** Show this state on the Lock Screen, or end the activity with null. */
export function syncStudyActivity(state: StudyActivityState | null): Promise<void> {
  if (!liveActivitySupported()) return Promise.resolve();
  const run = queue.then(() => StudyLiveActivity.sync({ state }))
    .then(() => undefined)
    .catch(error => logError('studyLiveActivity.sync', error));
  queue = run;
  return run;
}

export function endStudyActivities(): Promise<void> {
  return syncStudyActivity(null);
}

let listening = false;
/** Tapping the Live Activity opens the study room, like the notification. */
function listenForTaps(): void {
  if (listening || !liveActivitySupported()) return;
  listening = true;
  void StudyLiveActivity.addListener('open', event => {
    if (event.route === 'study-session') openFromDevice('study-session');
  }).catch(error => {
    listening = false;
    logError('studyLiveActivity.listen', error);
  });
}

if (typeof window !== 'undefined') {
  listenForTaps();
  // Sign-out, and a signed-out launch: no timer left on a shared iPad's Lock Screen.
  window.addEventListener('nextstepuni:session-cleared', () => { void endStudyActivities(); });
}
