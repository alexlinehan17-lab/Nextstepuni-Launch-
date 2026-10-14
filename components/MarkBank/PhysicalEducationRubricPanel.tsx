/** @license SPDX-License-Identifier: Apache-2.0 */
import React from 'react';
import type { PhysicalEducationRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { physicalEducationMarks, physicalEducationScoreId, type PhysicalEducationScoreId } from './physicalEducationScoring';
import './physical-education-rubric.css';

interface Props {
  card: SecRubricCard & { rubric: PhysicalEducationRubric };
  scores: Partial<Record<PhysicalEducationScoreId, number>>;
  onScore: (id: PhysicalEducationScoreId, marks: number) => void;
}

/** Mounted only on the revealed side of a card. Examples stay guidance and
 * never become binary checkboxes worth an invented number of marks. */
export default function PhysicalEducationRubricPanel({ card, scores, onScore }: Props) {
  const { rubric } = card;
  const schemeFileid = rubric.schemeMaterial.sourceFileid ?? card.paperFileid;
  return (
    <div className="mb-pe-rubric">
      <p className="mb-pe-eyebrow">SEC Physical Education marking scheme</p>
      <p className="mb-pe-heading">Compare your response with the published criteria.</p>
      {schemeFileid && <SourceMaterialReader
        source={rubric.schemeMaterial}
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={schemeFileid}
      />}
      {rubric.taskRequirements.map((requirement, index) => <p key={index}>{requirement}</p>)}
      {rubric.criteria.map(criterion => {
        const id = physicalEducationScoreId(criterion.id);
        const selected = scores[id] ?? 0;
        return (
          <section className="mb-pe-criterion" key={id} aria-label={criterion.label}>
            <div className="mb-pe-criterion-title"><strong>{criterion.label}</strong><span>/ {criterion.maxMarks}</span></div>
            {criterion.guidance.map((text, index) => <p key={index}>{text}</p>)}
            <div className="mb-pe-scores" role="group" aria-label={`${criterion.label} marks`}>
              {criterion.permittedMarks.map(mark => <button
                key={mark}
                type="button"
                aria-pressed={selected === mark}
                aria-label={`Set ${criterion.label} to ${mark} marks`}
                onClick={() => onScore(id, mark)}
              >{mark}</button>)}
            </div>
          </section>
        );
      })}
      <div className="mb-pe-total"><span>Your placement</span><strong>{physicalEducationMarks(card, scores)} / {card.totalMarks}</strong></div>
      <p className="mb-pe-note">{rubric.markingGuideNote}</p>
    </div>
  );
}
