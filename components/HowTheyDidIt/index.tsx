/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How They Did It" — an immersive "colour world" card deck of real people who
 * overcame a specific disadvantage a Leaving Cert student might share. Filter by
 * your own barrier, swipe through bold full-bleed cards, then a fast struggle-led
 * reveal: the hook → their words → the hard part → the moves (tap to flip) →
 * where they are now → one move to steal.
 *
 * Redesigned 2026-06-03: one bold idea per screen, tightened copy, each barrier
 * owns a saturated colour world (Headspace register, not the white-card module
 * system). Shares the swipe / sound / celebration primitives with Career Paths.
 * Portraits are emoji glyphs for now; real PNGs can be dropped in later.
 */

import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, Sparkles, HandHeart, X, BookOpen, RotateCcw, RefreshCw, ChevronDown, ExternalLink } from 'lucide-react';
import { useHowTheyDidIt } from '../../hooks/useHowTheyDidIt';
import { PEOPLE, peopleForBarrier } from '../../howTheyDidItData';
import { BARRIERS, type Barrier, type PersonCard, type PersonMove } from '../../types/howTheyDidIt';
import { WORLDS, type ColorWorld, DeckStack, useDeckSound, Celebration } from '../immersiveDeck';

/** Each barrier owns a colour world. */
const BARRIER_WORLD: Record<Barrier, ColorWorld> = {
  financial: WORLDS.teal,
  dyslexia: WORLDS.terracotta,
  eal: WORLDS.ocean,
  'first-gen': WORLDS.claret,
};

const SERIF = "'Source Serif 4', serif";
const fade = { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 }, transition: { duration: 0.24 } };

const barrierLabel = (b: Barrier) => BARRIERS.find((x) => x.id === b)?.label ?? '';

/** A faint decorative glow blob — "colour as environment", no gradients on the card itself. */
const Glow: React.FC<{ wd: ColorWorld }> = ({ wd }) => (
  <div className="absolute -top-12 -right-10 w-48 h-48 rounded-full pointer-events-none" style={{ backgroundColor: wd.glow, opacity: 0.4, filter: 'blur(10px)' }} />
);

/** Section label on a colour world. */
const Label: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <p className="text-[10px] font-bold uppercase tracking-[0.16em] mb-3" style={{ color: 'rgba(255,255,255,0.7)' }}>{children}</p>
);

/** Primary "next" button styled to pop on a colour world (white pill, coloured text). */
const WorldButton: React.FC<{ label: string; icon?: React.ElementType; onClick: () => void; wd: ColorWorld }> = ({ label, icon: Icon, onClick, wd }) => (
  <button
    onClick={onClick}
    className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-[14px] font-semibold transition-transform active:translate-y-0.5"
    style={{ backgroundColor: '#fff', color: wd.deep, boxShadow: `0 4px 0 0 rgba(0,0,0,0.18)` }}
  >
    {label} {Icon && <Icon size={16} />}
  </button>
);

const GhostBack: React.FC<{ onClick: () => void }> = ({ onClick }) => (
  <button onClick={onClick} className="text-[13px] font-medium" style={{ color: 'rgba(255,255,255,0.7)' }}>Back</button>
);

