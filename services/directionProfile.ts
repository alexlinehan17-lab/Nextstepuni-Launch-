import { NORTH_STAR_CATEGORIES, VISION_CARDS } from '../northStarData';
import type { DirectionProfile, DirectionVisionItem, NorthStar } from '../types';

export function getNorthStarCategoryCopy(northStar: NorthStar | null | undefined): string {
  if (!northStar) return '';
  return NORTH_STAR_CATEGORIES.find(category => category.id === northStar.category)?.description ?? '';
}

export function hasStudentAuthoredNorthStar(northStar: NorthStar | null | undefined): boolean {
  if (!northStar?.statement.trim()) return false;
  if (northStar.authoredByStudent !== undefined) return northStar.authoredByStudent;
  return northStar.statement.trim() !== getNorthStarCategoryCopy(northStar).trim();
}

/** Copy safe for ordinary UI. Generic category wording is intentionally not
 * wrapped in quotation marks or described as the student's own words. */
export function getNorthStarDisplayText(northStar: NorthStar | null | undefined): string {
  if (!northStar) return '';
  return hasStudentAuthoredNorthStar(northStar)
    ? northStar.statement.trim()
    : getNorthStarCategoryCopy(northStar);
}

export function createDirectionProfile(northStar: NorthStar, now = new Date().toISOString()): DirectionProfile {
  const safeNorthStar: NorthStar = {
    ...northStar,
    authoredByStudent: hasStudentAuthoredNorthStar(northStar),
    reviewedAt: northStar.reviewedAt ?? now,
  };
  return {
    version: 2,
    northStar: safeNorthStar,
    visionItems: safeNorthStar.visionBoard.map<DirectionVisionItem>(id => ({
      id,
      source: 'onboarding',
      state: 'curious',
      addedAt: safeNorthStar.createdAt || now,
      updatedAt: now,
    })),
    reviewedAt: now,
  };
}

export function normaliseDirectionProfile(raw: unknown, northStar: NorthStar): DirectionProfile {
  const fallback = createDirectionProfile(northStar);
  if (!raw || typeof raw !== 'object') return fallback;
  const candidate = raw as Partial<DirectionProfile>;
  if (candidate.version !== 2 || !Array.isArray(candidate.visionItems)) return fallback;

  const knownIds = new Set(VISION_CARDS.map(card => card.id));
  const items = candidate.visionItems.filter(item => item && typeof item.id === 'string' && knownIds.has(item.id));
  const seen = new Set(items.map(item => item.id));
  for (const item of fallback.visionItems) if (!seen.has(item.id)) items.push(item);

  return {
    version: 2,
    northStar: { ...fallback.northStar, ...(candidate.northStar ?? {}) },
    visionItems: items,
    reviewedAt: candidate.reviewedAt ?? fallback.reviewedAt,
  };
}
