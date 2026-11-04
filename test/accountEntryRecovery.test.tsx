import React from 'react';
import type * as FirebaseAuth from 'firebase/auth';
import type * as FirebaseFirestore from 'firebase/firestore';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import LoginPage from '../components/LoginPage';

const { signIn, report } = vi.hoisted(() => ({ signIn: vi.fn(), report: vi.fn() }));
vi.mock('firebase/auth', async importOriginal => ({ ...(await importOriginal<typeof FirebaseAuth>()), signInWithEmailAndPassword: signIn }));
vi.mock('firebase/firestore', async importOriginal => ({ ...(await importOriginal<typeof FirebaseFirestore>()), doc: () => ({}), getDoc: vi.fn(), setDoc: vi.fn() }));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: (_fns: unknown, name: string) => (name === 'reportSignInFailure' ? report : vi.fn().mockRejectedValue(new Error('not signed in'))) }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
// iPads get the mobile app design, which opens straight on Sign in.
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  signIn.mockReset();
  signIn.mockRejectedValue(Object.assign(new Error('bad'), { code: 'auth/invalid-credential' }));
  report.mockReset();
  report.mockResolvedValue({ data: { ok: true } });
});
const authError = (code: string) => Object.assign(new Error(code), { code });

const startRegistration = async () => {
  render(<LoginPage handleLoginSuccess={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
  await screen.findByLabelText('Your Name');
  fireEvent.change(screen.getByLabelText('Your Name'), { target: { value: 'Aoife Byrne' } });
};

describe('signup email typo suggestion', () => {
  it('pauses once on a likely typo and applies the suggested address', async () => {
    await startRegistration();
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'aoife@marinocollge.ie' } });
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByText(/Did you mean/)).toHaveTextContent('Did you mean aoife@marinocollege.ie?');
    expect(screen.queryByLabelText('School')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Use aoife@marinocollege.ie' }));
    expect(screen.getByLabelText('Email')).toHaveValue('aoife@marinocollege.ie');
    expect(screen.queryByText(/Did you mean/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByLabelText('School')).toBeInTheDocument();
  });

  it('never blocks: a second Continue keeps the address as typed', async () => {
    await startRegistration();
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'aoife@gmail.comdeedw' } });
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByText(/Did you mean/)).toHaveTextContent('aoife@gmail.com');
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByLabelText('School')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(await screen.findByLabelText('Email')).toHaveValue('aoife@gmail.comdeedw');
  });

  it('says nothing about an address that looks right', async () => {
    await startRegistration();
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'aoife@marinocollege.ie' } });
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(await screen.findByLabelText('School')).toBeInTheDocument();
    expect(screen.queryByText(/Did you mean/)).not.toBeInTheDocument();
  });
});

describe('failed sign-in', () => {
  const failSignIn = async (email: string, message = 'Invalid email or password.') => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.change(screen.getByLabelText('Email or username'), { target: { value: email } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'not the password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
    expect(await screen.findByRole('alert')).toHaveTextContent(message);
  };

  it('offers registration and carries the typed email over', async () => {
    await failSignIn('new.student@example.com');
    expect(screen.getByText('No account yet?')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Create an account' }));
    expect(await screen.findByLabelText('Your Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toHaveValue('new.student@example.com');
  });

  // Accounts made Feb–Apr 2026 signed in with a username, stored at
  // username@nextstep.app, a mailbox that does not exist (Oct 2026: returning
  // students could not get back in and could not reset).
  it('tells a username account how to get its password reset, not to start again', async () => {
    await failSignIn('aoife', 'That username and password don’t match.');
    expect(screen.getByText(/can’t get reset emails/)).toHaveTextContent('nextstepuniinfo@gmail.com');
    expect(screen.queryByText('No account yet?')).not.toBeInTheDocument();
  });

  it('withdraws the prompt as soon as the student edits their details', async () => {
    await failSignIn('new.student@example.com');
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'another try here' } });
    expect(screen.queryByText('No account yet?')).not.toBeInTheDocument();
  });
});

// Every failure used to read "Invalid email or password." At the Marino
// workshop (12 Oct 2026) 287 sign-ins failed while 60 accounts were created;
// a student locked out after a few wrong tries was told the password was
// wrong, kept trying, and kept the lock on.
describe('a failed sign-in says why', () => {
  const tryToSignIn = (email: string) => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.change(screen.getByLabelText('Email or username'), { target: { value: email } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'correct horse battery' } });
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
  };

  it('tells a locked-out student to wait, and rests the button instead of letting them extend the lock', async () => {
    // The countdown reads the clock: frozen here, so a loaded runner cannot tick it to 59s between the alert and
    // the assertion. Only Date is faked; the timers that findByRole polls with stay real.
    vi.useFakeTimers({ toFake: ['Date'] });
    vi.setSystemTime(new Date('2026-10-28T09:00:00Z'));
    try {
      signIn.mockRejectedValue(authError('auth/too-many-requests'));
      tryToSignIn('aoife@marinocollege.ie');
      expect(await screen.findByRole('alert')).toHaveTextContent('Too many tries on this account');
      expect(screen.getByRole('button', { name: /Try again in 60s/ })).toBeDisabled();
      expect(screen.queryByText('No account yet?')).not.toBeInTheDocument();
      expect(report).toHaveBeenCalledWith({ kind: 'too-many-requests', input: 'email', platform: 'web' });
      // A different email is a different account.
      fireEvent.change(screen.getByLabelText('Email or username'), { target: { value: 'other@marinocollege.ie' } });
      expect(screen.getByRole('button', { name: 'Sign in' })).toBeEnabled();
    } finally {
      vi.useRealTimers();
    }
  });

  it('blames the connection, not the password, when Firebase cannot be reached', async () => {
    signIn.mockRejectedValue(authError('auth/network-request-failed'));
    tryToSignIn('aoife@marinocollege.ie');
    expect(await screen.findByRole('alert')).toHaveTextContent('We can’t reach NextStepUni');
    expect(screen.queryByText(/Invalid email or password/)).not.toBeInTheDocument();
  });

  it('tries a username once, as its stored address, and reports only the reason', async () => {
    tryToSignIn('Aoife');
    expect(await screen.findByRole('alert')).toHaveTextContent('That username and password don’t match.');
    expect(signIn).toHaveBeenCalledOnce();
    expect(signIn.mock.calls[0][1]).toBe('aoife@nextstep.app');
    expect(report).toHaveBeenCalledWith({ kind: 'credentials', input: 'username', platform: 'web' });
    expect(JSON.stringify(report.mock.calls)).not.toMatch(/aoife|horse/i);
  });

  it('keeps the wrong-password wording for a wrong password', async () => {
    tryToSignIn('aoife@marinocollege.ie');
    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password.');
    expect(screen.getByText('No account yet?')).toBeInTheDocument();
  });
});
