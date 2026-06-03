/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * futureFinderRevampedAdapter — bridges the RIASEC scoring engine
 * (futureFinderRiasec.ts) into the shape the shared results UI
 * (FutureFinderResults.tsx) expects (a DisplayResult per course).
 *
 * The cardinal rule of the RIASEC engine is preserved: the headline match %
 * comes purely from interest fit (`fit.matchPct`) and is NEVER mixed with
 * points. Points "reach" is carried as a SEPARATE badge axis only.
 */
import { type DisplayResult } from './FutureFinderResults';
import { type CAOCourse } from './futureFinderData';
import {
  RIASEC_LABELS, WORK_VALUE_LABELS,
  type RiasecLetter, type WorkValue, type CourseFitResult,
} from './futureFinderRiasec';
import { COURSE_RIASEC } from './futureFinderRiasecData';

/** Reach metadata shared with FutureFinderRevamped's results list. */
export const REACH_META: Record<string, { label: string; color: string; bg: string }> = {
  safety: { label: 'Comfortable on points', color: '#1F5F3E', bg: '#E8F2EC' },
  match: { label: 'On target', color: '#2A5F8F', bg: '#E6EEF7' },
  reach: { label: 'A stretch', color: '#8C5A12', bg: '#FBF1E0' },
  'out-of-reach': { label: 'Big points stretch', color: '#8a5a5a', bg: '#F3ECEC' },
  open: { label: 'No points race', color: '#1F5F3E', bg: '#E8F2EC' },
};

/** Maps a reach bucket to a feasibility score (0-1) for the third score bar. */
const REACH_FEASIBILITY: Record<CourseFitResult['reach'], number> = {
  open: 1,
  safety: 1,
  match: 0.75,
  reach: 0.45,
  'out-of-reach': 0.15,
};

/** Reach -> a short, honest one-liner used in the "Why this suits you" reasons. */
const REACH_REASON: Record<CourseFitResult['reach'], string> = {
  open: 'Comfortable on your current points',
  safety: 'Comfortable on your current points',
  match: 'On target for the points',
  reach: 'A points stretch — reachable with strong results',
  'out-of-reach': 'A big points stretch this year',
};

/**
 * Build the interest-based reasons list (3-6 strings) in the original tool's
 * voice. Interest first, then a per-shared-letter overlap line, then values,
 * then a points-reach line, then eligibility, with a career-paths fallback.
 */
function buildReasons(
  course: CAOCourse,
  fit: CourseFitResult,
  studentTopLetters: RiasecLetter[],
  studentValues: WorkValue[],
): string[] {
  const reasons: string[] = [];
  const cr = COURSE_RIASEC[course.code];
  const courseLetters = (cr?.riasecCode ?? '')
    .toUpperCase()
    .split('')
    .filter((c): c is RiasecLetter => (['R', 'I', 'A', 'S', 'E', 'C'] as string[]).includes(c));

  // 1. Strong-fit line for the top buckets, naming the course's leading types.
  if ((fit.fitBucket === 'best' || fit.fitBucket === 'great') && courseLetters.length > 0) {
    const top = courseLetters.slice(0, 2).map((l) => RIASEC_LABELS[l]).join(' & ');
    reasons.push(`Strong fit for ${top} interests`);
  }

  // 2. Per-shared-letter overlap line.
  const shared = courseLetters.filter((l) => studentTopLetters.includes(l));
  if (shared.length > 0) {
    reasons.push(`Matches your ${shared.map((l) => RIASEC_LABELS[l]).join(' & ')} side`);
  }

  // 3. Values line.
  if (fit.valuesCongruence > 0) {
    const sharedValues = studentValues.filter((v) => (cr?.workValues ?? []).includes(v));
    if (sharedValues.length > 0) {
      reasons.push(`Fits what you value: ${sharedValues.map((v) => WORK_VALUE_LABELS[v]).join(' & ')}`);
    }
  }

  // 4. Points-reach line.
  reasons.push(REACH_REASON[fit.reach]);

  // 5. Eligibility line, when a hard subject gate is unmet.
  if (fit.eligibility.missing.length > 0) {
    reasons.push(`Needs ${fit.eligibility.missing.join(' & ')} — check requirements`);
  }

  // 6. Fallback so a card is never reason-less.
  if (reasons.length === 0 && course.careerPaths.length > 0) {
    reasons.push(`Career paths include ${course.careerPaths.slice(0, 2).join(' and ')}`);
  }

  return reasons;
}

/**
 * Convert a scored RIASEC course into a DisplayResult for the shared results UI.
 *
 * - `score` is interest match % only (fit.matchPct / 100), never blended with points.
 * - The three score-breakdown bars are: interest (Pearson r, mapped to 0-1),
 *   values congruence, and a points-reach-derived feasibility.
 * - `reach` is the separate points badge.
 * - `subjectAlignment` is 'partial' when eligible (suppresses BOTH the
 *   "Subjects align" and "Check requirements" pills) and 'none' when ineligible
 *   (shows the "Check requirements" warning).
 */
export function riasecToRecommendation(
  course: CAOCourse,
  fit: CourseFitResult,
  studentTopLetters: RiasecLetter[],
  studentValues: WorkValue[],
): DisplayResult {
  const reachMeta = REACH_META[fit.reach];
  return {
    course,
    score: fit.matchPct / 100,
    reasons: buildReasons(course, fit, studentTopLetters, studentValues),
    scoreBreakdown: {
      interestScore: (fit.fitR + 1) / 2,
      valuesScore: fit.valuesCongruence,
      feasibilityScore: REACH_FEASIBILITY[fit.reach],
    },
    subjectAlignment: fit.eligibility.eligible ? 'partial' : 'none',
    reach: { label: reachMeta.label, color: reachMeta.color, bg: reachMeta.bg },
  };
}
