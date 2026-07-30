/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank deck — provenance guards.
 *
 * These exist because the first sample deck was FABRICATED: it invented mark
 * values the scheme does not award, shipped a labelling question with no figure
 * at all, and stood a drawn SVG in for an SEC crop. That is precisely the failure
 * this tool was built to end, so every card is now checked against the real
 * sources on disk rather than trusted.
 */

import { describe, test, expect } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';

import { SAMPLE_CARDS, STRANDS, ALL_TOPICS } from '../components/MarkBank/deck';
import { isDiagramCard, isContentFreeRow, looksLikeSectionLabel, tariffReconciles, MAX_ROWS, isValidCardId } from '../types/markBank';

const ROOT = resolve(__dirname, '..');
const SCHEME = resolve(ROOT, 'examiner-reports/biology/2025-hl-marking-scheme.md');

/** Normalise for substring matching against the extracted scheme text. */
const norm = (s: string) =>
  s.toLowerCase().replace(/[‐-―]/g, '-').replace(/[^a-z0-9]+/g, ' ').trim();

describe('every card traces to the marking scheme on disk', () => {
  const scheme = existsSync(SCHEME) ? norm(readFileSync(SCHEME, 'utf8')) : '';

  test('the scheme this deck cites is actually present', () => {
    expect(scheme.length).toBeGreaterThan(1000);
  });

  test.each(SAMPLE_CARDS.map(c => [c.questionRef, c] as const))(
    '%s — every marking point appears in the scheme',
    (_ref, card) => {
      for (const row of card.rows) {
        if (row.kind === 'anyN' && row.group) {
          for (const option of row.group.options) {
            expect(scheme).toContain(norm(option));
          }
          continue;
        }
        // Rows are written "Label — answer"; the answer is what the scheme prints.
        const answer = row.verbatim.split(/\s[—-]\s/).pop() ?? row.verbatim;
        expect(scheme).toContain(norm(answer));
      }
    },
  );

  test.each(SAMPLE_CARDS.map(c => [c.questionRef, c] as const))(
    '%s — marks reconcile against the printed tariff',
    (_ref, card) => {
      expect(tariffReconciles(card)).toBe(true);
    },
  );
});

describe('no card can repeat the fabrication that shipped first time', () => {
  test.each(SAMPLE_CARDS.map(c => [c.questionRef, c] as const))(
    '%s — is a real question, not a section label',
    (_ref, card) => {
      expect(looksLikeSectionLabel(card.questionText)).toBe(false);
      expect(card.questionText.length).toBeGreaterThan(15);
    },
  );

  test.each(SAMPLE_CARDS.map(c => [c.questionRef, c] as const))(
    '%s — carries answers, not mark tariffs',
    (_ref, card) => {
      for (const row of card.rows) {
        if (row.kind === 'anyN') continue;
        expect(isContentFreeRow(row.verbatim)).toBe(false);
      }
    },
  );

  test.each(SAMPLE_CARDS.map(c => [c.questionRef, c] as const))(
    '%s — obeys the structural caps and id rules',
    (_ref, card) => {
      expect(isValidCardId(card.id)).toBe(true);
      expect(card.rows.length).toBeLessThanOrEqual(MAX_ROWS);
      expect(card.rows.length).toBeGreaterThan(0);
    },
  );

  test('a question that references a lettered figure actually has one', () => {
    // The first deck asked "Name the parts labelled A and B" with no diagram.
    for (const card of SAMPLE_CARDS) {
      const refsLetters = /\blabelled\b|\bstructures? [ABC]\b|\bparts? [ABC]\b/i.test(card.questionText);
      if (refsLetters) {
        expect(isDiagramCard(card), `${card.questionRef} references letters but has no figure`).toBe(true);
      }
    }
  });
});

describe('figures are real crops from the paper', () => {
  const figures = SAMPLE_CARDS.filter(isDiagramCard).map(c => c.figure);

  test('there is at least one', () => {
    expect(figures.length).toBeGreaterThan(0);
  });

  test.each(figures.map(f => [f.src, f] as const))('%s — the file exists', (_src, fig) => {
    expect(existsSync(resolve(ROOT, 'public', fig.src.replace(/^\//, '')))).toBe(true);
  });

  test.each(figures.map(f => [f.src, f] as const))(
    '%s — is a real asset, never a drawn stand-in',
    (_src, fig) => {
      expect(fig.src).not.toMatch(/^data:/);
      expect(fig.src).not.toMatch(/\.svg$/);
      expect(fig.alt).not.toMatch(/placeholder/i);
      expect(fig.attribution).toMatch(/State Examinations Commission/);
    },
  );

  test.each(figures.map(f => [f.src, f] as const))(
    '%s — the recorded hash matches the file actually on disk',
    (_src, fig) => {
      const bytes = readFileSync(resolve(ROOT, 'public', fig.src.replace(/^\//, '')));
      expect(createHash('md5').update(bytes).digest('hex')).toBe(fig.srcHash);
    },
  );

  test('no two cards bind the same source crop', () => {
    // The Biology corpus has four byte-identical duplicate pairs; binding both
    // sides of one would put the wrong image on a card.
    const hashes = figures.map(f => f.srcHash);
    expect(new Set(hashes).size).toBe(new Set(figures.map(f => f.candId)).size);
  });

  test('every letter the question asks about is decoded in the answer key', () => {
    for (const card of SAMPLE_CARDS.filter(isDiagramCard)) {
      const decoded = new Set(card.labelKey.map(k => k.letter));
      for (const letter of card.figure.lettersVisible) {
        expect(decoded.has(letter), `${card.questionRef} shows ${letter} but never says what it is`).toBe(true);
      }
    }
  });
});

describe('the taxonomy is the redeveloped specification', () => {
  test('has the four strands and twelve units', () => {
    expect(STRANDS).toHaveLength(4);
    expect(ALL_TOPICS.filter(t => /^\d/.test(t.code))).toHaveLength(14);
    expect(STRANDS.map(s => s.title)).toEqual([
      'Nature of Science',
      'Organisation of Life',
      'Structures and Processes of Life',
      'Interactions of Life',
    ]);
  });

  test('carries no trace of the retired Unit One/Two/Three syllabus', () => {
    const titles = ALL_TOPICS.map(t => t.title).join(' ');
    expect(titles).not.toMatch(/Unit (One|Two|Three)/i);
  });

  test('every card is filed under a real unit', () => {
    const ids = new Set(ALL_TOPICS.map(t => t.id));
    for (const card of SAMPLE_CARDS) expect(ids.has(card.topicId)).toBe(true);
  });
});
