import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';
import { languageCategoryCompensation, languageMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

// Russian2012 Higher, original scheme physicalp24, L2Q4. Source SHA256:
// eb369d55edcd65c40ace69eac2206c44ba545ddd0118658364537e5f9ac2e4fe.
// Categories are manual placements; the source does not price individual
// transport lines or allocate them automatically to a category.
const source = 'Assign 2 marks to venue; 2 marks to time; 2 marks to price. If a candidate scores 1 for a category, they can score 3 for another category.';
const categories = ['venue', 'time', 'price'];
const rubric: LanguagePointsRubric = {
  system: 'language-points', count: 3, taskRequirements: ['Give three details about venue, time and price of the concert.'],
  markingGuideNote: 'Place each category using the complete scheme pool. One mark: discount ticket offer.',
  allocationCap: { maxMarks: 6, sourceText: source, schemePages: [24],
    categoryCompensation: { normalMarks: 2, reducedMarks: 1, increasedMarks: 3 } },
  groups: categories.map(id => ({ id, label: id, rows: [{ id: 'response', text: `Assess ${id}`, marks: 3, steps: [0, 1, 2, 3] }] })),
};
const card = { kind: 'rubric', totalMarks: 6, rubric } as SecRubricCard & { rubric: LanguagePointsRubric };
const placed = (...marks: number[]): LanguageScores => Object.fromEntries(categories.flatMap((id, i) => [
  [`language:group:${id}`, 1], [`language:row:${id}:response`, marks[i]],
]));

describe('source-bound compensation between language categories', () => {
  it.each([
    [[0, 0, 0], 0], [[2, 2, 2], 6], [[3, 1, 2], 6], [[1, 3, 2], 6], [[2, 1, 3], 6],
    [[3, 1, 0], 4], [[3, 1, 1], 5], [[3, 0, 2], 4], [[3, 3, 0], 4], [[3, 3, 1], 5],
  ] as Array<[number[], number]>)('scores %j as %i without inventing a category award', (marks, expected) => {
    expect(tariffReconciles(card)).toBe(true);
    expect(languageMarks(card, placed(...marks))).toBe(expected);
  });

  it('requires a selected, valid qualifying mark and preserves raw placements when it changes', () => {
    const scores = placed(3, 1, 2);
    expect(languageMarks(card, scores)).toBe(6);
    expect(languageMarks(card, { ...scores, 'language:group:time': 0 })).toBe(4);
    expect(languageMarks(card, { ...scores, 'language:row:time:response': 0 })).toBe(4);
    expect(languageMarks(card, { ...scores, 'language:row:time:response': 2 })).toBe(6);
    expect(languageCategoryCompensation(rubric, { ...scores, 'language:row:time:response': 2 })?.needsReview).toBe(true);
    expect(languageMarks(card, { ...scores, 'language:row:time:response': 1.5 })).toBe(4);
    expect(languageMarks(card, { ...scores, 'language:row:venue:response': NaN })).toBe(3);
    expect(languageMarks(card, { ...scores, 'language:row:venue:response': 4 })).toBe(3);
    expect(scores['language:row:venue:response']).toBe(3);
    expect(languageCategoryCompensation(rubric, scores)?.needsReview).toBe(false);
  });

  it('does not use post-adjustment language credit as an inferred category placement', () => {
    // Synthetic combination, not a source claim about Russian2012 listening.
    const mixed = { ...card, answerLanguageRule: { otherLanguageMultiplier: 0.5 as const, sourceText: 'Synthetic half-credit rule.', schemePages: [1] } };
    expect(languageMarks(mixed, { ...placed(3, 2, 2), 'language:other-language:row:time:response': 1 })).toBe(5);
    expect(languageMarks(mixed, { ...placed(3, 1, 1), 'language:other-language:response': 1 })).toBe(2.5);
  });

  it('enables one increase for another reduced category and keeps unsupported saved marks clearable', () => {
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>(placed(2, 2, 2));
      return <LanguageRubricPanel card={card} scores={scores} onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    expect(screen.getByText(source)).toBeInTheDocument();
    for (const id of categories) expect(screen.getByRole('button', { name: `Claim 3 marks for Assess ${id}` })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Claim 1 marks for Assess price' }));
    expect(screen.getByRole('button', { name: 'Claim 3 marks for Assess price' })).toBeDisabled(); // cannot fund itself
    expect(screen.getByRole('button', { name: 'Claim 3 marks for Assess venue' })).toBeEnabled();
    fireEvent.click(screen.getByRole('button', { name: 'Claim 3 marks for Assess venue' }));
    expect(screen.getByText('6 / 6')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Claim 3 marks for Assess time' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Clear 1 marks for Assess price' }));
    expect(screen.getByText('4 / 6')).toBeInTheDocument();
    expect(screen.getByRole('status')).toHaveTextContent('Review the increased category marks');
    expect(screen.getByRole('button', { name: 'Clear 3 marks for Assess venue' })).toBeEnabled();
    fireEvent.click(screen.getByRole('button', { name: 'Claim 1 marks for Assess price' }));
    expect(screen.getByText('6 / 6')).toBeInTheDocument();
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Clear 3 marks for Assess venue' }));
    expect(screen.getByText('3 / 6')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Claim 3 marks for Assess time' })).toBeEnabled();
  });

  it.each([
    { normalMarks: 0 }, { reducedMarks: 0 }, { reducedMarks: 2 }, { reducedMarks: 1.5 },
    { increasedMarks: 2 }, { increasedMarks: 4 }, { normalMarks: NaN },
  ])('rejects unsupported transfer metadata %j', change => {
    const invalid = structuredClone(card);
    Object.assign(invalid.rubric.allocationCap!.categoryCompensation!, change);
    expect(tariffReconciles(invalid)).toBe(false);
  });

  it('requires all categories, a genuine normal total, full source binding and one manual row per category', () => {
    const changes: Array<(copy: typeof card) => void> = [
      copy => { copy.rubric.count = 2; },
      copy => { copy.rubric.allocationCap!.answerCount = 3; },
      copy => { copy.totalMarks = copy.rubric.allocationCap!.maxMarks = 5; },
      copy => { copy.rubric.allocationCap!.sourceText = ' '; },
      copy => { copy.rubric.allocationCap!.schemePages = []; },
      copy => { copy.rubric.groups[0].rows.push({ id: 'extra', text: 'Extra', marks: 1 }); },
      copy => { copy.rubric.groups[0].rows[0].steps = [0, 2, 3]; },
      copy => { copy.rubric.groups[0].rows[0].steps = [0, 1, 2, 2.5, 3]; },
      copy => { copy.rubric.groups[0].criteria = [{ id: 'extra', label: 'Extra', maxMarks: 1, permittedMarks: [0, 1], guidance: [] }]; },
    ];
    for (const change of changes) {
      const invalid = structuredClone(card); change(invalid);
      expect(tariffReconciles(invalid)).toBe(false);
    }
  });
});
