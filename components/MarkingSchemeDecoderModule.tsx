/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Eye, Layers, FileSearch, Key, Shield, PenTool, Target } from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory, ConceptCardGrid, GlossaryGrid } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---

// Mark Type Classifier
const classifierItems = [
  { text: '"Any relevant point — 2 marks"', correct: 'attempt' as const, explanation: 'This awards marks for any reasonable attempt, even if it\'s not the ideal answer.' },
  { text: '"Correct substitution into formula — 3 marks"', correct: 'method' as const, explanation: 'This rewards showing the right approach. Even if you calculate wrong, you get these 3 marks.' },
  { text: '"Final answer: 42.5 — 2 marks"', correct: 'answer' as const, explanation: 'These marks are only for the exact correct answer.' },
  { text: '"Diagram with labels — 4 marks"', correct: 'method' as const, explanation: 'Drawing and labelling shows your method/understanding, even before you solve anything.' },
  { text: '"States any valid hypothesis — 2 marks"', correct: 'attempt' as const, explanation: 'Any reasonable hypothesis earns these marks. The examiner just wants to see you tried.' },
  { text: '"Correct to 2 decimal places — 1 mark"', correct: 'answer' as const, explanation: 'This is strictly for the precise final answer in the right format.' },
];

const markTypeColors = {
  attempt: { bg: 'bg-emerald-100 dark:bg-emerald-900/30', border: 'border-emerald-300 dark:border-emerald-700', text: 'text-emerald-700 dark:text-emerald-300', dot: 'bg-emerald-500', label: 'Attempt' },
  method: { bg: 'bg-amber-100 dark:bg-amber-900/30', border: 'border-amber-300 dark:border-amber-700', text: 'text-amber-700 dark:text-amber-300', dot: 'bg-amber-500', label: 'Method' },
  answer: { bg: 'bg-rose-100 dark:bg-rose-900/30', border: 'border-rose-300 dark:border-rose-700', text: 'text-rose-700 dark:text-rose-300', dot: 'bg-rose-500', label: 'Answer' },
};

