import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Onboarding from '../components/Onboarding';
import ChangeSubjectsModal from '../components/ChangeSubjectsModal';
import SubjectOnboarding from '../components/SubjectOnboarding';
import { buildProfile, draftKey, emptyChoice, initialDraft, levelOptions, pointsFor, readDraft, type SetupDraft } from '../components/onboarding/model';
import { LCA_SUBJECTS, subjectMatchesQuery, type StudentSubjectProfile } from '../components/subjectData';

const device = vi.hoisted(() => ({ mobile: true }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
const uid = 'lca-subject-feedback';
const maths = 'Leaving Cert Maths';
const key = draftKey(uid, 'fresh');
function draft(): SetupDraft {
  const subjects = ['Science', maths, 'French'];
  return { ...initialDraft(), step: 'subjects', year: 'LCA1', category: 'college-learning', vision: ['campus'], date: '2030-06-05', dateConfirmed: true, rest: ['Sunday'], subjects,
    configs: Object.fromEntries(subjects.map(name => [name, emptyChoice('LCA1', name)])), gradeSubject: maths };
}
function mount(value = draft(), complete = vi.fn()) {
  localStorage.setItem(key, JSON.stringify(value));
  return render(<Onboarding userId={uid} userName="Alex" onComplete={complete} onSkip={vi.fn()} />);
}
async function choose(label: string, option: string) {
  await userEvent.click(screen.getByRole('combobox', { name: label }));
  await userEvent.click(await screen.findByRole('option', { name: option }));
}
beforeEach(() => { localStorage.clear(); sessionStorage.clear(); device.mobile = true; });

describe('LCA profile round trips', () => {
  it.each(['LCA1', 'LCA2'] as const)('retains all LC Maths levels and grades in %s', year => {
    for (const [level, current, target] of [['higher','H4','H2'], ['ordinary','O4','O2'], ['foundation','F4','F2']] as const) {
      const value = { ...draft(), year, step: 'grades' as const };
      value.configs[maths] = { level, current, target, reviewed: true };
      localStorage.setItem(key, JSON.stringify(value));
      const restored = readDraft(uid, 'fresh');
      expect(restored.step).toBe('grades');
      expect(restored.configs[maths]).toEqual(value.configs[maths]);
      expect(buildProfile(restored).subjects).toEqual([
        { subjectName: 'Science', level: 'common' },
        { subjectName: maths, level, currentGrade: current, targetGrade: target },
        { subjectName: 'French', level: 'common' },
      ]);
      expect(pointsFor(restored)).toEqual({ count: 0, current: 0, target: 0 });
    }
  });
  it('requires a real Maths level when an old draft saved Common', () => {
    const value = draft();
    value.configs[maths] = { level: 'common', current: 'later', target: 'later', reviewed: true };
    localStorage.setItem(key, JSON.stringify(value));
    const restored = readDraft(uid, 'fresh');
    expect(restored.configs[maths].level).toBeNull();
    expect(restored.configs[maths].reviewed).toBe(false);
    expect(() => buildProfile(restored)).toThrow(/Review the level and grades/);
    expect(levelOptions('LCA1', maths)).toEqual(['higher', 'ordinary', 'foundation']);
    expect(levelOptions('LCA1', 'French')).toEqual(['common']);
  });
  it('preserves an Ordinary current and Higher target, including deferred grades', () => {
    const value = draft();
    value.configs[maths] = { level: 'ordinary', current: 'O2', target: 'H4', reviewed: true };
    expect(buildProfile(value).subjects[1]).toMatchObject({ level: 'ordinary', currentGrade: 'O2', targetGrade: 'H4' });
    value.configs[maths] = { level: 'foundation', current: 'later', target: 'later', reviewed: true };
    expect(buildProfile(value).subjects[1]).toEqual({ subjectName: maths, level: 'foundation' });
  });
  it.each([
    ['wood technology', 'Graphics And Construction Studies'],
    ['woodwork', 'Graphics And Construction Studies'],
    ['woodcraft', 'Graphics And Construction Studies'],
    ['vocational studies', 'Vocational Preparation & Guidance'],
    ['ordinary maths', maths],
  ])('finds the existing official course for %s', (query, name) => {
    expect(LCA_SUBJECTS.filter(subject => subjectMatchesQuery(subject, query)).map(subject => subject.name)).toEqual([name]);
  });
});

describe.each([true, false])('LCA onboarding, mobile=%s', mobile => {
  it('routes only Maths through the existing grade controls and saves through reload', async () => {
    device.mobile = mobile;
    const view = mount();
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.queryByRole('group', { name: 'Live points preview' })).not.toBeInTheDocument();
    expect(screen.queryByText('Current points')).not.toBeInTheDocument();
    if (mobile) fireEvent.click(screen.getByRole('button', { name: 'Ordinary' }));
    else await choose(`${maths} level`, 'Ordinary');
    await choose(mobile ? 'Current grade' : `${maths} current grade`, 'O4');
    await choose(mobile ? 'Target grade' : `${maths} target grade`, 'O2');
    fireEvent.click(screen.getByRole('button', { name: 'Continue to schedule' }));
    await waitFor(() => expect(screen.getByRole('heading', { name: 'Make room for progress.' })).toBeInTheDocument());
    const saved = JSON.parse(localStorage.getItem(key)!);
    view.unmount();
    const complete = vi.fn();
    mount({ ...saved, step: 'summary' }, complete);
    expect(screen.getByRole('button', { name: `Edit ${maths} grades` })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Edit French grades' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Start Learning' }));
    await waitFor(() => expect(complete).toHaveBeenCalled());
    expect(complete.mock.calls[0][0].subjects[1]).toEqual({ subjectName: maths, level: 'ordinary', currentGrade: 'O4', targetGrade: 'O2' });
  });
  it('continues directly to the schedule when only LCA courses are chosen', () => {
    device.mobile = mobile;
    mount({ ...draft(), subjects: ['Science', 'French'] });
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.getByRole('heading', { name: 'Make room for progress.' })).toBeInTheDocument();
  });
});

