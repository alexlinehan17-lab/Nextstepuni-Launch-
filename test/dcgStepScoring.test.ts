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

  it('pays a step priced in parts at exactly the values the scheme prints', () => {
    // 2018 HL B-1(a): "Plan of required Spectator Point, Picture Plane and
    // Vanishing Points ….(2,2,2)" is worth 0, 2, 4 or 6 -- never 3.
    const card = cards.find(c => c.id === 'dcg-2018-hl-b1a-1')!;
    const row = rowsOf(card).find(r => /\(2,2,2\)/.test(r.verbatim))!;
    expect(row.permittedMarks).toEqual([0, 2, 4, 6]);
    expect(marksClaimed(card, { [row.id]: 4 })).toBe(4);
    expect(marksClaimed(card, { [row.id]: 3 })).toBe(0);
    const wrong: string[] = [];
    for (const c of cards) {
      for (const r of rowsOf(c)) {
        const ladders: Array<[string, number[]]> = r.parts
          ? r.parts.map(p => [partClaimId(r.id, p.id), p.permittedMarks] as [string, number[]])
          : r.permittedMarks ? [[r.id, r.permittedMarks]] : [];
        for (const [id, ladder] of ladders) {
          for (const v of ladder) if (marksClaimed(c, { [id]: v }) !== v) wrong.push(`${c.id} ${id}: ${v}`);
        }
      }
    }
    expect(wrong).toEqual([]);
  });

  it("adds each question's cards up to the tariff its paper prints", () => {
    // The covers: "All questions in Section A carry 20 marks"; Sections B and C
    // 45 a question to 2020, 60 from 2021. Ordinary Presentation is priced on
    // the whole question, so it is a row on the question's first card.
    const tariff = (year: number, section: string) => (section === 'A' ? 20 : year <= 2020 ? 45 : 60);
    const totals = new Map<string, { year: number; section: string; sum: number; cards: SecCard[] }>();
    for (const card of cards) {
      const [, year, level, section, q] = card.questionRef.match(/^(\d{4}) (HL|OL) Section ([ABC]) Q(\d)/)!;
      const key = `${year} ${level} ${section}-${q}`;
      const t = totals.get(key) ?? { year: Number(year), section, sum: 0, cards: [] };
      t.sum += card.totalMarks;
      t.cards.push(card);
      totals.set(key, t);
    }
    const wrong: string[] = [];
    for (const [key, t] of totals) {
      if (t.sum !== tariff(t.year, t.section)) wrong.push(`${key}: cards add to ${t.sum}`);
      const presentation = t.cards.flatMap((c, i) => rowsOf(c).filter(r => r.verbatim === 'Presentation').map(() => i));
      const want = key.includes(' OL ') ? [0] : [];
      if (JSON.stringify(presentation) !== JSON.stringify(want)) wrong.push(`${key}: Presentation on cards ${presentation}`);
    }
    expect(wrong).toEqual([]);
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
