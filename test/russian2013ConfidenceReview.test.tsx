import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen, { marksClaimed, showsRowMarks } from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import sources from '../scripts/markbank/authoring/russian-reviewed-sources.json';
import { isRubricCard } from '../types/markBank';

const sourceCard = () => {
  const card = REVIEWED_CARDS.find(card => card.id === 'ru-2013-hl-ca1');
  if (!card || isRubricCard(card)) throw new Error('Missing confidence-only cultural task');
  return card;
};
afterEach(cleanup);

describe('Russian 2013 cultural source conflict', () => {
  it('retains the complete original choice and both published allocations without priced rows', () => {
    const card = sourceCard();
    expect(card.questionText).toContain('Select two');
    expect(card.questionText).toContain('give two details');
    for (const option of ['церковь', 'Третьяковская галерея', 'Санкт-Петербург']) expect(card.questionText).toContain(option);
    expect(card.tariffModel).toEqual({ kind: 'questionTotal' });
    expect(card.totalMarks).toBe(8);
    expect(card.rows).toHaveLength(1);
    expect(card.rows[0].verbatim).toContain('Assign 1 mark for each relevant detail 2 х 2 = 4');
    expect(card.rows[0].marks).toBeNull();
    expect(card.rows[0].contextNote).toContain('not an agreed scoring maximum');
    expect(card.rows[0].contextNote).toContain('without exemplar factual answers');
    expect(card.answerLanguageRule).toBeUndefined();
    expect(showsRowMarks(card)).toBe(false);
    expect(marksClaimed(card, {}, {})).toBe(0);
    expect(marksClaimed(card, { 'published-guidance': 'yes' }, {})).toBe(0);
  });

  it('binds the original cultural identity to its own question and scheme page', () => {
    const card = sourceCard();
    expect(card.questionRef).toBe('2013 HL Section CA1');
    expect(card.sourceMaterial?.pages).toEqual([5]);
    expect(sources.find(record => record.id === card.id)).toMatchObject({
      questionRef: '2013 HL Section CA1', questionPages: [5], paperPages: [5], schemePages: [5], component: '000',
    });
  });

  it('shows the conflict and Irish allowance beside the literal guidance without a numeric claim control', async () => {
    const onGrade = vi.fn();
    render(<SessionScreen cards={[sourceCard()]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByText(/Source discrepancy: the original question paper prints 8 marks/)).toBeVisible());
    expect(screen.getByText(/The English paper column allows English or Russian; the Irish column and the scheme also allow Irish/)).toBeVisible();
    expect(screen.getAllByText(/Assign 1 mark for each relevant detail/)[0]).toBeVisible();
    expect(screen.queryByRole('button', { name: /^Claim \d+ marks/ })).not.toBeInTheDocument();
    expect(screen.queryByRole('checkbox', { name: /another language/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: 'ru-2013-hl-ca1', grade: 'got', marksClaimed: 0, marksAvailable: 0 }));
  });
});
