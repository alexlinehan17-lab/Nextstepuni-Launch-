/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
Brain,
ClipboardCheck,
Cpu,
Heart,
Shield,Utensils,
Zap
} from 'lucide-react';
import React,{ useState } from 'react';
import { EMOTIONAL_INTELLIGENCE_REFERENCE_LIST } from '../data/references/emotionalIntelligence';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { cyanTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection,SupportSignpost } from './ModuleShared';
import { AnswerGroup,AnswerLine,ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';
import { ChoiceTile } from './ui/Choice';

const theme = cyanTheme;

// --- INTERACTIVE COMPONENTS ---
const StressResponseComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 540, H = 280;
    const padL = 8, padR = 8, padT = 28, padB = 56;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const labels = ['Calm', 'Mild stress', 'Moderate', 'High stress', 'Panic', 'Meltdown'];
    const pfcData = [0.90, 0.82, 0.68, 0.45, 0.25, 0.12];
    const amygData = [0.10, 0.22, 0.40, 0.62, 0.82, 0.95];

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

    const phases = [
        { label: 'Thinking zone', x1: 0, x2: 0.33 },
        { label: 'Tipping point', x1: 0.33, x2: 0.66 },
        { label: 'Survival mode', x1: 0.66, x2: 1 },
    ];

    // Two series told apart by ink and line, not by green and red: the PFC solid ink, the
    // amygdala a dashed ink-2 line. Flat fills, no gradients; text in the one typeface, 11 or more.
    const font = { fontFamily: 'var(--font-ui)' };
    const Chart = () => (
        <svg viewBox={`0 0 ${W} ${H}`} className="ex-figure-art w-full">
            {/* Grid lines */}
            {[0.25, 0.5, 0.75, 1.0].map(v => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--hairline)" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--outline-soft)" />
            {/* PFC area */}
            <motion.path
                d={buildArea(pfcData)}
                fill="var(--ink-primary)" fillOpacity="0.06"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Amygdala area */}
            <motion.path
                d={buildArea(amygData)}
                fill="var(--ink-secondary)" fillOpacity="0.05"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.15 }}
            />
            {/* PFC line */}
            <motion.path
                d={buildLine(pfcData)}
                fill="none" stroke="var(--ink-primary)" strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Amygdala line */}
            <motion.path
                d={buildLine(amygData)}
                fill="none" stroke="var(--ink-secondary)" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="6 5"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* PFC dots */}
            {pfcData.map((v, i) => (
                <motion.circle key={`pfc-${i}`} cx={toX(i / (pfcData.length - 1))} cy={toY(v)} r="3.5" fill="var(--ink-primary)"
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Amygdala dots */}
            {amygData.map((v, i) => (
                <motion.circle key={`amyg-${i}`} cx={toX(i / (amygData.length - 1))} cy={toY(v)} r="3.5" fill="var(--surface-paper)" stroke="var(--ink-secondary)" strokeWidth="2"
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.5 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="11" fill="var(--ink-muted)" style={font}>Low</text>
            {/* X-axis labels */}
            {labels.map((m, i) => (
                <text key={m} x={toX(i / (labels.length - 1))} y={toY(0) + 16} fontSize="11" fill="var(--ink-muted)" textAnchor={i === 0 ? 'start' : i === labels.length - 1 ? 'end' : 'middle'} style={font}>{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 34} fontSize="11" fill="var(--ink-primary)" textAnchor="middle" style={font}>{p.label}</text>
            ))}
            {/* Chart label, at the left, so the legend has the right */}
            <text x={padL} y={15} fontSize="12" fill="var(--ink-secondary)" style={font}>Brain Activity Under Exam Stress</text>
            {/* Legend */}
            <line x1={W - padR - 208} x2={W - padR - 190} y1={11} y2={11} stroke="var(--ink-primary)" strokeWidth="2.5" />
            <text x={W - padR - 185} y={15} fontSize="11" fill="var(--ink-secondary)" style={font}>Prefrontal Cortex</text>
            <line x1={W - padR - 72} x2={W - padR - 54} y1={11} y2={11} stroke="var(--ink-secondary)" strokeWidth="2.5" strokeDasharray="6 5" />
            <text x={W - padR - 49} y={15} fontSize="11" fill="var(--ink-secondary)" style={font}>Amygdala</text>
        </svg>
    );

    return (
        <ExerciseSheet title="The Neural Tug of War" sub="As stress rises, your thinking brain loses the battle." name="StressResponseComparison">
            {!revealed ? (
                <div className="ex-stack">
                    <p className="t-body text-ink-primary">Your brain has two competing systems fighting for control during an exam. What happens as the pressure builds?</p>
                    <div className="ex-actions">
                        <Button onClick={() => setRevealed(true)}>
                            See the Neural Shift
                        </Button>
                    </div>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="ex-stack">
                    {/* The chart, on the sheet (no box of its own) */}
                    <div className="ex-figure">
                        <Chart />
                    </div>
                    {/* What each line is: words you read, under a hairline */}
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="ex-block">
                            <p className="ex-block-text"><strong className="text-ink-primary">Your PFC</strong> handles planning, working memory, and rational thinking. It's your exam brain. But it shuts down as cortisol rises.</p>
                        </div>
                        <div className="ex-block">
                            <p className="ex-block-text"><strong className="text-ink-primary">Your amygdala</strong> handles threat detection and survival. It hijacks control when stress crosses the tipping point. You can't think clearly in survival mode.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </ExerciseSheet>
    );
};

const PFCShutdownSimulator = () => {
    const [stressed, setStressed] = useState(false);

    const capabilities = [
      { label: 'Memory Retrieval', desc: 'Access to stored knowledge' },
      { label: 'Logical Reasoning', desc: 'Problem-solving and analysis' },
      { label: 'Planning & Strategy', desc: 'Organising and sequencing' },
    ];

    return (
        <ExerciseSheet label="Neuroscience Simulation" title="PFC Shutdown Simulator" sub="See what happens when your Amygdala hijacks your brain under exam stress." name="PFCShutdownSimulator">
          {/* The two parts of the brain, side by side on the sheet, each under a hairline (no boxes) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Amygdala */}
            <div className="ex-block">
              <motion.div
                animate={stressed ? { scale: [1, 1.1, 1] } : { scale: 1 }}
                transition={stressed ? { duration: 1.2, repeat: Infinity } : {}}
                className="ex-icon"
                style={{ width: 26, height: 26 }}
              >
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              </motion.div>
              <p className="ex-block-title">Amygdala</p>
              <p className="ex-block-text">Threat Response</p>

              <div className="mt-2" style={{ height: 6, borderRadius: 3, backgroundColor: "var(--hairline)", overflow: 'hidden' }}>
                <motion.div animate={{ width: stressed ? '100%' : '20%' }} transition={{ duration: 0.8 }} style={{ height: '100%', backgroundColor: "var(--ink-primary)", borderRadius: 3 }} />
              </div>

              <p className="t-label text-ink-primary">
                {stressed ? 'HIJACKING' : 'CALM'}
              </p>
            </div>

            {/* Prefrontal Cortex */}
            <div className="ex-block">
              <motion.div
                animate={{ opacity: stressed ? 0.3 : 1 }}
                transition={{ duration: 0.5 }}
                className="ex-icon"
                style={{ width: 26, height: 26 }}
              >
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M9.5 2C7 2 5 4 5 6.5c0 .8.2 1.5.5 2.1C4.2 9.3 3 10.8 3 12.5 3 15 5 17 7.5 17H9v3h6v-3h1.5C19 17 21 15 21 12.5c0-1.7-1.2-3.2-2.5-3.9.3-.6.5-1.3.5-2.1C19 4 17 2 14.5 2c-1.2 0-2.3.5-3 1.3C10.8 2.5 9.7 2 9.5 2z"/>
                </svg>
              </motion.div>
              <p className="ex-block-title">Prefrontal Cortex</p>
              <p className="ex-block-text">Rational Thinking</p>

              <div className="mt-2 flex flex-col gap-2">
                {capabilities.map((cap, i) => (
                  <motion.div
                    key={cap.label}
                    animate={stressed ? { opacity: 0.3, x: 4 } : { opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: stressed ? i * 0.3 : (2 - i) * 0.2 }}
                    className="flex items-center justify-between gap-3"
                  >
                    <div>
                      <p className="t-body text-ink-primary">{cap.label}</p>
                      <p className="t-meta">{cap.desc}</p>
                    </div>
                    <span className={`t-label shrink-0 ${stressed ? 'text-ink-muted' : 'text-ink-primary'}`}>
                      {stressed ? 'OFFLINE' : 'ONLINE'}
                    </span>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Cortisol: a line that answers the toggle, not a box */}
          <AnimatePresence>
            {stressed && (
              <motion.div
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 6 }}
              >
                <AnswerLine tone="note">
                  Cortisol is blocking the connection between your PFC and your stored knowledge. Your memory isn't gone — the pathway is temporarily offline.
                </AnswerLine>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Toggle button: a white button with a line; it still says it is pressed */}
          <div className="ex-actions">
            <Button
              onClick={() => setStressed(!stressed)}
              aria-pressed={!!(stressed)}
            >
              {stressed ? 'De-escalate' : 'Trigger Stress Response'}
            </Button>
          </div>
        </ExerciseSheet>
    );
}

const ArousalReappraisal = () => {
    const [attempt, setAttempt] = useState<'none' | 'calm' | 'reframe'>('none');
    const [animKey, setAnimKey] = useState(0);

    const handleAttempt = (type: 'calm' | 'reframe') => {
      setAttempt(type);
      setAnimKey(k => k + 1);
    };

    // Grid positions (percentage-based)
    // X: Valence (0=negative, 100=positive)
    // Y: Arousal (0=high, 100=low) — inverted so high arousal is at top
    const emotions = {
      anxiety:    { x: 15, y: 12, label: 'Anxiety' },
      excitement: { x: 85, y: 12, label: 'Excitement' },
      calm:       { x: 85, y: 85, label: 'Calm' },
      boredom:    { x: 15, y: 85, label: 'Boredom' },
    };

    // Dot target
    const dotTarget = attempt === 'reframe'
      ? { x: emotions.excitement.x, y: emotions.excitement.y }
      : attempt === 'calm'
        ? { x: 50, y: 50 } // gets stuck halfway
        : { x: emotions.anxiety.x, y: emotions.anxiety.y };

    return (
        <ExerciseSheet title="Arousal Reappraisal" sub={<>Scenario: Your heart is racing before an exam. What do you do?<span className="block mt-1">The emotion map shows two dimensions: how activated you feel (arousal) and whether it feels good or bad (valence).</span></>} name="ArousalReappraisal">
             {/* Emotion grid: the map drawn on the sheet, two ink axes, no tinted quadrants */}
             <div className="relative w-full aspect-square max-w-sm mx-auto">
               {/* Axis labels */}
               <div className="absolute top-2 left-1/2 -translate-x-1/2 t-label text-ink-muted whitespace-nowrap">High Arousal</div>
               <div className="absolute bottom-2 left-1/2 -translate-x-1/2 t-label text-ink-muted whitespace-nowrap">Low Arousal</div>
               <div className="absolute left-2 top-1/2 -translate-y-1/2 t-label text-ink-muted [writing-mode:vertical-lr] rotate-180">Negative</div>
               <div className="absolute right-2 top-1/2 -translate-y-1/2 t-label text-ink-muted [writing-mode:vertical-lr]">Positive</div>

               {/* Axis lines */}
               <div className="absolute left-1/2 top-0 bottom-0 w-px" style={{ background: 'var(--outline-soft)' }} />
               <div className="absolute top-1/2 left-0 right-0 h-px" style={{ background: 'var(--outline-soft)' }} />

               {/* Emotion labels */}
               {Object.values(emotions).map(e => (
                 <div key={e.label} className="absolute" style={{ left: `${e.x}%`, top: `${e.y}%`, transform: 'translate(-50%, -50%)' }}>
                   <div className="w-3 h-3 rounded-full mx-auto mb-1" style={{ background: 'var(--ink-muted)' }} />
                   <p className="t-meta text-ink-primary text-center whitespace-nowrap">{e.label}</p>
                 </div>
               ))}

               {/* Animated "You" dot */}
               <motion.div
                 key={animKey}
                 initial={{ left: `${emotions.anxiety.x}%`, top: `${emotions.anxiety.y}%` }}
                 animate={{ left: `${dotTarget.x}%`, top: `${dotTarget.y}%` }}
                 transition={attempt === 'calm'
                   ? { duration: 1.5, ease: 'easeOut' }
                   : { duration: 0.6, ease: [0.16, 1, 0.3, 1] }
                 }
                 className="absolute z-10"
                 style={{ transform: 'translate(-50%, -50%)' }}
               >
                 <div className="relative">
                   {/* The student's own place on the map: the one orange, with a paper edge */}
                   <div className="w-6 h-6 rounded-full" style={{ background: 'var(--nsu-orange)', border: '2px solid var(--surface-paper)' }} />
                   <p className="absolute -bottom-5 left-1/2 -translate-x-1/2 t-label text-ink-primary whitespace-nowrap">YOU</p>
                 </div>
               </motion.div>

               {/* Path trails */}
               {attempt === 'reframe' && (
                 <motion.div
                   key={`trail-r-${animKey}`}
                   initial={{ opacity: 0 }}
                   animate={{ opacity: 0.6 }}
                   transition={{ delay: 0.3 }}
                   className="absolute top-0 left-0 w-full h-full pointer-events-none"
                 >
                   <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                     <motion.line
                       x1={emotions.anxiety.x} y1={emotions.anxiety.y}
                       x2={emotions.excitement.x} y2={emotions.excitement.y}
                       stroke="var(--ink-primary)" strokeWidth="0.8" strokeDasharray="2 2"
                       initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                       transition={{ duration: 0.5 }}
                     />
                   </svg>
                   <div className="absolute text-[11px] leading-[14px] text-ink-primary whitespace-nowrap" style={{ left: '50%', top: `${emotions.anxiety.y}%`, transform: 'translate(-50%, 40%)' }}>
                     Short path (same arousal)
                   </div>
                 </motion.div>
               )}
               {attempt === 'calm' && (
                 <motion.div
                   key={`trail-c-${animKey}`}
                   initial={{ opacity: 0 }}
                   animate={{ opacity: 0.6 }}
                   transition={{ delay: 0.3 }}
                   className="absolute top-0 left-0 w-full h-full pointer-events-none"
                 >
                   <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                     <motion.line
                       x1={emotions.anxiety.x} y1={emotions.anxiety.y}
                       x2={emotions.calm.x} y2={emotions.calm.y}
                       stroke="var(--ink-primary)" strokeWidth="0.8" strokeDasharray="2 2"
                       initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                       transition={{ duration: 1.2 }}
                     />
                   </svg>
                   <div className="absolute text-[11px] leading-[14px] text-ink-primary whitespace-nowrap" style={{ left: '55%', top: '50%', transform: 'translate(-50%, -50%)' }}>
                     Long path (change arousal)
                   </div>
                 </motion.div>
               )}
             </div>

             {/* Buttons */}
             <AnswerGroup kind="one" columns={2}>
               <ChoiceTile
                 tile
                 chosen={attempt === 'calm'}
                 onClick={() => handleAttempt('calm')}
                 label={'"Calm down."'}
                 meta="Try to lower your arousal"
               />
               <ChoiceTile
                 tile
                 chosen={attempt === 'reframe'}
                 onClick={() => handleAttempt('reframe')}
                 label={'"I\'m excited!"'}
                 meta="Reframe the same arousal"
               />
             </AnswerGroup>

             {/* Result insight: a line that answers the choice */}
             <AnimatePresence mode="wait">
               {attempt === 'calm' && (
                 <motion.div key="calm-result" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
                   <AnswerLine tone="note"><b>Difficult path.</b> Telling yourself to "calm down" requires changing your entire arousal state — fighting your physiology. Your body is flooded with adrenaline; you can't just switch it off by willpower. The dot gets stuck halfway.</AnswerLine>
                 </motion.div>
               )}
               {attempt === 'reframe' && (
                 <motion.div key="reframe-result" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
                   <AnswerLine><b>Easy path.</b> Anxiety and excitement feel the same in your body — same racing heart, same adrenaline. You only need to change the label, not the state. People who say "I'm excited" before a test actually perform noticeably better than those who try to calm down.</AnswerLine>
                 </motion.div>
               )}
             </AnimatePresence>
        </ExerciseSheet>
    );
};

const BoxBreathing = () => {
    const [active, setActive] = useState(false);
    const [phase, setPhase] = useState(0); // 0=inhale, 1=hold, 2=exhale, 3=hold
    const [count, setCount] = useState(4);
    const [cycle, setCycle] = useState(0);
    const totalCycles = 3;

    const phases = [
      { label: 'Breathe In' },
      { label: 'Hold' },
      { label: 'Breathe Out' },
      { label: 'Hold' },
    ];

    // Ring arc: each phase is a quarter of the circle, all in ink (the current one is the bold one)
    const arcColors = ["var(--ink-primary)", "var(--ink-primary)", "var(--ink-primary)", "var(--ink-primary)"];
    const radius = 88;
    const circumference = 2 * Math.PI * radius;
    const _quarterArc = circumference / 4;

    const getArcPath = (index: number) => {
      const startAngle = (index * 90 - 90) * (Math.PI / 180);
      const endAngle = ((index + 1) * 90 - 90) * (Math.PI / 180);
      const x1 = 100 + radius * Math.cos(startAngle);
      const y1 = 100 + radius * Math.sin(startAngle);
      const x2 = 100 + radius * Math.cos(endAngle);
      const y2 = 100 + radius * Math.sin(endAngle);
      return `M ${x1} ${y1} A ${radius} ${radius} 0 0 1 ${x2} ${y2}`;
    };

    // Breathing circle scale
    const breathScale = phase === 0 ? 1.3 : phase === 2 ? 0.7 : phase === 1 ? 1.3 : 0.7;

    React.useEffect(() => {
      if (!active) return;
      const interval = setInterval(() => {
        setCount(c => {
          if (c <= 1) {
            setPhase(p => {
              const next = (p + 1) % 4;
              if (next === 0) {
                setCycle(cy => {
                  if (cy + 1 >= totalCycles) {
                    setActive(false);
                    return 0;
                  }
                  return cy + 1;
                });
              }
              return next;
            });
            return 4;
          }
          return c - 1;
        });
      }, 1000);
      return () => clearInterval(interval);
    }, [active]);

    const handleStart = () => {
      setPhase(0);
      setCount(4);
      setCycle(0);
      setActive(true);
    };

    const done = !active && cycle === 0 && phase === 0;

    return (
     <ExerciseSheet title="Box Breathing" sub="Your emergency protocol for the exam hall. 4 seconds per phase, 3 cycles." name="BoxBreathing">
         {/* The breathing box, drawn on the sheet */}
         <div className="flex justify-center py-8">
           <div className="relative w-52 h-52">
             {/* Outer phase ring */}
             <svg viewBox="0 0 200 200" className="w-full h-full absolute inset-0">
               {[0, 1, 2, 3].map(i => (
                 <motion.path
                   key={i}
                   d={getArcPath(i)}
                   fill="none"
                   stroke={arcColors[i]}
                   strokeWidth={active && i === phase ? 6 : 3}
                   strokeLinecap="round"
                   animate={{
                     opacity: active ? (i === phase ? 1 : 0.2) : 0.15,
                     strokeWidth: active && i === phase ? 6 : 3,
                   }}
                   transition={{ duration: 0.4 }}
                 />
               ))}
             </svg>

             {/* Phase labels on each side */}
             <div className={`absolute -top-7 left-1/2 -translate-x-1/2 t-label transition-opacity duration-300 ${active && phase === 0 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Inhale</div>
             <div className={`absolute top-1/2 -right-10 -translate-y-1/2 t-label transition-opacity duration-300 ${active && phase === 1 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Hold</div>
             <div className={`absolute -bottom-7 left-1/2 -translate-x-1/2 t-label transition-opacity duration-300 ${active && phase === 2 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Exhale</div>
             <div className={`absolute top-1/2 -left-10 -translate-y-1/2 t-label transition-opacity duration-300 ${active && phase === 3 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Hold</div>

             {/* Inner breathing circle */}
             <div className="absolute inset-0 flex items-center justify-center">
               <motion.div
                 animate={{
                   scale: active ? breathScale : 1,
                 }}
                 transition={{ duration: 3.8, ease: 'easeInOut' }}
                 className="w-28 h-28 rounded-full flex flex-col items-center justify-center"
                 style={{ background: 'var(--surface-paper)', border: '1.5px solid var(--outline-strong)' }}
               >
                 {active ? (
                   <>
                     <motion.p
                       key={`${phase}-${count}`}
                       initial={{ scale: 1.2, opacity: 0 }}
                       animate={{ scale: 1, opacity: 1 }}
                       className="t-number text-ink-primary"
                     >
                       {count}
                     </motion.p>
                     <p className="t-meta text-ink-primary">{phases[phase].label}</p>
                   </>
                 ) : (
                   <p className="t-meta">Ready</p>
                 )}
               </motion.div>
             </div>
           </div>
         </div>

         {/* Cycle progress */}
         {active && (
           <div className="flex justify-center gap-2">
             {Array.from({ length: totalCycles }).map((_, i) => (
               <div key={i} className="w-2 h-2 rounded-full transition-colors" style={{ background: i < cycle ? 'var(--ink-primary)' : i === cycle ? 'var(--ink-secondary)' : 'var(--outline-soft)' }} />
             ))}
           </div>
         )}

         <div className="ex-actions">
           {!active ? (
             <Button
               onClick={handleStart}
             >
               {done ? 'Begin' : 'Start Again'}
             </Button>
           ) : (
             <Button
               onClick={() => setActive(false)}
             >
               Stop
             </Button>
           )}
         </div>
    </ExerciseSheet>
    );
};

// --- MODULE COMPONENT ---
const EmotionalIntelligenceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'neurobiology-stress', title: 'Why Stress Messes With Your Brain', eyebrow: '01 // The Hardware', icon: Cpu },
    { id: 'emotional-intelligence', title: 'What is Emotional Intelligence?', eyebrow: '02 // The Software', icon: Brain },
    { id: 'self-awareness', title: 'Reading Your Own Body', eyebrow: '03 // Early Warning Signs', icon: Heart },
    { id: 'cognitive-regulation', title: 'Using Your Mind to Manage Stress', eyebrow: '04 // The Mind', icon: Zap },
    { id: 'physiological-regulation', title: 'Using Your Body to Calm Down', eyebrow: '05 // The Body', icon: Shield },
    { id: 'bio-support', title: 'Sleep, Food, and Water', eyebrow: '06 // Fuel & Maintenance', icon: Utensils },
    { id: 'integrated-timeline', title: 'Putting It All Together', eyebrow: '07 // The Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="13"
      moduleTitle="Emotional Intelligence"
      moduleSubtitle="The Stress Management Toolkit"
      moduleDescription={`Understand why your brain freaks out during exams and learn practical techniques — both mental and physical — to turn stress into something that works for you, not against you.`}
      theme={theme}
      sections={sections}
      references={EMOTIONAL_INTELLIGENCE_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Master Your Response"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why Stress Messes With Your Brain." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>Exam stress is not a character flaw. Your body floods you with cortisol under pressure. A little cortisol helps. Too much shuts down your thinking brain. That is why you "go blank."</p>
                  <p>Your thinking brain (prefrontal cortex) goes offline when stress is high.<Cite n={1} /> Your alarm brain takes over. Understanding this is the first step to beating it.</p>
                </>
              ) : (
                <>
                  <p>Exam stress isn't a character flaw — it's your brain doing exactly what it's designed to do. Your body has a built-in alarm system called the <Highlight description="Your body's built-in alarm system. When your brain senses danger (like opening an exam paper), it fires off a chain reaction that floods you with stress hormones, especially cortisol." theme={theme}>HPA Axis</Highlight>, and it floods you with stress hormones like cortisol. A small hit of cortisol actually sharpens your focus. But a season of big exams isn't one scary moment — it's months of pressure, and that's where things go wrong.</p>
                  <p>When stress stays high for weeks, all that cortisol basically takes your <Highlight description="Think of this as the 'boss' part of your brain. It handles planning, logic, and holding information in your head. It's still developing in your teens, which is why stress can knock it offline so easily at your age." theme={theme}>Prefrontal Cortex (PFC)</Highlight> offline.<Cite n={1} /> That's the part of your brain you need for thinking, planning, and remembering. This is the real reason you "go blank" in an exam — your brain has switched into survival mode and shut down the thinking part. Understanding this isn't an excuse; it's the first step to taking back control.</p>
                </>
              )}
              <StressResponseComparison />
              <PFCShutdownSimulator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="What is Emotional Intelligence?" eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <p>Emotional intelligence means noticing what you feel, understanding why, and doing something useful about it.<Cite n={2} /> You can train three skills: spotting stress early, naming the feeling, and using techniques to manage it.</p>
              ) : (
                <>
                  <p><Highlight description="Being able to notice what you're feeling, understand why, and then do something useful about it instead of just reacting on autopilot." theme={theme}>Emotional Intelligence (EI)</Highlight> isn't about being "nice." It's a practical set of skills for noticing what's going on inside you and doing something useful about it.<Cite n={2} /> Having good EI doesn't mean you don't feel stress — it means you can turn that stress into fuel (<Highlight description="The good kind of stress — the buzz you get before a match or a performance that actually helps you do better. Same racing heart, but it's working for you, not against you." theme={theme}>eustress</Highlight>) instead of letting it wreck your performance.</p>
                  <p>For big exams, we can break EI into three skills you can actually train:</p>
                </>
              )}
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">1</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Emotional Awareness</p>
                    <p className="ex-num-sub">Spotting the physical signs of stress early.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">2</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Emotional Understanding</p>
                    <p className="ex-num-sub">Putting the right name on what you're feeling.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">3</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Emotional Regulation</p>
                    <p className="ex-num-sub">Using specific techniques to manage it.</p>
                  </div>
                </li>
              </ol>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Reading Your Own Body." eyebrow="Step 3" icon={Heart} theme={theme}>
              {essentials ? (
                <p>Your body spots stress before your brain does. Learn to notice your early warning signs: tight stomach, shallow breathing, racing heart. A daily body scan builds this skill. Catch stress early and you can deal with it before panic takes over.</p>
              ) : (
                <>
                  <p>You can't manage what you don't notice. The first step is learning to read your own body — what we call <Highlight description="Getting good at reading your own body — noticing things like your heart speeding up, your breathing going shallow, or your shoulders tensing. It's like having an early warning system for stress." theme={theme}>Somatic Literacy</Highlight>. Your body usually picks up on stress before your brain does. Those early physical signs — the tight stomach, the shallow breathing — are your <Highlight description="Those physical feelings — like a knot in your stomach or sweaty palms — that show up before you even realise you're stressed. Your body is basically tapping you on the shoulder saying 'heads up.'" theme={theme}>Somatic Markers</Highlight>.<Cite n={3} /></p>
                  <p>A quick daily "Body Scan" trains you to notice these signals. If you can catch stress early, you can deal with it before it spirals into full-on panic. It's the difference between "I'm freaking out" and "OK, my heart is racing — I know what to do about that."</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Using Your Mind to Manage Stress." eyebrow="Step 4" icon={Zap} theme={theme}>
              {essentials ? (
                <p>Say "I am excited" instead of "I am anxious." They feel the same in your body. Relabelling is easier than calming down — and people who do it tend to perform better.<Cite n={4} /> When your brain says "I will fail," challenge it like a lawyer. What is the actual evidence?<Cite n={5} /> Try the tool below.</p>
              ) : (
                <>
                  <p>Once you've spotted the feeling, you need to manage it with your mind. This is <Highlight description="Using your thinking to change how you feel. Basically, your mind talks your body down from the ledge." theme={theme}>Top-Down Regulation</Highlight>. One surprisingly powerful trick is <Highlight description="Relabelling your nerves as excitement. Anxiety and excitement feel almost identical in your body — same racing heart, same adrenaline. The only real difference is the story you tell yourself about what's happening." theme={theme}>Arousal Reappraisal</Highlight>. It's actually much easier for your brain to switch from "anxious" to "excited" than it is to just "calm down" — and in studies, people who reappraised their nerves as excitement performed better.<Cite n={4} /></p>
                  <p>The second tool is <Highlight description="When your brain tells you something catastrophic like 'I'm going to fail everything,' you stop and challenge it like a lawyer — what's the actual evidence? Usually the panic is way bigger than the reality." theme={theme}>Cognitive Restructuring</Highlight>.<Cite n={5} /> When your brain screams "I'm going to fail everything," you treat that thought like you're a defence lawyer — what's the actual evidence? Is it really true, or is panic doing the talking?</p>
                </>
              )}
              <ArousalReappraisal/>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Using Your Body to Calm Down." eyebrow="Step 5" icon={Shield} theme={theme}>
              {essentials ? (
                <p>When you are too stressed to think, use your body. Box Breathing is your emergency tool: breathe in 4 seconds, hold 4, out 4, hold 4.<Cite n={6} /> It is invisible. It breaks the panic loop in under a minute. Practice it below.</p>
              ) : (
                <>
                  <p>Sometimes, your mind is too flooded to think straight. When that happens, trying to reason your way out won't work — you need to use your body to calm your mind instead. This is <Highlight description="Using your body to calm your mind. When you're too stressed to think straight, physical tricks like breathing exercises can break the panic cycle for you." theme={theme}>Bottom-Up Regulation</Highlight>. The fastest tool you have is your breathing.</p>
                  <p><Highlight description="A dead simple breathing pattern: 4 seconds in, hold 4, out 4, hold 4. It activates your body's built-in calm-down system. You can do it silently in the exam hall and nobody will even notice." theme={theme}>Box Breathing</Highlight> is your emergency move for the exam hall. Slow, deliberate breathing measurably lowers physiological arousal,<Cite n={6} /> it's invisible, takes less than a minute, and it breaks the panic loop so your thinking brain can come back online.</p>
                </>
              )}
              <BoxBreathing />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Sleep, Food, and Water." eyebrow="Step 6" icon={Utensils} theme={theme}>
              {essentials ? (
                <p>Your brain cannot manage stress if you are tired, hungry, or dehydrated. Eat slow-release food like porridge. Drink water. Sleep properly. Use short NSDR breaks (guided rest, 10-20 minutes) to reset during long study days.</p>
              ) : (
                <>
                  <p>Managing your emotions takes real energy. A tired, dehydrated, or hungry brain can't keep its cool, no matter how many techniques you know. Looking after the basics isn't optional — it's the foundation everything else is built on.</p>
                  <p>For food, focus on slow-release energy like porridge and omega-3s from fish or walnuts to keep you steady. Even being slightly dehydrated tanks your concentration. And sleep is when your brain locks in what you've learned.<Cite n={7} /> During study days, short breaks using <Highlight description="Non-Sleep Deep Rest — basically a guided relaxation where you lie down for 10-20 minutes without actually sleeping. It's a quick reset button that helps you feel sharper and less wrecked during a long study day." theme={theme}>NSDR</Highlight> are a great way to reset without losing your whole afternoon.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Putting It All Together." eyebrow="Step 7" icon={ClipboardCheck} theme={theme}>
              {essentials ? (
                <p>Months before: practice body scans and box breathing daily. Morning of: eat well, avoid panicked friends, say "I am excited." In the hall: stop, breathe, clench and release toes, start with easiest question. After: never compare answers.</p>
              ) : (
                <p>You now have a full toolkit — techniques that use your mind and techniques that use your body. The final step is knowing when to use what.</p>
              )}
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">1</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Months Before</p>
                    <p className="ex-num-sub">Build your foundation. Practice daily Body Scans and learn Box Breathing while stress is low so it's automatic when you need it.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">2</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Morning Of</p>
                    <p className="ex-num-sub">Managing your energy is everything. Eat a proper breakfast, stay away from panicked friends at the school gate, and tell yourself "I'm excited" instead of "I'm terrified."</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">3</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">In The Hall</p>
                    <p className="ex-num-sub">If panic hits, use the "Paper Panic" drill: Stop, Breathe (3 cycles of Box Breathing), clench and release your toes, and re-engage with the easiest question on the paper.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">4</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Post-Exam</p>
                    <p className="ex-num-sub">Do not — absolutely do not — compare answers with friends afterwards. It only fuels anxiety for the next paper.</p>
                  </div>
                </li>
              </ol>
              <SupportSignpost />
              <MicroCommitment theme={theme}><p>Pick one technique from this module. Commit to practising it for 5 minutes every day for one week. This isn't just studying — you're building a skill that kicks in automatically when you need it most.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EmotionalIntelligenceModule;
