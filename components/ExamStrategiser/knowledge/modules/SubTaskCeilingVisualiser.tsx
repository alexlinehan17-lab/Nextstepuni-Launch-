/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sub-task Ceiling Visualiser (Stage 2, E5).
 *
 * Four scenarios. Each opens an "answer-quality dashboard" — a bar chart
 * with four bars: Apparent Quality, Student Expectation, Actual Score,
 * Cap. On load, the Actual Score bar drops with a spring physics
 * animation to the cap level. The visible gap between Apparent Quality
 * and Actual Score is the lesson.
 *
 * Each scenario has a Rewind sequencer — the answer body broken into
 * sentences. A play button walks the highlight backwards through the
 * sentences until it reaches the cap-trigger, which then pulses with a
 * teal flag.
 *
 * Counterfactual: a "what if you had X" button that lifts the Actual
 * bar from the cap level to the lifted score, animating the recovery.
 *
 * When the Purpose Ceiling scenario is active, a cross-link to the
 * Stage 1 PCLM Allocator surfaces.
 *
 * Closing summary appears when all four scenarios have been viewed —
 * a personalised pattern card naming the cap rules the student saw
 * fire and proposing one unifying habit.
 *
 * Source: dossier § A2, English CERs 2008/2013, 2025 Business HL
 * Marking Scheme, 2012 Geography CER.
 *
 * Aesthetic: Stage 2 register. Framer Motion springs on the ceiling
 * drop and counterfactual lift; SVG cap line with dashed pattern.
 */

import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { CEILING_SCENARIOS } from '../../../../data/knowledge/ceilingScenarios';
import { type CeilingScenario } from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

interface Props {
  onBack: () => void;
}

const SubTaskCeilingVisualiser: React.FC<Props> = ({ onBack }) => {
  const [scenarioId, setScenarioId] = useState<string>(CEILING_SCENARIOS[0].id);
  const scenario = useMemo(() => CEILING_SCENARIOS.find(s => s.id === scenarioId)!, [scenarioId]);

  const [viewedIds, setViewedIds] = useState<Set<string>>(new Set([CEILING_SCENARIOS[0].id]));
  const [counterfactualOn, setCounterfactualOn] = useState(false);
  const [rewindStep, setRewindStep] = useState<number>(scenario.answerSentences.length - 1);

  const switchScenario = (id: string) => {
    setScenarioId(id);
    setViewedIds(prev => new Set([...prev, id]));
    setCounterfactualOn(false);
    const newScenario = CEILING_SCENARIOS.find(s => s.id === id)!;
    setRewindStep(newScenario.answerSentences.length - 1);
  };

  const allViewed = viewedIds.size === CEILING_SCENARIOS.length;

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <ScenarioPicker
        scenarios={CEILING_SCENARIOS}
        activeId={scenarioId}
        viewedIds={viewedIds}
        onChange={switchScenario}
      />

      <Dashboard
        scenario={scenario}
        counterfactualOn={counterfactualOn}
        onToggleCounterfactual={() => setCounterfactualOn(v => !v)}
      />

      <Rewind
        scenario={scenario}
        rewindStep={rewindStep}
        onSetStep={setRewindStep}
      />

      <Counterfactual
        scenario={scenario}
        counterfactualOn={counterfactualOn}
        onToggle={() => setCounterfactualOn(v => !v)}
      />

      {scenario.crossLink && <CrossLink crossLink={scenario.crossLink} />}

      {allViewed && <UnifiedSummary scenarios={CEILING_SCENARIOS} />}
    </div>
  );
};

// ─── Layout chrome ─────────────────────────────────────────────────────

const BackBar: React.FC<{ onBack: () => void }> = ({ onBack }) => (
  <button
    type="button"
    onClick={onBack}
    className="font-sans flex items-center gap-1.5"
    style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
  >
    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
      <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
    Necessary Knowledge
  </button>
);

