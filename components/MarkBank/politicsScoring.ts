/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scoring for a Politics card whose scheme is cut into parts
 * (cards/politics-and-society/answers.ts): a band part holds the mark the
 * student placed on it, a rows part holds a claim per row.
 */
import type { PoliticsAllocation, PoliticsPart } from '../../types/markBank';

export type PoliticsScores = Partial<Record<string, number>>;

export const politicsPartScoreId = (partId: string) => `politics:part:${partId}`;
export const politicsRowScoreId = (partId: string, rowId: string) => `politics:part:${partId}:row:${rowId}`;

/** The mark placed on a band part, 0 unless it sits in one of the part's bands. */
export const politicsPartValue = (part: PoliticsPart, scores: PoliticsScores): number => {
  const value = scores[politicsPartScoreId(part.id)] ?? 0;
  return part.bands?.some(band => band.marks.includes(value)) ? value : 0;
};

export const politicsRowClaimed = (part: PoliticsPart, rowId: string, scores: PoliticsScores) =>
  (scores[politicsRowScoreId(part.id, rowId)] ?? 0) > 0;

export const politicsPartMarks = (part: PoliticsPart, scores: PoliticsScores): number => {
  if (part.bands) return politicsPartValue(part, scores);
  const rows = part.rows ?? [];
  const claimed = rows.filter(row => politicsRowClaimed(part, row.id, scores));
  const count = part.count ?? 1;
  if (part.ladder) {
    const ticked = Math.min(claimed.length, part.ladder.length);
    return ticked > 0 ? part.ladder[ticked - 1] : 0;
  }
  const values = claimed.map(row => row.marks).sort((a, b) => b - a).slice(0, count);
  return Math.min(part.max, values.reduce((sum, value) => sum + value, 0));
};

export const politicsAllocationMarks = (allocation: PoliticsAllocation, scores: PoliticsScores): number =>
  allocation.parts.reduce((sum, part) => sum + politicsPartMarks(part, scores), 0);
