/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { expect, it } from 'vitest';
import credit from '../scripts/atlas-model/irish-section-credit.json';

// The Irish rows a card also counts toward are generated from the paper anchors; the committed map must match them.
it('the Irish section-credit map matches the paper anchors', () => {
  const script = path.join(__dirname, '..', 'scripts', 'atlas-model', 'build-irish-section-credit.mjs');
  expect(() => execFileSync(process.execPath, [script, '--check'], { stdio: 'pipe' })).not.toThrow();
});

it('a covering row is never one of the rows it covers', () => {
  for (const [paper, rows] of Object.entries((credit as { papers: Record<string, Record<string, string[]>> }).papers)) {
    for (const [row, covering] of Object.entries(rows)) expect(covering, `${paper} ${row}`).not.toContain(row);
  }
});
