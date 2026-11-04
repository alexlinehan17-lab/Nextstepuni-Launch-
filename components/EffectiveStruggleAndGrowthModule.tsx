import { BrandedRecallChart } from './learning/WideFeatures';
import { moduleFill,moduleText } from './learning/brandTokens';

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
BarChartHorizontal,
Brain,
Puzzle,
Scaling,
SlidersHorizontal,Thermometer
} from 'lucide-react';
import React,{ useState } from 'react';
import { EFFECTIVE_STRUGGLE_REFERENCE_LIST } from '../data/references/effectiveStruggle';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { accentTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';

const theme = accentTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitiveLoadBalancer = () => {
    const [loads, setLoads] = useState({ intrinsic: 30, extraneous: 15, germane: 20 });
    const total = loads.intrinsic + loads.extraneous + loads.germane;
    const overload = total > 100;
    const germaneRoom = Math.max(0, 100 - loads.intrinsic - loads.extraneous);
    const healthy = total <= 85;

    const loadTypes: { key: 'intrinsic' | 'extraneous' | 'germane'; label: string; plain: string; example: string; direction: string; color: string; barColor: string; fixed?: boolean }[] = [
      { key: 'intrinsic', label: 'Intrinsic Load', plain: 'The difficulty of the topic itself', example: 'e.g., Probability is harder than basic addition', direction: 'Fixed — you can\'t change this, only manage around it', color: "var(--module-ink)", barColor: "var(--module-muted)", fixed: true },
      { key: 'extraneous', label: 'Extraneous Load', plain: 'Waste from distractions & confusion', example: 'e.g., Phone buzzing, noisy room, unclear instructions', direction: 'Minimize this — it steals space from learning', color: "var(--module-ink)", barColor: "var(--module-ink)" },
      { key: 'germane', label: 'Germane Load', plain: 'The productive effort that builds memory', example: 'e.g., Active recall, self-explanation, practice questions', direction: 'Maximize this — it\'s the only load that causes learning', color: moduleText(COLORS.success), barColor: COLORS.success },
    ];

    return (
      <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
        {/* Section chip + title */}
        <div className="text-center mb-8">
          <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Interactive Simulation</span>
          <h4 className="font-serif font-bold" style={{ fontSize: 24, color: "var(--module-ink)" }}>Cognitive Load Balancer</h4>
          <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Your Working Memory is a small container. Three types of load compete for space inside it.</p>
        </div>

        {/* Stacked bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Working Memory Capacity</span>
            <span className="font-semibold" style={{ fontSize: 13, color: moduleText(overload ? "var(--module-ink)" : COLORS.success) }}>{total}% / 100%</span>
          </div>
          <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" style={{ border: "2px solid var(--module-line)", borderRadius: 12, overflow: 'hidden', height: 28 }}>
            <div className="flex h-full">
              <motion.div style={{ backgroundColor: "var(--module-surface)" }} animate={{ width: `${Math.min(loads.intrinsic, 100)}%` }} transition={{ duration: 0.3 }} />
              <motion.div style={{ backgroundColor: "var(--module-solid)" }} animate={{ width: `${Math.min(loads.extraneous, 100 - loads.intrinsic > 0 ? loads.extraneous : 0)}%` }} transition={{ duration: 0.3 }} />
              <motion.div style={{ backgroundColor: moduleFill(COLORS.success) }} animate={{ width: `${Math.min(loads.germane, germaneRoom > 0 ? loads.germane : 0)}%` }} transition={{ duration: 0.3 }} />
            </div>
          </div>
          {/* Legend */}
          <div className="flex gap-5 mt-3 justify-center">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: "var(--module-surface)" }} />
              <span style={{ fontSize: 12, color: "var(--module-muted)" }}>Intrinsic</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: "var(--module-solid)" }} />
              <span style={{ fontSize: 12, color: "var(--module-muted)" }}>Extraneous</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: moduleFill(COLORS.success) }} />
              <span style={{ fontSize: 12, color: "var(--module-muted)" }}>Germane</span>
            </div>
          </div>
        </div>

        {/* Slider cards */}
        <div className="space-y-3 mb-6">
          {loadTypes.map(l => (
            <div key={l.key} className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" style={{ border: `2px solid ${l.color}`, borderRadius: 14, padding: '20px 22px' }}>
              <div className="flex items-start justify-between mb-1">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-serif font-semibold" style={{ fontSize: 16, color: moduleText(l.color) }}>{l.label}</p>
                    {l.fixed && (
                      <span style={{ backgroundColor: "var(--module-surface)", color: "var(--module-muted)", border: "1px solid var(--module-line)", borderRadius: 20, padding: '2px 8px', fontSize: 10, fontWeight: 700 }}>FIXED</span>
                    )}
                  </div>
                  <p style={{ fontSize: 14, color: "var(--module-ink)" }}>{l.plain}</p>
                </div>
                <span className="font-serif font-bold ml-3" style={{ fontSize: 20, color: moduleText(l.color) }}>{loads[l.key]}%</span>
              </div>
              <p className="italic mb-2" style={{ fontSize: 13, color: "var(--module-muted)" }}>{l.example}</p>
              <input
                type="range" min="5" max="70"
                value={loads[l.key]}
                onChange={e => setLoads({ ...loads, [l.key]: parseInt(e.target.value) })}
                className="chunky-slider chunky-slider-accent"
                disabled={l.fixed}
                style={l.fixed ? { opacity: 0.5 } : undefined}
              />
              <p className="font-semibold mt-1" style={{ fontSize: 12, color: moduleText(l.color) }}>{l.direction}</p>
            </div>
          ))}
        </div>

        {/* Diagnosis callout */}
        <AnimatePresence mode="wait">
          {overload ? (
            <motion.div key="overload" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ borderLeft: "3px solid var(--module-line)", backgroundColor: "var(--module-surface)", borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm italic" style={{ color: "var(--module-ink)" }}>Working memory overloaded — learning becomes very difficult at this point.</p>
            </motion.div>
          ) : healthy ? (
            <motion.div key="healthy" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ borderLeft: `3px solid ${COLORS.success}`, backgroundColor: moduleFill(COLORS.successTint), borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm italic" style={{ color: moduleText(COLORS.successDarkText) }}>Good balance — your working memory has space to form lasting memories.</p>
            </motion.div>
          ) : (
            <motion.div key="moderate" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ borderLeft: "3px solid var(--module-line)", backgroundColor: "var(--module-surface)", borderRadius: '0 10px 10px 0', padding: '12px 16px' }}>
              <p className="text-sm italic" style={{ color: "var(--module-muted)" }}>Within capacity, but push Germane load higher or reduce Extraneous to optimise learning.</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
}

