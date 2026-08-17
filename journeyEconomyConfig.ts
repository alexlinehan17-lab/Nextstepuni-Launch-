/**
 * Journey economy V2. Values are centralised here so evidence-led adjustments
 * do not require hunting through UI components.
 */
import type { ShopItem } from './types';

export const JOURNEY_ECONOMY_TARGETS = {
  firstDay: { minimum: 50, maximum: 80 },
  firstSevenDays: { minimum: 350, maximum: 500 },
  establishedCasualWeek: { minimum: 200, maximum: 300 },
  establishedConsistentWeek: { minimum: 350, maximum: 500 },
  establishedHighlyActiveWeek: { minimum: 500, maximum: 650 },
} as const;

export const JOURNEY_JP_V2 = {
  studyPerTenMinutes: 10,
  reflection: {
    basic: 10,
    thoughtful: 15,
    deep: 20,
  },
  sectionComplete: 2,
  moduleCompleteBonus: 6,
  categoryCompleteBonus: 20,
  dailyQuest: { minimum: 20, maximum: 30 },
  weeklyChallenge: { minimum: 80, maximum: 150 },
  fullRateSessionsPerDay: 2,
  additionalSessionMultiplier: 0.5,
} as const;

export function normaliseWeeklyChallengeJP(points: number): number {
  return Math.min(JOURNEY_JP_V2.weeklyChallenge.maximum, Math.max(JOURNEY_JP_V2.weeklyChallenge.minimum, points));
}

/** The first week intentionally pays a little more; established daily quests
 * settle into the sustainable band below. */
export function normaliseDailyQuestJP(points: number, isOnboarding: boolean): number {
  if (isOnboarding) return points;
  return Math.min(JOURNEY_JP_V2.dailyQuest.maximum, Math.max(JOURNEY_JP_V2.dailyQuest.minimum, points));
}

export const JOURNEY_PRICE_BANDS = {
  smallDetail: { minimum: 25, maximum: 45 },
  natureOrBoundary: { minimum: 45, maximum: 75 },
  furniture: { minimum: 60, maximum: 110 },
  basicTerrain: { minimum: 50, maximum: 80 },
  specialTerrainOrPath: { minimum: 80, maximum: 140 },
  smallBuilding: { minimum: 160, maximum: 240 },
  majorBuilding: { minimum: 300, maximum: 500 },
  landmark: { minimum: 700, maximum: 1200 },
} as const;

export interface EstablishedWeekScenario {
  sessionMinutes: number[];
  reflections: Array<keyof typeof JOURNEY_JP_V2.reflection | 'none'>;
  dailyQuests: number;
  weeklyChallengePoints?: number;
}

/** Pure scenario calculator used to keep proposed pacing auditable. */
export function estimateProposedWeeklyJP(scenario: EstablishedWeekScenario): number {
  const sessionPoints = scenario.sessionMinutes.reduce((sum, minutes) => {
    return sum + Math.floor(minutes / 10) * JOURNEY_JP_V2.studyPerTenMinutes;
  }, 0);
  const reflectionPoints = scenario.reflections.reduce<number>((sum, tier) => {
    return sum + (tier === 'none' ? 0 : JOURNEY_JP_V2.reflection[tier]);
  }, 0);
  const questPoints = scenario.dailyQuests * JOURNEY_JP_V2.dailyQuest.minimum;
  return sessionPoints + reflectionPoints + questPoints + (scenario.weeklyChallengePoints ?? 0);
}

export function getJourneyV2BasePrice(item: ShopItem): number {
  if (item.price === 0) return 0;
  if (item.category === 'terrain') return /forest|hill|desert|rocks|mountain|lumber/.test(item.model) ? 90 : 60;
  if (item.category === 'path') return item.model === 'bridge.glb' ? 140 : 100;
  if (item.category === 'building') {
    if (/castle|wizard|village/.test(item.model)) return 700;
    if (/tower|watermill|market/.test(item.model)) return 320;
    return 200;
  }
  if (item.category === 'vehicle') return 350;
  if (item.category === 'furniture') return 80;
  if (item.category === 'nature') return item.model.startsWith('tree_') ? 55 : 35;
  if (/fountain|windmill|campfire|tent/.test(item.model)) return 90;
  return 45;
}

export interface JourneyEconomyRecord {
  totalEarned: number;
  totalSpent: number;
  placementCount: number;
  sessionPoints?: number[];
}

/** Aggregate-only evidence from progress data the product already needs.
 * Small cohorts are suppressed so this cannot become a student report. */
export function summariseJourneyEconomy(records: JourneyEconomyRecord[], minimumCohortSize = 10) {
  if (records.length < minimumCohortSize) return null;
  const median = (values: number[]) => {
    const ordered = [...values].sort((a, b) => a - b);
    const middle = Math.floor(ordered.length / 2);
    return ordered.length % 2 ? ordered[middle] : (ordered[middle - 1] + ordered[middle]) / 2;
  };
  const balances = records.map(record => Math.max(0, record.totalEarned - record.totalSpent));
  const spendRatios = records.map(record => record.totalEarned > 0 ? record.totalSpent / record.totalEarned : 0);
  const sessionPoints = records.flatMap(record => record.sessionPoints ?? []);
  return {
    cohortSize: records.length,
    medianEarned: median(records.map(record => record.totalEarned)),
    medianSpent: median(records.map(record => record.totalSpent)),
    medianBalance: median(balances),
    medianSpendRatio: median(spendRatios),
    medianPlacements: median(records.map(record => record.placementCount)),
    medianSessionPoints: sessionPoints.length ? median(sessionPoints) : null,
  };
}
