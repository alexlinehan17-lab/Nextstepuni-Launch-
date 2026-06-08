/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the data coupling behind Career Paths' "More than one way in" route map:
 * every career's `matchStrings` must resolve to at least one real CAO course's
 * `careerPaths`, or the route doors silently render empty. The scan flagged this
 * coupling as previously unguarded.
 */
import { describe, it, expect } from 'vitest';
import { CAREERS } from '../careerPathsData';
import { CAO_COURSES } from '../components/futureFinderData';
import { coursesByRoute } from '../components/CareerPaths';

describe('Career Paths — matchStrings resolve to real CAO courses', () => {
  const known = new Set(CAO_COURSES.flatMap((c) => c.careerPaths));

  it('every career has at least one matchString', () => {
    for (const c of CAREERS) {
      expect(c.matchStrings.length, `${c.title} has no matchStrings`).toBeGreaterThan(0);
    }
  });

  it('every matchString maps to at least one CAO course careerPath', () => {
    const orphans: string[] = [];
    for (const c of CAREERS) {
      for (const ms of c.matchStrings) {
        if (!known.has(ms)) orphans.push(`${c.title} :: "${ms}"`);
      }
    }
    expect(orphans, `orphan matchStrings (resolve to no CAO course):\n${orphans.join('\n')}`).toEqual([]);
  });

  it('the route grouping actually surfaces a lower-barrier door for some career', () => {
    // The de-circumscription promise only holds if coursesByRoute really yields a
    // non-degree route (PLC/L6–7 ladder or apprenticeship) for at least one career.
    const someoneHasABackDoor = CAREERS.some((c) =>
      coursesByRoute(c).some((d) => d.key !== 'degree' && d.courses.length > 0),
    );
    expect(someoneHasABackDoor).toBe(true);
  });

  it('every route door has at least one course (no empty doors render)', () => {
    for (const c of CAREERS) {
      for (const d of coursesByRoute(c)) {
        expect(d.courses.length, `${c.title} → ${d.key} door is empty`).toBeGreaterThan(0);
      }
    }
  });
});
