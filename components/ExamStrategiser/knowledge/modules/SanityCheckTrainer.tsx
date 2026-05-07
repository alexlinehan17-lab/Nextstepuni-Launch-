/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sanity-Check Trainer (Stage 2, E6).
 *
 * The absurdity radar. A 2x2 grid of candidate answers — three absurd,
 * one correct. Student taps each absurd answer AND identifies which
 * sanity check would have caught it (Order of Magnitude, Units, Sign,
 * Substitute-Back). On correct identification, an SVG radar pulses
 * around the candidate in the colour of the catching check.
 *
 * Reaction time tracking: each correct identification logs ms-since-
 * question-load. The closing screen surfaces which checks the student
 * is fastest and slowest at — a personal "checks neglected" report.
 *
 * Library: 12 questions across Maths, Chemistry, Physics, Biology.
 *
 * Source: dossier § C1 (sanity-check habit), § B2 / B4.
 *
 * Aesthetic: Stage 2 — 2px #1a1a1a borders; the radar is rendered as
 * concentric SVG circles via Framer Motion.
 */

import React, { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { SANITY_CHECK_QUESTIONS } from '../../../../data/knowledge/sanityChecks';
import { writePattern } from '../knowledgePatterns';
import {
  type SanityCheckQuestion,
  type SanityCandidate,
  type SanityCheck,
} from '../../../../types/knowledge';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

const CHECK_LABELS: Record<SanityCheck, string> = {
  'order-of-magnitude': 'Order of Magnitude',
  'units': 'Units',
  'sign': 'Sign / Direction',
  'substitute-back': 'Substitute-Back',
};

const CHECK_COLOURS: Record<SanityCheck, string> = {
  'order-of-magnitude': TEAL,
  'units': TEAL_DARK,
  'sign': INK,
  'substitute-back': WARN,
};

const CHECK_GLYPHS: Record<SanityCheck, string> = {
  'order-of-magnitude': 'O',
  'units': 'U',
  'sign': '±',
  'substitute-back': 'S',
};

/** Per-candidate verdict state captured during the session. */
type CandidateVerdict =
  | { kind: 'open' }
  | { kind: 'pending-check'; tapMs: number } // student tagged absurd, picking which check
  | { kind: 'tagged-correct' }
  | { kind: 'absurd-resolved'; check: SanityCheck; reactionMs: number; rightCheck: boolean }
  | { kind: 'wrong-tagged-correct' }   // student let an absurd answer through as "looks fine"
  | { kind: 'wrong-tagged-absurd' };   // student tagged the correct answer as absurd

interface QuestionLog {
  questionId: string;
  candidates: Record<string, CandidateVerdict>;
  startMs: number;
  resolvedMs?: number;
}

interface ReactionLogEntry {
  check: SanityCheck;
  reactionMs: number;
  correct: boolean;
}

interface Props {
  onBack: () => void;
}

const SanityCheckTrainer: React.FC<Props> = ({ onBack }) => {
  const [queue] = useState(() => shuffle(SANITY_CHECK_QUESTIONS));
  const [idx, setIdx] = useState(0);
  const question = queue[idx];

  const [log, setLog] = useState<QuestionLog>(() => freshLog(question));
  const [history, setHistory] = useState<ReactionLogEntry[]>([]);
  const [showSummary, setShowSummary] = useState(false);

  // Reset log when question changes
  useEffect(() => {
    setLog(freshLog(question));
  }, [question]);

  const allResolved = useMemo(() => {
    return question.candidates.every(c => {
      const v = log.candidates[c.id];
      return (
        v.kind === 'absurd-resolved' ||
        v.kind === 'tagged-correct' ||
        v.kind === 'wrong-tagged-correct' ||
        v.kind === 'wrong-tagged-absurd'
      );
    });
  }, [log, question]);

  const onTagAbsurd = (cid: string) => {
    if (log.candidates[cid].kind !== 'open') return;
    setLog(prev => ({
      ...prev,
      candidates: { ...prev.candidates, [cid]: { kind: 'pending-check', tapMs: Date.now() } },
    }));
  };

  const onTagCorrect = (cid: string) => {
    if (log.candidates[cid].kind !== 'open') return;
    const candidate = question.candidates.find(c => c.id === cid)!;
    if (candidate.correct) {
      setLog(prev => ({
        ...prev,
        candidates: { ...prev.candidates, [cid]: { kind: 'tagged-correct' } },
      }));
    } else {
      setLog(prev => ({
        ...prev,
        candidates: { ...prev.candidates, [cid]: { kind: 'wrong-tagged-correct' } },
      }));
    }
  };

  const onPickCheck = (cid: string, check: SanityCheck) => {
    const v = log.candidates[cid];
    if (v.kind !== 'pending-check') return;
    const candidate = question.candidates.find(c => c.id === cid)!;

    // The student tagged the correct answer as absurd. Picking any check
    // here resolves to a "wrong-tagged-absurd" verdict — the answer was
    // actually correct, the student over-corrected. We don't record this
    // in the reaction history because the timing isn't a meaningful signal.
    if (candidate.correct) {
      setLog(prev => ({
        ...prev,
        candidates: {
          ...prev.candidates,
          [cid]: { kind: 'wrong-tagged-absurd' },
        },
      }));
      return;
    }

    if (!candidate.catchingCheck) return;
    const reactionMs = Date.now() - log.startMs;
    const rightCheck = candidate.catchingCheck === check;
    setLog(prev => ({
      ...prev,
      candidates: {
        ...prev.candidates,
        [cid]: { kind: 'absurd-resolved', check, reactionMs, rightCheck },
      },
    }));
    setHistory(prev => [...prev, { check, reactionMs, correct: rightCheck }]);
  };

  /** Lets a student back out of a pending-check tag — useful when they
   *  realise they\'ve clicked "Absurd" on the correct answer. */
  const onUndoPending = (cid: string) => {
    if (log.candidates[cid].kind !== 'pending-check') return;
    setLog(prev => ({
      ...prev,
      candidates: { ...prev.candidates, [cid]: { kind: 'open' } },
    }));
  };

  const onAdvance = () => {
    if (idx + 1 < queue.length) {
      setIdx(idx + 1);
    } else {
      setShowSummary(true);
    }
  };

  const restart = () => {
    setShowSummary(false);
    setIdx(0);
    setHistory([]);
  };

  if (showSummary) {
    return (
      <div className="space-y-6" style={{ color: INK }}>
        <BackBar onBack={onBack} />
        <Hero />
        <SummaryReport history={history} onRestart={restart} />
      </div>
    );
  }

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <ProgressBar idx={idx} total={queue.length} />

      <QuestionFrame question={question} idx={idx}>
        <CandidateGrid
          question={question}
          log={log}
          onTagAbsurd={onTagAbsurd}
          onTagCorrect={onTagCorrect}
          onPickCheck={onPickCheck}
          onUndoPending={onUndoPending}
        />

        {allResolved && (
          <ResolvedFooter onAdvance={onAdvance} isLast={idx + 1 === queue.length} />
        )}
      </QuestionFrame>

      <CheckLegend />
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
      Necessary Knowledge · Stage 2
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Sanity-Check Trainer — the absurdity radar.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      Four candidate answers. Three are absurd; one is correct. Tap each absurd answer and pick the check that catches it.
      The 2015 Maths Chief Examiner Report says it directly: <em>"if you find a person's height is 800 m, something is wrong."</em>
    </p>
  </header>
);

const ProgressBar: React.FC<{ idx: number; total: number }> = ({ idx, total }) => {
  const pct = ((idx) / total) * 100;
  return (
    <div className="flex items-center gap-3">
      <div
        style={{
          flex: 1,
          height: 4,
          backgroundColor: '#EDEBE8',
          borderRadius: 999,
          overflow: 'hidden',
        }}
      >
        <motion.div
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.4 }}
          style={{ height: '100%', backgroundColor: TEAL }}
        />
      </div>
      <span className="font-sans" style={{ fontSize: 11, color: '#78716C', whiteSpace: 'nowrap' }}>
        Question {idx + 1} / {total}
      </span>
    </div>
  );
};

