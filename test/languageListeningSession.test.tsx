import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import type { CardAudioMaterial, SecCard, SecQuestionCard } from '../types/markBank';

afterEach(cleanup);

// Synthetic UI fixtures, never authored examination data. Both tasks share
// one topic and recording, but have independent point/rubric assessments.
function fixtures(subjectId: 'japanese' | 'russian'): SecCard[] {
  const audioMaterial: CardAudioMaterial = {
    kind: 'source-audio', label: 'Fixture recording', title: 'UI test audio',
    playbackUrl: 'https://example.test/recording.mp3', canonicalUrl: 'https://example.test/recording.mp3',
    secFileid: 'fixture.mp3', attribution: 'Test fixture', presentationNote: 'Test fixture',
  };
  const first: SecQuestionCard = {
    id: `${subjectId}-fixture-1`, source: 'sec', kind: 'question', subjectId,
    year: 2026, level: 'higher', section: 'A', paperFileid: null,
    topicId: `${subjectId}-1-0`, conceptId: 'fixture-listening', specVersion: 'fixture',
    questionRef: 'Fixture task 1', questionText: 'First listening prompt',
    schemeCitation: 'UI test fixture', totalMarks: 2, tariffModel: { kind: 'fixed' },
    rows: [{ id: 'answer', kind: 'point', verbatim: 'Fixture answer one', marks: 2 }],
    audioMaterial, qa: { gates: [], humanReviewedBy: 'fixture', humanReviewedAt: '2026-11-06' },
  };
  return [first, {
    ...first, id: `${subjectId}-fixture-2`, kind: 'rubric',
    questionRef: 'Fixture task 2', questionText: 'Second listening prompt',
    rubric: {
      system: 'language-points', count: 1, taskRequirements: [], markingGuideNote: '',
      groups: [{ id: 'response', label: 'Second response', rows: [{ id: 'answer', text: 'Fixture answer two', marks: 2 }] }],
    },
  }];
}

describe('independently scored language listening sessions', () => {
  it.each(['japanese', 'russian'] as const)('shows and grades both %s tasks sharing a recording', subjectId => {
    const cards = fixtures(subjectId);
    const onGrade = vi.fn();
    const { baseElement } = render(<SessionScreen cards={cards} subjectLabel={subjectId}
      onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(baseElement.querySelector('audio')).toHaveAttribute('controls');
    expect(screen.getByText('First listening prompt')).toBeInTheDocument();
    expect(screen.queryByText('Second listening prompt')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    fireEvent.click(screen.getByRole('button', { name: /Fixture answer one/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenNthCalledWith(1, expect.objectContaining({ cardId: cards[0].id, marksClaimed: 2, marksAvailable: 2 }));
    expect(screen.getByText('Second listening prompt')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    const answer = screen.getByRole('button', { name: 'Fixture answer two · 2m' });
    expect(answer).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(screen.getByRole('button', { name: 'Second response' }));
    fireEvent.click(answer);
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledTimes(2);
    expect(onGrade).toHaveBeenNthCalledWith(2, expect.objectContaining({ cardId: cards[1].id, marksClaimed: 2, marksAvailable: 2 }));
  });
});
