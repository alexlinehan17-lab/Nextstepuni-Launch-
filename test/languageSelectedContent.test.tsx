import React, { useState } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { languageMarks, languagePointsAllocation, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, type LanguagePointsRubric, type LanguageWritingCriterion, type SecRubricCard } from '../types/markBank';

const steps = (max: number) => Array.from({ length: max + 1 }, (_, mark) => mark);
const manual = (id: string, label: string, maxMarks: number): LanguageWritingCriterion => ({
  id, label, maxMarks, permittedMarks: steps(maxMarks), guidance: [],
});
const expression = (question: 5 | 6): LanguageWritingCriterion => ({
  ...manual('expression', 'Expression', question === 5 ? 20 : 30),
  limits: [{ id: 'lower-e', scaleLabel: 'Lower E', maxMarks: question === 5 ? 15 : 20,
    when: { any: [
      { criterionIds: question === 5 ? ['discretion'] : [], atMost: question === 5 ? 10 : 15, includeSelectedGroupMarks: true },
      { length: 'characters', below: question === 5 ? 150 : 200 },
    ] }, guidance: ['Use the published lower expression scale when either condition applies.'] }],
});

// Independent root review of Japanese2010HL original scheme, physical pp11–14,
// SHA256 7a71fa81c9f4dcdf00223ec1774c8e8c1fe86ce8ddffa61c04cb207c896d6628.
// These are scorer fixtures for its printed allocations, not published cards.
const q5: LanguagePointsRubric = {
  system: 'language-points', count: 4, taskRequirements: [], markingGuideNote: '',
  alternativeSets: [{ id: 'first', label: 'First selected response', sourceText: 'School location 2 marks; nearby places 2 marks.', schemePages: [11] }],
  groups: [
    { id: 'first', label: 'First complete response', alternativeSet: 'first', rows: [{ id: 'answer', text: 'Complete selected response', marks: 4 }] },
    { id: 'school', label: 'School response in first slot', alternativeSet: 'first', rows: [
      { id: 'location', text: 'School location', marks: 2 }, { id: 'nearby', text: 'Nearby places', marks: 2 },
    ] },
    ...[2, 3, 4].map(n => ({ id: `slot${n}`, label: `Selected response ${n}`, rows: [{ id: 'answer', text: `Complete response ${n}`, marks: 4 }] })),
  ],
  allocationCap: { maxMarks: 16, sourceText: 'Any four points, 4 marks each.', schemePages: [11] },
  criteria: [manual('discretion', 'Discretionary marks', 4), expression(5)],
};
const q6: LanguagePointsRubric = {
  system: 'language-points', count: 1, taskRequirements: [], markingGuideNote: '',
  groups: [
    { id: 'birthday', label: 'Birthday option', rows: [
      { id: 'required', text: 'Birthday', marks: 3 },
      { id: 'points', text: 'Any four additional points', marks: 20, steps: [0, 5, 10, 15, 20] },
    ], criteria: [manual('birthday-discretion', 'Birthday discretionary marks', 7)] },
    { id: 'country', label: 'Country option', rows: [
      { id: 'required', text: 'Country', marks: 5 },
      { id: 'points', text: 'Any four additional points', marks: 20, steps: [0, 5, 10, 15, 20] },
    ], criteria: [manual('country-discretion', 'Country discretionary marks', 5)] },
  ], criteria: [expression(6)],
};
const card = (rubric: LanguagePointsRubric, totalMarks: number) => ({ kind: 'rubric', rubric, totalMarks }) as SecRubricCard & { rubric: LanguagePointsRubric };
const q5Card = card(q5, 40);
const q6Card = card(q6, 60);
const initial: LanguageScores = {
  'language:group:school': 1, 'language:row:school:location': 1, 'language:row:school:nearby': 1,
  'language:group:slot2': 1, 'language:row:slot2:answer': 1,
  'language:discretion': 2, 'language:expression': 20, 'language:length:characters': 150,
};

afterEach(cleanup);

