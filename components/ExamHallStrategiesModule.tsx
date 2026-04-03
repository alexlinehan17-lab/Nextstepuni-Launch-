/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Cpu, ClipboardList, ListFilter, PlayCircle, BarChart2, HeartPulse, HardHat } from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
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
    const [totalTime, setTotalTime] = useState(0);
    const [answerTimes, setAnswerTimes] = useState<number[]>([]);
    const [lastAnswerTime, setLastAnswerTime] = useState(0);
    const choiceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    React.useEffect(() => {
        return () => {
            if (choiceTimerRef.current) clearTimeout(choiceTimerRef.current);
        };
    }, []);

    const colorMap = { green: { bg: 'bg-emerald-100 dark:bg-emerald-900/30', border: 'border-emerald-300 dark:border-emerald-700', text: 'text-emerald-700 dark:text-emerald-300', label: 'Do First', dot: 'bg-emerald-500' }, amber: { bg: 'bg-amber-100 dark:bg-amber-900/30', border: 'border-amber-300 dark:border-amber-700', text: 'text-amber-700 dark:text-amber-300', label: 'Do Second', dot: 'bg-amber-500' }, red: { bg: 'bg-rose-100 dark:bg-rose-900/30', border: 'border-rose-300 dark:border-rose-700', text: 'text-rose-700 dark:text-rose-300', label: 'Do Last', dot: 'bg-rose-500' } };

    React.useEffect(() => {
        if (phase !== 'drill' || showFeedback) return;
        if (timeLeft <= 0) { setTotalTime((Date.now() - startTime) / 1000); setPhase('done'); return; }
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
        choiceTimerRef.current = setTimeout(() => {
            setShowFeedback(false);
            if (qIndex + 1 >= triageQuestions.length) { setTotalTime((Date.now() - startTime) / 1000); setPhase('done'); }
            else { setQIndex(q => q + 1); }
        }, 1800);
    };

    const score = choices.filter((c, i) => c === triageQuestions[i].correct).length;

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

const dumpSheetFacts = [
    { text: 'Area of circle = \u03C0r\u00B2', keys: [/\u03C0r/i, /pi r/i] },
    { text: 'Photosynthesis: 6CO\u2082 + 6H\u2082O \u2192 C\u2086H\u2081\u2082O\u2086 + 6O\u2082', keys: [/photosynthesis/i, /6CO2/i, /C6H12O6/i] },
    { text: '1916 Rising: 24\u201330 April', keys: [/1916/i], combo: [/april/i, /24/] },
    { text: '\u2018Fair is foul, and foul is fair\u2019 \u2014 Macbeth, Act 1', keys: [/fair is foul/i, /foul is fair/i] },
    { text: 'GDP = C + I + G + (X \u2212 M)', keys: [/GDP/i, /C \+ I \+ G/i] },
    { text: 'Mitosis: PMAT (Prophase, Metaphase, Anaphase, Telophase)', keys: [/PMAT/i], combo: [/mitosis/i, /prophase|metaphase/i] },
    { text: 'Speed = Distance \u00F7 Time', keys: [/speed/i], combo: [/speed/i, /distance/i] },
    { text: 'Peig Sayers: \u2018Is fearr Gaeilge briste n\u00E1 B\u00E9arla cliste\u2019', keys: [/fearr/i, /Gaeilge briste/i] },
    { text: 'Quadratic formula: x = (\u2212b \u00B1 \u221A(b\u00B2\u22124ac)) / 2a', keys: [/quadratic/i, /-b \u00B1/i, /b\u00B2-4ac/i, /b2-4ac/i] },
    { text: 'Igneous, Sedimentary, Metamorphic \u2014 3 rock types', keys: [/igneous/i, /sedimentary/i, /metamorphic/i] },
];

const checkFactRecalled = (factIndex: number, text: string): boolean => {
    const fact = dumpSheetFacts[factIndex];
    // If any single key matches, it's recalled
    if (fact.keys.some(k => k.test(text))) return true;
    // If there's a combo requirement (all patterns in combo must match)
    if (fact.combo && fact.combo.every(k => k.test(text))) return true;
    return false;
};

const DumpSheetBuilder = () => {
    const [phase, setPhase] = useState<'ready' | 'memorise' | 'recall' | 'results'>('ready');
    const [memoriseTime, setMemoriseTime] = useState(30);
    const [recallTime, setRecallTime] = useState(60);
    const [recallText, setRecallText] = useState('');
    const [results, setResults] = useState<boolean[]>([]);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, []);

    useEffect(() => {
        if (phase === 'memorise') {
            intervalRef.current = setInterval(() => {
                setMemoriseTime(t => {
                    if (t <= 1) {
                        if (intervalRef.current) clearInterval(intervalRef.current);
                        setPhase('recall');
                        return 0;
                    }
                    return t - 1;
                });
            }, 1000);
            return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
        }
    }, [phase]);

    useEffect(() => {
        if (phase === 'recall') {
            setRecallTime(60);
            intervalRef.current = setInterval(() => {
                setRecallTime(t => {
                    if (t <= 1) {
                        if (intervalRef.current) clearInterval(intervalRef.current);
                        setPhase('results');
                        return 0;
                    }
                    return t - 1;
                });
            }, 1000);
            return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
        }
    }, [phase]);

    useEffect(() => {
        if (phase === 'results') {
            const r = dumpSheetFacts.map((_, i) => checkFactRecalled(i, recallText));
            setResults(r);
        }
    }, [phase]);

    const startDrill = () => {
        setPhase('memorise');
        setMemoriseTime(30);
        setRecallTime(60);
        setRecallText('');
        setResults([]);
    };

    const tryAgain = () => {
        setPhase('ready');
        setRecallText('');
        setResults([]);
    };

    const timerColor = (time: number, total: number) => {
        const pct = time / total;
        if (pct > 0.5) return 'text-emerald-500';
        if (pct > 0.2) return 'text-amber-500';
        return 'text-rose-500';
    };

    const timerBarColor = (time: number, total: number) => {
        const pct = time / total;
        if (pct > 0.5) return 'bg-emerald-500';
        if (pct > 0.2) return 'bg-amber-500';
        return 'bg-rose-500';
    };

    if (phase === 'ready') {
        return (
            <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Dump Sheet Drill</h4>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-6 max-w-lg mx-auto">Practice the brain dump that should be your first action in every exam.</p>
                <div className="flex flex-col items-center gap-3 mb-6">
                    <div className="flex items-center gap-4 text-xs font-semibold text-zinc-500 dark:text-zinc-400">
                        <span className="px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-700">30s to memorise</span>
                        <span className="text-zinc-300 dark:text-zinc-600">&rarr;</span>
                        <span className="px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-700">60s to recall</span>
                        <span className="text-zinc-300 dark:text-zinc-600">&rarr;</span>
                        <span className="px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-700">See your score</span>
                    </div>
                </div>
                <button onClick={startDrill} className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm rounded-lg transition-colors">Start Drill</button>
            </div>
        );
    }

    if (phase === 'memorise') {
        const pct = (memoriseTime / 30) * 100;
        return (
            <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
                <div className="flex items-center justify-between mb-2">
                    <h4 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white">Memorise These Facts</h4>
                    <span className={`text-2xl font-bold tabular-nums ${timerColor(memoriseTime, 30)}`}>{memoriseTime}s</span>
                </div>
                <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-700 rounded-full mb-6">
                    <motion.div className={`h-full rounded-full ${timerBarColor(memoriseTime, 30)}`} animate={{ width: `${pct}%` }} transition={{ duration: 0.3 }} />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {dumpSheetFacts.map((fact, i) => (
                        <MotionDiv
                            key={i}
                            initial={{ opacity: 0, y: 8 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className="p-3 rounded-lg bg-zinc-50 dark:bg-zinc-700/50 border border-zinc-200 dark:border-zinc-600"
                        >
                            <span className="text-xs font-bold text-amber-600 dark:text-amber-400 mr-2">{i + 1}.</span>
                            <span className="text-sm font-medium text-zinc-700 dark:text-zinc-200" style={{ fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace' }}>{fact.text}</span>
                        </MotionDiv>
                    ))}
                </div>
            </div>
        );
    }

    if (phase === 'recall') {
        const pct = (recallTime / 60) * 100;
        return (
            <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
                <div className="flex items-center justify-between mb-2">
                    <h4 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white">Write Everything You Remember</h4>
                    <span className={`text-2xl font-bold tabular-nums ${timerColor(recallTime, 60)}`}>{recallTime}s</span>
                </div>
                <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-700 rounded-full mb-4">
                    <motion.div className={`h-full rounded-full ${timerBarColor(recallTime, 60)}`} animate={{ width: `${pct}%` }} transition={{ duration: 0.3 }} />
                </div>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Don't worry about order or exact wording.</p>
                <textarea
                    value={recallText}
                    onChange={e => setRecallText(e.target.value)}
                    disabled={recallTime <= 0}
                    placeholder="Start typing everything you remember..."
                    className="w-full h-48 p-4 bg-zinc-50 dark:bg-zinc-700/50 border border-zinc-200 dark:border-zinc-600 rounded-xl text-sm text-zinc-700 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 resize-none transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
                    autoFocus
                />
            </div>
        );
    }

    // Results phase
    const score = results.filter(Boolean).length;
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Results</h4>
            <div className="text-center my-5">
                <div className="inline-block px-6 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
                    <span className="text-3xl font-bold text-zinc-800 dark:text-white">{score}</span>
                    <span className="text-lg text-zinc-500 dark:text-zinc-400">/{dumpSheetFacts.length} recalled</span>
                </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
                {dumpSheetFacts.map((fact, i) => {
                    const recalled = results[i];
                    return (
                        <MotionDiv
                            key={i}
                            initial={{ opacity: 0, y: 8 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className={`p-3 rounded-lg border flex items-start gap-2.5 ${
                                recalled
                                    ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-300 dark:border-emerald-700'
                                    : 'bg-rose-50 dark:bg-rose-900/20 border-rose-300 dark:border-rose-700'
                            }`}
                        >
                            <span className={`mt-0.5 flex-shrink-0 text-sm font-bold ${recalled ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                                {recalled ? '\u2713' : '\u2717'}
                            </span>
                            <span className="text-sm font-medium text-zinc-700 dark:text-zinc-200" style={{ fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace' }}>{fact.text}</span>
                        </MotionDiv>
                    );
                })}
            </div>
            <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 mb-6">
                <p className="text-sm text-amber-800 dark:text-amber-300 leading-relaxed">In the real exam, your dump sheet prevents interference — facts written down can't be displaced by exam stress. Do this in the first 2 minutes of every paper.</p>
            </div>
            <div className="text-center">
                <button onClick={tryAgain} className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm rounded-lg transition-colors">Try Again</button>
            </div>
        </div>
    );
};

const attackQuestions = [
    { id: 'q1', label: 'Q1: Short Questions (10 x 3 marks)', marks: 30, difficulty: 'green' as const },
    { id: 'q2', label: 'Q2: Essay on Theme of Ambition', marks: 60, difficulty: 'amber' as const },
    { id: 'q3', label: 'Q3: Algebra & Functions', marks: 50, difficulty: 'green' as const },
    { id: 'q4', label: 'Q4: Unseen Poetry Analysis', marks: 40, difficulty: 'red' as const },
    { id: 'q5', label: 'Q5: Experiment: Effect of pH on Enzyme', marks: 30, difficulty: 'green' as const },
    { id: 'q6', label: 'Q6: Extended Response: Evaluate Impact of WW2', marks: 50, difficulty: 'amber' as const },
];

const optimalOrder = ['q3', 'q1', 'q5', 'q2', 'q6', 'q4'];

const difficultyConfig = {
    green: { bg: 'bg-emerald-100 dark:bg-emerald-900/30', text: 'text-emerald-700 dark:text-emerald-300', border: 'border-emerald-300 dark:border-emerald-700', dot: 'bg-emerald-500', label: 'Confident' },
    amber: { bg: 'bg-amber-100 dark:bg-amber-900/30', text: 'text-amber-700 dark:text-amber-300', border: 'border-amber-300 dark:border-amber-700', dot: 'bg-amber-500', label: 'Manageable' },
    red: { bg: 'bg-rose-100 dark:bg-rose-900/30', text: 'text-rose-700 dark:text-rose-300', border: 'border-rose-300 dark:border-rose-700', dot: 'bg-rose-500', label: 'Hardest' },
};

const shuffleArray = <T,>(arr: T[]): T[] => {
    const copy = [...arr];
    for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
};

const OrderOfAttackOptimizer = () => {
    const [displayOrder, setDisplayOrder] = useState(() => shuffleArray(attackQuestions));
    const [sequence, setSequence] = useState<string[]>([]);
    const [checked, setChecked] = useState(false);

    const handleClickQuestion = (id: string) => {
        if (checked) return;
        if (sequence.includes(id)) {
            setSequence(prev => prev.filter(s => s !== id));
        } else {
            setSequence(prev => [...prev, id]);
        }
    };

    const getZone = (position: number): 'green' | 'amber' | 'red' => {
        if (position < 3) return 'green';
        if (position < 5) return 'amber';
        return 'red';
    };

    const computeScore = () => {
        let correct = 0;
        sequence.forEach((id, i) => {
            const q = attackQuestions.find(aq => aq.id === id)!;
            const zone = getZone(i);
            if (q.difficulty === zone) correct++;
        });
        return correct;
    };

    const handleCheck = () => {
        setChecked(true);
    };

    const handleReset = () => {
        setChecked(false);
        setSequence([]);
        setDisplayOrder(shuffleArray(attackQuestions));
    };

    const score = checked ? computeScore() : 0;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Order of Attack</h4>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8 text-center max-w-lg mx-auto">Sequence these 6 exam questions for maximum momentum. Click questions in the order you would attempt them.</p>

            <div className="flex flex-col md:flex-row gap-6">
                {/* Question cards */}
                <div className="flex-1 space-y-2.5">
                    <p className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">Questions</p>
                    {displayOrder.map(q => {
                        const dc = difficultyConfig[q.difficulty];
                        const selected = sequence.includes(q.id);
                        const seqNum = selected ? sequence.indexOf(q.id) + 1 : null;
                        return (
                            <MotionDiv
                                key={q.id}
                                onClick={() => handleClickQuestion(q.id)}
                                whileHover={!checked ? { scale: 1.01 } : {}}
                                whileTap={!checked ? { scale: 0.98 } : {}}
                                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                                    selected
                                        ? 'bg-zinc-100 dark:bg-zinc-700/40 border-zinc-200 dark:border-zinc-600 opacity-50'
                                        : 'bg-zinc-50 dark:bg-zinc-700/50 border-zinc-200 dark:border-zinc-600 hover:border-amber-300 dark:hover:border-amber-600'
                                } ${checked ? 'cursor-default' : ''}`}
                            >
                                <div className="flex items-center gap-3">
                                    {seqNum && (
                                        <span className="w-6 h-6 rounded-full bg-amber-500 text-white text-xs font-bold flex items-center justify-center flex-shrink-0">{seqNum}</span>
                                    )}
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-200">{q.label}</p>
                                        <div className="flex items-center gap-2 mt-1">
                                            <span className="text-xs font-bold text-zinc-400">{q.marks} marks</span>
                                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${dc.bg} ${dc.text} border ${dc.border}`}>{dc.label}</span>
                                        </div>
                                    </div>
                                </div>
                            </MotionDiv>
                        );
                    })}
                </div>

                {/* Sequence list */}
                <div className="md:w-64 flex-shrink-0">
                    <p className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">Your Sequence</p>
                    <div className="space-y-2 min-h-[120px]">
                        <AnimatePresence>
                            {sequence.map((id, i) => {
                                const q = attackQuestions.find(aq => aq.id === id)!;
                                const dc = difficultyConfig[q.difficulty];
                                const zone = getZone(i);
                                const inZone = checked && q.difficulty === zone;
                                const outZone = checked && q.difficulty !== zone;
                                return (
                                    <MotionDiv
                                        key={id}
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        className={`p-3 rounded-lg border flex items-center gap-2.5 ${
                                            inZone ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-300 dark:border-emerald-700' :
                                            outZone ? 'bg-rose-50 dark:bg-rose-900/20 border-rose-300 dark:border-rose-700' :
                                            'bg-zinc-50 dark:bg-zinc-700/50 border-zinc-200 dark:border-zinc-600'
                                        }`}
                                    >
                                        <span className={`w-6 h-6 rounded-full text-white text-xs font-bold flex items-center justify-center flex-shrink-0 ${
                                            inZone ? 'bg-emerald-500' : outZone ? 'bg-rose-500' : 'bg-amber-500'
                                        }`}>{i + 1}</span>
                                        <div className="min-w-0">
                                            <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-200 truncate">{q.label.split(':')[0]}</p>
                                            <div className="flex items-center gap-1.5">
                                                <span className={`w-1.5 h-1.5 rounded-full ${dc.dot}`} />
                                                <span className="text-[10px] text-zinc-400">{q.marks}m</span>
                                            </div>
                                        </div>
                                    </MotionDiv>
                                );
                            })}
                        </AnimatePresence>
                        {sequence.length === 0 && !checked && (
                            <p className="text-xs text-zinc-400 dark:text-zinc-500 italic text-center py-6">Click questions to build your sequence...</p>
                        )}
                    </div>

                    {/* Check / Try Again button */}
                    <div className="mt-4">
                        {!checked ? (
                            <button
                                onClick={handleCheck}
                                disabled={sequence.length < 6}
                                className={`w-full py-2.5 font-bold text-sm rounded-lg transition-all ${
                                    sequence.length === 6
                                        ? 'bg-amber-500 hover:bg-amber-600 text-white'
                                        : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
                                }`}
                            >
                                {sequence.length === 6 ? 'Check Strategy' : `Select ${6 - sequence.length} more`}
                            </button>
                        ) : (
                            <button
                                onClick={handleReset}
                                className="w-full py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm rounded-lg transition-colors"
                            >
                                Try Again
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Feedback */}
            {checked && (
                <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-8">
                    <div className="flex items-center justify-center gap-3 mb-5">
                        <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
                            <div className="text-2xl font-bold text-zinc-800 dark:text-white">{score}/6</div>
                            <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">In Optimal Zone</div>
                        </div>
                    </div>

                    <div className="p-5 rounded-xl bg-zinc-50 dark:bg-zinc-700/50 border border-zinc-200 dark:border-zinc-600 mb-5">
                        <p className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-3">Optimal Order</p>
                        <div className="space-y-1.5">
                            {optimalOrder.map((id, i) => {
                                const q = attackQuestions.find(aq => aq.id === id)!;
                                const dc = difficultyConfig[q.difficulty];
                                return (
                                    <div key={id} className="flex items-center gap-2.5">
                                        <span className="w-5 h-5 rounded-full bg-zinc-300 dark:bg-zinc-600 text-zinc-600 dark:text-zinc-300 text-[10px] font-bold flex items-center justify-center flex-shrink-0">{i + 1}</span>
                                        <span className={`w-1.5 h-1.5 rounded-full ${dc.dot}`} />
                                        <span className="text-xs text-zinc-600 dark:text-zinc-300">{q.label}</span>
                                        <span className="text-[10px] text-zinc-400">{q.marks}m</span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    <div className="p-5 rounded-xl bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-800/40">
                        <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
                            <strong className="text-zinc-800 dark:text-white">Why this order?</strong> Greens first builds confidence and banks marks early. Your brain warms up on familiar material, creating <strong>psychological momentum</strong>. Within each colour zone, tackle the highest-mark questions first to maximise early points. Save the hardest question (Red) for last — by then you are in flow state and have already secured most of your grade.
                        </p>
                    </div>
                </MotionDiv>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const ExamHallStrategiesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'knowing-vs-showing', title: 'Knowing vs. Showing It', eyebrow: '01 // The Real Problem', icon: Cpu },
    { id: 'brain-dump', title: 'The Brain Dump', eyebrow: '02 // Your First 3 Minutes', icon: ClipboardList },
    { id: 'reading-time-triage', title: 'Reading Time Triage', eyebrow: '03 // Sorting the Paper', icon: ListFilter },
    { id: 'order-of-attack', title: 'Order of Attack', eyebrow: '04 // Building Momentum', icon: PlayCircle },
    { id: 'time-budgeting', title: 'Time Budgeting', eyebrow: '05 // Spending Minutes Wisely', icon: BarChart2 },
    { id: 'staying-calm', title: 'Staying Calm Under Pressure', eyebrow: '06 // Managing Panic', icon: HeartPulse },
    { id: 'practice-drills', title: 'Practice Drills', eyebrow: '07 // Building the Habits', icon: HardHat },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Exam Hall Strategies"
      moduleSubtitle="Your Game Plan for Exam Day"
      moduleDescription={`You've done the study — now learn the practical tips that help top students turn what they know into the marks they deserve.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Own the Exam Hall"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Knowing vs. Showing It." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>You can be the smartest person in the room, have every definition memorised, and still get a bad result. The gap between what you <em>know</em> (<Highlight description="All the stuff you've actually learned and stored in your memory over months of study." theme={theme}>Competence</Highlight>) and what you can actually <em>show</em> on the day (<Highlight description="What you can actually pull out of your memory and put on paper under timed, stressful conditions." theme={theme}>Performance</Highlight>) is the whole problem. This module is about closing that gap.</p>
              <p>The exam hall is not a quiet library. It is a high-pressure environment where your brain has to juggle the questions AND manage your nerves, the clock, and everything else. All of that extra pressure creates <Highlight description="The mental drain that comes from things other than the actual question — stuff like managing your panic, watching the clock, or trying to remember a formula you half-know." theme={theme}>unnecessary mental load</Highlight> that steals the brainpower you need for the actual questions. The strategies in this module are about cutting that load so you can show what you really know.</p>
              <PersonalStory name="Ciara, Dublin" role="Leaving Cert 2024">
                <p>"I knew my stuff going into the English exam. But I panicked, spent 50 minutes on the essay question first, and ran out of time on the comprehension — the part I was actually best at. If I had sorted the paper during reading time and started with the questions I was confident on, I would have picked up way more marks. It wasn't about what I knew. It was about how I used the time."</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Brain Dump." eyebrow="Step 2" icon={ClipboardList} theme={theme}>
              <p>In the first few minutes of an exam, your stress hormones spike, which can block access to your memory. The <Highlight description="A list of key facts, quotes, and formulas you've memorised beforehand. You write it down from memory as soon as the exam starts, before you even look at the questions." theme={theme}>"Brain Dump"</Highlight> is a way to fight back. The idea is simple: get the most fragile, important information out of your head and onto paper before stress can erase it.</p>
              <p>This is not cheating — it is just <Highlight description="Moving information from your head onto paper so your brain doesn't have to hold it all at once. It frees up mental space so you can focus on actually answering questions." theme={theme}>offloading your memory onto paper</Highlight>. Your dump sheet should contain things that are easy to forget under pressure but likely to come up — key quotes, formulas, dates, acronyms. Practice writing it until you can do it in under 3 minutes without thinking.</p>
              <DumpSheetBuilder />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Reading Time Triage." eyebrow="Step 3" icon={ListFilter} theme={theme}>
              <p>Reading time is not for passively reading. It is for <Highlight description="During reading time, you quickly scan the whole paper and sort questions by how confident you are — so you know exactly where to start when writing time begins." theme={theme}>sorting the paper</Highlight>. Your goal is not to answer every question perfectly; it is to get the most marks possible with the time you have.</p>
              <p>Use a <strong>Traffic Light System</strong>: <strong>Green</strong> questions are ones you are 100% confident you can answer quickly. <strong>Amber</strong> questions are ones you know how to do but will take time or careful work. <strong>Red</strong> questions are the ones you find hardest — topics you are weak on or do not immediately understand. Your first job is to find 2-3 "Green" questions to serve as your <Highlight description="The first easy questions you tackle, no matter where they are on the paper. They build your confidence, calm your nerves, and get you into a rhythm." theme={theme}>Anchor Questions</Highlight>.</p>
              <TriageSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Order of Attack." eyebrow="Step 4" icon={PlayCircle} theme={theme}>
              <p>Starting at Question 1 is a common mistake. It hands control to the examiner, who may have put a difficult question first. Instead, think of yourself as a <Highlight description="Basically, always go for the easiest marks first. Do not waste time struggling with a hard question when there are easy ones waiting on the next page." theme={theme}>smart mark-collector</Highlight> — your job is to grab the maximum marks for the minimum effort. That means doing your "Green" questions first, no matter where they are on the paper.</p>
              <p>This builds <Highlight description="When you nail your first couple of answers, it gives you a confidence boost and gets your brain into a flow. That makes the harder questions feel more manageable when you get to them." theme={theme}>momentum</Highlight>. If you cannot figure out a question within 30 seconds (the "30-Second Rule"), skip it and move on. The good news is that your <Highlight description="Your brain keeps working on a problem in the background even after you move on. When you come back to it later, the answer often clicks into place." theme={theme}>brain keeps working on it in the background</Highlight>, so the answer often clicks when you come back to it later.</p>
              <OrderOfAttackOptimizer />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Time Budgeting." eyebrow="Step 5" icon={BarChart2} theme={theme}>
              <p>Time is the currency of the exam hall. Every minute you spend is an investment, and it needs to earn you marks. The key number is <Highlight description="A simple calculation: take the total exam time, subtract a buffer for reading and checking, then divide by the total marks. It tells you exactly how many minutes each mark is worth." theme={theme}>Minutes Per Mark (MPM)</Highlight>. This tells you exactly how long you can afford to spend on any given question.</p>
              <p>When your time for a question runs out, you need to do a <Highlight description="Forcing yourself to stop working on a question the moment its time is up, even if you are mid-sentence. It feels wrong, but it stops you wasting time on one answer while easier marks go uncollected." theme={theme}>"Hard Stop"</Highlight> and move on. This is tough because of the <Highlight description="That feeling of 'I've already spent 10 minutes on this, I can't leave it now.' But those 10 minutes are gone either way. The next 5 minutes on a fresh question will always earn you more marks than 5 more minutes on one you're stuck on." theme={theme}>sunk cost trap</Highlight> — the urge to keep going because you have already spent time on it. But the first 5 minutes on a new question will always be worth more than the last 5 minutes polishing an old one.</p>
              <MPMCalculator/>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Staying Calm Under Pressure." eyebrow="Step 6" icon={HeartPulse} theme={theme}>
              <p>When you hit a question you cannot answer, your body can go into panic mode — your heart races, your mind goes blank, and you feel like you are failing. You need a way to snap out of it. The fastest trick is <Highlight description="A simple breathing pattern: breathe in for 4 seconds, hold for 4, breathe out for 4, hold for 4. It physically calms your nervous system down in under a minute." theme={theme}>Box Breathing</Highlight>.</p>
              <p>Another tool is the <Highlight description="A quick grounding trick: name 3 things you can see, 3 sounds you can hear, and 3 things you can physically feel. It pulls your brain out of panic mode and back into the room." theme={theme}>3-3-3 Rule</Highlight> for grounding. Finally, use <Highlight description="Instead of thinking 'I'm failing,' you switch to 'This is a hard question — that's expected. I'll flag it and come back.' It turns panic into a plan." theme={theme}>reframing</Highlight> to turn panic into a planned response. Instead of "I'm failing," you think "This is a Red question. I'll skip it and come back."</p>
              <BoxBreathingVisualizer />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Practice Drills." eyebrow="Step 7" icon={HardHat} theme={theme}>
              <p>These strategies are skills, and like any skill, they need practice. After every practice test, use an <Highlight description="A simple review where you look at what went wrong and ask 'was it the content I didn't know, or the process I didn't follow?' — like misreading a question, running out of time, or doing questions in the wrong order." theme={theme}>Exam Wrapper</Highlight> to review your performance. Did your triage work? Did you stick to your time budget? Did you do the brain dump?</p>
              <p>You should also run specific drills. <strong>Triage Drills</strong>: Give yourself 5 minutes with a past paper to <em>only</em> sort questions as Green, Amber, or Red. <strong>Dump Sprints</strong>: Practice writing your brain dump until it takes less than 3 minutes. <strong>Hard Stop Drills</strong>: Do questions with a strict timer and force yourself to stop when it goes off. This builds the discipline you need to perform under pressure.</p>
              <MicroCommitment theme={theme}><p>For your next practice test, do a full Exam Wrapper analysis afterwards. Do not just check the answers — look at <em>how</em> you took the test.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamHallStrategiesModule;
