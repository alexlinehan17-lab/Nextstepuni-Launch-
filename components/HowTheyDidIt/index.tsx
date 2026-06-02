/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How They Did It" — a card deck of real people who overcame a specific
 * disadvantage a Leaving Cert student might share. Filter by your own barrier,
 * then a struggle-first reveal: the obstacle → the hard middle → what they
 * actually did (+ the outside help) → where they are now → one move you can steal.
 *
 * Aesthetic: the app's chunky cardShell + a gold "spotlight" accent. Portraits
 * are placeholders (initials) until real PNGs land at /assets/people/{key}.png —
 * the <Portrait> falls back automatically, so dropping the images in just works.
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, Users, Sparkles, Hand } from 'lucide-react';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useHowTheyDidIt } from '../../hooks/useHowTheyDidIt';
import { PEOPLE, peopleForBarrier } from '../../howTheyDidItData';
import { BARRIERS, type Barrier, type PersonCard } from '../../types/howTheyDidIt';

const GOLD = '#C8862B';
const GOLD_DARK = '#7c5414';
const GOLD_TINT = '#FBF3E2';

const cardShell =
  'w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7';
const fade = { initial: { opacity: 0, y: 10 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.22 } };

const initials = (name: string) => name.split(' ').filter(w => /[A-Za-z]/.test(w[0])).slice(0, 2).map(w => w[0]).join('').toUpperCase();

/** Portrait: tries the real PNG, falls back to initials so PNGs are drop-in. */
const Portrait: React.FC<{ person: PersonCard; size: number }> = ({ person, size }) => {
  const [failed, setFailed] = useState(false);
  return (
    <div className="rounded-full flex items-center justify-center shrink-0 overflow-hidden" style={{ width: size, height: size, backgroundColor: GOLD_TINT }}>
      {!failed ? (
        <img src={`/assets/people/${person.portraitKey}.png`} alt="" onError={() => setFailed(true)} className="w-full h-full object-cover" draggable={false} />
      ) : (
        <span className="font-semibold" style={{ color: GOLD_DARK, fontSize: size * 0.36, fontFamily: "'Source Serif 4', serif" }}>{initials(person.name)}</span>
      )}
    </div>
  );
};

const barrierLabel = (b: Barrier) => BARRIERS.find(x => x.id === b)?.label ?? '';

type Beat = 'front' | 'middle' | 'moves' | 'now';

