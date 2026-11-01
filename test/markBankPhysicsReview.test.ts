/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Physics paper-by-paper review: every reviewed sitting ships exactly the
 * tasks its ledger records, at the published tariffs, with every printed ask
 * carded (no exclusions, no open asks) and every figure it points at.
 *
 * The ledger (scripts/markbank/authoring/phys_review_<year>_<level>.py) is
 * checked against the SEC PDFs by phys_review.py, which also refuses a task
 * whose rows do not add up to the mark cells the scheme prints against them.
 * This pins what reached the shipped deck, so a later regeneration cannot
 * silently drop or reshape a reviewed sitting. One PINS row per sitting,
 * added when the sitting is written.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as PHYS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import audit from '../scripts/markbank/authored/physics-review-audit.json';
import exclusions from '../scripts/markbank/authoring/exclusions/physics.json';
import physicsFigures from '../components/MarkBank/figures-physics.json';
import sharedFigures from '../components/MarkBank/figures.json';
import { tariffReconciles } from '../types/markBank';

type Task = { id: string; questionRef: string; total: number; route: string | null; status: string;
  evidence?: string; cells?: { printed: string[]; sum: number | null; waiver?: string } };
type Sitting = { tasks: Task[]; cardCount: number; baseTaskCount: number; figures: string[];
  sources: Record<string, { sha256: string; pages: number }>;
  review?: { retained: Array<{ id: string; reason: string }>;
    withdrawn?: Record<string, { replacementId: string; reason: string }> };
  checks: { censusLeaves: number; censusLeavesClaimed: number; excluded: unknown[];
    openLeaves?: unknown[]; excludedLeaves?: unknown[] } };
const sittings = (audit as unknown as { sittings: Record<string, Sitting> }).sittings;

