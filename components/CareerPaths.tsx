/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Career Paths" — an immersive "colour world" card deck that shows Leaving Cert
 * students what real careers involve: what you do, what they pay (Irish €), how
 * you get there, the skills, and the honest pros & cons. Each card links to the
 * real CAO courses that lead there — the same courses the Future Finder outputs —
 * so it doubles as the "explore your matches" surface from the Future Finder
 * results (seeded via `seedMatches` + the shared InnovationDataContext picks).
 *
 * Same register + primitives as How They Did It: bold full-bleed colour per
 * field, one idea per screen, swipe + tap-to-reveal, animated salary count-up.
 */

import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, X, BookOpen, RotateCcw, Star, GraduationCap, ChevronDown, ExternalLink, ThumbsUp, ThumbsDown, Compass } from 'lucide-react';
import { useCareerPaths } from '../hooks/useCareerPaths';
import { CAREERS } from '../careerPathsData';
import { type CareerCard, type CareerField } from '../types/careerPaths';
import { WORLDS, type ColorWorld, DeckStack, useDeckSound, Celebration, CountUp } from './immersiveDeck';
import { CAO_COURSES, INSTITUTIONS, getCoursePageUrl, type CAOCourse } from './futureFinderData';
import { useInnovationData } from '../contexts/InnovationDataContext';

/** Each career field owns a colour world. */
const FIELD_WORLD: Record<CareerField, ColorWorld> = {
  health: WORLDS.teal,
  animals: WORLDS.forest,
  tech: WORLDS.ocean,
  engineering: WORLDS.slate,
  law: WORLDS.indigo,
  psychology: WORLDS.rose,
  business: WORLDS.denim,
  education: WORLDS.terracotta,
  design: WORLDS.rust,
  science: WORLDS.pine,
  trades: WORLDS.cocoa,
  creative: WORLDS.claret,
};

const SERIF = "'Source Serif 4', serif";
const fade = { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 }, transition: { duration: 0.24 } };
const euro = (k: number) => `€${k}k`;

/** Courses that lead to this career — computed at runtime from the real CAO catalog. */
const coursesFor = (c: CareerCard): CAOCourse[] =>
  CAO_COURSES.filter((course) => course.careerPaths.some((cp) => c.matchStrings.includes(cp)))
    .sort((a, b) => b.level - a.level || b.typicalPoints - a.typicalPoints)
    .slice(0, 6);

const Glow: React.FC<{ wd: ColorWorld }> = ({ wd }) => (
  <div className="absolute -top-12 -right-10 w-48 h-48 rounded-full pointer-events-none" style={{ backgroundColor: wd.glow, opacity: 0.4, filter: 'blur(10px)' }} />
);

const Label: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <p className="text-[10px] font-bold uppercase tracking-[0.16em] mb-3" style={{ color: 'rgba(255,255,255,0.7)' }}>{children}</p>
);

const WorldButton: React.FC<{ label: string; icon?: React.ElementType; onClick: () => void; wd: ColorWorld }> = ({ label, icon: Icon, onClick, wd }) => (
  <button onClick={onClick} className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-[14px] font-semibold transition-transform active:translate-y-0.5" style={{ backgroundColor: '#fff', color: wd.deep, boxShadow: '0 4px 0 0 rgba(0,0,0,0.18)' }}>
    {label} {Icon && <Icon size={16} />}
  </button>
);

const GhostBack: React.FC<{ onClick: () => void }> = ({ onClick }) => (
  <button onClick={onClick} className="text-[13px] font-medium" style={{ color: 'rgba(255,255,255,0.7)' }}>Back</button>
);

const Chip: React.FC<{ children: React.ReactNode; wd: ColorWorld }> = ({ children, wd }) => (
  <span className="text-[12px] font-medium px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: '#fff' }}>{children}</span>
);

/** A tappable "course that leads here" row → opens the course page. */
const CourseRow: React.FC<{ course: CAOCourse; wd: ColorWorld }> = ({ course, wd }) => {
  const inst = INSTITUTIONS[course.institution] || course.institution;
  const isAppr = course.pathwayType === 'apprenticeship';
  const meta = isAppr ? 'Apprenticeship · earn as you learn' : `${inst} · L${course.level}${course.typicalPoints ? ` · ~${course.typicalPoints} pts` : ''}`;
  return (
    <a href={getCoursePageUrl(course)} target="_blank" rel="noreferrer" className="flex items-center gap-2.5 rounded-xl p-3" style={{ backgroundColor: '#fff', color: '#1a1a1a' }}>
      <GraduationCap size={16} style={{ color: wd.bg }} className="shrink-0" />
      <span className="flex-1 min-w-0">
        <span className="block text-[13.5px] font-semibold leading-tight truncate">{course.title}</span>
        <span className="block text-[11.5px] text-zinc-500 truncate">{meta}</span>
      </span>
      <ExternalLink size={13} className="text-zinc-400 shrink-0" />
    </a>
  );
};

