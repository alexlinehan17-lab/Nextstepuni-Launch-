import { describe, expect, it } from 'vitest';
import review from '../scripts/markbank/authored/accounting-answer-review-20261028.json';
import residue from '../scripts/markbank/authored/accounting-rows-residue.json';
import authored from '../components/MarkBank/cards/accounting/authored.json';
import lifted from '../components/MarkBank/cards/accounting/rows.json';

const rows = lifted.cards as Record<string, { how: string; rows: Array<{ id: string; text: string; marks: number; page: number; block?: boolean }> }>;

describe('Accounting source review, 28 October 2026', () => {
  it('accounts for all 98 original exceptions with source evidence and an honest disposition', () => {
    expect(review.tasks).toHaveLength(98);
    expect(new Set(review.tasks.map(task => task.id)).size).toBe(98);
    const retained = review.tasks.filter(task => task.status === 'retained-source');
    expect(retained.map(task => task.id).sort()).toEqual(residue.tasks.map(task => task.id).sort());
    expect(retained).toHaveLength(49);
    for (const task of review.tasks) {
      const card = authored.cards.find(card => card.id === task.id)!;
      expect(card, task.id).toBeDefined();
      expect(task.source.path).toBe(`paper-trail-corpus/markingschemes/${card.year}/${card.paperFileid}`);
      expect(task.source.sha256).toMatch(/^[0-9a-f]{64}$/);
      expect(task.source.pages.length).toBeGreaterThan(0);
      for (const page of task.source.pages) expect(card.schemeRegions.some(region => region.p === page), task.id).toBe(true);
      if (task.status === 'resolved') {
        expect(rows[task.id]?.how, task.id).toBe('visual-review-20261028');
        expect(rows[task.id].rows, task.id).toEqual(task.rows);
      } else {
        expect(rows[task.id], task.id).toBeUndefined();
        expect(task.nextAction, task.id).toBeTruthy();
      }
    }
  });

  it('keeps whole-response allocations whole, but exposes the separately priced calculations', () => {
    const machineHours = rows['acc-2011-ol-q8(a)(ii)'].rows;
    expect(machineHours).toHaveLength(1);
    expect(machineHours[0]).toMatchObject({ marks: 15, block: true, page: 14 });
    expect(machineHours[0].text).toContain('€12 per machine hour');
    const changedProfit = rows['acc-2020-hl-q8(a)(iv)'].rows;
    expect(changedProfit.map(row => row.marks)).toEqual([6, 4, 2, 2]);
    expect(changedProfit[0].text).toContain('31,200 × €38');
    expect(changedProfit[1].text).toContain('€28.66');
    const absorption = rows['acc-2026-hl-q8(e)(i)-calculation'].rows;
    expect(absorption).toHaveLength(9);
    expect(absorption.reduce((sum, row) => sum + row.marks, 0)).toBe(11);
    expect(absorption.every(row => /Production dept\.|Total Overhead/.test(row.text))).toBe(true);
    // Explanations retain all source alternatives; they are not truncated to the parser's 400 characters.
    expect(rows['acc-2021-hl-q6(b)'].rows[0].text).toContain('The report will state the elements');
    expect(rows['acc-2023-hl-q8(b)(ii)'].rows[0].text).toContain('Profit is higher under absorption costing');
  });
});
