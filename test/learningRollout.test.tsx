import React, { useState } from 'react';
import { fireEvent, render, screen, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { ModuleLayout } from '@/components/ModuleLayout';
import { Cite, ModuleReferencesProvider } from '@/components/ModuleReferences';
import KobraScope from '../components/approved-ui-runtime';
import { BIMODAL_BRAIN_REFERENCE_LIST } from '@/data/references/bimodalBrain';
import { requestModuleSection, learningState } from '@/components/learning/data';
import { ALL_COURSES } from '@/courseData';
import type { ModuleProgress, ModuleTheme } from '@/types';

const reading = vi.hoisted(() => ({ essentials: false }));
vi.mock('@/hooks/useEssentialsMode', () => ({ useEssentialsMode: () => reading.essentials }));
vi.mock('@/contexts/NavigationContext', () => ({ useNavigation: () => ({ state: { currentModuleId: 'test-module' }, navigateToStudySession: vi.fn() }) }));
afterEach(cleanup);
beforeEach(() => { window.scrollTo = vi.fn(); reading.essentials = false; });
const icon = () => <svg />;
const sections = [0,1,2].map(index => ({ id: `part-${index}`, title: `Part ${index + 1}`, eyebrow: `0${index + 1} // Learn`, icon }));
function Reader({ unlocked = 1, fullCount, changed = vi.fn() }: { unlocked?: number; fullCount?: number; changed?: (value: unknown) => void }) {
  const [progress, setProgress] = useState<ModuleProgress>({ unlockedSection: unlocked });
  return <ModuleLayout moduleNumber="01" moduleTitle="Real learning" theme={{} as ModuleTheme} sections={sections} onBack={vi.fn()} progress={progress} onProgressUpdate={value => { changed(value); setProgress(value); }} fullSectionsCount={fullCount} references={BIMODAL_BRAIN_REFERENCE_LIST}>{index => <><h1>Reading part {index + 1}</h1><input aria-label="Exercise answer" /><p>A supported claim.<Cite n={1} /></p></>}</ModuleLayout>;
}
test('reader retains the exercise when Contents closes, and opens unread sections without awarding reading', async () => {
  const changed = vi.fn(); render(<Reader changed={changed} />);
  const input = screen.getByRole('textbox', { name: 'Exercise answer' });
  fireEvent.change(input, { target: { value: 'My work so far' } });
  fireEvent.click(screen.getByRole('button', { name: 'Collapse module navigation' }));
  expect(screen.getByRole('textbox', { name: 'Exercise answer' })).toBe(input);
  expect(input).toHaveValue('My work so far');
  fireEvent.click(screen.getByRole('button', { name: 'Expand module navigation' }));
  fireEvent.click(screen.getByRole('button', { name: /Part 3.*Open section/ }));
  expect(await screen.findByRole('heading', { name: 'Reading part 3' })).toBeInTheDocument();
  expect(changed).toHaveBeenCalledWith(expect.objectContaining({ unlockedSection: 1, reading: expect.objectContaining({ lastSectionId: 'part-2', sectionsByMode: { full: ['part-0'] } }) }));
  expect(screen.getByRole('progressbar', { name: 'Reading progress' })).toHaveAttribute('aria-valuenow', '1');
});
test('completing a real section persists progress, and revisiting does not award it again', async () => {
  const changed = vi.fn(); render(<Reader changed={changed} />);
  fireEvent.click(screen.getByRole('button', { name: /Part 1.*Read/ }));
  await screen.findByRole('heading', { name: 'Reading part 1' });
  fireEvent.click(screen.getByRole('button', { name: 'Continue to the next section' }));
  // Revisiting records a resume location without awarding a second read.
  expect(changed.mock.calls.every(([value]) => value.unlockedSection === 1)).toBe(true);
  await screen.findByRole('heading', { name: 'Reading part 2' });
  await new Promise(resolve => setTimeout(resolve, 510));
  fireEvent.click(screen.getByRole('button', { name: 'Continue to the next section' }));
  expect(changed).toHaveBeenLastCalledWith(expect.objectContaining({ unlockedSection: 2, reading: expect.objectContaining({ sectionsByMode: { full: ['part-0', 'part-1'] } }) }));
  expect(screen.getByRole('progressbar', { name: 'Reading progress' })).toHaveAttribute('aria-valuenow', '2');
});
test('essential-mode completion still reports the full module count and clamps the reader bar', async () => {
  reading.essentials = true;
  const changed = vi.fn(); render(<Reader unlocked={2} fullCount={8} changed={changed} />);
  fireEvent.click(screen.getByRole('button', { name: 'Complete Section' }));
  expect(changed).toHaveBeenCalledWith(expect.objectContaining({ unlockedSection: 8, reading: expect.objectContaining({ lastMode: 'essentials', sectionsByMode: { essentials: ['part-0', 'part-1', 'part-2'] } }) }));
  expect(screen.getByRole('progressbar', { name: 'Reading progress' })).toHaveAttribute('aria-valuenow', '3');
});
test('a world section selection survives strict mode and clamps out-of-range requests without awarding reading', () => {
  requestModuleSection('test-module', 0);
  const first = render(<React.StrictMode><Reader unlocked={1} /></React.StrictMode>);
  expect(screen.getByRole('heading', { name: 'Reading part 1' })).toBeInTheDocument();
  first.unmount();
  requestModuleSection('test-module', 50);
  const changed = vi.fn();
  render(<React.StrictMode><Reader unlocked={1} changed={changed} /></React.StrictMode>);
  expect(screen.getByRole('heading', { name: 'Reading part 3' })).toBeInTheDocument();
  expect(changed).not.toHaveBeenCalled();
});
test('Kobra bubbles expose the real claim sources, including multi-source navigation and DOI links', async () => {
  const user = userEvent.setup();
  render(<KobraScope><ModuleReferencesProvider value={BIMODAL_BRAIN_REFERENCE_LIST}><p>A claim<Cite n={[1,2]} /></p></ModuleReferencesProvider></KobraScope>);
  await user.click(screen.getByRole('button', { name: /^2 sources:/ }));
  const first = BIMODAL_BRAIN_REFERENCE_LIST[0]; const second = BIMODAL_BRAIN_REFERENCE_LIST[1];
  expect(screen.getByRole('link', { name: new RegExp(first.title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) })).toHaveAttribute('href', `https://doi.org/${first.doi}`);
  await user.click(screen.getByRole('button', { name: 'Next source' }));
  expect(screen.getByText('2/2')).toBeInTheDocument();
  const secondLink = screen.getAllByRole('link').find(link => link.textContent?.includes(second.title));
  expect(secondLink).toHaveAttribute('href', `https://doi.org/${second.doi}`);
});
test('empty and out-of-range progress never fabricates completion or a next course', () => {
  const state = learningState({}); expect(state.nextCourse([])).toBeUndefined();
  const course = ALL_COURSES[0]; expect(state.isComplete(course)).toBe(false);
  expect(learningState({ [course.id]: { unlockedSection: -3 } }).sectionCount(course)).toBe(0);
  expect(learningState({ [course.id]: { unlockedSection: 1000 } }).sectionCount(course)).toBe(course.sectionsCount);
});
