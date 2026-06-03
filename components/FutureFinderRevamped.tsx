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
import React, { useMemo, useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, ArrowLeft, RotateCcw, ExternalLink, Compass, Info } from 'lucide-react';
import { COLORS } from '../design/tokens';
import { useFutureFinderRevamped } from '../hooks/useFutureFinderRevamped';
import {
  buildStudentProfile, codeFromProfile, scoreCourseFit,
  RIASEC_LETTERS, RIASEC_LABELS, WORK_VALUE_LABELS,
  type RiasecLetter, type WorkValue, type CourseFitResult,
} from './futureFinderRiasec';
import { RIASEC_ITEMS, VALUE_ITEMS, riasecItems } from './futureFinderRiasecItems';
import { CAO_COURSES, INSTITUTIONS, getCoursePageUrl, type CAOCourse } from './futureFinderData';
import { COURSE_RIASEC } from './futureFinderRiasecData';
import { type StudentSubjectProfile, getPointsForGrade, LC_SUBJECTS } from './subjectData';

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

const REACH_META: Record<string, { label: string; color: string; bg: string }> = {
  safety: { label: 'Comfortable on points', color: '#1F5F3E', bg: '#E8F2EC' },
  match: { label: 'On target', color: '#2A5F8F', bg: '#E6EEF7' },
  reach: { label: 'A stretch', color: '#8C5A12', bg: '#FBF1E0' },
  'out-of-reach': { label: 'Big points stretch', color: '#8a5a5a', bg: '#F3ECEC' },
  open: { label: 'No points race', color: '#1F5F3E', bg: '#E8F2EC' },
};
const FIT_LABEL: Record<string, string> = { best: 'Excellent fit', great: 'Strong fit', good: 'Good fit', none: '' };

