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

import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence, motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, Users, Sparkles, Hand, X, BookOpen, RotateCcw } from 'lucide-react';
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

/** Large portrait for the Tinder-style card — tries the PNG, falls back to a big monogram. */
const BigPortrait: React.FC<{ person: PersonCard }> = ({ person }) => {
  const [failed, setFailed] = useState(false);
  if (failed) return <span className="font-semibold" style={{ color: GOLD_DARK, fontSize: 96, fontFamily: "'Source Serif 4', serif" }}>{initials(person.name)}</span>;
  return <img src={`/assets/people/${person.portraitKey}.png`} alt="" onError={() => setFailed(true)} className="max-h-[80%] max-w-[80%] object-contain" draggable={false} />;
};

/** The card face — a tall "profile card" (illustration on a tint + name/field/obstacle). */
const CardFace: React.FC<{ person: PersonCard; saved: boolean }> = ({ person, saved }) => (
  <div className="w-full h-full rounded-3xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[5px_7px_0_0_#1A1A1A] dark:shadow-[5px_7px_0_0_#3f3f46] overflow-hidden flex flex-col select-none">
    <div className="relative flex-1 flex items-center justify-center" style={{ backgroundColor: GOLD_TINT }}>
      <span className="absolute top-3 left-3 text-[10px] font-bold uppercase tracking-[0.1em] px-2 py-0.5 rounded-full bg-white" style={{ color: GOLD_DARK }}>{barrierLabel(person.barrier)}</span>
      {saved && <span className="absolute top-3 right-3 w-7 h-7 rounded-full bg-white flex items-center justify-center"><BookmarkCheck size={15} style={{ color: GOLD }} /></span>}
      <BigPortrait person={person} />
    </div>
    <div className="px-5 py-4 shrink-0">
      <h3 className="text-xl font-semibold text-zinc-900 dark:text-white leading-tight" style={{ fontFamily: "'Source Serif 4', serif" }}>{person.name}</h3>
      <p className="text-[12px] text-zinc-500 mb-1.5">{person.field}</p>
      <p className="text-[13.5px] leading-snug line-clamp-3" style={{ color: '#3a3530' }}>{person.start}</p>
    </div>
  </div>
);

/** Draggable top card — fling left/right to advance (right = save). */
const SwipeCard: React.FC<{ person: PersonCard; saved: boolean; onDismiss: (dir: 'left' | 'right') => void }> = ({ person, saved, onDismiss }) => {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-220, 220], [-13, 13]);
  const saveOp = useTransform(x, [30, 120], [0, 1]);
  const skipOp = useTransform(x, [-120, -30], [1, 0]);
  return (
    <motion.div
      className="absolute inset-0 cursor-grab active:cursor-grabbing"
      style={{ x, rotate, zIndex: 30 }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.7}
      onDragEnd={(_e, info) => {
        if (info.offset.x > 110 || info.velocity.x > 600) animate(x, 720, { duration: 0.3, onComplete: () => onDismiss('right') });
        else if (info.offset.x < -110 || info.velocity.x < -600) animate(x, -720, { duration: 0.3, onComplete: () => onDismiss('left') });
        else animate(x, 0, { type: 'spring', stiffness: 320, damping: 30 });
      }}
    >
      <motion.div className="absolute top-7 left-5 z-10 px-2.5 py-1 rounded-lg border-2 text-[15px] font-extrabold tracking-wide" style={{ opacity: saveOp, color: GOLD, borderColor: GOLD, transform: 'rotate(-12deg)' }}>SAVE</motion.div>
      <motion.div className="absolute top-7 right-5 z-10 px-2.5 py-1 rounded-lg border-2 text-[15px] font-extrabold tracking-wide text-zinc-400 border-zinc-300" style={{ opacity: skipOp, transform: 'rotate(12deg)' }}>SKIP</motion.div>
      <CardFace person={person} saved={saved} />
    </motion.div>
  );
};

type Beat = 'front' | 'middle' | 'moves' | 'now';

