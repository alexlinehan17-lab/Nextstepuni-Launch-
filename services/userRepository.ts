/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Authoritative reads and writes for users/{uid}. React components should not
 * infer privileged roles from email addresses: role and school are provisioned
 * server-side and this document is the client-visible source of truth.
 */

import { doc, getDoc, setDoc } from 'firebase/firestore';
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
 * Read users/{uid}, retrying briefly if it is not there yet.
 *
 * Registration creates the auth user first and writes this document straight
 * after, and onAuthStateChanged fires in between. A single read on that path
 * loses the race and reports "no document" for an account that is about to have
 * one — which is how a freshly registered student reached onboarding under a
 * placeholder name instead of their own.
 *
 * Only the absent case waits. A document that exists returns on the first read,
 * so the normal sign-in path is unchanged. An account that genuinely has no
 * document (deleted, or never provisioned) costs `(attempts - 1) * delayMs`
 * before the caller falls back — deliberately small, because that path still has
 * to end in a usable session rather than a spinner.
 */
export async function waitForUserDocument(
  uid: string,
  { attempts = 3, delayMs = 250 }: { attempts?: number; delayMs?: number } = {},
): Promise<UserDocument | null> {
  for (let attempt = 0; attempt < attempts; attempt++) {
    const found = await getUserDocument(uid);
    if (found) return found;
    if (attempt < attempts - 1) {
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  return null;
}

export function mergeUserDocument(uid: string, patch: Partial<UserDocument>): Promise<void> {
  return setDoc(doc(db, 'users', uid), patch, { merge: true });
}
