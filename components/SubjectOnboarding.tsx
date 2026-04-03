/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { X, ArrowRight, ArrowLeft, Check, Calendar, GraduationCap, CalendarOff } from 'lucide-react';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
  getGradeIndex, DAYS_OF_WEEK,
  type LCSubject,
} from './subjectData';

interface SubjectOnboardingProps {
  user: { uid: string };
  existingProfile?: StudentSubjectProfile;
  onComplete: (profile: StudentSubjectProfile) => void;
  onClose: () => void;
}

type Step = 1 | 2 | 3 | 4 | 5 | 6;
const TOTAL_STEPS = 6;

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

// ─── Component ──────────────────────────────────────────────────────────────

const SubjectOnboarding: React.FC<SubjectOnboardingProps> = ({ user, existingProfile, onComplete, onClose }) => {
  const isEditMode = !!existingProfile;

  const [step, setStep] = useState<Step>(isEditMode ? 2 : 1);
  const [direction, setDirection] = useState(1);

  // Subject selection
  const [selectedSubjects, setSelectedSubjects] = useState<Set<string>>(() => {
    if (existingProfile) return new Set(existingProfile.subjects.map(s => s.subjectName));
    return new Set<string>();
  });

  // Grade configs
  const [subjectConfigs, setSubjectConfigs] = useState<Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }>>(() => {
    if (existingProfile) {
      const configs: Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }> = {};
      for (const s of existingProfile.subjects) {
        configs[s.subjectName] = { level: s.level, currentGrade: s.currentGrade, targetGrade: s.targetGrade };
      }
      return configs;
    }
    return {};
  });

  const [examDate, setExamDate] = useState(existingProfile?.examStartDate || getDefaultExamDate());

  // Rest days
  const [restDays, setRestDays] = useState<Set<string>>(() => {
    if (existingProfile?.restDays) return new Set(existingProfile.restDays);
    return new Set<string>();
  });

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
      createdAt: existingProfile?.createdAt || now,
      updatedAt: now,
    };
  };

  // ─── Projected points gain ──────────────────────────────────────────────

  const projectedGain = useMemo(() => {
    let totalCurrentPoints = 0;
    let totalTargetPoints = 0;
    for (const name of selectedSubjects) {
      const config = subjectConfigs[name];
      if (!config) continue;
      const lcSubject = LC_SUBJECTS.find(s => s.name === name);
      const isMaths = lcSubject?.isMaths || false;
      totalCurrentPoints += getPointsForGrade(config.currentGrade, isMaths);
      totalTargetPoints += getPointsForGrade(config.targetGrade, isMaths);
    }
    return totalTargetPoints - totalCurrentPoints;
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
      case 2: return selectedSubjects.size > 0;
      case 3: {
        for (const name of selectedSubjects) {
          if (!subjectConfigs[name]) return false;
        }
        return true;
      }
      case 4: return examDate.length > 0 && getDaysUntil(examDate) > 0;
      case 5: return restDays.size < 7; // must have at least 1 study day
      case 6: return true;
      default: return false;
    }
  };

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, x: dir > 0 ? 50 : -50 }),
    visible: { opacity: 1, x: 0 },
    exit: (dir: number) => ({ opacity: 0, x: dir > 0 ? -50 : 50 }),
  };

  const daysLeft = getDaysUntil(examDate);

  return (
    <MotionDiv
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4"
      onClick={onClose}
    >
      <MotionDiv
        initial={{ scale: 0.96, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.96, opacity: 0 }}
        transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
        className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-lg shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[90vh] flex flex-col"
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        {/* Close */}
        <button onClick={onClose} className="absolute top-5 right-5 text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors z-10">
          <X size={18} />
        </button>

        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2 pt-6 px-8">
          {Array.from({ length: TOTAL_STEPS }, (_, i) => i + 1).map(s => (
            <div key={s} className={`h-1.5 rounded-full transition-all duration-300 ${
              s === step ? 'w-8 bg-purple-500' : s < step ? 'w-4 bg-purple-300 dark:bg-purple-700' : 'w-4 bg-zinc-200 dark:bg-zinc-700'
            }`} />
          ))}
        </div>

        {/* Content */}
        <div className="p-8 flex-1 overflow-y-auto min-h-0">
          <AnimatePresence mode="wait" custom={direction}>

            {/* Step 1: Welcome */}
            {step === 1 && (
              <MotionDiv key="step1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="text-center py-6">
                  <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-purple-100 dark:bg-purple-900/40 flex items-center justify-center">
                    <GraduationCap size={32} className="text-purple-600 dark:text-purple-400" />
                  </div>
                  <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-3">Set Up Your Subjects</h2>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed max-w-sm mx-auto">
                    Tell us about your Leaving Cert subjects to power all Innovation Zone tools. This takes about 2 minutes.
                  </p>
                </div>
              </MotionDiv>
            )}

            {/* Step 2: Select Subjects */}
            {step === 2 && (
              <MotionDiv key="step2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">Select Your Subjects</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
                  Tap to select. <span className="font-semibold text-purple-600 dark:text-purple-400">{selectedSubjects.size} selected</span>
                </p>
                <div className="space-y-5">
                  {Object.entries(groupedSubjects).map(([group, subjects]) => {
                    const colors = GROUP_COLORS[group as LCSubject['group']];
                    return (
                      <div key={group}>
                        <p className={`text-[10px] font-bold uppercase tracking-widest mb-2 ${colors.text}`}>
                          {SUBJECT_GROUP_LABELS[group as LCSubject['group']]}
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {subjects.map(subj => {
                            const selected = selectedSubjects.has(subj.name);
                            return (
                              <button key={subj.name} onClick={() => toggleSubject(subj.name)}
                                className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
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

            {/* Step 3: Grade Configuration — Segmented pill buttons */}
            {step === 3 && (
              <MotionDiv key="step3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">Set Your Grades</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
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
                      <div key={name} className="rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] overflow-hidden">
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
                              {grades.map((g) => (
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
                            <p className="text-[10px] font-semibold text-purple-600 dark:text-purple-400 mb-1">My target</p>
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

            {/* Step 4: Exam Date */}
            {step === 4 && (
              <MotionDiv key="step4" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="text-center py-4">
                  <div className="w-14 h-14 mx-auto mb-5 rounded-2xl bg-amber-100 dark:bg-amber-900/40 flex items-center justify-center">
                    <Calendar size={28} className="text-amber-600 dark:text-amber-400" />
                  </div>
                  <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">When Do Exams Start?</h2>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">We'll use this to plan your study intensity.</p>
                  <input type="date" value={examDate} onChange={(e) => setExamDate(e.target.value)}
                    className="w-full max-w-xs mx-auto px-4 py-3 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-center text-lg font-semibold text-zinc-900 dark:text-white"
                  />
                  {daysLeft > 0 && (
                    <div className="mt-6 p-4 rounded-xl bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30">
                      <p className="text-3xl font-bold font-mono text-purple-600 dark:text-purple-400">{daysLeft}</p>
                      <p className="text-xs font-semibold text-purple-500 dark:text-purple-400 uppercase tracking-widest">days to go</p>
                    </div>
                  )}
                </div>
              </MotionDiv>
            )}

            {/* Step 5: Rest Days */}
            {step === 5 && (
              <MotionDiv key="step5" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <div className="text-center py-2">
                  <div className="w-14 h-14 mx-auto mb-5 rounded-2xl bg-rose-100 dark:bg-rose-900/40 flex items-center justify-center">
                    <CalendarOff size={28} className="text-rose-600 dark:text-rose-400" />
                  </div>
                  <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">Rest Days</h2>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">Tap any days where study isn't possible. Your sessions will be redistributed across the remaining days.</p>

                  <div className="grid grid-cols-7 gap-2 max-w-sm mx-auto">
                    {DAYS_OF_WEEK.map(day => {
                      const isRest = restDays.has(day);
                      return (
                        <button
                          key={day}
                          onClick={() => toggleRestDay(day)}
                          className={`flex flex-col items-center gap-1 py-3 rounded-xl border-2 transition-all ${
                            isRest
                              ? 'bg-rose-50 dark:bg-rose-900/30 border-rose-400 dark:border-rose-500 text-rose-600 dark:text-rose-400'
                              : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:border-zinc-400 dark:hover:border-zinc-500'
                          }`}
                        >
                          <span className="text-[10px] font-bold uppercase">{DAY_SHORTS[day]}</span>
                          {isRest && <X size={14} className="text-rose-500 dark:text-rose-400" />}
                          {!isRest && <Check size={14} className="text-emerald-500 dark:text-emerald-400" />}
                        </button>
                      );
                    })}
                  </div>

                  <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-6">
                    {7 - restDays.size} study {7 - restDays.size === 1 ? 'day' : 'days'} per week{restDays.size > 0 ? ` — ${restDays.size} rest ${restDays.size === 1 ? 'day' : 'days'}` : ''}
                  </p>
                </div>
              </MotionDiv>
            )}

            {/* Step 6: Summary */}
            {step === 6 && (
              <MotionDiv key="step6" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">Your Study Profile</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">Review your subjects and grades before saving.</p>

                <div className="space-y-2 mb-6">
                  {Array.from(selectedSubjects).map(name => {
                    const config = subjectConfigs[name];
                    if (!config) return null;
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const isMaths = lcSubject?.isMaths || false;
                    const currentPts = getPointsForGrade(config.currentGrade, isMaths);
                    const targetPts = getPointsForGrade(config.targetGrade, isMaths);
                    const gain = targetPts - currentPts;

                    return (
                      <div key={name} className="flex items-center justify-between p-3 rounded-lg bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]">
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
                      </div>
                    );
                  })}
                </div>

                {/* Projected total gain */}
                <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-700/30 text-center mb-4">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-emerald-600 dark:text-emerald-400 mb-1">Projected CAO Points Gain</p>
                  <p className="text-3xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                    {projectedGain > 0 ? `+${projectedGain}` : projectedGain}
                  </p>
                </div>

                <div className="flex items-center justify-center gap-4 text-xs text-zinc-400 dark:text-zinc-500">
                  <span className="flex items-center gap-1"><Calendar size={12} /> {daysLeft} days left</span>
                  <span className="flex items-center gap-1"><CalendarOff size={12} /> {restDays.size} rest {restDays.size === 1 ? 'day' : 'days'}</span>
                </div>
              </MotionDiv>
            )}

          </AnimatePresence>
        </div>

        {/* Footer */}
        <div className="p-6 pt-0 flex items-center justify-between gap-3">
          {step > 1 ? (
            <button onClick={goBack} className="flex items-center gap-1.5 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
              <ArrowLeft size={14} /> Back
            </button>
          ) : <div />}

          {step < TOTAL_STEPS ? (
            <button onClick={goNext} disabled={!canProceed()}
              className="flex items-center gap-2 px-6 py-2.5 bg-purple-600 dark:bg-purple-500 text-white font-semibold text-sm rounded-xl hover:bg-purple-700 dark:hover:bg-purple-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {step === 1 ? 'Get Started' : 'Continue'} <ArrowRight size={14} />
            </button>
          ) : (
            <button onClick={() => onComplete(buildProfile())}
              className="flex items-center gap-2 px-6 py-2.5 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold text-sm rounded-xl hover:bg-emerald-700 dark:hover:bg-emerald-600 transition-colors"
            >
              <Check size={14} /> {isEditMode ? 'Update & Save' : 'Save & Continue'}
            </button>
          )}
        </div>
      </MotionDiv>
    </MotionDiv>
  );
};

export default SubjectOnboarding;
