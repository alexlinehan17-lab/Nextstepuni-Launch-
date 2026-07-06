/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — content registry. Order defines display order.
 */

import { type ChairSubject, type MarkingSession } from './types';
import { BUSINESS_CHAIR } from './business';
import { MATHS_CHAIR } from './maths';

export const CHAIR_SUBJECTS: ChairSubject[] = [BUSINESS_CHAIR, MATHS_CHAIR];

export const allSessions = (): MarkingSession[] => CHAIR_SUBJECTS.flatMap(s => s.sessions);

export const findSession = (id: string): MarkingSession | undefined =>
  allSessions().find(s => s.id === id);

export * from './types';
