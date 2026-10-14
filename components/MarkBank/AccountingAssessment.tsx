/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { AccountingRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';

export const accountingScoreId = 'accounting:allocation' as const;

/** Half marks occur in the published non-transfer convention. Clamp persisted
 * and entered scores as well as the controls; never reward invalid values. */
export function accountingMark(maximum: number, value = 0): number {
  return Number.isFinite(value)
    ? Math.max(0, Math.min(maximum, Math.round(value * 2) / 2)) : 0;
}

const AccountingAssessment: React.FC<{
  card: SecRubricCard & { rubric: AccountingRubric };
  score: number;
  onScore: (marks: number) => void;
}> = ({ card, score, onScore }) => {
  const selected = accountingMark(card.totalMarks, score);
  const control: React.CSSProperties = {
    border: '2px solid var(--mb-ink)', borderRadius: 8,
    background: 'var(--mb-paper)', color: 'var(--mb-ink)',
    padding: '9px 14px', minHeight: 44, fontWeight: 700,
  };
  return (
    <section aria-label="Accounting assessment">
      <p style={{ fontWeight: 700, margin: '0 0 8px' }}>Compare your workings with the SEC solution.</p>
      <p style={{ color: 'var(--mb-muted)', margin: '0 0 16px', fontSize: 13 }}>
        {card.rubric.allocationNote}
      </p>
      <SourceMaterialReader source={card.rubric.solution} subjectId={card.subjectId}
        year={card.year} paperFileid={card.paperFileid!} />
      <p style={{ color: 'var(--mb-muted)', margin: '16px 0', fontSize: 13 }}>
        Use the printed marks and any calculation or transfer penalties. Record the marks
        earned for this task, including partial credit for workings.
      </p>
      <label htmlFor={`accounting-score-${card.id}`} style={{ display: 'block', fontWeight: 700, marginBottom: 8 }}>
        Your marks out of {card.totalMarks}
      </label>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button type="button" aria-label="Subtract half a mark" disabled={selected === 0}
          style={{ ...control, cursor: selected === 0 ? 'default' : 'pointer' }}
          onClick={() => onScore(accountingMark(card.totalMarks, selected - 0.5))}>−</button>
        <input id={`accounting-score-${card.id}`} type="number" inputMode="decimal"
          min={0} max={card.totalMarks} step={0.5} value={selected}
          style={{ ...control, width: 100, background: '#F26B1F', color: '#171717', textAlign: 'center' }}
          onChange={event => onScore(accountingMark(card.totalMarks, Number(event.currentTarget.value)))} />
        <button type="button" aria-label="Add half a mark" disabled={selected === card.totalMarks}
          style={{ ...control, cursor: selected === card.totalMarks ? 'default' : 'pointer' }}
          onClick={() => onScore(accountingMark(card.totalMarks, selected + 0.5))}>+</button>
      </div>
    </section>
  );
};

export default AccountingAssessment;
