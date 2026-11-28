/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 5 of the design build: reading a module on a phone (board c-read-flow). It opens on a title
 * page and Continue reading picks up at the saved step; one step per screen with one Continue that
 * records reading exactly as before; Contents and Notes are sheets; notes save as you type; the
 * sources open the same list; finishing reports progress as before.
 */
import React, { useState } from 'react';
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';

const device = vi.hoisted(() => ({ phone: true }));
const nav = vi.hoisted(() => ({ navigateToStudySession: vi.fn() }));
vi.mock('@/hooks/useCompactLayout', () => ({ useCompactLayout: () => device.phone }));
vi.mock('@/hooks/useEssentialsMode', () => ({ useEssentialsMode: () => false }));
vi.mock('@/contexts/NavigationContext', () => ({ useNavigation: () => ({ state: { currentModuleId: 'agency-architecture-protocol' }, navigateToStudySession: nav.navigateToStudySession }), useOptionalNavigation: () => null, useBackStep: () => {} }));
vi.mock('@/contexts/AuthContext', () => ({ useAuth: () => ({ user: { uid: 'reader-a' } }) }));
vi.mock('@/firebase', () => ({ db: {}, auth: { currentUser: { uid: 'reader-a' } } }));
vi.mock('firebase/firestore', () => ({ doc: (...parts: unknown[]) => parts, getDoc: vi.fn().mockResolvedValue({ exists: () => false }), setDoc: vi.fn().mockResolvedValue(undefined), FieldPath: class { constructor(public parts: unknown) {} } }));

import { ModuleLayout } from '@/components/ModuleLayout';
import { ReadingSection } from '@/components/ModuleShared';
import { requestModuleResume } from '@/components/learning/intents';
import { BIMODAL_BRAIN_REFERENCE_LIST } from '@/data/references/bimodalBrain';
import { forgetModuleResponseMemory } from '@/services/moduleResponseStore';
import type { ModuleProgress, ModuleTheme } from '@/types';

beforeEach(() => { window.scrollTo = vi.fn(); forgetModuleResponseMemory(); localStorage.clear(); nav.navigateToStudySession.mockReset(); device.phone = true; });
afterEach(cleanup);

const icon = () => <svg />;
const sections = [0, 1, 2, 3, 4].map(index => ({ id: `part-${index}`, title: `Part ${index + 1}`, eyebrow: `0${index + 1} // Name ${index + 1}`, icon }));
function Reader({ start, changed = vi.fn(), onBack = vi.fn() }: { start: ModuleProgress; changed?: (value: ModuleProgress) => void; onBack?: () => void }) {
  const [progress, setProgress] = useState<ModuleProgress>(start);
  return (
    <ModuleLayout moduleNumber="06" moduleTitle="Controlling the Controllables" moduleSubtitle="The Attribution Retraining Guide" theme={{} as ModuleTheme}
      sections={sections} onBack={onBack} progress={progress} onProgressUpdate={value => { changed(value); setProgress(value); }}
      references={BIMODAL_BRAIN_REFERENCE_LIST} finishButtonText="Take the Controls">
      {index => <ReadingSection title={`Reading part ${index + 1}`} eyebrow={`Step ${index + 1}`} icon={icon} theme={{} as ModuleTheme}><p>Words of part {index + 1}.</p></ReadingSection>}
    </ModuleLayout>
  );
}
/** 3 of 5 read, stopped at step 4 (as the Demo Student is in Controlling the Controllables). */
const partway: ModuleProgress = { unlockedSection: 3, reading: { sectionsByMode: { full: ['part-0', 'part-1', 'part-2'] }, lastSectionId: 'part-3', lastSectionIndex: 3, lastMode: 'full', lastVisitedAt: '2026-11-20T10:00:00.000Z' } };

describe('reading a module on a phone', () => {
  test('it opens on its title page, and Continue reading picks up at the saved step', async () => {
    render(<Reader start={partway} />);
    expect(screen.getByRole('heading', { name: 'Controlling the Controllables', level: 1 })).toBeInTheDocument();
    expect(screen.getByText('You stopped at step 4, Part 4.')).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Reading part 4' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue reading' }));
    expect(await screen.findByRole('heading', { name: 'Reading part 4' })).toBeInTheDocument();
    expect(screen.getByText(/Step/, { selector: '.rs-eyebrow' })).toHaveTextContent('Step 4 of 5 · Name 4');
  });

  test('a student picking up where they left off lands on their step, with no title page', async () => {
    requestModuleResume('agency-architecture-protocol');
    const changed = vi.fn();
    render(<Reader start={partway} changed={changed} />);
    expect(await screen.findByRole('heading', { name: 'Reading part 4' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Continue reading' })).not.toBeInTheDocument();
    expect(changed).not.toHaveBeenCalled();
  });

  test('Continue moves one step and records reading exactly as before; the footer names the next step', async () => {
    requestModuleResume('agency-architecture-protocol');
    const changed = vi.fn();
    render(<Reader start={partway} changed={changed} />);
    expect(screen.getByText('Part 5', { selector: '.rd-next' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue to the next section' }));
    expect(changed).toHaveBeenLastCalledWith(expect.objectContaining({ unlockedSection: 4, reading: expect.objectContaining({ lastSectionId: 'part-4', lastSectionIndex: 4, sectionsByMode: { full: ['part-0', 'part-1', 'part-2', 'part-3'] } }) }));
    expect(await screen.findByRole('heading', { name: 'Reading part 5' })).toBeInTheDocument();
    expect(screen.getByText('Your last page. Yours to revisit.')).toBeInTheDocument();
  });

  test('Contents is a sheet listing every step; it jumps to a step as today and records only where you are', async () => {
    requestModuleResume('agency-architecture-protocol');
    const changed = vi.fn();
    render(<Reader start={partway} changed={changed} />);
    fireEvent.click(screen.getByRole('button', { name: 'Contents' }));
    const sheet = screen.getByRole('dialog', { name: 'Contents' });
    const steps = within(sheet).getAllByRole('button', { name: /^Part \d\./ });
    expect(steps).toHaveLength(5);
    expect(within(sheet).getByRole('button', { name: /Part 4\. You’re here/ })).toBeInTheDocument();
    fireEvent.click(within(sheet).getByRole('button', { name: /Part 2\. Read/ }));
    expect(await screen.findByRole('heading', { name: 'Reading part 2' })).toBeInTheDocument();
    expect(changed).toHaveBeenLastCalledWith(expect.objectContaining({ unlockedSection: 3, reading: expect.objectContaining({ lastSectionId: 'part-1', sectionsByMode: { full: ['part-0', 'part-1', 'part-2'] } }) }));
  });

  test('the sources open the same list as before, from Contents', async () => {
    requestModuleResume('agency-architecture-protocol');
    render(<Reader start={partway} />);
    fireEvent.click(screen.getByRole('button', { name: 'Contents' }));
    fireEvent.click(within(screen.getByRole('dialog', { name: 'Contents' })).getByRole('button', { name: /Sources and further reading/ }));
    const list = await screen.findByRole('dialog', { name: 'Sources & further reading' });
    for (const reference of BIMODAL_BRAIN_REFERENCE_LIST) expect(within(list).getByText(reference.title, { exact: false })).toBeInTheDocument();
  });

  test('notes save as you type: no Done, and they are there after leaving and coming back', async () => {
    requestModuleResume('agency-architecture-protocol');
    const first = render(<Reader start={partway} />);
    fireEvent.click(screen.getByRole('button', { name: 'Notes' }));
    const sheet = screen.getByRole('dialog', { name: 'Notes' });
    const notes = within(sheet).getByRole('textbox', { name: 'Your notes' });
    await waitFor(() => expect(notes).toBeEnabled());
    expect(within(sheet).queryByRole('button', { name: 'Done' })).not.toBeInTheDocument();
    fireEvent.change(notes, { target: { value: 'Two buckets: what I control and what I don’t.' } });
    fireEvent.click(within(sheet).getByRole('button', { name: 'Close' }));
    await act(async () => { await new Promise(resolve => setTimeout(resolve, 400)); });
    first.unmount();
    // leave the module and come back to it
    requestModuleResume('agency-architecture-protocol');
    render(<Reader start={partway} />);
    fireEvent.click(screen.getByRole('button', { name: 'Notes' }));
    expect(within(screen.getByRole('dialog', { name: 'Notes' })).getByRole('textbox', { name: 'Your notes' })).toHaveValue('Two buckets: what I control and what I don’t.');
  });

  test('finishing reports progress exactly as before; Start a study session stays the main action', async () => {
    const last: ModuleProgress = { unlockedSection: 4, reading: { sectionsByMode: { full: ['part-0', 'part-1', 'part-2', 'part-3'] }, lastSectionId: 'part-4', lastSectionIndex: 4, lastMode: 'full', lastVisitedAt: '2026-11-20T10:00:00.000Z' } };
    requestModuleResume('agency-architecture-protocol');
    const changed = vi.fn(); const onBack = vi.fn();
    render(<Reader start={last} changed={changed} onBack={onBack} />);
    fireEvent.click(screen.getByRole('button', { name: 'Take the Controls' }));
    expect(changed).toHaveBeenLastCalledWith(expect.objectContaining({ unlockedSection: 5, reading: expect.objectContaining({ sectionsByMode: { full: ['part-0', 'part-1', 'part-2', 'part-3', 'part-4'] } }) }));
    const done = await screen.findByRole('dialog', { name: 'Something to take with you.' });
    expect(within(done).getByText('5 / 5')).toBeInTheDocument();
    fireEvent.click(within(done).getByRole('button', { name: 'Start a study session' }));
    expect(nav.navigateToStudySession).toHaveBeenCalledOnce();
    expect(onBack).not.toHaveBeenCalled();
  });

  test('on a laptop today\'s bones stay: no title page, the steps down the left, the step in its box', async () => {
    device.phone = false;
    render(<Reader start={partway} />);
    expect(await screen.findByRole('heading', { name: 'Reading part 4' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Continue reading' })).not.toBeInTheDocument();
    const steps = screen.getByRole('complementary', { name: 'Module navigation' });
    expect(within(steps).getAllByRole('button', { name: /^Part \d\./ })).toHaveLength(5);
    expect(within(steps).getByRole('progressbar', { name: 'Reading progress' })).toHaveAttribute('aria-valuenow', '3');
    expect(screen.getByText(/step 5 of 5/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Collapse module navigation' }));
    expect(steps).toHaveAttribute('inert');
  });
});
