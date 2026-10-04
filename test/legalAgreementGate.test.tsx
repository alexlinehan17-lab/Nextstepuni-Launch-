import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import { PRIVACY_POLICY_VERSION, TERMS_VERSION } from '../functions/src/legalAgreementPolicy';
const mocks = vi.hoisted(() => ({ watch: vi.fn(), record: vi.fn(), take: vi.fn(), value: undefined as unknown }));
vi.mock('../services/legalAgreement', () => ({ watchLegalAcceptance: mocks.watch, recordLegalAcceptance: mocks.record, takeRegistrationAgreement: mocks.take }));
import { LegalAgreementGate } from '../components/legal/LegalAgreementGate';
const user = { uid: 'student-a', name: 'Student', avatar: 'crew-snoozer', school: 'marino', role: 'student' as const };
const current = () => ({ privacyVersion: PRIVACY_POLICY_VERSION, termsVersion: TERMS_VERSION, acceptedAt: 'server-time', method: 'explicit-checkbox', studentAgeConfirmed: true });
const view = (account = user) => <LegalAgreementGate user={account} ready onLogout={vi.fn()}><p>Private workspace</p></LegalAgreementGate>;
beforeEach(() => {
  vi.clearAllMocks(); mocks.value = undefined;
  mocks.watch.mockImplementation((_uid, onValue) => { queueMicrotask(() => onValue(mocks.value)); return vi.fn(); });
  mocks.record.mockResolvedValue(undefined); mocks.take.mockReturnValue(false);
});
describe('agreement before private account use', () => {
  test('legacy or social accounts cannot enter through an old consent timestamp', async () => {
    mocks.value = { policyVersion: PRIVACY_POLICY_VERSION, acceptedAt: 'implicit-social-time', basis: 'school-enrolment' };
    render(view());
    const continueButton = await screen.findByRole('button', { name: /Agree & continue/ });
    expect(continueButton).toBeDisabled();
    expect(screen.queryByText('Private workspace')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('checkbox', { name: /I have read/ }));
    expect(continueButton).toBeDisabled();
    expect(mocks.record).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('checkbox', { name: /I am aged 16/ }));
    fireEvent.click(continueButton);
    expect(await screen.findByText('Private workspace')).toBeInTheDocument();
    expect(mocks.record).toHaveBeenCalledExactlyOnceWith(true);
  });
  test('a current server record opens the workspace without a new action', async () => {
    mocks.value = current(); render(view());
    expect(await screen.findByText('Private workspace')).toBeInTheDocument();
    expect(mocks.record).not.toHaveBeenCalled();
  });
  test('a failed save keeps the account reviewable and can be retried', async () => {
    mocks.record.mockRejectedValueOnce(new Error('offline'));
    render(view());
    fireEvent.click(await screen.findByRole('checkbox', { name: /I have read/ }));
    fireEvent.click(screen.getByRole('checkbox', { name: /I am aged 16/ }));
    fireEvent.click(screen.getByRole('button', { name: /Agree & continue/ }));
    expect(await screen.findByRole('alert')).toHaveTextContent('has not been saved');
    expect(screen.queryByText('Private workspace')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Agree & continue/ }));
    expect(await screen.findByText('Private workspace')).toBeInTheDocument();
  });
  test('read errors do not invent acceptance or reveal the workspace', async () => {
    mocks.watch.mockImplementation((_uid, _onValue, onError) => { queueMicrotask(onError); return vi.fn(); });
    render(view());
    expect(await screen.findByRole('alert')).toHaveTextContent('has not been assumed');
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    await waitFor(() => expect(mocks.watch).toHaveBeenCalledTimes(2));
    expect(mocks.record).not.toHaveBeenCalled();
    expect(screen.queryByText('Private workspace')).not.toBeInTheDocument();
  });
  test('email signup transfers a real checkbox action through the same server endpoint', async () => {
    mocks.take.mockReturnValueOnce(true);
    render(view());
    expect(await screen.findByText('Private workspace')).toBeInTheDocument();
    expect(mocks.record).toHaveBeenCalledExactlyOnceWith(true);
  });
  test('changing accounts cannot reuse the previous account’s approval', async () => {
    mocks.value = current(); const rendered = render(view());
    await screen.findByText('Private workspace');
    mocks.value = undefined; rendered.rerender(view({ ...user, uid: 'student-b' }));
    expect(await screen.findByRole('checkbox', { name: /I have read/ })).not.toBeChecked();
    expect(screen.queryByText('Private workspace')).not.toBeInTheDocument();
  });
  test('verified company operators are not asked to accept school-user terms', () => {
    render(<LegalAgreementGate user={{ ...user, isAdmin: true }} ready onLogout={vi.fn()}><p>Operator workspace</p></LegalAgreementGate>);
    expect(screen.getByText('Operator workspace')).toBeInTheDocument();
    expect(mocks.watch).not.toHaveBeenCalled();
  });
  test('school staff agree without being asked to confirm a student age', async () => {
    render(<LegalAgreementGate user={{ ...user, role: 'staff' }} ready onLogout={vi.fn()}><p>Staff workspace</p></LegalAgreementGate>);
    fireEvent.click(await screen.findByRole('checkbox', { name: /I have read/ }));
    expect(screen.queryByRole('checkbox', { name: /I am aged/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Agree & continue/ }));
    expect(await screen.findByText('Staff workspace')).toBeInTheDocument();
    expect(mocks.record).toHaveBeenCalledExactlyOnceWith(false);
  });
});
