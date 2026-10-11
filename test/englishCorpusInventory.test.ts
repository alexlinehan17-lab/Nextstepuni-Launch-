/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it } from 'vitest';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import inventory from '../scripts/markbank/authored/english-paper-inventory.json';

describe('English full-corpus scope', () => {
  it('retains every indexed year, level and paper in the completion inventory', () => {
    const indexed = PAPER_TRAIL_INDEX.english.flatMap(entry => entry.papers.map(paper => ({
      year: entry.year,
      level: entry.level,
      paperFileid: paper.doc.f,
      schemeFileid: paper.scheme?.f,
    })));
    const inventoried = inventory.papers.map(({ year, level, paperFileid, schemeFileid }) => ({
      year, level, paperFileid, schemeFileid,
    }));
    const sorted = (rows: unknown[]) => rows.map(row => JSON.stringify(row)).sort();
    expect(sorted(inventoried)).toEqual(sorted(indexed));
    expect(inventory.paperCount).toBe(68);
    expect(new Set(inventory.papers.map(paper => paper.id)).size).toBe(68);
    expect([...new Set(inventory.papers.map(paper => paper.year))])
      .toEqual(Array.from({ length: 17 }, (_, index) => 2010 + index));
  });

  it('pins the source bytes while keeping inventory separate from completion evidence', () => {
    for (const paper of inventory.papers) {
      expect(paper.questionPaper.sha256, paper.id).toMatch(/^[a-f0-9]{64}$/);
      expect(paper.markingScheme.sha256, paper.id).toMatch(/^[a-f0-9]{64}$/);
      expect(paper.questionPaper.pages, paper.id).toBeGreaterThan(0);
      expect(paper.markingScheme.pages, paper.id).toBeGreaterThan(0);
    }
    expect(inventory.evidenceRule).toContain('do not prove');
  });
});
