import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';
import { languageMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

// Russian 2012 Higher original scheme physical p9, SHA256
// eb369d55edcd65c40ace69eac2206c44ba545ddd0118658364537e5f9ac2e4fe.
// Four details + discretion OR five details, because the general rubric was
// omitted on the paper. These fixture slots exercise that published structure;
// they are not authored answer pools or a replacement for source review.
const source = 'Award 2 marks for each of 4 details (up to 8 marks) AND 2 discretionary marks';
const alternative = 'OR – given that the general rubric was omitted on the examination paper: Award 2 marks for each of 5 details (up to 10 marks)';
const incomplete = 'If a candidate fails to answer all sections/sub-section of a question, do not award more than 1 discretionary mark';
const prompt = 'This response does not answer all sections or subsections.';
const rows = (count: number) => Array.from({ length: count }, (_, i) => ({
  id: `detail${i + 1}`, text: `Distinct detail ${i + 1}`, marks: 2, steps: [0, 1, 2],
}));
const rubric: LanguagePointsRubric = {
  system: 'language-points', count: 1, taskRequirements: [source, alternative], markingGuideNote: 'If candidates answer in Russian – do not penalise',
  alternativeSets: [{ id: 'summary-route', label: 'Published summary alternatives', sourceText: `${source}. ${alternative}`, schemePages: [9] }],
  groups: [
    { id: 'standard', label: 'Four details and discretionary marks', alternativeSet: 'summary-route', rows: rows(4),
      criteria: [{ id: 'discretion', label: 'Discretionary marks', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [source],
        limits: [{ id: 'incomplete', maxMarks: 1, when: { any: [{ flag: 'standard-incomplete', prompt }] }, guidance: [incomplete] }] }] },
    { id: 'alternative', label: 'Five details without discretionary marks', alternativeSet: 'summary-route', rows: rows(5) },
  ],
};
const card = { kind: 'rubric', totalMarks: 10, rubric } as SecRubricCard & { rubric: LanguagePointsRubric };
const scores: LanguageScores = { 'language:group:standard': 1, 'language:discretion': 2 };
for (const group of rubric.groups) for (const row of group.rows) scores[`language:row:${group.id}:${row.id}`] = 2;

describe('explicit flags within selected language responses', () => {
  it('applies the incomplete cap only within the selected four-detail route', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(languageMarks(card, scores)).toBe(10);
    const flagged: LanguageScores = { ...scores, 'language:flag:standard-incomplete': 1 };
    expect(languageMarks(card, flagged)).toBe(9);
    expect(languageMarks(card, { ...flagged, 'language:discretion': 0 })).toBe(8);
    expect(languageMarks(card, { ...flagged, 'language:group:standard': 0, 'language:group:alternative': 1 })).toBe(10);
    expect(languageMarks(card, { ...flagged, 'language:group:alternative': 1 })).toBe(0);
    expect(languageMarks(card, { ...flagged, 'language:flag:standard-incomplete': 0 })).toBe(10);
    expect(scores['language:discretion']).toBe(2);
  });

  it('renders an explicit scoped control and retains its state when switching routes', () => {
    function Harness() {
      const [placed, setPlaced] = useState<LanguageScores>(scores);
      return <LanguageRubricPanel card={card} scores={placed} onScore={(id, value) => setPlaced(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    const flag = screen.getByRole('checkbox', { name: prompt });
    expect(flag).toBeEnabled();
    fireEvent.click(flag);
    expect(screen.getByText('9 / 10')).toBeInTheDocument();
    expect(screen.getByText(incomplete)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Set Discretionary marks to 2 marks' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Four details and discretionary marks' }));
    expect(flag).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Five details without discretionary marks' }));
    expect(screen.getByText('10 / 10')).toBeInTheDocument();
    expect(flag).toBeChecked();
    fireEvent.click(screen.getByRole('button', { name: 'Five details without discretionary marks' }));
    fireEvent.click(screen.getByRole('button', { name: 'Four details and discretionary marks' }));
    expect(screen.getByText('9 / 10')).toBeInTheDocument();
    fireEvent.click(flag);
    expect(screen.getByText('10 / 10')).toBeInTheDocument();
  });

  it('disables a group flag when restored alternative selections conflict', () => {
    render(<LanguageRubricPanel card={card} scores={{ ...scores, 'language:group:alternative': 1 }} onScore={() => {}} />);
    expect(screen.getByRole('checkbox', { name: prompt })).toBeDisabled();
    expect(screen.getByText('0 / 10')).toBeInTheDocument();
  });

  it('rejects flags that leak between groups, response criteria or allocation controls', () => {
    const another = structuredClone(card);
    const criterion = structuredClone(another.rubric.groups[0].criteria![0]);
    criterion.id = 'other-discretion';
    another.rubric.groups[1].rows = rows(4);
    another.rubric.groups[1].criteria = [criterion];
    expect(tariffReconciles(another)).toBe(false);
    const condition = criterion.limits![0].when.any[0];
    if (!('flag' in condition)) throw new Error('fixture must have a flag');
    condition.flag = 'alternative-incomplete';
    expect(tariffReconciles(another)).toBe(true);

    const whole = structuredClone(card);
    whole.totalMarks = 12;
    whole.rubric.criteria = [structuredClone(criterion)];
    whole.rubric.criteria[0].id = 'whole-discretion';
    const wholeCondition = whole.rubric.criteria[0].limits![0].when.any[0];
    if (!('flag' in wholeCondition)) throw new Error('fixture must have a flag');
    wholeCondition.flag = 'standard-incomplete';
    expect(tariffReconciles(whole)).toBe(false);

    const capped = structuredClone(card);
    capped.rubric.allocationCap = { maxMarks: 10, sourceText: source, schemePages: [9],
      limits: [{ id: 'whole', maxMarks: 9, when: { flag: 'standard-incomplete', prompt }, sourceText: incomplete, schemePages: [9] }] };
    expect(tariffReconciles(capped)).toBe(false);
  });

  it('rejects contradictory prompts for the same group flag', () => {
    const changed = structuredClone(card);
    const limit = structuredClone(changed.rubric.groups[0].criteria![0].limits![0]);
    limit.id = 'different-wording';
    const condition = limit.when.any[0];
    if (!('flag' in condition)) throw new Error('fixture must have a flag');
    condition.prompt = 'A different condition';
    changed.rubric.groups[0].criteria![0].limits!.push(limit);
    expect(tariffReconciles(changed)).toBe(false);
  });
});
