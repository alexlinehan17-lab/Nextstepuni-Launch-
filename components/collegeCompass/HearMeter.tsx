/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * HearMeter — interactive HEAR eligibility self-check. Income is a hard gate
 * the meter stays locked behind; the four scored indicators fill it toward
 * Eligible (2.5) and Priority (5.5). Estimate only — always says so.
 */
import React from 'react';
import { Lock, Check } from 'lucide-react';
import { COLORS } from '../../design/tokens';
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
  const fillColor = outcome === 'not-eligible' ? COLORS.accent : COLORS.success;

  const outcomeText =
    outcome === 'priority'
      ? 'This points to HEAR Priority'
      : outcome === 'eligible'
        ? 'This points to HEAR Eligible'
        : incomeGateMet
          ? 'Not quite — but worth a chat with your guidance counsellor'
          : 'Income is the key indicator — tick it to see your score';

  return (
    <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-5">
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500 mb-1">
        Self-check
      </p>
      <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white mb-3">
        Could I qualify for HEAR?
      </h4>

      {/* Income gate */}
      <button
        type="button"
        onClick={() => toggle(incomeInd.id)}
        className="w-full text-left rounded-xl border-2 p-3 mb-3 transition-colors"
        style={{
          borderColor: incomeGateMet ? COLORS.success : COLORS.border,
          backgroundColor: incomeGateMet ? COLORS.successTint : '#FFFFFF',
        }}
      >
        <div className="flex items-start gap-3">
          <span
            className="mt-0.5 inline-flex items-center justify-center w-5 h-5 rounded-md shrink-0"
            style={{ backgroundColor: incomeGateMet ? COLORS.success : '#E7E5E2' }}
          >
            {incomeGateMet ? <Check size={13} className="text-white" /> : <Lock size={11} className="text-zinc-500" />}
          </span>
          <div className="min-w-0">
            <p className="text-sm font-bold text-[#1A1A1A]">
              {incomeInd.label} <span className="text-[10px] font-bold uppercase tracking-wide" style={{ color: COLORS.accentDarkText }}>· required</span>
            </p>
            <p className="text-xs text-[#7a7068] leading-relaxed mt-0.5">{incomeInd.detail}</p>
          </div>
        </div>
      </button>

      {/* Scored indicators */}
      <div className="space-y-2 mb-4">
        {scored.map(ind => {
          const on = selected.includes(ind.id);
          return (
            <button
              key={ind.id}
              type="button"
              onClick={() => toggle(ind.id)}
              className="w-full text-left rounded-xl border-2 p-3 transition-colors"
              style={{
                borderColor: on ? COLORS.accent : COLORS.border,
                backgroundColor: on ? COLORS.accentTint : '#FFFFFF',
              }}
            >
              <div className="flex items-start gap-3">
                <span
                  className="mt-0.5 inline-flex items-center justify-center w-5 h-5 rounded-md shrink-0 text-[11px] font-bold"
                  style={{ backgroundColor: on ? COLORS.accent : '#F0EEEB', color: on ? '#FFFFFF' : '#9e9186' }}
                >
                  {on ? <Check size={13} /> : `+${ind.points}`}
                </span>
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-[#1A1A1A]">{ind.label}</p>
                  <p className="text-xs text-[#7a7068] leading-relaxed mt-0.5">{ind.detail}</p>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Meter */}
      <div className="mb-2 flex items-baseline justify-between">
        <span className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400">Indicator score</span>
        <span className="font-mono text-sm font-bold" style={{ color: incomeGateMet ? fillColor : '#9e9186' }}>
          {score} / {HEAR_THRESHOLDS.max}
        </span>
      </div>
      <div className="relative h-4 rounded-full overflow-hidden" style={{ backgroundColor: '#E7E5E2' }}>
        {incomeGateMet ? (
          <div
            className="absolute inset-y-0 left-0 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${pct}%`, backgroundColor: fillColor }}
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center gap-1.5">
            <Lock size={11} className="text-zinc-400" />
            <span className="text-[10px] font-semibold text-zinc-400">Locked until income is met</span>
          </div>
        )}
        {/* threshold markers */}
        <div className="absolute inset-y-0 w-px bg-black/25" style={{ left: `${eligiblePct}%` }} />
        <div className="absolute inset-y-0 w-px bg-black/25" style={{ left: `${priorityPct}%` }} />
      </div>
      <div className="relative h-4 mt-1 text-[9px] font-semibold text-zinc-400">
        <span className="absolute -translate-x-1/2" style={{ left: `${eligiblePct}%` }}>Eligible</span>
        <span className="absolute -translate-x-1/2" style={{ left: `${priorityPct}%` }}>Priority</span>
      </div>

      {/* Outcome */}
      <div
        className="mt-3 rounded-xl px-4 py-3 text-center"
        style={{
          backgroundColor: outcome === 'not-eligible' ? '#F9F9F7' : COLORS.successTint,
        }}
      >
        <p
          className="text-sm font-bold"
          style={{ color: outcome === 'not-eligible' ? '#1A1A1A' : COLORS.successDarkText }}
        >
          {outcomeText}
        </p>
      </div>

      {/* Priority groups note */}
      <p className="text-[11px] text-[#7a7068] leading-relaxed mt-3">
        <span className="font-semibold text-[#1A1A1A]">Automatic priority</span> if any apply: {HEAR_PRIORITY_GROUPS.join('; ')}.
      </p>

      {/* Verify callout — sanctioned left-border */}
      <div className="mt-3 pl-3 py-1" style={{ borderLeft: `3px solid ${COLORS.accent}` }}>
        <p className="text-xs italic leading-relaxed" style={{ color: COLORS.accentDarkText }}>
          An estimate, not a decision. Point values and the income limit change yearly — confirm on{' '}
          <a href="https://accesscollege.ie/hear/" target="_blank" rel="noreferrer" className="underline font-semibold">accesscollege.ie</a>.
        </p>
      </div>
    </div>
  );
};

export default HearMeter;
