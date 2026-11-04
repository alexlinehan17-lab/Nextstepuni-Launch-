/** @license SPDX-License-Identifier: Apache-2.0 */
import type { PoliticsRubric, SecRubricCard } from '../../../../types/markBank';
import corrections from './corrections.json';

/**
 * Scheme lines a card's lifted block lost, restored from the marking scheme PDF.
 *
 * The SEC prints a sub-part's price in the margin column on its heading's
 * baseline ("(c) (i) One fact … 2 marks"). The text layer gives the price a
 * line of its own, and politics_author.readable() drops a line that is only a
 * price, so the block kept the heading and lost the tariff. Each entry names
 * the scheme page, and replaces the n-th occurrence of the printed heading
 * with the same line as the PDF's words read across that baseline. Nothing is
 * added that the page does not print; a block that no longer holds the line
 * it replaces fails loudly so a regenerated block cannot be corrected twice.
 */
interface LineCorrection { nth: number; from: string; to: string }
interface SchemeCorrection { scheme: string; why: string; lines: LineCorrection[] }

export const SCHEME_CORRECTIONS = corrections as Record<string, SchemeCorrection>;

type PoliticsCard = SecRubricCard & { rubric: PoliticsRubric };

export function withSchemeCorrections<T extends PoliticsCard>(card: T): T {
  const correction = SCHEME_CORRECTIONS[card.id];
  if (!correction) return card;
  const blocks = (card.rubric.schemeGuidance ?? []).map(block => block.split('\n'));
  // Occurrences are counted on the block as lifted, so one heading printed three times is corrected line by line.
  const original = blocks.map(lines => [...lines]);
  for (const { nth, from, to } of correction.lines) {
    let seen = 0;
    let done = false;
    original.forEach((lines, blockIndex) => lines.forEach((line, index) => {
      if (done || line.trim() !== from) return;
      seen += 1;
      if (seen === nth) { blocks[blockIndex][index] = to; done = true; }
    }));
    if (!done) throw new Error(`Politics card ${card.id}: scheme line "${from}" (occurrence ${nth}) is not in its block`);
  }
  return { ...card, rubric: { ...card.rubric, schemeGuidance: blocks.map(lines => lines.join('\n')) } };
}