const HowTheyDidIt: React.FC<{ uid?: string; studentSubjects?: string[] }> = ({ uid }) => {
  const { state, isLoaded, markSeen, toggleSaved } = useHowTheyDidIt(uid);
  const [filter, setFilter] = useState<Barrier | 'all'>('all');
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('front');
  const [showSaved, setShowSaved] = useState(false);

  const deck = useMemo(() => (filter === 'all' ? PEOPLE : peopleForBarrier(filter)), [filter]);
  const card = cardId ? PEOPLE.find(p => p.id === cardId) ?? null : null;
  const savedCards = useMemo(() => PEOPLE.filter(p => state.savedIds.includes(p.id)), [state.savedIds]);

  const open = (p: PersonCard) => { setCardId(p.id); setBeat('front'); markSeen(p.id); };
  const nextCard = (): PersonCard | null => deck.find(p => p.id !== card?.id && !state.seenIds.includes(p.id)) ?? deck.find(p => p.id !== card?.id) ?? null;

  if (!isLoaded) return <div className="w-full max-w-xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;

  // ── CARD DETAIL ────────────────────────────────────────────────
  if (card) {
    const beatIdx = beat === 'front' ? 0 : beat === 'middle' ? 1 : beat === 'moves' ? 2 : 3;
    const isSaved = state.savedIds.includes(card.id);
    return (
      <div className="w-full">
        <button onClick={() => setCardId(null)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4 max-w-xl mx-auto w-full">
          <ArrowLeft size={15} /> The deck
        </button>
        <AnimatePresence mode="wait">
          <MotionDiv key={beat} {...fade} className={cardShell}>
            <div className="flex items-center justify-between mb-4">
              <span className="text-[10px] font-bold uppercase tracking-[0.12em] px-2 py-0.5 rounded-full" style={{ backgroundColor: GOLD_TINT, color: GOLD_DARK }}>{barrierLabel(card.barrier)}</span>
              <div className="flex items-center gap-1.5">
                {[0, 1, 2, 3].map(s => <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === beatIdx ? 18 : 6, backgroundColor: s <= beatIdx ? GOLD : '#E2E0DC' }} />)}
              </div>
            </div>

            {beat === 'front' && (
              <>
                <div className="flex items-center gap-3.5 mb-4">
                  <Portrait person={card} size={64} />
                  <div>
                    <h2 className="text-xl font-semibold text-zinc-900 dark:text-white" style={{ fontFamily: "'Source Serif 4', serif" }}>{card.name}</h2>
                    <p className="text-[12px] text-zinc-500">{card.field}</p>
                  </div>
                </div>
                <p className="text-[17px] leading-relaxed mb-6" style={{ color: '#1a1a1a', fontFamily: "'Source Serif 4', serif" }}>{card.start}</p>
                <div className="flex justify-end"><PrimaryActionButton label="How did they do it?" icon={ArrowRight} onClick={() => setBeat('middle')} /></div>
              </>
            )}

            {beat === 'middle' && (
              <>
                <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: GOLD_DARK }}>The hard part</p>
                <p className="text-[15px] leading-relaxed mb-6" style={{ color: '#2a2622' }}>{card.hardMiddle}</p>
                <div className="flex justify-between items-center">
                  <button onClick={() => setBeat('front')} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
                  <PrimaryActionButton label="What they did" icon={ArrowRight} onClick={() => setBeat('moves')} />
                </div>
              </>
            )}

            {beat === 'moves' && (
              <>
                <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-2.5" style={{ color: GOLD_DARK }}>What they actually did</p>
                <div className="space-y-2 mb-4">
                  {card.moves.map((m, i) => (
                    <div key={i} className="flex items-start gap-2.5 rounded-xl p-3" style={{ backgroundColor: '#F6F6F4' }}>
                      <span className="w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-[11px] font-bold text-white" style={{ backgroundColor: GOLD }}>{i + 1}</span>
                      <span className="text-[14px] leading-snug" style={{ color: '#2a2622' }}>{m}</span>
                    </div>
                  ))}
                </div>
                <div className="rounded-xl p-3.5 mb-5" style={{ backgroundColor: GOLD_TINT }}>
                  <div className="flex items-center gap-1.5 mb-1"><Hand size={14} style={{ color: GOLD_DARK }} /><p className="text-[10px] font-bold uppercase tracking-[0.1em]" style={{ color: GOLD_DARK }}>What helped from outside</p></div>
                  <p className="text-[13.5px] leading-relaxed" style={{ color: '#3a3530' }}>{card.outsideHelp}</p>
                </div>
                <div className="flex justify-between items-center">
                  <button onClick={() => setBeat('middle')} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
                  <PrimaryActionButton label="Where they are now" icon={ArrowRight} onClick={() => setBeat('now')} />
                </div>
              </>
            )}

            {beat === 'now' && (
              <>
                <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: GOLD_DARK }}>Where they are now</p>
                <p className="text-[15px] leading-relaxed mb-3" style={{ color: '#2a2622' }}>{card.now}</p>
                {card.strengthsLine && <p className="text-[13.5px] leading-relaxed italic mb-4" style={{ color: GOLD_DARK }}>{card.strengthsLine}</p>}

                <div className="rounded-xl p-4 mb-3 border-2" style={{ borderColor: GOLD, backgroundColor: '#fff' }}>
                  <div className="flex items-center gap-1.5 mb-1.5"><Sparkles size={15} style={{ color: GOLD }} /><p className="text-[11px] font-bold uppercase tracking-[0.1em]" style={{ color: GOLD_DARK }}>Steal this move</p></div>
                  <p className="text-[14px] leading-relaxed mb-3" style={{ color: '#1a1a1a' }}>{card.stealThisMove}</p>
                  <button onClick={() => toggleSaved(card.id)} className="inline-flex items-center gap-1.5 text-[13px] font-semibold px-3.5 py-2 rounded-full" style={isSaved ? { backgroundColor: GOLD, color: '#fff' } : { border: `2px solid ${GOLD}`, color: GOLD_DARK }}>
                    {isSaved ? <><BookmarkCheck size={15} /> Saved</> : <><Bookmark size={15} /> Save this move</>}
                  </button>
                </div>

                {card.sources.length > 0 && <p className="text-[10px] mb-4" style={{ color: '#9e9186' }}>Real story · sourced</p>}

                <div className="flex flex-col sm:flex-row gap-2.5">
                  {nextCard() && <PrimaryActionButton label="Next person" icon={ArrowRight} onClick={() => { const n = nextCard(); if (n) open(n); }} />}
                  <button onClick={() => setCardId(null)} className="px-5 py-3 rounded-full text-[14px] font-semibold border-2 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300">Back to deck</button>
                </div>
              </>
            )}
          </MotionDiv>
        </AnimatePresence>
      </div>
    );
  }

  // ── SAVED VIEW ────────────────────────────────────────────────
  if (showSaved) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setShowSaved(false)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> The deck</button>
        <h2 className="text-2xl font-semibold mb-4" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Moves you’ve saved</h2>
        {savedCards.length === 0 ? (
          <p className="text-[14px] text-zinc-500">Nothing saved yet — open a card and tap “Save this move”.</p>
        ) : (
          <div className="space-y-3">
            {savedCards.map(p => (
              <div key={p.id} className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] p-4">
                <div className="flex items-center gap-2.5 mb-1.5"><Portrait person={p} size={32} /><p className="text-[14px] font-semibold text-zinc-900 dark:text-white">{p.name}</p></div>
                <p className="text-[13.5px] leading-relaxed" style={{ color: '#2a2622' }}>{p.stealThisMove}</p>
                <button onClick={() => open(p)} className="text-[12px] font-semibold mt-1.5" style={{ color: GOLD_DARK }}>Open card →</button>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  // ── DECK (browse) ─────────────────────────────────────────────
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[15px] leading-relaxed mb-4" style={{ color: '#5a5550', fontFamily: "'DM Sans', sans-serif" }}>
        Real people who started where you are — and the actual moves they made. Pick what’s closest to your own situation to find someone who gets it.
      </p>

      {/* barrier filter */}
      <div className="flex flex-wrap gap-1.5 mb-5">
        <button onClick={() => setFilter('all')} className="rounded-full px-3 py-1.5 text-[12.5px] font-medium transition-colors" style={filter === 'all' ? { backgroundColor: GOLD, color: '#fff' } : { backgroundColor: '#F6F6F4', color: '#2a2622' }}>Everyone</button>
        {BARRIERS.map(b => (
          <button key={b.id} onClick={() => setFilter(b.id)} className="rounded-full px-3 py-1.5 text-[12.5px] font-medium transition-colors" style={filter === b.id ? { backgroundColor: GOLD, color: '#fff' } : { backgroundColor: '#F6F6F4', color: '#2a2622' }}>{b.label}</button>
        ))}
      </div>

      <div className="space-y-3">
        {deck.map(p => (
          <button key={p.id} onClick={() => open(p)} className="w-full text-left rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] p-4 flex items-center gap-3.5 transition-transform hover:-translate-y-0.5">
            <Portrait person={p} size={52} />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <p className="text-[15px] font-semibold text-zinc-900 dark:text-white" style={{ fontFamily: "'Source Serif 4', serif" }}>{p.name}</p>
                {state.savedIds.includes(p.id) && <BookmarkCheck size={13} style={{ color: GOLD }} />}
              </div>
              <p className="text-[12.5px] leading-snug text-zinc-500 line-clamp-2">{p.start}</p>
            </div>
            <ArrowRight size={18} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
          </button>
        ))}
      </div>

      {state.savedIds.length > 0 && (
        <button onClick={() => setShowSaved(true)} className="w-full mt-5 flex items-center justify-center gap-2 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 py-3 text-[13px] font-semibold" style={{ color: GOLD_DARK }}>
          <BookmarkCheck size={15} /> Moves you’ve saved ({state.savedIds.length})
        </button>
      )}
    </div>
  );
};

export default HowTheyDidIt;
