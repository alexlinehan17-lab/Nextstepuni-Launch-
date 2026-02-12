/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, ClipboardList, ListFilter, PlayCircle, BarChart2, HeartPulse, HardHat } from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const triageQuestions = [
    { text: 'Q1 — Comprehension: Read the passage and answer parts (a) to (d) on language and style.', subject: 'Paper 1', marks: 50, correct: 'green' as const, reason: 'Comprehension has guided sub-parts and predictable question types. 50 reliable marks — always do this first.' },
    { text: 'Q5 — Composing: Write a personal essay in which you explore a moment that changed your perspective.', subject: 'Paper 1', marks: 100, correct: 'red' as const, reason: '100-mark essay is the biggest question on the paper. Needs planning, structure, and your best writing. Plan it during reading time, write it last when you know how much time you have.' },
    { text: 'Q3 — Functional Writing: Write a letter to a newspaper editor arguing for or against a proposed local development.', subject: 'Paper 1', marks: 50, correct: 'green' as const, reason: 'Functional writing has a clear format and structure. If you know the conventions (address, date, register), this is fast, bankable marks.' },
    { text: 'Q7 — Single Text: "Macbeth\'s downfall is entirely of his own making." Discuss with reference to the play.', subject: 'Paper 2', marks: 60, correct: 'amber' as const, reason: 'You know the play, but a 60-mark discuss question needs a structured argument with embedded quotes. Do it on your second pass with a clear plan.' },
    { text: 'Q2(b) — Comprehension: Identify three persuasive techniques used in Text 2 and comment on their effectiveness.', subject: 'Paper 1', marks: 15, correct: 'green' as const, reason: 'A short, targeted comprehension question — spot the techniques, write a line on each. Quick marks with low risk.' },
    { text: 'Q9 — Comparative Study: Compare how the theme of power is explored in at least two of your studied texts.', subject: 'Paper 2', marks: 70, correct: 'red' as const, reason: '70-mark comparative is the highest-stakes question on Paper 2. Needs a mode (theme, cultural context, or general vision) and sustained cross-referencing. Plan extensively, write last.' },
    { text: 'Q8 — Poetry: Discuss how the poetry of a studied poet appealed to both your mind and your emotions.', subject: 'Paper 2', marks: 50, correct: 'amber' as const, reason: 'Poetry requires careful quote selection and close reading. You know the poems, but crafting a strong response takes focus — do it second pass.' },
    { text: 'Q4 — Comprehension: Summarise the main argument of Text 3 in your own words (max 80 words).', subject: 'Paper 1', marks: 15, correct: 'green' as const, reason: 'A short summary with a word limit — read, condense, write. Minimal risk, fast completion.' },
];

