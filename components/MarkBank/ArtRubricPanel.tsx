/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of an Art card. A 2010–2022 component is its printed
 * rows (cards/art/answers.ts): each row, or each part its Notes cell prices,
 * is a row the student places marks on with the scheme's words and the
 * marks on it, and the component adds them up. A 2023+ criterion keeps its
 * published low / moderate / high descriptors as bands with their marks.
 * The task check above adds no marks.
 */
import React from 'react';
import type { ArtAllocationRow, ArtCriterion, ArtRubric, SecRubricCard } from '../../types/markBank';
import { ClaimPart, ClaimRow, MarkStrip, marksChip } from './ClaimRows';
import { artCriterionMarks, artMarks, artPlaced, artRowScoreId, artScoreId, type ArtScoreId, type ArtScores } from './artScoring';
import './art-rubric.css';

/** Up to this many marks a row offers step buttons; above it, a slider. */
const STEP_MAX = 15;
const STRIP_MAX = 16;
const ART_BAND_LABELS = { low: 'Low', moderate: 'Moderate', high: 'High' } as const;

interface Props {
  card: SecRubricCard & { rubric: ArtRubric };
  scores: ArtScores;
  requirementChecks: Record<number, boolean>;
  onScore: (id: ArtScoreId, marks: number) => void;
  onRequirement: (index: number) => void;
}

/** One row or part the student places marks on. */
const Placement: React.FC<{
  id: ArtScoreId; text: string; marks: number; tag?: string; note?: string; scores: ArtScores; onScore: Props['onScore'];
}> = ({ id, text, marks, tag, note, scores, onScore }) => {
  const value = artPlaced(scores[id], marks);
  if (marks <= STEP_MAX) {
    return (
      <ClaimRow
        text={text}
        tag={tag}
        note={note}
        steps={Array.from({ length: marks }, (_, index) => index + 1)}
        claimed={value > 0}
        value={value}
        onToggle={() => undefined}
        onStep={step => onScore(id, value === step ? 0 : step)}
      />
    );
  }
  return (
    <div className="mb-claim-row mb-claim-row--stepped mb-art-slider" data-claimed={value > 0}>
      <span className="mb-claim-text">
        {tag && <span className="mb-claim-tag">{tag}</span>}
        <span>{text}</span>
        {note && <small>{note}</small>}
      </span>
      <span className="mb-art-slider-control">
        <input
          type="range"
          min={0}
          max={marks}
          step={1}
          value={value}
          aria-label={`Marks for ${text}`}
          onChange={event => onScore(id, Number(event.currentTarget.value))}
        />
        <strong>{marksChip(value)}</strong>
        <span>of {marksChip(marks)}</span>
      </span>
    </div>
  );
};

/** A component's printed rows: a row with parts is a heading over them. */
const Rows: React.FC<{ criterion: ArtCriterion; rows: ArtAllocationRow[]; scores: ArtScores; onScore: Props['onScore'] }> = ({ criterion, rows, scores, onScore }) => (
  <>
    {rows.map(row => row.parts ? (
      <div className="mb-art-row" key={row.id}>
        <ClaimPart label={marksChip(row.marks)} prompt={row.text} />
        {row.parts.map(part => (
          <Placement key={part.id} id={artRowScoreId(criterion.id, row.id, part.id)} text={part.text} marks={part.marks} tag={part.tag} scores={scores} onScore={onScore} />
        ))}
        {row.note && <p className="mb-art-note">{row.note}</p>}
      </div>
    ) : (
      <Placement key={row.id} id={artRowScoreId(criterion.id, row.id)} text={row.text} marks={row.marks} note={row.note} scores={scores} onScore={onScore} />
    ))}
  </>
);

/** 2023+ descriptors: the band's published bullets over its marks. */
const Bands: React.FC<{ criterion: ArtCriterion; scores: ArtScores; onScore: Props['onScore'] }> = ({ criterion, scores, onScore }) => {
  const id = artScoreId(criterion.id);
  const placed = artPlaced(scores[id], criterion.maxMarks);
  return (
    <div className="mb-art-bands">
      {criterion.bands!.map(band => {
        const selected = band.marks.includes(placed);
        const range = band.marks.length === 1 ? `${band.marks[0]}` : `${band.marks[0]}–${band.marks[band.marks.length - 1]}`;
        return (
          <div key={band.level} className="mb-art-band" data-selected={selected}>
            <div className="mb-art-band-title">
              <strong>{ART_BAND_LABELS[band.level]}</strong>
              <span>{range} marks</span>
            </div>
            {band.lead && <p>{band.lead}</p>}
            <ul>{band.guidance.map((note, index) => <li key={`${band.level}-${index}`}>{note}</li>)}</ul>
            <MarkStrip label={criterion.label} marks={band.marks} selected={placed} onSelect={mark => onScore(id, mark)} />
          </div>
        );
      })}
    </div>
  );
};

