/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank deck — provenance guards.
 *
 * These exist because the first sample deck was FABRICATED: it invented mark
 * values the scheme does not award, shipped a labelling question with no figure
 * at all, and stood a drawn SVG in for an SEC crop. Every card is now checked
 * against the real sources on disk rather than trusted.
 *
 * The same checks also run inside scripts/markbank/build-deck.mjs, which DROPS a
 * card that fails rather than shipping it — so this file is a standing net over
 * whatever the build let through, not the first line of defence.
 *
 * Written as bulk sweeps that report every offender at once. A per-card
 * test.each over a thousand-card deck produces several thousand vitest cases and
 * takes minutes; this takes seconds and gives a far better failure message.
 */

import { describe, test, expect } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';

import { SAMPLE_CARDS, STRANDS, ALL_TOPICS, BLOCKED_FIGURES } from '../components/MarkBank/deck';
import {
  isDiagramCard, isContentFreeRow, looksLikeSectionLabel, tariffReconciles,
  MAX_ROWS, isValidCardId,
} from '../types/markBank';

const ROOT = resolve(__dirname, '..');
const SCHEME_DIR = resolve(ROOT, 'examiner-reports/biology/schemes');

const norm = (s: string) =>
  s.toLowerCase().replace(/[‐-―]/g, '-').replace(/[^a-z0-9]+/g, ' ').trim();

/**
 * Comparison text, whitespace-insensitive. Two layout facts stand in the way of a
 * character-exact match, and neither is extraction damage: chemical subscripts sit
 * on their own baseline (the carbohydrate formula extracts as "C x ( H 2 O )y"),
 * and a marks cell is vertically centred against a multi-line answer, so the mark
 * lands BETWEEN the two lines it belongs to. Mark-only lines are dropped and
 * spacing ignored; every character of an answer must still appear, in order.
 */
const MARKS_ONLY = /^\s*\d+\s*(\(\s*\d+\s*\))?\s*$/;
const tight = (s: string) => norm(s).replace(/ /g, '');
const comparable = (text: string) =>
  tight(text.split('\n').filter(l => !MARKS_ONLY.test(l)).join(' '));

const schemeFor = (card: { year: number; level: string }) =>
  resolve(SCHEME_DIR, `${card.year}-${card.level === 'higher' ? 'hl' : 'ol'}.md`);

const schemeCache = new Map<string, string>();
const schemeText = (card: { year: number; level: string }) => {
  const path = schemeFor(card);
  if (!schemeCache.has(path)) {
    schemeCache.set(path, existsSync(path) ? comparable(readFileSync(path, 'utf8')) : '');
  }
  return schemeCache.get(path)!;
};

const show = (bad: string[]) => `${bad.length} offender(s):\n${bad.slice(0, 25).join('\n')}`;

/* ----------------------------------------------------------- provenance ---- */

