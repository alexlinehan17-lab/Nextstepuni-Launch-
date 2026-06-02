/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Catch-Up Lane — absence-recovery micro-units.
 *
 * Missed some classes? Pick a subject and get caught up one quick topic at a
 * time: a 90-second gist → the one move that matters → a quick check you
 * self-mark → "recovered". Reassurance-first, no shame about the absence.
 *
 * Aesthetics: the Innovation-Zone tool card vocabulary (chunky bordered
 * cardShell, PrimaryActionButton) with a calm cyan identity. White cards on a
 * cool ground; cool teal-tint (#E6F4F5) for callouts — never warm cream; no
 * coloured left borders (status shown via dots / fills / text).
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import {
  ArrowLeft, ArrowRight, Check, CheckCircle2, Circle, RotateCcw,
  Sparkles, Waypoints, BookOpenCheck,
} from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useCatchUpLane } from '../../hooks/useCatchUpLane';
import { useInnovationData } from '../../contexts/InnovationDataContext';
import { RECOVERY_CARDS, cardsForSubject, subjectsWithContent } from '../../catchUpLaneData';
import { type RecoveryCard } from '../../types/catchUpLane';

const CYAN = '#0E9AA8';
const CYAN_DARK = '#0B6E7A';
const CYAN_TINT = '#E6F4F5';
const CYAN_DARK_TEXT = '#0A5560';

const cardShell =
  'w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7';

type View = 'home' | 'queue' | 'unit';
type Beat = 'gist' | 'move' | 'check' | 'reveal' | 'done';

const fade = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: { duration: 0.22 },
};

