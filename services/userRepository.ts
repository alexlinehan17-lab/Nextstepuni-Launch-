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

export function mergeUserDocument(uid: string, patch: Partial<UserDocument>): Promise<void> {
  return setDoc(doc(db, 'users', uid), patch, { merge: true });
}
