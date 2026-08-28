/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Authoritative reads and writes for users/{uid}. React components should not
 * infer privileged roles from email addresses: role and school are provisioned
 * server-side and this document is the client-visible source of truth.
 */

import { doc, getDoc, onSnapshot, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type CurriculumLevel } from '../utils/authUtils';
import { type YearGroup } from '../components/subjectData';

export type UserRole = 'gc' | 'staff' | 'admin';

export interface UserDocument {
  name?: string;
  avatar?: string;
  role?: UserRole;
  school?: string;
  yearGroup?: YearGroup;
  curriculumLevel?: CurriculumLevel;
  needsPasswordChange?: boolean;
  isAdmin?: boolean;
  [field: string]: unknown;
}

export async function getUserDocument(uid: string): Promise<UserDocument | null> {
  const snapshot = await getDoc(doc(db, 'users', uid));
  return snapshot.exists() ? snapshot.data() as UserDocument : null;
}

/**
 * Read users/{uid}, waiting briefly if it is not there yet.
 *
 * Registration creates the auth user first and writes this document straight
 * after, and onAuthStateChanged fires in between. A single read on that path
 * loses the race and reports "no document" for an account that is about to have
 * one — which is how a freshly registered student reached onboarding under a
 * placeholder name instead of their own.
 *
 * This waits by LISTENING, not by polling, and the difference is the whole
 * point. The poll this replaced took three reads 250ms apart, and registration
 * writes the document after two further round trips — so on a signup the write
 * landed after the last attempt had already been spent. Every registration paid
 * the entire budget and still returned null. Worse, the cost was invisible:
 * AuthContext only sets loadedDataUid once this resolves, so AppRouter could not
 * render onboarding until the doomed polling finished. That was the bulk of the
 * "five seconds between account creation and onboarding".
 *
 * A snapshot resolves the instant the write lands, so the wait is the write's
 * real duration rather than a sleep interval rounded up — and it returns the
 * actual document, so the student sees their own name instead of the fallback.
 *
 * Only the absent case waits. A document that exists returns on the first read,
 * so the normal sign-in path is one read, exactly as before. An account that
 * genuinely has no document (deleted, or never provisioned) waits `timeoutMs`
 * before the caller falls back — deliberately bounded, because that path still
 * has to end in a usable session rather than a spinner.
 */
export async function waitForUserDocument(
  uid: string,
  { timeoutMs = 1200 }: { timeoutMs?: number } = {},
): Promise<UserDocument | null> {
  const existing = await getUserDocument(uid);
  if (existing) return existing;

  return new Promise<UserDocument | null>(resolve => {
    let settled = false;
    let unsubscribe: (() => void) | null = null;

    const finish = (value: UserDocument | null) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      // The listener can emit before onSnapshot() has returned its unsubscribe
      // function, so tearing down here would leave it attached. The assignment
      // below covers that case by checking `settled`.
      unsubscribe?.();
      resolve(value);
    };

    // Declared after `finish` so it can be const: `finish` only ever runs from
    // the timer or the snapshot callback, both created below this line.
    const timer = setTimeout(() => finish(null), timeoutMs);
    unsubscribe = onSnapshot(
      doc(db, 'users', uid),
      snapshot => { if (snapshot.exists()) finish(snapshot.data() as UserDocument); },
      // A listen that cannot be established must not hold the session open;
      // fall back exactly as a missing document does.
      () => finish(null),
    );
    if (settled) unsubscribe();
  });
}

export function mergeUserDocument(uid: string, patch: Partial<UserDocument>): Promise<void> {
  return setDoc(doc(db, 'users', uid), patch, { merge: true });
}
