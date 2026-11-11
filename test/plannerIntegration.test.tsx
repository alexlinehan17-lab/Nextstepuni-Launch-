import React from 'react';
import { afterEach, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within, waitFor } from '@testing-library/react';
import SpacedRepetitionTimetable from '@/components/SpacedRepetitionTimetable';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import type { StudentSubjectProfile } from '@/components/subjectData';
import { readStudyPlan } from '../services/studyPlanStore';
import { addDays, dateKey, mondayOf } from '../services/studyPlanEngine';

vi.mock('@/contexts/AuthContext', () => ({ useAuth: () => ({ user: { curriculumLevel:'senior', yearGroup:'6th' } }) }));
vi.mock('@/contexts/ProgressContext', () => ({ useOptionalProgress: () => ({ rawProgressDoc:{} }) }));
vi.mock('@/contexts/InnovationDataContext', () => ({ useInnovationData: () => ({ topicMastery: { mastery:{} } }) }));
vi.mock('firebase/firestore', () => ({doc: vi.fn(), getDoc: vi.fn(async () => ({data: () => ({})}))}));
vi.mock('@/hooks/usePlanCues', () => ({ usePlanCues: () => ({ cues:{}, setCue:vi.fn() }) }));
const profile: StudentSubjectProfile = { subjects:[{subjectName:'Geography',level:'higher',currentGrade:'H4',targetGrade:'H2'},{subjectName:'Irish',level:'higher',currentGrade:'H4',targetGrade:'H2'}], examStartDate:'2027-06-09',restDays:['Sunday'],defaultBlockDuration:45,createdAt:'2026-09-01',updatedAt:'2026-09-01' };
afterEach(cleanup);
test('the real planner profile and algorithm feed the ledger and Study Room handoff', () => {
  const onStudyNow = vi.fn();
  render(<SpacedRepetitionTimetable profile={profile} uid={DEMO_STUDENT_UID} onOpenSettings={vi.fn()} onStudyNow={onStudyNow} />);
  const ledger = screen.getByText('The balance of your week').closest('.pp-workload') as HTMLElement;
  expect(within(ledger).getByText('Geography')).toBeInTheDocument();
  expect(within(ledger).getByText('Irish')).toBeInTheDocument();
  for (const duration of ledger.querySelectorAll('.pp-ledger-row strong')) expect(duration.textContent).not.toBe('0m');
  expect(screen.getByRole('button', { name:'Study this block' })).toBeEnabled();
  fireEvent.click(screen.getByRole('button', { name:'Study this block' }));
  expect(onStudyNow).toHaveBeenCalledWith(expect.objectContaining({ subject:expect.stringMatching(/Geography|Irish/),durationMinutes:expect.any(Number),dateKey:expect.stringMatching(/^\d{4}-\d{2}-\d{2}$/),blockId:expect.any(String) }));
});

test('a fresh profile uses the existing planner and settings without an availability questionnaire', () => {
  const onSettings = vi.fn();
  const { container } = render(<SpacedRepetitionTimetable profile={profile} uid="original-planner-cold-start" onOpenSettings={vi.fn()} onPlanSettingsChange={onSettings} />);
  expect(container.querySelector('.nsu-planner .pp-week-grid')).not.toBeNull();
  expect(screen.getByText('The balance of your week')).toBeInTheDocument();
  expect(screen.queryByText('Make room for your real week.')).not.toBeInTheDocument();
  expect(readStudyPlan('original-planner-cold-start')!.plan.tasks.length).toBeGreaterThan(0);
  fireEvent.click(screen.getByRole('button', { name: 'Plan settings' }));
  const dialog = screen.getByRole('dialog');
  expect(within(dialog).getByText('Make room for your week.')).toBeInTheDocument();
  fireEvent.change(within(dialog).getByLabelText('Minutes per block'), { target: { value: '90' } });
  fireEvent.click(within(dialog).getByRole('button', { name: 'Save plan settings' }));
  expect(onSettings).toHaveBeenCalledWith(['Sunday'], 90);
});

test('the original completion and undo controls update the shared task identity', async () => {
  const onToggleCompletion = vi.fn();
  const { container } = render(<SpacedRepetitionTimetable profile={profile} uid="original-planner-completion" onOpenSettings={vi.fn()} onToggleCompletion={onToggleCompletion} />);
  fireEvent.click(screen.getByRole('button', { name: 'Already studied' }));
  const [date, id] = onToggleCompletion.mock.calls[0];
  expect(readStudyPlan('original-planner-completion')!.plan.tasks.find(task => task.id === id)).toMatchObject({date, status: 'completed'});
  fireEvent.click(container.querySelector('.pp-block[data-status="done"]')!);
  fireEvent.click(await screen.findByRole('button', { name: 'Undo' }));
  expect(readStudyPlan('original-planner-completion')!.plan.tasks.find(task => task.id === id)?.status).toBe('planned');
  expect(onToggleCompletion).toHaveBeenLastCalledWith(date, id, false);
});

test('existing week navigation can launch a task beyond the stored fortnight', async () => {
  const onStudyNow = vi.fn();
  render(<SpacedRepetitionTimetable profile={profile} uid="original-planner-future" onOpenSettings={vi.fn()} onStudyNow={onStudyNow} />);
  fireEvent.click(screen.getByRole('button', { name: 'Next timetable week' }));
  fireEvent.click(screen.getByRole('button', { name: 'Next timetable week' }));
  fireEvent.click(screen.getAllByRole('button', { name: /Irish Practice/ })[0]);
  await waitFor(() => expect(within(screen.getByRole('complementary', {name: 'Selected study block'})).getByText('Irish')).toBeInTheDocument());
  fireEvent.click(screen.getByRole('button', { name: 'Study this block' }));
  const launched = onStudyNow.mock.calls[0][0];
  expect(launched.dateKey >= addDays(mondayOf(dateKey(new Date())), 14)).toBe(true);
  expect(readStudyPlan('original-planner-future')!.plan.tasks.find(task => task.id === launched.blockId)).toMatchObject({date: launched.dateKey, locked: true});
});
