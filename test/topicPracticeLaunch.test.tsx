import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ReviseByTopic from '../components/PaperTrail/ReviseByTopic';
import { siblingsFor, topicsForSubject } from '../components/PaperTrail/topics';
import { queueTopicPractice, peekTopicPractice, clearTopicPractice } from '../utils/topicLaunch';
import type { TopicSibling } from '../components/PaperTrail/topics';

// Keep the real topic feed and filters; rendering PDFs belongs to the reader tests.
vi.mock('../components/PaperTrail/VaultQuestionCard', () => ({
  default: ({ sibling, onOpenInPaper }: { sibling: TopicSibling; onOpenInPaper: () => void }) =>
    <button data-paper-level={sibling.level} onClick={onOpenInPaper}>Open {sibling.year} {sibling.level} {sibling.n}</button>,
}));

beforeEach(() => { localStorage.clear(); clearTopicPractice('one'); clearTopicPractice('two'); });

describe('topic practice launch', () => {
  it('scopes the subject, topic and level suggestion to the student', () => {
    queueTopicPractice('one', 'latin', 'latin-1-1', 'ordinary');
    expect(peekTopicPractice('two')).toBeUndefined();
    expect(peekTopicPractice('one')).toEqual({ subjectId: 'latin', subtopicId: 'latin-1-1', level: 'ordinary' });
    clearTopicPractice('one');
    expect(peekTopicPractice('one')).toBeUndefined();
  });

  it('opens the requested level and keeps it through the full-paper round trip', () => {
    const topic = topicsForSubject('latin').find(item => {
      const levels = new Set(siblingsFor('latin', item.subtopicId).map(question => question.level));
      return levels.has('higher') && levels.has('ordinary');
    })!;
    expect(topic).toBeDefined();
    const onOpenQuestion = vi.fn();
    const props = { subjects: [{ id: 'latin', label: 'Latin' }], mineIds: ['latin'], uid: 'one', subjectLabel: () => 'Latin', onOpenQuestion, onBack: vi.fn() };
    const first = render(<ReviseByTopic {...props} restore={{ subjectId: 'latin', subtopicId: topic.subtopicId, level: 'ordinary' }} />);
    const cards = screen.getAllByRole('button', { name: /^Open \d/ });
    expect(cards.every(card => card.dataset.paperLevel === 'ordinary')).toBe(true);
    fireEvent.click(cards[0]);
    expect(onOpenQuestion.mock.calls[0][1]).toEqual({ subjectId: 'latin', subtopicId: topic.subtopicId, level: 'ordinary' });
    first.unmount();
    render(<ReviseByTopic {...props} restore={onOpenQuestion.mock.calls[0][1]} />);
    expect(screen.getAllByRole('button', { name: /^Open \d/ }).every(card => card.dataset.paperLevel === 'ordinary')).toBe(true);
  });
});
