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
import { createHash } from 'node:crypto';
import { tariffReconciles } from '../types/markBank';

type Task = { id: string; questionRef: string; total: number; route: string | null;
  status: 'carded' | 'excluded' | 'verified' | 'corrected' | 'added' };
type Correction = { id: string; changed: string[]; fieldsBefore: Record<string, unknown> };
type Sitting = { tasks: Task[]; cardCount: number; baseTaskCount: number;
  routes: Record<string, string[]>;
  review?: { baselineCommit: string; verified: string[]; corrected: Correction[]; added: string[];
    retained: Array<{ id: string; reason: string }>;
    withdrawn: Record<string, { replacementId: string; reason: string }> };
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

const hl25 = sittings['2025-hl'];
const higher2025 = BIO_HIGHER.filter(card => card.year === 2025) as unknown as ReviewedCard[];
const hl25ById = new Map(higher2025.map(card => [card.id, card]));
const contentHash = (cards: readonly unknown[]) => createHash('sha256')
  .update(JSON.stringify(cards)).digest('hex');

describe('Biology 2025 Higher — reviewed sitting, corrected in place', () => {
  const review = hl25.review!;

  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(hl25.baseTaskCount).toBe(167);
    expect(hl25.cardCount).toBe(173);
    expect(higher2025).toHaveLength(173);
    expect(new Set(hl25.tasks.map(task => task.id))).toEqual(new Set(hl25ById.keys()));
  });

  it('keeps every pre-existing id: verified, corrected, or a withdrawn never-shipped twin', () => {
    expect(review.baselineCommit).toBe('6bb860204');
    expect([review.verified.length, review.corrected.length, review.added.length,
      review.retained.length]).toEqual([8, 99, 66, 12]);
    for (const id of [...review.verified, ...review.corrected.map(c => c.id), ...review.added]) {
      expect(hl25ById.has(id), id).toBe(true);
    }
    for (const { id } of review.retained) {
      expect(hl25ById.has(id), id).toBe(false);
      expect(review.withdrawn[id]?.replacementId, id).toBeTruthy();
      expect(hl25ById.has(review.withdrawn[id].replacementId), id).toBe(true);
    }
  });

  it('records what each corrected card showed before', () => {
    for (const correction of review.corrected) {
      expect(correction.changed.length, correction.id).toBeGreaterThan(0);
      for (const field of correction.changed) {
        expect(field in correction.fieldsBefore, `${correction.id}.${field}`).toBe(true);
      }
    }
  });

  it('leaves the cards the review verified exactly as they shipped', () => {
    const verified = review.verified.map(id => hl25ById.get(id)!)
      .sort((a, b) => a.id.localeCompare(b.id));
    // The eight cards' shipped text is byte-identical to the deck before the review.
    expect(contentHash(verified)).toBe('01ce2cf8d3c67b32e642be6ebe8f30d32cba3a5618ca55690bc1fab7df3c81cc');
  });

  it('pins the reviewed source PDFs', () => {
    expect(hl25.sources['038'].sha256)
      .toBe('23983f696580948ae097280069cd4bc7977fcefaadd3f17dc8c50c016960ee9c');
    expect(hl25.sources['040'].sha256)
      .toBe('d56e7550c86a92f8d9285d7265fd6b0c316f266d1a5d74e75cae425684d9044b');
    expect(hl25.sources.scheme.sha256)
      .toBe('f3417b27f2446080891b3f05444eaeccc06a7b820992a2d371662f2e6ec93843');
    expect([hl25.sources['038'].pages, hl25.sources['040'].pages, hl25.sources.scheme.pages])
      .toEqual([40, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of hl25.tasks) {
      const card = hl25ById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('adds up to the printed question totals', () => {
    const firstRoute = new Set(Object.values(hl25.routes).map(routes => routes[0]));
    const totals = new Map<number, number>();
    for (const task of hl25.tasks) {
      if (task.route && !firstRoute.has(task.route)) continue;
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    expect(totals.get(1)).toBe(24);   // best five of six parts at 4
    for (const q of [2, 3, 4, 5, 6, 7]) expect(totals.get(q), `Q${q}`).toBe(20);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);
  });

  it('expands the four closed choose-one pools into one card per printed option', () => {
    const routesOf = (ref: string) => higher2025
      .filter(card => card.questionRef.startsWith(`2025 HL ${ref} — `))
      .map(card => card.questionRef.split(' — ')[1]).sort();
    expect(routesOf('Q14(b)(iv)')).toEqual(['hearing-defect', 'long-sightedness', 'short-sightedness']);
    expect(routesOf('Q14(c)(iv)')).toEqual(['paralysis', 'parkinsons-disease']);
    expect(routesOf('Q15(c)(iii)')).toEqual(['agriculture', 'domestic', 'industry']);
    expect(routesOf('Q16(b)(vi)')).toEqual(['asthma', 'bronchitis']);
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|graph)s?\b|\bthe graphs\b/i;
    for (const card of higher2025) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // Q13(a)(ii): the scheme's equation, with the subscripts and arrow the
    // text layer drops, waits for the reveal.
    expect(hl25ById.get('bio-2025-hl-q13-a-ii')!.figure?.solution).toBe(true);
  });
});

const ol25 = sittings['2025-ol'];
const ordinary2025 = BIO_ORDINARY.filter(card => card.year === 2025) as unknown as ReviewedCard[];
const ol25ById = new Map(ordinary2025.map(card => [card.id, card]));
const ol25Verbatims = (id: string) => (ol25ById.get(id)!.rows as unknown as Array<{ verbatim: string }>)
  .map(row => row.verbatim);

describe('Biology 2025 Ordinary — reviewed sitting, corrected in place', () => {
  const review = ol25.review!;

  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(ol25.baseTaskCount).toBe(171);
    expect(ol25.cardCount).toBe(175);
    expect(ordinary2025).toHaveLength(175);
    expect(new Set(ol25.tasks.map(task => task.id))).toEqual(new Set(ol25ById.keys()));
  });

  it('keeps every shipped id but one aliased duplicate', () => {
    expect(review.baselineCommit).toBe('98d985b9d');
    expect([review.verified.length, review.corrected.length, review.added.length,
      review.retained.length]).toEqual([5, 127, 43, 1]);
    for (const id of [...review.verified, ...review.corrected.map(c => c.id), ...review.added]) {
      expect(ol25ById.has(id), id).toBe(true);
    }
    // "Q16(c)(iii)-(iv)" duplicated the cards for (iii) and (iv): withdrawn,
    // its progress carried to the (iii) card.
    expect(review.retained.map(r => r.id)).toEqual(['bio-2025-ol-q16-ciii-fig']);
    expect(ol25ById.has('bio-2025-ol-q16-ciii-fig')).toBe(false);
    expect(review.withdrawn['bio-2025-ol-q16-ciii-fig'].replacementId).toBe('bio-2025-ol-q16-c-iii');
    expect(ol25ById.has('bio-2025-ol-q16-c-iii')).toBe(true);
  });

  it('records what each corrected card showed before', () => {
    for (const correction of review.corrected) {
      expect(correction.changed.length, correction.id).toBeGreaterThan(0);
      for (const field of correction.changed) {
        expect(field in correction.fieldsBefore, `${correction.id}.${field}`).toBe(true);
      }
    }
  });

  it('leaves the cards the review verified exactly as they shipped', () => {
    const verified = review.verified.map(id => ol25ById.get(id)!)
      .sort((a, b) => a.id.localeCompare(b.id));
    // The five cards' shipped text is byte-identical to the deck before the review.
    expect(contentHash(verified)).toBe('9f7d90b2f5ac46b76bdc6f13ae6cd9cfa9023fa7b042c921048b3c60943bbbf4');
  });

  it('pins the reviewed source PDFs', () => {
    expect(ol25.sources['038'].sha256)
      .toBe('18d7bbfd7c80dd3a4d794f0b93f5b7b3878ad98235ae5ca4a3d364f4e9b37ae1');
    expect(ol25.sources['040'].sha256)
      .toBe('cb5f36e52e4ed56d66d6903ac53afe72759eea3881def5ef8bd627bfaefe1b35');
    expect(ol25.sources.scheme.sha256)
      .toBe('abe98d1dd4ba6b6b10fec7064156fde4dd13ed4679e663aaafb4440d897cad8e');
    expect([ol25.sources['038'].pages, ol25.sources['040'].pages, ol25.sources.scheme.pages])
      .toEqual([36, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of ol25.tasks) {
      const card = ol25ById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('adds up to the printed question totals', () => {
    const firstRoute = new Set(Object.values(ol25.routes).map(routes => routes[0]));
    const totals = new Map<number, number>();
    for (const task of ol25.tasks) {
      if (task.route && !firstRoute.has(task.route)) continue;   // one route per pool
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    for (const q of [1, 2]) expect(totals.get(q), `Q${q}`).toBe(20);   // 5(4)
    // "6(3) + 2": seven responses each carded at 3; the ladder pays the
    // seventh 2, so the question's 20 is the ladder's, not the cards' sum.
    for (const q of [3, 4, 5, 6, 7]) expect(totals.get(q), `Q${q}`).toBe(21);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);   // any two of four 30s
  });

  it('expands the three closed choose-one pools into one card per printed option', () => {
    const routesOf = (ref: string) => ordinary2025
      .filter(card => card.questionRef.startsWith(`2025 OL ${ref} — `))
      .map(card => card.questionRef.split(' — ')[1]).sort();
    expect(routesOf('Q14(b)(v)')).toEqual(['phloem', 'xylem']);
    expect(routesOf('Q17(b)(v)')).toEqual(['cartilage', 'ligament', 'synovial-fluid']);
    expect(routesOf('Q17(b)(vi)')).toEqual(['arthritis', 'osteoporosis']);
  });

  it('reads the answers the scheme prints as marks, boxes and drawings', () => {
    expect(ol25Verbatims('bio-2025-ol-q1-b')).toEqual(['C x ( H 2 O )y']);
    expect(ol25Verbatims('bio-2025-ol-q1-c')).toEqual(['Fatty acid — Glycerol Fatty acid — Fatty acid']);
    expect(['a-e', 'b', 'c', 'd', 'e'].map(x => ol25Verbatims(`bio-2025-ol-q2-${x}`)[0]))
      .toEqual(['Biosphere', 'Ecosystem', 'Conservation', 'Habitat', 'Pollution']);
    expect(['a', 'b', 'c', 'd', 'e', 'f', 'g'].map(x => ol25Verbatims(`bio-2025-ol-q3-${x}`)[0]))
      .toEqual(['True', 'False', 'True', 'True', 'False', 'False', 'True']);
    expect(ol25Verbatims('bio-2025-ol-q6-a')).toEqual(['hormones', 'bloodstream', 'impulses', 'neurons']);
    expect(ol25Verbatims('bio-2025-ol-q14-b-i-ii-fig')[0]).toBe('2');
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|graph|table)s?\b|\bthe one shown\b|\bdiagram, 1 or 2\b/i;
    for (const card of ordinary2025) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // Q1(b) and Q1(c) are set as the paper prints them and answered by the
    // scheme's own filled formula and drawn structure, held back until reveal.
    for (const id of ['bio-2025-ol-q1-b', 'bio-2025-ol-q1-c']) {
      expect(ol25ById.get(id)!.questionFigure, id).toBeTruthy();
      expect(ol25ById.get(id)!.figure?.solution, id).toBe(true);
    }
  });
});

const hl24 = sittings['2024-hl'];
const higher2024 = BIO_HIGHER.filter(card => card.year === 2024) as unknown as ReviewedCard[];
const hl24ById = new Map(higher2024.map(card => [card.id, card]));
const hl24Verbatims = (id: string) => (hl24ById.get(id)!.rows as unknown as Array<{ verbatim: string }>)
  .map(row => row.verbatim);

describe('Biology 2024 Higher — reviewed sitting, corrected in place', () => {
  const review = hl24.review!;

  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(hl24.baseTaskCount).toBe(161);
    expect(hl24.cardCount).toBe(163);
    expect(higher2024).toHaveLength(163);
    expect(new Set(hl24.tasks.map(task => task.id))).toEqual(new Set(hl24ById.keys()));
  });

  it('keeps every shipped id but one aliased half-task', () => {
    expect(review.baselineCommit).toBe('913bc5e57');
    expect([review.verified.length, review.corrected.length, review.added.length,
      review.retained.length]).toEqual([13, 121, 29, 1]);
    for (const id of [...review.verified, ...review.corrected.map(c => c.id), ...review.added]) {
      expect(hl24ById.has(id), id).toBe(true);
    }
    // "Q8(b) [2 of 2]" was the second half of one printed task: withdrawn,
    // its progress carried to the card that now holds the whole task.
    expect(review.retained.map(r => r.id)).toEqual(['bio-2024-hl-q8-b2']);
    expect(hl24ById.has('bio-2024-hl-q8-b2')).toBe(false);
    expect(review.withdrawn['bio-2024-hl-q8-b2'].replacementId).toBe('bio-2024-hl-q8-b1');
    expect(hl24ById.get('bio-2024-hl-q8-b1')!.totalMarks).toBe(24);
  });

  it('records what each corrected card showed before', () => {
    for (const correction of review.corrected) {
      expect(correction.changed.length, correction.id).toBeGreaterThan(0);
      for (const field of correction.changed) {
        expect(field in correction.fieldsBefore, `${correction.id}.${field}`).toBe(true);
      }
    }
  });

  it('leaves the cards the review verified exactly as they shipped', () => {
    const verified = review.verified.map(id => hl24ById.get(id)!)
      .sort((a, b) => a.id.localeCompare(b.id));
    // The thirteen cards' shipped text is byte-identical to the deck before the review.
    expect(contentHash(verified)).toBe('3d2938daadbb4242c222fea584f63569c4abb13f8ba542d75752459d55761785');
  });

  it('pins the reviewed source PDFs', () => {
    expect(hl24.sources['038'].sha256)
      .toBe('9213c5666f1816378111bb526ed7c27294a6336e70869830a918835d9ea99937');
    expect(hl24.sources['040'].sha256)
      .toBe('876631d384f0a5b73573df1c4e628ba43504a744eb133c714cab54a0cf7708c0');
    expect(hl24.sources.scheme.sha256)
      .toBe('1ffe460a25c6636ca1a1e62ec9d7dfa4d796857d68c0ad74b4d201c9b2ccbf3b');
    expect([hl24.sources['038'].pages, hl24.sources['040'].pages, hl24.sources.scheme.pages])
      .toEqual([40, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of hl24.tasks) {
      const card = hl24ById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('adds up to the printed question totals', () => {
    const totals = new Map<number, number>();
    for (const task of hl24.tasks) {
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    expect(totals.get(1)).toBe(24);   // best five of six parts at 4
    // "6(3) + 2": seven responses each carded at 3, so 21 against the
    // ladder's 20; Q3 adds its separately priced (a) 3(1) to "5(3) + 2".
    for (const q of [2, 3, 4, 5, 7]) expect(totals.get(q), `Q${q}`).toBe(21);
    expect(totals.get(6)).toBe(20);   // 10(2)
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);   // any two of four 30s
  });

  it('cards a choice the scheme marks the same way as one card, not routes', () => {
    expect(Object.keys(hl24.routes)).toEqual([]);
    expect(higher2024.filter(card => card.questionRef.includes('Q10(b)'))).toHaveLength(2);
    // Q16(b)(ii) is not a choice: every gland is answered, one card per gland.
    expect(higher2024.filter(card => card.questionRef.startsWith('2024 HL Q16(b)(ii) — '))
      .map(card => card.questionRef.split(' — ')[1])).toEqual(['X', 'Y', 'Z']);
  });

  it('reads the true/false ticks from the scheme', () => {
    expect(['a', 'b', 'c', 'd', 'e', 'f', 'g'].map(x => hl24Verbatims(`bio-2024-hl-q5-${x}`)[0]))
      .toEqual(['False', 'False', 'True', 'False', 'False', 'True', 'True']);
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|graph|table)s?\b|\bthe food web\b/i;
    for (const card of higher2024) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // Q15(b)(i): the underlining that names the terms is shown as printed.
    expect(hl24ById.get('bio-2024-hl-q15-b-i')!.questionFigure).toBeTruthy();
    // Q13(b)(ii): the scheme's equation waits for the reveal.
    expect(hl24ById.get('bio-2024-hl-q13-b-ii')!.figure?.solution).toBe(true);
  });
});

const ol24 = sittings['2024-ol'];
const ordinary2024 = BIO_ORDINARY.filter(card => card.year === 2024) as unknown as ReviewedCard[];
const ol24ById = new Map(ordinary2024.map(card => [card.id, card]));
const ol24Verbatims = (id: string) => (ol24ById.get(id)!.rows as unknown as Array<{ verbatim: string }>)
  .map(row => row.verbatim);

describe('Biology 2024 Ordinary — reviewed sitting, corrected in place', () => {
  const review = ol24.review!;

  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(ol24.baseTaskCount).toBe(168);
    expect(ol24.cardCount).toBe(168);
    expect(ordinary2024).toHaveLength(168);
    expect(new Set(ol24.tasks.map(task => task.id))).toEqual(new Set(ol24ById.keys()));
  });

  it('keeps every shipped id', () => {
    expect(review.baselineCommit).toBe('89843f7fc');
    expect([review.verified.length, review.corrected.length, review.added.length,
      review.retained.length]).toEqual([2, 122, 44, 0]);
    for (const id of [...review.verified, ...review.corrected.map(c => c.id), ...review.added]) {
      expect(ol24ById.has(id), id).toBe(true);
    }
    // The old Q7 bundle keeps its id for (e), the one part no other card carried.
    expect(ol24ById.get('bio-2024-ol-q7')!.questionRef).toBe('2024 OL Q7(e)');
  });

  it('records what each corrected card showed before', () => {
    for (const correction of review.corrected) {
      expect(correction.changed.length, correction.id).toBeGreaterThan(0);
      for (const field of correction.changed) {
        expect(field in correction.fieldsBefore, `${correction.id}.${field}`).toBe(true);
      }
    }
  });

  it('leaves the cards the review verified exactly as they shipped', () => {
    const verified = review.verified.map(id => ol24ById.get(id)!)
      .sort((a, b) => a.id.localeCompare(b.id));
    expect(contentHash(verified)).toBe('46ffb8f2d7f4510041e66bc271717b060581feafc70de6fb58e397a253350309');
  });

  it('pins the reviewed source PDFs', () => {
    expect(ol24.sources['038'].sha256)
      .toBe('e43ae547650731087183ecf4db9973b152ab9748d0138311434d57e305b683a3');
    expect(ol24.sources['040'].sha256)
      .toBe('0650c443e91a40dd9834992584569e2ae98bdd076465136a7f2f4302b073ea56');
    expect(ol24.sources.scheme.sha256)
      .toBe('65393273ec12042cf99d3b8f2876bfd798fc7b03af5d8d1e0f57579d12171c19');
    expect([ol24.sources['038'].pages, ol24.sources['040'].pages, ol24.sources.scheme.pages])
      .toEqual([36, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of ol24.tasks) {
      const card = ol24ById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('adds up to the printed question totals', () => {
    const totals = new Map<number, number>();
    for (const task of ol24.tasks) {
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    for (const q of [1, 3, 4, 7]) expect(totals.get(q), `Q${q}`).toBe(20);
    // "6(3) + 2": seven responses each carded at 3; the ladder makes 20.
    for (const q of [2, 5, 6]) expect(totals.get(q), `Q${q}`).toBe(21);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);   // any two of four 30s
  });

  it('cards each choice the scheme marks on one set of rows as one card, not routes', () => {
    expect(Object.keys(ol24.routes)).toEqual([]);
    expect(ordinary2024.filter(card => card.questionRef.includes(' — '))).toHaveLength(0);
  });

  it('reads the true/false ticks from the scheme', () => {
    expect(['a', 'b', 'c', 'd', 'e', 'f', 'g'].map(x => ol24Verbatims(`bio-2024-ol-q6-${x}`)[0]))
      .toEqual(['True', 'True', 'False', 'False', 'True', 'True', 'False']);
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|graph|table|food web)s?\b|\bthe one shown\b/i;
    for (const card of ordinary2024) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // Q13(b)(iii): the blank square is set as printed; the scheme's completed square waits for the reveal.
    expect(ol24ById.get('bio-2024-ol-q13-b-iii')!.questionFigure).toBeTruthy();
    expect(ol24ById.get('bio-2024-ol-q13-b-iii')!.figure?.solution).toBe(true);
  });
});

const hl23 = sittings['2023-hl'];
const higher2023 = BIO_HIGHER.filter(card => card.year === 2023) as unknown as ReviewedCard[];
const hl23ById = new Map(higher2023.map(card => [card.id, card]));

describe('Biology 2023 Higher — reviewed sitting, corrected in place', () => {
  const review = hl23.review!;

  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(hl23.baseTaskCount).toBe(175);
    expect(hl23.cardCount).toBe(176);
    expect(higher2023).toHaveLength(176);
    expect(new Set(hl23.tasks.map(task => task.id))).toEqual(new Set(hl23ById.keys()));
  });

  it('keeps every shipped id', () => {
    expect(review.baselineCommit).toBe('38ac900f1');
    expect([review.verified.length, review.corrected.length, review.added.length,
      review.retained.length]).toEqual([8, 105, 63, 1]);
    for (const id of [...review.verified, ...review.corrected.map(c => c.id), ...review.added]) {
      expect(hl23ById.has(id), id).toBe(true);
    }
    // An authored figure twin of Q14(b)(ii) that the build never shipped:
    // withdrawn, with no progress to carry.
    expect(review.retained.map(r => r.id)).toEqual(['bio-2023-hl-q14-b-ii-fig']);
    expect(hl23ById.has('bio-2023-hl-q14-b-ii-fig')).toBe(false);
    expect(review.withdrawn['bio-2023-hl-q14-b-ii-fig'].replacementId).toBe('bio-2023-hl-q14-b-ii');
  });

  it('records what each corrected card showed before', () => {
    for (const correction of review.corrected) {
      expect(correction.changed.length, correction.id).toBeGreaterThan(0);
      for (const field of correction.changed) {
        expect(field in correction.fieldsBefore, `${correction.id}.${field}`).toBe(true);
      }
    }
  });

  it('leaves the cards the review verified exactly as they shipped', () => {
    const verified = review.verified.map(id => hl23ById.get(id)!)
      .sort((a, b) => a.id.localeCompare(b.id));
    expect(contentHash(verified)).toBe('7e218a6c8e726737a53d4545c4f5405477541832c7a1a31bbcd5e38f7660e056');
  });

  it('pins the reviewed source PDFs', () => {
    expect(hl23.sources['038'].sha256)
      .toBe('cf3498bf77ee4254096fdd1c5a63b4315d97fa5cdedf687c7f1154a308910c89');
    expect(hl23.sources['040'].sha256)
      .toBe('d310ce617cae60431a5fc07c3bbc63186855831632fe4f82777061c0b877774e');
    expect(hl23.sources.scheme.sha256)
      .toBe('a432f615ff7e154d91a2151aad138eb0cb1bc92e128097a31a2e573f1b8bf50d');
    expect([hl23.sources['038'].pages, hl23.sources['040'].pages, hl23.sources.scheme.pages])
      .toEqual([40, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of hl23.tasks) {
      const card = hl23ById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('prices Section A on its ordered splits', () => {
    const notation = (id: string) =>
      (hl23ById.get(id) as unknown as { tariffModel: { kind: string; notation?: string } }).tariffModel;
    expect(notation('bio-2023-hl-q1-a')).toEqual({ kind: 'orderedSplit', notation: '3(6) + 2(1)' });
    expect(notation('bio-2023-hl-q2-a')).toEqual({ kind: 'orderedSplit', notation: '2(5) + 5(2)' });
    expect(notation('bio-2023-hl-q7-a-ii')).toEqual({ kind: 'orderedSplit', notation: '4 + 2(1)' });
    expect(notation('bio-2023-hl-q7-b')).toEqual({ kind: 'orderedSplit', notation: '3(4) + 2(1)' });
  });

  it('adds up to the printed question totals', () => {
    const firstRoute = new Set(Object.values(hl23.routes).map(routes => routes[0]));
    const totals = new Map<number, number>();
    for (const task of hl23.tasks) {
      if (task.route && !firstRoute.has(task.route)) continue;   // one route per pool
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    // Section A cards each response at the ladder's first rate: Q1's six
    // parts at 6 ("3(6) + 2(1)" makes 20), seven responses at 5 for Q2-Q6
    // ("2(5) + 5(2)") and eight at 4 for Q7 ("4 + 2(1)" and "3(4) + 2(1)").
    expect(totals.get(1)).toBe(36);
    for (const q of [2, 3, 4, 5, 6]) expect(totals.get(q), `Q${q}`).toBe(35);
    expect(totals.get(7)).toBe(32);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(30);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(60);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(120);   // any two of four 30s
  });

  it('splits only the choice the scheme marks differently per option', () => {
    expect(Object.keys(hl23.routes)).toEqual(['Q17(d)(vi)']);
    expect(higher2023.filter(card => card.questionRef.startsWith('2023 HL Q17(d)(vi) — '))
      .map(card => card.questionRef.split(' — ')[1]).sort()).toEqual(['phloem', 'xylem']);
    // Paralysis or Parkinson's disease share one scheme row: one card.
    expect(higher2023.filter(card => card.questionRef.startsWith('2023 HL Q17(b)(vii)'))).toHaveLength(1);
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|picture|graph)s?\b|\bpedigree chart\b/i;
    for (const card of higher2023) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // The underlined terms, the reaction and the equation are set as printed;
    // the scheme's equation, cell, pyramid and outline wait for the reveal.
    for (const id of ['bio-2023-hl-q13-b-i', 'bio-2023-hl-q12-a-ii', 'bio-2023-hl-q12-b-v']) {
      expect(hl23ById.get(id)!.questionFigure, id).toBeTruthy();
    }
    for (const id of ['bio-2023-hl-q12-b-v', 'bio-2023-hl-q12-b-i', 'bio-2023-hl-q11-b-iv',
      'bio-2023-hl-q17-a-iii']) {
      expect(hl23ById.get(id)!.figure?.solution, id).toBe(true);
    }
  });
});

const ol23 = sittings['2023-ol'];
const ordinary2023 = BIO_ORDINARY.filter(card => card.year === 2023) as unknown as ReviewedCard[];
const ol23ById = new Map(ordinary2023.map(card => [card.id, card]));
const ol23Verbatims = (id: string) => (ol23ById.get(id)!.rows as unknown as Array<{ verbatim: string }>)
  .map(row => row.verbatim);

describe('Biology 2023 Ordinary — reviewed sitting, corrected in place', () => {
  const review = ol23.review!;

  it('ships every reviewed task, and nothing else, for the sitting', () => {
    expect(ol23.baseTaskCount).toBe(182);
    expect(ol23.cardCount).toBe(182);
    expect(ordinary2023).toHaveLength(182);
    expect(new Set(ol23.tasks.map(task => task.id))).toEqual(new Set(ol23ById.keys()));
  });

  it('keeps every shipped id', () => {
    expect(review.baselineCommit).toBe('985abf905');
    expect([review.verified.length, review.corrected.length, review.added.length,
      review.retained.length]).toEqual([1, 98, 83, 1]);
    for (const id of [...review.verified, ...review.corrected.map(c => c.id), ...review.added]) {
      expect(ol23ById.has(id), id).toBe(true);
    }
    // An authored figure twin of Q16(b)(ii)-(v) that the build never shipped:
    // withdrawn, with no progress to carry.
    expect(review.retained.map(r => r.id)).toEqual(['bio-2023-ol-q16b-ii-v-fig']);
    expect(ol23ById.has('bio-2023-ol-q16b-ii-v-fig')).toBe(false);
    expect(review.withdrawn['bio-2023-ol-q16b-ii-v-fig'].replacementId).toBe('bio-2023-ol-q16b-ii-v');
    // The old Q3 bundle keeps its id for Q3(a).
    expect(ol23ById.get('bio-2023-ol-q3')!.questionRef).toBe('2023 OL Q3(a)');
  });

  it('records what each corrected card showed before', () => {
    for (const correction of review.corrected) {
      expect(correction.changed.length, correction.id).toBeGreaterThan(0);
      for (const field of correction.changed) {
        expect(field in correction.fieldsBefore, `${correction.id}.${field}`).toBe(true);
      }
    }
  });

  it('leaves the card the review verified exactly as it shipped', () => {
    const verified = review.verified.map(id => ol23ById.get(id)!)
      .sort((a, b) => a.id.localeCompare(b.id));
    expect(contentHash(verified)).toBe('50ef6097f54aa139701902af956c98fcea41a08afa4242ed8425b7cfa75832e2');
  });

  it('pins the reviewed source PDFs', () => {
    expect(ol23.sources['038'].sha256)
      .toBe('94e4584df499b78bf8034587f98e4fd6175d98e327eccc775b9b94d907ae79ed');
    expect(ol23.sources['040'].sha256)
      .toBe('b7b1e3356bc87a0968d42babeb22788672b5e69892eaa4f3203b5a2d1aae0a75');
    expect(ol23.sources.scheme.sha256)
      .toBe('992f9b1ea2a29628f7bf8b547ab7a5f1a8b234a7823d5ac5c9ecb891e357e8ff');
    expect([ol23.sources['038'].pages, ol23.sources['040'].pages, ol23.sources.scheme.pages])
      .toEqual([40, 12, 36]);
  });

  it('carries each task at its published tariff, never a partial one', () => {
    for (const task of ol23.tasks) {
      const card = ol23ById.get(task.id)!;
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
    }
  });

  it('prices every part on the ordered split its scheme prints', () => {
    const notation = (id: string) =>
      (ol23ById.get(id) as unknown as { tariffModel: { kind: string; notation?: string } }).tariffModel;
    expect(ordinary2023.every(card =>
      (card as unknown as { tariffModel: { kind: string } }).tariffModel.kind === 'orderedSplit')).toBe(true);
    expect(notation('bio-2023-ol-q1-a')).toEqual({ kind: 'orderedSplit', notation: '2(7) + 3(2)' });
    expect(notation('bio-2023-ol-q2-a')).toEqual({ kind: 'orderedSplit', notation: '8 + 7 + 5(1)' });
    expect(notation('bio-2023-ol-q8-a')).toEqual({ kind: 'orderedSplit', notation: '5 + 1' });
    expect(notation('bio-2023-ol-q8-b-i')).toEqual({ kind: 'orderedSplit', notation: '2(9) + 6(1)' });
    expect(notation('bio-2023-ol-q11-a-i')).toEqual({ kind: 'orderedSplit', notation: '5 + 2(2)' });
    expect(notation('bio-2023-ol-q11-b-iv')).toEqual({ kind: 'orderedSplit', notation: '3(5) + 6(2)' });
    expect(notation('bio-2023-ol-q11-c-iv')).toEqual({ kind: 'orderedSplit', notation: '2(6) + 6(2)' });
    expect(notation('bio-2023-ol-q17-c-iii')).toEqual({ kind: 'orderedSplit', notation: '2(7) + 8(2)' });
  });

  it('adds up to the printed question totals at each ladder\'s first rate', () => {
    const totals = new Map<number, number>();
    for (const task of ol23.tasks) {
      const q = Number(/ Q(\d+)/.exec(task.questionRef)![1]);
      totals.set(q, (totals.get(q) ?? 0) + task.total);
    }
    // Each response is carded at its ladder's first rate: five at 7 for Q1
    // and Q3, seven at 8 for the "8 + 7 + 5(1)" questions; Section B 2 at 5
    // plus 8 at 9; Section C 3 at 5, 9 at 5 and 8 at 6; Q16 and Q17 ten at 7
    // in each of four parts. The ladders make 20, 30, 60 and 30 per part.
    for (const q of [1, 3]) expect(totals.get(q), `Q${q}`).toBe(35);
    for (const q of [2, 4, 5, 6, 7]) expect(totals.get(q), `Q${q}`).toBe(56);
    for (const q of [8, 9, 10]) expect(totals.get(q), `Q${q}`).toBe(82);
    for (const q of [11, 12, 13, 14, 15]) expect(totals.get(q), `Q${q}`).toBe(108);
    for (const q of [16, 17]) expect(totals.get(q), `Q${q}`).toBe(280);
  });

  it('cards the eye-or-ear choice the scheme marks on one set of rows as one card, not routes', () => {
    expect(Object.keys(ol23.routes)).toEqual([]);
    expect(ordinary2023.filter(card => card.questionRef.includes(' — '))).toHaveLength(0);
    expect(ordinary2023.filter(card => card.questionRef.startsWith('2023 OL Q16(b)(vii)'))).toHaveLength(1);
  });

  it('reads the true/false ticks from the scheme', () => {
    expect(['a', 'b', 'c', 'd', 'e', 'f', 'g'].map(x => ol23Verbatims(`bio-2023-ol-q2-${x}`)[0]))
      .toEqual(['True', 'False', 'False', 'True', 'True', 'True', 'False']);
  });

  it('shows the printed figure wherever the ask points at one', () => {
    const pointsAtPrint = /\b(the|this) (diagram|image|photograph|graph|table)s?\b|\bdata table\b|\bword equation\b/i;
    for (const card of ordinary2023) {
      const text = `${card.stem ?? ''} ${card.questionText}`;
      if (pointsAtPrint.test(text)) {
        expect(Boolean(card.figure || card.questionFigure || card.sourceMaterial), card.id).toBe(true);
      }
    }
    // The underlined terms and the table to complete are set as printed; the
    // scheme's completed table waits for the reveal.
    for (const id of ['bio-2023-ol-q12-b-i', 'bio-2023-ol-q13-c-i-iii', 'bio-2023-ol-q17-d-iv',
      'bio-2023-ol-q17-b-ii']) {
      expect(ol23ById.get(id)!.questionFigure, id).toBeTruthy();
    }
    expect(ol23ById.get('bio-2023-ol-q17-b-ii')!.figure?.solution).toBe(true);
  });
});
