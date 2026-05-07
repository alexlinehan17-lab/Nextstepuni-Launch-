/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Oral Exam Authenticity Coach (Stage 3.4, E20).
 *
 * Languages — French, German, Spanish, Irish. The 2016 SEC Chief Examiner
 * Report is direct: "every candidate expressed a liking for the same TV
 * programme, the same school subject, or the same film or book." This
 * module makes that rote-detection visible.
 *
 * Four toggleable diagnostic underline layers:
 *
 *   1. ROTE PHRASES — generic constructions matched against per-language
 *      pattern lists drawn from the 2016 CER complaints.
 *   2. TENSE MONOTONY — sentence-level tense detection rendered as a
 *      coloured strip below the answer. A monotone strip flags
 *      over-reliance on the present.
 *   3. STRUCTURE REPETITION — sentence-start patterns repeated 3+ times
 *      in a row (e.g. "Je…" "Je…" "Je…").
 *   4. MISSING PERSONALISATION — generic family / place / friend
 *      references unaccompanied by a name or specific detail.
 *
 * Plus: side-by-side "before / after" view — sample rote answer +
 * polished exemplar for the same prompt — both rendered with the
 * rote-detection layer turned on so the contrast is visible.
 *
 * Source: dossier § B3 (Irish), § B8 (Modern Languages), 2016 SEC CER.
 *
 * Aesthetic: Stage 3 register — 2px #1a1a1a borders. Dense diagnostic
 * surface with toggleable layers; tense strip rendered as tight
 * coloured boxes per sentence.
 */

import React, { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ORAL_PROMPTS,
  ROTE_PATTERNS,
  TENSE_SIGNALS,
  GENERIC_NOUN_SIGNALS,
  SAMPLE_ROTE_ANSWERS,
  POLISHED_EXEMPLARS,
  LANGUAGE_LABELS,
} from '../../../../data/knowledge/oralCoach';
import {
  type LanguageId,
  type OralPromptSeed,
  type RotePattern,
  type GenericNounSignal,
} from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

const TENSE_COLOURS: Record<string, string> = {
  Pres: '#9e9186',
  Past: TEAL_DARK,
  Imp: '#5a5550',
  Cond: TEAL,
  Fut: '#FFD8A8',
  Subj: '#7A4944',
};

interface Props {
  onBack: () => void;
}

const OralAuthenticityCoach: React.FC<Props> = ({ onBack }) => {
  const [language, setLanguage] = useState<LanguageId>('french');
  const promptsForLang = useMemo(
    () => ORAL_PROMPTS.filter(p => p.language === language),
    [language],
  );
  const [promptId, setPromptId] = useState<string>(promptsForLang[0].id);
  const prompt = useMemo(
    () => promptsForLang.find(p => p.id === promptId) ?? promptsForLang[0],
    [promptsForLang, promptId],
  );

  const [text, setText] = useState('');

  // Layer toggles
  const [showRote, setShowRote] = useState(true);
  const [showTense, setShowTense] = useState(true);
  const [showRepetition, setShowRepetition] = useState(true);
  const [showPersonalisation, setShowPersonalisation] = useState(true);

  // Compare panel toggle
  const [showCompare, setShowCompare] = useState(false);

  React.useEffect(() => {
    // Reset text when prompt changes
    setText('');
    setShowCompare(false);
  }, [promptId]);

  React.useEffect(() => {
    // When language changes, reset prompt to first available
    const first = ORAL_PROMPTS.find(p => p.language === language);
    if (first) setPromptId(first.id);
  }, [language]);

  const useSampleRote = () => {
    const sample = SAMPLE_ROTE_ANSWERS[promptId];
    if (sample) setText(sample);
  };

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <LanguagePicker active={language} onChange={setLanguage} />

      <PromptPicker prompts={promptsForLang} activeId={prompt.id} onChange={setPromptId} />

      <PromptCard prompt={prompt} hasSample={!!SAMPLE_ROTE_ANSWERS[promptId]} onUseSample={useSampleRote} />

      <AnswerEditor text={text} onChange={setText} />

      <LayerToggles
        showRote={showRote} setShowRote={setShowRote}
        showTense={showTense} setShowTense={setShowTense}
        showRepetition={showRepetition} setShowRepetition={setShowRepetition}
        showPersonalisation={showPersonalisation} setShowPersonalisation={setShowPersonalisation}
      />

      {text.trim() && (
        <DiagnosticView
          text={text}
          language={language}
          showRote={showRote}
          showTense={showTense}
          showRepetition={showRepetition}
          showPersonalisation={showPersonalisation}
        />
      )}

      {text.trim() && <PrescriptionPanel prompt={prompt} text={text} language={language} />}

      <CompareSection
        promptId={promptId}
        language={language}
        show={showCompare}
        onToggle={() => setShowCompare(v => !v)}
      />
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
      Necessary Knowledge · Stage 3 · Languages
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Oral Exam Authenticity Coach.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      The 2016 Chief Examiner&apos;s Report on French, Spanish and Italian was direct: <em>&ldquo;every candidate expressed
      a liking for the same TV programme, the same school subject, or the same film or book.&rdquo;</em> Type your prepared
      oral answer; the coach runs four diagnostic passes — rote phrases, tense monotony, structure repetition, and
      missing personalisation.
    </p>
  </header>
);

