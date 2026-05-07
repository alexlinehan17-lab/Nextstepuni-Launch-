/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Scheme Phrase Match (Stage 3.3, E17).
 *
 * Visual metaphor: a phrase constellation. The marking scheme's required
 * key phrases are displayed as nodes scattered in a starfield. The
 * student types or pastes their answer; phrases the answer matches
 * (verbatim or by acceptable paraphrase) light up TEAL with a soft pulse
 * and draw a thin connecting line down to the answer panel below.
 * Missed phrases stay dim — visible gaps in the constellation.
 *
 * Two modes:
 *
 *   FORWARD — student writes; tool matches against the constellation
 *   and reports phrases hit / total. Each missed phrase carries a
 *   tooltip with acceptable paraphrases drawn from the marking scheme.
 *
 *   REVERSE — "build the model answer". Student is given the question
 *   and the canonical phrases out of order; they click them in the
 *   order they\'d use them. Tool grades for both completeness (all
 *   phrases used) and order (compared to the model paragraph).
 *
 * Library: 18 questions across Biology, Chemistry, Physics, drawn from
 * the dossier\'s catalogue of canonical key phrases.
 *
 * Source: dossier § B4 (Sciences key-phrase matching).
 *
 * Aesthetic: Stage 3 register — 2px #1a1a1a borders, dark constellation
 * panel for visual contrast, SVG nodes via Framer Motion.
 */

import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { PHRASE_MATCH_QUESTIONS } from '../../../../data/knowledge/phraseMatch';
import { type PhraseMatchQuestion, type PhraseMatchKey } from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

type SubjectFilter = 'all' | 'biology' | 'chemistry' | 'physics';
type Mode = 'forward' | 'reverse';

interface Props {
  onBack: () => void;
}

const PhraseMatch: React.FC<Props> = ({ onBack }) => {
  const [subjectFilter, setSubjectFilter] = useState<SubjectFilter>('all');
  const filteredQuestions = useMemo(() => {
    if (subjectFilter === 'all') return PHRASE_MATCH_QUESTIONS;
    return PHRASE_MATCH_QUESTIONS.filter(q => q.subject === subjectFilter);
  }, [subjectFilter]);

  const [questionId, setQuestionId] = useState<string>(filteredQuestions[0]?.id ?? PHRASE_MATCH_QUESTIONS[0].id);
  const question = useMemo(
    () => PHRASE_MATCH_QUESTIONS.find(q => q.id === questionId) ?? PHRASE_MATCH_QUESTIONS[0],
    [questionId],
  );

  const [mode, setMode] = useState<Mode>('forward');
  const [answer, setAnswer] = useState('');
  const [reverseOrder, setReverseOrder] = useState<string[]>([]);

  // Reset state when question changes
  React.useEffect(() => {
    setAnswer('');
    setReverseOrder([]);
  }, [questionId]);

  const switchSubjectFilter = (s: SubjectFilter) => {
    setSubjectFilter(s);
    const next = s === 'all' ? PHRASE_MATCH_QUESTIONS : PHRASE_MATCH_QUESTIONS.filter(q => q.subject === s);
    if (next.length > 0) setQuestionId(next[0].id);
  };

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <SubjectFilterRow filter={subjectFilter} onChange={switchSubjectFilter} />

      <QuestionPicker
        questions={filteredQuestions}
        activeId={question.id}
        onChange={setQuestionId}
      />

      <QuestionFrame question={question} />

      <ModeToggle mode={mode} onChange={setMode} />

      {mode === 'forward' ? (
        <ForwardMode question={question} answer={answer} setAnswer={setAnswer} />
      ) : (
        <ReverseMode
          question={question}
          order={reverseOrder}
          setOrder={setReverseOrder}
        />
      )}
    </div>
  );
};

// ─── Layout chrome ─────────────────────────────────────────────────────

const BackBar: React.FC<{ onBack: () => void }> = ({ onBack }) => (
  <button
    type="button"
    onClick={onBack}
    className="font-sans flex items-center gap-1.5"
    style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
  >
    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden>
      <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
    Necessary Knowledge
  </button>
);

