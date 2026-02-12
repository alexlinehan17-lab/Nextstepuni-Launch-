/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, SquarePen, Layers, GitBranch, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { indigoTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = indigoTheme;
const MotionDiv = motion.div as any;

// --- INTERACTIVE COMPONENTS ---

// 1. NOTE-TAKING COMPARISON (Planning Paradox style dual-chart)
const NoteTakingComparison = () => {
  const [revealed, setRevealed] = useState(false);

  const W = 440, H = 260;
  const padL = 8, padR = 8, padT = 28, padB = 44;
  const chartW = W - padL - padR, chartH = H - padT - padB;
  const toX = (f: number) => padL + f * chartW;
  const toY = (f: number) => padT + (1 - f) * chartH;

  const xLabels = ['Lecture', 'Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30'];

  // Verbatim Notes: volume high, understanding crashes
  const verbatimVolume = [0.90, 0.88, 0.85, 0.82, 0.78, 0.75];
  const verbatimUnderstanding = [0.55, 0.42, 0.30, 0.22, 0.15, 0.10];

  // Generative Notes: volume low, understanding holds and grows
  const generativeVolume = [0.35, 0.38, 0.40, 0.42, 0.45, 0.48];
  const generativeUnderstanding = [0.45, 0.50, 0.55, 0.60, 0.62, 0.65];

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

  const verbatimPhases = [
    { label: 'Feels productive', x1: 0, x2: 0.33, color: '#fca5a5' },
    { label: 'Confident', x1: 0.33, x2: 0.66, color: '#f87171' },
    { label: 'Exam shock', x1: 0.66, x2: 1, color: '#ef4444' },
  ];
  const generativePhases = [
    { label: 'Feels slow', x1: 0, x2: 0.33, color: '#6ee7b7' },
    { label: 'Processing', x1: 0.33, x2: 0.66, color: '#34d399' },
    { label: 'Deeply encoded', x1: 0.66, x2: 1, color: '#10b981' },
  ];

  const Chart = ({ volume, understanding, phases, areaColor, areaId, label }: {
    volume: number[]; understanding: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
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
      {/* Volume area */}
      <motion.path
        d={buildArea(volume)}
        fill={`url(#${areaId})`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      {/* Volume line (solid) */}
      <motion.path
        d={buildLine(volume)}
        fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      />
      {/* Understanding line (dashed) */}
      <motion.path
        d={buildLine(understanding)}
        fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
      />
      {/* Volume dots */}
      {volume.map((v, i) => (
        <motion.circle key={i} cx={toX(i / (volume.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
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
      <line x1={W - padR - 110} x2={W - padR - 94} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
      <text x={W - padR - 90} y={17} fontSize="8" fill="#a1a1aa">Note Volume</text>
      <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 2" />
      <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Understanding</text>
    </svg>
  );

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Note-Taking Paradox</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Two students. Same lecture. Opposite strategies.</p>

      {!revealed ? (
        <div className="text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Most students try to capture every word. What does that actually do to understanding over time?</p>
          <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-indigo-500 text-white hover:bg-indigo-600 transition-colors">
            Reveal the Paradox
          </button>
        </div>
      ) : (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <div className="grid md:grid-cols-2 gap-4 mb-5">
            <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
              <Chart volume={verbatimVolume} understanding={verbatimUnderstanding} phases={verbatimPhases}
                areaColor="#ef4444" areaId="verb-grad" label="Verbatim Notes" />
            </div>
            <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
              <Chart volume={generativeVolume} understanding={generativeUnderstanding} phases={generativePhases}
                areaColor="#10b981" areaId="gen-grad" label="Generative Notes" />
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
              <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Verbatim</strong> feels productive but bypasses understanding. Your hand is busy, but your brain is on autopilot.</p>
            </div>
            <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
              <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
              <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Generative</strong> feels slower but forces the processing that creates lasting knowledge. Less ink, more thinking.</p>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

// 2. CORNELL NOTE SIMULATOR
const CornellNoteSimulator = () => {
  const [mainNotes, setMainNotes] = useState('');
  const [cueQuestions, setCueQuestions] = useState('');
  const [summary, setSummary] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);

  const originalConcept = 'Osmosis is the movement of water molecules from a region of high water concentration to a region of low water concentration through a semi-permeable membrane. This is a passive process — it requires no energy. The membrane allows water to pass but blocks larger solute molecules.';

  const getFeedback = () => {
    const issues: { type: 'warning' | 'success'; message: string }[] = [];

    // Main notes checks
    if (mainNotes.trim().length === 0) {
      issues.push({ type: 'warning', message: 'Main notes are empty. Try paraphrasing the concept in your own words.' });
    } else if (mainNotes.trim().length < 20) {
      issues.push({ type: 'warning', message: 'Main notes are very brief. Try to capture the key idea in a full sentence.' });
    } else {
      issues.push({ type: 'success', message: 'Main notes completed. Good work paraphrasing!' });
    }

    // Cue questions checks
    const cueLines = cueQuestions.trim().split('\n').filter((l) => l.trim().length > 0);
    if (cueLines.length === 0) {
      issues.push({ type: 'warning', message: 'No cue questions added. Try writing 2-3 questions you could use to test yourself.' });
    } else if (cueLines.length < 2) {
      issues.push({ type: 'warning', message: 'Only one cue question. Aim for at least 2-3 for effective self-testing.' });
    } else {
      const hasYesNo = cueLines.some((q) => {
        const lower = q.toLowerCase().trim();
        return lower.startsWith('is ') || lower.startsWith('does ') || lower.startsWith('can ') || lower.startsWith('are ') || lower.startsWith('was ') || lower.startsWith('do ');
      });
      if (hasYesNo) {
        issues.push({ type: 'warning', message: 'Some cue questions look like yes/no questions. Open-ended questions (What, How, Why, Explain) force deeper retrieval.' });
      } else {
        issues.push({ type: 'success', message: `${cueLines.length} cue questions — great for self-testing!` });
      }
    }

    // Summary checks
    const summaryWords = summary.trim().split(/\s+/).filter((w) => w.length > 0).length;
    if (summaryWords === 0) {
      issues.push({ type: 'warning', message: 'Summary is empty. Write the core idea in one concise sentence.' });
    } else if (summaryWords > 25) {
      issues.push({ type: 'warning', message: `Summary is ${summaryWords} words. Aim for under 25 words — the constraint forces deeper compression.` });
    } else {
      issues.push({ type: 'success', message: `Summary is ${summaryWords} words — concise and focused!` });
    }

    return issues;
  };

  const handleCheck = () => {
    setShowFeedback(true);
  };

  const handleReset = () => {
    setMainNotes('');
    setCueQuestions('');
    setSummary('');
    setShowFeedback(false);
  };

  const feedback = showFeedback ? getFeedback() : [];
  const allSuccess = feedback.length > 0 && feedback.every((f) => f.type === 'success');

  return (
    <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Cornell Note Simulator</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-6">Practice the Cornell Method on a real concept. Paraphrase, question, summarise.</p>

      {/* Original concept */}
      <div className="p-4 bg-indigo-50 dark:bg-indigo-950/20 rounded-xl border border-indigo-200 dark:border-indigo-800 mb-6">
        <p className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-1">Original Concept</p>
        <p className="text-sm text-zinc-700 dark:text-zinc-200">{originalConcept}</p>
      </div>

      {/* Cornell template */}
      <div className="border border-zinc-300 dark:border-zinc-600 rounded-xl overflow-hidden mb-6">
        {/* Top section: Cue column + Main notes */}
        <div className="flex min-h-[200px]">
          {/* Cue column (left) */}
          <div className="w-1/3 border-r border-zinc-300 dark:border-zinc-600 p-3 bg-zinc-50 dark:bg-zinc-900/50">
            <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Cue Questions</p>
            <textarea
              value={cueQuestions}
              onChange={(e) => { setCueQuestions(e.target.value); setShowFeedback(false); }}
              placeholder={"What is osmosis?\nWhy is no energy needed?\nWhat does the membrane block?"}
              className="w-full h-36 bg-transparent text-sm text-zinc-700 dark:text-zinc-200 placeholder:text-zinc-400 dark:placeholder:text-zinc-500 resize-none focus:outline-none"
            />
          </div>
          {/* Main notes (right) */}
          <div className="w-2/3 p-3">
            <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Main Notes (Your Words)</p>
            <textarea
              value={mainNotes}
              onChange={(e) => { setMainNotes(e.target.value); setShowFeedback(false); }}
              placeholder="Paraphrase the concept here in your own words. Do NOT copy the original..."
              className="w-full h-36 bg-transparent text-sm text-zinc-700 dark:text-zinc-200 placeholder:text-zinc-400 dark:placeholder:text-zinc-500 resize-none focus:outline-none"
            />
          </div>
        </div>
        {/* Summary (bottom) */}
        <div className="border-t border-zinc-300 dark:border-zinc-600 p-3 bg-zinc-50 dark:bg-zinc-900/50">
          <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-2">Summary (One Sentence)</p>
          <textarea
            value={summary}
            onChange={(e) => { setSummary(e.target.value); setShowFeedback(false); }}
            placeholder="Summarise the entire concept in one concise sentence..."
            className="w-full h-12 bg-transparent text-sm text-zinc-700 dark:text-zinc-200 placeholder:text-zinc-400 dark:placeholder:text-zinc-500 resize-none focus:outline-none"
          />
        </div>
      </div>

      {/* Buttons */}
      <div className="flex justify-center gap-3 mb-4">
        <button onClick={handleCheck} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-indigo-500 text-white hover:bg-indigo-600 transition-colors">
          Check My Notes
        </button>
        <button onClick={handleReset} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-zinc-200 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-zinc-300 dark:hover:bg-zinc-600 transition-colors">
          Reset
        </button>
      </div>

      {/* Feedback */}
      {showFeedback && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
          {feedback.map((f, i) => (
            <div key={i} className={`flex items-start gap-2.5 p-3 rounded-lg text-sm ${f.type === 'success' ? 'bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800' : 'bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800'}`}>
              <span className={`text-lg mt-0.5 ${f.type === 'success' ? 'text-emerald-500' : 'text-amber-500'}`}>{f.type === 'success' ? '\u2714' : '\u26A0'}</span>
              <p className="text-zinc-600 dark:text-zinc-300">{f.message}</p>
            </div>
          ))}
          {allSuccess && (
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 text-sm font-medium text-emerald-700 dark:text-emerald-300 text-center">
              Excellent work! You've completed a full Cornell note cycle. Now the real power comes from covering the right column and testing yourself using only the cue questions.
            </MotionDiv>
          )}
        </MotionDiv>
      )}
    </div>
  );
};


// --- MODULE COMPONENT ---
const TheNoteTakingParadoxModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'transcription-trap', title: 'The Transcription Trap', eyebrow: '01 // The Paradox', icon: FileText },
    { id: 'generative-note-taking', title: 'Generative Note-Taking', eyebrow: '02 // The Processing Advantage', icon: SquarePen },
    { id: 'cornell-system', title: 'The Cornell System', eyebrow: '03 // The Architecture', icon: Layers },
    { id: 'mapping-vs-listing', title: 'Mapping vs Listing', eyebrow: '04 // Visual Structure', icon: GitBranch },
    { id: 'building-your-system', title: 'Building Your System', eyebrow: '05 // The Protocol', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="45"
      moduleTitle="The Note-Taking Paradox"
      moduleSubtitle="The Generative Processing Protocol"
      moduleDescription="Discover why students who write more notes learn less — and master the science of note-taking that actually builds durable knowledge."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Transcription Trap." eyebrow="Step 1" icon={FileText} theme={theme}>
              <p>Here is a paradox that undermines the study habits of nearly every student: the more notes you take, the less you learn. In 2014, <Highlight description="Pam Mueller (Princeton) and Daniel Oppenheimer (UCLA) published 'The Pen Is Mightier Than the Keyboard' in Psychological Science. Across three studies, laptop note-takers wrote significantly more words but performed substantially worse on conceptual questions compared to longhand writers." theme={theme}>Mueller and Oppenheimer</Highlight> published one of the most important studies in educational psychology. They compared students who took notes on laptops versus those who wrote by hand. The laptop group wrote significantly more — capturing nearly verbatim transcriptions of the lecture. The longhand group wrote far less. And yet, on conceptual questions that required understanding and application, the longhand writers dramatically outperformed the laptop users.</p>
              <p>Why? Because longhand writers physically cannot write fast enough to transcribe everything. They are forced to <Highlight description="The cognitive process of compressing, selecting, and rephrasing incoming information. This compression requires understanding the material deeply enough to decide what matters and how to express it concisely — which is itself the act of learning." theme={theme}>compress and paraphrase</Highlight>. They have to listen, understand, select what matters, and rephrase it in their own words — all in real time. That compression IS the learning. The brain must process information to condense it, and that processing creates durable <Highlight description="Encoding traces are the neural pathways created when information is actively processed and stored in long-term memory. Deeper processing (paraphrasing, connecting, explaining) creates stronger, more retrievable traces than shallow processing (copying, highlighting, re-reading)." theme={theme}>memory traces</Highlight>. Verbatim transcription, by contrast, is a shortcut that bypasses understanding entirely. Your hand is busy, but your brain is on autopilot.</p>
              <p>This is the <Highlight description="The counterintuitive finding that strategies which feel the most productive during study (more notes, faster writing, complete capture) often produce the worst learning outcomes, while strategies that feel slower and more effortful produce the best outcomes." theme={theme}>Note-Taking Paradox</Highlight>: the strategy that feels most productive — capturing everything — is actually the one that produces the least learning. And the strategy that feels slow and incomplete — selective paraphrasing — is the one that builds genuine understanding. The rest of this module will teach you how to exploit this paradox.</p>
              <NoteTakingComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Generative Note-Taking." eyebrow="Step 2" icon={SquarePen} theme={theme}>
              <p>The Mueller and Oppenheimer finding wasn't new — it confirmed a principle discovered decades earlier. In 1978, <Highlight description="Richard Peper and Richard Mayer demonstrated that students who paraphrased and summarised during note-taking outperformed verbatim transcribers by 30-40% on transfer tests — questions requiring application of knowledge to new situations, not just recall of the original material." theme={theme}>Peper and Mayer</Highlight> demonstrated that generative note-taking — paraphrasing, summarising, connecting — outperformed verbatim transcription by 30-40% on transfer tests. These weren't simple recall questions; they required students to apply knowledge to new situations. The students who had processed the material deeply during note-taking could transfer it. The transcribers couldn't.</p>
              <p><Highlight description="Merlin Wittrock's (1989) Generative Learning Theory proposes that meaningful learning occurs only when the learner actively generates relationships between new information and their existing knowledge. Passive reception of information — no matter how complete — does not produce understanding." theme={theme}>Wittrock's (1989) Generative Learning Theory</Highlight> explains the mechanism: when you rephrase information in your own words, you are forced to build connections between the new material and your existing knowledge. You must relate new concepts to what you already understand in order to express them differently. This connection-building is what transforms information from something you've heard into something you know.</p>
              <p>Three generative strategies will transform your note-taking. First, <Highlight description="After hearing or reading a concept, close the source and write a single sentence that captures the core idea. The one-sentence constraint forces you to identify what actually matters, discarding peripheral details. If you can't summarise it, you haven't understood it." theme={theme}>summarise each concept in one sentence</Highlight> — the constraint forces compression. Second, <Highlight description="Creating your own example tests for transfer, not just recall. If you can generate a novel instance of a concept, you understand the principle, not just the specific case you were taught. This is the deepest form of note-taking." theme={theme}>create your own example</Highlight> — if you can generate a new instance, you truly understand the principle. Third, <Highlight description="Explicitly linking new information to something you already know activates your existing knowledge schema and integrates the new material into it. This makes the new information far more durable and retrievable because it's connected to multiple retrieval pathways." theme={theme}>connect to something you already know</Highlight> — bridging to prior knowledge creates multiple retrieval pathways. These three moves — summarise, exemplify, connect — are the engine of generative note-taking.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Cornell System." eyebrow="Step 3" icon={Layers} theme={theme}>
              <p>Knowing that generative notes are superior is one thing. Having a system that structures them is another. The <Highlight description="Developed by Walter Pauk at Cornell University in the 1950s and refined in his textbook 'How to Study in College' (Pauk & Owens, 2010). The system divides the page into three zones that separate the act of note-taking from the acts of questioning and summarising — building a complete study system into the notes themselves." theme={theme}>Cornell Method</Highlight>, developed by Walter Pauk at Cornell University and refined in Pauk and Owens (2010), structures your page into three deliberate zones. The main notes area (the right column, roughly two-thirds of the page) is where you write during the lecture or study session — using generative strategies, not verbatim transcription. You paraphrase, summarise, and connect as you go.</p>
              <p>The real power emerges after the session. The <Highlight description="The left column of the Cornell template (roughly one-third of the page width). After the study session, you review your main notes and write key questions and terms in this column. These cues become your built-in retrieval practice tool — you cover the right column and use only the cues to test yourself." theme={theme}>cue column</Highlight> (the narrow left column) is completed within 24 hours of the session. You review your main notes and distill them into key questions and trigger terms. "What are the three types of rock?" "Explain osmosis in your own words." "Why does temperature affect reaction rate?" These cues transform your notes into a self-testing tool. Cover the right column, read the cues, and attempt to recall the content. That's <Highlight description="The evidence-based study strategy of attempting to retrieve information from memory rather than re-reading it. Retrieval practice is one of the most powerful learning techniques known to cognitive science, producing significantly better retention than passive review." theme={theme}>retrieval practice</Highlight> built directly into your notes.</p>
              <p>The <Highlight description="The bottom section of the Cornell page (roughly the bottom fifth). Written within 24 hours of the session, the summary forces you to compress the entire page of notes into one to three sentences. This generative compression requires deep processing and creates a powerful review aid — you can scan summaries to quickly identify which pages need further study." theme={theme}>summary section</Highlight> (the bottom of the page) completes the system. Within 24 hours, you write a one-to-three-sentence summary of the entire page. This forces another round of generative processing — compressing everything into its essence. The Cornell Method isn't just a note-taking format; it's a complete study system that embeds retrieval practice and generative processing into the structure of your notes.</p>
              <CornellNoteSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Mapping vs Listing." eyebrow="Step 4" icon={GitBranch} theme={theme}>
              <p>Even generative notes can take different structural forms, and the structure you choose should match the structure of the knowledge. In a comprehensive meta-analysis, <Highlight description="John Nesbit (Simon Fraser University) and Olusola Adesope (Washington State University) analysed 55 studies comparing concept maps to other study activities. They found that concept maps consistently outperformed text-based summaries, lists, and outlines for tasks requiring understanding of relationships between ideas." theme={theme}>Nesbit and Adesope (2006)</Highlight> found that concept maps consistently outperformed linear notes for tasks requiring understanding of relationships between ideas. When you write linear notes — numbered lists, bullet points, sequential outlines — you capture sequences. When you draw concept maps — nodes connected by labelled arrows — you capture structures.</p>
              <p>Consider the difference when studying Biology. A linear note might read: "1. Photosynthesis occurs in chloroplasts. 2. It requires sunlight, water, and CO2. 3. It produces glucose and oxygen." This captures facts in order. A concept map of the same content would show <Highlight description="A visual representation showing how concepts relate to each other, with nodes (concepts) connected by labelled links (relationships). Unlike linear notes, maps reveal the architecture of a topic — which concepts are central, which are peripheral, and how they depend on each other." theme={theme}>photosynthesis at the centre</Highlight>, with arrows connecting it to its inputs (sunlight, water, CO2), its outputs (glucose, oxygen), its location (chloroplasts), and its relationship to cellular respiration. The map reveals the architecture — how everything connects — which the list obscures.</p>
              <p>However, mapping isn't always superior. For sequential or procedural content — mathematical proofs, step-by-step chemical calculations, chronological historical narratives — <Highlight description="Note-taking structures should mirror the structure of the knowledge being learned. Interconnected conceptual knowledge (Biology, Business, History themes) benefits from maps. Sequential procedural knowledge (Maths proofs, Chemistry calculations, timelines) benefits from linear formats. The key insight is that there is no single best format." theme={theme}>linear notes may be more appropriate</Highlight> because the knowledge itself is sequential. The key insight is to match your note-taking structure to the structure of the knowledge. For subjects with interconnected concepts — Biology, History, Business — mapping reveals relationships that lists miss. For subjects with procedural sequences — Maths proofs, Chemistry calculations — linear formats preserve the step-by-step logic. The best note-takers switch between formats depending on what they're learning.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Building Your System." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The best note-taking system combines everything you've learned into a protocol that transforms notes from a passive record into an active study tool. <Highlight description="Kenneth Kiewra (University of Nebraska) conducted a comprehensive review in 1989 showing that the combination of organised notes plus active review dramatically outperformed all other note-taking conditions — including complete notes without review, and review without organised notes. Both organisation and review are necessary." theme={theme}>Kiewra (1989)</Highlight> reviewed decades of note-taking research and found that reviewed notes with organisation outperformed all other conditions. Not just organised notes. Not just reviewed notes. The combination of structure plus active review was the decisive factor.</p>
              <p>Here is your Generative Processing Protocol. <Highlight description="Phase 1 of the protocol. During the lecture or study session, use the Cornell format with the right column for main notes. Write in your own words — never copy a sentence verbatim. Summarise concepts in one sentence, create your own examples, and connect new ideas to prior knowledge." theme={theme}>During study</Highlight>: use the Cornell format. Write in the right column using your own words — never copy a sentence verbatim. Apply the three generative moves: summarise in one sentence, create your own example, connect to something you already know. For interconnected subjects, consider switching to concept maps to capture relationships. <Highlight description="Phase 2 of the protocol. Within 24 hours of the study session (before the next session if possible), review your main notes and add cue questions and key terms in the left column. Then write a one-to-three-sentence summary at the bottom. This second pass forces another round of generative processing." theme={theme}>Within 24 hours</Highlight>: return to your notes. Add cue questions and key terms in the left column. Write your summary at the bottom. This second pass forces another round of processing that dramatically strengthens encoding.</p>
              <p><Highlight description="Phase 3 of the protocol. Before your next study session on that topic, cover the right column and use only the cue questions to test yourself. This is retrieval practice — the most powerful learning technique known to cognitive science. The difficulty you feel during retrieval is the learning happening." theme={theme}>Before the next session</Highlight>: cover the main notes column. Read only the cue questions. Attempt to recall the content from memory. This is retrieval practice — and the difficulty you feel is not a sign of failure but of learning in progress. Check your answers against the main notes. Any cue you couldn't answer reveals a gap that needs targeted review. This three-phase system — generate, question, retrieve — turns every page of notes into a precision study tool.</p>
              <MicroCommitment theme={theme}>
                <p>For your next study session, draw the Cornell template: a vertical line 6cm from the left edge, a horizontal line 5cm from the bottom. Take notes in the right column using only your own words — never copy a sentence verbatim. Within 24 hours, add cue questions in the left column and a one-sentence summary at the bottom. Then close your notes and test yourself using only the cues.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheNoteTakingParadoxModule;
