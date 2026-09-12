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

import ToolMasthead from '../launchpad/ToolMasthead';
import SubjectPicker from '../launchpad/SubjectPicker';
import LaunchpadSelect from '../launchpad/LaunchpadSelect';
import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Check, RotateCcw, Sparkles, BookOpenCheck } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useCatchUpLane } from '../../hooks/useCatchUpLane';
import { useInnovationData } from '../../contexts/InnovationDataContext';
import { RECOVERY_CARDS, cardsForSubject, subjectsWithContent } from '../../catchUpLaneData';

import { type RecoveryCard } from '../../types/catchUpLane';
import { CURRICULUM_SPECIFICATIONS } from '../../curriculumRegistry';

import { baseName, displayName } from '../shared/subjectNames';
import Comeback from './Comeback';
import { figureUrl } from '../../utils/figureUrl';

const CYAN = '#0E9AA8';
const CYAN_TINT = '#E6F4F5';
const CYAN_DARK_TEXT = '#0A5560';

const cardShell =
  'w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7';

type View = 'home' | 'queue' | 'unit';
type Beat = 'gist' | 'move' | 'check' | 'reveal' | 'done';

// Strand (syllabus category) lookup, built from the canonical registry: the topic queue is
// grouped under these so it mirrors each subject's real LC syllabus structure
// (Biology Units, Maths Strands, Geography Core/Elective/Option units, etc.).
const STRAND_INFO = new Map<string, { name: string; order: number }>();
CURRICULUM_SPECIFICATIONS.forEach((specification) => specification.groups.forEach((group, i) => {
  STRAND_INFO.set(group.id, { name: group.title, order: i });
}));
/** topicId → strand id by dropping the last segment (the subtopic index).
 *  'biology-2-3' → 'biology-2'; 'home-economics-0-1' → 'home-economics-0'
 *  (handles hyphenated subject ids, which slicing the first 2 parts did not). */


const fade = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: { duration: 0.22 },
};

