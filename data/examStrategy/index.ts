/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam strategy registry — per-subject preambles + cross-question taxonomy.
 */

import { type ExamSubject, type SubjectStrategy } from '../../types/examStrategiser';
import { englishStrategy } from './english';
import { mathsStrategy } from './maths';
import { geographyStrategy } from './geography';
import { irishStrategy } from './irish';

export { TASK_TYPES, getTaskType, getTaskTypesForSubject } from './taskTypes';
export type { TaskTypeMeta } from './taskTypes';
export { TRAP_PATTERNS, getTrapPattern } from './trapPatterns';

const SUBJECT_STRATEGIES: Record<ExamSubject, SubjectStrategy> = {
  english: englishStrategy,
  maths: mathsStrategy,
  geography: geographyStrategy,
  irish: irishStrategy,
};

export function getSubjectStrategy(subject: ExamSubject): SubjectStrategy {
  return SUBJECT_STRATEGIES[subject];
}