const Hero: React.FC = () => (
  <header>
    <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#9e9186' }}>
      Necessary Knowledge · Stage 3 · Sciences
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Phrase Match Constellation.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      Marking schemes in Biology, Chemistry, and Physics hunt for specific key phrases. Per the dossier, "isotope" must
      include "same atomic number" and "different mass numbers"; "myelin sheath function" requires "to insulate" or
      "to speed up the transmission". Type your answer; the constellation shows which phrases you hit and which gaps
      remain.
    </p>
  </header>
);

// ─── Filter + picker ──────────────────────────────────────────────────

const SubjectFilterRow: React.FC<{ filter: SubjectFilter; onChange: (s: SubjectFilter) => void }> = ({ filter, onChange }) => {
  const opts: { id: SubjectFilter; label: string }[] = [
    { id: 'all', label: 'All' },
    { id: 'biology', label: 'Biology' },
    { id: 'chemistry', label: 'Chemistry' },
    { id: 'physics', label: 'Physics' },
  ];
  return (
    <div className="flex flex-wrap gap-1.5">
      {opts.map(o => {
        const active = o.id === filter;
        return (
          <button
            key={o.id}
            type="button"
            onClick={() => onChange(o.id)}
            className="font-sans rounded-full"
            style={{
              backgroundColor: active ? INK : '#FFFFFF',
              color: active ? '#FFFFFF' : INK,
              border: `1.5px solid ${INK}`,
              padding: '6px 14px',
              fontSize: 12,
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
};

const QuestionPicker: React.FC<{
  questions: PhraseMatchQuestion[];
  activeId: string;
  onChange: (id: string) => void;
}> = ({ questions, activeId, onChange }) => (
  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
    {questions.map(q => {
      const active = q.id === activeId;
      return (
        <button
          key={q.id}
          type="button"
          onClick={() => onChange(q.id)}
          className="font-sans text-left rounded-xl"
          style={{
            backgroundColor: active ? INK : '#FFFFFF',
            color: active ? '#FFFFFF' : INK,
            border: `1.5px solid ${INK}`,
            padding: '9px 11px',
            cursor: 'pointer',
          }}
        >
          <p style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7 }}>
            {q.subject}
          </p>
          <p style={{ fontSize: 12, fontWeight: 600, lineHeight: 1.3, marginTop: 2 }}>
            {q.topicLabel}
          </p>
        </button>
      );
    })}
  </div>
);

const QuestionFrame: React.FC<{ question: PhraseMatchQuestion }> = ({ question }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '20px 24px' }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Question
    </p>
    <p className="font-serif" style={{ fontSize: 16, fontWeight: 500, color: INK, lineHeight: 1.5, fontStyle: 'italic' }}>
      &ldquo;{question.questionPrompt}&rdquo;
    </p>
    <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550', marginTop: 8 }}>
      {question.keys.length} key phrase{question.keys.length === 1 ? '' : 's'} the marking scheme is hunting.
    </p>
  </section>
);

const ModeToggle: React.FC<{ mode: Mode; onChange: (m: Mode) => void }> = ({ mode, onChange }) => (
  <div className="inline-flex" style={{ border: `2px solid ${INK}`, borderRadius: 999, padding: 3 }}>
    {(['forward', 'reverse'] as const).map(m => {
      const active = m === mode;
      return (
        <button
          key={m}
          type="button"
          onClick={() => onChange(m)}
          className="font-sans rounded-full"
          style={{
            backgroundColor: active ? INK : 'transparent',
            color: active ? '#FFFFFF' : INK,
            border: 'none',
            padding: '7px 18px',
            fontSize: 12,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          {m === 'forward' ? 'Forward · write your answer' : 'Reverse · build the model'}
        </button>
      );
    })}
  </div>
);

// ─── Forward mode ─────────────────────────────────────────────────────

const ForwardMode: React.FC<{
  question: PhraseMatchQuestion;
  answer: string;
  setAnswer: (s: string) => void;
}> = ({ question, answer, setAnswer }) => {
  const matchMap = useMemo(() => computeMatches(answer, question.keys), [answer, question]);
  const hits = question.keys.filter(k => matchMap[k.id]).length;
  const total = question.keys.length;

  return (
    <>
      <Constellation question={question} matchMap={matchMap} />

      <section
        className="rounded-2xl"
        style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '22px 24px' }}
      >
        <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
            Your answer
          </p>
          {answer.trim() && (
            <span className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: hits === total ? TEAL : hits >= total / 2 ? TEAL_DARK : WARN }}>
              {hits} / {total} phrases matched
            </span>
          )}
        </div>
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Write your answer here. Phrases above will light up as you match them."
          className="w-full font-serif rounded-lg"
          style={{
            backgroundColor: CREAM,
            border: `1.5px solid ${INK}`,
            padding: '12px 14px',
            fontSize: 14,
            lineHeight: 1.65,
            color: INK,
            minHeight: 120,
            resize: 'vertical',
            outline: 'none',
          }}
        />
      </section>

      {answer.trim() && hits < total && (
        <MissedPhrases question={question} matchMap={matchMap} />
      )}
    </>
  );
};

// ─── Constellation ────────────────────────────────────────────────────

const Constellation: React.FC<{
  question: PhraseMatchQuestion;
  matchMap: Record<string, string | null>;
}> = ({ question, matchMap }) => {
  const positions = useMemo(() => layoutPhrases(question.keys, question.id), [question]);
  const hits = question.keys.filter(k => matchMap[k.id]).length;
  const total = question.keys.length;

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        padding: '22px 24px',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Starfield background dots */}
      <StarfieldBackground />

      <div className="relative" style={{ zIndex: 2 }}>
        <div className="flex items-baseline justify-between gap-3 mb-3 flex-wrap">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
            Marking-scheme constellation
          </p>
          <span className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: hits === total ? TEAL : '#FFFFFF' }}>
            {hits}<span style={{ fontSize: 13, color: '#FFD8A8', fontWeight: 500, opacity: 0.85 }}> / {total} phrases lit</span>
          </span>
        </div>

        <div style={{ position: 'relative', height: 240 }}>
          <svg viewBox="0 0 100 100" preserveAspectRatio="none" width="100%" height={240} style={{ display: 'block' }} aria-hidden>
            {/* Phrase nodes */}
            {question.keys.map((key, i) => {
              const pos = positions[i];
              const matched = !!matchMap[key.id];
              return (
                <PhraseNode
                  key={key.id}
                  pos={pos}
                  label={key.canonical}
                  matched={matched}
                  index={i}
                />
              );
            })}
          </svg>
        </div>
      </div>
    </section>
  );
};

