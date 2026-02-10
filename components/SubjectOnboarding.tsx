/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ArrowRight, ArrowLeft, Check, BookOpen, Calendar, GraduationCap, ChevronDown } from 'lucide-react';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
  getGradeIndex, isValidTarget,
  type LCSubject,
} from './subjectData';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

interface SubjectOnboardingProps {
  user: { uid: string };
  existingProfile?: StudentSubjectProfile;
  onComplete: (profile: StudentSubjectProfile) => void;
  onClose: () => void;
}

type Step = 1 | 2 | 3 | 4 | 5;

// ─── Subject Color Map (literal Tailwind strings for CDN) ───────────────────

const GROUP_COLORS: Record<LCSubject['group'], { bg: string; border: string; text: string; selectedBg: string; selectedBorder: string }> = {
  languages: { bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300', selectedBg: 'bg-blue-100 dark:bg-blue-900/40', selectedBorder: 'border-blue-400 dark:border-blue-500' },
  stem: { bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300', selectedBg: 'bg-emerald-100 dark:bg-emerald-900/40', selectedBorder: 'border-emerald-400 dark:border-emerald-500' },
  business: { bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300', selectedBg: 'bg-amber-100 dark:bg-amber-900/40', selectedBorder: 'border-amber-400 dark:border-amber-500' },
  humanities: { bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300', selectedBg: 'bg-purple-100 dark:bg-purple-900/40', selectedBorder: 'border-purple-400 dark:border-purple-500' },
  practical: { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300', selectedBg: 'bg-orange-100 dark:bg-orange-900/40', selectedBorder: 'border-orange-400 dark:border-orange-500' },
  creative: { bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300', selectedBg: 'bg-rose-100 dark:bg-rose-900/40', selectedBorder: 'border-rose-400 dark:border-rose-500' },
};

// ─── Helpers ────────────────────────────────────────────────────────────────

function getDefaultExamDate(): string {
  // First Wednesday of June in current year
  const year = new Date().getFullYear();
  const june1 = new Date(year, 5, 1); // June 1
  const dayOfWeek = june1.getDay(); // 0=Sun
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

// ─── Component ──────────────────────────────────────────────────────────────

const SubjectOnboarding: React.FC<SubjectOnboardingProps> = ({ user, existingProfile, onComplete, onClose }) => {
  const isEditMode = !!existingProfile;

  // Step state
  const [step, setStep] = useState<Step>(isEditMode ? 2 : 1);
  const [direction, setDirection] = useState(1);

  // Subject selection
  const [selectedSubjects, setSelectedSubjects] = useState<Set<string>>(() => {
    if (existingProfile) {
      return new Set(existingProfile.subjects.map(s => s.subjectName));
    }
    return new Set<string>();
  });

  // Grade configuration per subject
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

  // Exam date
  const [examDate, setExamDate] = useState(existingProfile?.examStartDate || getDefaultExamDate());

  // ─── Navigation ─────────────────────────────────────────────────────────

  const goNext = () => {
    setDirection(1);
    setStep(s => Math.min(5, s + 1) as Step);
  };
  const goBack = () => {
    setDirection(-1);
    setStep(s => Math.max(1, s - 1) as Step);
  };

  // ─── Subject toggle ─────────────────────────────────────────────────────

  const toggleSubject = (name: string) => {
    setSelectedSubjects(prev => {
      const next = new Set(prev);
      if (next.has(name)) {
        next.delete(name);
      } else {
        next.add(name);
        // Initialize config if not present
        if (!subjectConfigs[name]) {
          const lcSubject = LC_SUBJECTS.find(s => s.name === name);
          const defaultLevel: Level = 'higher';
          setSubjectConfigs(prev => ({
            ...prev,
            [name]: { level: defaultLevel, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade },
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
        // Reset grades to sensible defaults for new level
        const grades = getGradesForLevel(newLevel);
        next.currentGrade = grades[3]; // 4th grade
        next.targetGrade = grades[1]; // 2nd grade
      } else if (field === 'currentGrade') {
        next.currentGrade = value as Grade;
        // If target is now worse than current, adjust
        if (getGradeIndex(next.targetGrade) > getGradeIndex(value as Grade)) {
          // target index is higher (worse), keep as is but it'll be invalid — user can fix
        }
        if (getGradeIndex(next.targetGrade) > getGradeIndex(next.currentGrade)) {
          next.targetGrade = next.currentGrade;
        }
      } else {
        next.targetGrade = value as Grade;
      }

      return { ...prev, [subjectName]: next };
    });
  };

  // ─── Build final profile ────────────────────────────────────────────────

  const buildProfile = (): StudentSubjectProfile => {
    const subjects: StudentSubject[] = Array.from(selectedSubjects).map(name => {
      const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
      return {
        subjectName: name,
        level: config.level,
        currentGrade: config.currentGrade,
        targetGrade: config.targetGrade,
      };
    });

    const now = new Date().toISOString();
    return {
      subjects,
      examStartDate: examDate,
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
          const config = subjectConfigs[name];
          if (!config) return false;
        }
        return true;
      }
      case 4: return examDate.length > 0 && getDaysUntil(examDate) > 0;
      case 5: return true;
      default: return false;
    }
  };

  // ─── Animation variants ─────────────────────────────────────────────────

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, x: dir > 0 ? 50 : -50 }),
    visible: { opacity: 1, x: 0 },
    exit: (dir: number) => ({ opacity: 0, x: dir > 0 ? -50 : 50 }),
  };

  const daysLeft = getDaysUntil(examDate);

  // ─── Render ─────────────────────────────────────────────────────────────

  return (
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4"
      onClick={onClose}
    >
      <MotionDiv
        initial={{ scale: 0.96, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.96, opacity: 0 }}
        transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
        className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-lg shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[90vh] flex flex-col"
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        {/* Close button */}
        <button onClick={onClose} className="absolute top-5 right-5 text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors z-10">
          <X size={18} />
        </button>

        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2 pt-6 px-8">
          {[1, 2, 3, 4, 5].map(s => (
            <div key={s} className={`h-1.5 rounded-full transition-all duration-300 ${
              s === step ? 'w-8 bg-purple-500' : s < step ? 'w-4 bg-purple-300 dark:bg-purple-700' : 'w-4 bg-zinc-200 dark:bg-zinc-700'
            }`} />
          ))}
        </div>

        {/* Content area */}
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
                              <button
                                key={subj.name}
                                onClick={() => toggleSubject(subj.name)}
                                className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                                  selected
                                    ? `${colors.selectedBg} ${colors.selectedBorder} ${colors.text}`
                                    : `${colors.bg} ${colors.border} text-zinc-500 dark:text-zinc-400 hover:${colors.text}`
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

            {/* Step 3: Grade Configuration */}
            {step === 3 && (
              <MotionDiv key="step3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                <h2 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">Set Your Grades</h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">For each subject, set your level, current grade, and target grade.</p>

                <div className="space-y-3">
                  {Array.from(selectedSubjects).map(name => {
                    const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
                    const grades = getGradesForLevel(config.level);
                    const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                    const groupColor = lcSubject ? GROUP_COLORS[lcSubject.group] : GROUP_COLORS.stem;

                    return (
                      <div key={name} className="p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]">
                        <p className={`text-xs font-bold mb-2 ${groupColor.text}`}>{name}</p>
                        <div className="flex items-center gap-2">
                          {/* Level */}
                          <select
                            value={config.level}
                            onChange={(e) => updateConfig(name, 'level', e.target.value)}
                            className="flex-1 px-2 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-xs font-medium text-zinc-900 dark:text-white"
                          >
                            <option value="higher">Higher</option>
                            <option value="ordinary">Ordinary</option>
                          </select>

                          {/* Current Grade */}
                          <div className="flex-1">
                            <p className="text-[9px] text-zinc-400 dark:text-zinc-500 font-semibold mb-0.5">Current</p>
                            <select
                              value={config.currentGrade}
                              onChange={(e) => updateConfig(name, 'currentGrade', e.target.value)}
                              className="w-full px-2 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-xs font-medium text-zinc-900 dark:text-white"
                            >
                              {grades.map(g => <option key={g} value={g}>{g}</option>)}
                            </select>
                          </div>

                          {/* Arrow */}
                          <ArrowRight size={14} className="text-zinc-300 dark:text-zinc-600 flex-shrink-0 mt-3" />

                          {/* Target Grade */}
                          <div className="flex-1">
                            <p className="text-[9px] text-zinc-400 dark:text-zinc-500 font-semibold mb-0.5">Target</p>
                            <select
                              value={config.targetGrade}
                              onChange={(e) => updateConfig(name, 'targetGrade', e.target.value)}
                              className="w-full px-2 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-xs font-medium text-zinc-900 dark:text-white"
                            >
                              {grades.filter(g => getGradeIndex(g) <= getGradeIndex(config.currentGrade)).map(g => (
                                <option key={g} value={g}>{g}</option>
                              ))}
                            </select>
                          </div>
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

                  <input
                    type="date"
                    value={examDate}
                    onChange={(e) => setExamDate(e.target.value)}
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

            {/* Step 5: Summary */}
            {step === 5 && (
              <MotionDiv key="step5" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
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

                <div className="flex items-center justify-center gap-2 text-xs text-zinc-400 dark:text-zinc-500">
                  <Calendar size={12} />
                  <span>Exams start {examDate} — {daysLeft} days away</span>
                </div>
              </MotionDiv>
            )}

          </AnimatePresence>
        </div>

        {/* Footer navigation */}
        <div className="p-6 pt-0 flex items-center justify-between gap-3">
          {step > 1 ? (
            <button
              onClick={goBack}
              className="flex items-center gap-1.5 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
            >
              <ArrowLeft size={14} /> Back
            </button>
          ) : (
            <div />
          )}

          {step < 5 ? (
            <button
              onClick={goNext}
              disabled={!canProceed()}
              className="flex items-center gap-2 px-6 py-2.5 bg-purple-600 dark:bg-purple-500 text-white font-semibold text-sm rounded-xl hover:bg-purple-700 dark:hover:bg-purple-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {step === 1 ? 'Get Started' : 'Continue'} <ArrowRight size={14} />
            </button>
          ) : (
            <button
              onClick={() => onComplete(buildProfile())}
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
