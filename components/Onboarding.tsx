/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useLayoutEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, ArrowLeft, Check, Calendar, CalendarOff } from 'lucide-react';
import PrimaryActionButton from './ui/PrimaryActionButton';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  type YearGroup, type JCBand, type JCSubject,
  LC_SUBJECTS, JC_SUBJECTS, LCA_SUBJECTS, JC_BANDS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
  getGradeIndex, DAYS_OF_WEEK,
  type LCSubject,
} from './subjectData';
import { type NorthStar } from '../types';
import { type CurriculumLevel, isLcaYear, yearGroupToCurriculumLevel } from '../utils/authUtils';
import { getDefaultExamDate } from '../utils/examDates';
import NorthStarOnboarding from './NorthStarOnboarding';
import { COLORS } from '../design/tokens';
import { trackFunnel } from '../utils/funnel';

interface OnboardingProps {
  userId: string;
  userName: string;
  onComplete: (profile: StudentSubjectProfile, northStar?: NorthStar, essentialsMode?: boolean) => void | Promise<void>;
  onSkip: () => void;
  /** Phase 8: switches the flow into JC→senior re-onboarding mode. Skips
   *  the welcome/year/mode/rest-days/exam-date/summary steps and runs
   *  Subjects → Grades → North Star (5 → 6 → 4) in that order, starting
   *  from a known yearGroup='5th' or 'TY' and curriculumLevel='senior'
   *  (set by handleConfirmJCtoSenior before this component renders). */
  mode?: 'fresh' | 'transition-to-senior';
  /** When mode='transition-to-senior', this is the year picked in the
   *  TY-or-5th sub-modal — passed in so the rest of onboarding renders
   *  with the right curriculum already set without needing the year-picker
   *  step. */
  transitionTargetYear?: 'TY' | '5th';
}

type Step = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
const TOTAL_STEPS = 10; // Legacy screen ids; the visible journey uses a dynamic route.

interface OnboardingDraft {
  version: 1;
  step: Step;
  selectedSubjects: string[];
  subjectConfigs: Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }>;
  subjectBands: Record<string, { level: Level; currentBand: JCBand; targetBand: JCBand }>;
  examDate: string;
  yearGroup: YearGroup | null;
  essentialsMode: boolean;
  northStarData: NorthStar | null;
  restDays: string[];
}

