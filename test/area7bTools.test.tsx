/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 7b: the Launchpad tools in the agreed look keep their working. Coursework Studio's six parts
 * open from one menu ("Overview 1 of 6", board c-tools2-coursework) and a project still saves as before.
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import CourseworkStudio from '../components/CourseworkStudio/CourseworkStudio';
import { courseworkDemo } from '../components/CourseworkStudio/demo';
import type { CourseworkWorkspace } from '../components/CourseworkStudio/model';
import type { CourseworkStore } from '../components/CourseworkStudio/store';

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
