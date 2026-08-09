import { describe, expect, it } from 'vitest';
import {
  estimateProposedWeeklyJP,
  JOURNEY_ECONOMY_TARGETS,
  JOURNEY_PRICE_BANDS,
  getJourneyV2BasePrice,
  normaliseDailyQuestJP,
  normaliseWeeklyChallengeJP,
  summariseJourneyEconomy,
} from '../journeyEconomyConfig';

describe('Journey economy V2', () => {
  it('places a steady three-session week in the casual target range', () => {
    const points = estimateProposedWeeklyJP({
      sessionMinutes: [25, 25, 25],
      reflections: ['basic', 'basic', 'basic'],
      dailyQuests: 3,
      weeklyChallengePoints: 80,
    });
    expect(points).toBeGreaterThanOrEqual(JOURNEY_ECONOMY_TARGETS.establishedCasualWeek.minimum);
    expect(points).toBeLessThanOrEqual(JOURNEY_ECONOMY_TARGETS.establishedCasualWeek.maximum);
  });

  it('keeps a small building meaningfully above a single normal session', () => {
    const oneSession = estimateProposedWeeklyJP({
      sessionMinutes: [45],
      reflections: ['thoughtful'],
      dailyQuests: 1,
    });
    expect(JOURNEY_PRICE_BANDS.smallBuilding.minimum).toBeGreaterThan(oneSession);
  });

  it('keeps price bands ordered from details through landmarks', () => {
    expect(JOURNEY_PRICE_BANDS.basicTerrain.minimum).toBeGreaterThan(JOURNEY_PRICE_BANDS.smallDetail.minimum);
    expect(JOURNEY_PRICE_BANDS.majorBuilding.minimum).toBeGreaterThan(JOURNEY_PRICE_BANDS.smallBuilding.minimum);
    expect(JOURNEY_PRICE_BANDS.landmark.minimum).toBeGreaterThan(JOURNEY_PRICE_BANDS.majorBuilding.maximum);
  });

  it('makes buildings sustained goals while keeping details reachable', () => {
    expect(getJourneyV2BasePrice({ id: 'bush', name: 'Bush', description: '', model: 'plant_bush.glb', category: 'nature', type: 'decoration', price: 15 })).toBe(35);
    expect(getJourneyV2BasePrice({ id: 'house', name: 'House', description: '', model: 'building-house.glb', category: 'building', type: 'hex', price: 100 })).toBe(200);
    expect(getJourneyV2BasePrice({ id: 'castle', name: 'Castle', description: '', model: 'building-castle.glb', category: 'building', type: 'hex', price: 300 })).toBe(700);
  });

  it('suppresses small cohorts and emits aggregate-only medians', () => {
    const record = { totalEarned: 500, totalSpent: 200, placementCount: 3, sessionPoints: [30, 40] };
    expect(summariseJourneyEconomy(Array(9).fill(record))).toBeNull();
    expect(summariseJourneyEconomy(Array(10).fill(record))).toMatchObject({
      cohortSize: 10,
      medianBalance: 300,
      medianSpendRatio: 0.4,
      medianSessionPoints: 35,
    });
  });

  it('keeps the first-week boost but caps established repeat rewards', () => {
    expect(normaliseDailyQuestJP(45, true)).toBe(45);
    expect(normaliseDailyQuestJP(45, false)).toBe(30);
    expect(normaliseWeeklyChallengeJP(200)).toBe(150);
  });
});
