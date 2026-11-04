/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The authoring pre-check (scripts/markbank/authoring/provcheck.mjs) must agree
 * with the build's provenance gate (build-deck.mjs). A pre-check stricter than
 * the gate sends an author to "fix" cards the build accepts and ships.
 */

import { describe, expect, test } from 'vitest';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
// The build's own comparison, shared with build-deck.mjs and provcheck.mjs.
import { claimMatches, claimTraces, comparableScheme } from '../scripts/markbank/schemeText.mjs';

const authored = (subject: string) => JSON.parse(readFileSync(`scripts/markbank/authored/${subject}.json`, 'utf8')) as Array<{ id: string }>;
const provcheck = (cards: unknown[]) => {
  const file = join(mkdtempSync(join(tmpdir(), 'provcheck-')), 'cards.json');
  writeFileSync(file, JSON.stringify(cards));
  return execFileSync(process.execPath, ['scripts/markbank/authoring/provcheck.mjs', file], { encoding: 'utf8' });
};

describe('provcheck applies the build\'s rule', () => {
  test('a menu option pairing a label with its value traces by halves, as the build allows', () => {
    // Biology 2017 HL Q15(b)(i): names in one table row, numbers in the next.
    const scheme = comparableScheme(readFileSync('examiner-reports/biology/schemes/2017-hl.md', 'utf8'));
    expect(claimMatches(scheme, 'thoracic — 12')).toBe(false);
    expect(claimTraces(scheme, 'thoracic — 12', { menuOption: true })).toBe(true);
    // Only a menu option: a row's own verbatim is checked whole, as the build does.
    expect(claimTraces(scheme, 'thoracic — 12')).toBe(false);
  });

  test('cards the build ships pass the pre-check: label-value menus, an unprinted row, ask rows', () => {
    const wanted = new Set(['bio-2017-hl-q15-b-i', 'bio-2010-ol-q11-c-vii']);
    const biology = authored('biology').filter(c => wanted.has(c.id)).map(c => ({ subjectId: 'biology', ...c }));
    const chemistry = authored('chemistry').filter(c => c.id === 'chem-2021-hl-q9-c-i');
    expect(biology).toHaveLength(2);
    expect(chemistry).toHaveLength(1);
    // Before the port: 4 halves options, the unprinted row and the ask row were all "untraceable".
    expect(provcheck([...biology, ...chemistry])).toMatch(/, 0 untraceable\n$/);
  });

  test('a claim the scheme does not print is still reported', () => {
    const [card] = authored('chemistry').filter(c => c.id === 'chem-2021-hl-q9-c-i') as Array<{ rows: Array<{ ask?: boolean; verbatim: string }> }>;
    const broken = { ...card, rows: [{ id: 'r1', kind: 'point', verbatim: 'a marking point no scheme ever printed', marks: 3 }] };
    expect(provcheck([broken])).toMatch(/UNTRACEABLE chem-2021-hl-q9-c-i :: a marking point no scheme ever printed/);
  });
});
