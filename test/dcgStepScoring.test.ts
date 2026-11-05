/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A DCG card scores each construction step at its own printed price.
 *
 * The scheme prices a drawing as a run of steps, every one required and each
 * worth its own mark. Carried as one anyN group, the steps were paid by how
 * many were ticked, in the order the marks were listed: ticking only
 * dcg-2019-hl-a1b's 5-mark step scored 1. Every step is now a row (or, on a
 * unit past the six-row cap, a part of one row) claimed on its own, and this
 * holds every card in the deck to it: any single step claimed alone scores
 * exactly that step, and everything claimed scores the card's total.
 */

import { describe, expect, it } from 'vitest';
import { CARDS as DCG_HIGHER } from '../components/MarkBank/cards/dcg/higher';
import { CARDS as DCG_ORDINARY } from '../components/MarkBank/cards/dcg/ordinary';
import { claimableTotal, marksClaimed, partClaimId } from '../components/MarkBank/SessionScreen';
import type { MarkRow, SecCard } from '../types/markBank';

const cards = [...DCG_HIGHER, ...DCG_ORDINARY] as SecCard[];
type Claims = Record<string, 'yes' | number>;
const rowsOf = (card: SecCard) => ('rows' in card ? card.rows : []) as MarkRow[];

/** Every single claim a student can make on a card, with what it must score. */
function singleClaims(card: SecCard): Array<[string, Claims, number]> {
  return rowsOf(card).flatMap(row => {
    if (row.parts) {
      return row.parts.map(part => [`${row.id}/${part.id}`,
        { [partClaimId(row.id, part.id)]: part.marks }, part.marks] as [string, Claims, number]);
    }
    if (row.permittedMarks) return [[row.id, { [row.id]: row.marks ?? 0 }, row.marks ?? 0] as [string, Claims, number]];
    return [[row.id, { [row.id]: 'yes' }, row.marks ?? 0] as [string, Claims, number]];
  });
}

describe('DCG step scoring', () => {
  it('ticking only the 5-mark step of 2019 HL A-1(b) scores 5', () => {
    const card = cards.find(c => c.id === 'dcg-2019-hl-a1b')!;
    const rows = rowsOf(card);
    expect(rows.map(r => r.marks)).toEqual([1, 2, 5]);
    expect(marksClaimed(card, { [rows[2].id]: 'yes' })).toBe(5);
    expect(marksClaimed(card, { [rows[0].id]: 'yes' })).toBe(1);
  });

  it('no DCG card carries an any-N group: the scheme prints none', () => {
    expect(cards.flatMap(c => rowsOf(c).filter(r => r.kind === 'anyN').map(r => r.id))).toEqual([]);
  });

  it('scores every step alone at its own price, and the whole card at its total', () => {
    const wrong: string[] = [];
    for (const card of cards) {
      const all: Claims = {};
      for (const [what, claim, want] of singleClaims(card)) {
        const got = marksClaimed(card, claim);
        if (got !== want) wrong.push(`${card.id} ${what}: scored ${got}, prices ${want}`);
        Object.assign(all, claim);
      }
      if (marksClaimed(card, all) !== card.totalMarks || claimableTotal(card) !== card.totalMarks) {
        wrong.push(`${card.id}: all claimed ${marksClaimed(card, all)}, claimable ${claimableTotal(card)}, total ${card.totalMarks}`);
      }
    }
    expect(wrong).toEqual([]);
  });
});
