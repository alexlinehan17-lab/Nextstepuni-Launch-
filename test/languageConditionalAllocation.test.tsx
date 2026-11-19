import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';
import { languageMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

// Russian2015Higher scheme physicalp16, L3Q1: two2-mark details with a
// conditional overall3-mark maximum. There is no1-mark partial detail here.
const sourceText = 'In order to obtain full marks (4 marks), at least one detail must make reference one of the following: work, employment, boxing, trainer, position, post. Where none of these is mentioned, award a maximum of 3 marks.';
const prompt = 'No detail refers to work, employment, boxing, a trainer, a position or a post.';
const details = ['To take up post of', 'senior trainer', 'national boxing team', 'he was invited to the interview',
  'he was successful at interview', 'has been living in Ireland since 2003'];
const rubric: LanguagePointsRubric = {
  system: 'language-points', count: 1, taskRequirements: ['Give two details.'], markingGuideNote: '',
  allocationCap: { maxMarks: 4, answerCount: 2, sourceText, schemePages: [16], limits: [{
    id: 'missing-reference', maxMarks: 3, when: { flag: 'missing-reference', prompt }, sourceText, schemePages: [16],
  }] },
  groups: [{ id: 'details', label: 'Details you answered', answerCount: 2,
    rows: details.map((text, i) => ({ id: `${i}`, text, marks: 2 })) }],
};
const card = { kind: 'rubric', totalMarks: 4, rubric } as SecRubricCard & { rubric: LanguagePointsRubric };
const scores: LanguageScores = { 'language:group:details': 1, 'language:row:details:3': 1, 'language:row:details:4': 1 };

describe('source-defined conditional allocation caps', () => {
  it('caps two full details only when explicitly flagged and preserves raw placements', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(languageMarks(card, scores)).toBe(4);
    expect(languageMarks(card, { ...scores, 'language:flag:missing-reference': 1 })).toBe(3);
    expect(languageMarks(card, { ...scores, 'language:flag:missing-reference': 0 })).toBe(4);
    expect(scores['language:row:details:3']).toBe(1);
    expect(languageMarks(card, { ...scores, 'language:flag:missing-reference': 1, 'language:row:details:4': 0 })).toBe(2);
    expect(languageMarks(card, { 'language:flag:missing-reference': 1 })).toBe(0);
    expect(languageMarks(card, { ...scores, 'language:flag:missing-reference': 1, 'language:row:details:5': 1 })).toBe(3);
  });

  it('applies the cap before a separate whole-response language rule and outside discretionary criteria', () => {
    // Synthetic combination: Russian2015 listening accepts Russian and does
    // not carry this half-credit rule or discretionary allocation.
    const combined = { ...card, totalMarks: 6, answerLanguageRule: {
      otherLanguageMultiplier: 0.5 as const, sourceText: 'Synthetic half-credit rule.', schemePages: [1],
    }, rubric: { ...rubric, criteria: [{ id: 'discretion', label: 'Discretion', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [] }] } };
    expect(tariffReconciles(combined)).toBe(true);
    const placed: LanguageScores = { ...scores, 'language:flag:missing-reference': 1, 'language:discretion': 2 };
    expect(languageMarks(combined, placed)).toBe(5);
    expect(languageMarks(combined, { ...placed, 'language:other-language:response': 1 })).toBe(2.5);
    expect(languageMarks(combined, { ...placed, 'language:flag:missing-reference': 0, 'language:other-language:response': 1 })).toBe(3);
  });

  it.each([
    { maxMarks: -1 }, { maxMarks: 4 }, { maxMarks: 5 }, { maxMarks: 2.5 }, { maxMarks: NaN },
    { id: ' ' }, { sourceText: '\n' }, { schemePages: [] }, { schemePages: [0] }, { schemePages: [1.5] },
    { when: { flag: ' ', prompt } }, { when: { flag: 'missing-reference', prompt: ' ' } },
  ])('rejects invalid conditional cap metadata %j', change => {
    const invalid = structuredClone(card);
    Object.assign(invalid.rubric.allocationCap!.limits![0], change);
    expect(tariffReconciles(invalid)).toBe(false);
  });

  it('rejects duplicate conditions and combines distinct caps by their shared maximum', () => {
    const modified = structuredClone(card);
    modified.rubric.allocationCap!.limits!.push({ ...modified.rubric.allocationCap!.limits![0] });
    expect(tariffReconciles(modified)).toBe(false);
    Object.assign(modified.rubric.allocationCap!.limits![1], { id: 'other', maxMarks: 2, when: { flag: 'other', prompt: 'Another source condition' } });
    expect(tariffReconciles(modified)).toBe(true);
    expect(languageMarks(modified, { ...scores, 'language:flag:missing-reference': 1, 'language:flag:other': 1 })).toBe(2);
    modified.rubric.allocationCap!.limits![1].maxMarks = 0;
    expect(tariffReconciles(modified)).toBe(true);
    expect(languageMarks(modified, { ...scores, 'language:flag:other': 1 })).toBe(0);
  });

  it('renders the literal rule and explicit condition without inventing partial-detail controls', () => {
    function Harness() {
      const [placed, setPlaced] = useState<LanguageScores>(scores);
      return <LanguageRubricPanel card={card} scores={placed}
        onScore={(id, value) => setPlaced(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    expect(screen.getAllByText(sourceText)).toHaveLength(1);
    expect(screen.getByText('4 / 4')).toBeInTheDocument();
    for (const text of details) expect(screen.getByRole('button', { name: `${text} · 2m` })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /1 mark/ })).not.toBeInTheDocument();
    const flag = screen.getByRole('checkbox', { name: prompt });
    fireEvent.click(flag);
    expect(screen.getByText('3 / 4')).toBeInTheDocument();
    expect(screen.getByText('These answers earn up to 3 marks altogether.')).toBeInTheDocument();
    fireEvent.click(flag);
    expect(screen.getByText('4 / 4')).toBeInTheDocument();
    fireEvent.click(flag);
    fireEvent.click(screen.getByRole('button', { name: 'he was successful at interview · 2m' }));
    expect(screen.getByText('2 / 4')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'he was invited to the interview · 2m' }));
    expect(screen.getByText('0 / 4')).toBeInTheDocument();
  });
});
