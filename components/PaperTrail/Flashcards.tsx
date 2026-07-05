/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — student flashcards (feature E6). Author your own question/answer
 * cards and drill them with the same FSRS spacing as the past-paper deck: see
 * the front, try to recall, flip to your answer, rate honestly. A calm three-
 * mode surface — browse/create, edit, and a flip-review session.
 */

import React, { useState } from 'react';
import { ArrowLeft, Plus, Pencil, Trash2, RotateCcw } from 'lucide-react';
import {
  cardStats,
  createCard,
  deleteCard,
  dueCards,
  gradeCard,
  loadCards,
  projectCardInterval,
  updateCard,
  type Flashcard,
} from './flashcardStore';
import { type ReviewGrade } from './reviewStore';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

const GRADES: { g: ReviewGrade; label: string }[] = [
  { g: 'again', label: 'Again' },
  { g: 'hard', label: 'Hard' },
  { g: 'good', label: 'Good' },
  { g: 'easy', label: 'Easy' },
];
const gradeStyle = (g: ReviewGrade): React.CSSProperties => {
  if (g === 'good') return { backgroundColor: ACCENT, color: '#fff', borderColor: ACCENT };
  if (g === 'easy') return { backgroundColor: '#E8F2EC', color: '#1F5F3E', borderColor: '#3A8D5F' };
  return { backgroundColor: '#fff', color: '#7a7068', borderColor: '#d0cdc8' };
};
const fmtInterval = (d: number) => (d < 1 ? '<1d' : d < 30 ? `${d}d` : `${Math.round(d / 30)}mo`);
const dueLabel = (dueTs: number, now: number, lastTs: number) => {
  if (lastTs === 0) return 'new';
  const d = Math.round((dueTs - now) / 86_400_000);
  return d <= 0 ? 'due now' : d === 1 ? 'due tomorrow' : `due in ${d}d`;
};

interface Props {
  uid?: string;
  now: number;
  onBack: () => void;
}

