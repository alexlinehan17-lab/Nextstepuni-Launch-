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
import type { ModuleTheme } from '@/types';

vi.mock('@/contexts/NavigationContext', () => ({ useNavigation: () => ({ state: { currentModuleId: 'test-module' }, navigateToStudySession: vi.fn() }) }));
afterEach(cleanup);
beforeEach(() => { window.scrollTo = vi.fn(); });
const icon = () => <svg />;
const sections = [0,1,2].map(index => ({ id: `part-${index}`, title: `Part ${index + 1}`, eyebrow: `0${index + 1} // Learn`, icon }));
function Reader({ unlocked = 1, fullCount, changed = vi.fn() }: { unlocked?: number; fullCount?: number; changed?: (value: unknown) => void }) {
  const [progress, setProgress] = useState({ unlockedSection: unlocked });
  return <ModuleLayout moduleNumber="01" moduleTitle="Real learning" theme={{} as ModuleTheme} sections={sections} onBack={vi.fn()} progress={progress} onProgressUpdate={value => { changed(value); setProgress(value); }} fullSectionsCount={fullCount} references={BIMODAL_BRAIN_REFERENCE_LIST}>{index => <><h1>Reading part {index + 1}</h1><input aria-label="Exercise answer" /><p>A supported claim.<Cite n={1} /></p></>}</ModuleLayout>;
}
test('reader retains the exercise when Contents closes, and locks future sections', () => {
  render(<Reader />);
  const input = screen.getByRole('textbox', { name: 'Exercise answer' });
  fireEvent.change(input, { target: { value: 'My work so far' } });
  fireEvent.click(screen.getByRole('button', { name: 'Collapse module navigation' }));
  expect(screen.getByRole('textbox', { name: 'Exercise answer' })).toBe(input);
  expect(input).toHaveValue('My work so far');
  fireEvent.click(screen.getByRole('button', { name: 'Expand module navigation' }));
  expect(screen.getByRole('button', { name: /Part 3.*Coming next/ })).toBeDisabled();
  expect(screen.getByRole('progressbar', { name: 'Module completion' })).toHaveAttribute('aria-valuenow', '1');
});
test('completing a real section persists progress, and revisiting does not award it again', async () => {
  const changed = vi.fn(); render(<Reader changed={changed} />);
  fireEvent.click(screen.getByRole('button', { name: /Part 1.*Read/ }));
  await screen.findByRole('heading', { name: 'Reading part 1' });
  fireEvent.click(screen.getByRole('button', { name: 'Continue to the next section' }));
  expect(changed).not.toHaveBeenCalled();
  await screen.findByRole('heading', { name: 'Reading part 2' });
  await new Promise(resolve => setTimeout(resolve, 510));
  fireEvent.click(screen.getByRole('button', { name: 'Continue to the next section' }));
  expect(changed).toHaveBeenCalledWith({ unlockedSection: 2 });
  expect(screen.getByRole('progressbar', { name: 'Module completion' })).toHaveAttribute('aria-valuenow', '2');
});
test('essential-mode completion still reports the full module count and clamps the reader bar', async () => {
  const changed = vi.fn(); render(<Reader unlocked={2} fullCount={8} changed={changed} />);
  fireEvent.click(screen.getByRole('button', { name: 'Complete Section' }));
  expect(changed).toHaveBeenCalledWith({ unlockedSection: 8 });
  expect(screen.getByRole('progressbar', { name: 'Module completion' })).toHaveAttribute('aria-valuenow', '3');
});
test('a world section selection survives strict mode and cannot unlock a future section', () => {
  requestModuleSection('test-module', 0);
  const first = render(<React.StrictMode><Reader unlocked={1} /></React.StrictMode>);
  expect(screen.getByRole('heading', { name: 'Reading part 1' })).toBeInTheDocument();
  first.unmount();
  requestModuleSection('test-module', 50);
  render(<React.StrictMode><Reader unlocked={1} /></React.StrictMode>);
  expect(screen.getByRole('heading', { name: 'Reading part 2' })).toBeInTheDocument();
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