/** A component whose printed table did not reconcile: its rows as text over the mark strip. */
const Whole: React.FC<{ criterion: ArtCriterion; scores: ArtScores; onScore: Props['onScore'] }> = ({ criterion, scores, onScore }) => {
  const id = artScoreId(criterion.id);
  const placed = artPlaced(scores[id], criterion.maxMarks);
  return (
    <>
      {criterion.guidance.length > 0 && (
        <ul className="mb-art-guidance">
          {criterion.guidance.map((row, index) => (
            <li key={`${criterion.id}-${index}`}>
              <span>{row}{criterion.rowNotes?.[index] ? ` — ${criterion.rowNotes[index]}` : ''}</span>
              {criterion.rowMarks && <span>{marksChip(criterion.rowMarks[index])}</span>}
            </li>
          ))}
        </ul>
      )}
      {criterion.permittedMarks.length <= STRIP_MAX ? (
        <MarkStrip label={criterion.label} marks={criterion.permittedMarks} selected={placed} onSelect={mark => onScore(id, mark)} />
      ) : (
        <div className="mb-claim-row mb-claim-row--stepped mb-art-slider" data-claimed={placed > 0}>
          <span className="mb-claim-text"><span>Mark selected</span></span>
          <span className="mb-art-slider-control">
            <input type="range" min={0} max={criterion.maxMarks} step={1} value={placed} aria-label={`${criterion.label} mark`} onChange={event => onScore(id, Number(event.currentTarget.value))} />
            <strong>{marksChip(placed)}</strong>
            <span>of {marksChip(criterion.maxMarks)}</span>
          </span>
        </div>
      )}
    </>
  );
};

export default function ArtRubricPanel({ card, scores, requirementChecks, onScore, onRequirement }: Props) {
  const { rubric } = card;
  const rows = rubric.criteria.some(criterion => criterion.allocation);
  return (
    <div className="mb-art-rubric">
      <div className="mb-art-check">
        <p className="mb-art-eyebrow">Task check · no marks added here</p>
        <p className="mb-art-heading">Did you answer the exact task?</p>
        <div className="mb-art-check-list">
          {rubric.taskRequirements.map((requirement, index) => {
            const checked = !!requirementChecks[index];
            return (
              <button key={`${index}-${requirement}`} type="button" className="mb-art-requirement" aria-pressed={checked} onClick={() => onRequirement(index)}>
                <span className="mb-art-tick" aria-hidden="true" />
                <span>{requirement}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div>
        <p className="mb-art-eyebrow">SEC Art marking scheme</p>
        <p className="mb-art-heading">{rows ? 'Place your marks on each printed row.' : 'Place your response on the published Art scale.'}</p>
        <div className="mb-art-criteria">
          {rubric.criteria.map(criterion => (
            <section key={criterion.id} className="mb-art-criterion" aria-label={criterion.label}>
              <div className="mb-art-criterion-title">
                <strong>{criterion.label}</strong>
                <span className="mb-claim-chip">{marksChip(artCriterionMarks(criterion, scores))} of {marksChip(criterion.maxMarks)}</span>
              </div>
              {criterion.allocation
                ? <Rows criterion={criterion} rows={criterion.allocation.rows} scores={scores} onScore={onScore} />
                : criterion.bands?.length
                  ? <Bands criterion={criterion} scores={scores} onScore={onScore} />
                  : <Whole criterion={criterion} scores={scores} onScore={onScore} />}
            </section>
          ))}
        </div>
        <div className="mb-art-total">
          <span>Your placement</span>
          <strong>{artMarks(card, scores)} / {card.totalMarks}</strong>
        </div>
      </div>

      {rubric.markingGuideNote && (
        <aside className="mb-art-scheme-note">
          <strong>From the SEC marking scheme</strong>
          <p>{rubric.markingGuideNote}</p>
        </aside>
      )}

      {rubric.practiceNotes && rubric.practiceNotes.length > 0 && (
        <section className="mb-art-practice" aria-label="NextStepUni practice notes">
          <span className="mb-art-eyebrow">NextStepUni practice notes</span>
          <p>Our guidance for using this card. Not part of the SEC marking scheme.</p>
          <ul>{rubric.practiceNotes.map((note, index) => <li key={`practice-${index}`}>{note}</li>)}</ul>
        </section>
      )}
    </div>
  );
}