describe('every card traces to the marking scheme on disk', () => {
  test('the deck is substantial', () => {
    expect(SAMPLE_CARDS.length).toBeGreaterThan(100);
  });

  test('every year and level the deck draws on has its scheme present', () => {
    const missing = [...new Set(SAMPLE_CARDS.map(schemeFor))].filter(p => !existsSync(p));
    expect(missing, show(missing)).toEqual([]);
  });

  test('every marking point appears in its own scheme', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      const scheme = schemeText(card);
      for (const row of card.rows) {
        const claims = row.kind === 'anyN' && row.group
          ? row.group.options
          // Rows read "Label — answer"; the answer is what the scheme prints.
          : [row.verbatim.split(/\s[—-]\s/).pop() ?? row.verbatim];
        for (const claim of claims) {
          if (!scheme.includes(tight(claim))) bad.push(`${card.questionRef}: "${claim}"`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('marks reconcile against the printed tariff', () => {
    const bad = SAMPLE_CARDS.filter(c => !tariffReconciles(c)).map(c => c.questionRef);
    expect(bad, show(bad)).toEqual([]);
  });
});

/* -------------------------------------------------- fabrication guards ----- */

describe('no card can repeat the fabrication that shipped first time', () => {
  test('every card is a real question, not a section label or table fragment', () => {
    const bad = SAMPLE_CARDS
      .filter(c => looksLikeSectionLabel(c.questionText) || c.questionText.length <= 15)
      .map(c => `${c.questionRef}: "${c.questionText}"`);
    expect(bad, show(bad)).toEqual([]);
  });

  test('every row carries an answer, not a mark tariff', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS) {
      for (const row of card.rows) {
        if (row.kind !== 'anyN' && isContentFreeRow(row.verbatim)) {
          bad.push(`${card.questionRef}: "${row.verbatim}"`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('every card obeys the structural caps and id rules', () => {
    const bad = SAMPLE_CARDS
      .filter(c => !isValidCardId(c.id) || c.rows.length === 0 || c.rows.length > MAX_ROWS)
      .map(c => `${c.questionRef} (${c.id}, ${c.rows.length} rows)`);
    expect(bad, show(bad)).toEqual([]);
  });

  test('card ids are unique', () => {
    const seen = new Set<string>();
    const dupes: string[] = [];
    for (const c of SAMPLE_CARDS) {
      if (seen.has(c.id)) dupes.push(c.id);
      seen.add(c.id);
    }
    expect(dupes, show(dupes)).toEqual([]);
  });

  test('a question that names lettered parts actually carries a figure', () => {
    // The first deck asked "Name the parts labelled A and B" with no diagram.
    // "You may include a labelled diagram if you wish" invites the student to
    // draw one, and does not require the card to carry a figure.
    const bad = SAMPLE_CARDS.filter(c => {
      if (/you may include a labelled/i.test(c.questionText)) return false;
      const namesLetters = /\blabelled [A-Z]\b|\bstructures? [A-Z](,| and )|\bparts? [A-Z](,| and )|\blabelled\s+(parts|structures)\b/i.test(c.questionText);
      return namesLetters && !isDiagramCard(c);
    }).map(c => `${c.questionRef}: "${c.questionText}"`);
    expect(bad, show(bad)).toEqual([]);
  });
});

/* --------------------------------------------------------------- figures --- */

describe('figures are real crops from the paper', () => {
  const figures = SAMPLE_CARDS.filter(isDiagramCard).map(c => c.figure);

  test('there is at least one', () => {
    expect(figures.length).toBeGreaterThan(0);
  });

  test('every figure file exists', () => {
    const bad = figures
      .filter(f => !existsSync(resolve(ROOT, 'public', f.src.replace(/^\//, ''))))
      .map(f => f.src);
    expect(bad, show(bad)).toEqual([]);
  });

  test('every figure is a real asset, never a drawn stand-in', () => {
    const bad = figures.filter(f =>
      /^data:/.test(f.src) || /\.svg$/.test(f.src) || /placeholder/i.test(f.alt)
      || !/State Examinations Commission/.test(f.attribution)).map(f => f.src);
    expect(bad, show(bad)).toEqual([]);
  });

  test('every recorded hash matches the file actually on disk', () => {
    const bad = figures.filter(f => {
      const abs = resolve(ROOT, 'public', f.src.replace(/^\//, ''));
      if (!existsSync(abs)) return true;
      return createHash('md5').update(readFileSync(abs)).digest('hex') !== f.srcHash;
    }).map(f => f.src);
    expect(bad, show(bad)).toEqual([]);
  });

  test('no card binds a figure known to hold the wrong image', () => {
    // Four files in the Biology corpus carry a neighbour's crop, and two more
    // truncate a label the question asks about. Binding one puts a confidently
    // captioned wrong diagram in front of a student.
    const bad = figures.filter(f => BLOCKED_FIGURES.includes(f.candId)).map(f => f.candId);
    expect(bad, show(bad)).toEqual([]);
  });

  test('no two cards bind the same source crop under different names', () => {
    const byHash = new Map<string, string>();
    const bad: string[] = [];
    for (const f of figures) {
      const prev = byHash.get(f.srcHash);
      if (prev && prev !== f.candId) bad.push(`${f.candId} shares bytes with ${prev}`);
      byHash.set(f.srcHash, f.candId);
    }
    expect(bad, show(bad)).toEqual([]);
  });

  test('every letter the question asks about is decoded in the answer key', () => {
    const bad: string[] = [];
    for (const card of SAMPLE_CARDS.filter(isDiagramCard)) {
      const decoded = new Set(card.labelKey.map(k => k.letter));
      for (const letter of card.figure.lettersVisible) {
        if (!decoded.has(letter)) {
          bad.push(`${card.questionRef} shows ${letter} but never says what it is`);
        }
      }
    }
    expect(bad, show(bad)).toEqual([]);
  });
});

/* -------------------------------------------------------------- taxonomy --- */

describe('the taxonomy is the redeveloped specification', () => {
  test('has the four strands and their units', () => {
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
    expect(ALL_TOPICS.map(t => t.title).join(' ')).not.toMatch(/Unit (One|Two|Three)/i);
  });

  test('every card is filed under a real unit', () => {
    const ids = new Set(ALL_TOPICS.map(t => t.id));
    const bad = SAMPLE_CARDS.filter(c => !ids.has(c.topicId)).map(c => `${c.questionRef} -> ${c.topicId}`);
    expect(bad, show(bad)).toEqual([]);
  });
});
