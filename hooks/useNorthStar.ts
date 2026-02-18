/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db, auth } from '../firebase';
import { NorthStar } from '../types';

export function useNorthStar() {
  const [northStar, setNorthStar] = useState<NorthStar | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const uid = auth.currentUser?.uid;
    if (!uid) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        if (snap.exists()) {
          const data = snap.data();
          if (data.northStar) {
            setNorthStar(data.northStar as NorthStar);
          }
        }
      } catch (err) {
        console.error('Failed to load North Star:', err);
      }
      setIsLoaded(true);
    };

    load();
  }, []);

  const saveNorthStar = useCallback(async (ns: NorthStar) => {
    setNorthStar(ns);
    const uid = auth.currentUser?.uid;
    if (uid) {
      try {
        await setDoc(doc(db, 'progress', uid), { northStar: ns }, { merge: true });
      } catch (err) {
        console.error('Failed to save North Star:', err);
      }
    }
  }, []);

  return { northStar, saveNorthStar, isLoaded };
}
