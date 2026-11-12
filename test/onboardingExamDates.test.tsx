import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import SetupFlow from '../components/onboarding/SetupFlow';
import DesktopSetup from '../components/onboarding/DesktopSetup';
import { draftKey, initialDraft, readDraft } from '../components/onboarding/model';
import { getDefaultExamDateForYear } from '../utils/examDates';

vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
const today = new Date('2026-11-12T12:00:00');
const uid = 'exam-date-review';
const key = draftKey(uid, 'fresh');

beforeEach(() => {
  vi.useFakeTimers({ toFake: ['Date'] });
  vi.setSystemTime(today);
  localStorage.clear();
});
afterEach(() => vi.useRealTimers());

describe('cohort exam defaults', () => {
  it('offers the requested dates for sixth and fifth years, including the senior transition', () => {
    expect(getDefaultExamDateForYear('6th', today)).toBe('2027-06-09');
    expect(getDefaultExamDateForYear('5th', today)).toBe('2028-06-03');
    expect(initialDraft('5th').date).toBe('2028-06-03');
    expect(getDefaultExamDateForYear('3rd', today)).toBe('2027-06-02');
  });

  it('does not roll the sixth-year date before the configured sitting starts', () => {
    expect(getDefaultExamDateForYear('6th', new Date('2027-06-03T12:00:00'))).toBe('2027-06-09');
    expect(getDefaultExamDateForYear('6th', new Date('2027-06-10T12:00:00'))).toBe('2028-06-03');
  });

  it('upgrades an untouched old default while retaining an explicitly chosen date', () => {
    const draft = { ...initialDraft(), year: '5th', date: '2027-06-02' };
    localStorage.setItem(key, JSON.stringify(draft));
    expect(readDraft(uid, 'fresh').date).toBe('2028-06-03');
    localStorage.setItem(key, JSON.stringify({ ...draft, dateEdited: true }));
    expect(readDraft(uid, 'fresh').date).toBe('2027-06-02');
    localStorage.setItem(key, JSON.stringify({ ...draft, dateConfirmed: true }));
    expect(readDraft(uid, 'fresh').date).toBe('2027-06-02');
  });
});

describe.each([['mobile', SetupFlow], ['desktop', DesktopSetup]] as const)('%s onboarding dates', (_, Flow) => {
  it('updates the default when choosing a school year', () => {
    localStorage.setItem(key, JSON.stringify({ ...initialDraft(), step: 'year' }));
    render(<Flow userId={uid} userName="Alex" onComplete={vi.fn()} onSkip={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /6th Year/i }));
    expect(JSON.parse(localStorage.getItem(key)!).date).toBe('2027-06-09');
    fireEvent.click(screen.getByRole('button', { name: /5th Year/i }));
    expect(JSON.parse(localStorage.getItem(key)!).date).toBe('2028-06-03');
  });

  it('continues without confirmation and persists an editable date', () => {
    localStorage.setItem(key, JSON.stringify({ ...initialDraft('5th'), step: 'schedule', rest: ['Sunday'] }));
    render(<Flow userId={uid} userName="Alex" onComplete={vi.fn()} onSkip={vi.fn()} />);
    expect(screen.getByLabelText('Your exam date')).toHaveValue('2028-06-03');
    expect(screen.queryByRole('checkbox')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue' })).toBeEnabled();
    fireEvent.change(screen.getByLabelText('Your exam date'), { target: { value: '2028-06-07' } });
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(JSON.parse(localStorage.getItem(key)!)).toMatchObject({ date: '2028-06-07', dateEdited: true, step: 'summary' });
  });
});
