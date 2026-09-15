/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ways In — the key parts of a question.
 *
 * On three cards in four the old planner handed the student the question
 * back one sentence at a time. The breakdown replaces that with the job, how
 * many, what it is about, the limits and the material to use — and the whole
 * point of showing it before the marking scheme rests on one rule: every slot
 * is lifted from the printed paper. These tests hold that rule across every
 * built card, not a sample, and pin the cases a student meets most.
 */
/// <reference types="vite/client" />
import { describe, expect, test } from 'vitest';
import { buildKeyParts, planRowsFor, type KPSpan } from '@/components/WaysIn/keyParts';
import { buildQuestionModel } from '@/components/WaysIn/questionModel';
import { waysInSourceFromMarkBank } from '@/components/WaysIn/sources';
import type { WaysInQuestionSource } from '@/components/WaysIn/types';

// Every built deck, discovered rather than listed, so a new subject is
// checked the day it ships.
const decks = import.meta.glob('/components/MarkBank/cards/*/*.ts', { eager: true }) as Record<string, { CARDS?: readonly any[] }>;
const corpus = Object.entries(decks).flatMap(([path, mod]) => (mod.CARDS ?? []).map(card => {
  const subject = path.split('/').at(-2) ?? '';
  const source = waysInSourceFromMarkBank(card, subject);
  return { card, subject, source, kp: buildKeyParts(source) };
}));
const byId = new Map(corpus.map(entry => [entry.card.id as string, entry]));

const source = (questionText: string, extra: Partial<WaysInQuestionSource> = {}): WaysInQuestionSource => ({
  id: 'test', origin: 'mark-bank', subjectLabel: 'Test', questionRef: '', questionText,
  answerShape: {}, textConfidence: 'verified', sourceLabel: '', ...extra,
});
const slots = (u: ReturnType<typeof buildKeyParts>['units'][number]) => ({
  do: u.action?.display, n: u.count?.display ?? '', about: u.focus?.display ?? '',
  if: u.conditions.map(c => c.display), use: u.use.map(x => x.display),
});

describe('key parts across every built card', () => {
  test('reads the whole bank', () => {
    expect(corpus.length).toBeGreaterThan(15000);
  });

  test('every slot is lifted verbatim from the printed stem or question', () => {
    const unlifted: string[] = [];
    for (const { card, source: s, kp } of corpus) {
      const raw = { q: s.questionText ?? '', stem: s.stem ?? '' };
      const spans: KPSpan[] = [
        ...kp.cardRules,
        ...kp.units.flatMap(u => [u.action, u.count, u.focus, ...(u.sides ?? []), ...u.conditions, ...u.use]
          .filter((x): x is KPSpan => Boolean(x))),
      ];
      for (const span of spans) {
        const printed = raw[span.from].slice(span.start, span.end);
        if (printed !== span.text || span.display !== span.text.replace(/\s+/g, ' ').trim()) {
          unlifted.push(`${card.id}: “${span.display}”`);
        }
      }
    }
    expect(unlifted.slice(0, 10)).toEqual([]);
  });

  test('every part it shows has a job to do, or is shown exactly as printed', () => {
    const jobless = corpus.flatMap(({ card, kp }) => kp.units.filter(u => !u.action && !u.flags.includes('as-printed')).map(() => card.id));
    expect(jobless.slice(0, 10)).toEqual([]);
    // Showing a part as printed is the honest fallback, not the norm.
    const all = corpus.flatMap(({ kp }) => kp.units);
    const printed = all.filter(u => u.flags.includes('as-printed'));
    expect(printed.length / all.length).toBeLessThan(0.03);
  });

  test('breaks down at least nine English-language cards in ten', () => {
    const english = corpus.filter(({ kp }) => !kp.reasons.includes('non-english'));
    const broken = english.filter(({ kp }) => kp.mode === 'decomposed');
    expect(broken.length / english.length).toBeGreaterThanOrEqual(0.9);
  });

  test('never plans more than eight spaces', () => {
    const over = corpus.filter(({ source: s, kp }) => {
      const m = buildQuestionModel(s);
      return planRowsFor(kp, { basis: m.planShape.basis, prompts: m.planPrompts }).length > 8;
    });
    expect(over.map(({ card }) => card.id).slice(0, 5)).toEqual([]);
  });
});

