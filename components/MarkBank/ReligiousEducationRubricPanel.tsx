/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a Religious Education card. The SEC marks every RE
 * answer on one printed band grid, so each answer is a ladder of the scheme's
 * bands, each band a row carrying its printed range, its grid descriptors and
 * one button per mark it permits. The points of reference are the scheme's
 * examples and show as an indicative list; a Note's ceiling is a row the
 * student ticks when it describes their answer.
 */
import React from 'react';
import type { ReligiousEducationRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { ClaimDirections, ClaimRow, marksChip } from './ClaimRows';
import {
  RE_UNPLACED,
  reAnswerMarks,
  reAnswerPlaced,
  reAnswerScoreId,
  reAnswerValue,
  reCeiling,
  reCeilingScoreId,
  religiousEducationRubricMarks,
  type ReligiousEducationScoreId,
  type ReligiousEducationScores,
} from './religiousEducationScoring';
import './religious-education-rubric.css';

export type { ReligiousEducationScoreId };

/** "EXCELLENT · 34 – 40" with the range held together and to its label: the
 *  label may wrap between its words ("VERY / GOOD · 28 – 33"), the printed
 *  range never does ("EXCELLENT · 34 –" / "40" at desktop width was the
 *  coordinator's nit). No-break spaces stand for the spaces and a word joiner
 *  follows each dash, so the line cannot break inside the range. */
export const bandHeading = (label: string, printed: string): string =>
  `${label}\u00a0·\u00a0${printed.trim().replace(/\s+/g, '\u00a0').replace(/([-–—])/g, '$1\u2060')}`;

export function religiousEducationMarks(card: SecRubricCard, scores: ReligiousEducationScores): number {
  if (card.rubric.system !== 'religious-education') return 0;
  return religiousEducationRubricMarks(card.rubric, scores, card.totalMarks);
}

const Ladder: React.FC<{
  rubric: ReligiousEducationRubric;
  index: number;
  scores: ReligiousEducationScores;
  onScore: (id: ReligiousEducationScoreId, marks: number) => void;
}> = ({ rubric, index, scores, onScore }) => {
  const value = reAnswerValue(rubric, scores, index);
  const placed = reAnswerPlaced(rubric, scores, index);
  const ceiling = reCeiling(rubric, scores);
  const id = reAnswerScoreId(index);
  const label = rubric.answers > 1 ? `Answer ${index + 1} of ${rubric.answers}` : 'Your answer';
  return (
    <section className="mb-re-answer" aria-label={label}>
      <div className="mb-re-answer-head">
        <h4><span>{label}</span><small>{rubric.gridHead}</small></h4>
        <span className="mb-claim-chip">{marksChip(rubric.answerMax)}</span>
      </div>
      {rubric.bands.map((band, bandIndex) => {
        const above = ceiling !== null && Math.min(...band.marks) > ceiling;
        const steps = [...band.marks].sort((a, b) => b - a);
        return (
          <div key={bandIndex} className="mb-re-band" data-above-ceiling={above}>
            <ClaimRow
              text={bandHeading(band.label, band.printed)}
              note={band.descriptor?.join(' · ')}
              steps={steps}
              disabled={above}
              claimed={placed && band.marks.includes(value)}
              value={placed ? value : RE_UNPLACED}
              onToggle={() => undefined}
              onStep={step => onScore(id, placed && value === step ? RE_UNPLACED : step)}
            />
          </div>
        );
      })}
      <div className="mb-re-answer-total">
        <span>{ceiling !== null && value > ceiling ? `This answer, held at the ceiling` : 'This answer'}</span>
        <strong>{marksChip(reAnswerMarks(rubric, scores, index))}</strong>
      </div>
    </section>
  );
};

const ReligiousEducationRubricPanel: React.FC<{
  card: SecRubricCard & { rubric: ReligiousEducationRubric };
  scores: ReligiousEducationScores;
  onScore: (id: ReligiousEducationScoreId, marks: number) => void;
}> = ({ card, scores, onScore }) => {
  const { rubric } = card;
  const ticked = scores[reCeilingScoreId] ?? 0;
  return (
    <div className="mb-re-rubric">
      <p className="mb-re-eyebrow">SEC Religious Education marking scheme</p>
      <h3>{rubric.answers > 1 ? 'Place each answer on the scheme’s bands.' : 'Place your answer on the scheme’s bands.'}</h3>
      <p className="mb-re-criteria">{rubric.criteria}</p>
      <div className="mb-re-parts">
        {rubric.points.length > 0 && (
          <section className="mb-re-points" aria-label="Points of reference the scheme lists">
            <strong>Points of reference the scheme lists</strong>
            <ul>{rubric.points.map((point, index) => <li key={index}>{point}</li>)}</ul>
            <small>
              Indicative, not a checklist{rubric.openList ? ': the scheme ends its list with “Etc.”' : ''}.
              {' '}Any valid point is placed on the bands below.
            </small>
          </section>
        )}
        {rubric.ceilings?.map((ceiling, index) => (
          <ClaimRow
            key={index}
            tag="Ceiling — tick if this describes your answer"
            text={ceiling.when}
            marks={ceiling.max}
            claimed={ticked === index + 1}
            onToggle={() => onScore(reCeilingScoreId, ticked === index + 1 ? 0 : index + 1)}
          />
        ))}
        {Array.from({ length: rubric.answers }, (_, index) => (
          <Ladder key={index} rubric={rubric} index={index} scores={scores} onScore={onScore} />
        ))}
        <ClaimDirections notes={rubric.directions} />
      </div>
      <div className="mb-re-total" aria-live="polite">
        <span>Your placement</span><strong>{religiousEducationMarks(card, scores)} / {card.totalMarks}</strong>
      </div>
      <p className="mb-re-note">{rubric.markingGuideNote}</p>
      <SourceMaterialReader
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={rubric.schemeFileid}
        documentKind="scheme"
        source={{
          kind: 'source-data', label: 'the official scheme', title: card.questionRef,
          pages: rubric.schemePages,
          attribution: '© State Examinations Commission',
          presentationNote: 'Original marking guidance, including the printed band grid.',
        }}
      />
    </div>
  );
};

export default ReligiousEducationRubricPanel;