const StairsEscalator = () => {
    const [choice, setChoice] = useState<'stairs' | 'escalator' | null>(null);
    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Stairs vs. Escalator</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">Which path leads to real learning?</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setChoice('escalator')} className="p-4 rounded-xl text-center font-medium transition-all" style={choice === 'escalator' ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-danger-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(choice === 'escalator')} data-tone="coral" aria-pressed={!!(choice === 'escalator')}><strong>The Escalator:</strong> A perfectly clear lecture, re-reading your notes.</button>
                <button onClick={() => setChoice('stairs')} className="p-4 rounded-xl text-center font-medium transition-all" style={choice === 'stairs' ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-success-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }} data-wide-button="true" data-selected={!!(choice === 'stairs')} data-tone="mint" aria-pressed={!!(choice === 'stairs')}><strong>The Stairs:</strong> Struggling with a past paper, trying to explain a topic.</button>
            </div>
            {choice &&
            <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6 p-4 rounded-xl text-sm" style={choice === 'stairs' ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", boxShadow: 'none', color: "var(--module-success-text)" } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", boxShadow: 'none', color: "var(--module-danger-text)" }}>
                {choice === 'escalator' && <p><strong>You chose the escalator.</strong> It feels smooth and effortless. You arrive at the top (the answer) quickly. But your muscles (your brain) did no work. The feeling of fluency is high, but long-term learning is low.</p>}
                {choice === 'stairs' && <p><strong>You chose the stairs.</strong> It's slow and feels hard. You might stumble (make mistakes). But this effort is what strengthens your cardiovascular system (your long-term memory). The feeling of learning is low, but the actual result is high.</p>}
            </motion.div>}
        </div>
    );
};

