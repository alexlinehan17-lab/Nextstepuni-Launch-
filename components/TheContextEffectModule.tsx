import { BrandedLocationScore } from './learning/WideFeatures';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { AnimatePresence,motion } from 'framer-motion';
import { Activity,Brain,Map,Repeat,Wrench } from 'lucide-react';
import React,{ useState } from 'react';
import { CONTEXT_EFFECT_REFERENCE_LIST } from '../data/references/contextEffect';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { purpleTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,ExerciseLabel,ExercisePart,ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';
import { ChoiceTile } from './ui/Choice';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

// 1. CONTEXT MEMORY COMPARISON (Planning Paradox style dual-chart)
const ContextMemoryComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 21', 'Day 30'];

  // Both charts share the same encoding strength
  const encodingStrength = [0.40, 0.55, 0.65, 0.72, 0.78, 0.82];

  // Same context: retrieval tracks closely
  const sameRetrieval = [0.35, 0.50, 0.60, 0.68, 0.72, 0.78];

  // Different context: retrieval drops significantly
  const diffRetrieval = [0.35, 0.42, 0.40, 0.38, 0.35, 0.30];

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

  const samePhases = [
    { label: 'Building', x1: 0, x2: 0.33, color: "var(--ink-secondary)" },
    { label: 'Strengthening', x1: 0.33, x2: 0.66, color: "var(--ink-secondary)" },
    { label: 'Accessible', x1: 0.66, x2: 1, color: "var(--ink-secondary)" },
  ];
  const diffPhases = [
    { label: 'Building', x1: 0, x2: 0.33, color: "var(--ink-secondary)" },
    { label: 'Cues missing', x1: 0.33, x2: 0.66, color: "var(--ink-secondary)" },
    { label: 'Inaccessible', x1: 0.66, x2: 1, color: "var(--ink-secondary)" },
  ];

  // Learning strength solid ink, recall a dashed ink-2 line, a flat fill under learning strength (no
  // gradient); text in the one typeface, 11 or more.
  const font = { fontFamily: 'var(--font-ui)' };
  const Chart = ({ encoding, retrieval, phases, areaColor, label }: {
    encoding: number[]; retrieval: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
      {[0.25, 0.5, 0.75, 1.0].map((v) => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--ink-muted)" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--ink-muted)" strokeOpacity="0.3" />

      {/* Encoding area */}
      <motion.path d={buildArea(encoding)} fill={areaColor} fillOpacity="0.08" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />
      {/* Encoding line (solid) */}
      <motion.path d={buildLine(encoding)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut' }} />
      {/* Retrieval line (dashed) */}
      <motion.path d={buildLine(retrieval)} fill="none" stroke="var(--ink-secondary)" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }} />
      {/* Encoding dots */}
      {encoding.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (encoding.length - 1))} cy={toY(v)} r="3.5" fill={areaColor} initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }} />
      ))}

      <text x={padL + 2} y={toY(1.0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>Low</text>
      {/* Day labels (the first and last sit inside the drawing) */}
      {xLabels.map((m, i) => (
        <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="11" fill="var(--ink-muted)" textAnchor={i === 0 ? 'start' : i === xLabels.length - 1 ? 'end' : 'middle'} style={font}>{m}</text>
      ))}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 30} fontSize="11" fill={p.color} textAnchor="middle" style={font}>{p.label}</text>
      ))}
      <text x={padL} y={15} fontSize="11" fill="var(--ink-primary)" style={font}>{label}</text>
      <line x1={W - padR - 198} x2={W - padR - 182} y1={11} y2={11} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 178} y={15} fontSize="11" fill="var(--ink-muted)" style={font}>Learning Strength</text>
      <line x1={W - padR - 60} x2={W - padR - 44} y1={11} y2={11} stroke="var(--ink-secondary)" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR} y={15} fontSize="11" fill="var(--ink-muted)" textAnchor="end" style={font}>Recall</text>
    </svg>
  );

  return (
    <ExercisePart title="How Your Study Spot Affects Your Memory" sub="What happens to your memory when the environment changes?">
      {!revealed ? (
        <div className="ex-stack">
          <p className="t-body text-ink-secondary">You study perfectly in your bedroom. But what happens when you sit down in the exam hall?</p>
          <div className="ex-actions">
            <Button onClick={() => setRevealed(true)}>
              See the Context Effect
            </Button>
          </div>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="ex-stack">
          {/* The two charts, each on the sheet in ink (no coral or mint panel behind them) */}
          <div className="ex-figure">
            <Chart encoding={encodingStrength} retrieval={sameRetrieval} phases={samePhases} areaColor="var(--ink-primary)" label="Same Context (Study & Test)" />
          </div>
          <div className="ex-figure">
            <Chart encoding={encodingStrength} retrieval={diffRetrieval} phases={diffPhases} areaColor="var(--ink-primary)" label="Different Context (Study vs Test)" />
          </div>
          {/* What each one means: words you read, ruled like rows (no tinted boxes) */}
          <div className="ex-list">
            <div><p className="t-sub"><strong className="text-ink-primary">Same-place recall</strong> works because familiar surroundings help your brain find what it learned. But exams are in a DIFFERENT place. If your memories depend on your study spot, they become fragile.</p></div>
            <div><p className="t-sub"><strong className="text-ink-primary">When the exam hall strips away all your familiar clues</strong>, place-dependent memories become unreachable. You need knowledge that works anywhere, not just in your bedroom.</p></div>
          </div>
        </MotionDiv>
      )}
    </ExercisePart>
  );
};

