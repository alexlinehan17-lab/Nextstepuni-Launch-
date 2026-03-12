/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, SquarePen, Layers, GitBranch, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { indigoTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
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
    { label: 'Locked in', x1: 0.66, x2: 1, color: '#10b981' },
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
    { id: 'transcription-trap', title: 'The Copy-Paste Trap', eyebrow: '01 // The Paradox', icon: FileText },
    { id: 'generative-note-taking', title: 'Notes That Actually Work', eyebrow: '02 // Think, Don\'t Copy', icon: SquarePen },
    { id: 'cornell-system', title: 'The Cornell Method', eyebrow: '03 // The System', icon: Layers },
    { id: 'mapping-vs-listing', title: 'Maps vs Lists', eyebrow: '04 // Choosing Your Layout', icon: GitBranch },
    { id: 'building-your-system', title: 'Building Your Own System', eyebrow: '05 // Putting It Together', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="45"
      moduleTitle="The Note-Taking Paradox"
      moduleSubtitle="Why Less Is More"
      moduleDescription="More notes doesn't mean more learning. Find out why writing less — but thinking more — is the secret to notes that actually help you in the exam."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Think More, Write Less"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Transcription Trap." eyebrow="Step 1" icon={FileText} theme={theme}>
              <p>Here is a paradox that trips up nearly every student: the more notes you take, the less you actually learn. A famous study compared students who typed their notes on laptops with students who wrote by hand. The laptop group wrote way more — basically copying the lecture word for word. The handwriters wrote far less. But when they were tested on questions that needed real understanding, <Highlight description="When you copy everything word for word, your brain switches off. You feel busy, but you're not actually thinking about what's being said." theme={theme}>the handwriters crushed it</Highlight>.</p>
              <PersonalStory name="Maeve" role="6th Year, Sligo"><p>I used to type every single word in class — my notes were basically a transcript. I felt so productive. Then I'd sit down to study and realise I couldn't remember any of it. When I switched to writing by hand and putting things in my own words, my notes got way shorter but I actually understood what I'd written. My History grade went up a full grade in the mocks.</p></PersonalStory>
              <p>Why? Because when you write by hand, you physically can't keep up with every word. You're forced to <Highlight description="When you have to pick out the important bits and say them your own way, your brain has to actually think about the material. That thinking is where the learning happens." theme={theme}>pick out what matters and say it your own way</Highlight>. You have to listen, understand, decide what's important, and rephrase it — all in real time. That process IS the learning. Your brain has to work hard to shrink the information down, and that effort is what makes it <Highlight description="The stronger the mental effort you put into making sense of something, the better your brain stores it and the easier it is to remember later." theme={theme}>stick in your memory</Highlight>. Copying word for word, on the other hand, skips all of that. Your hand is busy, but your brain is on autopilot.</p>
              <p>This is the <Highlight description="It sounds backwards, but the study method that feels easiest and most productive — writing everything down — actually leads to the worst results. The method that feels harder — being selective and using your own words — leads to the best results." theme={theme}>Note-Taking Paradox</Highlight>: the strategy that feels most productive — capturing everything — is actually the one that produces the least learning. And the strategy that feels slow and incomplete — picking out the key ideas and putting them in your own words — is the one that builds real understanding. The rest of this module will show you how to make this work for you.</p>
              <NoteTakingComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Notes That Actually Work." eyebrow="Step 2" icon={SquarePen} theme={theme}>
              <p>This idea — that less writing leads to more learning — has been proven again and again over decades of research. Students who paraphrase, summarise, and make connections in their notes <Highlight description="When you put things in your own words instead of copying, you score way better — not just on basic recall questions, but on the tricky ones where you have to apply what you've learned to something new." theme={theme}>consistently outperform word-for-word note-takers by 30-40%</Highlight> on the kinds of questions that actually matter. Not just "name this thing" questions, but the ones where you have to apply what you know to a brand new situation — exactly the kind of questions you see on the Leaving Cert.</p>
              <p>Here's why it works: <Highlight description="Real learning only happens when you actively make connections between new stuff and things you already know. Just receiving information passively — no matter how much of it you write down — doesn't create understanding." theme={theme}>real learning only kicks in when you actively connect new information to things you already know</Highlight>. When you rephrase something in your own words, your brain has to figure out how it relates to what you already understand. You can't reword something unless you actually get it. That connection-building is what turns information from something you heard into something you know.</p>
              <p>Three simple moves will transform your note-taking. First, <Highlight description="After reading or hearing a concept, close the book and write one sentence that captures the main idea. If you can't boil it down, you probably don't understand it yet." theme={theme}>summarise each concept in one sentence</Highlight> — the constraint forces you to figure out what actually matters. Second, <Highlight description="If you can come up with your own example of a concept, you really get it. You're not just remembering the specific thing you were taught — you understand the idea behind it." theme={theme}>come up with your own example</Highlight> — if you can think of a new example, you truly understand the idea, not just the specific case you were taught. Third, <Highlight description="When you link new information to something you already know, your brain stores it in more places. That means more ways to find it again later — like having multiple doors into the same room." theme={theme}>connect it to something you already know</Highlight> — linking new ideas to old ones gives your brain more ways to find that information later. These three moves — summarise, give an example, connect — are what make notes actually useful.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Cornell System." eyebrow="Step 3" icon={Layers} theme={theme}>
              <p>Knowing that better notes exist is one thing. Having a system that makes it easy is another. The <Highlight description="A simple way to split your page into three zones — one for notes during class, one for questions after class, and one for a quick summary. It turns your notes into a built-in study tool." theme={theme}>Cornell Method</Highlight> splits your page into three zones. The main notes area (the right column, about two-thirds of the page) is where you write during class or study — using your own words, not copying. You paraphrase, summarise, and make connections as you go.</p>
              <p>The real power comes after the session. The <Highlight description="The narrow left column of the page. After class, you go back and write questions and key terms here. Then you can cover the right side and quiz yourself using only the cues — it's a built-in self-test." theme={theme}>cue column</Highlight> (the narrow left column) is filled in within 24 hours. You look over your main notes and turn them into key questions and trigger words. "What are the three types of rock?" "Explain osmosis in your own words." "Why does temperature affect reaction rate?" These cues turn your notes into a self-testing tool. Cover the right column, read the cues, and try to recall the answers. That's <Highlight description="Testing yourself by trying to remember something from memory, instead of just re-reading it. It feels harder, but it's one of the most powerful ways to make information stick." theme={theme}>self-testing</Highlight> built right into your notes.</p>
              <p>The <Highlight description="The bottom strip of the page. You write the whole page's content in one to three sentences. This forces you to figure out what really matters and gives you a quick way to scan your notes later." theme={theme}>summary section</Highlight> (the bottom of the page) completes the system. Within 24 hours, you write a one-to-three-sentence summary of the entire page. This forces you to boil everything down to its core — another round of real thinking. The Cornell Method isn't just a layout for your page; it's a complete study system that builds self-testing and real thinking into the structure of your notes.</p>
              <CornellNoteSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Mapping vs Listing." eyebrow="Step 4" icon={GitBranch} theme={theme}>
              <p>Even when you're writing notes in your own words, the shape of your notes matters too. Research across dozens of studies has shown that <Highlight description="When you draw out ideas as a map with arrows showing how things connect, you understand the relationships between ideas much better than if you just write a list." theme={theme}>concept maps consistently beat regular lists and bullet points</Highlight> when you need to understand how ideas relate to each other. When you write linear notes — numbered lists, bullet points, outlines — you capture things in order. When you draw concept maps — ideas in bubbles connected by arrows — you capture how things actually fit together.</p>
              <p>Think about studying Biology. A linear note might read: "1. Photosynthesis occurs in chloroplasts. 2. It requires sunlight, water, and CO2. 3. It produces glucose and oxygen." That captures facts in order. A concept map of the same content would put <Highlight description="A diagram where you put ideas in bubbles and draw arrows between them to show how they connect. Unlike lists, maps show you which ideas are central, which are less important, and how they depend on each other." theme={theme}>photosynthesis in the middle</Highlight>, with arrows connecting it to its inputs (sunlight, water, CO2), its outputs (glucose, oxygen), its location (chloroplasts), and its link to cellular respiration. The map shows you the big picture — how everything connects — which the list hides.</p>
              <p>But mapping isn't always better. For step-by-step content — Maths proofs, Chemistry calculations, historical timelines — <Highlight description="There's no single best format for notes. If the topic is about how ideas connect (like in Biology or Business), use a map. If it's about steps in order (like in Maths or Chemistry), use a list. The best note-takers switch it up depending on what they're studying." theme={theme}>linear notes are often the better choice</Highlight> because the knowledge itself follows a sequence. The key takeaway: match the shape of your notes to the shape of what you're learning. For subjects where ideas connect in webs — Biology, History, Business — mapping shows you relationships that lists miss. For subjects with step-by-step processes — Maths proofs, Chemistry calculations — linear formats keep the logic clear. The best note-takers switch between both depending on what they're studying.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Building Your System." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The best note-taking system pulls everything together — and decades of research confirm one thing: <Highlight description="Notes that are well-organised AND actively reviewed beat everything else. Having neat notes you never look at again doesn't work. Reviewing messy notes doesn't work either. You need both: good structure and regular review." theme={theme}>organised notes plus active review beats everything else</Highlight>. Not just neat notes. Not just reviewing notes. The combination of good structure plus actually going back and testing yourself is what makes the difference.</p>
              <p>Here's your three-step system. <Highlight description="Step one: while you're in class or studying, use the Cornell layout with the right column for your main notes. Always use your own words — never copy a sentence word for word. Summarise, give examples, and connect to things you already know." theme={theme}>During study</Highlight>: use the Cornell format. Write in the right column using your own words — never copy a sentence word for word. Use the three moves: summarise in one sentence, come up with your own example, connect to something you already know. For subjects where ideas connect in webs, try switching to concept maps. <Highlight description="Step two: within 24 hours of your study session, go back to your notes and add questions and key terms in the left column. Write a one-to-three-sentence summary at the bottom. This second pass forces your brain to process everything again, which makes it stick much better." theme={theme}>Within 24 hours</Highlight>: go back to your notes. Add cue questions and key terms in the left column. Write your summary at the bottom. This second pass forces your brain to process everything again, which massively strengthens your memory.</p>
              <p><Highlight description="Step three: before your next study session on that topic, cover the right column and test yourself using only the cue questions. The struggle you feel trying to remember is not failure — it's your brain strengthening its connections. That's where the real learning happens." theme={theme}>Before your next session</Highlight>: cover the main notes column. Read only the cue questions. Try to recall the answers from memory. This is self-testing — and the struggle you feel is not a sign of failure but of your brain getting stronger. Check your answers against the main notes. Any cue you couldn't answer shows you exactly where to focus next. This three-step system — write in your own words, add questions, test yourself — turns every page of notes into a powerful study tool.</p>
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