const StarfieldBackground: React.FC = () => (
  <svg
    aria-hidden
    style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', zIndex: 1, opacity: 0.35, pointerEvents: 'none' }}
    viewBox="0 0 100 100"
    preserveAspectRatio="none"
  >
    {Array.from({ length: 60 }).map((_, i) => {
      // Deterministic pseudo-random positions
      const x = ((i * 37) % 100);
      const y = ((i * 53) % 100);
      const r = 0.15 + ((i * 13) % 5) * 0.06;
      const op = 0.3 + ((i * 7) % 5) * 0.1;
      return (
        <circle key={i} cx={x} cy={y} r={r} fill="#FFD8A8" opacity={op} />
      );
    })}
  </svg>
);

interface PhrasePos { x: number; y: number }

function layoutPhrases(keys: PhraseMatchKey[], seed: string): PhrasePos[] {
  // Deterministic layout: spread keys across a 100x100 viewport in a
  // balanced starfield pattern based on key count.
  const n = keys.length;
  const positions: PhrasePos[] = [];
  const seedNum = simpleHash(seed);
  for (let i = 0; i < n; i++) {
    // Distribute around an oval with jitter
    const angle = (i / n) * Math.PI * 2 + (seedNum % 100) * 0.02;
    const radius = 28 + ((seedNum * (i + 1)) % 12);
    const cx = 50 + Math.cos(angle) * radius;
    const cy = 50 + Math.sin(angle) * radius * 0.78; // squash vertically for landscape feel
    positions.push({ x: clamp(cx, 12, 88), y: clamp(cy, 18, 82) });
  }
  return positions;
}

function clamp(n: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, n));
}

