/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a Politics and Society card. Where the scheme is cut
 * into parts (cards/politics-and-society/answers.ts) each quality band is a
 * row the student places themselves on, with the marks that band carries as
 * buttons; each exact answer is a row they claim; the points the scheme
 * lists are a visible list, labelled indicative. Where the block could not
 * be cut it shows as a list over mark buttons, never folded away.
 */
import React from 'react';
import type { PoliticsAllocation, PoliticsCriterion, PoliticsPart, PoliticsRubric, SecRubricCard } from '../../types/markBank';
import SourceMaterialReader from './SourceMaterialReader';
import { ClaimDirections, ClaimRow, MarkStrip, marksChip } from './ClaimRows';
import {
  politicsAllocationMarks,
  politicsPartMarks,
  politicsPartScoreId,
  politicsPartValue,
  politicsRowClaimed,
  politicsRowScoreId,
} from './politicsScoring';
import './politicsRubric.css';

export type PoliticsScoreId = `politics:${string}`;
export type PoliticsScores = Partial<Record<PoliticsScoreId, number>>;
export const politicsScoreId = (id: string): PoliticsScoreId => `politics:${id}`;

const NO_PRINTED_ANSWER = 'The scheme prints no answer here: any correct one earns the marks.';
const STRIP_MAX = 16;

/** Reject out-of-grid saved values instead of awarding impossible marks. */
export function politicsMarks(card: SecRubricCard, scores: PoliticsScores): number {
  if (card.rubric.system !== 'politics') return 0;
  if (card.rubric.allocation) return Math.min(card.totalMarks, politicsAllocationMarks(card.rubric.allocation, scores));
  const total = card.rubric.criteria.reduce((sum, criterion) => {
    const value = scores[politicsScoreId(criterion.id)] ?? 0;
    return sum + (criterion.permittedMarks.includes(value) ? value : 0);
  }, 0);
  return Math.min(card.totalMarks, Math.max(0, total));
}

/** The scheme's quality bands as rows: the band's words, its descriptor, and the marks it carries. */
const BandRows: React.FC<{
  bands: { label: string; marks: number[]; descriptor?: string }[];
  value: number;
  onSelect: (mark: number) => void;
}> = ({ bands, value, onSelect }) => (
  <>
    {bands.map(band => (
      <ClaimRow
        key={band.label}
        text={band.label}
        note={band.descriptor}
        steps={band.marks}
        claimed={band.marks.includes(value)}
        value={value}
        onToggle={() => undefined}
        onStep={step => onSelect(value === step ? 0 : step)}
      />
    ))}
  </>
);

const partCaption = (part: PoliticsPart): string => {
  if (part.ladder) return part.ladder.map((marks, index) => `${index + 1} right · ${marks}m`).join(' · ');
  if (part.rows && (part.count ?? 1) > 1) return `${part.count} answers · ${marksChip(part.max)}`;
  return marksChip(part.max);
};

const PartSection: React.FC<{
  part: PoliticsPart;
  scores: PoliticsScores;
  onScore: (id: PoliticsScoreId, marks: number) => void;
}> = ({ part, scores, onScore }) => {
  const claimed = (part.rows ?? []).filter(row => politicsRowClaimed(part, row.id, scores)).length;
  const full = claimed >= (part.count ?? 1);
  return (
    <section className="mb-politics-part" aria-label={part.label}>
      <div className="mb-politics-part-head">
        <h4>
          <span>{part.label}</span>
          {part.caption && <small>{part.caption}</small>}
        </h4>
        <span className="mb-claim-chip mb-politics-part-chip">{partCaption(part)}</span>
      </div>
      {part.bands && (
        <BandRows bands={part.bands} value={politicsPartValue(part, scores)} onSelect={mark => onScore(politicsPartScoreId(part.id) as PoliticsScoreId, mark)} />
      )}
      {part.rows?.map(row => {
        const id = politicsRowScoreId(part.id, row.id) as PoliticsScoreId;
        const isClaimed = politicsRowClaimed(part, row.id, scores);
        return (
          <ClaimRow
            key={row.id}
            text={row.text}
            marks={part.ladder ? undefined : row.marks}
            note={row.tariffOnly ? NO_PRINTED_ANSWER : undefined}
            claimed={isClaimed}
            disabled={full && !isClaimed}
            onToggle={() => onScore(id, isClaimed ? 0 : 1)}
          />
        );
      })}
      <div className="mb-politics-part-total">
        <span>This part</span>
        <strong>{marksChip(politicsPartMarks(part, scores))}</strong>
      </div>
    </section>
  );
};

