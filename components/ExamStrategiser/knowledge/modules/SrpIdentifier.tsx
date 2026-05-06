/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SRP Identifier (Stage 2, E10).
 *
 * Three-phase interactive heat map for Geography/History/Business long-
 * question paragraphs:
 *
 *   1. STUDENT — student highlights every sentence they think is an SRP.
 *      Each highlight glows teal.
 *   2. EXAMINER — actual classification revealed; sentences colour-coded
 *      (confirmed SRP, missed SRP pulsing, false-positive struck through,
 *      waffle greyed).
 *   3. PROVENANCE — every confirmed SRP sends a connector line down to a
 *      running mark counter, accruing in real time at 2 marks each. Pause
 *      at the 15-SRP cap with a pulse, continue to the 17-SRP safety
 *      buffer.
 *
 * Diagnostic feedback panel surfaces the *pattern* of the student's misses
 * — buried-after-waffle, unsupported-vs-undeveloped, etc. Specific to the
 * paragraph, not generic.
 *
 * Source: dossier § A2, § B6 (Geography 2012 CER), § B5 (History 2017
 * CER), § B7 (Business 2025 marking scheme).
 *
 * Aesthetic register: Stage 2 bold — 2px #1a1a1a card borders, denser
 * instrument-panel feel. Framer Motion for the provenance trail.
 */

import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { SRP_SAMPLES } from '../../../../data/knowledge/srpSamples';
import { type SrpSample, type SrpSentence } from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';

type Phase = 'student' | 'examiner' | 'provenance';

interface Props {
  onBack: () => void;
}

const SrpIdentifier: React.FC<Props> = ({ onBack }) => {
  const [sampleId, setSampleId] = useState<string>(SRP_SAMPLES[0].id);
  const sample = useMemo(() => SRP_SAMPLES.find(s => s.id === sampleId)!, [sampleId]);

  const [phase, setPhase] = useState<Phase>('student');
  const [studentPicks, setStudentPicks] = useState<Set<string>>(new Set());

  const switchSample = (id: string) => {
    setSampleId(id);
    setPhase('student');
    setStudentPicks(new Set());
  };

  const togglePick = (id: string) => {
    if (phase !== 'student') return;
    setStudentPicks(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />

      <Hero />

      <SubjectStrip
        samples={SRP_SAMPLES}
        activeSampleId={sample.id}
        onChange={switchSample}
      />

      <SampleHeader sample={sample} />

      <PhaseStepper phase={phase} onChange={setPhase} canAdvance={phase === 'student' && studentPicks.size > 0} />

      <ParagraphPanel
        sample={sample}
        phase={phase}
        studentPicks={studentPicks}
        onTogglePick={togglePick}
      />

      <PhaseControls
        phase={phase}
        studentPicks={studentPicks}
        sample={sample}
        onAdvance={() => {
          if (phase === 'student') setPhase('examiner');
          else if (phase === 'examiner') setPhase('provenance');
        }}
        onReset={() => { setStudentPicks(new Set()); setPhase('student'); }}
      />

      {phase === 'provenance' && <ProvenanceTrail sample={sample} />}

      {phase === 'examiner' && <DiagnosticPanel sample={sample} studentPicks={studentPicks} />}

      {phase === 'provenance' && <PatternCard sample={sample} studentPicks={studentPicks} />}
    </div>
  );
};

// ─── Layout chrome ─────────────────────────────────────────────────────

const BackBar: React.FC<{ onBack: () => void }> = ({ onBack }) => (
  <button
    type="button"
    onClick={onBack}
    className="font-sans flex items-center gap-1.5 transition-colors"
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
      Necessary Knowledge · Stage 2
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      SRP Identifier — see the marks accrue.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      An SRP is a <strong>Significant Relevant Point</strong> — typically <strong>2 marks</strong>. Highlight what you think
      counts; the examiner will then mark over your work, and we'll trace every credited SRP down to a running mark counter.
    </p>
  </header>
);

const SubjectStrip: React.FC<{
  samples: SrpSample[];
  activeSampleId: string;
  onChange: (id: string) => void;
}> = ({ samples, activeSampleId, onChange }) => (
  <div className="flex flex-wrap gap-2">
    {samples.map(s => {
      const active = s.id === activeSampleId;
      return (
        <button
          key={s.id}
          type="button"
          onClick={() => onChange(s.id)}
          className="font-sans rounded-xl text-left transition-colors"
          style={{
            backgroundColor: active ? INK : '#FFFFFF',
            color: active ? '#FFFFFF' : INK,
            border: `2px solid ${INK}`,
            padding: '10px 14px',
            cursor: 'pointer',
            fontSize: 12.5,
            fontWeight: 600,
            flex: '1 1 220px',
            minWidth: 0,
          }}
        >
          <span style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7 }}>
            {s.subject}
          </span>
          <br />
          <span>{s.topicLabel}</span>
        </button>
      );
    })}
  </div>
);