function simpleHash(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = (h * 31 + s.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

const PhraseNode: React.FC<{
  pos: PhrasePos;
  label: string;
  matched: boolean;
  index: number;
}> = ({ pos, label, matched, index }) => {
  // Render as <foreignObject> for HTML-text rendering inside SVG.
  // Width/height in SVG units (viewBox 0..100).
  const width = 30;
  const height = 12;
  const x = pos.x - width / 2;
  const y = pos.y - height / 2;
  return (
    <motion.g
      initial={{ opacity: 0.4 }}
      animate={{ opacity: matched ? 1 : 0.55 }}
      transition={{ duration: 0.3 }}
    >
      {matched && (
        <motion.circle
          cx={pos.x}
          cy={pos.y}
          r="4"
          fill={TEAL}
          opacity="0.45"
          animate={{ scale: [1, 1.4, 1], opacity: [0.45, 0.0, 0.45] }}
          transition={{ duration: 2, repeat: Infinity, delay: index * 0.15, ease: 'easeOut' }}
          style={{ transformOrigin: `${pos.x}px ${pos.y}px` }}
        />
      )}
      <foreignObject x={x} y={y} width={width} height={height}>
        <div
          className="font-sans"
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: matched ? TEAL : 'rgba(63, 59, 54, 0.85)',
            color: '#FFFFFF',
            border: `0.4px solid ${matched ? '#FFFFFF' : '#5a5550'}`,
            borderRadius: 1.5,
            padding: '0.6px 1.2px',
            fontSize: '2.4px',
            fontWeight: 600,
            textAlign: 'center',
            lineHeight: 1.15,
            overflow: 'hidden',
            wordBreak: 'break-word',
            boxShadow: matched ? `0 0 4px ${TEAL}` : 'none',
            transition: 'background-color 0.3s, border-color 0.3s',
          }}
        >
          {label}
        </div>
      </foreignObject>
    </motion.g>
  );
};

// ─── Missed phrases panel ─────────────────────────────────────────────

