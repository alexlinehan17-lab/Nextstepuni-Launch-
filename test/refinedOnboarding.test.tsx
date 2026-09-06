import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import Onboarding from '../components/Onboarding';
import { buildProfile, choiceReady, draftKey, emptyChoice, initialDraft, legacyDraftKey, pointsFor, readDraft, type SetupDraft } from '../components/onboarding/model';

vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
const uid = 'refined-setup-qa';
const key = draftKey(uid, 'fresh');
function reviewDraft(): SetupDraft {
  return { ...initialDraft(), step: 'summary', year: '6th', category: 'college-learning', vision: ['campus'], subjects: ['English', 'Irish', 'Japanese'],
    configs: { English: { level: 'ordinary', current: 'O2', target: 'O1', reviewed: true }, Irish: { level: 'higher', current: 'H3', target: 'H1', reviewed: true }, Japanese: { level: 'higher', current: 'H3', target: 'H1', reviewed: true } },
    date: '2030-06-05', dateConfirmed: true, rest: ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], gradeSubject: 'English' };
}
function mount(draft?: SetupDraft, complete = vi.fn()) {
  if (draft) localStorage.setItem(key, JSON.stringify(draft));
  return render(<Onboarding userId={uid} userName="Alex" onComplete={complete} onSkip={vi.fn()} />);
}
beforeEach(() => localStorage.clear());

describe('approved onboarding model', () => {
  it('never invents a level or grade for an LC subject', () => {
    expect(emptyChoice('6th', 'English')).toEqual({ level: null, current: '', target: '', reviewed: false });
    expect(choiceReady('6th', emptyChoice('6th', 'English'))).toBe(false);
  });
  it('uses common level only for genuinely common-level subjects', () => {
    expect(emptyChoice('2nd', 'Science').level).toBe('common');
    expect(emptyChoice('2nd', 'English').level).toBe(null);
    expect(emptyChoice('LCA1', 'English and Communications').level).toBe('common');
  });
  it('counts three confirmed subjects from 200 to 256 without a six-subject gate', () => {
    expect(pointsFor(reviewDraft())).toEqual({ count: 3, current: 200, target: 256 });
  });
  it('excludes unreviewed and deferred grades from partial totals', () => {
    const draft = reviewDraft();
    draft.configs.Japanese.reviewed = false;
    draft.configs.Irish.current = 'later';
    expect(pointsFor(draft)).toEqual({ count: 1, current: 46, target: 56 });
  });
  it('saves an explicitly deferred grade as absent, never as H4/H2', () => {
    const draft = reviewDraft();
    draft.configs.English = { level: 'ordinary', current: 'later', target: 'later', reviewed: true };
    expect(buildProfile(draft).subjects[0]).toEqual({ subjectName: 'English', level: 'ordinary' });
  });
  it('accepts a target below current without changing either answer', () => {
    const draft = reviewDraft();
    draft.configs.English = { level: 'higher', current: 'H1', target: 'H3', reviewed: true };
    expect(buildProfile(draft).subjects[0]).toMatchObject({ currentGrade: 'H1', targetGrade: 'H3' });
  });
  it('migrates old auto-filled drafts as unreviewed and requires date confirmation', () => {
    localStorage.setItem(legacyDraftKey(uid, 'fresh'), JSON.stringify({ version: 1, step: 9, yearGroup: '6th', selectedSubjects: ['English'], subjectConfigs: { English: { level: 'higher', currentGrade: 'H4', targetGrade: 'H2' } }, examDate: '2030-06-05', restDays: ['Sunday'] }));
    const draft = readDraft(uid, 'fresh');
    expect(draft.configs.English).toMatchObject({ current: 'H4', target: 'H2', reviewed: false });
    expect(draft.dateConfirmed).toBe(false);
    expect(pointsFor(draft).count).toBe(0);
  });
  it('recovers safely from malformed local storage and isolates accounts', () => {
    localStorage.setItem(key, '{bad');
    expect(readDraft(uid, 'fresh').step).toBe('welcome');
    localStorage.setItem(key, JSON.stringify(reviewDraft()));
    expect(readDraft('another-student', 'fresh').subjects).toEqual([]);
  });
  it('omits points for Junior Cycle and LCA', () => {
    const draft = reviewDraft();
    expect(pointsFor({ ...draft, year: '3rd' }).count).toBe(0);
    expect(pointsFor({ ...draft, year: 'LCA1' }).count).toBe(0);
  });
});

