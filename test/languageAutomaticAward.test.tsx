import React, { useState } from 'react';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import SessionScreen, { rubricMarks } from '../components/MarkBank/SessionScreen';
import { languageMarks, languageScoreId, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, type LanguagePointsRubric, type LanguageWritingRubric, type SecRubricCard } from '../types/markBank';
import original from './fixtures/russian2010UniversalAward.json';

type WritingCard = SecRubricCard & { rubric: LanguageWritingRubric };
const fixture = () => structuredClone(original) as WritingCard;
const fixedId = 'section2-dative-plural';
afterEach(cleanup);

describe('published language awards to all candidates', () => {
  it('retains the fixed award for blank, reset, stale and invalid saved placements without altering saved state', () => {
    const card = fixture();
    expect(tariffReconciles(card)).toBe(true);
    expect(card.rubric.criteria).toHaveLength(6);
    expect(card.rubric.criteria.reduce((sum, criterion) => sum + criterion.maxMarks, 0)).toBe(12);
    for (const scores of [{}, ...[0, 1, 2, 99, -1, Number.NaN].map(mark => ({ [languageScoreId(fixedId)]: mark }))]) {
      const saved = structuredClone(scores);
      expect(languageMarks(card, scores)).toBe(2);
      expect(rubricMarks(card, scores)).toBe(2);
      expect(scores).toEqual(saved);
    }
    const full = Object.fromEntries(card.rubric.criteria.filter(criterion => !criterion.automaticAward)
      .map(criterion => [languageScoreId(criterion.id), 2]));
    expect(languageMarks(card, full)).toBe(12);
    expect(languageMarks(card, {})).toBe(2);
  });

  it('shows the exact source award without a claim control and leaves the other five placements manual', () => {
    const card = fixture();
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>({ [languageScoreId(fixedId)]: 0 });
      return <><LanguageRubricPanel card={card} scores={scores} onScore={(id, marks) => setScores(previous => ({ ...previous, [id]: marks }))} />
        <button onClick={() => setScores({})}>Reset fixture</button></>;
    }
    render(<Harness />);
    const criterion = card.rubric.criteria.find(item => item.id === fixedId)!;
    const section = screen.getByRole('heading', { name: criterion.label }).closest('section')!;
    expect(within(section).getByText('2 marks awarded to all candidates')).toBeVisible();
    expect(within(section).getAllByText(criterion.automaticAward!.sourceText)[0]).toBeVisible();
    expect(within(section).queryByRole('button')).not.toBeInTheDocument();
    expect(within(section).queryByRole('checkbox')).not.toBeInTheDocument();
    expect(screen.getByText('2 / 12')).toBeVisible();
    for (const manual of card.rubric.criteria.filter(item => !item.automaticAward)) {
      fireEvent.click(screen.getByRole('button', { name: `Set ${manual.label} to 2 marks` }));
    }
    expect(screen.getByText('12 / 12')).toBeVisible();
    fireEvent.click(screen.getByRole('button', { name: 'Reset fixture' }));
    expect(screen.getByText('2 / 12')).toBeVisible();
  });

  it.each([false, true])('saves the published fixed award for an unplaced response in paper layout=%s', async paperLayout => {
    const card = fixture(), onGrade = vi.fn();
    render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian test fixture" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByText('2 marks awarded to all candidates')).toBeVisible());
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: card.id, marksClaimed: 2, marksAvailable: 12 }));
  });

  it.each([
    { marks: 0 }, { marks: 1 }, { marks: 2.5 }, { marks: Number.NaN },
    { sourceText: ' ' }, { schemePages: [] }, { schemePages: [0] }, { schemePages: [1.5] },
  ])('rejects unbound or mismatched automatic awards %j', change => {
    const card = fixture();
    Object.assign(card.rubric.criteria.find(item => item.id === fixedId)!.automaticAward!, change);
    expect(tariffReconciles(card)).toBe(false);
  });

  it('rejects manual zero, conditional limits, bands, deductions and whole-response language adjustments', () => {
    const edits: Array<(card: WritingCard) => void> = [
      card => { card.rubric.criteria[3].permittedMarks = [0, 2]; },
      card => { card.rubric.criteria[3].limits = []; },
      card => { card.rubric.criteria[3].bands = []; },
      card => { card.rubric.criteria[3].kind = 'deduction'; },
      card => { card.rubric.criteria[3].deductFrom = card.rubric.criteria[0].id; },
      card => { card.rubric.criteria[0].kind = 'deduction'; card.rubric.criteria[0].deductFrom = fixedId; },
      card => { card.answerLanguageRule = { otherLanguageMultiplier: 0, sourceText: 'Wrong language', schemePages: [3] }; },
    ];
    for (const edit of edits) { const card = fixture(); edit(card); expect(tariffReconciles(card)).toBe(false); }
  });

  it('rejects automatic awards inside selectable groups or top-level points criteria', () => {
    const card = fixture(), fixed = card.rubric.criteria[3];
    const points: SecRubricCard & { rubric: LanguagePointsRubric } = { ...card, totalMarks: 2, rubric: {
      system: 'language-points', count: 1, taskRequirements: [], markingGuideNote: '',
      groups: [{ id: 'choice', label: 'Choice', rows: [], criteria: [fixed] }],
    } };
    expect(tariffReconciles(points)).toBe(false);
    points.rubric = { ...points.rubric, criteria: [fixed], groups: [{ id: 'choice', label: 'Choice', rows: [{ id: 'row', text: 'Answer', marks: 2 }] }] };
    expect(tariffReconciles(points)).toBe(false);
  });

  it('does not grant the minimum of an ordinary manual source range', () => {
    const card = fixture();
    const criterion = card.rubric.criteria[3];
    delete criterion.automaticAward;
    criterion.permittedMarks = [0, 2];
    criterion.limits = [{ id: 'manual-range', minMarks: 2, maxMarks: 2,
      when: { any: [{ flag: 'manual', prompt: 'Use this source scale' }] }, guidance: ['Manual test range'] }];
    expect(tariffReconciles(card)).toBe(true);
    expect(languageMarks(card, { 'language:flag:manual': 1 })).toBe(0);
  });
});
