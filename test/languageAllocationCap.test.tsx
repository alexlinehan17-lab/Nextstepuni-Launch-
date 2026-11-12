import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';
import { languageMarks, languagePointsMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

// Russian2023Higher scheme p20: three2-mark details; hockey-only details
// earn at most4. Group quotas and the overall detail quota both apply.
const sourceText = 'Candidates must mention at least two hobbies; if all details relate only to hockey, a maximum of 4 marks can be awarded.';
const rubric: LanguagePointsRubric = {
  system: 'language-points', count: 3, taskRequirements: ['Give three details.'], markingGuideNote: '',
  allocationCap: { maxMarks: 6, answerCount: 3, sourceText, schemePages: [20] },
  groups: [
    { id: 'hockey', label: 'Hockey', answerCount: 2, rows: [
      { id: 'sport', text: 'Ice hockey', marks: 2 },
      { id: 'school', text: 'He went to a sports school', marks: 2 },
      { id: 'training', text: 'Trained in Czech Republic for a year', marks: 2 },
    ] },
    ...['Music', 'Break dance', 'YouTube'].map((text, i) => ({ id: `other${i}`, label: `${text} detail`, rows: [{ id: 'answer', text, marks: 2 }] })),
  ],
};
const card = { kind: 'rubric', totalMarks: 6, rubric } as SecRubricCard & { rubric: LanguagePointsRubric };
const hockey: LanguageScores = { 'language:group:hockey': 1,
  'language:row:hockey:sport': 1, 'language:row:hockey:school': 1, 'language:row:hockey:training': 1 };

describe('source-defined language allocation and detail quotas', () => {
  it('reconciles both quotas and requires another hobby for full credit', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(languagePointsMarks(rubric, hockey)).toBe(4);
    const mixed = { ...hockey, 'language:group:other0': 1, 'language:row:other0:answer': 1 } as LanguageScores;
    expect(languagePointsMarks(rubric, mixed)).toBe(6);
    expect(languagePointsMarks(rubric, { ...mixed, 'language:group:other1': 1, 'language:row:other1:answer': 1 })).toBe(6);
    expect(languagePointsMarks(rubric, { ...mixed, 'language:group:hockey': 0 })).toBe(2);
    expect(tariffReconciles({ ...card, totalMarks: 8 })).toBe(false);
  });

  it('counts at most three details even when independent language rules create unequal credit', () => {
    // Synthetic half-credit rule exercises the shared scorer, not a claim
    // that Russian2023's source has this particular language multiplier.
    const rule = { otherLanguageMultiplier: 0.5 as const, sourceText: 'Synthetic half-credit condition.', schemePages: [1] };
    const scores: LanguageScores = { ...hockey, 'language:row:hockey:training': 0,
      'language:other-language:row:hockey:sport': 1, 'language:other-language:row:hockey:school': 1,
      'language:group:other0': 1, 'language:row:other0:answer': 1,
      'language:group:other1': 1, 'language:row:other1:answer': 1 };
    expect(languagePointsMarks(rubric, scores, rule)).toBe(5); // best3 of1,1,2,2
    expect(languageMarks({ ...card, answerLanguageRule: rule }, { ...scores, 'language:other-language:response': 1 })).toBe(3);
    expect(languagePointsMarks(rubric, scores, { ...rule, otherLanguageMultiplier: 0 })).toBe(4);
  });

  it('keeps separately assessed discretionary criteria outside the detail allocation', () => {
    const withDiscretion = { ...rubric, criteria: [{ id: 'discretion', label: 'Discretion', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [] }] };
    expect(tariffReconciles({ ...card, totalMarks: 8, rubric: withDiscretion })).toBe(true);
    const scores: LanguageScores = { ...hockey, 'language:group:other0': 1, 'language:row:other0:answer': 1 };
    expect(languagePointsMarks(withDiscretion, scores)).toBe(6);
    expect(languagePointsMarks(withDiscretion, { ...scores, 'language:discretion': 2 })).toBe(8);
  });

  it('checks the achievable maximum under both group and row quotas', () => {
    const constrained: LanguagePointsRubric = { ...rubric, count: 1,
      allocationCap: { ...rubric.allocationCap!, maxMarks: 4, answerCount: 2 } };
    expect(tariffReconciles({ ...card, totalMarks: 4, rubric: constrained })).toBe(true);
    expect(tariffReconciles({ ...card, rubric: { ...constrained, allocationCap: { ...constrained.allocationCap!, maxMarks: 6 } } })).toBe(false);
  });

  it.each([
    { maxMarks: 0 }, { maxMarks: 7 }, { maxMarks: Infinity },
    { answerCount: 0 }, { answerCount: 1.5 }, { answerCount: 10 },
    { sourceText: '' }, { schemePages: [] }, { schemePages: [0] },
  ])('rejects an invalid or unbound allocation cap %j', change => {
    expect(tariffReconciles({ ...card, rubric: { ...rubric, allocationCap: { ...rubric.allocationCap!, ...change } } })).toBe(false);
  });

  it('rejects grouped writing criteria whose answers cannot be counted as rows', () => {
    const invalid = structuredClone(card);
    invalid.rubric.groups[0].criteria = [{ id: 'expression', label: 'Expression', maxMarks: 1, permittedMarks: [0, 1], guidance: [] }];
    expect(tariffReconciles(invalid)).toBe(false);
  });

  it('shows the source cap and prevents a fourth claimed detail until one is cleared', () => {
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>({});
      return <LanguageRubricPanel card={card} scores={scores}
        onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    expect(screen.getByText(sourceText)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Hockey' }));
    fireEvent.click(screen.getByRole('button', { name: 'Ice hockey · 2m' }));
    fireEvent.click(screen.getByRole('button', { name: 'He went to a sports school · 2m' }));
    expect(screen.getByRole('button', { name: 'Trained in Czech Republic for a year · 2m' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Music detail' }));
    fireEvent.click(screen.getByRole('button', { name: 'Music · 2m' }));
    fireEvent.click(screen.getByRole('button', { name: 'Break dance detail' }));
    expect(screen.getByRole('button', { name: 'Break dance · 2m' })).toBeDisabled();
    expect(screen.getByText('6 / 6')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Ice hockey · 2m' }));
    expect(screen.getByRole('button', { name: 'Break dance · 2m' })).toBeEnabled();
    fireEvent.click(screen.getByRole('button', { name: 'Break dance · 2m' }));
    expect(screen.getByText('6 / 6')).toBeInTheDocument();
  });
});
