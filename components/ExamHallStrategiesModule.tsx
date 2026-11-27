/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import { BarChart2,ClipboardList,Cpu,HardHat,HeartPulse,ListFilter,PlayCircle } from 'lucide-react';
import React,{ useEffect,useId,useRef,useState } from 'react';
import { EXAM_HALL_STRATEGIES_REFERENCE_LIST } from '../data/references/examHallStrategies';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { amberTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,AnswerTick,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { AreaField,Field } from './ui/Field';

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

export const TriageSimulator = () => {
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

    // The traffic light's own dots (the same three the triage markers are drawn in); the words say the rest.
    const colorMap = { green: { label: 'Do First', dot: "bg-[var(--module-success)]" }, amber: { label: 'Do Second', dot: "bg-[var(--module-orange)]" }, red: { label: 'Do Last', dot: "bg-[var(--module-danger)]" } };

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
            <ExerciseSheet title="Triage Drill" sub={<>Reading time has started. You have <strong className="text-ink-primary">40 seconds</strong> to categorise 8 exam questions as:</>} name="TriageSimulator">
                {/* The three categories: plain words, each after its traffic-light dot (no pills) */}
                <div className="flex flex-wrap gap-x-6 gap-y-2">
                    {(['green', 'amber', 'red'] as const).map(c => (
                        <span key={c} className="inline-flex items-center gap-2 t-row text-ink-primary"><span aria-hidden="true" className={`w-2 h-2 rounded-full flex-shrink-0 ${colorMap[c].dot}`} />{colorMap[c].label}</span>
                    ))}
                </div>
                <div className="ex-actions">
                    <Button onClick={startDrill}>Start Triage</Button>
                </div>
            </ExerciseSheet>
        );
    }

    if (phase === 'done') {
        return (
            <ExerciseSheet title="Triage Results" name="TriageSimulator">
                {/* The three numbers, on the sheet under a hairline (no boxes) */}
                <div className="ex-result">
                    <div className="grid grid-cols-3 gap-4">
                        <div>
                            <p className="ex-result-name">{score}/{triageQuestions.length}</p>
                            <p className="t-meta">Correct</p>
                        </div>
                        <div>
                            <p className="ex-result-name">{Math.round(totalTime)}s</p>
                            <p className="t-meta">Total Time</p>
                        </div>
                        <div>
                            <p className="ex-result-name">{answerTimes.length > 0 ? (answerTimes.reduce((a,b) => a+b, 0) / answerTimes.length).toFixed(1) : '—'}s</p>
                            <p className="t-meta">Avg / Question</p>
                        </div>
                    </div>
                </div>
                {/* Each question, ruled like rows: its dot is the category it should have been */}
                <div className="ex-list">
                    {triageQuestions.map((q, i) => {
                        const got = choices[i];
                        const correct = got === q.correct;
                        const c = colorMap[q.correct];
                        return (
                            <div key={i}>
                                <div className="flex items-start gap-3">
                                    <span aria-hidden="true" className={`mt-2 w-2 h-2 rounded-full flex-shrink-0 ${c.dot}`} />
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-x-3 gap-y-1 flex-wrap t-meta">
                                            <span>{q.subject} · {q.marks}m</span>
                                            {correct ? (
                                                <span className="inline-flex items-center gap-1 text-ink-primary"><AnswerTick />Correct</span>
                                            ) : (
                                                <span className="text-ink-primary">You said {got ? colorMap[got as keyof typeof colorMap].label : 'nothing'} — should be {c.label}</span>
                                            )}
                                            {answerTimes[i] !== undefined && <span className="ui-readout">{answerTimes[i].toFixed(1)}s</span>}
                                        </div>
                                        <p className="t-row text-ink-primary mt-1">{q.text}</p>
                                        {!correct && <p className="t-sub mt-1">{q.reason}</p>}
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
                {score < triageQuestions.length && (
                    <AnswerLine tone="note">The goal is speed <strong>and</strong> accuracy. In the real exam, a wrong triage means wasting time on hard questions while easy marks go uncollected.</AnswerLine>
                )}
                <div className="ex-actions">
                    <Button onClick={startDrill}>Run Drill Again</Button>
                </div>
            </ExerciseSheet>
        );
    }

    const q = triageQuestions[qIndex];
    const isCorrect = showFeedback && choices[qIndex] === q.correct;
    const isWrong = showFeedback && choices[qIndex] !== q.correct;
    const timerPct = (timeLeft / 40) * 100;

    return <ExerciseSheet title="Triage Drill" name="TriageSimulator">
            {/* Where you are and the clock, in the readout */}
            <div className="flex items-center justify-between gap-3">
                <span className="ex-count ui-readout">{qIndex + 1} / {triageQuestions.length}</span>
                <span className="ui-readout" style={{ color: timeLeft <= 10 ? "var(--ink-primary)" : "var(--ink-secondary)" }}>{timeLeft}s</span>
            </div>
            {/* Timer bar: a hairline track with an ink fill */}
            <div className="w-full h-1 rounded-sm overflow-hidden" style={{ backgroundColor: "var(--hairline)" }}>
                <motion.div className="h-full" style={{ backgroundColor: timeLeft <= 10 ? "var(--ink-primary)" : "var(--ink-secondary)" }} animate={{ width: `${timerPct}%` }} transition={{ duration: 0.3 }} />
            </div>
            {/* The question: words you read, on the sheet under a hairline (no tinted card) */}
            <AnimatePresence mode="wait">
                <motion.div key={qIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
                    className="ex-block min-h-[100px]">
                    <div className="flex items-center gap-2 t-meta">
                        <span className="text-ink-primary">{q.subject}</span>
                        <span>·</span>
                        <span>{q.marks} marks</span>
                    </div>
                    <p className="ex-block-title">{q.text}</p>
                    {showFeedback && (
                        <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}>
                            <AnswerLine tone={isWrong ? 'note' : 'ok'}>
                                {isCorrect ? 'Correct! ' : `Not quite — this is "${colorMap[q.correct].label}". `}{q.reason}
                            </AnswerLine>
                        </motion.div>
                    )}
                </motion.div>
            </AnimatePresence>
            {/* Choice buttons: answers that lock once one is chosen; each keeps its traffic-light marker */}
            <AnswerGroup kind="one" chooseOnArrow={false}>
                {(['green', 'amber', 'red'] as const).map(c => {
                    const cm = colorMap[c];
                    const selected = showFeedback && choices[qIndex] === c;
                    const isAnswer = showFeedback && q.correct === c;
                    return (
                        <ChoiceTile key={c} onClick={() => handleChoice(c)} disabled={showFeedback}
                            chosen={selected}
                            data-triage-choice={c} data-selected={selected || isAnswer}
                            label={<span className="inline-flex items-center gap-3">
                                <span data-triage-choice-marker={c} aria-hidden="true" style={{ display: 'inline-block', margin: 0, flexShrink: 0 }} />
                                {cm.label}
                            </span>}
                        />
                    );
                })}
            </AnswerGroup>
            {/* Progress dots */}
            <div className="flex justify-center gap-1.5">
                {triageQuestions.map((_, i) => (
                    <span key={i} data-triage-progress={choices[i] !== null ? (choices[i] === triageQuestions[i].correct ? "correct" : "incorrect") : i === qIndex ? "current" : "pending"} role="img" aria-label={`Question ${i + 1}: ${choices[i] !== null ? (choices[i] === triageQuestions[i].correct ? "correct" : "incorrect") : i === qIndex ? "current" : "not answered"}`} />
                ))}
            </div>
        </ExerciseSheet>;
}

const MPMCalculator = () => {
    const [time, setTime] = useState(180);
    const [marks, setMarks] = useState(100);
    const [buffer, setBuffer] = useState(15);
    const mpm = (time - buffer) / marks;

    return (
        <ExerciseSheet label="Exam Skills Tool" title="Minutes-Per-Mark Calculator" name="MPMCalculator">
             <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <Field label="Total Time (mins)" type="number" value={time} onChange={e=>setTime(parseInt(e.target.value))} />
                <Field label="Total Marks" type="number" value={marks} onChange={e=>setMarks(parseInt(e.target.value))} />
                <Field label="Buffer (mins)" type="number" value={buffer} onChange={e=>setBuffer(parseInt(e.target.value))} />
             </div>
             {/* What the numbers come to, said in words under a hairline (no orange panel) */}
             <div className="ex-result">
                <p className="t-body text-ink-primary">
                    <span>Your MPM is </span>
                    <span className="ui-readout" style={{ fontSize: 21, lineHeight: '26px', color: "var(--ink-primary)" }}>{mpm.toFixed(2)}</span>
                    <span>. A 20-mark question gets </span>
                    <span className="ui-readout" style={{ fontSize: 21, lineHeight: '26px', color: "var(--ink-primary)" }}>{(mpm*20).toFixed(1)}</span>
                    <span> minutes.</span>
                </p>
             </div>
        </ExerciseSheet>
    )
}

const BoxBreathingVisualizer = () => {
    const [active, setActive] = useState(false);
    const [phase, setPhase] = useState(0);
    const [count, setCount] = useState(4);
    const [cycle, setCycle] = useState(0);
    const totalCycles = 3;

    const phases = [
      { label: 'Breathe In', color: "text-ink-primary" },
      { label: 'Hold', color: "text-ink-primary" },
      { label: 'Breathe Out', color: "text-ink-primary" },
      { label: 'Hold', color: "text-ink-primary" },
    ];

    const arcColors = ["var(--ink-primary)", "var(--ink-primary)", "var(--ink-primary)", "var(--ink-primary)"];
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
     <ExerciseSheet title="4-4-4-4 Box Breathing" sub="Feeling panicked? Run this protocol. 4 seconds per phase, 3 cycles." name="BoxBreathingVisualizer">
         {/* The breathing square: the module's own drawing, in ink on the sheet */}
         <div className="flex justify-center py-8">
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

             <div className={`absolute -top-6 left-1/2 -translate-x-1/2 t-label transition-opacity duration-300 ${active && phase === 0 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Inhale</div>
             <div className={`absolute top-1/2 -right-10 -translate-y-1/2 t-label transition-opacity duration-300 ${active && phase === 1 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Hold</div>
             <div className={`absolute -bottom-6 left-1/2 -translate-x-1/2 t-label transition-opacity duration-300 ${active && phase === 2 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Exhale</div>
             <div className={`absolute top-1/2 -left-10 -translate-y-1/2 t-label transition-opacity duration-300 ${active && phase === 3 ? "text-ink-primary opacity-100" : "text-ink-muted"}`}>Hold</div>

             <div className="absolute inset-0 flex items-center justify-center">
               <motion.div
                 animate={{
                   scale: active ? breathScale : 1,
                 }}
                 transition={{ duration: 3.8, ease: 'easeInOut' }}
                 className="w-28 h-28 rounded-full flex flex-col items-center justify-center"
                 style={{ backgroundColor: "var(--surface-paper)", border: "1.5px solid var(--outline-soft)" }}
               >
                 {active ? (
                   <>
                     <motion.p
                       key={`${phase}-${count}`}
                       initial={{ scale: 1.2, opacity: 0 }}
                       animate={{ scale: 1, opacity: 1 }}
                       className="text-3xl text-ink-primary"
                     >
                       {count}
                     </motion.p>
                     <p className={`t-meta ${phases[phase].color}`}>{phases[phase].label}</p>
                   </>
                 ) : (
                   <p className="t-meta">Ready</p>
                 )}
               </motion.div>
             </div>
           </div>
         </div>

         {active && (
           <div className="flex justify-center gap-2">
             {Array.from({ length: totalCycles }).map((_, i) => (
               <div key={i} className="w-2 h-2 rounded-full transition-colors" style={i < cycle ? { backgroundColor: "var(--ink-primary)" } : i === cycle ? { border: "1.5px solid var(--ink-primary)" } : { border: "1.5px solid var(--outline-soft)" }} />
             ))}
           </div>
         )}

         <div className="ex-actions">
           {!active ? (
             <Button onClick={handleStart}>
               {done ? 'Begin' : 'Start Again'}
             </Button>
           ) : (
             <TextButton tone="quiet" onClick={() => setActive(false)}>
               Stop
             </TextButton>
           )}
         </div>
    </ExerciseSheet>
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
    const recallTitleId = useId();

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

    const isTimerLow = (time: number, total: number) => (time / total) <= 0.33;

    if (phase === 'ready') {
        return (
            <ExerciseSheet label="Active Recall" title="Dump Sheet Drill" sub="Practice the brain dump that should be your first action in every exam." name="DumpSheetBuilder">
                {/* The three stages as plain words with their arrows (no pills) */}
                <p className="flex items-center gap-3 flex-wrap t-body text-ink-primary">
                    <span>30s to memorise</span>
                    <span className="text-ink-muted" aria-hidden="true">→</span>
                    <span>60s to recall</span>
                    <span className="text-ink-muted" aria-hidden="true">→</span>
                    <span>See your score</span>
                </p>
                <div className="ex-actions">
                    <Button onClick={startDrill}>Start Drill</Button>
                </div>
            </ExerciseSheet>
        );
    }

    if (phase === 'memorise') {
        const pct = (memoriseTime / 30) * 100;
        const low = isTimerLow(memoriseTime, 30);
        return (
            <ExerciseSheet label="Active Recall" title="Memorise These Facts" name="DumpSheetBuilder">
                {/* The clock in the readout, its bar a hairline track with an ink fill */}
                <p className="ui-readout" style={{ color: low ? "var(--ink-primary)" : "var(--ink-secondary)" }}>
                    <span style={{ fontSize: 21, lineHeight: '26px' }}>{memoriseTime}</span>
                    <span style={{ marginLeft: 2 }}>s</span>
                </p>
                <div className="overflow-hidden" style={{ height: 4, backgroundColor: "var(--hairline)", borderRadius: 2 }}>
                    <motion.div style={{ height: '100%', backgroundColor: "var(--ink-primary)" }} animate={{ width: `${pct}%` }} transition={{ duration: 0.3 }} />
                </div>
                {/* The facts: words you read, ruled like rows, each with its number in a neutral ring */}
                <div className="ex-list">
                    {dumpSheetFacts.map((fact, i) => (
                        <MotionDiv key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
                            <div className="flex items-start gap-3">
                                <span className="ex-badge">{i + 1}</span>
                                <span className="t-body text-ink-primary">{fact.text}</span>
                            </div>
                        </MotionDiv>
                    ))}
                </div>
            </ExerciseSheet>
        );
    }

    if (phase === 'recall') {
        const pct = (recallTime / 60) * 100;
        const low = isTimerLow(recallTime, 60);
        return (
            <ExerciseSheet title="Write Everything You Remember" id={recallTitleId} name="DumpSheetBuilder">
                {/* The clock in the readout, its bar a hairline track with an ink fill */}
                <p className="ui-readout" style={{ color: low ? "var(--ink-primary)" : "var(--ink-secondary)" }}>
                    <span style={{ fontSize: 21, lineHeight: '26px' }}>{recallTime}</span>
                    <span style={{ marginLeft: 2 }}>s</span>
                </p>
                <div className="overflow-hidden" style={{ height: 4, backgroundColor: "var(--hairline)", borderRadius: 2 }}>
                    <motion.div style={{ height: '100%', backgroundColor: "var(--ink-primary)" }} animate={{ width: `${pct}%` }} transition={{ duration: 0.3 }} />
                </div>
                <p className="t-sub">Don't worry about order or exact wording.</p>
                <AreaField
                    aria-labelledby={recallTitleId}
                    value={recallText}
                    onChange={e => setRecallText(e.target.value)}
                    disabled={recallTime <= 0}
                    placeholder="Start typing everything you remember..."
                    rows={8}
                    autoFocus
                />
            </ExerciseSheet>
        );
    }

    // Results phase
    const score = results.filter(Boolean).length;
    return (
        <ExerciseSheet title="Results" name="DumpSheetBuilder">
            {/* The score, in words under a hairline (no green panel) */}
            <div className="ex-result">
                <p>
                    <span className="ex-result-name">{score}</span>
                    <span className="t-sub">/{dumpSheetFacts.length} recalled</span>
                </p>
            </div>
            {/* Each fact, ruled like rows: the done ring with its tick where it was recalled, a neutral ring where not */}
            <div className="ex-list">
                {dumpSheetFacts.map((fact, i) => {
                    const recalled = results[i];
                    return (
                        <MotionDiv key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
                            <div className="flex items-start gap-3">
                                <span className={recalled ? 'ex-badge ex-badge--done' : 'ex-badge'}>
                                    {recalled ? '✓' : '✗'}
                                </span>
                                <span className="t-body text-ink-primary">{fact.text}</span>
                            </div>
                        </MotionDiv>
                    );
                })}
            </div>
            <div className="ex-block">
                <p className="ex-block-text">In the real exam, your dump sheet is a safety net — facts already on the page are safe even if stress makes them harder to recall. Do this in the first 2 minutes of every paper.</p>
            </div>
            <div className="ex-actions">
                <Button onClick={tryAgain}>Try Again</Button>
            </div>
        </ExerciseSheet>
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

// The difficulty's word, and its traffic-light dot as it was (no tinted pill behind the word).
const difficultyConfig = {
    green: { dot: "bg-[var(--module-success)]", label: 'Confident' },
    amber: { dot: "bg-[var(--module-surface)]", label: 'Manageable' },
    red: { dot: "bg-[var(--module-danger)]", label: 'Hardest' },
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
        <ExerciseSheet title="Order of Attack" sub="Sequence these 6 exam questions for maximum momentum. Click questions in the order you would attempt them." name="OrderOfAttackOptimizer">
            <div className="flex flex-col md:flex-row gap-6">
                {/* Question cards: several are chosen, in order; each chosen one shows its place in a neutral ring */}
                <div className="flex-1 flex flex-col gap-3 min-w-0">
                    <ExerciseLabel>Questions</ExerciseLabel>
                    <AnswerGroup kind="several">
                        {displayOrder.map(q => {
                            const dc = difficultyConfig[q.difficulty];
                            const selected = sequence.includes(q.id);
                            const seqNum = selected ? sequence.indexOf(q.id) + 1 : null;
                            return (
                                <ChoiceTile
                                    key={q.id}
                                    kind="several"
                                    chosen={selected}
                                    onClick={() => handleClickQuestion(q.id)}
                                    label={<span className="flex items-center gap-3">
                                        {seqNum && (
                                            <span className="ex-badge ex-badge--on">{seqNum}</span>
                                        )}
                                        <span className="min-w-0">{q.label}</span>
                                    </span>}
                                    meta={<span className="inline-flex flex-wrap items-center gap-x-3 gap-y-1">
                                        <span>{q.marks} marks</span>
                                        <span className="inline-flex items-center gap-1.5"><span aria-hidden="true" className={`w-1.5 h-1.5 rounded-full ${dc.dot}`} />{dc.label}</span>
                                    </span>}
                                />
                            );
                        })}
                    </AnswerGroup>
                </div>

                {/* Sequence list: the order so far, ruled like rows (no tinted rows) */}
                <div className="md:w-64 flex-shrink-0 flex flex-col gap-3">
                    <ExerciseLabel>Your Sequence</ExerciseLabel>
                    <div className="min-h-[120px]">
                        <div className="ex-list">
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
                                            data-zone={inZone ? 'in' : outZone ? 'out' : undefined}
                                        >
                                            <div className="flex items-center gap-3">
                                                {/* in its zone: the done ring; out of it: the neutral ring (never a red disc) */}
                                                <span className={inZone ? 'ex-badge ex-badge--done' : 'ex-badge'}>{i + 1}</span>
                                                <div className="min-w-0">
                                                    <p className="t-body text-ink-primary truncate">{q.label.split(':')[0]}</p>
                                                    <div className="flex items-center gap-1.5 t-meta">
                                                        <span aria-hidden="true" className={`w-1.5 h-1.5 rounded-full ${dc.dot}`} />
                                                        <span>{q.marks}m</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </MotionDiv>
                                    );
                                })}
                            </AnimatePresence>
                        </div>
                        {sequence.length === 0 && !checked && (
                            <p className="t-meta text-center py-6">Click questions to build your sequence...</p>
                        )}
                    </div>

                    {/* Check / Try Again button */}
                    <div>
                        {!checked ? (
                            <Button
                                block
                                onClick={handleCheck}
                                {...{ disabled: sequence.length < 6 }}
                            >
                                {sequence.length === 6 ? 'Check Strategy' : `Select ${6 - sequence.length} more`}
                            </Button>
                        ) : (
                            <Button
                                block
                                onClick={handleReset}
                            >
                                Try Again
                            </Button>
                        )}
                    </div>
                </div>
            </div>

            {/* Feedback: words you read, held by hairlines (no boxes) */}
            {checked && (
                <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="ex-stack">
                    <div className="ex-result">
                        <p className="ex-result-name">{score}/6</p>
                        <p className="t-meta">In Optimal Zone</p>
                    </div>

                    <div className="ex-block">
                        <ExerciseLabel>Optimal Order</ExerciseLabel>
                        <div className="flex flex-col gap-2">
                            {optimalOrder.map((id, i) => {
                                const q = attackQuestions.find(aq => aq.id === id)!;
                                const dc = difficultyConfig[q.difficulty];
                                return (
                                    <div key={id} className="flex items-center gap-2.5">
                                        <span className="ex-badge">{i + 1}</span>
                                        <span aria-hidden="true" className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${dc.dot}`} />
                                        <span className="t-sub text-ink-primary">{q.label}</span>
                                        <span className="t-meta">{q.marks}m</span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    <div className="ex-block">
                        <p className="ex-block-text text-ink-primary">
                            <strong>Why this order?</strong> Greens first builds confidence and banks marks early. Your brain warms up on familiar material, creating <strong>psychological momentum</strong>. Within each colour zone, tackle the highest-mark questions first to maximise early points. Save the hardest question (Red) for last — by then you are in flow state and have already secured most of your grade.
                        </p>
                    </div>
                </MotionDiv>
            )}
        </ExerciseSheet>
    );
};

// --- MODULE COMPONENT ---
const ExamHallStrategiesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
      references={EXAM_HALL_STRATEGIES_REFERENCE_LIST}
      finishButtonText="Own the Exam Hall"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Knowing vs. Showing It." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <p>Knowing the material is not enough. You need strategies to show it under pressure. Exam stress, time pressure, and nerves steal brainpower from the actual questions.<Cite n={1} /> This module gives you the tools to close that gap.</p>
              ) : (
                <>
                  <p>You can be the smartest person in the room, have every definition memorised, and still get a bad result. The gap between what you <em>know</em> (<Highlight description="All the stuff you've actually learned and stored in your memory over months of study." theme={theme}>Competence</Highlight>) and what you can actually <em>show</em> on the day (<Highlight description="What you can actually pull out of your memory and put on paper under timed, stressful conditions." theme={theme}>Performance</Highlight>) is the whole problem. This module is about closing that gap.</p>
                  <p>The exam hall is not a quiet library. It is a high-pressure environment where your brain has to juggle the questions AND manage your nerves, the clock, and everything else. All of that extra pressure creates <Highlight description="The mental drain that comes from things other than the actual question — stuff like managing your panic, watching the clock, or trying to remember a formula you half-know." theme={theme}>unnecessary mental load</Highlight> that steals the brainpower you need for the actual questions.<Cite n={1} /> The strategies in this module are about cutting that load so you can show what you really know.</p>
                  <PersonalStory name="Ciara, Dublin" role="Senior cycle" junior={{ name: 'Ciara, Dublin', role: '3rd Year', children: (
                    <p>"I knew my stuff going into my English test. But I panicked, spent ages on the first big question, and ran out of time on the part I was actually best at. If I had planned my time and started with the questions I was confident on, I would have picked up way more marks. It wasn't about what I knew. It was about how I used the time."</p>
                  ) }}>
                    <p>"I knew my stuff going into the English exam. But I panicked, spent 50 minutes on the essay question first, and ran out of time on the comprehension — the part I was actually best at. If I had sorted the paper during reading time and started with the questions I was confident on, I would have picked up way more marks. It wasn't about what I knew. It was about how I used the time."</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Brain Dump." eyebrow="Step 2" icon={ClipboardList} theme={theme}>
              {essentials ? (
                <p>In the first 3 minutes of every exam, write down your most fragile facts: key quotes, formulas, dates. Get them on paper before stress can erase them.<Cite n={1} /> This is not cheating. It frees your brain to focus on the questions, and writing out your exam worries has been shown to lift performance.<Cite n={2} /> Practice until you can do it in under 3 minutes.</p>
              ) : (
                <>
                  <p>In the first few minutes of an exam, your stress hormones spike, which can block access to your memory.<Cite n={1} /> The <Highlight description="A list of key facts, quotes, and formulas you've memorised beforehand. You write it down from memory as soon as the exam starts, before you even look at the questions." theme={theme}>"Brain Dump"</Highlight> is a way to fight back. The idea is simple: get the most fragile, important information out of your head and onto paper before stress can erase it.</p>
                  <p>This is not cheating — it is just <Highlight description="Moving information from your head onto paper so your brain doesn't have to hold it all at once. It frees up mental space so you can focus on actually answering questions." theme={theme}>offloading your memory onto paper</Highlight>. In fact, students who spend a few minutes writing out their exam worries beforehand tend to score higher under pressure.<Cite n={2} /> Your dump sheet should contain things that are easy to forget under pressure but likely to come up — key quotes, formulas, dates, acronyms. Practice writing it until you can do it in under 3 minutes without thinking.</p>
                </>
              )}
              <DumpSheetBuilder />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Reading Time Triage." eyebrow="Step 3" icon={ListFilter} theme={theme}>
              {essentials ? (
                <p>During reading time, sort every question as Green (confident), Amber (doable), or Red (hardest). Find 2-3 Green questions to start with. Your goal is maximum marks for the time you have. Try the triage drill below.</p>
              ) : (
                <>
                  <p>Reading time is not for passively reading. It is for <Highlight description="During reading time, you quickly scan the whole paper and sort questions by how confident you are — so you know exactly where to start when writing time begins." theme={theme}>sorting the paper</Highlight>. Your goal is not to answer every question perfectly; it is to get the most marks possible with the time you have.</p>
                  <p>Use a <strong>Traffic Light System</strong>: <strong>Green</strong> questions are ones you are 100% confident you can answer quickly. <strong>Amber</strong> questions are ones you know how to do but will take time or careful work. <strong>Red</strong> questions are the ones you find hardest — topics you are weak on or do not immediately understand. Your first job is to find 2-3 "Green" questions to serve as your <Highlight description="The first easy questions you tackle, no matter where they are on the paper. They build your confidence, calm your nerves, and get you into a rhythm." theme={theme}>Anchor Questions</Highlight>.</p>
                </>
              )}
              <TriageSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Order of Attack." eyebrow="Step 4" icon={PlayCircle} theme={theme}>
              {essentials ? (
                <p>Do not start at Question 1. Do your Green questions first. This builds momentum and confidence. If you are stuck for 30 seconds, skip and move on — stepping away for a bit can sometimes help.<Cite n={3} /> Try the optimizer below.</p>
              ) : (
                <>
                  <p>Starting at Question 1 is a common mistake. It hands control to the examiner, who may have put a difficult question first. Instead, think of yourself as a <Highlight description="Basically, always go for the easiest marks first. Do not waste time struggling with a hard question when there are easy ones waiting on the next page." theme={theme}>smart mark-collector</Highlight> — your job is to grab the maximum marks for the minimum effort. That means doing your "Green" questions first, no matter where they are on the paper.</p>
                  <p>This builds <Highlight description="When you nail your first couple of answers, it gives you a confidence boost and gets your brain into a flow. That makes the harder questions feel more manageable when you get to them." theme={theme}>momentum</Highlight>. If you cannot figure out a question within 30 seconds (the "30-Second Rule"), skip it and move on. The good news is that <Highlight description="Taking a break from a stubborn problem can sometimes help — people often find the answer comes a little more easily when they return to it later." theme={theme}>stepping away can sometimes help</Highlight>: taking a break before you return to a stubborn question may let the answer come more easily.<Cite n={3} /></p>
                </>
              )}
              <OrderOfAttackOptimizer />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Time Budgeting." eyebrow="Step 5" icon={BarChart2} theme={theme}>
              {essentials ? (
                <p>Calculate your Minutes Per Mark. This tells you exactly how long each question deserves. When time runs out, do a hard stop and move on. The first 5 minutes on a new question earn more marks than the last 5 on a stuck one.</p>
              ) : (
                <>
                  <p>Time is the currency of the exam hall. Every minute you spend is an investment, and it needs to earn you marks. The key number is <Highlight description="A simple calculation: take the total exam time, subtract a buffer for reading and checking, then divide by the total marks. It tells you exactly how many minutes each mark is worth." theme={theme}>Minutes Per Mark (MPM)</Highlight>. This tells you exactly how long you can afford to spend on any given question.</p>
                  <p>When your time for a question runs out, you need to do a <Highlight description="Forcing yourself to stop working on a question the moment its time is up, even if you are mid-sentence. It feels wrong, but it stops you wasting time on one answer while easier marks go uncollected." theme={theme}>"Hard Stop"</Highlight> and move on. This is tough because of the <Highlight description="That feeling of 'I've already spent 10 minutes on this, I can't leave it now.' But those 10 minutes are gone either way. The next 5 minutes on a fresh question will always earn you more marks than 5 more minutes on one you're stuck on." theme={theme}>sunk cost trap</Highlight> — the urge to keep going because you have already spent time on it. But the first 5 minutes on a new question will always be worth more than the last 5 minutes polishing an old one.</p>
                </>
              )}
              <MPMCalculator/>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Staying Calm Under Pressure." eyebrow="Step 6" icon={HeartPulse} theme={theme}>
              {essentials ? (
                <p>If you panic: use a slow, structured breathing pattern like Box Breathing (4 in, hold 4, out 4, hold 4) to settle your nervous system.<Cite n={4} /> Then the 3-3-3 Rule: name 3 things you see, hear, and feel. Reframe: "This is a Red question. I will skip it and come back." Practice below.</p>
              ) : (
                <>
                  <p>When you hit a question you cannot answer, your body can go into panic mode — your heart races, your mind goes blank, and you feel like you are failing. You need a way to steady yourself. One reliable tool is slow, structured breathing — like <Highlight description="A simple breathing pattern: breathe in for 4 seconds, hold for 4, breathe out for 4, hold for 4. Slow, structured breathing like this helps settle your nervous system." theme={theme}>Box Breathing</Highlight>.<Cite n={4} /></p>
                  <p>Another tool is the <Highlight description="A quick grounding trick: name 3 things you can see, 3 sounds you can hear, and 3 things you can physically feel. It pulls your brain out of panic mode and back into the room." theme={theme}>3-3-3 Rule</Highlight> for grounding. Finally, use <Highlight description="Instead of thinking 'I'm failing,' you switch to 'This is a hard question — that's expected. I'll flag it and come back.' It turns panic into a plan." theme={theme}>reframing</Highlight> to turn panic into a planned response. Instead of "I'm failing," you think "This is a Red question. I'll skip it and come back."</p>
                </>
              )}
              <BoxBreathingVisualizer />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Practice Drills." eyebrow="Step 7" icon={HardHat} theme={theme}>
              {essentials ? (
                <p>Practice these skills. After each practice test, review your process, not just answers. Run triage drills (sort a paper in 5 minutes), dump sprints (brain dump under 3 minutes), and hard stop drills (strict timer, force yourself to move on).</p>
              ) : (
                <>
                  <p>These strategies are skills, and like any skill, they need practice. After every practice test, use an <Highlight description="A simple review where you look at what went wrong and ask 'was it the content I didn't know, or the process I didn't follow?' — like misreading a question, running out of time, or doing questions in the wrong order." theme={theme}>Exam Wrapper</Highlight> to review your performance. Did your triage work? Did you stick to your time budget? Did you do the brain dump?</p>
                  <p>You should also run specific drills. <strong>Triage Drills</strong>: Give yourself 5 minutes with a past paper to <em>only</em> sort questions as Green, Amber, or Red. <strong>Dump Sprints</strong>: Practice writing your brain dump until it takes less than 3 minutes. <strong>Hard Stop Drills</strong>: Do questions with a strict timer and force yourself to stop when it goes off. This builds the discipline you need to perform under pressure.</p>
                </>
              )}
              <MicroCommitment theme={theme}><p>For your next practice test, do a full Exam Wrapper analysis afterwards. Do not just check the answers — look at <em>how</em> you took the test.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamHallStrategiesModule;