const TriageSimulator = () => {
    const [phase, setPhase] = useState<'ready' | 'drill' | 'done'>('ready');
    const [qIndex, setQIndex] = useState(0);
    const [choices, setChoices] = useState<(string | null)[]>(Array(triageQuestions.length).fill(null));
    const [showFeedback, setShowFeedback] = useState(false);
    const [timeLeft, setTimeLeft] = useState(40);
    const [startTime, setStartTime] = useState(0);
    const [answerTimes, setAnswerTimes] = useState<number[]>([]);
    const [lastAnswerTime, setLastAnswerTime] = useState(0);

    const colorMap = { green: { bg: 'bg-emerald-100 dark:bg-emerald-900/30', border: 'border-emerald-300 dark:border-emerald-700', text: 'text-emerald-700 dark:text-emerald-300', label: 'Do First', dot: 'bg-emerald-500' }, amber: { bg: 'bg-amber-100 dark:bg-amber-900/30', border: 'border-amber-300 dark:border-amber-700', text: 'text-amber-700 dark:text-amber-300', label: 'Do Second', dot: 'bg-amber-500' }, red: { bg: 'bg-rose-100 dark:bg-rose-900/30', border: 'border-rose-300 dark:border-rose-700', text: 'text-rose-700 dark:text-rose-300', label: 'Do Last', dot: 'bg-rose-500' } };

    React.useEffect(() => {
        if (phase !== 'drill' || showFeedback) return;
        if (timeLeft <= 0) { setPhase('done'); return; }
        const t = setTimeout(() => setTimeLeft(s => s - 1), 1000);
        return () => clearTimeout(t);
    }, [phase, timeLeft, showFeedback]);

    const startDrill = () => {
        setPhase('drill');
        setQIndex(0);
        setChoices(Array(triageQuestions.length).fill(null));
        setAnswerTimes([]);
        setTimeLeft(40);
        setShowFeedback(false);
        const now = Date.now();
        setStartTime(now);
        setLastAnswerTime(now);
    };

    const handleChoice = (choice: string) => {
        if (showFeedback) return;
        const now = Date.now();
        const elapsed = (now - lastAnswerTime) / 1000;
        setLastAnswerTime(now);
        setAnswerTimes(prev => [...prev, elapsed]);
        const newChoices = [...choices];
        newChoices[qIndex] = choice;
        setChoices(newChoices);
        setShowFeedback(true);
        setTimeout(() => {
            setShowFeedback(false);
            if (qIndex + 1 >= triageQuestions.length) { setPhase('done'); }
            else { setQIndex(q => q + 1); }
        }, 1800);
    };

    const score = choices.filter((c, i) => c === triageQuestions[i].correct).length;
    const totalTime = ((Date.now() - startTime) / 1000);

    if (phase === 'ready') {
        return (
            <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">Triage Drill</h4>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-2 max-w-md mx-auto">Reading time has started. You have <strong className="text-zinc-700 dark:text-zinc-200">40 seconds</strong> to categorise 8 exam questions as:</p>
                <div className="flex justify-center gap-3 mb-6">
                    {(['green', 'amber', 'red'] as const).map(c => (
                        <span key={c} className={`px-3 py-1 rounded-full text-xs font-bold ${colorMap[c].bg} ${colorMap[c].text} border ${colorMap[c].border}`}>{colorMap[c].label}</span>
                    ))}
                </div>
                <button onClick={startDrill} className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm rounded-lg transition-colors">Start Triage</button>
            </div>
        );
    }

    if (phase === 'done') {
        return (
            <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Triage Results</h4>
                <div className="flex justify-center gap-4 my-5">
                    <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
                        <div className="text-2xl font-bold text-zinc-800 dark:text-white">{score}/{triageQuestions.length}</div>
                        <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">Correct</div>
                    </div>
                    <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
                        <div className="text-2xl font-bold text-zinc-800 dark:text-white">{Math.round(totalTime)}s</div>
                        <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">Total Time</div>
                    </div>
                    <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
                        <div className="text-2xl font-bold text-zinc-800 dark:text-white">{answerTimes.length > 0 ? (answerTimes.reduce((a,b) => a+b, 0) / answerTimes.length).toFixed(1) : '—'}s</div>
                        <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">Avg / Question</div>
                    </div>
                </div>
                <div className="space-y-2.5 mb-6">
                    {triageQuestions.map((q, i) => {
                        const got = choices[i];
                        const correct = got === q.correct;
                        const c = colorMap[q.correct];
                        return (
                            <div key={i} className={`p-3 rounded-lg border ${correct ? `${c.bg} ${c.border}` : 'bg-zinc-50 dark:bg-zinc-700/50 border-zinc-200 dark:border-zinc-600'}`}>
                                <div className="flex items-start gap-2.5">
                                    <span className={`mt-1 w-2 h-2 rounded-full flex-shrink-0 ${c.dot}`} />
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2 flex-wrap">
                                            <span className="text-xs font-bold text-zinc-400">{q.subject} · {q.marks}m</span>
                                            {correct ? (
                                                <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">Correct</span>
                                            ) : (
                                                <span className="text-xs font-bold text-rose-600 dark:text-rose-400">You said {got ? colorMap[got as keyof typeof colorMap].label : 'nothing'} — should be {c.label}</span>
                                            )}
                                            {answerTimes[i] !== undefined && <span className="text-xs text-zinc-400">{answerTimes[i].toFixed(1)}s</span>}
                                        </div>
                                        <p className="text-sm text-zinc-600 dark:text-zinc-300 mt-0.5">{q.text}</p>
                                        {!correct && <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 italic">{q.reason}</p>}
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
                {score < triageQuestions.length && (
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 text-center mb-4 italic">The goal is speed <strong>and</strong> accuracy. In the real exam, a wrong triage means wasting time on hard questions while easy marks go uncollected.</p>
                )}
                <div className="text-center">
                    <button onClick={startDrill} className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm rounded-lg transition-colors">Run Drill Again</button>
                </div>
            </div>
        );
    }

    const q = triageQuestions[qIndex];
    const isCorrect = showFeedback && choices[qIndex] === q.correct;
    const isWrong = showFeedback && choices[qIndex] !== q.correct;
    const timerPct = (timeLeft / 40) * 100;

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <div className="flex items-center justify-between mb-4">
                <h4 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white">Triage Drill</h4>
                <div className="flex items-center gap-3">
                    <span className="text-xs font-bold text-zinc-400">{qIndex + 1} / {triageQuestions.length}</span>
                    <span className={`text-sm font-bold tabular-nums ${timeLeft <= 10 ? 'text-rose-500' : 'text-zinc-600 dark:text-zinc-300'}`}>{timeLeft}s</span>
                </div>
            </div>
            {/* Timer bar */}
            <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-700 rounded-full mb-5">
                <motion.div className={`h-full rounded-full ${timeLeft <= 10 ? 'bg-rose-500' : 'bg-amber-500'}`} animate={{ width: `${timerPct}%` }} transition={{ duration: 0.3 }} />
            </div>
            {/* Question card */}
            <AnimatePresence mode="wait">
                <motion.div key={qIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
                    className={`p-5 rounded-xl border min-h-[100px] flex flex-col justify-center mb-5 transition-colors ${
                        isCorrect ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-300 dark:border-emerald-700' :
                        isWrong ? 'bg-rose-50 dark:bg-rose-900/30 border-rose-300 dark:border-rose-700' :
                        'bg-zinc-50 dark:bg-zinc-700/50 border-zinc-200 dark:border-zinc-600'
                    }`}>
                    <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs font-bold text-amber-600 dark:text-amber-400">{q.subject}</span>
                        <span className="text-xs text-zinc-400">·</span>
                        <span className="text-xs font-semibold text-zinc-400">{q.marks} marks</span>
                    </div>
                    <p className="font-semibold text-zinc-700 dark:text-zinc-200 text-sm">{q.text}</p>
                    {showFeedback && (
                        <motion.p initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className={`text-xs mt-3 italic ${isCorrect ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                            {isCorrect ? 'Correct! ' : `Not quite — this is "${colorMap[q.correct].label}". `}{q.reason}
                        </motion.p>
                    )}
                </motion.div>
            </AnimatePresence>
            {/* Choice buttons */}
            <div className="grid grid-cols-3 gap-3">
                {(['green', 'amber', 'red'] as const).map(c => {
                    const cm = colorMap[c];
                    const selected = showFeedback && choices[qIndex] === c;
                    const isAnswer = showFeedback && q.correct === c;
                    return (
                        <button key={c} onClick={() => handleChoice(c)} disabled={showFeedback}
                            className={`p-3 rounded-xl font-bold text-sm border transition-all ${
                                isAnswer ? `${cm.bg} ${cm.text} ${cm.border} ring-2 ring-offset-1 ring-emerald-500` :
                                selected && !isAnswer ? 'bg-rose-100 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 border-rose-300 dark:border-rose-700' :
                                `${cm.bg} ${cm.text} ${cm.border} hover:opacity-80`
                            } ${showFeedback ? 'cursor-default' : 'cursor-pointer'}`}>
                            <div className={`w-3 h-3 rounded-full ${cm.dot} mx-auto mb-1.5`} />
                            {cm.label}
                        </button>
                    );
                })}
            </div>
            {/* Progress dots */}
            <div className="flex justify-center gap-1.5 mt-5">
                {triageQuestions.map((_, i) => (
                    <div key={i} className={`w-2 h-2 rounded-full transition-colors ${
                        i < qIndex ? (choices[i] === triageQuestions[i].correct ? 'bg-emerald-500' : 'bg-rose-500') :
                        i === qIndex ? 'bg-amber-500' : 'bg-zinc-200 dark:bg-zinc-600'
                    }`} />
                ))}
            </div>
        </div>
    );
}

const MPMCalculator = () => {
    const [time, setTime] = useState(180);
    const [marks, setMarks] = useState(100);
    const [buffer, setBuffer] = useState(15);
    const mpm = (time - buffer) / marks;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Minutes-Per-Mark (MPM) Calculator</h4>
             <div className="grid grid-cols-3 gap-4 mt-6">
                <div><label className="text-xs font-bold">Total Time (mins)</label><input type="number" value={time} onChange={e=>setTime(parseInt(e.target.value))} className="w-full p-2 bg-zinc-100 dark:bg-zinc-800 rounded-md" /></div>
                <div><label className="text-xs font-bold">Total Marks</label><input type="number" value={marks} onChange={e=>setMarks(parseInt(e.target.value))} className="w-full p-2 bg-zinc-100 dark:bg-zinc-800 rounded-md" /></div>
                <div><label className="text-xs font-bold">Buffer (mins)</label><input type="number" value={buffer} onChange={e=>setBuffer(parseInt(e.target.value))} className="w-full p-2 bg-zinc-100 dark:bg-zinc-800 rounded-md" /></div>
             </div>
             <div className="mt-6 p-4 bg-zinc-900 rounded-xl text-center text-white">
                Your MPM is <span className="font-bold text-2xl text-amber-400">{mpm.toFixed(2)}</span>. A 20-mark question gets <span className="font-bold text-amber-400">{(mpm*20).toFixed(1)}</span> minutes.
             </div>
        </div>
    )
}

const BoxBreathingVisualizer = () => {
    const [active, setActive] = useState(false);
    const [phase, setPhase] = useState(0);
    const [count, setCount] = useState(4);
    const [cycle, setCycle] = useState(0);
    const totalCycles = 3;

    const phases = [
      { label: 'Breathe In', color: 'text-cyan-500' },
      { label: 'Hold', color: 'text-sky-400' },
      { label: 'Breathe Out', color: 'text-teal-500' },
      { label: 'Hold', color: 'text-sky-400' },
    ];

    const arcColors = ['#06b6d4', '#38bdf8', '#14b8a6', '#38bdf8'];
    const radius = 88;

    const getArcPath = (index: number) => {
      const startAngle = (index * 90 - 90) * (Math.PI / 180);
      const endAngle = ((index + 1) * 90 - 90) * (Math.PI / 180);
      const x1 = 100 + radius * Math.cos(startAngle);
      const y1 = 100 + radius * Math.sin(startAngle);
      const x2 = 100 + radius * Math.cos(endAngle);
      const y2 = 100 + radius * Math.sin(endAngle);
      return `M ${x1} ${y1} A ${radius} ${radius} 0 0 1 ${x2} ${y2}`;
    };

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
     <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
         <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">4-4-4-4 Box Breathing</h4>
         <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Feeling panicked? Run this protocol. 4 seconds per phase, 3 cycles.</p>

         <div className="flex justify-center mb-6">
           <div className="relative w-52 h-52">
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

             <div className={`absolute -top-6 left-1/2 -translate-x-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 0 ? 'text-cyan-500 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Inhale</div>
             <div className={`absolute top-1/2 -right-10 -translate-y-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 1 ? 'text-sky-400 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Hold</div>
             <div className={`absolute -bottom-6 left-1/2 -translate-x-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 2 ? 'text-teal-500 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Exhale</div>
             <div className={`absolute top-1/2 -left-8 -translate-y-1/2 text-[9px] font-bold uppercase tracking-wider transition-opacity duration-300 ${active && phase === 3 ? 'text-sky-400 opacity-100' : 'text-zinc-300 dark:text-zinc-600 opacity-60'}`}>Hold</div>

             <div className="absolute inset-0 flex items-center justify-center">
               <motion.div
                 animate={{
                   scale: active ? breathScale : 1,
                 }}
                 transition={{ duration: 3.8, ease: 'easeInOut' }}
                 className="w-28 h-28 rounded-full bg-cyan-50 dark:bg-cyan-950/30 border-2 border-cyan-200 dark:border-cyan-800/50 flex flex-col items-center justify-center"
               >
                 {active ? (
                   <>
                     <motion.p
                       key={`${phase}-${count}`}
                       initial={{ scale: 1.2, opacity: 0 }}
                       animate={{ scale: 1, opacity: 1 }}
                       className="text-3xl font-bold text-cyan-600 dark:text-cyan-400"
                     >
                       {count}
                     </motion.p>
                     <p className={`text-[10px] font-bold ${phases[phase].color}`}>{phases[phase].label}</p>
                   </>
                 ) : (
                   <p className="text-xs font-semibold text-zinc-400 dark:text-zinc-500">Ready</p>
                 )}
               </motion.div>
             </div>
           </div>
         </div>

         {active && (
           <div className="flex justify-center gap-2 mb-6">
             {Array.from({ length: totalCycles }).map((_, i) => (
               <div key={i} className={`w-2 h-2 rounded-full transition-colors ${i < cycle ? 'bg-cyan-500' : i === cycle ? 'bg-cyan-300' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
             ))}
           </div>
         )}

         <div className="flex justify-center">
           {!active ? (
             <button
               onClick={handleStart}
               className="px-6 py-2.5 bg-cyan-500 text-white font-bold text-sm rounded-xl hover:bg-cyan-600 shadow-lg shadow-cyan-500/20 transition-all"
             >
               {done ? 'Begin' : 'Start Again'}
             </button>
           ) : (
             <button
               onClick={() => setActive(false)}
               className="px-6 py-2.5 bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 font-bold text-sm rounded-xl hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-all"
             >
               Stop
             </button>
           )}
         </div>
    </div>
    );
}

// --- MODULE COMPONENT ---
const ExamHallStrategiesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'execution-gap', title: 'The Execution Gap', eyebrow: '01 // The Problem', icon: Cpu },
    { id: 'cognitive-offloading', title: 'Cognitive Offloading', eyebrow: '02 // The Dump Sheet', icon: ClipboardList },
    { id: 'tactical-triage', title: 'Tactical Triage', eyebrow: '03 // Reading Time Strategy', icon: ListFilter },
    { id: 'order-of-attack', title: 'Order of Attack', eyebrow: '04 // The Momentum Principle', icon: PlayCircle },
    { id: 'exam-economics', title: 'Exam Economics', eyebrow: '05 // Strict Time Budgeting', icon: BarChart2 },
    { id: 'anxiety-regulation', title: 'Anxiety Regulation', eyebrow: '06 // Physiological Management', icon: HeartPulse },
    { id: 'post-exam-training', title: 'Post-Exam Training', eyebrow: '07 // The Drills', icon: HardHat },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Exam Hall Strategies"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Execution Gap." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>You can be the smartest person in the room, have every definition memorized, and still get a bad result. The gap between what you know (<Highlight description="What you have learned and stored in your long-term memory over months of study." theme={theme}>Competence</Highlight>) and what you can actually do on the day (<Highlight description="What you can retrieve and apply from your memory under the intense pressure of a timed exam." theme={theme}>Performance</Highlight>) is called the <strong>Execution Gap</strong>. This module is about closing that gap.</p>
              <p>The exam hall is not a library for quiet recall; it's a high-pressure, resource-management game. The pressure adds <Highlight description="The 'bad' mental workload that comes from things other than the question itself, like managing your panic, checking the clock, or trying to remember a formula." theme={theme}>Extraneous Cognitive Load</Highlight> to your brain, stealing the limited mental bandwidth you need for the actual questions. The strategies in this module are about minimizing that load so you can show what you really know.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Cognitive Offloading." eyebrow="Step 2" icon={ClipboardList} theme={theme}>
              <p>In the first few minutes of an exam, your stress hormones spike, which can block access to your memory. The <Highlight description="A pre-memorized sheet of high-yield, high-volatility information that you write down from memory at the very start of the exam before you even look at the questions." theme={theme}>"Dump Sheet"</Highlight> is a proactive strategy to combat this. It's about getting the most fragile, important information out of your head and onto paper before stress can erase it.</p>
              <p>This isn't cheating; it's <Highlight description="The act of moving information from your limited biological working memory to a physical resource (like paper), freeing up mental capacity to focus on problem-solving." theme={theme}>Cognitive Offloading</Highlight>. The sheet should contain "High-Yield, High-Volatility" information: things that are easy to forget under pressure but are likely to be useful (e.g., key quotes, formulas, dates, acronyms). You must rehearse writing it until it's a 3-minute automatic motor skill.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Tactical Triage." eyebrow="Step 3" icon={ListFilter} theme={theme}>
              <p>Reading time is not for passively reading. It's for <Highlight description="An active process during reading time where you scan the entire paper and sort questions into categories of difficulty, like a medic at a disaster scene." theme={theme}>Tactical Triage</Highlight>. Just like in an emergency room, your goal isn't to save every "patient" (question) perfectly; it's to get the most marks possible with your limited time.</p>
              <p>Use a <strong>Traffic Light System</strong>: <strong>Green</strong> questions are "low-hanging fruit" you're 100% confident you can answer quickly. <strong>Amber</strong> questions are ones you know how to do but will take time or complex calculation. <strong>Red</strong> questions are "time sinks"--topics you're weak on or don't immediately understand. Your first job is to find 2-3 "Green" questions to serve as your <Highlight description="The first easy questions you attempt, regardless of their position on the paper. They build confidence, calm your nerves, and create psychological momentum." theme={theme}>Anchor Questions</Highlight>.</p>
              <TriageSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Order of Attack." eyebrow="Step 4" icon={PlayCircle} theme={theme}>
              <p>Starting at Question 1 is a rookie mistake. It gives control to the examiner, who may have put a difficult question first. You need to become a <Highlight description="A concept from cybersecurity where an attacker seeks the easiest path to breach a system. In an exam, you should act like one, seeking the easiest path to accumulate marks." theme={theme}>"Work-Averse Attacker"</Highlight>, extracting the maximum marks for the minimum effort. This means attacking the "Green" questions first, no matter where they are.</p>
              <p>This builds <Highlight description="The psychological phenomenon where early success creates a virtuous cycle of confidence and dopamine release, improving focus and making subsequent harder tasks feel more manageable." theme={theme}>Psychological Momentum</Highlight>. If you can't figure out a question in 30 seconds (the "30-Second Rule"), skip it immediately. The <Highlight description="The subconscious mind continues to work on a problem even after you've moved on. When you return to the question later, the solution often appears 'obvious.'" theme={theme}>Incubation Effect</Highlight> means your brain will keep working on it in the background.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Exam Economics." eyebrow="Step 5" icon={BarChart2} theme={theme}>
              <p>Time is the currency of the exam hall. Every minute is an investment that must provide a return (marks). The core metric is <Highlight description="Your fundamental time budget, calculated by dividing the total time (minus a buffer) by the total marks. E.g., (180-15 mins) / 100 marks = 1.65 minutes per mark." theme={theme}>Minutes Per Mark (MPM)</Highlight>. This tells you exactly how long you can spend on any given question.</p>
              <p>When your timer for a question goes off, you must execute a <Highlight description="The discipline of stopping work on a question immediately when its time budget expires, even if you are mid-sentence, to avoid the Sunk Cost Fallacy." theme={theme}>"Hard Stop."</Highlight> This is the hardest discipline to learn because of the <Highlight description="The cognitive bias to continue investing in a losing proposition (like a hard question) because of the resources (time) you have already spent. It's the number one cause of time mismanagement in exams." theme={theme}>Sunk Cost Fallacy</Highlight>. The first 5 minutes on a new question will always be more valuable than the last 5 minutes polishing an old one.</p>
              <MPMCalculator/>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Anxiety Regulation." eyebrow="Step 6" icon={HeartPulse} theme={theme}>
              <p>When you hit a difficult question, your sympathetic nervous system can trigger a "Panic Spike," narrowing your focus and blocking access to your memory. You need a protocol to fight back. The fastest is <Highlight description="A breathing technique (4s inhale, 4s hold, 4s exhale, 4s hold) that forces your nervous system back into a calm 'rest and digest' state." theme={theme}>Box Breathing</Highlight>.</p>
              <p>Another tool is the <Highlight description="A grounding technique where you name 3 things you see, 3 sounds you hear, and 3 body parts you can feel. It forces your brain to process sensory data, disengaging the emotional amygdala hijack." theme={theme}>3-3-3 Rule</Highlight> for grounding. Finally, use <Highlight description="Changing your internal story from catastrophic ('I'm failing') to procedural ('This is a Red question. This is part of the plan. I will flag it and move on.')." theme={theme}>Cognitive Reframing</Highlight> to turn panic into a planned response.</p>
              <BoxBreathingVisualizer />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Training Protocol." eyebrow="Step 7" icon={HardHat} theme={theme}>
              <p>These strategies are skills. They must be trained. After every practice test, you must use an <Highlight description="A post-exam reflection tool that forces you to analyze your errors by process ('I misread the question,' 'I ran out of time') not just by content ('I didn't know the date')." theme={theme}>Exam Wrapper</Highlight> to analyze your performance. Did your triage work? Did you stick to your time budget?</p>
              <p>You must also run specific drills. <strong>Triage Drills</strong>: Give yourself 5 minutes with a past paper to *only* categorize questions as Green, Amber, or Red. <strong>Dump Sprints</strong>: Practice writing your dump sheet until it takes less than 3 minutes. <strong>Hard Stop Drills</strong>: Do questions with a strict timer and force yourself to stop when it rings. This builds the discipline you need to execute under pressure.</p>
              <MicroCommitment theme={theme}><p>For your next practice test, do a full "Exam Wrapper" analysis afterwards. Don't just check the answers; analyze *how* you took the test.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamHallStrategiesModule;