// ─── The Guide — a painted blob that asks each step's question in a
//     hand-drawn speech bubble. One guide, one question, per screen (the
//     Duolingo/Brilliant conversational register, in our own language). ───
const GUIDE_BLOB = 'M 38 4 Q 12 6 6 28 Q 2 50 22 56 Q 50 62 60 36 Q 64 12 48 4 Q 42 2 38 4 Z';
const OnboardingGuide: React.FC<{ tint: string; ink: string; question: React.ReactNode; sub?: React.ReactNode; tilt?: number }> = ({ tint, ink, question, sub, tilt = 0 }) => (
  <div className="mx-auto mb-7 flex w-full max-w-xl items-start gap-3.5 text-left">
    <motion.span
      aria-hidden="true"
      initial={{ scale: 0.6, opacity: 0, rotate: tilt - 10 }}
      animate={{ scale: 1, opacity: 1, rotate: tilt }}
      transition={{ duration: 0.45, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
      className="relative mt-1 h-14 w-14 shrink-0"
    >
      <svg viewBox="0 0 64 64" className="absolute inset-0 h-full w-full">
        <path d={GUIDE_BLOB} fill={tint} />
        <path d={GUIDE_BLOB} fill="none" stroke={ink} strokeOpacity="0.3" strokeWidth="1.5" />
        <circle cx="26.5" cy="28" r="2.6" fill="#1A1A1A" />
        <circle cx="38.5" cy="28" r="2.6" fill="#1A1A1A" />
        <path d="M 27.5 37.5 Q 32.5 41.5 37.5 37.5" fill="none" stroke="#1A1A1A" strokeWidth="2" strokeLinecap="round" />
      </svg>
    </motion.span>
    <motion.div
      initial={{ opacity: 0, scale: 0.92, x: -6 }}
      animate={{ opacity: 1, scale: 1, x: 0 }}
      transition={{ duration: 0.4, delay: 0.16, ease: [0.16, 1, 0.3, 1] }}
      className="relative min-w-0 flex-1 rounded-2xl border-2 border-[#1A1A1A] bg-white px-5 py-4 shadow-[3px_3px_0_0_#1A1A1A] dark:border-zinc-200 dark:bg-zinc-900"
      style={{ transformOrigin: 'left center' }}
    >
      <span aria-hidden="true" className="absolute -left-[8px] top-6 h-3.5 w-3.5 rotate-45 border-b-2 border-l-2 border-[#1A1A1A] bg-white dark:border-zinc-200 dark:bg-zinc-900" />
      <p className="font-serif text-[21px] font-bold leading-snug text-[#1A1A1A] dark:text-white">{question}</p>
      {sub && <p className="mt-1 text-[13px] leading-relaxed text-[#78716C] dark:text-zinc-400">{sub}</p>}
    </motion.div>
  </div>
);

const onboardingDraftKey = (userId: string, mode: string) => `nextstepuni:onboarding-draft:v1:${userId}:${mode}`;

function writeOnboardingDraft(userId: string, mode: string, draft: OnboardingDraft): void {
  try { localStorage.setItem(onboardingDraftKey(userId, mode), JSON.stringify(draft)); } catch { /* storage may be unavailable */ }
}

function readOnboardingDraft(userId: string, mode: string): OnboardingDraft | null {
  try {
    const raw = localStorage.getItem(onboardingDraftKey(userId, mode));
    if (!raw) return null;
    const draft = JSON.parse(raw) as Partial<OnboardingDraft>;
    if (draft.version !== 1 || typeof draft.step !== 'number' || draft.step < 1 || draft.step > TOTAL_STEPS) return null;
    return draft as OnboardingDraft;
  } catch {
    return null;
  }
}

// ─── Step-specific ambient blob colors ──────────────────────────────────────

const _STEP_BLOBS: Record<Step, { a: string; b: string; c: string }> = {
  1: { a: 'bg-[rgba(var(--accent),0.07)]', b: 'bg-yellow-300/[0.09]', c: 'bg-orange-200/[0.08]' },
  2: { a: 'bg-indigo-300/[0.08]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-sky-200/[0.06]' },
  3: { a: 'bg-[#F26B1F]/[0.08]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-emerald-200/[0.06]' },
  4: { a: 'bg-purple-300/[0.08]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-amber-200/[0.06]' },
  5: { a: 'bg-blue-300/[0.08]', b: 'bg-emerald-300/[0.07]', c: 'bg-purple-200/[0.06]' },
  6: { a: 'bg-emerald-300/[0.08]', b: 'bg-amber-300/[0.07]', c: 'bg-blue-200/[0.06]' },
  7: { a: 'bg-amber-300/[0.09]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-yellow-200/[0.08]' },
  8: { a: 'bg-rose-300/[0.08]', b: 'bg-orange-200/[0.07]', c: 'bg-pink-200/[0.06]' },
  9: { a: 'bg-emerald-300/[0.09]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-amber-200/[0.06]' },
  10: { a: 'bg-rose-300/[0.08]', b: 'bg-indigo-300/[0.07]', c: 'bg-emerald-200/[0.06]' },
};

// ─── Subject Color Map (literal Tailwind strings for CDN) ───────────────────

const GROUP_COLORS: Record<LCSubject['group'], { bg: string; border: string; text: string; selectedBg: string; selectedBorder: string }> = {
  languages: { bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300', selectedBg: 'bg-blue-100 dark:bg-blue-900/40', selectedBorder: 'border-blue-400 dark:border-blue-500' },
  stem: { bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300', selectedBg: 'bg-emerald-100 dark:bg-emerald-900/40', selectedBorder: 'border-emerald-400 dark:border-emerald-500' },
  business: { bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300', selectedBg: 'bg-amber-100 dark:bg-amber-900/40', selectedBorder: 'border-amber-400 dark:border-amber-500' },
  humanities: { bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300', selectedBg: 'bg-purple-100 dark:bg-purple-900/40', selectedBorder: 'border-purple-400 dark:border-purple-500' },
  practical: { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300', selectedBg: 'bg-orange-100 dark:bg-orange-900/40', selectedBorder: 'border-orange-400 dark:border-orange-500' },
  creative: { bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300', selectedBg: 'bg-rose-100 dark:bg-rose-900/40', selectedBorder: 'border-rose-400 dark:border-rose-500' },
};

// Solid hex per subject group — used for the small colour dot on each
// subject card on Step 5 (Select Your Subjects). Practical is shifted off
// the primary brand orange (#F26B1F) so the dot reads distinctly against
// the selected-state orange background.
const GROUP_DOT_HEX: Record<LCSubject['group'], string> = {
  languages: '#3B82F6',
  stem: '#10B981',
  business: '#F59E0B',
  humanities: '#A855F7',
  practical: '#FB923C',
  creative: '#F43F5E',
};

// ─── Grade pill color helpers (literal Tailwind for CDN) ────────────────────
//
// Chunky-shadow language matching the rest of onboarding (year + subject
// pickers). Selected current grade fills black; selected target grade fills
// orange. Unselected pills stay cream with the same black border + smaller
// drop shadow so the row still has weight. Press animation translates +
// drops the shadow on active, identical to the year picker.

const PILL_BASE = 'border-2 border-[#1A1A1A] font-bold font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 shadow-[2px_2px_0_0_#1A1A1A] hover:shadow-[3px_3px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A]';

function getCurrentGradePillClass(isSelected: boolean): string {
  return isSelected
    ? `${PILL_BASE} bg-[#1A1A1A] text-[#FDF8F0]`
    : `${PILL_BASE} bg-[#FDF8F0] text-[#1A1A1A]`;
}

function getTargetGradePillClass(isSelected: boolean): string {
  return isSelected
    ? `${PILL_BASE} bg-[#F26B1F] text-[#FDF8F0]`
    : `${PILL_BASE} bg-[#FDF8F0] text-[#1A1A1A]`;
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function getDaysUntil(dateStr: string): number {
  const target = new Date(dateStr);
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  target.setHours(0, 0, 0, 0);
  return Math.ceil((target.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

const DAY_SHORTS: Record<string, string> = {
  Monday: 'Mon', Tuesday: 'Tue', Wednesday: 'Wed', Thursday: 'Thu',
  Friday: 'Fri', Saturday: 'Sat', Sunday: 'Sun',
};

// ─── Feature preview chips for welcome step ─────────────────────────────────
//
// Hand-drawn PNG icons sit on a soft pastel blob, matching the vision-board
// styling from NorthStarOnboarding (CategoryIconBlob). Blob paths borrowed
// from CATEGORY_BLOBS so the visual language stays consistent — four
// distinct pastel tones, one per preview chip.

interface PreviewChipConfig {
  label: string;
  iconPath: string;
  blob: string;
  blobPath: string;
}

const PREVIEW_CHIPS: PreviewChipConfig[] = [
  {
    label: 'Your North Star',
    iconPath: '/icons/onboarding/north-star.png',
    blob: '#DDC9A4',
    blobPath: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
  },
  {
    label: 'Your Subjects',
    iconPath: '/icons/onboarding/subjects.png',
    blob: '#BCCCE3',
    blobPath: 'M 6 22 Q -2 50 10 78 Q 26 98 56 94 Q 90 88 96 56 Q 100 24 80 6 Q 56 -6 28 6 Q 10 14 6 22 Z',
  },
  {
    label: 'Grade Targets',
    iconPath: '/icons/onboarding/grade-targets.png',
    blob: '#F5C7A0',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
  },
  {
    label: 'Exam Countdown',
    iconPath: '/icons/onboarding/countdown.png',
    blob: '#B5D4CC',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
  },
];

// Inline icon-on-blob renderer for the preview chips. Mirrors the
// CategoryIconBlob component from NorthStarOnboarding.
const PreviewChipIcon: React.FC<{ config: PreviewChipConfig; size: number }> = ({ config, size }) => (
  // overflow visible so the oversized icon can poke past the blob bounds
  // without being clipped.
  <div className="relative shrink-0" style={{ width: size, height: size, overflow: 'visible' }} aria-hidden>
    <svg
      className="absolute pointer-events-none"
      viewBox="0 0 100 100"
      preserveAspectRatio="xMidYMid meet"
      style={{ width: '100%', height: '100%', left: 0, top: 0, zIndex: 0 }}
    >
      <path d={config.blobPath} fill={config.blob} opacity="0.85" />
    </svg>
    <img
      src={config.iconPath}
      alt=""
      style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        // Oversize the icon relative to the blob so it pokes past the
        // edges, mirroring the vision-board chip styling.
        width: '115%',
        height: '115%',
        objectFit: 'contain',
        zIndex: 1,
      }}
    />
  </div>
);

// ─── Animated number counter ────────────────────────────────────────────────

const AnimatedNumber: React.FC<{ value: number; prefix?: string; className?: string; delay?: number }> = ({ value, prefix = '', className = '', delay = 0 }) => {
  const [display, setDisplay] = useState(0);
  const rafRef = useRef(0);

  useEffect(() => {
    const start = performance.now() + delay * 1000;
    const duration = 1200;
    const from = 0;
    const to = value;

    const tick = (now: number) => {
      const elapsed = now - start;
      if (elapsed < 0) { rafRef.current = requestAnimationFrame(tick); return; }
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(from + (to - from) * eased));
      if (progress < 1) rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [value, delay]);

  return <span className={className}>{prefix}{display}</span>;
};

// ─── Component ──────────────────────────────────────────────────────────────

const Onboarding: React.FC<OnboardingProps> = ({ userId, userName, onComplete, onSkip, mode = 'fresh', transitionTargetYear }) => {
  const isTransition = mode === 'transition-to-senior';
  const draft = useMemo(() => readOnboardingDraft(userId, mode), [userId, mode]);
  // In transition mode, we skip the welcome/year/mode steps and start
  // at Step 5 (Subjects). The target year is pre-set from the modal
  // pick, so the year picker never renders.
  const [step, setStep] = useState<Step>(draft?.step ?? (isTransition ? 5 : 1));
  const [direction, setDirection] = useState(1);
  const scrollRegionRef = useRef<HTMLDivElement>(null);
  const latestDraftRef = useRef<OnboardingDraft | null>(null);

  // Subject selection
  const [selectedSubjects, setSelectedSubjects] = useState<Set<string>>(() => new Set(draft?.selectedSubjects ?? []));

  // Grade configs (LC: Grade + Higher/Ordinary level)
  const [subjectConfigs, setSubjectConfigs] = useState<Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }>>(draft?.subjectConfigs ?? {});

  // JC band configs (parallel state for junior students: JCBand + level
  // which is 'higher' / 'ordinary' for the 3 jcHasLevelChoice subjects,
  // 'common' for all others). Phase 4 plumbing.
  const [subjectBands, setSubjectBands] = useState<Record<string, { level: Level; currentBand: JCBand; targetBand: JCBand }>>(draft?.subjectBands ?? {});

  const [examDate, setExamDate] = useState(draft?.examDate ?? getDefaultExamDate());

  // Year group. In transition mode we initialise from the prop (TY or
  // 5th) — the user has already picked in the YearTransitionFlow modal,
  // so the year picker step doesn't render and the value is fixed.
  const [yearGroup, setYearGroup] = useState<YearGroup | null>(
    draft?.yearGroup ?? (isTransition ? (transitionTargetYear ?? '5th') : null)
  );

  // Module mode
  const [essentialsMode, setEssentialsMode] = useState<boolean>(draft?.essentialsMode ?? false);

  // North Star
  const [northStarData, setNorthStarData] = useState<NorthStar | null>(draft?.northStarData ?? null);

  // Rest days
  const [restDays, setRestDays] = useState<Set<string>>(() => new Set(draft?.restDays ?? []));

  // iOS can reload or evict a Capacitor WebView with little warning. Persist in
  // a layout effect so a newly selected step is written before the next frame,
  // rather than waiting for a normal effect after the transition has painted.
  useLayoutEffect(() => {
    const next: OnboardingDraft = {
      version: 1, step, selectedSubjects: Array.from(selectedSubjects),
      subjectConfigs, subjectBands, examDate, yearGroup, essentialsMode,
      northStarData, restDays: Array.from(restDays),
    };
    latestDraftRef.current = next;
    writeOnboardingDraft(userId, mode, next);
  }, [userId, mode, step, selectedSubjects, subjectConfigs, subjectBands, examDate, yearGroup, essentialsMode, northStarData, restDays]);

  // Preserve the latest synchronous snapshot when iOS backgrounds or evicts
  // the WebView. pagehide covers reload/navigation; visibilitychange covers an
  // app moving to the background before iOS has decided whether to retain it.
  useEffect(() => {
    const persistLatestDraft = () => {
      if (latestDraftRef.current) writeOnboardingDraft(userId, mode, latestDraftRef.current);
    };
    const persistWhenHidden = () => {
      if (document.visibilityState === 'hidden') persistLatestDraft();
    };
    window.addEventListener('pagehide', persistLatestDraft);
    document.addEventListener('visibilitychange', persistWhenHidden);
    return () => {
      window.removeEventListener('pagehide', persistLatestDraft);
      document.removeEventListener('visibilitychange', persistWhenHidden);
    };
  }, [userId, mode]);

  // Every stage is a new screen. Carrying the previous stage's scroll offset
  // into the next one made the content appear to open halfway down the page.
  useLayoutEffect(() => {
    if (scrollRegionRef.current) scrollRegionRef.current.scrollTop = 0;
  }, [step]);

  // Keep a vertical gesture inside the onboarding scroller. At its top or
  // bottom, absorb only the outward part of a predominantly vertical drag so
  // it cannot become browser/WebView pull-to-refresh; normal scrolling and
  // horizontal controls remain untouched.
  useEffect(() => {
    const scrollRegion = scrollRegionRef.current;
    if (!scrollRegion) return;

    let touchStartX = 0;
    let touchStartY = 0;
    const onTouchStart = (event: TouchEvent) => {
      const touch = event.touches[0];
      if (!touch) return;
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
    };
    const onTouchMove = (event: TouchEvent) => {
      const touch = event.touches[0];
      if (!touch) return;
      const deltaX = touch.clientX - touchStartX;
      const deltaY = touch.clientY - touchStartY;
      if (Math.abs(deltaY) <= Math.abs(deltaX)) return;

      const atTop = scrollRegion.scrollTop <= 0;
      const atBottom = Math.ceil(scrollRegion.scrollTop + scrollRegion.clientHeight) >= scrollRegion.scrollHeight;
      if ((atTop && deltaY > 0) || (atBottom && deltaY < 0)) event.preventDefault();
    };

    scrollRegion.addEventListener('touchstart', onTouchStart, { passive: true });
    scrollRegion.addEventListener('touchmove', onTouchMove, { passive: false });
    return () => {
      scrollRegion.removeEventListener('touchstart', onTouchStart);
      scrollRegion.removeEventListener('touchmove', onTouchMove);
    };
  }, []);

  // First-run funnel. "Reached" rather than "completed" for the mid-steps: the
  // JC flow skips some of them, so how FAR a student got is the honest and
  // useful measure of where the flow loses people. trackFunnel dedupes per
  // session, so stepping back and forward cannot inflate a count.
  useEffect(() => { trackFunnel('onboarding_started'); }, []);
  useEffect(() => {
    if (step >= 5) trackFunnel('onboarding_reached_subjects');
    if (step >= 7) trackFunnel('onboarding_reached_exam_date');
  }, [step]);

  const completeOnboarding = async (northStar?: NorthStar) => {
    trackFunnel('onboarding_completed');
    await onComplete(buildProfile(), northStar, essentialsMode);
    try { localStorage.removeItem(onboardingDraftKey(userId, mode)); } catch { /* storage may be unavailable */ }
  };

  const skipOnboarding = () => {
    trackFunnel('onboarding_skipped');
    try { localStorage.removeItem(onboardingDraftKey(userId, mode)); } catch { /* storage may be unavailable */ }
    onSkip();
  };

  // ─── Curriculum-level-derived helpers (Phase 1 JC plumbing) ───────────
  //
  // Steps 4 (North Star), 6 (grade config), and 7 (exam date for 1st/2nd
  // JC) are skipped for junior students in Phase 1. JC content for those
  // steps lands in Phases 4/5. Senior flow is unchanged.

  const curriculumLevel: CurriculumLevel | null = yearGroup
    ? yearGroupToCurriculumLevel(yearGroup)
    : null;
  // LCA maps to 'senior' for curriculum gating, but drives its own subject
  // list and skips the H/O grade-config step (LCA is credit-based, common level).
  const isLca = isLcaYear(yearGroup ?? undefined);

  const activeSteps: Step[] = isTransition
    ? [5, 6, 4]
    : isLca
      ? [1, 2, 4, 5, 7, 9]
      : [1, 2, 4, 5, 6, 7, 9];
  const currentStageIndex = Math.max(0, activeSteps.indexOf(step));
  const currentStage = currentStageIndex + 1;
  const totalStages = activeSteps.length;
  const needsExamDate = !(curriculumLevel === 'junior' && (yearGroup === '1st' || yearGroup === '2nd'));

  const shouldSkipStep = (s: Step): boolean => {
    // Phase 8: transition-to-senior mode only runs Subjects (5), Grades
    // (6), and North Star (4). Skip every other step so the linear step
    // walker advances cleanly even though we route 5 → 6 → 4 manually
    // via the goNext override below.
    return !activeSteps.includes(s);
  };

  // ─── Navigation ─────────────────────────────────────────────────────────

  // Transition mode hops 5 → 6 → 4 → complete (NS is the emotional
  // anchor for the new chapter and lands last). After step 4 the
  // "Start Senior Cycle" button calls onComplete directly.
  const transitionGoNext = () => {
    setDirection(1);
    setStep(s => {
      if (s === 5) return 6;
      if (s === 6) return 4;
      // s === 4 (NS) handled by the dedicated Finish button — never
      // reached via this function in practice.
      return s;
    });
  };

  const goNext = () => {
    if (isTransition) {
      transitionGoNext();
      return;
    }
    setDirection(1);
    setStep(s => {
      let next = Math.min(TOTAL_STEPS, s + 1) as Step;
      while (next < TOTAL_STEPS && shouldSkipStep(next)) {
        next = (next + 1) as Step;
      }
      return next;
    });
  };
  const goBack = () => {
    setDirection(-1);
    setStep(s => {
      let prev = Math.max(1, s - 1) as Step;
      while (prev > 1 && shouldSkipStep(prev)) {
        prev = (prev - 1) as Step;
      }
      return prev;
    });
  };

  // ─── Subject toggle ─────────────────────────────────────────────────────

  const toggleSubject = (name: string) => {
    setSelectedSubjects(prev => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
        // Seed both LC config and JC band defaults — only the one matching
        // the user's curriculumLevel actually gets surfaced in Step 6.
        if (!subjectConfigs[name]) {
          setSubjectConfigs(prev => ({
            ...prev,
            [name]: { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade },
          }));
        }
        if (!subjectBands[name]) {
          const jc = JC_SUBJECTS.find(s => s.name === name);
          const defaultLevel: Level = jc?.jcHasLevelChoice ? 'higher' : 'common';
          setSubjectBands(prev => ({
            ...prev,
            [name]: { level: defaultLevel, currentBand: 'Merit', targetBand: 'Higher Merit' },
          }));
        }
      }
      return next;
    });
  };

  // ─── JC band config update ──────────────────────────────────────────────

  const updateBand = (subjectName: string, field: 'level' | 'currentBand' | 'targetBand', value: string) => {
    setSubjectBands(prev => {
      const current = prev[subjectName] || { level: 'common' as Level, currentBand: 'Merit' as JCBand, targetBand: 'Higher Merit' as JCBand };
      const next = { ...current };
      if (field === 'level') {
        next.level = value as Level;
      } else if (field === 'currentBand') {
        next.currentBand = value as JCBand;
        // Target should be at least as good as current (lower index = better band)
        if (JC_BANDS.indexOf(next.targetBand) > JC_BANDS.indexOf(next.currentBand)) {
          next.targetBand = next.currentBand;
        }
      } else {
        next.targetBand = value as JCBand;
      }
      return { ...prev, [subjectName]: next };
    });
  };

  // ─── Grade config update ────────────────────────────────────────────────

  const updateConfig = (subjectName: string, field: 'level' | 'currentGrade' | 'targetGrade', value: string) => {
    setSubjectConfigs(prev => {
      const current = prev[subjectName] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
      const next = { ...current };

      if (field === 'level') {
        const newLevel = value as Level;
        next.level = newLevel;
        const grades = getGradesForLevel(newLevel);
        next.currentGrade = grades[3];
        next.targetGrade = grades[1];
      } else if (field === 'currentGrade') {
        next.currentGrade = value as Grade;
        if (getGradeIndex(next.targetGrade) > getGradeIndex(next.currentGrade)) {
          next.targetGrade = next.currentGrade;
        }
      } else {
        next.targetGrade = value as Grade;
      }

      return { ...prev, [subjectName]: next };
    });
  };

  // ─── Rest day toggle ────────────────────────────────────────────────────

  const toggleRestDay = (day: string) => {
    setRestDays(prev => {
      const next = new Set(prev);
      if (next.has(day)) next.delete(day); else next.add(day);
      return next;
    });
  };

  // ─── Build final profile ────────────────────────────────────────────────

  const buildProfile = (): StudentSubjectProfile => {
    const finalYearGroup = yearGroup ?? '6th';
    const level = yearGroupToCurriculumLevel(finalYearGroup);

    const subjects: StudentSubject[] = Array.from(selectedSubjects).map(name => {
      if (level === 'junior') {
        const band = subjectBands[name] || { level: 'common' as Level, currentBand: 'Merit' as JCBand, targetBand: 'Higher Merit' as JCBand };
        return { subjectName: name, level: band.level, currentBand: band.currentBand, targetBand: band.targetBand };
      }
      if (isLcaYear(finalYearGroup)) {
        // LCA courses are common level and credit-based — no H/O grades.
        return { subjectName: name, level: 'common' as Level };
      }
      const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
      return { subjectName: name, level: config.level, currentGrade: config.currentGrade, targetGrade: config.targetGrade };
    });
    const now = new Date().toISOString();
    return {
      subjects,
      examStartDate: examDate,
      restDays: Array.from(restDays),
      yearGroup: finalYearGroup,
      curriculumLevel: level,
      createdAt: now,
      updatedAt: now,
    };
  };

  // ─── Projected points ──────────────────────────────────────────────────

  const pointsTotals = useMemo(() => {
    const currentPoints: number[] = [];
    const targetPoints: number[] = [];
    for (const name of selectedSubjects) {
      const config = subjectConfigs[name];
      if (!config) continue;
      const lcSubject = LC_SUBJECTS.find(s => s.name === name);
      const isMaths = lcSubject?.isMaths || false;
      currentPoints.push(getPointsForGrade(config.currentGrade, isMaths));
      targetPoints.push(getPointsForGrade(config.targetGrade, isMaths));
    }
    // CAO points = best 6 subjects, max 625
    currentPoints.sort((a, b) => b - a);
    targetPoints.sort((a, b) => b - a);
    const current = Math.min(625, currentPoints.slice(0, 6).reduce((sum, p) => sum + p, 0));
    const target = Math.min(625, targetPoints.slice(0, 6).reduce((sum, p) => sum + p, 0));
    return { current, target, gain: target - current };
  }, [selectedSubjects, subjectConfigs]);

  // ─── Grouped subjects (curriculum-aware) ───────────────────────────────
  //
  // JC students see the 24-subject JC list; senior students see LC_SUBJECTS
  // unchanged. The 6 group buckets and GROUP_DOT_HEX map work for both.

  const groupedSubjects = useMemo(() => {
    const list = curriculumLevel === 'junior' ? JC_SUBJECTS : isLca ? LCA_SUBJECTS : LC_SUBJECTS;
    const groups: Record<string, LCSubject[]> = {};
    for (const subj of list) {
      if (!groups[subj.group]) groups[subj.group] = [];
      groups[subj.group].push(subj as LCSubject);
    }
    return groups;
  }, [curriculumLevel, isLca]);

  // ─── Step validation ───────────────────────────────────────────────────

  const canProceed = () => {
    switch (step) {
      case 1: return true;
      case 2: return yearGroup !== null;
      case 3: return true;
      case 4: return northStarData !== null;
      case 5: return selectedSubjects.size > 0;
      case 6: {
        // LCA: nothing to configure — all courses are common level, credit-based.
        if (isLca) return true;
        // Curriculum-aware: JC checks subjectBands, senior checks subjectConfigs.
        const map = curriculumLevel === 'junior' ? subjectBands : subjectConfigs;
        for (const name of selectedSubjects) {
          if (!map[name]) return false;
        }
        return true;
      }
      case 7: return restDays.size < 7 && (!needsExamDate || (examDate.length > 0 && getDaysUntil(examDate) > 0));
      case 8: return restDays.size < 7;
      case 9: return true;
      case 10: return true;
      default: return false;
    }
  };

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, y: dir > 0 ? 14 : -10, scale: 0.992 }),
    visible: { opacity: 1, y: 0, scale: 1 },
    exit: (dir: number) => ({ opacity: 0, y: dir > 0 ? -8 : 12, scale: 0.995 }),
  };

  const daysLeft = getDaysUntil(examDate);

  return (
    <div className="theme-compat fixed inset-0 z-[60] flex touch-pan-y flex-col overflow-hidden overscroll-none" data-prevent-pull-to-refresh="true">

      {/* ─── Solid background — matches Library (module selection) screen ─── */}
      <div className="fixed inset-0 pointer-events-none dark:bg-zinc-900" aria-hidden="true" style={{ backgroundColor: '#FAFBF6' }} />

      {/* ─── Fixed Header: Progress bar + Skip ─── */}
      <div className="shrink-0 relative z-10 px-6 pt-5 pb-3">
        <div className="flex items-center justify-between mb-3 max-w-md mx-auto">
          <span className="text-[10px] font-bold uppercase tracking-[0.16em] text-[#8D857E] dark:text-zinc-500">
            Stage {currentStage} of {totalStages}
          </span>
          {step === 1 && !isTransition && (
            <button
              onClick={skipOnboarding}
              className="text-sm font-medium transition-colors text-[#8D857E] hover:text-[#1A1A1A] dark:text-zinc-500"
            >
              Skip for now
            </button>
          )}
        </div>
        <div className="max-w-md mx-auto">
          <div className="w-full h-[10px] rounded-full overflow-hidden bg-[#ECE8E3] dark:bg-zinc-700">
            <motion.div
              className="h-full rounded-full"
              style={{ backgroundColor: 'rgba(242,107,31,0.9)' }}
              animate={{ width: `${(currentStage / totalStages) * 100}%` }}
              transition={{ duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
            />
          </div>
        </div>
      </div>

      {/* ─── Scrollable Content ─── */}
      <div
        ref={scrollRegionRef}
        data-testid="onboarding-scroll-region"
        className="relative z-10 min-h-0 flex-1 touch-pan-y overflow-y-auto overscroll-contain [-webkit-overflow-scrolling:touch]"
      >
        <div className="mx-auto max-w-2xl px-7 py-6 sm:px-6 sm:py-10">
          <AnimatePresence mode="wait" custom={direction}>

            {/* Step 1: Welcome — staggered entrance, glass card, preview chips */}
            {step === 1 && (
              <MotionDiv key="step1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-lg mx-auto">
                    <OnboardingGuide
                      tint="#FBE9DC"
                      ink="#B5500F"
                      tilt={-3}
                      question={`Hi ${userName.split(' ')[0] || userName} — I'm your guide here.`}
                      sub="Two minutes of setup and the whole app fits itself around you. One question at a time."
                    />

                    {/* Feature preview chips */}
                    <motion.div
                      initial={{ opacity: 0, y: 16 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.8, ease: [0.16, 1, 0.3, 1] }}
                      className="grid grid-cols-2 gap-3 max-w-md mx-auto"
                    >
                      {PREVIEW_CHIPS.map((chip, i) => (
                        <motion.div
                          key={chip.label}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.4, delay: 0.9 + i * 0.08, ease: [0.16, 1, 0.3, 1] }}
                          className="flex flex-col items-center justify-center gap-2 px-3 py-5 rounded-2xl text-sm font-semibold text-center"
                          style={{ backgroundColor: 'rgba(255,255,255,0.85)', border: '1px solid rgba(0,0,0,0.06)', color: '#3a3530' }}
                        >
                          <PreviewChipIcon config={chip} size={72} />
                          <span>{chip.label}</span>
                        </motion.div>
                      ))}
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 2: Year Group — Junior Cycle + Senior Cycle two-band layout (Phase 1 JC) */}
            {step === 2 && (
              <MotionDiv key="step2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                <div className="flex flex-col items-center justify-center min-h-[60vh] py-6">
                  <div className="text-center w-full max-w-xl mx-auto">
                    <OnboardingGuide
                      tint="#DCE9F2"
                      ink="#33658A"
                      tilt={2}
                      question="What year are you in?"
                      sub="Pick your year — the whole app shapes itself around it."
                    />

                    {/* Junior Cycle band */}
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="mb-8"
                    >
                      <p className="text-[11px] font-semibold uppercase tracking-wider mb-3 text-[#6B6B6B] font-sans text-left">
                        Junior Cycle
                      </p>
                      <div className="grid grid-cols-3 gap-3">
                        {(['1st', '2nd', '3rd'] as const).map(yr => {
                          const selected = yearGroup === yr;
                          return (
                            <button
                              key={yr}
                              onClick={() => setYearGroup(yr)}
                              className={`group flex flex-col items-center justify-center py-5 rounded-2xl border-2 border-[#1A1A1A] font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${
                                selected ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'
                              }`}
                            >
                              <span className="text-2xl font-bold leading-none">{yr}</span>
                              <span className="text-[11px] font-medium mt-1 opacity-80">Year</span>
                            </button>
                          );
                        })}
                      </div>
                    </motion.div>

                    {/* Senior Cycle band */}
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}
                      className="mb-8"
                    >
                      <p className="text-[11px] font-semibold uppercase tracking-wider mb-3 text-[#6B6B6B] font-sans text-left">
                        Senior Cycle
                      </p>
                      <div className="grid grid-cols-3 gap-3">
                        {(['TY', '5th', '6th'] as const).map(yr => {
                          const selected = yearGroup === yr;
                          // TY = "4th year" colloquially, but the underlying
                          // YearGroup token stays 'TY' to match Phase 1's
                          // type union (no migration needed). UI shows "4th"
                          // with "Transition Year" subtitle for clarity.
                          const label = yr === 'TY' ? '4th' : yr;
                          const sub = yr === 'TY' ? 'Transition Year' : 'Year';
                          return (
                            <button
                              key={yr}
                              onClick={() => setYearGroup(yr)}
                              className={`group flex flex-col items-center justify-center py-5 rounded-2xl border-2 border-[#1A1A1A] font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${
                                selected ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'
                              }`}
                            >
                              <span className="text-2xl font-bold leading-none">{label}</span>
                              <span className="text-[11px] font-medium mt-1 opacity-80">{sub}</span>
                            </button>
                          );
                        })}
                      </div>
                    </motion.div>

                    {/* Leaving Cert Applied band */}
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
                    >
                      <p className="text-[11px] font-semibold uppercase tracking-wider mb-3 text-[#6B6B6B] font-sans text-left">
                        Leaving Cert Applied
                      </p>
                      <div className="grid grid-cols-2 gap-3">
                        {(['LCA1', 'LCA2'] as const).map(yr => {
                          const selected = yearGroup === yr;
                          return (
                            <button
                              key={yr}
                              onClick={() => setYearGroup(yr)}
                              className={`group flex flex-col items-center justify-center py-5 rounded-2xl border-2 border-[#1A1A1A] font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${
                                selected ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'
                              }`}
                            >
                              <span className="text-2xl font-bold leading-none">{yr === 'LCA1' ? 'Year 1' : 'Year 2'}</span>
                              <span className="text-[11px] font-medium mt-1 opacity-80">LCA</span>
                            </button>
                          );
                        })}
                      </div>
                    </motion.div>

                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.7, ease: [0.16, 1, 0.3, 1] }}
                      className="mt-9 border-t border-[#DED9D3] pt-7"
                    >
                      <div className="mb-3 text-left">
                        <p className="text-[11px] font-semibold uppercase tracking-wider text-[#6B6B6B]">Learning preference</p>
                        <p className="mt-1 text-xs text-[#78716C]">Choose the amount of explanation you prefer. You can change this later.</p>
                      </div>
                      <div className="grid gap-3 sm:grid-cols-2">
                        {([
                          { id: false, title: 'Full Modules', desc: 'All the science and strategy behind each idea.' },
                          { id: true, title: 'Essentials', desc: 'Key ideas faster, with the same activities and practice.' },
                        ] as const).map(option => {
                          const selected = essentialsMode === option.id;
                          return (
                            <button
                              key={String(option.id)}
                              type="button"
                              onClick={() => setEssentialsMode(option.id)}
                              className={`rounded-2xl border-2 border-[#1A1A1A] px-4 py-4 text-left shadow-[4px_4px_0_0_#1A1A1A] transition-all duration-150 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-none ${selected ? 'bg-[#F26B1F] text-white' : 'bg-[#FDF8F0] text-[#1A1A1A]'}`}
                            >
                              <p className="font-bold">{option.title}</p>
                              <p className={`mt-1 text-xs leading-relaxed ${selected ? 'text-white/80' : 'text-[#78716C]'}`}>{option.desc}</p>
                            </button>
                          );
                        })}
                      </div>
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 3: Module Mode */}
            {step === 3 && (
              <MotionDiv key="step3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-lg mx-auto">
                    <OnboardingGuide
                      tint="#EFEAF3"
                      ink="#5B4A7E"
                      tilt={-2}
                      question="How do you like to learn?"
                      sub="Choose the style that suits you best — you can change this any time in Settings."
                    />
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="flex flex-col sm:flex-row gap-4 justify-center"
                    >
                      {([
                        { id: false, title: 'Full Modules', desc: 'The deep dive \u2014 all the science and strategy behind each idea.' },
                        { id: true, title: 'Essentials', desc: 'Key ideas fast \u2014 less reading, same activities and practice.' },
                      ] as const).map(opt => {
                        const selected = essentialsMode === opt.id;
                        return (
                          <button
                            key={String(opt.id)}
                            onClick={() => setEssentialsMode(opt.id)}
                            // Chunky-shadow card to match the year/subject pickers.
                            // Same border-2 / 4-6px black drop-shadow / press
                            // translate as the rest of onboarding.
                            className={`flex-1 py-6 px-5 rounded-2xl border-2 border-[#1A1A1A] text-left font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${
                              selected ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'
                            }`}
                          >
                            <p className="text-base font-bold mb-1">{opt.title}</p>
                            <p className={`text-xs ${selected ? 'text-[#FDF8F0]/85' : 'text-[#78716C]'}`}>{opt.desc}</p>
                          </button>
                        );
                      })}
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 4: North Star — JC sees the 4 JC themes, senior sees the 6 senior themes.
                In transition mode (JC→senior re-onboarding) this is the LAST step:
                picking the senior NS finalizes the whole flow via onComplete. */}
            {step === 4 && (
              <MotionDiv key="step4" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                {isTransition && (
                  <div className="mb-4 px-4 py-3 rounded-xl border-2 border-[#F26B1F] bg-[rgba(242,107,31,0.08)] text-center">
                    <p className="text-xs font-bold uppercase tracking-widest text-[#F26B1F] mb-1">Stepping into senior cycle</p>
                    <p className="text-sm text-[#1A1A1A] dark:text-zinc-200">Last step — your new North Star for this chapter.</p>
                  </div>
                )}
                <NorthStarOnboarding
                  onComplete={(ns) => {
                    setNorthStarData(ns);
                    if (isTransition) {
                      // Final step in transition mode — finalise immediately.
                      void completeOnboarding(ns);
                    } else {
                      goNext();
                    }
                  }}
                  initialData={northStarData}
                  curriculumLevel={curriculumLevel ?? 'senior'}
                />
              </MotionDiv>
            )}

            {/* Step 5: Select Subjects */}
            {step === 5 && (
              <MotionDiv key="step5" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                {isTransition && (
                  <div className="mb-4 px-4 py-3 rounded-xl border-2 border-[#F26B1F] bg-[rgba(242,107,31,0.08)] text-center">
                    <p className="text-xs font-bold uppercase tracking-widest text-[#F26B1F] mb-1">Stepping into senior cycle</p>
                    <p className="text-sm text-[#1A1A1A] dark:text-zinc-200">Let's set up your Leaving Cert profile.</p>
                  </div>
                )}
                <OnboardingGuide
                  tint="#E8F2EC"
                  ink="#1F5F3E"
                  tilt={2}
                  question={isTransition ? 'Which Leaving Cert subjects are you taking?' : 'Which subjects are you carrying?'}
                  sub={<>
                    Tap to select {curriculumLevel === 'junior' ? 'your subjects' : 'your Leaving Cert subjects'}.{' '}
                    <span className="font-semibold text-[#F26B1F]">{selectedSubjects.size} selected</span>
                  </>}
                />
                <div>
                  {Object.entries(groupedSubjects).map(([group, subjects]) => {
                    const dotHex = GROUP_DOT_HEX[group as LCSubject['group']];
                    return (
                      <div key={group} className="mb-8 last:mb-0">
                        <p className="text-[11px] font-semibold uppercase tracking-wider mb-3 text-[#6B6B6B] font-sans">
                          {SUBJECT_GROUP_LABELS[group as LCSubject['group']]}
                        </p>
                        <div className="flex flex-wrap gap-3">
                          {subjects.map(subj => {
                            const selected = selectedSubjects.has(subj.name);
                            return (
                              <button
                                key={subj.name}
                                onClick={() => toggleSubject(subj.name)}
                                className={`group flex items-center gap-2.5 px-4 py-3 rounded-2xl border-2 border-[#1A1A1A] font-sans font-medium text-[15px] transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${
                                  selected
                                    ? 'bg-[#F26B1F] text-[#FDF8F0]'
                                    : 'bg-[#FDF8F0] text-[#1A1A1A]'
                                }`}
                              >
                                <span
                                  className="w-2.5 h-2.5 rounded-full shrink-0"
                                  style={{
                                    backgroundColor: selected ? 'transparent' : dotHex,
                                    boxShadow: selected ? 'inset 0 0 0 1.5px #FDF8F0' : 'none',
                                  }}
                                  aria-hidden
                                />
                                {subj.name}
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </MotionDiv>
            )}

            {/* Step 6: Grade Configuration */}
            {step === 6 && curriculumLevel === 'junior' && (
              <MotionDiv key="step6-jc" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                <OnboardingGuide
                  tint="#F6EEDF"
                  ink="#8A6B2D"
                  tilt={-2}
                  question="Where are you now — and where are you headed?"
                  sub="For each subject, set your current band and where you're aiming."
                />

                <div className="space-y-4">
                  {Array.from(selectedSubjects).map(name => {
                    const band = subjectBands[name] || { level: 'common' as Level, currentBand: 'Merit' as JCBand, targetBand: 'Higher Merit' as JCBand };
                    const jcSubject: JCSubject | undefined = JC_SUBJECTS.find(s => s.name === name);
                    const hasLevelChoice = jcSubject?.jcHasLevelChoice ?? false;
                    const groupColor = jcSubject ? GROUP_COLORS[jcSubject.group] : GROUP_COLORS.stem;
                    const currentIdx = JC_BANDS.indexOf(band.currentBand);

                    return (
                      <div
                        key={name}
                        className="rounded-2xl overflow-hidden border-2 border-[#1A1A1A] shadow-[4px_4px_0_0_#1A1A1A]"
                        style={{ backgroundColor: '#FDF8F0' }}
                      >
                        {/* Subject header row */}
                        <div className="flex items-center justify-between px-4 pt-3 pb-2 border-b-2 border-[#1A1A1A]/10">
                          <span className={`text-sm font-bold ${groupColor.text}`}>{name}</span>
                          {hasLevelChoice ? (
                            <div className="flex items-center gap-1">
                              {(['higher', 'ordinary'] as const).map(lvl => (
                                <button
                                  key={lvl}
                                  onClick={() => updateBand(name, 'level', lvl)}
                                  className={`px-2.5 py-1 rounded-md text-[10px] font-bold border-2 border-[#1A1A1A] transition-all duration-150 shadow-[2px_2px_0_0_#1A1A1A] active:translate-x-0.5 active:translate-y-0.5 active:shadow-[0px_0px_0_0_#1A1A1A] ${
                                    band.level === lvl
                                      ? 'bg-[#1A1A1A] text-[#FDF8F0]'
                                      : 'bg-[#FDF8F0] text-[#1A1A1A]'
                                  }`}
                                >
                                  {lvl === 'higher' ? 'Higher' : 'Ordinary'}
                                </button>
                              ))}
                            </div>
                          ) : (
                            <span className="text-[10px] font-bold uppercase tracking-widest text-[#78716C]">Common Level</span>
                          )}
                        </div>

                        {/* Two-row band selection */}
                        <div className="px-4 pt-3 pb-3 space-y-3">
                          {/* Current band */}
                          <div>
                            <p className="text-[10px] font-bold uppercase tracking-wider text-[#78716C] mb-1.5">Where I am now</p>
                            <div className="flex flex-wrap gap-1.5">
                              {JC_BANDS.map(b => (
                                <button
                                  key={b}
                                  onClick={() => updateBand(name, 'currentBand', b)}
                                  className={`flex-1 min-w-[70px] py-2 rounded-lg text-[10px] ${
                                    b === band.currentBand
                                      ? getCurrentGradePillClass(true)
                                      : getCurrentGradePillClass(false)
                                  }`}
                                >
                                  {b}
                                </button>
                              ))}
                            </div>
                          </div>
                          {/* Target band */}
                          <div>
                            <p className="text-[10px] font-bold uppercase tracking-wider text-[#F26B1F] mb-1.5">My target</p>
                            <div className="flex flex-wrap gap-1.5">
                              {JC_BANDS.map((b, bi) => {
                                // Target must be at least as good as current (lower index = better)
                                const disabled = bi > currentIdx;
                                return (
                                  <button
                                    key={b}
                                    onClick={() => { if (!disabled) updateBand(name, 'targetBand', b); }}
                                    disabled={disabled}
                                    className={`flex-1 min-w-[70px] py-2 rounded-lg text-[10px] ${
                                      disabled
                                        ? 'border-2 border-[#1A1A1A]/15 bg-[#FDF8F0]/40 text-[#1A1A1A]/25 cursor-not-allowed font-bold'
                                        : b === band.targetBand
                                          ? getTargetGradePillClass(true)
                                          : getTargetGradePillClass(false)
                                    }`}
                                  >
                                    {b}
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </MotionDiv>
            )}

            {step === 6 && curriculumLevel !== 'junior' && !isLca && (
              <MotionDiv key="step6" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                {isTransition && (
                  <div className="mb-4 px-4 py-3 rounded-xl border-2 border-[#F26B1F] bg-[rgba(242,107,31,0.08)] text-center">
                    <p className="text-xs font-bold uppercase tracking-widest text-[#F26B1F] mb-1">Stepping into senior cycle</p>
                    <p className="text-sm text-[#1A1A1A] dark:text-zinc-200">Pick where you are now and where you're aiming for your Leaving Cert.</p>
                  </div>
                )}
                <OnboardingGuide
                  tint="#F6EEDF"
                  ink="#8A6B2D"
                  tilt={2}
                  question="Where are you now — and where are you headed?"
                  sub="For each subject, set where you are now and where you want to be."
                />

                <div className="space-y-4">
                  {Array.from(selectedSubjects).map(name => {
                    const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
                    const grades = getGradesForLevel(config.level);
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const groupColor = lcSubject ? GROUP_COLORS[lcSubject.group] : GROUP_COLORS.stem;
                    const currentIdx = getGradeIndex(config.currentGrade);
                    const targetIdx = getGradeIndex(config.targetGrade);

                    return (
                      <div
                        key={name}
                        className="rounded-2xl overflow-hidden border-2 border-[#1A1A1A] shadow-[4px_4px_0_0_#1A1A1A]"
                        style={{ backgroundColor: '#FDF8F0' }}
                      >
                        {/* Subject header row */}
                        <div className="flex items-center justify-between px-4 pt-3 pb-2 border-b-2 border-[#1A1A1A]/10">
                          <span className={`text-sm font-bold ${groupColor.text}`}>{name}</span>
                          <div className="flex items-center gap-1">
                            {(['higher', 'ordinary'] as const).map(lvl => (
                              <button
                                key={lvl}
                                onClick={() => updateConfig(name, 'level', lvl)}
                                className={`px-2.5 py-1 rounded-md text-[10px] font-bold border-2 border-[#1A1A1A] transition-all duration-150 shadow-[2px_2px_0_0_#1A1A1A] active:translate-x-0.5 active:translate-y-0.5 active:shadow-[0px_0px_0_0_#1A1A1A] ${
                                  config.level === lvl
                                    ? 'bg-[#1A1A1A] text-[#FDF8F0]'
                                    : 'bg-[#FDF8F0] text-[#1A1A1A]'
                                }`}
                              >
                                {lvl === 'higher' ? 'Higher' : 'Ordinary'}
                              </button>
                            ))}
                          </div>
                        </div>

                        {/* Two-row grade selection */}
                        <div className="px-4 pt-3 pb-3 space-y-3">
                          {/* Current grade row */}
                          <div>
                            <p className="text-[10px] font-bold uppercase tracking-wider text-[#78716C] mb-1.5">Where I am now</p>
                            <div className="flex gap-1.5">
                              {grades.map((g, _gi) => (
                                <button
                                  key={g}
                                  onClick={() => updateConfig(name, 'currentGrade', g)}
                                  className={`flex-1 py-2 rounded-lg text-[11px] ${
                                    g === config.currentGrade
                                      ? getCurrentGradePillClass(true)
                                      : getCurrentGradePillClass(false)
                                  }`}
                                >
                                  {g}
                                </button>
                              ))}
                            </div>
                          </div>
                          {/* Target grade row */}
                          <div>
                            <p className="text-[10px] font-bold uppercase tracking-wider text-[#F26B1F] mb-1.5">My target</p>
                            <div className="flex gap-1.5">
                              {grades.map((g, gi) => {
                                const disabled = gi > currentIdx;
                                return (
                                  <button
                                    key={g}
                                    onClick={() => { if (!disabled) updateConfig(name, 'targetGrade', g); }}
                                    disabled={disabled}
                                    className={`flex-1 py-2 rounded-lg text-[11px] ${
                                      disabled
                                        ? 'border-2 border-[#1A1A1A]/15 bg-[#FDF8F0]/40 text-[#1A1A1A]/25 cursor-not-allowed font-bold'
                                        : g === config.targetGrade
                                          ? getTargetGradePillClass(true)
                                          : getTargetGradePillClass(false)
                                    }`}
                                  >
                                    {g}
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                          {/* Improvement indicator */}
                          {targetIdx < currentIdx && (
                            <div className="flex items-center justify-between pt-1 px-0.5">
                              <span className="text-[10px] text-zinc-400 dark:text-zinc-500">
                                {config.currentGrade} <ArrowRight size={8} className="inline -mt-0.5" /> {config.targetGrade}
                              </span>
                              <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
                                +{getPointsForGrade(config.targetGrade, lcSubject?.isMaths || false) - getPointsForGrade(config.currentGrade, lcSubject?.isMaths || false)} pts
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </MotionDiv>
            )}

            {/* Step 7: Exam date and weekly availability */}
            {step === 7 && (
              <MotionDiv key="step7" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                <div className="w-full max-w-2xl mx-auto py-4 sm:py-8">
                  <div className="text-center">
                    <OnboardingGuide
                      tint="#ECEFF0"
                      ink="#46555E"
                      tilt={-2}
                      question="When do the exams land?"
                      sub={needsExamDate
                        ? 'Add your exam date and choose the days that need to stay free — the year gets paced backwards from it.'
                        : 'Choose the days that need to stay free. You can add an exam date later.'}
                    />

                    {needsExamDate && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                        className="mx-auto mb-8 grid max-w-lg gap-3 sm:grid-cols-[1fr_auto] sm:items-stretch"
                      >
                        <label className="rounded-2xl border-2 border-[#1A1A1A] bg-white px-4 py-3 text-left">
                          <span className="mb-1 block text-[10px] font-bold uppercase tracking-[0.16em] text-[#8A8178]">Exam date</span>
                          <input
                            type="date"
                            value={examDate}
                            onChange={(e) => setExamDate(e.target.value)}
                            className="w-full bg-transparent text-base font-semibold text-[#1A1A1A] outline-none"
                          />
                        </label>
                        {daysLeft > 0 && (
                          <div className="flex min-w-32 items-center justify-center gap-2 rounded-2xl border-2 border-[#1A1A1A] bg-[#FDF8F0] px-5 py-3">
                            <span className="font-apercu text-3xl font-black leading-none text-[#1A1A1A]">{daysLeft}</span>
                            <span className="text-left text-[10px] font-bold uppercase leading-tight tracking-[0.12em] text-[#8A8178]">days<br />to go</span>
                          </div>
                        )}
                      </motion.div>
                    )}

                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.48, ease: [0.16, 1, 0.3, 1] }}
                      className="border-t border-[#DED9D3] pt-7"
                    >
                      <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-[#8A8178]">Weekly availability</p>
                      <p className="mx-auto mt-1 mb-5 max-w-md text-sm text-[#78716C]">Select any days when study is not possible. We will distribute sessions across the remaining days.</p>
                      <div className="mx-auto grid max-w-lg grid-cols-2 gap-3 sm:grid-cols-4">
                        {DAYS_OF_WEEK.map(day => {
                          const isRest = restDays.has(day);
                          return (
                            <button
                              key={day}
                              type="button"
                              onClick={() => toggleRestDay(day)}
                              className={`flex min-h-16 items-center justify-between rounded-2xl border-2 border-[#1A1A1A] px-4 py-3 font-sans shadow-[3px_3px_0_0_#1A1A1A] transition-all duration-150 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-none ${isRest ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'}`}
                            >
                              <span className="text-xs font-bold uppercase tracking-wider">{DAY_SHORTS[day]}</span>
                              {isRest ? <CalendarOff size={17} /> : <Check size={17} />}
                            </button>
                          );
                        })}
                      </div>
                      <p className="mt-5 text-sm text-[#8A8178]">
                        {7 - restDays.size} study {7 - restDays.size === 1 ? 'day' : 'days'} per week
                        {restDays.size > 0 ? ` · ${restDays.size} rest ${restDays.size === 1 ? 'day' : 'days'}` : ''}
                      </p>
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 8: Rest Days — glass card */}
            {step === 8 && (
              <MotionDiv key="step8" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[50vh]">
                  <div className="text-center w-full max-w-lg mx-auto">
                    <OnboardingGuide
                      tint="#F6EAED"
                      ink="#84495A"
                      tilt={2}
                      question="Which days are off-limits?"
                      sub="Rest is part of the plan — tap the days study isn't possible and the sessions redistribute around them."
                    />

                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="grid grid-cols-7 gap-2 max-w-md mx-auto"
                    >
                      {DAYS_OF_WEEK.map(day => {
                        const isRest = restDays.has(day);
                        return (
                          <button
                            key={day}
                            onClick={() => toggleRestDay(day)}
                            // Chunky day card. Rest = orange fill on cream
                            // background (matches selected state language).
                            // Study day = cream fill. Same press animation
                            // as the year + grade pickers.
                            className={`flex flex-col items-center justify-center gap-2 py-4 rounded-2xl border-2 border-[#1A1A1A] font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] ${
                              isRest ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'
                            }`}
                          >
                            <span className="text-[11px] font-bold uppercase tracking-wider">{DAY_SHORTS[day]}</span>
                            {isRest
                              ? <CalendarOff size={16} className="text-[#FDF8F0]" />
                              : <Check size={16} className="text-[#1A1A1A]" />}
                          </button>
                        );
                      })}
                    </motion.div>

                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.4, delay: 0.6 }}
                      className="text-sm text-zinc-400 dark:text-zinc-500 mt-8"
                    >
                      {7 - restDays.size} study {7 - restDays.size === 1 ? 'day' : 'days'} per week{restDays.size > 0 ? ` — ${restDays.size} rest ${restDays.size === 1 ? 'day' : 'days'}` : ''}
                    </motion.p>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 9: Review and launch */}
            {step === 9 && (
              <MotionDiv key="step9" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ type: 'spring', stiffness: 250, damping: 28, mass: 0.8 }}>
                <OnboardingGuide
                  tint="#E8F2EC"
                  ink="#1F5F3E"
                  tilt={-2}
                  question={`You're ready, ${userName.split(' ')[0] || userName}.`}
                  sub="Here's the plan we built together — review it, then start learning."
                />

                {/* Projected points banner — current → target with animated gain.
                    Senior-only: JC has no CAO points concept. The JC grade-summary
                    banner (descriptor bands) lands in Phase 4. */}
                {curriculumLevel === 'senior' && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                  className="p-6 rounded-2xl bg-white border-2 border-[#1A1A1A] text-center mb-6"
                >
                  {/* Current → Target row */}
                  <div className="flex items-center justify-center gap-3 mb-3">
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-0.5">Current</p>
                      <p className="text-2xl font-bold font-mono text-zinc-400 dark:text-zinc-500">
                        <AnimatedNumber value={pointsTotals.current} delay={0.2} />
                      </p>
                    </div>
                    <ArrowRight size={18} className="text-zinc-300 dark:text-zinc-600 mt-4" />
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-700 dark:text-zinc-300 mb-0.5">Target</p>
                      <p className="text-2xl font-bold font-mono text-zinc-800 dark:text-zinc-100">
                        <AnimatedNumber value={pointsTotals.target} delay={0.4} />
                      </p>
                    </div>
                  </div>
                  {/* Gain hero number */}
                  <div className="pt-3 border-t border-zinc-200/50 dark:border-white/[0.06]">
                    {/* Full accent, not 70% of it: the faded form composited to
                        3.27:1 on the dark card, and this is a 10px bold label.
                        It also now matches the number it sits over. */}
                    <p className="text-[10px] font-bold uppercase tracking-widest text-[var(--accent-hex)] mb-1">Projected Gain</p>
                    <p className="text-4xl font-bold font-mono text-[var(--accent-hex)]">
                      <AnimatedNumber value={pointsTotals.gain} prefix={pointsTotals.gain > 0 ? '+' : ''} delay={0.6} />
                    </p>
                  </div>
                </motion.div>
                )}

                {/* Subject summary — senior: grade + points columns;
                    junior: subject names only (grade/band columns land in Phase 4). */}
                <div className="space-y-2 mb-6">
                  {Array.from(selectedSubjects).map((name, i) => {
                    const config = subjectConfigs[name];
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const isMaths = lcSubject?.isMaths || false;

                    if (curriculumLevel === 'junior') {
                      const band = subjectBands[name];
                      const jc = JC_SUBJECTS.find(s => s.name === name);
                      const levelLabel = band?.level === 'higher' ? 'Higher'
                        : band?.level === 'ordinary' ? 'Ordinary'
                        : jc?.jcHasLevelChoice ? 'Higher' : 'Common';
                      return (
                        <motion.div
                          key={name}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.3, delay: 0.2 + i * 0.04, ease: [0.16, 1, 0.3, 1] }}
                          className="flex items-center justify-between p-3 rounded-xl bg-white border border-[#D8D3CD]"
                        >
                          <div>
                            <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">{name}</p>
                            <p className="text-[10px] text-zinc-400 dark:text-zinc-500">{levelLabel} Level</p>
                          </div>
                          {band && (
                            <div className="flex items-center gap-2">
                              <span className="text-[11px] font-bold text-zinc-500 dark:text-zinc-400">{band.currentBand}</span>
                              <ArrowRight size={12} className="text-zinc-300 dark:text-zinc-600" />
                              <span className="text-[11px] font-bold text-[#F26B1F] dark:text-[#F26B1F]">{band.targetBand}</span>
                            </div>
                          )}
                        </motion.div>
                      );
                    }

                    if (!config) return null;
                    const currentPts = getPointsForGrade(config.currentGrade, isMaths);
                    const targetPts = getPointsForGrade(config.targetGrade, isMaths);
                    const gain = targetPts - currentPts;

                    return (
                      <motion.div
                        key={name}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.2 + i * 0.04, ease: [0.16, 1, 0.3, 1] }}
                        className="flex items-center justify-between p-3 rounded-xl bg-white border border-[#D8D3CD]"
                      >
                        <div>
                          <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">{name}</p>
                          <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                            {config.level === 'higher' ? 'Higher' : 'Ordinary'} Level
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">{config.currentGrade}</span>
                          <ArrowRight size={12} className="text-zinc-300 dark:text-zinc-600" />
                          <span className="text-xs font-bold text-[#F26B1F] dark:text-[#F26B1F]">{config.targetGrade}</span>
                          {gain > 0 && (
                            <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 ml-1">+{gain}pts</span>
                          )}
                        </div>
                      </motion.div>
                    );
                  })}
                </div>

                {/* Stats row */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.4, delay: 0.5 }}
                  className="flex items-center justify-center gap-6 text-sm text-zinc-400 dark:text-zinc-500"
                >
                  {needsExamDate && <span className="flex items-center gap-1.5"><Calendar size={14} /> {daysLeft} days left</span>}
                  <span className="flex items-center gap-1.5"><CalendarOff size={14} /> {restDays.size} rest {restDays.size === 1 ? 'day' : 'days'}</span>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
                  className="mt-8 flex flex-col items-center gap-3"
                >
                  <button
                    type="button"
                    onClick={() => void completeOnboarding(northStarData ?? undefined)}
                    className="flex min-w-48 items-center gap-2 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] px-8 py-3 text-sm font-semibold text-[#FDF8F0] shadow-[4px_4px_0_0_#1A1A1A] transition-all duration-150 hover:-translate-y-0.5 hover:shadow-[6px_6px_0_0_#1A1A1A] active:translate-x-1 active:translate-y-1 active:shadow-none"
                  >
                    <span className="flex-1 text-center">Start Learning</span>
                    <ArrowRight size={14} />
                  </button>
                  <button type="button" onClick={goBack} className="flex items-center gap-1.5 text-sm font-medium text-[#8A8178] transition-colors hover:text-[#1A1A1A]">
                    <ArrowLeft size={14} /> Back
                  </button>
                </motion.div>
              </MotionDiv>
            )}

            {/* Step 10: You're All Set — celebratory completion */}
            {step === 10 && (
              <MotionDiv key="step10" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-md mx-auto">
                    {/* Checkmark icon */}
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-16 h-16 mx-auto mb-6 rounded-full flex items-center justify-center"
                      style={{ backgroundColor: COLORS.accent }}
                    >
                      <Check size={32} style={{ color: '#fff' }} strokeWidth={3} />
                    </motion.div>

                    {/* Heading */}
                    <motion.h2
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
                      className="font-serif text-3xl sm:text-4xl font-bold mb-2 text-[#1A1A1A] dark:text-white"
                    >
                      You're all set, {userName.split(' ')[0] || userName}.
                    </motion.h2>

                    <motion.p
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="text-base mb-8 text-[#78716C] dark:text-zinc-400"
                    >
                      Your personalised study plan is ready.
                    </motion.p>

                    {/* Stats hero card */}
                    <motion.div
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.55, ease: [0.16, 1, 0.3, 1] }}
                      className="rounded-2xl px-6 py-5 mb-8"
                      style={{ backgroundColor: 'rgba(255,255,255,0.85)', border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 4px 24px rgba(0,0,0,0.06)' }}
                    >
                      <div className="flex items-center justify-around">
                        {curriculumLevel === 'senior' && (
                          <>
                            <div>
                              <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Target</p>
                              <p className="text-3xl font-apercu font-black text-[#1A1A1A] dark:text-white">
                                <AnimatedNumber value={pointsTotals.target} delay={0.7} />
                              </p>
                              <p className="text-[11px] text-[#A8A29E] dark:text-zinc-500">CAO pts</p>
                            </div>
                            <div className="w-px h-12" style={{ backgroundColor: 'rgba(0,0,0,0.08)' }} />
                          </>
                        )}
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Countdown</p>
                          <p className="text-3xl font-apercu font-black text-[#1A1A1A] dark:text-white">
                            <AnimatedNumber value={daysLeft} delay={0.9} />
                          </p>
                          <p className="text-[11px] text-[#A8A29E] dark:text-zinc-500">days left</p>
                        </div>
                        <div className="w-px h-12" style={{ backgroundColor: 'rgba(0,0,0,0.08)' }} />
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Subjects</p>
                          <p className="text-3xl font-apercu font-black text-[#1A1A1A] dark:text-white">
                            <AnimatedNumber value={selectedSubjects.size} delay={1.1} />
                          </p>
                          <p className="text-[11px] text-[#A8A29E] dark:text-zinc-500">selected</p>
                        </div>
                      </div>
                    </motion.div>

                    {/* Start learning CTA */}
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.75, ease: [0.16, 1, 0.3, 1] }}
                      className="flex justify-center"
                    >
                      <PrimaryActionButton
                        label="Start Learning"
                        onClick={() => void completeOnboarding(northStarData ?? undefined)}
                        icon={ArrowRight}
                        variant="dark"
                      />
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

          </AnimatePresence>
        </div>
      </div>

      {/* ─── Fixed Footer: Back / Continue (hidden on step 4 — North Star has its own nav) ─── */}
      {step !== 4 && step !== 9 && step !== 10 && (
        <div className="shrink-0 px-6 py-5 relative z-10">
          <div className="max-w-2xl mx-auto flex flex-col items-center gap-3">
            {step < TOTAL_STEPS ? (
              <button
                onClick={goNext}
                disabled={!canProceed()}
                // Chunky orange CTA matching the year/subject pickers'
                // shadow language. Disabled state drops the shadow + dims.
                className="flex items-center gap-2 px-8 py-3 font-semibold text-sm rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-[2px_2px_0_0_#1A1A1A] disabled:translate-x-0 disabled:translate-y-0 disabled:hover:translate-y-0"
                style={{ minWidth: 160 }}
              >
                <span className="flex-1 text-center">{step === 1 ? 'Get Started' : 'Next'}</span>
                <ArrowRight size={14} />
              </button>
            ) : (
              <button
                onClick={() => void completeOnboarding(northStarData ?? undefined)}
                className="flex items-center gap-2 px-8 py-3 font-semibold text-sm rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A]"
                style={{ minWidth: 160 }}
              >
                <span className="flex-1 text-center">Start learning</span>
                <ArrowRight size={14} />
              </button>
            )}
            {step > 1 && (
              <button onClick={goBack} className="flex items-center gap-1.5 text-sm font-medium transition-colors text-[#A8A29E] dark:text-zinc-500">
                <ArrowLeft size={14} /> Back
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Onboarding;