describe('the parts a student meets most', () => {
  test('Geography 2021 HL: the job, the count, the thing, and the limit that decides it', () => {
    const entry = byId.get('geography-2021-hl-p1-q2');
    expect(entry).toBeDefined();
    const units = entry!.kp.units.map(slots);
    expect(units.map(u => u.do)).toEqual(['Match', 'Name', 'Name']);
    expect(units[0]).toMatchObject({ n: 'each of the letters A, B, C and D', use: ['the table below'] });
    expect(units[1]).toMatchObject({ n: 'one example', about: 'a mountain range formed by folding', if: ['found outside of Ireland'] });
    expect(units[2]).toMatchObject({ about: 'the type of plate boundary', use: ['the diagram above'] });
  });

  test('“Name and explain” is two jobs about one thing', () => {
    const kp = buildKeyParts(source('Name and explain one method of soil conservation used in Ireland.'));
    expect(kp.units.map(u => u.action?.display)).toEqual(['Name', 'explain']);
    expect(kp.units.every(u => u.focus?.display === kp.units[1].focus?.display)).toBe(true);
  });

  test('a distinction names both sides', () => {
    const [unit] = buildKeyParts(source('Distinguish between artisan produce and a niche market.')).units;
    expect(unit.action?.display).toBe('Distinguish between');
    expect(unit.sides?.map(s => s.display)).toEqual(['artisan produce', 'a niche market']);
  });

  test('a calculation lists the printed values but never the quantity it asks for', () => {
    const kp = buildKeyParts(source('The astronaut’s mass is 85 kg. Calculate the astronaut’s weight on Earth.', {
      stem: 'The acceleration due to gravity on Earth is 9.8 m s−2.',
    }));
    const [unit] = kp.units;
    expect(unit.action?.display).toBe('Calculate');
    expect(unit.use.filter(u => u.kind === 'given').map(u => u.display).join(' | ')).toMatch(/9\.8 m s/);
    expect(unit.flags).not.toContain('values-on-paper');
  });

  test('a calculation with no values on the card says where they are', () => {
    const [unit] = buildKeyParts(source('Calculate the total cost of operating the bakery for the week.')).units;
    expect(unit.flags).toContain('values-on-paper');
  });

  test('printed alternatives are kept apart and marked', () => {
    const kp = buildKeyParts(source('Outline one method of securely holding ferrous metals.\nOR\nDescribe automatic tool change.'));
    expect(kp.banner).toBe('answer-one-alt');
    expect(kp.units.map(u => u.altGroup)).toEqual(['A', 'B']);
  });

  test('a lead-in gives its instruction to every printed item', () => {
    const kp = buildKeyParts(source('1. The male parts of the flower. 2. The female parts of the flower.', { stem: 'Give the collective name for:' }));
    expect(kp.units.map(u => [u.ref, u.action?.display, u.focus?.display, u.item?.display])).toEqual([
      ['1.', 'Give', 'the collective name for', 'The male parts of the flower'],
      ['2.', 'Give', 'the collective name for', 'The female parts of the flower'],
    ]);
  });

  test('a question in the exam language is left as printed, not guessed at', () => {
    const kp = buildKeyParts(source('Qu’est-ce qui a empêché Marie-Solène de dire au revoir à ses élèves ? (Section 1)'));
    expect(kp.mode).not.toBe('decomposed');
    expect(kp.reasons).toContain('non-english');
  });

  test('a single part keeps the printed count of spaces', () => {
    const s = source('Name the parts labelled A and B.');
    const kp = buildKeyParts(s);
    const m = buildQuestionModel(s);
    expect(planRowsFor(kp, { basis: m.planShape.basis, prompts: m.planPrompts })).toHaveLength(2);
  });
});
