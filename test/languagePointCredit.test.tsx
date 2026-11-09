import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen, { answerLanguageClaimId, marksClaimed, partClaimId, type SessionResponse } from '../components/MarkBank/SessionScreen';
import { emptyWaysInWork } from '../components/MarkBank/WaysInPanel';
import { REVIEWED_CARDS as JAPANESE_REVIEWED } from '../components/MarkBank/cards/japanese/reviewed';
import type { SecQuestionCard } from '../types/markBank';

afterEach(cleanup);

// Synthetic interface fixtures: these are not authored examination content.
const fixture = (multiplier: 0 | 0.5 = 0.5): SecQuestionCard => ({
  id: 'language-credit-fixture', source: 'sec', kind: 'question', subjectId: 'japanese',
  year: 2026, level: 'higher', section: 'A', paperFileid: null,
  topicId: 'japanese-1-0', conceptId: 'fixture', specVersion: 'fixture',
  questionRef: 'Synthetic language fixture', questionText: 'Synthetic question',
  schemeCitation: 'Synthetic test fixture', totalMarks: 4, tariffModel: { kind: 'fixed' },
  rows: [
    { id: 'plain', kind: 'point', verbatim: 'First fixture answer', marks: 1 },
    { id: 'stepped', kind: 'point', verbatim: 'Second fixture answer', marks: 3, permittedMarks: [0, 1, 3] },
  ],
  answerLanguageRule: { otherLanguageMultiplier: multiplier, sourceText: 'Synthetic source language rule.', schemePages: [3] },
  qa: { gates: [], humanReviewedBy: 'fixture', humanReviewedAt: '2026-11-06' },
});