const QuestionFrame: React.FC<{ question: SanityCheckQuestion; idx: number; children: React.ReactNode }> = ({ question, idx, children }) => (
  <section
    className="rounded-2xl"
    style={{
      backgroundColor: '#FFFFFF',
      border: `2px solid ${INK}`,
      padding: '24px 26px',
    }}
  >
    <div className="flex items-baseline gap-3 mb-2 flex-wrap">
      <span
        className="font-sans"
        style={{
          fontSize: 10,
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: 0.5,
          color: TEAL,
          backgroundColor: `${TEAL}15`,
          border: `1px solid ${TEAL}66`,
          borderRadius: 999,
          padding: '3px 10px',
        }}
      >
        {question.subject}
      </span>
      <span className="font-sans" style={{ fontSize: 11, color: '#9e9186' }}>
        {question.topicLabel}
      </span>
    </div>
    <p className="font-serif" style={{ fontSize: 18, fontWeight: 500, color: INK, lineHeight: 1.45, fontStyle: 'italic', marginBottom: 22 }}>
      &ldquo;{question.questionPrompt}&rdquo;
    </p>
    {children}
  </section>
);

// ─── Candidate grid ────────────────────────────────────────────────────

const CandidateGrid: React.FC<{
  question: SanityCheckQuestion;
  log: QuestionLog;
  onTagAbsurd: (cid: string) => void;
  onTagCorrect: (cid: string) => void;
  onPickCheck: (cid: string, check: SanityCheck) => void;
  onUndoPending: (cid: string) => void;
}> = ({ question, log, onTagAbsurd, onTagCorrect, onPickCheck, onUndoPending }) => (
  <div className="grid sm:grid-cols-2 gap-4">
    {question.candidates.map(c => (
      <CandidateCard
        key={c.id}
        candidate={c}
        verdict={log.candidates[c.id]}
        onTagAbsurd={() => onTagAbsurd(c.id)}
        onTagCorrect={() => onTagCorrect(c.id)}
        onPickCheck={(check) => onPickCheck(c.id, check)}
        onUndo={() => onUndoPending(c.id)}
      />
    ))}
  </div>
);