const Flashcards: React.FC<Props> = ({ uid, now, onBack }) => {
  const [mode, setMode] = useState<'list' | 'edit' | 'review'>('list');
  const [cards, setCards] = useState<Flashcard[]>(() => loadCards(uid));
  const [editing, setEditing] = useState<Flashcard | null>(null);
  const [front, setFront] = useState('');
  const [back, setBack] = useState('');
  const [queue, setQueue] = useState<Flashcard[]>([]);
  const [pos, setPos] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const stats = cardStats(uid, now);
  const backToList = () => { setCards(loadCards(uid)); setMode('list'); };

  const openEditor = (card: Flashcard | null) => {
    setEditing(card);
    setFront(card?.front ?? '');
    setBack(card?.back ?? '');
    setMode('edit');
  };
  const save = () => {
    if (!front.trim() || !back.trim()) return;
    if (editing) updateCard(uid, editing.id, front, back);
    else createCard(uid, front, back, undefined, now);
    backToList();
  };
  const remove = (id: string) => setCards(deleteCard(uid, id));

  const startReview = () => {
    const due = dueCards(uid, now);
    if (!due.length) return;
    setQueue(due);
    setPos(0);
    setFlipped(false);
    setMode('review');
  };
  const rate = (g: ReviewGrade) => {
    const card = queue[pos];
    if (!card) return;
    gradeCard(uid, card.id, g, now);
    if (g === 'again') setQueue(q => [...q, card]);
    setFlipped(false);
    setPos(p => p + 1);
  };

  const header = (label: string, onClick: () => void) => (
    <button onClick={onClick} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
      <ArrowLeft size={15} /> {label}
    </button>
  );

  // ── Edit / create ──
  if (mode === 'edit') {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header('Flashcards', backToList)}
        <h2 className="text-2xl font-semibold mb-4" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{editing ? 'Edit card' : 'New card'}</h2>
        <label className="block text-[11px] font-bold uppercase tracking-[0.1em] mb-1.5" style={{ color: '#9e9186' }}>Front — the prompt</label>
        <textarea value={front} onChange={e => setFront(e.target.value)} rows={2} placeholder="e.g. State Le Chatelier's principle"
          className="w-full mb-4 px-3.5 py-2.5 rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 text-[14px] outline-none focus:border-[#F26B1F]" />
        <label className="block text-[11px] font-bold uppercase tracking-[0.1em] mb-1.5" style={{ color: '#9e9186' }}>Back — the answer</label>
        <textarea value={back} onChange={e => setBack(e.target.value)} rows={4} placeholder="Your answer, in your own words"
          className="w-full mb-5 px-3.5 py-2.5 rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 text-[14px] outline-none focus:border-[#F26B1F]" />
        <div className="flex items-center gap-2.5">
          <button onClick={save} disabled={!front.trim() || !back.trim()}
            className="rounded-full px-6 py-2.5 text-[14px] font-semibold text-white disabled:opacity-40 transition-transform active:translate-y-0.5"
            style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}>Save card</button>
          <button onClick={backToList} className="rounded-full px-4 py-2.5 text-[13px] font-medium" style={{ color: '#7a7068' }}>Cancel</button>
        </div>
      </div>
    );
  }

  // ── Review (flip) ──
  if (mode === 'review') {
    const card = queue[pos];
    if (!card) {
      return (
        <div className="w-full max-w-xl mx-auto pb-12">
          {header('Flashcards', backToList)}
          <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>All done</h2>
          <p className="text-[14px]" style={{ color: '#1F5F3E' }}>You reviewed every due card — nice work.</p>
        </div>
      );
    }
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <div className="flex items-center justify-between mb-4">
          <button onClick={backToList} className="flex items-center gap-1.5 text-[13px] font-medium" style={{ color: '#7a7068' }}>
            <ArrowLeft size={15} /> End
          </button>
          <span className="text-[12px] font-medium tabular-nums" style={{ color: '#9e9186' }}>{pos + 1} / {queue.length}</span>
        </div>
        <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-7 mb-5 min-h-[180px] flex flex-col">
          <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>Prompt</p>
          <p className="text-[17px] font-semibold leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{card.front}</p>
          {flipped && (
            <>
              <div className="my-4 border-t-2 border-dashed" style={{ borderColor: '#e0dbd4' }} />
              <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#1F5F3E' }}>Your answer</p>
              <p className="text-[14.5px] leading-relaxed whitespace-pre-wrap" style={{ color: '#3a3530' }}>{card.back}</p>
            </>
          )}
        </div>
        {!flipped ? (
          <button onClick={() => setFlipped(true)}
            className="w-full py-3 rounded-full text-[14.5px] font-semibold text-white transition-transform active:translate-y-0.5"
            style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}>Show answer</button>
        ) : (
          <>
            <p className="text-[12px] mb-2 text-center" style={{ color: '#7a7068' }}>How well did you recall it?</p>
            <div className="grid grid-cols-4 gap-2">
              {GRADES.map(({ g, label }) => (
                <button key={g} onClick={() => rate(g)}
                  className="flex flex-col items-center gap-0.5 rounded-xl border-2 py-2.5 text-[13px] font-semibold transition-transform active:translate-y-0.5"
                  style={gradeStyle(g)}>
                  {label}
                  <span className="text-[10.5px] font-medium tabular-nums opacity-80">{fmtInterval(projectCardInterval(card, g, now, uid))}</span>
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    );
  }

  // ── List / home ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {header('Paper Trail', onBack)}
      <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>Flashcards</h2>
      <p className="text-[13.5px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
        Write your own cards for anything the papers don’t cover — definitions, formulae, quotes. They’re scheduled with the same spacing as your review deck.
      </p>

      <div className="flex items-center gap-2.5 mb-5">
        <button onClick={() => openEditor(null)}
          className="inline-flex items-center gap-1.5 rounded-full px-4 py-2.5 text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
          style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}>
          <Plus size={15} /> New card
        </button>
        {stats.due > 0 && (
          <button onClick={startReview}
            className="inline-flex items-center gap-1.5 rounded-full px-4 py-2.5 text-[13.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
            style={{ borderColor: ACCENT, color: ACCENT }}>
            Review {stats.due} due
          </button>
        )}
      </div>

      {cards.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          No cards yet. Tap <b>New card</b> to write your first one.
        </p>
      ) : (
        <div className="space-y-1.5">
          {cards.map(c => (
            <div key={c.id} className="flex items-center gap-2 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 pr-2">
              <span className="flex-1 min-w-0 px-3.5 py-2.5">
                <span className="block text-[13.5px] font-semibold truncate" style={{ color: INK }}>{c.front}</span>
                <span className="block text-[11.5px] truncate" style={{ color: '#7a7068' }}>{dueLabel(c.dueTs, now, c.lastTs)}</span>
              </span>
              <button onClick={() => openEditor(c)} aria-label="Edit card" className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border-2" style={{ borderColor: '#d0cdc8', color: '#7a7068' }}>
                <Pencil size={13} />
              </button>
              <button onClick={() => remove(c.id)} aria-label="Delete card" className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border-2" style={{ borderColor: '#d0cdc8', color: '#9e9186' }}>
                <Trash2 size={13} />
              </button>
            </div>
          ))}
        </div>
      )}

      {cards.length > 0 && stats.due === 0 && (
        <p className="flex items-center gap-1.5 mt-5 text-[12.5px]" style={{ color: '#7a7068' }}>
          <RotateCcw size={13} /> No cards due right now — they’ll resurface on schedule.
        </p>
      )}
    </div>
  );
};

export default Flashcards;