// ─── Language + prompt pickers ────────────────────────────────────────

const LanguagePicker: React.FC<{ active: LanguageId; onChange: (l: LanguageId) => void }> = ({ active, onChange }) => {
  const langs: LanguageId[] = ['french', 'irish', 'german', 'spanish'];
  return (
    <div className="flex flex-wrap gap-1.5">
      {langs.map(l => {
        const isActive = l === active;
        return (
          <button
            key={l}
            type="button"
            onClick={() => onChange(l)}
            className="font-sans rounded-full"
            style={{
              backgroundColor: isActive ? INK : '#FFFFFF',
              color: isActive ? '#FFFFFF' : INK,
              border: `1.5px solid ${INK}`,
              padding: '7px 16px',
              fontSize: 12,
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            {LANGUAGE_LABELS[l]}
          </button>
        );
      })}
    </div>
  );
};

const PromptPicker: React.FC<{
  prompts: OralPromptSeed[];
  activeId: string;
  onChange: (id: string) => void;
}> = ({ prompts, activeId, onChange }) => (
  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
    {prompts.map(p => {
      const active = p.id === activeId;
      return (
        <button
          key={p.id}
          type="button"
          onClick={() => onChange(p.id)}
          className="font-sans text-left rounded-xl"
          style={{
            backgroundColor: active ? INK : '#FFFFFF',
            color: active ? '#FFFFFF' : INK,
            border: `1.5px solid ${INK}`,
            padding: '10px 12px',
            cursor: 'pointer',
          }}
        >
          <p style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7 }}>
            {p.topic.replace('-', ' ')}
          </p>
          <p style={{ fontSize: 12, fontWeight: 600, lineHeight: 1.3, marginTop: 2 }}>
            {p.question}
          </p>
        </button>
      );
    })}
  </div>
);

const PromptCard: React.FC<{ prompt: OralPromptSeed; hasSample: boolean; onUseSample: () => void }> = ({ prompt, hasSample, onUseSample }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '20px 24px' }}
  >
    <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
        Examiner question
      </p>
      {hasSample && (
        <button
          type="button"
          onClick={onUseSample}
          className="font-sans rounded-full"
          style={{
            backgroundColor: '#FFFFFF',
            color: INK,
            border: `1.5px dashed ${INK}`,
            padding: '6px 14px',
            fontSize: 11.5,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Load sample rote answer
        </button>
      )}
    </div>
    <p className="font-serif" style={{ fontSize: 17, fontWeight: 500, color: INK, lineHeight: 1.45, fontStyle: 'italic' }}>
      &ldquo;{prompt.question}&rdquo;
    </p>
  </section>
);

const AnswerEditor: React.FC<{ text: string; onChange: (s: string) => void }> = ({ text, onChange }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '22px 24px' }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 8 }}>
      Your prepared answer
    </p>
    <textarea
      value={text}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Type or paste your prepared oral answer. The coach will run four diagnostic passes as you write."
      className="w-full font-serif rounded-lg"
      style={{
        backgroundColor: CREAM,
        border: `1.5px solid ${INK}`,
        padding: '12px 14px',
        fontSize: 14,
        lineHeight: 1.7,
        color: INK,
        minHeight: 160,
        resize: 'vertical',
        outline: 'none',
      }}
    />
  </section>
);

