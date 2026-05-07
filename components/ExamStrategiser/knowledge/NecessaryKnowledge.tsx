/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Necessary Knowledge — tab landing.
 *
 * Hero, three module groups (Foundations / Tools / Subject Deep Dives),
 * a "Your patterns" panel that surfaces cross-module insights from
 * localStorage signals, and a closing Chief Examiner Report quote that
 * frames the whole tab's thesis.
 *
 * Stage 1 (Foundations) modules use the quieter Strategiser register.
 * Stage 2 (Tools) and Stage 3 (Subject Deep Dives) modules use the
 * bolder Brilliant.org / Mercury hybrid register — denser and more
 * instrument-panel-like.
 *
 * Source of truth for content: /docs/leaving-cert-knowledge-dossier.md.
 * Every claim here traces to that file.
 */

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { readPatterns, clearPatterns, type PatternSignals } from './knowledgePatterns';
import { TRAP_CATEGORY_LABELS, TRAP_CATEGORY_FIXES } from '../../../data/knowledge/trapCards';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

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

type Stage = 1 | 2 | 3;

interface ModuleTile {
  id: KnowledgeModuleId;
  stage: Stage;
  title: string;
  valueProp: string;
  estimatedMinutes: number;
}

const TILES: ModuleTile[] = [
  // ─── Stage 1 ────────────────────────────────────────────────────────
  {
    id: 'command-words',
    stage: 1,
    title: 'Command Word Decoder',
    valueProp: 'Paste any LC question. See the command words, modifiers, the structural template the examiner expects, and the specific error each one catches.',
    estimatedMinutes: 8,
  },
  {
    id: 'pclm',
    stage: 1,
    title: 'PCLM Allocator',
    valueProp: 'The Purpose Ceiling rule in English caps your Coherence and Language marks at your Purpose mark. See it in action with sliders.',
    estimatedMinutes: 6,
  },
  {
    id: 'time-allocation',
    stage: 1,
    title: 'Time-Allocation Calculator',
    valueProp: 'Per-mark timing for every paper. Plus a sunk-cost simulator showing why a part-answer to all required questions beats a perfect answer to fewer.',
    estimatedMinutes: 7,
  },
  {
    id: 'pet-peeves',
    stage: 1,
    title: 'Examiner Pet-Peeve Trainer',
    valueProp: 'The same complaints every Chief Examiner Report makes, year after year. Card-stack of the perennial 12, with the fix for each.',
    estimatedMinutes: 10,
  },
  {
    id: 'marking-grammar',
    stage: 1,
    title: 'Marking-Scheme Grammar',
    valueProp: 'How each subject is actually marked: PCLM in English, SRPs in Geography, Attempt-mark/Blunder/Slip in Maths, headings in Accounting, key-phrases in Sciences.',
    estimatedMinutes: 9,
  },
  // ─── Stage 2 ────────────────────────────────────────────────────────
  {
    id: 'srp-identifier',
    stage: 2,
    title: 'SRP Identifier',
    valueProp: 'Read a real long-question paragraph like an examiner. Three phases: highlight what you think counts, see the actual classification, then watch every credited SRP draw down to a live mark counter.',
    estimatedMinutes: 12,
  },
  {
    id: 'working-shown',
    stage: 2,
    title: 'Working-Shown Allocator',
    valueProp: 'Build a Maths/Science answer step by step. Marks land as ribbons next to each step. Slips and blunders are deducted in real time. Five answer paths show what each level of "showing your work" actually scores.',
    estimatedMinutes: 14,
  },
  {
    id: 'sanity-check',
    stage: 2,
    title: 'Sanity-Check Trainer',
    valueProp: 'Four candidate answers, three absurd. Tap each wrong one and identify which check (Order of Magnitude, Units, Sign, Substitute-Back) catches it. The radar pulses around the answer in the colour of the catching check. Reaction time logged.',
    estimatedMinutes: 12,
  },
  {
    id: 'spot-the-trap',
    stage: 2,
    title: 'Spot the Trap',
    valueProp: 'Past-paper-style traps across six subjects. 30-second timer to spot the trap before the reveal. Pattern card every 5 cards shows where your blind spots cluster. Closing trap-map names your worst category.',
    estimatedMinutes: 16,
  },
  {
    id: 'ceiling-visualiser',
    stage: 2,
    title: 'Sub-task Ceiling Visualiser',
    valueProp: 'Watch a beautiful answer hit the ceiling and drop. Rewind to the exact sentence where the cap fired. See what 2 minutes on the missed sub-task would have done. Four cap-rule scenarios; closing pattern names the single habit that defeats all four.',
    estimatedMinutes: 10,
  },
  // ─── Stage 3 — subject-deep ────────────────────────────────────────
  {
    id: 'comparative-linker',
    stage: 3,
    title: 'Comparative Texts Linker',
    valueProp: 'English Comparative answers fail when paragraphs are about one text at a time. Build your answer point by point; watch each point either thread across all three texts or sit isolated. Six sample questions across all four modes.',
    estimatedMinutes: 18,
  },
  {
    id: 'rsr-allocator',
    stage: 3,
    title: 'RSR Section Allocator',
    valueProp: 'Word-budget meter for every section of the History Research Study Report against its mark weight. Source-evaluation quality checker (Origin / Purpose / Value / Limitations). Review-of-Process slop detector with prescriptions.',
    estimatedMinutes: 16,
  },
  {
    id: 'phrase-match',
    stage: 3,
    title: 'Phrase Match Petri-Dish',
    valueProp: 'Marking schemes in Sciences hunt for specific key phrases. Write your definition first; reveal the petri-dish to see which phrases lit up. 18 questions across Biology, Chemistry, Physics. Reverse mode lets you build the model paragraph from phrases.',
    estimatedMinutes: 14,
  },
  {
    id: 'oral-coach',
    stage: 3,
    title: 'Oral Authenticity Coach',
    valueProp: 'French / Irish / German / Spanish. Type your prepared oral answer; four toggleable diagnostic layers — Rote phrases, Tense monotony, Structure repetition, Missing personalisation — flag what makes a memorised answer obvious. Before/after view for each prompt.',
    estimatedMinutes: 18,
  },
];

