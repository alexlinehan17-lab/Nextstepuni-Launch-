/** @license SPDX-License-Identifier: Apache-2.0 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/english/higher';
import {
  effectivePclmScores,
  pclmMarks,
  suggestPclmGrade,
} from '../components/MarkBank/SessionScreen';
import { isRubricCard, tariffReconciles } from '../types/markBank';

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

const census = JSON.parse(readFileSync(
  resolve(__dirname, '../scripts/markbank/authored/english-census.json'),
  'utf8',
)) as EnglishCensus;

const comparable = (value: string) => value
  .normalize('NFKC')
  .replace(/[‘’]/g, "'")
  .replace(/[“”]/g, '"')
  .replace(/[–—]/g, '-')
  .replace(/\s+/g, ' ')
  .trim()
  .toLowerCase();

describe('English all-question census', () => {
  it('accounts for every paper and every independently selectable response', () => {
    expect(census.paperCount).toBe(20);
    expect(census.cardUnitCount).toBe(630);
    expect(census.asks).toHaveLength(630);
    expect(new Set(census.asks.map(ask => ask.id)).size).toBe(630);
    expect(census.papers.every(paper => paper.cardUnits === paper.authored + paper.queued)).toBe(true);
    expect(census.authoredCount + census.queuedCount).toBe(630);
  });

  it('makes every printed choice explicit rather than silently omitting it', () => {
    const expectedPerPaper = new Map([
      ['hl-1', 19], ['ol-1', 22], ['hl-2', 23], ['ol-2', 62],
    ]);
    for (const year of [2021, 2022, 2023, 2024, 2025]) {
      for (const [key, count] of expectedPerPaper) {
        const [level, paper] = key.split('-');
        const asks = census.asks.filter(ask =>
          ask.year === year && ask.level === level && ask.paper === Number(paper));
        expect(asks, `${year} ${key}`).toHaveLength(count);
      }
    }
  });

  it('maps every live card one-to-one to an authored census ask', () => {
    const authored = census.asks.filter(ask => ask.status === 'authored');
    expect(authored).toHaveLength(19);
    expect(CARDS).toHaveLength(19);
    expect(CARDS.map(card => card.id).sort()).toEqual(authored.map(ask => ask.id).sort());
    expect(authored.every(ask => ask.year === 2025 && ask.level === 'hl' && ask.paper === 1)).toBe(true);
  });

  it('does not lose composite printed subparts inside a holistic card', () => {
    const examples = census.asks.filter(ask => ask.printedParts.length > 0);
    expect(examples.length).toBeGreaterThan(0);
    expect(examples.some(ask => ask.id.endsWith('comparative-a-q1') && ask.printedParts.length === 2)).toBe(true);
    expect(examples.some(ask => ask.id.endsWith('single-a-q1') && ask.printedParts.length === 3)).toBe(true);
  });
});

describe('English PCLM cards', () => {
  it('traces every exact prompt to the reviewed SEC scheme extract', () => {
    const scheme = comparable(readFileSync(
      resolve(__dirname, '../examiner-reports/english/schemes/2025-hl.md'),
      'utf8',
    ));
    expect(CARDS.filter(card => !scheme.includes(comparable(card.questionText)))
      .map(card => card.questionRef)).toEqual([]);
  });

  it('uses only the rubric variant and never answer rows', () => {
    expect(CARDS.every(isRubricCard)).toBe(true);
    expect(CARDS.every(card => !('rows' in card))).toBe(true);
    expect(CARDS.every(card => card.rubric.indicativeMaterialNote.includes('none is a required answer'))).toBe(true);
  });

  it('reconciles every published grid to the printed total', () => {
    expect(CARDS.filter(card => !tariffReconciles(card)).map(card => card.questionRef)).toEqual([]);
  });

  it('enforces the primacy-of-Purpose cap independently of the renderer', () => {
    const card = CARDS.find(entry => entry.totalMarks === 50)!;
    const scores = { purpose: 9, coherence: 15, language: 14, mechanics: 5 } as const;
    expect(effectivePclmScores(card, scores)).toEqual({
      purpose: 9, coherence: 9, language: 9, mechanics: 5,
    });
    expect(pclmMarks(card, scores)).toBe(32);
    expect(suggestPclmGrade(card, scores)).toBe('shaky');
  });

  it('uses the combined SEC grid for short comprehension answers', () => {
    const card = CARDS.find(entry => entry.totalMarks === 15)!;
    expect(card.rubric.assessment.mode).toBe('combined');
    expect(pclmMarks(card, { combined: 12 })).toBe(12);
    expect(suggestPclmGrade(card, { combined: 12 })).toBe('got');
  });
});
