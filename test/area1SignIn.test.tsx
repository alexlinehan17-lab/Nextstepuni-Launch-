/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 1, sign-in (r5-sign-in, agreed 26 Nov 2026). Sign-in is the standard
 * and does not change, with two exceptions: For schools takes the shared
 * choices for its role and has one way back (beside Sign in, to the student
 * sign-in you came from; "Student sign-in" at the top goes), and in the phone
 * app the "See the landing page" button under the card is not shown. On the
 * website it stays.
 */
import React from 'react';
import type * as CapacitorCore from '@capacitor/core';
import type * as FirebaseAuth from 'firebase/auth';
import type * as FirebaseFirestore from 'firebase/firestore';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import LoginPage from '../components/LoginPage';

const native = vi.hoisted(() => ({ on: false }));
vi.mock('@capacitor/core', async importOriginal => {
  const real = await importOriginal<typeof CapacitorCore>();
  return { ...real, Capacitor: { ...real.Capacitor, isNativePlatform: () => native.on, getPlatform: () => (native.on ? 'ios' : 'web') } };
});
vi.mock('firebase/auth', async importOriginal => ({ ...(await importOriginal<typeof FirebaseAuth>()) }));
vi.mock('firebase/firestore', async importOriginal => ({ ...(await importOriginal<typeof FirebaseFirestore>()), doc: () => ({}), getDoc: vi.fn(), setDoc: vi.fn() }));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: () => vi.fn().mockRejectedValue(new Error('not signed in')) }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => true }));

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); native.on = false; window.scrollTo = vi.fn(); });
afterEach(cleanup);

describe('the landing-page button under the card', () => {
  it('is there on the website', () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    expect(screen.getByRole('link', { name: /See the landing page|Back to the landing page/ })).toHaveAttribute('href', '/landing');
  });
  it('is not shown in the phone app, on sign-in, create account or For schools', () => {
    native.on = true;
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    expect(screen.queryByRole('link', { name: /landing page/ })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
    expect(screen.queryByRole('link', { name: /landing page/ })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'For schools' }));
    expect(screen.queryByRole('link', { name: /landing page/ })).toBeNull();
  });
});

describe('For schools', () => {
  it('chooses the role with the shared choices, marked for assistive technology', async () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'For schools' }));
    expect(await screen.findByRole('heading', { name: 'Hello, school team.' })).toBeInTheDocument();
    const group = screen.getByRole('radiogroup', { name: 'School role' });
    expect(group).toBeInTheDocument();
    const counsellor = screen.getByRole('radio', { name: 'Guidance counsellor' });
    const staff = screen.getByRole('radio', { name: 'Staff room' });
    expect(counsellor).toHaveAttribute('aria-checked', 'true');
    expect(counsellor).toHaveClass('ui-choice');
    fireEvent.click(staff);
    expect(staff).toHaveAttribute('aria-checked', 'true');
    expect(counsellor).toHaveAttribute('aria-checked', 'false');
  });

  it('has one way back: no Student sign-in at the top, and Back returns to the sign-in you came from', async () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    expect(screen.getByLabelText('Email or username')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'For schools' }));
    await screen.findByRole('radiogroup', { name: 'School role' });
    expect(screen.queryByRole('button', { name: /Student sign-in/ })).toBeNull();
    expect(screen.queryByRole('button', { name: 'For schools' })).toBeNull();
    expect(screen.getAllByRole('button', { name: 'Back' })).toHaveLength(1);
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(await screen.findByLabelText('Email or username')).toBeInTheDocument();
  });

  it('returns to create account when that is where you came from', async () => {
    render(<LoginPage handleLoginSuccess={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
    await screen.findByLabelText('Your Name');
    fireEvent.click(screen.getByRole('button', { name: 'For schools' }));
    await screen.findByRole('radiogroup', { name: 'School role' });
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(await screen.findByLabelText('Your Name')).toBeInTheDocument();
  });
});