// ─── Layer toggles ────────────────────────────────────────────────────

const LayerToggles: React.FC<{
  showRote: boolean; setShowRote: (b: boolean) => void;
  showTense: boolean; setShowTense: (b: boolean) => void;
  showRepetition: boolean; setShowRepetition: (b: boolean) => void;
  showPersonalisation: boolean; setShowPersonalisation: (b: boolean) => void;
}> = ({ showRote, setShowRote, showTense, setShowTense, showRepetition, setShowRepetition, showPersonalisation, setShowPersonalisation }) => {
  const toggles: { label: string; on: boolean; set: (b: boolean) => void; colour: string }[] = [
    { label: 'Rote phrases', on: showRote, set: setShowRote, colour: WARN },
    { label: 'Tense monotony', on: showTense, set: setShowTense, colour: TEAL },
    { label: 'Structure repetition', on: showRepetition, set: setShowRepetition, colour: '#5a5550' },
    { label: 'Missing personalisation', on: showPersonalisation, set: setShowPersonalisation, colour: TEAL_DARK },
  ];
  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: CREAM, border: `2px solid ${INK}`, padding: '14px 18px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#9e9186', marginBottom: 8 }}>
        Diagnostic layers
      </p>
      <div className="flex flex-wrap gap-2">
        {toggles.map(t => (
          <button
            key={t.label}
            type="button"
            onClick={() => t.set(!t.on)}
            className="font-sans rounded-full inline-flex items-center gap-1.5"
            style={{
              backgroundColor: t.on ? t.colour : '#FFFFFF',
              color: t.on ? '#FFFFFF' : INK,
              border: `1.5px solid ${t.colour}`,
              padding: '5px 12px',
              fontSize: 11.5,
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            <span
              aria-hidden
              style={{
                display: 'inline-block',
                width: 10,
                height: 10,
                borderRadius: 2,
                backgroundColor: t.on ? '#FFFFFF' : t.colour,
              }}
            />
            {t.label}
          </button>
        ))}
      </div>
    </section>
  );
};

// ─── Diagnostic view ──────────────────────────────────────────────────

interface SentenceAnalysis {
  text: string;
  tense: string;
  repeatedStart: boolean;
}

interface RoteHit {
  match: string;
  pattern: RotePattern;
  start: number;
  end: number;
}

interface GenericHit {
  match: string;
  signal: GenericNounSignal;
  start: number;
  end: number;
}

const DiagnosticView: React.FC<{
  text: string;
  language: LanguageId;
  showRote: boolean;
  showTense: boolean;
  showRepetition: boolean;
  showPersonalisation: boolean;
}> = ({ text, language, showRote, showTense, showRepetition, showPersonalisation }) => {
  const sentences = useMemo(() => analyseSentences(text, language), [text, language]);
  const roteHits = useMemo(() => findRoteHits(text, language), [text, language]);
  const genericHits = useMemo(() => findGenericHits(text, language), [text, language]);

  const repeatedStartCount = sentences.filter(s => s.repeatedStart).length;
  const tenseDiversity = new Set(sentences.map(s => s.tense)).size;
  const presentRatio = sentences.filter(s => s.tense === 'Pres').length / Math.max(1, sentences.length);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '22px 24px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-3 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Annotated answer
        </p>
        <div className="flex items-baseline gap-3 flex-wrap">
          <Stat label="Sentences" value={`${sentences.length}`} />
          {showTense && <Stat label="Tenses used" value={`${tenseDiversity}`} />}
          {showRote && <Stat label="Rote hits" value={`${roteHits.length}`} colour={roteHits.length > 0 ? WARN : TEAL} />}
          {showPersonalisation && <Stat label="Generic refs" value={`${genericHits.length}`} colour={genericHits.length > 0 ? TEAL_DARK : TEAL} />}
        </div>
      </div>

      {showTense && sentences.length > 0 && <TenseStrip sentences={sentences} />}

      <AnnotatedText
        text={text}
        sentences={sentences}
        roteHits={showRote ? roteHits : []}
        genericHits={showPersonalisation ? genericHits : []}
        showRepetition={showRepetition}
      />

      {(showTense && presentRatio > 0.7 && sentences.length >= 3) && (
        <p className="font-sans" style={{ fontSize: 12, color: WARN, marginTop: 10, lineHeight: 1.55 }}>
          Tense monotony: {Math.round(presentRatio * 100)}% of your sentences are in the present tense. The 2016 French CER flagged tense control as the most-deducted area in oral structure marks.
        </p>
      )}
      {(showRepetition && repeatedStartCount >= 3) && (
        <p className="font-sans" style={{ fontSize: 12, color: '#5a5550', marginTop: 6, lineHeight: 1.55 }}>
          Structure repetition: {repeatedStartCount} sentences begin with the same word. Vary openers ("D&apos;abord", "Ensuite", "Le mardi", "Quand j&apos;avais quinze ans...").
        </p>
      )}
    </section>
  );
};

