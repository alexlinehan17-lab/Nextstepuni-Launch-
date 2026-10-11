import React from 'react';
import type { FrenchRubric, SecRubricCard } from '../../types/markBank';
import { FRENCH_ATTEMPT_ID, frenchMarks, frenchScoreId, type FrenchScoreId, type FrenchScores } from './frenchRubric';
import './french-rubric.css';

export default function FrenchRubricPanel({ card, scores, onScore }: {
  card: SecRubricCard & { rubric: FrenchRubric };
  scores: FrenchScores;
  onScore: (id: FrenchScoreId, marks: number) => void;
}) {
  const { rubric } = card;
  const attempted = scores[FRENCH_ATTEMPT_ID] === 1;
  return <div className="mb-french-rubric">
    <p className="mb-french-eyebrow">SEC French marking scheme</p>
    <h3>Assess your response</h3>
    {rubric.taskRequirements.length > 0 && <ul className="mb-french-requirements">
      {rubric.taskRequirements.map((text, index) => <li key={index}>{text}</li>)}
    </ul>}
    {rubric.answerGuide && <details className="mb-french-answer-guide" open>
      <summary>Accepted answers and partial credit</summary>
      {rubric.answerGuide.map((text, index) => <p key={index}>{text}</p>)}
    </details>}
    {rubric.criteria.some(criterion => criterion.requiresAttempt) &&
      <button type="button" className="mb-french-attempt" aria-pressed={attempted}
        onClick={() => onScore(FRENCH_ATTEMPT_ID, attempted ? 0 : 1)}>
        {attempted ? 'Attempt recorded' : 'Confirm a communicative task was attempted'}
      </button>}
    {rubric.criteria.map(criterion => {
      const id = frenchScoreId(criterion.id);
      const disabled = !!criterion.requiresAttempt && !attempted;
      const selected = disabled ? 0 : scores[id] ?? 0;
      return <section key={criterion.id} className="mb-french-criterion">
        <div className="mb-french-criterion-heading"><h4>{criterion.label}</h4><span>/ {criterion.maxMarks}</span></div>
        {criterion.guidance.map((text, index) => <p key={index}>{text}</p>)}
        {disabled && <p>Language marks require an attempted communicative task.</p>}
        {criterion.bands?.map(band => <div key={band.label} className="mb-french-band">
          <strong>{band.label} · {band.marks[0]}–{band.marks.at(-1)} marks</strong>
          <ul>{band.guidance.map((text, index) => <li key={index}>{text}</li>)}</ul>
        </div>)}
        <label className="mb-french-score">{criterion.label} mark
          <select aria-label={`${criterion.label} mark`} disabled={disabled} value={selected} data-selected={selected > 0}
            onChange={event => onScore(id, Number(event.currentTarget.value))}>
            {criterion.permittedMarks.map(mark => <option key={mark} value={mark}>{mark} / {criterion.maxMarks}</option>)}
          </select>
        </label>
      </section>;
    })}
    <div className="mb-french-total"><span>Your placement</span><strong>{frenchMarks(card, scores)} / {card.totalMarks}</strong></div>
    {rubric.markingGuideNote && <p className="mb-french-note">{rubric.markingGuideNote}</p>}
    {rubric.practiceNotes && rubric.practiceNotes.length > 0 &&
      <section className="mb-french-practice" aria-label="NextStepUni practice notes">
        <p className="mb-french-eyebrow">NextStepUni practice notes</p>
        <p className="mb-french-practice-source">Our guidance for using this card. Not part of the SEC marking scheme.</p>
        <ul>{rubric.practiceNotes.map((text, index) => <li key={index}>{text}</li>)}</ul>
      </section>}
  </div>;
}
