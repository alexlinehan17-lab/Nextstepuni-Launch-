/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Comparative Texts Linker (Stage 3.1, E18).
 *
 * Integration grid with cross-text SVG threading. Six sample comparative
 * questions across the four LC English Comparative modes. Each question
 * has a curated point bank — a mix of integrated points (touching all
 * three texts) and serial points (one or two texts). The student builds
 * an answer by selecting points; the visualisation above is a 3-column
 * thread canvas where each selected point draws an SVG path connecting
 * the columns it engages with. Integrated points draw full threads; the
 * thread density across the canvas is the visualisation of integration
 * quality.
 *
 * Diagnostic: integration ratio + connecting-verb analysis. The 2013
 * English Chief Examiner Report flagged serial treatment as the
 * dominant cap on Comparative grades.
 *
 * Counter-factual: every serial point in the bank has an `integratedRewrite`
 * field. A "show integrated rewrite" button on each selected serial
 * point reveals the rewritten version, threading in the missing texts.
 *
 * Source: dossier § B1 (English Comparative — analytical fashion),
 * § A5 (three-text rule).
 *
 * Aesthetic: Stage 2/3 register — 2px #1a1a1a borders, cream insets,
 * SVG cubic-Bézier threads via Framer Motion path drawing.
 */

import React, { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { COMPARATIVE_QUESTIONS } from '../../../../data/knowledge/comparativeQuestions';
import {
  type ComparativeQuestion,
  type ComparativePoint,
  type ComparativeMode,
} from '../../../../types/knowledge';
import { writePattern } from '../knowledgePatterns';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

const MODE_LABELS: Record<ComparativeMode, string> = {
  'theme': 'Theme / Issue',
  'cultural-context': 'Cultural Context',
  'general-vision': 'General Vision and Viewpoint',
  'literary-genre': 'Literary Genre',
};

interface Props {
  onBack: () => void;
}

const ComparativeTextsLinker: React.FC<Props> = ({ onBack }) => {
  const [questionId, setQuestionId] = useState<string>(COMPARATIVE_QUESTIONS[0].id);
  const question = useMemo(() => COMPARATIVE_QUESTIONS.find(q => q.id === questionId)!, [questionId]);

  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [showRewriteFor, setShowRewriteFor] = useState<string | null>(null);

  const switchQuestion = (id: string) => {
    setQuestionId(id);
    setSelected(new Set());
    setShowRewriteFor(null);
  };

  const toggle = (pointId: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(pointId)) next.delete(pointId); else next.add(pointId);
      return next;
    });
    setShowRewriteFor(null);
  };

  const selectedPoints = useMemo(
    () => Array.from(selected).map(id => question.pointBank.find(p => p.id === id)!).filter(Boolean),
    [selected, question.pointBank],
  );

  const integratedCount = selectedPoints.filter(p => p.textsTouched.length === question.texts.length).length;
  const serialCount = selectedPoints.filter(p => p.textsTouched.length === 1).length;
  const partialCount = selectedPoints.filter(p => p.textsTouched.length === 2).length;
  const integrationRatio = selectedPoints.length === 0
    ? 0
    : Math.round((integratedCount / selectedPoints.length) * 100);

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <QuestionPicker
        questions={COMPARATIVE_QUESTIONS}
        activeId={questionId}
        onChange={switchQuestion}
      />

      <QuestionFrame question={question} />

      <ThreadCanvas question={question} selectedPoints={selectedPoints} />

      <PointBank
        question={question}
        selected={selected}
        onToggle={toggle}
        showRewriteFor={showRewriteFor}
        setShowRewriteFor={setShowRewriteFor}
      />

      {selectedPoints.length > 0 && (
        <Diagnostic
          integratedCount={integratedCount}
          partialCount={partialCount}
          serialCount={serialCount}
          integrationRatio={integrationRatio}
          selectedPoints={selectedPoints}
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
      Necessary Knowledge · Stage 3 · English
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Comparative Texts Linker.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      Comparative answers fail when each paragraph is about one text at a time. The 2013 English Chief Examiner Report
      flagged serial treatment as the dominant cap on Comparative grades. Build your answer; watch your points either
      thread across the three texts or sit isolated in a single column.
    </p>
  </header>
);

// ─── Question picker ───────────────────────────────────────────────────

const QuestionPicker: React.FC<{
  questions: ComparativeQuestion[];
  activeId: string;
  onChange: (id: string) => void;
}> = ({ questions, activeId, onChange }) => (
  <div className="grid sm:grid-cols-2 gap-2">
    {questions.map(q => {
      const active = q.id === activeId;
      return (
        <button
          key={q.id}
          type="button"
          onClick={() => onChange(q.id)}
          className="text-left rounded-xl"
          style={{
            backgroundColor: active ? INK : '#FFFFFF',
            color: active ? '#FFFFFF' : INK,
            border: `2px solid ${INK}`,
            padding: '11px 14px',
            cursor: 'pointer',
          }}
        >
          <p className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7, marginBottom: 2 }}>
            {MODE_LABELS[q.mode]}
          </p>
          <p className="font-serif" style={{ fontSize: 13, fontWeight: 600, lineHeight: 1.35 }}>
            {q.texts.map(t => t.label).join(' · ')}
          </p>
        </button>
      );
    })}
  </div>
);

// ─── Question frame ────────────────────────────────────────────────────

const QuestionFrame: React.FC<{ question: ComparativeQuestion }> = ({ question }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '20px 24px' }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Question · {MODE_LABELS[question.mode]}
    </p>
    <p className="font-serif" style={{ fontSize: 16, fontWeight: 500, color: INK, lineHeight: 1.5, fontStyle: 'italic' }}>
      &ldquo;{question.questionPrompt}&rdquo;
    </p>
  </section>
);

// ─── Thread canvas ─────────────────────────────────────────────────────

const COL_DOT_RADIUS = 9;
const CANVAS_HEIGHT = 200;
const COL_TOP_Y = 30;

const ThreadCanvas: React.FC<{
  question: ComparativeQuestion;
  selectedPoints: ComparativePoint[];
}> = ({ question, selectedPoints }) => {
  const cols = question.texts;
  const colCenters = useMemo(
    () => cols.map((_, i) => ((i + 1) / (cols.length + 1)) * 100), // percentage X positions
    [cols],
  );

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: CREAM,
        border: `2px solid ${INK}`,
        padding: '24px 26px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-4 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Thread canvas
        </p>
        <span className="font-sans" style={{ fontSize: 11.5, color: '#5a5550' }}>
          {selectedPoints.length === 0 ? 'Pick points below — threads weave between texts.' : `${selectedPoints.length} point${selectedPoints.length === 1 ? '' : 's'} on the canvas`}
        </span>
      </div>

      {/* Column headers */}
      <div className="grid gap-3 mb-3" style={{ gridTemplateColumns: `repeat(${cols.length}, 1fr)` }}>
        {cols.map(t => (
          <div key={t.id} className="text-center">
            <p className="font-serif" style={{ fontSize: 14, fontWeight: 700, color: INK }}>{t.label}</p>
            <p className="font-sans" style={{ fontSize: 10.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginTop: 1 }}>
              {t.formLabel}
            </p>
          </div>
        ))}
      </div>

      {/* SVG canvas */}
      <div style={{ position: 'relative', height: CANVAS_HEIGHT, width: '100%' }}>
        <svg
          viewBox={`0 0 100 ${CANVAS_HEIGHT}`}
          preserveAspectRatio="none"
          width="100%"
          height={CANVAS_HEIGHT}
          style={{ display: 'block' }}
          aria-hidden
        >
          {/* Column trunk lines */}
          {colCenters.map((cx, i) => (
            <line
              key={i}
              x1={cx}
              y1={COL_TOP_Y}
              x2={cx}
              y2={CANVAS_HEIGHT - 10}
              stroke="#d0cdc8"
              strokeWidth="0.3"
              strokeDasharray="0.8 1"
            />
          ))}

          {/* Threads — one per selected point */}
          {selectedPoints.map((point, i) => {
            const yOffset = COL_TOP_Y + 18 + (i * 22);
            const yClamped = Math.min(yOffset, CANVAS_HEIGHT - 22);
            const touched = cols
              .map((c, ci) => ({ idx: ci, cx: colCenters[ci], touched: point.textsTouched.includes(c.id) }))
              .filter(c => c.touched);
            return (
              <ThreadGroup key={point.id} colCenters={colCenters} cols={cols} touched={touched} y={yClamped} pointIndex={i} />
            );
          })}

          {/* Column dots (always visible above threads) */}
          {colCenters.map((cx, i) => (
            <circle
              key={`dot-${i}`}
              cx={cx}
              cy={COL_TOP_Y}
              r="0.8"
              fill={INK}
            />
          ))}
        </svg>
      </div>
    </section>
  );
};

