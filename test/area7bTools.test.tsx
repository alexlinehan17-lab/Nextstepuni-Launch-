/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 7b: the Launchpad tools in the agreed look keep their working. Coursework Studio's six parts
 * open from one menu ("Overview 1 of 6", board c-tools2-coursework) and a project still saves as before;
 * the Comeback Engine's Continue walks its steps and the seven-day count is today's arithmetic.
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import CourseworkStudio from '../components/CourseworkStudio/CourseworkStudio';
import { courseworkDemo } from '../components/CourseworkStudio/demo';
import type { CourseworkWorkspace } from '../components/CourseworkStudio/model';
import type { CourseworkStore } from '../components/CourseworkStudio/store';
import ComebackEngineV2 from '../components/ComebackEngineV2';
import { buildRecoveryPlan } from '../components/comeback/recoveryPlan';
import { DEMO_STUDENT_UID, createDevStudentProfile } from '../data/devStudent';
import CommandWordReflex from '../components/CommandWordReflex';
import { questionsForSubject } from '../commandWordData';

const progressDoc: { current: Record<string, unknown> } = { current: {} };
const updateDemoProgress = vi.fn((update: (current: Record<string, unknown>) => Record<string, unknown>) => { progressDoc.current = update(progressDoc.current); });
vi.mock('@/contexts/AuthContext', () => ({ useAuth: () => ({ user: null }) }));
vi.mock('@/contexts/InnovationDataContext', () => ({ useInnovationData: () => ({ topicMastery: { canonicalMastery: { topics: {} } }, subjectPriorities: [] }) }));
const recordResult = vi.fn();
vi.mock('@/hooks/useCommandWordReflex', () => ({ useCommandWordReflex: () => ({ state: { seenIds: [], firstTryIds: [], wordsMet: [], attempts: 0, updatedAt: '' }, isLoaded: true, recordResult }) }));
vi.mock('@/contexts/ProgressContext', () => ({ useOptionalProgress: () => ({ rawProgressDoc: progressDoc.current, updateDemoProgress }) }));

function memoryStore(value: CourseworkWorkspace = courseworkDemo()): CourseworkStore {
  let saved = structuredClone(value);
  return {
    load: vi.fn(async () => structuredClone(saved)),
    save: vi.fn(async (_owner, next) => { saved = { ...structuredClone(next), revision: saved.revision + 1 }; return saved; }),
  };
}

describe('Coursework Studio (area 7b)', () => {
  test('the six parts of a project open from one menu, with the count', async () => {
    render(<CourseworkStudio uid="student-7b" storage={memoryStore()} />);
    await screen.findByRole('heading', { name: 'The changing working day' });
    expect(screen.queryByRole('tab')).toBeNull();
    const menu = () => screen.getByRole('button', { name: /Coursework workspace views/ });
    expect(menu()).toHaveTextContent('Overview');
    expect(menu()).toHaveTextContent('1 of 6');
    const shows: [RegExp | string, string][] = [
      [/^Evidence/, 'Your evidence, with a reason.'], ['Connections', 'Make the connection.'], ['Plan', 'Make room for the work.'],
      ['Brief', 'Know what applies to you.'], ['Review', 'Be ready to explain your work.'], ['Overview', 'Keep the thread.'],
    ];
    for (const [part, heading] of shows) {
      fireEvent.click(menu());
      fireEvent.click(await screen.findByRole('menuitemradio', { name: part }));
      expect(await screen.findByRole('heading', { name: heading })).toBeInTheDocument();
    }
  });

  test('the name is said once: no masthead, no second title, Start my first project on the first screen', async () => {
    render(<CourseworkStudio uid="student-7b-empty" storage={memoryStore({ ...courseworkDemo(), projects: [] })} />);
    expect(await screen.findByRole('button', { name: 'Start my first project' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Your work\.\s*A clear way forward\./ })).toBeInTheDocument();
    expect(screen.queryByText(/NextStepUni \/ Coursework Studio/i)).toBeNull();
    expect(screen.getByRole('button', { name: 'Back up' })).toHaveAttribute('aria-disabled', 'true');
    expect(screen.getByRole('button', { name: 'Import' })).toBeInTheDocument();
  });

  test('a plan step ticks and saves as before', async () => {
    const store = memoryStore();
    render(<CourseworkStudio uid="student-7b-plan" storage={store} />);
    await screen.findByRole('heading', { name: 'The changing working day' });
    fireEvent.click(screen.getByRole('button', { name: /Coursework workspace views/ }));
    fireEvent.click(await screen.findByRole('menuitemradio', { name: 'Plan' }));
    const step = courseworkDemo().projects[0].milestones.find(m => !m.done)!;
    const check = screen.getByRole('checkbox', { name: `Complete ${step.label}` });
    expect(check).toHaveAttribute('aria-checked', 'false');
    fireEvent.click(check);
    await waitFor(() => expect(store.save).toHaveBeenCalled());
    const saved = (store.save as ReturnType<typeof vi.fn>).mock.calls[0][1] as CourseworkWorkspace;
    expect(saved.projects[0].milestones.find(m => m.label === step.label)?.done).toBe(true);
  });

  test('the editor is the shared sheet and keeps its fields', async () => {
    render(<CourseworkStudio uid="student-7b-sheet" storage={memoryStore()} />);
    await screen.findByRole('heading', { name: 'The changing working day' });
    fireEvent.click(screen.getByRole('button', { name: 'Capture evidence' }));
    const sheet = screen.getByRole('dialog');
    expect(sheet).toHaveClass('ui-sheet');
    expect(within(sheet).getByLabelText('Type of evidence')).toBeInTheDocument();
    expect(within(sheet).getByRole('button', { name: 'Save evidence' })).toHaveAttribute('aria-disabled', 'true');
    fireEvent.change(within(sheet).getByLabelText('Give it a useful name'), { target: { value: 'A note' } });
    fireEvent.change(within(sheet).getByLabelText('What did you find, do or notice?'), { target: { value: 'Something I saw.' } });
    expect(within(sheet).getByRole('button', { name: 'Save evidence' })).not.toHaveAttribute('aria-disabled');
  });
});