// 2. CONTEXT CUE EXPLORER (Section 1 interactive)
const CUE_ICONS: Record<string, React.ReactNode> = {
  music: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>,
  desk: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>,
  coffee: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>,
  pet: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>,
  window: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="12" y1="3" x2="12" y2="21"/></svg>,
  lamp: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>,
  silence: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>,
  clock: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
  people: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>,
  notes: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>,
  snacks: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 002 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>,
  hoodie: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M20.38 3.46L16 2a4 4 0 01-8 0L3.62 3.46a2 2 0 00-1.34 2.23l.58 3.57a1 1 0 00.99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 002-2V10h2.15a1 1 0 00.99-.84l.58-3.57a2 2 0 00-1.34-2.23z"/></svg>,
};

const STUDY_CUES = [
  { id: 'music', label: 'Music playing', survivesExam: false },
  { id: 'desk', label: 'Familiar desk', survivesExam: false },
  { id: 'coffee', label: 'Coffee / tea', survivesExam: false },
  { id: 'pet', label: 'Pet nearby', survivesExam: false },
  { id: 'window', label: 'Window view', survivesExam: false },
  { id: 'lamp', label: 'Desk lamp', survivesExam: false },
  { id: 'silence', label: 'Silence', survivesExam: true },
  { id: 'clock', label: 'Clock ticking', survivesExam: true },
  { id: 'people', label: 'Other people', survivesExam: true },
  { id: 'notes', label: 'Written notes', survivesExam: false },
  { id: 'snacks', label: 'Snacks', survivesExam: false },
  { id: 'hoodie', label: 'Comfy hoodie', survivesExam: true },
];

const ContextCueExplorer = () => {
  const [selectedCues, setSelectedCues] = useState<Set<string>>(new Set());
  const [revealed, setRevealed] = useState(false);

  const toggleCue = (id: string) => {
    if (revealed) return;
    setSelectedCues((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectedCount = selectedCues.size;
  const survivingCount = STUDY_CUES.filter((c) => selectedCues.has(c.id) && c.survivesExam).length;
  const lostPercent = selectedCount > 0 ? Math.round(((selectedCount - survivingCount) / selectedCount) * 100) : 0;

  return (
    <ExercisePart title="Your Study Environment Audit" sub="Pick the things that are around you when you study, then see how many of them will be there in the exam hall.">
      {/* The cues: answers you can choose several of, each with its bare glyph */}
      <AnswerGroup kind="several" columns={2}>
        {STUDY_CUES.map((cue) => {
          const isSelected = selectedCues.has(cue.id);
          return (
            <ChoiceTile
              key={cue.id}
              kind="several"
              chosen={isSelected}
              onClick={() => toggleCue(cue.id)}
              className={revealed ? 'cursor-default' : undefined}
              label={<span className="inline-flex items-center gap-2"><span className="ex-icon">{CUE_ICONS[cue.id]}</span>{cue.label}</span>}
            />
          );
        })}
      </AnswerGroup>

      {selectedCount > 0 && !revealed && (
        <div className="ex-stack items-center">
          <p className="ex-count t-readout">{selectedCount} cue{selectedCount !== 1 ? 's' : ''} selected</p>
          <Button onClick={() => setRevealed(true)}>
            See the Exam Hall
          </Button>
        </div>
      )}

      <AnimatePresence>
        {revealed && (
          <MotionDiv initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.5 }} className="ex-stack">
            {/* The two places, each under a hairline with its cues as plain words (no boxes, no chips) */}
            <div className="grid md:grid-cols-2 gap-4">
              {/* Study room */}
              <div className="ex-block">
                <p className="ex-block-title">Your Study Room — {selectedCount} cues</p>
                <ul className="flex flex-wrap gap-x-4 gap-y-1.5">
                  {STUDY_CUES.filter((c) => selectedCues.has(c.id)).map((c) => (
                    <li key={c.id} className="inline-flex items-center gap-1.5 t-sub">
                      <span className="ex-icon">{CUE_ICONS[c.id]}</span> {c.label}
                    </li>
                  ))}
                </ul>
              </div>
              {/* Exam hall */}
              <div className="ex-block">
                <p className="ex-block-title">The Exam Hall — {survivingCount} cue{survivingCount !== 1 ? 's' : ''} remain</p>
                <ul className="flex flex-wrap gap-x-4 gap-y-1.5">
                  {STUDY_CUES.filter((c) => selectedCues.has(c.id) && c.survivesExam).map((c) => (
                    <li key={c.id} className="inline-flex items-center gap-1.5 t-sub">
                      <span className="ex-icon">{CUE_ICONS[c.id]}</span> {c.label}
                    </li>
                  ))}
                  {survivingCount === 0 && (
                    <li className="t-sub">Nothing matches — your brain has zero familiar clues to help you remember</li>
                  )}
                </ul>
              </div>
            </div>

            {/* Stacked bar: what survives in ink, what is lost a hairline tone */}
            <div className="flex flex-col gap-1.5">
              <ExerciseLabel>Memory clues that survive</ExerciseLabel>
              <div className="flex" style={{ border: "1px solid var(--outline-soft)", borderRadius: 100, height: 28, overflow: 'hidden' }}>
                {survivingCount > 0 && (
                  <MotionDiv className="h-full flex items-center justify-center" style={{ backgroundColor: "var(--ink-primary)" }} initial={{ width: 0 }} animate={{ width: `${100 - lostPercent}%` }} transition={{ duration: 0.8, ease: 'easeOut' }}>
                    {(100 - lostPercent) > 15 && <span className="t-meta" style={{ color: "var(--surface-paper)" }}>{100 - lostPercent}% survive</span>}
                  </MotionDiv>
                )}
                <MotionDiv className="h-full flex items-center justify-center" style={{ backgroundColor: "var(--hairline)" }} initial={{ width: 0 }} animate={{ width: `${lostPercent}%` }} transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}>
                  {lostPercent > 15 && <span className="t-meta" style={{ color: "var(--ink-primary)" }}>{lostPercent}% lost</span>}
                </MotionDiv>
              </div>
            </div>

            <AnswerLine tone="note">
                <strong>You lost {lostPercent}% of the clues your brain uses to remember.</strong>{' '}
                {lostPercent >= 75
                  ? 'Your memories are tied tightly to your study spot. Studying in different places would help your brain remember without needing those clues.'
                  : lostPercent >= 50
                  ? 'More than half your clues disappear in the exam hall. Switching up your study spots would make a big difference.'
                  : 'Some clues still survive, but mixing up where you study would make your knowledge even stronger.'}
            </AnswerLine>
          </MotionDiv>
        )}
      </AnimatePresence>
    </ExercisePart>
  );
};

