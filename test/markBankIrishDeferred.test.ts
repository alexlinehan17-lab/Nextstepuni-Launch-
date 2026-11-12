/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The SEC's deferred Irish sittings, carded in the June shape (scripts/markbank/authoring/irish_deferred.py, 2026-11-12).
 * Each card is the June card's shape for its paper layout, cites "… — Deferred sitting", opens its deferred paper and
 * cites its deferred scheme, and its manifest lists the census asks it covers (paper_census.census_irish_deferred,
 * test/irishDeferredCensus.test.ts). The deferred schemes print no key for some options (the optional prose and poetry;
 * Higher 4C and 4E): those cards say so and are marked by what the scheme does print (its band tables and directions)
 * or, where it prints nothing, at the paper's printed tariffs.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import higher2025 from '../components/MarkBank/cards/irish/higher-2025-deferred-authored.json';
import { listeningExerciseKey } from '../components/MarkBank/sessionPlanning';
import type { IrishCriterion, SecRubricCard } from '../types/markBank';

interface Manifest { covers: Record<string, string[]>; cards: { id: string; criteria: unknown[] }[] }
interface Shape { listening: number; composition: number; wholeReading: number; readingParts: number; readingSlots: number; literature: number; literatureParts: number }
interface Sitting { file: Manifest; cards: number; asks: number; shape: Shape; unprinted: string[]; byTable: string[] }

// Per sitting: its cards, the census asks they cover (the denominator), the card shape for its layout, and the options
// its scheme prints no key for.
const SITTINGS: Record<string, Sitting> = {
  'higher 2025': { file: higher2025 as Manifest, cards: 99, asks: 90,
    shape: { listening: 8, composition: 9, wholeReading: 12, readingParts: 34, readingSlots: 22, literature: 14, literatureParts: 0 },
    unprinted: ['poetry-3b-a', 'poetry-3b-b'], byTable: ['literature-4-c', 'literature-4-e', 'prose-2b-a', 'prose-2b-b'] },
};

const DEFERRED = /^irish-(\d{4})-(hl|ol)-deferred-p([12])-/;
const deck = [...HIGHER, ...ORDINARY].filter(card => DEFERRED.test(card.id)) as SecRubricCard[];
const rubric = (card: SecRubricCard) => card.rubric as unknown as { criteria: IrishCriterion[]; markingGuideNote: string };
const criteria = (card: SecRubricCard) => rubric(card).criteria;
const key = (card: { id: string }) => card.id.replace(DEFERRED, '');
const name = (card: SecRubricCard) => `${card.level} ${card.year}`;
const entries = Object.entries(SITTINGS);

describe('Irish deferred sittings: the June shape', () => {
  it('ships every card of the carded sittings, and nothing else under a deferred id', () => {
    const files = entries.flatMap(([, sitting]) => sitting.file.cards);
    expect(deck.map(card => card.id).sort()).toEqual(files.map(card => card.id).sort());
    expect(new Set(files.map(card => card.id)).size).toBe(files.length);
    for (const [sittingName, sitting] of entries) {
      expect(sitting.file.cards, sittingName).toHaveLength(sitting.cards);
      expect(deck.filter(card => name(card) === sittingName), sittingName).toHaveLength(sitting.cards);
    }
  });

  it('says it is the deferred sitting twice, and opens its own paper and scheme', () => {
    for (const card of deck) {
      const [, year, level, paper] = card.id.match(DEFERRED)!;
      expect(Number(year)).toBe(card.year);
      expect(card.questionRef.startsWith(`${year} ${level.toUpperCase()} Paper ${paper} `), card.id).toBe(true);
      expect(card.questionRef.endsWith(' — Deferred sitting'), card.id).toBe(true);
      expect(card.paperFileid).toBe(`LC001${level === 'hl' ? 'A' : 'G'}LP${paper}00IV-deferred`);
      expect(card.schemeCitation).toMatch(new RegExp(`^SEC Gaeilge (?:Ardleibhéal|Gnáthleibhéal) deferred marking scheme ${year}, p\\.\\d+`));
      expect(card.qa.humanReviewedAt).toBe('2026-11-12');
    }
  });

  it('cards each paper layout as June does: extracts, titles, whole questions with their parts, options', () => {
    for (const [sittingName, sitting] of entries) {
      const cards = deck.filter(card => name(card) === sittingName);
      const of = (pattern: RegExp) => cards.filter(card => pattern.test(key(card))).length;
      expect({
        listening: of(/^listening-/), composition: of(/^composition-/), wholeReading: of(/^reading-[ab]-q\d$/),
        readingParts: of(/^reading-[ab]-q\d-(?:a|b|bi|bii)$/), readingSlots: of(/^reading-[ab]-q\d-(?:bi|bii|b)-\d$/),
        literature: of(/^(?:prose|poetry|literature)-(?:\d[ab]|4)-[a-f](?:-(?:caca-milis|an-lasair-choille))?$/),
        literatureParts: of(/^(?:prose|poetry)-\d[ab]-[a-c](?:-(?:caca-milis|an-lasair-choille))?-(?:i|ii|iii|iv|v)(?:-[a-d])?$/),
      }, sittingName).toEqual(sitting.shape);
    }
  });

  it('marks each printed listening question as its own criterion, and covers every census ask once at least', () => {
    for (const [sittingName, sitting] of entries) {
      for (const card of sitting.file.cards.filter(c => key(c).startsWith('listening-'))) {
        expect(sitting.file.covers[card.id], card.id).toHaveLength(card.criteria.length);
      }
      expect(Object.keys(sitting.file.covers).sort(), sittingName).toEqual(sitting.file.cards.map(card => card.id).sort());
      expect(new Set(Object.values(sitting.file.covers).flat()).size, sittingName).toBe(sitting.asks);
    }
  });

  it('plays the SEC’s deferred recording on every listening card, its own exercise apart from June’s', () => {
    for (const card of deck) {
      const listening = key(card).startsWith('listening-');
      expect(Boolean(card.audioMaterial), card.id).toBe(listening);
      if (listening) expect(card.audioMaterial!.playbackUrl).toBe(`https://www.examinations.ie/archive/deferredexams/${card.year}/LC001ZLP017IV.mp3`);
    }
    for (const card of deck.filter(c => key(c) === 'listening-a-f1')) {
      const june = [...HIGHER, ...ORDINARY].find(c => c.id === card.id.replace('-deferred-', '-'))!;
      expect(listeningExerciseKey(card)).not.toBe(listeningExerciseKey(june));
    }
  });

  it('makes every priced answer a claimable row', () => {
    const priced = (criterion: IrishCriterion) => criterion.guidanceKind !== 'quality'
      && criterion.guidance.some(line => /\d+\s*m?h?arc\b/.test(line));
    const rowless = deck.flatMap(card => criteria(card).filter(criterion => priced(criterion) && !criterion.allocation)
      .map(criterion => `${card.id} ${criterion.id}`));
    expect(rowless).toEqual([]);
  });

  it('says where the deferred scheme prints no key, and marks those options by what it prints', () => {
    for (const [sittingName, sitting] of entries) {
      const cards = deck.filter(card => name(card) === sittingName);
      expect(cards.filter(card => rubric(card).markingGuideNote.startsWith('The scheme prints no answer for this part.'))
        .map(key).sort(), sittingName).toEqual(sitting.unprinted);
      // The Higher optional prose and Ceist 4C/4E: the scheme's band table and Ceist 4's directions are their marking.
      expect(cards.filter(card => /prints no notes/.test(rubric(card).markingGuideNote)).map(key).sort(), sittingName).toEqual(sitting.byTable);
    }
  });
});
