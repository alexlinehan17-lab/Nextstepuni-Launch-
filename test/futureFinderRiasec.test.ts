/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * RIASEC scoring engine tests — the regression guard on the redesign's core
 * promises: profile-shape matching, O*NET fit cutoffs, Iachan congruence, and
 * (critically) interest fit NEVER changing with points/subjects.
 */
import { describe, test, expect } from 'vitest';
import {
  profileFromCode, codeFromProfile, profileCorrelation, fitBucket,
  iachanM, iachanPct, reachBucket, checkEligibility, scoreCourseFit,
  RIASEC_LETTERS, WORK_VALUES, type WorkValue,
} from '@/components/futureFinderRiasec';
import { COURSE_RIASEC } from '@/components/futureFinderRiasecData';

describe('RIASEC scoring engine', () => {
  test('profileFromCode / codeFromProfile round-trip', () => {
    expect(profileFromCode('IRA')).toEqual({ I: 3, R: 2, A: 1, S: 0, E: 0, C: 0 });
    expect(codeFromProfile(profileFromCode('IRA'))).toBe('IRA');
  });

  test('profileCorrelation: identical = 1, opposite < 0', () => {
    const inv = profileFromCode('IRA');
    expect(profileCorrelation(inv, inv)).toBeCloseTo(1, 5);
    expect(profileCorrelation(inv, profileFromCode('SEC'))).toBeLessThan(0);
  });

  test('fitBucket uses the O*NET cutoffs', () => {
    expect(fitBucket(0.8)).toBe('best');
    expect(fitBucket(0.65)).toBe('great');
    expect(fitBucket(0.2)).toBe('good');
    expect(fitBucket(-0.1)).toBe('none');
  });

  test('Iachan M: perfect = 28, wrong order < 28, no overlap = 0', () => {
    expect(iachanM('IRA', 'IRA')).toBe(28);
    expect(iachanM('IRA', 'RIA')).toBeLessThan(28);
    expect(iachanM('IRA', 'SEC')).toBe(0);
    expect(iachanPct('IRA', 'IRA')).toBe(100);
  });

  test('reach buckets', () => {
    expect(reachBucket(450, 400)).toBe('safety');
    expect(reachBucket(405, 400)).toBe('match');
    expect(reachBucket(360, 400)).toBe('reach');
    expect(reachBucket(300, 400)).toBe('out-of-reach');
    expect(reachBucket(300, 0)).toBe('open'); // PLC / apprenticeship
  });

  test('eligibility gates', () => {
    expect(checkEligibility(undefined, []).eligible).toBe(true);
    expect(checkEligibility(['Mathematics'], ['Mathematics', 'English']).eligible).toBe(true);
    const r = checkEligibility(['Chemistry'], ['Biology']);
    expect(r.eligible).toBe(false);
    expect(r.missing).toEqual(['Chemistry']);
  });

  test('REGRESSION: interest fit never changes with points', () => {
    const studentProfile = profileFromCode('IRA');
    const course = { riasecProfile: profileFromCode('IAR'), riasecCode: 'IAR', workValues: ['achievement'] as WorkValue[], typicalPoints: 500 };
    const base = { studentProfile, studentCode: 'IRA', studentSubjects: ['Mathematics'], studentValues: ['achievement'] as WorkValue[] };
    const high = scoreCourseFit({ ...base, studentPoints: 600, course });
    const low = scoreCourseFit({ ...base, studentPoints: 200, course });
    expect(high.fitR).toBe(low.fitR);       // fit identical...
    expect(high.matchPct).toBe(low.matchPct);
    expect(high.reach).toBe('safety');       // ...only reach differs
    expect(low.reach).toBe('out-of-reach');
  });

  test('a congruent course out-scores an incongruent one on fit', () => {
    const student = profileFromCode('IRA');
    expect(profileCorrelation(student, profileFromCode('IRA')))
      .toBeGreaterThan(profileCorrelation(student, profileFromCode('SEC')));
  });
});

describe('RIASEC course data', () => {
  const validLetters = new Set<string>(RIASEC_LETTERS);
  const validValues = new Set<string>(WORK_VALUES);
  const entries = Object.entries(COURSE_RIASEC);

  test('every course has a well-formed, self-consistent coding', () => {
    expect(entries.length).toBe(149);
    for (const [code, c] of entries) {
      expect(code).toBeTruthy();
      // riasecCode: 1-3 valid letters
      expect(c.riasecCode.length).toBeGreaterThanOrEqual(1);
      expect(c.riasecCode.length).toBeLessThanOrEqual(3);
      for (const l of c.riasecCode) expect(validLetters.has(l)).toBe(true);
      // profile: all six numeric scales
      for (const l of RIASEC_LETTERS) expect(typeof c.riasecProfile[l]).toBe('number');
      // work values: 1-3, all valid
      expect(c.workValues.length).toBeGreaterThanOrEqual(1);
      expect(c.workValues.length).toBeLessThanOrEqual(3);
      for (const v of c.workValues) expect(validValues.has(v)).toBe(true);
      // consistency: the code's lead letter is the profile's top scale
      const topScale = [...RIASEC_LETTERS].sort((a, b) => c.riasecProfile[b] - c.riasecProfile[a])[0];
      expect(c.riasecCode[0]).toBe(topScale);
    }
  });

  test('known fields map to the expected dominant interest', () => {
    expect(COURSE_RIASEC['DN450']?.riasecCode[0]).toBe('S'); // General Nursing → Social
    expect(COURSE_RIASEC['DN201']?.riasecCode[0]).toBe('I'); // Computer Science → Investigative
    expect(COURSE_RIASEC['DC232']?.riasecCode[0]).toBe('E'); // Civil Law → Enterprising
  });
});
