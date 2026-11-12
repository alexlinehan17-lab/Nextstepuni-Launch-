/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The deferred Irish sittings (2022-2025, Higher and Ordinary, Papers 1 and 2): their printed asks, read from each
 * paper's own text layer (scripts/markbank/authoring/irish_paper_asks.py) into the census beside June's, keyed
 * 'Deferred Paper N'. Hand counts: 2023 HL Paper 1 (33) and 2022 OL Paper 2 (51), read off the rendered pages. 2025 and
 * 2024 are carded (irish_deferred.py, markBankIrishDeferred.test.ts); each card's manifest lists the asks it covers.
 * CI has neither PyMuPDF nor the corpus: the census test runs where both are.
 */
import { describe, expect, it } from 'vitest';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const hasPyMuPDF = (() => { try { execFileSync('python3', ['-c', 'import fitz'], { stdio: 'ignore' }); return true; } catch { return false; } })();
const canRead = hasPyMuPDF && existsSync('paper-trail-corpus/deferredexams/2023/LC001ALP100IV.pdf');

const DENOMINATOR: Record<string, number> = {
  '2022 hl Deferred Paper 1': 33, '2022 hl Deferred Paper 2': 62, '2022 ol Deferred Paper 1': 29, '2022 ol Deferred Paper 2': 51,
  '2023 hl Deferred Paper 1': 33, '2023 hl Deferred Paper 2': 58, '2023 ol Deferred Paper 1': 29, '2023 ol Deferred Paper 2': 50,
  '2024 hl Deferred Paper 1': 33, '2024 hl Deferred Paper 2': 58, '2024 ol Deferred Paper 1': 29, '2024 ol Deferred Paper 2': 50,
  '2025 hl Deferred Paper 1': 32, '2025 hl Deferred Paper 2': 58, '2025 ol Deferred Paper 1': 29, '2025 ol Deferred Paper 2': 51,
};

describe('Irish deferred sittings: the denominator', () => {
  it.skipIf(!canRead)('censuses every printed ask of the 16 deferred papers, each with a deferred id and citation', () => {
    const out = execFileSync('python3', ['-c', `
import json, sys
sys.path.insert(0, 'scripts/markbank/authoring')
from paper_census import census_irish_deferred
print(json.dumps([[p['year'], p['level'], p['paper'], [l['key'][0] for l in p['leaves']], [l['label'] for l in p['leaves']]] for p in census_irish_deferred()]))
`], { encoding: 'utf8', maxBuffer: 1 << 24 });
    const papers = JSON.parse(out) as [number, string, string, string[], string[]][];
    expect(Object.fromEntries(papers.map(([year, level, paper, ids]) => [`${year} ${level} ${paper}`, ids.length]))).toEqual(DENOMINATOR);
    expect(papers.reduce((sum, [, , , ids]) => sum + ids.length, 0)).toBe(685);
    for (const [year, level, , ids, labels] of papers) {
      expect(new Set(ids).size).toBe(ids.length);
      for (const id of ids) expect(id).toMatch(new RegExp(`^irish-${year}-${level}-deferred-p[12]-[a-z0-9-]+$`));
      for (const label of labels) expect(label.endsWith(' — Deferred sitting')).toBe(true);
    }
    // The two hand counts.
    const ids = (key: string) => papers.find(([year, level, paper]) => `${year} ${level} ${paper}` === key)![3];
    expect(ids('2023 hl Deferred Paper 1').filter(id => id.includes('-cluastuiscint-'))).toHaveLength(24);
    expect(ids('2022 ol Deferred Paper 2').filter(id => id.includes('-litriocht-3a-b-i-'))).toHaveLength(4);
    // An answer line's label printed last on a page ("(i) (ii)" above the running head) is not a part of the question.
    expect(ids('2025 hl Deferred Paper 1')).toContain('irish-2025-hl-deferred-p1-cluastuiscint-piosa-a-do-3');
    expect(ids('2024 hl Deferred Paper 1')).toContain('irish-2024-hl-deferred-p1-cluastuiscint-comhra-a-haon-an-dara-mir-2');
    expect(ids('2022 hl Deferred Paper 1')).toContain('irish-2022-hl-deferred-p1-cluastuiscint-fogra-a-do-2');
    expect(papers.flatMap(([, , , paperIds]) => paperIds).filter(id => /-cluastuiscint-.*-\d-ii$/.test(id))).toEqual([]);
  });
});