const HowTheyDidIt: React.FC<{ uid?: string; studentSubjects?: string[] }> = ({ uid }) => {
  const { state, isLoaded, markSeen, toggleSaved } = useHowTheyDidIt(uid);
  const [filter, setFilter] = useState<Barrier | 'all'>('all');
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('front');
  const [showSaved, setShowSaved] = useState(false);
  const [index, setIndex] = useState(0); // top card in the swipe stack
  useEffect(() => { setIndex(0); }, [filter]);

  const deck = useMemo(() => (filter === 'all' ? PEOPLE : peopleForBarrier(filter)), [filter]);
  const card = cardId ? PEOPLE.find(p => p.id === cardId) ?? null : null;
  const savedCards = useMemo(() => PEOPLE.filter(p => state.savedIds.includes(p.id)), [state.savedIds]);

  const open = (p: PersonCard) => { setCardId(p.id); setBeat('front'); markSeen(p.id); };
  // Swipe stack: right = save the person, left = skip; both advance to the next.
  const advance = (dir: 'left' | 'right') => {
    const p = deck[index];
    if (dir === 'right' && p && !state.savedIds.includes(p.id)) toggleSaved(p.id);
    setIndex(i => i + 1);
  };
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
      <p className="text-[13px] font-medium mb-2.5" style={{ color: GOLD_DARK }}>Pick what’s closest to your situation:</p>

      {/* barrier filter */}
      <div className="flex flex-wrap gap-1.5 mb-5">
        <button onClick={() => setFilter('all')} className="rounded-full px-3 py-1.5 text-[12.5px] font-medium transition-colors" style={filter === 'all' ? { backgroundColor: GOLD, color: '#fff' } : { backgroundColor: '#F6F6F4', color: '#2a2622' }}>Everyone</button>
        {BARRIERS.map(b => (
          <button key={b.id} onClick={() => setFilter(b.id)} className="rounded-full px-3 py-1.5 text-[12.5px] font-medium transition-colors" style={filter === b.id ? { backgroundColor: GOLD, color: '#fff' } : { backgroundColor: '#F6F6F4', color: '#2a2622' }}>{b.label}</button>
        ))}
      </div>

      {index < deck.length ? (
        <>
          {/* Tinder-style swipe stack */}
          <div className="relative mx-auto" style={{ maxWidth: 330, height: 430 }}>
            {[2, 1, 0].map(off => {
              const p = deck[index + off];
              if (!p) return null;
              if (off === 0) return <SwipeCard key={p.id} person={p} saved={state.savedIds.includes(p.id)} onDismiss={advance} />;
              return (
                <div key={p.id} className="absolute inset-0" style={{ transform: `translateY(${off * 10}px) scale(${1 - off * 0.045})`, zIndex: 10 - off }}>
                  <CardFace person={p} saved={state.savedIds.includes(p.id)} />
                </div>
              );
            })}
          </div>
          {/* controls (for non-swipers + accessibility) */}
          <div className="flex items-center justify-center gap-3 mt-5">
            <button onClick={() => advance('left')} aria-label="Skip" className="w-12 h-12 rounded-full border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105"><X size={20} className="text-zinc-400" /></button>
            <PrimaryActionButton label="Read their story" icon={BookOpen} onClick={() => open(deck[index])} />
            <button onClick={() => advance('right')} aria-label="Save" className="w-12 h-12 rounded-full border-2 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105" style={{ borderColor: GOLD }}><Bookmark size={20} style={{ color: GOLD }} /></button>
          </div>
          <p className="text-center text-[12px] mt-3" style={{ color: '#9e9186' }}>Swipe the card, or use the buttons · {deck.length - index} to go</p>
        </>
      ) : (
        <div className={`${cardShell} text-center`}>
          <p className="text-[15px] mb-4" style={{ color: '#5a5550' }}>That’s everyone in this group. Start over, or pick another group above.</p>
          <PrimaryActionButton label="Start over" icon={RotateCcw} onClick={() => setIndex(0)} />
        </div>
      )}

      {state.savedIds.length > 0 && (
        <button onClick={() => setShowSaved(true)} className="w-full mt-5 flex items-center justify-center gap-2 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 py-3 text-[13px] font-semibold" style={{ color: GOLD_DARK }}>
          <BookmarkCheck size={15} /> Moves you’ve saved ({state.savedIds.length})
        </button>
      )}
    </div>
  );
};

export default HowTheyDidIt;