/** sitting -> [cards, tasks, census leaves, paper sha256, scheme sha256] */
const PINS: Record<string, [number, number, number, string, string]> = {
  '2016-ol': [97, 97, 70, 'c3de271bb5e816edfaca05b0ce05fb139b4c8a7b115ea22fb8b7736872e0eb78',
    '12d4feae32ab7ea1926e6c9a67bd07f771a88e850ccda5dac5fc58d01388abf4'],
  '2016-hl': [104, 104, 39, 'f258a6d132ad06476344d78410bdae04ea08050698c2978dc949f5ac35075c97',
    '2e0d63865ce6923c7186e8ab0f51ab66f81b4fceee3c75d3b19a2ff0b4d6eb59'],
  '2017-ol': [97, 97, 96, '918a5a2b1d6ce774cc40a9b0452a7ce11dc2ff4ffb271e1a05cb4d37a761e962',
    '52edb2df4e641d707e1270c131c685bbf5efd3a7258b09625cb543c505579720'],
  '2017-hl': [103, 103, 37, '4a3e69eebd86b3bed98fb557715fdc21511fbfa18895e1728da2a0e519be88de',
    '58265ccb8247b42ff911290cb7fc6c908c033d81490b9400fa0718b5d4b3bbfe'],
  '2018-ol': [100, 100, 97, 'ee7d3000ac3604387d4a12f669cd1884fcbde930f836542b02a757d5fab4fb91',
    '09c42866ecd6660a6bb5f93c00e6011ab92c969d7ab24b991c14283f06cf67a5'],
  '2018-hl': [109, 109, 47, '88fb4b04086dce87adf24edcb7bbf9a6c8d2334db532e9c9d798dfe0974d5eb3',
    '26dc1c8c662bbc3f05b20f629100f5adc9421cae965f2cad90bc8b4ac20be92a'],
  '2019-ol': [103, 103, 100, 'a514daf3e413fe08c8c149bf71e8ae05e964b1bb179f4eb47f0baa6887fa802e',
    '1956ce2b3c7370135b8156ca4e5f6c860258dbc5da692ca1457b14eeb76b3697'],
  '2019-hl': [112, 112, 42, '8c3dc1203ad17cc96558b9911695a8c921656745c1fdf0cb27828a7d0a90295f',
    '9f966f25ff366a276b7281bfda2b2e93231fb7a6d1abc9a831c26715355bf0b3'],
  '2026-ol': [125, 125, 120, 'ea4a0664bb1f14de76db44a5ef8095d76f98baef5266856ce949e29d8c99579e',
    'c7f984734a202b0fa5ef413b805d208c52cdb6bd3239a8513d4e8a6a6129f302'],
  '2026-hl': [136, 136, 107, 'fd1ff3286d201f396a282c38d4bf0f40adf71a1fca80d9111e763a4141a200d5',
    '228dec63cad7a6c8653dfb8b84ac29e908ec34277869cafea69e9481ad199463'],
  '2025-ol': [133, 133, 131, 'e25bb683dbff1c207dc4092b8e2fefb1dda2b1f2c9e294785c37cd99a605fffa',
    'bf8f2367d00286ae516dae6ded5ac311ec596df035f4cb53023decbb6dfc308e'],
  '2025-hl': [137, 137, 125, 'bd8d60f621d8d952e0aaefb054a5e064ea81d6fafcee0501bad5cf10b2ddbf27',
    'f0928d59d20bb0ea168dc17dcaf180b5c68389e8c9fecbf171a17ee90e21ffa2'],
  '2024-ol': [127, 127, 125, '60ef2b1b94f5c60c5589fd019b6ee590fdb0b6253eb2e77d891562255b74314b',
    '13577ca8546caf7e616343950217bebe589aeb71245348318f65c5622146ca51'],
  '2024-hl': [134, 134, 125, '5d9da3b660536b38a60d1494dbf8d83dc6e66ae56e53366d932647cfecc153fc',
    'df74412e93844119feb44c2770ec71490a57bfb80f360364be854fdc637eee5b'],
  '2023-ol': [121, 121, 119, 'd6dff89c7bd732fffcd14557a3d16d71cf17f516ca380ae7234af028997e4511',
    '8bd4e67afb47942be5dc8087860322d606b05a71009d89d2715a0f8fc7ab4b48'],
  '2023-hl': [128, 128, 114, 'aabc53d82a590d2c96556ee256a80f130cea2c2fea7b2b0bbae3f67065dab2a1',
    '9f610bf3f7ce51bdd7ad7b438cd0d5e92ee9cbd6aa10c3f961b081528aac8020'],
  '2022-ol': [127, 127, 125, '5246af9fbc8607914806b471a78ca0805a19cb3e3b038fce7ae45c4e99c9bbd5',
    '7b0ddda535e9dc2a1be382949bced3daf0abc0c3cce10578880a8724fd46fd8d'],
  '2022-hl': [128, 128, 118, '8b9b84d905e1d09691e115178f3d563116233928d075fcea9ffdafe387f26798',
    '7fd0309754396d9091b6dd2d15523d099a469c8d09078a43f145ef2c775e64b3'],
  '2021-hl': [123, 123, 121, '877a47fe07317037cee6147a35ec8648b91052b4748b3580dbf156c60e2c2d39',
    '7184b7194b479b4ee5129ea50847ff6f3a827df37a39f962fc5ccbe85a4b380d'],
  '2021-ol': [130, 130, 130, 'd31e6b959913c35b4700d5d1ec83b554dd1c3e00a7adbe642fdd032204145c1e',
    '228f3336be97ed97331f782625f8238c94b8bd19513519721cf261141c2f7686'],
  '2020-hl': [110, 110, 106, '03fcec1103a5196021790d3f05bd9f4952fdc86509b370d2129ea260e1649add',
    '325af94020ee2310c8afb79615542822b49fcf70c0e0476509657595ae7aa588'],
  '2020-ol': [109, 109, 109, 'f882399a7073efa548667ec51704b8ba9777937ffb91d553a49787095831094d',
    '73d70952c27b742801b3b1f31f9a12bf60e5567e37303a0bfd0b263a9550415d'],
};