const Hero: React.FC = () => (
  <header>
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#9e9186' }}>
      Necessary Knowledge · Stage 2
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Sub-task Ceiling Visualiser.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      Beautiful writing on a wrong question scores 30%. Watch the ceiling fire. Rewind to the exact sentence where the cap fired.
      See what 2 minutes on the missed sub-task would have done.
    </p>
  </header>
);

// ─── Scenario picker ───────────────────────────────────────────────────

const ScenarioPicker: React.FC<{
  scenarios: CeilingScenario[];
  activeId: string;
  viewedIds: Set<string>;
  onChange: (id: string) => void;
}> = ({ scenarios, activeId, viewedIds, onChange }) => (
  <div className="grid sm:grid-cols-2 gap-2">
    {scenarios.map(s => {
      const active = s.id === activeId;
      const viewed = viewedIds.has(s.id);
      return (
        <button
          key={s.id}
          type="button"
          onClick={() => onChange(s.id)}
          className="text-left rounded-xl"
          style={{
            backgroundColor: active ? INK : '#FFFFFF',
            color: active ? '#FFFFFF' : INK,
            border: `2px solid ${INK}`,
            padding: '12px 14px',
            cursor: 'pointer',
          }}
        >
          <div className="flex items-baseline justify-between gap-2 mb-1">
            <span className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7 }}>
              {s.capRuleLabel}
            </span>
            {viewed && !active && (
              <span aria-hidden style={{ color: TEAL, fontSize: 12, fontWeight: 700 }}>•</span>
            )}
          </div>
          <p className="font-serif" style={{ fontSize: 13.5, fontWeight: 600, lineHeight: 1.35 }}>
            {s.scenarioLabel}
          </p>
        </button>
      );
    })}
  </div>
);

// ─── Dashboard ─────────────────────────────────────────────────────────

const Dashboard: React.FC<{
  scenario: CeilingScenario;
  counterfactualOn: boolean;
  onToggleCounterfactual: () => void;
}> = ({ scenario, counterfactualOn }) => {
  const liftedActual = counterfactualOn ? scenario.counterfactual.liftedScore : scenario.actualScore;
  const ceilingDropDelta = scenario.studentExpectation - scenario.actualScore;

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '26px 28px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-1 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Answer-quality dashboard
        </p>
        <span
          className="font-sans"
          style={{
            fontSize: 11,
            fontWeight: 700,
            color: counterfactualOn ? TEAL : WARN,
            backgroundColor: counterfactualOn ? `${TEAL}15` : `${WARN}15`,
            border: `1px solid ${counterfactualOn ? TEAL : WARN}`,
            borderRadius: 999,
            padding: '4px 10px',
          }}
        >
          {counterfactualOn ? 'Counter-factual: lifted' : `Cap fired · −${ceilingDropDelta} marks`}
        </span>
      </div>
      <h3 className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: INK, marginBottom: 16, lineHeight: 1.35 }}>
        {scenario.scenarioLabel}
      </h3>

      <BarChart
        bars={[
          { label: 'Apparent quality', value: scenario.apparentQuality, tone: 'subtle' },
          { label: 'Marks expected', value: scenario.studentExpectation, tone: 'subtle' },
          { label: 'Marks actually awarded', value: liftedActual, tone: counterfactualOn ? 'lifted' : 'drop' },
        ]}
        capLevel={scenario.capLevel}
        capLabel={scenario.capRuleLabel}
        counterfactualOn={counterfactualOn}
      />
    </section>
  );
};

interface BarSpec {
  label: string;
  value: number;
  tone: 'subtle' | 'drop' | 'lifted';
}

