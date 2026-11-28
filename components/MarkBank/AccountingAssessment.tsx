/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { AccountingRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { ClaimRow } from './ClaimRows';

export const accountingScoreId = 'accounting:allocation' as const;
export type AccountingScoreId = typeof accountingScoreId | `accounting:row:${string}`;
/** A claimed row of a task's lifted scheme rows (cards/accounting/rows.json): 1 when claimed. */
export const accountingRowScoreId = (rowId: string): AccountingScoreId => `accounting:row:${rowId}`;
/** Half marks occur in the published non-transfer convention. Clamp persisted
 * and entered scores as well as the controls; never reward invalid values. */
export function accountingMark(maximum: number, value = 0): number {
  return Number.isFinite(value)
    ? Math.max(0, Math.min(maximum, Math.round(value * 2) / 2)) : 0;
}
/** The task's marks: the claimed rows' marks, never above the task. A task without rows, or a session saved
 * before its rows existed (no row claimed, a stepper figure kept), keeps the stepper's figure. */
export function accountingMarks(card: SecRubricCard & { rubric: AccountingRubric }, scores: Partial<Record<string, number>>): number {
  const rows = card.rubric.rows ?? [];
  const claimed = rows.filter(row => (scores[accountingRowScoreId(row.id)] ?? 0) > 0);
  if (!claimed.length) return accountingMark(card.totalMarks, scores[accountingScoreId]);
  return Math.min(card.totalMarks, claimed.reduce((sum, row) => sum + row.marks, 0));
}
const AccountingAssessment: React.FC<{
  card: SecRubricCard & { rubric: AccountingRubric };
  score: number;
  onScore: (marks: number) => void;
  /** Row claims by score id, on a task whose scheme rows were lifted. */
  scores?: Partial<Record<string, number>>;
  onClaim?: (id: AccountingScoreId, value: number) => void;
}> = ({ card, score, onScore, scores = {}, onClaim }) => {
  const selected = accountingMark(card.totalMarks, score);
  const rows = card.rubric.rows;
  if (rows?.length && onClaim) {
    const claimed = accountingMarks(card, scores);
    return (
      <section aria-label="Accounting assessment">
        <p className="mb-scheme-title">Claim each figure the scheme prices.</p>
        <p className="mb-scheme-sub">
          The scheme’s own lines with their marks, as printed; {claimed} of {card.totalMarks} marks claimed.
        </p>
        <div role="list" aria-label="Scheme rows" className="mb-anyn-options">
          {rows.map(row => {
            const on = (scores[accountingRowScoreId(row.id)] ?? 0) > 0;
            return (
              <ClaimRow key={row.id} text={row.text} marks={row.marks} claimed={on}
                tag={row.inferred ? 'section total' : row.block ? 'block' : undefined}
                onToggle={() => onClaim(accountingRowScoreId(row.id), on ? 0 : 1)} />
            );
          })}
        </div>
        <p className="mb-scheme-sub" style={{ marginTop: 16 }}>{card.rubric.allocationNote}</p>
        <SourceMaterialReader source={card.rubric.solution} subjectId={card.subjectId}
          year={card.year} paperFileid={card.paperFileid!} />
      </section>
    );
  }
  return (
    <section aria-label="Accounting assessment">
      <p className="mb-scheme-title">Compare your workings with the SEC solution.</p>
      <p className="mb-scheme-sub">
        {card.rubric.allocationNote}
      </p>
      <SourceMaterialReader source={card.rubric.solution} subjectId={card.subjectId}
        year={card.year} paperFileid={card.paperFileid!} />
      <p className="mb-scheme-sub" style={{ marginTop: 16 }}>
        Use the printed marks and any calculation or transfer penalties. Record the marks
        earned for this task, including partial credit for workings.
      </p>
      <label htmlFor={`accounting-score-${card.id}`} style={{ display: 'block', marginBottom: 8, font: '400 15px/21px var(--font-ui)' }}>
        Your marks out of {card.totalMarks}
      </label>
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
        <button type="button" className="mb-mark-btn mb-mark-btn--step" aria-label="Subtract half a mark" disabled={selected === 0}
          onClick={() => onScore(accountingMark(card.totalMarks, selected - 0.5))}>−</button>
        <input id={`accounting-score-${card.id}`} type="number" inputMode="decimal"
          min={0} max={card.totalMarks} step={0.5} value={selected}
          className="mb-mark-field"
          onChange={event => onScore(accountingMark(card.totalMarks, Number(event.currentTarget.value)))} />
        <button type="button" className="mb-mark-btn mb-mark-btn--step" aria-label="Add half a mark" disabled={selected === card.totalMarks}
          onClick={() => onScore(accountingMark(card.totalMarks, selected + 0.5))}>+</button>
      </div>
    </section>
  );
};

export default AccountingAssessment;
