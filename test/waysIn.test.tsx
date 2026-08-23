/**
 * Ways In — source fidelity, support-path behaviour and answer-leak guards.
 */
import React from 'react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import type { PDFDocumentProxy } from 'pdfjs-dist';

import WaysInWorkspace from '@/components/WaysIn/WaysInWorkspace';
import WaysInHub from '@/components/WaysIn/WaysInHub';
import {
  buildQuestionModel,
  findCommandDemand,
  findCommandDemands,
  findPrintedPlanShape,
  splitQuestionLines,
} from '@/components/WaysIn/questionModel';
import { waysInSourceFromMarkBank } from '@/components/WaysIn/sources';
import { extractQuestionText } from '@/components/PaperTrail/questionText';
import type { WaysInQuestionSource } from '@/components/WaysIn/types';
import type { MarkRow, SecCard } from '@/types/markBank';

const row = (id: string, verbatim: string, marks = 3): MarkRow => ({
  id, kind: 'point', verbatim, marks,
});

const card: SecCard = {
  source: 'sec', kind: 'question',
  id: 'biology-2025-hl-q7-f', subjectId: 'biology', level: 'higher',
  topicId: 'bio-u1', conceptId: 'scientific-theory',
  year: 2025, paperFileid: 'paper', section: 'A', questionRef: '2025 HL Q7(f)',
  stem: 'Answer the following question in relation to the scientific method.',
  questionText: 'Explain what is meant by the term theory. Give two features in your answer.',
  tariffModel: { kind: 'fixed' }, totalMarks: 6,
  rows: [row('r1', 'Supported hypothesis'), row('r2', 'Repeated experimental evidence')],
  schemeCitation: 'SEC Biology 2025', specVersion: 'lc-biology-2025',
  qa: { gates: [], humanReviewedBy: 'reviewer', humanReviewedAt: '2026-08-01' },
};

const source: WaysInQuestionSource = waysInSourceFromMarkBank(card, 'Biology');

beforeEach(() => window.localStorage.clear());

