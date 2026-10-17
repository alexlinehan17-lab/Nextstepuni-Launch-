/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The study timer notification as the student sees it: is it available on this
 * device, is it on, and should the study room offer it. The choice is saved with
 * the student's settings (settings/{uid}, so it follows them between devices);
 * the permission belongs to this device and is asked for only after a tap.
 */

import { useCallback, useSyncExternalStore } from 'react';
import { useSettingsContext } from '../contexts/SettingsContext';
import {
  getPermissionSnapshot,
  notificationPreference,
  notificationSettingsHint,
  requestNotificationPermission,
  subscribePermission,
  type NotificationPermission,
  type PermissionSnapshot,
} from '../services/notifications';

const UNAVAILABLE: PermissionSnapshot = { support: 'none', permission: 'unsupported', checked: true };

export function useStudyNotifications() {
  const device = useSyncExternalStore(subscribePermission, getPermissionSnapshot, () => UNAVAILABLE);
  const context = useSettingsContext();
  const preferences = context?.settings.notifications;
  const preference = notificationPreference(preferences, 'studyTimer');
  const available = Boolean(context) && device.support !== 'none';
  const enabled = available && preference === true && device.permission === 'granted';

  const setPreference = useCallback((value: boolean) => {
    context?.updateSetting('notifications', { ...preferences, studyTimer: value });
  }, [context, preferences]);

  /** Saves the choice, then asks the device if it has not been asked before. */
  const turnOn = useCallback(async (): Promise<NotificationPermission> => {
    setPreference(true);
    return device.permission === 'granted' ? 'granted' : requestNotificationPermission();
  }, [device.permission, setPreference]);

  const turnOff = useCallback(() => setPreference(false), [setPreference]);

  return {
    available,
    enabled,
    preference,
    permission: device.permission,
    /** They said yes, but the device says no: explain how to fix it. */
    blocked: available && preference === true && device.permission === 'denied',
    /**
     * The room asks once: not yet answered here, or chosen on another device
     * whose permission does not carry over. Never when the device has refused.
     */
    shouldOffer: available && device.checked && device.permission !== 'denied'
      && (preference === undefined || (preference === true && device.permission === 'prompt')),
    hint: notificationSettingsHint(device.support),
    turnOn,
    turnOff,
  };
}