// 3. NOISE LEVEL CURVE
const NoiseLevelCurve = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 480, H = 280;
  const padL = 50, padR = 20, padT = 30, padB = 60;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const noiseLabels = ['Silent', 'Whisper', 'Library', 'Cafe', 'Office', 'Traffic', 'Concert'];

  // Inverted-U bell curve: rises to peak at Cafe (~index 3), then drops
  const curvePoints = [
    { x: 0, y: 0.30 },
    { x: 0.083, y: 0.42 },
    { x: 0.167, y: 0.58 },
    { x: 0.25, y: 0.75 },
    { x: 0.333, y: 0.88 },
    { x: 0.417, y: 0.95 },
    { x: 0.50, y: 0.97 },  // Peak (Cafe)
    { x: 0.583, y: 0.92 },
    { x: 0.667, y: 0.78 },
    { x: 0.75, y: 0.55 },
    { x: 0.833, y: 0.35 },
    { x: 0.917, y: 0.20 },
    { x: 1.0, y: 0.12 },
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

  // Focused/analytical peak is slightly quieter (Library zone ~0.30)
  const focusedPeakX = 0.30;
  const focusedPeakY = 0.82;
  // Creative/conceptual peak is slightly louder (Cafe zone ~0.50)
  const creativePeakX = 0.50;
  const creativePeakY = 0.97;

  // The curve in ink: the sweet spot a faint ink band under a dashed line, its label at the foot of the band
  // beside the other zones'; the two markers' labels are plain text (no pills), inside the drawing. Text in
  // the one typeface, 11 or more.
  const font = { fontFamily: 'var(--font-ui)' };

  return (
    <ExercisePart label="Research Evidence" title="The Noise-Performance Curve" sub="How noise level affects how well your brain performs.">
      {!revealed ? (
        <div className="ex-stack">
          <p className="t-body text-ink-secondary">Is silence always best for studying? Or does a little noise actually help?</p>
          <div className="ex-actions">
            <Button onClick={() => setRevealed(true)}>
              See the Noise Curve
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
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--hairline)" strokeWidth="1" />
              ))}
              <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--ink-muted)" strokeWidth="1.5" />
              <line x1={padL} y1={padT} x2={padL} y2={toY(0)} stroke="var(--ink-muted)" strokeWidth="1.5" />

              {/* Sweet spot zone */}
              <rect x={toX(0.22)} y={padT} width={toX(0.62) - toX(0.22)} height={chartH} fill="var(--ink-primary)" fillOpacity="0.04" rx="4" />
              <rect x={toX(0.22)} y={padT} width={toX(0.62) - toX(0.22)} height={chartH} fill="none" stroke="var(--outline-soft)" strokeWidth="1" strokeDasharray="4 3" rx="4" />

              {/* Zone labels */}
              <text x={toX(0.08)} y={toY(0.05)} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" style={font}>Too quiet</text>
              <text x={toX(0.88)} y={toY(0.05)} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" style={font}>Too loud</text>

              {/* Sweet spot label — at the foot of the band, clear of the curve */}
              <text x={toX(0.42)} y={toY(0.05)} fontSize="11" fill="var(--ink-primary)" textAnchor="middle" style={font}>Sweet spot</text>

              {/* Area fill */}
              <motion.path d={buildArea(curvePoints)} fill="var(--ink-primary)" fillOpacity="0.05" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />

              {/* Curve line */}
              <motion.path d={buildCurve(curvePoints)} fill="none" stroke="var(--ink-primary)" strokeWidth="3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, ease: 'easeOut' }} />

              {/* Focused/Analytical marker — offset left to avoid overlap */}
              <motion.circle cx={toX(focusedPeakX)} cy={toY(focusedPeakY)} r="6" fill="var(--ink-primary)" stroke="var(--surface-paper)" strokeWidth="2.5" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 1.0 }} />
              <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}>
                <line x1={toX(focusedPeakX)} y1={toY(focusedPeakY) - 8} x2={toX(focusedPeakX) - 30} y2={toY(focusedPeakY) - 30} stroke="var(--ink-muted)" strokeWidth="1" />
                <text x={toX(focusedPeakX) - 30} y={toY(focusedPeakY) - 34} fontSize="11" fill="var(--ink-primary)" textAnchor="middle" style={font}>Focused tasks</text>
              </motion.g>

              {/* Creative/Conceptual marker — offset right, its label kept inside the top of the drawing */}
              <motion.circle cx={toX(creativePeakX)} cy={toY(creativePeakY)} r="6" fill="var(--ink-primary)" stroke="var(--surface-paper)" strokeWidth="2.5" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 1.3 }} />
              <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 }}>
                <line x1={toX(creativePeakX) + 6} y1={toY(creativePeakY) - 7} x2={toX(creativePeakX) + 22} y2={toY(creativePeakY) - 16} stroke="var(--ink-muted)" strokeWidth="1" />
                <text x={toX(creativePeakX) + 26} y={toY(creativePeakY) - 14} fontSize="11" fill="var(--ink-primary)" textAnchor="start" style={font}>Creative tasks</text>
              </motion.g>

              {/* X-axis labels (the last ends inside the drawing) */}
              {noiseLabels.map((label, i) => (
                <text key={label} x={i === noiseLabels.length - 1 ? toX(1) + 12 : toX(i / (noiseLabels.length - 1))} y={toY(0) + 16} fontSize="11" fill="var(--ink-muted)" textAnchor={i === noiseLabels.length - 1 ? 'end' : 'middle'} style={font}>{label}</text>
              ))}

              {/* Axis labels */}
              <text x={W / 2} y={H - 4} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" letterSpacing="0.05em" style={font}>Noise Level →</text>
              <text x={12} y={H / 2} fontSize="11" fill="var(--ink-muted)" textAnchor="middle" letterSpacing="0.05em" transform={`rotate(-90, 12, ${H / 2})`} style={font}>Performance →</text>
              <text x={padL + 2} y={toY(1.0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>High</text>
              <text x={padL + 2} y={toY(0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>Low</text>
            </svg>
          </div>

          {/* The two kinds of task: words you read, ruled like rows, each with its bare glyph (no side stripe) */}
          <div className="ex-list">
            <div className="!flex-row items-start gap-3">
              <span className="ex-icon mt-0.5"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }}><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg></span>
              <p className="t-sub"><strong className="text-ink-primary">Focused tasks</strong> (maths problems, memorisation) work best in quiet spots. Silence lets you concentrate without distraction.</p>
            </div>
            <div className="!flex-row items-start gap-3">
              <span className="ex-icon mt-0.5"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }}><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0018 8 6 6 0 006 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 018.91 14"/></svg></span>
              <p className="t-sub"><strong className="text-ink-primary">Creative tasks</strong> (understanding concepts, making connections) benefit from a bit of background noise. The buzz of a cafe nudges your brain into bigger-picture thinking.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </ExercisePart>
  );
};

