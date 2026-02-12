/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { UserSettings } from '../types';

const STORAGE_KEY = 'nextstep-settings';

const DEFAULT_SETTINGS: UserSettings = {
  language: 'en',
  avatar: '',
  darkMode: false,

  defaultWorkMinutes: 25,
};

function readLocalSettings(): Partial<UserSettings> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return {};
}

function writeLocalSettings(settings: UserSettings) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  localStorage.setItem('nextstep-language', settings.language);
}

export function useSettings(uid?: string, userAvatar?: string) {
  const [settings, setSettings] = useState<UserSettings>(() => {
    const local = readLocalSettings();
    return { ...DEFAULT_SETTINGS, avatar: userAvatar || '', ...local };
  });
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from Firestore on mount (Firestore wins on conflict)
  useEffect(() => {
    if (!uid) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const settingsDoc = await getDoc(doc(db, 'settings', uid));
        if (settingsDoc.exists()) {
          const firestoreSettings = settingsDoc.data() as Partial<UserSettings>;
          setSettings(prev => {
            const merged = { ...prev, ...firestoreSettings };
            writeLocalSettings(merged);
            return merged;
          });
        }
      } catch (err) {
        console.error('Failed to load settings from Firestore:', err);
      }
      setIsLoaded(true);
    };

    load();
  }, [uid]);

  // Set avatar default when userAvatar becomes available
  useEffect(() => {
    if (userAvatar && !settings.avatar) {
      setSettings(prev => ({ ...prev, avatar: userAvatar }));
    }
  }, [userAvatar]);

  // Sync dark mode with document
  useEffect(() => {
    if (settings.darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [settings.darkMode]);

  const updateSetting = useCallback(<K extends keyof UserSettings>(key: K, value: UserSettings[K]) => {
    setSettings(prev => {
      const next = { ...prev, [key]: value };
      writeLocalSettings(next);

      // Persist to Firestore
      if (uid) {
        setDoc(doc(db, 'settings', uid), next, { merge: true }).catch(err =>
          console.error('Failed to save settings:', err)
        );

        // If avatar changed, also update users/{uid}.avatar
        if (key === 'avatar') {
          setDoc(doc(db, 'users', uid), { avatar: value }, { merge: true }).catch(err =>
            console.error('Failed to update user avatar:', err)
          );
        }
      }

      return next;
    });
  }, [uid]);

  return { settings, updateSetting, isLoaded };
}
