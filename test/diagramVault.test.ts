/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — integrity gates. The vault is a read-only projection of the
 * verified figure exhibits in catchUpLaneData.ts / commandWordData.ts, so these
 * gates guard the projection itself:
 *   1. Every figure file the vault points at actually exists in public/.
 *   2. Every entry carries a decoded alt and an SEC-attributed source.
 *   3. Ids are unique; subjects resolve.
 * A vault tile that 404s, or that shows a figure with no exam source, is exactly
 * the kind of unmoored artifact the accreditation rule forbids.
 */
import { describe, it, expect } from 'vitest';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { DIAGRAM_VAULT, diagramSubjects, diagramsForSubject } from '../data/diagramVault';

const publicPath = (src: string) => resolve(__dirname, '..', 'public', src.replace(/^\//, ''));

describe('Diagram Vault integrity', () => {
  it('has entries to check', () => {
    expect(DIAGRAM_VAULT.length).toBeGreaterThan(0);
  });

  it('every figure file exists in public/', () => {
    const missing = DIAGRAM_VAULT.filter(e => !existsSync(publicPath(e.src))).map(e => e.src);
    expect(missing).toEqual([]);
  });

  it('every entry has a decoded alt and an SEC-attributed source', () => {
    const bad: string[] = [];
    for (const e of DIAGRAM_VAULT) {
      if (e.alt.trim().length < 20) bad.push(`${e.id}: alt too short`);
      if (!/State Examinations Commission|SEC|marking scheme/i.test(e.source)) bad.push(`${e.id}: source not SEC-attributed`);
    }
    expect(bad).toEqual([]);
  });

  it('ids are unique', () => {
    const seen = new Set<string>();
    for (const e of DIAGRAM_VAULT) {
      expect(seen.has(e.id), `duplicate id ${e.id}`).toBe(false);
      seen.add(e.id);
    }
  });

  it('subject counts reconcile with the entry list', () => {
    const subs = diagramSubjects();
    const total = subs.reduce((a, s) => a + s.count, 0);
    expect(total).toBe(DIAGRAM_VAULT.length);
    for (const s of subs) {
      expect(diagramsForSubject(s.id).length).toBe(s.count);
    }
  });
});
