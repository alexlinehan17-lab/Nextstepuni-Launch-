/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type UserSettings } from '../types';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const STORAGE_KEY = 'nextstep-settings';

// `accentTheme` was removed as part of the teal→orange brand pivot — the
// `--accent` CSS variables now come solely from index.html. Any existing
// `accentTheme` field on settings/{uid} docs is orphan data and is ignored
// on read.
const DEFAULT_SETTINGS: UserSettings = {
  language: 'en',
  avatar: '',
  darkMode: false,
  cardStyle: 'default',
  defaultWorkMinutes: 25,
  showDashboard: false,
};

function readLocalSettings(): Partial<UserSettings> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (err) { console.error('Failed to read local settings:', err); }
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
    if (!uid || uid === DEMO_STUDENT_UID) {
      setIsLoaded(true);
      return;
    }

    let cancelled = false;

    const load = async () => {
      try {
        const settingsDoc = await getDoc(doc(db, 'settings', uid));
        if (cancelled) return;
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
      if (!cancelled) setIsLoaded(true);
    };

    load();
    return () => { cancelled = true; };
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

  // Sync card style data attribute
  useEffect(() => {
    document.body.dataset.cardStyle = settings.cardStyle || 'default';
  }, [settings.cardStyle]);

  const updateSetting = useCallback(<K extends keyof UserSettings>(key: K, value: UserSettings[K]) => {
    // Immediately sync DOM before React re-render
    if (key === 'darkMode') {
      if (value) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } else if (key === 'cardStyle') {
      document.body.dataset.cardStyle = (value as string) || 'default';
    }

    setSettings(prev => {
      const next = { ...prev, [key]: value };
      writeLocalSettings(next);

      // Persist to Firestore
      if (uid && uid !== DEMO_STUDENT_UID) {
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