const CandidateCard: React.FC<{
  candidate: SanityCandidate;
  verdict: CandidateVerdict;
  onTagAbsurd: () => void;
  onTagCorrect: () => void;
  onPickCheck: (check: SanityCheck) => void;
  onUndo: () => void;
}> = ({ candidate, verdict, onTagAbsurd, onTagCorrect, onPickCheck, onUndo }) => {
  const open = verdict.kind === 'open';
  const pending = verdict.kind === 'pending-check';
  const correctTagged = verdict.kind === 'tagged-correct';
  const absurdResolved = verdict.kind === 'absurd-resolved';
  const wrongCorrectTag = verdict.kind === 'wrong-tagged-correct';
  const wrongAbsurdTag = verdict.kind === 'wrong-tagged-absurd';

  let outerBorder = `2px solid ${INK}`;
  let outerBg = '#FFFFFF';

  if (correctTagged) {
    outerBorder = `2px solid ${TEAL}`;
    outerBg = `${TEAL}10`;
  } else if (absurdResolved) {
    const c = CHECK_COLOURS[verdict.check];
    outerBorder = `2px solid ${c}`;
    outerBg = `${c}10`;
  } else if (wrongCorrectTag || wrongAbsurdTag) {
    outerBorder = `2px solid ${WARN}`;
    outerBg = `${WARN}10`;
  } else if (pending) {
    outerBorder = `2px dashed ${INK}`;
  }

  return (
    <div className="relative">
      {/* Absurdity radar SVG — only shows for resolved absurd answers */}
      {absurdResolved && verdict.kind === 'absurd-resolved' && verdict.rightCheck && (
        <RadarPulse colour={CHECK_COLOURS[verdict.check]} />
      )}

      <motion.div
        layout
        animate={{ scale: pending ? 1.01 : 1 }}
        transition={{ duration: 0.2 }}
        className="rounded-2xl relative"
        style={{
          backgroundColor: outerBg,
          border: outerBorder,
          padding: '18px 20px',
          minHeight: 180,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Candidate text */}
        <p
          className="font-serif"
          style={{
            fontSize: 22,
            fontWeight: 600,
            color: INK,
            lineHeight: 1.35,
            marginBottom: 12,
            textAlign: 'center',
            flex: 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {candidate.text}
        </p>

        {/* State-specific UI */}
        {open && (
          <div className="flex gap-2">
            <button
              type="button"
              onClick={onTagCorrect}
              className="font-sans flex-1 rounded-full"
              style={{
                backgroundColor: '#FFFFFF',
                color: INK,
                border: `1.5px solid ${INK}`,
                padding: '8px 14px',
                fontSize: 12,
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Looks fine
            </button>
            <button
              type="button"
              onClick={onTagAbsurd}
              className="font-sans flex-1 rounded-full"
              style={{
                backgroundColor: INK,
                color: '#FFFFFF',
                border: `1.5px solid ${INK}`,
                padding: '8px 14px',
                fontSize: 12,
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Absurd
            </button>
          </div>
        )}

        {pending && (
          <CheckPicker onPick={onPickCheck} onUndo={onUndo} />
        )}

        {correctTagged && (
          <ResolvedNote tone="ok" headline="Correct answer." detail="You let the right one stand." />
        )}

        {absurdResolved && verdict.kind === 'absurd-resolved' && (
          <ResolvedNote
            tone={verdict.rightCheck ? 'radar' : 'miss'}
            headline={
              verdict.rightCheck
                ? `${CHECK_LABELS[verdict.check]} — caught in ${formatMs(verdict.reactionMs)}`
                : `Different check applies. The catching check is ${CHECK_LABELS[candidate.catchingCheck!]}.`
            }
            detail={candidate.absurdityExplanation || ''}
            colour={CHECK_COLOURS[verdict.check]}
          />
        )}

        {wrongCorrectTag && (
          <ResolvedNote
            tone="miss"
            headline="This one was absurd — and you let it through."
            detail={`${candidate.absurdityExplanation || ''} Catching check: ${CHECK_LABELS[candidate.catchingCheck!]}.`}
          />
        )}

        {wrongAbsurdTag && (
          <ResolvedNote
            tone="miss"
            headline="This was actually the correct answer."
            detail="You over-corrected. The right answer can look surprising — that\'s why the four checks need to discriminate between unusual and absurd. None of the checks applies here."
          />
        )}
      </motion.div>
    </div>
  );
};

const CheckPicker: React.FC<{ onPick: (check: SanityCheck) => void; onUndo: () => void }> = ({ onPick, onUndo }) => {
  const checks: SanityCheck[] = ['order-of-magnitude', 'units', 'sign', 'substitute-back'];
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-2">
        <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#78716C' }}>
          Which check catches it?
        </p>
        <button
          type="button"
          onClick={onUndo}
          className="font-sans"
          style={{ fontSize: 11, color: '#78716C', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer', textDecoration: 'underline' }}
        >
          Not absurd — undo
        </button>
      </div>
      <div className="grid grid-cols-2 gap-1.5">
        {checks.map(c => (
          <button
            key={c}
            type="button"
            onClick={() => onPick(c)}
            className="font-sans rounded-md"
            style={{
              backgroundColor: '#FFFFFF',
              color: INK,
              border: `1.5px solid ${CHECK_COLOURS[c]}`,
              padding: '7px 10px',
              fontSize: 11.5,
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 6,
            }}
          >
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 18,
                height: 18,
                borderRadius: 4,
                backgroundColor: CHECK_COLOURS[c],
                color: '#FFFFFF',
                fontSize: 10,
                fontWeight: 700,
              }}
            >
              {CHECK_GLYPHS[c]}
            </span>
            {CHECK_LABELS[c]}
          </button>
        ))}
      </div>
    </motion.div>
  );
};

const ResolvedNote: React.FC<{
  tone: 'ok' | 'radar' | 'miss';
  headline: string;
  detail: string;
  colour?: string;
}> = ({ tone, headline, detail, colour }) => {
  const tint =
    tone === 'ok' ? `${TEAL}10` :
    tone === 'miss' ? `${WARN}15` :
    `${colour}15`;
  const accent =
    tone === 'ok' ? TEAL :
    tone === 'miss' ? WARN :
    colour || TEAL;
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="rounded-md"
      style={{
        backgroundColor: tint,
        border: `1px solid ${accent}66`,
        padding: '10px 12px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 11.5, fontWeight: 700, color: accent }}>
        {headline}
      </p>
      {detail && (
        <p className="font-sans" style={{ fontSize: 12, color: '#3F3B36', marginTop: 4, lineHeight: 1.5 }}>
          {detail}
        </p>
      )}
    </motion.div>
  );
};

// ─── Radar pulse SVG ───────────────────────────────────────────────────

const RadarPulse: React.FC<{ colour: string }> = ({ colour }) => (
  <svg
    aria-hidden
    style={{
      position: 'absolute',
      inset: -6,
      width: 'calc(100% + 12px)',
      height: 'calc(100% + 12px)',
      pointerEvents: 'none',
      zIndex: 1,
    }}
    viewBox="0 0 100 100"
    preserveAspectRatio="none"
  >
    {[0, 0.5, 1].map(delay => (
      <motion.rect
        key={delay}
        x="0"
        y="0"
        width="100"
        height="100"
        rx="8"
        ry="8"
        fill="none"
        stroke={colour}
        strokeWidth="0.5"
        initial={{ opacity: 0.4, scale: 1 }}
        animate={{ opacity: 0, scale: 1.05 }}
        transition={{
          duration: 1.6,
          delay,
          repeat: Infinity,
          ease: 'easeOut',
        }}
        style={{
          transformOrigin: '50px 50px',
        }}
      />
    ))}
  </svg>
);

// ─── Resolved footer ───────────────────────────────────────────────────

const ResolvedFooter: React.FC<{ onAdvance: () => void; isLast: boolean }> = ({ onAdvance, isLast }) => (
  <motion.div
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    className="mt-5 flex items-center justify-end"
  >
    <button
      type="button"
      onClick={onAdvance}
      className="font-sans rounded-full"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '11px 24px',
        fontSize: 13,
        fontWeight: 600,
        cursor: 'pointer',
      }}
    >
      {isLast ? 'See your checks-neglected report' : 'Next question'}
      <span style={{ marginLeft: 6 }}>→</span>
    </button>
  </motion.div>
);

// ─── Check legend ──────────────────────────────────────────────────────

const CheckLegend: React.FC = () => {
  const checks: SanityCheck[] = ['order-of-magnitude', 'units', 'sign', 'substitute-back'];
  const blurbs: Record<SanityCheck, string> = {
    'order-of-magnitude': 'Is this number plausible? A person can\'t be 800 m tall.',
    'units': 'Are units correct? mol vs g, m vs m/s, /min vs /hour.',
    'sign': 'Should this be positive? pH, probability, mass — none can be negative.',
    'substitute-back': 'Plug the answer back in. Does it satisfy the original equation?',
  };
  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: CREAM, border: '1.5px solid #d0cdc8', padding: '18px 22px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#9e9186', marginBottom: 10 }}>
        The four checks
      </p>
      <div className="grid sm:grid-cols-2 gap-2">
        {checks.map(c => (
          <div key={c} className="flex items-start gap-2">
            <span
              className="font-sans shrink-0"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 22,
                height: 22,
                borderRadius: 4,
                backgroundColor: CHECK_COLOURS[c],
                color: '#FFFFFF',
                fontSize: 11,
                fontWeight: 700,
                marginTop: 1,
              }}
            >
              {CHECK_GLYPHS[c]}
            </span>
            <div>
              <p className="font-serif" style={{ fontSize: 13, fontWeight: 600, color: INK }}>
                {CHECK_LABELS[c]}
              </p>
              <p className="font-sans" style={{ fontSize: 12, color: '#5a5550', lineHeight: 1.5 }}>
                {blurbs[c]}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

// ─── Summary report ────────────────────────────────────────────────────

const SummaryReport: React.FC<{
  history: ReactionLogEntry[];
  onRestart: () => void;
}> = ({ history, onRestart }) => {
  // Aggregate per check
  const byCheck = useMemo(() => {
    const checks: SanityCheck[] = ['order-of-magnitude', 'units', 'sign', 'substitute-back'];
    return checks.map(c => {
      const items = history.filter(h => h.check === c);
      const correct = items.filter(h => h.correct);
      const avgMs = correct.length === 0 ? null : Math.round(correct.reduce((sum, h) => sum + h.reactionMs, 0) / correct.length);
      return { check: c, total: items.length, correctCount: correct.length, avgMs };
    });
  }, [history]);

  const totalCorrect = history.filter(h => h.correct).length;
  const totalAttempts = history.length;

  // Find fastest and slowest checks (by average ms among those with data)
  const withData = byCheck.filter(b => b.avgMs !== null);
  const fastest = withData.reduce<typeof withData[number] | null>(
    (best, cur) => (best === null || cur.avgMs! < best.avgMs!) ? cur : best,
    null,
  );
  const slowest = withData.reduce<typeof withData[number] | null>(
    (worst, cur) => (worst === null || cur.avgMs! > worst.avgMs!) ? cur : worst,
    null,
  );

  // Detect neglected checks (low usage relative to others or low accuracy)
  const neglected = byCheck.filter(b => b.total > 0 && b.correctCount / b.total < 0.5);

  // Persist the weakest check to localStorage so the landing's "Your patterns"
  // panel can surface it cross-module.
  useEffect(() => {
    if (totalAttempts < 3) return;
    const ranked = byCheck
      .filter(b => b.total > 0)
      .map(b => ({ check: b.check, accuracy: b.correctCount / b.total }))
      .sort((a, b) => a.accuracy - b.accuracy);
    if (ranked.length === 0) return;
    const weakestCheck = ranked[0].check;
    const accuracyByCheck: Record<string, number> = {};
    byCheck.forEach(b => {
      accuracyByCheck[b.check] = b.total > 0 ? b.correctCount / b.total : 0;
    });
    writePattern('sanityCheck', {
      weakestCheck,
      accuracyByCheck,
      sampleSize: totalAttempts,
      updatedAt: Date.now(),
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [totalAttempts]);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '32px 32px 28px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Your checks-neglected report
      </p>
      <h2 className="font-serif" style={{ fontSize: 26, fontWeight: 600, lineHeight: 1.2, marginTop: 6 }}>
        {totalCorrect} of {totalAttempts} absurd answers caught.
      </h2>

      {/* Per-check bars */}
      <div className="mt-6 space-y-3">
        {byCheck.map(b => (
          <CheckBar key={b.check} entry={b} />
        ))}
      </div>

      {/* Personal insights */}
      <div className="mt-7 space-y-3">
        {fastest && (
          <Insight
            label="Fastest check"
            body={`Your radar pings hardest on ${CHECK_LABELS[fastest.check]} — average ${formatMs(fastest.avgMs!)}. This is your most-trusted check.`}
          />
        )}
        {slowest && fastest && fastest.check !== slowest.check && (
          <Insight
            label="Slowest check"
            body={`${CHECK_LABELS[slowest.check]} took longer (${formatMs(slowest.avgMs!)} on average). Most students who are slow at one check are also less likely to apply it spontaneously — make this your first habit on every calculation.`}
          />
        )}
        {neglected.length > 0 && (
          <Insight
            label="Make this your first habit"
            body={`You missed more than half of your ${neglected.map(n => CHECK_LABELS[n.check]).join(' and ')} flags. The fix is procedural: at the end of every calculation, before you write the final answer, run the four checks in order. ${CHECK_LABELS[neglected[0].check]} first.`}
            highlight
          />
        )}
        {neglected.length === 0 && totalAttempts >= 6 && (
          <Insight
            label="Solid radar"
            body="No single check is consistently dropping. Your sanity-checking habit is broad — the 2015 Maths CER complaint is exactly the kind of pattern this protects you from."
          />
        )}
      </div>

      <div className="mt-7">
        <button
          type="button"
          onClick={onRestart}
          className="font-sans rounded-full"
          style={{
            backgroundColor: '#FFFFFF',
            color: INK,
            border: '2px solid #FFFFFF',
            padding: '10px 22px',
            fontSize: 13,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Run the trainer again
        </button>
      </div>
    </section>
  );
};

const CheckBar: React.FC<{ entry: { check: SanityCheck; total: number; correctCount: number; avgMs: number | null } }> = ({ entry }) => {
  const accuracy = entry.total === 0 ? 0 : (entry.correctCount / entry.total) * 100;
  return (
    <div>
      <div className="flex items-baseline justify-between gap-3 mb-1">
        <span className="font-sans" style={{ fontSize: 12, fontWeight: 600, color: '#FFFFFF' }}>
          <span style={{ color: CHECK_COLOURS[entry.check], marginRight: 6 }}>●</span>
          {CHECK_LABELS[entry.check]}
        </span>
        <span className="font-sans" style={{ fontSize: 11, color: '#FFD8A8', opacity: 0.85 }}>
          {entry.correctCount}/{entry.total}
          {entry.avgMs !== null && ` · ${formatMs(entry.avgMs)} avg`}
        </span>
      </div>
      <div
        style={{
          height: 6,
          backgroundColor: '#3F3B36',
          borderRadius: 999,
          overflow: 'hidden',
        }}
      >
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${accuracy}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          style={{
            height: '100%',
            backgroundColor: CHECK_COLOURS[entry.check],
          }}
        />
      </div>
    </div>
  );
};

const Insight: React.FC<{ label: string; body: string; highlight?: boolean }> = ({ label, body, highlight }) => (
  <div
    style={{
      borderLeft: highlight ? `3px solid ${TEAL}` : '3px solid transparent',
      paddingLeft: highlight ? 14 : 0,
    }}
  >
    <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.9 }}>
      {label}
    </p>
    <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', marginTop: 2, lineHeight: 1.55 }}>
      {body}
    </p>
  </div>
);

// ─── Helpers ───────────────────────────────────────────────────────────

function freshLog(question: SanityCheckQuestion): QuestionLog {
  const candidates: Record<string, CandidateVerdict> = {};
  question.candidates.forEach(c => { candidates[c.id] = { kind: 'open' }; });
  return { questionId: question.id, candidates, startMs: Date.now() };
}

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function formatMs(ms: number): string {
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(1)} s`;
}

export default SanityCheckTrainer;