const FutureFinderRevamped: React.FC<{ uid?: string; profile: StudentSubjectProfile; studentSubjects?: string[] }> = ({ uid, profile }) => {
  const { saved, isLoaded, persist, reset } = useFutureFinderRevamped(uid);
  const [phase, setPhase] = useState<'intro' | 'quiz' | 'results'>('intro');
  const [length, setLength] = useState<'full' | 'quick'>('full');
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [valueResponses, setValueResponses] = useState<Record<string, number>>({});
  const [idx, setIdx] = useState(0);

  // Re-show saved results on revisit.
  useEffect(() => {
    if (!isLoaded || !saved?.completedAt) return;
    setResponses(saved.responses ?? {});
    setValueResponses(saved.valueResponses ?? {});
    setLength(saved.length ?? 'full');
    setPhase('results');
  }, [isLoaded, saved]);

  const questions = useMemo(() => buildQuestions(length), [length]);
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

  const answer = (val: number) => {
    const q = questions[idx];
    if (q.kind === 'interest') setResponses((r) => ({ ...r, [q.id]: val }));
    else setValueResponses((r) => ({ ...r, [q.id]: val }));
    if (idx + 1 >= questions.length) {
      const next = { length, responses: q.kind === 'interest' ? { ...responses, [q.id]: val } : responses, valueResponses: q.kind === 'value' ? { ...valueResponses, [q.id]: val } : valueResponses, completedAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      persist(next);
      setPhase('results');
    } else {
      setIdx((i) => i + 1);
    }
  };

  const retake = () => { reset(); setResponses({}); setValueResponses({}); setIdx(0); setPhase('intro'); };

  if (!isLoaded) return <div className="w-full max-w-2xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;

  // ── INTRO ─────────────────────────────────────────────────────
  if (phase === 'intro') {
    return (
      <div className="w-full max-w-2xl mx-auto">
        <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 p-6 md:p-8 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]">
          <div className="flex items-center gap-2 mb-3"><Compass size={20} style={{ color: COLORS.accent }} /><p className="text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: COLORS.accentDarkText }}>Interests · RIASEC</p></div>
          <h2 className="text-2xl font-semibold mb-2" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Find courses that fit who you are</h2>
          <p className="text-[14px] leading-relaxed text-zinc-600 dark:text-zinc-300 mb-4">Rate how much you’d enjoy a series of activities. We build your interest profile (the Holland RIASEC model used by Irish guidance services), then show CAO courses ranked by how well they <span className="font-semibold">fit your interests</span> — with points kept as a separate, honest signal.</p>
          <div className="rounded-xl p-3 mb-5 flex items-start gap-2" style={{ backgroundColor: COLORS.accentTint }}>
            <Info size={15} className="mt-0.5 shrink-0" style={{ color: COLORS.accentDarkText }} />
            <p className="text-[12.5px]" style={{ color: COLORS.accentDarkText }}>A snapshot of your interests right now — not a verdict. Worth re-taking, and best used alongside your guidance counsellor.</p>
          </div>
          <p className="text-[13px] font-semibold text-zinc-700 dark:text-zinc-300 mb-2">Choose your length:</p>
          <div className="grid sm:grid-cols-2 gap-3">
            <button onClick={() => { setLength('full'); setIdx(0); setPhase('quiz'); }} className="text-left rounded-xl border-2 p-4 transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800/40" style={{ borderColor: COLORS.accent }}>
              <p className="text-[15px] font-bold text-zinc-900 dark:text-white">Full · 72 quick taps</p>
              <p className="text-[12.5px] text-zinc-500 dark:text-zinc-400 mt-0.5">~9 min · most accurate read</p>
            </button>
            <button onClick={() => { setLength('quick'); setIdx(0); setPhase('quiz'); }} className="text-left rounded-xl border-2 border-zinc-200 dark:border-zinc-700 p-4 transition-colors hover:bg-zinc-50 dark:hover:bg-zinc-800/40">
              <p className="text-[15px] font-bold text-zinc-900 dark:text-white">Quick · 42 quick taps</p>
              <p className="text-[12.5px] text-zinc-500 dark:text-zinc-400 mt-0.5">~5 min · a faster, rougher steer</p>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ── QUIZ ──────────────────────────────────────────────────────
  if (phase === 'quiz') {
    const q = questions[idx];
    const scale = q.kind === 'interest' ? SCALE_INTEREST : SCALE_VALUE;
    const prompt = q.kind === 'interest' ? 'How much would you enjoy this?' : 'How important is this to you?';
    const pct = Math.round((idx / questions.length) * 100);
    return (
      <div className="w-full max-w-2xl mx-auto">
        <div className="flex items-center gap-3 mb-4">
          <button onClick={() => (idx > 0 ? setIdx((i) => i - 1) : setPhase('intro'))} className="text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"><ArrowLeft size={18} /></button>
          <div className="flex-1 h-2 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden"><div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: COLORS.accent }} /></div>
          <span className="text-[12px] font-semibold text-zinc-400 shrink-0">{idx + 1}/{questions.length}</span>
        </div>
        <AnimatePresence mode="wait">
          <MotionDiv key={q.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }} className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 p-6 md:p-8 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-400 mb-2">{prompt}</p>
            <p className="text-[22px] leading-tight font-semibold mb-7" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{q.text}</p>
            <div className="space-y-2">
              {scale.map((label, i) => {
                const val = i + 1;
                const cur = (q.kind === 'interest' ? responses[q.id] : valueResponses[q.id]) === val;
                return (
                  <button key={val} onClick={() => answer(val)} className="w-full text-left rounded-xl border-2 px-4 py-3 text-[14px] font-medium transition-colors" style={cur ? { borderColor: COLORS.accent, backgroundColor: COLORS.accentTint, color: COLORS.accentDarkText } : { borderColor: '#E2E0DC', color: '#3a3530' }}>{label}</button>
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
  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      {/* profile read-back */}
      <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 p-6 mb-5 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]">
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

      <div className="flex items-center justify-between mb-3">
        <p className="text-[13px] font-semibold text-zinc-700 dark:text-zinc-300">Courses ranked by interest fit</p>
        <button onClick={retake} className="inline-flex items-center gap-1.5 text-[12px] font-semibold text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"><RotateCcw size={13} /> Retake</button>
      </div>

      <div className="space-y-2.5">
        {a.shown.map(({ course, fit }) => {
          const reach = REACH_META[fit.reach];
          const inst = INSTITUTIONS[course.institution] || course.institution;
          return (
            <a key={course.code} href={getCoursePageUrl(course)} target="_blank" rel="noreferrer" className="block rounded-xl border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 p-4 hover:border-zinc-300 dark:hover:border-zinc-600 transition-colors">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <p className="text-[14.5px] font-semibold text-zinc-900 dark:text-white leading-tight">{course.title}</p>
                  <p className="text-[12px] text-zinc-500 dark:text-zinc-400">{inst} · Level {course.level}{course.typicalPoints ? ` · ~${course.typicalPoints} pts` : ' · Apprenticeship/PLC'}</p>
                </div>
                <ExternalLink size={14} className="text-zinc-300 shrink-0 mt-1" />
              </div>
              <div className="flex flex-wrap items-center gap-1.5 mt-2.5">
                <span className="text-[11px] font-bold px-2 py-0.5 rounded-full" style={{ color: '#fff', backgroundColor: COLORS.accent }}>{fit.matchPct}% match · {FIT_LABEL[fit.fitBucket]}</span>
                <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full" style={{ color: reach.color, backgroundColor: reach.bg }}>{reach.label}</span>
                {course.careerPaths.slice(0, 2).map((cp) => <span key={cp} className="text-[11px] text-zinc-500 dark:text-zinc-400 px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800">{cp}</span>)}
              </div>
            </a>
          );
        })}
        {a.shown.length === 0 && <p className="text-[13px] text-zinc-500 py-6 text-center">No strong matches yet — try retaking with a few more honest answers.</p>}
      </div>

      <p className="text-[11px] text-zinc-400 mt-5 leading-relaxed">Interest fit is computed purely from your interests (Pearson correlation on the RIASEC profile, the O*NET method) and is never changed by points. The points badge is a separate, honest signal — a great-fit course that’s a stretch on points is shown as exactly that. Points move year to year; check current cutoffs.</p>
    </div>
  );
};

export default FutureFinderRevamped;
