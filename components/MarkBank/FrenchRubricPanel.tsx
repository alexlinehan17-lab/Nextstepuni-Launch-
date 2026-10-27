/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a French card. Listening, reading and cloze cards whose
 * scheme is cut into rows (cards/french/answers.ts) show each priced answer as
 * a button carrying its marks; a card the parser could not cut shows its
 * lifted lines as a list over the permitted marks; writing cards place each
 * criterion on its band. The scheme's section rules sit folded under the
 * answers, where a student who wants them can open them.
 */
import React from 'react';
import type { FrenchAllocation, FrenchAnswerRow, FrenchCriterion, FrenchRubric, SecRubricCard } from '../../types/markBank';
import {
  FRENCH_ATTEMPT_ID,
  frenchMarks,
  frenchRowClaimed,
  frenchRowScoreId,
  frenchRowValue,
  frenchScoreId,
  type FrenchScoreId,
  type FrenchScores,
} from './frenchRubric';
import { ClaimDirections, ClaimPart, ClaimRow, MarkStrip } from './ClaimRows';
import './french-rubric.css';

/** A list marker on a lifted scheme line, for the fallback list only. */
const MARKER = /^[•\-–−‑*∗➢]\s*/;
/** Up to this many permitted marks are buttons; longer ladders take a slider. */
const STRIP_MAX = 16;

const answerCaption = (allocation: FrenchAllocation): string => {
  if (allocation.ladder) {
    return allocation.ladder.map((marks, index) => `${index + 1} right earns ${marks}m`).join(' · ');
  }
  if (allocation.scoring === 'higher-segment-both') {
    return 'Two details. Claim the row for each; the scheme awards the higher detail’s mark to both.';
  }
  if (allocation.count > 1) return `The task asks for ${allocation.count} details: claim up to ${allocation.count} rows.`;
  return 'Claim the row that matches what you wrote.';
};

const FrenchAnswerRows: React.FC<{
  allocation: FrenchAllocation;
  scores: FrenchScores;
  onScore: (id: FrenchScoreId, marks: number) => void;
}> = ({ allocation, scores, onScore }) => {
  const positive = allocation.rows.filter(row => row.marks >= 0);
  const deductions = allocation.rows.filter(row => row.marks < 0);
  const claimedCount = positive.filter(row => frenchRowClaimed(row, scores)).length;
  const full = claimedCount >= allocation.count;
  const groups: { part?: string; rows: FrenchAnswerRow[] }[] = [];
  for (const row of positive) {
    const last = groups[groups.length - 1];
    if (last && last.part === row.part) last.rows.push(row);
    else groups.push({ part: row.part, rows: [row] });
  }
  const renderRow = (row: FrenchAnswerRow, tone: 'full' | 'partial' | 'deduction') => {
    const id = frenchRowScoreId(row.id);
    const claimed = frenchRowClaimed(row, scores);
    const value = frenchRowValue(row, scores);
    return (
      <ClaimRow
        key={row.id}
        text={row.text}
        marks={allocation.ladder ? undefined : row.marks}
        steps={row.steps}
        claimed={claimed}
        value={value}
        tone={tone}
        disabled={tone !== 'deduction' && full && !claimed}
        onToggle={() => onScore(id, claimed ? 0 : 1)}
        onStep={step => onScore(id, value === step ? 0 : step)}
      />
    );
  };
  return (
    <div className="mb-french-answers">
      <p className="mb-french-caption">{answerCaption(allocation)}</p>
      {groups.map((group, index) => (
        <div className="mb-french-group" key={`${group.part ?? ''}-${index}`}>
          {group.part && <ClaimPart label={group.part} />}
          {group.rows.map(row => renderRow(row, row.partial ? 'partial' : 'full'))}
        </div>
      ))}
      {deductions.length > 0 && (
        <div className="mb-french-group">
          <span className="mb-claim-tag">Deductions the scheme prints</span>
          {deductions.map(row => renderRow(row, 'deduction'))}
        </div>
      )}
      <ClaimDirections notes={allocation.directions} />
    </div>
  );
};