const BarChart: React.FC<{
  bars: BarSpec[];
  capLevel: number;
  capLabel: string;
  counterfactualOn: boolean;
}> = ({ bars, capLevel, capLabel, counterfactualOn }) => {
  const maxValue = 100;
  const chartHeight = 220;
  const capPx = (capLevel / maxValue) * chartHeight;

  return (
    <div className="relative" style={{ marginTop: 8 }}>
      {/* Cap line */}
      <div
        aria-hidden
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          bottom: capPx + 32, // bar foot offset
          height: 0,
          borderTop: `2px dashed ${WARN}`,
          zIndex: 2,
        }}
      />
      <span
        className="font-sans"
        aria-hidden
        style={{
          position: 'absolute',
          right: 0,
          bottom: capPx + 36,
          fontSize: 10,
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: 0.5,
          color: WARN,
          backgroundColor: '#FFFFFF',
          padding: '0 4px',
          zIndex: 3,
        }}
      >
        Cap · {capLabel} · {capLevel}
      </span>

      {/* Bars */}
      <div className="flex items-end justify-between gap-3" style={{ height: chartHeight + 32, paddingTop: 12 }}>
        {bars.map((bar, i) => (
          <BarColumn key={i} bar={bar} chartHeight={chartHeight} maxValue={maxValue} counterfactualOn={counterfactualOn} />
        ))}
      </div>
    </div>
  );
};

const BarColumn: React.FC<{
  bar: BarSpec;
  chartHeight: number;
  maxValue: number;
  counterfactualOn: boolean;
}> = ({ bar, chartHeight, maxValue, counterfactualOn }) => {
  const heightPx = (bar.value / maxValue) * chartHeight;

  // For 'drop' tone, animate from apparent (top) down to actual (cap).
  // For 'lifted' tone, animate from cap up to lifted score.
  const isDrop = bar.tone === 'drop';
  const isLifted = bar.tone === 'lifted';

  return (
    <div className="flex-1 flex flex-col items-center" style={{ height: chartHeight + 32 }}>
      <div
        style={{
          flex: 1,
          width: '100%',
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          position: 'relative',
        }}
      >
        <motion.div
          key={`${bar.label}-${counterfactualOn}-${bar.value}`}
          initial={
            isDrop
              ? { height: chartHeight }
              : isLifted
              ? { height: (bar.tone === 'lifted' ? heightPx : 0) - 20 }
              : { height: 0 }
          }
          animate={{ height: heightPx }}
          transition={
            isDrop
              ? { type: 'spring', stiffness: 80, damping: 14, mass: 1.1, delay: 0.15 }
              : isLifted
              ? { type: 'spring', stiffness: 110, damping: 16 }
              : { duration: 0.55, ease: 'easeOut', delay: 0.05 }
          }
          style={{
            width: '78%',
            maxWidth: 92,
            backgroundColor: bar.tone === 'subtle' ? '#EDEBE8' : isLifted ? TEAL : WARN,
            border: `2px solid ${bar.tone === 'subtle' ? '#9e9186' : isLifted ? TEAL_DARK : '#7A4944'}`,
            borderBottom: 'none',
            borderRadius: '6px 6px 0 0',
          }}
        />
        <span
          className="font-serif"
          aria-hidden
          style={{
            position: 'absolute',
            bottom: heightPx + 6,
            fontSize: 13,
            fontWeight: 700,
            color: bar.tone === 'subtle' ? '#5a5550' : isLifted ? TEAL_DARK : INK,
          }}
        >
          {bar.value}
        </span>
      </div>
      <span className="font-sans text-center" style={{ fontSize: 11, color: '#5a5550', marginTop: 8, lineHeight: 1.3 }}>
        {bar.label}
      </span>
    </div>
  );
};

// ─── Rewind ────────────────────────────────────────────────────────────

