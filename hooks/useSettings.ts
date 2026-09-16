/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type UserSettings } from '../types';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const STORAGE_KEY = 'nextstep-settings';

// The profile owns the avatar. Device preferences must not replace the
// character selected at signup, especially on a shared school computer.
const DEFAULT_SETTINGS: UserSettings = {
  language: 'en',
  avatar: '',
  darkMode: false,
  cardStyle: 'default',
  defaultWorkMinutes: 25,
  showDashboard: false,
};

function readLocalSettings(uid?: string): Partial<UserSettings> {
  try {
    const scoped = uid && localStorage.getItem(`${STORAGE_KEY}:${uid}`);
    if (scoped) return JSON.parse(scoped);
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const { avatar: _previousAccountAvatar, ...preferences } = JSON.parse(raw);
      return preferences;
    }
  } catch (err) { console.error('Failed to read local settings:', err); }
  return {};
}

function initialSettings(uid?: string, userAvatar?: string): UserSettings {
  const local = readLocalSettings(uid);
  return {
    ...DEFAULT_SETTINGS,
    ...local,
    avatar: uid === DEMO_STUDENT_UID
      ? local.avatar || userAvatar || ''
      : userAvatar || local.avatar || '',
  };
}

function writeLocalSettings(settings: UserSettings, uid?: string) {
  localStorage.setItem(uid ? `${STORAGE_KEY}:${uid}` : STORAGE_KEY, JSON.stringify(settings));
  localStorage.setItem('nextstep-language', settings.language);
}

export function useSettings(uid?: string, userAvatar?: string, onAvatarChange?: (avatar: string) => void) {
  const [state, setState] = useState(() => ({ uid, settings: initialSettings(uid, userAvatar) }));
  const current = useRef(state);
  const preferredAvatar = useRef(userAvatar);
  const [isLoaded, setIsLoaded] = useState(false);
  const settings = state.uid === uid ? state.settings : initialSettings(uid, userAvatar);

  const replaceSettings = useCallback((owner: string | undefined, next: UserSettings) => {
    current.current = { uid: owner, settings: next };
    setState(current.current);
  }, []);

  // A completed signup can arrive after the initial auth fallback. Replace
  // that fallback even when settings already contain a legacy character.
  useEffect(() => {
    preferredAvatar.current = userAvatar;
    if (current.current.uid === uid && userAvatar) {
      const avatar = uid === DEMO_STUDENT_UID ? current.current.settings.avatar || userAvatar : userAvatar;
      replaceSettings(uid, { ...current.current.settings, avatar });
    }
  }, [uid, userAvatar, replaceSettings]);

  useEffect(() => {
    let cancelled = false;
    replaceSettings(uid, initialSettings(uid, preferredAvatar.current));
    setIsLoaded(false);
    if (!uid || uid === DEMO_STUDENT_UID) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const settingsDoc = await getDoc(doc(db, 'settings', uid));
        if (cancelled) return;
        if (settingsDoc.exists()) {
          const firestoreSettings = settingsDoc.data() as Partial<UserSettings>;
          const merged = {
            ...current.current.settings,
            ...firestoreSettings,
            // This ref also tracks a selection made while the read was pending.
            avatar: preferredAvatar.current || firestoreSettings.avatar || current.current.settings.avatar,
          };
          replaceSettings(uid, merged);
          writeLocalSettings(merged, uid);
        }
      } catch (err) {
        console.error('Failed to load settings from Firestore:', err);
      }
      if (!cancelled) setIsLoaded(true);
    };

    void load();
    return () => { cancelled = true; };
  }, [uid, replaceSettings]);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', settings.darkMode);
  }, [settings.darkMode]);

  useEffect(() => {
    document.body.dataset.cardStyle = settings.cardStyle || 'default';
  }, [settings.cardStyle]);

  const updateSetting = useCallback(<K extends keyof UserSettings>(key: K, value: UserSettings[K]) => {
    if (key === 'darkMode') {
      document.documentElement.classList.toggle('dark', Boolean(value));
    } else if (key === 'cardStyle') {
      document.body.dataset.cardStyle = (value as string) || 'default';
    }

    const previous = current.current.uid === uid ? current.current.settings : initialSettings(uid, preferredAvatar.current);
    const next = { ...previous, [key]: value };
    if (key === 'avatar') preferredAvatar.current = value as string;
    replaceSettings(uid, next);
    writeLocalSettings(next, uid);

    // Keep every profile consumer, including My Island, in sync immediately.
    if (key === 'avatar') onAvatarChange?.(value as string);

    if (uid && uid !== DEMO_STUDENT_UID) {
      setDoc(doc(db, 'settings', uid), next, { merge: true }).catch(err =>
        console.error('Failed to save settings:', err)
      );
      if (key === 'avatar') {
        setDoc(doc(db, 'users', uid), { avatar: value }, { merge: true }).catch(err =>
          console.error('Failed to update user avatar:', err)
        );
      }
    }
  }, [uid, onAvatarChange, replaceSettings]);

  return { settings, updateSetting, isLoaded: state.uid === uid && isLoaded };
}
