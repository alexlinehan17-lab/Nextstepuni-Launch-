/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — content registry. Order defines display order.
 */

import { type ChairSubject, type MarkingSession } from './types';
import { BUSINESS_CHAIR } from './business';
import { MATHS_CHAIR } from './maths';
import { BIOLOGY_CHAIR } from './biology';
import { GEOGRAPHY_CHAIR } from './geography';
import { ENGLISH_CHAIR } from './english';

export const CHAIR_SUBJECTS: ChairSubject[] = [
  ENGLISH_CHAIR,
  MATHS_CHAIR,
  BUSINESS_CHAIR,
  BIOLOGY_CHAIR,
  GEOGRAPHY_CHAIR,
];

export const allSessions = (): MarkingSession[] => CHAIR_SUBJECTS.flatMap(s => s.sessions);

export const findSession = (id: string): MarkingSession | undefined =>
  allSessions().find(s => s.id === id);

export * from './types';