const MissedPhrases: React.FC<{
  question: PhraseMatchQuestion;
  matchMap: Record<string, string | null>;
}> = ({ question, matchMap }) => {
  const missed = question.keys.filter(k => !matchMap[k.id]);
  if (missed.length === 0) return null;
  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '20px 24px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: WARN, marginBottom: 12 }}>
        Phrases the marker is still hunting
      </p>
      <div className="space-y-2">
        {missed.map(k => (
          <div
            key={k.id}
            className="rounded-lg"
            style={{
              backgroundColor: `${WARN}10`,
              border: `1.5px solid ${WARN}`,
              padding: '12px 14px',
            }}
          >
            <p className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: INK, marginBottom: 4 }}>
              &ldquo;{k.canonical}&rdquo;
            </p>
            <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550', marginBottom: 6, lineHeight: 1.55 }}>
              {k.rationale}
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginRight: 4 }}>
                acceptable paraphrases:
              </span>
              {k.acceptable.slice(0, 4).map(p => (
                <span
                  key={p}
                  className="font-sans"
                  style={{
                    fontSize: 11,
                    color: TEAL_DARK,
                    backgroundColor: '#FFFFFF',
                    border: `1px solid ${TEAL}66`,
                    borderRadius: 4,
                    padding: '2px 7px',
                  }}
                >
                  {p}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

// ─── Reverse mode ─────────────────────────────────────────────────────

const ReverseMode: React.FC<{
  question: PhraseMatchQuestion;
  order: string[];
  setOrder: (o: string[]) => void;
}> = ({ question, order, setOrder }) => {
  const remaining = question.keys.filter(k => !order.includes(k.id));
  const ordered = order.map(id => question.keys.find(k => k.id === id)!).filter(Boolean);
  const allUsed = order.length === question.keys.length;

  const addPhrase = (id: string) => setOrder([...order, id]);
  const removePhrase = (id: string) => setOrder(order.filter(o => o !== id));
  const reset = () => setOrder([]);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '24px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Build the model answer
        </p>
        <button
          type="button"
          onClick={reset}
          className="font-sans"
          style={{ fontSize: 11.5, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
        >
          Reset
        </button>
      </div>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#5a5550', marginBottom: 16, lineHeight: 1.55 }}>
        Click each phrase in the order you would put it in your answer. Phrases out of order count for marks but a coherent sequence is what separates the top band.
      </p>

      {/* Available phrases */}
      <div className="mb-4">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginBottom: 6 }}>
          Phrases · {remaining.length} remaining
        </p>
        <div className="flex flex-wrap gap-1.5">
          {remaining.map(k => (
            <button
              key={k.id}
              type="button"
              onClick={() => addPhrase(k.id)}
              className="font-serif rounded-md"
              style={{
                backgroundColor: '#FFFFFF',
                color: INK,
                border: `1.5px solid ${INK}`,
                padding: '7px 11px',
                fontSize: 12.5,
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              {k.canonical}
            </button>
          ))}
          {remaining.length === 0 && (
            <span className="font-sans" style={{ fontSize: 12, color: '#9e9186', fontStyle: 'italic' }}>
              All phrases placed.
            </span>
          )}
        </div>
      </div>

      {/* Ordered slots */}
      <div className="mb-4">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginBottom: 6 }}>
          Your sequence · {order.length} placed
        </p>
        <div className="space-y-1.5">
          {ordered.map((k, i) => (
            <div
              key={k.id}
              className="rounded-lg flex items-center gap-3"
              style={{
                backgroundColor: CREAM,
                border: `1.5px solid ${TEAL}`,
                padding: '10px 12px',
              }}
            >
              <span
                className="font-serif inline-flex items-center justify-center"
                style={{
                  backgroundColor: TEAL,
                  color: '#FFFFFF',
                  borderRadius: 999,
                  width: 24,
                  height: 24,
                  fontSize: 12,
                  fontWeight: 700,
                  flexShrink: 0,
                }}
              >
                {i + 1}
              </span>
              <p className="font-serif flex-1" style={{ fontSize: 13.5, color: INK, lineHeight: 1.5 }}>
                {k.canonical}
              </p>
              <button
                type="button"
                onClick={() => removePhrase(k.id)}
                className="font-sans"
                style={{ fontSize: 11, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
              >
                Remove
              </button>
            </div>
          ))}
          {ordered.length === 0 && (
            <p className="font-sans" style={{ fontSize: 12, color: '#9e9186', fontStyle: 'italic' }}>
              Click a phrase above to start building your sequence.
            </p>
          )}
        </div>
      </div>

      {allUsed && <ReverseDiagnostic question={question} order={order} />}
    </section>
  );
};

const ReverseDiagnostic: React.FC<{ question: PhraseMatchQuestion; order: string[] }> = ({ question, order }) => {
  const modelOrder = question.keys.map(k => k.id);
  const correctPositions = order.filter((id, i) => modelOrder[i] === id).length;
  const orderQuality = Math.round((correctPositions / order.length) * 100);

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="rounded-xl"
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '18px 20px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85, marginBottom: 6 }}>
        Sequence diagnostic
      </p>
      <h4 className="font-serif" style={{ fontSize: 16, fontWeight: 600, lineHeight: 1.4 }}>
        All {order.length} phrases placed · {orderQuality}% match the model order.
      </h4>
      <p className="font-sans" style={{ fontSize: 12.5, color: '#E8E4DE', marginTop: 8, lineHeight: 1.55 }}>
        {orderQuality === 100
          ? 'Both completeness and coherence achieved. The marker reads this paragraph in the same order they read the marking scheme.'
          : orderQuality >= 60
          ? 'Phrases all present, sequence partially aligned. Re-read the model below — the order matters because each phrase sets up the next.'
          : 'Phrases all used but the order doesn\'t flow. The model order builds: definition first, then mechanism, then conditions.'}
      </p>
      <div className="mt-4">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#FFD8A8', opacity: 0.85, marginBottom: 6 }}>
          Model paragraph
        </p>
        <p className="font-serif" style={{ fontSize: 13, color: '#E8E4DE', lineHeight: 1.65, fontStyle: 'italic' }}>
          {question.modelAnswer}
        </p>
      </div>
    </motion.div>
  );
};

// ─── Match logic ──────────────────────────────────────────────────────

/** Returns a map of keyId → matched substring (or null). Case-insensitive
 *  substring match against the canonical phrase or any acceptable
 *  paraphrase. */
function computeMatches(answer: string, keys: PhraseMatchKey[]): Record<string, string | null> {
  const lower = answer.toLowerCase();
  const result: Record<string, string | null> = {};
  for (const k of keys) {
    const candidates = [k.canonical, ...k.acceptable];
    let hit: string | null = null;
    for (const c of candidates) {
      const cl = c.toLowerCase();
      if (cl && lower.includes(cl)) {
        hit = c;
        break;
      }
    }
    result[k.id] = hit;
  }
  return result;
}

export default PhraseMatch;
