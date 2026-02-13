/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Eye, AlertTriangle, Lightbulb, SlidersHorizontal, Brain, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = tealTheme;

// --- INTERACTIVE COMPONENTS ---

const ForgettingCurveSimulator = () => {
    const [pins, setPins] = useState<number[]>([]);

    const togglePin = (day: number) => {
      if (day === 0) return;
      setPins(prev => prev.includes(day) ? prev.filter(d => d !== day) : [...prev, day].sort((a, b) => a - b));
    };

    // Calculate retention at each day given review pins
    // After learning/review, retention decays: R(t) = 100 * e^(-t/S)
    // Each review resets retention to ~95% and increases stability S
    const getRetentionCurve = (reviewDays: number[]): number[] => {
      const points: number[] = [];
      let lastReviewDay = 0;
      let stability = 1.5; // initial half-life in days (fast decay)
      let retentionAtReview = 100;

      for (let day = 0; day <= 7; day++) {
        const elapsed = day - lastReviewDay;
        const retention = retentionAtReview * Math.exp(-elapsed / stability);
        points.push(Math.max(5, Math.min(100, retention)));

        if (reviewDays.includes(day) && day > 0) {
          lastReviewDay = day;
          stability = stability * 2.2; // each review more than doubles stability
          retentionAtReview = Math.min(98, retention + (100 - retention) * 0.85);
        }
      }
      return points;
    };

    const baselineCurve = getRetentionCurve([]);
    const activeCurve = getRetentionCurve(pins);

    // SVG chart dimensions
    const chartLeft = 44;
    const chartRight = 380;
    const chartTop = 10;
    const chartBottom = 170;
    const chartW = chartRight - chartLeft;
    const chartH = chartBottom - chartTop;

    const toX = (day: number) => chartLeft + (day / 7) * chartW;
    const toY = (pct: number) => chartBottom - (pct / 100) * chartH;

    const buildPath = (curve: number[]) => {
      return curve.map((val, i) => {
        const x = toX(i);
        const y = toY(val);
        if (i === 0) return `M ${x} ${y}`;
        // Use quadratic bezier for smooth curve between points
        const prevX = toX(i - 1);
        const prevY = toY(curve[i - 1]);
        const cpX = (prevX + x) / 2;
        return `C ${cpX} ${prevY}, ${cpX} ${y}, ${x} ${y}`;
      }).join(' ');
    };

    const finalRetention = Math.round(activeCurve[7]);
    const dayLabels = ['Learn', '1', '2', '3', '4', '5', '6', '7'];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Forgetting Curve</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Click on days to place review sessions and see how spacing fights forgetting.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">You have 3 reviews to place. Where will you put them?</p>

            {/* Chart */}
            <div className="w-full overflow-visible">
              <svg viewBox="0 0 400 220" className="w-full h-auto">
                {/* Y-axis gridlines and labels */}
                {[0, 25, 50, 75, 100].map(pct => (
                  <g key={pct}>
                    <line x1={chartLeft} y1={toY(pct)} x2={chartRight} y2={toY(pct)} stroke="#e5e7eb" strokeWidth="0.5" className="dark:opacity-20" />
                    <text x={chartLeft - 6} y={toY(pct) + 4} textAnchor="end" fontSize="9" fill="#a1a1aa">{pct}%</text>
                  </g>
                ))}

                {/* Baseline curve (no reviews) - dashed */}
                <path d={buildPath(baselineCurve)} fill="none" stroke="#d4d4d8" strokeWidth="2" strokeDasharray="6 4" className="dark:opacity-40" />

                {/* Active curve with reviews */}
                <motion.path
                  key={pins.join(',')}
                  d={buildPath(activeCurve)}
                  fill="none"
                  stroke="#14b8a6"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.8, ease: 'easeOut' }}
                />

                {/* Shaded area under active curve */}
                <motion.path
                  key={`fill-${pins.join(',')}`}
                  d={`${buildPath(activeCurve)} L ${toX(7)} ${chartBottom} L ${toX(0)} ${chartBottom} Z`}
                  fill="url(#tealGrad)"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.15 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                />
                <defs>
                  <linearGradient id="tealGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#14b8a6" />
                    <stop offset="100%" stopColor="#14b8a6" stopOpacity="0" />
                  </linearGradient>
                </defs>

                {/* Day markers along x-axis */}
                {dayLabels.map((label, i) => {
                  const isPin = pins.includes(i);
                  const isClickable = i > 0 && (isPin || pins.length < 3);
                  return (
                    <g key={i}>
                      {/* Vertical pin line */}
                      {isPin && (
                        <motion.line
                          x1={toX(i)} y1={toY(activeCurve[i])} x2={toX(i)} y2={chartBottom}
                          stroke="#14b8a6" strokeWidth="1" strokeDasharray="3 3"
                          initial={{ opacity: 0 }} animate={{ opacity: 0.5 }}
                        />
                      )}
                      {/* Dot on curve */}
                      {isPin && (
                        <motion.circle
                          cx={toX(i)} cy={toY(activeCurve[i])} r="4"
                          fill="#14b8a6"
                          initial={{ scale: 0 }} animate={{ scale: 1 }}
                          transition={{ type: 'spring', stiffness: 300, damping: 15 }}
                        />
                      )}
                      {/* Clickable day button area */}
                      <g
                        onClick={() => isClickable ? togglePin(i) : undefined}
                        style={{ cursor: isClickable ? 'pointer' : i === 0 ? 'default' : 'not-allowed' }}
                      >
                        <rect
                          x={toX(i) - 16} y={chartBottom + 6} width="32" height="28" rx="6"
                          fill={isPin ? '#14b8a6' : i === 0 ? '#f4f4f5' : '#f4f4f5'}
                          stroke={isPin ? '#0d9488' : '#e4e4e7'}
                          strokeWidth="1"
                          className={isPin ? '' : 'dark:fill-zinc-700 dark:stroke-zinc-600'}
                        />
                        <text
                          x={toX(i)} y={chartBottom + 24}
                          textAnchor="middle" fontSize="9"
                          fontWeight={isPin || i === 0 ? 'bold' : 'normal'}
                          fill={isPin ? 'white' : '#71717a'}
                        >
                          {i === 0 ? label : `Day ${label}`}
                        </text>
                        {isPin && (
                          <text x={toX(i)} y={chartBottom + 48} textAnchor="middle" fontSize="8" fill="#14b8a6" fontWeight="bold">Review</text>
                        )}
                      </g>
                    </g>
                  );
                })}

                {/* Axis labels */}
                <text x={(chartLeft + chartRight) / 2} y={chartBottom + 60} textAnchor="middle" fontSize="10" fill="#a1a1aa" fontWeight="bold">Time (Days)</text>
              </svg>
            </div>

            {/* Result + controls */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mt-2">
              <div className="text-center sm:text-left">
                <p className="text-sm text-zinc-500 dark:text-zinc-400">Retention after 7 days:</p>
                <p className="text-3xl font-bold text-teal-600">{finalRetention}%
                  <span className="text-sm font-normal text-zinc-400 ml-2">
                    {pins.length === 0 ? '(no reviews)' : `(${pins.length} review${pins.length > 1 ? 's' : ''})`}
                  </span>
                </p>
              </div>
              <button
                onClick={() => setPins([])}
                className="px-4 py-2 text-xs font-bold bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-colors"
              >
                Reset
              </button>
            </div>

            {/* Insight message */}
            {pins.length === 3 && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className={`mt-4 p-4 rounded-xl text-sm font-medium ${
                  finalRetention >= 70
                    ? 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/50'
                    : 'bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/50'
                }`}
              >
                {finalRetention >= 70
                  ? 'Well spaced! Spreading reviews over the week keeps your retention high. This is the power of spaced repetition.'
                  : 'Try spacing your reviews further apart. Bunching them together wastes their power — your brain needs time between reviews to consolidate.'}
              </motion.div>
            )}
        </div>
    );
};