describe('approved onboarding interactions', () => {
  it('reveals the chosen motivation artwork and carries the choice into the vision board', () => {
    mount({ ...initialDraft(), step: 'north', year: '6th' });
    expect(screen.getByRole('img', { name: 'Find your direction illustration' })).toHaveAttribute('src', '/icons/onboarding/north-star.png');
    expect(screen.getByRole('button', { name: 'Continue' })).toBeDisabled();
    const learning = screen.getByRole('button', { name: 'Keep Learning' });
    learning.focus();
    fireEvent.click(learning);
    expect(learning).toHaveFocus();
    expect(learning).toHaveAttribute('aria-pressed', 'true');
    expect(within(learning).queryByRole('img')).not.toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Keep Learning illustration' })).toHaveAttribute('src', '/icons/north-star/learning.png');
    fireEvent.click(screen.getByRole('button', { name: 'My Own Path' }));
    expect(screen.queryByRole('img', { name: 'Keep Learning illustration' })).not.toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'My Own Path illustration' })).toHaveAttribute('src', '/icons/north-star/my-own-path.png');
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.getByLabelText('Explore ideas')).toHaveValue('independence');
    expect(screen.getByRole('button', { name: 'My First Real Paycheck' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByRole('button', { name: 'My Own Path' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('img', { name: 'My Own Path illustration' })).toBeInTheDocument();
  });
  it('keeps navigation outside the scrolling choices on every onboarding step', () => {
    const draft = reviewDraft();
    for (const step of ['welcome', 'year', 'north', 'vision', 'subjects', 'grades', 'schedule', 'summary'] as const) {
      const view = mount({ ...draft, step });
      const region = screen.getByTestId('onboarding-scroll-region');
      const footer = screen.getByRole('contentinfo');
      expect(region).not.toContainElement(footer);
      expect(within(footer).getAllByRole('button').length).toBeGreaterThan(0);
      view.unmount();
    }
  });

  it('does not jump to the top or steal focus when choosing the first subject', () => {
    mount({ ...reviewDraft(), step: 'subjects', subjects: [], configs: {}, gradeSubject: null });
    const region = screen.getByTestId('onboarding-scroll-region');
    const english = screen.getByRole('button', { name: 'English' });
    region.scrollTop = 220;
    english.focus();
    fireEvent.click(english);
    expect(region.scrollTop).toBe(220);
    expect(english).toHaveFocus();
    expect(english).toHaveAttribute('aria-pressed', 'true');
  });
  it('moves back and forward through grades one subject at a time', () => {
    mount({ ...reviewDraft(), step: 'grades', gradeSubject: 'Irish' });
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByRole('heading', { name: 'English', level: 1 })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Next subject' }));
    expect(screen.getByRole('heading', { name: 'Irish', level: 1 })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Next subject' }));
    expect(screen.getByRole('heading', { name: 'Japanese', level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue to schedule' })).toBeEnabled();
  });
  it('shows the count-up and target with only three subjects', () => {
    mount(reviewDraft());
    expect(screen.getByText('256 target points, from 200 current points')).toBeInTheDocument();
    expect(screen.getByText('Based on your 3 subjects.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start Learning' })).toBeEnabled();
  });
  it('keeps day buttons stable, focusable and positively selected, without decorative ticks', () => {
    mount({ ...reviewDraft(), step: 'schedule' });
    const monday = screen.getByRole('button', { name: 'Monday, study day' });
    monday.focus();
    fireEvent.click(monday);
    expect(screen.getByRole('button', { name: 'Monday, rest day' })).toBe(monday);
    expect(monday).toHaveFocus();
    expect(monday).toHaveAttribute('aria-pressed', 'false');
    expect(monday.textContent).toBe('MonRest');
    expect(screen.getByRole('button', { name: 'Continue' })).toBeDisabled();
  });
  it('resets date confirmation after changing the date', () => {
    mount({ ...reviewDraft(), step: 'schedule' });
    fireEvent.change(screen.getByLabelText('Your exam date'), { target: { value: '2030-06-06' } });
    expect(screen.getByRole('checkbox')).not.toBeChecked();
    expect(screen.getByRole('button', { name: 'Continue' })).toBeDisabled();
  });
  it('cancel restores the review and does not persist provisional edits', () => {
    const draft = reviewDraft(); mount(draft);
    fireEvent.click(screen.getByRole('button', { name: 'Edit English grades' }));
    fireEvent.change(screen.getByLabelText('Target grade'), { target: { value: 'O3' } });
    expect(JSON.parse(localStorage.getItem(key)!).configs.English.target).toBe('O1');
    fireEvent.click(screen.getByRole('button', { name: 'Cancel edits' }));
    expect(screen.getByText('O2 → O1')).toBeInTheDocument();
  });
  it('saving an individual grade returns directly to review', () => {
    mount(reviewDraft());
    fireEvent.click(screen.getByRole('button', { name: 'Edit English grades' }));
    fireEvent.change(screen.getByLabelText('Target grade'), { target: { value: 'O3' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save and review' }));
    expect(screen.getByText('O2 → O3')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start Learning' })).toBeEnabled();
  });
  it('requires new subjects to be reviewed rather than filling defaults', () => {
    mount(reviewDraft());
    fireEvent.click(screen.getByRole('button', { name: 'Edit subjects' }));
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'Biology' } });
    fireEvent.click(screen.getByRole('button', { name: 'Biology' }));
    fireEvent.click(screen.getByRole('button', { name: 'Save and review' }));
    expect(screen.getByText('Not reviewed')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start Learning' })).toBeDisabled();
  });
  it('keeps answers and allows retry after a rejected save', async () => {
    const complete = vi.fn().mockRejectedValueOnce(new Error('offline')).mockResolvedValue(undefined);
    mount(reviewDraft(), complete);
    fireEvent.click(screen.getByRole('button', { name: 'Start Learning' }));
    await screen.findByText('We couldn’t save your setup. Your answers are still here. Please try again.');
    fireEvent.click(screen.getByRole('button', { name: 'Start Learning' }));
    await waitFor(() => expect(complete).toHaveBeenCalledTimes(2));
    expect(complete.mock.calls[1][0].subjects).toHaveLength(3);
    expect(complete.mock.calls[1][2]).toBe(false);
  });
  it('requires confirmation before a programme change clears subject choices', () => {
    mount({ ...reviewDraft(), step: 'year' });
    fireEvent.click(screen.getByRole('button', { name: '2nd Year' }));
    expect(screen.getByRole('alertdialog')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Keep my choices' }));
    expect(JSON.parse(localStorage.getItem(key)!).subjects).toHaveLength(3);
    fireEvent.click(screen.getByRole('button', { name: '2nd Year' }));
    fireEvent.click(screen.getByRole('button', { name: 'Change programme and clear choices' }));
    expect(JSON.parse(localStorage.getItem(key)!).subjects).toEqual([]);
  });
});