/** The lifted lines as a list when they could not be cut into rows. */
const GuideList: React.FC<{ lines: readonly string[] }> = ({ lines }) => (
  <ul className="mb-french-guide">
    {lines.map((line, index) => {
      const marker = MARKER.exec(line);
      return marker
        ? <li key={index} className="mb-french-guide-answer"><span aria-hidden="true">{marker[0].trim()}</span><span dir="auto">{line.slice(marker[0].length)}</span></li>
        : <li key={index} className="mb-french-guide-note">{line}</li>;
    })}
  </ul>
);

const CriterionMarks: React.FC<{
  criterion: FrenchCriterion;
  selected: number;
  disabled: boolean;
  onSelect: (mark: number) => void;
}> = ({ criterion, selected, disabled, onSelect }) => {
  if (criterion.permittedMarks.length <= STRIP_MAX) {
    return <MarkStrip label={criterion.label} marks={criterion.permittedMarks} selected={selected} disabled={disabled} onSelect={onSelect} />;
  }
  return (
    <div className="mb-french-slider">
      <div>
        <span>Mark selected</span>
        <strong>{selected}</strong>
      </div>
      <input
        type="range"
        min={0}
        max={criterion.maxMarks}
        step={1}
        value={selected}
        disabled={disabled}
        aria-label={`${criterion.label} mark`}
        onChange={event => onSelect(Number(event.currentTarget.value))}
      />
      <div className="mb-french-slider-ends"><span>0</span><span>{criterion.maxMarks}</span></div>
    </div>
  );
};

export default function FrenchRubricPanel({ card, scores, onScore }: {
  card: SecRubricCard & { rubric: FrenchRubric };
  scores: FrenchScores;
  onScore: (id: FrenchScoreId, marks: number) => void;
}) {
  const { rubric } = card;
  const attempted = scores[FRENCH_ATTEMPT_ID] === 1;
  const guided = !!rubric.answerGuide?.length;
  const allocation = rubric.allocation;
  return <div className="mb-french-rubric">
    <p className="mb-french-eyebrow">SEC French marking scheme</p>
    <h3>{allocation ? 'Claim each answer you gave, as the scheme prices it.' : 'Assess your response'}</h3>
    {!guided && rubric.taskRequirements.length > 0 && <ul className="mb-french-requirements">
      {rubric.taskRequirements.map((text, index) => <li key={index}>{text}</li>)}
    </ul>}
    {allocation && <FrenchAnswerRows allocation={allocation} scores={scores} onScore={onScore} />}
    {!allocation && rubric.answerGuide && <section className="mb-french-answer-guide" aria-label="Accepted answers and partial credit">
      <p className="mb-french-caption">Accepted answers and partial credit, as the scheme prints them.</p>
      <GuideList lines={rubric.answerGuide} />
    </section>}
    {rubric.criteria.some(criterion => criterion.requiresAttempt) &&
      <button type="button" className="mb-french-attempt" aria-pressed={attempted}
        onClick={() => onScore(FRENCH_ATTEMPT_ID, attempted ? 0 : 1)}>
        {attempted ? 'Attempt recorded' : 'Confirm a communicative task was attempted'}
      </button>}
    {!allocation && rubric.criteria.map(criterion => {
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
        <div className="mb-french-score">
          <span>{criterion.label} mark</span>
          <CriterionMarks criterion={criterion} selected={selected} disabled={disabled} onSelect={mark => onScore(id, mark)} />
        </div>
      </section>;
    })}
    {guided && rubric.taskRequirements.length > 0 && <details className="mb-french-rules">
      <summary>Scheme rules for this section</summary>
      <ul>{rubric.taskRequirements.map((text, index) => <li key={index}>{text}</li>)}</ul>
    </details>}
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
