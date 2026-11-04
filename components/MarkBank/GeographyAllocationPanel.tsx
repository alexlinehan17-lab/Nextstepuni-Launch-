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
import type { GeographyAllocationGroup, GeographyCriterion, GeographySrpAllocation } from '../../types/markBank';
import {
  geographyPooledSrps,
  geographyRowInUnit,
  geographyRowScoreId,
  geographySrpScoreId,
  type GeographyScoreId,
  type GeographyScores,
} from './geographyScoring';
import { ClaimDirections, ClaimPart, ClaimRow, marksChip } from './ClaimRows';
import './geography-allocation.css';

interface Props {
  criterion: GeographyCriterion & { allocation: NonNullable<GeographyCriterion['allocation']> };
  scores: GeographyScores;
  onScore: (id: GeographyScoreId, marks: number) => void;
}

const NO_PRINTED_ANSWER = 'The scheme prints no answer here: any correct one earns the marks.';

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
      <span className="mb-claim-text">
        <span>{label}</span>
        <small>{caption}. One SRP is one valid point that emerges from a coherent answer.</small>
      </span>
      <span className="mb-geo-counter" role="group" aria-label={`${label}: SRPs counted`}>
        <button type="button" aria-label={`One fewer SRP for ${label}`} disabled={count <= 0} onClick={() => onCount(Math.max(0, count - 1))}>−</button>
        <output aria-live="polite">{count}</output>
        <button type="button" aria-label={`One more SRP for ${label}`} disabled={!canAdd} onClick={() => onCount(Math.min(max, count + 1))}>+</button>
      </span>
      <span className="mb-claim-chip">{marksChip(count * srp.marks)}</span>
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
        const claimed = scores[id] ?? 0;
        // A row the scheme prices unalike per point ("7/6 marks graded")
        // offers this point's own price and steps.
        const { marks, steps } = geographyRowInUnit(row, unit);
        return (
          <ClaimRow
            key={id}
            text={row.text}
            marks={marks}
            steps={steps}
            claimed={claimed > 0}
            value={claimed}
            note={row.tariffOnly ? NO_PRINTED_ANSWER : undefined}
            onToggle={() => onScore(id, claimed > 0 ? 0 : marks)}
            onStep={step => onScore(id, claimed === step ? 0 : step)}
          />
        );
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
          {(group.part || group.prompt) && <ClaimPart label={group.part} prompt={group.prompt} />}
          {group.repeat
            ? Array.from({ length: group.repeat.count }, (_, index) => renderUnit(group, index + 1))
            : renderUnit(group, undefined)}
        </section>
      ))}
      <ClaimDirections notes={allocation.directions} />
    </div>
  );
}
