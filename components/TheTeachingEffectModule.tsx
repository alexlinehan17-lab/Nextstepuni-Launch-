/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Users, Brain, MessageSquare, Lightbulb, Flag } from 'lucide-react';
import { ModuleProgress } from '../types';
import { limeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = limeTheme;
const MotionDiv = motion.div as any;

// --- INTERACTIVE COMPONENTS ---

// 1. TEACH VS TEST COMPARISON (Planning Paradox style dual-chart)
const TeachVsTestComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Study', 'Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30'];

  // Preparing for a Test: raw recall starts high but fades; organization stays low
  const testRecall = [0.70, 0.65, 0.55, 0.42, 0.30, 0.20];
  const testOrganization = [0.20, 0.22, 0.25, 0.22, 0.18, 0.15];

  // Preparing to Teach: raw recall moderate but stable; organization climbs strongly
  const teachRecall = [0.55, 0.52, 0.50, 0.48, 0.45, 0.42];
  const teachOrganization = [0.30, 0.45, 0.58, 0.68, 0.75, 0.80];

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

  const testPhases = [
    { label: 'Memorising facts', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Fading', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Fragmented', x1: 0.66, x2: 1, color: '#ef4444' },
  ];
  const teachPhases = [
    { label: 'Building framework', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Deepening', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Teachable', x1: 0.66, x2: 1, color: '#10b981' },
  ];

  const Chart = ({ recall, organization, phases, areaColor, areaId, label }: {
    recall: number[]; organization: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
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
      {[0.25, 0.5, 0.75, 1.0].map(v => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      {/* Baseline */}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
      {/* Recall area */}
      <motion.path
        d={buildArea(recall)}
        fill={`url(#${areaId})`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      {/* Recall line (solid) */}
      <motion.path
        d={buildLine(recall)}
        fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {/* Organization line (dashed) */}
      <motion.path
        d={buildLine(organization)}
        fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
      />
      {/* Recall dots */}
      {recall.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (recall.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
          initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
        />
      ))}
      {/* Y-axis labels */}
      <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
      {/* X-axis labels */}
      {xLabels.map((m, i) => (
        <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
      ))}
      {/* Phase labels */}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
      ))}
      {/* Chart label */}
      <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
      {/* Legend */}
      <line x1={W - padR - 120} x2={W - padR - 104} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 100} y={17} fontSize="8" fill="#a1a1aa">Raw Recall</text>
      <line x1={W - padR - 54} x2={W - padR - 38} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 34} y={17} fontSize="8" fill="#a1a1aa">Organized</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Teach vs. Test Effect</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Same material. Different expectation. Dramatically different outcomes.</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">What happens when you study to teach versus study to pass a test? The difference is not just how much you remember, but how you organize what you know.</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-lime-500 text-white hover:bg-lime-600 transition-colors">
            Reveal the Effect
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart recall={testRecall} organization={testOrganization} phases={testPhases}
                areaColor="#ef4444" areaId="test-grad" label="Preparing for a Test" />
            </div>
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart recall={teachRecall} organization={teachOrganization} phases={teachPhases}
                areaColor="#10b981" areaId="teach-grad" label="Preparing to Teach" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Test preppers</strong> absorb facts quickly but store them in isolation. Without organizational structure, recall decays rapidly and knowledge fragments under pressure.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Teaching preppers</strong> build hierarchical frameworks from the start. Even though initial intake is lower, the organized structure makes knowledge durable and retrievable.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 2. EXPLAIN IT BACK CHALLENGE
const ORIGINAL_CONCEPT = "Natural selection is the process by which organisms with traits better suited to their environment survive and reproduce at higher rates, passing those traits to the next generation. Over time, this differential survival and reproduction leads to changes in the inherited characteristics of a population, driving the adaptation of species to their environments.";

