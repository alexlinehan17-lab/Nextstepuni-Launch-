/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The SEC's deferred Irish sittings, carded in the June shape (scripts/markbank/authoring/irish_deferred.py, 2026-11-12).
 * Each card is the June card's shape for its paper layout, cites "… — Deferred sitting", opens its deferred paper and
 * cites its deferred scheme, and its manifest lists the census asks it covers (paper_census.census_irish_deferred,
 * test/irishDeferredCensus.test.ts). The 2024 and 2025 deferred schemes print no key for some options (the optional
 * prose and poetry; Higher 4C and 4E), and 2022's restates its Higher optional prose and 4A–4E without notes: those
 * cards say so and are marked by what the scheme does print (its band tables and directions) or, where it prints
 * nothing, at the paper's printed tariffs. The 2023 and 2022 Ordinary schemes key every optional option, so those cards
 * carry the scheme's own lines, the title row and the deduction printed under each.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import higher2025 from '../components/MarkBank/cards/irish/higher-2025-deferred-authored.json';
import ordinary2025 from '../components/MarkBank/cards/irish/ordinary-2025-deferred-authored.json';
import higher2024 from '../components/MarkBank/cards/irish/higher-2024-deferred-authored.json';
import ordinary2024 from '../components/MarkBank/cards/irish/ordinary-2024-deferred-authored.json';
import higher2023 from '../components/MarkBank/cards/irish/higher-2023-deferred-authored.json';
import { listeningExerciseKey } from '../components/MarkBank/sessionPlanning';
import type { IrishCriterion, SecRubricCard } from '../types/markBank';

interface Manifest { covers: Record<string, string[]>; cards: { id: string; criteria: unknown[] }[] }
interface Shape { listening: number; composition: number; wholeReading: number; readingParts: number; readingSlots: number; literature: number; literatureParts: number }
// Where an Ordinary option has no key, the 0-4 Gaeilge deduction applies only if the scheme prints it for the whole
// question ('question', with the page's own words), never when it is printed under the keyed options alone ('none').
// keyedOptional: an Ordinary scheme that keys its optional prose and poetry (2023, 2022), each option with its own deduction.
interface Sitting { file: Manifest; cards: number; asks: number; shape: Shape; unprinted: string[]; byTable: string[]; deduction?: 'none' | 'question'; keyedOptional?: boolean }

// Per sitting: its cards, the census asks they cover (the denominator), the card shape for its layout, and the options
// its scheme prints no key for.
const SITTINGS: Record<string, Sitting> = {
  'higher 2025': { file: higher2025 as Manifest, cards: 99, asks: 90,
    shape: { listening: 8, composition: 9, wholeReading: 12, readingParts: 34, readingSlots: 22, literature: 14, literatureParts: 0 },
    unprinted: ['poetry-3b-a', 'poetry-3b-b'], byTable: ['literature-4-c', 'literature-4-e', 'prose-2b-a', 'prose-2b-b'] },
  'ordinary 2025': { file: ordinary2025 as Manifest, cards: 76, asks: 80,
    shape: { listening: 6, composition: 9, wholeReading: 10, readingParts: 20, readingSlots: 0, literature: 13, literatureParts: 18 },
    unprinted: ['poetry-3b-a', 'poetry-3b-b', 'poetry-3b-c', 'prose-2a-c-an-lasair-choille', 'prose-2b-a', 'prose-2b-b', 'prose-2b-c'], byTable: [], deduction: 'none' },
  'higher 2024': { file: higher2024 as Manifest, cards: 90, asks: 91,
    shape: { listening: 8, composition: 9, wholeReading: 12, readingParts: 34, readingSlots: 12, literature: 15, literatureParts: 0 },
    unprinted: ['poetry-3b-a', 'poetry-3b-b'], byTable: ['literature-4-c', 'literature-4-e', 'prose-2b-a', 'prose-2b-b'] },
  'ordinary 2024': { file: ordinary2024 as Manifest, cards: 74, asks: 79,
    shape: { listening: 6, composition: 9, wholeReading: 10, readingParts: 20, readingSlots: 0, literature: 12, literatureParts: 17 },
    unprinted: ['poetry-3b-a', 'poetry-3b-b', 'poetry-3b-c', 'prose-2b-a', 'prose-2b-b', 'prose-2b-c'], byTable: [], deduction: 'question' },
  'higher 2023': { file: higher2023 as Manifest, cards: 91, asks: 91,
    shape: { listening: 8, composition: 9, wholeReading: 12, readingParts: 34, readingSlots: 14, literature: 14, literatureParts: 0 },
    unprinted: [], byTable: ['prose-2b-a', 'prose-2b-b'] },
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
      if (sitting.keyedOptional) {
        // Each optional option carries the scheme's lines, the title row it prices, and the deduction printed under it.
        for (const card of cards.filter(c => /^(?:prose-2b|poetry-3b)-[a-c]$/.test(key(c)))) {
          const ids = criteria(card).map(criterion => criterion.id);
          expect(ids, card.id).toContain('teideal');
          expect(criteria(card).filter(criterion => criterion.kind === 'deduction').map(d => d.guidance.join(' ')), card.id)
            .toEqual([expect.stringMatching(/^\[Gaeilge lochtach: 0[-‐]4 a bhaint den iomlán a gnóthaíodh\.?\]$/)]);
        }
      }
      if (!sitting.deduction) continue;
      for (const card of cards.filter(c => sitting.unprinted.includes(key(c)))) {
        const deductions = criteria(card).filter(criterion => criterion.kind === 'deduction');
        if (sitting.deduction === 'none') expect(deductions, card.id).toEqual([]);
        else expect(deductions.map(d => d.guidance.join(' ')), card.id).toEqual([expect.stringMatching(/^Ceist [23]: An (?:Prós|Fhilíocht) - .*\[Gaeilge lochtach: 0 - 4 a bhaint den iomlán a gnóthaíodh\]$/)]);
      }
    }
  });
});