const MarkTypeClassifier = () => {
  const [phase, setPhase] = useState<'ready' | 'drill' | 'done'>('ready');
  const [qIndex, setQIndex] = useState(0);
  const [choices, setChoices] = useState<(string | null)[]>(Array(classifierItems.length).fill(null));
  const [showFeedback, setShowFeedback] = useState(false);
  const timerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  React.useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const startDrill = () => {
    setPhase('drill');
    setQIndex(0);
    setChoices(Array(classifierItems.length).fill(null));
    setShowFeedback(false);
  };

  const handleChoice = (choice: string) => {
    if (showFeedback) return;
    const newChoices = [...choices];
    newChoices[qIndex] = choice;
    setChoices(newChoices);
    setShowFeedback(true);
    timerRef.current = setTimeout(() => {
      setShowFeedback(false);
      if (qIndex + 1 >= classifierItems.length) {
        setPhase('done');
      } else {
        setQIndex(q => q + 1);
      }
    }, 2200);
  };

  const score = choices.filter((c, i) => c === classifierItems[i].correct).length;

  if (phase === 'ready') {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white">Mark Type Classifier</h4>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-2 max-w-md mx-auto">Read each marking scheme extract and classify it as one of three mark types:</p>
        <div className="flex justify-center gap-3 mb-6">
          {(['attempt', 'method', 'answer'] as const).map(c => (
            <span key={c} className={`px-3 py-1 rounded-full text-xs font-bold ${markTypeColors[c].bg} ${markTypeColors[c].text} border ${markTypeColors[c].border}`}>{markTypeColors[c].label}</span>
          ))}
        </div>
        <button onClick={startDrill} className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">Start Classifying</button>
      </div>
    );
  }

  if (phase === 'done') {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Classification Results</h4>
        <div className="flex justify-center my-5">
          <div className="text-center px-5 py-3 rounded-xl bg-zinc-100 dark:bg-zinc-700">
            <div className="text-2xl font-bold text-zinc-800 dark:text-white">{score}/{classifierItems.length}</div>
            <div className="text-xs font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">Correct</div>
          </div>
        </div>
        <div className="space-y-2.5 mb-6">
          {classifierItems.map((q, i) => {
            const got = choices[i];
            const correct = got === q.correct;
            const c = markTypeColors[q.correct];
            return (
              <div key={i} className={`p-3 rounded-lg border ${correct ? `${c.bg} ${c.border}` : 'bg-zinc-50 dark:bg-zinc-700/50 border-zinc-200 dark:border-zinc-600'}`}>
                <div className="flex items-start gap-2.5">
                  <span className={`mt-1 w-2 h-2 rounded-full flex-shrink-0 ${c.dot}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-xs font-bold text-zinc-400">{c.label} marks</span>
                      {correct ? (
                        <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">Correct</span>
                      ) : (
                        <span className="text-xs font-bold text-rose-600 dark:text-rose-400">You said {got ? markTypeColors[got as keyof typeof markTypeColors].label : 'nothing'} — should be {c.label}</span>
                      )}
                    </div>
                    <p className="text-sm text-zinc-600 dark:text-zinc-300 mt-0.5 font-mono">{q.text}</p>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 italic">{q.explanation}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        {score < classifierItems.length && (
          <p className="text-sm text-zinc-500 dark:text-zinc-400 text-center mb-4 italic">Understanding mark types helps you know what to write even when you are unsure of the answer.</p>
        )}
        <div className="text-center">
          <button onClick={startDrill} className="px-5 py-2.5 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">Try Again</button>
        </div>
      </div>
    );
  }

  const q = classifierItems[qIndex];
  const isCorrect = showFeedback && choices[qIndex] === q.correct;
  const isWrong = showFeedback && choices[qIndex] !== q.correct;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <div className="flex items-center justify-between mb-4">
        <h4 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white">Mark Type Classifier</h4>
        <span className="text-xs font-bold text-zinc-400">{qIndex + 1} / {classifierItems.length}</span>
      </div>
      {/* Question card */}
      <AnimatePresence mode="wait">
        <motion.div key={qIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
          className={`p-5 rounded-xl border min-h-[100px] flex flex-col justify-center mb-5 transition-colors ${
            isCorrect ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-300 dark:border-emerald-700' :
            isWrong ? 'bg-rose-50 dark:bg-rose-900/30 border-rose-300 dark:border-rose-700' :
            'bg-zinc-50 dark:bg-zinc-700/50 border-zinc-200 dark:border-zinc-600'
          }`}>
          <p className="font-semibold text-zinc-700 dark:text-zinc-200 text-sm font-mono">{q.text}</p>
          {showFeedback && (
            <motion.p initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className={`text-xs mt-3 italic ${isCorrect ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
              {isCorrect ? 'Correct! ' : `Not quite — this is "${markTypeColors[q.correct].label}" marks. `}{q.explanation}
            </motion.p>
          )}
        </motion.div>
      </AnimatePresence>
      {/* Choice buttons */}
      <div className="grid grid-cols-3 gap-3">
        {(['attempt', 'method', 'answer'] as const).map(c => {
          const cm = markTypeColors[c];
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
        {classifierItems.map((_, i) => (
          <div key={i} className={`w-2 h-2 rounded-full transition-colors ${
            i < qIndex ? (choices[i] === classifierItems[i].correct ? 'bg-emerald-500' : 'bg-rose-500') :
            i === qIndex ? 'bg-red-500' : 'bg-zinc-200 dark:bg-zinc-600'
          }`} />
        ))}
      </div>
    </div>
  );
};

// Scheme Decoder
const schemeExtracts = [
  {
    text: 'Q4(b) Explain two factors affecting the rate of photosynthesis. (2 x 6 marks)',
    annotations: [
      { term: '2 x', start: 60, end: 63, explanation: 'You need exactly 2 factors. Writing 3 won\'t earn extra marks but wastes time.' },
      { term: '6 marks', start: 64, end: 71, explanation: '6 marks per factor = 3 for naming it + 3 for explaining. Always name AND explain.' },
      { term: 'Explain', start: 7, end: 14, explanation: 'Not "list" or "name" — you need to say HOW or WHY, not just WHAT.' },
    ]
  },
  {
    text: 'Q2(a) Discuss the impact of the Zimmermann Telegram on US foreign policy. (30 marks — any 3 points fully developed)',
    annotations: [
      { term: 'Discuss', start: 7, end: 14, explanation: '"Discuss" means weigh up different angles. A one-sided answer loses marks.' },
      { term: '30 marks', start: 76, end: 84, explanation: '30 marks for 3 points = 10 marks each. Spend equal time on all 3.' },
      { term: 'any 3 points', start: 87, end: 99, explanation: 'You choose which 3. Pick the ones you know best — there is no "correct" set.' },
    ]
  },
  {
    text: 'Q6 Solve the following equation. Show all work. Fully correct: 10 marks; partially correct (with work shown): 5 marks; attempt: 2 marks.',
    annotations: [
      { term: 'Show all work', start: 32, end: 45, explanation: '"Show all work" means every step earns marks independently. Never skip steps.' },
      { term: 'partially correct', start: 65, end: 82, explanation: 'Even a half-right answer with work shown gets 5 out of 10. That\'s huge.' },
      { term: 'attempt: 2 marks', start: 103, end: 120, explanation: 'Just writing the formula or starting the process earns 2 free marks. Never leave it blank.' },
    ]
  },
  {
    text: 'Q3(c) Define osmosis in your own words or equivalent. (9 marks — PCLM)',
    annotations: [
      { term: 'or equivalent', start: 40, end: 53, explanation: 'Your phrasing doesn\'t need to match the textbook exactly. The examiner is flexible.' },
      { term: '9 marks', start: 56, end: 63, explanation: '9 marks for a definition means they want detail — not just one sentence.' },
      { term: 'PCLM', start: 66, end: 70, explanation: 'Partial Credit Level Marks = you get marks for each correct element. Even 2 right keywords out of 5 earns marks.' },
    ]
  },
];

const SchemeDecoder = () => {
  const [activeExtract, setActiveExtract] = useState(0);
  const [activeAnnotation, setActiveAnnotation] = useState<number | null>(null);

  const extract = schemeExtracts[activeExtract];
  const _decodedCount = activeAnnotation !== null ? 1 : 0;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <div className="text-center mb-6">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Exam Skills Tool</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 22, color: '#1a1a1a' }}>Scheme Decoder</h4>
        <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Click the highlighted terms to decode what they really mean.</p>
      </div>

      {/* Extract tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {schemeExtracts.map((_, i) => (
          <button key={i} onClick={() => { setActiveExtract(i); setActiveAnnotation(null); }}
            style={{
              backgroundColor: activeExtract === i ? '#2A7D6F' : '#FFFFFF',
              border: activeExtract === i ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
              borderRadius: 20,
              padding: '8px 18px',
              fontSize: 13,
              fontWeight: 600,
              color: activeExtract === i ? '#FFFFFF' : '#7a7068',
              whiteSpace: 'nowrap' as const,
              cursor: 'pointer',
            }}>
            Extract {i + 1}
          </button>
        ))}
      </div>

      {/* Extract card */}
      <div className="bg-white dark:bg-zinc-900 mb-4" style={{ border: '2px solid #1a1a1a', borderRadius: 14, padding: '20px 24px' }}>
        <span className="inline-block mb-3" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', backgroundColor: '#f0ece6', color: '#9e9186', border: '1px solid #d0cdc8', borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Exam Question Extract</span>
        <p style={{ fontSize: 15, color: '#1a1a1a', lineHeight: 1.7 }}>
          {(() => {
            const sortedAnnotations = [...extract.annotations].sort((a, b) => a.start - b.start);
            const parts: React.ReactNode[] = [];
            let lastEnd = 0;
            sortedAnnotations.forEach((ann, i) => {
              if (ann.start > lastEnd) {
                parts.push(<span key={`t-${i}`}>{extract.text.slice(lastEnd, ann.start)}</span>);
              }
              const isClicked = activeAnnotation === i;
              parts.push(
                <button key={`a-${i}`} onClick={() => setActiveAnnotation(activeAnnotation === i ? null : i)}
                  style={{
                    backgroundColor: isClicked ? '#2A7D6F' : '#e8f5f2',
                    color: isClicked ? '#FFFFFF' : '#1a6358',
                    fontWeight: 700,
                    borderRadius: 4,
                    padding: '1px 6px',
                    cursor: 'pointer',
                    borderBottom: isClicked ? 'none' : '2px solid #2A7D6F',
                    transition: 'all 0.2s',
                  }}>
                  {ann.term}
                </button>
              );
              lastEnd = ann.end;
            });
            if (lastEnd < extract.text.length) {
              parts.push(<span key="end">{extract.text.slice(lastEnd)}</span>);
            }
            return parts;
          })()}
        </p>
      </div>

      {/* Decode panel */}
      <AnimatePresence mode="wait">
        {activeAnnotation !== null && (
          <motion.div key={activeAnnotation} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 8 }}
            style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px', marginTop: 12 }}>
            <p className="font-serif font-semibold" style={{ fontSize: 15, color: '#1a6358', marginBottom: 4 }}>{extract.annotations[activeAnnotation].term}</p>
            <p className="italic" style={{ fontSize: 14, color: '#5a5550' }}>{extract.annotations[activeAnnotation].explanation}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Answer Upgrader
const upgradeExamples = [
  {
    subject: 'Biology',
    question: 'What is osmosis?',
    before: { text: 'Water moves from where there\'s lots of it to where there\'s less through a membrane.', marks: 4 },
    after: { text: 'Osmosis is the movement of water molecules from a region of high water concentration to a region of low water concentration across a selectively permeable membrane.', marks: 9 },
    keywords: ['water molecules', 'high water concentration', 'low water concentration', 'selectively permeable membrane'],
    maxMarks: 9,
  },
  {
    subject: 'Business',
    question: 'Explain one advantage of a sole trader.',
    before: { text: 'You get to keep all the money and make all the decisions yourself.', marks: 5 },
    after: { text: 'The sole trader retains all profits generated by the business and has complete autonomy over decision-making without consulting partners or shareholders.', marks: 10 },
    keywords: ['retains all profits', 'complete autonomy', 'decision-making'],
    maxMarks: 10,
  },
  {
    subject: 'History',
    question: 'Why did the USA enter World War I?',
    before: { text: 'Germany was sinking their ships and they found out about a secret message to Mexico.', marks: 6 },
    after: { text: 'The USA entered WWI due to unrestricted submarine warfare by Germany, the interception of the Zimmermann Telegram proposing a German-Mexican alliance, and growing economic ties with the Allied Powers.', marks: 12 },
    keywords: ['unrestricted submarine warfare', 'Zimmermann Telegram', 'German-Mexican alliance', 'economic ties'],
    maxMarks: 12,
  },
];

const AnswerUpgrader = () => {
  const [activeExample, setActiveExample] = useState(0);
  const [showAfter, setShowAfter] = useState(false);
  const [showKeywords, setShowKeywords] = useState(false);

  const ex = upgradeExamples[activeExample];

  const highlightKeywords = (text: string, keywords: string[]) => {
    const result = text;
    const parts: React.ReactNode[] = [];
    let remaining = result;
    let keyIndex = 0;

    for (const keyword of keywords) {
      const idx = remaining.toLowerCase().indexOf(keyword.toLowerCase());
      if (idx !== -1) {
        if (idx > 0) {
          parts.push(<span key={`t-${keyIndex}`}>{remaining.slice(0, idx)}</span>);
        }
        parts.push(
          <span key={`k-${keyIndex}`} className="px-1 py-0.5 rounded bg-teal-100 dark:bg-teal-900/50 text-teal-700 dark:text-teal-300 font-bold">
            {remaining.slice(idx, idx + keyword.length)}
          </span>
        );
        remaining = remaining.slice(idx + keyword.length);
        keyIndex++;
      }
    }
    if (remaining) {
      parts.push(<span key="end">{remaining}</span>);
    }
    return parts;
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Answer Upgrader</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-6">See how adding the right keywords transforms marks.</p>

      {/* Subject tabs */}
      <div className="flex gap-2 mb-6 justify-center">
        {upgradeExamples.map((e, i) => (
          <button key={i} onClick={() => { setActiveExample(i); setShowAfter(false); setShowKeywords(false); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
              activeExample === i ? 'bg-red-500 text-white' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-600'
            }`}>
            {e.subject}
          </button>
        ))}
      </div>

      {/* Question */}
      <div className="text-center mb-4">
        <span className="text-xs font-bold uppercase tracking-wider text-zinc-400">{ex.subject}</span>
        <p className="font-serif text-lg font-semibold text-zinc-800 dark:text-white mt-1">{ex.question}</p>
      </div>

      {/* Before / After cards */}
      <div className="grid md:grid-cols-2 gap-4 mb-5">
        {/* Before */}
        <div className="p-5 rounded-xl border border-zinc-200 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-700/50">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-zinc-400">Before</span>
            <span className="text-xs font-bold text-rose-500">{ex.before.marks}/{ex.maxMarks} marks</span>
          </div>
          <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed italic">{ex.before.text}</p>
          {/* Mark bar */}
          <div className="mt-3 w-full h-2 bg-zinc-200 dark:bg-zinc-600 rounded-full overflow-hidden">
            <div className="h-full bg-rose-400 rounded-full transition-all duration-700" style={{ width: `${(ex.before.marks / ex.maxMarks) * 100}%` }} />
          </div>
        </div>

        {/* After */}
        <div className={`p-5 rounded-xl border transition-all duration-300 ${showAfter ? 'border-teal-300 dark:border-teal-700 bg-teal-50/50 dark:bg-teal-950/20' : 'border-zinc-200 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-700/50'}`}>
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-zinc-400">After</span>
            {showAfter && <span className="text-xs font-bold text-teal-600 dark:text-teal-400">{ex.after.marks}/{ex.maxMarks} marks</span>}
          </div>
          {showAfter ? (
            <>
              <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
                {showKeywords ? highlightKeywords(ex.after.text, ex.keywords) : ex.after.text}
              </p>
              <div className="mt-3 w-full h-2 bg-zinc-200 dark:bg-zinc-600 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-teal-500 rounded-full"
                  initial={{ width: `${(ex.before.marks / ex.maxMarks) * 100}%` }}
                  animate={{ width: `${(ex.after.marks / ex.maxMarks) * 100}%` }}
                  transition={{ duration: 0.8, ease: 'easeOut' }}
                />
              </div>
            </>
          ) : (
            <div className="flex items-center justify-center h-16">
              <button onClick={() => setShowAfter(true)}
                className="px-5 py-2 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-lg transition-colors">
                Show Upgraded Answer
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Show Keywords toggle */}
      {showAfter && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex justify-center mb-4">
            <button onClick={() => setShowKeywords(!showKeywords)}
              className={`px-4 py-2 rounded-lg text-sm font-bold transition-colors ${
                showKeywords ? 'bg-teal-500 text-white' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-600'
              }`}>
              {showKeywords ? 'Hide Keywords' : 'Show Keywords'}
            </button>
          </div>
          {showKeywords && (
            <div className="flex flex-wrap gap-2 justify-center">
              {ex.keywords.map((kw, i) => (
                <span key={i} className="px-2.5 py-1 rounded-full text-xs font-bold bg-teal-100 dark:bg-teal-900/40 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-700">
                  {kw}
                </span>
              ))}
            </div>
          )}
        </MotionDiv>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const MarkingSchemeDecoderModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'examiners-secret', title: "The Examiner's Secret", eyebrow: '01 // The Mindset', icon: Eye },
    { id: 'three-types-of-marks', title: 'The Three Types of Marks', eyebrow: '02 // The System', icon: Layers },
    { id: 'reading-a-real-scheme', title: 'Reading a Real Marking Scheme', eyebrow: '03 // The Decode', icon: FileSearch },
    { id: 'keyword-effect', title: 'The Keyword Effect', eyebrow: '04 // The Language', icon: Key },
    { id: 'attempt-marks', title: 'Attempt Marks: The Free Points', eyebrow: '05 // The Safety Net', icon: Shield },
    { id: 'presentation-protocol', title: 'The Presentation Protocol', eyebrow: '06 // The Polish', icon: PenTool },
    { id: 'decoding-action-plan', title: 'Your Decoding Action Plan', eyebrow: '07 // The Plan', icon: Target },
  ];

  return (
    <ModuleLayout
      moduleNumber="EZ07"
      moduleTitle="The Marking Scheme Decoder"
      moduleSubtitle="Turn the Examiner's Playbook Into Your Advantage"
      moduleDescription="Every SEC marking scheme follows patterns. Once you see them, you'll know exactly how to write answers that collect every available mark."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Decode Every Exam"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Examiner's Secret." eyebrow="01 // The Mindset" icon={Eye} theme={theme}>
              <p>Here is something most students never figure out: examiners <em>want</em> to give you marks. The marking scheme is their checklist. They are looking for reasons to <Highlight description="SEC examiners use positive marking. They scan your answer looking for things that deserve marks, not things to penalise. Every correct point you make earns credit." theme={theme}>award marks</Highlight>, not reasons to take them away.</p>
              <p>This changes everything. It means the examiner is on your side. The marking scheme is not a secret document locked away in a vault — it is published on <strong>examinations.ie</strong> every year, for every subject, for every paper. It is literally the <Highlight description="The marking scheme tells you exactly what the examiner will look for in your answer. It is the closest thing to an answer key you will ever get before the exam." theme={theme}>answer key published BEFORE the exam</Highlight>. And yet most students never read one.</p>
              <p>The students who <em>do</em> read marking schemes instantly understand what examiners want. They stop guessing and start giving examiners exactly what they are looking for. That is the edge this module will give you.</p>
              <Highlight description="Examiners use positive marking — they mark what is RIGHT in your answer, not what is wrong. Every relevant point earns credit. A blank answer is the only answer that gets zero." theme={theme}>Positive marking</Highlight> means examiners mark what is right, not what is wrong. If you write three correct points and two incorrect ones, you get marks for the three correct points. The incorrect ones are simply ignored.
              <PersonalStory name="Aoife, Leaving Cert 2024, Galway">
                <p>"I never looked at a marking scheme until my teacher made us go through one in class. I was shocked. I'd been writing these long, detailed answers for Biology, thinking more was better. But the scheme showed that each question only wanted 3 or 4 specific points. I was spending 15 minutes on answers that needed 5 minutes. Once I started studying the schemes, my grades went up a full grade in two subjects — not because I knew more, but because I finally understood what they were actually asking for."</p>
              </PersonalStory>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The Three Types of Marks." eyebrow="02 // The System" icon={Layers} theme={theme}>
              <p>Every mark in the Leaving Cert falls into one of three categories. Once you understand this system, you will never look at an exam question the same way again.</p>
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Attempt Marks", description: "1–3 marks awarded just for trying. Write anything relevant and you get these — even if your answer is incomplete or partly wrong, the examiner awards attempt marks for showing you engaged with the question." },
                  { number: 2, term: "Method Marks", description: "2–5 marks awarded for showing the right approach, even if your final answer is wrong. Using the right formula, setting up the equation correctly, or showing a logical chain of reasoning all earn method marks regardless of where you end up.", highlight: true },
                  { number: 3, term: "Answer Marks", description: "2–6 marks awarded for the correct final answer. These are the only marks that require you to actually get it right — but you can still earn attempt and method marks without them." },
                ]}
                accentNote="Method marks are the most powerful — you can earn the majority of marks on a question without ever reaching the correct answer."
              />
              <p>Here is the key insight: in a <strong>25-mark Maths question</strong>, you can get <strong>15+ marks with a wrong final answer</strong> if your method is right. The attempt marks and method marks add up fast. This is why leaving a question blank is the worst possible strategy — you are throwing away free marks.</p>
              <MarkTypeClassifier />
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="Reading a Real Marking Scheme." eyebrow="03 // The Decode" icon={FileSearch} theme={theme}>
              <p>SEC marking schemes use specific notation that tells you exactly how marks are allocated. Once you learn to read this language, the exam becomes much less mysterious.</p>
              <GlossaryGrid
                items={[
                  { term: "4M", definition: "4 method marks", explanation: "Earned for showing the right process, not the right answer. You can get all 4 without ever reaching the correct final answer." },
                  { term: "or equivalent", definition: "your phrasing doesn't have to match exactly", explanation: "The examiner accepts any wording that demonstrates the same understanding. This appears hundreds of times across marking schemes — examiners are far more flexible than students realise.", highlight: true },
                  { term: "any 3 points", definition: "literally pick any 3 valid points", explanation: "You do not need the 'best' ones or the ones the teacher highlighted. Any 3 valid points earn full marks." },
                  { term: "fully correct — 10; partially correct — 5", definition: "half-right gets half-marks", explanation: "This is the exam's built-in safety net. A partially correct answer is never zero." },
                  { term: "PCLM", definition: "Partial Credit Level Marks", explanation: "You get marks for each correct step in your answer independently. Every correct element earns its own credit, regardless of the others." },
                ]}
              />
              <p>The key insight here is that "or equivalent" changes everything. You do not need the textbook phrasing. You need to show understanding in your own words.</p>
              <SchemeDecoder />
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="The Keyword Effect." eyebrow="04 // The Language" icon={Key} theme={theme}>
              <p>Examiners scan for specific terminology. A student who writes "the plant needs light" gets fewer marks than one who writes "light intensity is a <Highlight description="Trigger words are the specific terms from the syllabus and textbook headings that examiners are trained to look for. Using them signals that you have precise knowledge, not just a vague idea." theme={theme}>limiting factor</Highlight> in photosynthesis." Same knowledge, completely different marks.</p>
              <p>This is not about being fancy or using big words for the sake of it. It is about using the <em>exact words</em> from the syllabus and textbook headings. These are the words examiners are trained to look for. They are <Highlight description="When an examiner sees the correct technical term in your answer, it acts like a trigger — they know immediately that you understand the concept and they can award the marks. Vague language makes them hesitate." theme={theme}>trigger words</Highlight> that activate marks.</p>
              <p>Think of it this way: the examiner is reading 500 answers to the same question. They are scanning quickly for evidence that you know the material. When they see the right keyword, it is like a green light — they can immediately award the mark. When they see vague language, they have to slow down and decide whether you really understand it. Make the examiner's job easy and they will make your marks higher.</p>
              <p>The trick is simple: when you are revising, pay attention to the <strong>exact words</strong> used in your textbook headings, diagrams, and definitions. These are the words the examiner is looking for.</p>
              <AnswerUpgrader />
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="Attempt Marks: The Free Points." eyebrow="05 // The Safety Net" icon={Shield} theme={theme}>
              <p>The most important rule in the Leaving Cert: <strong>NEVER leave a question blank.</strong> Here is why:</p>
              <p>A blank answer = 0 marks, always. There is no exception. But <Highlight description="Even the most basic attempt at answering — writing a definition, drawing a relevant diagram, restating part of the question — earns attempt marks. These are free points the examiner WANTS to give you." theme={theme}>any relevant attempt</Highlight> = 1-4 marks minimum. It does not matter if your answer is incomplete, partially wrong, or just a starting point. If it shows <em>any</em> relevant knowledge, the examiner will find marks to give you.</p>
              <p>Consider the maths: in a 6-subject, 2-paper exam, leaving just 3 questions blank could cost you <strong>10-15 CAO points</strong>. That is the difference between getting into your course and missing out. Those "impossible" questions you were going to skip? They are worth attempting.</p>
              <p>Even writing the <strong>formula you would have used</strong> earns method marks. Even <strong>defining a key term</strong> from the question earns attempt marks. Even <strong>drawing a labelled diagram</strong> related to the topic earns marks. The bar for attempt marks is incredibly low — the examiner just needs to see that you engaged with the question.</p>
              <PersonalStory name="Darragh, Leaving Cert 2023, Limerick">
                <p>"My teacher hammered it into us: write something for every single question. In my Physics exam, there were two questions I genuinely did not know how to solve. But I wrote down the relevant formulas, defined the key terms, and drew a diagram for each. When I got my results, I'd picked up 11 marks across those two questions — marks I would have completely lost if I'd left them blank. My final grade was a H3 instead of a H4. That was worth 10 CAO points."</p>
              </PersonalStory>
              <MicroCommitment theme={theme}>
                <p>Open your weakest subject's most recent past paper. Find 3 questions you would normally skip. For each one, write down what you <em>could</em> write to earn attempt marks — a formula, a definition, a diagram, anything. See how easy it is to collect free marks.</p>
              </MicroCommitment>
            </ReadingSection>
          )}

          {activeSection === 5 && (
            <ReadingSection title="The Presentation Protocol." eyebrow="06 // The Polish" icon={PenTool} theme={theme}>
              <p>Two students with identical knowledge can get different marks based purely on how they present their answers. Presentation is not about having neat handwriting — it is about making it <em>easy for the examiner to find your marks</em>.</p>
              <p><strong>Diagrams with labels.</strong> Examiners award marks per label. A diagram of the heart with 6 correct labels earns 6 marks, even if you do not write a single sentence of explanation. Always label diagrams clearly.</p>
              <p><strong>Numbered steps in Maths and Science.</strong> Each step can earn method marks independently. If you write a wall of calculations with no clear steps, the examiner might miss marks you deserve. Number your steps: Step 1, Step 2, Step 3.</p>
              <p><strong>Headings and structure in essays.</strong> Examiners reading their 300th essay that day will find your points faster if you use clear paragraph breaks and topic sentences. Do not make them hunt for your argument.</p>
              <p><strong>Underlining key terms.</strong> This signals to the examiner that you know the terminology. When they see an underlined technical term, it catches their eye and helps them award marks quickly.</p>
              <p><strong>Clean crossing-out vs scribbles.</strong> If you need to change an answer, draw a single neat line through the old text. Messy scribbles can obscure parts of your answer that might still earn marks. The examiner marks what they can read.</p>
              <p>The key insight: <Highlight description="Good presentation is not about neatness for its own sake. It is about making it easy for the examiner to see your correct points and award marks. If they cannot find it, they cannot mark it." theme={theme}>if the examiner cannot find it, they cannot mark it</Highlight>. Every mark they miss because your answer was hard to read is a mark you earned but did not collect.</p>
            </ReadingSection>
          )}

          {activeSection === 6 && (
            <ReadingSection title="Your Decoding Action Plan." eyebrow="07 // The Plan" icon={Target} theme={theme}>
              <p>You now have the tools to read any marking scheme like an insider. Here is how to put it all into practice.</p>
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Download marking schemes</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>Go to examinations.ie and download the marking scheme for every subject you are sitting. Start with last year's papers.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Read them alongside the exam paper</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>For each question, look at how marks are broken down. Notice the attempt marks, the method marks, and the answer marks. Notice where it says "or equivalent" and "any 3 points."</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Identify your mark-leaking questions</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>For each subject, find the question types where you are losing marks to technique, not knowledge. Maybe you are writing too much on short questions. Maybe you are skipping questions you could have attempted. Maybe you are not using keywords.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>4</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Practice with the scheme open</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>Do past paper questions and then mark your own answers using the marking scheme. This is the fastest way to understand what examiners want.</p>
                  </div>
                </div>
              </div>
              <MicroCommitment theme={theme}>
                <p>Pick your 3 most important subjects. Download each marking scheme from <strong>examinations.ie</strong>. For each subject, find one question type where you are losing marks to technique, not knowledge. Write down what you will do differently.</p>
              </MicroCommitment>
              <p className="mt-8 text-center font-serif text-lg font-semibold text-zinc-800 dark:text-white">You now know something most students never learn: the examiner is on your side. The marking scheme is their way of telling you exactly what they want. Give it to them.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default MarkingSchemeDecoderModule;
