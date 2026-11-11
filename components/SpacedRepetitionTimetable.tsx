/** @license SPDX-License-Identifier: Apache-2.0 */
import React, { useState, useMemo, useEffect } from 'react';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak } from './subjectData';
import { computeSubjectPrioritiesForCurriculum, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam, computeWeeklyStudyTarget, type SubjectSM2State } from './timetableAlgorithm';
import { useAuth } from '../contexts/AuthContext';
import { useOptionalProgress } from '../contexts/ProgressContext';
import { useInnovationData } from '../contexts/InnovationDataContext';
import { type DebriefEntry, computeStrategyHints, type SubjectStrategyHint } from './StudyDebrief';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { usePlanCues } from '../hooks/usePlanCues';
import type { SchoolEvent } from './gc/GCKeyEvents';
import CrewEmptyState from './CrewEmptyState';
import PlannerExplanation from './launchpad/PlannerExplanation';
import PlannerWorkbench from './launchpad/PlannerWorkbench';
import { Button } from './approved-ui-runtime';
import { useDatedStudyPlan } from '../hooks/useDatedStudyPlan';
import { retainPlannedTask, setTaskStatus } from '../services/studyPlanStore';
import { studyPlanPriorities, type PlanTask } from '../services/studyPlanEngine';

export interface TimetableBlockInfo {
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  dateKey: string;
  blockId: string;
}

interface SpacedRepetitionTimetableProps {
  profile: StudentSubjectProfile;
  uid?: string;
  onOpenSettings: () => void;
  onRestDaysChange?: (restDays: string[]) => void;
  completions?: TimetableCompletions;
  streak?: TimetableStreak;
  onToggleCompletion?: (dateKey: string, blockId: string, completed: boolean) => void;
  onOpenJournal?: () => void;
  skippedSessions?: string[];
  onStudyNow?: (block: TimetableBlockInfo) => void;
  onBlockDurationChange?: (subjectName: string, sessionType: string, newDuration: number) => void;
  schoolEvents?: SchoolEvent[];
  deferredBlocks?: string[];
  onSkipBlock?: (dateKey: string, blockId: string, skipped: boolean) => void;
  onPlanSettingsChange?: (restDays: string[], minutes: number) => void;
}


