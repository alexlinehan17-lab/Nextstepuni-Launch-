/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * YourPatternsContainer — stateful wrapper around the "Your patterns"
 * insights panel. Reads cross-module signals from localStorage on mount,
 * renders nothing when there are no signals, and lets the parent jump to
 * a specific knowledge module via onOpenModule.
 *
 * Used by both the Necessary Knowledge landing and the Practice flow —
 * any view where surfacing the student's interactive-session signals is
 * pedagogically useful.
 */

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { readPatterns, clearPatterns, type PatternSignals } from './knowledgePatterns';
import { TRAP_CATEGORY_LABELS, TRAP_CATEGORY_FIXES } from '../../../data/knowledge/trapCards';
import { ACCENT, ACCENT_TINT } from '../colors';

const WARN = '#A8746E';
const INK = '#1A1A1A';

export type KnowledgeModuleId =
  // Stage 1
  | 'command-words'
  | 'pclm'
  | 'time-allocation'
  | 'pet-peeves'
  | 'marking-grammar'
  // Stage 2
  | 'srp-identifier'
  | 'working-shown'
  | 'sanity-check'
  | 'spot-the-trap'
  | 'ceiling-visualiser'
  // Stage 3
  | 'comparative-linker'
  | 'rsr-allocator'
  | 'phrase-match'
  | 'oral-coach';

interface PatternInsight {
  kicker: string;
  headline: string;
  body: string;
  tone: 'ok' | 'warn';
  openModuleId?: KnowledgeModuleId;
  openModuleLabel?: string;
}

interface Props {
  onOpenModule: (id: KnowledgeModuleId) => void;
}

const YourPatternsContainer: React.FC<Props> = ({ onOpenModule }) => {
  const [patterns, setPatterns] = useState<PatternSignals>({});
  useEffect(() => {
    setPatterns(readPatterns());
  }, []);

  const handleReset = () => {
    clearPatterns();
    setPatterns({});
  };

  const insights = buildInsights(patterns);
  if (insights.length === 0) return null;

  const updatedAtMax = Math.max(
    ...[
      patterns.sanityCheck?.updatedAt ?? 0,
      patterns.spotTrap?.updatedAt ?? 0,
      patterns.comparative?.updatedAt ?? 0,
      patterns.ceiling?.updatedAt ?? 0,
    ],
  );

  return (
    <motion.section
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl"
      style={{
        backgroundColor: ACCENT_TINT,
        border: `1px solid ${ACCENT}33`,
        color: INK,
        padding: '22px 24px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 flex-wrap mb-2">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: ACCENT }}>
          Your patterns · {insights.length} signal{insights.length === 1 ? '' : 's'} from your sessions
        </p>
        <button
          type="button"
          onClick={handleReset}
          className="font-sans"
          style={{ fontSize: 11, color: ACCENT, opacity: 0.75, background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
        >
          Reset
        </button>
      </div>
      <h3 className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: INK, lineHeight: 1.35 }}>
        What this app has noticed about how you answer.
      </h3>
      <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C', marginTop: 4 }}>
        Stored on your device only. {updatedAtMax > 0 ? `Last updated ${formatRelativeTime(updatedAtMax)}.` : ''}
      </p>

      <div className="grid sm:grid-cols-2 gap-3 mt-5">
        {insights.map((ins, i) => (
          <div
            key={i}
            className="rounded-xl"
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #EDEBE8',
              padding: '14px 16px',
            }}
          >
            <p className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: ins.tone === 'ok' ? ACCENT : WARN, marginBottom: 4 }}>
              {ins.kicker}
            </p>
            <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: INK, lineHeight: 1.4 }}>
              {ins.headline}
            </p>
            <p className="font-sans" style={{ fontSize: 12, color: '#5a5550', marginTop: 6, lineHeight: 1.55 }}>
              {ins.body}
            </p>
            {ins.openModuleId && (
              <button
                type="button"
                onClick={() => onOpenModule(ins.openModuleId!)}
                className="font-sans inline-flex items-center gap-1 mt-3"
                style={{ fontSize: 11.5, fontWeight: 600, color: ACCENT, background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
              >
                {ins.openModuleLabel ?? 'Re-run tool'}
                <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
                  <path d="M4 3L7 6L4 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </button>
            )}
          </div>
        ))}
      </div>
    </motion.section>
  );
};