describe('source-defined language credit on point answers', () => {
  it('labels and grades only the named response-language condition from the source', () => {
    const card = fixture();
    card.answerLanguageRule = { ...card.answerLanguageRule!, penalizedLanguage: 'English' };
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    fireEvent.click(screen.getByRole('button', { name: /First fixture answer/ }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'First fixture answer answered in English' }));
    expect(screen.queryByRole('checkbox', { name: /answered in another language/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ marksClaimed: 0.5 }));
  });

  it('grades the actual Japanese two-reason task without inventing model answers', () => {
    const card = JAPANESE_REVIEWED.find(candidate => candidate.id === 'ja-2026-ol-2d');
    if (!card || card.kind !== 'question' || !card.rows[0].parts) throw new Error('Missing reviewed two-reason task');
    const row = card.rows[0];
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    for (const part of row.parts!) {
      fireEvent.click(screen.getByRole('button', { name: `Award 2 marks for ${part.verbatim} · ${row.verbatim}` }));
    }
    fireEvent.click(screen.getByRole('checkbox', { name: `${row.parts![0].verbatim} · ${row.verbatim} answered in another language` }));
    expect(screen.getByText('(any 2 points, 2 marks each)')).toBeInTheDocument();
    expect(screen.queryByRole('checkbox', { name: /extraneous material/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: card.id, marksClaimed: 3, marksAvailable: 4 }));
  });

  it('adjusts only the named earned answer, keeping half marks and the published steps', () => {
    const card = fixture();
    const claims = { plain: 'yes' as const, stepped: 1, [answerLanguageClaimId('stepped')]: 1 };
    expect(marksClaimed(card, claims)).toBe(1.5);
    expect(marksClaimed(card, { ...claims, stepped: 2 })).toBe(1); // not a source step
    expect(marksClaimed(card, { ...claims, [answerLanguageClaimId('plain')]: 1 })).toBe(1);
    expect(marksClaimed(card, { ...claims, stepped: 0 })).toBe(1);
    expect(marksClaimed({ ...card, answerLanguageRule: undefined }, claims)).toBe(2);
    expect(marksClaimed(fixture(0), claims)).toBe(1);
  });

  it('keeps separately placed components independent', () => {
    const card = fixture();
    card.rows = [{ id: 'parts', kind: 'point', verbatim: 'Two components', marks: 3, permittedMarks: [0, 1, 2, 3],
      parts: [
        { id: 'a', verbatim: 'Component A', marks: 1, permittedMarks: [0, 1] },
        { id: 'b', verbatim: 'Component B', marks: 2, permittedMarks: [0, 2] },
      ] }];
    card.totalMarks = 3;
    const a = partClaimId('parts', 'a');
    const b = partClaimId('parts', 'b');
    expect(marksClaimed(card, { [a]: 1, [b]: 2, [answerLanguageClaimId(a)]: 1 })).toBe(2.5);
    expect(marksClaimed(card, { [a]: 0, [b]: 2, [answerLanguageClaimId(a)]: 1 })).toBe(2);
  });

  it('attaches adjustments to each selected option through descending tariffs and reselection', () => {
    const card = fixture();
    card.totalMarks = 5;
    card.rows = [{ id: 'choice', kind: 'anyN', verbatim: 'Choose two', marks: 5,
      group: { options: ['A', 'B', 'C'], claimMax: 2, perOption: 3, perOptionSteps: [3, 2] } }];
    const flags = { [answerLanguageClaimId('choice', 2)]: 1 };
    expect(marksClaimed(card, flags, { choice: [2, 0] })).toBe(3.5);
    expect(marksClaimed(card, flags, { choice: [0, 2] })).toBe(4);
    expect(marksClaimed(card, flags, { choice: [0] })).toBe(3);
    expect(marksClaimed(card, flags, { choice: [2, 2, -1, 99, 0, 1] })).toBe(3.5);
    expect(marksClaimed({ ...card, answerLanguageRule: undefined }, flags, { choice: [2, 0] })).toBe(5);
  });

  it('grades a fractional score and clears language flags when advancing to another card', () => {
    const first = fixture();
    const second = { ...fixture(), id: 'second-language-fixture', questionText: 'Next synthetic question' };
    const onGrade = vi.fn();
    render(<SessionScreen cards={[first, second]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    const language = screen.getByRole('checkbox', { name: 'First fixture answer answered in another language' });
    expect(language).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: /First fixture answer/ }));
    fireEvent.click(language);
    fireEvent.click(screen.getByRole('button', { name: 'Award 1 marks for Second fixture answer' }));
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: first.id, marksClaimed: 1.5, marksAvailable: 4 }));
    expect(screen.getByText('Next synthetic question')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.getByRole('checkbox', { name: 'First fixture answer answered in another language' })).not.toBeChecked();
  });

  it('exposes independent any-N language controls and never reduces unselected alternatives', () => {
    const card = fixture();
    card.totalMarks = 2;
    card.rows = [{ id: 'choice', kind: 'anyN', verbatim: 'Choose two', marks: 2,
      group: { options: ['Option A', 'Option B', 'Option C'], claimMax: 2, perOption: 1 } }];
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    fireEvent.click(screen.getByRole('button', { name: 'Option A' }));
    fireEvent.click(screen.getByRole('button', { name: 'Option B' }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'Option B answered in another language' }));
    expect(screen.getByRole('checkbox', { name: 'Option C answered in another language' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Shaky' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ marksClaimed: 1.5 }));
  });

  it('restores language adjustments with a saved post-study response', () => {
    const card = fixture(0);
    const response: SessionResponse = {
      claims: { plain: 'yes', stepped: 3, [answerLanguageClaimId('plain')]: 1 }, picks: {}, rubricScores: {},
      draft: '', requirementChecks: {}, answerVariantId: null, waysInWork: emptyWaysInWork(),
    };
    render(<SessionScreen cards={[card]} subjectLabel="Russian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()}
      studyReview={{ banner: null, topicTitle: () => 'Fixture', onCue: vi.fn(), onResponse: vi.fn(), revisit: true,
        responses: { [card.id]: response } }} />);
    const reveal = screen.queryByRole('button', { name: 'Reveal the marking scheme' });
    if (reveal) fireEvent.click(reveal);
    expect(screen.getByRole('checkbox', { name: 'First fixture answer answered in another language' })).toBeChecked();
    expect(screen.getAllByText(/no credit/).length).toBeGreaterThan(0);
    expect(marksClaimed(card, response.claims, response.picks)).toBe(3);
  });

  it('does not display a language adjustment without a verified rule', () => {
    const card = { ...fixture(), answerLanguageRule: undefined };
    render(<SessionScreen cards={[card]} subjectLabel="Japanese" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.queryByRole('checkbox', { name: /answered in another language/ })).not.toBeInTheDocument();
  });
});