const ExplainItBackChallenge = () => {
  const [userText, setUserText] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const originalWords = useMemo(() => {
    const words = ORIGINAL_CONCEPT.toLowerCase().replace(/[.,;:!?'"()]/g, '').split(/\s+/);
    // Filter to meaningful words (skip common ones)
    const common = new Set(['the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'and', 'or', 'but', 'not', 'this', 'that', 'it', 'its', 'their', 'which', 'as', 'over', 'leads', 'more', 'than']);
    return new Set(words.filter(w => w.length > 3 && !common.has(w)));
  }, []);

  const analysis = useMemo(() => {
    if (!userText.trim()) return { wordCount: 0, jargonWords: [], simplicityScore: 0 };
    const words = userText.trim().split(/\s+/);
    const wordCount = words.length;
    const userWordsLower = userText.toLowerCase().replace(/[.,;:!?'"()]/g, '');
    const jargonWords: string[] = [];
    originalWords.forEach(ow => {
      if (userWordsLower.includes(ow)) {
        jargonWords.push(ow);
      }
    });
    // Simplicity: shorter is better (if key ideas preserved). Scale: 100 = very concise, 0 = very verbose
    const originalLen = ORIGINAL_CONCEPT.split(/\s+/).length;
    const ratio = wordCount / originalLen;
    const simplicityScore = ratio <= 0.5 ? 100 : ratio <= 1.0 ? Math.round(100 - (ratio - 0.5) * 120) : Math.max(0, Math.round(40 - (ratio - 1.0) * 60));
    return { wordCount, jargonWords, simplicityScore };
  }, [userText, originalWords]);

  const handleSubmit = () => {
    if (userText.trim().length > 10) setSubmitted(true);
  };

  const handleReset = () => {
    setUserText('');
    setSubmitted(false);
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Explain It Back Challenge</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-6">Read the concept below, then explain it in your own words. No copying allowed.</p>

      <div className="p-5 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700 mb-6">
        <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">Original Concept</p>
        <p className="text-sm text-zinc-700 dark:text-zinc-200 leading-relaxed font-serif">{ORIGINAL_CONCEPT}</p>
      </div>

      {!submitted ? (
        <>
          <textarea
            value={userText}
            onChange={(e) => setUserText(e.target.value)}
            placeholder="Now explain this concept in your own words, as if teaching a friend who has never heard of it..."
            className="w-full h-36 p-4 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-900/50 text-sm text-zinc-700 dark:text-zinc-200 placeholder:text-zinc-400 resize-none focus:outline-none focus:ring-2 focus:ring-lime-400/50 transition-all"
          />

          {/* Live analysis */}
          {userText.trim().length > 0 && (
            <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="mt-4 grid grid-cols-3 gap-3">
              <div className="text-center p-3 rounded-xl bg-zinc-100 dark:bg-zinc-700/50 border border-zinc-200 dark:border-zinc-600">
                <p className="text-lg font-bold text-zinc-700 dark:text-zinc-200">{analysis.wordCount}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">Words</p>
              </div>
              <div className={`text-center p-3 rounded-xl border ${analysis.jargonWords.length > 5 ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800' : 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800'}`}>
                <p className={`text-lg font-bold ${analysis.jargonWords.length > 5 ? 'text-amber-700 dark:text-amber-300' : 'text-emerald-700 dark:text-emerald-300'}`}>{analysis.jargonWords.length}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">Borrowed Words</p>
              </div>
              <div className={`text-center p-3 rounded-xl border ${analysis.simplicityScore >= 60 ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800' : 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800'}`}>
                <p className={`text-lg font-bold ${analysis.simplicityScore >= 60 ? 'text-emerald-700 dark:text-emerald-300' : 'text-amber-700 dark:text-amber-300'}`}>{analysis.simplicityScore}%</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">Simplicity</p>
              </div>
            </MotionDiv>
          )}

          {analysis.jargonWords.length > 0 && (
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-3 p-3 rounded-lg bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800">
              <p className="text-xs font-semibold text-amber-700 dark:text-amber-300 mb-1">Words borrowed from the original:</p>
              <div className="flex flex-wrap gap-1.5">
                {analysis.jargonWords.map((w, i) => (
                  <span key={i} className="px-2 py-0.5 text-xs font-medium bg-amber-200 dark:bg-amber-800/50 text-amber-800 dark:text-amber-200 rounded-full">{w}</span>
                ))}
              </div>
            </MotionDiv>
          )}

          <div className="mt-6 text-center">
            <button
              onClick={handleSubmit}
              disabled={userText.trim().length <= 10}
              className="px-6 py-3 bg-lime-500 hover:bg-lime-600 disabled:bg-zinc-300 dark:disabled:bg-zinc-600 text-white font-bold rounded-xl transition-colors text-sm disabled:cursor-not-allowed"
            >
              Submit My Explanation
            </button>
          </div>
        </>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-700">
              <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2">Original</p>
              <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">{ORIGINAL_CONCEPT}</p>
            </div>
            <div className="p-4 rounded-xl bg-lime-50 dark:bg-lime-900/20 border border-lime-200 dark:border-lime-800">
              <p className="text-xs font-semibold uppercase tracking-wider text-lime-600 dark:text-lime-400 mb-2">Your Explanation</p>
              <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">{userText}</p>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3 mb-6">
            <div className="text-center p-3 rounded-xl bg-zinc-100 dark:bg-zinc-700/50 border border-zinc-200 dark:border-zinc-600">
              <p className="text-lg font-bold text-zinc-700 dark:text-zinc-200">{analysis.wordCount}</p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400">Words Used</p>
            </div>
            <div className={`text-center p-3 rounded-xl border ${analysis.jargonWords.length > 5 ? 'bg-rose-50 dark:bg-rose-900/20 border-rose-200 dark:border-rose-800' : analysis.jargonWords.length > 2 ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800' : 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800'}`}>
              <p className={`text-lg font-bold ${analysis.jargonWords.length > 5 ? 'text-rose-700 dark:text-rose-300' : analysis.jargonWords.length > 2 ? 'text-amber-700 dark:text-amber-300' : 'text-emerald-700 dark:text-emerald-300'}`}>{analysis.jargonWords.length}</p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400">Borrowed Words</p>
            </div>
            <div className={`text-center p-3 rounded-xl border ${analysis.simplicityScore >= 60 ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800' : 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800'}`}>
              <p className={`text-lg font-bold ${analysis.simplicityScore >= 60 ? 'text-emerald-700 dark:text-emerald-300' : 'text-amber-700 dark:text-amber-300'}`}>{analysis.simplicityScore}%</p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400">Simplicity Score</p>
            </div>
          </div>

          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-xl text-sm font-medium ${analysis.jargonWords.length <= 2 && analysis.simplicityScore >= 60 ? 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800' : analysis.jargonWords.length <= 5 ? 'bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800' : 'bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800'}`}
          >
            {analysis.jargonWords.length <= 2 && analysis.simplicityScore >= 60
              ? 'Excellent knowledge-building! You used your own words and analogies to reconstruct the concept. This is exactly the kind of explanation that produces deep, durable learning.'
              : analysis.jargonWords.length <= 5
              ? 'Good effort, but some of your phrasing mirrors the original text. Try pushing further — can you explain it using a completely different analogy or metaphor? That\'s the leap from knowledge-telling to knowledge-building.'
              : 'This looks like knowledge-telling — you\'re echoing the original text rather than rebuilding the concept in your own framework. Close the original, and try explaining it as if to a 12-year-old. Use everyday examples and analogies.'}
          </MotionDiv>

          <div className="mt-6 text-center">
            <button onClick={handleReset} className="px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-semibold rounded-xl transition-colors text-sm">
              Try Again
            </button>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheTeachingEffectModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'protege-effect', title: 'The Protege Effect', eyebrow: '01 // The Discovery', icon: Users },
    { id: 'explaining-forces-restructuring', title: 'Explaining Forces Restructuring', eyebrow: '02 // The Mechanism', icon: Brain },
    { id: 'self-explanation-advantage', title: 'The Self-Explanation Advantage', eyebrow: '03 // The Solo Protocol', icon: MessageSquare },
    { id: 'feynman-multiplier', title: 'The Feynman Multiplier', eyebrow: '04 // The Technique', icon: Lightbulb },
    { id: 'teaching-protocol', title: 'The Teaching Protocol', eyebrow: '05 // The System', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="46"
      moduleTitle="The Teaching Effect"
      moduleSubtitle="The Protege Protocol"
      moduleDescription="Learn why preparing to teach someone produces deeper learning than preparing for a test — even if you never actually teach."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Protege Effect." eyebrow="Step 1" icon={Users} theme={theme}>
              <p>Here is one of the most surprising findings in all of learning science. In 2014, <Highlight description="John Nestojko and colleagues at Washington University in St. Louis conducted an elegant experiment: they gave two groups identical material to study. One group was told 'you will be tested on this.' The other was told 'you will teach this to another student afterwards.' Neither group actually taught anyone — but the teaching-expectation group dramatically outperformed the test-expectation group on every measure." theme={theme}>Nestojko et al. (2014)</Highlight> ran an experiment that would change how we think about learning. They gave two groups of students identical material to study. One group was told: "You will be tested on this." The other group was told: "You will teach this to another student afterwards."</p>
              <p>The results were striking. The group who expected to teach produced better organized recall and performed significantly better on every measure — free recall, short answer, even on questions that required deep understanding rather than surface recognition. But here is the stunning part: <Highlight description="Neither group in the Nestojko study actually taught anyone. The mere expectation of teaching was sufficient to change how participants encoded and organized the material. This means the learning benefit comes from the mental preparation, not the act of teaching itself." theme={theme}>neither group actually taught anyone</Highlight>. The mere expectation of teaching changed HOW they processed the material. Instead of passively absorbing facts, they organized information hierarchically, identified key principles, and built explanatory frameworks — all without being told to do so.</p>
              <p>This is the <Highlight description="The Protege Effect is the well-documented finding that preparing to teach (or actually teaching) produces deeper learning than preparing for a test. First described by Chase et al. (2009), it has been replicated across ages, subjects, and cultures. The effect works because teaching requires you to reorganize knowledge into a coherent, transmittable structure." theme={theme}>Protege Effect</Highlight>: teaching — even imagined teaching — restructures knowledge. When you expect to teach, your brain shifts from "How do I remember this?" to "How do I explain this?" That single shift activates a fundamentally different and more powerful encoding process. You don't just store facts — you build a mental architecture that connects them, because you know someone else will need to navigate that architecture.</p>
              <TeachVsTestComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Explaining Forces Restructuring." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p>Why does the expectation of teaching produce such a dramatic effect? The answer lies in what happens when you try to explain something. <Highlight description="Rod Roscoe and Michelene Chi (Arizona State University) published two landmark studies in 2007 and 2008 showing that explaining to others forces 'knowledge restructuring' — the process of breaking apart your existing understanding and rebuilding it in a more coherent, connected form. This restructuring is what produces durable learning." theme={theme}>Roscoe and Chi (2007, 2008)</Highlight> showed that explaining to others forces what they called "knowledge restructuring." You cannot explain something you don't truly understand, so the act of explaining — or even preparing to explain — exposes every gap, every shallow connection, every concept you thought you understood but actually just recognised.</p>
              <p>Critically, Roscoe and Chi identified two types of explanation. The first is <Highlight description="Knowledge-telling is the shallow form of explanation where you simply repeat back facts and definitions in roughly the same form you received them. It produces minimal learning gains because it doesn't require any restructuring of your understanding. The test: if your explanation uses the exact same words as the textbook, you're knowledge-telling." theme={theme}>knowledge-telling</Highlight> — simply repeating facts back in roughly the same form you received them. "Photosynthesis is the process by which plants convert light energy into chemical energy." That's knowledge-telling. You haven't transformed anything; you've just echoed the textbook. The second type is <Highlight description="Knowledge-building is the deep form of explanation where you generate new connections, analogies, and examples that weren't in the original material. It requires genuine understanding because you must reconstruct the concept in a new framework. This produces significant learning gains because the reconstruction process strengthens and reorganizes your mental model." theme={theme}>knowledge-building</Highlight> — generating new connections, analogies, and examples. "It's like the plant is running a solar-powered factory — light is the electricity, CO2 and water are the raw materials, and glucose is the product that comes off the assembly line."</p>
              <p>Only knowledge-building produces genuine learning gains. The test is simple: if your explanation uses the exact same words as the textbook, you're knowledge-telling. If you use your own analogies, your own examples, your own structure — you're knowledge-building. And it's knowledge-building that produces the deep, connected understanding that transfers to new problems and survives the pressure of exam conditions.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Self-Explanation Advantage." eyebrow="Step 3" icon={MessageSquare} theme={theme}>
              <p>You might be thinking: "This is all well and good, but I don't have someone to teach." The remarkable discovery is that you don't need another person. <Highlight description="Michelene Chi and colleagues (1989) conducted a seminal study with physics students. Those who self-explained — pausing after each worked example to explain to themselves why each step was taken — solved 82% of new physics problems, compared to just 46% for students who simply read through the examples. The effect size was massive, and it worked without any external audience." theme={theme}>Chi et al. (1989)</Highlight> conducted one of the most cited studies in educational psychology. They asked physics students to study worked examples, but with one critical instruction: pause after each example and explain to yourself why each step was taken. The self-explainers solved 82% of new problems on a transfer test. The non-explainers solved just 46%.</p>
              <p><Highlight description="Self-explanation is the practice of pausing during learning to explain concepts, steps, or reasoning to yourself. It is nearly as powerful as explaining to another person because the cognitive work is the same — you must retrieve, organize, and articulate your understanding. The 'audience' is secondary; the restructuring process is what matters." theme={theme}>Self-explanation</Highlight> — pausing after each concept to explain it to yourself — is nearly as powerful as explaining to another person. The key findings from Chi's research were threefold. First, self-explainers generated significantly more inferences, building bridges between new information and their prior knowledge. Second, they identified their own misunderstandings in real-time — the act of trying to explain exposed gaps that passive reading never would. Third, and perhaps most powerfully, <Highlight description="Chi's research showed that self-explanation produced the largest learning gains for students who started with the weakest understanding. The technique effectively narrowed the achievement gap between high and low performers, suggesting it is especially valuable for students who feel behind or confused." theme={theme}>the effect was strongest for the weakest students</Highlight>, dramatically narrowing the achievement gap.</p>
              <p>This means self-explanation is a great equaliser. If you're struggling with a topic, the instinct is to re-read the material more slowly. But the research says the opposite: stop reading and start explaining. Even if your explanation is halting and full of gaps, the process of generating it is doing the heavy cognitive lifting that passive re-reading never will.</p>
              <ExplainItBackChallenge />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Feynman Multiplier." eyebrow="Step 4" icon={Lightbulb} theme={theme}>
              <p>The research on teaching and self-explanation converges on a single, powerful technique that has become one of the most celebrated learning methods in existence. <Highlight description="Logan Fiorella and Richard Mayer (UC Santa Barbara) conducted a major meta-analysis in 2013-2014 examining 'generative learning strategies' — methods where learners actively produce something rather than passively absorbing. They found that generating explanations (even to an imaginary audience) produced an average effect size of d = 0.77, making it one of the highest-utility learning strategies ever documented." theme={theme}>Fiorella and Mayer (2013, 2014)</Highlight> conducted a comprehensive meta-analysis of what they called "generative learning strategies" — methods where learners actively produce something rather than passively receive information. Their conclusion: generating explanations, even to an imaginary audience, is one of the highest-utility learning strategies available, producing large effect sizes (d = 0.77).</p>
              <p>This finding gives scientific backing to a technique that the physicist <Highlight description="The Feynman Technique is named after Nobel laureate Richard Feynman, who was legendary for his ability to explain complex physics in simple, intuitive terms. The technique formalizes his approach: write a concept name, explain it simply, identify where you stumble, then return to the source to fill the gap. Each stumble point is a learning target." theme={theme}>Richard Feynman</Highlight> made famous through his extraordinary ability to explain complex physics in simple, intuitive language. The Feynman Technique works in four steps. Step one: write the concept name at the top of a blank page. Step two: explain it as if you were teaching a 12-year-old — no jargon, no textbook phrases, just clear simple language with concrete examples. Step three: when you stumble — when you reach a point where your explanation breaks down or becomes vague — go back to the source material and fill that specific gap. Step four: simplify further and develop analogies.</p>
              <p>The genius of this technique is in step three. The stumble points ARE the learning targets. Each moment where your explanation breaks down is a moment where your understanding has a hole in it. Without the Feynman Technique, those holes remain invisible — your brain papers over them with a feeling of familiarity. The technique makes them visible, specific, and actionable. After each round, your explanation gets smoother, your analogies get sharper, and your understanding gets deeper. If you can explain a concept to a 12-year-old, you truly understand it.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Teaching Protocol." eyebrow="Step 5" icon={Flag} theme={theme}>
              <p>Let's bring everything together into a practical system you can use in every study session. The research is clear: <Highlight description="Dunlosky et al. (2013) conducted the most comprehensive review of learning strategies ever published, evaluating ten techniques across hundreds of studies. Self-explanation and practice testing were ranked as the two highest-utility learning strategies. Highlighting, re-reading, and summarisation were ranked as the lowest. The teaching protocol combines the two highest-utility strategies into a single workflow." theme={theme}>Dunlosky et al. (2013)</Highlight> reviewed hundreds of studies on learning strategies and ranked self-explanation and practice testing as the two highest-utility techniques across all research. Highlighting, re-reading, and summarisation — the strategies most students rely on — were ranked among the lowest. The Teaching Protocol is designed to replace low-utility habits with high-utility ones.</p>
              <p>Here is the protocol. Before each study session, set the intention: "I will teach this to someone." This single mental shift, as Nestojko's research showed, changes your processing even before you open a book. While studying, take <Highlight description="Generative notes are notes where you rephrase concepts in your own words, draw connections to other topics, and generate your own examples — rather than copying text verbatim. This mirrors the knowledge-building process identified by Roscoe and Chi. The Note-Taking Paradox module covers this technique in depth." theme={theme}>generative notes</Highlight> — rephrase concepts in your own words, draw connections, and generate your own examples rather than copying the textbook. After studying, explain the material aloud. It doesn't matter who you explain it to — a friend, a family member, a pet, a wall. The audience is irrelevant; the cognitive process of generating the explanation is what matters.</p>
              <p>For concepts that feel difficult, deploy the Feynman Technique. Write the concept, explain it simply, and identify your stumble points. Those stumble points become your priority list for the next session. <Highlight description="Tracking stumble points creates a feedback loop: each study session generates specific, actionable targets for the next session. Over time, your stumble points list shrinks as gaps are filled, giving you concrete evidence of progress. This is far more effective than the common approach of re-studying everything equally." theme={theme}>Track your stumble points</Highlight> — they are the most valuable output of any study session, because they tell you exactly where your understanding breaks down. A stumble point identified today is a mark saved in the exam tomorrow.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one topic you're currently studying. Set a timer for 5 minutes and explain it out loud as if teaching a classmate who missed the lesson. No notes allowed. When you stumble — and you will — write down the exact point where you got stuck. That stumble point is your most valuable study target for tomorrow.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheTeachingEffectModule;