const Rewind: React.FC<{
  scenario: CeilingScenario;
  rewindStep: number;
  onSetStep: (idx: number) => void;
}> = ({ scenario, rewindStep, onSetStep }) => {
  const triggerIdx = scenario.answerSentences.findIndex(s => s.isCapTrigger);
  const isAtTrigger = rewindStep === triggerIdx;

  const playRewind = () => {
    // Walk from current step backwards to trigger
    const start = scenario.answerSentences.length - 1;
    let cur = start;
    onSetStep(start);
    const interval = setInterval(() => {
      cur -= 1;
      if (cur < triggerIdx) {
        clearInterval(interval);
        return;
      }
      onSetStep(cur);
      if (cur === triggerIdx) {
        clearInterval(interval);
      }
    }, 600);
  };

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: CREAM,
        border: `2px solid ${INK}`,
        padding: '24px 26px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-3 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Rewind to the cap-trigger
        </p>
        <button
          type="button"
          onClick={playRewind}
          className="font-sans rounded-full"
          style={{
            backgroundColor: INK,
            color: '#FFFFFF',
            border: `2px solid ${INK}`,
            padding: '7px 16px',
            fontSize: 12,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          {isAtTrigger ? 'Replay' : 'Rewind'}
          <span style={{ marginLeft: 4 }}>◀</span>
        </button>
      </div>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#5a5550', marginBottom: 16, lineHeight: 1.55 }}>
        Walk back through the answer until you reach the moment the cap fired. Everything after that point is uncapped quality — but it\'s all stuck under the ceiling.
      </p>

      <div className="space-y-2">
        {scenario.answerSentences.map((s, idx) => (
          <SentenceRow
            key={s.id}
            sentence={s}
            idx={idx}
            isHighlighted={idx === rewindStep}
            isTrigger={s.isCapTrigger ?? false}
            isAfterTrigger={triggerIdx !== -1 && idx > triggerIdx}
          />
        ))}
      </div>
    </section>
  );
};

const SentenceRow: React.FC<{
  sentence: { id: string; text: string; isCapTrigger?: boolean };
  idx: number;
  isHighlighted: boolean;
  isTrigger: boolean;
  isAfterTrigger: boolean;
}> = ({ sentence, idx, isHighlighted, isTrigger, isAfterTrigger }) => {
  const opacity = isAfterTrigger ? 0.5 : 1;
  return (
    <motion.div
      layout
      animate={{
        backgroundColor: isHighlighted && isTrigger
          ? `${WARN}30`
          : isHighlighted
          ? '#FFFFFF'
          : '#FFFFFF',
        borderColor: isHighlighted && isTrigger
          ? WARN
          : isHighlighted
          ? INK
          : '#d0cdc8',
      }}
      transition={{ duration: 0.3 }}
      className="rounded-xl relative"
      style={{
        border: '2px solid',
        padding: '12px 14px',
        opacity,
        display: 'grid',
        gridTemplateColumns: '32px 1fr auto',
        gap: 12,
        alignItems: 'flex-start',
      }}
    >
      <span
        className="font-serif inline-flex items-center justify-center"
        style={{
          backgroundColor: isHighlighted && isTrigger ? WARN : isHighlighted ? INK : '#9e9186',
          color: '#FFFFFF',
          borderRadius: 999,
          width: 24,
          height: 24,
          fontSize: 11,
          fontWeight: 700,
          marginTop: 1,
        }}
      >
        {idx + 1}
      </span>
      <p className="font-serif" style={{ fontSize: 14, color: INK, lineHeight: 1.55 }}>
        {sentence.text}
      </p>
      {isTrigger && (
        <motion.span
          animate={{
            opacity: isHighlighted ? [0.5, 1, 0.5] : 0.85,
          }}
          transition={isHighlighted ? { duration: 1.4, repeat: Infinity } : { duration: 0.2 }}
          className="font-sans shrink-0"
          style={{
            fontSize: 9.5,
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: 0.5,
            color: WARN,
            backgroundColor: '#FFFFFF',
            border: `1.5px solid ${WARN}`,
            borderRadius: 4,
            padding: '2px 7px',
            whiteSpace: 'nowrap',
            marginTop: 2,
          }}
        >
          Cap fired here
        </motion.span>
      )}
    </motion.div>
  );
};

// ─── Counterfactual ───────────────────────────────────────────────────

const Counterfactual: React.FC<{
  scenario: CeilingScenario;
  counterfactualOn: boolean;
  onToggle: () => void;
}> = ({ scenario, counterfactualOn, onToggle }) => {
  const lift = scenario.counterfactual.liftedScore - scenario.actualScore;
  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: counterfactualOn ? `${TEAL}10` : '#FFFFFF',
        border: `2px solid ${counterfactualOn ? TEAL : INK}`,
        padding: '22px 24px',
        transition: 'background-color 0.3s, border-color 0.3s',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: counterfactualOn ? TEAL_DARK : TEAL }}>
          Counter-factual
        </p>
        <button
          type="button"
          onClick={onToggle}
          className="font-sans rounded-full"
          style={{
            backgroundColor: counterfactualOn ? TEAL : INK,
            color: '#FFFFFF',
            border: `2px solid ${counterfactualOn ? TEAL : INK}`,
            padding: '8px 18px',
            fontSize: 12.5,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          {counterfactualOn ? 'Reset' : `Lift the ceiling — +${lift} marks`}
        </button>
      </div>
      <h4 className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: INK, lineHeight: 1.4, marginBottom: 6 }}>
        {scenario.counterfactual.actionLabel}
      </h4>
      <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.6 }}>
        {scenario.counterfactual.actionDetail}
      </p>
      {scenario.source.cite && (
        <p className="font-sans" style={{ fontSize: 11, color: '#78716C', marginTop: 10, fontStyle: 'italic' }}>
          {scenario.source.cite}
        </p>
      )}
    </section>
  );
};

