/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * HearMeter — interactive HEAR eligibility self-check. Income is a hard gate
 * the meter stays locked behind; the four scored indicators fill it toward
 * Eligible (2.5) and Priority (5.5). Estimate only — always says so.
 */
import React from 'react';
import { Check, Lock } from 'lucide-react';
import { ChoiceTile } from '../ui/Choice';
import {
  HEAR_INDICATORS,
  HEAR_THRESHOLDS,
  HEAR_PRIORITY_GROUPS,
  computeHearScore,
} from '../../collegeCompassData';

interface HearMeterProps {
  selected: string[];
  onChange: (ids: string[]) => void;
}

/** The HEAR self-check on its own screen (area 7a; board c-tools1-compass): the meter pinned under
 *  the title with Eligible and Priority marked and the score "3.5 / 7"; each indicator a choice row
 *  with the drawn mark. The arithmetic is computeHearScore's, unchanged. */
const HearMeter: React.FC<HearMeterProps> = ({ selected, onChange }) => {
  const { score, incomeGateMet, outcome } = computeHearScore(selected);
  const incomeInd = HEAR_INDICATORS.find(i => i.isIncomeGate)!;
  const scored = HEAR_INDICATORS.filter(i => !i.isIncomeGate);

  const toggle = (id: string) => {
    onChange(selected.includes(id) ? selected.filter(x => x !== id) : [...selected, id]);
  };

  const pct = Math.min(100, (score / HEAR_THRESHOLDS.max) * 100);
  const eligiblePct = (HEAR_THRESHOLDS.eligible / HEAR_THRESHOLDS.max) * 100;
  const priorityPct = (HEAR_THRESHOLDS.priority / HEAR_THRESHOLDS.max) * 100;

  const outcomeText =
    outcome === 'priority'
      ? 'This points to HEAR Priority'
      : outcome === 'eligible'
        ? 'This points to HEAR Eligible'
        : incomeGateMet
          ? 'Not quite — but worth a chat with your guidance counsellor'
          : 'Income is the key indicator — tick it to see your score';

  return (
    <div className="cc7-hear-body">
      <div className="cc7-meter" aria-live="polite">
        <div className="cc7-mrow">
          <p className="t-label cc7-label">Indicator score</p>
          <p className="cc7-mscore"><b>{score}</b><span className="cc7-of"> / {HEAR_THRESHOLDS.max}</span></p>
        </div>
        <div className="cc7-mtrack" data-ok={outcome !== 'not-eligible' || undefined}>
          {incomeGateMet ? <i style={{ width: `${pct}%` }} /> : null}
          <span className="cc7-mtick" style={{ left: `${eligiblePct}%` }} />
          <span className="cc7-mtick" style={{ left: `${priorityPct}%` }} />
        </div>
        <div className="cc7-mkey t-meta"><span style={{ left: `${eligiblePct}%` }}>Eligible</span><span style={{ left: `${priorityPct}%` }}>Priority</span></div>
        {incomeGateMet ? null : <p className="cc7-locked t-meta"><Lock size={12} aria-hidden="true" /> Locked until income is met</p>}
        <p className="cc7-outcome" data-ok={outcome !== 'not-eligible' || undefined}>{outcome !== 'not-eligible' ? <Check size={16} aria-hidden="true" /> : null}<span>{outcomeText}</span></p>
      </div>

      <div className="cc7-hlist" role="group" aria-label="HEAR indicators">
        <ChoiceTile kind="several" className="cc7-hopt" chosen={incomeGateMet} onClick={() => toggle(incomeInd.id)}
          label={<span className="cc7-hopt-in"><span className="cc7-hpts" aria-hidden="true"><Lock size={14} /></span><span className="cc7-hopt-copy"><span className="cc7-hopt-title">{incomeInd.label}</span><span className="t-meta">Required. {incomeInd.detail}</span></span></span>} />
        {scored.map(ind => (
          <ChoiceTile key={ind.id} kind="several" className="cc7-hopt" chosen={selected.includes(ind.id)} onClick={() => toggle(ind.id)}
            label={<span className="cc7-hopt-in"><span className="cc7-hpts t-readout">+{ind.points}</span><span className="cc7-hopt-copy"><span className="cc7-hopt-title">{ind.label}</span><span className="t-meta">{ind.detail}</span></span></span>} />
        ))}
      </div>

      <p className="t-meta"><b className="cc7-strong">Automatic priority</b> if any apply: {HEAR_PRIORITY_GROUPS.join('; ')}.</p>
      <p className="t-meta">An estimate, not a decision. Point values and the income limit change yearly — confirm on{' '}
        <a href="https://accesscollege.ie/hear/" target="_blank" rel="noreferrer" className="cc7-link">accesscollege.ie</a>.</p>
    </div>
  );
};

export default HearMeter;
