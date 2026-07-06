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
import { IRISH_CHAIR } from './irish';
import { FRENCH_CHAIR } from './french';
import { CHEMISTRY_CHAIR } from './chemistry';
import { PHYSICS_CHAIR } from './physics';
import { HISTORY_CHAIR } from './history';
import { ACCOUNTING_CHAIR } from './accounting';
import { GERMAN_CHAIR } from './german';
import { SPANISH_CHAIR } from './spanish';
import { ECONOMICS_CHAIR } from './economics';
import { HOME_ECONOMICS_CHAIR } from './homeeconomics';
import { AG_SCIENCE_CHAIR } from './agscience';
import { APPLIED_MATHS_CHAIR } from './appliedmaths';

// Order: the highest-enrolment subjects first, then the rest.
export const CHAIR_SUBJECTS: ChairSubject[] = [
  ENGLISH_CHAIR,
  MATHS_CHAIR,
  IRISH_CHAIR,
  BIOLOGY_CHAIR,
  BUSINESS_CHAIR,
  GEOGRAPHY_CHAIR,
  FRENCH_CHAIR,
  HISTORY_CHAIR,
  CHEMISTRY_CHAIR,
  PHYSICS_CHAIR,
  ACCOUNTING_CHAIR,
  GERMAN_CHAIR,
  SPANISH_CHAIR,
  ECONOMICS_CHAIR,
  HOME_ECONOMICS_CHAIR,
  AG_SCIENCE_CHAIR,
  APPLIED_MATHS_CHAIR,
];

export const allSessions = (): MarkingSession[] => CHAIR_SUBJECTS.flatMap(s => s.sessions);

export const findSession = (id: string): MarkingSession | undefined =>
  allSessions().find(s => s.id === id);

export * from './types';
