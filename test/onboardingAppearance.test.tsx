import React, { useState } from 'react';
import { act, fireEvent, render, renderHook, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import DesktopSetup from '../components/onboarding/DesktopSetup';
import SetupFlow from '../components/onboarding/SetupFlow';
import { draftKey, initialDraft, readDraft, type SetupDraft } from '../components/onboarding/model';
import { SettingsContext } from '../contexts/SettingsContext';
import { useSettings } from '../hooks/useSettings';
import { guestStorage } from '../components/onboarding/guest';

const mocks = vi.hoisted(() => ({ getDoc: vi.fn(), setDoc: vi.fn() }));
vi.mock('firebase/firestore', () => ({
  doc: (_db: unknown, collection: string, uid: string) => `${collection}/${uid}`,
  getDoc: mocks.getDoc,
  setDoc: mocks.setDoc,
}));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));

const uid = 'appearance-student';
function reviewDraft(): SetupDraft {
  return {
    ...initialDraft(), step: 'summary', year: '5th', category: 'college-learning', vision: ['campus'],
    subjects: ['English'], configs: { English: { level: 'higher', current: 'H3', target: 'H1', reviewed: true } },
    date: '2030-06-05', dateConfirmed: true, rest: ['Saturday', 'Sunday'], gradeSubject: 'English',
  };
}

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  document.documentElement.classList.remove('dark');
  mocks.getDoc.mockReset().mockResolvedValue({ exists: () => false });
  mocks.setDoc.mockReset().mockResolvedValue(undefined);
});
afterEach(() => document.documentElement.classList.remove('dark'));