type Card = (typeof PHYS_HIGHER)[number] & {
  rows: Array<{ verbatim?: string; contextNote?: string; marks?: number | null }>;
  figure?: { candId: string }; questionFigure?: { candId: string };
};
const deck = [...PHYS_HIGHER, ...PHYS_ORDINARY] as unknown as Card[];
const figureKeys = new Set([...Object.keys(physicsFigures), ...Object.keys(sharedFigures)]);
const UNPRINTED = 'The scheme prints no answer for this part.';

describe('Physics — reviewed sittings', () => {
  it('retains 2016 Ordinary data, choices and exact marking boundaries', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2016-ol-${id}`)!;
    expect(deck.filter(c => c.id.startsWith('phys-2016-ol-'))).toHaveLength(97);
    expect(card('q1-iii-measurements').totalMarks).toBe(6);
    expect(card('q1-iii-calculation').totalMarks).toBe(3);
    expect(card('q4-iii').rows.map(r => [r.verbatim, r.marks]))
      .toEqual([['1', 1], ['4', 1], ['6.25', 1], ['9', 1], ['12.25', 1], ['16', 1]]);
    expect(card('q4-iv').questionFigure?.candId).toBe('physics-2016-ol-q4-graph-question');
    expect(card('q5-d').rows[0].contextNote).not.toContain('Conduction');
    expect(card('q10-iii').rows[0]).toMatchObject({ group: {
      claimMax: 2, perOptionSteps: [6, 3], options: [
        'cathode emits electrons / particles', 'anode attracts / focuses /accelerates (electrons)',
        'screen lights up / shows presence (of electrons)',
      ],
    } });
    expect(card('q10-ii').rows.map(r => r.verbatim)).toEqual(['A — cathode', 'B — anode', 'C — screen']);
    expect(card('q12-c-iv').rows.map(r => r.marks)).toEqual([3, 3, 3]);
    expect(card('q12-c-iv').rows[2].verbatim).toBe('neutral is blue and the earth is green-yellow');
    expect(card('q12-a-i').stem).toContain('9.8 m s⁻²');
    for (const part of 'abcd') {
      expect(deck.filter(c => c.id.startsWith(`phys-2016-ol-q12-${part}-`))
        .reduce((sum, c) => sum + c.totalMarks, 0)).toBe(28);
    }
    for (const part of ['i', 'ii', 'iii']) {
      expect(card(`q8-${part}`).questionFigure?.candId).toMatch(/^physics-2016-ol-q8-/);
      expect(card(`q9-${part}`).stem).toContain('0.75 kg');
      expect(card(`q9-${part}`).stem).toContain('4200 J kg⁻¹ K⁻¹');
      expect(card(`q9-${part}`).stem).toContain('3.3 × 10⁵ J kg⁻¹');
      expect(card(`q9-${part}`).stem).toContain('2200 J kg⁻¹ K⁻¹');
    }
    expect(card('q9-iii').questionText).not.toContain('to to');
    for (const part of 'abcdefgh') expect(card(`q11-${part}`).stem).toContain('Brian Clegg, Icon Books, 2015');
  });

  it('retains every 2016 Higher option, complete source context and corrected mathematical layout', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2016-hl-${id}`)!;
    expect(deck.filter(c => c.id.startsWith('phys-2016-hl-'))).toHaveLength(104);
    expect(card('q2-apparatus').rows[0]).toMatchObject({ group: { claimMax: 3, perOption: 3,
      options: ['stretched string', 'two bridges', 'tuning fork / signal generator', 'newton balance / pulley & (known) weights'],
    } });
    expect(card('q3-method').rows).toHaveLength(6);
    expect(card('q3-method').totalMarks).toBe(15);
    expect(card('q2-ii-density').rows[0].verbatim).toBe('f= 1/(2l) √(T/μ)');
    expect(card('q2-ii-density').questionFigure?.candId).toBe('physics-2016-hl-q2-density-question');
    expect(card('q6-height').rows[0].verbatim).toBe('T=2π√(l/g)');
    expect(card('q6-restoring-force').questionText).toBe('Calculate the restoring force at this point.');
    expect(card('q7-heat-temperature').questionText).toBe('Distinguish between heat and temperature.');
    expect(card('q9-moderator').questionText).toBe('The neutrons emitted are sometimes passed through a moderator. Explain the function of the moderator.');
    expect(card('q9-radium-decay').rows[0].verbatim).toBe('²²⁵₈₈Ra → ²²⁵₈₉Ac + ⁰₋₁e');
    for (const id of ['q10-i-dc-coil', 'q10-ii-resistor-current', 'q10-i-induced-emf', 'q10-ii-ac-current']) {
      expect(card(id).figure?.candId).toBe('physics-2016-hl-q10-circuit');
      expect(card(id).stem).toContain('150 turns');
      expect(card(id).stem).toContain('50 Ω resistor');
    }
    expect(card('q5-j-quarks').totalMarks).toBe(7);
    expect(card('q5-j-relay').totalMarks).toBe(7);
    expect(card('q12-c-i-frequencies').rows[0].contextNote).toContain('fc/(c − u) for the maximum');
    expect(card('q12-c-i-frequencies').rows[0].contextNote).toContain('fc/(c + u) for the minimum');
    for (const part of ['a', 'b', 'c', 'd-i', 'd-ii']) {
      expect(deck.filter(c => c.id.startsWith(`phys-2016-hl-q12-${part}-`))
        .reduce((sum, c) => sum + c.totalMarks, 0)).toBe(28);
    }
    for (const part of 'abcdefgh') {
      expect(card(`q11-${part}`).stem).toContain('Humphrey Lloyd');
      expect(card(`q11-${part}`).stem).toContain('Lisa Randall');
    }
  });

  it('retains 2017 Ordinary context, every labelled pin, and the published stepped responses', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2017-ol-${id}`)!;
    expect(deck.filter(c => c.id.startsWith('phys-2017-ol-'))).toHaveLength(97);
    expect(card('q3-iv').questionFigure?.candId).toBe('physics-2017-ol-q3iv-question');
    expect(card('q3-iv').figure?.candId).toBe('physics-2017-ol-q3iv-solution');
    expect(card('q4-iii').questionFigure?.candId).toBe('physics-2017-ol-q4iii-question');
    expect(card('q5-c').questionText).toContain('ammeter protractor metre stick barometer');
    expect(card('q5-c').rows[0]).toMatchObject({ group: {
      claimMax: 2, perOptionSteps: [4, 3], options: ['ammeter', 'metre stick'],
    } });
    expect(card('q6-i').totalMarks).toBe(18);
    expect(card('q6-i').questionFigure?.candId).toBe('physics-2017-ol-q6i-question');
    expect(card('q6-v').stem).toContain('400 kg');
    expect(card('q6-v').stem).toContain('9.8 m s⁻²');
    expect(card('q6-vii').questionText).toContain('8 m s⁻¹');
    expect(card('q8-viii').stem).toContain('330 m s⁻¹');
    expect(card('q8-viii').figure?.candId).toBe('physics-2017-ol-q8viii-solution');
    for (const id of ['q10-ix-a', 'q10-ix-b']) expect(card(id).totalMarks).toBe(6);
    for (const part of 'abcdefgh') {
      expect(card(`q11-${part}`).stem).toContain('Making the Connection – Plugs and Cable Colours');
      expect(card(`q11-${part}`).stem).toContain('well maintained');
    }
    expect(card('q11-f').kind).toBe('diagram');
    expect(card('q11-f').labelKey).toEqual([
      { letter: 'A', meaning: 'neutral', askedInThisQuestion: true },
      { letter: 'B', meaning: 'live', askedInThisQuestion: true },
      { letter: 'C', meaning: 'earth', askedInThisQuestion: true },
    ]);
    expect(card('q11-f').rows[0]).toMatchObject({ group: { claimMax: 3, perOptionSteps: [3, 2, 2] } });
    expect(card('q12-a-definitions').rows[0]).toMatchObject({ group: { claimMax: 2, perOptionSteps: [6, 3] } });
    for (const part of 'abcd') expect(deck.filter(c => c.id.startsWith(`phys-2017-ol-q12-${part}-`))
      .reduce((sum, c) => sum + c.totalMarks, 0)).toBe(28);
    expect(card('q12-b-iii').stem).toContain('4200 J kg⁻¹ K⁻¹');
    expect(card('q12-c-iii').stem).toContain('10.1 × 10⁴ Pa');
    expect(card('q12-d-iv').questionFigure?.candId).toBe('physics-2017-ol-q12div-question');
    expect(card('q12-d-iv').figure?.candId).toBe('physics-2017-ol-q12div-solution');
  });

  it('retains 2017 Higher optional branches, experimental data, circuit cases and equation layouts', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2017-hl-${id}`)!;
    expect(card('q1-graph').figure?.candId).toBe('physics-2017-hl-q1-data');
    expect(card('q3-latent-heat').questionFigure?.candId).toBe('physics-2017-hl-q3-latent-question');
    expect(card('q3-latent-heat').figure?.candId).toBe('physics-2017-hl-q3-latent-solution');
    expect(card('q3-thermometer').rows[0]).toMatchObject({ group: { claimMax: 2, options: [
      'small heat capacity', 'graduated to 0.1 °C', 'suitable range', 'reacts quickly',
    ] } });
    expect(card('q4-resistances').totalMarks).toBe(9);
    expect(card('q4-resistances').questionText).toContain('0.5 V and (ii) at 8.5 V');
    expect(card('q5-j-gravity').totalMarks).toBe(7);
    expect(card('q5-j-voltmeter').totalMarks).toBe(7);
    expect(card('q6-period').stem).toContain('250 N m⁻¹');
    expect(card('q6-period').stem).toContain('60 kg');
    expect(card('q6-period').figure?.candId).toBe('physics-2017-hl-q6-period-solution');
    expect(card('q8-i-coil').figure?.candId).toBe('physics-2017-hl-q8-coil');
    expect(card('q8-ii-diode').figure?.candId).toBe('physics-2017-hl-q8-diode');
    expect(card('q8-ii-current').questionFigure?.candId).toBe('physics-2017-hl-q8-current-question');
    expect(card('q11-e').stem).toContain('2.6 hour orbit');
    expect(card('q11-g').stem).toContain('29 milliseconds');
    expect(card('q12-a-equilibrium').rows[0]).toMatchObject({ group: { claimMax: 2, perOptionSteps: [6, 3] } });
    for (const branch of ['i', 'ii']) {
      expect(deck.filter(c => c.id.startsWith(`phys-2017-hl-q12-d-${branch}-`))
        .reduce((sum, c) => sum + c.totalMarks, 0)).toBe(28);
    }
    expect(card('q12-b-nuclear-equation').rows[0].verbatim).toContain('K⁴⁰₁₉ → Ca⁴⁰₂₀ + e⁰₋₁');
    expect(card('q12-d-i-reaction').rows[0].verbatim).toContain('Li⁷₃ + H¹₁ → 2He⁴₂');
    expect(card('q12-d-ii-currents').figure?.candId).toBe('physics-2017-hl-q12d-currents-solution');
  });

  it('retains 2018 Ordinary stepped marks, complete context and mathematical figures', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2018-ol-${id}`)!;
    for (const id of ['q1-ii', 'q2-ii', 'q6-i', 'q6-iv']) {
      expect(card(id).totalMarks).toBe(9);
      expect(card(id).rows[0]).toMatchObject({ kind: 'anyN', group: { claimMax: 2, perOptionSteps: [6, 3] } });
    }
    expect(card('q4-ii').rows[0]).toMatchObject({ group: { claimMax: 3, perOptionSteps: [6, 3, 3] } });
    expect(card('q5-c').questionText).toContain('barometer joulemeter lens ohmmeter');
    expect(card('q5-c').rows[0]).toMatchObject({ group: { claimMax: 2, perOptionSteps: [4, 3], options: ['(i) joulemeter', '(ii) ohmmeter'] } });
    expect(card('q6-kinetic-energy-definition').questionText).toBe('Define (ii) kinetic energy.');
    expect(card('q12-a-ii').questionText).toBe('Define (ii) acceleration.');
    expect(card('q6-iv').rows[0]).toMatchObject({ group: { options: ['9000 J', '0 J'] } });
    expect(card('q6-iv').stem).toContain('500 kg');
    expect(card('q6-iv').stem).toContain('300 kg');
    expect(card('q6-iv').figure?.candId).toBe('physics-2018-ol-q6iv-solutions');
    expect(card('q5-b').figure?.candId).toBe('physics-2018-ol-q5b-solution');
    expect(card('q5-b').questionFigure?.candId).toBe('physics-2018-ol-q5b-question');
    expect(card('q8-i').questionFigure?.candId).toBe('physics-2018-ol-q8i-question');
    expect(card('q11-h').stem).toContain('The Physics of Surfing');
    expect(card('q11-h').stem).toContain('University of Southern California');
    expect(card('q11-h').figure?.candId).toBe('physics-2018-ol-q11-surfer');
    expect(card('q11-g').rows[0]).toMatchObject({ group: { claimMax: 2, perOptionSteps: [4, 3], options: ['weight down', 'upthrust up', 'forward force'] } });
    expect(card('q12-c-iii').stem).toContain('4200 J kg⁻¹ K⁻¹');
    expect(card('q12-c-iii').questionFigure?.candId).toBe('physics-2018-ol-q12ciii-question');
    expect(card('q12-c-iii').figure?.candId).toBe('physics-2018-ol-q12ciii-solution');
    for (const part of ['a', 'b', 'c', 'd']) {
      expect(deck.filter(c => c.id.startsWith(`phys-2018-ol-q12-${part}-`))
        .reduce((sum, c) => sum + c.totalMarks, 0)).toBe(28);
    }
    const reviewed = deck.filter(c => c.id.startsWith('phys-2018-ol-'));
    expect(JSON.stringify(reviewed)).not.toMatch(/[\uE000-\uF8FF]/);
    for (const c of reviewed) for (const r of c.rows) {
      const group = (r as { group?: { options: string[] } }).group;
      expect(group?.options ?? []).not.toContain('etc');
    }
  });

  it('retains 2018 Higher context, optional branches, inline asks and mathematical source layouts', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2018-hl-${id}`)!;
    expect(card('q6-b-i').questionText).toContain('Calculate his velocity');
    expect(card('q6-b-i').stem).toContain('10.9 m s⁻¹');
    expect(card('q6-b-i').stem).toContain('43°');
    expect(card('q6-b-i').figure?.candId).toBe('physics-2018-hl-q6bi-solution');
    expect(card('q7-i').figure?.candId).toBe('physics-2018-hl-q7i-solution');
    expect(card('q6-c-i').rows[0]).toMatchObject({ kind: 'point', verbatim: 'energy cannot be created or destroyed' });
    expect(card('q4-graph').figure?.candId).toBe('physics-2018-hl-q4-data');
    expect(card('q4-graph').totalMarks).toBe(15);
    expect(card('q5-j-quarks').totalMarks).toBe(7);
    expect(card('q5-j-and-gate').totalMarks).toBe(7);
    for (const [part, marks] of [['i', 3], ['ii', 6], ['iii', 6], ['iv', 3]] as const) {
      expect(card(`q9-${part}`).totalMarks).toBe(marks);
    }
    expect(card('q9-invisible-spectrum').rows[0]).toMatchObject({
      kind: 'anyN', group: { claimMax: 2, perOption: 3, options: ['ultraviolet', 'X‐rays', 'gamma rays'] },
    });
    expect(card('q10-a-forces').questionText).not.toContain('(12)');
    for (const part of ['a', 'b']) {
      expect(deck.filter(c => c.id.startsWith(`phys-2018-hl-q10-${part}-`))
        .reduce((sum, c) => sum + c.totalMarks, 0)).toBe(56);
    }
    expect(card('q11-g').stem).toContain('570 km');
    expect(card('q11-g').stem).toContain('15.1 orbits per day');
    expect(card('q11-g').stem).toContain('6400 km');
    expect(card('q12-a-shm').questionFigure?.candId).toBe('physics-2018-hl-q12a-underlined');
    expect(card('q12-b-nuclei').figure?.candId).toBe('physics-2018-hl-q12b-data');
  });

  it('retains 2019 Ordinary context, printed choices and separately priced sub-asks', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2019-ol-${id}`)!;
    expect(card('q6-viii').stem).toContain('90 kg');
    expect(card('q6-viii').stem).toContain('17%');
    expect(card('q6-viii').stem).toContain('0.03 m²');
    expect(card('q6-viii').stem).toContain('9.8 m s⁻²');
    expect(card('q5-c').questionText).toContain('ampere coulomb farad volt');
    expect(card('q7-vii').stem).toContain('reflection, refraction, diffraction, interference and polarisation');
    expect(card('q2-iii-a').totalMarks).toBe(6);
    expect(card('q2-iii-b').totalMarks).toBe(6);
    expect(card('q2-iii-b').questionText).toBe('Name (b) one temperature measured.');
    expect(card('q3-iii-measurements').totalMarks).toBe(6);
    expect(card('q3-iii-instrument').totalMarks).toBe(6);
    expect(card('q12-d-i-protons').totalMarks).toBe(4);
    expect(card('q12-d-i-neutrons').totalMarks).toBe(4);
    expect(card('q11-g').totalMarks).toBe(7);
    expect(card('q11-g').questionText).toContain('What is the focal length of this lens?');
    expect(card('q11-f').questionFigure?.candId).toBe('physics-2019-ol-q11f-question');
    expect(card('q11-f').figure?.candId).toBe('physics-2019-ol-q11f-solution');
    expect(card('q9-b-i').figure?.candId).toBe('physics-2019-ol-q9b-parallel');
    expect(card('q9-c-i').figure?.candId).toBe('physics-2019-ol-q9c-plug');
    const plotting = card('q12-c-iii');
    expect(plotting.rows).toHaveLength(3);
    expect(plotting.rows.filter(row => 'route' in row).map(row => row.route).sort()).toEqual(['compass', 'filings']);
  });

  it('keeps adjacent unnumbered 2019 asks separate and retains their necessary context', () => {
    const card = (id: string) => deck.find(c => c.id === `phys-2019-hl-${id}`)!;
    expect(card('q8-line-spectrum').questionText).toBe('What is a line emission spectrum?');
    expect(card('q9-b-graph').questionText).toBe('Plot a graph on graph paper of force against current.');
    expect(card('q12-b-semiconductor').questionText).toBe('What is a semiconductor?');
    expect(card('q12-c-disc-area').stem).toContain('circular window of light on the surface of the water');
    expect(card('q12-d-ii-amplifier').stem).not.toContain('Draw a');
    expect(card('q12-a-conservation').rows[0].contextNote)
      .toContain('award 3 marks to all candidates who attempt Q12 (a)');
    // The paper reuses (i)/(ii) for semiconductor doping and capacitor calculations.
    expect(card('q12-b-i-n-type').totalMarks).toBe(3);
    expect(card('q12-b-i-capacitor-energy').totalMarks).toBe(9);
    expect(card('q12-b-ii-p-type').totalMarks).toBe(3);
    expect(card('q12-b-ii-capacitor-electrons').totalMarks).toBe(7);
  });

  it('explains the 2021 Ordinary source graph’s reversed axes without changing the published marks', () => {
    const card = deck.find(c => c.id === 'phys-2021-ol-q2-v')!;
    expect(card.totalMarks).toBe(12);
    expect(card.rows[0].contextNote).toContain('pressure p on the vertical axis and 1/V on the horizontal axis');
    expect(card.rows[0].contextNote).toContain('official scheme’s sample graph reverses these axes');
    expect(card.figure?.candId).toBe('physics-2021-ol-q2v-scheme-graph');
  });

  it('pins every reviewed sitting, and reviews no sitting it does not pin', () => {
    expect(Object.keys(sittings).sort()).toEqual(Object.keys(PINS).sort());
  });

  it.each(Object.entries(PINS))('%s ships every reviewed task, and nothing else', (key, pin) => {
    const [cards, tasks, leaves, paperSha, schemeSha] = pin;
    const s = sittings[key];
    const [year, level] = key.split('-');
    const prefix = `phys-${year}-${level}-`;
    const shipped = deck.filter(card => card.id.startsWith(prefix));
    // A retained id the review withdrew onto its replacement does not ship.
    const withdrawn = new Set(Object.keys(s.review?.withdrawn ?? {}));
    const retained = new Set((s.review?.retained ?? []).map(r => r.id).filter(id => !withdrawn.has(id)));
    expect(s.cardCount).toBe(cards);
    expect(s.baseTaskCount).toBe(tasks);
    expect(s.sources.paper.sha256).toBe(paperSha);
    expect(s.sources.scheme.sha256).toBe(schemeSha);
    expect(new Set(shipped.map(card => card.id)))
      .toEqual(new Set([...s.tasks.map(task => task.id), ...retained]));
    // Every printed ask is carded: none open, none excluded.
    expect(s.checks.censusLeaves).toBe(leaves);
    expect(s.checks.censusLeavesClaimed).toBe(leaves);
    expect(s.checks.excluded).toEqual([]);
    expect(s.checks.openLeaves ?? []).toEqual([]);
    expect(s.checks.excludedLeaves ?? []).toEqual([]);
    expect(s.tasks.filter(task => task.status === 'excluded')).toEqual([]);
  });

  it.each(Object.keys(PINS))('%s carries each task at its published tariff', (key) => {
    const byId = new Map(deck.map(card => [card.id, card]));
    for (const task of sittings[key].tasks) {
      const card = byId.get(task.id)!;
      expect(card, task.id).toBeDefined();
      expect(card.totalMarks, task.id).toBe(task.total);
      expect(tariffReconciles(card as never), task.id).toBe(true);
      // The mark cells the scheme prints against the rows make the total, or
      // the ledger says why not.
      if (task.cells && task.cells.printed.length && !task.cells.waiver) {
        expect(task.cells.sum, task.id).toBe(task.total);
      }
    }
  });

  it.each(Object.keys(PINS))('%s shows an unprinted answer only as the one row, with its evidence', (key) => {
    const byId = new Map(deck.map(card => [card.id, card]));
    for (const task of sittings[key].tasks) {
      const card = byId.get(task.id)!;
      const unprinted = card.rows.filter(row => row.verbatim === UNPRINTED);
      if (!unprinted.length) continue;
      expect(card.rows, task.id).toHaveLength(1);
      expect(unprinted[0].contextNote, task.id).toBeTruthy();
      expect(task.evidence, task.id).toBeTruthy();
    }
  });

  it.each(Object.keys(PINS))('%s binds every figure it crops, from the manifest', (key) => {
    const [year, level] = key.split('-');
    const prefix = `phys-${year}-${level}-`;
    for (const card of deck.filter(c => c.id.startsWith(prefix))) {
      for (const k of [card.figure?.candId, card.questionFigure?.candId]) {
        if (k) expect(figureKeys.has(k), `${card.id}: ${k}`).toBe(true);
      }
    }
    for (const k of sittings[key].figures) expect(figureKeys.has(k), k).toBe(true);
  });

  it('keeps no exclusion for a reviewed sitting', () => {
    const reviewed = Object.keys(PINS).map(key => {
      const [year, level] = key.split('-');
      return `${year} ${level.toUpperCase()} `;
    });
    const stale = (exclusions as Array<{ ref: string }>).filter(e => reviewed.some(r => e.ref.startsWith(r)));
    expect(stale).toEqual([]);
  });
});
