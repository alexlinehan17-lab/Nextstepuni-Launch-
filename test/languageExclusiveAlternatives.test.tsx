import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';
import { languageAlternativeConflicts, languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

// A focused subset of Russian 2017 Higher comprehension 2 section 4:
// physical scheme p7 makes the general answer an alternative to at most two
// specific actions. Physical p6 awards 2 marks per relevant detail, plus
// separately assessed discretion. This fixture is not a complete source card.
const sourceText = 'everyone was joining in / [up to a maximum of 2 of the following: dancing + shouting + singing along + raising their arms up towards the stage]';
const rubric: LanguagePointsRubric = {
  system: 'language-points', count: 4, taskRequirements: ['Give four details.'], markingGuideNote: '',
  alternativeSets: [{ id: 'participation', label: 'Crowd participation', sourceText, schemePages: [7] }],
  allocationCap: { maxMarks: 8, answerCount: 4, sourceText: '2 marks for each relevant detail', schemePages: [6] },
  groups: [
    { id: 'general', label: 'General participation', alternativeSet: 'participation',
      rows: [{ id: 'answer', text: 'everyone was joining in', marks: 2 }] },
    { id: 'actions', label: 'Specific actions', alternativeSet: 'participation', answerCount: 2,
      rows: ['dancing', 'shouting', 'singing along', 'raising their arms up towards the stage']
        .map((text, i) => ({ id: `action${i}`, text, marks: 2 })) },
    ...['looked back from 2nd floor of complex', 'the musicians were fantastic', 'hope this will not be last concert']
      .map((text, i) => ({ id: `other${i}`, label: `Other detail ${i + 1}`, rows: [{ id: 'answer', text, marks: 2 }] })),
  ],
  criteria: [{ id: 'discretion', label: 'Discretion', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [] }],
};
const card = { kind: 'rubric', totalMarks: 10, rubric } as SecRubricCard & { rubric: LanguagePointsRubric };
const general: LanguageScores = { 'language:group:general': 1, 'language:row:general:answer': 1 };
const actions: LanguageScores = { 'language:group:actions': 1, 'language:row:actions:action0': 1, 'language:row:actions:action1': 1 };
const other: LanguageScores = { 'language:group:other0': 1, 'language:row:other0:answer': 1 };

function Harness({ initial = {} }: { initial?: LanguageScores }) {
  const [scores, setScores] = useState<LanguageScores>(initial);
  return <LanguageRubricPanel card={card} scores={scores} onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
}

describe('source-defined exclusive language alternatives', () => {
  it('credits either the general answer or up to two specific details', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(languagePointsMarks(rubric, general)).toBe(2);
    expect(languagePointsMarks(rubric, actions)).toBe(4);
    expect(languagePointsMarks(rubric, { ...actions, 'language:row:actions:action2': 1, 'language:row:actions:action3': 1 })).toBe(4);
    expect(languagePointsMarks(rubric, { ...general, ...actions })).toBe(0);
  });

  it('withholds conflicting alternatives until the student resolves them, preserving stored marks', () => {
    const scores = { ...general, ...actions, ...other };
    const original = { ...scores };
    expect([...languageAlternativeConflicts(rubric, scores)]).toEqual(['participation']);
    expect(languagePointsMarks(rubric, scores)).toBe(2);
    expect(languagePointsMarks(rubric, { ...scores, 'language:group:general': 0 })).toBe(6);
    expect(languagePointsMarks(rubric, { ...scores, 'language:group:actions': 0 })).toBe(4);
    expect(scores).toEqual(original);
  });

  it('enforces the four-detail quota before discretion and a whole-response language penalty', () => {
    const scores: LanguageScores = { ...actions, ...other, 'language:group:other1': 1, 'language:row:other1:answer': 1,
      'language:group:other2': 1, 'language:row:other2:answer': 1, 'language:discretion': 2 };
    expect(languagePointsMarks(rubric, scores)).toBe(10);
    // Synthetic rule checks composition; it is not attributed to this paper.
    const rule = { otherLanguageMultiplier: 0.5 as const, sourceText: 'Synthetic half-credit rule', schemePages: [1] };
    expect(languagePointsMarks(rubric, { ...scores, 'language:other-language:response': 1 }, rule)).toBe(5);
  });

  it('reconciles the maximum without combining variants from the same alternative', () => {
    const onlyAlternatives = { ...rubric, count: 1, groups: rubric.groups.slice(0, 2), criteria: undefined,
      allocationCap: { ...rubric.allocationCap!, answerCount: 2, maxMarks: 4 } };
    expect(tariffReconciles({ ...card, totalMarks: 4, rubric: onlyAlternatives })).toBe(true);
    expect(tariffReconciles({ ...card, totalMarks: 6, rubric: { ...onlyAlternatives,
      allocationCap: { ...onlyAlternatives.allocationCap, maxMarks: 6, answerCount: 3 } } })).toBe(false);
    expect(tariffReconciles({ ...card, totalMarks: 4, rubric: { ...onlyAlternatives, count: 2 } })).toBe(false);
    expect(tariffReconciles({ ...card, totalMarks: 4, rubric: { ...onlyAlternatives, allocationCap: undefined } })).toBe(true);
    expect(tariffReconciles({ ...card, totalMarks: 6, rubric: { ...onlyAlternatives, allocationCap: undefined } })).toBe(false);
  });

  it('chooses feasible alternative variants under unequal tariffs and a global row quota', () => {
    const varied: LanguagePointsRubric = { ...rubric, count: 2, criteria: undefined,
      allocationCap: { ...rubric.allocationCap!, maxMarks: 12, answerCount: 2 },
      groups: [
        { id: 'one', label: 'One detail', alternativeSet: 'participation', rows: [{ id: 'a', text: 'Synthetic single detail', marks: 8 }] },
        { id: 'two', label: 'Two details', alternativeSet: 'participation', rows: [
          { id: 'b', text: 'Synthetic first detail', marks: 5 }, { id: 'c', text: 'Synthetic second detail', marks: 5 }] },
        { id: 'independent', label: 'Independent', rows: [{ id: 'd', text: 'Synthetic independent detail', marks: 4 }] },
      ] };
    // Best feasible result is 8 + 4, not 8 + 5 from competing alternatives.
    expect(tariffReconciles({ ...card, totalMarks: 12, rubric: varied })).toBe(true);
    expect(tariffReconciles({ ...card, totalMarks: 13, rubric: { ...varied, allocationCap: { ...varied.allocationCap!, maxMarks: 13 } } })).toBe(false);
  });

  it('supports alternative writing criteria without a global row quota', () => {
    const writing: LanguagePointsRubric = { ...rubric, count: 1, criteria: undefined, allocationCap: undefined,
      groups: ['first', 'second'].map((id, i) => ({ id, label: id, alternativeSet: 'participation', rows: [],
        criteria: [{ id, label: id, maxMarks: i + 2, permittedMarks: Array.from({ length: i + 3 }, (_, n) => n), guidance: [] }] })) };
    expect(tariffReconciles({ ...card, totalMarks: 3, rubric: writing })).toBe(true);
    expect(languagePointsMarks(writing, { 'language:group:first': 1, 'language:first': 2 })).toBe(2);
    expect(languagePointsMarks(writing, { 'language:group:first': 1, 'language:first': 2, 'language:group:second': 1, 'language:second': 3 })).toBe(0);
  });

  it.each([{ id: '' }, { label: '' }, { sourceText: '' }, { schemePages: [] }, { schemePages: [0] }, { schemePages: [1.5] }])('rejects an unbound alternative %j', change => {
    expect(tariffReconciles({ ...card, rubric: { ...rubric, alternativeSets: [{ ...rubric.alternativeSets![0], ...change }] } })).toBe(false);
  });

  it('rejects unknown, duplicate and single-member alternative sets', () => {
    expect(tariffReconciles({ ...card, rubric: { ...rubric, alternativeSets: undefined } })).toBe(false);
    expect(tariffReconciles({ ...card, rubric: { ...rubric, alternativeSets: [...rubric.alternativeSets!, ...rubric.alternativeSets!] } })).toBe(false);
    expect(tariffReconciles({ ...card, rubric: { ...rubric, groups: rubric.groups.map(group => group.id === 'general' ? { ...group, alternativeSet: undefined } : group) } })).toBe(false);
  });

  it('requires clearing the selected route before choosing another and never invents credit', () => {
    render(<Harness />);
    expect(screen.getByText(sourceText)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'General participation' }));
    expect(screen.getByRole('button', { name: 'Specific actions' })).toBeDisabled();
    expect(screen.getByText('0 / 10')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'everyone was joining in · 2m' }));
    expect(screen.getByText('2 / 10')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'General participation' }));
    expect(screen.getByRole('button', { name: 'Specific actions' })).toBeEnabled();
    fireEvent.click(screen.getByRole('button', { name: 'Specific actions' }));
    expect(screen.getByText('0 / 10')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'dancing · 2m' }));
    fireEvent.click(screen.getByRole('button', { name: 'shouting · 2m' }));
    expect(screen.getByRole('button', { name: 'singing along · 2m' })).toBeDisabled();
    expect(screen.getByText('4 / 10')).toBeInTheDocument();
  });

  it('visibly resolves restored conflicts without erasing the remaining route', () => {
    render(<Harness initial={{ ...general, ...actions, ...other }} />);
    expect(screen.getByRole('status')).toHaveTextContent('conflicting alternatives are currently unassessed');
    expect(screen.getByText('2 / 10')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'General participation' }));
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
    expect(screen.getByText('6 / 10')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'dancing · 2m' })).toHaveAttribute('aria-pressed', 'true');
  });
});