const CatchUpLane: React.FC<{ uid?: string; studentSubjects?: string[] }> = ({ uid, studentSubjects }) => {
  const { state, isLoaded, markRecovered, markShaky, marksProtected } = useCatchUpLane(uid);
  const { topicMastery } = useInnovationData();

  const [view, setView] = useState<View>('home');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('gist');
  const [ticks, setTicks] = useState<boolean[]>([]);

  const recovered = useMemo(() => new Set(state.recoveredTopicIds), [state.recoveredTopicIds]);
  const shaky = useMemo(() => new Set(state.shakyTopicIds), [state.shakyTopicIds]);

  const available = useMemo(() => subjectsWithContent(), []);
  const studentSet = useMemo(
    () => new Set((studentSubjects ?? []).map(s => s.toLowerCase())),
    [studentSubjects],
  );
  // Subjects the student takes that we don't have content for yet (honest "coming soon").
  const comingSoon = useMemo(
    () => (studentSubjects ?? []).filter(
      name => !available.some(a => a.subjectLabel.toLowerCase() === name.toLowerCase()),
    ),
    [studentSubjects, available],
  );

  const subjectCards = subjectId ? cardsForSubject(subjectId) : [];
  const card = cardId ? RECOVERY_CARDS.find(c => c.id === cardId) ?? null : null;
  const totalCards = RECOVERY_CARDS.length;
  const recoveredCount = recovered.size;

  // ── navigation ──
  const openSubject = (sid: string) => { setSubjectId(sid); setView('queue'); };
  const openCard = (c: RecoveryCard) => {
    setCardId(c.id);
    setBeat('gist');
    setTicks(new Array(c.check.needed.length).fill(false));
    setView('unit');
  };
  const onRecovered = () => {
    if (!card) return;
    markRecovered(card.topicId);
    try { topicMastery.setTopicConfidence(card.subjectLabel, card.topicLabel, 'solid'); } catch { /* mastery optional */ }
    setBeat('done');
  };
  const onShaky = () => {
    if (!card) return;
    markShaky(card.topicId);
    try { topicMastery.setTopicConfidence(card.subjectLabel, card.topicLabel, 'shaky'); } catch { /* optional */ }
    setView('queue');
  };
  const nextUnrecovered = (): RecoveryCard | null =>
    subjectCards.find(c => !recovered.has(c.topicId) && c.id !== card?.id) ?? null;

  if (!isLoaded) {
    return <div className="w-full max-w-xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;
  }

  // ───────────────────────── HOME ─────────────────────────
  if (view === 'home') {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {/* Reassurance intro */}
        <p className="text-[15px] leading-relaxed mb-5" style={{ color: '#5a5550', fontFamily: "'DM Sans', sans-serif" }}>
          Missed a few classes? It happens — and it’s fixable. Pick a subject and we’ll get you back on track,
          one quick topic at a time. No catch-up is too small.
        </p>

        {/* Progress (only once they've recovered something) */}
        {recoveredCount > 0 && (
          <div className="rounded-2xl p-5 mb-6" style={{ backgroundColor: CYAN_TINT }}>
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: CYAN_DARK_TEXT }}>Caught up so far</span>
              <span className="text-[11px] font-semibold" style={{ color: CYAN_DARK_TEXT }}>≈{marksProtected} marks back in reach</span>
            </div>
            <p className="text-2xl font-semibold mb-3" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
              {recoveredCount} {recoveredCount === 1 ? 'topic' : 'topics'} recovered
            </p>
            <div className="h-2.5 rounded-full overflow-hidden" style={{ backgroundColor: '#ffffff' }}>
              <div className="h-full rounded-full transition-all" style={{ width: `${Math.round((recoveredCount / totalCards) * 100)}%`, backgroundColor: CYAN }} />
            </div>
          </div>
        )}

        <h2 className="text-[13px] font-bold uppercase tracking-[0.14em] mb-3" style={{ color: '#9e9186' }}>
          Pick a subject to catch up on
        </h2>

        <div className="space-y-3">
          {available.map(s => {
            const cards = cardsForSubject(s.subjectId);
            const done = cards.filter(c => recovered.has(c.topicId)).length;
            const isMine = studentSet.has(s.subjectLabel.toLowerCase());
            return (
              <button
                key={s.subjectId}
                onClick={() => openSubject(s.subjectId)}
                className="w-full text-left rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] p-4 flex items-center gap-4 transition-transform hover:-translate-y-0.5"
              >
                <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: CYAN_TINT }}>
                  <BookOpenCheck size={20} style={{ color: CYAN }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="text-base font-semibold text-zinc-900 dark:text-white" style={{ fontFamily: "'Source Serif 4', serif" }}>{s.subjectLabel}</p>
                    {isMine && (
                      <span className="text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-full" style={{ backgroundColor: CYAN_TINT, color: CYAN_DARK_TEXT }}>Yours</span>
                    )}
                  </div>
                  <p className="text-[12px] text-zinc-500">
                    {done > 0 ? `${done} of ${s.count} caught up` : `${s.count} topics ready`}
                  </p>
                </div>
                <ArrowRight size={18} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
              </button>
            );
          })}
        </div>

        {comingSoon.length > 0 && (
          <p className="text-[12px] leading-relaxed mt-5" style={{ color: '#9e9186' }}>
            More of your subjects are on the way{comingSoon.length <= 4 ? `: ${comingSoon.join(', ')}` : ''}. We’re adding
            them subject by subject.
          </p>
        )}
      </div>
    );
  }

  // ───────────────────────── QUEUE ─────────────────────────
  if (view === 'queue' && subjectId) {
    const subjLabel = subjectCards[0]?.subjectLabel ?? '';
    const done = subjectCards.filter(c => recovered.has(c.topicId)).length;
    // shaky first, then not-started, then recovered last
    const ordered = [...subjectCards].sort((a, b) => {
      const rank = (c: RecoveryCard) => recovered.has(c.topicId) ? 2 : shaky.has(c.topicId) ? 0 : 1;
      return rank(a) - rank(b);
    });
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setView('home')} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4">
          <ArrowLeft size={15} /> All subjects
        </button>

        <div className="flex items-baseline justify-between mb-1">
          <h2 className="text-2xl font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{subjLabel}</h2>
          <span className="text-[12px] font-semibold" style={{ color: CYAN_DARK_TEXT }}>{done} of {subjectCards.length} caught up</span>
        </div>
        <p className="text-[13px] mb-5" style={{ color: '#7a7068' }}>Tap a topic you missed. Each one’s about three minutes.</p>

        <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] overflow-hidden">
          {ordered.map((c, i) => {
            const isRec = recovered.has(c.topicId);
            const isShaky = shaky.has(c.topicId);
            return (
              <button
                key={c.id}
                onClick={() => openCard(c)}
                className={`w-full text-left flex items-center gap-3 px-4 py-3.5 transition-colors hover:bg-zinc-50 dark:hover:bg-white/[0.04] ${i > 0 ? 'border-t border-zinc-100 dark:border-zinc-800' : ''}`}
              >
                {isRec
                  ? <CheckCircle2 size={20} style={{ color: COLORS.success }} className="shrink-0" />
                  : isShaky
                    ? <RotateCcw size={18} style={{ color: CYAN }} className="shrink-0" />
                    : <Circle size={20} className="text-zinc-300 dark:text-zinc-600 shrink-0" />}
                <div className="flex-1 min-w-0">
                  <p className={`text-[15px] font-medium ${isRec ? 'text-zinc-400 dark:text-zinc-500' : 'text-zinc-800 dark:text-zinc-100'}`}>{c.topicLabel}</p>
                  {isShaky && <p className="text-[11px]" style={{ color: CYAN_DARK_TEXT }}>Marked to revisit</p>}
                </div>
                {isRec
                  ? <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: COLORS.success }}>Recovered</span>
                  : <ArrowRight size={16} className="text-zinc-300 dark:text-zinc-600 shrink-0" />}
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  // ───────────────────────── UNIT ─────────────────────────
  if (view === 'unit' && card) {
    const beatIndex = beat === 'gist' ? 0 : beat === 'move' ? 1 : 2; // check+reveal share step 3
    return (
      <div className="w-full">
        <button onClick={() => setView('queue')} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4 max-w-xl mx-auto w-full">
          <ArrowLeft size={15} /> {card.subjectLabel}
        </button>

        <AnimatePresence mode="wait">
          {beat === 'done' ? (
            <MotionDiv key="done" {...fade} className={cardShell}>
              <div className="flex flex-col items-center text-center py-2">
                <div className="w-14 h-14 rounded-full flex items-center justify-center mb-4" style={{ backgroundColor: COLORS.successTint }}>
                  <Check size={28} strokeWidth={3} style={{ color: COLORS.success }} />
                </div>
                <h3 className="text-xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Recovered — nice one</h3>
                <p className="text-[14px] mb-5" style={{ color: '#5a5550' }}>
                  <span className="font-semibold" style={{ color: COLORS.successDarkText }}>{card.topicLabel}</span> is back in your pocket.
                  That’s ≈{marksProtected} marks back in reach so far.
                </p>
                <div className="flex flex-col sm:flex-row gap-2.5 w-full sm:w-auto">
                  {nextUnrecovered() && (
                    <PrimaryActionButton label="Next topic" icon={ArrowRight} onClick={() => { const n = nextUnrecovered(); if (n) openCard(n); }} />
                  )}
                  <button onClick={() => setView('queue')} className="px-6 py-3 rounded-full text-[15px] font-semibold border-2 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300">
                    Back to topics
                  </button>
                </div>
              </div>
            </MotionDiv>
          ) : (
            <MotionDiv key={beat} {...fade} className={cardShell}>
              {/* topic + beat dots */}
              <div className="flex items-center justify-between mb-4">
                <span className="text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: CYAN_DARK_TEXT }}>{card.topicLabel}</span>
                <div className="flex items-center gap-1.5">
                  {[0, 1, 2].map(s => (
                    <span key={s} className="h-1.5 rounded-full transition-all" style={{ width: s === beatIndex ? 18 : 6, backgroundColor: s <= beatIndex ? CYAN : '#E2E0DC' }} />
                  ))}
                </div>
              </div>

              {beat === 'gist' && (
                <>
                  <p className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2" style={{ color: '#9e9186' }}>The 90-second version</p>
                  <p className="text-[16px] leading-relaxed mb-6" style={{ color: '#2a2622', fontFamily: "'DM Sans', sans-serif" }}>{card.gist}</p>
                  <div className="flex justify-end">
                    <PrimaryActionButton label="The one move" icon={ArrowRight} onClick={() => setBeat('move')} />
                  </div>
                </>
              )}

              {beat === 'move' && (
                <>
                  <div className="rounded-xl p-4 mb-6" style={{ backgroundColor: CYAN_TINT }}>
                    <div className="flex items-center gap-2 mb-1.5">
                      <Sparkles size={15} style={{ color: CYAN }} />
                      <p className="text-[11px] font-bold uppercase tracking-[0.12em]" style={{ color: CYAN_DARK_TEXT }}>The one move that matters</p>
                    </div>
                    <p className="text-[15px] font-semibold mb-1" style={{ color: '#1a1a1a', fontFamily: "'Source Serif 4', serif" }}>{card.oneMove.label}</p>
                    <p className="text-[14px] leading-relaxed" style={{ color: '#3a3530' }}>{card.oneMove.text}</p>
                  </div>
                  <div className="flex justify-between items-center">
                    <button onClick={() => setBeat('gist')} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
                    <PrimaryActionButton label="Quick check" icon={ArrowRight} onClick={() => setBeat('check')} />
                  </div>
                </>
              )}

              {beat === 'check' && (
                <>
                  <p className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2" style={{ color: '#9e9186' }}>Quick check</p>
                  <p className="text-[16px] leading-relaxed mb-5" style={{ color: '#1a1a1a', fontFamily: "'Source Serif 4', serif" }}>{card.check.prompt}</p>
                  <p className="text-[12px] mb-4" style={{ color: '#9e9186' }}>Have a go in your head (or on paper), then check yourself.</p>
                  <div className="flex justify-between items-center">
                    <button onClick={() => setBeat('move')} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700">Back</button>
                    <PrimaryActionButton label="Show a strong answer" icon={BookOpenCheck} onClick={() => setBeat('reveal')} />
                  </div>
                </>
              )}

              {beat === 'reveal' && (
                <>
                  <p className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2" style={{ color: '#9e9186' }}>A strong answer</p>
                  <p className="text-[15px] leading-relaxed mb-5" style={{ color: '#2a2622' }}>{card.check.modelAnswer}</p>

                  <p className="text-[12px] font-semibold mb-2.5" style={{ color: CYAN_DARK_TEXT }}>Tick what your answer had:</p>
                  <div className="space-y-2 mb-5">
                    {card.check.needed.map((n, i) => (
                      <button
                        key={i}
                        onClick={() => setTicks(t => t.map((v, j) => j === i ? !v : v))}
                        className="w-full flex items-start gap-2.5 text-left rounded-xl p-2.5 transition-colors"
                        style={{ backgroundColor: ticks[i] ? COLORS.successTint : '#F6F6F4' }}
                      >
                        <span className="w-5 h-5 rounded-md flex items-center justify-center shrink-0 mt-0.5" style={ticks[i] ? { backgroundColor: COLORS.success } : { border: '2px solid #d0cdc8' }}>
                          {ticks[i] && <Check size={13} strokeWidth={3} className="text-white" />}
                        </span>
                        <span className="text-[14px]" style={{ color: ticks[i] ? COLORS.successDarkText : '#3a3530' }}>{n}</span>
                      </button>
                    ))}
                  </div>

                  <p className="text-[11px] mb-3" style={{ color: '#9e9186', fontFamily: "'DM Sans', sans-serif" }}>{card.source}</p>

                  <div className="flex flex-col sm:flex-row gap-2.5">
                    <PrimaryActionButton label="Got it — recovered" icon={Check} onClick={onRecovered} />
                    <button onClick={onShaky} className="px-5 py-3 rounded-full text-[14px] font-semibold border-2 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 inline-flex items-center justify-center gap-2">
                      <RotateCcw size={15} /> Still shaky — later
                    </button>
                  </div>
                </>
              )}
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>
    );
  }

  return null;
};

export default CatchUpLane;
