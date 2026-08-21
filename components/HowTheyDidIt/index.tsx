/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "How They Did It" — a card deck of real people who overcame a specific
 * disadvantage a Leaving Cert student might share. Filter by your own barrier,
 * swipe through the deck, then a fast struggle-led reveal: the hook → their words
 * → the hard part → the moves (tap to flip) → where they are now → one move to
 * steal.
 *
 * 2026-06-03 hybrid aesthetic: light white cards with a brightened colour HEADER
 * BAND, a serif INITIALS avatar per person, Source Serif titles and orange chunky
 * CTAs — same family as the rest of the app. Each barrier still owns a saturated
 * colour (BARRIER_WORLD) but it now feeds the Band/headers/accents, not a
 * full-bleed dark surface. Uses the shared immersiveDeck/HybridCard primitives so
 * all three decks stay identical. Shares the swipe / sound / celebration engine
 * with Career Paths.
 */

import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowRight, Bookmark, BookmarkCheck, Sparkles, HandHeart, X, BookOpen, RotateCcw, RefreshCw, ChevronDown, ExternalLink } from 'lucide-react';
import { useHowTheyDidIt } from '../../hooks/useHowTheyDidIt';
import { PEOPLE, peopleForBarrier } from '../../howTheyDidItData';
import { BARRIERS, type Barrier, type PersonCard, type PersonMove } from '../../types/howTheyDidIt';
import {
  WORLDS, type ColorWorld, DeckStack, useDeckSound, Celebration, initials,
  HybridCard, Band, BlobIcon, ProgressDots, OrangeBtn, NeutralBtn, Eyebrow, BackLink,
  SERIF, INK, BODY, MUTED, LABEL, HAIRLINE,
  usePaperInk,
} from '../immersiveDeck';

/** Each barrier owns a colour world (now feeds the Band / headers / accents). */
const BARRIER_WORLD: Record<Barrier, ColorWorld> = {
  financial: WORLDS.teal,
  dyslexia: WORLDS.terracotta,
  eal: WORLDS.ocean,
  'first-gen': WORLDS.claret,
};

const fade = { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 }, transition: { duration: 0.24 } };

const barrierLabel = (b: Barrier) => BARRIERS.find((x) => x.id === b)?.label ?? '';