const IllusionOfCompetenceChart = BrandedRecallChart;

const ScenarioDiagnosis = () => {
  const scenarios = [
    {
      situation: 'Re-reading your History notes in a noisy kitchen while your family watches TV.',
      answer: 'extraneous',
      explanation: 'The task itself (re-reading) is too easy (Comfort Zone) AND the environment is full of distractions (high Extraneous Load). The primary fix is the environment — move somewhere quiet, then switch to active recall.',
    },
    {
      situation: 'Doing a past paper question from memory in a quiet room, on a topic you studied last week.',
      answer: 'optimal',
      explanation: 'This is Optimized Friction. The task is in your ZPD (hard but doable), the environment is clean (low Extraneous Load), and retrieval practice is a Desirable Difficulty. This is what effective study looks like.',
    },
    {
      situation: 'Watching a perfectly clear YouTube explainer on a topic you already understand well.',
      answer: 'zpd',
      explanation: 'The task is in the Comfort Zone — it feels productive because the explanation is fluent, but your brain is doing zero work. No struggle means no growth. You need to attempt harder problems on this topic.',
    },
    {
      situation: 'Attempting a Maths proof on a topic you haven\'t covered yet, with no guidance.',
      answer: 'zpd',
      explanation: 'This is the Frustration Zone. The task is so far beyond your current level that Working Memory overloads immediately. You need to step back to a worked example or ask for help to bring it into your ZPD.',
    },
    {
      situation: 'Highlighting your textbook in five different colours with a colour-coded system you invented.',
      answer: 'desirable',
      explanation: 'This feels effortful but it\'s fake friction. Highlighting is a passive task that doesn\'t force retrieval or generation. The effort is going into the system, not into learning. Replace it with a Brain Dump or practice questions.',
    },
    {
      situation: 'Trying to write an essay plan from memory, but your phone keeps buzzing with notifications.',
      answer: 'extraneous',
      explanation: 'The task is right (retrieval practice in the ZPD) but the environment is sabotaging it. Each notification hijacks your Working Memory, wiping out the very information you\'re trying to hold. Phone in another room.',
    },
  ];

  const pillars = [
    { key: 'zpd', label: 'Wrong Zone', desc: 'Too easy or too hard', color: "bg-[var(--module-solid)] text-[var(--module-ink)]", borderActive: "border-[var(--module-line)]" },
    { key: 'extraneous', label: 'Too Much Noise', desc: 'Extraneous load is high', color: "bg-[var(--module-danger)] text-[var(--module-ink)]", borderActive: "border-[var(--module-line)]" },
    { key: 'desirable', label: 'Fake Friction', desc: 'No desirable difficulties', color: "bg-[var(--module-surface)] text-[var(--module-ink)]", borderActive: "border-[var(--module-line)]" },
    { key: 'optimal', label: 'Optimized', desc: 'All three pillars aligned', color: "bg-[var(--module-success)] text-[var(--module-ink)]", borderActive: "border-success" },
  ];

  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});
  const [revealed, setRevealed] = useState<Set<number>>(new Set());

  const handleAnswer = (pillarKey: string) => {
    if (revealed.has(current)) return;
    setAnswers(prev => ({ ...prev, [current]: pillarKey }));
    setRevealed(prev => new Set(prev).add(current));
  };

  const correct = Object.entries(answers).filter(([i, a]) => a === scenarios[parseInt(i)].answer).length;
  const allDone = revealed.size === scenarios.length;

  return <div className="wr-skin" data-wide="ScenarioDiagnosis"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Unified Model: Diagnose the Study Session</h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Read each scenario and identify the primary problem — or if the session is already optimized.</p>

      {/* Progress */}
      <div className="flex gap-1.5 mb-6">
        {scenarios.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`flex-1 h-2 rounded-full transition-all ${
              revealed.has(i)
                ? answers[i] === scenarios[i].answer ? "bg-[var(--module-success)]" : "bg-[var(--module-danger)]"
                : i === current ? "bg-[var(--module-danger)]" : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)]"
            }`} data-wide-button="true" data-progress-step="true" data-current={i === current} data-result={revealed.has(i) ? (answers[i] === scenarios[i].answer ? "correct" : "incorrect") : undefined} aria-label={`Scenario ${i+1}`}
          />
        ))}
      </div>

      {/* Scenario card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={current}
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -15 }}
        >
          <div className="p-5 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] mb-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-2">Scenario {current + 1} of {scenarios.length}</p>
            <p className="text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-muted)] leading-relaxed">{scenarios[current].situation}</p>
          </div>

          {/* Diagnosis buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-5">
            {pillars.map(p => {
              const isChosen = answers[current] === p.key;
              const isCorrect = scenarios[current].answer === p.key;
              const isRevealed = revealed.has(current);

              let btnStyle: React.CSSProperties = { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' };
              let btnTextColor = '';
              if (isRevealed && isChosen && isCorrect) { btnStyle = { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }; btnTextColor = "var(--module-success-text)"; }
              else if (isRevealed && isChosen && !isCorrect) { btnStyle = { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }; btnTextColor = "var(--module-danger-text)"; }
              else if (isRevealed && isCorrect) { btnStyle = { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', opacity: 0.7 }; btnTextColor = "var(--module-success-text)"; }

              return (
                <button
                  key={p.key}
                  onClick={() => handleAnswer(p.key)}
                  disabled={isRevealed}
                  className="p-3 rounded-xl text-center transition-all"
                  style={{ ...btnStyle, color: moduleText(btnTextColor || undefined) }} data-wide-button="true"
                >
                  <p className="text-xs font-bold">{p.label}</p>
                  <p className="text-[9px] opacity-70 mt-0.5">{p.desc}</p>
                </button>
              );
            })}
          </div>

          {/* Feedback */}
          {revealed.has(current) && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-4 rounded-xl border ${
                answers[current] === scenarios[current].answer
                  ? "bg-[var(--module-success-soft)] dark:bg-[var(--module-success)]/15 border-success/30 dark:border-success/40"
                  : "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border-[var(--module-line)] dark:border-[var(--module-line)]"
              }`}
            >
              <p className={`text-xs font-bold mb-1 ${answers[current] === scenarios[current].answer ? "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]" : "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"}`}>
                {answers[current] === scenarios[current].answer ? 'Correct' : 'Not quite'}
              </p>
              <p className="text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)]">{scenarios[current].explanation}</p>
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setCurrent(c => Math.max(0, c - 1))}
          disabled={current === 0}
          className="px-4 py-2 text-xs font-bold text-[var(--module-muted)] dark:text-[var(--module-muted)] disabled:opacity-30" data-wide-button="true"
        >
          Previous
        </button>
        {current < scenarios.length - 1 ? (
          <button
            onClick={() => setCurrent(c => c + 1)}
            className="px-4 py-2 text-xs font-bold text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]" data-wide-button="true"
          >
            Next
          </button>
        ) : allDone ? (
          <span className="px-4 py-2 text-xs font-bold text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">
            {correct}/{scenarios.length} correct
          </span>
        ) : null}
      </div>

      {/* Final insight */}
      {allDone && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-[var(--module-surface)] dark:bg-[var(--module-success)] rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] text-center"
        >
          <p className="text-sm font-semibold text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">
            The formula: Right Zone + Low Noise + Real Friction = Optimized Learning.
          </p>
          <p className="text-xs text-[var(--module-success-text)] dark:text-[var(--module-success-text)] mt-1">
            Before every study session, run this quick diagnostic on your setup.
          </p>
        </motion.div>
      )}
    </div></div>;
}


const ConfidenceRetentionParadox = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const days = ['Day 0', 'Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30'];
    // Passive Re-reading: Confidence stays high, Retention crashes
    const passiveConfidence = [0.90, 0.88, 0.82, 0.78, 0.72, 0.68];
    const passiveRetention  = [0.85, 0.55, 0.38, 0.28, 0.22, 0.18];
    // Active Recall: Confidence starts low and stays moderate, Retention holds
    const activeConfidence = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60];
    const activeRetention  = [0.50, 0.52, 0.55, 0.58, 0.60, 0.61];

    const buildArea = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${toY(0)} L ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        d += ` L ${pts[pts.length - 1].x} ${toY(0)} Z`;
        return d;
    };

    const buildLine = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        return d;
    };

    const passivePhases = [
        { label: 'Feels easy', x1: 0, x2: 0.33, color: "var(--module-ink)" },
        { label: 'Still confident', x1: 0.33, x2: 0.66, color: "var(--module-danger-text)" },
        { label: 'Exam shock', x1: 0.66, x2: 1, color: "var(--module-danger-text)" },
    ];
    const activePhases = [
        { label: 'Feels hard', x1: 0, x2: 0.33, color: moduleText(COLORS.success) },
        { label: 'Building', x1: 0.33, x2: 0.66, color: moduleText(COLORS.success) },
        { label: 'Exam ready', x1: 0.66, x2: 1, color: moduleText(COLORS.success) },
    ];

    const Chart = ({ confidence, retention, phases, areaColor, areaId, areaData, label }: {
        confidence: number[]; retention: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; areaData: number[]; label: string;
    }) => (
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
            <defs>
                <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
                    <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
                </linearGradient>
            </defs>
            {/* Grid lines */}
            {[0.25, 0.5, 0.75, 1.0].map(v => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--module-muted)" strokeOpacity="0.15" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--module-muted)" strokeOpacity="0.3" />
            {/* Area fill */}
            <motion.path
                d={buildArea(areaData)}
                fill={`url(#${areaId})`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Confidence line (solid — primary) */}
            <motion.path
                d={buildLine(confidence)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Retention line (dashed — secondary) */}
            <motion.path
                d={buildLine(retention)}
                fill="none" stroke={areaColor} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* Confidence dots */}
            {confidence.map((v, i) => (
                <motion.circle key={i} cx={toX(i / (confidence.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="var(--module-surface)" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="var(--module-surface)" fontWeight="600">Low</text>
            {/* Day labels */}
            {days.map((d, i) => (
                <text key={d} x={toX(i / (days.length - 1))} y={toY(0) + 14} fontSize="9" fill="var(--module-surface)" textAnchor="middle" fontWeight="600">{d}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="var(--module-muted)" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 108} x2={W - padR - 92} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 88} y={17} fontSize="8" fill="var(--module-surface)">Confidence</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke={areaColor} strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="var(--module-surface)">Retention</text>
        </svg>
    );

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Confidence Trap</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">What feels best works worst. What feels worst works best.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-4">Most students judge their learning by how confident they feel. What does that confidence actually track over time?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-[var(--module-danger)] text-[var(--module-ink)] hover:bg-[var(--module-danger)] transition-colors" data-wide-button="true">
                        Reveal the Trap
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] p-3">
                            <Chart confidence={passiveConfidence} retention={passiveRetention} phases={passivePhases}
                                areaColor="var(--module-danger-text)" areaId="passive-grad" areaData={passiveConfidence} label="Passive Re-reading" />
                        </div>
                        <div className="rounded-lg border border-success/30 dark:border-success/40 bg-[var(--module-success-soft)]/50 dark:bg-[var(--module-success)]/15 p-3">
                            <Chart confidence={activeConfidence} retention={activeRetention} phases={activePhases}
                                areaColor={COLORS.success} areaId="active-grad" areaData={activeRetention} label="Active Recall" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
                            <span className="text-[var(--module-danger-text)] text-lg mt-0.5"></span>
                            <p className="text-[var(--module-ink)] dark:text-[var(--module-muted)]"><strong className="text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]">Re-reading</strong> creates fluency — the material feels familiar. But recognition isn't recall. When the exam asks you to produce answers, the knowledge isn't there.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
                            <span className="text-[var(--module-success-text)] text-lg mt-0.5"></span>
                            <p className="text-[var(--module-ink)] dark:text-[var(--module-muted)]"><strong className="text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">Active recall</strong> feels effortful and uncertain. But that struggle is the learning happening. Each retrieval strengthens the memory trace.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const EffectiveStruggleAndGrowthModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'fallacy-of-ease', title: 'The Fallacy of Ease', eyebrow: '01 // The Illusion', icon: Thermometer },
    { id: 'cognitive-load', title: 'Your Brain\'s Bottleneck', eyebrow: '02 // The Governor', icon: Brain },
    { id: 'zpd', title: 'The Sweet Spot', eyebrow: '03 // The Boundary', icon: Scaling },
    { id: 'desirable-difficulties', title: 'The Engine of Memory', eyebrow: '04 // The Engine', icon: Puzzle },
    { id: 'unified-model', title: 'The Unified Model', eyebrow: '05 // The Formula', icon: SlidersHorizontal },
    { id: 'recalibrate', title: 'Recalibrate Your Dashboard', eyebrow: '06 // The Feeling', icon: BarChartHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Effective Struggle"
      moduleSubtitle="Why the Hard Stuff Is the Stuff That Works"
      moduleDescription={`That frustrated feeling when you're stuck on a hard question? It's not a sign you're failing — it's actually how real learning happens. Here's how to use it.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      references={EFFECTIVE_STRUGGLE_REFERENCE_LIST}
      finishButtonText="Embrace the Struggle"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Fallacy of Ease." eyebrow="Step 1" icon={Thermometer} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain tricks you. If learning feels easy, you think you are learning well. The opposite is true. Easy learning gets forgotten fast. Hard, effortful learning sticks.</p>
                  <p>In one study, students who re-read felt more confident — but a week later they recalled just 40%. Students who tested themselves felt less sure, yet recalled 61%.<Cite n={1} /> The method that feels worse works better.</p>
                </>
              ) : (
                <>
                  <p>Our intuition tells us that learning should feel easy. We think that if a teacher explains something perfectly and we understand it without any friction, that's a sign of great learning. This is the <Highlight description="Basically, your brain tricks you into thinking that if something feels easy to learn, you must be learning it well. But it's the opposite — the easy stuff slides right out of your memory." theme={theme}>Intuitive Fallacy of Ease</Highlight>, and it's the single biggest trap students fall into.</p>
                </>
              )}
              <ConfidenceRetentionParadox />
              {!essentials && (
                <>
                  <p>Here's the thing most people get wrong: your feeling of how well you're learning is often the exact opposite of what's actually happening in your brain. Easy learning feels good but gets forgotten fast. Hard, effortful learning feels rough but it sticks. It's the difference between taking an escalator and taking the stairs. Only one of them makes you stronger.</p>
                </>
              )}
              <StairsEscalator />
              {!essentials && (
                <>
                  <p>This isn't just a vibe — it's been tested. In one experiment, two groups studied the same material: one re-read it repeatedly, the other read it once and then tested themselves. The re-readers came away feeling more confident they'd remember it. But when both groups were tested a week later, the re-readers scored just 40%, while the self-testers scored 61%.<Cite n={1} /> The strategy that felt worse was the one that worked. The chart below shows that gap between confidence and reality.</p>
                </>
              )}
              <IllusionOfCompetenceChart />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain's Bottleneck." eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Your working memory is tiny. It holds only about three to five things at once.<Cite n={2} /> Three types of load compete for space: bad load (distractions), fixed load (topic difficulty), and good load (the effort that builds memory).<Cite n={3} /></p>
                  <p>Cut the bad load. Maximise the good load. That is how you learn efficiently. Use the simulator below to see it in action.</p>
                </>
              ) : (
                <>
                  <p>To understand why difficulty is necessary, you need to know about a bottleneck in your brain called <Highlight description="Think of this as your brain's tiny desk. You can only hold about 3-5 things on it at once. If you pile on too much, stuff falls off and nothing gets learned." theme={theme}>Working Memory</Highlight>. It can only juggle a handful of things at once,<Cite n={2} /> and if you overload it, learning just stops.</p>
                  <p>There are three types of "load": <Highlight description="This is the useless stuff clogging up your brain — your phone buzzing, a noisy room, confusing instructions. It's not helping you learn, it's just taking up space. Get rid of as much of it as you can." theme={theme}>Extraneous Load</Highlight> (the bad stuff), <Highlight description="This is just how hard the topic actually is. Probability is harder than basic addition — you can't change that, you just have to work with it." theme={theme}>Intrinsic Load</Highlight> (the topic itself), and <Highlight description="This is the good kind of effort — the mental work that actually builds understanding. Things like testing yourself, explaining ideas out loud, or working through problems. You want as much of this as possible." theme={theme}>Germane Load</Highlight> (the good stuff).<Cite n={3} /> The art of learning is to clear out all the 'bad' difficulty so you have enough mental space for the 'good' difficulty that actually builds memory.</p>
                </>
              )}
              <CognitiveLoadBalancer />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Sweet Spot." eyebrow="Step 3" icon={Scaling} theme={theme}>
              {essentials ? (
                <p>You learn best when the task is hard enough to stretch you but not so hard you freeze. Too easy means zero growth. Too hard means your brain shuts down. Find the sweet spot in between.</p>
              ) : (
                <>
                  <p>The perfect level of difficulty is not too hard and not too easy. In psychology, this is called the <Highlight description="Your sweet spot. It's that zone where something is just hard enough that you have to think, but not so hard that you're completely lost. With a bit of effort or a hint, you can get there. That's where the real learning happens." theme={theme}>Zone of Proximal Development (ZPD)</Highlight>. It's the Goldilocks zone of learning.</p>
                  <p>Imagine three zones. The <strong>Comfort Zone</strong> is where you do things you've already mastered. You can do them fine, but you're learning nothing new. The <strong>Frustration Zone</strong> is where the task is so far beyond you that you can't even get started — your brain just freezes and you want to give up. The <strong>ZPD</strong> is the sweet spot in between, where you're stretched but not overwhelmed. This is the only place where real growth happens.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Think about your hardest subject. What's one topic that feels just out of reach? Can you find a worked example or ask a friend for help to bring it into your ZPD?</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Engine of Memory." eyebrow="Step 4" icon={Puzzle} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain only locks things into long-term memory when they are hard to recall. You need to partially forget before your brain bothers storing it properly. That is why re-reading feels easy but does not work.<Cite n={4} /></p>
                  <p>Testing yourself feels harder and less confident. But it produces far better results.<Cite n={1} /> The struggle to remember is the signal that tells your brain "this matters."</p>
                </>
              ) : (
                <>
                  <p>So why does the "sweet spot" feel so hard? Because of how memory actually works. It turns out memory has two strengths: <Highlight description="How easily something comes to mind right now. It's high right after you've just read your notes, but it fades fast. This is the one that tricks you into feeling confident." theme={theme}>Retrieval Strength</Highlight> (how easy it is to access now) and <Highlight description="How deeply something is actually locked into your brain for the long haul. This only grows when you struggle to remember something — not when you passively read it again. This is what actual learning looks like." theme={theme}>Storage Strength</Highlight> (how well you've actually learned it).</p>
                  <p>Here's the paradox: your brain only increases Storage Strength when Retrieval Strength is <em>low</em>. In other words, you have to forget something a little bit before your brain will put in the effort to store it properly for the long term. This is why re-reading your notes feels easy (high retrieval strength) but does nothing for long-term memory. You need the "desirable difficulty" of struggling to remember.<Cite n={4} /></p>
                  <p>This was shown clearly in <Highlight description="A well-known experiment where one group re-read their notes repeatedly, and the other group read once then tested themselves. A week later, the self-testers remembered far more — even though the re-readers had felt more confident." theme={theme}>a well-known experiment</Highlight>. Two groups of students studied the same text. One group re-read it repeatedly. The other group read it once and then tested themselves on it. After five minutes, the re-readers did slightly better — which makes sense, it was still fresh. But after one week, the results flipped: the re-readers recalled about 40% while the self-testing group held onto 61%.<Cite n={1} /> This is the <Highlight description="Testing yourself isn't just a way to check what you know — it's one of the best ways to actually learn. Every time you try to pull something out of your memory, you make that memory stronger. So quizzing yourself beats re-reading every time." theme={theme}>Testing Effect</Highlight> in action.</p>
                  <p>Here's the kicker: the re-readers were also more <em>confident</em>. They predicted higher scores. They genuinely felt like they knew the material better. But their confidence was completely wrong. The students who struggled through self-testing — who felt less confident, who made mistakes, who found it uncomfortable — were the ones who actually learned. That's the engine of memory: the struggle to pull something out of your brain is the signal that tells it "this matters, lock it in."</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Unified Model." eyebrow="Step 5" icon={SlidersHorizontal} theme={theme}>
                {essentials ? (
                  <p>The formula: Right difficulty zone + Low distractions + Real effort = Effective learning. Diagnose your study setup with the tool below.</p>
                ) : (
                  <p>Now let's put everything together into one simple formula for studying that actually works.</p>
                )}
                <ScenarioDiagnosis />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Recalibrate Your Dashboard." eyebrow="Step 6" icon={BarChartHorizontal} theme={theme}>
              {essentials ? (
                <>
                  <p>If it feels hard but you are still making some progress, keep going — that is learning. But if you are completely lost, that is a signal to step back and get a worked example or ask for help, not to push harder. Comfortable review has its place too; the aim is effort you can actually make progress with.</p>
                  <p>Regular low-stakes self-testing can also ease exam anxiety.<Cite n={5} /> You walk in knowing exactly what you know and where your gaps are. Fewer surprises.</p>
                </>
              ) : (
                <>
                  <p>Your brain is lazy by design. It prefers the escalator to the stairs. This means your gut feeling about how well you're learning is basically broken. You have to learn to override it.</p>
                  <p>From now on, when learning feels slow, frustrating, and difficult, that's not a sign you should stop. It's a sign that you're in the sweet spot. It's the feeling of your brain actually rewiring itself. You're not "confused" — you're building real understanding. You're not "slow" — you're building long-term memory. If it feels like a struggle, it's working.</p>
                  <p>Here's a bonus: regular low-stakes self-testing doesn't just improve your memory — classroom studies have found it can also ease exam anxiety.<Cite n={5} /> Think about it: anxiety usually comes from uncertainty. You *think* you know the material, but you've never actually tested that belief until the day of the real exam. Quizzing yourself regularly is a form of <Highlight description="Getting honest with yourself about what you actually know vs. what you just think you know. When you quiz yourself regularly, you stop guessing and start knowing exactly where your gaps are — so there are no nasty surprises on exam day." theme={theme}>Metacognitive Calibration</Highlight> — it replaces false confidence with honest self-knowledge. When you test yourself regularly, you walk into the exam knowing exactly what you know and what you don't. No surprises, no panic. You've already faced the hard stuff at home.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Commit to the <strong>10/20 Rule</strong>: for every 30-minute study session, spend only 10 minutes reading or reviewing the material, and then spend 20 minutes testing yourself with the book closed. Write everything you can remember, do practice questions, or explain the topic out loud. This single shift — from mostly reading to mostly recalling — will transform your retention and eliminate exam-day surprises. Start with your very next study session.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EffectiveStruggleAndGrowthModule;
