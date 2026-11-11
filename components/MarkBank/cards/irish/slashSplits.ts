/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Slash-joined scheme rows cut into their items.
 *
 * Where the scheme prints one point's alternatives on one row, joined by "/" ("Tráchtaire spóirt/Gaeilgeoir/
 * Ciarraíoch/cuirfidh sé tús leis an oíche eolais", "Poist/obair/jabanna", "Tá/Níl"), and every item read alone as
 * printed is an acceptable answer, each item is its own option row. The items share a group (the original row's id),
 * so the point counts once, at its best claimed item: the part scores exactly as the joined row did. Rows whose slash
 * sits inside one answer ("Bhí áthas/lúcháir/ríméad/gliondar air", "Is maith linn/leo an scoil", dates, "agus/nó",
 * criteria prose) stay whole. slashSplits.json lists every row cut, each read against its part (2026-11-11); the
 * decision and reason for every slash row, cut and whole, are in scripts/markbank/authored/irish-slash-rows-20261111.json.
 */
import type { IrishAllocation } from '../../../../types/markBank';
import SPLITS from './slashSplits.json';

interface Split { card: string; criterion: string; part: string; text: string; items: string[] }

const keyOf = (card: string, criterion: string, part: string, text: string) => `${card}::${criterion}::${part}::${text}`;
const BY_KEY = new Map((SPLITS as Split[]).map(split => [keyOf(split.card, split.criterion, split.part, split.text), split]));
const joined = (text: string) => text.replace(/\s*\/\s*/g, '/');

/** Every split applied while the decks were built: a split that no longer meets its row is a stale entry (tested). */
export const SLASH_SPLITS_APPLIED = new Set<string>();
export const SLASH_SPLIT_COUNT = BY_KEY.size;

export const splitSlashRows = (cardId: string, criterionId: string, allocation: IrishAllocation): IrishAllocation => {
  let changed = false;
  const parts = allocation.parts.map(part => ({
    ...part,
    rows: part.rows.flatMap(row => {
      const key = keyOf(cardId, criterionId, part.id, row.text);
      const split = BY_KEY.get(key);
      if (!split) return [row];
      if (joined(split.items.join('/')) !== joined(row.text) || split.items.some(item => !row.text.includes(item))) {
        throw new Error(`Slash split is not the row's own items: ${key}`);
      }
      SLASH_SPLITS_APPLIED.add(key);
      changed = true;
      return split.items.map((text, index) => ({ ...row, id: `${row.id}-${index + 1}`, text, group: row.id }));
    }),
  }));
  return changed ? { ...allocation, parts } : allocation;
};
