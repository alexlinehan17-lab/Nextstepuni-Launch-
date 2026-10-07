/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { PoliticsRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import './politicsRubric.css';

export type PoliticsScoreId = `politics:${string}`;
export type PoliticsScores = Partial<Record<PoliticsScoreId, number>>;
export const politicsScoreId = (id: string): PoliticsScoreId => `politics:${id}`;

/** Reject out-of-grid saved values instead of awarding impossible marks. */
export function politicsMarks(card: SecRubricCard, scores: PoliticsScores): number {
  if (card.rubric.system !== 'politics') return 0;
  const total = card.rubric.criteria.reduce((sum, criterion) => {
    const value = scores[politicsScoreId(criterion.id)] ?? 0;
    return sum + (criterion.permittedMarks.includes(value) ? value : 0);
  }, 0);
  return Math.min(card.totalMarks, Math.max(0, total));
}

const PoliticsRubricPanel: React.FC<{
  card: SecRubricCard & { rubric: PoliticsRubric };
  scores: PoliticsScores;
  onScore: (id: PoliticsScoreId, marks: number) => void;
}> = ({ card, scores, onScore }) => (
  <div className="mb-politics-rubric">
    <p className="mb-politics-eyebrow">SEC Politics and Society marking scheme</p>
    <h3>Compare your answer with the published criteria.</h3>
    <p>{card.rubric.markingGuideNote}</p>
    {card.rubric.taskRequirements.length > 0 && <p>{card.rubric.taskRequirements.join(' · ')}</p>}
    {card.rubric.schemeGuidance?.length ? (
      <details>
        <summary>Read the published answer guidance</summary>
        {card.rubric.schemeGuidance.map((text, index) => <p key={index} className="mb-politics-guidance">{text}</p>)}
      </details>
    ) : null}
    {card.rubric.criteria.map(criterion => {
      const value = scores[politicsScoreId(criterion.id)] ?? 0;
      const selected = criterion.permittedMarks.includes(value) ? value : 0;
      const band = criterion.bands?.find(item => item.marks.includes(selected));
      return (
        <section key={criterion.id}>
          <div className="mb-politics-criterion-heading">
            <h4>{criterion.label}</h4>
            <label>
              <span className="sr-only">{criterion.label} mark</span>
              <select
                aria-label={`${criterion.label} mark`}
                value={selected}
                onChange={event => onScore(politicsScoreId(criterion.id), Number(event.currentTarget.value))}
              >
                {criterion.permittedMarks.map(mark => <option key={mark} value={mark}>{mark} / {criterion.maxMarks}</option>)}
              </select>
            </label>
          </div>
          {criterion.guidance.map((text, index) => <p key={index} className="mb-politics-guidance">{text}</p>)}
          {band && <p className="mb-politics-selected-band"><strong>{band.label}</strong> · {band.guidance}</p>}
          {criterion.bands?.length ? (
            <details>
              <summary>View all descriptor bands</summary>
              <dl>
                {criterion.bands.map(item => (
                  <React.Fragment key={item.label}>
                    <dt>{item.label} · {item.marks[0]}–{item.marks.at(-1)} marks</dt>
                    <dd>{item.guidance}</dd>
                  </React.Fragment>
                ))}
              </dl>
            </details>
          ) : null}
        </section>
      );
    })}
    <div className="mb-politics-total" aria-live="polite">
      <span>Your placement</span><strong>{politicsMarks(card, scores)} / {card.totalMarks}</strong>
    </div>
    <SourceMaterialReader
      subjectId={card.subjectId}
      year={card.year}
      paperFileid={card.rubric.schemeFileid}
      documentKind="scheme"
      source={{
        kind: 'source-data', label: 'the official scheme', title: card.questionRef,
        pages: card.rubric.schemePages,
        attribution: '© State Examinations Commission',
        presentationNote: 'Original marking guidance, including the published allocations and descriptor tables.',
      }}
    />
  </div>
);

export default PoliticsRubricPanel;
