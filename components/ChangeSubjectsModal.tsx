/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { ArrowRight, ArrowLeft } from 'lucide-react';
import SignatureCard from './ui/SignatureCard';
import ActionButton from './ui/ActionButton';
import { SubjectCardPicker, SubjectGradeCards } from './shared/SubjectProfileCards';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, LCA_SUBJECTS, getGradesForLevel, getGradeIndex, type LCSubject,
} from './subjectData';

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


  return <SignatureCard open={isOpen} onClose={onClose} wide title={step === 1 ? 'Change Your Subjects' : 'Set Your Grades'} eyebrow={`Change subjects · ${step} of 2`} description={step === 1 ? <>{currentProfile.curriculumLevel === 'junior' ? 'Tap to select your subjects.' : 'Tap to select your Leaving Cert subjects.'} {selectedSubjects.size} selected</> : 'Set where you are now and where you want to be.'} progress={{ current: step, total: 2 }} footer={<>
    <ActionButton intent="quiet" onClick={step === 2 ? () => setStep(1) : onClose}>{step === 2 ? <><ArrowLeft size={14} aria-hidden="true" />Back</> : 'Cancel'}</ActionButton>
    {step === 1 ? <ActionButton onClick={() => setStep(2)} disabled={selectedSubjects.size === 0}>Continue<ArrowRight size={14} aria-hidden="true" /></ActionButton> : <ActionButton onClick={handleSave}>Save Changes</ActionButton>}
  </>}>
    {step === 1 ? <SubjectCardPicker groups={groupedSubjects} selected={selectedSubjects} onToggle={toggleSubject} /> : <SubjectGradeCards selected={selectedSubjects} configs={subjectConfigs} onUpdate={updateConfig} />}
  </SignatureCard>;
};

export default ChangeSubjectsModal;
