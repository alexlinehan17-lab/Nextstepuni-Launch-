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
  type StudentSubjectProfile,
  catalogueForProgramme, subjectProgramme, subjectLevels, type LCSubject,
} from './subjectData';

import { newSubjectConfig, updateSubjectConfig, saveSubjectConfig, type GradeConfig, type SubjectConfigField } from './shared/subjectProfileModel';

// ─── Props ───────────────────────────────────────────────────────────────────

interface ChangeSubjectsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (profile: StudentSubjectProfile) => void;
  currentProfile: StudentSubjectProfile;
}

// ─── Component ───────────────────────────────────────────────────────────────

const ChangeSubjectsModal: React.FC<ChangeSubjectsModalProps> = ({ isOpen, onClose, onSave, currentProfile }) => {
  const programme = subjectProgramme(currentProfile.yearGroup, currentProfile.curriculumLevel);
  const isJunior = programme === 'jc';
  const newConfig = (name: string) => newSubjectConfig(programme, name);
  const [step, setStep] = useState<1 | 2>(1);

  // Initialise from current profile
  const [selectedSubjects, setSelectedSubjects] = useState<Set<string>>(() =>
    new Set(currentProfile.subjects.map(s => s.subjectName))
  );

  const [subjectConfigs, setSubjectConfigs] = useState<Record<string, GradeConfig>>(() => {
    const configs: Record<string, GradeConfig> = {};
    for (const s of currentProfile.subjects) {
      configs[s.subjectName] = { level: s.level, currentGrade: s.currentGrade, targetGrade: s.targetGrade, currentBand: s.currentBand, targetBand: s.targetBand };
    }
    return configs;
  });

  // Reset state when modal opens with new profile data
  const [lastProfile, setLastProfile] = useState(currentProfile);
  if (currentProfile !== lastProfile) {
    setLastProfile(currentProfile);
    setSelectedSubjects(new Set(currentProfile.subjects.map(s => s.subjectName)));
    const configs: Record<string, GradeConfig> = {};
    for (const s of currentProfile.subjects) {
      configs[s.subjectName] = { level: s.level, currentGrade: s.currentGrade, targetGrade: s.targetGrade, currentBand: s.currentBand, targetBand: s.targetBand };
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
            [name]: newConfig(name),
          }));
        }
      }
      return next;
    });
  };

  // ─── Grade config update ─────────────────────────────────────────────────

  const updateConfig = (subjectName: string, field: SubjectConfigField, value: string) => {
    setSubjectConfigs(prev => ({ ...prev, [subjectName]: updateSubjectConfig(programme, subjectName,
      prev[subjectName] ?? newConfig(subjectName), field, value) }));
  };

  // ─── Grouped subjects ───────────────────────────────────────────────────

  const missingLevel = Array.from(selectedSubjects).some(name => !subjectLevels(programme, name).includes(subjectConfigs[name]?.level ?? 'common'));
  const groupedSubjects = useMemo(() => {
    const groups: Record<string, LCSubject[]> = {};
    for (const subj of catalogueForProgramme(programme)) {
      if (!groups[subj.group]) groups[subj.group] = [];
      groups[subj.group].push(subj);
    }
    return groups;
  }, [programme]);

  // ─── Save handler ───────────────────────────────────────────────────────

  const handleSave = () => {
    if (missingLevel) return;
    const subjects = Array.from(selectedSubjects).map(name =>
      saveSubjectConfig(programme, name, subjectConfigs[name] ?? newConfig(name)));
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


  return <SignatureCard open={isOpen} onClose={onClose} wide title={step === 1 ? 'Change Your Subjects' : 'Set Your Grades'} eyebrow={`Change subjects · ${step} of 2`} description={step === 1 ? <>{isJunior ? 'Tap to select your subjects.' : 'Tap to select your Leaving Cert subjects.'} {selectedSubjects.size} selected</> : 'Set where you are now and where you want to be.'} progress={{ current: step, total: 2 }} footer={<>
    <ActionButton intent="quiet" onClick={step === 2 ? () => setStep(1) : onClose}>{step === 2 ? <><ArrowLeft size={14} aria-hidden="true" />Back</> : 'Cancel'}</ActionButton>
    {step === 1 ? <ActionButton onClick={() => setStep(2)} disabled={selectedSubjects.size === 0}>Continue<ArrowRight size={14} aria-hidden="true" /></ActionButton> : <ActionButton onClick={handleSave} disabled={missingLevel}>Save Changes</ActionButton>}
  </>}>
    {step === 1 ? <SubjectCardPicker groups={groupedSubjects} selected={selectedSubjects} onToggle={toggleSubject} /> : <SubjectGradeCards programme={programme} selected={selectedSubjects} configs={subjectConfigs} onUpdate={updateConfig} />}
  </SignatureCard>;
};

export default ChangeSubjectsModal;
