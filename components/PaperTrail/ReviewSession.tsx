/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — daily spaced-recall session (feature A2). Runs through the cards
 * due today, one at a time: the student tries to recall the full-marks answer to
 * a real past question, optionally opens it beside its marking scheme to check,
 * then rates their recall (Again / Hard / Good / Easy). SM-2 reschedules each
 * card. No fabricated answers — every card points at a genuine SEC question.
 */

import { usePulse } from '../../hooks/usePulse';
import Rua from '../ui/Rua';
import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ExternalLink, RotateCcw, Settings2, Trash2 } from 'lucide-react';
import {
  addCard,
  dueCards,
  gradeCard,
  getTargetRetention,
  loadDeck,
  projectInterval,
  removeCard,
  setTargetRetention,
  type ReviewCard,
  type ReviewGrade,
} from './reviewStore';
import { siblingsFor, topicLabel, topicsForPaper, type TopicSibling } from './topics';
import { allMarks } from './attemptStore';
import { computeProgress } from './progressStats';
import { recordActivity } from './streakStore';
import { topUpDaily } from './dailySet';
import { ArrowRight, Check } from 'lucide-react';
import { AnimatePresence, MotionDiv, useReducedMotion } from '../Motion';
import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };

const fmtInterval = (days: number) => (days < 1 ? '<1d' : days < 30 ? `${days}d` : `${Math.round(days / 30)}mo`);

const GRADES: { g: ReviewGrade; label: string }[] = [
  { g: 'again', label: 'Again' },
  { g: 'hard', label: 'Hard' },
  { g: 'good', label: 'Good' },
  { g: 'easy', label: 'Easy' },
];

// Rating colours stay inside the token system: Again/Hard are neutral (muted),
// Good is the accent action, Easy is success ("nailed it"). Never red.
const gradeStyle = (g: ReviewGrade): React.CSSProperties => {
  if (g === 'good') return { backgroundColor: ACCENT, color: '#fff', borderColor: ACCENT };
  if (g === 'easy') return { backgroundColor: '#E8F2EC', color: '#1F5F3E', borderColor: '#3A8D5F' };
  return { backgroundColor: '#fff', color: '#7a7068', borderColor: '#d0cdc8' };
};

const asSibling = (c: ReviewCard): TopicSibling => ({
  subjectId: c.subjectId,
  level: c.level,
  lang: c.lang,
  year: c.year,
  fileid: c.fileid,
  paperKey: '',
  n: c.n,
});

interface Props {
  uid?: string;
  now: number;
  subjectLabel: (id: string) => string;
  onOpenQuestion: (t: TopicSibling) => void;
  onBack: () => void;
}