// ─── Cross-link ────────────────────────────────────────────────────────

const CrossLink: React.FC<{ crossLink: { moduleId: string; moduleLabel: string } }> = ({ crossLink }) => (
  <div
    className="rounded-xl flex items-center gap-3"
    style={{
      backgroundColor: '#FFFFFF',
      border: `1.5px solid ${TEAL}`,
      padding: '12px 16px',
    }}
  >
    <svg width="18" height="18" viewBox="0 0 16 16" fill="none" aria-hidden style={{ color: TEAL, flexShrink: 0 }}>
      <path d="M8 1L8 15M1 8L15 8" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
    <p className="font-sans" style={{ fontSize: 13, color: INK, lineHeight: 1.5 }}>
      The cap rule here is the <strong>Purpose Ceiling</strong>. The {crossLink.moduleLabel} lets you set P, C, L, M sliders directly to feel the ceiling rule in action.
    </p>
  </div>
);

// ─── Unified summary ───────────────────────────────────────────────────

const UnifiedSummary: React.FC<{ scenarios: CeilingScenario[] }> = ({ scenarios }) => {
  const totalLost = scenarios.reduce((sum, s) => sum + (s.studentExpectation - s.actualScore), 0);
  const ruleLabels = scenarios.map(s => s.capRuleLabel);
  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="rounded-2xl"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        padding: '28px 30px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Ceilings you saw fire
      </p>
      <h3 className="font-serif" style={{ fontSize: 22, fontWeight: 600, lineHeight: 1.25, marginTop: 6 }}>
        Four cap rules. {totalLost} marks of beautifully written work, capped.
      </h3>

      <ul className="mt-5 space-y-2">
        {ruleLabels.map(label => (
          <li
            key={label}
            className="font-sans flex items-baseline gap-2"
            style={{ fontSize: 13, color: '#E8E4DE' }}
          >
            <span style={{ color: TEAL, fontSize: 18, lineHeight: 1 }}>·</span>
            <span><strong>{label}</strong></span>
          </li>
        ))}
      </ul>

      <div className="mt-5" style={{ borderLeft: `3px solid ${TEAL}`, paddingLeft: 16 }}>
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.9 }}>
          The single habit that defeats all four
        </p>
        <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', marginTop: 4, lineHeight: 1.6 }}>
          Read the rubric for sub-task counts, named-example demands, and quotation rules <em>before</em> writing. Underline the cue and tick it off in the answer. Two minutes of rubric-reading at the start defeats every ceiling on this dashboard.
        </p>
      </div>
    </motion.section>
  );
};

export default SubTaskCeilingVisualiser;
