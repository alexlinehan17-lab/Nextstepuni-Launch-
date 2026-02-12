/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Map, Repeat, Activity, Brain, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = purpleTheme;
const MotionDiv = motion.div as any;

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
    { label: 'Building', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Strengthening', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Accessible', x1: 0.66, x2: 1, color: '#10b981' },
  ];
  const diffPhases = [
    { label: 'Building', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Cues missing', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Inaccessible', x1: 0.66, x2: 1, color: '#ef4444' },
  ];

  const Chart = ({ encoding, retrieval, phases, areaColor, areaId, label }: {
    encoding: number[]; retrieval: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
    areaColor: string; areaId: string; label: string;
  }) => (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
      <defs>
        <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
          <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
        </linearGradient>
      </defs>
      {[0.25, 0.5, 0.75, 1.0].map((v) => (
        <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
      ))}
      <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />

      {/* Encoding area */}
      <motion.path d={buildArea(encoding)} fill={`url(#${areaId})`} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />
      {/* Encoding line (solid) */}
      <motion.path d={buildLine(encoding)} fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut' }} />
      {/* Retrieval line (dashed) */}
      <motion.path d={buildLine(retrieval)} fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }} />
      {/* Encoding dots */}
      {encoding.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (encoding.length - 1))} cy={toY(v)} r="3.5" fill={areaColor} initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }} />
      ))}

      <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
      <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
      {xLabels.map((m, i) => (
        <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
      ))}
      {phases.map((p, i) => (
        <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
      ))}
      <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
      <line x1={W - padR - 120} x2={W - padR - 104} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 100} y={17} fontSize="8" fill="#a1a1aa">Encoding Strength</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Retrieval</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Context-Dependent Memory</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">What happens to retrieval when the environment changes? Godden & Baddeley (1975).</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">You study perfectly in your bedroom. But what happens when you sit down in the exam hall?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-purple-500 text-white hover:bg-purple-600 transition-colors">
            See the Context Effect
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart encoding={encodingStrength} retrieval={sameRetrieval} phases={samePhases} areaColor="#10b981" areaId="same-ctx-grad" label="Same Context (Study & Test)" />
            </div>
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart encoding={encodingStrength} retrieval={diffRetrieval} phases={diffPhases} areaColor="#ef4444" areaId="diff-ctx-grad" label="Different Context (Study vs Test)" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Same-context recall</strong> works because environmental cues aid retrieval. But exams are in a DIFFERENT context. If your memories depend on your study environment, they become fragile.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">When the exam hall strips away your study cues</strong>, context-dependent memories become inaccessible. You need context-INDEPENDENT knowledge that works anywhere.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 2. NOISE LEVEL CURVE
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

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Noise-Performance Curve</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">The inverted-U relationship between noise level and cognitive performance. Mehta, Zhu & Cheema (2012).</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Is silence always best for studying? Or does a little noise actually help?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-purple-500 text-white hover:bg-purple-600 transition-colors">
            See the Noise Curve
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="rounded-lg border border-purple-200 dark:border-purple-900 bg-purple-50/50 dark:bg-purple-950/20 p-3">
            <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
              <defs>
                <linearGradient id="noise-grad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#a855f7" stopOpacity="0.4" />
                  <stop offset="100%" stopColor="#a855f7" stopOpacity="0.03" />
                </linearGradient>
                {/* Sweet spot highlight */}
                <linearGradient id="sweet-spot-grad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#a855f7" stopOpacity="0.15" />
                  <stop offset="100%" stopColor="#a855f7" stopOpacity="0.05" />
                </linearGradient>
              </defs>

              {/* Grid lines */}
              {[0.25, 0.5, 0.75, 1.0].map((v) => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
              ))}
              <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />

              {/* Sweet spot region highlight */}
              <rect x={toX(0.22)} y={padT} width={toX(0.62) - toX(0.22)} height={chartH} fill="url(#sweet-spot-grad)" rx="4" />

              {/* Region annotations */}
              <text x={toX(0.08)} y={toY(0.05)} fontSize="9" fill="#ef4444" textAnchor="middle" fontWeight="700" opacity="0.8">Too quiet</text>
              <text x={toX(0.42)} y={toY(1.05)} fontSize="9" fill="#a855f7" textAnchor="middle" fontWeight="700">Sweet spot</text>
              <text x={toX(0.88)} y={toY(0.05)} fontSize="9" fill="#ef4444" textAnchor="middle" fontWeight="700" opacity="0.8">Too loud</text>

              {/* Curve area */}
              <motion.path d={buildArea(curvePoints)} fill="url(#noise-grad)" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />

              {/* Curve line */}
              <motion.path d={buildCurve(curvePoints)} fill="none" stroke="#a855f7" strokeWidth="2.5" strokeLinecap="round" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, ease: 'easeOut' }} />

              {/* Focused/Analytical peak marker */}
              <motion.circle cx={toX(focusedPeakX)} cy={toY(focusedPeakY)} r="5" fill="#3b82f6" stroke="white" strokeWidth="2" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 1.0 }} />
              <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}>
                <text x={toX(focusedPeakX)} y={toY(focusedPeakY) - 14} fontSize="8" fill="#3b82f6" textAnchor="middle" fontWeight="700">Focused/</text>
                <text x={toX(focusedPeakX)} y={toY(focusedPeakY) - 5} fontSize="8" fill="#3b82f6" textAnchor="middle" fontWeight="700">Analytical</text>
              </motion.g>

              {/* Creative/Conceptual peak marker */}
              <motion.circle cx={toX(creativePeakX)} cy={toY(creativePeakY)} r="5" fill="#10b981" stroke="white" strokeWidth="2" initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 1.3 }} />
              <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 }}>
                <text x={toX(creativePeakX)} y={toY(creativePeakY) - 14} fontSize="8" fill="#10b981" textAnchor="middle" fontWeight="700">Creative/</text>
                <text x={toX(creativePeakX)} y={toY(creativePeakY) - 5} fontSize="8" fill="#10b981" textAnchor="middle" fontWeight="700">Conceptual</text>
              </motion.g>

              {/* X-axis labels */}
              {noiseLabels.map((label, i) => (
                <text key={label} x={toX(i / (noiseLabels.length - 1))} y={toY(0) + 16} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{label}</text>
              ))}

              {/* Axis labels */}
              <text x={W / 2} y={H - 4} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">Noise Level &rarr;</text>
              <text x={12} y={H / 2} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600" transform={`rotate(-90, 12, ${H / 2})`}>Cognitive Performance &rarr;</text>
              <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
              <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
            </svg>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mt-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900">
              <span className="text-blue-500 text-lg mt-0.5">&#x1F3AF;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-blue-600 dark:text-blue-400">Focused tasks</strong> (maths problems, memorisation) perform best in quieter environments. Silence lets you concentrate without processing interference.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x1F4A1;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Creative tasks</strong> (understanding concepts, making connections) benefit from moderate ambient noise. The slight processing difficulty pushes thinking into broader, more abstract modes.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheContextEffectModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'context-dependent-memory', title: 'Context-Dependent Memory', eyebrow: '01 // The Discovery', icon: Map },
    { id: 'variation-advantage', title: 'The Variation Advantage', eyebrow: '02 // The Counterintuitive Fix', icon: Repeat },
    { id: 'noise-question', title: 'The Noise Question', eyebrow: '03 // The Optimal Signal', icon: Activity },
    { id: 'encoding-variability', title: 'Encoding Variability', eyebrow: '04 // The Science', icon: Brain },
    { id: 'designing-environments', title: 'Designing Your Environments', eyebrow: '05 // The Protocol', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="49"
      moduleTitle="The Context Effect"
      moduleSubtitle="The Environmental Encoding Protocol"
      moduleDescription="Where you study changes what you remember. Learn why studying in multiple places beats one 'perfect' spot — and how to design environments that enhance your brain's encoding."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Context-Dependent Memory." eyebrow="Step 1" icon={Map} theme={theme}>
              <p><Highlight description="Duncan Godden and Alan Baddeley conducted this experiment at the University of Stirling in 1975. Divers learned lists of 40 words either on dry land or 20 feet underwater. They were then tested in either the same or a different environment. The results demonstrated one of the most striking examples of context-dependent memory ever recorded." theme={theme}>Godden & Baddeley (1975)</Highlight> conducted one of psychology's most famous experiments. Divers learned word lists either underwater or on land, then were tested in either the same or different environment. Those tested in the same environment they learned in recalled approximately 40% more. Your brain doesn't just encode the information — it encodes the entire context: the room, the lighting, the sounds, even the smell.</p>
              <p>These <Highlight description="Environmental details — sounds, smells, lighting, temperature, even your posture — that become associated with the information you're learning. Your brain uses these details as retrieval pathways, like bookmarks that help it find the right memory. The more cues available at retrieval that match those present at encoding, the easier the recall." theme={theme}>contextual cues</Highlight> become retrieval pathways. This is Context-Dependent Memory, and it explains why you can remember something perfectly in your bedroom but draw a blank in the exam hall. The exam hall is stripped of every environmental cue your brain associated with that knowledge.</p>
              <p>The implications for students are profound. If you only ever study in one place, your memories become <Highlight description="When a memory is strongly associated with a specific context, it can only be reliably retrieved in that context. The knowledge exists in your brain, but without the right environmental cues to trigger retrieval, it feels inaccessible. This is not a failure of storage — it's a failure of retrieval." theme={theme}>context-bound</Highlight> — deeply tied to that specific environment. They feel solid and accessible in your bedroom. But move to an unfamiliar exam hall with fluorescent lights and rows of desks, and those same memories can suddenly feel unreachable. The knowledge is still there; your brain just can't find the path to it without its usual signposts.</p>
              <ContextMemoryComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Variation Advantage." eyebrow="Step 2" icon={Repeat} theme={theme}>
              <p><Highlight description="Steven Smith, Arthur Glenberg, and Robert Bjork (University of Michigan) demonstrated that students who studied the same material in two different rooms recalled approximately 40% more words on a free-recall test than students who studied twice in the same room. This was one of the first experimental demonstrations that environmental variation could enhance memory." theme={theme}>Smith, Glenberg & Bjork (1978)</Highlight> found the solution: students who studied the same material in two different rooms recalled approximately 40% more than those who studied in the same room twice. This seems to contradict context-dependent memory, but it doesn't — it transcends it.</p>
              <p>When you study in multiple environments, your brain can't rely on any single context as a cue, so it creates <Highlight description="Memory traces that are not bound to any particular environment. Instead of relying on contextual cues for retrieval, context-independent memories are associated with the content itself — the meaning, the structure, the relationships between ideas. This makes the knowledge portable, accessible in any setting including unfamiliar exam halls." theme={theme}>context-INDEPENDENT memory traces</Highlight>. The knowledge becomes portable — accessible anywhere, including the unfamiliar exam hall. Instead of encoding "this fact + my bedroom lamp + the sound of rain," your brain encodes "this fact + multiple diverse associations," creating a web of retrieval routes that doesn't depend on any single environment.</p>
              <p><Highlight description="Robert Bjork and Andrew Richardson-Klavehn formalised this principle in their 1989 chapter on retrieval processes in memory. They argued that varying the conditions of encoding increases the number of retrieval cues associated with a memory, making it more accessible across a wider range of contexts. This became known as Encoding Variability Theory." theme={theme}>Bjork & Richardson-Klavehn (1989)</Highlight> explained this through Encoding Variability Theory: varied contexts create multiple retrieval routes to the same information. Each new environment adds a different set of associations — the hum of a cafe, the silence of a library, the kitchen radio in the background. When exam day arrives and none of those specific cues are present, it doesn't matter. Your brain has so many alternative pathways that at least some will activate, making the memory retrievable even in a completely novel setting.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Noise Question." eyebrow="Step 3" icon={Activity} theme={theme}>
              <p><Highlight description="Ravi Mehta (University of Illinois), Rui Zhu (University of British Columbia), and Amar Cheema (University of Virginia) published this finding in the Journal of Consumer Research (2012). They ran five experiments showing that moderate ambient noise (~70 dB) enhanced performance on creative tasks by inducing a higher level of construal — broader, more abstract processing — compared to both low noise (~50 dB) and high noise (~85 dB)." theme={theme}>Mehta, Zhu & Cheema (2012)</Highlight> published a surprising finding in the Journal of Consumer Research: moderate ambient noise (~70 decibels, roughly equivalent to a busy cafe) enhanced creative thinking compared to both silence and loud noise. The mechanism: moderate noise creates just enough processing difficulty — a form of <Highlight description="Robert Bjork's concept of desirable difficulties describes conditions that make learning feel harder during encoding but lead to stronger long-term retention. Moderate noise acts as a mild desirable difficulty by slightly disrupting focused processing, which paradoxically pushes the brain into broader, more abstract thinking patterns that benefit creative and conceptual tasks." theme={theme}>desirable difficulty</Highlight> — to push thinking from focused, analytical mode into broader, more abstract processing.</p>
              <p>However, <Highlight description="James Szalma and Peter Hancock (University of Central Florida) conducted a comprehensive meta-analysis published in Psychological Bulletin (2011) covering decades of research on noise effects on performance. They found that noise consistently impaired performance on tasks requiring sustained attention, vigilance, and focused concentration, while the effects on simpler or more creative tasks were mixed or sometimes positive." theme={theme}>Szalma & Hancock's (2011) meta-analysis</Highlight> showed that for tasks requiring focused concentration — like mathematical problem-solving or detailed memorisation — quiet environments are superior. Noise interferes with the precise, sequential processing these tasks demand. The practical rule emerges clearly: use moderate noise for understanding and connecting ideas, use silence for memorisation and practice problems.</p>
              <p>This means your study environment should match your task. Reading a history chapter to understand the narrative arc? A cafe might actually enhance your processing. Drilling past paper questions in maths or memorising vocabulary? You need silence. The environment isn't just a backdrop — it's an active ingredient in your cognitive processing. Designing your study sessions around this principle means deliberately choosing where you work based on what you're working on.</p>
              <NoiseLevelCurve />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Encoding Variability." eyebrow="Step 4" icon={Brain} theme={theme}>
              <p><Highlight description="In their 1989 chapter 'Retrieval Processes in Human Memory,' Bjork and Richardson-Klavehn formalised the theoretical framework: each study episode creates a unique memory trace that includes both the target information and the contextual features present during encoding. When the same material is studied in different contexts, multiple distinct traces are created, each with different contextual associations." theme={theme}>Bjork & Richardson-Klavehn (1989)</Highlight> formalised Encoding Variability Theory: every time you study the same material in a different context, you create a new set of associations. Each context adds different retrieval cues. The more diverse the cues, the more routes your brain has to access the memory. Think of it like building roads to a city — one road is vulnerable to a single blocked bridge, but five roads from different directions means you can always find a way through.</p>
              <p>This is why studying the same flashcards on the bus, in your bedroom, and in the library creates stronger memories than studying them three times in the same spot. Each location wraps the information in a different contextual package. The bus adds the rumble of the engine and the movement. Your bedroom adds the familiar sounds of home. The library adds the particular quality of silence and the presence of other students. Each version of the memory is slightly different, and those differences create <Highlight description="The concept that memories are not stored as single, isolated traces but as overlapping networks of associations. Each study episode in a different context creates a new node in this network, with connections to both the target information and the unique contextual features. More nodes and connections mean more potential retrieval pathways, creating redundancy that protects against forgetting." theme={theme}>redundant retrieval pathways</Highlight>.</p>
              <p><Highlight description="Steven Smith and Edward Vela (Texas A&M University) conducted a meta-analysis published in Memory & Cognition (2001) examining all available studies on environmental context-dependent memory. They confirmed that environmental variation during encoding reliably improves free recall. The effect size was modest (d ≈ 0.25) but consistent, and importantly, it stacked additively with other evidence-based techniques like spacing and interleaving." theme={theme}>Smith & Vela's (2001) meta-analysis</Highlight> confirmed: environmental variation during encoding improves free recall. The effect is modest but reliable, and it stacks with other techniques like spacing and interleaving. This is key — context variation isn't a replacement for other effective study strategies; it's a multiplier. When you combine varied environments with spaced retrieval practice and interleaved topics, the compound effect on long-term retention is substantially greater than any single technique alone.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Designing Your Environments." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The research converges on a clear protocol. First: <Highlight description="The locations don't need to be exotic or specially designed. Research shows that even modest differences in environment — a different room in your house, a different seat in the library, a cafe versus your kitchen — are sufficient to create distinct contextual encoding. The key is genuine perceptual difference, not the quality of the space." theme={theme}>identify 2-3 study locations</Highlight> you can rotate between. They don't need to be fancy, just genuinely different — bedroom, kitchen table, library, cafe. The perceptual differences between these spaces are what create the distinct contextual traces your brain needs.</p>
              <p>Second: study the same subject in at least two different locations across the week. This is the critical application of Encoding Variability Theory. Don't reserve the library for one subject and your bedroom for another — that just creates new context dependencies. Instead, study Biology in your bedroom on Monday and in the library on Wednesday. The same content, different contexts, multiple retrieval pathways. Third: <Highlight description="Mehta et al. (2012) demonstrated that the optimal noise level depends on the cognitive demands of the task. Creative and conceptual tasks benefit from moderate ambient noise (~70 dB), while focused analytical tasks perform best in quiet conditions (~50 dB). Planning your environment around your task type optimises both encoding and processing." theme={theme}>match noise level to task</Highlight> — quiet for practice problems and memorisation, moderate ambient for reading and understanding.</p>
              <p>Fourth — and this is perhaps the most powerful technique: <Highlight description="Grant et al. (1998, Memory & Cognition) demonstrated that students who practised retrieval under conditions that matched the test environment showed significantly better transfer to the actual exam. By periodically studying in silence at a desk with a timer, you train your brain to retrieve under the exact conditions that matter most — recreating the sensory experience of the exam hall." theme={theme}>simulate exam conditions</Highlight> periodically. Study in silence at a desk with a timer, recreating the exam hall environment. This trains your brain to retrieve under the conditions that matter most. Grant et al. (1998) showed that students who practised retrieval in a novel environment showed better transfer to the actual exam setting. By deliberately practising in exam-like conditions, you're building retrieval pathways that will activate precisely when you need them.</p>
              <MicroCommitment theme={theme}>
                <p>This week, take one subject you'd normally study in the same spot and split it across two different locations. Study the same material in your bedroom on Tuesday and in the school library or kitchen on Thursday. Notice how retrieving the same content in a different setting feels harder — that extra effort is building context-independent memory that will be accessible anywhere, including the exam hall.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheContextEffectModule;