const ThreadGroup: React.FC<{
  colCenters: number[];
  cols: ComparativeQuestion['texts'];
  touched: { idx: number; cx: number; touched: boolean }[];
  y: number;
  pointIndex: number;
}> = ({ colCenters, touched, y, pointIndex }) => {
  const fullyIntegrated = touched.length === colCenters.length;
  const partial = touched.length === 2;
  const serial = touched.length === 1;

  const colour = fullyIntegrated ? TEAL : partial ? TEAL_DARK : '#9e9186';
  const strokeWidth = fullyIntegrated ? 0.7 : partial ? 0.5 : 0.4;
  const opacity = fullyIntegrated ? 0.95 : partial ? 0.55 : 0.4;

  // Build the thread path — connect touched columns left-to-right with cubic curves.
  const sorted = touched.slice().sort((a, b) => a.cx - b.cx);

  // Dot at each touched column
  return (
    <motion.g
      initial={{ opacity: 0 }}
      animate={{ opacity }}
      transition={{ duration: 0.45, ease: 'easeOut', delay: pointIndex * 0.05 }}
    >
      {/* Connecting curve for 2+ touched columns */}
      {sorted.length >= 2 && (
        <motion.path
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.05 + pointIndex * 0.05 }}
          d={buildCurve(sorted.map(s => s.cx), y)}
          stroke={colour}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
        />
      )}
      {/* Touched dots — all the same colour as the thread */}
      {sorted.map((s, i) => (
        <motion.circle
          key={i}
          cx={s.cx}
          cy={y}
          r={fullyIntegrated ? 1.3 : partial ? 1.1 : 1.0}
          fill={colour}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 280, damping: 18, delay: pointIndex * 0.05 + i * 0.04 }}
        />
      ))}
      {/* Serial: render a small dashed isolation indicator */}
      {serial && (
        <circle cx={sorted[0].cx} cy={y} r={2.5} stroke={colour} strokeWidth="0.25" strokeDasharray="0.5 0.4" fill="none" />
      )}
    </motion.g>
  );
};

function buildCurve(xs: number[], y: number): string {
  if (xs.length < 2) return '';
  // For each adjacent pair build a small dip below y to make the thread look woven.
  let d = `M ${xs[0]} ${y}`;
  for (let i = 1; i < xs.length; i++) {
    const x0 = xs[i - 1];
    const x1 = xs[i];
    const cx0 = x0 + (x1 - x0) * 0.35;
    const cx1 = x0 + (x1 - x0) * 0.65;
    const dipY = y + 8;
    d += ` C ${cx0} ${dipY}, ${cx1} ${dipY}, ${x1} ${y}`;
  }
  return d;
}

// ─── Point bank ────────────────────────────────────────────────────────

