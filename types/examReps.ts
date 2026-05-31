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
  answerKind: 'written' | 'steps';
  commandWord?: CommandWordPrimer;
  /** The marking scheme as 3–7 checkable components. Non-gate marks sum ≈ tariff. */
  ribbons: MarkRibbon[];
  /** ONE specific, examiner-sourced takeaway about this question's biggest leak. */
  lesson: { text: string; source: string };
  taskType?: string;       // for interleaving + coverage
}

/** Stable id for a ribbon (falls back to index when a forged card omits one). */
export function ribbonId(ribbon: MarkRibbon, index: number): string {
  return ribbon.id ?? `r${index}`;
}
