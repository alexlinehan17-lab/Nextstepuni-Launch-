/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — types. One "Rep Card" is a real Leaving Cert question turned
 * into a predict → attempt → mark-it-against-the-real-scheme loop. Content is
 * agent-forged from real SEC sources (examiner-reports/ + examinations.ie) and
 * every lesson carries a citation.
 */

export type RepSubject = 'business' | 'maths' | 'geography' | 'english' | 'history';

export type RibbonKind =
  | 'attempt' | 'method' | 'srp' | 'name' | 'explain' | 'link'
  | 'evaluation' | 'application' | 'quote' | 'gate' | 'other';

/** One credited point in the marking scheme, shown as a chunky "mark ribbon".
 *  A `gate` ribbon (marks 0) is an all-or-nothing requirement — e.g. "name a
 *  valid region or the whole answer scores 0". */
export interface MarkRibbon {
  id?: string;
  label: string;
  marks: number;
  kind: RibbonKind;
}

export interface CommandWordPrimer {
  /** The command word as it appears in the question (e.g. "Account for"). */
  word: string;
  /** The 3-second lesson, e.g. "This says EXPLAIN — give the reason, not just the fact." */
  reminder: string;
}

export type Confidence = 'unsure' | 'maybe' | 'confident';

/**
 * A full-mark exemplar for a card ("Show Me One"). Each segment is tied to the
 * ribbon it earns (by index into `ribbons`), so the reveal can light the ribbons
 * in sequence on the model. Agent-forged from the SEC marking scheme + Chief
 * Examiner reports already cited on the card — never invented. Optional per card:
 * cards without one behave exactly as before (no scaffold, no compare).
 */
export interface ModelAnswer {
  /** Exemplar segments, each tied to the ribbon index it earns. */
  segments: { ribbonIndex: number; text: string }[];
  /** Source citation (SEC marking scheme / Chief Examiner report). */
  source: string;
}

export interface RepCard {
  id: string;
  subject: RepSubject;
  subjectLabel: string;
  level: 'higher' | 'ordinary';
  year: number;
  questionRef: string;     // e.g. "2023 HL · Q6B"
  questionText: string;    // faithfully reproduced SEC stem
  marks: number;           // the tariff
  minutes: number;         // derived ~1 min/mark
  /** 'written' = text box; 'steps' = text box for working; 'paper' = a chart
   *  / diagram / drawing the student does on paper (no text box). */
  answerKind: 'written' | 'steps' | 'paper';
  commandWord?: CommandWordPrimer;
  /** The marking scheme as 3–7 checkable components. Non-gate marks sum ≈ tariff. */
  ribbons: MarkRibbon[];
  /** ONE specific, examiner-sourced takeaway about this question's biggest leak. */
  lesson: { text: string; source: string };
  /** Optional full-mark exemplar ("Show Me One"). Rolled out subject-by-subject. */
  modelAnswer?: ModelAnswer;
  taskType?: string;       // for interleaving + coverage
  /** Curriculum subject id (curriculum.ts), e.g. 'mathematics'. */
  subjectId?: string;
  /** Curriculum sub-topic id (curriculum.ts) — what the picker filters on. */
  topicId?: string;
}

/** A student's Subject → Level → Topic selection, persisted. */
export interface RepSelection {
  subjectId: string;
  level: string;
  topicId: string;
}

/** Stable id for a ribbon (falls back to index when a forged card omits one). */
export function ribbonId(ribbon: MarkRibbon, index: number): string {
  return ribbon.id ?? `r${index}`;
}
