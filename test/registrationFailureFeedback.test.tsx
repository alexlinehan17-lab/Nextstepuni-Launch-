import React from 'react';
import type * as FirebaseAuth from 'firebase/auth';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginPage from '../components/LoginPage';
import { isRegistrationProvisioning } from '../utils/registrationProvisioning';

const mocks = vi.hoisted(() => ({ create: vi.fn(), claim: vi.fn(), remove: vi.fn(), write: vi.fn() }));
vi.mock('firebase/auth', async importOriginal => ({
  ...(await importOriginal<typeof FirebaseAuth>()),
  createUserWithEmailAndPassword: mocks.create,
  updateProfile: vi.fn().mockResolvedValue(undefined),
  sendEmailVerification: vi.fn().mockResolvedValue(undefined),
  deleteUser: mocks.remove,
  signOut: vi.fn().mockResolvedValue(undefined),
}));
vi.mock('firebase/firestore', () => ({ doc: () => ({}), getDoc: vi.fn(), setDoc: mocks.write }));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: () => mocks.claim }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
vi.mock('../utils/programmeAnalytics', () => ({ trackProgrammeEvent: vi.fn() }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));
vi.mock('../components/Onboarding', () => ({ default: () => null }));

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  mocks.create.mockReset().mockResolvedValue({ user: { uid: 'local-signup-attempt' } });
  mocks.remove.mockReset().mockResolvedValue(undefined);
  mocks.write.mockReset();
  mocks.claim.mockReset();
});

async function submitRegistration(joinCode: string) {
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
  fireEvent.change(await screen.findByLabelText('Your Name'), { target: { value: 'Preview Student' } });
  fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'preview@example.com' } });
  fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
  await userEvent.click(await screen.findByLabelText('School'));
  await userEvent.click(await screen.findByRole('option', { name: /Marino/ }));
  fireEvent.change(screen.getByLabelText('School join code'), { target: { value: joinCode } });
  fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
  fireEvent.change(await screen.findByLabelText('Password', { selector: 'input' }), { target: { value: 'A memorable preview phrase' } });
  fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
  fireEvent.click(await screen.findByRole('checkbox', { name: 'I have read the Privacy Notice and agree to the Terms of Use' }));
  fireEvent.click(screen.getByRole('button', { name: 'Create my account' }));
}

describe('registration failure feedback in the real form', () => {
  it.each([
    ['bad', 'functions/invalid-argument', 'A valid join code is required.'],
    ['wrong-code', 'functions/permission-denied', 'That join code is not correct.'],
  ])('returns rejected code %s to its field and keeps the entered details', async (joinCode, code, message) => {
    mocks.claim.mockRejectedValue({ code, message });
    const success = vi.fn();
    render(<LoginPage handleLoginSuccess={success} />);
    await submitRegistration(joinCode);
    const field = await screen.findByLabelText('School join code');
    expect(field).toHaveValue(joinCode);
    expect(field).toHaveAttribute('aria-invalid', 'true');
    expect(field).toHaveAccessibleDescription(/school join code is not correct/i);
    await waitFor(() => expect(field).toHaveFocus());
    expect(screen.getByLabelText('School')).toHaveTextContent('Marino');
    expect(mocks.remove).toHaveBeenCalledExactlyOnceWith({ uid: 'local-signup-attempt' });
    expect(mocks.write).not.toHaveBeenCalled();
    expect(success).not.toHaveBeenCalled();
    expect(isRegistrationProvisioning()).toBe(false);
    fireEvent.change(field, { target: { value: 'corrected-code' } });
    expect(screen.queryByRole('alert')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByLabelText('Password', { selector: 'input' })).toHaveValue('A memorable preview phrase');
  });

  it('shows the specific reason when account cleanup unmounts the signup form', async () => {
    mocks.claim.mockRejectedValue({ code: 'functions/invalid-argument', message: 'A valid join code is required.' });
    const view = render(<LoginPage handleLoginSuccess={vi.fn()} />);
    mocks.remove.mockImplementation(async () => { view.unmount(); });
    await submitRegistration('bad');
    await waitFor(() => expect(sessionStorage.getItem('nsu:registration-error')).toBe('bad-join-code'));
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    expect(screen.getByRole('alert')).toHaveTextContent('That school join code is not correct.');
    expect(sessionStorage.getItem('nsu:registration-error')).toBeNull();
    expect(isRegistrationProvisioning()).toBe(false);
  });
});
