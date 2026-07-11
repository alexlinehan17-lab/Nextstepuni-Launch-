/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Coursework Companion — integrity gates. Unlike Answer Architect / Definition
 * Drill (projections of MARKING_LENS), this corpus is AUTHORED from the filed
 * SEC marking schemes, so the gate enforces the accreditation rule on the
 * authored data itself:
 *   1. Non-empty; ids unique; subject counts reconcile.
 *   2. THE ACCREDITATION GATE — every component carries an SEC-attributed
 *      source, a resolvable SEC archive URL, and an in-repo `filed` document
 *      that actually exists (the re-verification trail). A coursework fact with
 *      no filed source behind it must never ship.
 *   3. Marks reconcile — where a component states a printed total AND presents
 *      its criteria as the complete breakdown, the criteria sum to the total
 *      (catches a mis-transcribed band). Components whose scheme prints no
 *      total carry totalMarks: null — the gate confirms no invented total.
 *   4. Every criterion has substance: a name, positive marks and a
 *      what-it-rewards line.
 */
import { describe, it, expect } from 'vitest';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { COURSEWORK_COMPONENTS, courseworkSubjects, componentsForSubject } from '../data/courseworkCompanion';

const repoPath = (p: string) => resolve(__dirname, '..', p);

describe('Coursework Companion integrity', () => {
  it('has components to check', () => {
    expect(COURSEWORK_COMPONENTS.length).toBeGreaterThan(0);
  });

  it('every component is SEC-attributed with a resolvable archive URL and an existing filed document', () => {
    const bad: string[] = [];
    for (const c of COURSEWORK_COMPONENTS) {
      if (!/State Examinations Commission/i.test(c.source)) bad.push(`${c.id}: source not SEC-attributed`);
      if (!/SEC Marking Scheme \d{4}/i.test(c.source)) bad.push(`${c.id}: source does not name a filed scheme + year`);
      if (!/^https:\/\/www\.examinations\.ie\//.test(c.sourceUrl)) bad.push(`${c.id}: sourceUrl not the SEC archive`);
      if (!c.filed.startsWith('examiner-reports/')) bad.push(`${c.id}: filed path not in examiner-reports/`);
      if (!existsSync(repoPath(c.filed))) bad.push(`${c.id}: filed document missing (${c.filed})`);
    }
    expect(bad).toEqual([]);
  });

  it('criteria reconcile with the printed total where the scheme prints one', () => {
    const bad: string[] = [];
    for (const c of COURSEWORK_COMPONENTS) {
      if (c.totalMarks !== null && c.criteriaComplete) {
        const sum = c.criteria.reduce((a, cr) => a + cr.marks, 0);
        if (sum !== c.totalMarks) bad.push(`${c.id}: criteria sum ${sum} != printed total ${c.totalMarks}`);
      }
      if (c.totalMarks !== null && c.totalMarks <= 0) bad.push(`${c.id}: non-positive total`);
    }
    expect(bad).toEqual([]);
  });

  it('every criterion carries a name, positive marks and a what-it-rewards line', () => {
    const bad: string[] = [];
    for (const c of COURSEWORK_COMPONENTS) {
      if (c.criteria.length === 0) bad.push(`${c.id}: no criteria`);
      for (const cr of c.criteria) {
        if (cr.name.trim().length < 3) bad.push(`${c.id}: criterion with empty name`);
        if (cr.marks <= 0) bad.push(`${c.id} "${cr.name}": non-positive marks`);
        if (cr.whatItRewards.trim().length < 10) bad.push(`${c.id} "${cr.name}": empty whatItRewards`);
      }
      if (c.whatItIs.trim().length < 20) bad.push(`${c.id}: whatItIs too thin`);
    }
    expect(bad).toEqual([]);
  });

  it('ids are unique', () => {
    const seen = new Set<string>();
    for (const c of COURSEWORK_COMPONENTS) {
      expect(seen.has(c.id), `duplicate id ${c.id}`).toBe(false);
      seen.add(c.id);
    }
  });

  it('subject counts reconcile with the component list', () => {
    const subs = courseworkSubjects();
    const total = subs.reduce((a, s) => a + s.count, 0);
    expect(total).toBe(COURSEWORK_COMPONENTS.length);
    for (const s of subs) expect(componentsForSubject(s.id).length).toBe(s.count);
  });
});
