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
 * Concurrent reads of the same uid are de-duped via a short-lived in-flight cache
 * (cleared once settled), so several tool hooks mounting together share ONE
 * getDoc instead of each firing its own — while a later re-mount still re-fetches
 * fresh data.
 *
 * Returns `{ doc, loaded }` shaped to drop in for `{ rawProgressDoc, progressLoaded }`:
 *   const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
 */
import { useState, useEffect } from 'react';
import { getProgressDocument, type ProgressDocument } from '../services/progressRepository';

const inflight = new Map<string, Promise<ProgressDocument | null>>();

function loadProgress(uid: string): Promise<ProgressDocument | null> {
  const existing = inflight.get(uid);
  if (existing) return existing;
  const p = getProgressDocument(uid)
    .catch(() => null)
    .finally(() => { inflight.delete(uid); });
  inflight.set(uid, p);
  return p;
}

export function useFreshProgress(uid: string | undefined) {
  const [doc, setDoc] = useState<ProgressDocument | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    if (!uid) { setDoc(null); setLoaded(true); return; }
    loadProgress(uid).then((d) => { if (!cancelled) { setDoc(d); setLoaded(true); } });
    return () => { cancelled = true; };
  }, [uid]);

  return { doc, loaded };
}
