/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Accounting scheme lines as claimable rows (cards/accounting/rows.json, lifted
 * by scripts/markbank/authoring/acc_rows.py): what the factory attaches, how the
 * rows score, and how the panel offers them — or the half-mark stepper on a task
 * whose rows could not be lifted.
 */
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { accountingCardsForLevel } from '../components/MarkBank/cards/accounting/factory';
import AccountingAssessment, { accountingMarks, accountingRowScoreId, accountingScoreId } from '../components/MarkBank/AccountingAssessment';
import type { AccountingRubric, SecRubricCard } from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

type Card = SecRubricCard & { rubric: AccountingRubric };
const HIGHER = accountingCardsForLevel('higher') as Card[];
const byId = (id: string) => {
  const card = HIGHER.find(candidate => candidate.id === id);
  if (!card) throw new Error(`no card ${id}`);
  return card;
};

describe('Accounting scheme rows', () => {
  it('attaches the lifted rows to a task, figure by figure, adding up to the task', () => {
    const card = byId('acc-2023-hl-q1A(a)');
    const rows = card.rubric.rows!;
    expect(rows).toHaveLength(19);
    expect(rows[0]).toMatchObject({ id: 'r1', text: "(a) Trading Profit and Loss Account of V. Leahy for the year ended 31/12/22", marks: 1, page: 3 });
    expect(rows[1]).toMatchObject({ text: "Sales 1,848,900", marks: 3, figure: "1,848,900" });
    expect(rows.reduce((sum, row) => sum + row.marks, 0)).toBe(card.totalMarks);
  });

  it('scores the claimed rows and never above the task', () => {
    const card = byId('acc-2023-hl-q1A(a)');
    const [first, second] = card.rubric.rows!;
    expect(accountingMarks(card, {})).toBe(0);
    expect(accountingMarks(card, { [accountingRowScoreId(first.id)]: 1, [accountingRowScoreId(second.id)]: 1 })).toBe(first.marks + second.marks);
    const all = Object.fromEntries(card.rubric.rows!.map(row => [accountingRowScoreId(row.id), 1]));
    expect(accountingMarks(card, { ...all, [accountingScoreId]: 70 })).toBe(card.totalMarks);
  });

  it('keeps the half-mark stepper on a task whose rows are in the residue', () => {
    const card = HIGHER.find(candidate => !candidate.rubric.rows?.length)!;
    expect(accountingMarks(card, { [accountingScoreId]: 4.5 })).toBe(4.5);
    render(<AccountingAssessment card={card} score={4.5} onScore={() => {}} scores={{}} onClaim={() => {}} />);
    expect(screen.getByLabelText(`Your marks out of ${card.totalMarks}`)).toBeInTheDocument();
    expect(screen.queryByRole('list', { name: 'Scheme rows' })).not.toBeInTheDocument();
  });

  it('offers each priced line as a button with its marks and reports the claim', () => {
    const card = byId('acc-2023-hl-q1A(a)');
    const onClaim = vi.fn();
    render(<AccountingAssessment card={card} score={0} onScore={() => {}} scores={{}} onClaim={onClaim} />);
    const row = card.rubric.rows![1];
    fireEvent.click(screen.getByRole('button', { name: `${row.text} · ${row.marks}m` }));
    expect(onClaim).toHaveBeenCalledWith(accountingRowScoreId(row.id), 1);
    expect(screen.queryByLabelText(`Your marks out of ${card.totalMarks}`)).not.toBeInTheDocument();
  });
});
