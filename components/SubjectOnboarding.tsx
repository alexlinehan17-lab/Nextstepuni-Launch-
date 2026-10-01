/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { ArrowRight, ArrowLeft, Check } from 'lucide-react';
import SignatureCard from './ui/SignatureCard';
import ActionButton from './ui/ActionButton';
import { TextField } from './ui/FormControls';
import { SubjectCardPicker, SubjectGradeCards } from './shared/SubjectProfileCards';
import {
  type Grade, type Level, type StudentSubject, type StudentSubjectProfile,
  LC_SUBJECTS, getGradesForLevel, getPointsForGrade,
  getGradeIndex, DAYS_OF_WEEK,
  type LCSubject,
} from './subjectData';
import { getDefaultExamDate } from '../utils/examDates';

interface SubjectOnboardingProps {
  user: { uid: string };
  existingProfile?: StudentSubjectProfile;
  onComplete: (profile: StudentSubjectProfile) => void;
  onClose: () => void;
}

type Step = 1 | 2 | 3 | 4 | 5 | 6;
const TOTAL_STEPS = 6;

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

// ─── Component ──────────────────────────────────────────────────────────────

const SubjectOnboarding: React.FC<SubjectOnboardingProps> = ({ user: _user, existingProfile, onComplete, onClose }) => {
  const isEditMode = !!existingProfile;

  const [step, setStep] = useState<Step>(isEditMode ? 2 : 1);

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

  const goNext = () => { setStep(s => Math.min(TOTAL_STEPS, s + 1) as Step); };
  const goBack = () => { setStep(s => Math.max(1, s - 1) as Step); };

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
    // Same rule as ChangeSubjectsModal: never emit an undefined grade. JC
    // subjects carry bands and LCA subjects carry level only — writing
    // `currentGrade: undefined` for them makes setDoc throw and the edit is
    // silently lost behind a connectivity toast.
    const isJunior = existingProfile?.curriculumLevel === 'junior';
    const isLca = existingProfile?.yearGroup === 'LCA1' || existingProfile?.yearGroup === 'LCA2';
    const subjects: StudentSubject[] = Array.from(selectedSubjects).map(name => {
      if (isJunior) {
        const prev = existingProfile?.subjects.find(s => s.subjectName === name);
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
    return {
      subjects,
      examStartDate: examDate,
      restDays: Array.from(restDays),
      // Preserve the curriculum plumbing — rebuilding the profile without it
      // leaves the student curriculum-less for the rest of the session.
      // Conditional spreads, not plain assignment: an absent optional field
      // must be omitted, never written as undefined (see the grades above).
      ...(existingProfile?.yearGroup ? { yearGroup: existingProfile.yearGroup } : {}),
      ...(existingProfile?.curriculumLevel ? { curriculumLevel: existingProfile.curriculumLevel } : {}),
      ...(existingProfile?.defaultBlockDuration ? { defaultBlockDuration: existingProfile.defaultBlockDuration } : {}),
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


  const daysLeft = getDaysUntil(examDate);
  const titles = ['Set Up Your Subjects','Select Your Subjects','Set Your Grades','When Do Exams Start?','Rest Days','Your Study Profile'];
  const descriptions = [
    'A few details to personalise your Launchpad tools.',
    `Tap to select. ${selectedSubjects.size} selected`,
    'Set where you are now and where you want to be.',
    '', '', 'Review your details before saving.',
  ];
  return <SignatureCard open onClose={onClose} wide title={titles[step - 1]} eyebrow={`Study profile · ${step} of ${TOTAL_STEPS}`} description={descriptions[step - 1]} progress={{ current: step, total: TOTAL_STEPS }} footer={<>
    <ActionButton intent="quiet" onClick={step > 1 ? goBack : onClose}>{step > 1 ? <><ArrowLeft size={14} aria-hidden="true" />Back</> : 'Do this later'}</ActionButton>
    {step < TOTAL_STEPS ? <ActionButton onClick={goNext} disabled={!canProceed()}>{step === 1 ? 'Get Started' : 'Continue'}<ArrowRight size={14} aria-hidden="true" /></ActionButton> : <ActionButton onClick={() => onComplete(buildProfile())}>{isEditMode ? 'Update & Save' : 'Save & Continue'}</ActionButton>}
  </>}>
    {step === 1 && <div>
      <p className="sc-muted text-sm leading-relaxed">{existingProfile?.curriculumLevel === 'junior' ? 'Tell us about your subjects.' : 'Tell us about your Leaving Cert subjects.'} This takes about 2 minutes.</p>
      <div className="sc-welcome-list"><div><span>01</span><p className="text-sm">Your subjects and grade targets</p></div><div><span>02</span><p className="text-sm">Your exam date and study week</p></div></div>
    </div>}
    {step === 2 && <SubjectCardPicker groups={groupedSubjects} selected={selectedSubjects} onToggle={toggleSubject} />}
    {step === 3 && <SubjectGradeCards selected={selectedSubjects} configs={subjectConfigs} onUpdate={updateConfig} />}
    {step === 4 && <div>
      <p className="sc-muted text-sm">We'll use this to plan your study intensity.</p>
      <label htmlFor="subject-setup-exam-date" className="sc-date-label">Exam start date</label>
      <TextField id="subject-setup-exam-date" type="date" value={examDate} onChange={event => setExamDate(event.target.value)} className="sc-date" />
      {daysLeft > 0 && <p className="sc-countdown"><strong>{daysLeft}</strong><span className="sc-muted text-sm">days to go</span></p>}
    </div>}
    {step === 5 && <div>
      <p className="sc-muted text-sm leading-relaxed">Tap any days where study isn't possible. Your sessions will be redistributed across the remaining days.</p>
      <div className="sc-rest-days">{DAYS_OF_WEEK.map(day => <button key={day} type="button" className="sc-rest-day" aria-pressed={restDays.has(day)} aria-label={`${DAY_SHORTS[day]}, ${restDays.has(day) ? 'rest day' : 'study day'}`} onClick={() => toggleRestDay(day)}>
        <span>{DAY_SHORTS[day].toUpperCase()}</span>{restDays.has(day) ? <span>Rest</span> : <Check size={14} aria-hidden="true" />}
      </button>)}</div>
      <p className="sc-small" role="status">{7 - restDays.size} study {7 - restDays.size === 1 ? 'day' : 'days'} per week{restDays.size > 0 ? ` — ${restDays.size} rest ${restDays.size === 1 ? 'day' : 'days'}` : ''}</p>
    </div>}
    {step === 6 && <div>
      {Array.from(selectedSubjects).map(name => {
        const config = subjectConfigs[name]; if (!config) return null;
        const isMaths = LC_SUBJECTS.find(subject => subject.name === name)?.isMaths || false;
        const gain = getPointsForGrade(config.targetGrade, isMaths) - getPointsForGrade(config.currentGrade, isMaths);
        return <div key={name} className="sc-review-row"><div><strong>{name}</strong><small className="sc-small">{config.level === 'higher' ? 'Higher' : 'Ordinary'} Level</small></div><div className="text-right"><span className="text-sm">{config.currentGrade} → {config.targetGrade}</span>{gain > 0 && <small className="sc-small">+{gain} pts</small>}</div></div>;
      })}
      <div className="sc-review-row"><strong>Exams start</strong><span className="sc-muted text-sm">{new Date(`${examDate}T12:00:00`).toLocaleDateString('en-IE',{ day: 'numeric', month: 'short', year: 'numeric' })}</span></div>
      <div className="sc-review-row"><strong>Rest days</strong><span className="sc-muted text-sm">{restDays.size ? Array.from(restDays).map(day => DAY_SHORTS[day]).join(', ') : 'None selected'}</span></div>
      {existingProfile?.curriculumLevel !== 'junior' && <p className="sc-points-gain"><span className="sc-small">Projected CAO points gain</span><strong>{projectedGain > 0 ? `+${projectedGain}` : projectedGain}</strong></p>}
      <p className="sc-small">{daysLeft} days left · {restDays.size} rest {restDays.size === 1 ? 'day' : 'days'}</p>
    </div>}
  </SignatureCard>;
};

export default SubjectOnboarding;
