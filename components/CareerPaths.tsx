/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Career Paths" — a swipe card deck that shows Leaving Cert students what real
 * careers involve: what you do, what they pay (Irish €), how you get there, the
 * skills, and the honest pros & cons. Each card links to the real CAO courses
 * that lead there — the same courses the Future Finder outputs — so it doubles
 * as the "explore your matches" surface from the Future Finder results (seeded
 * via `seedMatches` + the shared InnovationDataContext picks).
 *
 * 2026-06-03 hybrid aesthetic: light white cards with a brightened colour HEADER
 * BAND + Lucide line-icon per field, Source Serif titles, orange chunky CTAs —
 * same family as the rest of the app. Uses the shared immersiveDeck/HybridCard
 * primitives so all three decks stay identical.
 */

import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, X, BookOpen, RotateCcw, Star, GraduationCap, ChevronDown, ExternalLink, ThumbsUp, Compass } from 'lucide-react';
import { useCareerPaths } from '../hooks/useCareerPaths';
import { CAREERS } from '../careerPathsData';
import { type CareerCard } from '../types/careerPaths';
import {
  WORLDS, type ColorWorld, DeckStack, useDeckSound, Celebration, CountUp,
  FIELD_WORLD, careerIcon,
  HybridCard, Band, BlobIcon, ProgressDots, OrangeBtn, NeutralBtn, Eyebrow,
  SERIF, INK, BODY, MUTED, LABEL, HAIRLINE,
} from './immersiveDeck';
import { CAO_COURSES, INSTITUTIONS, getCoursePageUrl, type CAOCourse } from './futureFinderData';
import { useInnovationData } from '../contexts/InnovationDataContext';

const fade = { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 }, transition: { duration: 0.24 } };
const euro = (k: number) => `€${k}k`;
/** Neutral light panel for "the catch" — not dark, not red, not warm-cream. */
const NEUTRAL_PANEL = '#F1F0ED';

/** Courses that lead to this career — computed at runtime from the real CAO catalog. */
const coursesFor = (c: CareerCard): CAOCourse[] =>
  CAO_COURSES.filter((course) => course.careerPaths.some((cp) => c.matchStrings.includes(cp)))
    .sort((a, b) => b.level - a.level || b.typicalPoints - a.typicalPoints)
    .slice(0, 6);

/** A tappable "course that leads here" row → opens the course page (white bordered row). */
const CourseRow: React.FC<{ course: CAOCourse; wd: ColorWorld }> = ({ course, wd }) => {
  const inst = INSTITUTIONS[course.institution] || course.institution;
  const isAppr = course.pathwayType === 'apprenticeship';
  const meta = isAppr ? 'Apprenticeship · earn as you learn' : `${inst} · L${course.level}${course.typicalPoints ? ` · ~${course.typicalPoints} pts` : ''}`;
  return (
    <a href={getCoursePageUrl(course)} target="_blank" rel="noreferrer" className="flex items-center gap-2.5 rounded-xl p-3" style={{ backgroundColor: '#fff', border: `1.5px solid ${HAIRLINE}`, color: INK }}>
      <GraduationCap size={16} style={{ color: wd.bg }} className="shrink-0" />
      <span className="flex-1 min-w-0">
        <span className="block text-[13.5px] font-semibold leading-tight truncate">{course.title}</span>
        <span className="block text-[11.5px] truncate" style={{ color: MUTED }}>{meta}</span>
      </span>
      <ExternalLink size={13} className="shrink-0" style={{ color: LABEL }} />
    </a>
  );
};

