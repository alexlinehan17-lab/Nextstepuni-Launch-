/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Strategiser — types shared across the tool's components and the
 * per-subject question data files.
 */

export type AnnotationType = 'command' | 'keyword' | 'trap' | 'marks-allocation';

export interface TextSegment {
  text: string;
  annotation?: { note: string; type: AnnotationType };
}

export interface QuestionPart {
  type: 'paragraph' | 'list-item' | 'subpart-label' | 'formula' | 'spacer';
  content: TextSegment[];
}

export interface PredictPrompt {
  id: string;
  prompt: string;
  type: 'multiple-choice' | 'short-text' | 'number';
  options?: string[];
  correctAnswer?: string | number;
  hint?: string;
}

export type ExamSubject = 'english' | 'irish' | 'maths';

export interface ExamQuestion {
  id: string;                    // e.g. "english-2023-p2-q1"
  subject: ExamSubject;
  year: number;
  paper?: string;                // e.g. "Paper 1"
  section?: string;
  questionNumber: string;        // e.g. "1", "2(a)"
  level?: 'higher' | 'ordinary' | 'foundation';
  marks: number;
  totalPaperMarks?: number;      // for marks-to-minutes calc
  totalPaperMinutes?: number;
  commandWords: string[];
  questionText: QuestionPart[];
  predictPrompts: PredictPrompt[];
  topAnswerIncludes: string[];
  commonTraps: string[];
  markScheme?: string;           // markdown, optional
}

export interface ExamSubjectMeta {
  id: ExamSubject;
  label: string;
  questions: ExamQuestion[];
}

export type ExamStrategiserStage = 'raw' | 'predict' | 'annotation' | 'insights' | 'mark-scheme';

/** Player-local predict answers — kept in component state only, never persisted. */
export type PredictAnswers = Record<string, string | number>;
