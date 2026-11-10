import { createStudyPlan } from '../services/studyPlanStore';
import { initialPlanSettings, dateKey, mondayOf } from '../services/studyPlanEngine';
import React from 'react';
import { afterEach, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import SpacedRepetitionTimetable from '@/components/SpacedRepetitionTimetable';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import type { StudentSubjectProfile } from '@/components/subjectData';

vi.mock('@/contexts/AuthContext', () => ({ useAuth: () => ({ user: { curriculumLevel:'senior', yearGroup:'6th' } }) }));
vi.mock('@/contexts/ProgressContext', () => ({ useOptionalProgress: () => ({ rawProgressDoc:{} }) }));
vi.mock('@/contexts/InnovationDataContext', () => ({ useInnovationData: () => ({ topicMastery: { mastery:{} } }) }));
vi.mock('@/hooks/usePlanCues', () => ({ usePlanCues: () => ({ cues:{}, setCue:vi.fn() }) }));
const profile: StudentSubjectProfile = { subjects:[{subjectName:'Geography',level:'higher',currentGrade:'H4',targetGrade:'H2'},{subjectName:'Irish',level:'higher',currentGrade:'H4',targetGrade:'H2'}], examStartDate:'2027-06-09',restDays:['Sunday'],defaultBlockDuration:45,createdAt:'2026-09-01',updatedAt:'2026-09-01' };
afterEach(cleanup);
test('the real planner profile and algorithm feed the ledger and Study Room handoff', () => {
  const onStudyNow = vi.fn();
  const settings=initialPlanSettings(profile);settings.confirmed=true;settings.revisionMinutes=300;settings.days=settings.days.map(()=>({windowMinutes:60,breakMinutes:0,assignedMinutes:0,bufferMinutes:0}));
  const today=dateKey(new Date());createStudyPlan(DEMO_STUDENT_UID,{profile,settings,evidence:[],cards:[],deadlines:[],requirements:[],lastContact:{}},mondayOf(today),today,true);
  render(<SpacedRepetitionTimetable profile={profile} uid={DEMO_STUDENT_UID} onOpenSettings={vi.fn()} onStudyNow={onStudyNow} />);
  const ledger = screen.getByText('A place for each subject.').parentElement as HTMLElement;
  expect(within(ledger).getByText('Geography')).toBeInTheDocument();
  expect(within(ledger).getByText('Irish')).toBeInTheDocument();
  for (const duration of ledger.querySelectorAll('.dp-subject-line strong')) expect(duration.textContent).not.toBe('0m');
  expect(screen.getByRole('button', { name:'Study this block' })).toBeEnabled();
  fireEvent.click(screen.getByRole('button', { name:'Study this block' }));
  expect(onStudyNow).toHaveBeenCalledWith(expect.objectContaining({ subject:expect.stringMatching(/Geography|Irish/),durationMinutes:expect.any(Number),dateKey:expect.stringMatching(/^\d{4}-\d{2}-\d{2}$/),blockId:expect.any(String) }));
});
