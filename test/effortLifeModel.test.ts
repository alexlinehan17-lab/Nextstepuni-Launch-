/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Effort → Life model tests — the regression guard on the only net-new maths
 * behind "Your Possible Life": Irish take-home (2026 PAYE/USC/PRSI), the
 * lifestyle translation, and the points/reach reuse helpers.
 */
import { describe, test, expect } from 'vitest';
import {
  irishNetPay, lifestyleFromNet, bestSixPoints, careerReach,
} from '@/components/effortLifeModel';
import { type StudentSubjectProfile } from '@/components/subjectData';
import { type CAOCourse } from '@/components/futureFinderData';

describe('irishNetPay (2026)', () => {
  test('€50,000 reproduces the revenue ready-reckoner worked example', () => {
    const p = irishNetPay(50000);
    expect(p.incomeTax).toBeCloseTo(7200, 2);   // 0.2·44000 + 0.4·6000 − 4000
    expect(p.usc).toBeCloseTo(1032.82, 2);       // 0.5/2/3% bands
    expect(p.prsi).toBeCloseTo(2100, 2);         // 4.2% of 50000
    expect(p.net).toBeCloseTo(39667.18, 2);
    expect(p.netMonthly).toBeCloseTo(3305.6, 1);
  });

  test('USC exemption is a cliff at €13,000', () => {
    expect(irishNetPay(13000).usc).toBe(0);
    expect(irishNetPay(13001).usc).toBeGreaterThan(0);
  });

  test('PRSI only applies once weekly pay clears €352 (≈ €18,304/yr)', () => {
    expect(irishNetPay(18000).prsi).toBe(0);     // €346/wk
    expect(irishNetPay(19000).prsi).toBeGreaterThan(0); // €365/wk
  });

  test('income tax is floored at €0 by credits for low earners', () => {
    expect(irishNetPay(15000).incomeTax).toBe(0); // 3000 gross tax < 4000 credits
  });

  test('net rises monotonically with gross', () => {
    const a = irishNetPay(30000).net;
    const b = irishNetPay(40000).net;
    const c = irishNetPay(75000).net;
    expect(b).toBeGreaterThan(a);
    expect(c).toBeGreaterThan(b);
    expect(c).toBeLessThan(75000); // always less than gross
  });

  test('clamps negative gross to zero', () => {
    expect(irishNetPay(-5000).net).toBe(0);
  });
});

describe('lifestyleFromNet', () => {
  test('tiers follow the Daft/CSO grad bands', () => {
    expect(lifestyleFromNet(2000).tier).toBe('Getting by');
    expect(lifestyleFromNet(2700).tier).toBe('Independent-lite');
    expect(lifestyleFromNet(3200).tier).toBe('Comfortable');
    expect(lifestyleFromNet(4000).tier).toBe('Thriving');
  });

  test('rent-share-of-net uses the regional share rent', () => {
    expect(lifestyleFromNet(3000, 'city').rentShareOfNet).toBeCloseTo(0.2, 2); // 600/3000
    expect(lifestyleFromNet(3000, 'dublin').shareRent).toBeGreaterThan(lifestyleFromNet(3000, 'city').shareRent);
  });

  test('renting alone only becomes feasible at higher net', () => {
    expect(lifestyleFromNet(2200, 'dublin').canRentAlone).toBe(false);
    expect(lifestyleFromNet(5000, 'regional').aloneComfortable).toBe(true);
  });

  test('disposable never goes negative', () => {
    expect(lifestyleFromNet(1000, 'dublin').disposable).toBe(0);
  });

  test('the saving figure never overstates real disposable (honesty)', () => {
    // €1,425 net city → disposable €75: must read "tight", not "€100 aside".
    const tight = lifestyleFromNet(1425, 'city');
    expect(tight.disposable).toBe(75);
    expect(tight.saving.toLowerCase()).toContain('tight');
    // Across a sweep, the displayed monthly saving never exceeds disposable.
    for (const net of [1500, 2000, 2700, 3200, 4000, 5500]) {
      const l = lifestyleFromNet(net, 'city');
      expect(l.savingMonthly).toBeLessThanOrEqual(l.disposable);
    }
  });
});

describe('bestSixPoints', () => {
  const profile: StudentSubjectProfile = {
    subjects: [
      { subjectName: 'English', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Irish', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'French', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'History', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Geography', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Biology', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Chemistry', level: 'higher', currentGrade: 'H5', targetGrade: 'H5' }, // dropped from best-6
    ],
    examStartDate: null, restDays: [], createdAt: '', updatedAt: '',
  };

  test('sums the best six current grades, dropping the rest', () => {
    expect(bestSixPoints(profile, 'current')).toBe(77 * 6); // six H3 = 462; H5 dropped
  });

  test('target uses target grades and is never below current', () => {
    expect(bestSixPoints(profile, 'target')).toBe(88 * 6); // six H2 = 528
  });

  test('falls back to current grade where no target is set', () => {
    const noTargets: StudentSubjectProfile = {
      ...profile,
      subjects: profile.subjects.map((s) => ({ ...s, targetGrade: undefined })),
    };
    expect(bestSixPoints(noTargets, 'target')).toBe(bestSixPoints(noTargets, 'current'));
  });
});

describe('careerReach', () => {
  const courses = [
    { code: 'A', typicalPoints: 400, pathwayType: 'cao' },
    { code: 'B', typicalPoints: 0, pathwayType: 'apprenticeship' },
  ] as unknown as CAOCourse[];

  test('finds the lowest CAO entry threshold and flags the no-points route', () => {
    const r = careerReach(courses, 420, 450);
    expect(r.entryPoints).toBe(400);
    expect(r.hasOpenRoute).toBe(true);
    expect(r.gapFromCurrent).toBe(0); // already over 400
    expect(r.reachTarget).toBe('safety'); // 450 − 400 = 50 ≥ 30
  });

  test('apprenticeship-only careers are always open', () => {
    const apprOnly = [{ code: 'B', typicalPoints: 0, pathwayType: 'apprenticeship' }] as unknown as CAOCourse[];
    const r = careerReach(apprOnly, 0, 0);
    expect(r.entryPoints).toBe(null);
    expect(r.reachNow).toBe('open');
    expect(r.gapFromCurrent).toBe(0);
  });

  test('surfaces a real gap when points fall short', () => {
    const r = careerReach([{ code: 'A', typicalPoints: 500, pathwayType: 'cao' }] as unknown as CAOCourse[], 400, 460);
    expect(r.gapFromCurrent).toBe(100);
    expect(r.gapFromTarget).toBe(40);
    expect(r.reachNow).toBe('out-of-reach'); // 400 − 500 = −100, below the −60 'reach' floor
    expect(r.reachTarget).toBe('reach');     // 460 − 500 = −40, within −60
  });
});
