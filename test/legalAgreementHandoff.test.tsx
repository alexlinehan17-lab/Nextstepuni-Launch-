import React, { StrictMode } from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { PRIVACY_POLICY_VERSION, TERMS_VERSION } from '../functions/src/legalAgreementPolicy';

const mocks = vi.hoisted(() => ({ watch: vi.fn(), accept: vi.fn() }));
vi.mock('firebase/firestore', () => ({
  doc: (_db: unknown, collection: string, uid: string) => `${collection}/${uid}`,
  onSnapshot: mocks.watch,
}));
vi.mock('firebase/functions', () => ({
  getFunctions: vi.fn(),
  httpsCallable: () => mocks.accept,
}));
import { LegalAgreementGate } from '../components/legal/LegalAgreementGate';
import { clearRegistrationAgreement, hasRegistrationAgreement, rememberRegistrationAgreement } from '../services/legalAgreement';

const user = { uid: 'handoff-student', name: 'Student', avatar: 'crew-snoozer', school: 'marino', role: 'student' as const };
const confirmed = { success: true, privacyVersion: PRIVACY_POLICY_VERSION, termsVersion: TERMS_VERSION };
const current = { ...confirmed, acceptedAt: 'server-time', method: 'explicit-checkbox', studentAgeConfirmed: true };
const view = () => <StrictMode><LegalAgreementGate user={user} ready onLogout={vi.fn()}><p>Onboarding ready</p></LegalAgreementGate></StrictMode>;
const snapshot = (fromCache: boolean, legalAcceptance?: unknown, exists = true) => ({
  metadata: { fromCache }, exists: () => exists, data: () => ({ legalAcceptance }),
});
const emit = async (value: ReturnType<typeof snapshot>) => {
  await act(async () => { mocks.watch.mock.calls.at(-1)![2](value); });
};
const expectNoReview = () => {
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(screen.queryByText(/Review how your information/)).not.toBeInTheDocument();
};

beforeEach(() => {
  vi.clearAllMocks();
  clearRegistrationAgreement(user.uid);
  mocks.watch.mockReturnValue(vi.fn());
  mocks.accept.mockResolvedValue({ data: confirmed });
});
afterEach(() => { clearRegistrationAgreement(user.uid); });

describe('signup agreement handoff with Firestore snapshots', () => {
  test('cached missing profiles stay on setup until the server read and signup save finish', async () => {
    let finishSave!: (value: { data: typeof confirmed }) => void;
    mocks.accept.mockImplementationOnce(() => new Promise(resolve => { finishSave = resolve; }));
    rememberRegistrationAgreement(user.uid);
    render(view());
    expect(screen.getByRole('status')).toHaveTextContent('Setting up your account');
    expectNoReview();

    await emit(snapshot(true, undefined, false));
    expectNoReview();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    expect(mocks.accept).not.toHaveBeenCalled();

    await emit(snapshot(false));
    expect(mocks.accept).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({ agreeTerms: true, studentAgeConfirmed: true }));
    expectNoReview();
    expect(hasRegistrationAgreement(user.uid)).toBe(true);
    expect(screen.queryByText('Onboarding ready')).not.toBeInTheDocument();

    await act(async () => { finishSave({ data: confirmed }); });
    expect(await screen.findByText('Onboarding ready')).toBeInTheDocument();
    expect(hasRegistrationAgreement(user.uid)).toBe(false);
  });

  test('a stale cached agreement does not flash a review before a current server record', async () => {
    render(view());
    await emit(snapshot(true, { ...current, termsVersion: 'old-version' }));
    expectNoReview();
    expect(screen.getByRole('status')).toHaveTextContent('Opening your space');
    await emit(snapshot(false, current));
    expect(await screen.findByText('Onboarding ready')).toBeInTheDocument();
    expectNoReview();
    expect(mocks.accept).not.toHaveBeenCalled();
  });

  test('an unchanged profile delivered from the server still opens required review', async () => {
    render(view());
    await emit(snapshot(true));
    expectNoReview();
    // Without metadata events, a cache -> server transition with unchanged
    // document fields never arrives and would leave the loader stuck.
    expect(mocks.watch).toHaveBeenLastCalledWith(`users/${user.uid}`, { includeMetadataChanges: true }, expect.any(Function), expect.any(Function));
    await emit(snapshot(false));
    expect(await screen.findByRole('checkbox', { name: /I have read/ })).not.toBeChecked();
    expect(screen.queryByText('Onboarding ready')).not.toBeInTheDocument();
    expect(mocks.accept).not.toHaveBeenCalled();
  });

  test('remounting during the save retains the original signup action', async () => {
    let finishSave!: (value: { data: typeof confirmed }) => void;
    const saving = new Promise(resolve => { finishSave = resolve; });
    mocks.accept.mockReturnValue(saving);
    rememberRegistrationAgreement(user.uid);
    const first = render(view());
    await emit(snapshot(false));
    first.unmount();
    expect(hasRegistrationAgreement(user.uid)).toBe(true);
    render(view());
    await emit(snapshot(false));
    expectNoReview();
    await act(async () => { finishSave({ data: confirmed }); });
    await waitFor(() => expect(screen.getByText('Onboarding ready')).toBeInTheDocument());
    expect(hasRegistrationAgreement(user.uid)).toBe(false);
  });
});
