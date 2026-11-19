import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { tariffReconciles, type SecRubricCard, type LanguagePointsRubric } from '../types/markBank';
import { languageMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

// Russian 2010 Ordinary scheme p11 awards5 for a full listening answer,
// half for an answer entirely in Russian, and2 for the named partial
// "President". Isolated Russian words are explicitly exempt.
const card = (steps = [0, 1, 2, 2.5, 5]) => ({
  kind: 'rubric', totalMarks: 5,
  rubric: { system: 'language-points', taskRequirements: [], markingGuideNote: '', count: 1,
    groups: [{ id: 'visitor', label: 'Visitor detail', answerCount: 1,
      rows: [{ id: 'answer', text: 'Accepted visitor detail', marks: 5, steps }] }] },
}) as SecRubricCard & { rubric: LanguagePointsRubric };

describe('source-defined fractional language steps', () => {
  it('retains the exact half award and rejects unprinted selections', () => {
    const source = card();
    expect(tariffReconciles(source)).toBe(true);
    const scores: LanguageScores = { 'language:group:visitor': 1, 'language:row:visitor:answer': 2.5 };
    expect(languageMarks(source, scores)).toBe(2.5);
    expect(languageMarks(source, { ...scores, 'language:row:visitor:answer': 1 })).toBe(1);
    expect(languageMarks(source, { ...scores, 'language:row:visitor:answer': 3.5 })).toBe(0);
    expect(languageMarks(source, { ...scores, 'language:group:visitor': 0 })).toBe(0);
    expect(languageMarks(source, JSON.parse(JSON.stringify(scores)))).toBe(2.5);
  });

  it.each([
    [], [0, NaN, 5], [0, Infinity, 5], [0, -0.5, 5], [0, 2.5, 2.5, 5],
    [0, 5, 2.5], [0, 6, 5], [0.5, 5], [0, 2.5],
  ].map(steps => ({ steps })))('rejects malformed source steps $steps', ({ steps }) => {
    expect(tariffReconciles(card(steps))).toBe(false);
  });

  it('lets the student select and clear a fractional award without rounding', () => {
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>({});
      return <LanguageRubricPanel card={card()} scores={scores}
        onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    const half = screen.getByRole('button', { name: 'Claim 2.5 marks for Accepted visitor detail' });
    expect(half).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Visitor detail' }));
    fireEvent.click(half);
    expect(screen.getByText('2.5 / 5')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Clear 2.5 marks for Accepted visitor detail' }));
    expect(screen.getByText('0 / 5')).toBeInTheDocument();
  });
});
