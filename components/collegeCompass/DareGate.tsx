/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * DareGate — interactive DARE eligibility self-check. Two gates that BOTH
 * must light green: Evidence of Disability (pick a category → reveals the
 * appropriate professional + report-age rule) AND Educational Impact (toggle
 * indicators). Estimate only.
 */
import React, { useState } from 'react';
import { Check, Stethoscope, GraduationCap, Clock } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import {
  DARE_CATEGORIES,
  DARE_IMPACT_INDICATORS,
  DARE_FORM_PARTS,
  meetsDareImpact,
} from '../../collegeCompassData';

interface DareGateProps {
  categoryId: string | undefined;
  onCategoryChange: (id: string | undefined) => void;
}

const DareGate: React.FC<DareGateProps> = ({ categoryId, onCategoryChange }) => {
  const [impact, setImpact] = useState<string[]>([]);
  const category = DARE_CATEGORIES.find(c => c.id === categoryId) ?? null;
  const isLitNum = categoryId === 'dyslexia' || categoryId === 'dyscalculia';

  const pillar1 = !!categoryId;
  const pillar2 = meetsDareImpact(impact, categoryId ?? null);
  const both = pillar1 && pillar2;

  const visibleIndicators = DARE_IMPACT_INDICATORS.filter(i => !i.literacyNumeracyOnly || isLitNum);

  const toggleImpact = (id: string) => {
    setImpact(prev => (prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]));
  };

  const GateBadge = ({ met, label }: { met: boolean; label: string }) => (
    <div
      className="flex items-center gap-2 rounded-xl border-2 px-3 py-2 flex-1"
      style={{ borderColor: met ? COLORS.success : COLORS.border, backgroundColor: met ? COLORS.successTint : '#FFFFFF' }}
    >
      <span
        className="inline-flex items-center justify-center w-5 h-5 rounded-md shrink-0"
        style={{ backgroundColor: met ? COLORS.success : '#E7E5E2' }}
      >
        {met ? <Check size={13} className="text-white" /> : <span className="block w-2 h-2 rounded-full bg-zinc-400" />}
      </span>
      <span className="text-xs font-bold" style={{ color: met ? COLORS.successDarkText : '#1A1A1A' }}>{label}</span>
    </div>
  );

  return (
    <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-5">
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500 mb-1">
        Self-check
      </p>
      <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white mb-1">
        Could I qualify for DARE?
      </h4>
      <p className="text-xs text-[#7a7068] mb-4">You need <span className="font-bold">both</span> gates — a diagnosis isn’t enough on its own.</p>

      <div className="flex gap-2 mb-4">
        <GateBadge met={pillar1} label="Evidence of disability" />
        <GateBadge met={pillar2} label="Educational impact" />
      </div>

      {/* Gate 1 — category picker */}
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2 flex items-center gap-1.5">
        <Stethoscope size={12} /> 1 · Pick the category that fits
      </p>
      <div className="flex flex-wrap gap-1.5 mb-3">
        {DARE_CATEGORIES.map(cat => {
          const on = categoryId === cat.id;
          return (
            <button
              key={cat.id}
              type="button"
              onClick={() => onCategoryChange(on ? undefined : cat.id)}
              className="text-left rounded-full border-2 px-3 py-1.5 text-xs font-semibold transition-colors"
              style={{
                borderColor: on ? COLORS.accent : COLORS.border,
                backgroundColor: on ? COLORS.accentTint : '#FFFFFF',
                color: '#1A1A1A',
              }}
            >
              {cat.name}
            </button>
          );
        })}
      </div>

      {category && (
        <div className="rounded-xl p-3 mb-4" style={{ backgroundColor: '#F9F9F7' }}>
          <p className="text-xs text-[#1A1A1A] mb-1.5 flex items-center gap-1.5">
            <Stethoscope size={13} style={{ color: COLORS.success }} />
            <span><span className="font-bold">Who confirms it:</span> {category.appropriateProfessional} — a GP alone isn’t enough.</span>
          </p>
          <p className="text-xs text-[#1A1A1A] flex items-center gap-1.5">
            <Clock size={13} style={{ color: COLORS.accent }} />
            <span>
              <span className="font-bold">Report age:</span>{' '}
              {category.reportAgeLimitYears === null
                ? 'no age limit on the diagnostic report'
                : `must be less than ${category.reportAgeLimitYears} years old`}
              {category.note ? ` — ${category.note}` : ''}
            </span>
          </p>
        </div>
      )}

      {/* Gate 2 — impact indicators */}
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2 flex items-center gap-1.5">
        <GraduationCap size={12} /> 2 · How it affected school {isLitNum ? '(need the attainment one + 1 more)' : '(pick any 2)'}
      </p>
      <div className="space-y-2 mb-4">
        {visibleIndicators.map(ind => {
          const on = impact.includes(ind.id);
          return (
            <button
              key={ind.id}
              type="button"
              onClick={() => toggleImpact(ind.id)}
              className="w-full text-left rounded-xl border-2 px-3 py-2 text-sm font-semibold transition-colors flex items-center gap-2.5"
              style={{
                borderColor: on ? COLORS.accent : COLORS.border,
                backgroundColor: on ? COLORS.accentTint : '#FFFFFF',
                color: '#1A1A1A',
              }}
            >
              <span
                className="inline-flex items-center justify-center w-5 h-5 rounded-md shrink-0"
                style={{ backgroundColor: on ? COLORS.accent : '#F0EEEB' }}
              >
                {on && <Check size={13} className="text-white" />}
              </span>
              {ind.label}
            </button>
          );
        })}
      </div>

      {/* Outcome */}
      <div
        className="rounded-xl px-4 py-3 text-center mb-4"
        style={{ backgroundColor: both ? COLORS.successTint : '#F9F9F7' }}
      >
        <p className="text-sm font-bold" style={{ color: both ? COLORS.successDarkText : '#1A1A1A' }}>
          {both
            ? 'Both gates met — this looks like a DARE case worth applying for'
            : pillar1
              ? 'Add the school-impact evidence to complete the second gate'
              : 'Pick your category to start the first gate'}
        </p>
      </div>

      {/* Who fills which form */}
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2">Who fills in what</p>
      <div className="space-y-1.5 mb-3">
        {DARE_FORM_PARTS.map(p => (
          <div key={p.id} className="flex items-baseline gap-2 text-xs">
            <span className="font-bold text-[#1A1A1A] shrink-0">{p.part}:</span>
            <span className="text-[#7a7068]">{p.who}</span>
          </div>
        ))}
      </div>

      {/* Verify callout */}
      <div className="pl-3 py-1" style={{ borderLeft: `3px solid ${COLORS.accent}` }}>
        <p className="text-xs italic leading-relaxed" style={{ color: COLORS.accentDarkText }}>
          An estimate, not a decision. Categories, professionals and report rules change yearly — confirm on{' '}
          <a href="https://accesscollege.ie/dare/" target="_blank" rel="noreferrer" className="underline font-semibold">accesscollege.ie</a>.
        </p>
      </div>
    </div>
  );
};

export default DareGate;