const StructuredPanel: React.FC<{
  allocation: PoliticsAllocation;
  scores: PoliticsScores;
  onScore: (id: PoliticsScoreId, marks: number) => void;
}> = ({ allocation, scores, onScore }) => (
  <div className="mb-politics-parts">
    {allocation.examples.length > 0 && (
      <section className="mb-politics-examples" aria-label="Points the scheme lists">
        <strong>Points the scheme lists</strong>
        <ul>{allocation.examples.map((text, index) => <li key={index}>{text}</li>)}</ul>
        <small>Indicative, not a checklist: any valid point earns credit under the bands below.</small>
      </section>
    )}
    {allocation.parts.map(part => <PartSection key={part.id} part={part} scores={scores} onScore={onScore} />)}
    <ClaimDirections notes={allocation.directions} />
  </div>
);

/** The lifted block as a list when it could not be cut: bullets as items, other lines as notes. */
const GuideList: React.FC<{ blocks: readonly string[] }> = ({ blocks }) => (
  <ul className="mb-politics-guide">
    {blocks.flatMap(block => block.split('\n')).map(line => line.trim()).filter(Boolean).map((line, index) => {
      const bullet = /^[•∗]\s*(.*)$/.exec(line);
      return bullet
        ? <li key={index} className="mb-politics-guide-point"><span aria-hidden="true">•</span><span>{bullet[1]}</span></li>
        : <li key={index} className="mb-politics-guide-note">{line}</li>;
    })}
  </ul>
);

const CriterionControl: React.FC<{
  criterion: PoliticsCriterion;
  selected: number;
  onSelect: (mark: number) => void;
}> = ({ criterion, selected, onSelect }) => {
  if (criterion.bands?.length) return <BandRows bands={criterion.bands.map(band => ({ label: band.label, marks: band.marks, descriptor: band.guidance }))} value={selected} onSelect={onSelect} />;
  if (criterion.permittedMarks.length <= STRIP_MAX) return <MarkStrip label={criterion.label} marks={criterion.permittedMarks} selected={selected} onSelect={onSelect} />;
  return (
    <div className="mb-politics-slider">
      <div><span>Mark selected</span><strong>{selected}</strong></div>
      <input type="range" min={0} max={criterion.maxMarks} step={1} value={selected} aria-label={`${criterion.label} mark`} onChange={event => onSelect(Number(event.currentTarget.value))} />
      <div className="mb-politics-slider-ends"><span>0</span><span>{criterion.maxMarks}</span></div>
    </div>
  );
};

const PoliticsRubricPanel: React.FC<{
  card: SecRubricCard & { rubric: PoliticsRubric };
  scores: PoliticsScores;
  onScore: (id: PoliticsScoreId, marks: number) => void;
}> = ({ card, scores, onScore }) => {
  const { rubric } = card;
  const allocation = rubric.allocation;
  const claimable = allocation?.parts.some(part => part.rows);
  return (
    <div className="mb-politics-rubric">
      <p className="mb-politics-eyebrow">SEC Politics and Society marking scheme</p>
      <h3>{allocation ? (claimable ? 'Claim your answers and place the rest on the scheme’s bands.' : 'Place your answer on the scheme’s bands.') : 'Compare your answer with the published criteria.'}</h3>
      {rubric.taskRequirements.length > 0 && <p className="mb-politics-task">{rubric.taskRequirements.join(' · ')}</p>}
      {allocation ? (
        <StructuredPanel allocation={allocation} scores={scores} onScore={onScore} />
      ) : (
        <>
          {rubric.schemeGuidance?.length ? (
            <section className="mb-politics-fallback" aria-label="Published answer guidance">
              <p className="mb-politics-caption">The published answer guidance, as the scheme prints it.</p>
              <GuideList blocks={rubric.schemeGuidance} />
            </section>
          ) : null}
          {rubric.criteria.map(criterion => {
            const value = scores[politicsScoreId(criterion.id)] ?? 0;
            const selected = criterion.permittedMarks.includes(value) ? value : 0;
            return (
              <section key={criterion.id} className="mb-politics-criterion">
                <div className="mb-politics-criterion-heading">
                  <h4>{criterion.label}</h4>
                  <span className="mb-claim-chip">{marksChip(selected)} of {marksChip(criterion.maxMarks)}</span>
                </div>
                {criterion.guidance.map((text, index) => <p key={index} className="mb-politics-guidance">{text}</p>)}
                <CriterionControl criterion={criterion} selected={selected} onSelect={mark => onScore(politicsScoreId(criterion.id), mark)} />
              </section>
            );
          })}
        </>
      )}
      <div className="mb-politics-total" aria-live="polite">
        <span>Your placement</span><strong>{politicsMarks(card, scores)} / {card.totalMarks}</strong>
      </div>
      <p className="mb-politics-note">{rubric.markingGuideNote}</p>
      <SourceMaterialReader
        subjectId={card.subjectId}
        year={card.year}
        paperFileid={rubric.schemeFileid}
        documentKind="scheme"
        source={{
          kind: 'source-data', label: 'the official scheme', title: card.questionRef,
          pages: rubric.schemePages,
          attribution: '© State Examinations Commission',
          presentationNote: 'Original marking guidance, including the published allocations and descriptor tables.',
        }}
      />
    </div>
  );
};

export default PoliticsRubricPanel;
