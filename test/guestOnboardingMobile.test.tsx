/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The mobile onboarding (components/onboarding/SetupFlow.tsx) in guest mode:
 * the same "Dive in" ending, the draft in the guest namespace, and no
 * Firestore write from the funnel.
 */
import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

const firestoreSpies = vi.hoisted(() => ({
  addDoc: vi.fn(() => Promise.resolve({ id: 'evt' })),
  setDoc: vi.fn(() => Promise.resolve()),
  updateDoc: vi.fn(() => Promise.resolve()),
}));
const collectionStub = vi.hoisted(() => (_db: unknown, path: string) => ({ path }));
vi.mock('firebase/firestore', async importOriginal => ({ ...(await importOriginal<object>()), ...firestoreSpies, collection: collectionStub }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));

import Onboarding from '@/components/Onboarding';
import { draftKey, initialDraft, type SetupDraft } from '@/components/onboarding/model';
import type { StudentSubjectProfile } from '@/components/subjectData';
import { GUEST_USER_ID, GUEST_USER_NAME, endGuestSetup, guestStorage, setGuestPhase } from '@/components/onboarding/guest';

const key = draftKey(GUEST_USER_ID, 'fresh');
const reviewDraft = (): SetupDraft => ({
  ...initialDraft(), step: 'summary', year: '6th', category: 'college-learning', vision: ['campus'], subjects: ['English', 'Irish'],
  configs: { English: { level: 'ordinary', current: 'O2', target: 'O1', reviewed: true }, Irish: { level: 'higher', current: 'H3', target: 'H1', reviewed: true } },
  date: '2030-06-05', dateConfirmed: true, rest: ['Sunday'], gradeSubject: 'English',
});

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  endGuestSetup({ keepDraft: false });
  Object.values(firestoreSpies).forEach(spy => spy.mockClear());
  // What AppRouter's guest branch does before mounting the flow.
  setGuestPhase('onboarding');
});

describe('mobile onboarding in guest mode', () => {
  it('ends with "Dive in", hands the built profile to onComplete, and writes nothing', async () => {
    guestStorage.setItem(key, JSON.stringify(reviewDraft()));
    const complete = vi.fn((_profile: StudentSubjectProfile) => Promise.resolve());
    render(<Onboarding guest userId={GUEST_USER_ID} userName={GUEST_USER_NAME} onComplete={complete} onSkip={vi.fn()} />);

    expect(screen.getByRole('heading', { level: 1, name: 'You’re ready.' })).toBeInTheDocument();
    const dive = screen.getByRole('button', { name: 'Dive in' });
    expect(screen.queryByRole('button', { name: 'Start Learning' })).not.toBeInTheDocument();

    fireEvent.click(dive);
    await waitFor(() => expect(complete).toHaveBeenCalledTimes(1));
    expect(complete.mock.calls[0][0]).toMatchObject({ yearGroup: '6th', curriculumLevel: 'senior' });
    expect(complete.mock.calls[0][0].subjects).toHaveLength(2);
    Object.values(firestoreSpies).forEach(spy => expect(spy).not.toHaveBeenCalled());
    // The answers are still there for a later adoption.
    expect(guestStorage.getItem(key)).not.toBeNull();
  });

  it('keeps the guest draft in the tab-scoped guest namespace, never in localStorage', () => {
    render(<Onboarding guest userId={GUEST_USER_ID} userName={GUEST_USER_NAME} onComplete={vi.fn()} onSkip={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Get Started' }));
    expect(JSON.parse(guestStorage.getItem(key) ?? '{}')).toMatchObject({ version: 2, step: 'year' });
    expect(sessionStorage.getItem(`nsu:guest-setup:${key}`)).not.toBeNull();
    expect(localStorage.getItem(key)).toBeNull();
    expect(localStorage.length).toBe(0);
  });

  it('a signed-in student\'s flow is untouched: "Start Learning", greeting by name, localStorage draft', () => {
    endGuestSetup({ keepDraft: false });
    localStorage.setItem(draftKey('student-2', 'fresh'), JSON.stringify(reviewDraft()));
    render(<Onboarding userId="student-2" userName="Alex Murphy" onComplete={vi.fn()} onSkip={vi.fn()} />);
    expect(screen.getByRole('heading', { level: 1, name: 'You’re ready, Alex.' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start Learning' })).toBeEnabled();
    expect(screen.queryByRole('button', { name: 'Dive in' })).not.toBeInTheDocument();
    expect(sessionStorage.getItem(`nsu:guest-setup:${draftKey('student-2', 'fresh')}`)).toBeNull();
  });
});