function buildInsights(p: PatternSignals): PatternInsight[] {
  const out: PatternInsight[] = [];

  // Sanity-check signal
  if (p.sanityCheck && p.sanityCheck.sampleSize >= 3) {
    const acc = p.sanityCheck.accuracyByCheck[p.sanityCheck.weakestCheck] ?? 0;
    const pct = Math.round(acc * 100);
    const checkLabel: Record<string, string> = {
      'order-of-magnitude': 'Order of Magnitude',
      'units': 'Units',
      'sign': 'Sign / Direction',
      'substitute-back': 'Substitute-Back',
    };
    out.push({
      kicker: 'Sanity radar',
      headline: `${checkLabel[p.sanityCheck.weakestCheck]} is your slowest check.`,
      body: `You catch this check ${pct}% of the time across ${p.sanityCheck.sampleSize} attempts. Make it your first habit on every Maths/Science calculation — before you write the final answer.`,
      tone: pct < 50 ? 'warn' : 'ok',
      openModuleId: 'sanity-check',
      openModuleLabel: 'Re-run Sanity-Check Trainer',
    });
  }

  // Trap signal
  if (p.spotTrap && p.spotTrap.sampleSize >= 5) {
    const acc = p.spotTrap.accuracyByCategory[p.spotTrap.weakestCategory] ?? 0;
    const pct = Math.round(acc * 100);
    const label = TRAP_CATEGORY_LABELS[p.spotTrap.weakestCategory as keyof typeof TRAP_CATEGORY_LABELS] ?? p.spotTrap.weakestCategory;
    const fix = TRAP_CATEGORY_FIXES[p.spotTrap.weakestCategory as keyof typeof TRAP_CATEGORY_FIXES] ?? '';
    out.push({
      kicker: 'Trap blind spot',
      headline: `${label} are your weakest category — ${pct}% caught.`,
      body: fix,
      tone: pct < 50 ? 'warn' : 'ok',
      openModuleId: 'spot-the-trap',
      openModuleLabel: 'Re-run Spot the Trap',
    });
  }

  // Comparative signal
  if (p.comparative && p.comparative.sampleSize >= 3) {
    const ratio = p.comparative.avgIntegrationRatio;
    out.push({
      kicker: 'Comparative integration',
      headline:
        ratio >= 80
          ? `Your integration ratio runs at ${ratio}% — H1 territory.`
          : ratio >= 50
          ? `Your integration ratio sits at ${ratio}%. Mid-band.`
          : `Your last comparative answer was ${ratio}% integrated.`,
      body:
        ratio >= 80
          ? 'The 2013 English CER described top answers as "analytical fashion" — you\'re reading the question the same way the marker is.'
          : ratio >= 50
          ? 'The gap is the connecting verb. "Whereas", "similarly", "in contrast to" are the load-bearing words that lift mid-band into upper.'
          : 'Most of your points are still serial. Each serial point in the bank has an integrated rewrite — that\'s the rehearsal.',
      tone: ratio >= 80 ? 'ok' : 'warn',
      openModuleId: 'comparative-linker',
      openModuleLabel: 'Re-run Comparative Linker',
    });
  }

  // Ceiling signal
  if (p.ceiling && p.ceiling.scenariosViewed >= 1) {
    const all = p.ceiling.scenariosViewed === 4;
    out.push({
      kicker: 'Cap rules seen',
      headline: all
        ? 'You\'ve walked through all four cap-rule scenarios.'
        : `${p.ceiling.scenariosViewed} of 4 cap-rule scenarios viewed.`,
      body: all
        ? 'Read the rubric for sub-task counts, named-example demands, and quotation rules before writing. Two minutes of rubric-reading defeats every ceiling on the dashboard.'
        : 'View the remaining scenarios to see all four ceilings the marking schemes can fire.',
      tone: 'ok',
      openModuleId: 'ceiling-visualiser',
      openModuleLabel: 'Open Sub-task Ceiling Visualiser',
    });
  }

  return out;
}

function formatRelativeTime(epochMs: number): string {
  const now = Date.now();
  const diffSec = Math.round((now - epochMs) / 1000);
  if (diffSec < 60) return 'just now';
  if (diffSec < 3600) return `${Math.round(diffSec / 60)} min ago`;
  if (diffSec < 86400) return `${Math.round(diffSec / 3600)} hour${diffSec >= 7200 ? 's' : ''} ago`;
  const days = Math.round(diffSec / 86400);
  return `${days} day${days === 1 ? '' : 's'} ago`;
}

export default YourPatternsContainer;
