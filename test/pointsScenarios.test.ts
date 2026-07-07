/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Points Passport scenario runway (feature F7): per-uid
 * localStorage persistence of the Safe / Target / Stretch slots, best-six
 * CAO totals (reusing the shared points table, Maths bonus included), and
 * the "biggest single grade jump" lever toward a scenario.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import {
  type ScenarioGradeEntry,
  loadScenarios, saveScenario, clearScenario,
  computeBestSixTotal, bestLeverToward,
} from '../components/pointsScenarioStore';
import type { Grade, Level } from '../components/subjectData';

const entry = (subjectName: string, grade: Grade, level: Level = 'higher'): ScenarioGradeEntry =>
  ({ subjectName, grade, level });

describe('Points Passport — scenario store', () => {
  beforeEach(() => localStorage.clear());

  it('round-trips a scenario per slot and per uid', () => {
    saveScenario('u1', { slot: 'safe', grades: [entry('English', 'H4')], savedAt: '2026-07-07' });
    saveScenario('u1', { slot: 'stretch', grades: [entry('English', 'H2')], savedAt: '2026-07-07' });
    saveScenario('u2', { slot: 'safe', grades: [entry('English', 'H6')], savedAt: '2026-07-07' });

    const u1 = loadScenarios('u1');
    expect(u1.safe?.grades[0].grade).toBe('H4');
    expect(u1.stretch?.grades[0].grade).toBe('H2');
    expect(u1.target).toBeUndefined();

    // uid isolation
    expect(loadScenarios('u2').safe?.grades[0].grade).toBe('H6');
    expect(loadScenarios('u2').stretch).toBeUndefined();
  });

  it('overwrites a slot on re-save and clears a single slot', () => {
    saveScenario('u1', { slot: 'target', grades: [entry('Irish', 'H5')], savedAt: '2026-07-01' });
    saveScenario('u1', { slot: 'target', grades: [entry('Irish', 'H3')], savedAt: '2026-07-07' });
    expect(loadScenarios('u1').target?.grades[0].grade).toBe('H3');

    saveScenario('u1', { slot: 'safe', grades: [entry('Irish', 'H6')], savedAt: '2026-07-07' });
    clearScenario('u1', 'target');
    const map = loadScenarios('u1');
    expect(map.target).toBeUndefined();
    expect(map.safe?.grades[0].grade).toBe('H6');
  });

  it('falls back to the anon bucket without a uid', () => {
    saveScenario(undefined, { slot: 'safe', grades: [entry('English', 'H4')], savedAt: '2026-07-07' });
    expect(loadScenarios(undefined).safe?.grades[0].grade).toBe('H4');
    expect(loadScenarios('u1').safe).toBeUndefined();
  });

  it('survives corrupt or foreign stored data', () => {
    localStorage.setItem('pp:scenarios:u1', 'not json');
    expect(loadScenarios('u1')).toEqual({});

    localStorage.setItem('pp:scenarios:u2', JSON.stringify({ bogusSlot: { grades: [] }, safe: { grades: 'nope' } }));
    expect(loadScenarios('u2')).toEqual({});
  });
});

describe('Points Passport — best-six totals', () => {
  it('sums the best six subjects only', () => {
    const seven = [
      entry('English', 'H2'),   // 88
      entry('Irish', 'H3'),     // 77
      entry('French', 'H3'),    // 77
      entry('Biology', 'H4'),   // 66
      entry('Chemistry', 'H4'), // 66
      entry('History', 'H5'),   // 56
      entry('Geography', 'H7'), // 37 — dropped as 7th best
    ];
    expect(computeBestSixTotal(seven)).toBe(88 + 77 + 77 + 66 + 66 + 56);
  });

  it('includes the +25 Maths HL bonus for H6 and above', () => {
    expect(computeBestSixTotal([entry('Mathematics', 'H6')])).toBe(46 + 25);
    expect(computeBestSixTotal([entry('Mathematics', 'H7')])).toBe(37); // below H6 — no bonus
    expect(computeBestSixTotal([entry('Applied Maths', 'H6')])).toBe(46); // not Maths — no bonus
  });
});

describe('Points Passport — bestLeverToward', () => {
  const baseline = [
    entry('English', 'H4'),      // next step H3: 77 - 66 = +11
    entry('Mathematics', 'H7'),  // next step H6: (46+25) - 37 = +34 (bonus kicks in)
    entry('Geography', 'O3', 'ordinary'), // next step O2: 46 - 37 = +9
  ];

  it('picks the single grade jump that closes the biggest gap', () => {
    const scenario = [
      entry('English', 'H2'),
      entry('Mathematics', 'H5'),
      entry('Geography', 'O2', 'ordinary'),
    ];
    const lever = bestLeverToward(baseline, scenario);
    expect(lever).toEqual({
      subjectName: 'Mathematics',
      fromGrade: 'H7',
      toGrade: 'H6',
      pointsGain: 34, // includes the +25 Maths bonus unlocked at H6
    });
  });

  it('ignores subjects where the scenario is not above the baseline', () => {
    const scenario = [
      entry('English', 'H3'), // above baseline — the only live lever
      entry('Mathematics', 'H7'), // equal
      entry('Geography', 'O4', 'ordinary'), // below
    ];
    expect(bestLeverToward(baseline, scenario)).toEqual({
      subjectName: 'English',
      fromGrade: 'H4',
      toGrade: 'H3',
      pointsGain: 11,
    });
  });

  it('returns null when the scenario asks for nothing above the baseline', () => {
    expect(bestLeverToward(baseline, baseline)).toBeNull();
    expect(bestLeverToward(baseline, [entry('English', 'H5')])).toBeNull();
  });

  it('skips cross-level comparisons and unknown subjects', () => {
    const scenario = [
      entry('Geography', 'H3'), // level switch from O3 — not a one-grade jump
      entry('Music', 'H1'),     // not in baseline
    ];
    expect(bestLeverToward(baseline, scenario)).toBeNull();
  });
});