interface Props {
  onOpenModule: (id: KnowledgeModuleId) => void;
}

const NecessaryKnowledge: React.FC<Props> = ({ onOpenModule }) => {
  const stage1 = TILES.filter(t => t.stage === 1);
  const stage2 = TILES.filter(t => t.stage === 2);
  const stage3 = TILES.filter(t => t.stage === 3);

  const [patterns, setPatterns] = useState<PatternSignals>({});
  useEffect(() => {
    setPatterns(readPatterns());
  }, []);

  const handleResetPatterns = () => {
    clearPatterns();
    setPatterns({});
  };

  return (
    <div className="space-y-6">
      <header>
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#A8A29E' }}>
          Necessary Knowledge
        </p>
        <h1 className="font-serif" style={{ fontSize: 28, fontWeight: 600, color: '#1A1A1A', marginTop: 4, lineHeight: 1.2 }}>
          The hidden curriculum of the Leaving Cert.
        </h1>
        <p className="font-sans max-w-xl" style={{ fontSize: 14, color: '#78716C', marginTop: 8, lineHeight: 1.55 }}>
          Marking schemes, command words, examiner pet peeves — the stuff that separates a H4 from a H2 that nobody actually teaches you.
        </p>
      </header>

      <YourPatternsPanel patterns={patterns} onReset={handleResetPatterns} onOpenModule={onOpenModule} />

      <GroupHeader
        number={1}
        kicker="Foundations"
        title="Learn the marking grammar."
        subtitle="Five fundamentals every Leaving Cert student should know first. Command words, marking-scheme architecture, time per mark, perennial examiner peeves."
      />
      <div className="grid sm:grid-cols-2 gap-3">
        {stage1.map(tile => (
          <Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
        ))}
      </div>

      <GroupHeader
        number={2}
        kicker="Tools"
        title="See the marks happen."
        subtitle="Mistake-first interactives — see the wrong answer, feel why it loses marks, surface the fix. Mark provenance, ceiling drops, sanity radar, trap detection."
      />
      <div className="grid sm:grid-cols-2 gap-3">
        {stage2.map(tile => (
          <Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
        ))}
      </div>

      {stage3.length > 0 && (
        <>
          <GroupHeader
            number={3}
            kicker="Subject deep dives"
            title="Where a top answer separates from a middle one."
            subtitle="Per-subject simulators that go where teachers can rarely reach. Comparative integration, RSR section budgeting, Sciences phrase matching, Languages oral authenticity."
          />
          <div className="grid sm:grid-cols-2 gap-3">
            {stage3.map(tile => (
              <Tile key={tile.id} tile={tile} onOpen={() => onOpenModule(tile.id)} />
            ))}
          </div>
        </>
      )}

      <ChiefExaminerCallout />
    </div>
  );
};

