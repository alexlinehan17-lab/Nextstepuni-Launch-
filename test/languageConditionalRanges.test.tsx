import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { tariffReconciles, type LanguageWritingRubric, type SecRubricCard } from '../types/markBank';
import { languageCriterionValue, languageMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

const steps = (min: number, max: number) => Array.from({ length: max - min + 1 }, (_, i) => min + i);
// Russian2017Higher scheme pp10–11 gives Lower A9–14 for the short essay;
// pp12–13 gives7–12 for guided writing. Zero is unassessed, not an invented
// positive source band below those published ranges.
function source(min = 9, max = 14, normal = 20) {
  const rubric: LanguageWritingRubric = { system: 'language-writing', taskRequirements: [], markingGuideNote: '', criteria: [
    { id: 'content', label: 'Content', maxMarks: 10, permittedMarks: steps(0, 10), guidance: [] },
    { id: 'expression', label: 'Expression', maxMarks: normal, permittedMarks: steps(0, normal), guidance: [],
      limits: [
        { id: 'lower-a', minMarks: min, maxMarks: max, scaleLabel: 'Lower A',
          when: { any: [{ flag: 'accuracy', prompt: 'Source Lower A accuracy condition applies' }] },
          bands: [
            { label: 'Lower A first band', marks: steps(min, min + 1), guidance: ['Published first descriptor.'] },
            { label: 'Lower A second band', marks: steps(min + 2, min + 3), guidance: ['Published second descriptor.'] },
            { label: 'Lower A third band', marks: steps(min + 4, max), guidance: ['Published third descriptor.'] },
          ], guidance: ['Use the published Lower A range.'] },
        { id: 'zero-content', maxMarks: 0,
          when: { any: [{ criterionIds: ['content'], atMost: 0 }] }, guidance: ['No expression marks without content.'] },
      ] },
  ] };
  return { kind: 'rubric', totalMarks: 10 + normal, rubric } as SecRubricCard & { rubric: LanguageWritingRubric };
}

describe('conditional source ranges for language writing', () => {
  it.each([[9, 14, 20], [7, 12, 15]])('allows the printed %s–%s range without inventing lower positive bands', (min, max, normal) => {
    const card = source(min, max, normal);
    expect(tariffReconciles(card)).toBe(true);
    const scores: LanguageScores = { 'language:content': 10, 'language:flag:accuracy': 1 };
    expect(languageCriterionValue(card.rubric, 'expression', scores)).toBe(0);
    expect(languageCriterionValue(card.rubric, 'expression', { ...scores, 'language:expression': min - 1 })).toBe(0);
    expect(languageCriterionValue(card.rubric, 'expression', { ...scores, 'language:expression': min })).toBe(min);
    expect(languageCriterionValue(card.rubric, 'expression', { ...scores, 'language:expression': normal })).toBe(max);
  });

  it('restores the stored placement when a condition is cleared', () => {
    const card = source();
    const scores: LanguageScores = { 'language:content': 10, 'language:expression': 6 };
    expect(languageMarks(card, scores)).toBe(16);
    expect(languageMarks(card, { ...scores, 'language:flag:accuracy': 1 })).toBe(10);
    expect(languageMarks(card, { ...scores, 'language:flag:accuracy': 0 })).toBe(16);
    expect(scores['language:expression']).toBe(6);
  });

  it('intersects other caps and keeps zero-content and deductions authoritative', () => {
    const card = source();
    card.rubric.criteria[1].limits!.push({ id: 'other-cap', maxMarks: 10,
      when: { any: [{ flag: 'other', prompt: 'Other source cap applies' }] }, guidance: [] });
    card.rubric.criteria.push({ id: 'deduction', label: 'Deduction', kind: 'deduction', deductFrom: 'expression', maxMarks: 1, permittedMarks: [0, 1], guidance: [] });
    expect(tariffReconciles(card)).toBe(true);
    const scores: LanguageScores = { 'language:content': 10, 'language:expression': 20, 'language:flag:accuracy': 1, 'language:flag:other': 1 };
    expect(languageCriterionValue(card.rubric, 'expression', scores)).toBe(10);
    expect(languageCriterionValue(card.rubric, 'expression', { ...scores, 'language:deduction': 1 })).toBe(9);
    expect(languageMarks(card, { ...scores, 'language:content': 0 })).toBe(0);
    card.rubric.criteria[1].limits!.at(-1)!.maxMarks = 5;
    expect(languageCriterionValue(card.rubric, 'expression', scores)).toBe(0);
  });

  it('rejects invalid ranges, missing bands and overlapping source bands', () => {
    for (const min of [-1, 8.5, 15, NaN, Infinity]) {
      const card = source();
      card.rubric.criteria[1].limits![0].minMarks = min;
      expect(tariffReconciles(card)).toBe(false);
    }
    const missing = source();
    missing.rubric.criteria[1].limits![0].bands!.pop();
    expect(tariffReconciles(missing)).toBe(false);
    const overlap = source();
    overlap.rubric.criteria[1].limits![0].bands![0].marks.push(11);
    expect(tariffReconciles(overlap)).toBe(false);
  });

  it('offers only the active source range and never auto-awards its minimum', () => {
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>({ 'language:content': 10 });
      return <LanguageRubricPanel card={source()} scores={scores}
        onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: 'Set Expression to 6 marks' }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'Source Lower A accuracy condition applies' }));
    const controls = screen.getByRole('group', { name: 'Expression mark' });
    expect(within(controls).getAllByRole('button').map(button => button.textContent)).toEqual(['0', '9', '10', '11', '12', '13', '14']);
    expect(screen.getByText('10 / 30')).toBeInTheDocument();
    expect(screen.getByText('Choose a mark within the active range.')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('checkbox', { name: 'Source Lower A accuracy condition applies' }));
    expect(screen.getByRole('button', { name: 'Set Expression to 6 marks' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByText('16 / 30')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('checkbox', { name: 'Source Lower A accuracy condition applies' }));
    fireEvent.click(screen.getByRole('button', { name: 'Set Expression to 9 marks' }));
    expect(screen.getByText('19 / 30')).toBeInTheDocument();
    expect(screen.queryByText('Choose a mark within the active range.')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Set Content to 0 marks' }));
    expect(screen.getByText('0 / 30')).toBeInTheDocument();
    expect(within(controls).getAllByRole('button').map(button => button.textContent)).toEqual(['0']);
    expect(screen.queryByText('Published first descriptor.')).not.toBeInTheDocument();
  });

  it('prompts reassessment when an existing placement is capped onto a different source range', () => {
    render(<LanguageRubricPanel card={source()} scores={{ 'language:content': 10, 'language:expression': 20, 'language:flag:accuracy': 1 }} onScore={() => {}} />);
    expect(screen.getByText('24 / 30')).toBeInTheDocument();
    expect(screen.getByText('Review this placement against the active range.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Set Expression to 14 marks' })).toHaveAttribute('aria-pressed', 'true');
  });

  it('retains both applicable source tables without choosing descriptor precedence or rewriting ranges', () => {
    const card = source();
    card.rubric.criteria[1].limits!.push({ id: 'lower-e', maxMarks: 10, scaleLabel: 'Lower E',
      when: { any: [{ flag: 'short', prompt: 'Lower E condition applies' }] }, guidance: [], bands: [
        { label: 'Lower E bottom band', marks: steps(0, 3), guidance: ['Published lower expression bottom descriptor.'] },
        { label: 'Lower E middle band', marks: steps(4, 6), guidance: ['Published lower expression middle descriptor.'] },
        { label: 'Lower E upper band', marks: steps(7, 10), guidance: ['Published lower expression upper descriptor.'] },
      ] });
    expect(tariffReconciles(card)).toBe(true);
    render(<LanguageRubricPanel card={card} scores={{ 'language:content': 10, 'language:expression': 20,
      'language:flag:accuracy': 1, 'language:flag:short': 1 }} onScore={() => {}} />);
    expect(screen.getByText('Lower A')).toBeInTheDocument();
    expect(screen.getByText('Lower E')).toBeInTheDocument();
    expect(screen.getByText('Both source scales apply. Use their shared mark range and reassess against each set of descriptors.')).toBeInTheDocument();
    expect(screen.getByText('7–10 marks · Lower E upper band')).toBeInTheDocument();
    expect(screen.getByText('Published first descriptor.')).toBeInTheDocument();
    expect(screen.getByText('Published lower expression upper descriptor.')).toBeInTheDocument();
    expect(within(screen.getByRole('group', { name: 'Expression mark' })).getAllByRole('button').map(button => button.textContent)).toEqual(['0', '9', '10']);
    expect(screen.getByText('20 / 30')).toBeInTheDocument();
  });
});