function profile(): StudentSubjectProfile {
  const value = draft();
  value.configs[maths] = { level: 'ordinary', current: 'O4', target: 'O2', reviewed: true };
  return buildProfile(value);
}
describe('LCA subject changes', () => {
  it('preserves Maths grades and keeps LCA courses common through save and reopen', () => {
    const save = vi.fn();
    const view = render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={profile()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(within(screen.getByRole('group', { name: `${maths} level` })).getByRole('button', { name: 'Ordinary' })).toHaveAttribute('aria-pressed','true');
    expect(screen.queryByRole('group', { name: 'French current grade' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save Changes' }));
    const saved = JSON.parse(JSON.stringify(save.mock.calls[0][0]));
    expect(saved.subjects).toEqual(profile().subjects);
    view.unmount();
    render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={saved} />);
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(within(screen.getByRole('group', { name: `${maths} current grade` })).getByRole('button', { name: 'O4' })).toHaveAttribute('aria-pressed','true');
  });
  it('repairs an old Common Maths level without inventing grades', () => {
    const save = vi.fn();
    const value = profile();
    value.subjects[1] = { subjectName: maths, level: 'common' };
    render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={value} />);
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.getByRole('button', { name: 'Save Changes' })).toBeDisabled();
    fireEvent.click(within(screen.getByRole('group', { name: `${maths} level` })).getByRole('button', { name: 'Foundation' }));
    fireEvent.click(screen.getByRole('button', { name: 'Save Changes' }));
    expect(save.mock.calls[0][0].subjects[1]).toEqual({ subjectName: maths, level: 'foundation' });
  });
});


describe('Launchpad subject setup', () => {
  it('uses the LCA catalogue and preserves Maths through its existing edit flow', () => {
    const save = vi.fn();
    render(<SubjectOnboarding user={{ uid, yearGroup: 'LCA1' }} existingProfile={profile()} onComplete={save} onClose={vi.fn()} />);
    expect(screen.getByRole('button', { name: 'Mathematical Applications' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Mathematics' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(within(screen.getByRole('group', { name: `${maths} level` })).getByRole('button', { name: 'Ordinary' })).toHaveAttribute('aria-pressed', 'true');
    for (let step = 3; step < 6; step++) fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.queryByText('Projected CAO points gain')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Update & Save' }));
    expect(save.mock.calls[0][0].subjects).toEqual(profile().subjects);
    expect(save.mock.calls[0][0].yearGroup).toBe('LCA1');
  });
});

it('offers the LCA catalogue for first-time Launchpad setup from the signed-in year', () => {
  const save = vi.fn();
  render(<SubjectOnboarding user={{ uid, yearGroup: 'LCA2' }} onComplete={save} onClose={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: 'Get Started' }));
  fireEvent.click(screen.getByRole('button', { name: 'Science' }));
  fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
  expect(screen.queryByRole('group', { name: 'Science current grade' })).not.toBeInTheDocument();
  expect(screen.getByText('Common level · LCA credits')).toBeInTheDocument();
  for (let step = 3; step < 6; step++) fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
  fireEvent.click(screen.getByRole('button', { name: 'Save & Continue' }));
  expect(save.mock.calls[0][0].subjects).toStrictEqual([{ subjectName: 'Science', level: 'common' }]);
  expect(save.mock.calls[0][0].yearGroup).toBe('LCA2');
});
