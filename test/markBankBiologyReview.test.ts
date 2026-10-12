/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Biology paper-by-paper review: the reviewed sittings ship exactly the tasks
 * their ledgers record, at the published tariffs, with every finite printed
 * route expanded and every printed figure the ask needs.
 *
 * The ledger (scripts/markbank/authoring/bio_review_<year>_<level>.py) is
 * checked against the SEC PDFs by bio_review.py; this pins what reached the
 * shipped deck so a later regeneration cannot silently drop or reshape it.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as BIO_HIGHER } from '../components/MarkBank/cards/biology/higher';
import { CARDS as BIO_ORDINARY } from '../components/MarkBank/cards/biology/ordinary';
import audit from '../scripts/markbank/authored/biology-review-audit.json';
import { tariffReconciles } from '../types/markBank';

type Task = { id: string; questionRef: string; total: number; route: string | null;
  status: 'carded' | 'excluded' };
type Sitting = { tasks: Task[]; cardCount: number; baseTaskCount: number;
  routes: Record<string, string[]>;
  sources: Record<string, { sha256: string; pages: number }>;
  checks: { excluded: Array<{ id: string; reason: string; evidence: string; schemeRows: string[] }> } };
const sittings = (audit as unknown as { sittings: Record<string, Sitting> }).sittings;
const sitting = sittings['2026-hl'];

type ReviewedCard = (typeof BIO_HIGHER)[number] & {
  rows: Array<{ contextNote?: string }>;
  figure?: { solution?: boolean };
  questionFigure?: unknown;
  sourceMaterial?: { pages: number[] };
};
const cards2026 = BIO_HIGHER.filter(card => card.year === 2026) as unknown as ReviewedCard[];
const byId = new Map(cards2026.map(card => [card.id, card]));