const CatchUpLane: React.FC<{ uid?: string; studentSubjects?: string[]; studentCycle?: 'junior-cycle' | 'leaving-cert' }> = ({ uid, studentSubjects, studentCycle }) => {
  const { state, isLoaded, markRecovered, markShaky, saveComeback, setFirstWeekDay, marksProtected } = useCatchUpLane(uid);
  const { topicMastery } = useInnovationData();

  // Which arm: the hub chooser, the content arm (arm 1), or the comeback arm (arm 2).
  const [topicQuery, setTopicQuery] = useState('');
  const [arm, setArm] = useState<'hub' | 'content' | 'comeback'>('content');
  const [view, setView] = useState<View>('home');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [cardId, setCardId] = useState<string | null>(null);
  const [beat, setBeat] = useState<Beat>('gist');
  const [ticks, setTicks] = useState<boolean[]>([]);
  // Higher / Ordinary filter — 'common' cards show at both levels; level-specific
  // ones (e.g. HL-only de Moivre) show only at their level.
  const [levelFilter, setLevelFilter] = useState<'higher' | 'ordinary'>('higher');
  const matchesLevel = (c: RecoveryCard) => c.level === 'common' || c.level === levelFilter;
  // Subject-picker scope: just the student's chosen subjects, or every subject in their cycle.


  const recovered = useMemo(() => new Set(state.recoveredTopicIds), [state.recoveredTopicIds]);
  const shaky = useMemo(() => new Set(state.shakyTopicIds), [state.shakyTopicIds]);

  // Subjects that have at least one card at the selected level (count = visible
  // cards), filtered to the student's own cycle — JC students see only Junior
  // Cycle subjects, LC students only Leaving Cert. (No studentCycle → show all.)
  const available = useMemo(() => subjectsWithContent()
    .filter(s => !studentCycle || s.cycle === studentCycle)
    .map(s => ({ ...s, count: cardsForSubject(s.subjectId).filter(c => c.level === 'common' || c.level === levelFilter).length }))
    .filter(s => s.count > 0), [levelFilter, studentCycle]);
  const studentSet = useMemo(
    () => new Set((studentSubjects ?? []).map(baseName)),
    [studentSubjects],
  );
  // Subjects the student takes that we don't have content for yet (honest "coming soon").


  const activeSubjectId = available.some(s => s.subjectId === subjectId) ? subjectId! : (available.find(s => studentSet.has(baseName(s.subjectLabel))) ?? available[0])?.subjectId;
  const subjectCards = activeSubjectId ? cardsForSubject(activeSubjectId).filter(matchesLevel) : [];
  const card = cardId ? RECOVERY_CARDS.find(c => c.id === cardId) ?? null : null;


  // Denominator for the "caught up so far" bar: the unique TOPICS recoverable
  // for the student's own subjects at the selected level — not RECOVERY_CARDS
  // .length (676 cards across all subjects/levels), which no student could ever
  // clear, so the bar was permanently a sliver. Falls back to every available
  // subject when we don't know the student's subjects.
  const catchUpTopicUniverse = useMemo(() => {
    const ids = new Set<string>();
    for (const a of available) {
      if (studentSet.size > 0 && !studentSet.has(baseName(a.subjectLabel))) continue;
      for (const c of cardsForSubject(a.subjectId)) {
        if (c.level === 'common' || c.level === levelFilter) ids.add(c.topicId);
      }
    }
    return ids;
  }, [available, studentSet, levelFilter]);
  const recoveredInUniverse = useMemo(
    () => state.recoveredTopicIds.filter(id => catchUpTopicUniverse.has(id)).length,
    [state.recoveredTopicIds, catchUpTopicUniverse],
  );


  // ── navigation ──

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

  // ───────────────────────── ARM 2: COMEBACK ─────────────────────────
  if (arm === 'comeback') {
    return (
      <Comeback
        saved={state.comeback}
        onSave={saveComeback}
        onExit={() => setArm('hub')}
        onGoContent={() => { setArm('content'); setView('home'); }}
        onDayUpdate={setFirstWeekDay}
      />
    );
  }

  if (view !== 'unit') {
    const filteredCards = subjectCards.filter(c => `${c.focus ?? ''} ${c.topicLabel}`.toLowerCase().includes(topicQuery.toLowerCase().trim()));
    const pickerOptions = available.map(s => ({value:s.subjectId,label:displayName(s.subjectLabel),detail:`${s.count} topics`}));
    return <div className="pb-12">
      <ToolMasthead tool="catch-up-lane" eyebrow="Pick up where you left off" title="Catch-Up Lane." subtitle="One topic. A short lesson. A quick check." />
      <div className="lp-library"><aside>
        <SubjectPicker value={activeSubjectId ?? ''} options={pickerOptions} onChange={value => {setSubjectId(value);setTopicQuery('');}} />
        <LaunchpadSelect className="w-full mt-3" aria-label="Catch-Up level" value={levelFilter} onChange={e => setLevelFilter(e.target.value as 'higher' | 'ordinary')}><option value="higher">Higher level</option><option value="ordinary">Ordinary level</option></LaunchpadSelect>
        <p className="lp-body mt-4">{recoveredInUniverse} of {catchUpTopicUniverse.size} topics caught up across your subjects.</p>
        <button className="lp-catch-comeback" onClick={() => setArm('comeback')}>{state.comeback ? 'Open your comeback plan' : 'Need a wider reset? Your comeback'} <ArrowRight size={16} /></button>
      </aside><section>
        <div className="lp-catch-heading"><h2 className="lp-title">{pickerOptions.find(s => s.value === activeSubjectId)?.label ?? 'Choose a subject'}</h2><span className="lp-body">Short lessons · Quick checks</span></div>
        <input className="lp-search mb-5" type="search" aria-label="Find the topic you missed" placeholder="Find the topic you missed" value={topicQuery} onChange={e => setTopicQuery(e.target.value)} />
        <div className="lp-lesson-grid">{filteredCards.map((c,index) => <article className="lp-lesson" key={c.id}>
          <span className="lp-eyebrow">{String(index+1).padStart(2,'0')} · {recovered.has(c.topicId) ? 'Recovered' : shaky.has(c.topicId) ? 'To revisit' : 'Short lesson'}</span><h3>{c.focus ?? c.topicLabel}</h3>
          <button onClick={() => openCard(c)}>Start lesson <span>3 min <ArrowRight size={16} /></span></button>
        </article>)}</div>
        {!filteredCards.length && <p className="lp-body py-6">{available.length ? 'No matching topics. Try a shorter search or another subject.' : 'No lessons at this level yet. Try another level.'}</p>}
      </section></div>
    </div>;
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

              {/* Figure for visually-dependent topics — the real SEC figure, shown
                  (not described), with attribution. Persists across the beats. */}
              {card.figure && (
                <figure className="mb-5 rounded-xl border-2 border-[#1A1A1A] dark:border-zinc-700 overflow-hidden bg-white">
                  <img src={figureUrl(card.figure.src)} alt={card.figure.alt} loading="lazy" className="w-full h-auto block" />
                  <figcaption className="text-[10px] px-3 py-1.5" style={{ color: CYAN_DARK_TEXT, backgroundColor: CYAN_TINT }}>{card.figure.source}</figcaption>
                </figure>
              )}

              {/* Comprehension passage — the FULL real text, shown verbatim
                  (under the SEC agreement). Not clipped: the student sees all of it. */}
              {card.passage && (
                <div className="mb-5 rounded-xl border-2 border-[#1A1A1A] dark:border-zinc-700 overflow-hidden bg-white">
                  <div className="px-4 py-3.5 text-[14px] leading-relaxed whitespace-pre-line" style={{ color: '#2a2622', fontFamily: "'Source Serif 4', serif" }}>
                    {card.passage.text}
                  </div>
                  <div className="text-[10px] px-3 py-1.5 border-t border-zinc-100 dark:border-zinc-800" style={{ color: CYAN_DARK_TEXT, backgroundColor: CYAN_TINT }}>{card.passage.source}</div>
                </div>
              )}

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
