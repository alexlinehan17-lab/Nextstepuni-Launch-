import React from 'react';
import type * as FirebaseAuth from 'firebase/auth';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

const { checkCode, applyCode, verifyResetCode, confirmReset } = vi.hoisted(() => ({
  checkCode: vi.fn(),
  applyCode: vi.fn(),
  verifyResetCode: vi.fn(),
  confirmReset: vi.fn(),
}));
vi.mock('firebase/auth', async importOriginal => ({
  ...(await importOriginal<typeof FirebaseAuth>()),
  checkActionCode: checkCode,
  applyActionCode: applyCode,
  verifyPasswordResetCode: verifyResetCode,
  confirmPasswordReset: confirmReset,
}));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: () => vi.fn() }));

import AuthActionPage from '../components/AuthActionPage';

let code = 0;
const visit = (query: string, path = '/reset-password') => {
  window.history.replaceState({}, '', `${path}${query.replace('CODE', `code-${++code}`)}`);
  return render(<AuthActionPage />);
};
const authError = (authCode: string) => Object.assign(new Error(authCode), { code: authCode });

beforeEach(() => {
  checkCode.mockReset();
  applyCode.mockReset();
  verifyResetCode.mockReset();
  confirmReset.mockReset();
});
afterEach(() => window.history.replaceState({}, '', '/'));

describe('AuthActionPage', () => {
  it('confirms an email from a verifyEmail link instead of offering a password reset', async () => {
    applyCode.mockResolvedValue(undefined);
    visit('?mode=verifyEmail&oobCode=CODE&apiKey=k&lang=en');
    expect(await screen.findByRole('heading', { name: 'Email confirmed' })).toBeInTheDocument();
    expect(applyCode).toHaveBeenCalledTimes(1);
    expect(screen.queryByText('Set a new password')).not.toBeInTheDocument();
    expect(verifyResetCode).not.toHaveBeenCalled();
    expect(confirmReset).not.toHaveBeenCalled();
  });

  it('explains a used confirmation link without calling it a reset link', async () => {
    applyCode.mockRejectedValue(authError('auth/invalid-action-code'));
    visit('?mode=verifyEmail&oobCode=CODE');
    expect(await screen.findByText(/confirmation link has already been used/)).toBeInTheDocument();
    expect(screen.queryByText(/reset link/i)).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Back to sign in' })).toBeInTheDocument();
  });

  it('explains an expired confirmation link', async () => {
    applyCode.mockRejectedValue(authError('auth/expired-action-code'));
    visit('?mode=verifyEmail&oobCode=CODE');
    expect(await screen.findByRole('heading', { name: 'This link has expired' })).toBeInTheDocument();
  });

  it('also handles an action link that arrives on the app root', async () => {
    applyCode.mockResolvedValue(undefined);
    visit('?mode=verifyEmail&oobCode=CODE', '/');
    expect(await screen.findByRole('heading', { name: 'Email confirmed' })).toBeInTheDocument();
  });

  it('shows the password form only for a genuine password-reset code', async () => {
    checkCode.mockResolvedValue({ operation: 'PASSWORD_RESET', data: { email: 'aoife@example.com' } });
    visit('?mode=resetPassword&oobCode=CODE');
    expect(await screen.findByRole('heading', { name: 'Set a new password' })).toBeInTheDocument();
    expect(screen.getByText('aoife@example.com')).toBeInTheDocument();
    expect(applyCode).not.toHaveBeenCalled();
  });

  it('refuses a non-reset code sent with mode=resetPassword', async () => {
    checkCode.mockResolvedValue({ operation: 'VERIFY_EMAIL', data: { email: 'aoife@example.com' } });
    visit('?mode=resetPassword&oobCode=CODE');
    expect(await screen.findByText(/isn.t a password reset link/)).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Set a new password' })).not.toBeInTheDocument();
  });

  it('treats a code-only legacy link as a password reset', async () => {
    checkCode.mockResolvedValue({ operation: 'PASSWORD_RESET', data: { email: 'aoife@example.com' } });
    visit('?oobCode=CODE');
    expect(await screen.findByRole('heading', { name: 'Set a new password' })).toBeInTheDocument();
  });

  it('restores the previous email from a recoverEmail link', async () => {
    checkCode.mockResolvedValue({ operation: 'RECOVER_EMAIL', data: { email: 'aoife@example.com' } });
    applyCode.mockResolvedValue(undefined);
    visit('?mode=recoverEmail&oobCode=CODE');
    expect(await screen.findByRole('heading', { name: 'Email address restored' })).toBeInTheDocument();
    expect(screen.getByText(/aoife@example.com again/)).toBeInTheDocument();
  });

  it('explains a link that is missing its code or uses an unsupported action', async () => {
    const first = visit('');
    expect(await screen.findByText(/missing some information/)).toBeInTheDocument();
    first.unmount();
    visit('?mode=revertSecondFactorAddition&oobCode=CODE');
    expect(await screen.findByText(/not used by NextStepUni/)).toBeInTheDocument();
    expect(applyCode).not.toHaveBeenCalled();
    expect(checkCode).not.toHaveBeenCalled();
  });

  it('applies a one-use code once even when React mounts the page twice', async () => {
    applyCode.mockResolvedValue(undefined);
    window.history.replaceState({}, '', '/reset-password?mode=verifyEmail&oobCode=strict-code');
    render(<React.StrictMode><AuthActionPage /></React.StrictMode>);
    expect(await screen.findByRole('heading', { name: 'Email confirmed' })).toBeInTheDocument();
    expect(applyCode).toHaveBeenCalledTimes(1);
  });
});
