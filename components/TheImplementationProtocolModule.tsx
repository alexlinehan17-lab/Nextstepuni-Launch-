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
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

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
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Most students rely on motivation alone to actually get studying done. But does that actually work?</p>
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
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Motivation fades</strong> and without a specific plan, study hours collapse with it. By week 6, you've basically stopped -- even though you started out fully committed.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">With if-then plans</strong>, motivation still fades -- but study hours actually go up. The studying becomes automatic, no longer depending on how motivated you feel.</p>
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
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">Create 3 specific if-then plans for your study schedule.</p>

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
  const { northStar } = useNorthStar();
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
      moduleTitle="The Implementation Playbook"
      moduleSubtitle="The Intention-Action Blueprint"
      moduleDescription="Feeling motivated doesn't mean you'll actually study. This module teaches you a dead-simple planning trick that closes the gap between saying you'll study and actually doing it."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Close the Gap"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Intention-Action Gap." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Here is the most important thing you need to know about getting stuff done: <Highlight description="When researchers looked at over 400 studies on this, they found that how motivated you feel only explains about 28% of whether you actually do the thing. The other 72%? That comes down to strategy, not willpower." theme={theme}>a massive review of over 400 studies</Highlight> found that your intentions -- your motivation, goals, and plans -- only explain about 28% of whether you actually follow through. That means 72% of what determines whether you actually study has nothing to do with how motivated you feel.</p>
              <p>Think about what that means. Students who say "I'll study more this week" are barely more likely to do so than those who say nothing at all. The desire is real. The follow-through is not. This is the <Highlight description="That massive gap between wanting to do something and actually doing it. It's why New Year's resolutions fail, why study schedules fall apart after a week, and why knowing what you should do is completely different from doing it." theme={theme}>Intention-Action Gap</Highlight> -- the gap between wanting to do something and actually doing it.</p>
              <p><Highlight description="This gap gets even worse when the thing you need to do requires effort over a long time. A one-off task? Not so bad. But something like a six-month Leaving Cert study plan? That's where the gap is at its widest." theme={theme}>Here's the kicker</Highlight>: this gap is especially large for goals that need sustained effort over time -- like Leaving Cert prep. It's one thing to feel motivated on a Sunday evening when you're planning your week. It's another thing entirely to sit down at 4pm on a rainy Tuesday and actually open your textbook. Motivation is a feeling. Action is a behaviour. And the bridge between them is not willpower -- it's something far more specific.</p>
              <IntentionGapComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="If-Then Plans." eyebrow="Step 2" icon={GitBranch} theme={theme}>
              <p>In the late 90s, <Highlight description="A psychologist figured out that simply making a specific 'if-then' plan -- connecting a situation to an action -- roughly doubled how often people actually followed through on their goals. Not a small bump. Doubled." theme={theme}>a psychologist</Highlight> discovered what might be the single most effective way to actually change your behaviour: <Highlight description="Instead of a vague goal like 'I want to study more,' you make a specific plan: 'If this situation happens, then I'll do this action.' You're pre-loading the decision so you don't have to think about it in the moment. It basically puts your good intentions on autopilot." theme={theme}>implementation intentions</Highlight>. These are specific "if-then" plans that link a trigger to an action. Across 94 separate studies, they roughly doubled follow-through rates.</p>
              <p>The format is deceptively simple: <strong>"If [situation], then [action]."</strong> For example: "If it is 4:00pm on Monday, then I will sit at my desk and do 25 minutes of Maths past papers." The power is entirely in the specificity. Not "I'll study Maths this week" but exactly when, where, and what.</p>
              <p><Highlight description="A big review of the research showed that if-then plans work because they create an automatic link between a trigger and a behaviour -- the same way habits work. The situation fires and you just do the thing, without having to convince yourself first." theme={theme}>A big review of the research</Highlight> showed why if-then plans work: they create an automatic trigger. The situation fires and the behaviour follows, without needing you to feel motivated in that moment. When 4pm on Monday arrives, you don't sit there debating whether you feel like studying. The trigger goes off and you just do it -- the same way habits work. You've already made the decision in advance, so in the moment, there's no decision to make. And it's the decision that kills you. Every moment of "should I study now or later?" is a moment you're likely to choose later.</p>
              <IfThenPlanBuilder />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Temptation Bundling." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'implementation-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p><Highlight description="In one experiment, people were given really addictive audiobooks they could only listen to while at the gym. That one simple rule -- you only get the fun thing while doing the hard thing -- boosted gym attendance by 51%. No extra willpower needed." theme={theme}>Researchers tested a brilliantly simple idea</Highlight>: what if you paired something boring with something you actually enjoy? They gave people access to addictive audiobooks -- but only at the gym. The result: gym attendance went up by 51%. Not through willpower. Not through motivation. Just by bundling a "should" with a "want."</p>
              <p>This works perfectly for studying. A <Highlight description="You pair something you have to do (studying) with something you actually enjoy -- but the catch is you ONLY allow yourself the fun thing during the hard thing. If you let yourself have the reward whenever, it stops working. The exclusivity is what makes it powerful." theme={theme}>temptation bundle</Highlight> pairs something you need to do (studying) with something you want to do (listening to a favourite playlist, sitting in your favourite cafe, having a particular snack). The critical rule: the "want" activity is ONLY available during the "should" activity. If you listen to that playlist at other times, the bundle breaks. The exclusivity is what creates the pull.</p>
              <p>Practical examples for students: only listen to your favourite playlist while doing past papers. Only go to that nice cafe when you're studying. Only have that particular snack during study sessions. Only watch that YouTube channel as a reward between pomodoros. The key is finding something you genuinely look forward to and making it conditional on the study behaviour. You're not using willpower to force yourself to study — you're creating a genuine incentive that makes you want to start.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Commitment Devices." eyebrow="Step 4" icon={Shield} theme={theme}>
              <p><Highlight description="In one experiment, students who set their own deadlines -- and faced penalties for missing them -- did way better than students given total flexibility. Sounds backwards, right? But when you can do something 'whenever,' you usually do it never. Locking yourself in actually works." theme={theme}>One study found something surprising</Highlight>: students who set their own deadlines -- and accepted penalties for missing them -- performed significantly better than those given complete flexibility. This is counterintuitive. More freedom should mean better outcomes, right? Wrong. Freedom to act is also freedom not to act. Commitment devices work by raising the cost of not following through, making it harder to skip.</p>
              <p>There are several practical commitment devices that work for students. First: <strong>give your phone to a friend</strong> during study sessions. The social accountability means you can't mindlessly scroll — and asking for it back feels embarrassing enough to keep you studying. Second: <strong>use app blockers with a time lock you can't override</strong>. Not ones with an "unlock early" option — that defeats the purpose. Third: <strong>tell someone your study plan</strong>. <Highlight description="When you tell someone what you're going to do, you feel pressure to actually do it. Nobody wants to be the person who says they'll study and then doesn't. That social pressure is surprisingly effective." theme={theme}>Here's why this works</Highlight>: when you tell someone what you're going to do, you feel pressure to actually follow through. Nobody wants to say one thing and do another. Simply texting a friend "I'm going to study Biology from 4-5pm" makes it more likely you'll actually do it.</p>
              <p>Fourth: <strong>study with a partner</strong>. When you've arranged to meet someone, showing up feels like something you have to do, not something you can skip. You wouldn't cancel on someone at 4pm. Make your study session feel the same way. The common thread across all these tricks is this: they turn a private plan into something you'd feel bad about ditching, and they make skipping harder than just doing the work.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Building Your Protocol." eyebrow="Step 5" icon={Flag} theme={theme}>
              <p>The Implementation Playbook combines all four tools into one system. Each one tackles a different reason you might not follow through, and together they make studying close to automatic. Here's how to put yours together.</p>
              <p><strong>Step 1: Write 3-5 if-then plans</strong> covering your weekly study schedule. Make them specific enough to be automatic. Not "I'll study Biology" but "If it is 5pm on Tuesday and I am at my desk, then I will do 25 minutes of Biology flashcards." <strong>Step 2: Attach a temptation bundle</strong> to your hardest subject — the one you're most likely to avoid. Make it the only time you get that reward. <strong>Step 3: Install one commitment device</strong> — something that raises the cost of skipping. Tell a friend, use an app blocker, or schedule a study partner. <strong>Step 4: Review and revise weekly</strong>. Plans that don't work aren't failures — they're data. If your Tuesday 5pm plan keeps failing because you're tired after football practice, move it. Adjust the system, don't blame yourself.</p>
              <p><Highlight description="If-then plans are actually most effective for the students who struggle the most with following through. If you're someone who always plans to study but never does, this is genuinely the best tool for you. It's not just for the organised kids -- it works best for everyone else." theme={theme}>Here's the best part</Highlight>: if-then plans are especially effective for students who've always struggled with follow-through. If you're someone who regularly plans to study and then doesn't -- if that gap between intention and action feels painfully familiar -- then this technique was basically built for you. The students who need it most benefit the most.</p>
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
