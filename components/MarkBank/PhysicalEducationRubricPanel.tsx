/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a Physical Education card. Where a criterion's
 * guidance is cut into what the scheme prices (cards/physical-education/
 * answers.ts) each quality band is a row with its marks as buttons, each
 * answer or component is a row the student claims, and the rest of the
 * guidance is a note underneath; a criterion that could not be cut keeps
 * its guidance over plain mark buttons. The original scheme stays one tap
 * away for its diagrams and tick tables.
 */
import React from 'react';
import type { PhysicalEducationRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { ClaimRow, MarkStrip, marksChip } from './ClaimRows';
import {
  physicalEducationCriterionMarks,
  physicalEducationMarks,
  physicalEducationRowScoreId,
  physicalEducationRowValue,
  physicalEducationScoreId,
  type PhysicalEducationScoreId,
  type PhysicalEducationScores,
} from './physicalEducationScoring';
import './physical-education-rubric.css';

interface Props {
  card: SecRubricCard & { rubric: PhysicalEducationRubric };
  scores: PhysicalEducationScores;
  onScore: (id: PhysicalEducationScoreId, marks: number) => void;
}

type Criterion = PhysicalEducationRubric['criteria'][number];

const CriterionBody: React.FC<{ criterion: Criterion; scores: PhysicalEducationScores; onScore: Props['onScore'] }> = ({ criterion, scores, onScore }) => {
  const id = physicalEducationScoreId(criterion.id);
  const placed = scores[id] ?? 0;
  const allocation = criterion.allocation;
  if (!allocation) {
    return (
      <>
        {criterion.guidance.map((text, index) => <p key={index} className="mb-pe-guidance">{text}</p>)}
        <MarkStrip label={criterion.label} marks={criterion.permittedMarks} selected={criterion.permittedMarks.includes(placed) ? placed : 0} onSelect={mark => onScore(id, mark)} />
      </>
    );
  }
  const bandValue = allocation.bands?.some(band => band.marks.includes(placed)) ? placed : 0;
  return (
    <>
      {allocation.caption && <p className="mb-pe-caption">{allocation.caption}</p>}
      {allocation.rows?.map(row => {
        const rowId = physicalEducationRowScoreId(criterion.id, row.id);
        const value = physicalEducationRowValue(criterion, row, scores);
        return (
          <ClaimRow
            key={row.id}
            text={row.text}
            marks={row.marks}
            steps={row.steps}
            claimed={value > 0}
            value={value}
            onToggle={() => onScore(rowId, value > 0 ? 0 : 1)}
            onStep={step => onScore(rowId, value === step ? 0 : step)}
          />
        );
      })}
      {allocation.bands?.map(band => (
        <ClaimRow
          key={band.label}
          text={band.label}
          steps={band.marks}
          claimed={band.marks.includes(bandValue)}
          value={bandValue}
          onToggle={() => undefined}
          onStep={step => onScore(id, bandValue === step ? 0 : step)}
        />
      ))}
      {allocation.notes.length > 0 && <p className="mb-pe-notes">{allocation.notes.join(' ')}</p>}
    </>
  );
};

/** Mounted only on the revealed side of a card. Examples stay guidance and
 * never become binary checkboxes worth an invented number of marks. */
export default function PhysicalEducationRubricPanel({ card, scores, onScore }: Props) {
  const { rubric } = card;
  const schemeFileid = rubric.schemeMaterial.sourceFileid ?? card.paperFileid;
  const structured = rubric.criteria.some(criterion => criterion.allocation);
  return (
    <div className="mb-pe-rubric">
      <p className="mb-pe-eyebrow">SEC Physical Education marking scheme</p>
      <p className="mb-pe-heading">{structured ? 'Claim what you had, as the scheme prices it.' : 'Compare your response with the published criteria.'}</p>
      {schemeFileid && <SourceMaterialReader
        source={rubric.schemeMaterial}
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={schemeFileid}
      />}
      {rubric.taskRequirements.map((requirement, index) => <p key={index} className="mb-pe-requirement">{requirement}</p>)}
      {rubric.criteria.map(criterion => (
        <section className="mb-pe-criterion" key={criterion.id} aria-label={criterion.label}>
          <div className="mb-pe-criterion-title">
            <strong>{criterion.label}</strong>
            <span className="mb-claim-chip">{marksChip(physicalEducationCriterionMarks(criterion, scores))} of {marksChip(criterion.maxMarks)}</span>
          </div>
          <CriterionBody criterion={criterion} scores={scores} onScore={onScore} />
        </section>
      ))}
      <div className="mb-pe-total"><span>Your placement</span><strong>{physicalEducationMarks(card, scores)} / {card.totalMarks}</strong></div>
      <p className="mb-pe-note">{rubric.markingGuideNote}</p>
    </div>
  );
}
