/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for a History essay card (types/markBank.ts HistoryEssayRubric),
 * exactly as the SEC marks one.
 *
 *  - Higher Level, by paragraph: each paragraph the student wrote is placed on
 *    ONE band of the scheme's paragraph ladder, at one of that band's marks.
 *  - Ordinary Level, by Core Statement: each completed Core Statement earns the
 *    printed value ("awarded 5 marks"), and an incomplete one at the end may
 *    earn one of the printed marks below it ("1-4 marks").
 *  - Either way the Cumulative Mark is the sum, in the order written, capped at
 *    the printed maximum, so material past it counts zero — the scheme's
 *    annotation for an excess paragraph ("any remaining material will be awarded
 *    notional marks with zero value attached").
 *  - Where the question prints a NOTE ("If only ONE, Max. CM = 50") and the
 *    student judges that one of its ceilings applies, that ceiling is the
 *    maximum. A question with no NOTE has no such switch.
 *  - Overall Evaluation (OE): one mark inside one band, where the scheme prints
 *    one (Ordinary Q4 has none).
 *  - A saved value the scheme does not permit (a mark between bands, a
 *    fraction, a negative, a mark above the ladder) is rejected, never rounded
 *    into an award.
 *
 * The number of paragraphs or Core Statements is the student's: there is no
 * preset number of slots, so nothing on the card implies how many to write.
 */
import type {
  HistoryCoreStatementCm, HistoryEssayBand, HistoryEssayRubric, HistoryParagraphCm, SecRubricCard,
} from '../../types/markBank';

export type HistoryEssayScoreId = `history:${string}`;
export type HistoryEssayScores = Partial<Record<string, number>>;

/** How many paragraphs or Core Statements the score store holds for one
 *  answer. A bound on storage, never shown and never a target. */
export const HISTORY_PARAGRAPH_LIMIT = 40;

export const historyParagraphCountId: HistoryEssayScoreId = 'history:cm:count';
export const historyParagraphId = (n: number): HistoryEssayScoreId => `history:cm:p${n}`;
/** The NOTE ceiling the student judges applies: its 1-based place in the
 *  NOTE's own list; 0 or absent is none. */
export const historyCapId: HistoryEssayScoreId = 'history:cm:cap';
export const historyStatementCountId: HistoryEssayScoreId = 'history:cm:statements';
export const historyIncompleteId: HistoryEssayScoreId = 'history:cm:incomplete';
export const historyOeId: HistoryEssayScoreId = 'history:oe';

/** A value the ladder permits: a whole mark inside one of its bands. */
export const onLadder = (bands: readonly HistoryEssayBand[], value: number | undefined): value is number =>
  typeof value === 'number' && Number.isInteger(value) && bands.some(band => band.marks.includes(value));

/** The band a placed mark sits in, or undefined when it sits in none. */
export const bandOf = (bands: readonly HistoryEssayBand[], value: number | null | undefined) =>
  value === null || value === undefined ? undefined : bands.find(band => band.marks.includes(value));

const wholeCount = (raw: number | undefined) =>
  typeof raw === 'number' && Number.isInteger(raw) && raw > 0 ? Math.min(raw, HISTORY_PARAGRAPH_LIMIT) : 0;

export const historyParagraphCount = (scores: HistoryEssayScores): number =>
  wholeCount(scores[historyParagraphCountId]);

/** The mark paragraph `n` (1-based) is placed at, or null when it is not placed on the ladder. */
export function historyParagraphMark(cm: HistoryParagraphCm, scores: HistoryEssayScores, n: number): number | null {
  const value = scores[historyParagraphId(n)];
  return onLadder(cm.bands, value) ? value : null;
}

/** The NOTE ceiling in force, or undefined. Honoured only where the question prints a NOTE. */
export function historyCap(rubric: HistoryEssayRubric, scores: HistoryEssayScores) {
  const index = scores[historyCapId];
  const caps = rubric.cm.elementRule?.caps ?? [];
  return typeof index === 'number' && Number.isInteger(index) && index >= 1 && index <= caps.length
    ? caps[index - 1] : undefined;
}

/** The CM maximum in force: the printed one, or the NOTE ceiling the student says applies. */
export const historyCmCeiling = (rubric: HistoryEssayRubric, scores: HistoryEssayScores): number =>
  historyCap(rubric, scores)?.max ?? rubric.cm.max;

export interface HistoryParagraphTally {
  n: number;
  /** The mark the paragraph is placed at, or null. */
  placed: number | null;
  /** What it adds to the CM once the ceiling is applied in order. */
  counted: number;
}

export interface HistoryStatementTally {
  /** Completed Core Statements counted, and the marks they come to before the ceiling. */
  completed: number;
  completedMarks: number;
  /** The incomplete last Core Statement's mark, or null. */
  incomplete: number | null;
  /** What the Core Statements come to before the ceiling. */
  raw: number;
}

/** Paragraph by paragraph (Higher) or Core Statements in all (Ordinary): what is placed, and what counts under the ceiling. */
export function historyCmTally(rubric: HistoryEssayRubric, scores: HistoryEssayScores) {
  const ceiling = historyCmCeiling(rubric, scores);
  const paragraphs: HistoryParagraphTally[] = [];
  let statements: HistoryStatementTally | null = null;
  let cm = 0;
  if (rubric.cm.mode === 'paragraph') {
    for (let n = 1; n <= historyParagraphCount(scores); n += 1) {
      const placed = historyParagraphMark(rubric.cm, scores, n);
      const counted = placed === null ? 0 : Math.max(0, Math.min(placed, ceiling - cm));
      cm += counted;
      paragraphs.push({ n, placed, counted });
    }
  } else {
    const core: HistoryCoreStatementCm = rubric.cm;
    const completed = wholeCount(scores[historyStatementCountId]);
    const part = scores[historyIncompleteId];
    const incomplete = typeof part === 'number' && core.incomplete.includes(part) ? part : null;
    const raw = completed * core.perStatement + (incomplete ?? 0);
    statements = { completed, completedMarks: completed * core.perStatement, incomplete, raw };
    cm = Math.min(raw, ceiling);
  }
  return { paragraphs, statements, ceiling, cm };
}

/** The OE mark placed, or null when none is placed on the ladder (or the scheme prints no OE). */
export function historyOeMark(rubric: HistoryEssayRubric, scores: HistoryEssayScores): number | null {
  if (!rubric.oe) return null;
  const value = scores[historyOeId];
  return onLadder(rubric.oe.bands, value) ? value : null;
}

/** Whether the whole answer has been placed. An essay with an OE is placed in
 *  two halves, the CM and then the answer as a whole, so until its OE is
 *  placed the CM is a running total rather than a placement, and a grade
 *  suggested from it would read a half-placed essay as missed. Where the
 *  scheme prints no OE (Ordinary Q4), the CM is the whole placement. */
export const historyEssayPlacementComplete = (rubric: HistoryEssayRubric, scores: HistoryEssayScores): boolean =>
  !rubric.oe || historyOeMark(rubric, scores) !== null;

export function historyEssayMarks(card: SecRubricCard, scores: HistoryEssayScores): number {
  if (card.rubric.system !== 'history-essay') return 0;
  const { cm } = historyCmTally(card.rubric, scores);
  const oe = historyOeMark(card.rubric, scores) ?? 0;
  return Math.max(0, Math.min(card.totalMarks, cm + oe));
}

/** The writes that add one more paragraph, unplaced. */
export function historyAddParagraph(scores: HistoryEssayScores): Array<[HistoryEssayScoreId, number]> {
  const count = historyParagraphCount(scores);
  if (count >= HISTORY_PARAGRAPH_LIMIT) return [];
  return [[historyParagraphId(count + 1), -1], [historyParagraphCountId, count + 1]];
}

/** The writes that remove paragraph `n`: the paragraphs after it move up one, and the vacated last slot is cleared. */
export function historyRemoveParagraph(scores: HistoryEssayScores, n: number): Array<[HistoryEssayScoreId, number]> {
  const count = historyParagraphCount(scores);
  if (n < 1 || n > count) return [];
  const writes: Array<[HistoryEssayScoreId, number]> = [];
  for (let k = n; k < count; k += 1) writes.push([historyParagraphId(k), scores[historyParagraphId(k + 1)] ?? -1]);
  writes.push([historyParagraphId(count), -1], [historyParagraphCountId, count - 1]);
  return writes;
}

/** The write that sets how many completed Core Statements are counted. */
export const historySetStatements = (count: number): [HistoryEssayScoreId, number] =>
  [historyStatementCountId, Math.max(0, Math.min(HISTORY_PARAGRAPH_LIMIT, Math.floor(count)))];
