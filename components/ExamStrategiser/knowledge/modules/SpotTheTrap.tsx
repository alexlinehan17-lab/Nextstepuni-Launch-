/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Spot the Trap (Stage 2, E4).
 *
 * Card-stack of 15 paraphrased past-paper-style questions. Each card
 * flips through three states:
 *
 *   1. NEUTRAL READ — student sees the question. 30-second timer.
 *      Student taps "I see the trap" or "Looks fine".
 *   2. TRAP REVEAL — the trap word, modifier, or pluralisation is
 *      underlined and pulses with a teal highlight. The trap label
 *      explains what most students missed.
 *   3. CONSEQUENCE PANEL — shows the marking-scheme cost. Marks-at-
 *      risk meter visualises how much of the question's marks are at
 *      stake.
 *
 * Pattern recognition: every 5 cards, the tool surfaces a pattern card
 * that aggregates the categories the student is missing and proposes a
 * specific fix per category.
 *
 * Subject filter: All / English / Maths / Chemistry / Geography /
 * French / History.
 *
 * Source: dossier § A1 (modifiers), § B1-B8, multiple CERs.
 *
 * Aesthetic: Stage 2 register. SVG underlines via Framer Motion stroke
 * dasharray for the trap pulse.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { TRAP_CARDS, TRAP_CATEGORY_LABELS, TRAP_CATEGORY_FIXES } from '../../../../data/knowledge/trapCards';
import { type TrapCard, type TrapCategory } from '../../../../types/knowledge';
import { writePattern } from '../knowledgePatterns';

const TEAL = '#2A7D6F';
const TEAL_DARK = '#1a5a4e';
const INK = '#1a1a1a';
const CREAM = '#FDF8F0';
const WARN = '#A8746E';

const TIMER_SECONDS = 30;

type Phase = 'neutral' | 'reveal' | 'consequence';

interface ResolvedCard {
  cardId: string;
  category: TrapCategory;
  spotted: boolean;
  reactionMs?: number;
}

interface Props {
  onBack: () => void;
}