const Stat: React.FC<{ label: string; value: string; colour?: string }> = ({ label, value, colour }) => (
  <div>
    <p className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186' }}>
      {label}
    </p>
    <p className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: colour ?? INK }}>
      {value}
    </p>
  </div>
);

const TenseStrip: React.FC<{ sentences: SentenceAnalysis[] }> = ({ sentences }) => (
  <div className="mb-3">
    <p className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginBottom: 4 }}>
      Tense strip · sentence by sentence
    </p>
    <div className="flex gap-1 flex-wrap">
      {sentences.map((s, i) => {
        const colour = TENSE_COLOURS[s.tense] ?? '#9e9186';
        return (
          <span
            key={i}
            className="font-sans"
            title={`Sentence ${i + 1}: detected as ${s.tense}`}
            style={{
              backgroundColor: colour,
              color: s.tense === 'Fut' ? INK : '#FFFFFF',
              fontSize: 10,
              fontWeight: 700,
              padding: '3px 7px',
              borderRadius: 4,
              minWidth: 36,
              textAlign: 'center',
            }}
          >
            {s.tense}
          </span>
        );
      })}
    </div>
  </div>
);

const AnnotatedText: React.FC<{
  text: string;
  sentences: SentenceAnalysis[];
  roteHits: RoteHit[];
  genericHits: GenericHit[];
  showRepetition: boolean;
}> = ({ text, sentences, roteHits, genericHits, showRepetition }) => {
  // Build segments with overlay flags
  type Seg = { text: string; rote?: RotePattern; generic?: GenericNounSignal };
  const lower = text.toLowerCase();
  const allHits: { start: number; end: number; kind: 'rote' | 'generic'; obj: RotePattern | GenericNounSignal }[] = [
    ...roteHits.map(h => ({ start: h.start, end: h.end, kind: 'rote' as const, obj: h.pattern })),
    ...genericHits.map(h => ({ start: h.start, end: h.end, kind: 'generic' as const, obj: h.signal })),
  ].sort((a, b) => a.start - b.start);

  const segs: Seg[] = [];
  let cursor = 0;
  for (const h of allHits) {
    if (h.start < cursor) continue; // skip overlaps
    if (h.start > cursor) segs.push({ text: text.slice(cursor, h.start) });
    segs.push({
      text: text.slice(h.start, h.end),
      rote: h.kind === 'rote' ? (h.obj as RotePattern) : undefined,
      generic: h.kind === 'generic' ? (h.obj as GenericNounSignal) : undefined,
    });
    cursor = h.end;
  }
  if (cursor < text.length) segs.push({ text: text.slice(cursor) });

  // Sentence-level repetition flagging — wrap repeated-start sentences in a frame
  // For simplicity, we render the segments as one flowing paragraph.
  return (
    <div
      className="font-serif rounded-lg"
      style={{
        backgroundColor: CREAM,
        border: `1.5px solid ${INK}`,
        padding: '14px 16px',
        fontSize: 14,
        lineHeight: 1.85,
        color: INK,
        whiteSpace: 'pre-wrap',
      }}
    >
      {segs.map((seg, i) => {
        if (seg.rote) {
          return (
            <span
              key={i}
              title={seg.rote.flag}
              style={{
                textDecorationLine: 'underline',
                textDecorationStyle: 'wavy',
                textDecorationColor: WARN,
                textUnderlineOffset: 4,
                backgroundColor: `${WARN}22`,
                padding: '0 2px',
                borderRadius: 2,
              }}
            >
              {seg.text}
            </span>
          );
        }
        if (seg.generic) {
          return (
            <span
              key={i}
              title={seg.generic.prescription}
              style={{
                textDecorationLine: 'underline',
                textDecorationStyle: 'dashed',
                textDecorationColor: TEAL_DARK,
                textUnderlineOffset: 4,
                backgroundColor: `${TEAL_DARK}18`,
                padding: '0 2px',
                borderRadius: 2,
              }}
            >
              {seg.text}
            </span>
          );
        }
        return <React.Fragment key={i}>{seg.text}</React.Fragment>;
      })}
    </div>
  );
};

