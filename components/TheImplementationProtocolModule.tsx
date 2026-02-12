/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Target, GitBranch, Lightbulb, Shield, Flag } from 'lucide-react';
import { ModuleProgress } from '../types';
import { roseTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = roseTheme;
const MotionDiv = motion.div as any;

// --- INTERACTIVE COMPONENTS ---

// 1. INTENTION-GAP COMPARISON (Planning Paradox style dual-chart)
const IntentionGapComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'];

  // Good Intentions Alone: motivation drops, actual study hours drop faster
  const gapMotivation = [0.90, 0.75, 0.55, 0.38, 0.25, 0.15];
  const gapStudy = [0.60, 0.40, 0.25, 0.15, 0.10, 0.08];

  // Implementation Intentions: motivation normalises, actual study hours hold strong
  const implMotivation = [0.90, 0.72, 0.60, 0.55, 0.52, 0.50];
  const implStudy = [0.60, 0.58, 0.62, 0.65, 0.68, 0.70];

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

  const gapPhases = [
    { label: 'Excited', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Slipping', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Abandoned', x1: 0.66, x2: 1, color: '#ef4444' },
  ];
  const implPhases = [
    { label: 'Planned', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Habitual', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Automatic', x1: 0.66, x2: 1, color: '#10b981' },
  ];

  const Chart = ({ motivation, study, phases, areaColor, areaId, label }: {
    motivation: number[]; study: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; areaId: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
      <defs>
        <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
          <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      {[0.25, 0.5, 0.75, 1.0].map((v) => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      {/* Baseline */}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
      {/* Motivation area */}
      <motion.path
        d={buildArea(motivation)}
        fill={`url(#${areaId})`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      {/* Motivation line (solid) */}
      <motion.path
        d={buildLine(motivation)}
        fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {/* Actual Study Hours line (dashed) */}
      <motion.path
        d={buildLine(study)}
        fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
      />
      {/* Motivation dots */}
      {motivation.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (motivation.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
          initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
        />
      ))}
      {/* Y-axis labels */}
      <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
      {/* Week labels */}
      {weeks.map((m, i) => (
        <text key={m} x={toX(i / (weeks.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
      ))}
      {/* Phase labels */}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
      ))}
      {/* Chart label */}
      <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
      {/* Legend */}
      <line x1={W - padR - 110} x2={W - padR - 94} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 90} y={17} fontSize="8" fill="#a1a1aa">Motivation</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Study</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Intention-Action Gap</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Same motivation. Different strategies. Opposite outcomes.</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Most students rely on motivation alone to drive study behaviour. What does the data actually show?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-rose-500 text-white hover:bg-rose-600 transition-colors">
            Reveal the Gap
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart motivation={gapMotivation} study={gapStudy} phases={gapPhases}
                areaColor="#ef4444" areaId="gap-grad" label="Good Intentions Alone" />
            </div>
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart motivation={implMotivation} study={implStudy} phases={implPhases}
                areaColor="#10b981" areaId="impl-grad" label="Implementation Intentions" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Motivation fades</strong> and without a specific plan, study hours collapse with it. By week 6, the student has essentially stopped — despite starting with the best intentions.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">With if-then plans</strong>, motivation still fades — but study hours actually increase. The behaviour becomes automatic, decoupled from how motivated the student feels.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 2. IF-THEN PLAN BUILDER
const IfThenPlanBuilder = () => {
  const [plans, setPlans] = useState([
    { ifText: '', thenText: '' },
    { ifText: '', thenText: '' },
    { ifText: '', thenText: '' },
  ]);
  const [showSummary, setShowSummary] = useState(false);

  const updatePlan = (index: number, field: 'ifText' | 'thenText', value: string) => {
    setPlans((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], [field]: value };
      return next;
    });
  };

  const checkQuality = (plan: { ifText: string; thenText: string }) => {
    const ifLower = plan.ifText.toLowerCase();
    const thenLower = plan.thenText.toLowerCase();
    const combined = ifLower + ' ' + thenLower;

    const hasTime = /\d{1,2}(:\d{2})?\s*(am|pm|o'clock)?/.test(combined) || /morning|afternoon|evening|night|after (dinner|lunch|breakfast|school|class)/.test(combined);
    const hasLocation = /desk|room|library|cafe|kitchen|table|school|home|bed|chair|office|study/.test(combined);
    const hasAction = /do|write|complete|solve|practice|read|review|revise|study|work on|start|begin|open|attempt/.test(thenLower);
    const hasDuration = /\d+\s*(min|minute|hour|hr|mins|minutes|hours|hrs|pomodoro)/.test(combined);

    return { hasTime, hasLocation, hasAction, hasDuration };
  };

  const getStrength = (checks: { hasTime: boolean; hasLocation: boolean; hasAction: boolean; hasDuration: boolean }) => {
    const count = [checks.hasTime, checks.hasLocation, checks.hasAction, checks.hasDuration].filter(Boolean).length;
    if (count <= 1) return { label: 'Weak', color: 'text-rose-500', bg: 'bg-rose-500', width: '25%' };
    if (count === 2) return { label: 'Fair', color: 'text-amber-500', bg: 'bg-amber-500', width: '50%' };
    if (count === 3) return { label: 'Strong', color: 'text-emerald-500', bg: 'bg-emerald-500', width: '75%' };
    return { label: 'Excellent', color: 'text-emerald-600', bg: 'bg-emerald-600', width: '100%' };
  };

  const allFilled = plans.every((p) => p.ifText.trim().length > 0 && p.thenText.trim().length > 0);

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">If-Then Plan Builder</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">Create 3 specific implementation intentions for your study schedule.</p>

      <div className="space-y-6">
        {plans.map((plan, i) => {
          const checks = checkQuality(plan);
          const strength = getStrength(checks);
          const hasContent = plan.ifText.trim().length > 0 || plan.thenText.trim().length > 0;

          return (
            <div key={i} className="p-5 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700">
              <p className="text-xs font-bold text-zinc-400 dark:text-zinc-500 mb-3">PLAN {i + 1}</p>
              <div className="grid md:grid-cols-2 gap-4 mb-3">
                <div>
                  <label className="block text-sm font-semibold text-rose-600 dark:text-rose-400 mb-1">If...</label>
                  <input
                    type="text"
                    value={plan.ifText}
                    onChange={(e) => updatePlan(i, 'ifText', e.target.value)}
                    placeholder={i === 0 ? 'it is 4pm on Monday' : i === 1 ? 'I sit down after dinner' : 'I finish my last class on Wednesday'}
                    className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 text-sm focus:outline-none focus:border-rose-400 dark:focus:border-rose-500 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-emerald-600 dark:text-emerald-400 mb-1">Then I will...</label>
                  <input
                    type="text"
                    value={plan.thenText}
                    onChange={(e) => updatePlan(i, 'thenText', e.target.value)}
                    placeholder={i === 0 ? 'do 25 minutes of Maths past papers' : i === 1 ? 'revise Biology flashcards for 30 minutes at my desk' : 'practice Chemistry problems for 20 minutes in the library'}
                    className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 text-sm focus:outline-none focus:border-emerald-400 dark:focus:border-emerald-500 transition-colors"
                  />
                </div>
              </div>

              {hasContent && (
                <MotionDiv initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} transition={{ duration: 0.3 }}>
                  <div className="flex flex-wrap gap-2 mb-2">
                    <span className={`text-xs px-2 py-1 rounded-full font-semibold ${checks.hasTime ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500'}`}>
                      {checks.hasTime ? '\u2713' : '\u2717'} Specific time
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full font-semibold ${checks.hasLocation ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500'}`}>
                      {checks.hasLocation ? '\u2713' : '\u2717'} Specific location
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full font-semibold ${checks.hasAction ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500'}`}>
                      {checks.hasAction ? '\u2713' : '\u2717'} Specific action
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full font-semibold ${checks.hasDuration ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500'}`}>
                      {checks.hasDuration ? '\u2713' : '\u2717'} Specific duration
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
                      <MotionDiv className={`h-full rounded-full ${strength.bg}`} initial={{ width: 0 }} animate={{ width: strength.width }} transition={{ duration: 0.5 }} />
                    </div>
                    <span className={`text-xs font-bold ${strength.color}`}>{strength.label}</span>
                  </div>
                </MotionDiv>
              )}
            </div>
          );
        })}
      </div>

      {allFilled && !showSummary && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="mt-6 text-center">
          <button onClick={() => setShowSummary(true)} className="px-6 py-3 bg-rose-500 hover:bg-rose-600 text-white font-bold rounded-xl transition-colors text-sm">
            View My Protocol
          </button>
        </MotionDiv>
      )}

      {showSummary && (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="mt-6 p-6 bg-rose-50 dark:bg-rose-950/20 rounded-xl border border-rose-200 dark:border-rose-800">
          <h5 className="font-serif text-lg font-semibold text-rose-800 dark:text-rose-200 mb-4 text-center">Your Implementation Intentions</h5>
          <div className="space-y-3">
            {plans.map((plan, i) => (
              <div key={i} className="p-3 bg-white dark:bg-zinc-800 rounded-lg border border-rose-200 dark:border-rose-800">
                <p className="text-sm text-zinc-700 dark:text-zinc-200">
                  <span className="font-bold text-rose-600 dark:text-rose-400">If</span> {plan.ifText}, <span className="font-bold text-emerald-600 dark:text-emerald-400">then I will</span> {plan.thenText}.
                </p>
              </div>
            ))}
          </div>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-4 text-center">Write these down. Put them where you'll see them. The specificity is what makes them work.</p>
        </MotionDiv>
      )}
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheImplementationProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'intention-action-gap', title: 'The Intention-Action Gap', eyebrow: '01 // The Problem', icon: Target },
    { id: 'if-then-plans', title: 'If-Then Plans', eyebrow: '02 // The Solution', icon: GitBranch },
    { id: 'temptation-bundling', title: 'Temptation Bundling', eyebrow: '03 // The Reward Hack', icon: Lightbulb },
    { id: 'commitment-devices', title: 'Commitment Devices', eyebrow: '04 // The Lock-In', icon: Shield },
    { id: 'building-your-protocol', title: 'Building Your Protocol', eyebrow: '05 // The System', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="48"
      moduleTitle="The Implementation Protocol"
      moduleSubtitle="The Intention-Action Blueprint"
      moduleDescription="Motivation doesn't predict action. Learn the single most powerful psychological technique for closing the gap between planning to study and actually doing it."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Intention-Action Gap." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Here is the most important statistic in the psychology of behaviour change: <Highlight description="Peter Sheeran (University of Sheffield) conducted a meta-analysis of 422 studies in 2002, examining the relationship between people's intentions and their actual behaviour. The finding that intentions explain only 28% of variance in behaviour is one of the most replicated findings in social psychology." theme={theme}>Sheeran's (2002) meta-analysis of 422 studies</Highlight> found that intentions — your motivation, goals, and plans — explain only 28% of the variance in actual behaviour. That means 72% of what determines whether you actually study is NOT your motivation.</p>
              <p>Think about what that means. Students who say "I'll study more this week" are barely more likely to do so than those who say nothing at all. The desire is real. The follow-through is not. This is the <Highlight description="The psychological chasm between wanting to do something and actually doing it. First formally described by Sheeran (2002), it explains why New Year's resolutions fail, why study schedules collapse, and why knowing what to do is not the same as doing it." theme={theme}>Intention-Action Gap</Highlight> — the psychological chasm between wanting to do something and actually doing it.</p>
              <p><Highlight description="Thomas Webb and Peter Sheeran (University of Sheffield) published a meta-analysis in 2006 demonstrating that the intention-action gap is largest for behaviours requiring sustained effort over extended periods. Short-term, one-off actions (like getting a vaccine) have a smaller gap than long-term commitments (like a six-month study plan)." theme={theme}>Webb and Sheeran (2006)</Highlight> showed that this gap is especially large for goals requiring sustained effort over time — like exam preparation. It's one thing to feel motivated on a Sunday evening when you're planning your week. It's another thing entirely to sit down at 4pm on a rainy Tuesday and actually open your textbook. Motivation is a feeling. Action is a behaviour. And the bridge between them is not willpower — it's something far more specific.</p>
              <IntentionGapComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="If-Then Plans." eyebrow="Step 2" icon={GitBranch} theme={theme}>
              <p>In 1999, psychologist <Highlight description="Peter Gollwitzer (New York University) published his landmark paper on implementation intentions, demonstrating that simply forming an 'if-then' plan — linking a specific situation to a specific action — roughly doubled the rate at which people followed through on their goals across 94 independent studies." theme={theme}>Peter Gollwitzer</Highlight> discovered what is arguably the single most effective behaviour change technique in psychology: <Highlight description="Implementation intentions are a specific form of planning that takes the format 'If [situation X occurs], then I will [perform behaviour Y].' Unlike goal intentions ('I want to study more'), implementation intentions pre-load the decision by linking a cue to an action, making the behaviour semi-automatic." theme={theme}>implementation intentions</Highlight>. These are specific "if-then" plans that link a situational cue to a desired behaviour. Across 94 independent studies, they roughly doubled follow-through rates.</p>
              <p>The format is deceptively simple: <strong>"If [situation], then [action]."</strong> For example: "If it is 4:00pm on Monday, then I will sit at my desk and do 25 minutes of Maths past papers." The power is entirely in the specificity. Not "I'll study Maths this week" but exactly when, where, and what.</p>
              <p><Highlight description="Gollwitzer and Sheeran published a comprehensive meta-analysis in 2006 (effect size d = 0.65, which is considered a medium-to-large effect) showing that implementation intentions work by creating automatic cue-behaviour links. The situational cue activates the planned response without requiring conscious deliberation — the same mechanism that drives habits." theme={theme}>Gollwitzer and Sheeran's (2006) meta-analysis</Highlight> (d = 0.65, a medium-to-large effect) showed why if-then plans work: they create an automatic trigger. The situation cue activates the behaviour without requiring conscious motivation. When 4pm on Monday arrives, you don't deliberate about whether you feel like studying. The cue fires and the behaviour follows — the same mechanism that drives habits. You pre-decide, so in the moment, there's no decision to make. And it's the decision that kills you. Every moment of "should I study now or later?" is a moment you're likely to choose later.</p>
              <IfThenPlanBuilder />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Temptation Bundling." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
              <p><Highlight description="Katherine Milkman (University of Pennsylvania), Julia Minson, and Kevin Volpp published a 2014 study where participants were given audiobooks they could only listen to at the gym. This simple constraint — bundling a 'want' with a 'should' — increased gym attendance by 51% compared to the control group." theme={theme}>Milkman, Minson, and Volpp (2014)</Highlight> tested an elegantly simple idea: what if you paired an unpleasant task with an enjoyable one? They gave participants access to addictive audiobooks — but only at the gym. The result: gym attendance increased by 51%. Not through willpower. Not through motivation. Through strategic bundling of a "should" activity with a "want" activity.</p>
              <p>The principle applies directly to studying. A <Highlight description="Temptation bundling works by creating a genuine incentive rather than relying on willpower. The key constraint is that the 'want' activity is ONLY available during the 'should' activity. If you allow yourself the reward at other times, the bundling effect collapses." theme={theme}>temptation bundle</Highlight> pairs something you need to do (studying) with something you want to do (listening to a favourite playlist, sitting in your favourite cafe, having a particular snack). The critical constraint: the "want" activity is ONLY available during the "should" activity. If you listen to that playlist at other times, the bundle breaks. The exclusivity is what creates the pull.</p>
              <p>Practical examples for students: only listen to your favourite playlist while doing past papers. Only go to that nice cafe when you're studying. Only have that particular snack during study sessions. Only watch that YouTube channel as a reward between pomodoros. The key is finding something you genuinely look forward to and making it conditional on the study behaviour. You're not using willpower to force yourself to study — you're creating a genuine incentive that makes you want to start.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Commitment Devices." eyebrow="Step 4" icon={Shield} theme={theme}>
              <p><Highlight description="Dan Ariely and Klaus Wertenbroch (MIT Sloan) published a 2002 study where students were given the choice to set their own deadlines for three papers, with penalties for late submission. Students who set binding deadlines for themselves performed significantly better than those given total flexibility — demonstrating that self-imposed constraints improve outcomes." theme={theme}>Ariely and Wertenbroch (2002)</Highlight> showed that students who set their own deadlines — and accepted penalties for missing them — performed significantly better than those given complete flexibility. This is counterintuitive. More freedom should mean better outcomes, right? Wrong. Freedom to act is also freedom not to act. Commitment devices work by raising the cost of inaction, making it harder to do the wrong thing.</p>
              <p>There are several practical commitment devices that work for students. First: <strong>give your phone to a friend</strong> during study sessions. The social accountability means you can't mindlessly scroll — and asking for it back feels embarrassing enough to keep you studying. Second: <strong>use app blockers with a time lock you can't override</strong>. Not ones with an "unlock early" option — that defeats the purpose. Third: <strong>tell someone your study plan</strong>. <Highlight description="Robert Cialdini (Arizona State University) demonstrated in his 2001 work on influence that public commitment significantly increases follow-through. When we tell someone what we intend to do, we feel psychological pressure to remain consistent with that stated intention." theme={theme}>Cialdini (2001)</Highlight> showed that public commitment increases follow-through because we feel pressure to remain consistent with what we've told others. Simply texting a friend "I'm going to study Biology from 4-5pm" makes it more likely you'll actually do it.</p>
              <p>Fourth: <strong>study with a partner</strong>. The "appointment effect" means that showing up feels obligatory rather than optional. You wouldn't cancel a meeting with someone at 4pm. Make your study session feel the same way. The common thread across all commitment devices is this: they convert a private intention into a public obligation, and they raise the cost of not following through.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Building Your Protocol." eyebrow="Step 5" icon={Flag} theme={theme}>
              <p>The Implementation Protocol combines all four tools into a complete system. Each tool addresses a different failure point in the intention-action chain, and together they make follow-through nearly automatic. Here's how to assemble your protocol.</p>
              <p><strong>Step 1: Write 3-5 if-then plans</strong> covering your weekly study schedule. Make them specific enough to be automatic. Not "I'll study Biology" but "If it is 5pm on Tuesday and I am at my desk, then I will do 25 minutes of Biology flashcards." <strong>Step 2: Attach a temptation bundle</strong> to your hardest subject — the one you're most likely to avoid. Make it the only time you get that reward. <strong>Step 3: Install one commitment device</strong> — something that raises the cost of skipping. Tell a friend, use an app blocker, or schedule a study partner. <strong>Step 4: Review and revise weekly</strong>. Plans that don't work aren't failures — they're data. If your Tuesday 5pm plan keeps failing because you're tired after football practice, move it. Adjust the system, don't blame yourself.</p>
              <p><Highlight description="Angela Duckworth, Heidi Grant, Benjamin Loew, Gabriele Oettingen, and Peter Gollwitzer published a 2011 study showing that implementation intentions were especially effective for students who had previously struggled with self-regulation. The students who needed them most benefited the most — suggesting this is not just a technique for the already-organised." theme={theme}>Duckworth, Grant, Loew, Oettingen, and Gollwitzer (2011)</Highlight> found that implementation intentions were especially effective for students who had previously struggled with self-regulation. If you're someone who regularly plans to study and then doesn't — if that gap between intention and action feels painfully familiar — then this technique was literally designed for you. The students who need it most benefit the most.</p>
              <MicroCommitment theme={theme}>
                <p>Right now, write one if-then plan for tomorrow. Make it specific: "If [exact time and place], then I will [exact subject and technique] for [exact duration]." Text it to a friend or write it on a sticky note and put it where you'll see it in the morning. One specific plan is worth more than a hundred good intentions.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheImplementationProtocolModule;
