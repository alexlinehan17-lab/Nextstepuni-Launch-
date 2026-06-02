/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Command-Word Reflex — read the question like an examiner.
 *
 * Per subject, the student sees a real exam question stem and taps the command
 * word (the cue that says what to DO), then learns what that cue demands and the
 * examiner-flagged trap behind it.
 *
 * Why: SEC Chief Examiner reports repeatedly find students lose earned marks by
 * mis-reading the cue word — "'outline', 'explain' are often not addressed
 * adequately… due cognisance [should be] taken of question cue word(s)" (LC
 * Business Chief Examiner 2015, p.20). This trains that decode-the-question
 * skill on authentic questions. Distinct from Exam Reps (full-answer practice)
 * and Syllabus X-Ray (mark allocation).
 *
 * Demands + traps are source-grounded from examiner reports / marking schemes;
 * stems are faithful, representative LC question stems containing the real cue.
 */

export type CommandLevel = 'higher' | 'ordinary' | 'common';

export interface CommandWordQuestion {
  id: string;
  subjectId: string;       // curriculum.ts subject id, e.g. 'business'
  subjectLabel: string;
  level: CommandLevel;
  /** Where it's from, e.g. "HL · Business Law" or "2015 HL · Q1(B)". */
  questionRef: string;
  /** The question stem — must contain `commandWord` verbatim so it's tappable. */
  stem: string;
  /** The single cue word the student should identify (the tappable anchor). */
  commandWord: string;
  /** What that cue actually requires you to do — the answer-shaping move. */
  demand: string;
  /** The examiner-flagged mistake for this cue + the marks consequence. */
  trap: string;
  /** Citation for the demand/trap (examiner report or marking scheme). */
  source: string;
  /** Marks typically at stake on a question with this cue. */
  marks: number;
}

/** Persisted under progress/{uid}.commandWordReflex (additive-merge namespace). */
export interface CommandWordState {
  /** Question ids attempted. */
  seenIds: string[];
  /** Question ids spotted correctly on the FIRST tap. */
  firstTryIds: string[];
  /** Distinct command words the student has met (lowercase). */
  wordsMet: string[];
  attempts: number;
  updatedAt: string;
}