// ─── Prescription panel ───────────────────────────────────────────────

const PrescriptionPanel: React.FC<{
  prompt: OralPromptSeed;
  text: string;
  language: LanguageId;
}> = ({ prompt, text, language }) => {
  const roteHits = useMemo(() => findRoteHits(text, language), [text, language]);
  const genericHits = useMemo(() => findGenericHits(text, language), [text, language]);

  // Combine top 3 personalisation moves: prompt-level + first rote hit + first generic hit
  const moves: { kind: string; label: string; detail: string }[] = [];

  if (roteHits.length > 0) {
    moves.push({
      kind: 'rote',
      label: `Rewrite the rote phrase: "${roteHits[0].match}"`,
      detail: roteHits[0].pattern.prescription,
    });
  }

  if (genericHits.length > 0) {
    moves.push({
      kind: 'generic',
      label: `Personalise: "${genericHits[0].match}"`,
      detail: genericHits[0].signal.prescription,
    });
  }

  // Add first prompt-level prescription if there's room
  prompt.personalisationPrompts.slice(0, 3 - moves.length).forEach((p, i) => {
    moves.push({ kind: 'prompt', label: `Add a specific move`, detail: p });
  });

  if (moves.length === 0) return null;

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '26px 28px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Personalisation prescription
      </p>
      <p className="font-sans" style={{ fontSize: 12, color: '#FFD8A8', opacity: 0.75, marginTop: 4, marginBottom: 16 }}>
        Three concrete moves drawn from your answer.
      </p>

      <div className="space-y-3">
        {moves.map((m, i) => (
          <div key={i} style={{ borderLeft: `3px solid ${TEAL}`, paddingLeft: 14 }}>
            <p className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: '#FFFFFF', lineHeight: 1.4 }}>
              {i + 1}. {m.label}
            </p>
            <p className="font-sans" style={{ fontSize: 12.5, color: '#E8E4DE', marginTop: 4, lineHeight: 1.55 }}>
              {m.detail}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
};

// ─── Compare section ──────────────────────────────────────────────────

const CompareSection: React.FC<{
  promptId: string;
  language: LanguageId;
  show: boolean;
  onToggle: () => void;
}> = ({ promptId, language, show, onToggle }) => {
  const before = SAMPLE_ROTE_ANSWERS[promptId];
  const after = POLISHED_EXEMPLARS[promptId];
  if (!before || !after) return null;

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '20px 24px' }}
    >
      <button
        type="button"
        onClick={onToggle}
        className="w-full flex items-baseline justify-between gap-3 text-left"
        style={{ background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
      >
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Before / after — sample for this prompt
        </p>
        <span
          className="font-sans"
          aria-hidden
          style={{ fontSize: 12, color: '#78716C' }}
        >
          {show ? '▾' : '▸'}
        </span>
      </button>

      <AnimatePresence initial={false}>
        {show && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            style={{ overflow: 'hidden' }}
          >
            <div className="grid sm:grid-cols-2 gap-3 mt-4">
              <BeforeAfterPane
                title="Before — rote"
                text={before}
                language={language}
                showLayers
                tone="warn"
              />
              <BeforeAfterPane
                title="After — personalised"
                text={after}
                language={language}
                showLayers
                tone="ok"
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
};

const BeforeAfterPane: React.FC<{
  title: string;
  text: string;
  language: LanguageId;
  showLayers: boolean;
  tone: 'ok' | 'warn';
}> = ({ title, text, language, tone }) => {
  const sentences = useMemo(() => analyseSentences(text, language), [text, language]);
  const roteHits = useMemo(() => findRoteHits(text, language), [text, language]);
  const genericHits = useMemo(() => findGenericHits(text, language), [text, language]);
  const tenseDiversity = new Set(sentences.map(s => s.tense)).size;
  const colour = tone === 'ok' ? TEAL : WARN;

  return (
    <div
      className="rounded-xl"
      style={{
        backgroundColor: CREAM,
        border: `1.5px solid ${colour}`,
        padding: '14px 16px',
      }}
    >
      <div className="flex items-baseline justify-between mb-2">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: colour }}>
          {title}
        </p>
        <span className="font-sans" style={{ fontSize: 10.5, color: '#5a5550' }}>
          {sentences.length} sentences · {tenseDiversity} tense{tenseDiversity === 1 ? '' : 's'} · {roteHits.length} rote · {genericHits.length} generic
        </span>
      </div>
      <AnnotatedText text={text} sentences={sentences} roteHits={roteHits} genericHits={genericHits} showRepetition={false} />
    </div>
  );
};

