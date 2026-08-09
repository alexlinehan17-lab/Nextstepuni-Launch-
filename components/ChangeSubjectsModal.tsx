/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, ArrowLeft, Check, X } from 'lucide-react';
import { useModal } from '../hooks/useModal';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, LCA_SUBJECTS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
  getGradeIndex,
  type LCSubject,
} from './subjectData';

// ─── Subject Color Map (literal Tailwind strings for CDN) ───────────────────

const GROUP_COLORS: Record<LCSubject['group'], { bg: string; border: string; text: string; selectedBg: string; selectedBorder: string }> = {
  languages: { bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300', selectedBg: 'bg-blue-100 dark:bg-blue-900/40', selectedBorder: 'border-blue-400 dark:border-blue-500' },
  stem: { bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300', selectedBg: 'bg-emerald-100 dark:bg-emerald-900/40', selectedBorder: 'border-emerald-400 dark:border-emerald-500' },
  business: { bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300', selectedBg: 'bg-amber-100 dark:bg-amber-900/40', selectedBorder: 'border-amber-400 dark:border-amber-500' },
  humanities: { bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300', selectedBg: 'bg-purple-100 dark:bg-purple-900/40', selectedBorder: 'border-purple-400 dark:border-purple-500' },
  practical: { bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300', selectedBg: 'bg-orange-100 dark:bg-orange-900/40', selectedBorder: 'border-orange-400 dark:border-orange-500' },
  creative: { bg: 'bg-rose-50 dark:bg-rose-900/20', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-300', selectedBg: 'bg-rose-100 dark:bg-rose-900/40', selectedBorder: 'border-rose-400 dark:border-rose-500' },
};

const GROUP_DOT_HEX: Record<LCSubject['group'], string> = {
  languages: '#3B82F6',
  stem: '#10B981',
  business: '#F59E0B',
  humanities: '#A855F7',
  practical: '#FB923C',
  creative: '#F43F5E',
};

// ─── Grade pill color helpers ────────────────────────────────────────────────

const GRADE_BUTTON_BASE = 'border-2 border-[#1A1A1A] font-bold font-sans transition-all duration-150 hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 shadow-[2px_2px_0_0_#1A1A1A] hover:shadow-[3px_3px_0_0_#1A1A1A] active:shadow-none';

function getCurrentGradePillClass(isSelected: boolean): string {
  return isSelected
    ? `${GRADE_BUTTON_BASE} bg-[#1A1A1A] text-[#FDF8F0]`
    : `${GRADE_BUTTON_BASE} bg-[#FDF8F0] text-[#1A1A1A]`;
}

function getTargetGradePillClass(isSelected: boolean): string {
  return isSelected
    ? `${GRADE_BUTTON_BASE} bg-[#F26B1F] text-[#FDF8F0]`
    : `${GRADE_BUTTON_BASE} bg-[#FDF8F0] text-[#1A1A1A]`;
}

// ─── Props ───────────────────────────────────────────────────────────────────

interface ChangeSubjectsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (profile: StudentSubjectProfile) => void;
  currentProfile: StudentSubjectProfile;
}

// ─── Component ───────────────────────────────────────────────────────────────

const ChangeSubjectsModal: React.FC<ChangeSubjectsModalProps> = ({ isOpen, onClose, onSave, currentProfile }) => {
  useModal(isOpen, onClose);
  const [step, setStep] = useState<1 | 2>(1);

  // Initialise from current profile
  const [selectedSubjects, setSelectedSubjects] = useState<Set<string>>(() =>
    new Set(currentProfile.subjects.map(s => s.subjectName))
  );

  const [subjectConfigs, setSubjectConfigs] = useState<Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }>>(() => {
    const configs: Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }> = {};
    for (const s of currentProfile.subjects) {
      configs[s.subjectName] = { level: s.level, currentGrade: s.currentGrade, targetGrade: s.targetGrade };
    }
    return configs;
  });

  // Reset state when modal opens with new profile data
  const [lastProfile, setLastProfile] = useState(currentProfile);
  if (currentProfile !== lastProfile) {
    setLastProfile(currentProfile);
    setSelectedSubjects(new Set(currentProfile.subjects.map(s => s.subjectName)));
    const configs: Record<string, { level: Level; currentGrade: Grade; targetGrade: Grade }> = {};
    for (const s of currentProfile.subjects) {
      configs[s.subjectName] = { level: s.level, currentGrade: s.currentGrade, targetGrade: s.targetGrade };
    }
    setSubjectConfigs(configs);
    setStep(1);
  }

  // ─── Subject toggle ──────────────────────────────────────────────────────

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

  // ─── Grade config update ─────────────────────────────────────────────────

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

  // ─── Grouped subjects ───────────────────────────────────────────────────

  // LCA students pick from the LCA course list; everyone else the LC list.
  const isLca = currentProfile.yearGroup === 'LCA1' || currentProfile.yearGroup === 'LCA2';
  const groupedSubjects = useMemo(() => {
    const groups: Record<string, LCSubject[]> = {};
    for (const subj of (isLca ? LCA_SUBJECTS : LC_SUBJECTS)) {
      if (!groups[subj.group]) groups[subj.group] = [];
      groups[subj.group].push(subj);
    }
    return groups;
  }, [isLca]);

  // ─── Save handler ───────────────────────────────────────────────────────

  const handleSave = () => {
    // Junior Cycle subjects carry bands, LCA subjects carry level only, and
    // neither has an H/O grade. Emitting `currentGrade: undefined` for them
    // made setDoc throw before anything was written (the SDK rejects undefined
    // unless ignoreUndefinedProperties is set, and it deliberately isn't), so
    // a JC or LCA student's subject edit failed with a misleading
    // "check your connection" toast every single time. Mirror Onboarding's
    // curriculum branch and never put an undefined in the payload.
    const isJunior = currentProfile.curriculumLevel === 'junior';
    const subjects: StudentSubject[] = Array.from(selectedSubjects).map(name => {
      if (isJunior) {
        const prev = currentProfile.subjects.find(s => s.subjectName === name);
        return {
          subjectName: name,
          level: prev?.level ?? 'common',
          currentBand: prev?.currentBand ?? 'Merit',
          targetBand: prev?.targetBand ?? 'Higher Merit',
        };
      }
      if (isLca) return { subjectName: name, level: 'common' as Level };
      const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
      return {
        subjectName: name,
        level: config.level,
        ...(config.currentGrade ? { currentGrade: config.currentGrade } : {}),
        ...(config.targetGrade ? { targetGrade: config.targetGrade } : {}),
      };
    });
    const now = new Date().toISOString();
    onSave({
      subjects,
      examStartDate: currentProfile.examStartDate,
      restDays: currentProfile.restDays,
      // Carried through deliberately: dropping these rebuilt the in-memory
      // profile without a curriculum, so the rest of the session ran as if the
      // student had no year group. Conditional spreads, not plain assignment —
      // an absent optional field must be omitted, never written as undefined.
      ...(currentProfile.yearGroup ? { yearGroup: currentProfile.yearGroup } : {}),
      ...(currentProfile.curriculumLevel ? { curriculumLevel: currentProfile.curriculumLevel } : {}),
      ...(currentProfile.defaultBlockDuration ? { defaultBlockDuration: currentProfile.defaultBlockDuration } : {}),
      createdAt: currentProfile.createdAt,
      updatedAt: now,
    });
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <MotionDiv
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[200] bg-[#1A1A1A]/55 flex items-end sm:items-center justify-center p-0 sm:p-4"
        onClick={onClose}
      >
        <MotionDiv
          initial={{ opacity: 0, y: 24, scale: 0.985 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 16, scale: 0.99 }}
          transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
          onClick={(event: React.MouseEvent) => event.stopPropagation()}
          className="flex h-[92dvh] w-full max-w-5xl flex-col overflow-hidden rounded-t-[24px] border-[1.5px] border-[#383838] bg-[#FAFBF6] shadow-[5px_5px_0_0_#383838] sm:rounded-[24px] dark:border-zinc-600 dark:bg-zinc-900"
        >
        {/* Header */}
        <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-[#DDD8D2] dark:border-zinc-700 bg-[#FAFBF6] dark:bg-zinc-900">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className={`h-2 rounded-full transition-all ${step === 1 ? 'w-8 bg-[var(--accent-hex)]' : 'w-4 bg-[rgba(var(--accent),0.4)]'}`} />
              <div className={`h-2 rounded-full transition-all ${step === 2 ? 'w-8 bg-[var(--accent-hex)]' : step > 2 ? 'w-4 bg-[rgba(var(--accent),0.4)]' : 'w-4 bg-zinc-200 dark:bg-zinc-700'}`} />
            </div>
            <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
              {step === 1 ? 'Select Subjects' : 'Set Grades'}
            </span>
          </div>
          <button
            onClick={onClose}
            aria-label="Close"
            className="w-9 h-9 rounded-lg flex items-center justify-center hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <X size={18} className="text-zinc-500" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto min-h-0">
          <div className="max-w-2xl mx-auto px-6 py-10">
            <AnimatePresence mode="wait">

              {/* Step 1: Select Subjects */}
              {step === 1 && (
                <MotionDiv key="cs-step1" initial={{ opacity: 0, y: 12, scale: 0.995 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -8, scale: 0.995 }} transition={{ type: 'spring', stiffness: 260, damping: 28, mass: 0.8 }}>
                  <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Change Your Subjects</h2>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">
                    {currentProfile.curriculumLevel === 'junior'
                      ? 'Tap to select your subjects.'
                      : 'Tap to select your Leaving Cert subjects.'}{' '}
                    <span className="font-semibold text-[var(--accent-hex)]">{selectedSubjects.size} selected</span>
                  </p>
                  <div className="space-y-6">
                    {Object.entries(groupedSubjects).map(([group, subjects]) => {
                      const dotHex = GROUP_DOT_HEX[group as LCSubject['group']];
                      return (
                        <div key={group} className="mb-8 last:mb-0">
                          <p className="mb-3 font-sans text-[11px] font-semibold uppercase tracking-wider text-[#6B6B6B]">
                            {SUBJECT_GROUP_LABELS[group as LCSubject['group']]}
                          </p>
                          <div className="flex flex-wrap gap-3">
                            {subjects.map(subj => {
                              const selected = selectedSubjects.has(subj.name);
                              return (
                                <button key={subj.name} onClick={() => toggleSubject(subj.name)}
                                  className={`group flex items-center gap-2.5 rounded-2xl border-2 border-[#1A1A1A] px-4 py-3 font-sans text-[15px] font-medium transition-all duration-150 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-none ${
                                    selected ? 'bg-[#F26B1F] text-[#FDF8F0]' : 'bg-[#FDF8F0] text-[#1A1A1A]'
                                  }`}
                                >
                                  <span
                                    className="h-2.5 w-2.5 shrink-0 rounded-full"
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

              {/* Step 2: Grade Configuration */}
              {step === 2 && (
                <MotionDiv key="cs-step2" initial={{ opacity: 0, y: 12, scale: 0.995 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -8, scale: 0.995 }} transition={{ type: 'spring', stiffness: 260, damping: 28, mass: 0.8 }}>
                  <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Set Your Grades</h2>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
                    For each subject, set where you are now and where you want to be.
                  </p>

                  <div className="mt-6 space-y-4">
                    {Array.from(selectedSubjects).map(name => {
                      const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
                      const grades = getGradesForLevel(config.level);
                      const lcSubject = LC_SUBJECTS.find(s => s.name === name);
                      const groupColor = lcSubject ? GROUP_COLORS[lcSubject.group] : GROUP_COLORS.stem;
                      const currentIdx = getGradeIndex(config.currentGrade);
                      const targetIdx = getGradeIndex(config.targetGrade);

                      return (
                        <div key={name} className="overflow-hidden rounded-2xl border-2 border-[#1A1A1A] bg-[#FDF8F0] shadow-[4px_4px_0_0_#1A1A1A]">
                          {/* Subject header row */}
                          <div className="flex items-center justify-between border-b-2 border-[#1A1A1A]/10 px-4 pb-2 pt-3">
                            <span className={`text-sm font-bold ${groupColor.text}`}>{name}</span>
                            <div className="flex items-center gap-1">
                              <button
                                onClick={() => updateConfig(name, 'level', 'higher')}
                                className={`rounded-md border-2 border-[#1A1A1A] px-2.5 py-1 text-[10px] font-bold transition-all duration-150 shadow-[2px_2px_0_0_#1A1A1A] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none ${
                                  config.level === 'higher'
                                    ? 'bg-[#1A1A1A] text-[#FDF8F0]'
                                    : 'bg-[#FDF8F0] text-[#1A1A1A]'
                                }`}
                              >
                                Higher
                              </button>
                              <button
                                onClick={() => updateConfig(name, 'level', 'ordinary')}
                                className={`rounded-md border-2 border-[#1A1A1A] px-2.5 py-1 text-[10px] font-bold transition-all duration-150 shadow-[2px_2px_0_0_#1A1A1A] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none ${
                                  config.level === 'ordinary'
                                    ? 'bg-[#1A1A1A] text-[#FDF8F0]'
                                    : 'bg-[#FDF8F0] text-[#1A1A1A]'
                                }`}
                              >
                                Ordinary
                              </button>
                            </div>
                          </div>

                          <div className="space-y-3 px-4 pb-3 pt-3">
                            <div>
                              <p className="mb-1.5 text-[10px] font-bold uppercase tracking-wider text-[#78716C]">Where I am now</p>
                              <div className="flex gap-1.5">
                                {grades.map(g => (
                                  <button key={g} onClick={() => updateConfig(name, 'currentGrade', g)} className={`flex-1 rounded-lg py-2 text-[11px] ${getCurrentGradePillClass(g === config.currentGrade)}`}>
                                    {g}
                                  </button>
                                ))}
                              </div>
                            </div>
                            <div>
                              <p className="mb-1.5 text-[10px] font-bold uppercase tracking-wider text-[#F26B1F]">My target</p>
                              <div className="flex gap-1.5">
                                {grades.map((g, gi) => {
                                  const disabled = gi > currentIdx;
                                  return (
                                    <button
                                      key={g}
                                      onClick={() => { if (!disabled) updateConfig(name, 'targetGrade', g); }}
                                      disabled={disabled}
                                      className={`flex-1 rounded-lg py-2 text-[11px] ${disabled ? 'cursor-not-allowed border-2 border-[#1A1A1A]/15 bg-[#FDF8F0]/40 font-bold text-[#1A1A1A]/25' : getTargetGradePillClass(g === config.targetGrade)}`}
                                    >
                                      {g}
                                    </button>
                                  );
                                })}
                              </div>
                            </div>
                            {/* Improvement indicator */}
                            {targetIdx < currentIdx && (
                              <div className="flex items-center justify-between mt-2 px-0.5">
                                <span className="text-[10px] text-zinc-400 dark:text-zinc-500">
                                  {config.currentGrade} <ArrowRight size={8} className="inline -mt-0.5" /> {config.targetGrade}
                                </span>
                                <span className="text-[10px] font-bold text-success dark:text-success">
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

            </AnimatePresence>
          </div>
        </div>

        {/* Footer */}
        <div className="shrink-0 border-t border-[#DDD8D2] dark:border-zinc-700 px-6 py-4 bg-white/60 dark:bg-zinc-950/30">
          <div className="max-w-2xl mx-auto flex items-center justify-between">
            {step === 2 ? (
              <button onClick={() => setStep(1)} className="flex items-center gap-1.5 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
                <ArrowLeft size={14} /> Back
              </button>
            ) : (
              <button onClick={onClose} className="text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
                Cancel
              </button>
            )}

            {step === 1 ? (
              <button onClick={() => setStep(2)} disabled={selectedSubjects.size === 0}
                className="flex items-center gap-2 px-7 py-2.5 bg-[#F26B1F] text-white font-semibold text-sm rounded-xl border-2 border-[#1A1A1A] shadow-[3px_3px_0_0_#1A1A1A] transition-all active:translate-x-1 active:translate-y-1 active:shadow-none disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Continue <ArrowRight size={14} />
              </button>
            ) : (
              <button onClick={handleSave}
                className="flex items-center gap-2 px-7 py-2.5 bg-[#F26B1F] text-white font-semibold text-sm rounded-xl border-2 border-[#1A1A1A] shadow-[3px_3px_0_0_#1A1A1A] transition-all active:translate-x-1 active:translate-y-1 active:shadow-none"
              >
                <Check size={14} /> Save Changes
              </button>
            )}
          </div>
        </div>
        </MotionDiv>
      </MotionDiv>
    </AnimatePresence>
  );
};

export default ChangeSubjectsModal;