const SampleHeader: React.FC<{ sample: SrpSample }> = ({ sample }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#FFFFFF',
      border: `2px solid ${INK}`,
      padding: '20px 24px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 6 }}>
      Question prompt
    </p>
    <p className="font-serif" style={{ fontSize: 16, fontWeight: 500, color: INK, lineHeight: 1.5, fontStyle: 'italic' }}>
      &ldquo;{sample.questionPrompt}&rdquo;
    </p>
    <div className="flex items-center gap-4 mt-3 flex-wrap">
      <Pill label="Marks available" value={`${sample.marksAvailable}`} />
      <Pill label="SRP cap" value={`${sample.srpCap} SRPs`} />
      <Pill label="Per SRP" value="2 marks" />
    </div>
  </section>
);

const Pill: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div>
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186' }}>
      {label}
    </p>
    <p className="font-serif" style={{ fontSize: 16, fontWeight: 700, color: INK }}>
      {value}
    </p>
  </div>
);

// ─── Phase stepper ─────────────────────────────────────────────────────

const PHASE_ORDER: Phase[] = ['student', 'examiner', 'provenance'];
const PHASE_LABELS: Record<Phase, string> = {
  student: 'You mark it',
  examiner: 'Examiner reveals',
  provenance: 'Marks accrue',
};
const PHASE_DESC: Record<Phase, string> = {
  student: 'Tap every sentence you think is an SRP.',
  examiner: 'See the actual classification, side by side with your picks.',
  provenance: 'Every credited SRP draws down to the mark counter.',
};

