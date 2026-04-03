/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Users, Brain, MessageSquare, Lightbulb, Flag } from 'lucide-react';
import { ModuleProgress } from '../types';
import { limeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = limeTheme;

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
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Test preppers</strong> take in facts quickly but store them as loose, disconnected pieces. Without any structure holding them together, those facts fade fast and fall apart under pressure.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Teaching preppers</strong> build a mental framework from the start. Even though they take in less at first, the organised structure means the knowledge sticks around and is easy to pull up when they need it.</p>
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
              ? 'Nice one! You properly rebuilt that in your own words. That\'s exactly the kind of explaining that makes things stick in your head long-term.'
              : analysis.jargonWords.length <= 5
              ? 'Good effort, but some of your phrasing is pretty close to the original. Try pushing further — can you explain it using a totally different comparison or example? That\'s the jump from repeating to really understanding.'
              : 'This reads like you\'re echoing the original rather than rebuilding it in your own words. Try closing the original, and explain it as if to a younger sibling. Use everyday examples and comparisons.'}
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
    { id: 'protege-effect', title: 'Why Teaching Beats Testing', eyebrow: '01 // The Discovery', icon: Users },
    { id: 'explaining-forces-restructuring', title: 'Explaining Changes How You Think', eyebrow: '02 // How It Works', icon: Brain },
    { id: 'self-explanation-advantage', title: 'You Don\'t Need an Audience', eyebrow: '03 // Going Solo', icon: MessageSquare },
    { id: 'feynman-multiplier', title: 'The Simplicity Technique', eyebrow: '04 // The Technique', icon: Lightbulb },
    { id: 'teaching-protocol', title: 'Putting It All Together', eyebrow: '05 // Your System', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="46"
      moduleTitle="The Teaching Effect"
      moduleSubtitle="Learn It by Teaching It"
      moduleDescription="Want to actually remember what you study? Pretend you have to explain it to someone else. Seriously — it changes how your brain stores everything, even if you never teach a single person."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Teach It Forward"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why Teaching Beats Testing." eyebrow="Step 1" icon={Users} theme={theme}>
              <p>Here is something that might surprise you. <Highlight description="Researchers gave two groups the exact same material to study. One group was told they'd be tested on it. The other was told they'd have to teach it to someone else afterwards. Same stuff, different mindset — and the 'teach it' group absolutely smashed it on every type of question." theme={theme}>In one experiment</Highlight>, two groups of students were given the exact same material to study. One group was told: "You will be tested on this." The other group was told: "You will teach this to another student afterwards."</p>
              <p>The results were wild. The group who expected to teach remembered more, organised it better, and performed significantly better on every type of question — even the tricky ones that needed real understanding, not just recognition. But here is the mad part: <Highlight description="Nobody in the 'teach it' group actually taught anyone. Just thinking they'd have to teach was enough to change how their brains processed the material. So the magic isn't in the teaching itself — it's in how you prepare when you think you'll have to explain it." theme={theme}>neither group actually taught anyone</Highlight>. Just believing they would have to teach changed HOW they processed the material. Instead of passively absorbing facts, they started organising information, spotting the key ideas, and building explanations in their head — all without being told to do so.</p>
              <p>This is <Highlight description="When you think you'll have to teach something, your brain shifts from 'how do I remember this?' to 'how do I explain this?' That one shift completely changes how you process information. You don't just store random facts — you build connections between them, because you know someone else would need to follow your thinking." theme={theme}>the teaching effect</Highlight>: teaching — even imagined teaching — restructures how you know things. When you expect to teach, your brain shifts from "How do I remember this?" to "How do I explain this?" That one shift changes everything. You stop just storing facts and start building connections between them, because you know someone else would need to follow your thinking.</p>
              <TeachVsTestComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Explaining Changes How You Think." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p>So why does expecting to teach make such a big difference? It comes down to what happens when you try to explain something. <Highlight description="When you try to explain something, your brain is forced to take apart what you think you know and rebuild it in a way that actually makes sense. You can't explain something you don't truly get — so the explaining process shines a light on every gap and every bit you only half-understood." theme={theme}>Explaining forces you to restructure what you know</Highlight>. You can't explain something you don't truly understand, so the act of explaining — or even just preparing to explain — exposes every gap, every shallow connection, every concept you thought you understood but actually just recognised.</p>
              <p>There are two types of explaining, and they are very different. The first is <Highlight description="This is when you basically parrot back the textbook definition without really changing anything. If your explanation uses the exact same words as the book, you're just repeating — not understanding. It feels like you know it, but you haven't actually processed it deeply." theme={theme}>parroting</Highlight> — simply repeating facts back in roughly the same form you received them. "Photosynthesis is the process by which plants convert light energy into chemical energy." That's parroting. You haven't transformed anything; you've just echoed the textbook. The second type is <Highlight description="This is when you come up with your own way to explain it — your own comparisons, your own examples, your own way of connecting the dots. This is where real learning happens, because you're actually rebuilding the idea in your own head rather than just copying someone else's version." theme={theme}>rebuilding</Highlight> — coming up with your own connections, comparisons, and examples. "It's like the plant is running a solar-powered factory — light is the electricity, CO2 and water are the raw materials, and glucose is the product that comes off the assembly line."</p>
              <p>Only rebuilding produces real learning. The test is simple: if your explanation uses the exact same words as the textbook, you're just parroting. If you use your own comparisons, your own examples, your own structure — you're rebuilding. And it's rebuilding that gives you the deep, connected understanding that works on new problems and holds up under exam pressure.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="You Don't Need an Audience." eyebrow="Step 3" icon={MessageSquare} theme={theme}>
              <p>You might be thinking: "Grand, but I don't have someone to teach." Here's the good news — you don't need another person. <Highlight description="In one study, physics students who paused after each worked example to explain to themselves why each step was taken solved 82% of new problems. Students who just read through the examples? Only 46%. No audience needed — just the act of stopping and explaining it to yourself made a massive difference." theme={theme}>In one study with physics students</Highlight>, those who paused after each worked example to explain to themselves why each step was taken solved 82% of new problems on a test. The students who just read through the examples? Only 46%.</p>
              <p><Highlight description="Explaining things to yourself means pausing while you're studying to put what you just learned into your own words. It works almost as well as explaining to another person because the hard work is the same — you have to pull the information together and make sense of it. Who's listening doesn't really matter; it's the thinking that counts." theme={theme}>Explaining to yourself</Highlight> — pausing after each concept to put it in your own words — works almost as well as explaining to another person. Here's why it's so powerful. First, you make more connections between new stuff and things you already know. Second, you catch your own misunderstandings in real-time — trying to explain something exposes gaps that just re-reading never would. Third, and this is the best bit, <Highlight description="This technique helps the most if you're someone who's struggling with the material. It narrows the gap between students who find things easy and students who find things hard. So if you feel behind or confused, this is especially for you." theme={theme}>it helps the most if you're struggling</Highlight>. It narrows the gap between students who find things easy and students who find things hard.</p>
              <p>This is a proper equaliser. If you're struggling with a topic, your instinct is probably to re-read it more slowly. But that's the wrong move. Stop reading and start explaining — even if it's just to yourself. Even if your explanation is messy and full of gaps, the process of trying to put it into words is doing the heavy lifting that re-reading never will.</p>
              <ExplainItBackChallenge />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Simplicity Technique." eyebrow="Step 4" icon={Lightbulb} theme={theme}>
              <p>Everything we've covered so far points to one simple idea: <Highlight description="When you actively create something — an explanation, a comparison, an example — rather than just passively reading, your learning goes through the roof. It's one of the most effective things you can do while studying. Even explaining to an imaginary audience works brilliantly." theme={theme}>actively creating explanations</Highlight> (even to an imaginary audience) is one of the most powerful things you can do while studying. It works because producing something forces your brain to do the hard work that passive reading skips over.</p>
              <p>There's a brilliant four-step technique built around this idea. <Highlight description="This is a dead-simple four-step method. Write the topic at the top of a blank page, explain it as simply as you can (like you're talking to a younger sibling), notice where you get stuck, then go back to your notes and fill that specific gap. Each place you stumble is showing you exactly what you need to learn next." theme={theme}>Here's how it works</Highlight>. Step one: write the topic at the top of a blank page. Step two: explain it as if you were talking to a younger sibling — no jargon, no textbook phrases, just clear simple language with real examples. Step three: when you stumble — when you hit a point where your explanation breaks down or gets vague — go back to your notes and fill that specific gap. Step four: simplify even further and come up with comparisons that make it click.</p>
              <p>The magic is in step three. The places where you stumble ARE the things you need to learn. Every moment where your explanation breaks down is a moment where your understanding has a hole in it. Without this technique, those holes stay invisible — your brain papers over them with a feeling of "yeah, I know this." This technique makes them visible, specific, and fixable. After each round, your explanation gets smoother and your understanding gets deeper. If you can explain a concept to a 12-year-old, you truly get it.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Putting It All Together." eyebrow="Step 5" icon={Flag} theme={theme}>
              <p>Let's bring everything together into a system you can use every time you sit down to study. Here's what it comes down to: <Highlight description="When you look at what actually works for learning, explaining things to yourself and testing yourself come out on top — by a mile. Highlighting, re-reading, and summarising (which is what most of us spend our time doing) are some of the least effective things you can do. This system swaps out the stuff that doesn't work for the stuff that does." theme={theme}>explaining things to yourself and testing yourself</Highlight> are far and away the most effective study techniques. Highlighting, re-reading, and summarising — the things most students spend their time on — are some of the least effective. This system is about swapping the stuff that doesn't work for the stuff that does.</p>
              <p>Here's the system. Before each study session, set the intention: "I'm going to teach this to someone." That one mental shift changes how you process everything, even before you open a book. While studying, take <Highlight description="These are notes where you put things in your own words, draw connections to other topics, and come up with your own examples — instead of just copying the textbook word for word. It's the same idea as 'rebuilding' rather than 'parroting'. The Note-Taking Paradox module goes deeper on this." theme={theme}>notes in your own words</Highlight> — rephrase concepts, draw connections, and come up with your own examples rather than copying the textbook. After studying, explain the material out loud. It doesn't matter who you explain it to — a friend, your mam, the dog, the wall. The audience genuinely doesn't matter; it's the act of putting it into words that does the work.</p>
              <p>For concepts that feel tough, use the simplicity technique from the last section. Write the concept, explain it simply, and spot your stumble points. Those stumble points become your to-do list for the next session. <Highlight description="When you write down the places where you got stuck, each study session gives you a clear list of what to work on next time. Over time, your stumble points list gets shorter as you fill the gaps, and you can actually see yourself making progress. This is way better than just re-reading everything and hoping for the best." theme={theme}>Track your stumble points</Highlight> — they are the most valuable thing you get from any study session, because they tell you exactly where your understanding breaks down. A stumble point you spot today is a mark saved in the exam tomorrow.</p>
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
