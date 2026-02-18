/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, ArrowLeft, Check, Calendar, CalendarOff, BookOpen, Target, Clock, CalendarDays, Star } from 'lucide-react';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
  getGradeIndex, DAYS_OF_WEEK,
  type LCSubject,
} from './subjectData';
import { NorthStar } from '../types';
import NorthStarOnboarding from './NorthStarOnboarding';

const MotionDiv = motion.div as any;
const MotionP = motion.p as any;
const MotionSpan = motion.span as any;

interface OnboardingProps {
  userName: string;
  onComplete: (profile: StudentSubjectProfile, northStar?: NorthStar) => void;
  onSkip: () => void;
}

type Step = 1 | 2 | 3 | 4 | 5 | 6 | 7;
const TOTAL_STEPS = 7;

// ─── Step-specific ambient blob colors ──────────────────────────────────────

const STEP_BLOBS: Record<Step, { a: string; b: string; c: string }> = {
  1: { a: 'bg-[#CC785C]/[0.07]', b: 'bg-yellow-300/[0.09]', c: 'bg-orange-200/[0.08]' },
  2: { a: 'bg-purple-300/[0.08]', b: 'bg-[#CC785C]/[0.07]', c: 'bg-amber-200/[0.06]' },
  3: { a: 'bg-blue-300/[0.08]', b: 'bg-emerald-300/[0.07]', c: 'bg-purple-200/[0.06]' },
  4: { a: 'bg-emerald-300/[0.08]', b: 'bg-amber-300/[0.07]', c: 'bg-blue-200/[0.06]' },
  5: { a: 'bg-amber-300/[0.09]', b: 'bg-[#CC785C]/[0.07]', c: 'bg-yellow-200/[0.08]' },
  6: { a: 'bg-rose-300/[0.08]', b: 'bg-orange-200/[0.07]', c: 'bg-pink-200/[0.06]' },
  7: { a: 'bg-emerald-300/[0.09]', b: 'bg-[#CC785C]/[0.07]', c: 'bg-amber-200/[0.06]' },
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

// ─── Grade pill color helpers (literal Tailwind for CDN) ────────────────────

function getCurrentGradePillClass(isSelected: boolean): string {
  return isSelected
    ? 'bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 border-zinc-800 dark:border-white shadow-sm'
    : 'bg-white dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 dark:hover:border-zinc-500';
}

function getTargetGradePillClass(isSelected: boolean): string {
  return isSelected
    ? 'bg-purple-600 dark:bg-purple-500 text-white border-purple-600 dark:border-purple-500 shadow-sm'
    : 'bg-white dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:border-purple-400 dark:hover:border-purple-500';
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function getDefaultExamDate(): string {
  const year = new Date().getFullYear();
  const june1 = new Date(year, 5, 1);
  const dayOfWeek = june1.getDay();
  const daysUntilWed = (3 - dayOfWeek + 7) % 7;
  const firstWed = new Date(year, 5, 1 + daysUntilWed);
  return firstWed.toISOString().split('T')[0];
}

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

const PREVIEW_CHIPS = [
  { icon: Star, label: 'Your North Star' },
  { icon: BookOpen, label: 'Your Subjects' },
  { icon: Target, label: 'Grade Targets' },
  { icon: CalendarDays, label: 'Exam Countdown' },
];

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

const Onboarding: React.FC<OnboardingProps> = ({ userName, onComplete, onSkip }) => {
  const [step, setStep] = useState<Step>(1);
  const [direction, setDirection] = useState(1);

  // Subject selection
  const [selectedSubjects, setSelectedSubjects] = useState<Set<string>>(new Set());

  // Grade configs
  const [subjectConfigs, setSubjectConfigs] = useState<Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }>>({});

  const [examDate, setExamDate] = useState(getDefaultExamDate());

  // North Star
  const [northStarData, setNorthStarData] = useState<NorthStar | null>(null);

  // Rest days
  const [restDays, setRestDays] = useState<Set<string>>(new Set());

  // ─── Navigation ─────────────────────────────────────────────────────────

  const goNext = () => { setDirection(1); setStep(s => Math.min(TOTAL_STEPS, s + 1) as Step); };
  const goBack = () => { setDirection(-1); setStep(s => Math.max(1, s - 1) as Step); };

  // ─── Subject toggle ─────────────────────────────────────────────────────

  const toggleSubject = (name: string) => {
    setSelectedSubjects(prev => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
        if (!subjectConfigs[name]) {
          setSubjectConfigs(prev => ({
            ...prev,
            [name]: { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade },
          }));
        }
      }
      return next;
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
    const subjects: StudentSubject[] = Array.from(selectedSubjects).map(name => {
      const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
      return { subjectName: name, level: config.level, currentGrade: config.currentGrade, targetGrade: config.targetGrade };
    });
    const now = new Date().toISOString();
    return {
      subjects,
      examStartDate: examDate,
      restDays: Array.from(restDays),
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

  // ─── Grouped subjects ──────────────────────────────────────────────────

  const groupedSubjects = useMemo(() => {
    const groups: Record<string, LCSubject[]> = {};
    for (const subj of LC_SUBJECTS) {
      if (!groups[subj.group]) groups[subj.group] = [];
      groups[subj.group].push(subj);
    }
    return groups;
  }, []);

  // ─── Step validation ───────────────────────────────────────────────────

  const canProceed = () => {
    switch (step) {
      case 1: return true;
      case 2: return northStarData !== null;
      case 3: return selectedSubjects.size > 0;
      case 4: {
        for (const name of selectedSubjects) {
          if (!subjectConfigs[name]) return false;
        }
        return true;
      }
      case 5: return examDate.length > 0 && getDaysUntil(examDate) > 0;
      case 6: return restDays.size < 7;
      case 7: return true;
      default: return false;
    }
  };

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, x: dir > 0 ? 50 : -50 }),
    visible: { opacity: 1, x: 0 },
    exit: (dir: number) => ({ opacity: 0, x: dir > 0 ? -50 : 50 }),
  };

  const daysLeft = getDaysUntil(examDate);
  const blobs = STEP_BLOBS[step];

  // Split welcome heading for word-by-word animation
  const welcomeWords = `Welcome, ${userName}`.split(' ');

  return (
    <div className="fixed inset-0 bg-zinc-50 dark:bg-zinc-950 flex flex-col z-[60]">

      {/* ─── Animated background blobs (step-specific colors) ─── */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <motion.div
          key={`blob-a-${step}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className={`absolute top-[15%] right-[10%] w-[500px] h-[500px] rounded-full ${blobs.a} blur-[100px]`}
          style={{ animation: 'blob-drift-1 18s ease-in-out infinite' }}
        />
        <motion.div
          key={`blob-b-${step}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.1 }}
          className={`absolute bottom-[20%] left-[5%] w-[450px] h-[450px] rounded-full ${blobs.b} blur-[100px]`}
          style={{ animation: 'blob-drift-2 22s ease-in-out infinite' }}
        />
        <motion.div
          key={`blob-c-${step}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className={`absolute top-[40%] left-[30%] w-[400px] h-[400px] rounded-full ${blobs.c} blur-[120px]`}
          style={{ animation: 'blob-drift-3 20s ease-in-out infinite' }}
        />
      </div>

      {/* Inject blob keyframes */}
      <style>{`
        @keyframes blob-drift-1 { 0%, 100% { transform: translate(0, 0) scale(1); } 33% { transform: translate(30px, -40px) scale(1.05); } 66% { transform: translate(-20px, 20px) scale(0.95); } }
        @keyframes blob-drift-2 { 0%, 100% { transform: translate(0, 0) scale(1); } 33% { transform: translate(-25px, 35px) scale(1.08); } 66% { transform: translate(35px, -15px) scale(0.92); } }
        @keyframes blob-drift-3 { 0%, 100% { transform: translate(0, 0) scale(1); } 33% { transform: translate(20px, 25px) scale(0.97); } 66% { transform: translate(-30px, -30px) scale(1.03); } }
      `}</style>

      {/* ─── Fixed Header: Progress + Skip ─── */}
      <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-zinc-200/50 dark:border-white/[0.06] relative z-10 bg-zinc-50/80 dark:bg-zinc-950/80 backdrop-blur-sm">
        <div className="flex items-center gap-2">
          {Array.from({ length: TOTAL_STEPS }, (_, i) => i + 1).map(s => (
            <motion.div
              key={s}
              layout
              className={`h-2 rounded-full ${
                s === step ? 'w-8 bg-[#CC785C]' : s < step ? 'w-4 bg-[#CC785C]/40' : 'w-4 bg-zinc-200 dark:bg-zinc-700'
              }`}
              transition={{ type: 'spring', stiffness: 500, damping: 30 }}
            />
          ))}
        </div>
        <button
          onClick={onSkip}
          className="text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
        >
          Skip for now
        </button>
      </div>

      {/* ─── Scrollable Content ─── */}
      <div className="flex-1 overflow-y-auto min-h-0 relative z-10">
        <div className="max-w-2xl mx-auto px-6 py-10">
          <AnimatePresence mode="wait" custom={direction}>

            {/* Step 1: Welcome — staggered entrance, glass card, preview chips */}
            {step === 1 && (
              <MotionDiv key="step1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-lg mx-auto p-10 rounded-3xl bg-white/60 dark:bg-zinc-900/40 backdrop-blur-xl border border-white/40 dark:border-white/[0.08] shadow-[0_8px_60px_rgba(0,0,0,0.06)] dark:shadow-[0_8px_60px_rgba(0,0,0,0.3)]">
                    {/* Word-by-word heading */}
                    <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-zinc-900 dark:text-white mb-5">
                      {welcomeWords.map((word, i) => (
                        <span key={i} className="inline-block overflow-hidden align-bottom pb-[0.1em] mb-[-0.1em]">
                          <MotionSpan
                            className="inline-block"
                            initial={{ y: '100%' }}
                            animate={{ y: 0 }}
                            transition={{ duration: 0.6, delay: 0.15 + i * 0.08, ease: [0.16, 1, 0.3, 1] }}
                          >{word}{i < welcomeWords.length - 1 ? '\u00A0' : ''}</MotionSpan>
                        </span>
                      ))}
                    </h1>

                    {/* Staggered subtitle */}
                    <MotionP
                      initial={{ opacity: 0, y: 16 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}
                      className="text-base text-zinc-500 dark:text-zinc-400 leading-relaxed max-w-md mx-auto mb-2"
                    >
                      Let's set up your study profile so we can personalise your experience from day one.
                    </MotionP>
                    <MotionP
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.65, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm text-zinc-400 dark:text-zinc-500 mb-8"
                    >
                      This takes about 2 minutes.
                    </MotionP>

                    {/* Feature preview chips */}
                    <motion.div
                      initial={{ opacity: 0, y: 16 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.8, ease: [0.16, 1, 0.3, 1] }}
                      className="grid grid-cols-2 gap-2 max-w-sm mx-auto"
                    >
                      {PREVIEW_CHIPS.map((chip, i) => (
                        <motion.div
                          key={chip.label}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.4, delay: 0.9 + i * 0.08, ease: [0.16, 1, 0.3, 1] }}
                          className="flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-full bg-white/80 dark:bg-white/[0.06] border border-zinc-200/60 dark:border-white/[0.08] text-xs font-medium text-zinc-500 dark:text-zinc-400"
                        >
                          <chip.icon size={12} className="text-[#CC785C]" />
                          {chip.label}
                        </motion.div>
                      ))}
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 2: North Star */}
            {step === 2 && (
              <MotionDiv key="step2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <NorthStarOnboarding
                  onComplete={(ns) => { setNorthStarData(ns); goNext(); }}
                  initialData={northStarData}
                />
              </MotionDiv>
            )}

            {/* Step 3: Select Subjects */}
            {step === 3 && (
              <MotionDiv key="step3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Select Your Subjects</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">
                  Tap to select your Leaving Cert subjects. <span className="font-semibold text-[#CC785C]">{selectedSubjects.size} selected</span>
                </p>
                <div className="space-y-6">
                  {Object.entries(groupedSubjects).map(([group, subjects]) => {
                    const colors = GROUP_COLORS[group as LCSubject['group']];
                    return (
                      <div key={group}>
                        <p className={`text-[10px] font-bold uppercase tracking-widest mb-3 ${colors.text}`}>
                          {SUBJECT_GROUP_LABELS[group as LCSubject['group']]}
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {subjects.map(subj => {
                            const selected = selectedSubjects.has(subj.name);
                            return (
                              <button key={subj.name} onClick={() => toggleSubject(subj.name)}
                                className={`px-3.5 py-2 rounded-full text-xs font-semibold border transition-all ${
                                  selected ? `${colors.selectedBg} ${colors.selectedBorder} ${colors.text}` : `${colors.bg} ${colors.border} text-zinc-500 dark:text-zinc-400`
                                }`}
                              >
                                {selected && <Check size={12} className="inline mr-1 -mt-0.5" />}
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

            {/* Step 4: Grade Configuration */}
            {step === 4 && (
              <MotionDiv key="step4" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Set Your Grades</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
                  For each subject, tap your <span className="font-bold text-zinc-700 dark:text-zinc-200">current</span> grade, then your <span className="font-bold text-purple-600 dark:text-purple-400">target</span>.
                </p>
                <div className="flex items-center gap-3 mb-6">
                  <span className="flex items-center gap-1.5 text-[10px] font-semibold text-zinc-500 dark:text-zinc-400">
                    <span className="w-3 h-3 rounded bg-zinc-800 dark:bg-white inline-block" /> Current
                  </span>
                  <span className="flex items-center gap-1.5 text-[10px] font-semibold text-zinc-500 dark:text-zinc-400">
                    <span className="w-3 h-3 rounded bg-purple-600 dark:bg-purple-500 inline-block" /> Target
                  </span>
                </div>

                <div className="space-y-4">
                  {Array.from(selectedSubjects).map(name => {
                    const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
                    const grades = getGradesForLevel(config.level);
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const groupColor = lcSubject ? GROUP_COLORS[lcSubject.group] : GROUP_COLORS.stem;
                    const currentIdx = getGradeIndex(config.currentGrade);
                    const targetIdx = getGradeIndex(config.targetGrade);

                    return (
                      <div key={name} className="rounded-xl bg-white/70 dark:bg-white/[0.03] backdrop-blur-sm border border-zinc-200/50 dark:border-white/[0.06] overflow-hidden">
                        {/* Subject header row */}
                        <div className="flex items-center justify-between px-4 pt-3 pb-2">
                          <span className={`text-sm font-bold ${groupColor.text}`}>{name}</span>
                          <div className="flex items-center gap-1 bg-zinc-100 dark:bg-zinc-800 rounded-lg p-0.5">
                            <button
                              onClick={() => updateConfig(name, 'level', 'higher')}
                              className={`px-2.5 py-1 rounded-md text-[10px] font-bold transition-all ${
                                config.level === 'higher'
                                  ? 'bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm'
                                  : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300'
                              }`}
                            >
                              Higher
                            </button>
                            <button
                              onClick={() => updateConfig(name, 'level', 'ordinary')}
                              className={`px-2.5 py-1 rounded-md text-[10px] font-bold transition-all ${
                                config.level === 'ordinary'
                                  ? 'bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm'
                                  : 'text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300'
                              }`}
                            >
                              Ordinary
                            </button>
                          </div>
                        </div>

                        {/* Grade pills */}
                        <div className="px-4 pb-3">
                          <div className="flex gap-1">
                            {grades.map((g, gi) => {
                              const isCurrent = g === config.currentGrade;
                              const isTarget = g === config.targetGrade;
                              const isBetween = gi > targetIdx && gi < currentIdx;

                              return (
                                <button
                                  key={g}
                                  onClick={() => {
                                    if (gi <= targetIdx) {
                                      updateConfig(name, 'targetGrade', g);
                                    } else if (gi >= currentIdx) {
                                      updateConfig(name, 'currentGrade', g);
                                    } else {
                                      updateConfig(name, 'currentGrade', g);
                                    }
                                  }}
                                  className={`flex-1 py-1.5 rounded-lg text-[11px] font-bold border transition-all ${
                                    isTarget ? getTargetGradePillClass(true)
                                    : isCurrent ? getCurrentGradePillClass(true)
                                    : isBetween ? 'bg-purple-50 dark:bg-purple-900/15 text-purple-400 dark:text-purple-500 border-purple-200 dark:border-purple-800/40'
                                    : getCurrentGradePillClass(false)
                                  }`}
                                >
                                  {g}
                                </button>
                              );
                            })}
                          </div>
                          {/* Improvement indicator */}
                          {targetIdx < currentIdx && (
                            <div className="flex items-center justify-between mt-2 px-0.5">
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

            {/* Step 5: Exam Date — glass card */}
            {step === 5 && (
              <MotionDiv key="step5" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[50vh]">
                  <div className="text-center w-full max-w-md mx-auto p-10 rounded-3xl bg-white/60 dark:bg-zinc-900/40 backdrop-blur-xl border border-white/40 dark:border-white/[0.08] shadow-[0_8px_60px_rgba(0,0,0,0.06)] dark:shadow-[0_8px_60px_rgba(0,0,0,0.3)]">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-amber-100 dark:bg-amber-900/40 flex items-center justify-center"
                    >
                      <Calendar size={32} className="text-amber-600 dark:text-amber-400" />
                    </motion.div>
                    <motion.h2
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                      className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1"
                    >
                      When Do Exams Start?
                    </motion.h2>
                    <motion.p
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm text-zinc-500 dark:text-zinc-400 mb-8"
                    >
                      We'll use this to plan your study intensity.
                    </motion.p>
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                    >
                      <input type="date" value={examDate} onChange={(e) => setExamDate(e.target.value)}
                        className="w-full max-w-xs mx-auto px-4 py-3 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white/80 dark:bg-zinc-800 backdrop-blur-sm text-center text-lg font-semibold text-zinc-900 dark:text-white"
                      />
                    </motion.div>
                    {daysLeft > 0 && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}
                        className="mt-6 p-4 rounded-xl bg-[#CC785C]/10 border border-[#CC785C]/20"
                      >
                        <p className="text-3xl font-bold font-mono text-[#CC785C]">{daysLeft}</p>
                        <p className="text-xs font-semibold text-[#CC785C]/80 uppercase tracking-widest">days to go</p>
                      </motion.div>
                    )}
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 6: Rest Days — glass card */}
            {step === 6 && (
              <MotionDiv key="step6" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[50vh]">
                  <div className="text-center w-full max-w-lg mx-auto p-10 rounded-3xl bg-white/60 dark:bg-zinc-900/40 backdrop-blur-xl border border-white/40 dark:border-white/[0.08] shadow-[0_8px_60px_rgba(0,0,0,0.06)] dark:shadow-[0_8px_60px_rgba(0,0,0,0.3)]">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-rose-100 dark:bg-rose-900/40 flex items-center justify-center"
                    >
                      <CalendarOff size={32} className="text-rose-600 dark:text-rose-400" />
                    </motion.div>
                    <motion.h2
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                      className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1"
                    >
                      Rest Days
                    </motion.h2>
                    <motion.p
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm text-zinc-500 dark:text-zinc-400 mb-8"
                    >
                      Tap any days where study isn't possible. Your sessions will be redistributed across the remaining days.
                    </motion.p>

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
                            className={`flex flex-col items-center gap-1.5 py-3.5 rounded-xl border-2 transition-all ${
                              isRest
                                ? 'bg-rose-50 dark:bg-rose-900/30 border-rose-400 dark:border-rose-500 text-rose-600 dark:text-rose-400'
                                : 'bg-white/80 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:border-zinc-400 dark:hover:border-zinc-500'
                            }`}
                          >
                            <span className="text-[10px] font-bold uppercase">{DAY_SHORTS[day]}</span>
                            {isRest ? <CalendarOff size={14} className="text-rose-500 dark:text-rose-400" /> : <Check size={14} className="text-emerald-500 dark:text-emerald-400" />}
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

            {/* Step 7: Summary */}
            {step === 7 && (
              <MotionDiv key="step7" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Your Study Profile</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">Here's a summary of everything you've set up.</p>

                {/* Projected points banner — current → target with animated gain */}
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                  className="p-6 rounded-2xl bg-white/70 dark:bg-white/[0.04] backdrop-blur-xl border border-zinc-200/50 dark:border-white/[0.08] shadow-[0_4px_40px_rgba(0,0,0,0.04)] dark:shadow-[0_4px_40px_rgba(0,0,0,0.2)] text-center mb-6"
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
                    <p className="text-[10px] font-bold uppercase tracking-widest text-[#CC785C]/70 mb-1">Projected Gain</p>
                    <p className="text-4xl font-bold font-mono text-[#CC785C]">
                      <AnimatedNumber value={pointsTotals.gain} prefix={pointsTotals.gain > 0 ? '+' : ''} delay={0.6} />
                    </p>
                  </div>
                </motion.div>

                {/* Subject summary */}
                <div className="space-y-2 mb-6">
                  {Array.from(selectedSubjects).map((name, i) => {
                    const config = subjectConfigs[name];
                    if (!config) return null;
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const isMaths = lcSubject?.isMaths || false;
                    const currentPts = getPointsForGrade(config.currentGrade, isMaths);
                    const targetPts = getPointsForGrade(config.targetGrade, isMaths);
                    const gain = targetPts - currentPts;

                    return (
                      <motion.div
                        key={name}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: 0.2 + i * 0.04, ease: [0.16, 1, 0.3, 1] }}
                        className="flex items-center justify-between p-3 rounded-xl bg-white/70 dark:bg-white/[0.03] backdrop-blur-sm border border-zinc-200/50 dark:border-white/[0.06]"
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
                          <span className="text-xs font-bold text-purple-600 dark:text-purple-400">{config.targetGrade}</span>
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
                  <span className="flex items-center gap-1.5"><Calendar size={14} /> {daysLeft} days left</span>
                  <span className="flex items-center gap-1.5"><CalendarOff size={14} /> {restDays.size} rest {restDays.size === 1 ? 'day' : 'days'}</span>
                </motion.div>
              </MotionDiv>
            )}

          </AnimatePresence>
        </div>
      </div>

      {/* ─── Fixed Footer: Back / Continue (hidden on step 2 — North Star has its own nav) ─── */}
      {step !== 2 && (
        <div className="shrink-0 border-t border-zinc-200/50 dark:border-white/[0.06] px-6 py-4 relative z-10 bg-zinc-50/80 dark:bg-zinc-950/80 backdrop-blur-sm">
          <div className="max-w-2xl mx-auto flex items-center justify-between">
            {step > 1 ? (
              <button onClick={goBack} className="flex items-center gap-1.5 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
                <ArrowLeft size={14} /> Back
              </button>
            ) : <div />}

            {step < TOTAL_STEPS ? (
              <button onClick={goNext} disabled={!canProceed()}
                className="flex items-center gap-2 px-7 py-2.5 bg-[#CC785C] text-white font-semibold text-sm rounded-full hover:bg-[#B56A50] transition-colors disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-[#CC785C]/20"
              >
                {step === 1 ? 'Get Started' : 'Continue'} <ArrowRight size={14} />
              </button>
            ) : (
              <button onClick={() => onComplete(buildProfile(), northStarData ?? undefined)}
                className="flex items-center gap-2 px-7 py-2.5 bg-[#CC785C] text-white font-semibold text-sm rounded-full hover:bg-[#B56A50] transition-colors shadow-lg shadow-[#CC785C]/20"
              >
                <Check size={14} /> Save & Start Learning
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Onboarding;