const PhaseStepper: React.FC<{
  phase: Phase;
  onChange: (p: Phase) => void;
  canAdvance: boolean;
}> = ({ phase, onChange }) => {
  const activeIdx = PHASE_ORDER.indexOf(phase);
  return (
    <div
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '14px 18px',
      }}
    >
      <div className="flex items-stretch gap-3">
        {PHASE_ORDER.map((p, i) => {
          const isActive = p === phase;
          const isPast = i < activeIdx;
          const reachable = i <= activeIdx; // can revisit past phases
          return (
            <React.Fragment key={p}>
              <button
                type="button"
                disabled={!reachable}
                onClick={() => reachable && onChange(p)}
                className="font-sans flex-1 text-left rounded-xl transition-colors"
                style={{
                  backgroundColor: isActive ? TEAL : isPast ? '#FAF7F4' : '#FFFFFF',
                  color: isActive ? '#FFFFFF' : isPast ? INK : '#9e9186',
                  border: `1.5px solid ${isActive ? TEAL : isPast ? INK : '#d0cdc8'}`,
                  padding: '10px 14px',
                  cursor: reachable ? 'pointer' : 'not-allowed',
                }}
              >
                <p style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, opacity: 0.7 }}>
                  Phase {i + 1}
                </p>
                <p style={{ fontSize: 13, fontWeight: 700 }}>{PHASE_LABELS[p]}</p>
                <p style={{ fontSize: 11.5, opacity: 0.85, marginTop: 2 }}>{PHASE_DESC[p]}</p>
              </button>
              {i < PHASE_ORDER.length - 1 && (
                <div className="flex items-center" style={{ color: '#d0cdc8' }} aria-hidden>
                  <svg width="14" height="14" viewBox="0 0 12 12" fill="none">
                    <path d="M4 3L7 6L4 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

// ─── Paragraph panel ───────────────────────────────────────────────────

const ParagraphPanel: React.FC<{
  sample: SrpSample;
  phase: Phase;
  studentPicks: Set<string>;
  onTogglePick: (id: string) => void;
}> = ({ sample, phase, studentPicks, onTogglePick }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: CREAM,
      border: `2px solid ${INK}`,
      padding: '24px 26px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 10 }}>
      Sample answer paragraph
    </p>
    <div className="space-y-1.5" style={{ fontSize: 15.5, lineHeight: 1.7 }}>
      {sample.sentences.map((s, idx) => (
        <SentenceLine
          key={s.id}
          sentence={s}
          index={idx}
          phase={phase}
          studentPicked={studentPicks.has(s.id)}
          onToggle={() => onTogglePick(s.id)}
        />
      ))}
    </div>
  </section>
);

const SentenceLine: React.FC<{
  sentence: SrpSentence;
  index: number;
  phase: Phase;
  studentPicked: boolean;
  onToggle: () => void;
}> = ({ sentence, phase, studentPicked, onToggle }) => {
  const isExaminerSrp = sentence.type === 'srp';
  const interactive = phase === 'student';

  let bg = 'transparent';
  let border = '1.5px solid transparent';
  let textColor = INK;
  let textDecoration: string | undefined;
  let opacity = 1;

  if (phase === 'student') {
    if (studentPicked) {
      bg = `${TEAL}20`;
      border = `1.5px solid ${TEAL}`;
    }
  } else if (phase === 'examiner' || phase === 'provenance') {
    if (isExaminerSrp && studentPicked) {
      // Confirmed SRP — both student and examiner agree
      bg = TEAL;
      textColor = '#FFFFFF';
      border = `1.5px solid ${TEAL_DARK}`;
    } else if (isExaminerSrp && !studentPicked) {
      // Missed SRP
      bg = 'transparent';
      border = `1.5px dashed ${TEAL}`;
      textColor = TEAL_DARK;
    } else if (!isExaminerSrp && studentPicked) {
      // False positive
      bg = '#FFFFFF';
      border = `1.5px solid ${INK}`;
      textDecoration = 'line-through';
      opacity = 0.55;
    } else {
      // Waffle / unsupported / inaccurate, not picked
      bg = 'transparent';
      border = '1.5px solid transparent';
      textColor = '#9e9186';
      opacity = 0.85;
    }
  }

  const Wrapper = interactive ? motion.button : motion.div;
  const wrapperProps = interactive
    ? { type: 'button' as const, onClick: onToggle, 'aria-pressed': studentPicked }
    : {};

  return (
    <Wrapper
      {...(wrapperProps as Record<string, unknown>)}
      layout
      className="w-full text-left rounded-lg font-serif"
      style={{
        backgroundColor: bg,
        border,
        padding: '8px 12px',
        cursor: interactive ? 'pointer' : 'default',
        color: textColor,
        textDecoration,
        opacity,
        display: 'flex',
        alignItems: 'flex-start',
        gap: 10,
      }}
      animate={
        phase !== 'student' && isExaminerSrp && !studentPicked
          ? { boxShadow: [`0 0 0 0 ${TEAL}00`, `0 0 0 4px ${TEAL}33`, `0 0 0 0 ${TEAL}00`] }
          : { boxShadow: '0 0 0 0 transparent' }
      }
      transition={
        phase !== 'student' && isExaminerSrp && !studentPicked
          ? { duration: 1.6, repeat: Infinity, ease: 'easeInOut' }
          : { duration: 0.2 }
      }
    >
      <SentenceMarker phase={phase} sentence={sentence} studentPicked={studentPicked} />
      <span style={{ flex: 1 }}>
        {sentence.text}
        {(phase === 'examiner' || phase === 'provenance') && sentence.reason && (
          <span
            className="font-sans block"
            style={{ fontSize: 11.5, color: phase === 'student' ? '#78716C' : 'currentColor', opacity: 0.85, marginTop: 4, fontStyle: 'italic' }}
          >
            {sentence.reason}
          </span>
        )}
        {(phase === 'examiner' || phase === 'provenance') && sentence.developsFactor && isExaminerSrp && (
          <span
            className="font-sans block"
            style={{ fontSize: 10.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, marginTop: 4, opacity: 0.9 }}
          >
            +2 · {sentence.developsFactor}
            {sentence.buried && <span style={{ marginLeft: 8, opacity: 0.8 }}>· buried after waffle</span>}
          </span>
        )}
      </span>
    </Wrapper>
  );
};

const SentenceMarker: React.FC<{
  phase: Phase;
  sentence: SrpSentence;
  studentPicked: boolean;
}> = ({ phase, sentence, studentPicked }) => {
  if (phase === 'student') {
    return (
      <span
        aria-hidden
        style={{
          width: 18,
          height: 18,
          borderRadius: 6,
          border: `1.5px solid ${studentPicked ? TEAL : '#9e9186'}`,
          backgroundColor: studentPicked ? TEAL : 'transparent',
          flexShrink: 0,
          marginTop: 4,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {studentPicked && (
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none">
            <path d="M3 6L5 8L9 4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </span>
    );
  }
  // Examiner / provenance — show a glyph indicating the type
  const glyph = (() => {
    if (sentence.type === 'srp' && studentPicked) return '✓';
    if (sentence.type === 'srp' && !studentPicked) return '!';
    if (studentPicked) return '×';
    return '·';
  })();
  return (
    <span
      aria-hidden
      className="font-serif"
      style={{
        width: 18,
        height: 18,
        flexShrink: 0,
        marginTop: 4,
        fontSize: 13,
        fontWeight: 700,
        textAlign: 'center',
        lineHeight: '18px',
        opacity: 0.9,
      }}
    >
      {glyph}
    </span>
  );
};

// ─── Phase controls ────────────────────────────────────────────────────

const PhaseControls: React.FC<{
  phase: Phase;
  studentPicks: Set<string>;
  sample: SrpSample;
  onAdvance: () => void;
  onReset: () => void;
}> = ({ phase, studentPicks, sample, onAdvance, onReset }) => {
  if (phase === 'provenance') {
    return (
      <div className="flex items-center justify-end">
        <button
          type="button"
          onClick={onReset}
          className="font-sans rounded-full"
          style={{
            backgroundColor: '#FFFFFF',
            color: INK,
            border: `2px solid ${INK}`,
            padding: '10px 22px',
            fontSize: 13,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Mark another paragraph
        </button>
      </div>
    );
  }

  const advanceLabel = phase === 'student' ? 'Reveal examiner classification' : 'Run the mark provenance';
  const disabled = phase === 'student' && studentPicks.size === 0;

  const totalSrps = sample.sentences.filter(s => s.type === 'srp').length;
  const stats = phase === 'student'
    ? `${studentPicks.size} sentence${studentPicks.size === 1 ? '' : 's'} marked`
    : `${totalSrps} SRPs in this paragraph · ${sample.sentences.length - totalSrps} non-credited sentences`;

  return (
    <div className="flex items-center justify-between flex-wrap gap-3">
      <p className="font-sans" style={{ fontSize: 12, color: '#78716C' }}>
        {stats}
      </p>
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={onReset}
          className="font-sans rounded-full"
          style={{
            backgroundColor: '#FFFFFF',
            color: '#78716C',
            border: '1.5px solid #d0cdc8',
            padding: '9px 18px',
            fontSize: 12.5,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Reset
        </button>
        <button
          type="button"
          disabled={disabled}
          onClick={onAdvance}
          className="font-sans rounded-full"
          style={{
            backgroundColor: disabled ? '#F5F4F1' : INK,
            color: disabled ? '#C4C0BC' : '#FFFFFF',
            border: `2px solid ${disabled ? '#d0cdc8' : INK}`,
            padding: '10px 22px',
            fontSize: 13,
            fontWeight: 600,
            cursor: disabled ? 'not-allowed' : 'pointer',
          }}
        >
          {advanceLabel}
        </button>
      </div>
    </div>
  );
};

// ─── Provenance trail ──────────────────────────────────────────────────

const ProvenanceTrail: React.FC<{ sample: SrpSample }> = ({ sample }) => {
  const credited = sample.sentences.filter(s => s.type === 'srp');
  const total = credited.length;
  const cap = sample.srpCap;
  const safetyMargin = cap + 2;

  const [tick, setTick] = useState(0);
  React.useEffect(() => {
    if (tick >= total) return;
    const t = setTimeout(() => setTick(tick + 1), 480);
    return () => clearTimeout(t);
  }, [tick, total]);

  const accruedSrps = Math.min(tick, cap);
  const overflowSrps = Math.max(0, Math.min(tick - cap, safetyMargin - cap));
  const accruedMarks = accruedSrps * 2;
  const cappedAtCap = tick >= cap;

  const fillCappedPct = (accruedSrps / cap) * 100;
  const fillBufferPct = cap === safetyMargin ? 0 : (overflowSrps / (safetyMargin - cap)) * 100;

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '28px 30px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-4 flex-wrap">
        <div>
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL }}>
            Mark provenance
          </p>
          <p className="font-serif" style={{ fontSize: 17, fontWeight: 600, color: INK, marginTop: 2 }}>
            Each credited SRP draws down to the counter.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setTick(0)}
          className="font-sans"
          style={{ fontSize: 12, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' }}
        >
          Replay
        </button>
      </div>

      {/* SRP draw rail */}
      <div className="flex flex-wrap gap-1.5 mb-5">
        {credited.map((s, i) => {
          const accrued = i < tick;
          const isAtCap = accrued && i === cap - 1;
          return (
            <motion.div
              key={s.id}
              className="rounded-md font-sans"
              initial={{ opacity: 0, y: -8 }}
              animate={
                accrued
                  ? { opacity: 1, y: 0 }
                  : { opacity: 0.25, y: -8 }
              }
              transition={{ duration: 0.4, ease: 'easeOut' }}
              style={{
                backgroundColor: accrued ? TEAL : '#F5F4F1',
                color: accrued ? '#FFFFFF' : '#9e9186',
                border: `1.5px solid ${accrued ? TEAL_DARK : '#d0cdc8'}`,
                padding: '4px 9px',
                fontSize: 11,
                fontWeight: 700,
                position: 'relative',
              }}
              title={s.developsFactor || ''}
            >
              SRP {i + 1}
              {accrued && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  style={{ marginLeft: 6, opacity: 0.85 }}
                >
                  +2
                </motion.span>
              )}
              {isAtCap && (
                <motion.span
                  initial={{ scale: 1, opacity: 0.6 }}
                  animate={{ scale: 1.4, opacity: 0 }}
                  transition={{ duration: 1.0, repeat: Infinity }}
                  aria-hidden
                  style={{
                    position: 'absolute',
                    inset: 0,
                    borderRadius: 6,
                    border: `2px solid ${TEAL}`,
                  }}
                />
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Mark counter — instrument panel */}
      <div
        className="rounded-xl"
        style={{
          backgroundColor: CREAM,
          border: `1.5px solid ${INK}`,
          padding: '18px 20px',
        }}
      >
        <div className="flex items-baseline justify-between mb-2 flex-wrap gap-2">
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186' }}>
            Marks accrued
          </p>
          <div className="font-serif" style={{ fontSize: 32, fontWeight: 700, color: INK }}>
            {accruedMarks + overflowSrps * 2}
            <span style={{ fontSize: 16, color: '#9e9186', fontWeight: 500 }}> / {sample.marksAvailable}</span>
          </div>
        </div>

        {/* Progress bar with cap marker */}
        <div
          style={{
            position: 'relative',
            backgroundColor: '#FFFFFF',
            border: `1.5px solid ${INK}`,
            borderRadius: 999,
            height: 22,
            overflow: 'hidden',
          }}
        >
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${fillCappedPct * (cap / safetyMargin)}%` }}
            transition={{ duration: 0.4 }}
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              backgroundColor: TEAL,
            }}
          />
          {cappedAtCap && fillBufferPct > 0 && (
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${fillBufferPct * ((safetyMargin - cap) / safetyMargin)}%` }}
              transition={{ duration: 0.4 }}
              style={{
                position: 'absolute',
                left: `${(cap / safetyMargin) * 100}%`,
                top: 0,
                bottom: 0,
                backgroundColor: TEAL_DARK,
              }}
            />
          )}
          {/* Cap line */}
          <div
            aria-hidden
            style={{
              position: 'absolute',
              left: `${(cap / safetyMargin) * 100}%`,
              top: -3,
              bottom: -3,
              width: 2,
              backgroundColor: INK,
            }}
          />
        </div>

        <div className="flex items-center justify-between mt-2 font-sans" style={{ fontSize: 11, color: '#78716C' }}>
          <span>0 SRPs</span>
          <span style={{ fontWeight: 700, color: INK }}>
            Cap at {cap} SRPs ({cap * 2} marks) — safety buffer to {safetyMargin}
          </span>
          <span>{safetyMargin}+</span>
        </div>

        {cappedAtCap && (
          <motion.p
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className="font-sans"
            style={{ fontSize: 12.5, color: TEAL, marginTop: 12, lineHeight: 1.55, fontWeight: 600 }}
          >
            Ceiling reached at {cap} SRPs. The next two carry into the safety margin — they cushion against any SRP the marker might reject as not "developing the question".
          </motion.p>
        )}
      </div>
    </section>
  );
};

// ─── Diagnostic + pattern ──────────────────────────────────────────────

const DiagnosticPanel: React.FC<{
  sample: SrpSample;
  studentPicks: Set<string>;
}> = ({ sample, studentPicks }) => {
  const examinerSrps = sample.sentences.filter(s => s.type === 'srp');
  const studentSrpsRight = examinerSrps.filter(s => studentPicks.has(s.id));
  const missed = examinerSrps.filter(s => !studentPicks.has(s.id));
  const falsePositives = sample.sentences.filter(s => s.type !== 'srp' && studentPicks.has(s.id));

  const buriedMissed = missed.filter(s => s.buried).length;
  const fpReasons = falsePositives.map(fp => ({
    text: fp.text,
    reason: fp.reason || 'No specific examiner reason recorded.',
    type: fp.type,
  }));

  const accuracy = examinerSrps.length === 0
    ? 0
    : Math.round((studentSrpsRight.length / examinerSrps.length) * 100);

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '24px 26px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: TEAL, marginBottom: 12 }}>
        Diagnostic
      </p>

      <div className="grid sm:grid-cols-3 gap-3 mb-5">
        <DiagnosticStat label="Caught" value={`${studentSrpsRight.length} / ${examinerSrps.length}`} subtitle={`${accuracy}% accuracy`} />
        <DiagnosticStat label="Missed" value={`${missed.length}`} subtitle={buriedMissed > 0 ? `${buriedMissed} buried after waffle` : 'No buried misses'} />
        <DiagnosticStat label="False positives" value={`${falsePositives.length}`} subtitle={falsePositives.length === 0 ? 'Clean' : 'Examiner-flagged below'} />
      </div>

      {missed.length > 0 && (
        <div className="space-y-2 mb-4">
          <h4 className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: INK }}>
            SRPs you missed
          </h4>
          {missed.slice(0, 3).map(s => (
            <div
              key={s.id}
              className="rounded-lg"
              style={{
                backgroundColor: CREAM,
                border: `1.5px solid ${TEAL}`,
                padding: '10px 14px',
              }}
            >
              <p className="font-serif" style={{ fontSize: 13, color: INK, lineHeight: 1.5 }}>
                {s.text}
              </p>
              <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: TEAL_DARK, marginTop: 6 }}>
                +2 · {s.developsFactor}
                {s.buried && <span style={{ color: '#9e9186', marginLeft: 8 }}>· buried after waffle</span>}
              </p>
            </div>
          ))}
          {missed.length > 3 && (
            <p className="font-sans" style={{ fontSize: 11.5, color: '#78716C' }}>
              … and {missed.length - 3} more.
            </p>
          )}
        </div>
      )}

      {falsePositives.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-serif" style={{ fontSize: 14, fontWeight: 600, color: INK }}>
            Sentences the examiner won't credit
          </h4>
          {fpReasons.slice(0, 3).map((fp, i) => (
            <div
              key={i}
              className="rounded-lg"
              style={{
                backgroundColor: '#FFFFFF',
                border: `1.5px solid ${INK}`,
                padding: '10px 14px',
              }}
            >
              <p className="font-serif" style={{ fontSize: 13, color: INK, lineHeight: 1.5, textDecoration: 'line-through', opacity: 0.65 }}>
                {fp.text}
              </p>
              <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550', marginTop: 6, lineHeight: 1.5 }}>
                <span style={{ fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, fontSize: 10, marginRight: 6 }}>
                  {fp.type}:
                </span>
                {fp.reason}
              </p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

const DiagnosticStat: React.FC<{ label: string; value: string; subtitle: string }> = ({ label, value, subtitle }) => (
  <div
    className="rounded-xl"
    style={{
      backgroundColor: CREAM,
      border: `1.5px solid ${INK}`,
      padding: '14px 16px',
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#9e9186' }}>
      {label}
    </p>
    <p className="font-serif" style={{ fontSize: 24, fontWeight: 700, color: INK, marginTop: 2 }}>
      {value}
    </p>
    <p className="font-sans" style={{ fontSize: 11.5, color: '#5a5550', marginTop: 2 }}>
      {subtitle}
    </p>
  </div>
);

const PatternCard: React.FC<{ sample: SrpSample; studentPicks: Set<string> }> = ({ sample, studentPicks }) => {
  const missedSrps = sample.sentences.filter(s => s.type === 'srp' && !studentPicks.has(s.id));
  const falsePositives = sample.sentences.filter(s => s.type !== 'srp' && studentPicks.has(s.id));

  const buried = missedSrps.filter(s => s.buried).length;
  const fpUnsupported = falsePositives.filter(s => s.type === 'unsupported').length;
  const fpWaffle = falsePositives.filter(s => s.type === 'waffle').length;

  // Emergent pattern detection — specific to this student's actual pattern
  const patternMessages: { headline: string; detail: string }[] = [];

  if (missedSrps.length === 0 && falsePositives.length === 0) {
    patternMessages.push({
      headline: 'You read like an examiner.',
      detail: 'Perfect SRP map on this paragraph. Try a harder sample.',
    });
  } else {
    if (buried >= 2) {
      patternMessages.push({
        headline: `${buried} of your missed SRPs were buried after waffle.`,
        detail: 'Examiners scan first sentences. When the SRP is the second or third sentence, it gets less weight. Lead each paragraph with the credited content and use waffle (if any) as glue, not opener.',
      });
    } else if (buried === 1) {
      patternMessages.push({
        headline: 'One missed SRP was buried after waffle.',
        detail: 'The marker scanned the opening — generic — and skimmed the rest. Lead with the named factor or process, not with framing.',
      });
    }
    if (fpUnsupported >= 2) {
      patternMessages.push({
        headline: `You credited ${fpUnsupported} accurate-but-undeveloped sentences.`,
        detail: 'These look like SRPs because they are factual, but they don\'t develop the question. The marking scheme requires "an SRP… leading to an overall coherent response" — facts that don\'t advance the argument score zero.',
      });
    }
    if (fpWaffle >= 2) {
      patternMessages.push({
        headline: `You credited ${fpWaffle} waffle sentences as SRPs.`,
        detail: 'Generic phrases ("very interesting", "for a long time") feel like content but carry no examinable detail. Ask: "what specific factor is this developing?" If the answer is none, it\'s waffle.',
      });
    }
    if (patternMessages.length === 0) {
      patternMessages.push({
        headline: 'A close-to-clean SRP map.',
        detail: `You caught ${sample.sentences.filter(s => s.type === 'srp' && studentPicks.has(s.id)).length} of ${sample.sentences.filter(s => s.type === 'srp').length} SRPs with minimal false positives. Move on to a new paragraph or subject — the fundamentals are landing.`,
      });
    }
  }

  return (
    <section
      className="rounded-2xl"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        padding: '26px 28px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', marginBottom: 10, opacity: 0.85 }}>
        Your pattern
      </p>
      <div className="space-y-4">
        {patternMessages.map((msg, i) => (
          <div key={i}>
            <h4 className="font-serif" style={{ fontSize: 18, fontWeight: 600, lineHeight: 1.3 }}>
              {msg.headline}
            </h4>
            <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', marginTop: 4, lineHeight: 1.6 }}>
              {msg.detail}
            </p>
          </div>
        ))}
      </div>
      <p className="font-sans" style={{ fontSize: 11, color: '#9e9186', marginTop: 18, lineHeight: 1.5 }}>
        Pattern feedback is generated from your picks on this paragraph only. Try a different subject — habits travel; the absolute hits won't.
      </p>
    </section>
  );
};

export default SrpIdentifier;
