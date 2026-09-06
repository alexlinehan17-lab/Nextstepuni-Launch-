import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import MobileQuestionTools from '../components/PaperTrail/MobileQuestionTools';
import type { PaperAnswerQuestion } from '../types/paperTrail';

const composition = 'Composition — choice of formats (essay / personal essay / short story / speech)';
const questions: PaperAnswerQuestion[] = Array.from({ length: 7 }, (_, i) => ({
  n: String(i + 1), label: `Composition ${i + 1}`, pP: 7, pY: [0.2 + i * 0.08, 0.26 + i * 0.08],
  region: [{ p: 12 + i }], mode: 'pagejump', conf: 1,
}));
const topicInfo = new Map(questions.map(q => [q.n, { subtopicId: 'composition', label: composition, yearsWith: 10, totalYears: 10 }]));

describe('mobile question tools', () => {
  it('retains the exact question targeted by a cross-year jump', () => {
    render(<MobileQuestionTools page={8} initialQuestion="6" questions={questions} topicInfo={topicInfo} showAnswers onAnswer={vi.fn()} onTopic={vi.fn()} />);
    expect(screen.getByRole('combobox')).toHaveValue('6');
    expect(screen.getByRole('button', { name: 'Open the marking scheme for Composition 6' })).toBeInTheDocument();
  });
  it('shows one full topic for a dense page and opens the selected question’s real scheme and topic', () => {
    const onAnswer = vi.fn(), onTopic = vi.fn();
    render(<MobileQuestionTools page={7} questions={questions} topicInfo={topicInfo} showAnswers onAnswer={onAnswer} onTopic={onTopic} />);
    expect(screen.getAllByText(composition)).toHaveLength(1);
    expect(screen.getAllByRole('option')).toHaveLength(7);
    fireEvent.change(screen.getByRole('combobox', { name: 'Question on page 7' }), { target: { value: '6' } });
    fireEvent.click(screen.getByRole('button', { name: 'Open the marking scheme for Composition 6' }));
    expect(onAnswer).toHaveBeenCalledWith(questions[5]);
    fireEvent.click(screen.getByRole('button', { name: `Explore ${composition} across years` }));
    expect(onTopic).toHaveBeenCalledWith('6');
  });
  it('switches to the new page’s question rather than keeping an old scheme selected', () => {
    const onAnswer = vi.fn(), onTopic = vi.fn();
    const view = render(<MobileQuestionTools page={7} questions={questions} showAnswers onAnswer={onAnswer} onTopic={onTopic} />);
    fireEvent.change(screen.getByRole('combobox'), { target: { value: '6' } });
    const next: PaperAnswerQuestion = { ...questions[0], n: '8', label: 'Comprehension 1', pP: 8 };
    view.rerender(<MobileQuestionTools page={8} questions={[next]} showAnswers onAnswer={onAnswer} onTopic={onTopic} />);
    expect(screen.getByRole('combobox', { name: 'Question on page 8' })).toHaveValue('8');
    fireEvent.click(screen.getByRole('button', { name: 'Open the marking scheme for Comprehension 1' }));
    expect(onAnswer).toHaveBeenCalledWith(next);
  });
  it('collapses details to leave more reading space and retains the selected question', () => {
    render(<MobileQuestionTools page={7} questions={questions} topicInfo={topicInfo} showAnswers onAnswer={vi.fn()} onTopic={vi.fn()} />);
    fireEvent.change(screen.getByRole('combobox'), { target: { value: '7' } });
    fireEvent.click(screen.getByRole('button', { name: 'Hide question details' }));
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Show question details' })).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(screen.getByRole('button', { name: 'Show question details' }));
    expect(screen.getByRole('combobox')).toHaveValue('7');
  });
  it('supports topics alone and explains pages with no mapped questions', () => {
    const props = { onAnswer: vi.fn(), onTopic: vi.fn(), showAnswers: false, topicInfo };
    const view = render(<MobileQuestionTools {...props} page={7} questions={questions} />);
    expect(screen.queryByRole('button', { name: /marking scheme/ })).not.toBeInTheDocument();
    view.rerender(<MobileQuestionTools {...props} page={1} questions={[]} />);
    expect(screen.getByText('No mapped questions on this page. Scroll to a question page.')).toBeInTheDocument();
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
  });
});