const FeynmanExplainer = () => {
    const concept = "Osmosis is the net movement of water molecules through a selectively permeable membrane from a region of higher water concentration to a region of lower water concentration.";
    const [explanation, setExplanation] = useState('');
    const jargon = ['molecules', 'selectively', 'permeable', 'concentration'];
    const jargonCount = jargon.filter(word => explanation.toLowerCase().includes(word)).length;

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Feynman Explainer</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-4">Task: Explain this definition of Osmosis in simple terms, as if to a 12-year-old.</p>
             <p className="p-4 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-xs text-center mb-4">{concept}</p>
             <textarea value={explanation} onChange={e => setExplanation(e.target.value)} className="w-full h-32 p-4 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl focus:outline-none focus:border-teal-400" placeholder="Your simple explanation..."></textarea>
             {explanation.length > 0 &&
                <div className={`mt-4 text-center text-xs p-2 rounded-lg ${jargonCount > 0 ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'}`}>
                    {jargonCount > 0 ? `Warning: You're using ${jargonCount} jargon word(s). Simplify further!` : 'Great! This is a simple, clear explanation.'}
                </div>
             }
        </div>
    );
};


// --- MODULE COMPONENT ---
const IllusionOfCompetenceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'the-deception', title: 'The Great Deception', eyebrow: '01 // The Illusion', icon: Eye },
    { id: 'passive-traps', title: 'The Passive Traps', eyebrow: '02 // The False Comfort', icon: AlertTriangle },
    { id: 'desirable-difficulties', title: 'The Antidote', eyebrow: '03 // Desirable Difficulties', icon: Lightbulb },
    { id: 'strategic-toolkit', title: 'The Strategic Toolkit', eyebrow: '04 // The System', icon: SlidersHorizontal },
    { id: 'feynman-protocol', title: 'The Feynman Protocol', eyebrow: '05 // The Litmus Test', icon: Brain },
    { id: 'anti-fragile', title: 'Building Anti-Fragile Knowledge', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="10"
      moduleTitle="Overcoming Illusions of Competence"
      moduleSubtitle="The Fluency Illusion"
      moduleDescription="Deconstruct the cognitive biases that trick you into feeling confident when you're unprepared, and learn the science-backed strategies to build real, durable knowledge."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Great Deception." eyebrow="Step 1" icon={Eye} theme={theme}>
              <p>The most dangerous thing in your academic life isn't the stuff you know you don't know. It's the stuff you *think* you know, but actually don't. This is the <Highlight description="The cognitive bias where your subjective confidence in your mastery of a topic is significantly higher than your objective ability to retrieve and apply that knowledge." theme={theme}>Illusion of Competence</Highlight>. It's the primary driver of 'grade shock' after the Mocks.</p>
              <p>It's caused by a simple brain shortcut: we mistake the ease of *recognising* information for the ability to *recall* it. Seeing a definition in your notes and thinking "Oh yeah, I know that" feels like learning. But it's a trap. It creates a false sense of security that is brutally exposed under exam conditions when the notes are gone and you have to retrieve the information from a blank page.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Passive Traps." eyebrow="Step 2" icon={AlertTriangle} theme={theme}>
              <p>This illusion is created by the most common study methods because they are low-stress and feel effective. The first is the <Highlight description="When you re-read, your brain recognizes the visual pattern of the highlighted text, not the information itself. The cue is the yellow ink, not your internal memory." theme={theme}>Highlighting Trap</Highlight>. The second is the <Highlight description="Following the logic of a solved problem feels like you could have solved it yourself. This is the 'passenger effect' - you practiced verification, not derivation." theme={theme}>'Solved Example' Fallacy</Highlight>. The third is the <Highlight description="When a teacher explains something clearly, you confuse their fluency with your own. You've toured their understanding, not built your own." theme={theme}>Lecture Delusion</Highlight>.</p>
              <p>All these passive methods fail to account for the biological reality of your memory: the <Highlight description="The natural, exponential decay of memory. Without active reinforcement, you lose the majority of new information within 24 hours." theme={theme}>Forgetting Curve</Highlight>. Passive learning feels good, but the knowledge simply evaporates.</p>
              <ForgettingCurveSimulator />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Antidote." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
              <p>To dismantle this illusion, we must shift from study methods that feel easy (passive) to ones that feel hard (active). The science of learning is built on the counter-intuitive concept of <Highlight description="Introduced by Robert & Elizabeth Bjork, this is the idea that learning conditions that feel harder and slow down initial performance often lead to far superior long-term retention." theme={theme}>Desirable Difficulties</Highlight>.</p>
              <p>The single most powerful "desirable difficulty" is <Highlight description="The act of retrieving information from memory without cues. This 'testing effect' is a memory modifier; the struggle to recall is the learning process itself." theme={theme}>Active Recall</Highlight>. When you force your brain to retrieve information, you send a powerful signal to strengthen that neural pathway for future use. The struggle is not a sign you are failing; it is the physical sensation of your brain getting stronger.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Strategic Toolkit." eyebrow="Step 4" icon={SlidersHorizontal} theme={theme}>
              <p>Active Recall is the engine, but it needs a system to work effectively. The two key partners are <Highlight description="The strategy of spreading out your study sessions over time to interrupt the forgetting curve." theme={theme}>Spaced Repetition</Highlight> and <Highlight description="The strategy of mixing different topics within a study session to train the crucial 'problem spotting' skill." theme={theme}>Interleaving</Highlight>.</p>
              <p>These strategies can be managed with a simple but powerful system: the <Highlight description="A way to plan study by logging what you've done and using a Red/Amber/Green system to rate your confidence, forcing you to always work on your weakest topics first." theme={theme}>Retrospective Revision Timetable</Highlight>. This system forces you to confront your incompetence daily and prioritizes output (mastery) over input (time spent studying).</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Feynman Protocol." eyebrow="Step 5" icon={Brain} theme={theme}>
              <p>The ultimate litmus test for genuine understanding is the <Highlight description="Named after the Nobel prize-winning physicist Richard Feynman, this technique involves explaining a concept in simple terms, as if to a child, to identify the gaps in your own knowledge." theme={theme}>Feynman Technique</Highlight>. If you can't explain it simply, you don't really know it. The moment you stumble or have to use jargon is the "Illusion Gap"--the precise point where your knowledge is fragile.</p>
              <p>For STEM subjects, a practical application of this is <Highlight description="Practicing exam questions under exam conditions--no notes, no textbook, no marking scheme. This forces you to confront what you can actually retrieve." theme={theme}>'Blind Practice'</Highlight> combined with a <Highlight description="A dedicated notebook where you log every mistake, diagnose why it happened (Slip, Gap, or Misconception), and prescribe a fix." theme={theme}>Mistake Log</Highlight>. This turns vague failure ("I'm bad at Maths") into specific, actionable data ("I keep forgetting the chain rule").</p>
              <FeynmanExplainer />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Anti-Fragile Knowledge." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>The goal is to move from <Highlight description="Knowledge that is context-dependent and breaks under pressure or when a question is phrased differently. It's a product of passive learning." theme={theme}>Fragile Knowledge</Highlight> to <Highlight description="Knowledge that actually gets stronger when challenged with new contexts and problems. It is the product of desirable difficulties." theme={theme}>Anti-Fragile Knowledge</Highlight>. This is the only path to genuine confidence.</p>
              <p>By embracing these effortful strategies, you are not just learning more effectively; you are also managing your wellbeing. The anxiety of the Leaving Cert often stems from the subconscious knowledge that your understanding is fragile. Genuine competence, built through desirable difficulties, is the ultimate antidote to exam stress.</p>
               <MicroCommitment theme={theme}>
                <p>For your very next study session, commit to the "Book Closed" rule. Spend 20 minutes reading, then close the book and spend 10 minutes writing down everything you can remember. This one change will transform your learning.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default IllusionOfCompetenceModule;
