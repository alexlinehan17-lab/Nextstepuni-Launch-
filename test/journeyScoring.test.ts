/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, test } from 'vitest';

import {
  ARCHETYPES,
  CAPABILITY_KEYS,
  INITIAL_GAME_STATE,
  ROUTE_RESOLVERS,
  STORY_DATA,
  applyJourneyChoice,
  createJourneyEvidence,
  getWeakestCapability,
  normaliseCapabilityImpact,
  normaliseEnergyImpact,
  selectJourneyEnding,
  type Choice,
  type GameState,
  type HistoryItem,
} from '@/components/journeySimulatorData';

const makeHistoryItem = (sceneId: string, choiceText = 'Test choice'): HistoryItem => ({
  scene: STORY_DATA[sceneId],
  choiceText,
  effects: {},
});

const resolveTarget = (target: string, state: GameState, history: HistoryItem[]): string => {
  let current = target;
  let guard = 0;
  while (current.startsWith('__') && ROUTE_RESOLVERS[current]) {
    current = ROUTE_RESOLVERS[current](state, history);
    guard += 1;
    if (guard > 10) throw new Error(`Resolver loop at ${target}`);
  }
  return current;
};

const seededRandom = (seed: number): (() => number) => () => {
  seed |= 0;
  seed = seed + 0x6D2B79F5 | 0;
  let value = Math.imul(seed ^ seed >>> 15, 1 | seed);
  value = value + Math.imul(value ^ value >>> 7, 61 | value) ^ value;
  return ((value ^ value >>> 14) >>> 0) / 4294967296;
};