/** A move tile that flips in 3D to reveal its detail. */
const MoveTile: React.FC<{ move: PersonMove; idx: number; wd: ColorWorld; onFlip: () => void }> = ({ move, idx, wd, onFlip }) => {
  const [flipped, setFlipped] = useState(false);
  return (
    <div style={{ perspective: 1000 }} onClick={() => { setFlipped((f) => !f); onFlip(); }} className="cursor-pointer">
      <MotionDiv
        className="relative w-full"
        style={{ transformStyle: 'preserve-3d', minHeight: 76 }}
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        {/* front */}
        <div className="rounded-2xl p-4 flex items-center gap-3" style={{ backgroundColor: wd.chip, backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}>
          <span className="w-7 h-7 rounded-full flex items-center justify-center shrink-0 text-[13px] font-bold" style={{ backgroundColor: '#fff', color: wd.deep, fontFamily: SERIF }}>{idx + 1}</span>
          <span className="text-[15.5px] font-semibold flex-1" style={{ color: '#fff' }}>{move.title}</span>
          <RefreshCw size={14} style={{ color: 'rgba(255,255,255,0.6)' }} />
        </div>
        {/* back */}
        <div className="absolute inset-0 rounded-2xl p-4 flex items-center" style={{ backgroundColor: '#fff', color: '#1a1a1a', transform: 'rotateY(180deg)', backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}>
          <span className="text-[13.5px] leading-snug">{move.detail}</span>
        </div>
      </MotionDiv>
    </div>
  );
};

/** Expandable "see the sources" disclosure. */
const Sources: React.FC<{ sources: string[] }> = ({ sources }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="mb-4">
      <button onClick={() => setOpen((o) => !o)} className="inline-flex items-center gap-1.5 text-[12px] font-semibold" style={{ color: 'rgba(255,255,255,0.78)' }}>
        Real story · {sources.length} {sources.length === 1 ? 'source' : 'sources'}
        <ChevronDown size={14} style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
      </button>
      {open && (
        <div className="mt-2 space-y-1.5">
          {sources.map((s, i) => (
            <a key={i} href={s} target="_blank" rel="noreferrer" className="flex items-start gap-1.5 text-[11.5px] leading-snug underline" style={{ color: 'rgba(255,255,255,0.82)' }}>
              <ExternalLink size={12} className="mt-0.5 shrink-0" />
              <span className="break-all">{s.replace(/^https?:\/\//, '').split('/')[0]}</span>
            </a>
          ))}
        </div>
      )}
    </div>
  );
};

/** The swipe-card / stack face — a bold colour world with the person's hook. */
const CardFace: React.FC<{ p: PersonCard; saved: boolean }> = ({ p, saved }) => {
  const wd = BARRIER_WORLD[p.barrier];
  return (
    <div
      className="w-full h-full rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden flex flex-col select-none relative"
      style={{ backgroundColor: wd.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: wd.onBg }}
    >
      <Glow wd={wd} />
      <div className="relative flex-1 flex items-center justify-center px-6 pt-9">
        <span className="absolute top-4 left-4 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: wd.onBg }}>{barrierLabel(p.barrier)}</span>
        {saved && <span className="absolute top-4 right-4 w-7 h-7 rounded-full flex items-center justify-center" style={{ backgroundColor: '#fff' }}><BookmarkCheck size={15} style={{ color: wd.bg }} /></span>}
        <div className="w-28 h-28 rounded-full flex items-center justify-center" style={{ backgroundColor: wd.chip }}>
          <span style={{ fontSize: 60, lineHeight: 1 }}>{p.emoji}</span>
        </div>
      </div>
      <div className="relative px-6 pb-6 pt-2">
        <h3 className="text-[25px] leading-tight font-semibold" style={{ fontFamily: SERIF }}>{p.name}</h3>
        <p className="text-[12.5px] mb-2.5" style={{ color: wd.onSoft }}>{p.field}</p>
        <p className="text-[15px] leading-snug font-medium">{p.hook}</p>
      </div>
    </div>
  );
};

type Beat = 'front' | 'struggle' | 'moves' | 'now';
const BEAT_IDX: Record<Beat, number> = { front: 0, struggle: 1, moves: 2, now: 3 };

const HowTheyDidIt: React.FC<{ uid?: string; studentSubjects?: string[] }> = ({ uid }) => {
  const { state, isLoaded, markSeen, toggleSaved } = useHowTheyDidIt(uid);
  const sound = useDeckSound();
  const [filter, setFilter] = useState<Barrier | 'all'>('all');
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('front');
  const [showSaved, setShowSaved] = useState(false);
  const [index, setIndex] = useState(0);
  const [burst, setBurst] = useState(false);
  useEffect(() => { setIndex(0); }, [filter]);

  const deck = useMemo(() => (filter === 'all' ? PEOPLE : peopleForBarrier(filter)), [filter]);
  const card = cardId ? PEOPLE.find((p) => p.id === cardId) ?? null : null;
  const savedCards = useMemo(() => PEOPLE.filter((p) => state.savedIds.includes(p.id)), [state.savedIds]);

  const open = (p: PersonCard) => { setCardId(p.id); setBeat('front'); markSeen(p.id); sound.play('tap'); };

  const advance = (p: PersonCard, dir: 'left' | 'right') => {
    if (dir === 'right') {
      if (!state.savedIds.includes(p.id)) toggleSaved(p.id);
      sound.play('save');
    } else sound.play('skip');
    setIndex((i) => {
      const ni = i + 1;
      if (ni >= deck.length) sound.play('complete');
      return ni;
    });
  };

  const goBeat = (b: Beat) => { setBeat(b); sound.play('tap'); };

  const saveFromDetail = (id: string) => {
    const wasSaved = state.savedIds.includes(id);
    toggleSaved(id);
    if (!wasSaved) { setBurst(true); sound.play('save'); window.setTimeout(() => setBurst(false), 950); }
  };

  const nextUnseen = (): PersonCard | null =>
    deck.find((p) => p.id !== card?.id && !state.seenIds.includes(p.id)) ?? deck.find((p) => p.id !== card?.id) ?? null;

  if (!isLoaded) return <div className="w-full max-w-xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;

  // ── CARD DETAIL (immersive colour world) ──────────────────────
  if (card) {
    const wd = BARRIER_WORLD[card.barrier];
    const isSaved = state.savedIds.includes(card.id);
    const bi = BEAT_IDX[beat];
    return (
      <div className="w-full max-w-xl mx-auto pb-10">
        <button onClick={() => { setCardId(null); }} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4">
          <ArrowLeft size={15} /> The deck
        </button>

        <div className="relative rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden" style={{ backgroundColor: wd.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: wd.onBg }}>
          <Glow wd={wd} />
          {burst && <Celebration colors={['#ffffff', wd.glow]} />}
          <div className="relative p-6 md:p-7">
            {/* header: chip + progress dots */}
            <div className="flex items-center justify-between mb-5">
              <span className="text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: wd.onBg }}>{barrierLabel(card.barrier)}</span>
              <div className="flex items-center gap-1.5">
                {[0, 1, 2, 3].map((s) => (
                  <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === bi ? 18 : 6, backgroundColor: s <= bi ? '#fff' : 'rgba(255,255,255,0.35)' }} />
                ))}
              </div>
            </div>

            <AnimatePresence mode="wait">
              <MotionDiv key={beat} {...fade}>
                {beat === 'front' && (
                  <>
                    <div className="flex items-center gap-3.5 mb-5">
                      <div className="w-16 h-16 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.chip }}>
                        <span style={{ fontSize: 34, lineHeight: 1 }}>{card.emoji}</span>
                      </div>
                      <div>
                        <h2 className="text-[22px] font-semibold leading-tight" style={{ fontFamily: SERIF }}>{card.name}</h2>
                        <p className="text-[12.5px]" style={{ color: wd.onSoft }}>{card.field}</p>
                      </div>
                    </div>
                    {card.quote ? (
                      <>
                        <p className="text-[27px] leading-tight font-semibold mb-4" style={{ fontFamily: SERIF }}>“{card.quote}”</p>
                        <p className="text-[15px] leading-snug mb-7" style={{ color: wd.onSoft }}>{card.hook}</p>
                      </>
                    ) : (
                      <p className="text-[25px] leading-tight font-semibold mb-7" style={{ fontFamily: SERIF }}>{card.hook}</p>
                    )}
                    <div className="flex justify-end"><WorldButton label="See how" icon={ArrowRight} onClick={() => goBeat('struggle')} wd={wd} /></div>
                  </>
                )}

                {beat === 'struggle' && (
                  <>
                    <Label>The hard part</Label>
                    <div className="space-y-3.5 mb-7">
                      {card.struggle.map((s, i) => (
                        <MotionDiv key={i} className="flex items-start gap-3" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.08 + i * 0.12 }}>
                          <span className="mt-2 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: '#fff' }} />
                          <p className="text-[17px] leading-snug">{s}</p>
                        </MotionDiv>
                      ))}
                    </div>
                    <div className="flex justify-between items-center">
                      <GhostBack onClick={() => goBeat('front')} />
                      <WorldButton label="What they did" icon={ArrowRight} onClick={() => goBeat('moves')} wd={wd} />
                    </div>
                  </>
                )}

                {beat === 'moves' && (
                  <>
                    <Label>What they did · tap a card</Label>
                    <div className="space-y-2.5 mb-5">
                      {card.moves.map((m, i) => <MoveTile key={i} move={m} idx={i} wd={wd} onFlip={() => sound.play('tap')} />)}
                    </div>
                    {card.helpedBy && (
                      <div className="rounded-2xl p-4 mb-6" style={{ backgroundColor: wd.chip }}>
                        <div className="flex items-center gap-1.5 mb-1.5"><HandHeart size={14} style={{ color: '#fff' }} /><p className="text-[10px] font-bold uppercase tracking-[0.12em]" style={{ color: 'rgba(255,255,255,0.8)' }}>Who helped</p></div>
                        <p className="text-[13.5px] leading-relaxed">{card.helpedBy}</p>
                      </div>
                    )}
                    <div className="flex justify-between items-center">
                      <GhostBack onClick={() => goBeat('struggle')} />
                      <WorldButton label="Where they are now" icon={ArrowRight} onClick={() => goBeat('now')} wd={wd} />
                    </div>
                  </>
                )}

                {beat === 'now' && (
                  <>
                    <Label>Where they are now</Label>
                    <p className="text-[18px] leading-snug font-medium mb-3">{card.now}</p>
                    {card.strengthsLine && <p className="text-[13.5px] leading-relaxed italic mb-5" style={{ color: wd.onSoft }}>{card.strengthsLine}</p>}

                    <div className="rounded-2xl p-4 mb-4" style={{ backgroundColor: '#fff', color: '#1a1a1a' }}>
                      <div className="flex items-center gap-1.5 mb-1.5"><Sparkles size={15} style={{ color: wd.bg }} /><p className="text-[11px] font-bold uppercase tracking-[0.1em]" style={{ color: wd.deep }}>Steal this move</p></div>
                      <p className="text-[14.5px] leading-relaxed mb-3">{card.stealThisMove}</p>
                      <button
                        onClick={() => saveFromDetail(card.id)}
                        className="inline-flex items-center gap-1.5 text-[13px] font-semibold px-3.5 py-2 rounded-full transition-transform active:translate-y-0.5"
                        style={isSaved ? { backgroundColor: wd.bg, color: '#fff' } : { border: `2px solid ${wd.bg}`, color: wd.deep }}
                      >
                        {isSaved ? <><BookmarkCheck size={15} /> Saved to your playbook</> : <><Bookmark size={15} /> Save this move</>}
                      </button>
                    </div>

                    {card.sources.length > 0 && <Sources sources={card.sources} />}

                    <div className="flex flex-col sm:flex-row gap-2.5">
                      {nextUnseen() && <WorldButton label="Next person" icon={ArrowRight} onClick={() => { const n = nextUnseen(); if (n) open(n); }} wd={wd} />}
                      <button onClick={() => setCardId(null)} className="px-5 py-3 rounded-full text-[14px] font-semibold" style={{ border: '2px solid rgba(255,255,255,0.5)', color: '#fff' }}>Back to deck</button>
                    </div>
                  </>
                )}
              </MotionDiv>
            </AnimatePresence>
          </div>
        </div>
      </div>
    );
  }

  // ── SAVED VIEW ("your playbook") ──────────────────────────────
  if (showSaved) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setShowSaved(false)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> The deck</button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: SERIF, color: '#1a1a1a' }}>Your playbook</h2>
        <p className="text-[13px] text-zinc-500 mb-4">The moves you saved — your own list of things to try.</p>
        {savedCards.length === 0 ? (
          <p className="text-[14px] text-zinc-500">Nothing saved yet — open a card and tap “Save this move”.</p>
        ) : (
          <div className="space-y-3">
            {savedCards.map((p) => {
              const wd = BARRIER_WORLD[p.barrier];
              return (
                <div key={p.id} className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] p-4">
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <span className="w-8 h-8 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.bg }}><span style={{ fontSize: 17 }}>{p.emoji}</span></span>
                    <p className="text-[14px] font-semibold text-zinc-900 dark:text-white">{p.name}</p>
                  </div>
                  <p className="text-[13.5px] leading-relaxed text-zinc-700 dark:text-zinc-300">{p.stealThisMove}</p>
                  <button onClick={() => open(p)} className="text-[12px] font-semibold mt-1.5" style={{ color: wd.deep }}>Open card →</button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  }

  // ── DECK (browse) ─────────────────────────────────────────────
  const top = deck[index];
  const topWorld = top ? BARRIER_WORLD[top.barrier] : WORLDS.teal;
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[13px] font-medium mb-2.5 text-zinc-600 dark:text-zinc-300">Pick what’s closest to your situation:</p>

      {/* barrier filter */}
      <div className="flex flex-wrap gap-1.5 mb-6">
        <button onClick={() => setFilter('all')} className="rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold transition-colors" style={filter === 'all' ? { backgroundColor: '#1a1a1a', color: '#fff' } : { backgroundColor: '#F1F0ED', color: '#3a3530' }}>Everyone</button>
        {BARRIERS.map((b) => {
          const wd = BARRIER_WORLD[b.id];
          const active = filter === b.id;
          return (
            <button key={b.id} onClick={() => setFilter(b.id)} className="rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold transition-colors inline-flex items-center gap-1.5" style={active ? { backgroundColor: wd.bg, color: '#fff' } : { backgroundColor: '#F1F0ED', color: '#3a3530' }}>
              <span>{b.emoji}</span> {b.label}
            </button>
          );
        })}
      </div>

      {index < deck.length ? (
        <>
          <DeckStack items={deck} index={index} onAdvance={advance} onOpen={open} renderFace={(p) => <CardFace p={p} saved={state.savedIds.includes(p.id)} />} />

          {/* controls (non-swipers + accessibility) */}
          <div className="flex items-center justify-center gap-3 mt-6">
            <button onClick={() => top && advance(top, 'left')} aria-label="Skip" className="w-12 h-12 rounded-full border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105"><X size={20} className="text-zinc-400" /></button>
            <button onClick={() => top && open(top)} className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-[14px] font-semibold text-white transition-transform active:translate-y-0.5" style={{ backgroundColor: topWorld.bg, boxShadow: `0 4px 0 0 ${topWorld.deep}` }}><BookOpen size={16} /> Read their story</button>
            <button onClick={() => top && advance(top, 'right')} aria-label="Save" className="w-12 h-12 rounded-full border-2 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105" style={{ borderColor: topWorld.bg }}><Bookmark size={20} style={{ color: topWorld.bg }} /></button>
          </div>
          <p className="text-center text-[12px] mt-3 text-zinc-400">Swipe the card, or use the buttons · {deck.length - index} to go</p>
        </>
      ) : (
        <div className="relative rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden text-center" style={{ backgroundColor: WORLDS.teal.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: '#fff' }}>
          <Glow wd={WORLDS.teal} />
          <Celebration colors={['#ffffff', WORLDS.teal.glow]} />
          <div className="relative p-8">
            <p className="text-[15px] mb-1" style={{ color: 'rgba(255,255,255,0.85)' }}>That’s everyone in this group.</p>
            <p className="text-[22px] font-semibold mb-5" style={{ fontFamily: SERIF }}>You’ve saved {state.savedIds.length} {state.savedIds.length === 1 ? 'move' : 'moves'} 💪</p>
            <div className="flex flex-col sm:flex-row gap-2.5 justify-center">
              <WorldButton label="Start over" icon={RotateCcw} onClick={() => setIndex(0)} wd={WORLDS.teal} />
              {state.savedIds.length > 0 && <button onClick={() => setShowSaved(true)} className="px-5 py-3 rounded-full text-[14px] font-semibold" style={{ border: '2px solid rgba(255,255,255,0.5)', color: '#fff' }}>See your playbook</button>}
            </div>
          </div>
        </div>
      )}

      {state.savedIds.length > 0 && index < deck.length && (
        <button onClick={() => setShowSaved(true)} className="w-full mt-6 flex items-center justify-center gap-2 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 py-3 text-[13px] font-semibold text-zinc-700 dark:text-zinc-300">
          <BookmarkCheck size={15} /> Your playbook ({state.savedIds.length})
        </button>
      )}
    </div>
  );
};

export default HowTheyDidIt;
