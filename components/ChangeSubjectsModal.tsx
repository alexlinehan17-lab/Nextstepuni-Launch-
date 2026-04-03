/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, ArrowLeft, Check, X } from 'lucide-react';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, SUBJECT_GROUP_LABELS, getGradesForLevel, getPointsForGrade,
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

// ─── Grade pill color helpers ────────────────────────────────────────────────

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

// ─── Props ───────────────────────────────────────────────────────────────────

interface ChangeSubjectsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (profile: StudentSubjectProfile) => void;
  currentProfile: StudentSubjectProfile;
}

// ─── Component ───────────────────────────────────────────────────────────────

const ChangeSubjectsModal: React.FC<ChangeSubjectsModalProps> = ({ isOpen, onClose, onSave, currentProfile }) => {
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

  const groupedSubjects = useMemo(() => {
    const groups: Record<string, LCSubject[]> = {};
    for (const subj of LC_SUBJECTS) {
      if (!groups[subj.group]) groups[subj.group] = [];
      groups[subj.group].push(subj);
    }
    return groups;
  }, []);

  // ─── Save handler ───────────────────────────────────────────────────────

  const handleSave = () => {
    const subjects: StudentSubject[] = Array.from(selectedSubjects).map(name => {
      const config = subjectConfigs[name] || { level: 'higher' as Level, currentGrade: 'H4' as Grade, targetGrade: 'H2' as Grade };
      return { subjectName: name, level: config.level, currentGrade: config.currentGrade, targetGrade: config.targetGrade };
    });
    const now = new Date().toISOString();
    onSave({
      subjects,
      examStartDate: currentProfile.examStartDate,
      restDays: currentProfile.restDays,
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
        className="fixed inset-0 z-[70] bg-zinc-50 dark:bg-zinc-950 flex flex-col"
      >
        {/* Header */}
        <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-zinc-200/50 dark:border-white/[0.06] bg-zinc-50/80 dark:bg-zinc-950/80 backdrop-blur-sm">
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
                <MotionDiv key="cs-step1" initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }} transition={{ duration: 0.3, ease: 'easeInOut' }}>
                  <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Change Your Subjects</h2>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">
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

              {/* Step 2: Grade Configuration */}
              {step === 2 && (
                <MotionDiv key="cs-step2" initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }} transition={{ duration: 0.3, ease: 'easeInOut' }}>
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

            </AnimatePresence>
          </div>
        </div>

        {/* Footer */}
        <div className="shrink-0 border-t border-zinc-200/50 dark:border-white/[0.06] px-6 py-4 bg-zinc-50/80 dark:bg-zinc-950/80 backdrop-blur-sm">
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
                className="flex items-center gap-2 px-7 py-2.5 bg-[var(--accent-hex)] text-white font-semibold text-sm rounded-full hover:bg-[var(--accent-dark-hex)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-[rgba(var(--accent),0.2)]"
              >
                Continue <ArrowRight size={14} />
              </button>
            ) : (
              <button onClick={handleSave}
                className="flex items-center gap-2 px-7 py-2.5 bg-[var(--accent-hex)] text-white font-semibold text-sm rounded-full hover:bg-[var(--accent-dark-hex)] transition-colors shadow-lg shadow-[rgba(var(--accent),0.2)]"
              >
                <Check size={14} /> Save Changes
              </button>
            )}
          </div>
        </div>
      </MotionDiv>
    </AnimatePresence>
  );
};

export default ChangeSubjectsModal;
