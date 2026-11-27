/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 8a, second pass: a failed delete or password reset on the counsellor's dashboard says so in the
 * app's own message (the shared MessageHost), with today's words, and no browser alert comes up.
 * Here the sign-in check fails first (no signed-in user), which is the same failure path as a refused
 * call: nothing is sent.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { GCDashboard } from '../components/GCDashboard';

vi.mock('firebase/firestore', () => ({
  collection: vi.fn(() => ({})), query: vi.fn(() => ({})), where: vi.fn(), limit: vi.fn(), doc: vi.fn(() => ({})),
  getDocs: vi.fn(async () => ({ docs: [{ id: 'sam', data: () => ({ name: 'Sam Student', school: 's1', role: 'student', avatar: 'star-crew:maker' }) }] })),
  getDoc: vi.fn(async () => ({ exists: () => false, data: () => ({}) })),
  setDoc: vi.fn(async () => undefined),
}));
const callable = vi.fn(async () => ({ data: {} }));
vi.mock('firebase/functions', () => ({ getFunctions: vi.fn(() => ({})), httpsCallable: vi.fn(() => callable) }));
vi.mock('../hooks/useGCFlags', () => ({
  useGCFlags: () => ({
    flags: {}, flagStudent: vi.fn(), unflagStudent: vi.fn(), updateFlagPriority: vi.fn(),
    isFlagged: () => false, getFlagData: () => null, flaggedStudentUids: [],
  }),
}));

let alertSpy: ReturnType<typeof vi.spyOn>;
beforeEach(() => { alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {}); callable.mockClear(); });
afterEach(() => { cleanup(); alertSpy.mockRestore(); });

async function openStudentMenu() {
  render(<GCDashboard school="s1" onLogout={vi.fn()} allCourses={[]} gcName="Demo Counsellor" gcUid="gc1" role="gc" />);
  await screen.findByRole('heading', { name: 'Attention' });
  fireEvent.click(screen.getByRole('button', { name: 'Students' }));
  fireEvent.click(await screen.findByRole('button', { name: /^View Sam Student/ }));
  fireEvent.click(await screen.findByRole('button', { name: /^More for Sam Student/ }));
}

describe('a failed delete or reset on the counsellor\'s dashboard (area 8a)', () => {
  test('a failed delete shows today\'s words in the app\'s message, and no browser alert', async () => {
    await openStudentMenu();
    fireEvent.click(await screen.findByRole('menuitem', { name: 'Delete account' }));
    const sheet = await screen.findByRole('dialog', { name: 'Delete student' });
    fireEvent.change(within(sheet).getByLabelText('Re-enter your password to continue'), { target: { value: 'secret' } });
    await act(async () => { fireEvent.click(within(sheet).getByRole('button', { name: 'Delete' })); });
    // The toast, and the polite live region that reads it out.
    expect(await screen.findByRole('status')).toHaveTextContent('Failed to delete student. You may not have permission.');
    expect(document.querySelector('.ui-toast')).toHaveTextContent('Failed to delete student. You may not have permission.');
    expect(alertSpy).not.toHaveBeenCalled();
    expect(callable).not.toHaveBeenCalled();
  });

  test('a failed reset shows today\'s words in the app\'s message, and no browser alert', async () => {
    await openStudentMenu();
    fireEvent.click(await screen.findByRole('menuitem', { name: 'Reset password' }));
    const sheet = await screen.findByRole('dialog', { name: 'Reset student password?' });
    fireEvent.change(within(sheet).getByLabelText('Re-enter your password'), { target: { value: 'secret' } });
    await act(async () => { fireEvent.click(within(sheet).getByRole('button', { name: 'Reset password' })); });
    // The toast, and the polite live region that reads it out.
    expect(await screen.findByRole('status')).toHaveTextContent('Failed to reset password. Please try again.');
    expect(document.querySelector('.ui-toast')).toHaveTextContent('Failed to reset password. Please try again.');
    expect(alertSpy).not.toHaveBeenCalled();
    expect(callable).not.toHaveBeenCalled();
  });
});
