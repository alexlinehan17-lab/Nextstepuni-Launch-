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

import React, { useMemo, useState } from 'react';
import { ArrowLeft, ExternalLink, RotateCcw } from 'lucide-react';
import {
  addCard,
  dueCards,
  gradeCard,
  loadDeck,
  schedule,
  type ReviewCard,
  type ReviewGrade,
} from './reviewStore';
import { topicLabel, topicsForPaper, type TopicSibling } from './topics';
import { allMarks } from './attemptStore';
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
  // Snapshot the due queue once, at mount — grading reschedules cards out of the
  // due set, so a live query would shrink under us. `again` re-queues in-session.
  const [queue, setQueue] = useState<ReviewCard[]>(() => dueCards(uid, now));
  const [pos, setPos] = useState(0);
  const [done, setDone] = useState(0);
  const [deckSize, setDeckSize] = useState(() => loadDeck(uid).length);

  const card = queue[pos];

  const projected = useMemo(() => {
    if (!card) return {} as Record<ReviewGrade, number>;
    const out = {} as Record<ReviewGrade, number>;
    for (const { g } of GRADES) out[g] = schedule(card, g).intervalDays;
    return out;
  }, [card]);

  const rate = (g: ReviewGrade) => {
    if (!card) return;
    gradeCard(uid, card, g, now);
    setDone(d => d + 1);
    // A failed card comes back before the session ends.
    if (g === 'again') setQueue(q => [...q, card]);
    setPos(p => p + 1);
  };

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

  // ── Empty / caught-up states ──
  if (!card) {
    const weakCount = allMarks(uid).filter(m => m.max > 0 && m.score < m.max).length;
    const nextDue = loadDeck(uid)
      .map(c => c.dueTs)
      .filter(ts => ts > now)
      .sort((a, b) => a - b)[0];
    const daysToNext = nextDue ? Math.max(1, Math.round((nextDue - now) / 86_400_000)) : null;
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header}
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Daily review</h2>
        {done > 0 ? (
          <p className="text-[14px] mb-5" style={{ color: '#1F5F3E' }}>
            Reviewed {done} card{done === 1 ? '' : 's'} — nice work.{daysToNext ? ` Next batch due in ${daysToNext} day${daysToNext === 1 ? '' : 's'}.` : ''}
          </p>
        ) : deckSize > 0 ? (
          <p className="text-[14px] mb-5" style={{ color: '#5a5550' }}>
            You’re all caught up — {deckSize} card{deckSize === 1 ? '' : 's'} scheduled{daysToNext ? `, next due in ${daysToNext} day${daysToNext === 1 ? '' : 's'}` : ''}.
          </p>
        ) : (
          <p className="text-[14px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
            Your review deck is empty. Save questions from <span style={{ color: INK, fontWeight: 600 }}>Revise by topic</span> to drill them on a spaced schedule — or seed it from the questions you’ve already self-marked below full marks.
          </p>
        )}
        {weakCount > 0 && (
          <button
            onClick={seedFromWeak}
            className="inline-flex items-center gap-2 rounded-full px-5 py-2.5 text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
            style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
          >
            Seed from my {weakCount} weak question{weakCount === 1 ? '' : 's'}
          </button>
        )}
      </div>
    );
  }

  const total = queue.length;
  const topic = card.topicId ? topicLabel(card.topicId) : null;

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {header}
      {/* Progress */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Daily review</h2>
        <span className="text-[12px] font-medium tabular-nums" style={{ color: '#9e9186' }}>{done + 1} / {total}</span>
      </div>
      <div className="h-1.5 rounded-full mb-6 overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
        <div className="h-full rounded-full transition-all" style={{ width: `${(done / total) * 100}%`, backgroundColor: ACCENT }} />
      </div>

      {/* Card */}
      <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-6 mb-5">
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
      </div>

      {/* Rating */}
      <p className="text-[12px] mb-2 text-center" style={{ color: '#7a7068' }}>How well did you recall it?</p>
      <div className="grid grid-cols-4 gap-2">
        {GRADES.map(({ g, label }) => (
          <button
            key={g}
            onClick={() => rate(g)}
            className="flex flex-col items-center gap-0.5 rounded-xl border-2 py-2.5 text-[13px] font-semibold transition-transform active:translate-y-0.5"
            style={gradeStyle(g)}
          >
            {label}
            <span className="text-[10.5px] font-medium tabular-nums opacity-80">{fmtInterval(projected[g])}</span>
          </button>
        ))}
      </div>

      <button
        onClick={onBack}
        className="flex items-center gap-1.5 mx-auto mt-6 text-[12px] font-medium"
        style={{ color: '#9e9186' }}
      >
        <RotateCcw size={13} /> End session
      </button>
    </div>
  );
};

export default ReviewSession;
