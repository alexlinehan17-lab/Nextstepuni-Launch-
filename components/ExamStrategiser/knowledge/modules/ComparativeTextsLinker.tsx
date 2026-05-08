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
//
// All HTML — no SVG, no viewBox, no aspect-ratio distortion. Each row is
// a strict horizontal stripe. Connecting line is a 0-height div with a
// border-top, spanning leftmost-to-rightmost touched columns. Dots are
// small filled/hollow circles. Each row gets a numeric label on the left.

const HEADER_H = 60;
const ROW_H = 44;
const PADDING_TOP = 14;
const PADDING_BOTTOM = 18;
const MIN_ROWS = 3;
const ROW_LABEL_W = 32;

const ThreadCanvas: React.FC<{
  question: ComparativeQuestion;
  selectedPoints: ComparativePoint[];
}> = ({ question, selectedPoints }) => {
  const cols = question.texts;
  const colCount = cols.length;

  // Column X position. Distribute across the area to the right of the row
  // label (which occupies ROW_LABEL_W on the left).
  const xPercent = (i: number) =>
    `calc(${ROW_LABEL_W}px + (100% - ${ROW_LABEL_W}px) * ${(i + 1) / (colCount + 1)})`;

  const rowsToRender = Math.max(selectedPoints.length, MIN_ROWS);
  const canvasHeight = HEADER_H + PADDING_TOP + rowsToRender * ROW_H + PADDING_BOTTOM;

  const integrationOf = (p: ComparativePoint): 'integrated' | 'partial' | 'serial' =>
    p.textsTouched.length === colCount ? 'integrated' :
    p.textsTouched.length === 1 ? 'serial' : 'partial';
  const colourOf = (kind: 'integrated' | 'partial' | 'serial') =>
    kind === 'integrated' ? TEAL : kind === 'partial' ? TEAL_DARK : WARN;

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: CREAM, border: `2px solid ${INK}`, padding: '22px 26px' }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2 flex-wrap">
        <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
          Thread canvas
        </p>
        <span className="font-sans" style={{ fontSize: 11.5, color: '#5a5550' }}>
          {selectedPoints.length === 0
            ? 'Pick points below — threads weave between texts.'
            : `${selectedPoints.length} point${selectedPoints.length === 1 ? '' : 's'} on the canvas`}
        </span>
      </div>

      <div style={{ position: 'relative', width: '100%', height: canvasHeight }}>
        {/* Column headers */}
        {cols.map((t, i) => (
          <div
            key={t.id}
            style={{
              position: 'absolute',
              left: xPercent(i),
              top: 0,
              transform: 'translateX(-50%)',
              textAlign: 'center',
              minWidth: 90,
            }}
          >
            <p className="font-serif" style={{ fontSize: 14.5, fontWeight: 700, color: INK, lineHeight: 1.15 }}>
              {t.label}
            </p>
            <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186', marginTop: 2 }}>
              {t.formLabel}
            </p>
          </div>
        ))}

        {/* Subtle column trunks — 1px-wide div centered on xPercent via
            translateX(-50%), so the trunk axis aligns exactly with the
            dot centers (which are also translateX(-50%) centered). */}
        {cols.map((_, i) => (
          <div
            key={`trunk-${i}`}
            aria-hidden
            style={{
              position: 'absolute',
              left: xPercent(i),
              transform: 'translateX(-50%)',
              top: HEADER_H - 2,
              bottom: PADDING_BOTTOM / 2,
              width: 1,
              backgroundImage: 'repeating-linear-gradient(to bottom, #dbd6cf 0 3px, transparent 3px 6px)',
            }}
          />
        ))}

        {/* Selected-point rows */}
        {selectedPoints.map((point, i) => {
          const kind = integrationOf(point);
          const colour = colourOf(kind);
          const y = HEADER_H + PADDING_TOP + i * ROW_H + ROW_H / 2;
          const touchedIdxs = cols
            .map((c, ci) => ({ ci, touched: point.textsTouched.includes(c.id) }))
            .filter(t => t.touched)
            .map(t => t.ci)
            .sort((a, b) => a - b);
          const leftmost = touchedIdxs[0];
          const rightmost = touchedIdxs[touchedIdxs.length - 1];

          return (
            <React.Fragment key={point.id}>
              {/* Row label */}
              <div
                style={{
                  position: 'absolute',
                  left: 0,
                  top: y,
                  transform: 'translateY(-50%)',
                  width: ROW_LABEL_W,
                  textAlign: 'left',
                }}
              >
                <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, color: '#9e9186', letterSpacing: 0.5 }}>
                  {String(i + 1).padStart(2, '0')}
                </p>
              </div>

              {/* Connector line — straight, between leftmost and rightmost touched */}
              {touchedIdxs.length >= 2 && (
                <motion.div
                  aria-hidden
                  initial={{ scaleX: 0, opacity: 0 }}
                  animate={{ scaleX: 1, opacity: 1 }}
                  transition={{ duration: 0.5, ease: 'easeOut', delay: i * 0.06 }}
                  style={{
                    position: 'absolute',
                    left: xPercent(leftmost),
                    width: `calc(${xPercent(rightmost)} - ${xPercent(leftmost)})`,
                    top: y,
                    height: 0,
                    borderTop: `2px solid ${colour}`,
                    transformOrigin: 'left center',
                    pointerEvents: 'none',
                  }}
                />
              )}

              {/* Dots — one per column */}
              {cols.map((c, ci) => (
                <ThreadDot
                  key={c.id}
                  xCalc={xPercent(ci)}
                  y={y}
                  isTouched={point.textsTouched.includes(c.id)}
                  colour={colour}
                  delay={i * 0.06 + ci * 0.03}
                />
              ))}

              {/* Serial isolation halo */}
              {kind === 'serial' && leftmost !== undefined && (
                <motion.div
                  aria-hidden
                  initial={{ opacity: 0, scale: 0.6 }}
                  animate={{ opacity: 0.55, scale: 1 }}
                  transition={{ delay: i * 0.06 + 0.2, duration: 0.4 }}
                  style={{
                    position: 'absolute',
                    left: xPercent(leftmost),
                    top: y,
                    transform: 'translate(-50%, -50%)',
                    width: 28,
                    height: 28,
                    borderRadius: '50%',
                    border: `1.5px dashed ${colour}`,
                    pointerEvents: 'none',
                  }}
                />
              )}
            </React.Fragment>
          );
        })}

        {/* Empty-state hint dots on the first row when nothing selected */}
        {selectedPoints.length === 0 && cols.map((_, ci) => (
          <div
            key={`ghost-${ci}`}
            aria-hidden
            style={{
              position: 'absolute',
              left: xPercent(ci),
              top: HEADER_H + PADDING_TOP + ROW_H / 2,
              transform: 'translate(-50%, -50%)',
              width: 7,
              height: 7,
              borderRadius: '50%',
              border: '1.5px solid #c8c4be',
              opacity: 0.7,
            }}
          />
        ))}
      </div>
    </section>
  );
};

const ThreadDot: React.FC<{ xCalc: string; y: number; isTouched: boolean; colour: string; delay: number }> = ({ xCalc, y, isTouched, colour, delay }) => (
  <motion.div
    aria-hidden
    initial={{ scale: 0 }}
    animate={{ scale: 1 }}
    transition={{ type: 'spring', stiffness: 340, damping: 22, delay }}
    style={{
      position: 'absolute',
      left: xCalc,
      top: y,
      transform: 'translate(-50%, -50%)',
      width: isTouched ? 12 : 6,
      height: isTouched ? 12 : 6,
      borderRadius: '50%',
      backgroundColor: isTouched ? colour : CREAM,
      border: isTouched ? `2px solid ${colour}` : `1.5px solid #b8b1a8`,
      zIndex: 1,
    }}
  />
);

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
