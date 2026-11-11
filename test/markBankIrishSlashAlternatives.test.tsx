/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Slash-joined scheme rows cut into their items (cards/irish/slashSplits.ts): each item its own option row, the items
 * one point's alternatives (a group), so the point counts once and the part scores as the joined row did.
 */
import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/irish/foundation';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { SLASH_SPLITS_APPLIED, SLASH_SPLIT_COUNT } from '../components/MarkBank/cards/irish/slashSplits';
import { irishPartMarks, irishRowScoreId } from '../components/MarkBank/irishScoring';
import IrishAllocationPanel from '../components/MarkBank/IrishAllocationPanel';
import type { IrishCriterion, SecRubricCard } from '../types/markBank';

const ALL = [...HIGHER, ...ORDINARY, ...FOUNDATION] as SecRubricCard[];
const criteria = (card: SecRubricCard): IrishCriterion[] => (card.rubric.system === 'irish' ? card.rubric.criteria : []);
const parts = ALL.flatMap(card => criteria(card).flatMap(criterion => (criterion.allocation?.parts ?? []).map(part => ({ card, criterion, part }))));

describe('slash-joined alternatives as option rows', () => {
  it('applies every reviewed split exactly once, to rows whose own items they are', () => {
    expect(SLASH_SPLIT_COUNT).toBe(113);
    expect(SLASH_SPLITS_APPLIED.size).toBe(SLASH_SPLIT_COUNT);
    const grouped = parts.flatMap(({ part }) => part.rows.filter(row => row.group));
    expect(new Set(grouped.map(row => row.group)).size).toBeGreaterThan(0);
    for (const { card, part } of parts) {
      for (const group of new Set(part.rows.filter(row => row.group).map(row => row.group))) {
        const members = part.rows.filter(row => row.group === group);
        expect(members.length, card.id).toBeGreaterThan(1);
        expect(new Set(members.map(row => row.marks)).size, card.id).toBe(1);
        expect(members.every(row => !row.text.includes('/') || row.text.includes('/go dona')), `${card.id} ${members[0].text}`).toBe(true);
      }
    }
  });

  it('counts a group once: claiming two of one point’s alternatives earns that point once', () => {
    for (const { card, criterion, part } of parts) {
      for (const group of new Set(part.rows.filter(row => row.group).map(row => row.group))) {
        const members = part.rows.filter(row => row.group === group);
        const one = { [irishRowScoreId(criterion.id, part.id, members[0].id)]: 1 };
        const both = { ...one, [irishRowScoreId(criterion.id, part.id, members[1].id)]: 1 };
        expect(irishPartMarks(criterion.id, part, both), card.id).toBe(irishPartMarks(criterion.id, part, one));
        expect(irishPartMarks(criterion.id, part, one), card.id).toBe(Math.min(part.tariff, members[0].marks));
      }
    }
  });

  it('keeps a stance with its reasons: any one stance plus the two reasons is the whole part', () => {
    const found = parts.find(({ part }) => part.rows.some(row => row.text === 'Is maith') && part.rows.some(row => row.text === 'Ní maith') && part.tariff === 9)!;
    const { criterion, part } = found;
    const id = (text: string) => irishRowScoreId(criterion.id, part.id, part.rows.find(row => row.text === text)!.id);
    // A reason priced in steps is claimed at its full printed step.
    const reasons = part.rows.filter(row => !row.group).map(row => [irishRowScoreId(criterion.id, part.id, row.id), row.steps ? row.marks : 1] as const);
    const scores = Object.fromEntries([[id('Is maith'), 1], [id('Ní maith'), 1], ...reasons]);
    expect(irishPartMarks(criterion.id, part, scores)).toBe(9);
    expect(irishPartMarks(criterion.id, part, { [id('Is maith')]: 1, [id('Ní maith')]: 1 })).toBe(1);
  });

  it('shows the alternatives together as "1 freagra", and a claimed one closes its siblings', () => {
    const card = HIGHER.find(entry => entry.id === 'irish-2010-hl-listening-a-f1')!;
    const criterion = criteria(card).find(entry => entry.allocation?.parts.some(part => part.rows.some(row => row.text === 'Ciarraíoch')))!;
    const scores: Record<string, number> = {};
    const onScore = vi.fn((key: string, marks: number) => { scores[key] = marks; });
    const { rerender } = render(<IrishAllocationPanel criterionId={criterion.id} allocation={criterion.allocation!} scores={scores} onScore={onScore} />);
    const group = screen.getByRole('group', { name: 'Any one of these: 2 marks' });
    expect(within(group).getByText('1 freagra · 2m')).toBeInTheDocument();
    expect(within(group).getAllByRole('button').map(button => button.textContent)).toEqual(
      ['Tráchtaire spóirt2m', 'Gaeilgeoir2m', 'Ciarraíoch2m', 'cuirfidh sé tús leis an oíche eolais2m']);
    fireEvent.click(within(group).getByRole('button', { name: /Gaeilgeoir/ }));
    rerender(<IrishAllocationPanel criterionId={criterion.id} allocation={criterion.allocation!} scores={{ ...scores }} onScore={onScore} />);
    expect(within(group).getByRole('button', { name: /Ciarraíoch/ })).toBeDisabled();
  });
});