/** A move tile that flips in 3D to reveal its detail. */
const MoveTile: React.FC<{ move: PersonMove; idx: number; wd: ColorWorld; onFlip: () => void }> = ({ move, idx, wd, onFlip }) => {
  /* `wd.deep` is tuned for white paper and is unreadable on the dark deck
     paper; paperTone() flips to the world's light tone in dark mode. */
  const paperTone = usePaperInk();
  const [flipped, setFlipped] = useState(false);
  return (
    <div style={{ perspective: 1000 }} onClick={() => { setFlipped((f) => !f); onFlip(); }} className="cursor-pointer">
      <MotionDiv
        className="relative w-full"
        style={{ transformStyle: 'preserve-3d', minHeight: 76 }}
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        {/* front — tinted panel, ink text, coloured number badge */}
        <div className="rounded-2xl p-4 flex items-center gap-3" style={{ backgroundColor: wd.tint, backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}>
          <span className="w-7 h-7 rounded-full flex items-center justify-center shrink-0 text-[13px] font-bold" style={{ backgroundColor: wd.bg, color: '#fff', fontFamily: SERIF }}>{idx + 1}</span>
          <span className="text-[15.5px] font-semibold flex-1" style={{ color: INK }}>{move.title}</span>
          <RefreshCw size={14} style={{ color: paperTone(wd) }} />
        </div>
        {/* back — white, ink detail */}
        <div className="absolute inset-0 rounded-2xl p-4 flex items-center" style={{ backgroundColor: 'var(--deck-paper)', border: `1.5px solid ${HAIRLINE}`, color: INK, transform: 'rotateY(180deg)', backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}>
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
      <button onClick={() => setOpen((o) => !o)} className="inline-flex items-center gap-1.5 text-[12px] font-semibold" style={{ color: MUTED }}>
        Real story · {sources.length} {sources.length === 1 ? 'source' : 'sources'}
        <ChevronDown size={14} style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
      </button>
      {open && (
        <div className="mt-2 space-y-1.5">
          {sources.map((s, i) => (
            <a key={i} href={s} target="_blank" rel="noreferrer" className="flex items-start gap-1.5 text-[11.5px] leading-snug underline" style={{ color: MUTED }}>
              <ExternalLink size={12} className="mt-0.5 shrink-0" />
              <span className="break-all">{s.replace(/^https?:\/\//, '').split('/')[0]}</span>
            </a>
          ))}
        </div>
      )}
    </div>
  );
};

/** The swipe-card / stack face — a white card with a colour top zone + serif initials avatar. */
const CardFace: React.FC<{ p: PersonCard; saved: boolean }> = ({ p, saved }) => {
  const wd = BARRIER_WORLD[p.barrier];
  return (
    <div
      className="w-full h-full rounded-[28px] overflow-hidden flex flex-col select-none"
      style={{ backgroundColor: 'var(--deck-paper)', border: `2px solid ${INK}`, boxShadow: 'var(--deck-shadow)' }}
    >
      {/* white hero zone — initials blob + barrier chip + saved chip */}
      <div className="relative flex-1 flex items-center justify-center pt-8">
        <span className="absolute top-4 left-4 text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.tint, color: wd.deep }}>{barrierLabel(p.barrier)}</span>
        {saved && <span className="absolute top-4 right-4 w-7 h-7 rounded-full flex items-center justify-center" style={{ backgroundColor: wd.tint }}><BookmarkCheck size={15} style={{ color: wd.deep }} /></span>}
        <BlobIcon wd={wd} initials={initials(p.name)} image={p.portraitKey ? `/portraits/${p.portraitKey}.png` : undefined} size={108} seed={p.name} />
      </div>
      {/* white bottom zone — name, field, hook */}
      <div className="relative px-6 pt-2 pb-6 flex flex-col">
        <h3 className="text-[25px] leading-tight font-semibold" style={{ fontFamily: SERIF, color: INK }}>{p.name}</h3>
        <p className="text-[12.5px] mb-2.5" style={{ color: MUTED }}>{p.field}</p>
        <p className="text-[15px] leading-snug font-medium" style={{ color: BODY }}>{p.hook}</p>
      </div>
    </div>
  );
};

type Beat = 'front' | 'struggle' | 'moves' | 'now';
const BEAT_IDX: Record<Beat, number> = { front: 0, struggle: 1, moves: 2, now: 3 };

const HowTheyDidIt: React.FC<{ uid?: string; studentSubjects?: string[] }> = ({ uid }) => {
  /* `wd.deep` is tuned for white paper and is unreadable on the dark deck
     paper; paperTone() flips to the world's light tone in dark mode. */
  const paperTone = usePaperInk();
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

  // ── CARD DETAIL (white card + colour band) ─────────────────────
  if (card) {
    const wd = BARRIER_WORLD[card.barrier];
    const isSaved = state.savedIds.includes(card.id);
    const bi = BEAT_IDX[beat];
    return (
      <div className="immersive-deck-theme w-full max-w-xl mx-auto pb-10">
        <BackLink onClick={() => { setCardId(null); }} label="The deck" />
        <HybridCard>
          {burst && <Celebration colors={[wd.bg, wd.glow]} />}
          <Band
            wd={wd}
            initials={initials(card.name)}
            image={card.portraitKey ? `/portraits/${card.portraitKey}.png` : undefined}
            eyebrow={barrierLabel(card.barrier)}
            title={card.name}
            right={<ProgressDots total={4} active={bi} />}
          />
          <div className="p-6 md:p-7">
            <AnimatePresence mode="wait">
              <MotionDiv key={beat} {...fade}>
                {beat === 'front' && (
                  <>
                    <p className="text-[12.5px] mb-4" style={{ color: MUTED }}>{card.field}</p>
                    {card.quote ? (
                      <>
                        <p className="text-[27px] leading-tight font-semibold mb-4" style={{ fontFamily: SERIF, color: INK }}>“{card.quote}”</p>
                        <p className="text-[15px] leading-snug mb-7" style={{ color: MUTED }}>{card.hook}</p>
                      </>
                    ) : (
                      <p className="text-[25px] leading-tight font-semibold mb-7" style={{ fontFamily: SERIF, color: INK }}>{card.hook}</p>
                    )}
                    <div className="flex justify-end"><OrangeBtn label="See how" icon={ArrowRight} onClick={() => goBeat('struggle')} /></div>
                  </>
                )}

                {beat === 'struggle' && (
                  <>
                    <Eyebrow>The hard part</Eyebrow>
                    <div className="space-y-3.5 mb-7">
                      {card.struggle.map((s, i) => (
                        <MotionDiv key={i} className="flex items-start gap-3" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.08 + i * 0.12 }}>
                          <span className="mt-2 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: wd.bg }} />
                          <p className="text-[17px] leading-snug" style={{ color: INK }}>{s}</p>
                        </MotionDiv>
                      ))}
                    </div>
                    <div className="flex justify-between items-center">
                      <NeutralBtn label="Back" onClick={() => goBeat('front')} />
                      <OrangeBtn label="What they did" icon={ArrowRight} onClick={() => goBeat('moves')} />
                    </div>
                  </>
                )}

                {beat === 'moves' && (
                  <>
                    <Eyebrow>What they did · tap a card</Eyebrow>
                    <div className="space-y-2.5 mb-5">
                      {card.moves.map((m, i) => <MoveTile key={i} move={m} idx={i} wd={wd} onFlip={() => sound.play('tap')} />)}
                    </div>
                    {card.helpedBy && (
                      <div className="rounded-2xl p-4 mb-6" style={{ backgroundColor: wd.tint }}>
                        <div className="flex items-center gap-1.5 mb-1.5"><HandHeart size={14} style={{ color: paperTone(wd) }} /><p className="text-[10px] font-bold uppercase tracking-[0.12em]" style={{ color: paperTone(wd) }}>Who helped</p></div>
                        <p className="text-[13.5px] leading-relaxed" style={{ color: BODY }}>{card.helpedBy}</p>
                      </div>
                    )}
                    <div className="flex justify-between items-center">
                      <NeutralBtn label="Back" onClick={() => goBeat('struggle')} />
                      <OrangeBtn label="Where they are now" icon={ArrowRight} onClick={() => goBeat('now')} />
                    </div>
                  </>
                )}

                {beat === 'now' && (
                  <>
                    <Eyebrow>Where they are now</Eyebrow>
                    <p className="text-[18px] leading-snug font-medium mb-3" style={{ color: INK }}>{card.now}</p>
                    {card.strengthsLine && <p className="text-[13.5px] leading-relaxed italic mb-5" style={{ color: MUTED }}>{card.strengthsLine}</p>}

                    <div className="rounded-2xl p-4 mb-4" style={{ backgroundColor: 'var(--deck-paper)', border: `1.5px solid ${HAIRLINE}` }}>
                      <div className="flex items-center gap-1.5 mb-1.5"><Sparkles size={15} style={{ color: paperTone(wd) }} /><p className="text-[11px] font-bold uppercase tracking-[0.1em]" style={{ color: paperTone(wd) }}>Steal this move</p></div>
                      <p className="text-[14.5px] leading-relaxed mb-3" style={{ color: BODY }}>{card.stealThisMove}</p>
                      <button
                        onClick={() => saveFromDetail(card.id)}
                        className="inline-flex items-center gap-1.5 text-[13px] font-semibold px-3.5 py-2 rounded-full transition-transform active:translate-y-0.5"
                        style={isSaved ? { backgroundColor: wd.bg, color: '#fff' } : { border: `2px solid ${wd.bg}`, color: paperTone(wd) }}
                      >
                        {isSaved ? <><BookmarkCheck size={15} /> Saved to your playbook</> : <><Bookmark size={15} /> Save this move</>}
                      </button>
                    </div>

                    {card.sources.length > 0 && <Sources sources={card.sources} />}

                    <div className="flex flex-col sm:flex-row gap-2.5">
                      {nextUnseen() && <OrangeBtn label="Next person" icon={ArrowRight} onClick={() => { const n = nextUnseen(); if (n) open(n); }} />}
                      <NeutralBtn label="Back to deck" onClick={() => setCardId(null)} />
                    </div>
                  </>
                )}
              </MotionDiv>
            </AnimatePresence>
          </div>
        </HybridCard>
      </div>
    );
  }

  // ── SAVED VIEW ("your playbook") ──────────────────────────────
  if (showSaved) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <BackLink onClick={() => setShowSaved(false)} label="The deck" />
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>Your playbook</h2>
        <p className="text-[13px] mb-4" style={{ color: MUTED }}>The moves you saved — your own list of things to try.</p>
        {savedCards.length === 0 ? (
          <p className="text-[14px]" style={{ color: MUTED }}>Nothing saved yet — open a card and tap “Save this move”.</p>
        ) : (
          <div className="space-y-3">
            {savedCards.map((p) => {
              const wd = BARRIER_WORLD[p.barrier];
              return (
                <div key={p.id} className="rounded-2xl border-2 border-[#1A1A1A] bg-white shadow-[3px_3px_0_0_#1A1A1A] p-4">
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <span className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-[12px] font-bold" style={{ backgroundColor: wd.bg, fontFamily: SERIF, color: '#fff' }}>{initials(p.name)}</span>
                    <p className="text-[14px] font-semibold" style={{ color: INK }}>{p.name}</p>
                  </div>
                  <p className="text-[13.5px] leading-relaxed" style={{ color: BODY }}>{p.stealThisMove}</p>
                  <button onClick={() => open(p)} className="text-[12px] font-semibold mt-1.5" style={{ color: paperTone(wd) }}>Open card →</button>
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
    <div className="immersive-deck-theme w-full max-w-xl mx-auto pb-12">
      <p className="text-[13px] font-medium mb-2.5" style={{ color: BODY }}>Pick what’s closest to your situation:</p>

      {/* barrier filter */}
      <div className="flex flex-wrap gap-1.5 mb-6">
        <button onClick={() => setFilter('all')} className="rounded-xl border px-3.5 py-2 text-[12.5px] font-semibold transition-all" style={filter === 'all' ? { backgroundColor: 'var(--deck-ink)', color: 'var(--deck-paper)', borderColor: 'var(--deck-ink)' } : { backgroundColor: 'var(--deck-soft)', color: BODY, borderColor: 'var(--deck-hairline)' }}>Everyone</button>
        {BARRIERS.map((b) => {
          const wd = BARRIER_WORLD[b.id];
          const active = filter === b.id;
          return (
            <button key={b.id} onClick={() => setFilter(b.id)} className="rounded-xl border px-3.5 py-2 text-[12.5px] font-semibold transition-all" style={active ? { backgroundColor: wd.bg, color: '#fff', borderColor: wd.deep } : { backgroundColor: 'var(--deck-soft)', color: BODY, borderColor: 'var(--deck-hairline)' }}>
              {b.label}
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
        <HybridCard className="text-center">
          <Celebration colors={[WORLDS.teal.bg, WORLDS.teal.glow]} />
          <div className="relative p-8">
            <p className="text-[15px] mb-1" style={{ color: MUTED }}>That’s everyone in this group.</p>
            <p className="text-[22px] font-semibold mb-5" style={{ fontFamily: SERIF, color: INK }}>You’ve saved {state.savedIds.length} {state.savedIds.length === 1 ? 'move' : 'moves'}</p>
            <div className="flex flex-col sm:flex-row gap-2.5 justify-center items-center">
              <OrangeBtn label="Start over" icon={RotateCcw} onClick={() => setIndex(0)} />
              {state.savedIds.length > 0 && <NeutralBtn label="See your playbook" onClick={() => setShowSaved(true)} />}
            </div>
          </div>
        </HybridCard>
      )}

      {state.savedIds.length > 0 && index < deck.length && (
        <button onClick={() => setShowSaved(true)} className="w-full mt-6 flex items-center justify-center gap-2 rounded-xl border-2 py-3 text-[13px] font-semibold transition-colors" style={{ borderColor: HAIRLINE, color: BODY }}>
          <BookmarkCheck size={15} style={{ color: LABEL }} /> Your playbook ({state.savedIds.length})
        </button>
      )}
    </div>
  );
};

export default HowTheyDidIt;