describe('Academic Journey scoring model', () => {
  test('normalises authored magnitudes and keeps energy separate from capability evidence', () => {
    const alternatives: Choice[] = [
      { text: 'Measured practice', effects: { academicCap: 15, energy: -5 }, nextSceneId: 'START' },
      { text: 'Avoid practice', effects: { academicCap: -15, energy: 5 }, nextSceneId: 'START' },
    ];

    const result = applyJourneyChoice(
      { ...INITIAL_GAME_STATE },
      createJourneyEvidence(),
      alternatives[0],
      alternatives,
    );

    expect(result.evidence.academicCap).toEqual({ earned: 2, possible: 2 });
    expect(result.state.academicCap).toBe(63);
    expect(result.state.energy).toBe(63);
    expect(result.state.socialSupport).toBe(50);
  });

  test('does not score safety choices or use them as capability opportunities', () => {
    const safetyChoice: Choice = {
      text: 'Tell the responsible adult',
      effects: {},
      nextSceneId: 'START',
      scoreless: true,
    };
    const result = applyJourneyChoice(
      { ...INITIAL_GAME_STATE },
      createJourneyEvidence(),
      safetyChoice,
      [
        safetyChoice,
        { text: 'Scored alternative', effects: { resilience: 15 }, nextSceneId: 'START' },
      ],
    );

    expect(result.state).toEqual(INITIAL_GAME_STATE);
    expect(result.evidence).toEqual(createJourneyEvidence());
  });

  test('reports tied growth edges instead of silently choosing the first field', () => {
    expect(getWeakestCapability({
      energy: 5,
      academicCap: 42,
      socialSupport: 42,
      systemSavvy: 70,
      resilience: 65,
    })).toEqual(['academicCap', 'socialSupport']);
  });

  test('requires route evidence before assigning route-specific profiles', () => {
    const opportunityState: GameState = {
      energy: 70,
      academicCap: 80,
      socialSupport: 75,
      systemSavvy: 100,
      resilience: 80,
    };
    expect(selectJourneyEnding(opportunityState, [])).not.toBe('END_SCHOLARSHIP');
    expect(selectJourneyEnding(opportunityState, [makeHistoryItem('SCHOLARSHIP_PATH')])).toBe('END_SCHOLARSHIP');

    const recoveryState: GameState = {
      energy: 55,
      academicCap: 78,
      socialSupport: 78,
      systemSavvy: 76,
      resilience: 90,
    };
    expect(selectJourneyEnding(recoveryState, [])).not.toBe('END_COMEBACK');
    expect(selectJourneyEnding(recoveryState, [makeHistoryItem('PASSIVE_SPIRAL')])).toBe('END_COMEBACK');
  });

  test('keeps low-evidence profiles reachable after a sustained adverse route', () => {
    let state = { ...INITIAL_GAME_STATE };
    let evidence = createJourneyEvidence();
    let sceneId = 'START';
    const history: HistoryItem[] = [];
    let decisions = 0;

    while (!sceneId.startsWith('END_') && decisions < 80) {
      const scene = STORY_DATA[sceneId];
      const choices = scene.choices ?? [];
      const choice = [...choices].sort((a, b) => {
        const impact = (candidate: Choice) => CAPABILITY_KEYS.reduce(
          (sum, key) => sum + normaliseCapabilityImpact(candidate.effects[key]),
          normaliseEnergyImpact(candidate.effects.energy) / 5,
        );
        return impact(a) - impact(b);
      })[0];
      const update = applyJourneyChoice(state, evidence, choice, choices);
      state = update.state;
      evidence = update.evidence;
      history.push({ scene, choiceText: choice.text, effects: choice.effects, moduleLink: choice.moduleLink });
      sceneId = resolveTarget(choice.nextSceneId, state, history);
      decisions += 1;
    }

    expect(decisions).toBeLessThan(80);
    expect(['END_REGROUPING', 'END_REPEAT']).toContain(sceneId);
    expect(CAPABILITY_KEYS.reduce((sum, key) => sum + state[key], 0) / CAPABILITY_KEYS.length).toBeLessThan(55);
    expect(state.energy).toBeLessThan(20);
  });

  test('keeps support open and uses safe crisis guidance', () => {
    for (const scene of Object.values(STORY_DATA)) {
      for (const choice of scene.choices ?? []) {
        expect('requires' in choice, `${scene.id}: ${choice.text}`).toBe(false);
      }
    }

    const friendChoices = STORY_DATA.FRIEND_IN_CRISIS.choices ?? [];
    expect(friendChoices).toHaveLength(3);
    expect(friendChoices.every(choice => choice.scoreless && Object.keys(choice.effects).length === 0)).toBe(true);
    expect(friendChoices.map(choice => choice.text).join(' ')).toMatch(/112\/999/);
    expect(friendChoices.map(choice => choice.text).join(' ')).toMatch(/trusted adult/i);

    const classroomChoices = STORY_DATA.GRACE_UNDER_PRESSURE.choices ?? [];
    expect(classroomChoices.every(choice => choice.scoreless)).toBe(true);
    expect(classroomChoices[0].text).toMatch(/alert the teacher immediately/i);
  });

  test('contains the corrected application guidance and non-predictive endings', () => {
    expect(STORY_DATA.CAO_DEADLINE.text).toMatch(/Level 8 courses.*Level 7\/6 courses/i);
    expect(STORY_DATA.CAO_DEADLINE.text).toMatch(/genuine order of preference/i);
    expect(STORY_DATA.ASSESSMENT_DEADLINES.text).toMatch(/oral, practical, project or coursework/i);

    for (const endingId of Object.keys(ARCHETYPES)) {
      expect(STORY_DATA[endingId].text, endingId).not.toMatch(/got your course|offer received|secured a PLC|you(?:'re| are) repeating|scholarship\. HEAR/i);
    }
  });

  test('keeps all authored targets valid and the formerly dead scenes reachable', () => {
    for (const scene of Object.values(STORY_DATA)) {
      for (const choice of scene.choices ?? []) {
        expect(
          Boolean(STORY_DATA[choice.nextSceneId] || ROUTE_RESOLVERS[choice.nextSceneId]),
          `${scene.id} points to missing target ${choice.nextSceneId}`,
        ).toBe(true);
      }
    }

    const directTargets = new Set(
      Object.values(STORY_DATA).flatMap(scene => (scene.choices ?? []).map(choice => choice.nextSceneId)),
    );
    expect(directTargets.has('TEACHING_LEGACY')).toBe(true);
    expect(directTargets.has('__COMEBACK_CHECK__')).toBe(true);
    expect(ROUTE_RESOLVERS.__COMEBACK_CHECK__(
      { ...INITIAL_GAME_STATE, resilience: 70 },
      [makeHistoryItem('PASSIVE_SPIRAL')],
    )).toBe('COMEBACK_RALLY');
    expect(ROUTE_RESOLVERS.__SYSTEM_MASTERY_CHECK__({ ...INITIAL_GAME_STATE, systemSavvy: 70 })).toBe('SYSTEM_MASTERY');
  });

  test('completes varied seeded journeys without the old energy collapse or score saturation', () => {
    const random = seededRandom(20260814);
    const endings = new Map<string, number>();
    const visited = new Set<string>();
    const energies: number[] = [];
    const capabilityScores: number[] = [];
    const runCount = 10_000;

    for (let run = 0; run < runCount; run += 1) {
      let state = { ...INITIAL_GAME_STATE };
      let evidence = createJourneyEvidence();
      let sceneId = 'START';
      const history: HistoryItem[] = [];
      let decisions = 0;

      while (!sceneId.startsWith('END_') && decisions < 80) {
        const scene = STORY_DATA[sceneId];
        expect(scene, `Missing scene ${sceneId}`).toBeDefined();
        visited.add(sceneId);
        const choices = scene.choices ?? [];
        expect(choices.length, `No choices at ${sceneId}`).toBeGreaterThan(0);
        const choice = choices[Math.floor(random() * choices.length)];
        const update = applyJourneyChoice(state, evidence, choice, choices);
        state = update.state;
        evidence = update.evidence;
        history.push({ scene, choiceText: choice.text, effects: choice.effects, moduleLink: choice.moduleLink });
        sceneId = resolveTarget(choice.nextSceneId, state, history);
        decisions += 1;
      }

      expect(decisions).toBeLessThan(80);
      expect(sceneId.startsWith('END_')).toBe(true);
      endings.set(sceneId, (endings.get(sceneId) ?? 0) + 1);
      energies.push(state.energy);
      capabilityScores.push(...CAPABILITY_KEYS.map(key => state[key]));
    }

    energies.sort((a, b) => a - b);
    const energyMedian = energies[Math.floor(energies.length / 2)];
    const lowEnergyShare = energies.filter(value => value < 40).length / runCount;
    const topEndingShare = Math.max(...endings.values()) / runCount;
    expect(visited.has('SYSTEM_MASTERY')).toBe(true);
    expect(visited.has('TEACHING_LEGACY')).toBe(true);
    expect(visited.has('COMEBACK_RALLY')).toBe(true);
    expect(
      Object.values(STORY_DATA)
        .filter(scene => !scene.id.startsWith('END_') && !visited.has(scene.id))
        .map(scene => scene.id),
    ).toEqual([]);
    expect(endings.size).toBeGreaterThanOrEqual(7);
    expect(topEndingShare).toBeLessThan(0.65);
    expect(energyMedian).toBeGreaterThanOrEqual(45);
    expect(lowEnergyShare).toBeLessThan(0.45);
    expect(Math.max(...capabilityScores)).toBeLessThanOrEqual(90);
    expect(capabilityScores.filter(value => value >= 95)).toHaveLength(0);
  });
});
