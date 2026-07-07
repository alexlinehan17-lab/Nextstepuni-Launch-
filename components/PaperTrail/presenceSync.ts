/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared focus presence (F10) — "N classmates at their desks right now".
 *
 * Anonymous by construction: per class code, one counter doc per 5-minute
 * time bucket (focusPresence/{code}/buckets/{index}). Each active student
 * increments the current bucket exactly once (cadence enforced here), so the
 * current bucket's count IS the presence number — no uids, no join/leave
 * tracking, and a stale bucket simply ages out within five minutes. Firestore
 * rules pin every write to a +1 increment.
 */

import { collection, doc, increment, onSnapshot, setDoc } from 'firebase/firestore';
import { db } from '../../firebase';

const BUCKET_MS = 5 * 60_000;

export const presenceBucket = (now: number) => Math.floor(now / BUCKET_MS);

const bucketDoc = (code: string, bucket: number) =>
  doc(collection(db, 'focusPresence', code.trim().toLowerCase(), 'buckets'), String(bucket));

/**
 * Start broadcasting presence for an active focus session. Increments the
 * current bucket immediately, then once per bucket rollover. Returns a stop
 * function — call it when the session ends or unmounts. Best-effort: network
 * or permission failures are silent (presence is decoration, never load-bearing).
 */
export function startPresence(code: string, now: number): () => void {
  const c = code.trim();
  if (!c) return () => {};
  let lastSent = -1;
  const send = (ts: number) => {
    const b = presenceBucket(ts);
    if (b === lastSent) return;
    lastSent = b;
    setDoc(bucketDoc(c, b), { n: increment(1) }, { merge: true }).catch(() => {});
  };
  send(now);
  const timer = setInterval(() => send(Date.now()), 30_000);
  return () => clearInterval(timer);
}

/** Live count of classmates in the current bucket (including this device once
 * it has broadcast). Calls back on every change; returns an unsubscribe. */
export function subscribePresence(code: string, now: number, cb: (n: number) => void): () => void {
  const c = code.trim();
  if (!c) { cb(0); return () => {}; }
  let unsubDoc: (() => void) | null = null;
  let currentBucket = -1;
  const attach = (ts: number) => {
    const b = presenceBucket(ts);
    if (b === currentBucket) return;
    currentBucket = b;
    unsubDoc?.();
    unsubDoc = onSnapshot(
      bucketDoc(c, b),
      snap => cb(snap.exists() ? ((snap.data().n as number) || 0) : 0),
      () => cb(0),
    );
  };
  attach(now);
  const timer = setInterval(() => attach(Date.now()), 30_000);
  return () => { clearInterval(timer); unsubDoc?.(); };
}