describe('Biology 2026 Higher — reviewed sitting', () => {
  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(sitting.baseTaskCount).toBe(184);
    expect(sitting.cardCount).toBe(188);
    expect(cards2026).toHaveLength(188);
    expect(new Set(sitting.tasks.map(task => task.id))).toEqual(new Set(byId.keys()));
  });

  it('pins the reviewed source PDFs', () => {
    expect(sitting.sources['038'].sha256)
      .toBe('1c3aa8ed6f7543e9ee2ced1f749ccdf8f85c708317bd243d51c2d4d8503dfa51');
    expect(sitting.sources['040'].sha256)
      .toBe('c86209f155cfce3e0a9ddbd23567c5029b2ae59e8f631b56e951adf911966c24');
    expect(sitting.sources.scheme.sha256)
      .toBe('82da86ffaa8e6989e44d4d4175488b5debe07193c31d05316089446888c0571e');
    expect([sitting.sources['038'].pages, sitting.sources['040'].pages,
      sitting.sources.scheme.pages]).toEqual([40, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of sitting.tasks) {
      const card = byId.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('adds up to the printed question totals', () => {
    const totals = new Map<number, number>();
    for (const task of sitting.tasks) {
      if (task.route && task.route !== 'agriculture') continue;   // one route per pool
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    expect(totals.get(1)).toBe(24);   // best five of six parts at 4
    for (const q of [2, 3, 4, 5, 6, 7]) expect(totals.get(q), `Q${q}`).toBe(20);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);   // any two of four 30s
  });

  it('expands the two closed choose-one pools into one card per printed area', () => {
    for (const part of ['ii', 'iii']) {
      const routes = cards2026.filter(card => card.questionRef.startsWith(`2026 HL Q12(c)(${part}) — `));
      expect(routes.map(card => card.questionRef.split(' — ')[1]).sort())
        .toEqual(['agriculture', 'fisheries', 'forestry']);
      expect(new Set(routes.map(card => card.totalMarks)).size).toBe(1);
    }
  });

  it('links each card to the booklet its question is printed in', () => {
    for (const card of cards2026) {
      expect(card.paperFileid, card.id).toBe(card.section === 'C' ? 'LC025ALP040EV' : 'LC025ALP038EV');
    }
  });

  it('keeps the scheme\'s Q16(a) erratum on the parts it affects', () => {
    for (const id of ['bio-2026-hl-q16-a-i-1', 'bio-2026-hl-q16-a-i-2',
      'bio-2026-hl-q16-a-ii-1', 'bio-2026-hl-q16-a-ii-2']) {
      const card = byId.get(id)!;
      expect(card.rows.some(row => /error in the labelling of Diagram B/.test(row.contextNote ?? '')), id)
        .toBe(true);
    }
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|graph)s?\b|\bgraph 2\b|\bdiagram [12]\b|\bdiagrams [AB]\b/i;
    for (const card of cards2026) {
      const text = `${card.stem ?? ''} ${card.questionText}`.replace(/the diagram you have drawn/gi, '');
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // Q4(d) is answered by the scheme's drawing, held back until reveal.
    expect(byId.get('bio-2026-hl-q4-d')!.figure?.solution).toBe(true);
    expect(byId.get('bio-2026-hl-q4-d')!.sourceMaterial?.pages).toEqual([6]);
  });
});

const ol = sittings['2026-ol'];
const ordinary2026 = BIO_ORDINARY.filter(card => card.year === 2026) as unknown as ReviewedCard[];
const olById = new Map(ordinary2026.map(card => [card.id, card]));
const verbatims = (id: string) => (olById.get(id)!.rows as unknown as Array<{ verbatim: string }>)
  .map(row => row.verbatim);

describe('Biology 2026 Ordinary — reviewed sitting', () => {
  it('ships every carded task, excludes the one it cannot card, and nothing else', () => {
    expect(ol.baseTaskCount).toBe(183);
    expect(ol.cardCount).toBe(187);
    expect(ordinary2026).toHaveLength(187);
    const carded = ol.tasks.filter(task => task.status === 'carded').map(task => task.id);
    expect(new Set(carded)).toEqual(new Set(olById.keys()));
    // Q12(b)(ii)2: the scheme prints "Rr" in both offspring boxes, against its
    // own "White" phenotype for the r row. Reviewed, priced and excluded with
    // its evidence; neither the misprint nor a correction is carded.
    expect(ol.tasks.filter(task => task.status === 'excluded').map(task => task.id))
      .toEqual(['bio-2026-ol-q12-b-ii-2']);
    expect(olById.has('bio-2026-ol-q12-b-ii-2')).toBe(false);
    const [exclusion] = ol.checks.excluded;
    expect(exclusion.schemeRows).toEqual(['Rr', 'Rr']);
    expect(exclusion.evidence).toMatch(/both offspring boxes .* print "Rr"/);
    expect(exclusion.evidence).toMatch(/"White"/);
  });

  it('pins the reviewed source PDFs', () => {
    expect(ol.sources['038'].sha256)
      .toBe('446438a5c540b061f7aadd5a5ee8db45dd353cfda06481c80c93771baf573000');
    expect(ol.sources['040'].sha256)
      .toBe('b245a4e4d0ca2038953407442a1cd61c4b8adddffb36fcd1edfc1bc9bff309d1');
    expect(ol.sources.scheme.sha256)
      .toBe('f42244755e482722cc5584503b73b78ffcc9167d92a7a7cd3104ccd2d1b94047');
    expect([ol.sources['038'].pages, ol.sources['040'].pages, ol.sources.scheme.pages])
      .toEqual([36, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of ol.tasks.filter(t => t.status === 'carded')) {
      const card = olById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('adds up to the printed question totals', () => {
    const firstRoute = new Set(Object.values(ol.routes).map(routes => routes[0]));
    const totals = new Map<number, number>();
    for (const task of ol.tasks) {
      if (task.route && !firstRoute.has(task.route)) continue;   // one route per pool
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    for (const q of [1, 3, 4, 7]) expect(totals.get(q), `Q${q}`).toBe(20);
    // "6(3) + (2)": seven responses each carded at 3; the ladder pays the
    // seventh 2, so the question's 20 is the ladder's, not the cards' sum.
    for (const q of [2, 5, 6]) expect(totals.get(q), `Q${q}`).toBe(21);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);   // any two of four 30s
  });

  it('expands the four closed choose-one pools into one card per printed option', () => {
    const routesOf = (ref: string) => ordinary2026
      .filter(card => card.questionRef.startsWith(`2026 OL ${ref} — `))
      .map(card => card.questionRef.split(' — ')[1]).sort();
    expect(routesOf('Q7(c)')).toEqual(['asthma', 'bronchitis']);
    expect(routesOf('Q13(b)(vi)')).toEqual(['electrons', 'protons']);
    expect(routesOf('Q16(c)(vi)')).toEqual(['diet', 'exercise', 'smoking']);
    expect(routesOf('Q17(a)(iv)')).toEqual(['ear', 'eye']);
  });

  it('reads the answers the scheme prints as marks, not words', () => {
    expect(verbatims('bio-2026-ol-q1-a')).toEqual(['Protein']);
    expect(['a', 'b', 'c', 'd', 'e', 'f', 'g'].map(x => verbatims(`bio-2026-ol-q2-${x}`)[0]))
      .toEqual(['False', 'True', 'True', 'False', 'True', 'False', 'True']);
    // Q7(a): seven named parts, one card each (seven rows would pass a card's five).
    expect(['diaphragm', 'lungs', 'bronchus', 'trachea', 'bronchiole', 'rings-of-cartilage', 'larynx']
      .map(part => verbatims(`bio-2026-ol-q7-a-${part}`)[0]))
      .toEqual(['Diaphragm — ⑧', 'Lungs — ⑦', 'Bronchus — ②', 'Trachea (windpipe) — ①',
        'Bronchiole — ⑥', 'Rings of cartilage — ④', 'Larynx (voice box) — ③']);
    expect(verbatims('bio-2026-ol-q8-a-ii')).toEqual(['x10']);
    expect(verbatims('bio-2026-ol-q9-a-i')).toEqual(['Folded (globular)']);
    expect(verbatims('bio-2026-ol-q12-c-i')).toEqual(['C — G', 'G — C', 'A — T', 'T — A']);
    expect(verbatims('bio-2026-ol-q13-b-ii')).toEqual(['C H O — 6 12 6']);
  });

  it('links each card to the booklet its question is printed in', () => {
    for (const card of ordinary2026) {
      expect(card.paperFileid, card.id).toBe(card.section === 'C' ? 'LC025GLP040EV' : 'LC025GLP038EV');
    }
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|graph|table)s?\b|\bdiagrams? [AB]\b|\bthe axes\b|\bformula shown\b/i;
    for (const card of ordinary2026) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // Two drawing asks are set as the paper prints them (the question crop
    // keeps the dotted-line symbol the text layer drops), and answered by the
    // scheme's drawing, held back until reveal.
    for (const [id, page] of [['bio-2026-ol-q10-b-i-1', 11], ['bio-2026-ol-q16-c-ii', 8]] as const) {
      expect(olById.get(id)!.questionFigure, id).toBeTruthy();
      expect(olById.get(id)!.figure?.solution, id).toBe(true);
      expect(olById.get(id)!.sourceMaterial?.pages, id).toEqual([page]);
    }
  });
});
