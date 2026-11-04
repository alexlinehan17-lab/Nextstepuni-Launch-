import { moduleFill,moduleText } from './learning/brandTokens';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { AnimatePresence,motion } from 'framer-motion';
import { Eye,FileSearch,Key,Layers,PenTool,Shield,Target } from 'lucide-react';
import React,{ useState } from 'react';
import { MARKING_SCHEME_DECODER_REFERENCE_LIST } from '../data/references/markingSchemeDecoder';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { redTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,GlossaryGrid,Highlight,MicroCommitment,PersonalStory,ReadingSection,ToolJumpCard } from './ModuleShared';
import { MotionDiv } from './Motion';

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
  attempt: { bg: "bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]", dot: "bg-[var(--module-success)]", label: 'Attempt' },
  method: { bg: "bg-[var(--module-surface)] dark:bg-[var(--module-surface)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-ink)] dark:text-[var(--module-ink)]", dot: "bg-[var(--module-surface)]", label: 'Method' },
  answer: { bg: "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]", dot: "bg-[var(--module-danger)]", label: 'Answer' },
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
      <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)]">Mark Type Classifier</h4>
        <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-2 mb-2 max-w-md mx-auto">Read each marking scheme extract and classify it as one of three mark types:</p>
        <div className="flex justify-center gap-3 mb-6">
          {(['attempt', 'method', 'answer'] as const).map(c => (
            <span key={c} className={`px-3 py-1 rounded-full text-xs font-bold ${markTypeColors[c].bg} ${markTypeColors[c].text} border ${markTypeColors[c].border}`}>{markTypeColors[c].label}</span>
          ))}
        </div>
        <button onClick={startDrill} className="px-6 py-3 bg-[var(--module-danger)] hover:bg-[var(--module-danger)] text-[var(--module-ink)] font-bold text-sm rounded-lg transition-colors" data-wide-button="true">Start Classifying</button>
      </div>
    );
  }

  if (phase === 'done') {
    return (
      <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Classification Results</h4>
        <div className="flex justify-center my-5">
          <div className="text-center px-5 py-3 rounded-xl bg-[var(--module-surface)] dark:bg-[var(--module-surface)]">
            <div className="text-2xl font-bold text-[var(--module-ink)] dark:text-[var(--module-ink)]">{score}/{classifierItems.length}</div>
            <div className="text-xs font-semibold text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-0.5">Correct</div>
          </div>
        </div>
        <div className="space-y-2.5 mb-6">
          {classifierItems.map((q, i) => {
            const got = choices[i];
            const correct = got === q.correct;
            const c = markTypeColors[q.correct];
            return (
              <div key={i} className={`p-3 rounded-lg border ${correct ? `${c.bg} ${c.border}` : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] border-[var(--module-line)] dark:border-[var(--module-line)]"}`}>
                <div className="flex items-start gap-2.5">
                  <span className={`mt-1 w-2 h-2 rounded-full flex-shrink-0 ${c.dot}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-xs font-bold text-[var(--module-muted)]">{c.label} marks</span>
                      {correct ? (
                        <span className="text-xs font-bold text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">Correct</span>
                      ) : (
                        <span className="text-xs font-bold text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]">You said {got ? markTypeColors[got as keyof typeof markTypeColors].label : 'nothing'} — should be {c.label}</span>
                      )}
                    </div>
                    <p className="text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)] mt-0.5 font-mono">{q.text}</p>
                    <p className="text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-1 italic">{q.explanation}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        {score < classifierItems.length && (
          <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] text-center mb-4 italic">Understanding mark types helps you know what to write even when you are unsure of the answer.</p>
        )}
        <div className="text-center">
          <button onClick={startDrill} className="px-5 py-2.5 bg-[var(--module-danger)] hover:bg-[var(--module-danger)] text-[var(--module-ink)] font-bold text-sm rounded-lg transition-colors" data-wide-button="true">Try Again</button>
        </div>
      </div>
    );
  }

  const q = classifierItems[qIndex];
  const isCorrect = showFeedback && choices[qIndex] === q.correct;
  const isWrong = showFeedback && choices[qIndex] !== q.correct;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <div className="flex items-center justify-between mb-4">
        <h4 className="font-serif text-lg font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)]">Mark Type Classifier</h4>
        <span className="text-xs font-bold text-[var(--module-muted)]">{qIndex + 1} / {classifierItems.length}</span>
      </div>
      {/* Question card */}
      <AnimatePresence mode="wait">
        <motion.div key={qIndex} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -24 }}
          className={`p-5 rounded-xl border min-h-[100px] flex flex-col justify-center mb-5 transition-colors ${
            isCorrect ? "bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] border-[var(--module-line)] dark:border-[var(--module-line)]" :
            isWrong ? "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border-[var(--module-line)] dark:border-[var(--module-line)]" :
            "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] border-[var(--module-line)] dark:border-[var(--module-line)]"
          }`}>
          <p className="font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)] text-sm font-mono">{q.text}</p>
          {showFeedback && (
            <motion.p initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className={`text-xs mt-3 italic ${isCorrect ? "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]" : "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"}`}>
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
                selected && !isAnswer ? "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] border-[var(--module-line)] dark:border-[var(--module-line)]" :
                `${cm.bg} ${cm.text} ${cm.border} hover:opacity-80`
              } ${showFeedback ? 'cursor-default' : 'cursor-pointer'}`} data-wide-button="true" data-selected={!!(selected && !isAnswer)} data-tone="coral" aria-pressed={!!(selected && !isAnswer)}>
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
            i < qIndex ? (choices[i] === classifierItems[i].correct ? "bg-[var(--module-success)]" : "bg-[var(--module-danger)]") :
            i === qIndex ? "bg-[var(--module-danger)]" : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)]"
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
    text: 'Q3(c) Define osmosis in your own words or equivalent. (9 marks)',
    annotations: [
      { term: 'or equivalent', start: 40, end: 53, explanation: 'Your phrasing doesn\'t need to match the textbook exactly. The examiner is flexible.' },
      { term: '9 marks', start: 56, end: 63, explanation: '9 marks for a definition means they want detail — not just one sentence.' },
      { term: 'your own words', start: 24, end: 38, explanation: 'Science schemes credit each correct element separately, so a definition in your own words still scores mark-by-mark — you don\'t need the exact textbook wording.' },
    ]
  },
];

const SchemeDecoder = () => {
  const [activeExtract, setActiveExtract] = useState(0);
  const [activeAnnotation, setActiveAnnotation] = useState<number | null>(null);

  const extract = schemeExtracts[activeExtract];
  const _decodedCount = activeAnnotation !== null ? 1 : 0;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <div className="text-center mb-6">
        <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Exam Skills Tool</span>
        <h4 className="font-serif font-bold" style={{ fontSize: 22, color: "var(--module-ink)" }}>Scheme Decoder</h4>
        <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Click the highlighted terms to decode what they really mean.</p>
      </div>

      {/* Extract tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {schemeExtracts.map((_, i) => (
          <button key={i} onClick={() => { setActiveExtract(i); setActiveAnnotation(null); }}
            style={{
              backgroundColor: moduleFill(activeExtract === i ? COLORS.accent : "var(--module-surface)"),
              border: activeExtract === i ? `2px solid ${COLORS.accent}` : "2px solid var(--module-line)",
              borderRadius: 20,
              padding: '8px 18px',
              fontSize: 13,
              fontWeight: 600,
              color: moduleText(activeExtract === i ? "var(--module-on-fill)" : "var(--module-muted)"),
              whiteSpace: 'nowrap' as const,
              cursor: 'pointer',
            }} data-wide-button="true" data-selected={!!(activeExtract === i)} data-tone="orange" aria-pressed={!!(activeExtract === i)}>
            Extract {i + 1}
          </button>
        ))}
      </div>

      {/* Extract card */}
      <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)] mb-4" style={{ border: "2px solid var(--module-line)", borderRadius: 14, padding: '20px 24px' }}>
        <span className="inline-block mb-3" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', backgroundColor: "var(--module-surface)", color: "var(--module-muted)", border: "1px solid var(--module-line)", borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Exam Question Extract</span>
        <p style={{ fontSize: 15, color: "var(--module-ink)", lineHeight: 1.7 }}>
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
                    backgroundColor: moduleFill(isClicked ? COLORS.accent : COLORS.accentTint),
                    color: moduleText(isClicked ? "var(--module-on-fill)" : COLORS.accentDarkText),
                    fontWeight: 700,
                    borderRadius: 4,
                    padding: '1px 6px',
                    cursor: 'pointer',
                    borderBottom: isClicked ? 'none' : `2px solid ${COLORS.accent}`,
                    transition: 'all 0.2s',
                  }} data-wide-button="true" data-selected={!!(isClicked)} data-tone="orange" aria-pressed={!!(isClicked)}>
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
            style={{ borderLeft: `3px solid ${COLORS.accent}`, backgroundColor: moduleFill(COLORS.accentTint), borderRadius: '0 10px 10px 0', padding: '12px 16px', marginTop: 12 }}>
            <p className="font-serif font-semibold" style={{ fontSize: 15, color: moduleText(COLORS.accentDarkText), marginBottom: 4 }}>{extract.annotations[activeAnnotation].term}</p>
            <p className="italic" style={{ fontSize: 14, color: "var(--module-ink)" }}>{extract.annotations[activeAnnotation].explanation}</p>
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
          <span key={`k-${keyIndex}`} className="px-1 py-0.5 rounded bg-[var(--module-surface)] dark:bg-[var(--module-danger)] text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] font-bold">
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
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Answer Upgrader</h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-1 mb-6">See how adding the right keywords transforms marks.</p>

      {/* Subject tabs */}
      <div className="flex gap-2 mb-6 justify-center">
        {upgradeExamples.map((e, i) => (
          <button key={i} onClick={() => { setActiveExample(i); setShowAfter(false); setShowKeywords(false); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
              activeExample === i ? "bg-[var(--module-danger)] text-[var(--module-ink)]" : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-ink)] dark:text-[var(--module-muted)] hover:bg-[var(--module-surface)] dark:hover:bg-[var(--module-surface)]"
            }`} data-wide-button="true" data-selected={!!(activeExample === i)} data-tone="coral" aria-pressed={!!(activeExample === i)}>
            {e.subject}
          </button>
        ))}
      </div>

      {/* Question */}
      <div className="text-center mb-4">
        <span className="text-xs font-bold uppercase tracking-wider text-[var(--module-muted)]">{ex.subject}</span>
        <p className="font-serif text-lg font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] mt-1">{ex.question}</p>
      </div>

      {/* Before / After cards */}
      <div className="grid md:grid-cols-2 gap-4 mb-5">
        {/* Before */}
        <div className="p-5 rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-surface)] dark:bg-[var(--module-surface)]">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-[var(--module-muted)]">Before</span>
            <span className="text-xs font-bold text-[var(--module-danger-text)]">{ex.before.marks}/{ex.maxMarks} marks</span>
          </div>
          <p className="text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)] leading-relaxed italic">{ex.before.text}</p>
          {/* Mark bar */}
          <div className="mt-3 w-full h-2 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full overflow-hidden">
            <div className="h-full bg-[var(--module-danger)] rounded-full transition-all duration-700" style={{ width: `${(ex.before.marks / ex.maxMarks) * 100}%` }} />
          </div>
        </div>

        {/* After */}
        <div className={`p-5 rounded-xl border transition-all duration-300 ${showAfter ? "border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-surface)] dark:bg-[var(--module-success)]" : "border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-surface)] dark:bg-[var(--module-surface)]"}`}>
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-[var(--module-muted)]">After</span>
            {showAfter && <span className="text-xs font-bold text-[var(--module-success-text)]">{ex.after.marks}/{ex.maxMarks} marks</span>}
          </div>
          {showAfter ? (
            <>
              <p className="text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)] leading-relaxed">
                {showKeywords ? highlightKeywords(ex.after.text, ex.keywords) : ex.after.text}
              </p>
              <div className="mt-3 w-full h-2 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-[var(--module-success)] rounded-full"
                  initial={{ width: `${(ex.before.marks / ex.maxMarks) * 100}%` }}
                  animate={{ width: `${(ex.after.marks / ex.maxMarks) * 100}%` }}
                  transition={{ duration: 0.8, ease: 'easeOut' }}
                />
              </div>
            </>
          ) : (
            <div className="flex items-center justify-center h-16">
              <button onClick={() => setShowAfter(true)}
                className="px-5 py-2 bg-[var(--module-danger)] hover:bg-[var(--module-danger)] text-[var(--module-ink)] font-bold text-sm rounded-lg transition-colors" data-wide-button="true">
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
                showKeywords ? "bg-[var(--module-danger)] text-[var(--module-ink)]" : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-ink)] dark:text-[var(--module-muted)] hover:bg-[var(--module-surface)] dark:hover:bg-[var(--module-surface)]"
              }`} data-wide-button="true" data-selected={!!(showKeywords)} data-tone="coral" aria-pressed={!!(showKeywords)}>
              {showKeywords ? 'Hide Keywords' : 'Show Keywords'}
            </button>
          </div>
          {showKeywords && (
            <div className="flex flex-wrap gap-2 justify-center">
              {ex.keywords.map((kw, i) => (
                <span key={i} className="px-2.5 py-1 rounded-full text-xs font-bold bg-[var(--module-surface)] dark:bg-[var(--module-danger)] text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
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
  const essentials = useEssentialsMode();
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
      references={MARKING_SCHEME_DECODER_REFERENCE_LIST}
      finishButtonText="Decode Every Exam"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Examiner's Secret." eyebrow="01 // The Mindset" icon={Eye} theme={theme}>
              {essentials ? (<>
              <p>Examiners <em>want</em> to give you marks. They use <Highlight description="SEC examiners use positive marking. They scan your answer looking for things that deserve marks, not things to penalise. Every correct point you make earns credit." theme={theme}>positive marking</Highlight>: they reward what is right, ignore what is wrong.<Cite n={1} /> The marking scheme is the <Highlight description="The marking scheme tells you exactly what the examiner will look for in your answer. It is the closest thing to an answer key you will ever get before the exam." theme={theme}>answer key published before the exam</Highlight> on examinations.ie. Most students never read one. You should. It tells you exactly what to write.</p>
              </>) : (<>
              <p>Here is something most students never figure out: examiners <em>want</em> to give you marks. The marking scheme is their checklist. They are looking for reasons to <Highlight description="SEC examiners use positive marking. They scan your answer looking for things that deserve marks, not things to penalise. Every correct point you make earns credit." theme={theme}>award marks</Highlight>, not reasons to take them away.<Cite n={1} /></p>
              <p>This changes everything. It means the examiner is on your side. The marking scheme is not a secret document locked away in a vault — it is published on <strong>examinations.ie</strong> every year, for every subject, for every paper. It is literally the <Highlight description="The marking scheme tells you exactly what the examiner will look for in your answer. It is the closest thing to an answer key you will ever get before the exam." theme={theme}>answer key published BEFORE the exam</Highlight>. And yet most students never read one.</p>
              <p>The students who <em>do</em> read marking schemes instantly understand what examiners want. They stop guessing and start giving examiners exactly what they are looking for. That is the edge this module will give you.</p>
              <Highlight description="Examiners use positive marking — they mark what is RIGHT in your answer, not what is wrong. Every relevant point earns credit. A blank answer is the only answer that gets zero." theme={theme}>Positive marking</Highlight> means examiners mark what is right, not what is wrong. If you write three correct points and two incorrect ones, you get marks for the three correct points. The incorrect ones are simply ignored.
              </>)}
              <PersonalStory name="Aoife, Leaving Cert 2024, Galway">
                <p>"I never looked at a marking scheme until my teacher made us go through one in class. I was shocked. I'd been writing these long, detailed answers for Biology, thinking more was better. But the scheme showed that each question only wanted 3 or 4 specific points. I was spending 15 minutes on answers that needed 5 minutes. Once I started studying the schemes, my grades went up a full grade in two subjects — not because I knew more, but because I finally understood what they were actually asking for."</p>
              </PersonalStory>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="The Three Types of Marks." eyebrow="02 // The System" icon={Layers} theme={theme}>
              {essentials ? (<>
              <p>Every mark falls into three types: Attempt (1-3 marks for trying), Method (2-5 marks for showing the right approach), and Answer (2-6 marks for the correct final answer). You can get 15+ marks on a 25-mark Maths question with a wrong final answer if your method is right.<Cite n={1} /> Never leave anything blank.</p>
              </>) : (<>
              <p>Every mark in the Leaving Cert falls into one of three categories. Once you understand this system, you will never look at an exam question the same way again.</p>
              </>)}
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Attempt Marks", description: "1–3 marks awarded just for trying. Write anything relevant and you get these — even if your answer is incomplete or partly wrong, the examiner awards attempt marks for showing you engaged with the question." },
                  { number: 2, term: "Method Marks", description: "2–5 marks awarded for showing the right approach, even if your final answer is wrong. Using the right formula, setting up the equation correctly, or showing a logical chain of reasoning all earn method marks regardless of where you end up.", highlight: true },
                  { number: 3, term: "Answer Marks", description: "2–6 marks awarded for the correct final answer. These are the only marks that require you to actually get it right — but you can still earn attempt and method marks without them." },
                ]}
                accentNote="Method marks are the most powerful — you can earn the majority of marks on a question without ever reaching the correct answer."
              />
              <p>Here is the key insight: in a <strong>25-mark Maths question</strong>, you can get <strong>15+ marks with a wrong final answer</strong> if your method is right. The attempt marks and method marks add up fast.<Cite n={1} /> This is why leaving a question blank is the worst possible strategy — you are throwing away free marks.</p>
              <MarkTypeClassifier />
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="Reading a Real Marking Scheme." eyebrow="03 // The Decode" icon={FileSearch} theme={theme}>
              {essentials ? (<>
              <p>Marking schemes use a code. "4M" means 4 method marks. "Or equivalent" means any phrasing works. "Any 3 points" means you choose. "Partial credit" means each correct step earns its own marks. Learn this language and the exam becomes much less mysterious.<Cite n={1} /> Try the decoder below.</p>
              </>) : (<>
              <p>SEC marking schemes use specific notation that tells you exactly how marks are allocated.<Cite n={1} /> Once you learn to read this language, the exam becomes much less mysterious.</p>
              </>)}
              <GlossaryGrid
                items={[
                  { term: "4M", definition: "4 method marks", explanation: "Earned for showing the right process, not the right answer. You can get all 4 without ever reaching the correct final answer." },
                  { term: "or equivalent", definition: "your phrasing doesn't have to match exactly", explanation: "The examiner accepts any wording that demonstrates the same understanding. This appears hundreds of times across marking schemes — examiners are far more flexible than students realise.", highlight: true },
                  { term: "any 3 points", definition: "literally pick any 3 valid points", explanation: "You do not need the 'best' ones or the ones the teacher highlighted. Any 3 valid points earn full marks." },
                  { term: "fully correct — 10; partially correct — 5", definition: "half-right gets half-marks", explanation: "This is the exam's built-in safety net. A partially correct answer is never zero." },
                  { term: "partial credit", definition: "on-the-right-track work earns part-marks", explanation: "SEC schemes (especially Maths) award graduated partial credit — low, mid, or high — for work that uses the right approach, so each correct step earns its own credit regardless of where you end up." },
                ]}
              />
              <p>The key insight here is that "or equivalent" changes everything. You do not need the textbook phrasing. You need to show understanding in your own words.</p>
              <SchemeDecoder />
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="The Keyword Effect." eyebrow="04 // The Language" icon={Key} theme={theme}>
              {essentials ? (<>
              <p>Use the exact words from the syllabus. "Light intensity is a <Highlight description="Trigger words are the specific terms from the syllabus and textbook headings that examiners are trained to look for. Using them signals that you have precise knowledge, not just a vague idea." theme={theme}>limiting factor</Highlight>" earns more marks than "the plant needs light." These <Highlight description="When an examiner sees the correct technical term in your answer, it acts like a trigger — they know immediately that you understand the concept and they can award the marks. Vague language makes them hesitate." theme={theme}>trigger words</Highlight> tell the examiner you know the material.<Cite n={1} /> When revising, note the exact words in textbook headings and definitions. Use those words in your answers.</p>
              </>) : (<>
              <p>Examiners scan for specific terminology. A student who writes "the plant needs light" gets fewer marks than one who writes "light intensity is a <Highlight description="Trigger words are the specific terms from the syllabus and textbook headings that examiners are trained to look for. Using them signals that you have precise knowledge, not just a vague idea." theme={theme}>limiting factor</Highlight> in photosynthesis." Same knowledge, completely different marks.<Cite n={1} /></p>
              <p>This is not about being fancy or using big words for the sake of it. It is about using the <em>exact words</em> from the syllabus and textbook headings. These are the words examiners are trained to look for. They are <Highlight description="When an examiner sees the correct technical term in your answer, it acts like a trigger — they know immediately that you understand the concept and they can award the marks. Vague language makes them hesitate." theme={theme}>trigger words</Highlight> that activate marks.</p>
              <p>Think of it this way: the examiner is reading 500 answers to the same question. They are scanning quickly for evidence that you know the material. When they see the right keyword, it is like a green light — they can immediately award the mark. When they see vague language, they have to slow down and decide whether you really understand it. Make the examiner's job easy and they will make your marks higher.</p>
              <p>The trick is simple: when you are revising, pay attention to the <strong>exact words</strong> used in your textbook headings, diagrams, and definitions. These are the words the examiner is looking for.</p>
              </>)}
              <AnswerUpgrader />
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="Attempt Marks: The Free Points." eyebrow="05 // The Safety Net" icon={Shield} theme={theme}>
              {essentials ? (<>
              <p>Never leave a question blank. Blank = 0 marks always. <Highlight description="Even the most basic attempt at answering — writing a definition, drawing a relevant diagram, restating part of the question — earns attempt marks. These are free points the examiner WANTS to give you." theme={theme}>Any relevant attempt</Highlight> = 1-4 marks.<Cite n={1} /> Write the formula, define a key term, or draw a diagram. Leaving 3 questions blank across your exams could cost you 10-15 CAO points.<Cite n={2} /> That could be the difference for your course.</p>
              </>) : (<>
              <p>The most important rule in the Leaving Cert: <strong>NEVER leave a question blank.</strong> Here is why:</p>
              <p>A blank answer = 0 marks, always. There is no exception. But <Highlight description="Even the most basic attempt at answering — writing a definition, drawing a relevant diagram, restating part of the question — earns attempt marks. These are free points the examiner WANTS to give you." theme={theme}>any relevant attempt</Highlight> = 1-4 marks minimum.<Cite n={1} /> It does not matter if your answer is incomplete, partially wrong, or just a starting point. If it shows <em>any</em> relevant knowledge, the examiner will find marks to give you.</p>
              <p>Consider the maths: in a 6-subject, 2-paper exam, leaving just 3 questions blank could cost you <strong>10-15 CAO points</strong>.<Cite n={2} /> That is the difference between getting into your course and missing out. Those "impossible" questions you were going to skip? They are worth attempting.</p>
              <p>Even writing the <strong>formula you would have used</strong> earns method marks. Even <strong>defining a key term</strong> from the question earns attempt marks. Even <strong>drawing a labelled diagram</strong> related to the topic earns marks. The bar for attempt marks is incredibly low — the examiner just needs to see that you engaged with the question.</p>
              </>)}
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
              {essentials ? (<>
              <p>Presentation earns marks. Label your diagrams clearly. Number your steps in Maths. Use headings in essays. Underline key terms. Cross out neatly, never scribble. The rule: <Highlight description="Good presentation is not about neatness for its own sake. It is about making it easy for the examiner to see your correct points and award marks. If they cannot find it, they cannot mark it." theme={theme}>if the examiner cannot find it, they cannot mark it</Highlight>.<Cite n={1} /> Make their job easy and your marks go up.</p>
              </>) : (<>
              <p>Two students with identical knowledge can get different marks based purely on how they present their answers. Presentation is not about having neat handwriting — it is about making it <em>easy for the examiner to find your marks</em>.</p>
              <p><strong>Diagrams with labels.</strong> Examiners award marks per label.<Cite n={1} /> A diagram of the heart with 6 correct labels earns 6 marks, even if you do not write a single sentence of explanation. Always label diagrams clearly.</p>
              <p><strong>Numbered steps in Maths and Science.</strong> Each step can earn method marks independently. If you write a wall of calculations with no clear steps, the examiner might miss marks you deserve. Number your steps: Step 1, Step 2, Step 3.</p>
              <p><strong>Headings and structure in essays.</strong> Examiners reading their 300th essay that day will find your points faster if you use clear paragraph breaks and topic sentences. Do not make them hunt for your argument.</p>
              <p><strong>Underlining key terms.</strong> This signals to the examiner that you know the terminology. When they see an underlined technical term, it catches their eye and helps them award marks quickly.</p>
              <p><strong>Clean crossing-out vs scribbles.</strong> If you need to change an answer, draw a single neat line through the old text. Messy scribbles can obscure parts of your answer that might still earn marks. The examiner marks what they can read.</p>
              <p>The key insight: <Highlight description="Good presentation is not about neatness for its own sake. It is about making it easy for the examiner to see your correct points and award marks. If they cannot find it, they cannot mark it." theme={theme}>if the examiner cannot find it, they cannot mark it</Highlight>. Every mark they miss because your answer was hard to read is a mark you earned but did not collect.</p>
              </>)}
            </ReadingSection>
          )}

          {activeSection === 6 && (
            <ReadingSection title="Your Decoding Action Plan." eyebrow="07 // The Plan" icon={Target} theme={theme}>
              {essentials ? (<>
              <p>Download marking schemes from examinations.ie. Read them alongside past papers. Find where you lose marks to technique. Practise marking your own answers. Follow the steps below.</p>
              </>) : (<>
              <p>You now have the tools to read any marking scheme like an insider. Here is how to put it all into practice.</p>
              </>)}
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-solid)" }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-ink)" }}>Download marking schemes</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-ink)", opacity: 0.8 }}>Go to examinations.ie and download the marking scheme for every subject you are sitting. Start with last year's papers.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-danger-text)" }}>Read them alongside the exam paper</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-danger-text)", opacity: 0.8 }}>For each question, look at how marks are broken down. Notice the attempt marks, the method marks, and the answer marks. Notice where it says "or equivalent" and "any 3 points."</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-danger-text)" }}>Identify your mark-leaking questions</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-danger-text)", opacity: 0.8 }}>For each subject, find the question types where you are losing marks to technique, not knowledge. Maybe you are writing too much on short questions. Maybe you are skipping questions you could have attempted. Maybe you are not using keywords.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-success)" }}>4</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-success-text)" }}>Practice with the scheme open</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-success-text)", opacity: 0.8 }}>Do past paper questions and then mark your own answers using the marking scheme. This is the fastest way to understand what examiners want.</p>
                  </div>
                </div>
              </div>
              <MicroCommitment theme={theme}>
                <p>Pick your 3 most important subjects. Open each one in <strong>Paper Trail</strong> (in the Launchpad) — the real paper and its marking scheme, side by side. For each subject, find one question type where you are losing marks to technique, not knowledge. Write down what you will do differently.</p>
              </MicroCommitment>
              <p className="mt-8 text-center font-serif text-lg font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)]">You now know something most students never learn: the examiner is on your side. The marking scheme is their way of telling you exactly what they want. Give it to them.</p>
              <ToolJumpCard
                toolId="paper-trail"
                title="Open the real paper and scheme"
                description="Paper Trail has every SEC past paper and marking scheme for your subjects — free, in the app, with the scheme one tap from the paper."
                ctaLabel="Open Paper Trail"
              />
              <ToolJumpCard
                toolId="war-room"
                title="Choose the next syllabus area"
                description="Subject Coverage in War Room keeps the official map beside your confidence. Choose a shaky area, then practise it here with the marking scheme open."
                ctaLabel="Open Subject Coverage"
              />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default MarkingSchemeDecoderModule;
