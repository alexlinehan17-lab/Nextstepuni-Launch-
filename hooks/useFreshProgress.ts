/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * useFreshProgress — reads progress/{uid} FRESH from Firestore on every mount.
 *
 * Use this instead of the shared ProgressContext snapshot (`useProgress().
 * rawProgressDoc`) in any tool hook that both READS and WRITES its own namespace.
 * The context snapshot is taken once at app start and is NOT refreshed after a
 * tool writes; because the Innovation Zone remounts the active tool on every nav,
 * seeding from that stale snapshot made tools "reset" — losing state saved THIS
 * session — when the student left a tool and came back. Reading fresh on mount
 * always restores the latest saved state. (See project memory:
 * progress-hook-staleness.)
 *
 * Returns `{ doc, loaded }` shaped to drop in for `{ rawProgressDoc, progressLoaded }`:
 *   const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
 */
import { useState, useEffect } from 'react';
import { doc as fsDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';

export function useFreshProgress(uid: string | undefined) {
  const [doc, setDoc] = useState<Record<string, any> | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    if (!uid) { setDoc(null); setLoaded(true); return; }
    getDoc(fsDoc(db, 'progress', uid))
      .then((snap) => {
        if (cancelled) return;
        setDoc(snap.exists() ? snap.data() : null);
        setLoaded(true);
      })
      .catch(() => { if (!cancelled) { setDoc(null); setLoaded(true); } });
    return () => { cancelled = true; };
  }, [uid]);

  return { doc, loaded };
}
