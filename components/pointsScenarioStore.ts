/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Points Passport — Safe / Target / Stretch scenario runway (feature F7).
 * Up to three named CAO scenarios (grade sets) per student, persisted in
 * localStorage keyed by uid (same pattern as components/PaperTrail/*Store.ts).
 * All points math reuses the shared CAO table in subjectData
 * (getPointsForGrade) — nothing is duplicated here.
 *
 * Honesty rule: scenarios are compared against the student's own recorded
 * mocks ("your mocks so far") — never framed as a prediction of the real exam.
 */

import {
  type Grade, type Level,
  LC_SUBJECTS, getPointsForGrade, getGradesForLevel, getGradeIndex,
} from './subjectData';

// ─── Types ───────────────────────────────────────────────────────────────────

export type ScenarioSlot = 'safe' | 'target' | 'stretch';

export const SCENARIO_SLOTS: ScenarioSlot[] = ['safe', 'target', 'stretch'];

export interface ScenarioGradeEntry {
  subjectName: string;
  grade: Grade;
  level: Level;
}

export interface PointsScenario {
  slot: ScenarioSlot;
  grades: ScenarioGradeEntry[];
  savedAt: string; // ISO date "YYYY-MM-DD"
}

/** At most one scenario per slot — three slots total. */
export type ScenarioMap = Partial<Record<ScenarioSlot, PointsScenario>>;

// ─── Persistence (localStorage, per uid) ─────────────────────────────────────

const PREFIX = 'pp:scenarios:';
const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

export function loadScenarios(uid?: string): ScenarioMap {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object') return {};
    const out: ScenarioMap = {};
    for (const slot of SCENARIO_SLOTS) {
      const s = parsed[slot];
      if (s && Array.isArray(s.grades)) {
        out[slot] = {
          slot,
          grades: s.grades,
          savedAt: typeof s.savedAt === 'string' ? s.savedAt : '',
        };
      }
    }
    return out;
  } catch {
    return {};
  }
}

export function saveScenario(uid: string | undefined, scenario: PointsScenario): ScenarioMap {
  const map = loadScenarios(uid);
  map[scenario.slot] = scenario;
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(map));
  } catch {
    /* quota / private mode — degrade silently */
  }
  return map;
}

export function clearScenario(uid: string | undefined, slot: ScenarioSlot): ScenarioMap {
  const map = loadScenarios(uid);
  delete map[slot];
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(map));
  } catch {
    /* ignore */
  }
  return map;
}

// ─── Pure computation ────────────────────────────────────────────────────────

/**
 * Best-six CAO total for a grade set. Reuses getPointsForGrade (shared CAO
 * table, including the +25 Maths HL bonus for H6 and above).
 */
export function computeBestSixTotal(
  subjects: { subjectName: string; grade: Grade }[],
): number {
  const scored = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths ?? false;
    return getPointsForGrade(s.grade, isMaths);
  });
  scored.sort((a, b) => b - a);
  return scored.slice(0, 6).reduce((sum, p) => sum + p, 0);
}

export interface ScenarioLever {
  subjectName: string;
  fromGrade: Grade;
  toGrade: Grade;
  pointsGain: number;
}

/**
 * The single one-grade jump — starting from the baseline grade set, moving
 * toward the scenario — that closes the biggest slice of the points gap.
 * Only considers subjects where the scenario asks for a better grade at the
 * same level (a level switch isn't a "one grade jump"). Returns null when
 * the scenario asks for nothing above the baseline.
 */
export function bestLeverToward(
  baseline: ScenarioGradeEntry[],
  scenario: ScenarioGradeEntry[],
): ScenarioLever | null {
  let best: ScenarioLever | null = null;
  for (const target of scenario) {
    const cur = baseline.find(b => b.subjectName === target.subjectName);
    if (!cur || !cur.grade || !target.grade) continue;
    if (cur.grade.charAt(0) !== target.grade.charAt(0)) continue;
    if (getGradeIndex(target.grade) >= getGradeIndex(cur.grade)) continue;

    const ladder = getGradesForLevel(cur.grade.startsWith('H') ? 'higher' : 'ordinary');
    const curIdx = ladder.indexOf(cur.grade);
    if (curIdx <= 0) continue;

    const nextGrade = ladder[curIdx - 1];
    const isMaths = LC_SUBJECTS.find(lc => lc.name === target.subjectName)?.isMaths ?? false;
    const gain = getPointsForGrade(nextGrade, isMaths) - getPointsForGrade(cur.grade, isMaths);
    if (gain > 0 && (!best || gain > best.pointsGain)) {
      best = { subjectName: target.subjectName, fromGrade: cur.grade, toGrade: nextGrade, pointsGain: gain };
    }
  }
  return best;
}
