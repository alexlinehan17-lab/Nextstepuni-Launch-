/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv, MotionP, MotionSpan } from './Motion';
import { ArrowRight, ArrowLeft, Check, Calendar, CalendarOff, BookOpen, Target, CalendarDays, Star } from 'lucide-react';
import PrimaryActionButton from './ui/PrimaryActionButton';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  type YearGroup,
  LC_SUBJECTS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
  getGradeIndex, DAYS_OF_WEEK,
  type LCSubject,
} from './subjectData';
import { type NorthStar } from '../types';
import NorthStarOnboarding from './NorthStarOnboarding';

interface OnboardingProps {
  userName: string;
  onComplete: (profile: StudentSubjectProfile, northStar?: NorthStar) => void;
  onSkip: () => void;
}

type Step = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
const TOTAL_STEPS = 9;

// ─── Step-specific ambient blob colors ──────────────────────────────────────

const _STEP_BLOBS: Record<Step, { a: string; b: string; c: string }> = {
  1: { a: 'bg-[rgba(var(--accent),0.07)]', b: 'bg-yellow-300/[0.09]', c: 'bg-orange-200/[0.08]' },
  2: { a: 'bg-indigo-300/[0.08]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-sky-200/[0.06]' },
  3: { a: 'bg-purple-300/[0.08]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-amber-200/[0.06]' },
  4: { a: 'bg-blue-300/[0.08]', b: 'bg-emerald-300/[0.07]', c: 'bg-purple-200/[0.06]' },
  5: { a: 'bg-emerald-300/[0.08]', b: 'bg-amber-300/[0.07]', c: 'bg-blue-200/[0.06]' },
  6: { a: 'bg-amber-300/[0.09]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-yellow-200/[0.08]' },
  7: { a: 'bg-rose-300/[0.08]', b: 'bg-orange-200/[0.07]', c: 'bg-pink-200/[0.06]' },
  8: { a: 'bg-emerald-300/[0.09]', b: 'bg-[rgba(var(--accent),0.07)]', c: 'bg-amber-200/[0.06]' },
  9: { a: 'bg-rose-300/[0.08]', b: 'bg-indigo-300/[0.07]', c: 'bg-emerald-200/[0.06]' },
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
    ? 'bg-teal-600 dark:bg-teal-500 text-white border-teal-600 dark:border-teal-500 shadow-sm'
    : 'bg-white dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:border-teal-400 dark:hover:border-teal-500';
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

  // Year group
  const [yearGroup, setYearGroup] = useState<YearGroup | null>(null);

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
      yearGroup: yearGroup ?? '6th',
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
      case 2: return yearGroup !== null;
      case 3: return northStarData !== null;
      case 4: return selectedSubjects.size > 0;
      case 5: {
        for (const name of selectedSubjects) {
          if (!subjectConfigs[name]) return false;
        }
        return true;
      }
      case 6: return examDate.length > 0 && getDaysUntil(examDate) > 0;
      case 7: return restDays.size < 7;
      case 8: return true;
      case 9: return true;
      default: return false;
    }
  };

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, x: dir > 0 ? 50 : -50 }),
    visible: { opacity: 1, x: 0 },
    exit: (dir: number) => ({ opacity: 0, x: dir > 0 ? -50 : 50 }),
  };

  const daysLeft = getDaysUntil(examDate);

  // Split welcome heading for word-by-word animation
  const welcomeWords = `Welcome, ${userName}`.split(' ');

  return (
    <div className="fixed inset-0 flex flex-col z-[60] overflow-hidden">

      {/* ─── Solid background — matches Library (module selection) screen ─── */}
      <div className="fixed inset-0 pointer-events-none dark:bg-zinc-900" aria-hidden="true" style={{ backgroundColor: '#FDF8F0' }} />

      {/* ─── Fixed Header: Progress bar + Skip ─── */}
      <div className="shrink-0 relative z-10 px-6 pt-5 pb-3">
        <div className="flex items-center justify-end mb-3">
          <button
            onClick={onSkip}
            className="text-sm font-medium transition-colors text-[#A8A29E] dark:text-zinc-500"
          >
            Skip for now
          </button>
        </div>
        <div className="max-w-md mx-auto">
          <div className="w-full h-[5px] rounded-full overflow-hidden" style={{ backgroundColor: 'rgba(0,0,0,0.08)' }}>
            <motion.div
              className="h-full rounded-full bg-[#1A1A1A] dark:bg-white"
              animate={{ width: `${(step / TOTAL_STEPS) * 100}%` }}
              transition={{ duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
            />
          </div>
        </div>
      </div>

      {/* ─── Scrollable Content ─── */}
      <div className="flex-1 overflow-y-auto min-h-0 relative z-10">
        <div className="max-w-2xl mx-auto px-6 py-10">
          <AnimatePresence mode="wait" custom={direction}>

            {/* Step 1: Welcome — staggered entrance, glass card, preview chips */}
            {step === 1 && (
              <MotionDiv key="step1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-lg mx-auto">
                    {/* Word-by-word heading */}
                    <h1 className="font-serif text-3xl sm:text-4xl font-bold mb-5 text-[#1A1A1A] dark:text-white">
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
                      className="text-base leading-relaxed max-w-md mx-auto mb-2 text-[#78716C] dark:text-zinc-400"
                    >
                      Let's set up your study profile so we can personalise your experience from day one.
                    </MotionP>
                    <MotionP
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.65, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm mb-8 text-[#A8A29E] dark:text-zinc-500"
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
                          className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium"
                          style={{ backgroundColor: 'rgba(255,255,255,0.85)', border: '1px solid rgba(0,0,0,0.06)', color: '#57534E' }}
                        >
                          <chip.icon size={12} style={{ color: '#2A7D6F' }} />
                          {chip.label}
                        </motion.div>
                      ))}
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 2: Year Group */}
            {step === 2 && (
              <MotionDiv key="step2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-lg mx-auto">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-16 h-16 mx-auto mb-6 rounded-2xl flex items-center justify-center"
                      style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}
                    >
                      <BookOpen size={32} style={{ color: '#2A7D6F' }} />
                    </motion.div>
                    <motion.h2
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                      className="font-serif text-2xl font-bold mb-1 text-[#1A1A1A] dark:text-white"
                    >
                      What Year Are You In?
                    </motion.h2>
                    <motion.p
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm mb-8 text-[#78716C] dark:text-zinc-400"
                    >
                      This helps us show you the right events and deadlines for your year group.
                    </motion.p>
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      className="flex gap-4 justify-center"
                    >
                      {(['5th', '6th'] as const).map(yr => (
                        <button
                          key={yr}
                          onClick={() => setYearGroup(yr)}
                          className="w-36 py-6 rounded-2xl transition-all"
                          style={{
                            backgroundColor: yearGroup === yr ? 'rgba(42,125,111,0.08)' : 'rgba(255,255,255,0.85)',
                            border: yearGroup === yr ? '2px solid #2A7D6F' : '1px solid rgba(0,0,0,0.08)',
                            boxShadow: yearGroup === yr ? '0 0 0 3px rgba(42,125,111,0.1)' : 'none',
                          }}
                        >
                          <p className={`text-3xl font-bold mb-1 ${yearGroup === yr ? 'text-[#2A7D6F]' : 'text-[#1A1A1A] dark:text-white'}`}>{yr}</p>
                          <p className={`text-xs font-medium ${yearGroup === yr ? 'text-[#2A7D6F]' : 'text-[#A8A29E] dark:text-zinc-500'}`}>Year</p>
                        </button>
                      ))}
                    </motion.div>
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 3: North Star */}
            {step === 3 && (
              <MotionDiv key="step3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <NorthStarOnboarding
                  onComplete={(ns) => { setNorthStarData(ns); goNext(); }}
                  initialData={northStarData}
                />
              </MotionDiv>
            )}

            {/* Step 4: Select Subjects */}
            {step === 4 && (
              <MotionDiv key="step4" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-2xl font-bold text-center mb-1 text-[#1A1A1A] dark:text-white">Select Your Subjects</h2>
                <p className="text-sm text-center mb-8 text-[#78716C] dark:text-zinc-400">
                  Tap to select your Leaving Cert subjects. <span className="font-semibold text-[var(--accent-hex)]">{selectedSubjects.size} selected</span>
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
                                className="px-3.5 py-2 rounded-full text-xs font-semibold transition-all"
                                style={{
                                  backgroundColor: selected ? 'rgba(42,125,111,0.08)' : 'rgba(255,255,255,0.85)',
                                  border: selected ? '2px solid #2A7D6F' : '1px solid rgba(0,0,0,0.08)',
                                  color: selected ? '#2A7D6F' : '#57534E',
                                }}
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

            {/* Step 5: Grade Configuration */}
            {step === 5 && (
              <MotionDiv key="step5" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-2xl font-bold text-center mb-1 text-[#1A1A1A] dark:text-white">Set Your Grades</h2>
                <p className="text-sm text-center mb-6 text-[#78716C] dark:text-zinc-400">
                  For each subject, set where you are now and where you want to be.
                </p>

                <div className="space-y-4">
                  {Array.from(selectedSubjects).map(name => {
                    const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
                    const grades = getGradesForLevel(config.level);
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const groupColor = lcSubject ? GROUP_COLORS[lcSubject.group] : GROUP_COLORS.stem;
                    const currentIdx = getGradeIndex(config.currentGrade);
                    const targetIdx = getGradeIndex(config.targetGrade);

                    return (
                      <div key={name} className="rounded-xl overflow-hidden" style={{ backgroundColor: 'rgba(255,255,255,0.9)', border: '1px solid rgba(0,0,0,0.06)' }}>
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

                        {/* Two-row grade selection */}
                        <div className="px-4 pb-3 space-y-2">
                          {/* Current grade row */}
                          <div>
                            <p className="text-[10px] font-semibold text-zinc-500 dark:text-zinc-400 mb-1">Where I am now</p>
                            <div className="flex gap-1">
                              {grades.map((g, _gi) => (
                                <button
                                  key={g}
                                  onClick={() => updateConfig(name, 'currentGrade', g)}
                                  className={`flex-1 py-1.5 rounded-lg text-[11px] font-bold border transition-all ${
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
                            <p className="text-[10px] font-semibold text-teal-600 dark:text-teal-400 mb-1">My target</p>
                            <div className="flex gap-1">
                              {grades.map((g, gi) => {
                                const disabled = gi > currentIdx;
                                return (
                                  <button
                                    key={g}
                                    onClick={() => { if (!disabled) updateConfig(name, 'targetGrade', g); }}
                                    disabled={disabled}
                                    className={`flex-1 py-1.5 rounded-lg text-[11px] font-bold border transition-all ${
                                      disabled
                                        ? 'bg-zinc-50 dark:bg-zinc-900 text-zinc-300 dark:text-zinc-700 border-zinc-100 dark:border-zinc-800 cursor-not-allowed'
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

            {/* Step 6: Exam Date — glass card */}
            {step === 6 && (
              <MotionDiv key="step6" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[65vh]">
                  <div className="text-center w-full max-w-md mx-auto">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-14 h-14 mx-auto mb-5 rounded-2xl flex items-center justify-center"
                      style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}
                    >
                      <Calendar size={28} style={{ color: '#2A7D6F' }} />
                    </motion.div>
                    <motion.h2
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                      className="font-serif text-2xl font-bold mb-1 text-[#1A1A1A] dark:text-white"
                    >
                      When Do Exams Start?
                    </motion.h2>
                    <motion.p
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm mb-6 text-[#78716C] dark:text-zinc-400"
                    >
                      We'll use this to plan your study intensity.
                    </motion.p>
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                    >
                      <input type="date" value={examDate} onChange={(e) => setExamDate(e.target.value)}
                        className="w-full max-w-xs mx-auto px-4 py-3 rounded-xl text-center text-lg font-semibold text-[#1A1A1A] dark:text-white"
                        style={{ backgroundColor: 'rgba(255,255,255,0.9)', border: '1px solid rgba(0,0,0,0.08)' }}
                      />
                    </motion.div>
                    {daysLeft > 0 && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}
                        className="mt-8 inline-flex flex-col items-center px-10 py-6 rounded-3xl"
                        style={{ backgroundColor: 'rgba(255,255,255,0.5)', backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)', border: '1px solid rgba(255,255,255,0.6)' }}
                      >
                        <p className="font-apercu font-black text-[#1A1A1A] dark:text-white" style={{ fontSize: 'clamp(64px, 15vw, 100px)', lineHeight: 1 }}>{daysLeft}</p>
                        <p className="text-sm font-bold uppercase tracking-widest mt-1 text-[#A8A29E] dark:text-zinc-500">days to go</p>
                      </motion.div>
                    )}
                  </div>
                </div>
              </MotionDiv>
            )}

            {/* Step 7: Rest Days — glass card */}
            {step === 7 && (
              <MotionDiv key="step7" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[50vh]">
                  <div className="text-center w-full max-w-lg mx-auto">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-16 h-16 mx-auto mb-6 rounded-2xl flex items-center justify-center"
                      style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}
                    >
                      <CalendarOff size={32} style={{ color: '#2A7D6F' }} />
                    </motion.div>
                    <motion.h2
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                      className="font-serif text-2xl font-bold mb-1 text-[#1A1A1A] dark:text-white"
                    >
                      Rest Days
                    </motion.h2>
                    <motion.p
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
                      className="text-sm mb-8 text-[#78716C] dark:text-zinc-400"
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
                            className={`flex flex-col items-center gap-1.5 py-3.5 rounded-xl transition-all ${isRest ? '' : 'text-[#1A1A1A] dark:text-white'}`}
                            style={{
                              backgroundColor: isRest ? 'rgba(220,38,38,0.06)' : 'rgba(255,255,255,0.9)',
                              border: isRest ? '2px solid #DC2626' : '1px solid rgba(0,0,0,0.08)',
                              ...(isRest ? { color: '#DC2626' } : {}),
                            }}
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

            {/* Step 8: Summary */}
            {step === 8 && (
              <MotionDiv key="step8" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
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
                    <p className="text-[10px] font-bold uppercase tracking-widest text-[rgba(var(--accent),0.7)] mb-1">Projected Gain</p>
                    <p className="text-4xl font-bold font-mono text-[var(--accent-hex)]">
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
                          <span className="text-xs font-bold text-teal-600 dark:text-teal-400">{config.targetGrade}</span>
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

            {/* Step 9: You're All Set — celebratory completion */}
            {step === 9 && (
              <MotionDiv key="step9" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="flex items-center justify-center min-h-[60vh]">
                  <div className="text-center w-full max-w-md mx-auto">
                    {/* Checkmark icon */}
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                      className="w-16 h-16 mx-auto mb-6 rounded-full flex items-center justify-center"
                      style={{ backgroundColor: '#2A7D6F' }}
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
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Target</p>
                          <p className="text-3xl font-apercu font-black text-[#1A1A1A] dark:text-white">
                            <AnimatedNumber value={pointsTotals.target} delay={0.7} />
                          </p>
                          <p className="text-[11px] text-[#A8A29E] dark:text-zinc-500">CAO pts</p>
                        </div>
                        <div className="w-px h-12" style={{ backgroundColor: 'rgba(0,0,0,0.08)' }} />
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
                        onClick={() => onComplete(buildProfile(), northStarData ?? undefined)}
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

      {/* ─── Fixed Footer: Back / Continue (hidden on step 3 — North Star has its own nav) ─── */}
      {step !== 3 && step !== 9 && (
        <div className="shrink-0 px-6 py-5 relative z-10">
          <div className="max-w-2xl mx-auto flex flex-col items-center gap-3">
            {step < TOTAL_STEPS ? (
              <button onClick={goNext} disabled={!canProceed()}
                className="flex items-center gap-2 px-8 py-3 font-semibold text-sm rounded-2xl transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                style={{ backgroundColor: 'rgba(0,0,0,0.65)', color: '#fff', minWidth: 160 }}
              >
                <span className="flex-1 text-center">{step === 1 ? 'Get Started' : 'Next'}</span>
                <ArrowRight size={14} />
              </button>
            ) : (
              <button onClick={() => onComplete(buildProfile(), northStarData ?? undefined)}
                className="flex items-center gap-2 px-8 py-3 rounded-2xl font-semibold text-sm transition-all active:scale-[0.98]"
                style={{ backgroundColor: '#2A7D6F', color: '#fff', minWidth: 160 }}
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