describe('Ways In question model', () => {
  test('keeps the exact question and finds the job, constraints and answer shape', () => {
    const model = buildQuestionModel(source);
    expect(model.exactText).toBe(card.questionText);
    expect(model.command?.surface.toLowerCase()).toBe('explain');
    expect(model.command?.requiredAction).toMatch(/how or why/i);
    expect(model.constraints.join(' ')).toMatch(/two features/i);
    expect(model.expectedPoints).toBe(2);
    expect(model.steps.map(step => step.id)).toEqual(['meet', 'job', 'boundaries', 'shape', 'attempt', 'return']);
  });

  test('interprets the printed stem and question together without changing either', () => {
    const model = buildQuestionModel({
      ...source,
      stem: 'Give the collective name for:',
      questionText: '1. The male reproductive parts of the flower. 2. The female reproductive parts of the flower.',
    });

    expect(model.exactText).toBe('1. The male reproductive parts of the flower. 2. The female reproductive parts of the flower.');
    expect(model.command?.surface.toLowerCase()).toBe('give');
    expect(model.givens).toEqual([]);
    expect(model.planKind).toBe('printed-parts');
    expect(model.planPrompts.map(item => item.sourceText)).toEqual([
      '1. The male reproductive parts of the flower.',
      '2. The female reproductive parts of the flower.',
    ]);
  });

  test('keeps every essential calculation value and builds a numerical working frame', () => {
    const model = buildQuestionModel({
      ...source,
      stem: undefined,
      questionText: 'A ball is kicked with an initial velocity of 20 m s–1 at an angle of 50° to the horizontal. Calculate the horizontal distance it travels in 1.2 seconds.',
    });

    expect(model.givens).toEqual([
      'A ball is kicked with an initial velocity of 20 m s–1 at an angle of 50° to the horizontal.',
      '1.2 seconds',
    ]);
    expect(model.planKind).toBe('calculation');
    expect(model.planPrompts.map(item => item.label)).toEqual([
      'Values supplied',
      'Quantity to find',
      'Relationship',
      'Substitution',
      'Result and unit',
    ]);
  });

  test('does not mistake a decimal measurement for an answer limit or duplicate its task', () => {
    const stem = 'To determine the concentration of hypochlorite ion (ClO–) in a solution of bleach, 25.0 cm3 of the bleach solution were first diluted to exactly 500 cm3.';
    const model = buildQuestionModel({
      ...source,
      stem,
      questionText: 'Describe how the 25.0 cm3 sample of the original bleach solution, provided in a beaker, was diluted to exactly 500 cm3.',
      answerShape: { totalMarks: 9 },
    });

    expect(model.constraints).toEqual(['9 marks are available in total.']);
    expect(model.givens).toEqual([stem]);
    expect(model.planKind).toBe('procedure');
    expect(model.planPrompts.map(item => item.label)).toEqual([
      'Starting action',
      'Next action or actions',
      'Finish or check',
    ]);
  });

  test('breaks a supplied comparison into exact, scannable sentences', () => {
    const model = buildQuestionModel({
      ...source,
      stem: 'The same mass of magnesium ribbon and of granulated zinc was added to the same volume of the same copper(II) sulfate solution. With magnesium the blue colour disappeared completely; with zinc it only faded.',
      questionText: 'Suggest a reason for the different results.',
    });

    expect(model.givens).toEqual([
      'The same mass of magnesium ribbon and of granulated zinc was added to the same volume of the same copper(II) sulfate solution.',
      'With magnesium the blue colour disappeared completely;',
      'with zinc it only faded.',
    ]);
  });

  test('passes only paper-visible metadata into Ways In, never marking-scheme structure or content', () => {
    const serialised = JSON.stringify(source);
    expect(serialised).not.toContain('Supported hypothesis');
    expect(serialised).not.toContain('Repeated experimental evidence');
    expect(source.answerShape).toEqual({ totalMarks: 6 });
    expect(serialised).not.toContain('alternativeRoutes');
    expect(serialised).not.toContain('choice');
  });

  test('uses the first printed command when a question contains more than one verb', () => {
    expect(findCommandDemand('State one feature. Then explain why it matters.')?.surface.toLowerCase()).toBe('state');
  });

  test('ignores command-like words in the scenario and keeps the paper instruction', () => {
    expect(findCommandDemands(
      'When bulls arrive, they enter an area where they are clipped. Suggest one reason for any three treatments.',
    ).map(command => command.surface.toLowerCase())).toEqual(['suggest']);
    expect(findCommandDemands(
      'He carried out a trial to distinguish between two batches. Describe how he would carry out this trial.',
    ).map(command => command.surface.toLowerCase())).toEqual(['describe']);
    expect(findCommandDemands(
      'Using the list provided, state which item is correct.',
    ).map(command => command.surface.toLowerCase())).toEqual(['state']);
    expect(findCommandDemands(
      'Some buses run on hydrogen gas which could reduce emissions. Write the balanced equation.',
    ).map(command => command.surface.toLowerCase())).toEqual(['Write'.toLowerCase()]);
  });

  test('keeps explicitly joined and separately printed instructions', () => {
    expect(findCommandDemands('State and explain one effect.').map(command => command.surface.toLowerCase()))
      .toEqual(['state', 'explain']);
    expect(findCommandDemands('Identify X. Explain Y.').map(command => command.surface.toLowerCase()))
      .toEqual(['identify', 'explain']);
  });

  test('recognises common interrogative and practical paper instructions conservatively', () => {
    expect(findCommandDemands('How many amino acids are found in proteins?')[0]?.surface.toLowerCase()).toBe('how');
    expect(findCommandDemands('Why was it important to keep the temperature constant?')[0]?.surface.toLowerCase()).toBe('why');
    expect(findCommandDemands('Illustrate, using an example, the role of an interest group.')[0]?.surface.toLowerCase()).toBe('illustrate');
    expect(findCommandDemands('Use the data above to calculate the result.').map(command => command.surface.toLowerCase()))
      .toEqual(['use']);
  });

  test('does not treat option text or label-value fields as extra instructions', () => {
    expect(findCommandDemands(
      'Place these steps in the correct order. A: Produce seed. B: Test the plants. C: Identify the desired gene. D: Remove it. E: Insert it into the plant.',
    ).map(command => command.surface.toLowerCase())).toEqual(['place']);
    expect(findCommandDemands(
      'Name: Asthma. 1. Give a symptom. 2. Describe a cause. 3. Suggest a possible treatment.',
    ).map(command => command.surface.toLowerCase())).toEqual(['give', 'describe', 'suggest']);
    expect(findCommandDemands(
      'Identify the region in the kidney, by name or label, where filtration occurs. Explain why pressure matters.',
    ).map(command => command.surface.toLowerCase())).toEqual(['identify', 'explain']);
    expect(findCommandDemands(
      'Give any one application (or use) of DNA profiling.',
    ).map(command => command.surface.toLowerCase())).toEqual(['give']);
    expect(findCommandDemands(
      'Using the price figures set out above, calculate the total.',
    ).map(command => command.surface.toLowerCase())).toEqual(['calculate']);
    expect(findCommandDemands(
      'A G-M tube and a solid-state detector have the same function. What is this function?',
    ).map(command => command.surface.toLowerCase())).toEqual(['what is']);
    expect(findCommandDemands(
      'According to the label, oxygen is released on complete decomposition. State and explain whether it fully decomposed.',
    ).map(command => command.surface.toLowerCase())).toEqual(['state', 'explain']);
    expect(findCommandDemands(
      'Write True or False. 3. State broadcaster RTE announced a target.',
    ).map(command => command.surface.toLowerCase())).toEqual(['write']);
    expect(findCommandDemands(
      'Using the data in the table below briefly explain the effect of harvest date.',
    ).map(command => command.surface.toLowerCase())).toEqual(['explain']);
    expect(findCommandDemands(
      'Referring to the data in the table below outline two benefits.',
    ).map(command => command.surface.toLowerCase())).toEqual(['outline']);
  });

  test('takes planning counts from printed wording, never any-N groups or hidden routes', () => {
    const anyN: SecCard = {
      ...card,
      rows: [{
        id: 'group', kind: 'anyN', verbatim: 'Any four', marks: null,
        group: { claimMax: 4, perOption: 3, options: ['a', 'b', 'c', 'd', 'e'] },
      }],
    };
    // The card still prints “two features”, so the four scheme options cannot
    // silently change the pre-reveal planning frame.
    expect(buildQuestionModel(waysInSourceFromMarkBank(anyN, 'Biology')).planShape).toMatchObject({
      count: 2,
      basis: 'printed',
    });

    const routed = {
      ...card,
      questionText: 'Explain the result shown in the graph.',
      rows: [
        row('common', 'Common'),
        { ...row('a1', 'Route A 1'), route: 'a' },
        { ...row('a2', 'Route A 2'), route: 'a' },
        { ...row('b1', 'Route B'), route: 'b' },
      ],
    } satisfies SecCard;
    expect(buildQuestionModel(waysInSourceFromMarkBank(routed, 'Biology')).planShape).toEqual({
      count: 1,
      basis: 'flexible',
    });
  });

  test('can count figure labels when that count is printed in the question', () => {
    expect(findPrintedPlanShape('Name the parts labelled A and B.')).toEqual({
      count: 2,
      basis: 'printed',
      evidence: 'labelled A and B',
      structure: 'labels',
    });
    expect(findPrintedPlanShape('Name the parts labelled A, B, and C.')).toEqual({
      count: 3,
      basis: 'printed',
      evidence: 'labelled A, B, and C',
      structure: 'labels',
    });
    expect(findPrintedPlanShape('Match the parts marked D, E, and F.')).toEqual({
      count: 3,
      basis: 'printed',
      evidence: 'marked D, E, and F',
      structure: 'labels',
    });
  });

  test('does not turn contextual quantities into required answer counts', () => {
    expect(findPrintedPlanShape(
      'Choose the appropriate terms. (One term does not apply.)',
    )).toEqual({ count: 1, basis: 'flexible' });
    expect(findPrintedPlanShape(
      'Which one of these three observations was the most unexpected?',
    )).toEqual({
      count: 1,
      basis: 'printed',
      evidence: 'one of these',
      structure: 'choice',
    });
  });

  test('uses only unambiguous visible structures to seed the plan', () => {
    expect(findPrintedPlanShape(
      'Suggest one reason for any three treatments listed below.',
    )).toEqual({
      count: 3,
      basis: 'printed',
      evidence: 'any three treatments',
      structure: 'count-phrase',
    });
    expect(findPrintedPlanShape(
      'Choose the correct terms: The European __________ is elected. The __________ checks the budget.',
    )).toMatchObject({ count: 2, basis: 'printed', structure: 'blanks' });
    expect(findPrintedPlanShape(
      '(i) Which observation was unexpected? (ii) What conclusion was reached?',
    )).toEqual({
      count: 2,
      basis: 'printed',
      evidence: '(i), (ii)',
      structure: 'parts',
    });
    expect(findPrintedPlanShape(
      'Explain what the term means. Give two features in your answer.',
    )).toEqual({
      count: 2,
      basis: 'printed',
      evidence: 'Explain, Give',
      structure: 'instructions',
    });
    expect(findPrintedPlanShape(
      'Explain three of the following elements: (i) Offer (ii) Capacity (iii) Consideration (iv) Consent.',
    )).toEqual({
      count: 3,
      basis: 'printed',
      evidence: 'three of the following',
      structure: 'choice',
    });
    expect(findPrintedPlanShape(
      'Name: Asthma. 1. Give a symptom. 2. Describe a cause. 3. Suggest a treatment.',
    )).toEqual({
      count: 3,
      basis: 'printed',
      evidence: '1., 2., 3.',
      structure: 'parts',
    });
  });

  test('keeps supplied numerical data complete and excludes task numbering', () => {
    const dataModel = buildQuestionModel({
      ...source,
      questionText: 'The student collected these data — Trial 1: 62, Trial 2: 59, Trial 3: 61, Trial 4: 58. Calculate the mean at 20 °C.',
      stem: undefined,
    });
    expect(dataModel.givens).toHaveLength(2);
    expect(dataModel.givens[0]).toContain('Trial 1: 62');
    expect(dataModel.givens[0]).toContain('Trial 4: 58');
    expect(dataModel.givens[1]).toBe('20 °C');

    const numberedModel = buildQuestionModel({
      ...source,
      questionText: '1. What is geotropism? 2. Give one benefit.',
      stem: undefined,
    });
    expect(numberedModel.givens).toEqual([]);
  });

  test('keeps every exact question line instead of silently truncating long questions', () => {
    const text = Array.from({ length: 15 }, (_, index) => `Part ${index + 1} asks a question.`).join(' ');
    const lines = splitQuestionLines(text);
    expect(lines).toHaveLength(15);
    expect(lines.at(-1)).toBe('Part 15 asks a question.');
  });

  test('keeps printed part numbers attached to the wording they identify', () => {
    expect(splitQuestionLines(
      '1. The male reproductive parts of the flower. 2. The female reproductive parts of the flower.',
    )).toEqual([
      '1. The male reproductive parts of the flower.',
      '2. The female reproductive parts of the flower.',
    ]);
    expect(splitQuestionLines('a. First statement. b. Second statement.')).toEqual([
      'a. First statement.',
      'b. Second statement.',
    ]);
    expect(splitQuestionLines(
      '(i) Briefly describe enzymes under the following headings: 1. Biochemical nature 2. Shape. (ii) Name where enzymes are made.',
    )).toEqual([
      '(i) Briefly describe enzymes under the following headings:',
      '1. Biochemical nature',
      '2. Shape.',
      '(ii) Name where enzymes are made.',
    ]);
    expect(splitQuestionLines(
      'Describe the role of each structure. 1. Cornea 2. Retina 3. Optic nerve 4. Lens',
    )).toEqual([
      'Describe the role of each structure.',
      '1. Cornea',
      '2. Retina',
      '3. Optic nerve',
      '4. Lens',
    ]);
    expect(splitQuestionLines('Suggest an effect of: 1. a disease; 2. cutting vegetation.')).toEqual([
      'Suggest an effect of:',
      '1. a disease;',
      '2. cutting vegetation.',
    ]);
    expect(splitQuestionLines('Use your answer at part 1. above.')).toEqual([
      'Use your answer at part 1. above.',
    ]);
    expect(splitQuestionLines(
      '(i) State whether it increased. (ii) Explain what your answer in part (i) above means.',
    )).toEqual([
      '(i) State whether it increased.',
      '(ii) Explain what your answer in part (i) above means.',
    ]);
    expect(splitQuestionLines(
      '1. Oxygen is exchanged between structures A and B. Match each gas. 2. Name the process.',
    )).toEqual([
      '1. Oxygen is exchanged between structures A and B.',
      'Match each gas.',
      '2. Name the process.',
    ]);
    expect(splitQuestionLines(
      'A. Requires oxygen. B. Does not require oxygen. C. Produces less energy.',
    )).toEqual([
      'A. Requires oxygen.',
      'B. Does not require oxygen.',
      'C. Produces less energy.',
    ]);
  });

  test('admits when image-only Paper Trail text cannot be parsed', () => {
    const imageOnly = buildQuestionModel({
      ...source,
      id: 'paper-trail:image-only',
      origin: 'paper-trail',
      questionText: '',
      textConfidence: 'image-only',
    });
    expect(imageOnly.command).toBeNull();
    expect(imageOnly.lines).toEqual([]);
  });
});

