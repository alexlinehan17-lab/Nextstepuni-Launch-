/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Strategiser question registry. Each subject lives in its own file so
 * adding/editing one subject's questions doesn't churn unrelated diffs.
 */

import { type ExamQuestion, type ExamSubject, type ExamSubjectMeta } from '../../types/examStrategiser';
import { englishQuestions } from './english';
import { irishQuestions } from './irish';
import { mathsQuestions } from './maths';

export const EXAM_SUBJECTS: ExamSubjectMeta[] = [
  { id: 'english', label: 'English', questions: englishQuestions },
  { id: 'irish',   label: 'Irish',   questions: irishQuestions },
  { id: 'maths',   label: 'Maths',   questions: mathsQuestions },
];

export function getQuestionsBySubject(subject: ExamSubject): ExamQuestion[] {
  return EXAM_SUBJECTS.find(s => s.id === subject)?.questions ?? [];
}

export function getSubjectMeta(subject: ExamSubject): ExamSubjectMeta | undefined {
  return EXAM_SUBJECTS.find(s => s.id === subject);
}