describe.each([['desktop', DesktopSetup], ['mobile', SetupFlow]] as const)('%s onboarding appearance', (_name, Setup) => {
  function Harness({ guest = false }: { guest?: boolean }) {
    const { settings, updateSetting } = useSettings(guest ? undefined : uid);
    const [complete, setComplete] = useState(false);
    return <SettingsContext.Provider value={{ settings, updateSetting, unlockedThemes: [], unlockedCardStyles: [] }}>
      {complete ? <button onClick={() => updateSetting('darkMode', !settings.darkMode)}>Switch appearance</button>
        : <Setup userId={guest ? 'guest' : uid} userName="Aoife" guest={guest} onComplete={() => setComplete(true)} onSkip={vi.fn()} />}
    </SettingsContext.Provider>;
  }

  it('selects and saves Dark by default, then allows the existing app setting to switch to Light', async () => {
    localStorage.setItem(draftKey(uid, 'fresh'), JSON.stringify(reviewDraft()));
    render(<Harness />);
    expect(screen.getByRole('radio', { name: 'Dark' })).toBeChecked();
    expect(screen.getByRole('radio', { name: 'Light' })).not.toBeChecked();
    fireEvent.click(screen.getByRole('button', { name: 'Start Learning' }));
    await screen.findByRole('button', { name: 'Switch appearance' });
    expect(document.documentElement).toHaveClass('dark');
    expect(JSON.parse(localStorage.getItem(`nextstep-settings:${uid}`)!).darkMode).toBe(true);
    expect(mocks.setDoc).toHaveBeenCalledWith(`settings/${uid}`, expect.objectContaining({ darkMode: true }), { merge: true });
    fireEvent.click(screen.getByRole('button', { name: 'Switch appearance' }));
    expect(document.documentElement).not.toHaveClass('dark');
    expect(JSON.parse(localStorage.getItem(`nextstep-settings:${uid}`)!).darkMode).toBe(false);
  });

  it('previews Light immediately and retains the choice through edits, reload and completion', async () => {
    localStorage.setItem(draftKey(uid, 'fresh'), JSON.stringify(reviewDraft()));
    const view = render(<Harness />);
    fireEvent.click(screen.getByRole('radio', { name: 'Light' }));
    expect(view.container.querySelector('.setup-flow')).toHaveAttribute('data-surface', 'paper');
    fireEvent.click(screen.getByRole('button', { name: 'Edit schedule' }));
    expect(screen.queryByRole('radio', { name: 'Light' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save and review' }));
    expect(screen.getByRole('radio', { name: 'Light' })).toBeChecked();
    view.unmount();
    render(<Harness />);
    expect(screen.getByRole('radio', { name: 'Light' })).toBeChecked();
    fireEvent.click(screen.getByRole('button', { name: 'Start Learning' }));
    await screen.findByRole('button', { name: 'Switch appearance' });
    expect(document.documentElement).not.toHaveClass('dark');
    expect(JSON.parse(localStorage.getItem(`nextstep-settings:${uid}`)!).darkMode).toBe(false);
    expect(mocks.setDoc).toHaveBeenCalledWith(`settings/${uid}`, expect.objectContaining({ darkMode: false }), { merge: true });
  });

  it('leaves the welcome screen and existing preference alone', async () => {
    localStorage.setItem(`nextstep-settings:${uid}`, JSON.stringify({ darkMode: false }));
    render(<Harness />);
    expect(screen.getByRole('button', { name: 'Get Started' })).toBeInTheDocument();
    expect(screen.queryByRole('group', { name: 'Choose your view.' })).not.toBeInTheDocument();
    await waitFor(() => expect(mocks.getDoc).toHaveBeenCalled());
    expect(mocks.setDoc).not.toHaveBeenCalled();
    expect(document.documentElement).not.toHaveClass('dark');
  });

  it('offers the same default in guest setup without an account write', async () => {
    guestStorage.setItem(draftKey('guest', 'fresh'), JSON.stringify(reviewDraft()));
    render(<Harness guest />);
    expect(screen.getByRole('radio', { name: 'Dark' })).toBeChecked();
    fireEvent.click(screen.getByRole('button', { name: 'Dive in' }));
    await screen.findByRole('button', { name: 'Switch appearance' });
    expect(document.documentElement).toHaveClass('dark');
    expect(JSON.parse(localStorage.getItem('nextstep-settings')!).darkMode).toBe(true);
    expect(mocks.setDoc).not.toHaveBeenCalled();
  });
});

describe('appearance persistence', () => {
  it('migrates older or malformed appearance drafts to Dark without losing the plan', () => {
    const { appearance: _appearance, ...oldDraft } = reviewDraft();
    for (const appearance of [undefined, 'system', null]) {
      localStorage.setItem(draftKey(uid, 'fresh'), JSON.stringify({ ...oldDraft, appearance }));
      expect(readDraft(uid, 'fresh')).toMatchObject({ appearance: 'dark', subjects: ['English'], step: 'summary' });
    }
    expect(readDraft('another-student', 'fresh').appearance).toBe('dark');
  });

  it.each([true, false])('retains a selected darkMode=%s when older account settings arrive after completion', async (darkMode) => {
    let finish!: (value: unknown) => void;
    mocks.getDoc.mockReturnValue(new Promise(resolve => { finish = resolve; }));
    const view = renderHook(() => useSettings(uid));
    act(() => view.result.current.updateSetting('darkMode', darkMode));
    await act(async () => finish({ exists: () => true, data: () => ({ darkMode: !darkMode, defaultWorkMinutes: 45 }) }));
    expect(view.result.current.settings).toMatchObject({ darkMode, defaultWorkMinutes: 45 });
    expect(document.documentElement.classList.contains('dark')).toBe(darkMode);
    expect(JSON.parse(localStorage.getItem(`nextstep-settings:${uid}`)!).darkMode).toBe(darkMode);
    view.unmount();
    mocks.getDoc.mockResolvedValue({ exists: () => false });
    const reloaded = renderHook(() => useSettings(uid));
    expect(reloaded.result.current.settings.darkMode).toBe(darkMode);
  });
});
