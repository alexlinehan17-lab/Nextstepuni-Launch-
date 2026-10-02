import React from 'react';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import PlannerWorkbench, { plannerEntries, workloadLedger } from '@/components/launchpad/PlannerWorkbench';
import { readPlannerTodos } from '@/components/launchpad/plannerTodos';
import { DAYS_OF_WEEK, type WeeklyTimetable } from '@/components/subjectData';

afterEach(cleanup);
beforeEach(() => { localStorage.clear(); });
const timetable: WeeklyTimetable = DAYS_OF_WEEK.map((day, index) => ({ day, blocks: index === 0 ? [{ subjectName:'Geography', sessionType:'practice', durationMinutes:30 }, { subjectName:'Irish', sessionType:'revision', durationMinutes:45 }] : index === 2 ? [{ subjectName:'Geography', sessionType:'new-learning', durationMinutes:60 }] : [] }));
const weekStart = new Date(2026,8,28);
function props() { return { uid:'student-a', timetable, subjects:['Geography','Irish'], weekStart, weekOffset:0, onWeekChange:vi.fn(), restDays:['Sunday'], duration:45, onSettings:vi.fn(), onPlanSettingsChange:vi.fn(), isComplete:() => false, isSkipped:() => false, onComplete:vi.fn(), onSkip:vi.fn(), onStudy:vi.fn(), schoolEvents:[], hints:{}, cues:{}, onCueSave:vi.fn(), explanation:<p>The real allocation.</p> }; }

test('uses each scheduled duration for the full-width subject ledger', () => {
  expect(workloadLedger(timetable, ['Geography','Irish'])).toEqual([{ subject:'Geography', minutes:90 }, { subject:'Irish', minutes:45 }]);
  render(<PlannerWorkbench {...props()} />);
  const ledger = screen.getByText('The balance of your week').closest('.pp-workload')!;
  expect(within(ledger as HTMLElement).getByText('1h 30m')).toBeInTheDocument();
  expect(within(ledger as HTMLElement).getByText('45m')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name:'Behind your plan' }));
  expect(screen.getByText('The real allocation.')).toBeInTheDocument();
});
test('the selected block keeps its real date and stable block id when started or completed', async () => {
  const handlers = props(); render(<PlannerWorkbench {...handlers} />);
  fireEvent.click(screen.getByRole('button', { name:/Irish Revision/ }));
  await waitFor(() => expect(within(screen.getByRole('complementary', { name:'Selected study block' })).getByText('Irish')).toBeInTheDocument());
  fireEvent.click(screen.getByRole('button', { name:'Study this block' }));
  const entry = plannerEntries(timetable, weekStart)[1];
  expect(handlers.onStudy).toHaveBeenCalledWith(entry);
  fireEvent.click(screen.getByRole('button', { name:'Already studied' }));
  expect(handlers.onComplete).toHaveBeenCalledWith(entry, true);
  fireEvent.click(screen.getByRole('button', { name:'Skip this block' }));
  expect(handlers.onSkip).toHaveBeenCalledWith(entry, true);
});
test('editing to-dos blocks the start shortcut and keeps account/date/block-scoped work for Study Room', async () => {
  const handlers = props(); const user = userEvent.setup(); render(<PlannerWorkbench {...handlers} />);
  await user.click(screen.getByRole('button', { name:'Edit to-dos' }));
  const dialog = screen.getByRole('dialog', { name:'Edit your to-dos' });
  const input = within(dialog).getByRole('textbox', { name:'To-do 1' });
  await user.clear(input); await user.type(input, 'Practise river processes');
  fireEvent.keyDown(window, { key:'Enter', metaKey:true }); expect(handlers.onStudy).not.toHaveBeenCalled();
  await user.click(within(dialog).getByRole('button', { name:'Save to-dos' }));
  const entry = plannerEntries(timetable, weekStart)[0];
  expect(readPlannerTodos('student-a',entry.dateKey,entry.id)?.[0].label).toBe('Practise river processes');
  expect(readPlannerTodos('student-b',entry.dateKey,entry.id)).toBeNull();
  expect(readPlannerTodos('student-a','2026-10-05',entry.id)).toBeNull();
});
test('rest days and duration save atomically and rest days are capped at three', async () => {
  const handlers = props(); const user = userEvent.setup(); render(<PlannerWorkbench {...handlers} />);
  await user.click(screen.getByRole('button', { name:'Plan settings' }));
  const dialog = screen.getByRole('dialog', { name:'Make room for your week.' });
  await user.click(within(dialog).getByRole('checkbox', { name:'Saturday' }));
  await user.click(within(dialog).getByRole('checkbox', { name:'Friday' }));
  expect(within(dialog).getByRole('checkbox', { name:'Thursday' })).toHaveAttribute('aria-disabled', 'true');
  await user.click(within(dialog).getByRole('checkbox', { name:'Thursday' }));
  expect(within(dialog).getByRole('checkbox', { name:'Thursday' })).toHaveAttribute('aria-checked', 'false');
  await user.selectOptions(within(dialog).getByRole('combobox'), '30');
  await user.click(within(dialog).getByRole('button', { name:'Save plan settings' }));
  expect(handlers.onPlanSettingsChange).toHaveBeenCalledWith(['Sunday','Saturday','Friday'],30);
});

test('week view omits empty rest days but retains school events and day navigation', async () => {
  render(<PlannerWorkbench {...props()} schoolEvents={[{ id:'event', date:'2026-09-29', title:'School assembly', category:'school', yearGroup:'all', createdAt:'2026-09-27T12:00:00Z' }]} />);
  const schedule = screen.getByRole('region', { name:'Your study schedule' });
  expect(within(schedule).queryByText('Room to recharge.')).not.toBeInTheDocument();
  expect(within(schedule).getByText('School assembly')).toBeInTheDocument();
  expect(within(schedule).queryByRole('button', { name:/Thursday/ })).not.toBeInTheDocument();
  await userEvent.click(screen.getByRole('tab', { name:/^Day$/ }));
  expect(screen.getByRole('button', { name:/Thu/ })).toBeInTheDocument();
});
