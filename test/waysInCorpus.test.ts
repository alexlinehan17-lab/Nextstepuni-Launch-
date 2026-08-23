/**
 * Ways In corpus guard — every built SEC card must survive the support handoff
 * without its exact question changing or any marking-scheme fields crossing the
 * boundary. Command coverage is monitored across the real corpus so a future
 * authoring wave cannot silently turn the interpreter into an empty scaffold.
 */
import { describe, expect, test } from 'vitest';

import { CARDS as agHigher } from '@/components/MarkBank/cards/agricultural-science/higher';
import { CARDS as agOrdinary } from '@/components/MarkBank/cards/agricultural-science/ordinary';
import { CARDS as biologyHigher } from '@/components/MarkBank/cards/biology/higher';
import { CARDS as biologyOrdinary } from '@/components/MarkBank/cards/biology/ordinary';
import { CARDS as businessHigher } from '@/components/MarkBank/cards/business/higher';
import { CARDS as businessOrdinary } from '@/components/MarkBank/cards/business/ordinary';
import { CARDS as chemistryHigher } from '@/components/MarkBank/cards/chemistry/higher';
import { CARDS as chemistryOrdinary } from '@/components/MarkBank/cards/chemistry/ordinary';
import { CARDS as homeEconomicsHigher } from '@/components/MarkBank/cards/home-economics/higher';
import { CARDS as homeEconomicsOrdinary } from '@/components/MarkBank/cards/home-economics/ordinary';
import { CARDS as physicsHigher } from '@/components/MarkBank/cards/physics/higher';
import { CARDS as physicsOrdinary } from '@/components/MarkBank/cards/physics/ordinary';
import { buildQuestionModel } from '@/components/WaysIn/questionModel';
import { waysInSourceFromMarkBank } from '@/components/WaysIn/sources';

const cards = [
  ...agHigher, ...agOrdinary,
  ...biologyHigher, ...biologyOrdinary,
  ...businessHigher, ...businessOrdinary,
  ...chemistryHigher, ...chemistryOrdinary,
  ...homeEconomicsHigher, ...homeEconomicsOrdinary,
  ...physicsHigher, ...physicsOrdinary,
];

const countWords: Record<string, number> = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8,
};

