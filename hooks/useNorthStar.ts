/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useCallback } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import { type NorthStar } from '../types';
import { useAuth } from '../contexts/AuthContext';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';

/**
 * Shared North Star access for module content. ProgressContext is the source of
 * truth so the localhost Demo Account and a freshly edited North Star are both
 * visible immediately; the previous auth.currentUser lookup excluded demo
 * sessions entirely and duplicated the app-level progress read.
 */
export function useNorthStar() {
  const { user } = useAuth();
  const {
    northStar,
    setNorthStar,
    progressLoaded,
    updateDemoProgress,
  } = useProgress();

  const saveNorthStar = useCallback(async (next: NorthStar) => {
    setNorthStar(next);
    if (!user?.uid) return;
    if (user.uid === DEMO_STUDENT_UID) {
      updateDemoProgress(current => ({ ...current, northStar: next }));
      return;
    }
    saveInBackground(
      setDoc(doc(db, 'progress', user.uid), { northStar: next }, { merge: true }),
      'useNorthStar.save',
    );
  }, [setNorthStar, updateDemoProgress, user?.uid]);

  return { northStar, saveNorthStar, isLoaded: progressLoaded };
}
