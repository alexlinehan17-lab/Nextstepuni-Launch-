import React from 'react';
import type * as FirebaseAuth from 'firebase/auth';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import LoginPage from '../components/LoginPage';

const { resetEmail } = vi.hoisted(() => ({ resetEmail: vi.fn() }));
vi.mock('firebase/auth', async importOriginal => ({ ...(await importOriginal<typeof FirebaseAuth>()), sendPasswordResetEmail: resetEmail }));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: () => vi.fn().mockRejectedValue(new Error('not signed in')) }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); resetEmail.mockReset(); resetEmail.mockResolvedValue(undefined); });
describe('account entry refinements', () => {
  it('uses password-manager semantics on the real sign-in form', () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    expect(screen.getByLabelText('Email')).toHaveAttribute('autocomplete', 'username');
    expect(screen.getByLabelText('Password')).toHaveAttribute('autocomplete', 'current-password');
  });
  it('join-code help preserves the registration details', async () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Register' }));
    await screen.findByLabelText('Your Name');
    fireEvent.change(screen.getByLabelText('Your Name'), { target: { value: 'Alex' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'alex@example.com' } });
    fireEvent.click(screen.getByRole('button', { name: 'Where do I find my join code?' }));
    expect(screen.getByRole('dialog')).toHaveTextContent('Ask the teacher or guidance counsellor');
    fireEvent.click(screen.getByRole('button', { name: 'Back to your details' }));
    expect(screen.getByLabelText('Your Name')).toHaveValue('Alex');
    expect(screen.getByLabelText('Email')).toHaveValue('alex@example.com');
  });
  it('allows correcting the reset email without losing it or sending twice', async () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Forgot password?' }));
    await screen.findByRole('button', { name: 'Send Reset Link' });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'wrong@example.com' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send Reset Link' }));
    await screen.findByRole('button', { name: 'Change email address' });
    expect(resetEmail).toHaveBeenCalledOnce();
    expect(screen.getByRole('button', { name: /Resend in/ })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Change email address' }));
    expect(screen.getByLabelText('Email')).toHaveValue('wrong@example.com');
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'right@example.com' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send Reset Link' }));
    await waitFor(() => expect(resetEmail).toHaveBeenCalledTimes(2));
    expect(resetEmail.mock.calls[1][1]).toBe('right@example.com');
  });
});
