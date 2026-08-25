/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * The Home Economics cards are produced by the Python scripts in
 * scripts/markbank/authoring/. Their value is that they are reproducible: the
 * script records which slice of the marking scheme every option came from, so
 * re-running one is how you audit a card's provenance without re-reading the PDF.
 *
 * That only holds while the scripts still run and still emit what shipped. This
 * pins both — a drifted helper in he_lib.py would otherwise go unnoticed until
 * the next paper was authored on top of it.
 */
import { describe, it, expect } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const ROOT = resolve(__dirname, '..');
const DIR = resolve(ROOT, 'scripts/markbank/authoring');
const authored = JSON.parse(
  readFileSync(resolve(ROOT, 'scripts/markbank/authored/home-economics.json'), 'utf8'),
) as Array<{ id: string }>;
const byId = new Map(authored.map(c => [c.id, c]));

/**
 * A figure is bound AFTER the script runs — stamp_figures.py writes the key a
 * figure pass verified, because a card whose ask points at printed artwork
 * ("the table below") is unanswerable without it and the script has no way to
 * know which crop was inspected. The script therefore emits figureKey: "" for
 * those cards and the deck carries the key; this mirrors that step so the
 * comparison stays about the SCHEME content the script is responsible for.
 */
const bindingsPath = resolve(DIR, 'figure_bindings.json');
const bindings: Record<string, string> = existsSync(bindingsPath)
  ? JSON.parse(readFileSync(bindingsPath, 'utf8'))
  : {};
const stamped = (card: { id: string; figureKey?: string }) =>
  bindings[card.id] ? { ...card, figureKey: bindings[card.id] } : card;

/** Skip cleanly on a machine without python3 rather than failing the suite. */
const hasPython = (() => {
  try { execFileSync('python3', ['--version'], { stdio: 'ignore' }); return true; }
  catch { return false; }
})();

describe.skipIf(!hasPython)('mark bank authoring toolkit', () => {
  it('keeps the shared helpers importable', () => {
    const out = execFileSync('python3', ['-c',
      `import sys; sys.path.insert(0, ${JSON.stringify(DIR)}); import he_lib; print(he_lib.MAX_OPTIONS)`,
    ], { encoding: 'utf8' });
    expect(Number(out.trim())).toBe(14);
  });

  // One Section C paper per year, so a regression in he_lib shows up whichever
  // scheme quirk it touches. Running all sixteen would dominate the suite.
  for (const script of ['he_2025_hl_secC', 'he_2024_ol_secC', 'he_2023_ol_secC']) {
    it(`${script} still emits exactly the cards that shipped`, () => {
      const path = resolve(DIR, `${script}.py`);
      expect(existsSync(path)).toBe(true);
      const stdout = execFileSync('python3', [path], { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
      const emitted = JSON.parse(stdout) as Array<{ id: string }>;
      expect(emitted.length).toBeGreaterThan(0);
      for (const card of emitted) {
        expect(byId.get(card.id), `${card.id} is not in the authored deck`)
          .toEqual(stamped(card));
      }
    }, 30_000);
  }
});
