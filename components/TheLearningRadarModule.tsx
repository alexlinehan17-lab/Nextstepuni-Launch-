/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import { Activity,AlertTriangle,Clock,Flag,Layers,Target } from 'lucide-react';
import React,{ useState } from 'react';
import { LEARNING_RADAR_REFERENCE_LIST } from '../data/references/learningRadar';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { violetTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,AnswerTick,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';

const theme = violetTheme;

// --- INTERACTIVE COMPONENTS ---

// 1. CALIBRATION QUIZ
const CALIBRATION_STATEMENTS = [
  { statement: 'The Great Wall of China is visible from space with the naked eye.', answer: false },
  { statement: 'Humans use only 10% of their brain.', answer: false },
  { statement: 'Sound travels faster through water than through air.', answer: true },
  { statement: 'An octopus has three hearts.', answer: true },
  { statement: 'Lightning never strikes the same place twice.', answer: false },
  { statement: 'Bananas grow on trees.', answer: false },
  { statement: 'The Sahara is the largest desert in the world.', answer: false },
  { statement: 'Diamond is the hardest natural substance on Earth.', answer: true },
];

const CONFIDENCE_LEVELS = [25, 50, 75, 100];

const CalibrationQuiz = () => {
  const [step, setStep] = useState(0); // 0-7 = questions, 8 = results
  const [phase, setPhase] = useState<'confidence' | 'answer'>('confidence');
  const [responses, setResponses] = useState<{ confidence: number; correct: boolean }[]>([]);
  const [currentConfidence, setCurrentConfidence] = useState<number | null>(null);

  const handleConfidence = (level: number) => {
    setCurrentConfidence(level);
    setPhase('answer');
  };

  const handleAnswer = (answer: boolean) => {
    const correct = answer === CALIBRATION_STATEMENTS[step].answer;
    setResponses((prev) => [...prev, { confidence: currentConfidence!, correct }]);
    setCurrentConfidence(null);
    setPhase('confidence');
    setStep((s) => s + 1);
  };

  const reset = () => {
    setStep(0);
    setPhase('confidence');
    setResponses([]);
    setCurrentConfidence(null);
  };

  // Calculate calibration data for results
  const getCalibrationData = () => {
    const buckets: Record<number, { total: number; correct: number }> = {};
    CONFIDENCE_LEVELS.forEach((l) => (buckets[l] = { total: 0, correct: 0 }));
    responses.forEach((r) => {
      buckets[r.confidence].total++;
      if (r.correct) buckets[r.confidence].correct++;
    });
    return CONFIDENCE_LEVELS.map((level) => ({
      level,
      predicted: level,
      actual: buckets[level].total > 0 ? Math.round((buckets[level].correct / buckets[level].total) * 100) : null,
      count: buckets[level].total,
    }));
  };

  if (step >= 8) {
    const data = getCalibrationData();
    const totalCorrect = responses.filter((r) => r.correct).length;
    const avgConfidence = Math.round(responses.reduce((s, r) => s + r.confidence, 0) / responses.length);
    const actualAccuracy = Math.round((totalCorrect / 8) * 100);
    const gap = avgConfidence - actualAccuracy;

    return (
      <ExerciseSheet title="Your Calibration Report" sub="How well did your confidence predict your accuracy?" name="CalibrationQuiz">
        {/* The three figures in a line, on the sheet (no box round each) */}
        <div className="grid grid-cols-3 gap-4 text-center py-3 border-y border-hairline">
          <div>
            <p className="t-name-sm text-ink-primary">{avgConfidence}%</p>
            <p className="t-meta mt-1">Avg Confidence</p>
          </div>
          <div>
            <p className="t-name-sm text-ink-primary">{actualAccuracy}%</p>
            <p className="t-meta mt-1">Actual Accuracy</p>
          </div>
          <div>
            <p className="t-name-sm text-ink-primary">{gap > 0 ? '+' : ''}{gap}%</p>
            <p className="t-meta mt-1">Calibration Gap</p>
          </div>
        </div>

        {/* Calibration chart: a hairline track, the prediction a soft bar with an ink mark at its end, the
            actual bar green where it kept up with the prediction and ink where it fell short */}
        <div className="space-y-3">
          {data.filter((d) => d.count > 0).map((d) => (
            <div key={d.level} className="flex items-center gap-3">
              <span className="t-meta w-20 text-right">{d.level}% conf.</span>
              <div className="flex-1 relative h-7 rounded-full overflow-hidden" style={{ backgroundColor: "var(--hairline)" }}>
                {/* Predicted bar */}
                <div className="absolute inset-y-0 left-0 rounded-full" style={{ width: `${d.predicted}%`, backgroundColor: "var(--outline-soft)" }} />
                {/* Actual bar */}
                <MotionDiv
                  initial={{ width: 0 }}
                  animate={{ width: `${d.actual ?? 0}%` }}
                  transition={{ duration: 0.8, delay: 0.2 }}
                  className="absolute inset-y-0 left-0 rounded-full"
                  style={{ backgroundColor: d.actual !== null && d.actual >= d.predicted - 10 ? "var(--success-hex)" : "var(--ink-primary)" }}
                />
                {/* Diagonal marker for predicted */}
                <div className="absolute inset-y-0 flex items-center" style={{ left: `${d.predicted}%` }}>
                  <div className="w-0.5 h-full" style={{ backgroundColor: "var(--ink-primary)" }} />
                </div>
              </div>
              <span className="t-meta w-16" style={{ color: "var(--ink-primary)" }}>
                {d.actual !== null ? `${d.actual}% actual` : '—'}
              </span>
            </div>
          ))}
        </div>
        <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1 t-meta">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded inline-block" style={{ backgroundColor: "var(--outline-soft)" }} /> Predicted</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded inline-block" style={{ backgroundColor: "var(--success-hex)" }} /> Actual (calibrated)</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded inline-block" style={{ backgroundColor: "var(--ink-primary)" }} /> Actual (overconfident)</span>
        </div>

        <MotionDiv
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <AnswerLine tone={gap > 5 ? 'note' : 'ok'}>
          {gap > 15
            ? 'You were quite a bit more confident than your accuracy shows. Don\'t worry — most people are. The gap between what you thought you knew and what you actually got right is your blind spot. The good news? Now that you can see it, you can start fixing it.'
            : gap > 5
            ? 'You were a little more confident than your results suggest. That\'s pretty normal. With practice, you can close this gap and get much better at knowing what you actually know.'
            : 'Nice one! Your confidence closely matches your accuracy. That\'s a really valuable skill — it means you can trust your gut when deciding what to study and what to skip.'}
          </AnswerLine>
        </MotionDiv>

        <div className="ex-actions">
          <TextButton tone="quiet" onClick={reset}>
            Try Again
          </TextButton>
        </div>
      </ExerciseSheet>
    );
  }

  const q = CALIBRATION_STATEMENTS[step];

  return (
    <ExerciseSheet title="Calibration Quiz" sub="Rate your confidence, then answer. Let's see how well you know what you know." name="CalibrationQuiz">
      <p className="ex-count t-readout">Question {step + 1} of 8</p>

      {/* The statement: words you read, on the sheet (no box) */}
      <p className="ex-quote">"{q.statement}"</p>

      {phase === 'confidence' ? (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="conf">
          <AnswerGroup kind="one" legend="How confident are you that you know the correct answer?" columns={2} chooseOnArrow={false}>
            {CONFIDENCE_LEVELS.map((level) => (
              <ChoiceTile
                key={level}
                chosen={currentConfidence === level}
                onClick={() => handleConfidence(level)}
                label={<>{level}%</>}
              />
            ))}
          </AnswerGroup>
        </MotionDiv>
      ) : (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="ans">
          <AnswerGroup kind="one" legend="Is this statement True or False?" columns={2} chooseOnArrow={false}>
            <ChoiceTile chosen={false} onClick={() => handleAnswer(true)} label="True" />
            <ChoiceTile chosen={false} onClick={() => handleAnswer(false)} label="False" />
          </AnswerGroup>
          <p className="t-meta mt-3">You rated: {currentConfidence}% confident</p>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// 2. DUNNING-KRUGER CURVE
const DunningKrugerCurve = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 240;
  const padL = 45, padR = 15, padT = 20, padB = 50;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  // The classic DK curve: confidence vs competence
  // Overconfidence peak → valley of doubt → steady improvement → realistic confidence
  const dkPoints = [
    { x: 0, y: 0.15 },
    { x: 0.08, y: 0.55 },
    { x: 0.15, y: 0.92 }, // Peak of Overconfidence
    { x: 0.25, y: 0.72 },
    { x: 0.38, y: 0.25 }, // Valley of Doubt
    { x: 0.55, y: 0.40 },
    { x: 0.70, y: 0.58 }, // Steady Improvement
    { x: 0.85, y: 0.72 },
    { x: 1.0, y: 0.78 },  // Realistic Confidence
  ];

  const buildCurve = (points: { x: number; y: number }[]) => {
    const pts = points.map((p) => ({ x: toX(p.x), y: toY(p.y) }));
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 1; i < pts.length; i++) {
      const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.5;
      const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.5;
      d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
    }
    return d;
  };

  const buildArea = (points: { x: number; y: number }[]) => {
    return buildCurve(points) + ` L ${toX(1)} ${toY(0)} L ${toX(0)} ${toY(0)} Z`;
  };

  const labels = [
    { text: 'Peak of\nOverconfidence', x: 0.15, y: 0.92, anchor: 'middle' as const },
    { text: 'Valley of\nDoubt', x: 0.38, y: 0.25, anchor: 'middle' as const },
    { text: 'Steady\nImprovement', x: 0.70, y: 0.58, anchor: 'middle' as const },
    { text: 'Realistic\nConfidence', x: 0.92, y: 0.78, anchor: 'middle' as const },
  ];

  // The drawing in ink: a flat fill under the curve, no gradient; text in the one typeface, 11 or more.
  const font = { fontFamily: 'var(--font-ui)' };

  return (
    <ExerciseSheet title="The Confidence vs. Reality Curve" sub="A simplified illustration of how confidence and real ability can drift apart — not a literal graph of any single study." name="DunningKrugerCurve">
      {!revealed ? (
        <div className="ex-stack">
          <p className="t-body text-ink-secondary">Where do you think your confidence sits relative to your actual knowledge?</p>
          <div className="ex-actions">
            <Button onClick={() => setRevealed(true)}>
              Reveal the Curve
            </Button>
          </div>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="ex-stack">
          {/* The curve, on the sheet (no box of its own) */}
          <div className="ex-figure">
            <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
              {/* Grid lines */}
              {[0.25, 0.5, 0.75, 1.0].map((v) => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--ink-muted)" strokeOpacity="0.15" strokeDasharray="3 3" />
              ))}
              <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--ink-muted)" strokeOpacity="0.3" />

              {/* Perfect calibration diagonal (its label sits over the line's top end, clear of the curve's labels) */}
              <line x1={toX(0)} y1={toY(0)} x2={toX(1)} y2={toY(1)} stroke="var(--ink-muted)" strokeWidth="1" strokeDasharray="6 4" strokeOpacity="0.6" />
              <text x={toX(1)} y={toY(1) - 8} fontSize="11" fill="var(--ink-muted)" textAnchor="end" style={font}>Perfect calibration</text>

              {/* DK curve area */}
              <motion.path d={buildArea(dkPoints)} fill="var(--ink-primary)" fillOpacity="0.05" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />

              {/* DK curve line */}
              <motion.path d={buildCurve(dkPoints)} fill="none" stroke="var(--ink-primary)" strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, ease: 'easeOut' }} />

              {/* Key point dots */}
              {dkPoints.filter((_, i) => [2, 4, 6, 8].includes(i)).map((p, i) => (
                <motion.circle key={i} cx={toX(p.x)} cy={toY(p.y)} r="4" fill="var(--surface-paper)" stroke="var(--ink-primary)" strokeWidth="2" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.5 + i * 0.3 }} />
              ))}

              {/* Labels */}
              {labels.map((l, i) => (
                <motion.g key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 + i * 0.3 }}>
                  {l.text.split('\n').map((line, j) => (
                    <text key={j} x={toX(l.x)} y={toY(l.y) + (j === 0 ? -20 : -8)} fontSize="11" fill="var(--ink-primary)" textAnchor={l.anchor} style={font}>{line}</text>
                  ))}
                </motion.g>
              ))}

              {/* Axis labels */}
              <text x={padL + 2} y={toY(1.0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>High</text>
              <text x={padL + 2} y={toY(0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>Low</text>
              <text x={W / 2} y={H - 4} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" style={font}>Actual Competence →</text>
              <text x={10} y={H / 2} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" transform={`rotate(-90, 10, ${H / 2})`} style={font}>Confidence →</text>
            </svg>
          </div>

          {/* What the two ends mean: words you read, ruled like rows (no tinted boxes) */}
          <div className="ex-list">
            <div><p className="t-sub"><strong className="text-ink-primary">The Peak</strong> is where most students sit after just reading their notes. They feel confident because the material looks familiar — but they can't actually pull it out of their heads under exam conditions.</p></div>
            <div><p className="t-sub"><strong className="text-ink-primary">Realistic Confidence</strong> is where well-prepared students land. They've tested themselves enough to know exactly what they know — and what they don't. Their confidence matches reality.</p></div>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// 3. JOL TIMING COMPARISON (Planning Paradox style)
const JOLTimingComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Study', '+1hr', '+1 day', '+3 days', '+7 days', '+14 days'];

  // Immediate JOLs: confidence stays high, actual recall crashes
  const immConfidence = [0.90, 0.88, 0.85, 0.82, 0.78, 0.75];
  const immRecall = [0.88, 0.55, 0.35, 0.25, 0.18, 0.12];

  // Delayed JOLs: confidence is lower but tracks actual recall closely
  const delConfidence = [0.50, 0.48, 0.45, 0.42, 0.40, 0.38];
  const delRecall = [0.55, 0.48, 0.42, 0.38, 0.35, 0.32];

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

  const immPhases = [
    { label: 'Feels obvious', x1: 0, x2: 0.33, color: "var(--ink-secondary)" },
    { label: 'Still confident', x1: 0.33, x2: 0.66, color: "var(--ink-secondary)" },
    { label: 'Blind to decay', x1: 0.66, x2: 1, color: "var(--ink-secondary)" },
  ];
  const delPhases = [
    { label: 'Honest check', x1: 0, x2: 0.33, color: "var(--ink-secondary)" },
    { label: 'Tracks reality', x1: 0.33, x2: 0.66, color: "var(--ink-secondary)" },
    { label: 'Calibrated', x1: 0.66, x2: 1, color: "var(--ink-secondary)" },
  ];

  // Confidence solid ink, recall a dashed ink-2 line, a flat fill under confidence (no gradient);
  // text in the one typeface, 11 or more.
  const font = { fontFamily: 'var(--font-ui)' };
  const Chart = ({ confidence, recall, phases, areaColor, label }: {
    confidence: number[]; recall: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
      {[0.25, 0.5, 0.75, 1.0].map((v) => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--ink-muted)" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--ink-muted)" strokeOpacity="0.3" />

      {/* Confidence area */}
      <motion.path d={buildArea(confidence)} fill={areaColor} fillOpacity="0.08" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />
      {/* Confidence line (solid) */}
      <motion.path d={buildLine(confidence)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut' }} />
      {/* Recall line (dashed) */}
      <motion.path d={buildLine(recall)} fill="none" stroke="var(--ink-secondary)" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }} />
      {/* Confidence dots */}
      {confidence.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (confidence.length - 1))} cy={toY(v)} r="3.5" fill={areaColor} initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }} />
      ))}

      <text x={padL + 2} y={toY(1.0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>Low</text>
      {/* Time labels (the first and last sit inside the drawing) */}
      {xLabels.map((m, i) => (
        <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="11" fill="var(--ink-muted)" textAnchor={i === 0 ? 'start' : i === xLabels.length - 1 ? 'end' : 'middle'} style={font}>{m}</text>
      ))}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 30} fontSize="11" fill={p.color} textAnchor="middle" style={font}>{p.label}</text>
      ))}
      <text x={padL} y={15} fontSize="12" fill="var(--ink-primary)" style={font}>{label}</text>
      <line x1={W - padR - 152} x2={W - padR - 136} y1={11} y2={11} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 132} y={15} fontSize="11" fill="var(--ink-muted)" style={font}>Confidence</text>
      <line x1={W - padR - 60} x2={W - padR - 44} y1={11} y2={11} stroke="var(--ink-secondary)" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR} y={15} fontSize="11" fill="var(--ink-muted)" textAnchor="end" style={font}>Recall</text>
    </svg>
  );

  return (
    <ExerciseSheet title="The Timing Effect" sub="When you check your learning changes everything." name="JOLTimingComparison">
      {!revealed ? (
        <div className="ex-stack">
          <p className="t-body text-ink-secondary">Right after studying, everything feels familiar. But what happens when you check your confidence 24 hours later?</p>
          <div className="ex-actions">
            <Button onClick={() => setRevealed(true)}>
              Reveal the Timing Effect
            </Button>
          </div>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="ex-stack">
          {/* The two charts, each on the sheet in ink (no coral or mint panel behind them) */}
          <div className="ex-figure">
            <Chart confidence={immConfidence} recall={immRecall} phases={immPhases} areaColor="var(--ink-primary)" label="Checking Straight Away" />
          </div>
          <div className="ex-figure">
            <Chart confidence={delConfidence} recall={delRecall} phases={delPhases} areaColor="var(--ink-primary)" label="Checking After 24 Hours" />
          </div>
          {/* What each one means: words you read, ruled like rows (no tinted boxes) */}
          <div className="ex-list">
            <div><p className="t-sub"><strong className="text-ink-primary">Checking straight away</strong> tricks you because everything is still fresh. The material is still "in the room." Your confidence stays high while your actual memory of it collapses — creating a dangerous blind spot.</p></div>
            <div><p className="t-sub"><strong className="text-ink-primary">Checking after a delay</strong> forces your brain to actually pull the information from memory. Your confidence drops — but it honestly reflects what you'll remember in the exam. The discomfort IS the honesty.</p></div>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// 4. TRAFFIC LIGHT AUDIT
const AUDIT_TOPICS = [
  {
    topic: 'Active Recall',
    question: 'What makes active recall more effective than re-reading?',
    options: ['It is faster to do', 'It creates desirable difficulty that strengthens retrieval pathways', 'It is less tiring on the brain', 'It covers more material per session'],
    correct: 1,
  },
  {
    topic: 'The Spacing Effect',
    question: 'Why does spacing out study sessions improve memory?',
    options: ['Your brain gets bored with the same topic', 'It gives you time to find more resources', 'Forgetting between sessions forces retrieval effort that strengthens memory', 'It reduces total study time needed'],
    correct: 2,
  },
  {
    topic: 'Interleaving',
    question: 'What is the main benefit of interleaving different topics?',
    options: ['It keeps you entertained', 'It trains your brain to discriminate between problem types', 'It covers the syllabus faster', 'It is easier than blocked practice'],
    correct: 1,
  },
  {
    topic: 'Growth Mindset',
    question: 'According to Carol Dweck, what is a growth mindset?',
    options: ['Believing you will naturally get smarter as you age', 'Setting bigger goals each year', 'Believing abilities can be developed through effort and strategy', 'Thinking positively about exams'],
    correct: 2,
  },
  {
    topic: 'Desirable Difficulties',
    question: 'Why are desirable difficulties beneficial for learning?',
    options: ['They build character and resilience', 'They make studying more enjoyable', 'Conditions that feel harder during study lead to stronger long-term retention', 'They help you study faster'],
    correct: 2,
  },
  {
    topic: 'The Forgetting Curve',
    question: 'According to Ebbinghaus, what happens to newly learned information without review?',
    options: ['It is stored permanently but becomes harder to access', 'You lose the majority within 24 hours through exponential decay', 'It stays stable for about a week then drops', 'It disappears completely after exactly 30 days'],
    correct: 1,
  },
];

type Rating = 'green' | 'amber' | 'red';

const TrafficLightAudit = () => {
  const [phase, setPhase] = useState<'rate' | 'quiz' | 'results'>('rate');
  const [ratings, setRatings] = useState<Record<number, Rating>>({});
  const [quizStep, setQuizStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});

  const handleRate = (idx: number, rating: Rating) => {
    setRatings((prev) => ({ ...prev, [idx]: rating }));
  };

  const startQuiz = () => setPhase('quiz');

  const handleQuizAnswer = (optionIdx: number) => {
    setAnswers((prev) => ({ ...prev, [quizStep]: optionIdx }));
    if (quizStep < AUDIT_TOPICS.length - 1) {
      setQuizStep((s) => s + 1);
    } else {
      setPhase('results');
    }
  };

  const reset = () => {
    setPhase('rate');
    setRatings({});
    setQuizStep(0);
    setAnswers({});
  };

  // Each light is a dot in its own colour inside a white ring you press (an ink ring once chosen); the
  // light's name is its accessible name.
  const ratingColors = {
    green: { dot: 'var(--success-hex)', label: 'Green' },
    amber: { dot: 'var(--warning-text)', label: 'Amber' },
    red: { dot: 'var(--danger-tint-ink)', label: 'Red' },
  };
  const ragRing = (chosen: boolean): React.CSSProperties => ({
    background: 'var(--surface-paper)',
    border: chosen ? '2px solid var(--ink-primary)' : '1px solid var(--outline-soft)',
  });

  if (phase === 'rate') {
    const allRated = Object.keys(ratings).length === AUDIT_TOPICS.length;
    return (
      <ExerciseSheet title="Traffic Light Audit" sub="Rate your knowledge of each concept honestly. Then we'll test you." name="TrafficLightAudit">
        {/* One row per concept, ruled by hairlines; its three lights at the right */}
        <div className="ex-list">
          {AUDIT_TOPICS.map((t, i) => (
            <div key={i} className="!flex-row items-center justify-between gap-3">
              <span className="t-body text-ink-primary">{t.topic}</span>
              <div className="flex gap-1">
                {(['green', 'amber', 'red'] as Rating[]).map((r) => (
                  <button
                    key={r}
                    type="button"
                    onClick={() => handleRate(i, r)}
                    className="w-11 h-11 rounded-full grid place-items-center"
                    style={ragRing(ratings[i] === r)} aria-pressed={!!(ratings[i] === r)} aria-label={ratingColors[r].label}
                  ><span className="block w-5 h-5 rounded-full" style={{ background: ratingColors[r].dot, opacity: ratings[i] === r ? 1 : 0.35 }} /></button>
                ))}
              </div>
            </div>
          ))}
        </div>
        {allRated && (
          <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="ex-actions">
            <Button onClick={startQuiz}>
              Now Test Me
            </Button>
          </MotionDiv>
        )}
      </ExerciseSheet>
    );
  }

  if (phase === 'quiz') {
    const t = AUDIT_TOPICS[quizStep];
    const r = ratings[quizStep];
    return (
      <ExerciseSheet title="Traffic Light Audit" name="TrafficLightAudit">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
          <span className="ex-count t-readout">Question {quizStep + 1} of {AUDIT_TOPICS.length}</span>
          <span className="t-meta inline-flex items-center gap-1.5"><span className="block w-2.5 h-2.5 rounded-full" style={{ background: ratingColors[r].dot }} aria-hidden="true" />You rated: {ratingColors[r].label}</span>
        </div>
        <AnswerGroup kind="one" legend={t.question} chooseOnArrow={false}>
          {t.options.map((opt, i) => (
            <ChoiceTile
              key={i}
              chosen={answers[quizStep] === i}
              onClick={() => handleQuizAnswer(i)}
              label={opt}
            />
          ))}
        </AnswerGroup>
      </ExerciseSheet>
    );
  }

  // Results phase
  const results = { green: { total: 0, correct: 0 }, amber: { total: 0, correct: 0 }, red: { total: 0, correct: 0 } };
  AUDIT_TOPICS.forEach((t, i) => {
    const r = ratings[i];
    results[r].total++;
    if (answers[i] === t.correct) results[r].correct++;
  });

  return <ExerciseSheet title="Your Audit Results" sub="How well did your traffic lights match reality?" name="TrafficLightAudit">
      {/* The three lights' scores in a line, on the sheet (no box round each); a tick where the light was honest */}
      <div className="grid grid-cols-3 gap-4 text-center py-3 border-y border-hairline">
        {(['green', 'amber', 'red'] as Rating[]).map((r) => {
          const pct = results[r].total > 0 ? Math.round((results[r].correct / results[r].total) * 100) : null;
          const isCalibrated = r === 'green' ? (pct !== null && pct >= 80) : r === 'red' ? true : (pct !== null && pct >= 40 && pct <= 80);
          return (
            <div key={r} className="flex flex-col items-center">
              <span className="block w-3 h-3 rounded-full mb-2" style={{ background: ratingColors[r].dot }} aria-hidden="true" />
              <p className="t-name-sm text-ink-primary">
                {results[r].total > 0 ? `${results[r].correct}/${results[r].total}` : '—'}
              </p>
              <p className="t-meta mt-1">{ratingColors[r].label} rated</p>
              {pct !== null && (
                <p className="t-meta mt-1 inline-flex items-center gap-1" style={{ color: isCalibrated ? "var(--ink-primary)" : "var(--ink-muted)" }}>
                  {isCalibrated && <AnswerTick />}{pct}% correct
                </p>
              )}
            </div>
          );
        })}
      </div>

      {results.green.total > 0 && results.green.correct < results.green.total && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
          <AnswerLine tone="note">
          You rated {results.green.total - results.green.correct} topic(s) as Green but got them wrong. These are your metacognitive blind spots — topics where you feel confident but aren't actually prepared. This is exactly what catches students in exams.
          </AnswerLine>
        </MotionDiv>
      )}

      <div className="ex-actions">
        <TextButton tone="quiet" onClick={reset}>
          Try Again
        </TextButton>
      </div>
    </ExerciseSheet>;
};

// 5. PREDICTION TRACKER
const PREDICTION_QUESTIONS = [
  { question: 'What is the capital of Australia?', options: ['Sydney', 'Melbourne', 'Canberra', 'Perth'], correct: 2 },
  { question: 'Which element has the chemical symbol Fe?', options: ['Fluorine', 'Fermium', 'Iron', 'Francium'], correct: 2 },
  { question: 'How many chromosomes do humans have?', options: ['23', '46', '48', '64'], correct: 1 },
  { question: 'What year did World War I begin?', options: ['1912', '1914', '1916', '1918'], correct: 1 },
  { question: 'What is the SI unit of force?', options: ['Joule', 'Watt', 'Newton', 'Pascal'], correct: 2 },
];

const PredictionTracker = () => {
  const [step, setStep] = useState(0);
  const [phase, setPhase] = useState<'predict' | 'answer' | 'done'>('predict');
  const [predictions, setPredictions] = useState<boolean[]>([]);
  const [answers, setAnswers] = useState<number[]>([]);

  const handlePredict = (confident: boolean) => {
    setPredictions((prev) => [...prev, confident]);
    setPhase('answer');
  };

  const handleAnswer = (idx: number) => {
    setAnswers((prev) => [...prev, idx]);
    if (step < PREDICTION_QUESTIONS.length - 1) {
      setStep((s) => s + 1);
      setPhase('predict');
    } else {
      setPhase('done');
    }
  };

  const reset = () => {
    setStep(0);
    setPhase('predict');
    setPredictions([]);
    setAnswers([]);
  };

  if (phase === 'done') {
    const results = PREDICTION_QUESTIONS.map((q, i) => ({
      question: q.question,
      predicted: predictions[i],
      actual: answers[i] === q.correct,
    }));
    const correctPredictions = results.filter((r) => r.predicted === r.actual).length;
    const accuracy = Math.round((correctPredictions / results.length) * 100);
    const overconfident = results.filter((r) => r.predicted && !r.actual).length;
    const underconfident = results.filter((r) => !r.predicted && r.actual).length;

    return (
      <ExerciseSheet title="Prediction Results" sub="How accurately did you predict your own performance?" name="PredictionTracker">
        <div className="text-center">
          <p className="t-number text-ink-primary">{accuracy}%</p>
          <p className="t-sub mt-1">Prediction Accuracy</p>
        </div>

        {/* One row per question, ruled by hairlines; a tick where the prediction held */}
        <div className="ex-list">
          {results.map((r, i) => (
            <div key={i} className="!flex-row items-center justify-between gap-3">
              <span className="t-sub" style={{ color: "var(--ink-primary)" }}>{r.question}</span>
              <div className="flex items-center gap-2 shrink-0 ml-3 t-meta">
                <span style={{ color: "var(--ink-primary)" }}>{r.actual ? 'Correct' : 'Wrong'}</span>
                <span className="inline-flex items-center gap-1">
                  {r.predicted === r.actual && <AnswerTick />}
                  {r.predicted === r.actual ? 'Predicted' : r.predicted ? 'Overconfident' : 'Underconfident'}
                </span>
              </div>
            </div>
          ))}
        </div>

        {overconfident > 0 && (
          <AnswerLine tone="note">
            You predicted correctly {overconfident} time(s) but were wrong — these are blind spots.
          </AnswerLine>
        )}
        {underconfident > 0 && (
          <AnswerLine tone="note">
            You doubted yourself {underconfident} time(s) but were actually right — trust your knowledge more.
          </AnswerLine>
        )}

        <div className="ex-actions">
          <TextButton tone="quiet" onClick={reset}>
            Try Again
          </TextButton>
        </div>
      </ExerciseSheet>
    );
  }

  const q = PREDICTION_QUESTIONS[step];

  return (
    <ExerciseSheet title="Prediction Tracker" sub="Predict first, then answer. See how well you really know what you know." name="PredictionTracker">
      <p className="ex-count t-readout">Question {step + 1} of {PREDICTION_QUESTIONS.length}</p>

      {/* The question: words you read, on the sheet (no box) */}
      <p className="ex-quote">{q.question}</p>

      {phase === 'predict' ? (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="pred">
          <AnswerGroup kind="one" legend="Do you think you'll get this right?" columns={2} chooseOnArrow={false}>
            <ChoiceTile chosen={false} onClick={() => handlePredict(true)} label="Yes, I know this" />
            <ChoiceTile chosen={false} onClick={() => handlePredict(false)} label="Not sure" />
          </AnswerGroup>
        </MotionDiv>
      ) : (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} key="ans">
          <AnswerGroup kind="one" chooseOnArrow={false}>
            {q.options.map((opt, i) => (
              <ChoiceTile
                key={i}
                chosen={false}
                onClick={() => handleAnswer(i)}
                label={opt}
              />
            ))}
          </AnswerGroup>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const TheLearningRadarModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'calibration-problem', title: 'You Don\'t Know What You Don\'t Know', eyebrow: '01 // The Blind Spot', icon: Target },
    { id: 'dunning-kruger', title: 'Why the Least Prepared Feel Most Confident', eyebrow: '02 // The Confidence Trap', icon: AlertTriangle },
    { id: 'judgements-of-learning', title: 'When to Check If You\'ve Learned Something', eyebrow: '03 // The Timing Trick', icon: Clock },
    { id: 'traffic-light-audit', title: 'The Traffic Light Audit', eyebrow: '04 // The Reality Check', icon: Layers },
    { id: 'monitoring-during-study', title: 'Checking Yourself During Study', eyebrow: '05 // The Signals', icon: Activity },
    { id: 'prediction-protocol', title: 'The Prediction Game', eyebrow: '06 // The Training Ground', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="44"
      moduleTitle="The Learning Radar"
      moduleSubtitle="Know What You Actually Know"
      moduleDescription="Most students think they know more than they do — and it costs them marks. This module shows you how to spot your blind spots and study smarter."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Scan Your Blind Spots"
      references={LEARNING_RADAR_REFERENCE_LIST}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="You Don't Know What You Don't Know." eyebrow="Step 1" icon={Target} theme={theme}>
              {essentials ? (
                <>
                  <p>Students routinely predict they'll remember far more than they actually do.<Cite n={1} /> Your brain consistently fools you into thinking you know more than you do.</p>
                  <p>This is a <strong>confidence blind spot</strong>. You cannot tell the difference between "I recognise this" and "I actually know this." This module teaches you to spot the gap.</p>
                </>
              ) : (
                <>
                  <p>Before you read another word, answer this: how confident are you that you could pass a test right now on whatever you studied most recently? Hold that number in your head. Now consider this: across many studies, <Highlight description="Researchers pooled hundreds of studies on how well people judge their own abilities. On average, people's self-assessments line up only modestly with how they actually perform." theme={theme}>researchers found</Highlight> that the link between how well students think they'll do and how they actually do is often weak — people's self-assessments line up only modestly with reality.<Cite n={1} /></p>
                  <p>Students also routinely <Highlight description="Across study after study, learners predict they'll remember far more than they actually do when tested later. That gap is your brain mistaking familiarity for real knowledge." theme={theme}>overpredict</Highlight> how much they'll recall — often by a wide margin. It means when you sit down to study and think "I know this," there's a real chance that you don't. This gap is basically a <Highlight description="When your confidence in what you know doesn't match what you can actually do. You feel like you've got it, but when it comes to the exam, you can't pull it out of your head. You can't tell the difference between 'I recognise this' and 'I actually know this.'" theme={theme}>confidence blind spot</Highlight>.</p>
                  <p>This isn't about intelligence. The smartest students can have the worst blind spots. It's a skill — and like any skill, it can be trained. This module will teach you how to build a <Highlight description="Being able to honestly tell the difference between what you actually know and what you just think you know. It's like having a built-in detector that tells you where your real gaps are." theme={theme}>Learning Radar</Highlight>: the ability to spot the difference between what you actually know and what just looks familiar.</p>
                </>
              )}
              <CalibrationQuiz />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Why the Least Prepared Feel Most Confident." eyebrow="Step 2" icon={AlertTriangle} theme={theme}>
              {essentials ? (
                <>
                  <p>People who scored worst on tests massively overestimated their results. This is the <strong>Confidence Trap</strong>: you need the same skills to judge your answer as you need to get it right.</p>
                  <p>Top performers tend to slightly underestimate themselves. They see how much more there is to learn. The least prepared student is often the most confident.</p>
                </>
              ) : (
                <>
                  <p>In 1999, two psychologists ran <Highlight description="They tested people on things like logic and grammar, then asked them to guess how well they did. The people who scored the worst massively overestimated their results. They thought they were above average when they were actually near the bottom." theme={theme}>a now-famous experiment</Highlight>.<Cite n={2} /> They tested people on things like logic and grammar, then asked everyone to guess how well they'd done compared to others. The outcome surprised everyone: the people who scored in the bottom quarter tended to think they'd finished above average. Their actual rank? Near the bottom.</p>
                  <p>But here's the really unfair part — the <Highlight description="To know whether your answer is right, you need the same skills you'd need to get it right in the first place. If you don't understand the topic, you also can't tell that you don't understand it. You're not just wrong — you're confidently wrong, and you have no idea." theme={theme}>Confidence Trap</Highlight>. The skills you need to get a question right are the exact same skills you need to recognise whether your answer is right. If you don't understand the chain rule in Maths, you also can't tell whether your attempt at it was any good. You're not just getting it wrong — you don't have the tools to know you're getting it wrong.</p>
                  <p>Meanwhile, top performers tend to slightly underestimate how well they've done. When you really know a subject, you can see how much more there is to learn, so you stay humble. This is why the most prepared student in the room is often the most nervous, while the least prepared is mysteriously confident.</p>
                </>
              )}
              <DunningKrugerCurve />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="When to Check If You've Learned Something." eyebrow="Step 3" icon={Clock} theme={theme}>
              {essentials ? (
                <>
                  <p>Never judge whether you have learned something in the same session you studied it. Right after studying, everything feels familiar. Your brain mistakes that familiarity for real knowledge.</p>
                  <p>Wait 24 hours, then check yourself. After a delay, your self-assessment becomes far more accurate.<Cite n={3} /> Come back tomorrow, close your notes, and see what you actually remember.</p>
                </>
              ) : (
                <>
                  <p>If we're so bad at judging what we know, is there a way to get better at it? Yes — and the secret is <Highlight description="The gap between when you study something and when you check whether it stuck. If you check straight away, your brain tricks you into thinking you know it. If you wait a day and then check, you get a much more honest answer." theme={theme}>timing</Highlight>. <Highlight description="Researchers found that when students guessed how well they'd learned something right after studying, their guesses were basically useless. But when they waited 24 hours and then guessed, they were almost perfectly accurate. Just by changing when you check yourself, you go from clueless to spot-on." theme={theme}>Researchers discovered</Highlight> something powerful about how we <Highlight description="Your personal prediction of whether you'll remember something on a test. Basically: 'Do I actually know this or not?' Getting good at these predictions is one of the most useful study skills you can build." theme={theme}>judge our own learning</Highlight>.</p>
                  <p>When students checked how well they'd learned something straight after studying, their self-assessment was basically worthless. But when they waited 24 hours and then checked, their self-assessments became far more accurate.<Cite n={3} /> Why? Right after studying, everything is still fresh in your short-term memory. It all feels familiar. Your brain mistakes that familiarity for real knowledge. But after 24 hours, the short-term stuff has faded. Checking yourself now forces you to actually pull information from long-term memory — and that gives you honest feedback.</p>
                  <p>The practical rule is simple: never judge whether you've learned something in the same session you studied it. Come back tomorrow, close your notes, and ask yourself what you remember. That delayed self-check is worth more than hours of confident re-reading.</p>
                </>
              )}
              <JOLTimingComparison />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Traffic Light Audit." eyebrow="Step 4" icon={Layers} theme={theme}>
              {essentials ? (
                <>
                  <p>Rate every topic on your syllabus: <strong>Green</strong> (I can explain this from memory), <strong>Amber</strong> (I sort of know it), or <strong>Red</strong> (I do not know this). Then test yourself on your Greens.</p>
                  <p>Most students find their "Greens" are actually Ambers. That is uncomfortable but incredibly useful information before an exam. Testing yourself trains your brain to be more honest.<Cite n={4} /></p>
                </>
              ) : (
                <>
                  <p>Now you know that checking yourself after a delay is more accurate — but you need an actual system to do it. The <Highlight description="A simple system where you go through every topic on your syllabus and rate it Green (I could explain this from memory right now), Amber (I sort of know it but couldn't fully explain it), or Red (I'm lost on this). Then you test yourself on the Greens to see if you're being honest." theme={theme}>Traffic Light Audit</Highlight> is that system. It works in two steps: rate yourself, then test yourself.</p>
                  <p><Highlight description="Studies showed that students who tested themselves after rating their own confidence became way better at knowing what they actually knew. Testing yourself doesn't just check your knowledge — it trains your brain to be more honest about what's really sticking." theme={theme}>Research shows</Highlight> that students who test themselves after rating their knowledge get dramatically better at judging what they actually know.<Cite n={4} /> Testing doesn't just measure your knowledge — it trains your brain to be more honest. You start to learn the difference between "I recognise this" (Amber) and "I could actually explain this in an exam" (Green).</p>
                  <p>Here's how it works: take your subject syllabus and rate every topic Green, Amber, or Red. Green means "I could explain this to someone from memory." Amber means "I sort of know it but couldn't fully explain it." Red means "I don't know this." Then — and this is the key step — test yourself on your Greens. Most students discover that loads of their "Greens" are actually Ambers when put to the test. That's uncomfortable, but it's the most useful information you can have before an exam.</p>
                </>
              )}
              <TrafficLightAudit />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Checking Yourself During Study." eyebrow="Step 5" icon={Activity} theme={theme}>
              {essentials ? (
                <p>Build self-checking into every study session.<Cite n={5} /> After each section, close the book and list the key ideas from memory. If you cannot, you were reading on autopilot. Use these three checks: close the book test, make your own example test, and connect the dots test.</p>
              ) : (
                <>
                  <p>Your Learning Radar isn't just something you use once — it's a habit you can build into every single study session. <Highlight description="Research shows that the best students don't just read their notes — they're constantly checking in with themselves: 'Am I actually taking this in, or am I just staring at the page?' That habit is what separates real studying from wasted time." theme={theme}>Research shows</Highlight> that the best learners constantly check their own understanding while studying.<Cite n={5} /> They don't just read — they keep asking themselves: "Am I actually learning this, or just looking at it?"</p>
                  <p>There are clear signals that tell you whether you're actually learning or just going through the motions. <Highlight description="If you can close your book and list the key ideas from what you just studied, the information is actually going in. If you can't, you've basically been staring at the page without absorbing anything. It's a quick and honest test." theme={theme}>One powerful trick</Highlight>: after studying a section, try to list the key ideas from memory. If you've been studying a chapter and you can close the book and name the five main points, you're on track. If you can't, you've been reading without learning.</p>
                  <p>Here are three quick checks you can use during any study session.</p>
                </>
              )}
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "The \"Close the Book\" Test", description: "Close your notes and try to say or write down everything you just studied. If you can hit the main points, it's working. If your mind goes blank, you were reading on autopilot and need to change your approach." },
                  { number: 2, term: "The \"Make Your Own Example\" Test", description: "Try to come up with your own example of what you just learned. If you can, it means you actually understand the idea, not just the specific case you read about." },
                  { number: 3, term: "The \"Connect the Dots\" Test", description: "Try to connect what you just learned to something you already know. If you can make that link, the new information is sticking to what's already in your brain, which makes it way harder to forget." },
                ]}
                accentNote="If you can do all three, you're genuinely learning. If you can't, you're in the familiarity trap — and now you know to switch up your approach."
              />
              <PersonalStory name="Ciara" role="5th Year, Cork" junior={{ name: 'Ciara', role: '2nd Year, Cork', children: (
                <>I used to spend hours reading my Science notes and feel grand about it. Then I tried the "Close the Book" test and I literally couldn't remember a single thing I'd just read. It was a shock. Now I stop every 20 minutes and try to write down the main points without looking. It's way harder but I actually remember stuff for tests now.</>
              ) }}>
                I used to spend hours reading my Biology notes and feel grand about it. Then I tried the "Close the Book" test and I literally couldn't remember a single thing I'd just read. It was a shock. Now I stop every 20 minutes and try to write down the main points without looking. It's way harder but I actually remember stuff for tests now.
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Prediction Game." eyebrow="Step 6" icon={Flag} theme={theme}>
              {essentials ? (
                <>
                  <p>Before every test, predict your score. Write it down. After the test, compare your prediction to your actual result. That gap is your <strong>prediction gap</strong>.</p>
                  <p>Students who do this get noticeably better at predicting their performance over time.<Cite n={4} /> The habit tends to carry over to other subjects too — train it in Maths and it can help you in History.</p>
                </>
              ) : (
                <>
                  <p>The best way to train your Learning Radar? Start predicting. <Highlight description="Researchers tracked students who predicted their exam scores before each test throughout a whole school year. By the end, they had got noticeably better at predicting their own performance. Just by guessing your score and then seeing how close you were, your brain gets better and better at knowing what it actually knows." theme={theme}>Researchers</Highlight> tracked students who predicted their exam scores before each test and then compared their predictions to reality. By the end of the year, their predictions had become noticeably more accurate.<Cite n={4} /> The simple act of guessing your score and seeing how close you were trained their brain to be more honest with itself.</p>
                  <p>What's more, <Highlight description="Students who practised predicting their scores in one subject often got better at knowing what they knew in other subjects too. It behaves less like a one-topic trick and more like a general habit you can build." theme={theme}>this habit tends to carry over</Highlight>. Students who practised predicting in one subject often showed better self-awareness in other subjects too. It behaves less like a one-topic trick and more like a general habit — train it in Maths and it can help you in History too.</p>
                  <p>Here's the game: before every test, mock exam, or practice paper, predict your score for each section. Write it down. After the test, compare your predictions to your actual results. The gap between what you predicted and what you got is your <Highlight description="The difference between what you predicted you'd score and what you actually scored. Track this number over time. As it gets smaller, you're getting better at knowing what you know — which means you spend your study time on the stuff that actually needs work instead of wasting it." theme={theme}>prediction gap</Highlight>. Track it over time. Watch it shrink. That shrinking gap means your Learning Radar is getting sharper — and it means every hour you spend studying is targeted at the right material, not wasted on topics you only think you need to review.</p>
                </>
              )}
              <PredictionTracker />
              <MicroCommitment theme={theme}>
                <p>Before your next study session, take 2 minutes to rate your top 5 exam topics as Green, Amber, or Red. Then test yourself on one of your "Greens" — close your notes and try to explain it from memory. If you stumble, congratulations: you've just found a blind spot that would have cost you marks. That's your Learning Radar in action.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheLearningRadarModule;
