import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen, { answerLanguageClaimId, extraneousMaterialClaimId, marksClaimed, partClaimId, type SessionResponse } from '../components/MarkBank/SessionScreen';
import { emptyWaysInWork } from '../components/MarkBank/WaysInPanel';
import { tariffReconciles, type SecQuestionCard } from '../types/markBank';

afterEach(cleanup);

// Synthetic interface fixture, not examination content. The source rule is
// attached separately by the subject's verified PDF selectors.
const fixture = (): SecQuestionCard => ({
  id: 'extraneous-fixture', source: 'sec', kind: 'question', subjectId: 'japanese',
  year: 2025, level: 'higher', section: 'A', paperFileid: null,
  topicId: 'japanese-1-0', conceptId: 'fixture', specVersion: 'fixture',
  questionRef: 'Synthetic response', questionText: 'Synthetic question',
  schemeCitation: 'Synthetic test fixture', totalMarks: 2, tariffModel: { kind: 'fixed' },
  rows: [
    { id: 'a', kind: 'point', verbatim: 'First fixture detail', marks: 1 },
    { id: 'b', kind: 'point', verbatim: 'Second fixture detail', marks: 1 },
  ],
  answerLanguageRule: { otherLanguageMultiplier: 0.5, sourceText: 'Synthetic language rule.', schemePages: [8] },
  extraneousMaterialRule: { multiplier: 0.5, sourceText: 'Synthetic extraneous-material rule.', schemePages: [8] },
  qa: { gates: [], humanReviewedBy: 'fixture', humanReviewedAt: '2026-11-09' },
});

describe('source-defined extraneous-material credit', () => {
  it('halves the complete priced response once when either condition applies', () => {
    const card = fixture();
    const claims = { a: 'yes' as const, b: 'yes' as const, [answerLanguageClaimId('a')]: 1 };
    expect(marksClaimed(card, claims)).toBe(1.5);
    expect(marksClaimed(card, { ...claims, [extraneousMaterialClaimId]: 1 })).toBe(1);
    expect(marksClaimed(card, { ...claims, b: 'no', [extraneousMaterialClaimId]: 1 })).toBe(0.5);
    expect(marksClaimed({ ...card, extraneousMaterialRule: undefined }, { ...claims, [extraneousMaterialClaimId]: 1 })).toBe(1.5);
    expect(marksClaimed({ ...card, answerLanguageRule: undefined }, { ...claims, [extraneousMaterialClaimId]: 1 })).toBe(1);
    expect(marksClaimed({ ...card, answerLanguageRule: { ...card.answerLanguageRule!, otherLanguageMultiplier: 0 } },
      { ...claims, [extraneousMaterialClaimId]: 1 })).toBe(0.5);
  });

  it('applies to selected source steps and parts without crediting unearned answers', () => {
    const card = fixture();
    card.rows = [{ id: 'parts', kind: 'point', verbatim: 'Paired response', marks: 2, parts: [
      { id: 'first', verbatim: 'First component', marks: 1, permittedMarks: [0, 1] },
      { id: 'second', verbatim: 'Second component', marks: 1, permittedMarks: [0, 1] },
    ] }];
    const first = partClaimId('parts', 'first');
    const claims = { [first]: 1, [answerLanguageClaimId(first)]: 1, [extraneousMaterialClaimId]: 1 };
    expect(marksClaimed(card, claims)).toBe(0.5);
    expect(marksClaimed(card, { ...claims, [first]: 2 })).toBe(0); // not a published step
    card.rows = [{ id: 'step', kind: 'point', verbatim: 'Placed response', marks: 2, permittedMarks: [0, 1, 2] }];
    expect(marksClaimed(card, { step: 1, [extraneousMaterialClaimId]: 1 })).toBe(0.5);
  });

  it('respects a finite quota and ignores stale option indices without a language rule', () => {
    const card = fixture();
    card.answerLanguageRule = undefined;
    card.rows = [{ id: 'choice', kind: 'anyN', verbatim: 'Two selected answers', marks: 2,
      group: { options: ['A', 'B', 'C'], claimMax: 2, perOption: 1 } }];
    expect(marksClaimed(card, { [extraneousMaterialClaimId]: 1 }, { choice: [1, 1, -1, 99, 2] })).toBe(1);
  });

  it('requires a source-bound half rule and rejects unsupported tariffs', () => {
    const card = fixture();
    expect(tariffReconciles(card)).toBe(true);
    expect(tariffReconciles({ ...card, extraneousMaterialRule: { ...card.extraneousMaterialRule!, sourceText: ' ' } })).toBe(false);
    expect(tariffReconciles({ ...card, extraneousMaterialRule: { ...card.extraneousMaterialRule!, schemePages: [0] } })).toBe(false);
    expect(tariffReconciles({ ...card, answerLanguageRule: undefined, tariffModel: { kind: 'questionTotal' } })).toBe(false);
  });

  it('renders the independent condition, grades its score and resets it for the next response', () => {
    const first = fixture();
    const second = { ...fixture(), id: 'next-fixture', questionText: 'Next synthetic response' };
    const onGrade = vi.fn();
    render(<SessionScreen cards={[first, second]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    fireEvent.click(screen.getByRole('button', { name: /First fixture detail/ }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'First fixture detail answered in another language' }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'Strong evidence of extraneous material in this response' }));
    expect(screen.getByText(first.extraneousMaterialRule!.sourceText)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: first.id, marksClaimed: 0.5, marksAvailable: 2 }));
    expect(screen.getByText('Next synthetic response')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.getByRole('checkbox', { name: 'Strong evidence of extraneous material in this response' })).not.toBeChecked();
  });

  it('restores the condition from a saved response and preserves the language flag when cleared', () => {
    const card = fixture();
    const response: SessionResponse = {
      claims: { a: 'yes', b: 'yes', [answerLanguageClaimId('a')]: 1, [extraneousMaterialClaimId]: 1 },
      picks: {}, rubricScores: {}, draft: '', requirementChecks: {}, answerVariantId: null, waysInWork: emptyWaysInWork(),
    };
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}
      studyReview={{ banner: null, topicTitle: () => 'Fixture', onCue: vi.fn(), onResponse: vi.fn(), revisit: true,
        responses: { [card.id]: response } }} />);
    const reveal = screen.queryByRole('button', { name: 'Reveal the marking scheme' });
    if (reveal) fireEvent.click(reveal);
    const condition = screen.getByRole('checkbox', { name: 'Strong evidence of extraneous material in this response' });
    expect(condition).toBeChecked();
    expect(marksClaimed(card, response.claims)).toBe(1);
    fireEvent.click(condition);
    expect(condition).not.toBeChecked();
    expect(screen.getByRole('checkbox', { name: 'First fixture detail answered in another language' })).toBeChecked();
    // Revisiting the recap preserves the answer without grading it again.
    fireEvent.click(screen.getByRole('button', { name: 'Back to summary' }));
    expect(onGrade).not.toHaveBeenCalled();
  });

  it('never shows the condition when no verified rule is attached', () => {
    const card = { ...fixture(), extraneousMaterialRule: undefined };
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.queryByRole('checkbox', { name: /extraneous material/ })).not.toBeInTheDocument();
  });
});