const Sources: React.FC<{ sources: string[] }> = ({ sources }) => {
  const [open, setOpen] = useState(false);
  if (!sources.length) return null;
  return (
    <div className="mb-1">
      <button onClick={() => setOpen((o) => !o)} className="inline-flex items-center gap-1.5 text-[12px] font-semibold" style={{ color: 'rgba(255,255,255,0.78)' }}>
        Pay &amp; route sources ({sources.length})
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

/** The swipe-card / stack face. */
const CardFace: React.FC<{ c: CareerCard; saved: boolean; matched: boolean }> = ({ c, saved, matched }) => {
  const wd = FIELD_WORLD[c.field];
  return (
    <div className="w-full h-full rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden flex flex-col select-none relative" style={{ backgroundColor: wd.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: wd.onBg }}>
      <Glow wd={wd} />
      <div className="relative flex-1 flex items-center justify-center px-6 pt-9">
        {matched && <span className="absolute top-4 left-4 text-[10px] font-bold uppercase tracking-[0.1em] px-2.5 py-1 rounded-full inline-flex items-center gap-1" style={{ backgroundColor: '#fff', color: wd.deep }}><Star size={11} /> Your match</span>}
        {saved && <span className="absolute top-4 right-4 w-7 h-7 rounded-full flex items-center justify-center" style={{ backgroundColor: '#fff' }}><BookmarkCheck size={15} style={{ color: wd.bg }} /></span>}
        <div className="w-28 h-28 rounded-full flex items-center justify-center" style={{ backgroundColor: wd.chip }}>
          <span style={{ fontSize: 58, lineHeight: 1 }}>{c.emoji}</span>
        </div>
      </div>
      <div className="relative px-6 pb-6 pt-2">
        <h3 className="text-[25px] leading-tight font-semibold" style={{ fontFamily: SERIF }}>{c.title}</h3>
        <p className="text-[15px] leading-snug font-medium mb-3" style={{ color: wd.onSoft }}>{c.tagline}</p>
        <div className="inline-flex items-center gap-1.5 text-[13px] font-semibold px-3 py-1.5 rounded-full" style={{ backgroundColor: wd.chip }}>
          {euro(c.salary.startK)} <ArrowRight size={12} /> {euro(c.salary.experiencedK)}
        </div>
      </div>
    </div>
  );
};

type Beat = 'front' | 'day' | 'deal' | 'route';
const BEAT_IDX: Record<Beat, number> = { front: 0, day: 1, deal: 2, route: 3 };

const CareerPaths: React.FC<{ uid?: string; studentSubjects?: string[]; seedMatches?: boolean }> = ({ uid, seedMatches }) => {
  const { state, isLoaded, markSeen, toggleSaved } = useCareerPaths(uid);
  const { futureFinderPicks } = useInnovationData();
  const sound = useDeckSound();

  // Careers the student's Future Finder results point to.
  const matchedIds = useMemo(() => {
    const picked = new Set<string>();
    futureFinderPicks.forEach((course) => course.careerPaths.forEach((cp) => picked.add(cp)));
    if (picked.size === 0) return new Set<string>();
    return new Set(CAREERS.filter((c) => c.matchStrings.some((m) => picked.has(m))).map((c) => c.id));
  }, [futureFinderPicks]);
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
    const isSaved = state.savedIds.includes(card.id);
    const bi = BEAT_IDX[beat];
    const courses = coursesFor(card);
    return (
      <div className="w-full max-w-xl mx-auto pb-10">
        <button onClick={() => setCardId(null)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> All careers</button>
        <div className="relative rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden" style={{ backgroundColor: wd.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: wd.onBg }}>
          <Glow wd={wd} />
          {burst && <Celebration colors={['#ffffff', wd.glow]} />}
          <div className="relative p-6 md:p-7">
            <div className="flex items-center justify-between mb-5">
              <span className="text-[10px] font-bold uppercase tracking-[0.12em] px-2.5 py-1 rounded-full" style={{ backgroundColor: wd.chip, color: wd.onBg }}>{card.field}</span>
              <div className="flex items-center gap-1.5">
                {[0, 1, 2, 3].map((s) => <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === bi ? 18 : 6, backgroundColor: s <= bi ? '#fff' : 'rgba(255,255,255,0.35)' }} />)}
              </div>
            </div>

            <AnimatePresence mode="wait">
              <MotionDiv key={beat} {...fade}>
                {beat === 'front' && (
                  <>
                    <div className="flex items-center gap-3.5 mb-5">
                      <div className="w-16 h-16 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.chip }}><span style={{ fontSize: 33, lineHeight: 1 }}>{card.emoji}</span></div>
                      <div>
                        <h2 className="text-[23px] font-semibold leading-tight" style={{ fontFamily: SERIF }}>{card.title}</h2>
                        {matchedIds.has(card.id) && <span className="inline-flex items-center gap-1 text-[11px] font-semibold mt-0.5" style={{ color: '#fff' }}><Star size={11} /> matches your results</span>}
                      </div>
                    </div>
                    <p className="text-[24px] leading-tight font-semibold mb-7" style={{ fontFamily: SERIF }}>{card.tagline}</p>
                    <div className="flex justify-end"><WorldButton label="What's it like?" icon={ArrowRight} onClick={() => goBeat('day')} wd={wd} /></div>
                  </>
                )}

                {beat === 'day' && (
                  <>
                    <Label>What you actually do</Label>
                    <div className="space-y-3 mb-6">
                      {card.whatYouDo.map((d, i) => (
                        <MotionDiv key={i} className="flex items-start gap-3" initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.08 + i * 0.1 }}>
                          <span className="mt-2 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: '#fff' }} />
                          <p className="text-[16px] leading-snug">{d}</p>
                        </MotionDiv>
                      ))}
                    </div>
                    <Label>Skills it takes</Label>
                    <div className="flex flex-wrap gap-1.5 mb-7">{card.skills.map((s, i) => <Chip key={i} wd={wd}>{s}</Chip>)}</div>
                    <div className="flex justify-between items-center">
                      <GhostBack onClick={() => goBeat('front')} />
                      <WorldButton label="The pay" icon={ArrowRight} onClick={() => goBeat('deal')} wd={wd} />
                    </div>
                  </>
                )}

                {beat === 'deal' && (
                  <>
                    <Label>What it pays in Ireland</Label>
                    <div className="flex items-end gap-4 mb-2">
                      <div>
                        <p className="text-[11px] mb-0.5" style={{ color: wd.onSoft }}>Starting</p>
                        <CountUp to={card.salary.startK} durationMs={800} format={euro} className="text-[34px] font-bold" style={{ fontFamily: SERIF }} />
                      </div>
                      <ArrowRight size={20} className="mb-2.5" style={{ color: wd.onSoft }} />
                      <div>
                        <p className="text-[11px] mb-0.5" style={{ color: wd.onSoft }}>Experienced</p>
                        <CountUp to={card.salary.experiencedK} durationMs={1100} format={euro} className="text-[34px] font-bold" style={{ fontFamily: SERIF }} />
                      </div>
                    </div>
                    <div className="h-2 rounded-full mb-2 overflow-hidden" style={{ backgroundColor: wd.chip }}>
                      <MotionDiv className="h-full rounded-full" style={{ backgroundColor: '#fff' }} initial={{ width: '12%' }} animate={{ width: '100%' }} transition={{ duration: 1.1, ease: 'easeOut' }} />
                    </div>
                    <p className="text-[12.5px] mb-6" style={{ color: wd.onSoft }}>{card.salary.note}</p>

                    <div className="grid grid-cols-2 gap-3 mb-7">
                      <div className="rounded-2xl p-3.5" style={{ backgroundColor: wd.chip }}>
                        <div className="flex items-center gap-1.5 mb-2"><ThumbsUp size={13} /><p className="text-[10px] font-bold uppercase tracking-[0.1em]">The good</p></div>
                        <ul className="space-y-1.5">{card.pros.map((p, i) => <li key={i} className="text-[12.5px] leading-snug">{p}</li>)}</ul>
                      </div>
                      <div className="rounded-2xl p-3.5" style={{ backgroundColor: 'rgba(0,0,0,0.18)' }}>
                        <div className="flex items-center gap-1.5 mb-2"><ThumbsDown size={13} /><p className="text-[10px] font-bold uppercase tracking-[0.1em]">The catch</p></div>
                        <ul className="space-y-1.5">{card.cons.map((p, i) => <li key={i} className="text-[12.5px] leading-snug">{p}</li>)}</ul>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <GhostBack onClick={() => goBeat('day')} />
                      <WorldButton label="How you get there" icon={ArrowRight} onClick={() => goBeat('route')} wd={wd} />
                    </div>
                  </>
                )}

                {beat === 'route' && (
                  <>
                    <Label>How you get there from the Leaving Cert</Label>
                    <div className="space-y-2.5 mb-6">
                      {card.routes.map((r, i) => (
                        <div key={i} className="rounded-2xl p-3.5" style={{ backgroundColor: wd.chip }}>
                          <p className="text-[13.5px] font-bold mb-0.5">{r.label}</p>
                          <p className="text-[13px] leading-snug" style={{ color: wd.onSoft }}>{r.detail}</p>
                        </div>
                      ))}
                    </div>

                    {courses.length > 0 && (
                      <>
                        <Label>Courses that lead here</Label>
                        <div className="space-y-2 mb-6">{courses.map((co) => <CourseRow key={co.code} course={co} wd={wd} />)}</div>
                      </>
                    )}

                    <button onClick={() => saveFromDetail(card.id)} className="inline-flex items-center gap-1.5 text-[13px] font-semibold px-4 py-2.5 rounded-full mb-4 transition-transform active:translate-y-0.5" style={isSaved ? { backgroundColor: '#fff', color: wd.deep } : { border: '2px solid rgba(255,255,255,0.6)', color: '#fff' }}>
                      {isSaved ? <><BookmarkCheck size={15} /> Saved to your shortlist</> : <><Bookmark size={15} /> Save to shortlist</>}
                    </button>

                    <Sources sources={card.sources} />

                    <div className="flex flex-col sm:flex-row gap-2.5 mt-4">
                      {nextUnseen() && <WorldButton label="Next career" icon={ArrowRight} onClick={() => { const n = nextUnseen(); if (n) open(n); }} wd={wd} />}
                      <button onClick={() => setCardId(null)} className="px-5 py-3 rounded-full text-[14px] font-semibold" style={{ border: '2px solid rgba(255,255,255,0.5)', color: '#fff' }}>All careers</button>
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

  // ── SAVED ("your shortlist") ──────────────────────────────────
  if (showSaved) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setShowSaved(false)} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"><ArrowLeft size={15} /> The deck</button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: SERIF, color: '#1a1a1a' }}>Your shortlist</h2>
        <p className="text-[13px] text-zinc-500 mb-4">Careers you saved — bring these to your guidance counsellor.</p>
        {savedCards.length === 0 ? (
          <p className="text-[14px] text-zinc-500">Nothing saved yet — swipe right or tap “Save to shortlist”.</p>
        ) : (
          <div className="space-y-3">
            {savedCards.map((c) => {
              const wd = FIELD_WORLD[c.field];
              return (
                <div key={c.id} className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] p-4">
                  <div className="flex items-center gap-2.5 mb-1">
                    <span className="w-8 h-8 rounded-full flex items-center justify-center shrink-0" style={{ backgroundColor: wd.bg }}><span style={{ fontSize: 17 }}>{c.emoji}</span></span>
                    <div><p className="text-[14px] font-semibold text-zinc-900 dark:text-white leading-tight">{c.title}</p><p className="text-[12px] text-zinc-500">{euro(c.salary.startK)} → {euro(c.salary.experiencedK)}</p></div>
                  </div>
                  <p className="text-[13px] leading-snug text-zinc-600 dark:text-zinc-300">{c.tagline}</p>
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
            <button onClick={() => top && open(top)} className="inline-flex items-center gap-2 px-5 py-3 rounded-full text-[14px] font-semibold text-white transition-transform active:translate-y-0.5" style={{ backgroundColor: topWorld.bg, boxShadow: `0 4px 0 0 ${topWorld.deep}` }}><BookOpen size={16} /> Explore this career</button>
            <button onClick={() => top && advance(top, 'right')} aria-label="Save" className="w-12 h-12 rounded-full border-2 bg-white dark:bg-zinc-900 flex items-center justify-center transition-transform hover:scale-105" style={{ borderColor: topWorld.bg }}><Bookmark size={20} style={{ color: topWorld.bg }} /></button>
          </div>
          <p className="text-center text-[12px] mt-3 text-zinc-400">Swipe the card, or use the buttons · {deck.length - index} to go</p>
        </>
      ) : (
        <div className="relative rounded-[28px] border-2 border-[#1A1A1A] overflow-hidden text-center" style={{ backgroundColor: WORLDS.ocean.bg, boxShadow: '6px 8px 0 0 #1A1A1A', color: '#fff' }}>
          <Glow wd={WORLDS.ocean} />
          <Celebration colors={['#ffffff', WORLDS.ocean.glow]} />
          <div className="relative p-8">
            <p className="text-[15px] mb-1" style={{ color: 'rgba(255,255,255,0.85)' }}>That’s the deck.</p>
            <p className="text-[22px] font-semibold mb-5" style={{ fontFamily: SERIF }}>{state.savedIds.length} {state.savedIds.length === 1 ? 'career' : 'careers'} on your shortlist 🎯</p>
            <div className="flex flex-col sm:flex-row gap-2.5 justify-center">
              <WorldButton label="Start over" icon={RotateCcw} onClick={() => setIndex(0)} wd={WORLDS.ocean} />
              {state.savedIds.length > 0 && <button onClick={() => setShowSaved(true)} className="px-5 py-3 rounded-full text-[14px] font-semibold" style={{ border: '2px solid rgba(255,255,255,0.5)', color: '#fff' }}>See your shortlist</button>}
            </div>
          </div>
        </div>
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
