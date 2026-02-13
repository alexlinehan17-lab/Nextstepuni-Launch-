/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db, auth } from '../firebase';

export function useModuleResponses(moduleId: string) {
  const [responses, setResponses] = useState<Record<string, any>>({});
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const uid = auth.currentUser?.uid;
    if (!uid) {
      setIsLoaded(true);
      return;
    }

    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'responses', uid));
        if (snap.exists()) {
          const data = snap.data();
          if (data[moduleId]) {
            setResponses(data[moduleId]);
          }
        }
      } catch (err) {
        console.error('Failed to load responses:', err);
      }
      setIsLoaded(true);
    };

    load();
  }, [moduleId]);

  const saveResponse = useCallback((key: string, value: any) => {
    setResponses(prev => {
      const next = { ...prev, [key]: value };

      const uid = auth.currentUser?.uid;
      if (uid) {
        setDoc(doc(db, 'responses', uid), { [moduleId]: next }, { merge: true }).catch(err =>
          console.error('Failed to save response:', err)
        );
      }

      return next;
    });
  }, [moduleId]);

  return { responses, saveResponse, isLoaded };
}
