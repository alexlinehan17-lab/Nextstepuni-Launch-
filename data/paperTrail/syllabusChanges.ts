/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — which archived years were set on an earlier syllabus.
 *
 * The archive now reaches back to 1995, so a student can open a paper set on a
 * syllabus that has since been replaced. The SEC's own archive notes that such
 * papers "do not reflect accurately the examination of the current syllabus"
 * and are listed "for reference purposes" (examinations.ie/?l=en&mc=en&sc=sy).
 *
 * Sources of record:
 *  - SEC, Syllabus changes for Leaving Certificate:
 *    https://www.examinations.ie/misc-doc/BI-AR-99013455.pdf
 *  - SEC, Syllabus changes for Leaving Certificate Applied:
 *    https://www.examinations.ie/misc-doc/BI-AR-40878962.pdf
 *  - SEC, Senior Cycle Redevelopment, Tranche 1 (new specifications introduced
 *    September 2025, first examined 2027): https://www.examinations.ie/scr/
 *    (matches curriculumRegistry.ts transitionSubjects for Biology, Chemistry,
 *    Physics and Business).
 *
 * Keys are Paper Trail subject ids. `changes` lists the first examination year
 * of each syllabus change, ascending. The SEC lists "Physics and Chemistry
 * 2002"; the Physics and Chemistry syllabuses were revised together (1999
 * syllabus documents, first examined 2002), so the year applies to all three.
 * Mathematics uses its own sentence: the SEC lists 1996/1997, but every paper
 * before 2010 also predates Project Maths, which the SEC archives separately
 * for 2010-2015 because it reached the exam in stages.
 *
 * Annual refresh: when a redeveloped subject is first examined (Tranche 2 in
 * 2028, and so on — CURRICULUM_REDEVELOPMENT_TRANSITIONS), add its year here.
 */

export interface SyllabusHistory {
  /** First examination year of each syllabus change, ascending. */
  changes: number[];
  /** Replaces the generated per-paper sentence (Project Maths, a retired subject). */
  text?: string;
  /** Replaces the generated year-grid sentence. */
  gridText?: string;
  /** Replaces the short tag (default "Earlier syllabus"). */
  tag?: string;
}

export const PAPER_TRAIL_SYLLABUS_HISTORY: Record<string, SyllabusHistory> = {
  // Leaving Certificate (SEC table)
  accounting: { changes: [1997] },
  french: { changes: [1997] },
  german: { changes: [1997] },
  italian: { changes: [1997] },
  spanish: { changes: [1997] },
  music: { changes: [1999] },
  business: { changes: [1999, 2027] },
  english: { changes: [2001] },
  'physics-and-chemistry': { changes: [2002] },
  physics: { changes: [2002, 2027] },
  chemistry: { changes: [2002, 2027] },
  arabic: { changes: [2004, 2027] },
  japanese: { changes: [2004] },
  biology: { changes: [2004, 2027] },
  'home-economics-s-and-s': { changes: [2004] },
  history: { changes: [2006] },
  'history-early-modern': { changes: [2006] },
  geography: { changes: [2006] },
  russian: { changes: [2006] },
  irish: { changes: [2006] },
  'classical-studies': { changes: [2011, 2023] },
  economics: { changes: [2021] },
  'agricultural-science': { changes: [2021] },
  lithuanian: { changes: [2022] },
  polish: { changes: [2022] },
  portuguese: { changes: [2022] },
  'applied-mathematics': { changes: [2023] },
  art: { changes: [2023] },
  // Tranche 1 subjects without an earlier SEC-listed change
  latin: { changes: [2027] },
  'ancient-greek': { changes: [2027] },
  mathematics: {
    changes: [2010],
    text: 'Earlier syllabus. Set before Project Maths, the current syllabus, which reached the Leaving Cert exam in stages from 2010.',
    gridText: 'Years marked “Earlier syllabus” were set before Project Maths.',
  },
  'technical-drawing': {
    changes: [2009],
    text: 'No longer examined. Design and Communication Graphics replaced Technical Drawing from the 2009 exams.',
    gridText: 'No longer examined. Design and Communication Graphics replaced Technical Drawing from the 2009 exams.',
    tag: 'No longer examined',
  },
  // Leaving Certificate Applied (SEC table)
  'lca-mathematical-applications': { changes: [2023] },
  'lca-information-and-communication-tech': { changes: [2023] },
  'lca-english-and-communications': { changes: [2023] },
};

/** The short tag shown beside an earlier-syllabus year or paper. */
export const EARLIER_SYLLABUS_TAG = 'Earlier syllabus';

export const syllabusTag = (subjectId: string) =>
  PAPER_TRAIL_SYLLABUS_HISTORY[subjectId]?.tag ?? EARLIER_SYLLABUS_TAG;

/**
 * The sentence for a paper of `year`, or null when it is on the current
 * syllabus. `latestExamYear` is the subject's newest June sitting in the
 * archive: changes up to it are past ("was first examined"), later ones are
 * announced ("is first examined") — so the wording follows the data, not the
 * clock.
 */
export function earlierSyllabusNote(
  subjectId: string,
  subjectLabel: string,
  year: number,
  latestExamYear: number,
): string | null {
  const history = PAPER_TRAIL_SYLLABUS_HISTORY[subjectId];
  if (!history) return null;
  const later = history.changes.filter(change => change > year);
  if (!later.length) return null;
  if (history.text) return history.text;
  const past = later.filter(change => change <= latestExamYear);
  const future = later.filter(change => change > latestExamYear);
  if (!past.length) return `Earlier syllabus. A new ${subjectLabel} specification is first examined in ${future[0]}.`;
  const changed = past.length > 1
    ? `The ${subjectLabel} syllabus changed for the ${past[0]} exams and again in ${past[past.length - 1]}`
    : future.length
      ? `The ${subjectLabel} syllabus changed for the ${past[0]} exams`
      : `The current ${subjectLabel} syllabus was first examined in ${past[0]}`;
  return future.length
    ? `Earlier syllabus. ${changed}, and a new specification is first examined in ${future[0]}.`
    : `Earlier syllabus. ${changed}.`;
}

/**
 * Years before the most recent change the archive straddles: the ones worth
 * tagging in a year grid, because current-syllabus years sit beside them.
 * Returns the boundary year, or null when no archived year is current.
 */
export function syllabusBoundary(subjectId: string, latestExamYear: number): number | null {
  const history = PAPER_TRAIL_SYLLABUS_HISTORY[subjectId];
  if (!history) return null;
  const past = history.changes.filter(change => change <= latestExamYear);
  return past.length ? past[past.length - 1] : null;
}

/** One line above a subject's year grid explaining its syllabus history, or
 *  null when nothing in the archive predates a change. */
export function syllabusGridNote(
  subjectId: string,
  subjectLabel: string,
  latestExamYear: number,
): string | null {
  const history = PAPER_TRAIL_SYLLABUS_HISTORY[subjectId];
  if (!history) return null;
  if (history.gridText) return history.gridText;
  const boundary = syllabusBoundary(subjectId, latestExamYear);
  const future = history.changes.filter(change => change > latestExamYear);
  const parts: string[] = [];
  if (boundary) parts.push(`Years marked “${EARLIER_SYLLABUS_TAG}” were set before the ${boundary} syllabus change.`);
  if (future.length) {
    parts.push(boundary
      ? `A new ${subjectLabel} specification is first examined in ${future[0]}.`
      : `A new ${subjectLabel} specification is first examined in ${future[0]}, so every paper here was set on an earlier syllabus.`);
  }
  return parts.length ? parts.join(' ') : null;
}
