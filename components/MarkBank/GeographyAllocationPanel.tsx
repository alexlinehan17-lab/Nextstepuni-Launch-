/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The revealed side of a Geography criterion whose scheme has been cut into
 * rows (cards/geography/allocation.ts). Every answer the scheme prices is a
 * button carrying its marks, like a science card's marking points; a part the
 * scheme counts in Significant Relevant Points is a counter; the examiner's
 * directions are a short list underneath, never the thing a student has to
 * read to find the answer. Where the scheme prices an answer without printing
 * one ("Tectonic plate named 3m") the row shows the scheme's own words and
 * says so: the card never carries an example the scheme did not print.
 */
import React from 'react';
import type { GeographyAllocationGroup, GeographyAnswerRow, GeographyCriterion, GeographySrpAllocation } from '../../types/markBank';
import {
  geographyPooledSrps,
  geographyRowScoreId,
  geographySrpScoreId,
  type GeographyScoreId,
  type GeographyScores,
} from './geographyScoring';
import './geography-allocation.css';

interface Props {
  criterion: GeographyCriterion & { allocation: NonNullable<GeographyCriterion['allocation']> };
  scores: GeographyScores;
  onScore: (id: GeographyScoreId, marks: number) => void;
}

const Tick: React.FC = () => (
  <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
    <path d="M2.5 6.2l2.4 2.4L9.5 3.9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const NO_PRINTED_ANSWER = 'The scheme prints no answer here: any correct one earns the marks.';

const AnswerRow: React.FC<{
  row: GeographyAnswerRow;
  claimed: number;
  onClaim: (marks: number) => void;
}> = ({ row, claimed, onClaim }) => {
  const steps = row.steps;
  const isClaimed = claimed > 0;
  if (steps) {
    return (
      <div className="mb-geo-row mb-geo-row--stepped" data-claimed={isClaimed}>
        <span className="mb-geo-row-text">
          <span dir="auto">{row.text}</span>
          {row.tariffOnly && <small>{NO_PRINTED_ANSWER}</small>}
        </span>
        <span className="mb-geo-steps" role="group" aria-label={`Marks for ${row.text}`}>
          {steps.map(step => (
            <button
              key={step}
              type="button"
              aria-pressed={claimed === step}
              aria-label={`${claimed === step ? 'Clear' : 'Claim'} ${step} marks for ${row.text}`}
              onClick={() => onClaim(claimed === step ? 0 : step)}
            >
              {step}m
            </button>
          ))}
        </span>
      </div>
    );
  }
  return (
    <button
      type="button"
      className="mb-geo-row"
      data-claimed={isClaimed}
      aria-pressed={isClaimed}
      onClick={() => onClaim(isClaimed ? 0 : row.marks)}
    >
      <span className="mb-geo-check" aria-hidden="true">{isClaimed && <Tick />}</span>
      <span className="mb-geo-row-text">
        <span dir="auto">{row.text}</span>
        {row.tariffOnly && <small>{NO_PRINTED_ANSWER}</small>}
      </span>
      <span className="mb-geo-chip">{row.marks}m</span>
    </button>
  );
};

const SrpCounter: React.FC<{
  srp: GeographySrpAllocation;
  count: number;
  /** Pooled parts: how many SRPs the pool still has for this part. */
  headroom?: number;
  onCount: (count: number) => void;
}> = ({ srp, count, headroom, onCount }) => {
  const max = srp.count;
  const canAdd = count < max && (headroom === undefined || headroom > 0);
  const caption = srp.min !== undefined && srp.min !== max
    ? `${srp.min}–${max} SRPs × ${srp.marks}m`
    : `${max} SRP${max === 1 ? '' : 's'} × ${srp.marks}m`;
  const label = srp.label || 'Significant Relevant Points';
  return (
    <div className="mb-geo-srp" data-claimed={count > 0}>
      <span className="mb-geo-row-text">
        <span>{label}</span>
        <small>{caption}. One SRP is one valid point that emerges from a coherent answer.</small>
      </span>
      <span className="mb-geo-counter" role="group" aria-label={`${label}: SRPs counted`}>
        <button type="button" aria-label={`One fewer SRP for ${label}`} disabled={count <= 0} onClick={() => onCount(Math.max(0, count - 1))}>−</button>
        <output aria-live="polite">{count}</output>
        <button type="button" aria-label={`One more SRP for ${label}`} disabled={!canAdd} onClick={() => onCount(Math.min(max, count + 1))}>+</button>
      </span>
      <span className="mb-geo-chip">{count * srp.marks}m</span>
    </div>
  );
};

export default function GeographyAllocationPanel({ criterion, scores, onScore }: Props) {
  const { allocation } = criterion;
  const pool = allocation.srpPool;
  const pooled = pool ? geographyPooledSrps(criterion, allocation, scores) : 0;

  const renderUnit = (group: GeographyAllocationGroup, unit: number | undefined) => (
    <div className="mb-geo-unit" key={unit ?? 'single'}>
      {unit !== undefined && group.repeat && (
        <span className="mb-geo-unit-label">{group.repeat.unit} · {unit} of {group.repeat.count}</span>
      )}
      {group.rows.map(row => {
        const id = geographyRowScoreId(criterion.id, row.id, unit);
        return <AnswerRow key={id} row={row} claimed={scores[id] ?? 0} onClaim={marks => onScore(id, marks)} />;
      })}
      {group.srp.map(srp => {
        const id = geographySrpScoreId(criterion.id, srp.id, unit);
        const count = scores[id] ?? 0;
        const headroom = srp.min !== undefined && pool ? pool.count - pooled : undefined;
        return <SrpCounter key={id} srp={srp} count={count} headroom={headroom} onCount={next => onScore(id, next)} />;
      })}
    </div>
  );

  return (
    <div className="mb-geo-alloc">
      {pool && (
        <p className="mb-geo-pool">
          These parts share {pool.count} SRPs between them, {pooled} counted so far.
        </p>
      )}
      {allocation.groups.map((group, index) => (
        <section className="mb-geo-group" key={`${group.part ?? ''}-${index}`} aria-label={group.prompt ?? group.part ?? `Part ${index + 1}`}>
          {(group.part || group.prompt) && (
            <h4 className="mb-geo-prompt">
              {group.part && <span className="mb-geo-part">{group.part}</span>}
              {group.prompt && <span>{group.prompt}</span>}
            </h4>
          )}
          {group.repeat
            ? Array.from({ length: group.repeat.count }, (_, index) => renderUnit(group, index + 1))
            : renderUnit(group, undefined)}
        </section>
      ))}
      {allocation.directions.length > 0 && (
        <aside className="mb-geo-directions">
          <strong>Examiner directions</strong>
          <ul>
            {allocation.directions.map((note, index) => <li key={index}>{note}</li>)}
          </ul>
        </aside>
      )}
    </div>
  );
}