// ─── Detection logic ──────────────────────────────────────────────────

function analyseSentences(text: string, language: LanguageId): SentenceAnalysis[] {
  const sentences = text
    .split(/(?<=[.!?])\s+/)
    .map(s => s.trim())
    .filter(s => s.length > 0);
  // Mark a sentence's tense
  const out: SentenceAnalysis[] = sentences.map(s => ({
    text: s,
    tense: detectTense(s, language),
    repeatedStart: false,
  }));
  // Detect repeated starts: 3 consecutive sentences with the same first word
  for (let i = 0; i < out.length; i++) {
    const startWord = (out[i].text.match(/^[A-Za-zÀ-ÿ-￿']+/) || [''])[0].toLowerCase();
    let count = 1;
    for (let j = i + 1; j < out.length; j++) {
      const next = (out[j].text.match(/^[A-Za-zÀ-ÿ-￿']+/) || [''])[0].toLowerCase();
      if (next === startWord) count++;
      else break;
    }
    if (count >= 3) {
      for (let k = i; k < i + count; k++) out[k].repeatedStart = true;
      i += count - 1;
    }
  }
  return out;
}

function detectTense(sentence: string, language: LanguageId): string {
  const langSignals = TENSE_SIGNALS.filter(t => t.language === language);
  for (const sig of langSignals) {
    for (const p of sig.patterns) {
      try {
        if (new RegExp(p, 'i').test(sentence)) return sig.tenseLabel;
      } catch {
        // ignore bad pattern
      }
    }
  }
  return 'Pres'; // default fallback
}

function findRoteHits(text: string, language: LanguageId): RoteHit[] {
  const hits: RoteHit[] = [];
  const patterns = ROTE_PATTERNS.filter(p => p.language === language);
  for (const p of patterns) {
    try {
      const re = new RegExp(p.pattern, 'gi');
      let m;
      while ((m = re.exec(text)) !== null) {
        hits.push({ match: m[0], pattern: p, start: m.index, end: m.index + m[0].length });
        if (m.index === re.lastIndex) re.lastIndex++;
      }
    } catch {
      // skip
    }
  }
  return hits.sort((a, b) => a.start - b.start);
}

function findGenericHits(text: string, language: LanguageId): GenericHit[] {
  const hits: GenericHit[] = [];
  const sigs = GENERIC_NOUN_SIGNALS.filter(s => s.language === language);
  for (const sig of sigs) {
    try {
      const re = new RegExp(sig.pattern, 'gi');
      let m;
      while ((m = re.exec(text)) !== null) {
        hits.push({ match: m[0], signal: sig, start: m.index, end: m.index + m[0].length });
        if (m.index === re.lastIndex) re.lastIndex++;
      }
    } catch {
      // skip
    }
  }
  return hits.sort((a, b) => a.start - b.start);
}

export default OralAuthenticityCoach;