const SpotTheTrap: React.FC<Props> = ({ onBack }) => {
  const allSubjects = useMemo(() => {
    const set = new Set<string>();
    TRAP_CARDS.forEach(c => set.add(c.subject));
    return ['All', ...Array.from(set)];
  }, []);

  const [subject, setSubject] = useState<string>('All');
  const filteredCards = useMemo(() => {
    if (subject === 'All') return TRAP_CARDS;
    return TRAP_CARDS.filter(c => c.subject === subject);
  }, [subject]);

  const [queue, setQueue] = useState(() => filteredCards);
  // re-init queue when filter changes
  useEffect(() => {
    setQueue(filteredCards);
    setIdx(0);
    setHistory([]);
    setPatternBreak(false);
  }, [filteredCards]);

  const [idx, setIdx] = useState(0);
  const card = queue[idx];

  const [history, setHistory] = useState<ResolvedCard[]>([]);
  const [patternBreak, setPatternBreak] = useState(false);
  const [showFinal, setShowFinal] = useState(false);

  const handleResolve = (resolved: ResolvedCard) => {
    const nextHistory = [...history, resolved];
    setHistory(nextHistory);
    const isMultipleOfFive = nextHistory.length > 0 && nextHistory.length % 5 === 0;
    if (isMultipleOfFive && nextHistory.length < queue.length) {
      setPatternBreak(true);
    } else if (nextHistory.length === queue.length) {
      setShowFinal(true);
    } else {
      setIdx(idx + 1);
    }
  };

  const closePatternBreak = () => {
    setPatternBreak(false);
    setIdx(idx + 1);
  };

  const restart = () => {
    setShowFinal(false);
    setIdx(0);
    setHistory([]);
  };

  if (showFinal) {
    return (
      <div className="space-y-6" style={{ color: INK }}>
        <BackBar onBack={onBack} />
        <Hero />
        <FinalReport history={history} totalCards={queue.length} onRestart={restart} />
      </div>
    );
  }

  return (
    <div className="space-y-6" style={{ color: INK }}>
      <BackBar onBack={onBack} />
      <Hero />

      <SubjectFilter subjects={allSubjects} active={subject} onChange={setSubject} />

      <ProgressTrack idx={idx} total={queue.length} history={history} />

      {!patternBreak && card && (
        <Card key={card.id} card={card} onResolve={handleResolve} />
      )}

      {patternBreak && (
        <PatternBreakCard history={history} onContinue={closePatternBreak} />
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
      Necessary Knowledge · Stage 2
    </p>
    <h1 className="font-serif" style={{ fontSize: 30, fontWeight: 600, color: INK, marginTop: 4, lineHeight: 1.15 }}>
      Spot the Trap.
    </h1>
    <p className="font-sans max-w-2xl" style={{ fontSize: 14.5, color: '#5a5550', marginTop: 8, lineHeight: 1.55 }}>
      Past-paper-style questions across six subjects. 30 seconds to spot the trap before the reveal. Every five cards
      we surface a pattern card showing where your blind spots cluster.
    </p>
  </header>
);

// ─── Subject filter ────────────────────────────────────────────────────

const SubjectFilter: React.FC<{
  subjects: string[];
  active: string;
  onChange: (s: string) => void;
}> = ({ subjects, active, onChange }) => (
  <div className="flex flex-wrap gap-1.5">
    {subjects.map(s => {
      const isActive = s === active;
      return (
        <button
          key={s}
          type="button"
          onClick={() => onChange(s)}
          className="font-sans rounded-full"
          style={{
            backgroundColor: isActive ? INK : '#FFFFFF',
            color: isActive ? '#FFFFFF' : INK,
            border: `1.5px solid ${INK}`,
            padding: '6px 14px',
            fontSize: 12,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          {s}
        </button>
      );
    })}
  </div>
);

// ─── Progress track ────────────────────────────────────────────────────

const ProgressTrack: React.FC<{ idx: number; total: number; history: ResolvedCard[] }> = ({ idx, total, history }) => (
  <div className="flex items-center gap-2">
    <div className="flex-1 flex gap-1">
      {Array.from({ length: total }).map((_, i) => {
        const past = history[i];
        const current = i === idx;
        let bg = '#EDEBE8';
        if (past) bg = past.spotted ? TEAL : WARN;
        else if (current) bg = INK;
        return (
          <div
            key={i}
            style={{
              flex: 1,
              height: 4,
              backgroundColor: bg,
              borderRadius: 999,
            }}
          />
        );
      })}
    </div>
    <span className="font-sans" style={{ fontSize: 11, color: '#78716C', whiteSpace: 'nowrap' }}>
      {Math.min(idx + 1, total)} / {total}
    </span>
  </div>
);

// ─── Card ──────────────────────────────────────────────────────────────

const Card: React.FC<{ card: TrapCard; onResolve: (r: ResolvedCard) => void }> = ({ card, onResolve }) => {
  const [phase, setPhase] = useState<Phase>('neutral');
  const [secondsLeft, setSecondsLeft] = useState(TIMER_SECONDS);
  const startMsRef = useRef<number>(Date.now());
  const [verdict, setVerdict] = useState<'spotted' | 'missed' | null>(null);

  // Start timer on neutral phase
  useEffect(() => {
    if (phase !== 'neutral') return;
    setSecondsLeft(TIMER_SECONDS);
    startMsRef.current = Date.now();
    const t = setInterval(() => {
      setSecondsLeft(prev => {
        if (prev <= 1) {
          clearInterval(t);
          // timer expired → treated as missed
          setVerdict(prevV => prevV ?? 'missed');
          setPhase('reveal');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(t);
  }, [phase, card.id]);

  // Reset card when card changes
  useEffect(() => {
    setPhase('neutral');
    setVerdict(null);
  }, [card.id]);

  const handleSpotIt = () => {
    if (phase !== 'neutral') return;
    setVerdict('spotted');
    setPhase('reveal');
  };
  const handleLooksFine = () => {
    if (phase !== 'neutral') return;
    setVerdict('missed');
    setPhase('reveal');
  };

  const handleAdvanceToConsequence = () => {
    setPhase('consequence');
  };

  const handleResolveCard = () => {
    onResolve({
      cardId: card.id,
      category: card.category,
      spotted: verdict === 'spotted',
      reactionMs: verdict === 'spotted' ? Date.now() - startMsRef.current : undefined,
    });
  };

  return (
    <article
      className="rounded-2xl"
      style={{
        backgroundColor: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '26px 28px',
      }}
    >
      <div className="flex items-baseline justify-between gap-3 mb-3 flex-wrap">
        <div className="flex items-baseline gap-2 flex-wrap">
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
            {card.subject}
          </span>
          <span className="font-sans" style={{ fontSize: 11, color: '#9e9186' }}>
            {card.paperLabel}
          </span>
        </div>
        <PhaseBadge phase={phase} secondsLeft={secondsLeft} verdict={verdict} />
      </div>

      <QuestionDisplay card={card} phase={phase} />

      <div className="mt-5">
        {phase === 'neutral' && (
          <NeutralActions onSpot={handleSpotIt} onFine={handleLooksFine} />
        )}
        {phase === 'reveal' && (
          <RevealPanel card={card} verdict={verdict} onContinue={handleAdvanceToConsequence} />
        )}
        {phase === 'consequence' && (
          <ConsequencePanel card={card} onContinue={handleResolveCard} />
        )}
      </div>
    </article>
  );
};

const PhaseBadge: React.FC<{ phase: Phase; secondsLeft: number; verdict: 'spotted' | 'missed' | null }> = ({ phase, secondsLeft, verdict }) => {
  if (phase === 'neutral') {
    return (
      <div className="flex items-center gap-2">
        <TimerRing seconds={secondsLeft} />
        <span className="font-sans" style={{ fontSize: 12, fontWeight: 600, color: INK }}>
          {secondsLeft}s
        </span>
      </div>
    );
  }
  if (phase === 'reveal') {
    return (
      <span
        className="font-sans"
        style={{
          fontSize: 11,
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: 0.5,
          color: verdict === 'spotted' ? TEAL : WARN,
          backgroundColor: verdict === 'spotted' ? `${TEAL}15` : `${WARN}15`,
          border: `1px solid ${verdict === 'spotted' ? TEAL : WARN}`,
          borderRadius: 999,
          padding: '4px 12px',
        }}
      >
        {verdict === 'spotted' ? 'You spotted it' : 'Trap revealed'}
      </span>
    );
  }
  return (
    <span className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: INK }}>
      Consequence
    </span>
  );
};

const TimerRing: React.FC<{ seconds: number }> = ({ seconds }) => {
  const pct = seconds / TIMER_SECONDS;
  const r = 11;
  const c = 2 * Math.PI * r;
  const dash = c * pct;
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden>
      <circle cx="14" cy="14" r={r} fill="none" stroke="#EDEBE8" strokeWidth="2" />
      <circle
        cx="14"
        cy="14"
        r={r}
        fill="none"
        stroke={seconds <= 5 ? WARN : TEAL}
        strokeWidth="2"
        strokeLinecap="round"
        strokeDasharray={`${dash} ${c}`}
        transform="rotate(-90 14 14)"
        style={{ transition: 'stroke-dasharray 1s linear, stroke 0.3s' }}
      />
    </svg>
  );
};

// ─── Question display ─────────────────────────────────────────────────

const QuestionDisplay: React.FC<{ card: TrapCard; phase: Phase }> = ({ card, phase }) => {
  // Render the question with trap spans either neutral or highlighted depending on phase
  return (
    <p
      className="font-serif"
      style={{
        fontSize: 22,
        lineHeight: 1.45,
        color: INK,
        fontStyle: 'italic',
        padding: '18px 22px',
        backgroundColor: CREAM,
        borderRadius: 12,
        border: `1.5px solid ${INK}`,
      }}
    >
      <RenderedQuestion text={card.questionText} spans={card.trapSpans} highlight={phase !== 'neutral'} />
    </p>
  );
};

const RenderedQuestion: React.FC<{
  text: string;
  spans: { start: number; end: number }[];
  highlight: boolean;
}> = ({ text, spans, highlight }) => {
  if (!highlight || spans.length === 0) return <>{text}</>;
  // sort spans, build segments
  const sorted = spans.slice().sort((a, b) => a.start - b.start);
  const parts: { text: string; isTrap: boolean }[] = [];
  let cursor = 0;
  for (const s of sorted) {
    if (s.start > cursor) parts.push({ text: text.slice(cursor, s.start), isTrap: false });
    parts.push({ text: text.slice(s.start, s.end), isTrap: true });
    cursor = s.end;
  }
  if (cursor < text.length) parts.push({ text: text.slice(cursor), isTrap: false });
  return (
    <>
      {parts.map((p, i) =>
        p.isTrap ? (
          <motion.span
            key={i}
            initial={{ backgroundColor: 'transparent' }}
            animate={{ backgroundColor: `${TEAL}33` }}
            transition={{ duration: 0.35 }}
            style={{
              padding: '2px 4px',
              borderRadius: 4,
              fontWeight: 700,
              color: TEAL_DARK,
              borderBottom: `2px solid ${TEAL}`,
              fontStyle: 'normal',
            }}
          >
            {p.text}
          </motion.span>
        ) : (
          <React.Fragment key={i}>{p.text}</React.Fragment>
        ),
      )}
    </>
  );
};

// ─── Phase actions ────────────────────────────────────────────────────

const NeutralActions: React.FC<{ onSpot: () => void; onFine: () => void }> = ({ onSpot, onFine }) => (
  <div className="flex gap-2 flex-wrap">
    <button
      type="button"
      onClick={onSpot}
      className="font-sans rounded-full"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        border: `2px solid ${INK}`,
        padding: '11px 22px',
        fontSize: 13,
        fontWeight: 600,
        cursor: 'pointer',
      }}
    >
      I see the trap
    </button>
    <button
      type="button"
      onClick={onFine}
      className="font-sans rounded-full"
      style={{
        backgroundColor: '#FFFFFF',
        color: INK,
        border: `2px solid ${INK}`,
        padding: '11px 22px',
        fontSize: 13,
        fontWeight: 600,
        cursor: 'pointer',
      }}
    >
      Looks fine
    </button>
  </div>
);

const RevealPanel: React.FC<{ card: TrapCard; verdict: 'spotted' | 'missed' | null; onContinue: () => void }> = ({ card, verdict, onContinue }) => (
  <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
    <div
      className="rounded-xl"
      style={{
        backgroundColor: verdict === 'spotted' ? `${TEAL}10` : `${WARN}10`,
        border: `1.5px solid ${verdict === 'spotted' ? TEAL : WARN}`,
        padding: '14px 16px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: verdict === 'spotted' ? TEAL_DARK : WARN, marginBottom: 6 }}>
        {TRAP_CATEGORY_LABELS[card.category]}
      </p>
      <p className="font-serif" style={{ fontSize: 16, fontWeight: 600, color: INK, marginBottom: 6, lineHeight: 1.4 }}>
        {card.trapLabel}
      </p>
      <p className="font-sans" style={{ fontSize: 13, color: '#3F3B36', lineHeight: 1.6 }}>
        {card.whyStudentsMiss}
      </p>
    </div>
    <div className="mt-3 flex justify-end">
      <button
        type="button"
        onClick={onContinue}
        className="font-sans rounded-full"
        style={{
          backgroundColor: INK,
          color: '#FFFFFF',
          border: `2px solid ${INK}`,
          padding: '9px 20px',
          fontSize: 12.5,
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        See the marks-at-risk
      </button>
    </div>
  </motion.div>
);

const ConsequencePanel: React.FC<{ card: TrapCard; onContinue: () => void }> = ({ card, onContinue }) => (
  <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
    <div
      className="rounded-xl"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        padding: '18px 20px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10.5, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, color: '#FFD8A8', opacity: 0.9, marginBottom: 8 }}>
        Marking-scheme cost
      </p>
      <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', lineHeight: 1.6, marginBottom: 14 }}>
        {card.consequence}
      </p>
      <RiskMeter pct={card.marksAtRiskPct} />
      {card.source.cite && (
        <p className="font-sans" style={{ fontSize: 11, color: '#9e9186', marginTop: 12, fontStyle: 'italic' }}>
          {card.source.cite}
        </p>
      )}
    </div>
    <div className="mt-3 flex justify-end">
      <button
        type="button"
        onClick={onContinue}
        className="font-sans rounded-full"
        style={{
          backgroundColor: INK,
          color: '#FFFFFF',
          border: `2px solid ${INK}`,
          padding: '9px 20px',
          fontSize: 12.5,
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        Next card
        <span style={{ marginLeft: 6 }}>→</span>
      </button>
    </div>
  </motion.div>
);

const RiskMeter: React.FC<{ pct: number }> = ({ pct }) => (
  <div>
    <div className="flex items-baseline justify-between mb-1.5">
      <span className="font-sans" style={{ fontSize: 11, fontWeight: 700, color: '#FFD8A8', opacity: 0.85 }}>
        Marks at risk on this question
      </span>
      <span className="font-serif" style={{ fontSize: 18, fontWeight: 700, color: '#FFFFFF' }}>
        {pct}%
      </span>
    </div>
    <div
      style={{
        height: 8,
        backgroundColor: '#3F3B36',
        borderRadius: 999,
        overflow: 'hidden',
      }}
    >
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        style={{ height: '100%', backgroundColor: WARN }}
      />
    </div>
  </div>
);

// ─── Pattern break ─────────────────────────────────────────────────────

const PatternBreakCard: React.FC<{ history: ResolvedCard[]; onContinue: () => void }> = ({ history, onContinue }) => {
  // Tally categories
  const recent5 = history.slice(-5);
  const recentMisses = recent5.filter(h => !h.spotted);
  const allMisses = history.filter(h => !h.spotted);

  // Top miss category in this batch and overall
  const tally = (entries: ResolvedCard[]) => {
    const m = new Map<TrapCategory, number>();
    entries.forEach(e => m.set(e.category, (m.get(e.category) ?? 0) + 1));
    return Array.from(m.entries()).sort((a, b) => b[1] - a[1]);
  };

  const recentTally = tally(recentMisses);
  const overallTally = tally(allMisses);
  const topCategory = recentTally[0]?.[0] ?? overallTally[0]?.[0] ?? null;
  const topCount = recentTally[0]?.[1] ?? 0;

  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: 'easeOut' }}
      className="rounded-2xl"
      style={{
        backgroundColor: INK,
        color: '#FFFFFF',
        padding: '28px 30px',
      }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Pattern check · {history.length} cards in
      </p>
      <h3 className="font-serif" style={{ fontSize: 22, fontWeight: 600, lineHeight: 1.25, marginTop: 6 }}>
        {recentMisses.length === 0
          ? 'Five cards, five spots. You\'re reading the questions like an examiner.'
          : topCategory && topCount >= 2
          ? `You missed ${topCount} ${TRAP_CATEGORY_LABELS[topCategory].toLowerCase()} in the last five.`
          : `${recentMisses.length} of the last five caught you.`}
      </h3>

      {topCategory && topCount >= 2 && (
        <div className="mt-4">
          <p className="font-sans" style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85, marginBottom: 6 }}>
            Behavioural fix
          </p>
          <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', lineHeight: 1.6 }}>
            {TRAP_CATEGORY_FIXES[topCategory]}
          </p>
        </div>
      )}

      {recentMisses.length === 0 && (
        <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', lineHeight: 1.6, marginTop: 4 }}>
          That five-card streak is the trap-reader&rsquo;s habit forming. Keep reading every cue twice — modifier, count, restriction, command — before answering.
        </p>
      )}

      <div className="mt-6 flex justify-end">
        <button
          type="button"
          onClick={onContinue}
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
          Keep going
          <span style={{ marginLeft: 6 }}>→</span>
        </button>
      </div>
    </motion.section>
  );
};

// ─── Final report ──────────────────────────────────────────────────────

const FinalReport: React.FC<{ history: ResolvedCard[]; totalCards: number; onRestart: () => void }> = ({ history, totalCards, onRestart }) => {
  const spotted = history.filter(h => h.spotted).length;
  const byCategory = useMemo(() => {
    const cats = Array.from(new Set(history.map(h => h.category)));
    return cats.map(cat => {
      const entries = history.filter(h => h.category === cat);
      const hits = entries.filter(h => h.spotted).length;
      return { category: cat, total: entries.length, hits };
    }).sort((a, b) => (a.hits / a.total) - (b.hits / b.total)); // worst first
  }, [history]);

  const blindSpot = byCategory.find(c => c.total >= 1 && c.hits / c.total <= 0.5);

  // Persist the weakest trap category to localStorage for the cross-module
  // "Your patterns" panel.
  useEffect(() => {
    if (history.length < 5) return;
    const accuracyByCategory: Record<string, number> = {};
    byCategory.forEach(b => {
      accuracyByCategory[b.category] = b.total > 0 ? b.hits / b.total : 0;
    });
    const weakest = byCategory[0]; // already sorted worst-first
    if (!weakest) return;
    writePattern('spotTrap', {
      weakestCategory: weakest.category,
      accuracyByCategory,
      sampleSize: history.length,
      updatedAt: Date.now(),
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [history.length]);

  return (
    <section
      className="rounded-2xl"
      style={{ backgroundColor: INK, color: '#FFFFFF', padding: '32px 32px 28px' }}
    >
      <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.85 }}>
        Your trap map
      </p>
      <h2 className="font-serif" style={{ fontSize: 26, fontWeight: 600, lineHeight: 1.2, marginTop: 6 }}>
        {spotted} of {totalCards} traps caught.
      </h2>

      <div className="mt-6 space-y-3">
        {byCategory.map(b => {
          const pct = (b.hits / b.total) * 100;
          return (
            <div key={b.category}>
              <div className="flex items-baseline justify-between mb-1">
                <span className="font-sans" style={{ fontSize: 12, fontWeight: 600, color: '#FFFFFF' }}>
                  {TRAP_CATEGORY_LABELS[b.category]}
                </span>
                <span className="font-sans" style={{ fontSize: 11, color: '#FFD8A8', opacity: 0.85 }}>
                  {b.hits}/{b.total}
                </span>
              </div>
              <div style={{ height: 6, backgroundColor: '#3F3B36', borderRadius: 999, overflow: 'hidden' }}>
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${pct}%` }}
                  transition={{ duration: 0.6, ease: 'easeOut' }}
                  style={{ height: '100%', backgroundColor: pct >= 67 ? TEAL : WARN }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {blindSpot && (
        <div className="mt-7" style={{ borderLeft: `3px solid ${TEAL}`, paddingLeft: 16 }}>
          <p className="font-sans" style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.6, color: '#FFD8A8', opacity: 0.9 }}>
            Your biggest blind spot
          </p>
          <h4 className="font-serif" style={{ fontSize: 17, fontWeight: 600, marginTop: 4, marginBottom: 6 }}>
            {TRAP_CATEGORY_LABELS[blindSpot.category]}
          </h4>
          <p className="font-sans" style={{ fontSize: 13.5, color: '#E8E4DE', lineHeight: 1.6 }}>
            {TRAP_CATEGORY_FIXES[blindSpot.category]}
          </p>
        </div>
      )}

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
          Run again
        </button>
      </div>
    </section>
  );
};

export default SpotTheTrap;
