/** @license SPDX-License-Identifier: Apache-2.0 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/english/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/english/ordinary';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import authoredJson from '../components/MarkBank/cards/english/authored.json';
import { generatedCardsForLevel } from '../components/MarkBank/cards/english/factory';
import publishedHigher from '../components/MarkBank/cards/english/published-higher.json';
import publishedOrdinary from '../components/MarkBank/cards/english/published-ordinary.json';
import {
  effectivePclmScores,
  pclmMarks,
  suggestPclmGrade,
} from '../components/MarkBank/SessionScreen';
import {
  isRubricCard,
  tariffReconciles,
  type CardSourceMaterial,
  type PclmRubric,
  type SecRubricCard,
} from '../types/markBank';

interface CensusAsk {
  id: string;
  year: number;
  level: 'hl' | 'ol';
  paper: 1 | 2;
  questionRef: string;
  printedParts: string[];
  status: 'authored' | 'queued';
}

interface EnglishCensus {
  paperCount: number;
  cardUnitCount: number;
  authoredCount: number;
  queuedCount: number;
  papers: Array<{ cardUnits: number; authored: number; queued: number }>;
  asks: CensusAsk[];
}

interface AuthoredCard {
  id: string;
  year: number;
  level: 'higher' | 'ordinary';
  paper: 1 | 2;
  questionRef: string;
  questionText: string;
  totalMarks: number;
  printedParts: string[];
  schemePage: number;
  schemeTraceScore: number;
  taskRequirements: string[];
  sourceMaterial?: CardSourceMaterial;
}

interface EnglishManifest {
  cardCount: number;
  cards: AuthoredCard[];
  withdrawnAliases: Record<string, string>;
}

const census = JSON.parse(readFileSync(
  resolve(__dirname, '../scripts/markbank/authored/english-census.json'),
  'utf8',
)) as EnglishCensus;
const manifest = authoredJson as unknown as EnglishManifest;
type EnglishCard = SecRubricCard & { rubric: PclmRubric };
// Reviewed full-corpus papers are published alongside the legacy manifest
// (see test/markBankEnglishPublished.test.ts). These legacy assertions cover
// the preserved 2021–2025 runtime cards, which must stay exactly as they were.
// A bridged paper (2025 HL P1/P2) is served by its reviewed published cards:
// each of its legacy ids is kept by that card or is a progress alias, which
// test/markBankEnglishPublished.test.ts proves; its legacy runtime card is gone.
const PUBLISHED_IDS = new Set([...publishedHigher.cards, ...publishedOrdinary.cards].map(card => card.id));
const BRIDGED = new Set([...publishedHigher.bridgedLegacyIds, ...publishedOrdinary.bridgedLegacyIds]);
const LEGACY_HIGHER = HIGHER.filter(card => !PUBLISHED_IDS.has(card.id));
const LEGACY_ORDINARY = ORDINARY.filter(card => !PUBLISHED_IDS.has(card.id));
const ALL = [...LEGACY_HIGHER, ...LEGACY_ORDINARY] as EnglishCard[];
const byId = new Map(ALL.map(card => [card.id, card]));
// Every legacy runtime card as the factory builds it, bridged or not: the PCLM
// scoring tests below exercise the factory and scorer, not which deck serves it.
const LEGACY_BUILT = new Map([...generatedCardsForLevel('higher'), ...generatedCardsForLevel('ordinary')]
  .map(card => [card.id, card as EnglishCard]));

const comparable = (value: string) => value
  .normalize('NFKC')
  .replace(/[‘’]/g, "'")
  .replace(/[“”]/g, '"')
  .replace(/[–—]/g, '-')
  .replace(/[^a-z0-9]+/gi, ' ')
  .trim()
  .toLowerCase();

const schemes = new Map<string, Map<number, string>>();
const schemePages = (card: AuthoredCard) => {
  const level = card.level === 'higher' ? 'hl' : 'ol';
  const key = String(card.year) + '-' + level;
  const cached = schemes.get(key);
  if (cached) return cached;
  const text = readFileSync(resolve(
    __dirname, '../examiner-reports/english/schemes/' + key + '.md'), 'utf8');
  const bits = text.split(/^## Page (\d+)\s*$/m);
  const pages = new Map<number, string>();
  for (let index = 1; index < bits.length; index += 2) {
    pages.set(Number(bits[index]), comparable(bits[index + 1]));
  }
  schemes.set(key, pages);
  return pages;
};

const sharedTraceScore = (card: AuthoredCard, questionText = card.questionText) => {
  const question = comparable(questionText);
  const words = question.split(' ');
  const width = Math.min(8, Math.max(4, words.length));
  const grams = Array.from(
    { length: Math.max(1, words.length - width + 1) },
    (_, index) => words.slice(index, index + width).join(' '),
  );
  const page = schemePages(card).get(card.schemePage) ?? '';
  const shared = grams.filter(gram => page.includes(gram)).length;
  return { shared, encoded: shared * 1000 + question.length };
};

const expectedPaperFileid = (card: AuthoredCard) =>
  'LC002' + (card.level === 'higher' ? 'A' : 'G')
  + 'LP' + (card.paper === 1 ? '100' : '200') + 'EV';

describe('English all-question census', () => {
  it('accounts for every paper and every independently selectable response', () => {
    expect(census.paperCount).toBe(20);
    expect(census.cardUnitCount).toBe(660);
    expect(census.asks).toHaveLength(660);
    expect(new Set(census.asks.map(ask => ask.id)).size).toBe(660);
    expect(census.papers.every(paper => paper.cardUnits === paper.authored + paper.queued)).toBe(true);
    expect(census.authoredCount).toBe(660);
    expect(census.queuedCount).toBe(0);
  });

  it('makes every printed choice explicit rather than silently omitting it', () => {
    const expectedPerPaper = new Map([
      ['hl-1', 19], ['ol-1', 22], ['hl-2', 23], ['ol-2', 68],
    ]);
    for (const year of [2021, 2022, 2023, 2024, 2025]) {
      for (const [key, count] of expectedPerPaper) {
        const [level, paper] = key.split('-');
        const asks = census.asks.filter(ask =>
          ask.year === year && ask.level === level && ask.paper === Number(paper));
        expect(asks, String(year) + ' ' + key).toHaveLength(count);
      }
      const ordinaryPrescribed = census.asks.filter(ask =>
        ask.year === year && ask.level === 'ol' && ask.paper === 2
        && ask.questionRef.includes('Prescribed Poetry'));
      expect(ordinaryPrescribed, String(year) + ' OL prescribed poetry').toHaveLength(24);
      for (const roman of ['i', 'ii', 'iii']) {
        expect(ordinaryPrescribed.filter(ask =>
          ask.questionRef.endsWith('Q2(' + roman + ')'))).toHaveLength(6);
      }
    }
  });

  it('maps all 660 authored tasks to 650 canonical practice identities', () => {
    const authored = census.asks.filter(ask => ask.status === 'authored');
    const canonicalAuthoredIds = [...new Set(authored.map(ask =>
      manifest.withdrawnAliases[ask.id] ?? ask.id))].sort();
    const bridgedAt = (level: 'higher' | 'ordinary') => manifest.cards
      .filter(card => card.level === level && BRIDGED.has(card.id)).length;
    expect(BRIDGED.size).toBeGreaterThanOrEqual(42);
    expect(LEGACY_HIGHER).toHaveLength(210 - bridgedAt('higher'));
    expect(LEGACY_ORDINARY).toHaveLength(440 - bridgedAt('ordinary'));
    expect(ALL).toHaveLength(650 - BRIDGED.size);
    expect(manifest.cardCount).toBe(650);
    expect(new Set(ALL.map(card => card.id)).size).toBe(650 - BRIDGED.size);
    expect(canonicalAuthoredIds).toHaveLength(650);
    expect([...ALL.map(card => card.id), ...BRIDGED].sort()).toEqual(canonicalAuthoredIds);
    expect(manifest.cards.map(card => card.id).sort()).toEqual(canonicalAuthoredIds);
    // Every census ask still reaches a live card, through an alias where bridged.
    const live = new Set([...HIGHER, ...ORDINARY].map(card => card.id));
    expect(authored.filter(ask => !live.has(CARD_ID_ALIASES[ask.id] ?? ask.id)).map(ask => ask.id)).toEqual([]);
  });

  it('keeps compulsory linked parts together while recording each separate tariff', () => {
    const examples = census.asks.filter(ask => ask.printedParts.length > 0);
    expect(examples.some(ask =>
      ask.id.endsWith('comparative-a-q1') && ask.printedParts.length === 2)).toBe(true);
    expect(examples.some(ask =>
      ask.id.endsWith('single-a-q1') && ask.printedParts.length === 3)).toBe(true);
    expect(examples.some(ask =>
      ask.id.endsWith('prescribed-a-q1') && ask.printedParts.length === 2)).toBe(true);
  });
});

describe('English prompt and source integrity', () => {
  it('traces every exact extracted prompt to its question-specific scheme page', () => {
    const weak: string[] = [];
    for (const authored of manifest.cards) {
      const trace = sharedTraceScore(authored);
      if (trace.shared === 0 || trace.encoded !== authored.schemeTraceScore) {
        weak.push(authored.questionRef + ' -> p.' + String(authored.schemePage));
      }
      if (BRIDGED.has(authored.id)) continue;
      const runtime = byId.get(authored.id)!;
      expect(runtime.questionRef, authored.id).toBe(authored.questionRef);
      expect(runtime.totalMarks, authored.id).toBe(authored.totalMarks);
      expect(runtime.paperFileid, authored.id).toBe(expectedPaperFileid(authored));
      expect(runtime.schemeCitation, authored.id).toContain('p.' + String(authored.schemePage));
      expect(runtime.questionText, authored.id).not.toMatch(
        /^(?:Leaving Certificate Examination\s+\d{4}|Copyright notice)|\bN\.?B\.?\s*$/i);

      if (runtime.qa.humanReviewedBy === 'corpus-verified') {
        expect(runtime.questionText, authored.id).toBe(authored.questionText);
      } else if (sharedTraceScore(authored, runtime.questionText).shared === 0) {
        weak.push(runtime.questionRef + ' hand-reviewed prompt -> p.'
          + String(authored.schemePage));
      }
    }
    expect(weak).toEqual([]);
  });

  it('attaches every required passage or poem to the official paper page', () => {
    const withSource = manifest.cards.filter(card => card.sourceMaterial);
    expect(withSource).toHaveLength(217);

    for (const authored of withSource.filter(card => !BRIDGED.has(card.id))) {
      const runtime = byId.get(authored.id)!;
      const source = runtime.sourceMaterial;
      expect(source, authored.questionRef).toBeDefined();
      expect(source?.kind, authored.questionRef).toBe('source-text');
      expect(source?.label, authored.questionRef).toBe(authored.sourceMaterial?.label);
      expect(source?.pages, authored.questionRef).toEqual(authored.sourceMaterial?.pages);
      expect(source?.pages.length, authored.questionRef).toBeGreaterThan(0);
      expect(source?.pages, authored.questionRef).toEqual(
        [...(source?.pages ?? [])].sort((left, right) => left - right));
      expect(new Set(source?.pages).size, authored.questionRef).toBe(source?.pages.length);
      expect((source?.title ?? '') + ' ' + (source?.attribution ?? ''), authored.questionRef)
        .not.toMatch(/the named poet|author named|unseen poem|poem [a-f]|marking scheme/i);
      expect(runtime.paperFileid, authored.questionRef).toBe(expectedPaperFileid(authored));
    }

    const unseen = manifest.cards.filter(card => card.questionRef.includes('Unseen Poetry'));
    expect(unseen).toHaveLength(20);
    expect(unseen.every(card => card.sourceMaterial)).toBe(true);

    const ordinaryPrescribed = manifest.cards.filter(card =>
      card.level === 'ordinary' && card.questionRef.includes('Prescribed Poetry'));
    expect(ordinaryPrescribed).toHaveLength(120);
    expect(ordinaryPrescribed.every(card => card.sourceMaterial)).toBe(true);

    const directlyDependentP1 = manifest.cards.filter(card =>
      /Paper 1 Text [1-3] QA/.test(card.questionRef)
      && /based on your reading|support your (?:answer|response) with reference to the text|with reference to the text(?: and images)?|above (?:text|article|passage|memoir)/i
        .test(card.questionText));
    expect(directlyDependentP1.length).toBeGreaterThan(30);
    expect(directlyDependentP1.filter(card => !card.sourceMaterial)
      .map(card => card.questionRef)).toEqual([]);

    const restoredContextDependentIds = [
      'english-2023-hl-p1-t1-a-iii',
      'english-2023-hl-p1-t2-a-ii',
      'english-2023-hl-p1-t2-a-iii',
      'english-2023-ol-p1-t2-a-ii',
      'english-2023-ol-p1-t2-a-iii-b',
      'english-2023-ol-p1-t3-a-ii',
      'english-2024-ol-p1-t1-a-ii',
      'english-2024-ol-p1-t1-a-iii-b',
      'english-2024-ol-p1-t2-a-ii',
      'english-2024-ol-p1-t3-a-iii-b',
    ];
    for (const id of restoredContextDependentIds) {
      const authored = manifest.cards.find(card => card.id === id);
      const runtime = byId.get(id);
      expect(authored?.sourceMaterial, id).toBeDefined();
      expect(runtime?.sourceMaterial, id).toBeDefined();
      expect(authored?.taskRequirements, id).toContain(
        'Read and use the official source material supplied with the card.');
    }
  });

  it('does not add a paper passage to self-contained writing choices', () => {
    const selfContained = manifest.cards.filter(card =>
      card.questionRef.includes(' Composing ')
      || card.questionRef.includes(' Text 1 QB')
      || card.questionRef.includes(' Text 2 QB')
      || card.questionRef.includes(' Text 3 QB'));
    expect(selfContained).toHaveLength(100);
    expect(selfContained.filter(card => card.sourceMaterial)
      .map(card => card.questionRef)).toEqual([]);
  });
});

describe('English PCLM cards', () => {
  it('uses only rubric cards, never fabricated exact-answer rows', () => {
    expect(ALL.every(isRubricCard)).toBe(true);
    expect(ALL.every(card => !('rows' in card))).toBe(true);
    expect(ALL.every(card =>
      card.rubric.indicativeMaterialNote.includes('none is a required answer'))).toBe(true);
  });

  it('reconciles every published grid to the printed total', () => {
    expect(ALL.filter(card => !tariffReconciles(card)).map(card => card.questionRef)).toEqual([]);
  });

  it('retains the 2021–2022 Ordinary Single Text adjustment and its published PCLM allocation', () => {
    const adjusted = ALL.filter(card => card.level === 'ordinary'
      && (card.year === 2021 || card.year === 2022)
      && card.questionRef.includes('Single Text'));
    // SEC Ordinary schemes, PDF p.19: all nine texts have four 35-mark
    // questions. Q1 is 10+10+15; Q2–4 use P=11,C=11,L=11,M=2. 72 legacy cards,
    // minus any now served by a bridged reviewed paper.
    const legacyAdjusted = manifest.cards.filter(card => card.level === 'ordinary'
      && (card.year === 2021 || card.year === 2022) && card.questionRef.includes('Single Text'));
    expect(legacyAdjusted).toHaveLength(72);
    expect(adjusted).toHaveLength(legacyAdjusted.filter(card => !BRIDGED.has(card.id)).length);
    for (const card of adjusted) {
      expect(card.totalMarks, card.id).toBe(35);
      const assessment = card.rubric.assessment;
      if (card.id.endsWith('-q1')) {
        expect(assessment.mode, card.id).toBe('composite');
        if (assessment.mode !== 'composite') throw new Error(card.id);
        expect(assessment.components.map(part => part.totalMarks), card.id).toEqual([10, 10, 15]);
      } else {
        expect(assessment.mode, card.id).toBe('discrete');
        if (assessment.mode !== 'discrete') throw new Error(card.id);
        expect(assessment.criteria.map(criterion => criterion.maxMarks), card.id).toEqual([11, 11, 11, 2]);
        expect(pclmMarks(card, { purpose: 11, coherence: 11, language: 11, mechanics: 2 }), card.id).toBe(35);
      }
    }
  });

  it('keeps Higher and Ordinary grade families separate', () => {
    for (const card of ALL) {
      const assessment = card.rubric.assessment;
      const bands = assessment.mode === 'composite'
        ? assessment.components.flatMap(component => component.bands)
        : assessment.bands;
      const prefix = card.level === 'higher' ? 'H' : 'O';
      expect(bands.every(band => band.grade.startsWith(prefix)), card.questionRef).toBe(true);
    }
  });

  it('preserves the SEC marking mode of every linked component', () => {
    const composites = ALL.filter(card => card.rubric.assessment.mode === 'composite');
    // The legacy manifest bundles 125 cards of linked parts (265 combined, 60
    // discrete). A bridged paper serves its parts as separate reviewed tasks.
    const linked = manifest.cards.filter(card => card.printedParts.length > 0);
    const parts = (cards: AuthoredCard[]) => cards.flatMap(card => card.printedParts
      .map(part => Number(part.match(/(\d+)\s+marks?$/i)![1])));
    expect([linked.length, parts(linked).filter(m => m <= 20).length, parts(linked).filter(m => m > 20).length])
      .toEqual([125, 265, 60]);
    const served = linked.filter(card => !BRIDGED.has(card.id));
    expect(composites).toHaveLength(served.length);
    const components = composites.flatMap(card => {
      const assessment = card.rubric.assessment;
      if (assessment.mode !== 'composite') throw new Error('unreachable');
      return assessment.components.map(component => ({ card, component }));
    });
    expect(components.filter(({ component }) => component.mode === 'combined'))
      .toHaveLength(parts(served).filter(m => m <= 20).length);
    expect(components.filter(({ component }) => component.mode === 'discrete'))
      .toHaveLength(parts(served).filter(m => m > 20).length);
    expect(components.filter(({ component }) => component.totalMarks <= 20
      && component.mode !== 'combined').map(({ card }) => card.questionRef)).toEqual([]);
    expect(components.filter(({ component }) => component.totalMarks > 20
      && component.mode !== 'discrete').map(({ card }) => card.questionRef)).toEqual([]);
  });

  it('enforces the primacy-of-Purpose cap independently of the renderer', () => {
    const card = [...LEGACY_BUILT.values()].find(entry =>
      entry.totalMarks === 50 && entry.rubric.assessment.mode === 'discrete')!;
    const scores = { purpose: 9, coherence: 15, language: 14, mechanics: 5 } as const;
    expect(effectivePclmScores(card, scores)).toEqual({
      purpose: 9, coherence: 9, language: 9, mechanics: 5,
    });
    expect(pclmMarks(card, scores)).toBe(32);
    expect(suggestPclmGrade(card, scores)).toBe('shaky');
  });

  it('uses one combined SEC grid for a short response', () => {
    const card = LEGACY_BUILT.get('english-2024-hl-p1-t1-a-i')!;
    expect(card.rubric.assessment.mode).toBe('combined');
    expect(pclmMarks(card, { combined: 12 })).toBe(12);
    expect(suggestPclmGrade(card, { combined: 12 })).toBe('got');
  });

  it('scores every compulsory linked part on its own grid', () => {
    const single = LEGACY_BUILT.get('english-2025-ol-p2-single-a-q1')!;
    expect(single.rubric.assessment.mode).toBe('composite');
    if (single.rubric.assessment.mode !== 'composite') throw new Error('unreachable');
    expect(single.rubric.assessment.components.map(component => [
      component.id, component.totalMarks, component.mode,
    ])).toEqual([
      ['a', 10, 'combined'], ['b', 10, 'combined'], ['c', 10, 'combined'],
    ]);
    expect(pclmMarks(single, {
      'component:a': 10, 'component:b': 8, 'component:c': 6,
    })).toBe(24);

    const comparative = LEGACY_BUILT.get('english-2025-ol-p2-comparative-a-q1')!;
    expect(comparative.rubric.assessment.mode).toBe('composite');
    if (comparative.rubric.assessment.mode !== 'composite') throw new Error('unreachable');
    expect(comparative.rubric.assessment.components.map(component => [
      component.id, component.totalMarks, component.mode,
    ])).toEqual([
      ['a-i', 15, 'combined'], ['a-ii', 15, 'combined'], ['b', 40, 'discrete'],
    ]);
    expect(pclmMarks(comparative, {
      'component:a-i': 14,
      'component:a-ii': 12,
      'component:b:purpose': 11,
      'component:b:coherence': 10,
      'component:b:language': 10,
      'component:b:mechanics': 4,
    })).toBe(61);

    expect(effectivePclmScores(comparative, {
      'component:b:purpose': 8,
      'component:b:coherence': 12,
      'component:b:language': 11,
      'component:b:mechanics': 4,
    })).toMatchObject({
      'component:b:purpose': 8,
      'component:b:coherence': 8,
      'component:b:language': 8,
      'component:b:mechanics': 4,
    });

    const higherComparative = LEGACY_BUILT.get('english-2024-hl-p2-comparative-a-q1')!;
    expect(higherComparative.rubric.assessment.mode).toBe('composite');
    if (higherComparative.rubric.assessment.mode !== 'composite') throw new Error('unreachable');
    expect(higherComparative.rubric.assessment.components.map(component => [
      component.totalMarks, component.mode,
    ])).toEqual([[30, 'discrete'], [40, 'discrete']]);
  });
});
