/** Recommendation ordering for Future Finder. Interest fit remains separately inspectable. */
import type { CAOCourse } from './futureFinderData';
import type { CourseFitResult } from './futureFinderRiasec';
import { getPointsForGrade, LC_SUBJECTS, type StudentSubjectProfile } from './subjectData';

/** Bump when the persisted top-ten ordering policy changes. */
export const RECOMMENDATION_RANKING_VERSION = 3;

/**
 * Best-six projected CAO points from the targets the student chose.
 * A missing target falls back to the current grade, so older profiles remain
 * useful without silently treating the subject as zero.
 */
export function computeTargetCAOPoints(profile: StudentSubjectProfile): number {
  return profile.subjects
    .map((subject) => getPointsForGrade(
      subject.targetGrade ?? subject.currentGrade,
      LC_SUBJECTS.find((candidate) => candidate.name === subject.subjectName)?.isMaths || false,
    ))
    .sort((a, b) => b - a)
    .slice(0, 6)
    .reduce((sum, points) => sum + points, 0);
}

export type RecommendationBand = 'realistic' | 'ambitious' | 'explore';
export interface RecommendationRank {
  score: number;
  band: RecommendationBand;
  interestScore: number;
  pointsScore: number;
  routeScore: number;
  valuesScore: number;
}

/** Continuous rather than bucket-only because annual cut-offs are indicative, not guarantees. */
export function pointsFeasibility(targetPoints: number, coursePoints: number): number {
  if (coursePoints <= 0) return 1;
  const gap = coursePoints - targetPoints;
  if (gap <= 15) return 1;
  if (gap <= 60) return 1 - ((gap - 15) / 45) * 0.45;
  if (gap <= 120) return 0.55 - ((gap - 60) / 60) * 0.4;
  return 0.08;
}

/** Prefer an attainment-appropriate route without declaring lower NFQ levels inferior. */
export function routeAlignment(targetPoints: number, course: Pick<CAOCourse, 'level' | 'pathwayType'>): number {
  if (course.pathwayType === 'apprenticeship') return targetPoints >= 450 ? 0.55 : 0.9;
  if (course.pathwayType === 'plc' || course.level === 5) return targetPoints >= 450 ? 0.25 : targetPoints >= 300 ? 0.65 : 1;
  if (course.level === 6) return targetPoints >= 450 ? 0.35 : targetPoints >= 300 ? 0.75 : 1;
  if (course.level === 7) return targetPoints >= 450 ? 0.5 : targetPoints >= 300 ? 1 : 0.9;
  return targetPoints >= 450 ? 1 : targetPoints >= 300 ? 0.9 : 0.45;
}

export function recommendationBand(fit: CourseFitResult): RecommendationBand {
  if (!fit.eligibility.eligible || fit.reach === 'out-of-reach') return 'explore';
  if (fit.reach === 'reach') return 'ambitious';
  return 'realistic';
}

export function scoreRecommendation(course: CAOCourse, fit: CourseFitResult, targetPoints: number): RecommendationRank {
  // Pearson r=0 means no relationship, not a half-strength recommendation.
  // Squaring the normalised correlation preserves excellent matches while
  // preventing neutral or weakly related routes from filling the top ten.
  const normalisedInterest = Math.max(0, Math.min(1, (fit.fitR + 1) / 2));
  const interestScore = normalisedInterest ** 2;
  const pointsScore = pointsFeasibility(targetPoints, course.typicalPoints);
  const routeScore = routeAlignment(targetPoints, course);
  const valuesScore = fit.valuesCongruence;
  const eligibilityMultiplier = fit.eligibility.eligible ? 1 : 0.55;
  const attainmentGap = course.typicalPoints > 0 ? course.typicalPoints - targetPoints : 0;
  // Keep a nearby stretch visible, but do not let a 500-point course become a
  // leading recommendation for a student projecting roughly 100 points.
  const extremeStretchMultiplier = attainmentGap > 250 ? 0.7 : attainmentGap > 180 ? 0.82 : 1;
  const score = (
    interestScore * 0.58
    + pointsScore * 0.22
    + valuesScore * 0.12
    + routeScore * 0.08
  ) * eligibilityMultiplier * extremeStretchMultiplier;
  return { score, band: recommendationBand(fit), interestScore, pointsScore, routeScore, valuesScore };
}

/**
 * Feasibility should influence the order, but must not overwhelm relevance.
 * An absolute band sort made unrelated PLCs outrank strongly matched courses
 * that were only modestly above a student's target. These calibrated bonuses
 * keep credible routes prominent while allowing a much better fit through.
 */
const BAND_BONUS: Record<RecommendationBand, number> = {
  realistic: 0.1,
  ambitious: 0.04,
  explore: 0,
};
const BAND_ORDER: Record<RecommendationBand, number> = { realistic: 0, ambitious: 1, explore: 2 };
export function compareRecommendations(
  a: { recommendation: RecommendationRank; fit: CourseFitResult },
  b: { recommendation: RecommendationRank; fit: CourseFitResult },
): number {
  const aRankScore = a.recommendation.score + BAND_BONUS[a.recommendation.band];
  const bRankScore = b.recommendation.score + BAND_BONUS[b.recommendation.band];
  const score = bRankScore - aRankScore;
  const band = BAND_ORDER[a.recommendation.band] - BAND_ORDER[b.recommendation.band];
  return score || band || b.fit.fitR - a.fit.fitR;
}
