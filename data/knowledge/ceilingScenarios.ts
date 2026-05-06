/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Scenarios for the Sub-task Ceiling Visualiser (Stage 2, E5).
 *
 * Four scenarios — one per cap-rule type that recurs across the LC:
 *   1. English Composition — skipped sub-task → Purpose Ceiling
 *   2. English Comparative — answered on two texts when three were
 *      required
 *   3. Business ABQ — theory + application but no direct case-study
 *      quote
 *   4. Geography option essay — no named example
 *
 * Each scenario carries: the apparent quality of the writing, the marks
 * the student expected, the actual marks under the marking scheme, and
 * the cap level. The answer body is broken into sentences with one
 * flagged as the cap-trigger — the moment in the answer where the cap
 * fired. A counterfactual ("what if you had X") provides the lifted
 * score under that recovery.
 *
 * Per /CLAUDE.md content rule: question prompts paraphrased, never more
 * than 15 words verbatim from any SEC paper.
 *
 * Sources:
 * - English CERs 2008/2013 (Purpose Ceiling, Comparative three-text rule)
 * - 2025 Business HL Marking Scheme (ABQ Theory+Application+Quote rule)
 * - 2012 Geography CER (named example requirement)
 */

import { type CeilingScenario } from '../../types/knowledge';

export const CEILING_SCENARIOS: CeilingScenario[] = [
  // ─── 1. English Composition — skipped sub-task ──────────────────
  {
    id: 'eng-comp-skipped',
    scenarioLabel: 'English Composition — skipped sub-task',
    capRuleLabel: 'Purpose Ceiling',
    apparentQuality: 88,
    studentExpectation: 80,
    actualScore: 50,
    capLevel: 50,
    answerSentences: [
      {
        id: 's1',
        text: 'Opening: "I remember the morning we drove out to the river — the dawn came up over the water like a held breath."',
      },
      {
        id: 's2',
        text: 'Reflection 1: a paragraph on belonging — the writer\'s relationship to the land, sustained through controlled imagery and specific detail.',
      },
      {
        id: 's3',
        text: 'Reflection 2: a paragraph on memory and what stays with us — the writer pivots from external description to interior reflection without losing register.',
      },
      {
        id: 's4',
        text: '"I could go on, but the time has come to draw this to a close."',
        isCapTrigger: true,
      },
      {
        id: 's5',
        text: 'Closing image: the writer returns to the river, dawn fading, the prose still careful and controlled.',
      },
    ],
    counterfactual: {
      actionLabel: 'Spend two minutes on a third reflection — even a paragraph.',
      actionDetail: 'A third reflection lifts the Purpose mark from "partial sub-task coverage" to "full". The Coherence and Language ceilings lift in step. Two minutes\' work is worth ~28 marks.',
      liftedScore: 78,
    },
    crossLink: { moduleId: 'pclm', moduleLabel: 'PCLM Allocator (Stage 1)' },
    source: { section: 'A2', page: 4, cite: 'English Marking Scheme — Purpose Ceiling rule' },
  },

  // ─── 2. Comparative — answered on two texts ─────────────────────
  {
    id: 'eng-comp-two-texts',
    scenarioLabel: 'English Comparative — two texts when three were required',
    capRuleLabel: 'Three-text rubric cap',
    apparentQuality: 80,
    studentExpectation: 70,
    actualScore: 38,
    capLevel: 38,
    answerSentences: [
      {
        id: 's1',
        text: 'Opening: a strong statement of the comparative point on cultural context as a frame for both texts.',
      },
      {
        id: 's2',
        text: 'Sustained analytical paragraph on Text A — integrated comparative voice, specific quotes, clear claim.',
      },
      {
        id: 's3',
        text: 'Sustained analytical paragraph on Text B — counterpoint integrated; the texts are in dialogue.',
      },
      {
        id: 's4',
        text: '"I will briefly mention Text C as well — its context features similar themes."',
        isCapTrigger: true,
      },
      {
        id: 's5',
        text: 'A single sentence gesture at Text C\'s context — no quotation, no integration, no comparative analytical voice.',
      },
      {
        id: 's6',
        text: 'Closing paragraph drawing the comparative back to Text A and B; Text C absent from the conclusion.',
      },
    ],
    counterfactual: {
      actionLabel: 'Give Text C one substantive comparative paragraph.',
      actionDetail: 'The English Chief Examiner is explicit: "candidates… should be prepared to refer to three texts" and "you cannot answer on two films". A single substantive paragraph on Text C lifts the cap from ~50% to upper-band — ~34 extra marks on the 70-mark Comparative.',
      liftedScore: 72,
    },
    source: { section: 'A5', page: 7, cite: 'English Comparative Studies CER — three-text rule' },
  },

  // ─── 3. Business ABQ — no quotes from case study ────────────────
  {
    id: 'biz-abq-no-quote',
    scenarioLabel: 'Business ABQ — no quote from the case study',
    capRuleLabel: 'Theory + Application + Quote',
    apparentQuality: 80,
    studentExpectation: 70,
    actualScore: 50,
    capLevel: 50,
    answerSentences: [
      {
        id: 's1',
        text: 'Identification: "Mary applied a democratic management style throughout her tenure as CEO."',
      },
      {
        id: 's2',
        text: 'Theory: clear definition of democratic management and a link to Maslow / Herzberg motivation theory.',
      },
      {
        id: 's3',
        text: 'Application: "Mary applied this in practice at FreshFoods by holding monthly listening sessions with floor staff."',
      },
      {
        id: 's4',
        text: '"This shows democracy in her style."',
        isCapTrigger: true,
      },
      {
        id: 's5',
        text: 'Evaluation: a strong personal-opinion paragraph on the fit with the food sector, but still no direct quotation from the case study text.',
      },
    ],
    counterfactual: {
      actionLabel: 'Quote one line from the case study, in inverted commas, after each ABQ point.',
      actionDetail: 'The 2025 Business HL Marking Scheme requires Theory + Application + Quote. Without the quote, the link mark is forfeited and the answer caps at theory + application — about 50%. One line of quotation per point lifts the band into upper marks.',
      liftedScore: 75,
    },
    source: { section: 'B7', page: 12, cite: '2025 Business HL Marking Scheme — ABQ link rule' },
  },

  // ─── 4. Geography option essay — no named example ──────────────
  {
    id: 'geo-no-named',
    scenarioLabel: 'Geography option essay — no named example',
    capRuleLabel: 'Named-example anchor',
    apparentQuality: 75,
    studentExpectation: 65,
    actualScore: 35,
    capLevel: 35,
    answerSentences: [
      {
        id: 's1',
        text: 'Opening: a generalised statement about human activity reshaping landscapes — strong vocabulary, no specific region named.',
      },
      {
        id: 's2',
        text: 'Detailed paragraph on agricultural intensification — accurate processes, accurate effects.',
      },
      {
        id: 's3',
        text: '"These changes have transformed many regions in recent decades."',
        isCapTrigger: true,
      },
      {
        id: 's4',
        text: 'Industrialisation paragraph — fluent, technical, but still framed in generalities.',
      },
      {
        id: 's5',
        text: 'Conclusion drawing the threads together; "the region" referred to throughout but never named.',
      },
    ],
    counterfactual: {
      actionLabel: 'Name one specific region in the opening sentence and anchor every SRP back to it.',
      actionDetail: 'Per the 2012 Geography CER and the option-essay marking convention: SRPs about an unnamed region don\'t qualify as "Significant Relevant Points". Naming a specific region (e.g. "Brazil\'s Amazonian frontier") at the top of the answer lets every fluent sentence below count. Lift: ~33 marks on an 80-mark essay.',
      liftedScore: 68,
    },
    source: { section: 'B6', page: 12, cite: '2012 Geography CER — named-example requirement' },
  },
];