const ReviewSession: React.FC<Props> = ({ uid, now, subjectLabel, onOpenQuestion, onBack }) => {
  // Snapshot the due queue once, at mount — after topping the daily set up to ~10
  // from the weakest topics. Grading reschedules cards out of the due set, so a
  // live query would shrink under us; `again` re-queues in-session.
  const [queue, setQueue] = useState<ReviewCard[]>(() => {
    topUpDaily(uid, now);
    return dueCards(uid, now);
  });
  const [pos, setPos] = useState(0);
  const [done, setDone] = useState(0);
  const [deckSize, setDeckSize] = useState(() => loadDeck(uid).length);
  const [managing, setManaging] = useState(false);
  const [deckVer, setDeckVer] = useState(0); // bump to re-read the deck list
  const [retention, setRetentionState] = useState(() => getTargetRetention(uid));
  // Restrained correct-recall micro-celebration.
  const [flash, pulseFlash] = usePulse(550);
  // Round summaries: grades this session, and whether we're on a break screen.
  const [gradeLog, setGradeLog] = useState<ReviewGrade[]>([]);
  const [roundBreak, setRoundBreak] = useState(false);
  const reduceMotion = useReducedMotion();

  const card = queue[pos];

  const projected = useMemo(() => {
    if (!card) return {} as Record<ReviewGrade, number>;
    const out = {} as Record<ReviewGrade, number>;
    for (const { g } of GRADES) out[g] = projectInterval(card, g, now, uid);
    return out;
  }, [card, now, uid]);

  const rate = (g: ReviewGrade) => {
    if (!card) return;
    gradeCard(uid, card, g, now);
    recordActivity(uid, now, 1); // feeds the practice streak + daily goal
    setDone(d => d + 1);
    setGradeLog(l => [...l, g]);
    // Restrained micro-celebration on genuine recall (Good/Easy), never on a miss.
    if (g === 'good' || g === 'easy') pulseFlash();
    // A failed card comes back before the session ends.
    if (g === 'again') setQueue(q => [...q, card]);
    setPos(p => p + 1);
    // Every ten cards, a breath: the round summary (Quizlet's Learn rhythm).
    if ((done + 1) % 10 === 0) setRoundBreak(true);
  };

  // "Review ahead": when caught up, let a keen student work their whole deck
  // early (soonest-due first). Grading still reschedules honestly from now.
  const reviewAhead = () => {
    const all = loadDeck(uid).sort((a, b) => a.dueTs - b.dueTs);
    if (!all.length) return;
    setQueue(all);
    setPos(0);
    setDone(0);
  };

  // Keyboard: 1–4 rate the current card, O opens it. Active only while a card is
  // showing (not in the deck manager). Mobile is unaffected.
  useEffect(() => {
    if (!card || managing) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const map: Record<string, ReviewGrade> = { '1': 'again', '2': 'hard', '3': 'good', '4': 'easy' };
      if (map[e.key]) {
        e.preventDefault();
        rate(map[e.key]);
      } else if (e.key === 'o' || e.key === 'O') {
        e.preventDefault();
        onOpenQuestion(asSibling(card));
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [card, managing]);

  const finePointer = typeof window !== 'undefined' && !!window.matchMedia?.('(pointer: fine)').matches;

  const seedFromWeak = () => {
    const weak = allMarks(uid).filter(m => m.max > 0 && m.score < m.max);
    for (const m of weak) {
      const tags = topicsForPaper(m.subjectId, m.year, m.level as PaperLevel, m.lang as PaperLang, m.fileid);
      const topicId = tags?.q.find(q => q.n === m.n)?.primary;
      addCard(uid, { subjectId: m.subjectId, year: m.year, level: m.level as PaperLevel, lang: m.lang as PaperLang, fileid: m.fileid, n: m.n }, topicId, now);
    }
    setQueue(dueCards(uid, now));
    setPos(0);
    setDone(0);
    setDeckSize(loadDeck(uid).length);
  };

  const header = (
    <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
      <ArrowLeft size={15} /> Paper Trail
    </button>
  );

  const removeFromDeck = (c: ReviewCard) => {
    removeCard(uid, c);
    setDeckSize(loadDeck(uid).length);
    setDeckVer(v => v + 1);
  };
  const dueText = (dueTs: number) => {
    const d = Math.round((dueTs - now) / 86_400_000);
    return d <= 0 ? 'due now' : d === 1 ? 'due tomorrow' : `due in ${d} days`;
  };

  // ── Deck manager ──
  if (managing) {
    void deckVer;
    const deck = loadDeck(uid);
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setManaging(false)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> Daily review
        </button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Your review deck</h2>
        <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>
          {deck.length} card{deck.length === 1 ? '' : 's'} · {deck.filter(c => c.dueTs <= now).length} due today
        </p>

        {/* Recall strength (FSRS target retention). */}
        <div className="rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3.5 py-3 mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[12.5px] font-semibold" style={{ color: INK }}>Recall strength</span>
            <span className="text-[11px]" style={{ color: '#9e9186' }}>how sure before a card returns</span>
          </div>
          <div className="flex items-center gap-1 p-1 rounded-lg bg-zinc-100 dark:bg-zinc-800/50" role="group" aria-label="Recall strength">
            {([['Relaxed', 0.85], ['Balanced', 0.9], ['Strong', 0.95]] as const).map(([label, r]) => (
              <button
                key={label}
                aria-pressed={Math.abs(retention - r) < 0.001}
                onClick={() => { setTargetRetention(uid, r); setRetentionState(r); }}
                className={`flex-1 py-1.5 rounded-md text-[12px] font-semibold transition-all ${Math.abs(retention - r) < 0.001 ? 'bg-white dark:bg-zinc-800 shadow-sm' : ''}`}
                style={{ color: Math.abs(retention - r) < 0.001 ? '#F26B1F' : '#7a7068' }}
              >
                {label}<span className="ml-1 text-[10px] opacity-70 tabular-nums">{Math.round(r * 100)}%</span>
              </button>
            ))}
          </div>
        </div>
        {deck.length === 0 ? (
          <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
            Your deck is empty. Add questions from Revise by topic to build it.
          </p>
        ) : (
          <div className="space-y-1.5">
            {deck.map(c => (
              <div key={`${c.subjectId}-${c.year}-${c.level}-${c.lang}-${c.fileid}-${c.n}`} className="flex items-center gap-2 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 pr-2">
                <button onClick={() => onOpenQuestion(asSibling(c))} className="flex-1 px-3.5 py-2.5 text-left transition-transform active:translate-y-0.5">
                  <span className="block text-[13px] font-semibold" style={{ color: INK }}>
                    {subjectLabel(c.subjectId)}{c.topicId ? ` · ${topicLabel(c.topicId)}` : ''}
                  </span>
                  <span className="block text-[11.5px]" style={{ color: '#7a7068' }}>
                    {c.year} · {LVL[c.level] ?? c.level} · Q{c.n} · {c.lastTs === 0 ? 'new' : dueText(c.dueTs)}
                  </span>
                </button>
                <button
                  onClick={() => removeFromDeck(c)}
                  aria-label="Remove from deck"
                  title="Remove from deck"
                  className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border-2"
                  style={{ borderColor: '#d0cdc8', color: '#9e9186' }}
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  // ── Round break — every ten cards, show the round's shape before going on ──
  if (roundBreak && card) {
    const round = gradeLog.slice(-10);
    const know = round.filter(g => g === 'good' || g === 'easy').length;
    const shaky = round.length - know;
    const pct = round.length ? know / round.length : 0;
    const C = 2 * Math.PI * 44;
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header}
        <div className="rounded-2xl bg-white dark:bg-zinc-900 px-6 py-7" style={{ border: '1.5px solid #383838' }}>
          <div className="flex items-start justify-between gap-4">
            <p className="text-[10px] font-bold uppercase tracking-[0.16em]" style={{ color: '#A0968D' }}>Round complete · {done} reviewed</p>
            <Rua pose="cheer" size={52} className="-mt-3 shrink-0" />
          </div>
          <div className="mt-4 flex flex-wrap items-center gap-6">
            <div className="relative h-[104px] w-[104px] shrink-0">
              <svg width="104" height="104" viewBox="0 0 104 104" className="-rotate-90" aria-hidden="true">
                <circle cx="52" cy="52" r="44" fill="none" stroke="#ECE8E3" strokeWidth="7" className="dark:stroke-zinc-700" />
                <circle cx="52" cy="52" r="44" fill="none" strokeWidth="7" strokeLinecap="round"
                  stroke={pct >= 1 ? '#3A8D5F' : 'rgba(242,107,31,0.62)'}
                  strokeDasharray={C} strokeDashoffset={C * (1 - pct)} />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-serif text-[24px] font-bold tabular-nums leading-none" style={{ color: INK }}>{know}/{round.length}</span>
                <span className="mt-1 text-[8.5px] font-bold uppercase tracking-[0.14em]" style={{ color: '#A0968D' }}>Recalled</span>
              </div>
            </div>
            <div className="min-w-[180px] flex-1 space-y-1.5 text-[13px]" style={{ color: '#3a3530' }}>
              <p className="flex items-center gap-2"><span aria-hidden="true" className="h-[9px] w-[9px] rounded-full bg-[#3A8D5F]" /><b className="font-bold" style={{ color: INK }}>{know} solid</b> — recalled without help</p>
              <p className="flex items-center gap-2"><span aria-hidden="true" className="h-[9px] w-[9px] rounded-full border-[1.5px] border-[#D6D3D0]" /><b className="font-bold" style={{ color: INK }}>{shaky} still settling</b> — they will come back around</p>
              <p className="pt-1 text-[11.5px]" style={{ color: '#A8A29E' }}>{queue.length - pos} card{queue.length - pos === 1 ? '' : 's'} left in this session.</p>
            </div>
          </div>
          <div className="mt-6 flex items-center gap-3">
            <button onClick={() => setRoundBreak(false)}
              className="rounded-xl bg-[#1A1A1A] px-5 py-2.5 text-sm font-bold text-white transition-transform hover:-translate-y-0.5 dark:bg-white dark:text-zinc-900">
              Keep going
            </button>
            <button onClick={() => { setRoundBreak(false); setQueue(q => q.slice(0, pos)); }}
              className="text-[13px] font-semibold" style={{ color: '#7a7068' }}>
              Finish for now
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── Empty / caught-up states ──
  if (!card) {
    const weakCount = allMarks(uid).filter(m => m.max > 0 && m.score < m.max).length;
    const nextDue = loadDeck(uid)
      .map(c => c.dueTs)
      .filter(ts => ts > now)
      .sort((a, b) => a - b)[0];
    const daysToNext = nextDue ? Math.max(1, Math.round((nextDue - now) / 86_400_000)) : null;
    // "What next" — once the deck is clear, point at the weakest topic so review
    // flows straight into targeted practice. Only for students who've practised.
    const weakest = deckSize > 0 || done > 0 ? computeProgress(uid, now).weakestTopics.find(t => t.avg < 60) : undefined;
    const drillWeakest = () => {
      if (!weakest) return;
      const sib = siblingsFor(weakest.subjectId, weakest.subtopicId)[0];
      if (sib) onOpenQuestion(sib);
    };
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header}
        <div className="flex items-start justify-between gap-4">
          <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Daily review</h2>
          <Rua pose={done > 0 ? 'nod' : deckSize > 0 ? 'perch' : 'think'} size={56} className="shrink-0" />
        </div>
        {done > 0 ? (
          <div className="mb-5">
            <p className="text-[14px]" style={{ color: '#1F5F3E' }}>
              Reviewed {done} card{done === 1 ? '' : 's'} — nice work.{daysToNext ? ` Next batch due in ${daysToNext} day${daysToNext === 1 ? '' : 's'}.` : ''}
            </p>
            {gradeLog.length > 0 && (
              <p className="mt-1.5 text-[12.5px]" style={{ color: '#7a7068' }}>
                <b className="font-bold" style={{ color: '#3A8D5F' }}>{gradeLog.filter(g => g === 'good' || g === 'easy').length} solid</b>
                {' · '}
                <b className="font-bold" style={{ color: INK }}>{gradeLog.filter(g => g === 'again' || g === 'hard').length} still settling</b>
              </p>
            )}
          </div>
        ) : deckSize > 0 ? (
          <p className="text-[14px] mb-5" style={{ color: '#5a5550' }}>
            You’re all caught up — {deckSize} card{deckSize === 1 ? '' : 's'} scheduled{daysToNext ? `, next due in ${daysToNext} day${daysToNext === 1 ? '' : 's'}` : ''}.
          </p>
        ) : (
          <p className="text-[14px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
            Your review deck is empty. Save questions from <span style={{ color: INK, fontWeight: 600 }}>Revise by topic</span> to drill them on a spaced schedule — or seed it from the questions you’ve already self-marked below full marks.
          </p>
        )}
        {weakCount > 0 && deckSize === 0 && (
          <button
            onClick={seedFromWeak}
            className="inline-flex items-center gap-2 rounded-full px-5 py-2.5 text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
            style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
          >
            Seed from my {weakCount} weak question{weakCount === 1 ? '' : 's'}
          </button>
        )}
        {deckSize > 0 && (
          <button
            onClick={reviewAhead}
            className="inline-flex items-center gap-2 rounded-full px-5 py-2.5 text-[13.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
            style={{ borderColor: 'rgba(242,107,31,0.35)', color: ACCENT }}
          >
            Review ahead ({deckSize})
          </button>
        )}
        {weakest && (
          <button
            onClick={drillWeakest}
            className="w-full flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3.5 py-3 mt-4 text-left transition-transform active:translate-y-0.5 hover:border-[#F26B1F]"
          >
            <span className="flex-1 min-w-0">
              <span className="block text-[10.5px] font-bold uppercase tracking-[0.1em]" style={{ color: '#9e9186' }}>Keep going</span>
              <span className="block text-[13.5px] font-semibold" style={{ color: INK }}>Drill your weakest topic: {topicLabel(weakest.subtopicId)}</span>
              <span className="block text-[11.5px]" style={{ color: '#7a7068' }}>{subjectLabel(weakest.subjectId)} · you’re averaging {weakest.avg}%</span>
            </span>
            <ArrowRight size={16} className="shrink-0" style={{ color: ACCENT }} />
          </button>
        )}
        {deckSize > 0 && (
          <button onClick={() => setManaging(true)} className="flex items-center gap-1.5 mt-5 text-[12.5px] font-semibold" style={{ color: '#7a7068' }}>
            <Settings2 size={14} /> Manage deck ({deckSize})
          </button>
        )}
      </div>
    );
  }

  const total = queue.length;
  const topic = card.topicId ? topicLabel(card.topicId) : null;

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {/* Correct-recall micro-celebration — subtle, brief, never on a miss. */}
      <AnimatePresence>
        {flash && !reduceMotion && (
          <MotionDiv
            key="recall-flash"
            initial={{ opacity: 0, scale: 0.6 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.1 }}
            transition={{ duration: 0.22, ease: 'easeOut' }}
            className="pointer-events-none fixed inset-0 z-[120] flex items-center justify-center"
          >
            <span className="w-16 h-16 rounded-full flex items-center justify-center" style={{ backgroundColor: '#E8F2EC', border: '2px solid #3A8D5F' }}>
              <Check size={30} style={{ color: '#3A8D5F' }} />
            </span>
          </MotionDiv>
        )}
      </AnimatePresence>
      {header}
      {/* Progress */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Daily review</h2>
        <span className="text-[12px] font-medium tabular-nums" style={{ color: '#9e9186' }}>{done + 1} / {total}</span>
      </div>
      <div className="h-1.5 rounded-full mb-6 overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
        <div className="h-full rounded-full transition-all" style={{ width: `${(done / total) * 100}%`, backgroundColor: ACCENT }} />
      </div>

      {/* Card — animates in/out as the student rates and the next card arrives. */}
      <AnimatePresence mode="wait">
        <MotionDiv
          key={`${card.subjectId}-${card.year}-${card.level}-${card.lang}-${card.fileid}-${card.n}-${done}`}
          initial={reduceMotion ? { opacity: 0 } : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={reduceMotion ? { opacity: 0 } : { opacity: 0, y: -10 }}
          transition={{ duration: reduceMotion ? 0 : 0.2, ease: 'easeOut' }}
          className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-6 mb-5"
        >
          <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>
            {subjectLabel(card.subjectId)}{topic ? ` · ${topic}` : ''}
          </p>
          <p className="text-[19px] font-semibold leading-snug mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
            {card.year} · {LVL[card.level] ?? card.level} · Question {card.n}
          </p>
          <p className="text-[13.5px] leading-relaxed mt-3" style={{ color: '#5a5550' }}>
            Try to recall how you’d earn full marks on this question — the structure of the answer, the key points, the method. Then check yourself against the marking scheme.
          </p>
          <button
            onClick={() => onOpenQuestion(asSibling(card))}
            className="inline-flex items-center gap-1.5 mt-4 text-[13px] font-semibold"
            style={{ color: ACCENT }}
          >
            Open question + marking scheme <ExternalLink size={14} />
          </button>
        </MotionDiv>
      </AnimatePresence>

      {/* Rating */}
      <p className="text-[12px] mb-2 text-center" style={{ color: '#7a7068' }}>How well did you recall it?</p>
      <div className="grid grid-cols-4 gap-2">
        {GRADES.map(({ g, label }, i) => (
          <button
            key={g}
            onClick={() => rate(g)}
            className="flex flex-col items-center gap-0.5 rounded-xl border-2 py-2.5 text-[13px] font-semibold transition-transform active:translate-y-0.5"
            style={gradeStyle(g)}
          >
            {label}
            <span className="text-[10.5px] font-medium tabular-nums opacity-80">{fmtInterval(projected[g])}</span>
            {finePointer && <span className="text-[9px] font-bold opacity-50 tabular-nums">{i + 1}</span>}
          </button>
        ))}
      </div>
      {finePointer && (
        <p className="text-[10.5px] mt-2 text-center" style={{ color: '#b0a898' }}>Press 1–4 to rate · O to open the paper</p>
      )}

      <div className="flex items-center justify-center gap-5 mt-6">
        <button onClick={onBack} className="flex items-center gap-1.5 text-[12px] font-medium" style={{ color: '#9e9186' }}>
          <RotateCcw size={13} /> End session
        </button>
        <button onClick={() => setManaging(true)} className="flex items-center gap-1.5 text-[12px] font-medium" style={{ color: '#9e9186' }}>
          <Settings2 size={13} /> Manage deck
        </button>
      </div>
    </div>
  );
};

export default ReviewSession;
