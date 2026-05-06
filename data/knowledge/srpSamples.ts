/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sample paragraphs for the SRP Identifier (Stage 2 Necessary Knowledge).
 * Each sample is a fictional paragraph in the style of a Higher Level
 * student answer, with per-sentence examiner classification.
 *
 * Per /CLAUDE.md content rule: question prompts paraphrased, never more
 * than 15 words verbatim from any SEC paper.
 *
 * Sources:
 * - Geography 2012 Chief Examiner Report (SRP economy, annotation rule)
 * - History 2017 Chief Examiner Report (DBQ source criticism, RSR)
 * - Business 2025 HL Marking Scheme (ABQ link rule)
 * - Dossier § A2, § B5-B7
 */

import { type SrpSample } from '../../types/knowledge';

export const SRP_SAMPLES: SrpSample[] = [
  // ─── Geography ─────────────────────────────────────────────────────
  {
    id: 'geo-stack',
    subject: 'geography',
    topicLabel: 'Coastal erosion — formation of a sea stack',
    questionPrompt: 'Examine the formation of a coastal landform of erosion that you have studied.',
    marksAvailable: 30,
    srpCap: 15,
    sentences: [
      {
        id: 'g1-1',
        text: 'A sea stack is a tall column of rock that has been separated from the cliff by erosion.',
        type: 'srp',
        developsFactor: 'Definition + landform identification',
      },
      {
        id: 'g1-2',
        text: 'A famous example is the Old Man of Hoy off the coast of Scotland.',
        type: 'srp',
        developsFactor: 'Named example',
      },
      {
        id: 'g1-3',
        text: 'Stacks form in many places around the world and are very interesting.',
        type: 'waffle',
        reason: 'Generic. Adds no factual content that develops the question.',
      },
      {
        id: 'g1-4',
        text: 'Hydraulic action attacks lines of weakness in the cliff face.',
        type: 'srp',
        developsFactor: 'Process — hydraulic action',
        buried: true,
      },
      {
        id: 'g1-5',
        text: 'Trapped air in joints and cracks is compressed by waves; pressure widens the joints over time.',
        type: 'srp',
        developsFactor: 'Process — hydraulic action mechanism',
      },
      {
        id: 'g1-6',
        text: 'Abrasion uses the wave\'s load — pebbles and boulders — as cutting tools against the cliff.',
        type: 'srp',
        developsFactor: 'Process — abrasion',
      },
      {
        id: 'g1-7',
        text: 'This continues for a long time and eventually the rock changes.',
        type: 'waffle',
        reason: 'Vague. "A long time" and "eventually" are filler — no specific process is named.',
      },
      {
        id: 'g1-8',
        text: 'Weathering, particularly freeze-thaw, weakens the cliff top and assists wave erosion below.',
        type: 'srp',
        developsFactor: 'Process — weathering integration',
        buried: true,
      },
      {
        id: 'g1-9',
        text: 'A small notch is cut at the base of the cliff at high-tide level.',
        type: 'srp',
        developsFactor: 'Sequence — notch',
      },
      {
        id: 'g1-10',
        text: 'The notch is enlarged into a wave-cut cave by repeated abrasion.',
        type: 'srp',
        developsFactor: 'Sequence — cave',
      },
      {
        id: 'g1-11',
        text: 'Two caves on either side of a headland may eventually meet, forming a sea arch.',
        type: 'srp',
        developsFactor: 'Sequence — arch',
      },
      {
        id: 'g1-12',
        text: 'Cliffs can be very dangerous to walk near.',
        type: 'unsupported',
        reason: 'Accurate but does not develop the question — there is no SRP credit for safety advice.',
      },
      {
        id: 'g1-13',
        text: 'Continued erosion of the arch base and weathering of the roof eventually causes the roof to collapse.',
        type: 'srp',
        developsFactor: 'Sequence — arch collapse',
      },
      {
        id: 'g1-14',
        text: 'The seaward pillar that remains is the sea stack.',
        type: 'srp',
        developsFactor: 'Sequence — stack identification',
      },
      {
        id: 'g1-15',
        text: 'In time the stack itself will be undercut and collapse, leaving a stump.',
        type: 'srp',
        developsFactor: 'Sequence — stump',
      },
    ],
    source: { section: 'B6', page: 12, cite: '2012 Geography Chief Examiner Report — formation of erosion features' },
  },
  {
    id: 'geo-river',
    subject: 'geography',
    topicLabel: 'Fluvial deposition — formation of a levée',
    questionPrompt: 'Describe the formation of one feature of fluvial deposition.',
    marksAvailable: 30,
    srpCap: 15,
    sentences: [
      {
        id: 'g2-1',
        text: 'A levée is a raised embankment of alluvium that runs parallel to a river channel.',
        type: 'srp',
        developsFactor: 'Definition',
      },
      {
        id: 'g2-2',
        text: 'Levées are found along the lower course of large rivers such as the Mississippi.',
        type: 'srp',
        developsFactor: 'Named example',
      },
      {
        id: 'g2-3',
        text: 'They form because of flooding.',
        type: 'unsupported',
        reason: 'Accurate but undeveloped. The marker is looking for the mechanism, not a label.',
      },
      {
        id: 'g2-4',
        text: 'When the river floods, it bursts its banks and water spreads across the floodplain.',
        type: 'srp',
        developsFactor: 'Process — flooding event',
      },
      {
        id: 'g2-5',
        text: 'The river is very full at this time of year.',
        type: 'waffle',
        reason: 'Generic and partly redundant — adds no process content.',
      },
      {
        id: 'g2-6',
        text: 'On leaving the channel, the velocity of the water drops sharply due to friction with the floodplain surface.',
        type: 'srp',
        developsFactor: 'Process — velocity drop',
        buried: true,
      },
      {
        id: 'g2-7',
        text: 'A drop in velocity reduces the river\'s ability to carry its load — its capacity falls.',
        type: 'srp',
        developsFactor: 'Process — capacity loss',
      },
      {
        id: 'g2-8',
        text: 'The heaviest material in the load — coarse sand and gravel — is deposited first, immediately at the channel margin.',
        type: 'srp',
        developsFactor: 'Process — coarse deposition',
      },
      {
        id: 'g2-9',
        text: 'Finer material is carried further onto the floodplain before being deposited.',
        type: 'srp',
        developsFactor: 'Process — graded deposition',
      },
      {
        id: 'g2-10',
        text: 'Levées are good for farming because they protect the land.',
        type: 'inaccurate',
        reason: 'Levées are the embankments themselves — saying they "protect the land" without naming flood-defence is imprecise.',
      },
      {
        id: 'g2-11',
        text: 'Repeated flooding events deposit successive layers of coarse material, building the embankment up over decades.',
        type: 'srp',
        developsFactor: 'Process — accumulation',
      },
      {
        id: 'g2-12',
        text: 'The embankment is highest closest to the channel and slopes gently away onto the floodplain.',
        type: 'srp',
        developsFactor: 'Morphology',
      },
    ],
    source: { section: 'B6', page: 12, cite: '2012 Geography CER — feature formation requires named process and named example' },
  },
  // ─── History ──────────────────────────────────────────────────────
  {
    id: 'hist-treaty',
    subject: 'history',
    topicLabel: 'Treaty of Versailles — long-question paragraph',
    questionPrompt: 'Discuss the terms of the Treaty of Versailles and their consequences.',
    marksAvailable: 30,
    srpCap: 15,
    sentences: [
      {
        id: 'h1-1',
        text: 'The Treaty of Versailles was signed on 28 June 1919 in the Hall of Mirrors.',
        type: 'srp',
        developsFactor: 'Date + place',
      },
      {
        id: 'h1-2',
        text: 'The treaty placed the war guilt clause, Article 231, on Germany.',
        type: 'srp',
        developsFactor: 'Term — Article 231',
      },
      {
        id: 'h1-3',
        text: 'This was a very harsh thing to do.',
        type: 'waffle',
        reason: 'Opinion without development. Examiners want the consequence, not the moral judgement.',
      },
      {
        id: 'h1-4',
        text: 'Germany was required to pay reparations totalling 132 billion gold marks.',
        type: 'srp',
        developsFactor: 'Term — reparations sum',
        buried: true,
      },
      {
        id: 'h1-5',
        text: 'The German army was reduced to 100,000 men with no air force, no submarines, and only six battleships.',
        type: 'srp',
        developsFactor: 'Term — military restrictions',
      },
      {
        id: 'h1-6',
        text: 'Germany also lost territory on its eastern and western borders.',
        type: 'srp',
        developsFactor: 'Term — territorial loss (general)',
      },
      {
        id: 'h1-7',
        text: 'For example, Alsace-Lorraine was returned to France and the Polish Corridor cut Germany in two.',
        type: 'srp',
        developsFactor: 'Term — territorial loss (specific)',
      },
      {
        id: 'h1-8',
        text: 'These conditions caused great hardship.',
        type: 'unsupported',
        reason: 'Generic — doesn\'t name a specific consequence the marker can credit.',
      },
      {
        id: 'h1-9',
        text: 'Hyperinflation in 1923 — when the dollar reached 4.2 trillion marks — was triggered by reparations and the French occupation of the Ruhr.',
        type: 'srp',
        developsFactor: 'Consequence — hyperinflation',
      },
      {
        id: 'h1-10',
        text: 'The German people felt humiliated and called the treaty a Diktat.',
        type: 'srp',
        developsFactor: 'Consequence — political resentment',
      },
      {
        id: 'h1-11',
        text: 'Hitler used resentment of the treaty as a central plank of the Nazi platform from 1920 onwards.',
        type: 'srp',
        developsFactor: 'Consequence — rise of Nazism',
        buried: true,
      },
      {
        id: 'h1-12',
        text: 'In summary the treaty had many effects on Germany.',
        type: 'waffle',
        reason: 'Restates the question without adding content. Conclusions need to take a position, not summarise.',
      },
    ],
    source: { section: 'B5', page: 11, cite: '2017 History CER — long-question essays marked by paragraph' },
  },
  // ─── Business ─────────────────────────────────────────────────────
  {
    id: 'biz-abq',
    subject: 'business',
    topicLabel: 'ABQ — Theory + Application + Quote',
    questionPrompt: 'Evaluate one factor that influenced the management style at FreshFoods Ltd.',
    marksAvailable: 20,
    srpCap: 10,
    sentences: [
      {
        id: 'b1-1',
        text: 'Mary applied a democratic management style throughout her tenure as CEO.',
        type: 'srp',
        developsFactor: 'Identification — democratic style',
      },
      {
        id: 'b1-2',
        text: 'Democratic management is when staff are consulted on key decisions and feel ownership of outcomes.',
        type: 'srp',
        developsFactor: 'Theory — definition',
      },
      {
        id: 'b1-3',
        text: 'This is a popular style in modern Irish workplaces.',
        type: 'waffle',
        reason: 'General context — does not develop the FreshFoods case.',
      },
      {
        id: 'b1-4',
        text: 'A democratic style increases motivation through Maslow\'s self-actualisation needs and Herzberg\'s motivators.',
        type: 'srp',
        developsFactor: 'Theory — motivation linkage',
        buried: true,
      },
      {
        id: 'b1-5',
        text: 'It also slows decision-making, as consultation takes time, which can hurt fast-moving sectors.',
        type: 'srp',
        developsFactor: 'Theory — drawback',
      },
      {
        id: 'b1-6',
        text: 'Mary applied this in practice at FreshFoods by holding monthly listening sessions with floor staff.',
        type: 'srp',
        developsFactor: 'Application — monthly meetings',
      },
      {
        id: 'b1-7',
        text: 'Mary said in the case study that she "ran every major decision past the floor before signing off".',
        type: 'srp',
        developsFactor: 'Quote — direct from case',
      },
      {
        id: 'b1-8',
        text: 'This shows democracy in her style.',
        type: 'unsupported',
        reason: 'Bald restatement. The quote already showed it; this sentence adds nothing.',
      },
      {
        id: 'b1-9',
        text: 'In my opinion this style is well-suited to FreshFoods because the workforce is highly skilled and engagement drives innovation in food product development.',
        type: 'srp',
        developsFactor: 'Evaluation — student opinion (required for "Evaluate")',
      },
      {
        id: 'b1-10',
        text: 'Overall the style was good for the company.',
        type: 'waffle',
        reason: 'Vague conclusion. "Evaluate" requires a reasoned judgement, not a verdict.',
      },
    ],
    source: { section: 'B7', page: 12, cite: '2025 Business HL Marking Scheme — ABQ Theory + Application + Quote rule' },
  },
];
