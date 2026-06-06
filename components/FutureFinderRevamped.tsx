/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Future Finder Revamped — a RIASEC-grounded course-recommendation tool, built
 * ALONGSIDE the original Future Finder so the two can be compared before the old
 * one is retired. See docs/future-finder-redesign-plan.md.
 *
 * Flow: choose length (Full 60 / Quick 30 interest items + 12 work-values) →
 * activity-card quiz (5-point dislike→like) → student RIASEC profile → courses
 * ranked by INTEREST FIT (Pearson correlation, O*NET's method), each annotated
 * with an independent points-REACH badge. Fit is never altered by points.
 */
import React, { useMemo, useState, useEffect, useCallback, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowLeft, Compass, X, ArrowRight } from 'lucide-react';
import { COLORS } from '../design/tokens';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { useFutureFinderRevamped, type FutureFinderRevampedState } from '../hooks/useFutureFinderRevamped';
import {
  buildStudentProfile, codeFromProfile, scoreCourseFit,
  RIASEC_LETTERS, RIASEC_LABELS, WORK_VALUE_LABELS,
  type RiasecLetter, type WorkValue, type CourseFitResult,
} from './futureFinderRiasec';
import { RIASEC_ITEMS, VALUE_ITEMS, riasecItems } from './futureFinderRiasecItems';
import { CAO_COURSES, type CAOCourse } from './futureFinderData';
import { COURSE_RIASEC } from './futureFinderRiasecData';
import { type StudentSubjectProfile, getPointsForGrade, LC_SUBJECTS } from './subjectData';
import FutureFinderResults, { type DisplayResult, type SortMode } from './FutureFinderResults';
import { riasecToRecommendation } from './futureFinderRevampedAdapter';

const SCALE_INTEREST = ['Strongly dislike', 'Dislike', 'Neutral', 'Like', 'Strongly like'];
const SCALE_VALUE = ['Not important', 'A little', 'Neutral', 'Important', 'Very important'];

interface Question { id: string; kind: 'interest' | 'value'; scale?: RiasecLetter; value?: WorkValue; text: string; }

function buildQuestions(length: 'full' | 'quick'): Question[] {
  const interest: Question[] = riasecItems(length === 'quick').map((i) => ({ id: i.id, kind: 'interest', scale: i.scale, text: i.text }));
  const values: Question[] = VALUE_ITEMS.map((v) => ({ id: v.id, kind: 'value', value: v.value, text: v.text }));
  return [...interest, ...values];
}

/** Best-six CAO points from current grades (mirrors the original Future Finder). */
function computeCurrentPoints(profile: StudentSubjectProfile): number {
  return profile.subjects
    .map((s) => getPointsForGrade(s.currentGrade, LC_SUBJECTS.find((lc) => lc.name === s.subjectName)?.isMaths || false))
    .sort((a, b) => b - a)
    .slice(0, 6)
    .reduce((sum, p) => sum + p, 0);
}

const FutureFinderRevamped: React.FC<{ uid?: string; profile: StudentSubjectProfile; studentSubjects?: string[]; onOpenCareerPaths?: (careerStrings: string[]) => void }> = ({ uid, profile, onOpenCareerPaths }) => {
  const { saved, isLoaded, persist, reset } = useFutureFinderRevamped(uid);
  const [phase, setPhase] = useState<'intro' | 'quiz' | 'results'>('intro');
  const [length, setLength] = useState<'full' | 'quick'>('full');
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [valueResponses, setValueResponses] = useState<Record<string, number>>({});
  const [idx, setIdx] = useState(0);
  // Results-UI state, seeded from the persisted revamped namespace.
  const [savedPicks, setSavedPicks] = useState<string[]>([]);
  const [compareCodes, setCompareCodes] = useState<string[]>([]);
  const [sortMode, setSortMode] = useState<SortMode>('match');
  const [pointsAsc, setPointsAsc] = useState(true);
  const [regionFilter, setRegionFilter] = useState<string>('');

  // Re-show saved results on revisit.
  useEffect(() => {
    if (!isLoaded || !saved?.completedAt) return;
    setResponses(saved.responses ?? {});
    setValueResponses(saved.valueResponses ?? {});
    setLength(saved.length ?? 'full');
    setSavedPicks(saved.picks ?? []);
    setCompareCodes(saved.compareCodes ?? []);
    setPhase('results');
  }, [isLoaded, saved]);

  const questions = useMemo(() => buildQuestions(length), [length]);

  // Safety net: if the index ever runs past the last question — e.g. a tap that
  // lands during the card transition advances twice — finish the quiz instead of
  // rendering questions[idx].kind on `undefined` (which used to crash to the
  // tool error boundary right as the student completed the quiz).
  useEffect(() => {
    if (phase === 'quiz' && idx >= questions.length) setPhase('results');
  }, [phase, idx, questions.length]);
  const studentPoints = useMemo(() => computeCurrentPoints(profile), [profile]);
  const studentSubjectNames = useMemo(() => profile.subjects.map((s) => s.subjectName), [profile]);

  const analysis = useMemo(() => {
    const byScale: Partial<Record<RiasecLetter, number[]>> = {};
    for (const it of RIASEC_ITEMS) { const r = responses[it.id]; if (r) (byScale[it.scale] ??= []).push(r); }
    const studentProfile = buildStudentProfile(byScale);
    const studentCode = codeFromProfile(studentProfile);
    const valScore: Partial<Record<WorkValue, number>> = {};
    for (const v of VALUE_ITEMS) { const r = valueResponses[v.id]; if (r) valScore[v.value] = (valScore[v.value] ?? 0) + r; }
    const studentValues = (Object.entries(valScore).sort((a, b) => (b[1] as number) - (a[1] as number)).slice(0, 3).map((x) => x[0]) as WorkValue[]);
    const scored = CAO_COURSES
      .map((course) => {
        const cr = COURSE_RIASEC[course.code];
        if (!cr) return null;
        const fit = scoreCourseFit({ studentProfile, studentCode, studentPoints, studentSubjects: studentSubjectNames, studentValues, course: { ...cr, typicalPoints: course.typicalPoints } });
        return { course, fit };
      })
      .filter((x): x is { course: CAOCourse; fit: CourseFitResult } => x !== null)
      .sort((a, b) => b.fit.fitR - a.fit.fitR);
    const maxScale = Math.max(1, ...RIASEC_LETTERS.map((l) => studentProfile[l]));
    return { studentProfile, studentCode, studentValues, maxScale, shown: scored.filter((s) => s.fit.fitBucket !== 'none').slice(0, 24) };
  }, [responses, valueResponses, studentPoints, studentSubjectNames]);

  // Holds true between selecting an answer and the (brief) auto-advance, so the
  // orange selected state is actually visible and a fast double-tap can't skip
  // two questions.
  const advancingRef = useRef(false);
  const answer = (val: number) => {
    if (advancingRef.current) return;
    const q = questions[idx];
    if (!q) return;
    if (q.kind === 'interest') setResponses((r) => ({ ...r, [q.id]: val }));
    else setValueResponses((r) => ({ ...r, [q.id]: val }));
    advancingRef.current = true;
    window.setTimeout(() => {
      advancingRef.current = false;
      if (idx + 1 >= questions.length) {
        const next: FutureFinderRevampedState = { length, responses: q.kind === 'interest' ? { ...responses, [q.id]: val } : responses, valueResponses: q.kind === 'value' ? { ...valueResponses, [q.id]: val } : valueResponses, picks: savedPicks, compareCodes, completedAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
        persist(next);
        setPhase('results');
      } else {
        setIdx((i) => i + 1);
      }
    }, 280);
  };

  const retake = () => { reset(); setResponses({}); setValueResponses({}); setSavedPicks([]); setCompareCodes([]); setSortMode('match'); setPointsAsc(true); setRegionFilter(''); setIdx(0); setPhase('intro'); };

  // Full-state merge to the revamped namespace — mirrors the original's
  // toggleSavedPick/toggleCompare, but writing futureFinderRevamped.
  const persistResultsState = useCallback((picks: string[], compares: string[]) => {
    persist({
      length: saved?.length ?? length,
      responses: saved?.responses ?? responses,
      valueResponses: saved?.valueResponses ?? valueResponses,
      picks,
      compareCodes: compares,
      completedAt: saved?.completedAt ?? new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
  }, [persist, saved, length, responses, valueResponses]);

  const onToggleSave = useCallback((code: string) => {
    setSavedPicks((prev) => {
      const next = prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code];
      persistResultsState(next, compareCodes);
      return next;
    });
  }, [compareCodes, persistResultsState]);

  const onToggleCompare = useCallback((r: DisplayResult) => {
    setCompareCodes((prev) => {
      let next: string[];
      if (prev.includes(r.course.code)) next = prev.filter((c) => c !== r.course.code);
      else if (prev.length >= 3) return prev;
      else next = [...prev, r.course.code];
      persistResultsState(savedPicks, next);
      return next;
    });
  }, [savedPicks, persistResultsState]);

  const onRemoveCompare = useCallback((code: string) => {
    setCompareCodes((prev) => {
      const next = prev.filter((c) => c !== code);
      persistResultsState(savedPicks, next);
      return next;
    });
  }, [savedPicks, persistResultsState]);

  if (!isLoaded) return <div className="w-full max-w-2xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;

  // ── INTRO ─────────────────────────────────────────────────────
  if (phase === 'intro') {
    return (
      <div className="w-full max-w-md mx-auto py-6 text-center">
        <img src="/assets/tools/future-finder.png" alt="" draggable={false} className="w-44 h-44 md:w-52 md:h-52 mx-auto -mb-1 object-contain pointer-events-none select-none" />
        <div className="inline-flex items-center gap-1.5 mb-3 px-3 py-1.5 rounded-full" style={{ backgroundColor: COLORS.accentTint }}>
          <Compass size={14} style={{ color: COLORS.accent }} />
          <span className="text-[10.5px] font-bold uppercase tracking-[0.14em]" style={{ color: COLORS.accentDarkText }}>Interests · RIASEC</span>
        </div>
        <h2 className="font-serif text-[28px] md:text-[32px] font-semibold leading-[1.08] mb-3" style={{ color: '#1a1a1a' }}>Find courses that fit<br />who you are</h2>
        <p className="text-[14.5px] leading-relaxed text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto mb-6">Rate quick activities, we build your interest profile, then rank CAO courses by how well they <span className="font-semibold text-zinc-700 dark:text-zinc-200">fit you</span> — points kept separate and honest.</p>

        {/* length choice — chunky year-selector style buttons (a touch smaller) */}
        <div className="grid grid-cols-2 gap-3 max-w-sm mx-auto mb-6">
          {(['full', 'quick'] as const).map((l) => {
            const selected = length === l;
            return (
              <button
                key={l}
                onClick={() => setLength(l)}
                className={`flex flex-col items-center justify-center py-4 rounded-2xl border-2 border-[#1A1A1A] font-sans transition-all duration-150 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[5px_5px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${selected ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'}`}
              >
                <span className="text-xl font-bold leading-none">{l === 'full' ? 'Full' : 'Quick'}</span>
                <span className="text-[11px] font-medium mt-1 opacity-80">{l === 'full' ? '72 taps · ~9 min' : '42 taps · ~5 min'}</span>
              </button>
            );
          })}
        </div>

        <div className="flex justify-center">
          <PrimaryActionButton label="Start" onClick={() => { setIdx(0); setPhase('quiz'); }} icon={ArrowRight} />
        </div>

        <p className="text-[12px] text-zinc-400 italic max-w-sm mx-auto mt-7">A snapshot of your interests right now — not a verdict. Best re-taken, and used alongside your guidance counsellor.</p>
      </div>
    );
  }

  // ── QUIZ ──────────────────────────────────────────────────────
  if (phase === 'quiz') {
    const q = questions[idx];
    if (!q) return null; // overshoot guard — the effect above flips phase to results
    const scale = q.kind === 'interest' ? SCALE_INTEREST : SCALE_VALUE;
    const prompt = q.kind === 'interest' ? 'How much would you enjoy this?' : 'How important is this to you?';
    const pct = Math.round((idx / questions.length) * 100);
    return (
      <div className="w-full max-w-2xl mx-auto">
        <div className="flex items-center gap-3 mb-4">
          <button onClick={() => (idx > 0 ? setIdx((i) => i - 1) : setPhase('intro'))} className="text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"><ArrowLeft size={18} /></button>
          <div className="flex-1 h-2 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden"><div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: COLORS.accent, transition: 'width 0.45s cubic-bezier(0.22,1,0.36,1)' }} /></div>
          <span className="text-[12px] font-semibold text-zinc-400 shrink-0">{idx + 1}/{questions.length}</span>
        </div>
        <AnimatePresence mode="wait">
          <MotionDiv key={q.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }} className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6 md:p-8 shadow-sm">
            <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-400 mb-2">{prompt}</p>
            <p className="text-[22px] leading-tight font-semibold mb-7" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{q.text}</p>
            <div className="space-y-2">
              {scale.map((label, i) => {
                const val = i + 1;
                const cur = (q.kind === 'interest' ? responses[q.id] : valueResponses[q.id]) === val;
                return (
                  <button key={val} onClick={() => answer(val)} className="w-full text-left rounded-xl border-2 px-4 py-3 text-[14px] font-medium transition-colors" style={cur ? { borderColor: COLORS.accent, backgroundColor: COLORS.accent, color: '#fff' } : { borderColor: '#E2E0DC', color: '#3a3530' }}>{label}</button>
                );
              })}
            </div>
          </MotionDiv>
        </AnimatePresence>
      </div>
    );
  }

  // ── RESULTS ───────────────────────────────────────────────────
  const a = analysis;
  const topTypes = [...RIASEC_LETTERS].sort((x, y) => a.studentProfile[y] - a.studentProfile[x]).slice(0, 3).filter((l) => a.studentProfile[l] > 0);

  // Map the RIASEC-scored courses into the shared results UI's shape, then
  // apply the SAME sort/region filtering the original Future Finder does
  // (FutureFinder.tsx displayResults memo): top 30 → region → sort → top 10.
  const allResults: DisplayResult[] = a.shown.map(({ course, fit }) =>
    riasecToRecommendation(course, fit, topTypes, a.studentValues));
  let displayResults = allResults.slice(0, 30);
  if (regionFilter) displayResults = displayResults.filter((r) => r.course.region === regionFilter);
  if (sortMode === 'points') displayResults = [...displayResults].sort((x, y) => pointsAsc ? x.course.typicalPoints - y.course.typicalPoints : y.course.typicalPoints - x.course.typicalPoints);
  displayResults = displayResults.slice(0, 10);
  const compareCourses = compareCodes
    .map((code) => allResults.find((r) => r.course.code === code))
    .filter((r): r is DisplayResult => !!r);

  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      {/* profile read-back */}
      <div className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6 mb-5 shadow-sm">
        <p className="text-[11px] font-bold uppercase tracking-[0.14em] mb-1" style={{ color: COLORS.accentDarkText }}>Your interest profile</p>
        <h2 className="text-xl font-semibold mb-3" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>You lean {topTypes.map((l, i) => <span key={l}>{i > 0 ? (i === topTypes.length - 1 ? ' & ' : ', ') : ''}<span style={{ color: COLORS.accent }}>{RIASEC_LABELS[l]}</span></span>)}</h2>
        <div className="flex items-end gap-2 h-20 mb-2">
          {RIASEC_LETTERS.map((l) => (
            <div key={l} className="flex-1 flex flex-col items-center justify-end h-full">
              <div className="w-full rounded-t-md" style={{ height: `${Math.max(6, (a.studentProfile[l] / a.maxScale) * 100)}%`, backgroundColor: topTypes.includes(l) ? COLORS.accent : '#D8D4CE' }} />
              <span className="text-[10px] font-bold text-zinc-400 mt-1">{l}</span>
            </div>
          ))}
        </div>
        {a.studentValues.length > 0 && <p className="text-[12px] text-zinc-500 dark:text-zinc-400">You value: {a.studentValues.map((v) => WORK_VALUE_LABELS[v]).join(' · ')}</p>}
        <p className="text-[11.5px] text-zinc-400 mt-2 italic">A snapshot, not a verdict — these are directions worth exploring.</p>
      </div>

      <FutureFinderResults
        results={displayResults}
        autoPoints={studentPoints}
        sortMode={sortMode}
        onSortChange={setSortMode}
        pointsAsc={pointsAsc}
        onPointsDirToggle={() => setPointsAsc((v) => !v)}
        regionFilter={regionFilter}
        onRegionFilterChange={setRegionFilter}
        onOpenCareerPaths={onOpenCareerPaths}
        savedPicks={savedPicks}
        compareCourses={compareCourses}
        onToggleSave={onToggleSave}
        onToggleCompare={onToggleCompare}
        onRemoveCompare={onRemoveCompare}
        onRetake={retake}
        explainer={RiasecExplainerModal}
        scoreBreakdownLabels={{ interest: 'Interest fit', values: 'Values fit', feasibility: 'Points reach' }}
      />

      <p className="text-[11px] text-zinc-400 mt-5 leading-relaxed">Interest fit is computed purely from your interests (Pearson correlation on the RIASEC profile, the O*NET method) and is never changed by points. The points badge is a separate, honest signal — a great-fit course that’s a stretch on points is shown as exactly that. Points move year to year; check current cutoffs.</p>
    </div>
  );
};