// 4. TASK ENVIRONMENT MATCHER (Section 3 interactive)
const TASK_ITEMS = [
  { id: 'maths', label: 'Maths past paper', correct: 'quiet' as const, reason: 'Maths needs careful step-by-step focus — noise breaks your concentration when you need it most.' },
  { id: 'history', label: 'History essay planning', correct: 'moderate' as const, reason: 'Essay planning is creative work — a bit of background noise actually helps you think more broadly.' },
  { id: 'vocab', label: 'Language vocabulary drill', correct: 'quiet' as const, reason: 'Memorising vocab needs sharp focus — even a little noise makes it harder to lock new words into your memory.' },
  { id: 'physics', label: 'Physics concept mapping', correct: 'moderate' as const, reason: 'Connecting physics ideas is creative thinking — some background noise nudges your brain into bigger-picture mode.' },
  { id: 'chem', label: 'Chemistry equation balancing', correct: 'quiet' as const, reason: 'Balancing equations is precise, step-by-step work — noise pulls your attention away from the details.' },
  { id: 'english', label: 'English literature analysis', correct: 'moderate' as const, reason: 'Analysing literature means making connections between ideas — a bit of noise helps your brain think more creatively.' },
];

const TaskEnvironmentMatcher = () => {
  const [answers, setAnswers] = useState<Record<string, 'quiet' | 'moderate'>>({});
  const [submitted, setSubmitted] = useState(false);

  const allAnswered = TASK_ITEMS.every((t) => answers[t.id]);
  const score = submitted ? TASK_ITEMS.filter((t) => answers[t.id] === t.correct).length : 0;

  const setAnswer = (id: string, val: 'quiet' | 'moderate') => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [id]: val }));
  };

  return (
    <ExercisePart title="Match the Task to the Environment" sub="For each study task, decide: quiet or moderate noise?">
      <div className="ex-questions">
        {TASK_ITEMS.map((task) => {
          const answer = answers[task.id];
          const isCorrect = submitted && answer === task.correct;
          const _isWrong = submitted && answer !== task.correct;
          return (
            <div key={task.id} className="ex-stack">
              <AnswerGroup kind="one" legend={task.label} columns={2}>
                <ChoiceTile
                  chosen={answer === 'quiet'}
                  onClick={() => setAnswer(task.id, 'quiet')}
                  className={submitted ? 'cursor-default' : 'cursor-pointer'}
                  label="Quiet"
                />
                <ChoiceTile
                  chosen={answer === 'moderate'}
                  onClick={() => setAnswer(task.id, 'moderate')}
                  className={submitted ? 'cursor-default' : 'cursor-pointer'}
                  label="Moderate Noise"
                />
              </AnswerGroup>
              {submitted && (
                <MotionDiv initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} transition={{ duration: 0.3 }}>
                  {/* The mark and the reason, in ink (the tick green, the cross quiet) */}
                  <div className="flex items-start gap-2">
                    <span className="t-sub" style={{ color: isCorrect ? "var(--success-hex)" : "var(--ink-muted)" }}>
                      {isCorrect ? '✓' : '✗'}
                    </span>
                    <p className="t-sub">
                      <strong className="text-ink-primary">
                        {isCorrect ? 'Correct' : `Correct answer: ${task.correct === 'quiet' ? 'Quiet' : 'Moderate Noise'}`}
                      </strong>{' — '}
                      {task.reason}
                    </p>
                  </div>
                </MotionDiv>
              )}
            </div>
          );
        })}
      </div>

      {!submitted && allAnswered && (
        <div className="ex-actions">
          <Button onClick={() => setSubmitted(true)}>
            Check My Answers
          </Button>
        </div>
      )}

      <AnimatePresence>
        {submitted && (
          <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }} className="ex-result">
            <p className="ex-result-name">{score}/{TASK_ITEMS.length}</p>
            <AnswerLine tone={score >= 5 ? 'ok' : 'note'}>
                {score === 6
                  ? 'Perfect! You understand exactly how to match tasks to environments.'
                  : score >= 4
                  ? 'Strong intuition — the key principle is: focused/precise tasks need quiet, creative/conceptual tasks benefit from moderate noise.'
                  : 'The rule of thumb: if a task needs precise, step-by-step processing, choose quiet. If it involves making connections or creative thinking, moderate noise helps.'}
            </AnswerLine>
          </MotionDiv>
        )}
      </AnimatePresence>
    </ExercisePart>
  );
};

