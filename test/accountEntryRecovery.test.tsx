import React from 'react';
import type * as FirebaseAuth from 'firebase/auth';
import type * as FirebaseFirestore from 'firebase/firestore';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import LoginPage from '../components/LoginPage';

const { signIn } = vi.hoisted(() => ({ signIn: vi.fn() }));
vi.mock('firebase/auth', async importOriginal => ({ ...(await importOriginal<typeof FirebaseAuth>()), signInWithEmailAndPassword: signIn }));
vi.mock('firebase/firestore', async importOriginal => ({ ...(await importOriginal<typeof FirebaseFirestore>()), doc: () => ({}), getDoc: vi.fn(), setDoc: vi.fn() }));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: () => vi.fn().mockRejectedValue(new Error('not signed in')) }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
// iPads get the mobile app design, which opens straight on Sign in.
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  signIn.mockReset();
  signIn.mockRejectedValue(Object.assign(new Error('bad'), { code: 'auth/invalid-credential' }));
});

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
  const failSignIn = async (email: string) => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: email } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'not the password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password.');
  };

  it('offers registration and carries the typed email over', async () => {
    await failSignIn('new.student@example.com');
    expect(screen.getByText('No account yet?')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Create an account' }));
    expect(await screen.findByLabelText('Your Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toHaveValue('new.student@example.com');
  });

  it('does not carry a username into the email field', async () => {
    await failSignIn('aoife');
    fireEvent.click(screen.getByRole('button', { name: 'Create an account' }));
    await screen.findByLabelText('Your Name');
    expect(screen.getByLabelText('Email')).toHaveValue('');
  });

  it('withdraws the prompt as soon as the student edits their details', async () => {
    await failSignIn('new.student@example.com');
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'another try here' } });
    expect(screen.queryByText('No account yet?')).not.toBeInTheDocument();
  });
});