describe('Comeback Engine (area 7b)', () => {
  test('Continue walks the four steps, the count is today\'s, a block ticks, and Rebuild plan asks first', async () => {
    progressDoc.current = {};
    sessionStorage.clear();
    const profile = createDevStudentProfile();
    render(<ComebackEngineV2 uid={DEMO_STUDENT_UID} profile={profile} timetableCompletions={{}} />);
    expect(await screen.findByRole('heading', { name: 'No judgement. Just a better starting point.' })).toBeInTheDocument();
    expect(screen.getByText('Step 1 of 4')).toBeInTheDocument();
    const momentum = screen.getByRole('radio', { name: /I lost momentum/ });
    fireEvent.click(momentum);
    expect(momentum).toHaveAttribute('aria-checked', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByRole('heading', { name: 'What can you genuinely manage?' })).toBeInTheDocument();
    expect(screen.getByText('Step 2 of 4')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: /Strong return/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Read my recovery signals' }));
    expect(await screen.findByRole('heading', { name: 'Here is what the app can actually see.' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Build my seven-day plan' }));
    expect(await screen.findByRole('heading', { name: 'A smaller plan. A little momentum.' })).toBeInTheDocument();

    // Today's arithmetic: the same plan the engine builds for these answers.
    const expected = buildRecoveryPlan({ profile, priorities: [], masteryEntries: [], timetableCompletions: {}, reason: 'motivation', capacity: 7, curriculumLevel: profile.curriculumLevel ?? 'senior', legacyAnchor: undefined });
    const count = () => document.querySelector('.cb7-count')?.textContent;
    expect(count()).toBe(`0 / ${expected.actions.length} blocks done`);
    expect(screen.getAllByRole('button', { name: 'Mark complete' })).toHaveLength(expected.actions.length);
    fireEvent.click(screen.getAllByRole('button', { name: 'Mark complete' })[0]);
    expect(count()).toBe(`1 / ${expected.actions.length} blocks done`);
    const saved = progressDoc.current.comebackRecoveryPlan as { actions: { done: boolean }[] };
    expect(saved.actions.filter(action => action.done)).toHaveLength(1);

    fireEvent.click(screen.getByRole('button', { name: 'Rebuild plan' }));
    const ask = await screen.findByRole('alertdialog', { name: 'Rebuild plan?' });
    fireEvent.click(within(ask).getByRole('button', { name: 'Keep this plan' }));
    expect(screen.getByRole('heading', { name: 'A smaller plan. A little momentum.' })).toBeInTheDocument();
    await waitFor(() => expect(screen.queryByRole('alertdialog')).toBeNull());
    fireEvent.click(screen.getByRole('button', { name: 'Rebuild plan' }));
    fireEvent.click(within(await screen.findByRole('alertdialog', { name: 'Rebuild plan?' })).getByRole('button', { name: 'Rebuild plan' }));
    expect(await screen.findByRole('heading', { name: 'No judgement. Just a better starting point.' })).toBeInTheDocument();
    expect(progressDoc.current.comebackRecoveryPlan).toBeNull();
  });
});

describe('Command-Word Reflex (area 7b)', () => {
  test('the example question leads with its command word marked, and a round scores as before', async () => {
    recordResult.mockClear();
    const { container } = render(<CommandWordReflex uid="u1" studentSubjects={['Accounting']} studentCycle="leaving-cert" />);
    const [first, second] = questionsForSubject('accounting').filter(q => q.level === 'common' || q.level === 'higher');
    expect(screen.getByText(/^Try the idea · Accounting/)).toBeInTheDocument();
    expect(container.querySelector('.cr7-cmd')?.textContent?.toLowerCase()).toBe(first.commandWord.toLowerCase());
    expect(screen.getByRole('button', { name: /^Accounting/ })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Start practising' }));
    expect(screen.getByText('Tap the command word: the cue telling you what to actually do.')).toBeInTheDocument();
    // A wrong word is struck through with the hint; the command word then scores "not first try".
    const words = [...container.querySelectorAll<HTMLButtonElement>('.cr7-word')];
    const cmd = first.commandWord.split(/\s+/)[0].replace(/[^a-z]/gi, '').toLowerCase();
    const wrong = words.find(word => word.textContent!.replace(/[^a-z]/gi, '').toLowerCase() !== cmd)!;
    fireEvent.click(wrong);
    expect(wrong).toHaveAttribute('data-wrong', 'true');
    expect(screen.getByText(/That’s a topic word/)).toBeInTheDocument();
    fireEvent.click(words.find(word => word.textContent!.replace(/[^a-z]/gi, '').toLowerCase() === cmd)!);
    expect(recordResult).toHaveBeenLastCalledWith(first.id, first.commandWord, false);
    expect(await screen.findByText('Read it like an examiner')).toBeInTheDocument();
    expect(container.querySelector('.cr7-hit')).not.toBeNull();
    // Next question; Reveal it scores "not first try" too, as before.
    fireEvent.click(screen.getByRole('button', { name: 'Next question' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Reveal it' }));
    expect(recordResult).toHaveBeenLastCalledWith(second.id, second.commandWord, false);
    expect(await screen.findByText(`The command word is “${second.commandWord}”`)).toBeInTheDocument();
  });
});
