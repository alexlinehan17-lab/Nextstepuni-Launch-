/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Future Finder — RIASEC scoring engine (Phase A of the scientific re-base; see
 * docs/future-finder-redesign-plan.md).
 *
 * Anchored on Holland's RIASEC vocational-interest model (the basis of the
 * O*NET Interest Profiler). Course matching uses the O*NET method: the Pearson
 * correlation between the student's six-number interest profile and each
 * course's six-number profile (matches on profile SHAPE, not absolute level,
 * and needs no tie-breaking). A human-readable congruence number (Iachan's M)
 * is reported alongside.
 *
 * The cardinal rule: interest "fit" is computed PURELY from interests and is
 * NEVER altered by CAO points or subjects. Points feasibility ("reach") and
 * subject requirements ("eligibility") are independent axes, combined only at
 * the presentation layer — so a perfect-fit course that's a points stretch is
 * shown as exactly that, never silently demoted.
 *
 * Sources: O*NET IP Manual (matching, OIP, cutoffs) onetcenter.org/reports/IP_Manual.html;
 * Iachan (1984) JVB 24:133-141; `holland` R package weight matrix.
 *
 * Nothing here is wired into the live tool yet — the new questionnaire (which
 * produces RIASEC responses) lands in a later phase.
 */

export type RiasecLetter = 'R' | 'I' | 'A' | 'S' | 'E' | 'C';
export const RIASEC_LETTERS = ['R', 'I', 'A', 'S', 'E', 'C'] as const;
export const RIASEC_LABELS: Record<RiasecLetter, string> = {
  R: 'Realistic',
  I: 'Investigative',
  A: 'Artistic',
  S: 'Social',
  E: 'Enterprising',
  C: 'Conventional',
};
/** Six-number interest profile (scale scores). */
export type RiasecProfile = Record<RiasecLetter, number>;

/** O*NET's six work values (Theory of Work Adjustment). Secondary, satisfaction-relevant layer. */
export type WorkValue = 'achievement' | 'independence' | 'recognition' | 'relationships' | 'support' | 'working-conditions';
export const WORK_VALUES = ['achievement', 'independence', 'recognition', 'relationships', 'support', 'working-conditions'] as const;
export const WORK_VALUE_LABELS: Record<WorkValue, string> = {
  achievement: 'Achievement',
  independence: 'Independence',
  recognition: 'Recognition',
  relationships: 'Relationships',
  support: 'Support',
  'working-conditions': 'Working Conditions',
};

/** RIASEC metadata attached to a course (stored separately, keyed by course code). */
export interface CourseRiasec {
  /** 1-3 ordered Holland letters, e.g. "IRA". */
  riasecCode: string;
  /** Six-number profile (canonical, derived from the code or an expert OIP). */
  riasecProfile: RiasecProfile;
  /** Top 2-3 work values the field emphasises. */
  workValues: WorkValue[];
  /** Hard subject gates (e.g. ["Mathematics"]). Empty/absent = no gate. Forward-compatible. */
  requiredSubjects?: string[];
}

const EMPTY_PROFILE = (): RiasecProfile => ({ R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 });
const isLetter = (c: string): c is RiasecLetter => (RIASEC_LETTERS as readonly string[]).includes(c);

/** Ordered Holland code -> canonical six-number profile (1st letter 3, 2nd 2, 3rd 1, rest 0). */
export function profileFromCode(code: string): RiasecProfile {
  const p = EMPTY_PROFILE();
  const letters = code.toUpperCase().split('').filter(isLetter);
  const weights = [3, 2, 1];
  letters.slice(0, 3).forEach((l, i) => { p[l] = weights[i]; });
  return p;
}

/** Six-number profile -> ordered code (top n scales). Ties resolved by RIASEC order. */
export function codeFromProfile(p: RiasecProfile, n = 3): string {
  return [...RIASEC_LETTERS].sort((a, b) => p[b] - p[a]).slice(0, n).join('');
}

/** Sum a student's Likert responses per scale into a six-number profile. */
export function buildStudentProfile(responsesByScale: Partial<Record<RiasecLetter, number[]>>): RiasecProfile {
  const p = EMPTY_PROFILE();
  for (const l of RIASEC_LETTERS) p[l] = (responsesByScale[l] ?? []).reduce((s, x) => s + x, 0);
  return p;
}

/** Pearson correlation between two six-number profiles — O*NET's profile-shape match. */
export function profileCorrelation(a: RiasecProfile, b: RiasecProfile): number {
  const av = RIASEC_LETTERS.map((l) => a[l]);
  const bv = RIASEC_LETTERS.map((l) => b[l]);
  const n = av.length;
  const ma = av.reduce((s, x) => s + x, 0) / n;
  const mb = bv.reduce((s, x) => s + x, 0) / n;
  let num = 0, da = 0, db = 0;
  for (let i = 0; i < n; i++) {
    const xa = av[i] - ma;
    const xb = bv[i] - mb;
    num += xa * xb;
    da += xa * xa;
    db += xb * xb;
  }
  if (da === 0 || db === 0) return 0; // a flat profile has no shape to correlate
  return num / Math.sqrt(da * db);
}

export type FitBucket = 'best' | 'great' | 'good' | 'none';
/** O*NET fit cutoffs on the profile correlation. */
export function fitBucket(r: number): FitBucket {
  if (r >= 0.729) return 'best';
  if (r >= 0.608) return 'great';
  if (r >= 0) return 'good';
  return 'none';
}

// Iachan (1984) "M" — order-/hexagon-aware congruence over two 3-letter codes.
// Weight matrix [person position][environment position]; perfect ordered match = 22+5+1 = 28.
const IACHAN_W = [
  [22, 10, 4],
  [10, 5, 2],
  [4, 2, 1],
];
/** Iachan's M congruence (0-28) between a person code and an environment code. */
export function iachanM(personCode: string, envCode: string): number {
  const pc = personCode.toUpperCase().split('').filter(isLetter).slice(0, 3);
  const ec = envCode.toUpperCase().split('').filter(isLetter).slice(0, 3);
  let m = 0;
  for (let i = 0; i < pc.length; i++) {
    const j = ec.indexOf(pc[i]);
    if (j >= 0 && j < 3) m += IACHAN_W[i][j];
  }
  return m;
}
/** Iachan's M as a 0-100 "interest match" percentage for display. */
export function iachanPct(personCode: string, envCode: string): number {
  return Math.round((iachanM(personCode, envCode) / 28) * 100);
}

// ── Reach (points feasibility) — independent of interest fit ──
export type Reach = 'open' | 'safety' | 'match' | 'reach' | 'out-of-reach';
/** Bucket a course by the gap between the student's points and the course cutoff. */
export function reachBucket(studentPoints: number, coursePoints: number): Reach {
  if (!coursePoints || coursePoints <= 0) return 'open'; // PLC / apprenticeship — no points race
  const diff = studentPoints - coursePoints;
  if (diff >= 30) return 'safety';
  if (diff >= -15) return 'match';
  if (diff >= -60) return 'reach';
  return 'out-of-reach';
}

// ── Eligibility (hard subject gates) — independent of interest fit ──
export interface EligibilityResult { eligible: boolean; missing: string[]; }
export function checkEligibility(requiredSubjects: string[] | undefined, studentSubjects: string[]): EligibilityResult {
  if (!requiredSubjects || requiredSubjects.length === 0) return { eligible: true, missing: [] };
  const have = new Set(studentSubjects.map((s) => s.toLowerCase().trim()));
  const missing = requiredSubjects.filter((r) => !have.has(r.toLowerCase().trim()));
  return { eligible: missing.length === 0, missing };
}

/** Work-values congruence (0-1) — secondary signal, kept separate from interest fit. */
export function workValuesCongruence(studentTop: WorkValue[], courseTop: WorkValue[]): number {
  if (!studentTop.length || !courseTop.length) return 0;
  const cs = new Set(courseTop);
  const overlap = studentTop.filter((v) => cs.has(v)).length;
  return overlap / Math.min(studentTop.length, courseTop.length);
}

/** The three axes for one course, kept SEPARATE (combined only at display time). */
export interface CourseFitResult {
  /** Interest congruence (Pearson r) — never altered by points or subjects. */
  fitR: number;
  fitBucket: FitBucket;
  /** Human-readable interest match %, from Iachan's M. */
  matchPct: number;
  reach: Reach;
  eligibility: EligibilityResult;
  valuesCongruence: number;
}

export function scoreCourseFit(opts: {
  studentProfile: RiasecProfile;
  studentCode: string;
  studentPoints: number;
  studentSubjects: string[];
  studentValues: WorkValue[];
  course: Pick<CourseRiasec, 'riasecProfile' | 'riasecCode' | 'workValues' | 'requiredSubjects'> & { typicalPoints: number };
}): CourseFitResult {
  const fitR = profileCorrelation(opts.studentProfile, opts.course.riasecProfile);
  return {
    fitR,
    fitBucket: fitBucket(fitR),
    matchPct: iachanPct(opts.studentCode, opts.course.riasecCode),
    reach: reachBucket(opts.studentPoints, opts.course.typicalPoints),
    eligibility: checkEligibility(opts.course.requiredSubjects, opts.studentSubjects),
    valuesCongruence: workValuesCongruence(opts.studentValues, opts.course.workValues ?? []),
  };
}
