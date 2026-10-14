import React from 'react';
import type { AppliedMathematicsRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';

export type AppliedMathematicsScoreId = `applied:${string}:${'credit' | 'errors' | 'slips'}`;
export type AppliedMathematicsScores = Partial<Record<AppliedMathematicsScoreId, number>>;

export function appliedMathematicsMarks(card: SecRubricCard, scores: AppliedMathematicsScores): number {
  if (card.rubric.system !== 'applied-mathematics') return 0;
  return card.rubric.allocations.reduce((total, item) => {
    const credit = scores[`applied:${item.id}:credit`] ?? 0;
    if (!item.credit.includes(credit)) return total;
    const count = (type: 'errors' | 'slips') => {
      const value = scores[`applied:${item.id}:${type}`] ?? 0;
      return Number.isFinite(value) ? Math.max(0, Math.floor(value)) : 0;
    };
    return total + Math.max(0, credit - 3 * count('errors') - count('slips'));
  }, 0);
}

const AppliedMathematicsRubricPanel: React.FC<{
  card: SecRubricCard & { rubric: AppliedMathematicsRubric };
  scores: AppliedMathematicsScores;
  onScore: (id: AppliedMathematicsScoreId, marks: number) => void;
}> = ({ card, scores, onScore }) => (
  <div className="mb-applied-scheme">
    <p>Compare your working with the official solution, including any diagrams.</p>
    <SourceMaterialReader
      source={card.rubric.solution}
      subjectId={card.subjectId}
      year={card.year}
      paperFileid={card.rubric.solution.sourceFileid ?? card.paperFileid!}
    />
    <p>{card.rubric.markingGuideNote}</p>
    {card.rubric.allocations.map(item => (
      <fieldset key={item.id}>
        <legend>{item.label} · {Math.max(...item.credit)} marks</legend>
        {item.guidance && <p>{item.guidance}</p>}
        <div className="mb-applied-credit" aria-label={`${item.label} credit`}>
          {item.credit.map(mark => (
            <button
              type="button" key={mark}
              aria-label={`Set ${item.label} to ${mark} marks`}
              aria-pressed={(scores[`applied:${item.id}:credit`] ?? 0) === mark}
              onClick={() => onScore(`applied:${item.id}:credit`, mark)}
            >{mark}</button>
          ))}
        </div>
        <div className="mb-applied-deductions">
          {(['errors', 'slips'] as const).map(type => (
            <label key={type}>
              {type === 'errors' ? 'Mathematical errors (−3 each)' : 'Slips or minor misreadings (−1 each)'}
              <input type="number" min={0} step={1}
                aria-label={`${item.label} ${type}`}
                value={scores[`applied:${item.id}:${type}`] ?? 0}
                onChange={event => onScore(`applied:${item.id}:${type}`, Math.max(0, Math.floor(Number(event.target.value) || 0)))}
              />
            </label>
          ))}
        </div>
      </fieldset>
    ))}
    <p aria-live="polite"><strong>Your mark: {appliedMathematicsMarks(card, scores)} / {card.totalMarks}</strong></p>
  </div>
);

export default AppliedMathematicsRubricPanel;
