/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The responses a Business scheme prints for a part (bus_expected.py) as rows
 * the student claims: how they map onto the card's responses and score.
 */
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import SessionScreen from '@/components/MarkBank/SessionScreen';
import { businessExpectedId, businessExpectedLayout, businessMarks, businessPoolTarget, businessResponseFill, businessResponseMarks, businessScoreId, type BusinessScores } from '@/components/MarkBank/businessRubric';
import { isRubricCard, type BusinessRubric, type SecCard, type SecRubricCard } from '@/types/markBank';
import { CARDS as BUSINESS_HIGHER } from '@/components/MarkBank/cards/business/higher';
import { CARDS as BUSINESS_ORDINARY } from '@/components/MarkBank/cards/business/ordinary';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const byId = (id: string) => {
  const card = [...BUSINESS_HIGHER, ...BUSINESS_ORDINARY].find(candidate => candidate.id === id);
  if (!card || !isRubricCard(card) || card.rubric.system !== 'business') throw new Error(`no Business rubric card ${id}`);
  return card as SecRubricCard & { rubric: BusinessRubric };
};

describe('the responses a Business scheme prints', () => {
  test('a pool: three challenges drawn from the seven the scheme lists, each claim worth one response', () => {
    const card = byId('bus-2010-ol-s2-q2d');
    const layout = businessExpectedLayout(card.rubric);
    expect(layout?.kind).toBe('pool');
    expect(card.rubric.expected!.items.map(item => item.text)).toContain('Distribution costs – far-away locations');
    expect(businessResponseMarks(card.rubric)).toEqual({ marks: 5 });
    // A claim fills the first empty response; a clear empties the last full one.
    const scores: BusinessScores = {};
    expect(businessPoolTarget(card.rubric, scores, true)).toBe(card.rubric.responses[0].id);
    for (const [id, marks] of businessResponseFill(card.rubric, card.rubric.responses[0].id, true)) scores[id] = marks;
    expect(businessMarks(card, scores)).toBe(5);
    expect(businessPoolTarget(card.rubric, scores, true)).toBe(card.rubric.responses[1].id);
    expect(businessPoolTarget(card.rubric, scores, false)).toBe(card.rubric.responses[0].id);
  });

  test('a response that names its printed answer carries that row itself', () => {
    const card = byId('bus-2011-ol-s1-q10');
    const layout = businessExpectedLayout(card.rubric);
    expect(layout?.kind).toBe('per-response');
    if (layout?.kind !== 'per-response') return;
    expect(layout.items.get(card.rubric.responses[0].id)!.text.startsWith('On-the-job training')).toBe(true);
    expect(layout.items.get(card.rubric.responses[1].id)!.text.startsWith('Off-the-job training')).toBe(true);
  });

  test('renders the printed responses as claimable rows whose claim places the response marks', () => {
    const card = byId('bus-2010-ol-s2-q2d');
    render(<SessionScreen cards={[card as SecCard]} subjectLabel="Business" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const pool = screen.getByRole('region', { name: /Scheme responses, page \d+/ });
    const first = within(pool).getByRole('button', { name: 'Distribution costs – far-away locations · 5m' });
    fireEvent.click(first);
    expect(first).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: 'Set Challenge 1 Component 1 to 3 marks' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: 'Set Challenge 1 Component 2 to 2 marks' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByText('5 / 15')).toBeInTheDocument();
    fireEvent.click(within(pool).getByRole('button', { name: 'Different customs/cultures in other countries · 5m' }));
    expect(screen.getByText('10 / 15')).toBeInTheDocument();
    // Clearing a row takes the marks off the last response still at full marks.
    fireEvent.click(first);
    expect(first).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByText('5 / 15')).toBeInTheDocument();
    // The scheme's list is a sample: another valid response is still a row.
    expect(within(pool).getByRole('button', { name: 'Another valid response · 5m' })).toBeInTheDocument();
    expect(businessExpectedId('e1')).toBe('business:expected:e1');
    expect(businessScoreId('r', 'a')).toBe('business:r:a');
  });
});