export default FutureFinderRevamped;

// ── RIASEC scoring explainer modal ─────────────────────────────────────────
// Replaces the original tool's ScoringExplainerModal when opened from the
// shared results UI's "How this works". Explains the RIASEC/Pearson interest-
// fit method (O*NET), what the three score bars mean, and why points-reach is
// kept as a SEPARATE axis that never lowers a course's interest match.
function RiasecExplainerModal({ onClose }: { onClose: () => void }) {
  // Portalled to document.body so the modal escapes the results' Framer
  // transform context (otherwise `position: fixed` anchors to the transformed
  // ancestor and the modal spills off-screen).
  return createPortal(
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[200] flex items-center justify-center bg-black/55 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <MotionDiv
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 12 }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] as number[] }}
        className="bg-[#FAFBF6] dark:bg-zinc-900 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[6px_6px_0_0_#1A1A1A] dark:shadow-[6px_6px_0_0_#3f3f46] max-w-xl w-full max-h-[90vh] flex flex-col overflow-hidden"
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        {/* Header (fixed) */}
        <div className="flex items-start justify-between p-6 pb-4 shrink-0">
          <div className="flex items-start gap-3 min-w-0">
            <div className="w-11 h-11 rounded-xl flex items-center justify-center bg-[rgba(242,107,31,0.12)] shrink-0">
              <Compass size={20} className="text-[#F26B1F]" />
            </div>
            <div className="min-w-0">
              <h2 className="font-serif text-xl font-bold text-[#1A1A1A] dark:text-white">How your matches are calculated</h2>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">Interest fit, the RIASEC way</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0"
            aria-label="Close"
          >
            <X size={18} className="text-zinc-500" />
          </button>
        </div>

        {/* Body (scrolls when content exceeds the viewport-capped modal) */}
        <div className="px-6 pb-6 space-y-5 overflow-y-auto flex-1 min-h-0">
          {/* Interest fit */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">The match percentage</p>
            <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
              <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed mb-2">
                Your answers build a six-part interest profile using the <span className="font-bold">Holland RIASEC model</span> (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) — the same framework Irish guidance services use.
              </p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                Each course has its own RIASEC profile. The match % compares the <span className="font-bold">shape</span> of your profile against the course's (a Pearson correlation — O*NET's method), so it rewards courses that lean the same way you do, not just ones with high scores everywhere.
              </p>
            </div>
          </section>

          {/* The three bars */}
          <section>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2">The three bars</p>
            <div className="space-y-2.5">
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <p className="text-sm font-bold text-[#1A1A1A] dark:text-white mb-1">Interest fit</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">How closely the course's interest profile matches yours.</p>
              </div>
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <p className="text-sm font-bold text-[#1A1A1A] dark:text-white mb-1">Values fit</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">Whether the things you said matter to you in work (achievement, independence, helping people, and so on) line up with the field.</p>
              </div>
              <div className="rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 p-3">
                <p className="text-sm font-bold text-[#1A1A1A] dark:text-white mb-1">Points reach</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">How comfortable the course's typical points are given your current grades — a separate signal, shown so you can see it honestly.</p>
              </div>
            </div>
          </section>

          {/* Points stay separate */}
          <section className="rounded-xl p-3" style={{ backgroundColor: 'rgba(242,107,31,0.10)' }}>
            <p className="text-xs text-[#8C3A0E] dark:text-[#FDEEDF] leading-relaxed">
              <span className="font-bold">Points never lower your interest match.</span> Reach is kept as its own axis, so a course that fits you perfectly but is a points stretch is shown as exactly that — a great fit that's a stretch — rather than being quietly demoted.
            </p>
          </section>

          {/* Snapshot, not a verdict */}
          <section>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed italic">
              This is a snapshot of your interests right now, not a verdict. It's worth re-taking, and it's best used alongside your guidance counsellor. Points move year to year — always check current cutoffs.
            </p>
          </section>
        </div>

        {/* Footer CTA (fixed below the scrolling body) */}
        <div className="px-6 pb-6 pt-2 shrink-0 border-t border-black/[0.04] dark:border-white/[0.06]">
          <button
            onClick={onClose}
            className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] transition-all duration-150"
          >
            Got it
          </button>
        </div>
      </MotionDiv>
    </MotionDiv>,
    document.body
  );
}