const Sources: React.FC<{ sources: string[] }> = ({ sources }) => {
  const [open, setOpen] = useState(false);
  if (!sources.length) return null;
  return (
    <div className="mb-1">
      <button onClick={() => setOpen((o) => !o)} className="inline-flex items-center gap-1.5 text-[12px] font-semibold" style={{ color: MUTED }}>
        Pay &amp; route sources ({sources.length})
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

/** The swipe-card / stack face — bespoke white card with a top colour zone. */
const CardFace: React.FC<{ c: CareerCard; saved: boolean; matched: boolean }> = ({ c, saved, matched }) => {
  const wd = FIELD_WORLD[c.field];
  const Icon = careerIcon(c.field, c.iconKey);
  return (
    <div className="w-full h-full rounded-[28px] overflow-hidden flex flex-col select-none relative" style={{ backgroundColor: '#fff', border: '2px solid #1a1a1a', boxShadow: '6px 8px 0 0 #1a1a1a' }}>
      <div className="relative flex-1 flex items-center justify-center pt-8">
        {matched && <span className="absolute top-4 left-4 text-[10px] font-bold uppercase tracking-[0.1em] px-2.5 py-1 rounded-full inline-flex items-center gap-1" style={{ backgroundColor: wd.tint, color: wd.deep }}><Star size={11} /> Your match</span>}
        {saved && <span className="absolute top-4 right-4 w-7 h-7 rounded-full flex items-center justify-center" style={{ backgroundColor: wd.tint }}><BookmarkCheck size={15} style={{ color: wd.deep }} /></span>}
        <BlobIcon wd={wd} icon={Icon} size={108} seed={c.title} />
      </div>
      <div className="px-6 pb-6 pt-2">
        <h3 className="text-[24px] leading-tight font-semibold" style={{ fontFamily: SERIF, color: INK }}>{c.title}</h3>
        <p className="text-[14.5px] leading-snug font-medium mb-3" style={{ color: MUTED }}>{c.tagline}</p>
        <div className="inline-flex items-center gap-1.5 self-start text-[13px] font-semibold px-3 py-1.5 rounded-full" style={{ backgroundColor: wd.tint, color: wd.deep }}>
          {euro(c.salary.startK)} <ArrowRight size={12} /> {euro(c.salary.experiencedK)}
        </div>
      </div>
    </div>
  );
};

type Beat = 'front' | 'day' | 'deal' | 'route';
const BEAT_IDX: Record<Beat, number> = { front: 0, day: 1, deal: 2, route: 3 };

const CareerPaths: React.FC<{ uid?: string; studentSubjects?: string[]; seedMatches?: boolean; seedMatchStrings?: string[] }> = ({ uid, seedMatches, seedMatchStrings }) => {
  const { state, isLoaded, markSeen, toggleSaved } = useCareerPaths(uid);
  const { futureFinderPicks } = useInnovationData();
  const sound = useDeckSound();

  // Careers the student's Future Finder results point to. Prefer the strings
  // passed straight from the Future Finder (always current); fall back to the
  // shared context's saved picks when opened cold from the tool grid.
  const matchedIds = useMemo(() => {
    const picked = new Set<string>();
    const strings = seedMatchStrings && seedMatchStrings.length ? seedMatchStrings : futureFinderPicks.flatMap((c) => c.careerPaths);
    strings.forEach((cp) => picked.add(cp));
    if (picked.size === 0) return new Set<string>();
    return new Set(CAREERS.filter((c) => c.matchStrings.some((m) => picked.has(m))).map((c) => c.id));
  }, [futureFinderPicks, seedMatchStrings]);
  const hasMatches = matchedIds.size > 0;

  const [filter, setFilter] = useState<'all' | 'matches'>(seedMatches && hasMatches ? 'matches' : 'all');
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('front');
  const [showSaved, setShowSaved] = useState(false);
  const [index, setIndex] = useState(0);
  const [burst, setBurst] = useState(false);
  useEffect(() => { setIndex(0); }, [filter]);
  // If we arrive seeded from the Future Finder once picks have loaded, jump to matches.
  useEffect(() => { if (seedMatches && hasMatches) setFilter('matches'); }, [seedMatches, hasMatches]);

  const deck = useMemo(() => (filter === 'matches' ? CAREERS.filter((c) => matchedIds.has(c.id)) : CAREERS), [filter, matchedIds]);
  const card = cardId ? CAREERS.find((c) => c.id === cardId) ?? null : null;
  const savedCards = useMemo(() => CAREERS.filter((c) => state.savedIds.includes(c.id)), [state.savedIds]);

  const open = (c: CareerCard) => { setCardId(c.id); setBeat('front'); markSeen(c.id); sound.play('tap'); };
  const advance = (c: CareerCard, dir: 'left' | 'right') => {
    if (dir === 'right') { if (!state.savedIds.includes(c.id)) toggleSaved(c.id); sound.play('save'); } else sound.play('skip');
    setIndex((i) => { const ni = i + 1; if (ni >= deck.length) sound.play('complete'); return ni; });
  };
  const goBeat = (b: Beat) => { setBeat(b); sound.play('tap'); };
  const saveFromDetail = (id: string) => {
    const wasSaved = state.savedIds.includes(id);
    toggleSaved(id);
    if (!wasSaved) { setBurst(true); sound.play('save'); window.setTimeout(() => setBurst(false), 950); }
  };
  const nextUnseen = (): CareerCard | null => deck.find((c) => c.id !== card?.id && !state.seenIds.includes(c.id)) ?? deck.find((c) => c.id !== card?.id) ?? null;

  if (!isLoaded) return <div className="w-full max-w-xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;

  // ── CARD DETAIL ───────────────────────────────────────────────
  if (card) {
    const wd = FIELD_WORLD[card.field];
    const CareerIcon = careerIcon(card.field, card.iconKey);
    const isSaved = state.savedIds.includes(card.id);
    const bi = BEAT_IDX[beat];
    const courses = coursesFor(card);
    return (
      <div className="w-full max-w-xl mx-auto pb-10">
        <button onClick={() => setCardId(null)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> All careers</button>
        <HybridCard>
          {burst && <Celebration colors={[wd.bg, wd.glow]} />}
          <Band wd={wd} icon={CareerIcon} eyebrow={card.field} title={card.title} right={<ProgressDots total={4} active={bi} />} />
          <div className="p-6 md:p-7">
            <AnimatePresence mode="wait">
              <MotionDiv key={beat} {...fade}>
                {beat === 'front' && (
                  <>
                    <p className="text-[24px] leading-tight font-semibold mb-3" style={{ fontFamily: SERIF, color: INK }}>{card.tagline}</p>
                    {matchedIds.has(card.id) && <span className="inline-flex items-center gap-1 text-[12px] font-semibold mb-7" style={{ color: wd.deep }}><Star size={12} /> matches your results</span>}
                    <div className="flex justify-end mt-4"><OrangeBtn label="What's it like?" icon={ArrowRight} onClick={() => goBeat('day')} /></div>
                  </>
                )}

                {beat === 'day' && (
                  <>
                    <Eyebrow>What you actually do</Eyebrow>
                    <div className="space-y-3 mb-6">
                      {card.whatYouDo.map((d, i) => (
                        <MotionDiv key={i} className="flex items-start gap-3" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.08 + i * 0.1 }}>
                          <span className="mt-2 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: wd.bg }} />
                          <p className="text-[15.5px] leading-snug" style={{ color: INK }}>{d}</p>
                        </MotionDiv>
                      ))}
                    </div>
                    <Eyebrow>Skills it takes</Eyebrow>
                    <div className="flex flex-wrap gap-1.5 mb-7">
                      {card.skills.map((s, i) => (
                        <span key={i} className="text-[12px] font-semibold px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.tint, color: wd.deep }}>{s}</span>
                      ))}
                    </div>
                    <div className="flex justify-between items-center">
                      <NeutralBtn label="Back" onClick={() => goBeat('front')} />
                      <OrangeBtn label="The pay" icon={ArrowRight} onClick={() => goBeat('deal')} />
                    </div>
                  </>
                )}

                {beat === 'deal' && (
                  <>
                    <Eyebrow>What it pays in Ireland</Eyebrow>
                    <div className="flex items-end gap-4 mb-2">
                      <div>
                        <p className="text-[11px] mb-0.5" style={{ color: MUTED }}>Starting</p>
                        <CountUp to={card.salary.startK} durationMs={800} format={euro} className="text-[34px] font-bold" style={{ fontFamily: SERIF, color: INK }} />
                      </div>
                      <ArrowRight size={20} className="mb-2.5" style={{ color: MUTED }} />
                      <div>
                        <p className="text-[11px] mb-0.5" style={{ color: MUTED }}>Experienced</p>
                        <CountUp to={card.salary.experiencedK} durationMs={1100} format={euro} className="text-[34px] font-bold" style={{ fontFamily: SERIF, color: INK }} />
                      </div>
                    </div>
                    <div className="h-2 rounded-full mb-2 overflow-hidden" style={{ backgroundColor: wd.tint }}>
                      <MotionDiv className="h-full rounded-full" style={{ backgroundColor: wd.bg }} initial={{ width: '12%' }} animate={{ width: '100%' }} transition={{ duration: 1.1, ease: 'easeOut' }} />
                    </div>
                    <p className="text-[12.5px] mb-6" style={{ color: MUTED }}>{card.salary.note}</p>

                    <div className="grid grid-cols-2 gap-3 mb-7">
                      <div className="rounded-2xl p-3.5" style={{ backgroundColor: wd.tint }}>
                        <div className="flex items-center gap-1.5 mb-2" style={{ color: wd.deep }}><ThumbsUp size={13} /><p className="text-[10px] font-bold uppercase tracking-[0.1em]">The good</p></div>
                        <ul className="space-y-1.5">{card.pros.map((p, i) => <li key={i} className="text-[12.5px] leading-snug" style={{ color: BODY }}>{p}</li>)}</ul>
                      </div>
                      <div className="rounded-2xl p-3.5" style={{ backgroundColor: NEUTRAL_PANEL }}>
                        <div className="flex items-center gap-1.5 mb-2" style={{ color: MUTED }}>
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 14V2" /><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z" /></svg>
                          <p className="text-[10px] font-bold uppercase tracking-[0.1em]">The catch</p>
                        </div>
                        <ul className="space-y-1.5">{card.cons.map((p, i) => <li key={i} className="text-[12.5px] leading-snug" style={{ color: BODY }}>{p}</li>)}</ul>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <NeutralBtn label="Back" onClick={() => goBeat('day')} />
                      <OrangeBtn label="How you get there" icon={ArrowRight} onClick={() => goBeat('route')} />
                    </div>
                  </>
                )}

                {beat === 'route' && (
                  <>
                    <Eyebrow>How you get there</Eyebrow>
                    <div className="space-y-2.5 mb-6">
                      {card.routes.map((r, i) => (
                        <div key={i} className="rounded-2xl p-3.5" style={{ backgroundColor: wd.tint }}>
                          <p className="text-[13.5px] font-bold mb-0.5" style={{ color: INK }}>{r.label}</p>
                          <p className="text-[13px] leading-snug" style={{ color: MUTED }}>{r.detail}</p>
                        </div>
                      ))}
                    </div>

                    {courses.length > 0 && (
                      <>
                        <Eyebrow>Courses that lead here</Eyebrow>
                        <div className="space-y-2 mb-6">{courses.map((co) => <CourseRow key={co.code} course={co} wd={wd} />)}</div>
                      </>
                    )}

                    <button onClick={() => saveFromDetail(card.id)} className="inline-flex items-center gap-1.5 text-[13px] font-semibold px-4 py-2.5 rounded-full mb-4 transition-transform active:translate-y-0.5" style={isSaved ? { backgroundColor: wd.bg, color: '#fff' } : { backgroundColor: '#fff', border: `2px solid ${wd.bg}`, color: wd.deep }}>
                      {isSaved ? <><BookmarkCheck size={15} /> Saved to your shortlist</> : <><Bookmark size={15} /> Save to shortlist</>}
                    </button>

                    <Sources sources={card.sources} />

                    <div className="flex flex-col sm:flex-row gap-2.5 mt-4">
                      {nextUnseen() && <OrangeBtn label="Next career" icon={ArrowRight} onClick={() => { const n = nextUnseen(); if (n) open(n); }} />}
                      <NeutralBtn label="All careers" onClick={() => setCardId(null)} />
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

  // ── SAVED ("your shortlist") ──────────────────────────────────
  if (showSaved) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setShowSaved(false)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> The deck</button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>Your shortlist</h2>
        <p className="text-[13px] mb-4" style={{ color: MUTED }}>Careers you saved — bring these to your guidance counsellor.</p>
        {savedCards.length === 0 ? (
          <p className="text-[14px]" style={{ color: MUTED }}>Nothing saved yet — swipe right or tap “Save to shortlist”.</p>
        ) : (
          <div className="space-y-3">
            {savedCards.map((c) => {
              const wd = FIELD_WORLD[c.field];
              const Icon = careerIcon(c.field, c.iconKey);
              return (
                <div key={c.id} className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] p-4">
                  <div className="flex items-center gap-2.5 mb-1">
                    <span className="w-8 h-8 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.bg }}><Icon size={16} color="#fff" /></span>
                    <div><p className="text-[14px] font-semibold leading-tight" style={{ color: INK }}>{c.title}</p><p className="text-[12px]" style={{ color: MUTED }}>{euro(c.salary.startK)} → {euro(c.salary.experiencedK)}</p></div>
                  </div>
                  <p className="text-[13px] leading-snug" style={{ color: BODY }}>{c.tagline}</p>
                  <button onClick={() => open(c)} className="text-[12px] font-semibold mt-1.5" style={{ color: wd.deep }}>Open card →</button>
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
  const topWorld = top ? FIELD_WORLD[top.field] : WORLDS.ocean;
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {hasMatches && (
        <div className="flex flex-wrap gap-1.5 mb-4">
          <button onClick={() => setFilter('matches')} className="rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold inline-flex items-center gap-1.5 transition-colors" style={filter === 'matches' ? { backgroundColor: '#1a1a1a', color: '#fff' } : { backgroundColor: '#F1F0ED', color: '#3a3530' }}><Star size={13} /> Your matches ({matchedIds.size})</button>
          <button onClick={() => setFilter('all')} className="rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold transition-colors" style={filter === 'all' ? { backgroundColor: '#1a1a1a', color: '#fff' } : { backgroundColor: '#F1F0ED', color: '#3a3530' }}>All careers</button>
        </div>
      )}
      {filter === 'matches' && (
        <div className="flex items-start gap-2 rounded-xl p-3 mb-4" style={{ backgroundColor: '#F1F0ED' }}>
          <Compass size={15} className="mt-0.5 shrink-0 text-zinc-500" />
          <p className="text-[12.5px] text-zinc-600">Careers your Future Finder results point toward. Swipe through, then tap any for the full picture.</p>
        </div>
      )}
      {!hasMatches && <p className="text-[13px] font-medium mb-3 text-zinc-600 dark:text-zinc-300">Swipe through real careers — what they’re like, what they pay, and how to get there.</p>}

      {index < deck.length ? (
        <>
          <DeckStack items={deck} index={index} onAdvance={advance} onOpen={open} renderFace={(c) => <CardFace c={c} saved={state.savedIds.includes(c.id)} matched={matchedIds.has(c.id)} />} />
          <div className="flex items-center justify-center gap-3 mt-6">
            <button onClick={() => top && advance(top, 'left')} aria-label="Skip" className="w-12 h-12 rounded-full border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105"><X size={20} className="text-zinc-400" /></button>
            <OrangeBtn label="Explore this career" icon={BookOpen} onClick={() => top && open(top)} />
            <button onClick={() => top && advance(top, 'right')} aria-label="Save" className="w-12 h-12 rounded-full border-2 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105" style={{ borderColor: topWorld.bg }}><Bookmark size={20} style={{ color: topWorld.bg }} /></button>
          </div>
          <p className="text-center text-[12px] mt-3 text-zinc-400">Swipe the card, or use the buttons · {deck.length - index} to go</p>
        </>
      ) : (
        <HybridCard className="text-center">
          <Celebration colors={[WORLDS.ocean.bg, WORLDS.ocean.glow]} />
          <div className="relative p-8">
            <span className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4" style={{ backgroundColor: WORLDS.ocean.bg }}><BookmarkCheck size={22} color="#fff" /></span>
            <p className="text-[15px] mb-1" style={{ color: MUTED }}>That’s the deck.</p>
            <p className="text-[22px] font-semibold mb-5" style={{ fontFamily: SERIF, color: INK }}>{state.savedIds.length} {state.savedIds.length === 1 ? 'career' : 'careers'} on your shortlist</p>
            <div className="flex flex-col sm:flex-row gap-2.5 justify-center">
              <OrangeBtn label="Start over" icon={RotateCcw} onClick={() => setIndex(0)} />
              {state.savedIds.length > 0 && <NeutralBtn label="See your shortlist" onClick={() => setShowSaved(true)} />}
            </div>
          </div>
        </HybridCard>
      )}

      {state.savedIds.length > 0 && index < deck.length && (
        <button onClick={() => setShowSaved(true)} className="w-full mt-6 flex items-center justify-center gap-2 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 py-3 text-[13px] font-semibold text-zinc-700 dark:text-zinc-300">
          <BookmarkCheck size={15} /> Your shortlist ({state.savedIds.length})
        </button>
      )}
    </div>
  );
};

export default CareerPaths;
