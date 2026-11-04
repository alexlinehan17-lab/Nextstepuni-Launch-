/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for a History essay card (types/markBank.ts HistoryEssayRubric),
 * exactly as the SEC marks one: by paragraph.
 *
 *  - Cumulative Mark (CM): each paragraph the student wrote is placed on ONE
 *    band of the scheme's paragraph ladder, at one of that band's marks. The
 *    CM is their sum, in the order written, capped at the printed maximum.
 *    A paragraph past the maximum counts zero, which is what the scheme's
 *    annotation for an excess paragraph says ("any remaining material will be
 *    awarded notional marks with zero value attached").
 *  - Where the question prints a NOTE ("If only ONE, Max. CM = 50") and the
 *    student judges that their answer covers only one element, the ceiling is
 *    the NOTE's. A question with no NOTE has no such switch.
 *  - Overall Evaluation (OE): one mark inside one band.
 *  - A saved value the scheme does not permit (a mark between bands, a
 *    fraction, a negative, a mark above the ladder) is rejected, never
 *    rounded into an award.
 *
 * Paragraph count is the student's: there is no preset number of slots, so
 * nothing on the card implies how many paragraphs to write.
 */
import type { HistoryEssayBand, HistoryEssayRubric, SecRubricCard } from '../../types/markBank';

export type HistoryEssayScoreId = `history:${string}`;
export type HistoryEssayScores = Partial<Record<string, number>>;

/** How many paragraphs the score store will hold for one answer. A bound on
 *  storage, never shown and never a target. */
export const HISTORY_PARAGRAPH_LIMIT = 40;

export const historyParagraphCountId: HistoryEssayScoreId = 'history:cm:count';
export const historyParagraphId = (n: number): HistoryEssayScoreId => `history:cm:p${n}`;
export const historyOneElementId: HistoryEssayScoreId = 'history:cm:one-element';
export const historyOeId: HistoryEssayScoreId = 'history:oe';

/** A value the ladder permits: a whole mark inside one of its bands. */
export const onLadder = (bands: readonly HistoryEssayBand[], value: number | undefined): value is number =>
  typeof value === 'number' && Number.isInteger(value) && bands.some(band => band.marks.includes(value));

/** The band a placed mark sits in, or undefined when it sits in none. */
export const bandOf = (bands: readonly HistoryEssayBand[], value: number | null | undefined) =>
  value === null || value === undefined ? undefined : bands.find(band => band.marks.includes(value));

export function historyParagraphCount(scores: HistoryEssayScores): number {
  const raw = scores[historyParagraphCountId];
  return typeof raw === 'number' && Number.isInteger(raw) && raw > 0 ? Math.min(raw, HISTORY_PARAGRAPH_LIMIT) : 0;
}

/** The mark paragraph `n` (1-based) is placed at, or null when it is not placed on the ladder. */
export function historyParagraphMark(rubric: HistoryEssayRubric, scores: HistoryEssayScores, n: number): number | null {
  const value = scores[historyParagraphId(n)];
  return onLadder(rubric.cm.bands, value) ? value : null;
}

/** Whether the student has judged that the answer covers only one element. Honoured only where the question prints a NOTE. */
export const historyOneElement = (rubric: HistoryEssayRubric, scores: HistoryEssayScores): boolean =>
  Boolean(rubric.cm.elementRule) && scores[historyOneElementId] === 1;

/** The CM maximum in force: the printed one, or the NOTE's when the student says the answer covers one element. */
export const historyCmCeiling = (rubric: HistoryEssayRubric, scores: HistoryEssayScores): number =>
  historyOneElement(rubric, scores) ? rubric.cm.elementRule!.max : rubric.cm.max;

export interface HistoryParagraphTally {
  n: number;
  /** The mark the paragraph is placed at, or null. */
  placed: number | null;
  /** What it adds to the CM once the ceiling is applied in order. */
  counted: number;
}

/** Paragraph by paragraph, in the order written: what each is placed at and what it counts under the ceiling. */
export function historyCmTally(rubric: HistoryEssayRubric, scores: HistoryEssayScores) {
  const ceiling = historyCmCeiling(rubric, scores);
  const paragraphs: HistoryParagraphTally[] = [];
  let cm = 0;
  for (let n = 1; n <= historyParagraphCount(scores); n += 1) {
    const placed = historyParagraphMark(rubric, scores, n);
    const counted = placed === null ? 0 : Math.max(0, Math.min(placed, ceiling - cm));
    cm += counted;
    paragraphs.push({ n, placed, counted });
  }
  return { paragraphs, ceiling, cm };
}

/** The OE mark placed, or null when none is placed on the ladder. */
export function historyOeMark(rubric: HistoryEssayRubric, scores: HistoryEssayScores): number | null {
  const value = scores[historyOeId];
  return onLadder(rubric.oe.bands, value) ? value : null;
}

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