export function getWeekStartDate(weekOffset: number): Date {
  const now = new Date(); const day = now.getDay();
  const monday = new Date(now); monday.setDate(now.getDate() + (day === 0 ? -6 : 1 - day) + weekOffset * 7); monday.setHours(0, 0, 0, 0);
  return monday;
}
const SpacedRepetitionTimetable: React.FC<SpacedRepetitionTimetableProps> = ({ profile, uid, onOpenSettings, onRestDaysChange, completions = {}, onToggleCompletion, skippedSessions = [], deferredBlocks = [], onSkipBlock, onStudyNow, onBlockDurationChange, onPlanSettingsChange, schoolEvents = [] }) => {
  const { cues: planCues, setCue: setPlanCue } = usePlanCues(uid);
  const { user } = useAuth();
  const progress = useOptionalProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const curriculumLevel = user?.curriculumLevel ?? profile.curriculumLevel ?? 'senior';
  const isJunior = curriculumLevel === 'junior';
  const yearGroup = user?.yearGroup ?? profile.yearGroup;
  const isPreExamJunior = isJunior && (yearGroup === '1st' || yearGroup === '2nd');
  const [weekOffset, setWeekOffset] = useState(0);
  const [showExplainer, setShowExplainer] = useState(false);
  const restDaysArray = useMemo(() => profile.restDays ?? [], [profile.restDays]);
  const dated = useDatedStudyPlan(profile, uid, weekOffset);
  const { topicMastery: topicMasteryHook } = useInnovationData();
  const topicMastery = topicMasteryHook.mastery;
  // Strategy hints from Learning DNA (per-subject best strategy)
  const [strategyHints, setStrategyHints] = useState<Record<string, SubjectStrategyHint>>({});
  const [sm2States, setSm2States] = useState<SubjectSM2State[]>([]);
  useEffect(() => {
    if (!uid) return;
    if (isDemo) {
      const data = progress?.rawProgressDoc.studyDebriefs as DebriefEntry[] | undefined;
      if (data) setStrategyHints(computeStrategyHints(data));
      else setStrategyHints({});
      setSm2States((progress?.rawProgressDoc.sm2States as SubjectSM2State[] | undefined) ?? []);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'progress', uid));
        const progress = snap.data();
        const data = progress?.studyDebriefs as DebriefEntry[] | undefined;
        if (!cancelled) {
          if (data) setStrategyHints(computeStrategyHints(data));
          setSm2States((progress?.sm2States as SubjectSM2State[] | undefined) ?? []);
        }
      } catch (err) { console.error('Failed to load strategy hints:', err); }
    })();
    return () => { cancelled = true; };
  }, [uid, isDemo, progress?.rawProgressDoc.studyDebriefs, progress?.rawProgressDoc.sm2States]);

  // Pre-exam JC (1st/2nd year): no real exam countdown. The placeholder LC
  // June date that Phase 1 writes would yield a 22-month figure — meaningless
  // here. Synthesise a "school-term cadence" weeks value (~18 weeks ≈ one
  // term) so the intensity factor stays low and the sustainability caps
  // resolve to the "far from exams" base values. The UI ribbon below is
  // hidden for this case.
  const weeksUntilExam = isPreExamJunior
    ? 22 // school-term cadence: the lower building-phase workload
    : (profile.examStartDate ? computeWeeksUntilExam(profile.examStartDate) : 22);

  const priorities = useMemo(
    () => dated.saved ? studyPlanPriorities(dated.saved.inputs) : computeSubjectPrioritiesForCurriculum(profile.subjects, topicMastery, curriculumLevel, profile.examStartDate),
    [profile.subjects, topicMastery, curriculumLevel, profile.examStartDate, dated.saved]
  );

  const blockDuration = profile.defaultBlockDuration ?? 45;
  const effectiveWeeksUntilExam = Math.max(0, weeksUntilExam - weekOffset);
  const weeklyTarget = useMemo(
    () => dated.enabled ? { explanation: `Your existing rest days and block length shape this plan. ${dated.saved?.inputs.settings.revisionMinutes ?? 360} minutes is a planning ceiling, not a required amount of study. Due reviews take priority; longer sessions and approaching exams do not raise the ceiling.` } : computeWeeklyStudyTarget(effectiveWeeksUntilExam),
    [effectiveWeeksUntilExam, dated.enabled, dated.saved]
  );

  const allocations = useMemo(
    () => dated.enabled ? priorities.map(priority => ({subjectName: priority.subjectName, sessions: dated.timetable?.flatMap(day => day.blocks).filter(block => block.subjectName === priority.subjectName).length ?? 0, priorityLabel: 'Medium' as const, priorityScore: priority.priorityScore})) : allocateSessions(priorities, effectiveWeeksUntilExam, sm2States, blockDuration),
    [priorities, effectiveWeeksUntilExam, sm2States, blockDuration, dated.enabled, dated.timetable]
  );

  const timetable = useMemo(
    () => dated.enabled ? dated.timetable ?? [] : generateWeeklyTimetable(allocations, weeksUntilExam, weekOffset, restDaysArray, blockDuration, sm2States, topicMastery),
    [allocations, weeksUntilExam, weekOffset, restDaysArray, blockDuration, sm2States, topicMastery, dated.enabled, dated.timetable]
  );

  const weekStart = getWeekStartDate(weekOffset);

  const totalSessions = timetable.reduce((sum, day) => sum + day.blocks.length, 0);
  const totalMinutes = timetable.reduce((sum, day) => sum + day.blocks.reduce((minutes, block) => minutes + block.durationMinutes, 0), 0);


  if (!profile.subjects.length) return <CrewEmptyState title="A little room for a plan." action="Choose your subjects" onAction={onOpenSettings}>Start with your subjects. We’ll help you shape a week with time to study, revisit and rest.</CrewEmptyState>;
  return <PlannerWorkbench uid={uid ?? 'guest'} timetable={timetable} subjects={profile.subjects.map(subject => subject.subjectName)} weekStart={weekStart} weekOffset={weekOffset} onWeekChange={setWeekOffset} restDays={restDaysArray} duration={blockDuration} onSettings={onOpenSettings}
    onPlanSettingsChange={(days, minutes) => { if (onPlanSettingsChange) onPlanSettingsChange(days, minutes); else { onRestDaysChange?.(days); onBlockDurationChange?.('', '', minutes); } }}
    isComplete={entry => (completions[entry.dateKey]?.includes(entry.id) ?? false) || dated.saved?.plan.tasks.some(task => task.id === entry.id && task.status === 'completed') === true}
    isSkipped={entry => skippedSessions.includes(entry.key) || deferredBlocks.includes(entry.key)}
    isDeferred={entry => deferredBlocks.includes(entry.key)}
    onComplete={onToggleCompletion ? (entry, done) => { if (dated.enabled) { retainPlannedTask(dated.scope, entry.block as PlanTask); setTaskStatus(dated.scope, entry.id, done ? 'completed' : 'planned'); } onToggleCompletion(entry.dateKey, entry.id, done); } : undefined}
    onSkip={onSkipBlock ? (entry, skipped) => onSkipBlock(entry.dateKey, entry.id, skipped) : undefined}
    onStudy={onStudyNow ? entry => { if (dated.enabled) retainPlannedTask(dated.scope, entry.block as PlanTask); onStudyNow({ subject: entry.block.subjectName, sessionType: entry.block.sessionType, durationMinutes: entry.block.durationMinutes, dateKey: entry.dateKey, blockId: entry.id }); } : undefined}
    schoolEvents={schoolEvents} hints={strategyHints} cues={planCues} onCueSave={setPlanCue}
    explanation={<><p>{weeklyTarget.explanation}</p><p>Work is spread across your available days, with repeat sessions spaced apart and room for rest.</p><p>{isJunior ? 'Target bands, due reviews and recent subject contact guide the allocation. Topics are checked before assuming they need more practice.' : 'Targets, due reviews and recent subject contact guide the allocation. Confidence alone does not prove recall; a completed session does not postpone a review.'}</p>{!isJunior && <><Button variant="ghost" onClick={() => setShowExplainer(true)}>See the allocation in detail</Button><PlannerExplanation open={showExplainer} onClose={() => setShowExplainer(false)} priorities={priorities} allocations={allocations} totalSessions={totalSessions} totalMinutes={totalMinutes} workloadExplanation={weeklyTarget.explanation} /></>}</>}
  />;
};
export default SpacedRepetitionTimetable;
