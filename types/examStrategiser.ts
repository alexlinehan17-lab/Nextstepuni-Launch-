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
  /** Per-prompt debrief content (Stage 3). REQUIRED for new questions.
   *  See /CLAUDE.md § "Strategiser content quality rules". */
  debrief?: PromptDebrief;
}

// ─── Per-prompt debrief (Stage 3) ───────────────────────────────────────
// Replaces the legacy flat `topAnswerIncludes` / `commonTraps` fields.
// Per-prompt structure forces specificity — each prompt names the
// strategic principle it tests and the common wrong answer to it.

export interface ExaminerSource {
  /** Year of the report or marking scheme. */
  year: number;
  /** Document type. Marking schemes are examiner-authored too. */
  type: 'chief-examiner' | 'marking-scheme' | 'sample-paper';
  /** Optional page reference into the source. */
  pageRef?: string;
}

export interface PromptDebrief {
  /** One short line: what strategic principle this prompt was testing. */
  strategicPrinciple: string;
  /** Common wrong answer + why students pick it. Source citation required
   *  if drawn from a report; flagged unsourced otherwise. */
  commonWrongAnswer: {
    answer: string;
    reason: string;
    source?: ExaminerSource;
  };
}

export interface BiggestMistake {
  /** Short headline framing the mistake. */
  title: string;
  /** 2-4 sentences explaining the recurring mistake on this task type. */
  body: string;
  /** Examiner-source citation. Required if drawn from a report. */
  source?: ExaminerSource;
}

export type ExamSubject = 'english' | 'irish' | 'maths' | 'geography' | 'business';

export interface ExamQuestion {
  id: string;                    // e.g. "english-2023-p2-q1"
  subject: ExamSubject;
  /** Cross-question taxonomy id from data/examStrategy/taskTypes.ts. Used to
   *  group questions of the same structural type (e.g. all "style elements"
   *  A(iii) tasks across years) so students can see the recurring pattern. */
  taskType: string;
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

  /** Closing card on the Debrief stage. REQUIRED for new questions per
   *  /CLAUDE.md § "Strategiser content quality rules". */
  biggestMistake?: BiggestMistake;

  /** @deprecated Replaced by per-prompt `PromptDebrief` and question-level
   *  `biggestMistake`. Kept as legacy fallback so existing questions
   *  continue rendering until migrated — see /STRATEGISER_MIGRATION.md.
   *  Do not use in new questions. */
  topAnswerIncludes?: string[];
  /** @deprecated As above. */
  commonTraps?: string[];
  /** @deprecated The mark-scheme stage was folded into Debrief's biggest
   *  mistake card. Do not use. */
  markScheme?: string;
}

export interface ExamSubjectMeta {
  id: ExamSubject;
  label: string;
  questions: ExamQuestion[];
}

export type ExamStrategiserStage = 'question' | 'predict' | 'debrief';

/** Player-local predict answers — kept in component state only, never persisted. */
export type PredictAnswers = Record<string, string | number>;

// ─── Subject strategy preamble ──────────────────────────────────────────
// Per-subject meta-rules read ONCE before opening any specific question.
// Surfaced above the question list. Teaches the marking-shape vocabulary
// (P/C/L/M, SRPs, partial-credit ladder, etc.) so individual question
// tooltips can stop repeating universal rules.

export interface StrategyRule {
  id: string;
  title: string;
  body: string;
  /** Optional — flags this as the *most punitive* / "killer" rule for the
   *  subject. Rendered with stronger emphasis. */
  pinned?: boolean;
}

export interface SubjectStrategy {
  subject: ExamSubject;
  headline: string;
  intro: string;
  rules: StrategyRule[];
  marksToMinutes: {
    summary: string;
    examples: string[];
  };
}

// ─── Cross-subject trap patterns ────────────────────────────────────────
// Trap *types* that recur across subjects and years. The Trap Library view
// catalogs these, with example links back to specific real questions in
// the bank — the point of pattern recognition.

export interface TrapExample {
  /** ID of an existing ExamQuestion in the bank. */
  questionId: string;
  /** Short snippet showing where the trap fires in that question. */
  snippet: string;
}

export interface TrapPattern {
  id: string;
  name: string;
  /** What the trap is and why it costs marks. */
  description: string;
  /** "How to spot it" — diagnostic feature visible in the question. */
  diagnostic: string;
  /** Subjects where this pattern appears. Used for subject filtering. */
  subjects: ExamSubject[];
  /** 1-3 example links back to real questions. */
  examples: TrapExample[];
}
