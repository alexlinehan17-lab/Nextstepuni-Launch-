/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How your points work": the CAO grid for Higher, Ordinary and Foundation,
 * opened from the grades step. Only the levels a student's subjects actually
 * offer get a column, and the grades they have picked are marked on it.
 */

import React, { useId, useMemo, useState } from 'react';
import { ArrowUpRight, Info } from 'lucide-react';
import ModalFrame from '../ui/ModalFrame';
import {
  FOUNDATION_POINTS, HIGHER_POINTS, LCVP_POINTS, ORDINARY_POINTS, lcSubjectLevels, type Level,
} from '../subjectData';
import type { SetupDraft } from './model';
import './points-guide.css';

type Column = 'higher' | 'ordinary' | 'foundation';
const COLUMNS: { level: Column; label: string; prefix: string; points: Record<string, number> }[] = [
  { level: 'higher', label: 'Higher', prefix: 'H', points: HIGHER_POINTS },
  { level: 'ordinary', label: 'Ordinary', prefix: 'O', points: ORDINARY_POINTS },
  { level: 'foundation', label: 'Foundation', prefix: 'F', points: FOUNDATION_POINTS },
];
const BAR_MAX = 100;

/** Levels worth showing for these subjects; every level before any are chosen. */
export function guideColumns(subjects: string[]): Column[] {
  if (!subjects.length) return ['higher', 'ordinary', 'foundation'];
  const offered = new Set<Level>(subjects.flatMap(lcSubjectLevels));
  const columns = COLUMNS.map(c => c.level).filter(level => offered.has(level));
  return columns.length ? columns : ['higher', 'ordinary'];
}

interface Props {
  draft: Pick<SetupDraft, 'subjects' | 'configs'>;
  /** Wording of the button. */
  label?: string;
  className?: string;
}

export default function PointsGuide({ draft, label = 'How do points work?', className = '' }: Props) {
  const [open, setOpen] = useState(false);
  const id = useId();
  const columns = useMemo(() => COLUMNS.filter(c => guideColumns(draft.subjects).includes(c.level)), [draft.subjects]);
  const current = new Set<string>();
  const target = new Set<string>();
  for (const name of draft.subjects) {
    const config = draft.configs[name];
    if (config?.current && config.current !== 'later') current.add(config.current);
    if (config?.target && config.target !== 'later') target.add(config.target);
  }
  const hasMaths = draft.subjects.includes('Mathematics');
  const hasLcvp = draft.subjects.includes('LCVP Link Modules');
  const hasFoundation = columns.some(c => c.level === 'foundation');

  return (
    <>
      <button type="button" className={`pg-trigger ${className}`} onClick={() => setOpen(true)} aria-haspopup="dialog">
        <Info size={15} aria-hidden="true" />{label}<ArrowUpRight size={14} aria-hidden="true" />
      </button>
      <ModalFrame
        open={open}
        onClose={() => setOpen(false)}
        width="lg"
        eyebrow="Leaving Cert · CAO points"
        title="Every grade is worth points."
        labelledBy={`${id}-title`}
      >
        <div className="pg">
          <p className="pg-intro">
            Colleges add up your <strong>best six subjects</strong> for a total out of <strong>625</strong>. The same grade is
            worth more at a higher level, so the level you sit matters as much as the grade.
          </p>

          <div className="pg-grid" role="table" aria-label="Points for each grade and level" style={{ ['--pg-cols' as string]: columns.length }}>
            <div className="pg-row pg-head" role="row">
              <span role="columnheader">Grade</span>
              {columns.map(c => <span role="columnheader" key={c.level}>{c.label}</span>)}
            </div>
            {Array.from({ length: 8 }, (_, index) => index + 1).map(grade => (
              <div className="pg-row" role="row" key={grade}>
                <span className="pg-grade" role="rowheader">{grade}</span>
                {columns.map(c => {
                  const code = `${c.prefix}${grade}`;
                  const points = c.points[code] ?? 0;
                  const isCurrent = current.has(code);
                  const isTarget = target.has(code);
                  return (
                    <span
                      role="cell"
                      key={c.level}
                      className="pg-cell"
                      data-level={c.level}
                      data-current={isCurrent || undefined}
                      data-target={isTarget || undefined}
                      aria-label={`${code}: ${points} points${isCurrent ? ', your current grade' : ''}${isTarget ? ', your target' : ''}`}
                    >
                      <i aria-hidden="true" style={{ width: `${Math.max(points ? 6 : 0, (points / BAR_MAX) * 100)}%` }} />
                      <b>{points}</b>
                      <small aria-hidden="true">{code}</small>
                    </span>
                  );
                })}
              </div>
            ))}
          </div>

          {(current.size > 0 || target.size > 0) && (
            <p className="pg-legend" aria-hidden="true"><span data-key="current">Your current grades</span><span data-key="target">Your targets</span></p>
          )}

          <ul className="pg-notes">
            <li><b>Same points, different level.</b> O1 and H5 are both 56. An Ordinary student aiming at Higher is aiming at more points, and that&rsquo;s fine to set as a target.</li>
            <li><b>The bottom grades score nothing.</b> H8, O7 and O8, and Foundation below F2, are worth zero points. The subject still earns study time in your plan.</li>
            {hasFoundation && <li><b>Foundation</b> is examined in Maths and Irish only. F1 is 20 points and F2 is 12, and not every college counts them.</li>}
            {hasMaths && <li><b>Higher Maths bonus.</b> H6 or better in Higher Maths earns <strong>25 extra points</strong> on top of its grade, so H1 is worth 125.</li>}
            {hasLcvp && <li><b>LCVP Link Modules</b> is graded Distinction, Merit or Pass: {LCVP_POINTS.Distinction}, {LCVP_POINTS.Merit} or {LCVP_POINTS.Pass} points, and can stand in for one of your six.</li>}
          </ul>
        </div>
      </ModalFrame>
    </>
  );
}
