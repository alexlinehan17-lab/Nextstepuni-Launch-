/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * English Paper 2 chip labels keep the paper's printed title.
 *
 * The labels are written by scripts/paper-trail/english_p2_complete.py
 * (Higher) and english_p2_ol.py (Ordinary) through one title_case(), and the
 * app serves them from the hosted copies in public/paper-answers/
 * (HOSTED_ANSWER_OVERRIDES). str.title() capitalised after an apostrophe
 * ("The Handmaid’S Tale", "Yeats’S"), and a split at the first spaced dash
 * cut 2019 Ordinary's "THE FISH (EXTRACT: LINES 45 – 76)" to
 * "The Fish (Extract: Lines 45". The unit tests for the function itself are in
 * scripts/paper-trail/test_english_p2_labels.py (they need no corpus).
 */

import { existsSync, readFileSync, readdirSync } from 'fs';
import path from 'path';
import { describe, expect, it } from 'vitest';

const DIRECTORIES = {
  sidecar: path.resolve(__dirname, '../scripts/paper-trail/answers'),
  hosted: path.resolve(__dirname, '../public/paper-answers'),
};
const ENGLISH_PAPER_2 = /^LC002[AG]LP200EV\.pdf\.json$/;

interface Label { source: string; year: string; file: string; n: string; label: string }

function englishLabels(): Label[] {
  const out: Label[] = [];
  for (const [source, directory] of Object.entries(DIRECTORIES)) {
    for (const year of readdirSync(directory)) {
      const yearDirectory = path.join(directory, year);
      for (const file of readdirSync(yearDirectory)) {
        if (!ENGLISH_PAPER_2.test(file)) continue;
        const map = JSON.parse(readFileSync(path.join(yearDirectory, file), 'utf-8')) as {
          q: Array<{ n: string; label?: string }>;
        };
        for (const question of map.q) {
          if (question.label) out.push({ source, year, file, n: question.n, label: question.label });
        }
      }
    }
  }
  return out;
}

const labelsFor = (source: string, year: string, file: string) =>
  englishLabels().filter(row => row.source === source && row.year === year && row.file === file)
    .map(row => row.label);

describe('English Paper 2 Paper Trail labels', () => {
  const labels = englishLabels();

  it('reads every English Paper 2 map in both the sidecars and the hosted copies', () => {
    for (const source of Object.keys(DIRECTORIES)) {
      const files = new Set(labels.filter(row => row.source === source).map(row => `${row.year}/${row.file}`));
      // 2010–2026, Higher and Ordinary.
      expect(files.size, source).toBe(34);
    }
    expect(existsSync(path.join(DIRECTORIES.hosted, '2019', 'LC002GLP200EV.pdf.json'))).toBe(true);
  });

  it('never capitalises the letter after an apostrophe in a possessive', () => {
    const bad = labels.filter(row => /[a-z][’'][A-Z]\b/.test(row.label))
      .map(row => `${row.source} ${row.year} ${row.file} Q${row.n}: ${row.label}`);
    expect(bad).toEqual([]);
    expect(labelsFor('hosted', '2019', 'LC002ALP200EV.pdf.json')).toContain('Single Text B · The Handmaid’s Tale · (i)');
    expect(labelsFor('hosted', '2019', 'LC002ALP200EV.pdf.json')).toContain(
      'Prescribed Poetry · “Yeats’s Poetry Is Both Intellectually Stimulating And Emotionally Charged.” · Q3');
    expect(labelsFor('hosted', '2019', 'LC002GLP200EV.pdf.json')).toContain('Single Text B · The Handmaid’s Tale');
  });

  it('keeps the whole printed 2019 Ordinary extract headings', () => {
    const ordinary2019 = labelsFor('hosted', '2019', 'LC002GLP200EV.pdf.json');
    expect(ordinary2019).toContain('Poetry C · The Fish (Extract: Lines 45 – 76)');
    expect(ordinary2019).toContain('Poetry D · Daniel’s Duck (Extract: Lines 7 – 27)');
    const unbalanced = labels.filter(row => (row.label.match(/\(/g) ?? []).length !== (row.label.match(/\)/g) ?? []).length)
      .map(row => `${row.source} ${row.year} ${row.file} Q${row.n}: ${row.label}`);
    expect(unbalanced).toEqual([]);
  });

  it('serves the same labels it generates', () => {
    const key = (row: Label) => `${row.year}/${row.file}/${row.n}`;
    const hosted = new Map(labels.filter(row => row.source === 'hosted').map(row => [key(row), row.label]));
    const sidecar = labels.filter(row => row.source === 'sidecar');
    expect(sidecar.length).toBe(hosted.size);
    for (const row of sidecar) expect(hosted.get(key(row)), key(row)).toBe(row.label);
  });
});