describe('expression thresholds from selected content', () => {
  it('adds selected Q5 components and discretionary marks exactly once at the source boundary', () => {
    expect(tariffReconciles(q5Card)).toBe(true);
    expect(languagePointsAllocation(q5, initial)).toBe(8);
    expect(languageMarks(q5Card, initial)).toBe(25); // C10 + lowerE15
    expect(languageMarks(q5Card, { ...initial, 'language:discretion': 3 })).toBe(31); // C11 + E20
    const full = { ...initial, 'language:discretion': 4, 'language:group:slot3': 1, 'language:row:slot3:answer': 1,
      'language:group:slot4': 1, 'language:row:slot4:answer': 1 };
    expect(languageMarks(q5Card, full)).toBe(40);
  });

  it('keeps short and missing length independent and restores the saved expression placement', () => {
    const scores: LanguageScores = { ...initial, 'language:discretion': 3 };
    const before = structuredClone(scores);
    expect(languageMarks(q5Card, { ...scores, 'language:length:characters': 149 })).toBe(26);
    const missing = { ...scores }; delete missing['language:length:characters'];
    expect(languageMarks(q5Card, missing)).toBe(26);
    expect(languageMarks(q5Card, scores)).toBe(31);
    expect(scores).toEqual(before);
  });

  it('ignores deselected, conflicting and invalid restored components when choosing the expression scale', () => {
    const stored = { ...initial, 'language:discretion': 3 };
    expect(languageMarks(q5Card, { ...stored, 'language:group:school': 0 })).toBe(22); // C7 + lowerE15
    expect(languageMarks(q5Card, { ...stored, 'language:row:school:location': 9 })).toBe(24); // C9
    expect(languageMarks(q5Card, { ...stored, 'language:group:first': 1, 'language:row:first:answer': 1 })).toBe(22);
  });

  it('uses the allocation cap, including an explicit source flag, before testing content', () => {
    const limited = structuredClone(q5Card);
    limited.rubric.allocationCap!.limits = [{ id: 'source-limit', maxMarks: 4,
      when: { flag: 'source-limit', prompt: 'Published allocation condition applies' },
      sourceText: 'Allocation capped at 4 under this condition.', schemePages: [1] }];
    expect(languageMarks(limited, { ...initial, 'language:discretion': 3 })).toBe(31);
    expect(languageMarks(limited, { ...initial, 'language:discretion': 3, 'language:flag:source-limit': 1 })).toBe(22);
  });

  it.each(['birthday', 'country'] as const)('uses only the selected Q6 %s option, including its own discretionary marks', option => {
    expect(tariffReconciles(q6Card)).toBe(true);
    const scores: LanguageScores = {
      [`language:group:${option}`]: 1, [`language:row:${option}:required`]: 1,
      [`language:row:${option}:points`]: 10,
      'language:birthday-discretion': option === 'birthday' ? 2 : 7,
      'language:country-discretion': option === 'country' ? 0 : 5,
      'language:expression': 30, 'language:length:characters': 200,
    };
    expect(languageMarks(q6Card, scores)).toBe(35); // C15 + lowerE20; unselected saved marks ignored
    const higher = { ...scores, [`language:${option}-discretion`]: option === 'birthday' ? 3 : 1 };
    expect(languageMarks(q6Card, higher)).toBe(46);
    expect(languageMarks(q6Card, { ...higher, 'language:length:characters': 199 })).toBe(36);
  });

  it('rejects the condition outside a whole-task points context or with unsupported language adjustments', () => {
    const writing = { ...q5Card, totalMarks: 24, rubric: { system: 'language-writing' as const,
      criteria: q5.criteria!, taskRequirements: [], markingGuideNote: '' } };
    expect(tariffReconciles(writing)).toBe(false);
    const nested = structuredClone(q6Card);
    nested.rubric.groups[0].criteria![0].limits = [{ id: 'recursive', maxMarks: 5,
      when: { any: [{ criterionIds: [], atMost: 10, includeSelectedGroupMarks: true }] }, guidance: [] }];
    expect(tariffReconciles(nested)).toBe(false);
    expect(tariffReconciles({ ...q5Card, answerLanguageRule: {
      otherLanguageMultiplier: 0.5, sourceText: 'Half marks.', schemePages: [1],
    } })).toBe(false);
    const empty = structuredClone(q6Card);
    const condition = empty.rubric.criteria![0].limits![0].when.any[0];
    if ('criterionIds' in condition) delete condition.includeSelectedGroupMarks;
    expect(tariffReconciles(empty)).toBe(false);
  });

  it('shows the same active scale as the scorer and restores the saved choice after reselection', () => {
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>(initial);
      return <LanguageRubricPanel card={q5Card} scores={scores} onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    expect(screen.getByText('25 / 40')).toBeVisible();
    expect(screen.queryByRole('button', { name: 'Set Expression to 20 marks' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Set Discretionary marks to 3 marks' }));
    expect(screen.getByText('31 / 40')).toBeVisible();
    expect(screen.getByRole('button', { name: 'Set Expression to 20 marks' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'School response in first slot' }));
    expect(screen.getByText('22 / 40')).toBeVisible();
    expect(screen.queryByRole('button', { name: 'Set Expression to 20 marks' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'School response in first slot' }));
    expect(screen.getByText('31 / 40')).toBeVisible();
    expect(screen.getByRole('button', { name: 'Set Expression to 20 marks' })).toHaveAttribute('aria-pressed', 'true');
  });
});
