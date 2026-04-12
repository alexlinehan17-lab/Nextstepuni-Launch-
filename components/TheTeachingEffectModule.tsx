/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Users, Brain, MessageSquare, Lightbulb, Flag } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { limeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, ConceptCardGrid } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

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
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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

  const isGood = analysis.jargonWords.length <= 2 && analysis.simplicityScore >= 60;
  const isMid = !isGood && analysis.jargonWords.length <= 5;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      {/* Section header */}
      <div className="text-center mb-8">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Feynman Technique</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>Explain It Back Challenge</h4>
        <p className="mt-1" style={{ fontSize: 15, color: '#7a7068' }}>Explain this definition in simple terms — as if to a 12-year-old.</p>
      </div>

      {/* Zone 1 — Definition card */}
      <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 14, padding: '20px 24px' }}>
        <div className="flex items-center justify-between mb-3">
          <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', backgroundColor: '#f0ece6', color: '#9e9186', border: '1px solid #d0cdc8', borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>The Definition</span>
          <span style={{ fontSize: 11, fontWeight: 600, backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', borderRadius: 20, padding: '3px 10px' }}>Biology</span>
        </div>
        <p className="font-serif" style={{ fontSize: 16, color: '#1a1a1a', lineHeight: 1.7 }}>{ORIGINAL_CONCEPT}</p>
      </div>

      {!submitted ? (
        <>
          {/* Connector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '16px 0' }}>
            <div style={{ flex: 1, height: 1, background: '#e0dbd4' }} />
            <div style={{ background: '#e8f5f2', border: '1.5px solid rgba(42,125,111,0.3)', borderRadius: 20, padding: '6px 14px', flexShrink: 0 }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: '#1a6358', letterSpacing: '0.05em' }}>NOW EXPLAIN IT</span>
            </div>
            <div style={{ flex: 1, height: 1, background: '#e0dbd4' }} />
          </div>

          {/* Zone 2 — Response */}
          <div style={{ backgroundColor: '#f0faf8', border: '2px solid #2A7D6F', borderRadius: 14, padding: '18px 20px' }}>
            <div className="flex items-center justify-between mb-3">
              <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', backgroundColor: '#d0ede8', color: '#1a6358', borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Your Explanation</span>
              <span style={{ fontSize: 11, color: '#9e9186' }}>Aim for 2–3 sentences</span>
            </div>
            <textarea
              value={userText}
              onChange={(e) => setUserText(e.target.value)}
              placeholder="Imagine you're explaining this to a younger sibling..."
              className="w-full outline-none font-serif"
              style={{ backgroundColor: '#FFFFFF', border: '1.5px solid #d0d8d4', borderRadius: 10, padding: '14px 16px', fontSize: 15, color: '#1a1a1a', lineHeight: 1.6, minHeight: 120, resize: 'none' as const }}
              onFocus={(e) => { e.currentTarget.style.borderColor = '#2A7D6F'; }}
              onBlur={(e) => { e.currentTarget.style.borderColor = '#d0d8d4'; }}
            />

            {/* Live stats */}
            {userText.trim().length > 0 && (
              <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="mt-3 grid grid-cols-3 gap-2">
                <div className="text-center p-2 bg-white rounded-lg" style={{ border: '1.5px solid #d0cdc8' }}>
                  <p className="font-serif font-bold" style={{ fontSize: 18, color: '#1a1a1a' }}>{analysis.wordCount}</p>
                  <p style={{ fontSize: 10, color: '#9e9186' }}>Words</p>
                </div>
                <div className="text-center p-2 bg-white rounded-lg" style={{ border: `1.5px solid ${analysis.jargonWords.length > 5 ? '#E85D75' : '#2A7D6F'}` }}>
                  <p className="font-serif font-bold" style={{ fontSize: 18, color: analysis.jargonWords.length > 5 ? '#E85D75' : '#2A7D6F' }}>{analysis.jargonWords.length}</p>
                  <p style={{ fontSize: 10, color: '#9e9186' }}>Borrowed</p>
                </div>
                <div className="text-center p-2 bg-white rounded-lg" style={{ border: `1.5px solid ${analysis.simplicityScore >= 60 ? '#2A7D6F' : '#9e9186'}` }}>
                  <p className="font-serif font-bold" style={{ fontSize: 18, color: analysis.simplicityScore >= 60 ? '#2A7D6F' : '#9e9186' }}>{analysis.simplicityScore}%</p>
                  <p style={{ fontSize: 10, color: '#9e9186' }}>Simplicity</p>
                </div>
              </MotionDiv>
            )}

            {analysis.jargonWords.length > 0 && (
              <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-3">
                <p style={{ fontSize: 11, fontWeight: 600, color: '#9e9186', marginBottom: 6 }}>Words borrowed from original:</p>
                <div className="flex flex-wrap gap-1.5">
                  {analysis.jargonWords.map((w, i) => (
                    <span key={i} style={{ fontSize: 11, fontWeight: 500, backgroundColor: '#f0ece6', color: '#7a7068', border: '1px solid #d0cdc8', borderRadius: 20, padding: '2px 8px' }}>{w}</span>
                  ))}
                </div>
              </MotionDiv>
            )}

            <div className="mt-4">
              <motion.button
                onClick={handleSubmit}
                disabled={userText.trim().length <= 10}
                whileTap={{ y: 3 }}
                className="text-white font-semibold"
                style={{ backgroundColor: userText.trim().length > 10 ? '#2A7D6F' : '#d0cdc8', borderRadius: 100, padding: '13px 32px', fontSize: 15, borderBottom: userText.trim().length > 10 ? '3px solid #1a5a4e' : 'none', boxShadow: userText.trim().length > 10 ? '0 4px 0 #1a5a4e' : 'none', cursor: userText.trim().length > 10 ? 'pointer' : 'not-allowed', opacity: userText.trim().length > 10 ? 1 : 0.5 }}
              >
                Submit Explanation
              </motion.button>
            </div>
          </div>
        </>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6">
          {/* Side by side comparison */}
          <div className="grid md:grid-cols-2 gap-3 mb-6">
            <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 14, padding: '16px 20px' }}>
              <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', color: '#9e9186', textTransform: 'uppercase' as const }}>Original</span>
              <p className="font-serif mt-2" style={{ fontSize: 14, color: '#5a5550', lineHeight: 1.6 }}>{ORIGINAL_CONCEPT}</p>
            </div>
            <div style={{ backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 14, padding: '16px 20px' }}>
              <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', color: '#1a6358', textTransform: 'uppercase' as const }}>Your Explanation</span>
              <p className="font-serif mt-2" style={{ fontSize: 14, color: '#1a1a1a', lineHeight: 1.6 }}>{userText}</p>
            </div>
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-3 gap-2 mb-6">
            <div className="text-center p-3 bg-white rounded-xl" style={{ border: '2px solid #1a1a1a' }}>
              <p className="font-serif font-bold" style={{ fontSize: 22, color: '#1a1a1a' }}>{analysis.wordCount}</p>
              <p style={{ fontSize: 10, color: '#9e9186' }}>Words</p>
            </div>
            <div className="text-center p-3 bg-white rounded-xl" style={{ border: `2px solid ${analysis.jargonWords.length > 5 ? '#E85D75' : analysis.jargonWords.length > 2 ? '#9e9186' : '#2A7D6F'}` }}>
              <p className="font-serif font-bold" style={{ fontSize: 22, color: analysis.jargonWords.length > 5 ? '#E85D75' : analysis.jargonWords.length > 2 ? '#9e9186' : '#2A7D6F' }}>{analysis.jargonWords.length}</p>
              <p style={{ fontSize: 10, color: '#9e9186' }}>Borrowed</p>
            </div>
            <div className="text-center p-3 bg-white rounded-xl" style={{ border: `2px solid ${analysis.simplicityScore >= 60 ? '#2A7D6F' : '#9e9186'}` }}>
              <p className="font-serif font-bold" style={{ fontSize: 22, color: analysis.simplicityScore >= 60 ? '#2A7D6F' : '#9e9186' }}>{analysis.simplicityScore}%</p>
              <p style={{ fontSize: 10, color: '#9e9186' }}>Simplicity</p>
            </div>
          </div>

          {/* Feedback */}
          <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            {isGood ? (
              <div style={{ backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 14, padding: '20px 22px' }}>
                <div className="flex items-center gap-3 mb-2">
                  <div style={{ width: 36, height: 36, borderRadius: '50%', backgroundColor: '#2A7D6F', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, fontSize: 18, color: 'white' }}>✓</div>
                  <p className="font-serif font-semibold" style={{ fontSize: 18, color: '#1a6358' }}>Explanation approved.</p>
                </div>
                <p style={{ fontSize: 14, color: '#2A7D6F' }}>Nice one! You properly rebuilt that in your own words. That's exactly the kind of explaining that makes things stick long-term.</p>
              </div>
            ) : (
              <div style={{ borderLeft: '3px solid #E85D75', backgroundColor: '#fde4e4', borderRadius: '0 14px 14px 0', padding: '16px 20px' }}>
                <p className="italic" style={{ fontSize: 14, color: '#5a5550' }}>
                  {isMid
                    ? "Good effort, but some of your phrasing is pretty close to the original. Try pushing further — can you explain it using a totally different comparison or example?"
                    : "This reads like you're echoing the original rather than rebuilding it. Try closing the original, and explain it as if to a younger sibling. Use everyday examples."}
                </p>
              </div>
            )}
          </MotionDiv>

          <div className="mt-6 text-center">
            <button onClick={handleReset} className="font-medium transition-colors" style={{ fontSize: 13, color: '#2A7D6F', background: 'none', border: 'none', cursor: 'pointer' }}>
              Try again
            </button>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const TheTeachingEffectModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
              {essentials ? (
                <>
                  <p><Highlight description="Two groups studied the same material. The 'teach it' group massively outperformed the 'test' group." theme={theme}>In one experiment</Highlight>, students told to prepare to teach outperformed students told to prepare for a test. The key: <Highlight description="Nobody actually taught. Just expecting to teach changed how they studied." theme={theme}>neither group actually taught anyone</Highlight>. Just believing you will teach changes how your brain processes material. This is <Highlight description="Your brain shifts from 'remember this' to 'explain this' — building connections automatically." theme={theme}>the teaching effect</Highlight>. Your brain shifts from storing facts to building connections.</p>
                </>
              ) : (
                <>
                  <p>Here is something that might surprise you. <Highlight description="Researchers gave two groups the exact same material to study. One group was told they'd be tested on it. The other was told they'd have to teach it to someone else afterwards. Same stuff, different mindset — and the 'teach it' group absolutely smashed it on every type of question." theme={theme}>In one experiment</Highlight>, two groups of students were given the exact same material to study. One group was told: "You will be tested on this." The other group was told: "You will teach this to another student afterwards."</p>
                  <p>The results were wild. The group who expected to teach remembered more, organised it better, and performed significantly better on every type of question — even the tricky ones that needed real understanding, not just recognition. But here is the mad part: <Highlight description="Nobody in the 'teach it' group actually taught anyone. Just thinking they'd have to teach was enough to change how their brains processed the material. So the magic isn't in the teaching itself — it's in how you prepare when you think you'll have to explain it." theme={theme}>neither group actually taught anyone</Highlight>. Just believing they would have to teach changed HOW they processed the material. Instead of passively absorbing facts, they started organising information, spotting the key ideas, and building explanations in their head — all without being told to do so.</p>
                  <p>This is <Highlight description="When you think you'll have to teach something, your brain shifts from 'how do I remember this?' to 'how do I explain this?' That one shift completely changes how you process information. You don't just store random facts — you build connections between them, because you know someone else would need to follow your thinking." theme={theme}>the teaching effect</Highlight>: teaching — even imagined teaching — restructures how you know things. When you expect to teach, your brain shifts from "How do I remember this?" to "How do I explain this?" That one shift changes everything. You stop just storing facts and start building connections between them, because you know someone else would need to follow your thinking.</p>
                </>
              )}
              <TeachVsTestComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Explaining Changes How You Think." eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <p><Highlight description="Explaining forces you to rebuild your understanding." theme={theme}>Explaining forces you to restructure what you know</Highlight>. There are two types. <Highlight description="Repeating the textbook word-for-word without transforming it." theme={theme}>Parroting</Highlight> is just echoing the textbook. <Highlight description="Explaining in your own words with your own examples." theme={theme}>Rebuilding</Highlight> is using your own comparisons and examples. Only rebuilding produces real learning. If your explanation sounds like the textbook, you are parroting. Use your own words and you will actually understand it.</p>
              ) : (
                <>
                  <p>So why does expecting to teach make such a big difference? It comes down to what happens when you try to explain something. <Highlight description="When you try to explain something, your brain is forced to take apart what you think you know and rebuild it in a way that actually makes sense. You can't explain something you don't truly get — so the explaining process shines a light on every gap and every bit you only half-understood." theme={theme}>Explaining forces you to restructure what you know</Highlight>. You can't explain something you don't truly understand, so the act of explaining — or even just preparing to explain — exposes every gap, every shallow connection, every concept you thought you understood but actually just recognised.</p>
                  <p>There are two types of explaining, and they are very different. The first is <Highlight description="This is when you basically parrot back the textbook definition without really changing anything. If your explanation uses the exact same words as the book, you're just repeating — not understanding. It feels like you know it, but you haven't actually processed it deeply." theme={theme}>parroting</Highlight> — simply repeating facts back in roughly the same form you received them. "Photosynthesis is the process by which plants convert light energy into chemical energy." That's parroting. You haven't transformed anything; you've just echoed the textbook. The second type is <Highlight description="This is when you come up with your own way to explain it — your own comparisons, your own examples, your own way of connecting the dots. This is where real learning happens, because you're actually rebuilding the idea in your own head rather than just copying someone else's version." theme={theme}>rebuilding</Highlight> — coming up with your own connections, comparisons, and examples. "It's like the plant is running a solar-powered factory — light is the electricity, CO2 and water are the raw materials, and glucose is the product that comes off the assembly line."</p>
                  <p>Only rebuilding produces real learning. The test is simple: if your explanation uses the exact same words as the textbook, you're just parroting. If you use your own comparisons, your own examples, your own structure — you're rebuilding. And it's rebuilding that gives you the deep, connected understanding that works on new problems and holds up under exam pressure.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="You Don't Need an Audience." eyebrow="Step 3" icon={MessageSquare} theme={theme}>
              {essentials ? (
                <>
                  <p>You do not need someone to teach. <Highlight description="Physics students who explained steps to themselves solved 82% of new problems vs 46% for those who just read." theme={theme}>In one study</Highlight>, students who explained each step to themselves solved 82% of new problems. Those who just read solved 46%. <Highlight description="Pausing to put what you learned into your own words." theme={theme}>Explaining to yourself</Highlight> works almost as well as teaching someone else.</p>
                  <ConceptCardGrid
                    cards={[
                      { number: 1, term: "More Connections", description: "You make more connections between new stuff and things you already know." },
                      { number: 2, term: "Catch Misunderstandings", description: "You catch your own misunderstandings in real-time — trying to explain something exposes gaps that just re-reading never would." },
                      { number: 3, term: "Helps Most If You're Struggling", description: "It narrows the gap between students who find things easy and students who find things hard. So if you feel behind or confused, this is especially for you." },
                    ]}
                  />
                </>
              ) : (
                <>
                  <p>You might be thinking: "Grand, but I don't have someone to teach." Here's the good news — you don't need another person. <Highlight description="In one study, physics students who paused after each worked example to explain to themselves why each step was taken solved 82% of new problems. Students who just read through the examples? Only 46%. No audience needed — just the act of stopping and explaining it to yourself made a massive difference." theme={theme}>In one study with physics students</Highlight>, those who paused after each worked example to explain to themselves why each step was taken solved 82% of new problems on a test. The students who just read through the examples? Only 46%.</p>
                  <p><Highlight description="Explaining things to yourself means pausing while you're studying to put what you just learned into your own words. It works almost as well as explaining to another person because the hard work is the same — you have to pull the information together and make sense of it. Who's listening doesn't really matter; it's the thinking that counts." theme={theme}>Explaining to yourself</Highlight> — pausing after each concept to put it in your own words — works almost as well as explaining to another person. Here's why it's so powerful.</p>
                  <ConceptCardGrid
                    cards={[
                      { number: 1, term: "More Connections", description: "You make more connections between new stuff and things you already know." },
                      { number: 2, term: "Catch Misunderstandings", description: "You catch your own misunderstandings in real-time — trying to explain something exposes gaps that just re-reading never would." },
                      { number: 3, term: "Helps Most If You're Struggling", description: "It narrows the gap between students who find things easy and students who find things hard. So if you feel behind or confused, this is especially for you." },
                    ]}
                  />
                  <p>This is a proper equaliser. If you're struggling with a topic, your instinct is probably to re-read it more slowly. But that's the wrong move. Stop reading and start explaining — even if it's just to yourself. Even if your explanation is messy and full of gaps, the process of trying to put it into words is doing the heavy lifting that re-reading never will.</p>
                </>
              )}
              <ExplainItBackChallenge />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Simplicity Technique." eyebrow="Step 4" icon={Lightbulb} theme={theme}>
              {essentials ? (
                <p><Highlight description="Creating explanations forces your brain to do work that reading skips." theme={theme}>Actively creating explanations</Highlight> beats passive reading every time. <Highlight description="Write the topic, explain it simply, notice where you get stuck, fill the gap." theme={theme}>Here is the technique</Highlight>. Write the topic on a blank page. Explain it as if to a younger sibling. When you stumble, go back and fill that gap. The places you stumble are exactly what you need to learn. If you can explain it to a 12-year-old, you truly get it.</p>
              ) : (
                <>
                  <p>Everything we've covered so far points to one simple idea: <Highlight description="When you actively create something — an explanation, a comparison, an example — rather than just passively reading, your learning goes through the roof. It's one of the most effective things you can do while studying. Even explaining to an imaginary audience works brilliantly." theme={theme}>actively creating explanations</Highlight> (even to an imaginary audience) is one of the most powerful things you can do while studying. It works because producing something forces your brain to do the hard work that passive reading skips over.</p>
                  <p>There's a brilliant four-step technique built around this idea. <Highlight description="This is a dead-simple four-step method. Write the topic at the top of a blank page, explain it as simply as you can (like you're talking to a younger sibling), notice where you get stuck, then go back to your notes and fill that specific gap. Each place you stumble is showing you exactly what you need to learn next." theme={theme}>Here's how it works</Highlight>. Step one: write the topic at the top of a blank page. Step two: explain it as if you were talking to a younger sibling — no jargon, no textbook phrases, just clear simple language with real examples. Step three: when you stumble — when you hit a point where your explanation breaks down or gets vague — go back to your notes and fill that specific gap. Step four: simplify even further and come up with comparisons that make it click.</p>
                  <p>The magic is in step three. The places where you stumble ARE the things you need to learn. Every moment where your explanation breaks down is a moment where your understanding has a hole in it. Without this technique, those holes stay invisible — your brain papers over them with a feeling of "yeah, I know this." This technique makes them visible, specific, and fixable. After each round, your explanation gets smoother and your understanding gets deeper. If you can explain a concept to a 12-year-old, you truly get it.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Putting It All Together." eyebrow="Step 5" icon={Flag} theme={theme}>
              {essentials ? (
                <>
                  <p><Highlight description="Self-explanation and self-testing are the most effective study techniques." theme={theme}>Explaining and testing yourself</Highlight> beat highlighting and re-reading every time. Before studying, tell yourself "I will teach this." Take <Highlight description="Notes in your own words with your own examples." theme={theme}>notes in your own words</Highlight>. After studying, explain it out loud. For tough concepts, use the simplicity technique. <Highlight description="Write down where your explanation breaks down." theme={theme}>Track your stumble points</Highlight>. They become your study to-do list.</p>
                </>
              ) : (
                <>
                  <p>Let's bring everything together into a system you can use every time you sit down to study. Here's what it comes down to: <Highlight description="When you look at what actually works for learning, explaining things to yourself and testing yourself come out on top — by a mile. Highlighting, re-reading, and summarising (which is what most of us spend our time doing) are some of the least effective things you can do. This system swaps out the stuff that doesn't work for the stuff that does." theme={theme}>explaining things to yourself and testing yourself</Highlight> are far and away the most effective study techniques. Highlighting, re-reading, and summarising — the things most students spend their time on — are some of the least effective. This system is about swapping the stuff that doesn't work for the stuff that does.</p>
                  <p>Here's the system. Before each study session, set the intention: "I'm going to teach this to someone." That one mental shift changes how you process everything, even before you open a book. While studying, take <Highlight description="These are notes where you put things in your own words, draw connections to other topics, and come up with your own examples — instead of just copying the textbook word for word. It's the same idea as 'rebuilding' rather than 'parroting'. The Note-Taking Paradox module goes deeper on this." theme={theme}>notes in your own words</Highlight> — rephrase concepts, draw connections, and come up with your own examples rather than copying the textbook. After studying, explain the material out loud. It doesn't matter who you explain it to — a friend, your mam, the dog, the wall. The audience genuinely doesn't matter; it's the act of putting it into words that does the work.</p>
                  <p>For concepts that feel tough, use the simplicity technique from the last section. Write the concept, explain it simply, and spot your stumble points. Those stumble points become your to-do list for the next session. <Highlight description="When you write down the places where you got stuck, each study session gives you a clear list of what to work on next time. Over time, your stumble points list gets shorter as you fill the gaps, and you can actually see yourself making progress. This is way better than just re-reading everything and hoping for the best." theme={theme}>Track your stumble points</Highlight> — they are the most valuable thing you get from any study session, because they tell you exactly where your understanding breaks down. A stumble point you spot today is a mark saved in the exam tomorrow.</p>
                </>
              )}
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