const PointBank: React.FC<{
  question: ComparativeQuestion;
  selected: Set<string>;
  onToggle: (id: string) => void;
  showRewriteFor: string | null;
  setShowRewriteFor: (id: string | null) => void;
}> = ({ question, selected, onToggle, showRewriteFor, setShowRewriteFor }) => (
  <section
    className="rounded-2xl"
    style={{ backgroundColor: '#FFFFFF', border: `2px solid ${INK}`, padding: '22px 24px' }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Point bank
    </p>
    <p className="font-sans" style={{ fontSize: 12.5, color: '#5a5550', marginBottom: 14, lineHeight: 1.55 }}>
      Pick the points you would put in your answer. Watch the canvas above — fully-threaded points (touching all three texts) integrate; one- or two-text points stay isolated. Every serial point can be rewritten as integrated.
    </p>
    <div className="space-y-2">
      {question.pointBank.map(point => (
        <PointCard
          key={point.id}
          point={point}
          texts={question.texts}
          selected={selected.has(point.id)}
          onToggle={() => onToggle(point.id)}
          showRewrite={showRewriteFor === point.id}
          onToggleRewrite={() => setShowRewriteFor(showRewriteFor === point.id ? null : point.id)}
        />
      ))}
    </div>
  </section>
);

const PointCard: React.FC<{
  point: ComparativePoint;
  texts: ComparativeQuestion['texts'];
  selected: boolean;
  onToggle: () => void;
  showRewrite: boolean;
  onToggleRewrite: () => void;
}> = ({ point, texts, selected, onToggle, showRewrite, onToggleRewrite }) => {
  const integrationLevel: 'integrated' | 'partial' | 'serial' =
    point.textsTouched.length === texts.length ? 'integrated' :
    point.textsTouched.length === 1 ? 'serial' : 'partial';
  const hasRewrite = !!point.integratedRewrite;

  const tagColour = integrationLevel === 'integrated' ? TEAL : integrationLevel === 'partial' ? TEAL_DARK : WARN;
  const tagLabel = integrationLevel === 'integrated' ? 'Integrated' : integrationLevel === 'partial' ? 'Partial' : 'Serial';

  return (
    <article
      className="rounded-xl"
      style={{
        backgroundColor: selected ? `${TEAL}10` : '#FFFFFF',
        border: `1.5px solid ${selected ? TEAL : '#d0cdc8'}`,
        padding: '14px 16px',
      }}
    >
      <div className="flex items-start gap-3">
        <button
          type="button"
          onClick={onToggle}
          aria-pressed={selected}
          className="shrink-0"
          style={{
            width: 22,
            height: 22,
            borderRadius: 6,
            border: `1.5px solid ${selected ? TEAL : '#9e9186'}`,
            backgroundColor: selected ? TEAL : '#FFFFFF',
            cursor: 'pointer',
            marginTop: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {selected && (
            <svg width="13" height="13" viewBox="0 0 12 12" fill="none" aria-hidden>
              <path d="M3 6L5 8L9 4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          )}
        </button>
        <div className="flex-1">
          <div className="flex items-baseline gap-2 flex-wrap mb-1">
            <span
              className="font-sans"
              style={{
                fontSize: 9.5,
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: 0.5,
                color: tagColour,
                backgroundColor: `${tagColour}15`,
                border: `1px solid ${tagColour}66`,
                borderRadius: 999,
                padding: '2px 8px',
              }}
            >
              {tagLabel}
            </span>
            <span className="font-sans" style={{ fontSize: 10.5, color: '#9e9186' }}>
              touches: {point.textsTouched.map(id => texts.find(t => t.id === id)?.label ?? id).join(', ')}
            </span>
          </div>
          <p className="font-serif" style={{ fontSize: 14, color: INK, lineHeight: 1.55 }}>
            {point.text}
          </p>
          <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550', marginTop: 6, lineHeight: 1.5, fontStyle: 'italic' }}>
            {point.rationale}
          </p>
          {point.connectingVerbs && point.connectingVerbs.length > 0 && (
            <div className="flex items-center gap-1.5 mt-2 flex-wrap">
              <span className="font-sans" style={{ fontSize: 10, color: '#9e9186' }}>connecting verbs:</span>
              {point.connectingVerbs.map(v => (
                <span
                  key={v}
                  className="font-sans"
                  style={{
                    fontSize: 10.5,
                    fontWeight: 600,
                    color: TEAL_DARK,
                    backgroundColor: `${TEAL}15`,
                    borderRadius: 4,
                    padding: '1px 6px',
                  }}
                >
                  {v}
                </span>
              ))}
            </div>
          )}

          {hasRewrite && (
            <button
              type="button"
              onClick={onToggleRewrite}
              className="font-sans"
              style={{
                marginTop: 8,
                fontSize: 11.5,
                fontWeight: 600,
                color: TEAL,
                backgroundColor: 'transparent',
                border: `1px dashed ${TEAL}`,
                borderRadius: 999,
                padding: '4px 10px',
                cursor: 'pointer',
              }}
            >
              {showRewrite ? 'Hide rewrite' : 'Show integrated rewrite'}
            </button>
          )}

          {showRewrite && hasRewrite && (
            <motion.div
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25 }}
              className="rounded-lg mt-3"
              style={{
                backgroundColor: CREAM,
                border: `1.5px solid ${TEAL}`,
                padding: '10px 12px',
              }}
            >
              <p className="font-sans" style={{ fontSize: 9.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: TEAL, marginBottom: 4 }}>
                Integrated rewrite
              </p>
              <p className="font-serif" style={{ fontSize: 13, color: INK, lineHeight: 1.55 }}>
                {point.integratedRewrite}
              </p>
            </motion.div>
          )}
        </div>
      </div>
    </article>
  );
};

// ─── Diagnostic ────────────────────────────────────────────────────────

const Diagnostic: React.FC<{
  integratedCount: number;
  partialCount: number;
  serialCount: number;
  integrationRatio: number;
  selectedPoints: ComparativePoint[];
}> = ({ integratedCount, partialCount, serialCount, integrationRatio, selectedPoints }) => {
  // Pull the connecting-verb words from selected integrated points
  const connectingVerbs = useMemo(() => {
    const set = new Set<string>();
    selectedPoints.forEach(p => {
      if (p.textsTouched.length >= 2 && p.connectingVerbs) {
        p.connectingVerbs.forEach(v => set.add(v));
      }
    });
    return Array.from(set);
  }, [selectedPoints]);

  // Persist integration ratio to localStorage for the cross-module "Your patterns" panel.
  useEffect(() => {
    if (selectedPoints.length < 3) return;
    writePattern('comparative', {
      avgIntegrationRatio: integrationRatio,
      sampleSize: selectedPoints.length,
      updatedAt: Date.now(),
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [integrationRatio, selectedPoints.length]);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '28px 30px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Integration diagnostic
      </p>
      <div className="flex items-baseline gap-4 mt-2 flex-wrap">
        <div>
          <span className="font-serif" style={{ fontSize: 38, fontWeight: 700, color: '#FFFFFF' }}>
            {integrationRatio}%
          </span>
          <span className="font-sans" style={{ fontSize: 12.5, color: '#FFD8A8', marginLeft: 8, opacity: 0.85 }}>
            integration ratio
          </span>
        </div>
        <div className="flex items-baseline gap-3 flex-wrap">
          <Badge label="Integrated" count={integratedCount} colour={TEAL} />
          <Badge label="Partial (2-text)" count={partialCount} colour={TEAL_DARK} />
          <Badge label="Serial (1-text)" count={serialCount} colour={WARN} />
        </div>
      </div>

      <p className="font-sans" style={{ fontSize: 13, color: '#E8E4DE', marginTop: 16, lineHeight: 1.6 }}>
        {integrationRatio >= 80
          ? 'You are reading the question like an examiner. H1 answers run at 80%+ — every paragraph operates on three texts at once.'
          : integrationRatio >= 50
          ? 'Mid-band integration. The 2013 English CER described top answers as "analytical fashion" — meaning every paragraph holds the three texts together. Your gap is the connecting verb.'
          : selectedPoints.length === 0
          ? ''
          : `Most of your selected points are serial. Each serial point has an integrated rewrite — the move is to use connecting verbs as load-bearing words. ${selectedPoints.filter(p => p.integratedRewrite).length} of your points have a rewrite available.`}
      </p>

      {connectingVerbs.length > 0 && (
        <div className="mt-4">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#FFD8A8', opacity: 0.75, marginBottom: 6 }}>
            Connecting verbs in your answer
          </p>
          <div className="flex items-center gap-1.5 flex-wrap">
            {connectingVerbs.map(v => (
              <span
                key={v}
                className="font-sans"
                style={{
                  fontSize: 11,
                  fontWeight: 600,
                  color: TEAL,
                  backgroundColor: 'rgba(42,125,111,0.18)',
                  borderRadius: 4,
                  padding: '2px 8px',
                }}
              >
                {v}
              </span>
            ))}
          </div>
        </div>
      )}
    </section>
  );
};

const Badge: React.FC<{ label: string; count: number; colour: string }> = ({ label, count, colour }) => (
  <div
    className="font-sans"
    style={{
      fontSize: 11,
      fontWeight: 700,
      color: '#FFFFFF',
      backgroundColor: colour,
      borderRadius: 999,
      padding: '4px 11px',
    }}
  >
    {count} · {label}
  </div>
);

export default ComparativeTextsLinker;