describe('Paper Trail source handoff', () => {
  test('extracts only searchable text inside the verified crop', async () => {
    const cleanup = vi.fn();
    const pdf = {
      getPage: vi.fn().mockResolvedValue({
        getViewport: () => ({ width: 1000, height: 1000, transform: [1, 0, 0, -1, 0, 1000] }),
        getTextContent: vi.fn().mockResolvedValue({ items: [
          { str: 'Explain', width: 45, height: 10, transform: [10, 0, 0, 10, 100, 800] },
          { str: 'photosynthesis.', width: 92, height: 10, transform: [10, 0, 0, 10, 150, 800] },
          { str: 'Text outside this question crop', width: 180, height: 10, transform: [10, 0, 0, 10, 100, 300] },
        ] }),
        cleanup,
      }),
    } as unknown as PDFDocumentProxy;

    const extracted = await extractQuestionText(pdf, [{ p: 1, r: [0, 0.1, 1, 0.4] }]);
    expect(extracted).toEqual({
      text: 'Explain photosynthesis.',
      lines: ['Explain photosynthesis.'],
      confidence: 'pdf-text',
    });
    expect(cleanup).toHaveBeenCalledTimes(1);
  });
});

describe('Ways In workspace', () => {
  test('runs the six-stage path and preserves an unfinished draft on-device', () => {
    const onClose = vi.fn();
    render(<WaysInWorkspace source={source} onClose={onClose} />);

    expect(screen.getByText('Find a way into this question.')).toBeInTheDocument();
    expect(screen.getByText(card.questionText)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /One step at a time/i }));
    expect(screen.getByRole('heading', { name: 'Meet the exact question' })).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /go to step 5/i }));
    const draft = screen.getByLabelText('Your attempt');
    fireEvent.change(draft, { target: { value: 'A theory is supported by evidence.' } });
    expect(window.localStorage.getItem(`nextstepuni:ways-in:${source.id}`)).toContain('supported by evidence');
    expect(onClose).not.toHaveBeenCalled();
  });

  test('shows a task map, editable empty answer shape and colour key without scheme answers', () => {
    render(<WaysInWorkspace source={source} initialMode="show-me" onClose={vi.fn()} />);
    expect(screen.getByRole('heading', { name: 'See the shape before you answer.' })).toBeInTheDocument();
    expect(screen.getByRole('list', { name: 'Question task map' })).toBeInTheDocument();
    expect(screen.queryByText('Supported hypothesis')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: /Answer shape/i }));
    expect(screen.getAllByPlaceholderText('Your idea—not the scheme')).toHaveLength(2);
    fireEvent.change(screen.getByLabelText('Plan answer idea 1'), { target: { value: 'First idea' } });
    expect(window.localStorage.getItem(`nextstepuni:ways-in:${source.id}`)).toContain('First idea');

    fireEvent.click(screen.getByRole('tab', { name: /Question colours/i }));
    const actionMark = document.querySelector('.wi-colour-question .wi-mark--action');
    expect(actionMark).toHaveTextContent('Explain');
  });

  test('can return to the source without grading the question', () => {
    const onClose = vi.fn();
    render(<WaysInWorkspace source={source} initialMode="one-step" onClose={onClose} />);
    fireEvent.click(screen.getByRole('button', { name: /go to step 6/i }));
    screen.getAllByRole('button', { name: /My answer|I respected|I can see/i }).forEach(button => fireEvent.click(button));
    fireEvent.click(screen.getByRole('button', { name: /Return to the original question/i }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});

describe('Ways In Launchpad hub', () => {
  test('routes students to the two trusted question sources', () => {
    const onOpenTool = vi.fn();
    render(<WaysInHub onOpenTool={onOpenTool} />);
    fireEvent.click(screen.getByRole('button', { name: /Choose from Mark Bank/i }));
    expect(onOpenTool).toHaveBeenCalledWith('mark-bank');
    fireEvent.click(screen.getByRole('button', { name: /Choose from Paper Trail/i }));
    expect(onOpenTool).toHaveBeenCalledWith('paper-trail');
  });
});