describe('Ways In across the Mark Bank corpus', () => {
  test('preserves every exact question and carries no scheme payload', () => {
    expect(cards.length).toBeGreaterThan(100);
    for (const card of cards) {
      const source = waysInSourceFromMarkBank(card, card.subjectId);
      const model = buildQuestionModel(source);
      expect(model.exactText, card.id).toBe(card.questionText.trim());
      expect(model.expectedPoints, card.id).toBeGreaterThanOrEqual(1);
      expect(model.expectedPoints, card.id).toBeLessThanOrEqual(8);

      const payload = source as unknown as Record<string, unknown>;
      expect(payload, card.id).not.toHaveProperty('rows');
      expect(payload, card.id).not.toHaveProperty('schemeCitation');
      expect(payload, card.id).not.toHaveProperty('tariffModel');
      expect(payload, card.id).not.toHaveProperty('schemeRegion');
      expect(Object.keys(source.answerShape ?? {}), card.id).toEqual(['totalMarks']);
    }
  });

  test('builds a bounded, paper-grounded planning frame for every card', () => {
    for (const card of cards) {
      const source = waysInSourceFromMarkBank(card, card.subjectId);
      const model = buildQuestionModel(source);
      const paperText = [source.stem, source.questionText].filter(Boolean).join('\n');

      expect(model.planPrompts.length, card.id).toBeGreaterThanOrEqual(1);
      expect(model.planPrompts.length, card.id).toBeLessThanOrEqual(8);
      expect(new Set(model.planPrompts.map(item => item.id)).size, card.id).toBe(model.planPrompts.length);
      for (const item of model.planPrompts) {
        expect(item.label.trim().length, card.id).toBeGreaterThan(0);
        expect(item.placeholder.trim().length, card.id).toBeGreaterThan(0);
        if (item.sourceText) expect(paperText, `${card.id}: ${item.sourceText}`).toContain(item.sourceText);
      }
    }
  });

  test('recognises the command in at least nine out of ten real questions', () => {
    const missing = cards.filter(card => {
      const source = waysInSourceFromMarkBank(card, card.subjectId);
      return buildQuestionModel(source).command === null;
    });
    const coverage = (cards.length - missing.length) / cards.length;
    expect(
      coverage,
      missing.slice(0, 30).map(card => `${card.id}: ${card.questionText}`).join('\n'),
    ).toBeGreaterThanOrEqual(0.9);
  });

  test('honours every explicit choice count before counting its labelled options', () => {
    const choicePattern = /\b(?:any\s+)?(one|two|three|four|five|six|seven|eight|[1-8])\s+of\s+(?:the\s+)?(?:following|these)\b/i;
    const choiceCards = cards.flatMap(card => {
      const match = choicePattern.exec(card.questionText);
      return match ? [{ card, token: match[1] }] : [];
    });
    expect(choiceCards.length).toBeGreaterThan(20);
    for (const { card, token } of choiceCards) {
      const model = buildQuestionModel(waysInSourceFromMarkBank(card, card.subjectId));
      const expected = countWords[token.toLowerCase()] ?? Number(token);
      expect(model.planShape, card.id).toMatchObject({
        count: expected,
        basis: 'printed',
        structure: 'choice',
      });
    }
  });

  test('does not promote ordinary wording to instructions in known SEC cards', () => {
    const expectedCommands: Record<string, string[]> = {
      'phys-2021-hl-q11-iii': ['what is'],
      'chem-2022-ol-q3-c': ['state', 'explain'],
      'bus-2024-hl-s1-q7': ['write'],
      'agsci-2022-hl-q4c': ['describe'],
      'agsci-2022-hl-q12aii': ['explain'],
      'agsci-2022-hl-q12aiii': ['outline'],
      'bus-2024-ol-s2-q5bii': ['identify'],
      'he-2021-hl-sb-q4b': ['outline'],
    };

    for (const [cardId, expected] of Object.entries(expectedCommands)) {
      const card = cards.find(candidate => candidate.id === cardId);
      expect(card, cardId).toBeDefined();
      const model = buildQuestionModel(waysInSourceFromMarkBank(card!, card!.subjectId));
      expect(
        model.commands.map(command => command.surface.toLowerCase()),
        cardId,
      ).toEqual(expected);
    }

    const twoBenefitCard = cards.find(card => card.id === 'agsci-2022-hl-q12aiii');
    expect(twoBenefitCard).toBeDefined();
    expect(buildQuestionModel(
      waysInSourceFromMarkBank(twoBenefitCard!, twoBenefitCard!.subjectId),
    ).planShape).toMatchObject({ count: 2, basis: 'printed' });
  });

  test('uses the card instructions, not a contextual stem command, for multi-task plans', () => {
    const expectedLabels: Record<string, string[]> = {
      'agsci-2022-hl-q18ci': ['task 1: identify', 'task 2: state'],
      'agsci-2022-hl-q18cii': ['task 1: identify', 'task 2: state'],
      'agsci-2024-hl-q8c': ['task 1: provide', 'task 2: state'],
      'bio-2021-ol-q3-ab': ['task 1: choose', 'task 2: place'],
    };

    for (const [cardId, expected] of Object.entries(expectedLabels)) {
      const card = cards.find(candidate => candidate.id === cardId);
      expect(card, cardId).toBeDefined();
      const model = buildQuestionModel(waysInSourceFromMarkBank(card!, card!.subjectId));
      expect(model.planPrompts.map(prompt => prompt.label.toLowerCase()), cardId).toEqual(expected);
    }
  });

  test('keeps repeated command words beside their own printed sentence', () => {
    const expectedSources: Record<string, string[]> = {
      'bio-2024-hl-q13-c-v': [
        'Name the simple molecule from which a plant obtains the protons (H+ ions) used to make these compounds.',
        'Name another simple molecule from which plants obtain the carbon (C) used to make these compounds.',
      ],
      'bio-2024-hl-q14-c-iv': [
        'Give one example of a harmful virus.',
        'Give one way in which viruses can be beneficial.',
      ],
      'bio-2023-hl-q15-c-iii-iv-vii': [
        'Describe one effect on the female reproductive system of the low levels of hormones A and B.',
        'Explain why hormone A levels increase after approximately day 5.',
        'Explain why hormone B levels increase in the days after day 14.',
      ],
    };

    for (const [cardId, expected] of Object.entries(expectedSources)) {
      const card = cards.find(candidate => candidate.id === cardId);
      expect(card, cardId).toBeDefined();
      const model = buildQuestionModel(waysInSourceFromMarkBank(card!, card!.subjectId));
      expect(model.planPrompts.map(prompt => prompt.sourceText), cardId).toEqual(expected);
    }
  });

  test('separates compact printed lists without detaching or misplacing their labels', () => {
    const expectedLines: Record<string, string[]> = {
      'bio-2025-hl-q13-c-i-ii': [
        '(i) Briefly describe enzymes under the following headings:',
        '1. Biochemical nature',
        '2. Shape.',
        '(ii) Based on the biochemical nature of enzymes, name the cell component where enzymes are made.',
      ],
      'bio-2025-hl-q14-b-eye': [
        'Describe the role of each of the following in the eye.',
        '1. Cornea',
        '2. Retina',
        '3. Optic nerve',
        '4. Lens',
      ],
      'agsci-2025-ol-q9bi-ii': [
        '(i) State if the input prices have increased or decreased.',
        '(ii) Identify what your answer in part (i) above means for farmers by placing a tick in the correct box:',
        'Costs less to produce / Cost the same to produce / Costs more to produce.',
      ],
      'agsci-2025-ol-q9biii-iv': [
        "(iii) Which agricultural enterprise's output price has increased?",
        '(iv) Identify what your answer in part (iii) above means for farmers by placing a tick in the correct box:',
        'Increased profit / Increased cost.',
      ],
      'bio-2022-hl-q3-bc-fig': [
        '(b) Is the karyotype shown above from a female or a male?',
        '(c) Justify the answer you have given at part (b) above.',
      ],
      'bio-2025-ol-q4-a-fig': [
        '(i) Is this a plant cell or an animal cell?',
        '(ii) Give two reasons for your answer in part (i) above.',
      ],
      'chem-2025-ol-q10-b-i-iii': [
        '(i) Name the three states of matter.',
        '(ii) What is meant by the term ion?',
        '(iii) Classify helium (He) as an atom, a molecule or an ion.',
      ],
      'bio-2025-hl-q16-b-iii-fig': [
        '1. Oxygen and carbon dioxide are two gases that are exchanged between structures A and B.',
        'Match each gas to the letters X and Y, based on their main directions of movement.',
        '2. What term describes the movement of these gases?',
      ],
      'bio-2025-hl-q16-a-i-ii-fig': [
        '(i) Name the structures A, B and C.',
        '(ii) Give one function of structure C.',
      ],
      'bio-2025-ol-q10-b-iii-v-fig': [
        '(iii) Dish C was placed in an anaerobic jar.',
        'What gas does this remove from the air?',
        '(iv) Which factor affecting germination is being investigated in dish B?',
        '(v) There is unlikely to be germination in dishes B and C.',
        'Identify one other dish where germination is unlikely to happen.',
        'Justify your answer.',
      ],
      'chem-2024-hl-q8-b-iii-iv': [
        '(iii) A trace quantity of C4H10 is formed during reaction B.',
        'Explain how the formation of C4H10 is evidence for the mechanism described.',
        '(iv) Apart from the formation of C4H10, state one other piece of evidence for this mechanism.',
      ],
      'chem-2024-ol-q3-b': [
        '(ii) Identify the gas produced.',
        '(iii) Identify compound A.',
        '(iv) Identify compound B.',
        '(v) Identify a reagent which could be used to confirm that compound C contained chloride (Cl–) ions.',
      ],
      'bio-2024-ol-q16-a-ii-iii': [
        '(ii) 1. Give one function of xylem.',
        '2. Give one function of phloem.',
        '(iii) Which of the following terms describes evaporation of water into the airspaces of the leaf?',
      ],
      'bio-2024-ol-q17-c-i-iii': [
        '(i) What is meant by the term vegetative propagation?',
        '(iii) 1. Give one advantage that vegetative propagation has over reproduction by seed.',
        '2. Give one advantage that reproduction by seed has over vegetative propagation.',
      ],
      'bio-2024-ol-q11-a': [
        '(i) What is the primary source of energy for organisms on Earth?',
        '(ii) Define the following terms as used in ecology:',
        '1. Biosphere',
        '2. Niche',
      ],
      'bio-2024-ol-q16-b-ii-iii': [
        '(ii) Explain the following terms:',
        '1. Ingestion',
        '2. Digestion',
        '(iii) Why is digestion is important in the body?',
      ],
    };

    for (const [cardId, expected] of Object.entries(expectedLines)) {
      const card = cards.find(candidate => candidate.id === cardId);
      expect(card, cardId).toBeDefined();
      const model = buildQuestionModel(waysInSourceFromMarkBank(card!, card!.subjectId));
      expect(model.lines, cardId).toEqual(expected);
      expect(model.lines.some(line => /^(?:(?:\([^)]*\)|[a-h][.)])\s*)*\d+[.)]$/i.test(line)), cardId).toBe(false);
    }

    const nestedPlanLabels: Record<string, string[]> = {
      'bio-2024-ol-q16-a-ii-iii': ['Part (ii) 1', 'Part 2', 'Part (iii)'],
      'bio-2024-ol-q17-c-i-iii': ['Part (i)', 'Part (iii) 1', 'Part 2'],
      'bio-2025-hl-q13-c-i-ii': ['Part 1', 'Part 2', 'Part (ii)'],
      'bio-2024-ol-q11-a': ['Part (i)', 'Part 1', 'Part 2'],
      'bio-2024-ol-q16-b-ii-iii': ['Part 1', 'Part 2', 'Part (iii)'],
    };
    for (const [cardId, expected] of Object.entries(nestedPlanLabels)) {
      const card = cards.find(candidate => candidate.id === cardId)!;
      const model = buildQuestionModel(waysInSourceFromMarkBank(card, card.subjectId));
      expect(model.planPrompts.map(prompt => prompt.label), cardId).toEqual(expected);
    }
  });
});