// 5. STUDY LOCATION PLANNER (Section 5 interactive)
const PLANNER_SUBJECTS = ['Biology', 'Maths', 'English', 'History'];
const PLANNER_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
const PLANNER_LOCATIONS = [
  { id: 'none', label: '—' },
  { id: 'bedroom', label: 'Bedroom' },
  { id: 'kitchen', label: 'Kitchen' },
  { id: 'library', label: 'Library' },
  { id: 'cafe', label: 'Cafe' },
  { id: 'school', label: 'School' },
];

const StudyLocationPlanner = () => {
  // grid[subjectIndex][dayIndex] = locationIndex (0=none, 1-5=locations)
  const [grid, setGrid] = useState<number[][]>(
    PLANNER_SUBJECTS.map(() => PLANNER_DAYS.map(() => 0))
  );
  const [scored, setScored] = useState(false);

  const cycleCell = (si: number, di: number) => {
    if (scored) return;
    setGrid((prev) => {
      const next = prev.map((row) => [...row]);
      next[si][di] = (next[si][di] + 1) % PLANNER_LOCATIONS.length;
      return next;
    });
  };

  const getSubjectScore = (subjectRow: number[]): number => {
    const usedLocations = new Set(subjectRow.filter((v) => v > 0));
    const filledDays = subjectRow.filter((v) => v > 0).length;
    if (filledDays <= 1) return 0;
    // Score = unique locations / filled days, scaled to 100
    return Math.round((usedLocations.size / filledDays) * 100);
  };

  const subjectScores = grid.map(getSubjectScore);
  const hasAnyFilled = grid.some((row) => row.some((v) => v > 0));
  const overallScore = Math.round(subjectScores.reduce((a, b) => a + b, 0) / PLANNER_SUBJECTS.length);

  const getVerdict = (score: number): { label: string } => {
    if (score >= 80) return { label: 'Great variety (strong)' };
    if (score >= 50) return { label: 'Some variety' };
    return { label: 'Stuck in one spot (risky)' };
  };

  return <ExerciseSheet title="Your Weekly Location Planner" sub="Click each cell to assign a study location. Mix up your spots across the week so your knowledge works anywhere." name="StudyLocationPlanner">
      {/* Planner grid: each cell a white box with a line you press; a planned cell an ink outline */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-center">
          <thead>
            <tr>
              <th className="p-2 text-left w-24"></th>
              {PLANNER_DAYS.map((day) => (
                <th key={day} className="p-2 t-label text-ink-muted">{day}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PLANNER_SUBJECTS.map((subject, si) => (
              <tr key={subject}>
                <td className="p-2 t-sub text-left" style={{ color: "var(--ink-primary)" }}>{subject}</td>
                {PLANNER_DAYS.map((_, di) => {
                  const loc = PLANNER_LOCATIONS[grid[si][di]];
                  const planned = grid[si][di] > 0;
                  return (
                    <td key={di} className="p-1">
                      <button
                        type="button"
                        onClick={() => cycleCell(si, di)}
                        className={`w-full min-h-[44px] min-w-[44px] px-1 text-[11px] leading-[14px] ${scored ? 'cursor-default' : 'cursor-pointer'}`}
                        style={{
                          minHeight: 44,
                          backgroundColor: "var(--surface-paper)",
                          border: planned ? "1.5px solid var(--ink-primary)" : "1px solid var(--outline-soft)",
                          borderRadius: 'var(--r-sm)',
                          color: planned ? "var(--ink-primary)" : "var(--ink-muted)",
                        }} aria-label={PLANNER_SUBJECTS[si] + ', ' + PLANNER_DAYS[di] + ': ' + loc.label} disabled={scored}
                      >
                        {loc.label}
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend: the places a cell cycles through, as plain words */}
      <div className="flex flex-wrap justify-center gap-x-3 gap-y-1 t-meta">
        {PLANNER_LOCATIONS.slice(1).map((loc) => (
          <span key={loc.id}>
            {loc.label}
          </span>
        ))}
      </div>

      {hasAnyFilled && !scored && (
        <div className="ex-actions">
          <Button onClick={() => setScored(true)}>
            See My Score
          </Button>
        </div>
      )}

      <AnimatePresence>
        {scored && (
          <MotionDiv initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.5 }} className="ex-stack">
            <BrandedLocationScore score={overallScore}/>

            {/* One row per subject, ruled by hairlines: its bar (green once the variety is strong), score and verdict */}
            <div className="ex-list">
              {PLANNER_SUBJECTS.map((subject, si) => {
                const s = subjectScores[si];
                const v = getVerdict(s);
                const filledDays = grid[si].filter((val) => val > 0).length;
                return (
                  <div key={subject} className="!flex-row items-center gap-3">
                    <span className="t-sub w-20" style={{ color: "var(--ink-primary)" }}>{subject}</span>
                    <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: "var(--hairline)" }}>
                      <MotionDiv
                        className="h-full rounded-full"
                        style={{ backgroundColor: s >= 80 ? "var(--success-hex)" : "var(--ink-primary)" }}
                        initial={{ width: 0 }}
                        animate={{ width: `${s}%` }}
                        transition={{ duration: 0.6, ease: 'easeOut' }}
                      />
                    </div>
                    <span className="t-readout w-8 text-right text-ink-muted">{s}%</span>
                    <span className="t-meta w-44 text-right" style={{ color: filledDays === 0 ? "var(--ink-muted)" : "var(--ink-primary)" }}>
                      {filledDays === 0 ? 'No sessions planned' : v.label}
                    </span>
                  </div>
                );
              })}
            </div>

            <AnswerLine tone={overallScore >= 70 ? 'ok' : 'note'}>
                {overallScore >= 70
                  ? <><strong>Excellent variety!</strong> Your study plan means your knowledge will work anywhere, including the exam hall.</>
                  : overallScore >= 40
                  ? <><strong>Good start, but more variety would help.</strong> Try adding a second or third spot for each subject so your memories are not tied to one place.</>
                  : <><strong>Your knowledge is stuck in one spot.</strong> Each subject should be studied in at least 2 different places across the week so you can remember it anywhere.</>
                }
            </AnswerLine>
          </MotionDiv>
        )}
      </AnimatePresence>
    </ExerciseSheet>;
};

// --- MODULE COMPONENT ---
const TheContextEffectModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'context-dependent-memory', title: 'Why You Blank in the Exam Hall', eyebrow: '01 // The Problem', icon: Map },
    { id: 'variation-advantage', title: "The 'Switch It Up' Fix", eyebrow: '02 // The Solution', icon: Repeat },
    { id: 'noise-question', title: 'Does Noise Help or Hurt?', eyebrow: '03 // The Noise Question', icon: Activity },
    { id: 'encoding-variability', title: 'Why Switching Spots Works', eyebrow: '04 // How It Works', icon: Brain },
    { id: 'designing-environments', title: 'Setting Up Your Study Rotation', eyebrow: '05 // Your Game Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="49"
      moduleTitle="The Context Effect"
      moduleSubtitle="Where You Study Matters"
      moduleDescription="Where you study changes what you remember. Learn why switching study spots beats sticking to one 'perfect' place."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Switch It Up"
      references={CONTEXT_EFFECT_REFERENCE_LIST}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why You Blank in the Exam Hall." eyebrow="Step 1" icon={Map} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain links what you learn to where you learn it. The room, the sounds, the lighting all become memory clues. People tested in the same place they studied tend to recall noticeably more.<Cite n={1} /></p>
                  <p>This is why you blank in the exam hall. It strips away every familiar clue your brain was relying on. The knowledge is still there -- your brain just cannot find the path to it.</p>
                </>
              ) : (
                <>
                  <p>In one of psychology's most famous experiments, divers learned word lists either underwater or on dry land, then were tested in either the same or a different environment. The result? Those tested in the <Highlight description="The place where you study — the room, the sounds, the lighting — all get tangled up with what you learn. Your brain links the info to the surroundings, so the same surroundings help you remember." theme={theme}>same environment</Highlight> they learned in recalled noticeably more than those tested in a different one.<Cite n={1} /> Your brain doesn't just store the information — it stores the whole scene around you: the room, the lighting, the sounds, even the smell.</p>
                  <PersonalStory name="Aoife" role="5th Year, Cork" junior={{ name: 'Aoife', role: '2nd Year, Cork', children: (
                    <p>I used to do all my study in my bedroom with music on. I felt like I knew everything. Then I'd sit down for a test and my mind would just go blank. I couldn't understand it — I'd studied for hours. It was like my brain left everything back in my room.</p>
                  ) }}>
                    <p>I used to do all my study in my bedroom with music on. I felt like I knew everything. Then I'd sit down in the exam hall and my mind would just go blank. I couldn't understand it — I'd studied for hours. It was like my brain left everything back in my room.</p>
                  </PersonalStory>
                  <p>These <Highlight description="Things in your surroundings �� background noise, the feel of your chair, the lighting, even your posture — that get linked to what you're learning. Your brain uses them like bookmarks to find the right memory later." theme={theme}>study environment clues</Highlight> become the paths your brain uses to find what it learned. This is why you can remember something perfectly in your bedroom but draw a complete blank in the exam hall. The exam hall has stripped away every familiar clue your brain was relying on.</p>
                  <p>If you only ever study in one place, your memories become <Highlight description="When a memory is strongly linked to one specific place, you can only pull it back reliably in that place. The knowledge is still in your brain, but without the right surroundings your brain can't find it. It's not that you didn't learn it — your brain just lost the path to it." theme={theme}>stuck to that spot</Highlight> — deeply tied to that specific environment. They feel solid and easy to access in your bedroom. But move to an unfamiliar exam hall with fluorescent lights and rows of desks, and those same memories can suddenly feel unreachable. The knowledge is still there; your brain just can't find the path to it without its usual signposts.</p>
                </>
              )}
              <ExerciseSheet name="ContextMemoryComparison">
                <ContextMemoryComparison />
                <ContextCueExplorer />
              </ExerciseSheet>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 'Switch It Up' Fix." eyebrow="Step 2" icon={Repeat} theme={theme}>
              {essentials ? (
                <>
                  <p>Students who studied in two different rooms recalled more than those who stayed in one room.<Cite n={2} /> When you study in multiple places, your brain creates <strong>location-proof memories</strong> that work anywhere.</p>
                  <p>Each new place adds different connections to the same information. More connections means more ways your brain can find it -- even in an unfamiliar exam hall.</p>
                </>
              ) : (
                <>
                  <p>Researchers found something surprising: students who studied the same material in <Highlight description="When you study the same thing in two different places, your brain can't rely on any single room to help it remember. So it stores the information in a way that works anywhere." theme={theme}>two different rooms</Highlight> recalled more than those who studied in the same room twice.<Cite n={2} /> This seems to go against what we just learned about your brain linking memories to places — but it actually goes one step further.</p>
                  <p>When you study in multiple places, your brain can't rely on any single place as a clue, so it creates <Highlight description="Memories that aren't tied to any one place. Instead of needing your bedroom lamp or the sound of rain to remember, your brain connects the info to the ideas themselves. That makes the knowledge portable — it works anywhere, including the exam hall." theme={theme}>location-proof memories</Highlight>. The knowledge becomes portable — it works anywhere, including an unfamiliar exam hall. Instead of storing "this fact + my bedroom lamp + the sound of rain," your brain stores "this fact + lots of different connections," creating a web of memory paths that doesn't depend on any single place.</p>
                  <p>This is sometimes called the <Highlight description="When you study the same thing in different places, each place adds a new set of connections to that memory. More connections means more ways your brain can find the information later, even in a totally new setting like an exam hall." theme={theme}>variety advantage</Highlight>: different study spots create multiple paths to the same information. Each new place adds a different set of connections — the hum of a cafe, the silence of a library, the kitchen radio in the background. When exam day arrives and none of those specific clues are around, it doesn't matter. Your brain has so many alternative paths that some of them will activate, letting you remember even in a completely new setting.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Does Noise Help or Hurt?" eyebrow="Step 3" icon={Activity} theme={theme}>
              {essentials ? (
                <>
                  <p>Moderate background noise can boost creative thinking.<Cite n={3} /> But for focused tasks like maths problems or memorisation, quiet is better. The rule is simple: match your noise level to your task.</p>
                  <p>Reading a chapter for understanding? A cafe might help. Drilling past papers or memorising vocab? You need silence. Choose your environment based on what you are doing.</p>
                </>
              ) : (
                <>
                  <p>Here's a surprising finding: moderate background noise (about the level of a busy cafe) can <Highlight description="A bit of background buzz — like in a cafe — gives your brain just enough of a challenge to push it into bigger-picture thinking. It's not so loud that it distracts you, but it's enough to stop you from getting too narrowly focused." theme={theme}>boost creative thinking</Highlight><Cite n={3} /> compared to both total silence and loud noise. A bit of background buzz creates just enough of a challenge — a kind of <Highlight description="Sometimes making studying feel a little harder actually helps you learn better in the long run. A small amount of background noise is one example — it slightly disrupts your focus, which pushes your brain into a broader way of thinking that helps with creative tasks." theme={theme}>helpful challenge</Highlight> — to push your thinking from narrow, step-by-step mode into bigger-picture mode.</p>
                  <p>However, decades of research have shown that for tasks needing focused concentration — like maths problem-solving or detailed memorisation — <Highlight description="Research across many studies found that noise consistently hurts performance on tasks that need careful, focused attention. But for creative or big-picture tasks, a moderate amount of noise can sometimes help." theme={theme}>quiet is better</Highlight>. Noise gets in the way of the careful, step-by-step thinking these tasks need. The practical rule is simple: use moderate noise for understanding and connecting ideas, use silence for memorisation and practice problems.</p>
                  <p>This means your study environment should match your task. Reading a history chapter to understand the big picture? A cafe might actually help your thinking. Drilling past paper questions in maths or memorising vocabulary? You need silence. The environment isn't just a backdrop — it's an active ingredient in how well your brain works. Planning your study sessions around this means deliberately choosing where you work based on what you're working on.</p>
                </>
              )}
              <ExerciseSheet name="NoiseLevelCurve">
                <NoiseLevelCurve />
                <TaskEnvironmentMatcher />
              </ExerciseSheet>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Why Switching Spots Works." eyebrow="Step 4" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Each new study location wraps your information in different clues. More varied clues means more routes your brain has to find the memory. Think of it as building multiple roads to the same city.</p>
                  <p>This effect stacks with other good habits like spaced repetition and self-testing.<Cite n={4} /> Switching spots is not a replacement for good study techniques -- it is a booster on top of them.</p>
                </>
              ) : (
                <>
                  <p>Here's the science behind it: every time you study the same material in a different place, you create a <Highlight description="Each time you study in a new spot, your brain wraps the information in different surroundings — the sounds, the feel of the chair, the lighting. Each version gives your brain a different path to find that memory later." theme={theme}>new set of connections</Highlight>. Each place adds different clues. The more varied those clues are, the more routes your brain has to find the memory. Think of it like building roads to a city — one road is vulnerable to a single blocked bridge, but five roads from different directions means you can always find a way through.</p>
                  <p>This is why studying the same flashcards on the bus, in your bedroom, and in the library creates stronger memories than studying them three times in the same spot. Each location wraps the information in a different package. The bus adds the rumble of the engine and the movement. Your bedroom adds the familiar sounds of home. The library adds the particular quality of silence and the presence of other students. Each version of the memory is slightly different, and those differences create <Highlight description="Your brain doesn't store memories in just one place — it builds a web of connections. Each time you study in a new spot, you add another thread to that web. More threads means more ways to pull the memory back, so even if one path is blocked, others still work." theme={theme}>backup paths to the same information</Highlight>.</p>
                  <p>Research has confirmed that varying where you study can <Highlight description="A meta-analysis pulling together many studies found this effect is real but modest in size. It's not huge on its own, but it stacks on top of other good study habits like spaced repetition and mixing topics. Together, they make a much bigger difference." theme={theme}>improve how well you remember</Highlight>,<Cite n={4} /> though the effect is modest. The effect is not massive on its own, but it stacks with other good habits like spaced repetition and mixing topics. This is key — switching study spots is not a replacement for other good study strategies; it's a booster. When you combine varied locations with regular self-testing and mixed topics, the combined effect on long-term memory is much bigger than any single trick alone.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Setting Up Your Study Rotation." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>Pick 2-3 genuinely different study spots. Study each subject in at least two different places per week. Use quiet for practice problems and moderate noise for reading. Practise in exam-like conditions too.</p>
              ) : (
                <p>The research points to a simple game plan.</p>
              )}
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Pick 2-3 Study Spots", description: "Rotate between genuinely different places — bedroom, kitchen table, library, cafe. They don't need to be fancy; the differences between these spaces are what give your brain the variety it needs." },
                  { number: 2, term: "Same Subject, Different Spots", description: "Study the same subject in at least two different spots across the week. Study Biology in your bedroom on Monday and in the library on Wednesday. Same content, different places, more paths to the memory." },
                  { number: 3, term: "Match Your Noise Level", description: "Quiet for practice problems and memorisation, a bit of background noise for reading and understanding. The best noise level depends on what you're doing." },
                  { number: 4, term: "Practise in Exam-Like Conditions", description: "Sit at a quiet desk with a timer, recreating the exam hall as closely as you can. Students who practised remembering things in exam-like conditions did better in the real exam.", highlight: true },
                ]}
              />
              <StudyLocationPlanner />
              <MicroCommitment theme={theme}>
                <p>This week, take one subject you'd normally study in the same spot and split it across two different locations. Study the same material in your bedroom on Tuesday and in the school library or kitchen on Thursday. Notice how remembering the same content in a different setting feels harder — that extra effort is what builds memories that work anywhere, including the exam hall.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheContextEffectModule;