// ─── Your patterns panel ───────────────────────────────────────────────

const YourPatternsPanel: React.FC<{
  patterns: PatternSignals;
  onReset: () => void;
  onOpenModule: (id: KnowledgeModuleId) => void;
}> = ({ patterns, onReset, onOpenModule }) => {
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
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '24px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 flex-wrap mb-2">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
          Your patterns · {insights.length} signal{insights.length === 1 ? '' : 's'} from your sessions
        </p>
        <button
          type="button"
          onClick={onReset}
          className="font-sans"
          style={{ fontSize: 11, color: '#FFD8A8', opacity: 0.7, background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
        >
          Reset
        </button>
      </div>
      <h3 className="font-serif" style={{ fontSize: 18, fontWeight: 600, lineHeight: 1.35 }}>
        What this app has noticed about how you answer.
      </h3>
      <p className="font-sans" style={{ fontSize: 11.5, color: '#FFD8A8', opacity: 0.7, marginTop: 4 }}>
        Stored on your device only. {updatedAtMax > 0 ? `Last updated ${formatRelativeTime(updatedAtMax)}.` : ''}
      </p>

      <div className="grid sm:grid-cols-2 gap-3 mt-5">
        {insights.map((ins, i) => (
          <div
            key={i}
            className="rounded-xl"
            style={{
              backgroundColor: '#3F3B36',
              padding: '14px 16px',
            }}
          >
            <p className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: ins.tone === 'ok' ? TEAL : '#FFD8A8', opacity: 0.85, marginBottom: 4 }}>
              {ins.kicker}
            </p>
            <p className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: '#FFFFFF', lineHeight: 1.4 }}>
              {ins.headline}
            </p>
            <p className="font-sans" style={{ fontSize: 12, color: '#E8E4DE', marginTop: 6, lineHeight: 1.55 }}>
              {ins.body}
            </p>
            {ins.openModuleId && (
              <button
                type="button"
                onClick={() => onOpenModule(ins.openModuleId!)}
                className="font-sans inline-flex items-center gap-1 mt-3"
                style={{ fontSize: 11.5, fontWeight: 600, color: TEAL, background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
              >
                {ins.openModuleLabel ?? 'Re-run module'}
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

interface PatternInsight {
  kicker: string;
  headline: string;
  body: string;
  tone: 'ok' | 'warn';
  openModuleId?: KnowledgeModuleId;
  openModuleLabel?: string;
}

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

const GroupHeader: React.FC<{
  number: number;
  kicker: string;
  title: string;
  subtitle: string;
}> = ({ number, kicker, title, subtitle }) => (
  <div className="flex items-start gap-3 pt-3">
    <span
      className="font-serif shrink-0"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        borderRadius: 999,
        width: 28,
        height: 28,
        fontSize: 12.5,
        fontWeight: 700,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 1,
      }}
    >
      {number}
    </span>
    <div>
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
        {kicker}
      </p>
      <p className="font-serif" style={{ fontSize: 18, fontWeight: 600, color: INK, marginTop: 1, lineHeight: 1.3 }}>
        {title}
      </p>
      <p className="font-sans max-w-2xl" style={{ fontSize: 12.5, color: '#5a5550', marginTop: 4, lineHeight: 1.55 }}>
        {subtitle}
      </p>
    </div>
  </div>
);

const STAGE_KICKERS: Record<Stage, string> = {
  1: 'Stage 1 · Foundations',
  2: 'Stage 2 · Tools',
  3: 'Stage 3 · Subject deep dive',
};

/** Unified module tile — bold register across all three stages. Inverts
 *  on hover. The kicker text reflects the tile's stage. */
const Tile: React.FC<{ tile: ModuleTile; onOpen: () => void }> = ({ tile, onOpen }) => (
  <button
    type="button"
    onClick={onOpen}
    className="rounded-2xl text-left transition-colors w-full"
    style={{
      backgroundColor: '#FFFFFF',
      border: `2px solid ${INK}`,
      padding: '20px 22px',
      cursor: 'pointer',
    }}
    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = INK; e.currentTarget.querySelectorAll('[data-flip]').forEach(el => { (el as HTMLElement).style.color = '#FFFFFF'; }); }}
    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#FFFFFF'; e.currentTarget.querySelectorAll('[data-flip]').forEach(el => { (el as HTMLElement).style.color = INK; }); }}
  >
    <div className="flex items-start justify-between gap-3 mb-2">
      <div>
        <p
          className="font-sans"
          style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.7, color: TEAL, marginBottom: 4 }}
        >
          {STAGE_KICKERS[tile.stage]}
        </p>
        <h3 data-flip className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: INK, lineHeight: 1.25, transition: 'color 0.2s' }}>
          {tile.title}
        </h3>
      </div>
      <span
        className="font-sans shrink-0"
        style={{
          fontSize: 10,
          fontWeight: 700,
          color: '#FFFFFF',
          backgroundColor: TEAL,
          borderRadius: 999,
          padding: '3px 9px',
          whiteSpace: 'nowrap',
        }}
      >
        {tile.estimatedMinutes} min
      </span>
    </div>
    <p data-flip className="font-sans" style={{ fontSize: 12.5, color: '#3F3B36', lineHeight: 1.55, marginBottom: 14, transition: 'color 0.2s' }}>
      {tile.valueProp}
    </p>
    <span
      className="font-sans inline-flex items-center gap-1"
      style={{ fontSize: 12, fontWeight: 700, color: TEAL }}
    >
      Start
      <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden>
        <path d="M4 3L7 6L4 9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </span>
  </button>
);

/** Closing CER quote to frame the tab's thesis. Drawn from dossier § B1
 *  (English CER 2013) — the line the entire "exam technique > content"
 *  argument rests on. */
const ChiefExaminerCallout: React.FC = () => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#FAF7F4',
      border: `1px solid ${TEAL}33`,
      padding: '22px 26px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
      What the examiners keep saying
    </p>
    <blockquote
      className="font-serif"
      style={{
        fontSize: 17,
        fontStyle: 'italic',
        color: '#1A1A1A',
        lineHeight: 1.45,
        marginBottom: 10,
      }}
    >
      "Weaker responses tended to be characterised by an over-rehearsed formulaic approach."
    </blockquote>
    <p className="font-sans" style={{ fontSize: 12, color: '#78716C' }}>
      — Chief Examiner's Report, English 2013. The complaint recurs across English (2001, 2005, 2008), Modern Languages (2016), Home Economics (2017) and every other subject the SEC has reported on. Exam technique is the trainable variable that separates grades.
    </p>
  </section>
);

export default NecessaryKnowledge;
